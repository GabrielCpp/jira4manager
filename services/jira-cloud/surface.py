"""Jira as a surface: every step is one REST call sent with HTTP Basic.

Two sites number the same standing record apart, so the book names a standing record by what a person reads: a project by its key, a
board and a sprint by name, a custom field as `cf[<name>]`, an issue type as `type[<project>:<name>]`. At each restore the surface reads
the site with the app's own calls (myself, the boards, their configuration and sprints, the create metadata) and learns each real id under
the model's name. As a call goes out, the client turns every name in its body, path and query into the site's id; as an answer comes back,
it turns each custom field id back into its name. An issue the book made goes out as the key Jira gave it. It deletes nothing an earlier
cell made, so every list it reads holds other people's issues too, which the keys it never learned leave out."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from ostler.book import Arrange, Client, Done, Environment, HttpSurface, Outcome, Reference
from ostler.book.errors import Unhealthy

from .endpoints.common import BASIC
from .endpoints.board import ScreenComesOffDone, ScreenGoesOnDone
from .model.cast import MANAGER, REVOKED
from .model.records import AccountRecord, BoardRecord, FieldRecord, FilterRecord, IssueRecord, LabelRecord, ProjectRecord, SprintRecord
from .model.world import BOARDS, FIELDS, PROJECTS, SCREENS, TYPES

TOKEN = re.compile(r"cf\[[^\]]+\]|type\[[A-Z0-9]+:[A-Za-z ]+\]")
LABEL_NAME = re.compile(r"\bj4m-[a-z0-9-]+?(?=$|[\s\"',)&]|%20|\+)")
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
CUSTOM = re.compile(r"customfield_\d+")
TRANSITION_ID = re.compile(r"Transition id '(\d+)'")


def jira_message(body: object) -> str:
    """The refusal Jira gives: the first of errorMessages, else `<field id>: <message>` for the first field error, else the text."""
    if not isinstance(body, dict):
        return str(body).strip()
    messages = body.get("errorMessages") or []
    if messages:
        return str(messages[0])
    errors = body.get("errors") or {}
    for field, message in errors.items():
        return f"{field}: {message}"
    return str(body.get("message", ""))


class JiraClient(Client):
    """The runtime's client, with the names the book writes turned into the site's ids on the way out and back on the way in."""

    def __init__(self, base: str):
        super().__init__(base, message_of=self.message)
        self.tokens: dict[str, str] = {}
        self.names: dict[str, str] = {}
        self.transitions: dict[tuple[str, str], str] = {}
        
    def message(self, body: object) -> str:
        text = jira_message(body)
        text = CUSTOM.sub(lambda found: self.names.get(found[0], found[0]), text)
        return TRANSITION_ID.sub(lambda found: f"Transition id '{self.transition_name(found[1])}'", text)

    def transition_name(self, real: str) -> str:
        return next((f"to {status}" for (project, status), known in self.transitions.items() if known == real), real)

    def outgoing(self, text: str) -> str:
        text = TOKEN.sub(lambda found: self.tokens.get(found[0], found[0]), text)
        text = UUID.sub(lambda found: self.ids.real(IssueRecord, found[0]) or found[0], text)
        return LABEL_NAME.sub(lambda found: self.ids.minted(LabelRecord, found[0]), text)

    def incoming(self, raw: bytes) -> bytes:
        if not raw or not self.names:
            return raw
        text = raw.decode("utf-8", "replace")
        return CUSTOM.sub(lambda found: self.names.get(found[0], found[0]), text).encode()

    def transport(self, method: str, url: str, headers: dict[str, str], data: bytes | None) -> tuple[int, bytes]:
        parts = urllib.parse.urlsplit(url)
        path = urllib.parse.quote(self.outgoing(urllib.parse.unquote(parts.path)), safe="/")
        query = urllib.parse.urlencode([(k, self.outgoing(v)) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)])
        url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, query, ""))
        if data:
            data = self.outgoing(data.decode()).encode()
        headers = {**headers, "Accept": "application/json"}
        status, raw = self.raw(method, url, headers, data)
        return status, self.incoming(raw)

    def raw(self, method: str, url: str, headers: dict[str, str], data: bytes | None) -> tuple[int, bytes]:
        request = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as reply:
                return reply.status, reply.read()
        except urllib.error.HTTPError as reply:
            return reply.code, reply.read()
        except (urllib.error.URLError, OSError) as down:
            raise Unhealthy(f"{method} {url} did not answer: {getattr(down, 'reason', down)}") from None

    def get(self, path: str) -> Any:
        credential = self.held[(MANAGER, BASIC)]
        name, value = BASIC.header(str(credential))
        status, raw = self.raw("GET", self.base + path, {name: value, "Accept": "application/json"}, None)
        if status != 200:
            raise Unhealthy(f"GET {path} answered {status}: {raw[:200]!r}")
        return json.loads(raw)

    def resolve(self, reference: Reference) -> Any:
        kind, _, rest = reference.name.partition(":")
        if kind == "transition":
            key, _, status = rest.partition(":")
            return self.transition_id(key, status)
        return super().resolve(reference)

    def transition_id(self, key: str, status: str) -> str:
        """The id of the transition into `status` that the issue offers now, else the id the project's workflow gave it when an earlier
        read offered it, so a forbidden transition is still sent and refused."""
        real = self.ids.real(IssueRecord, key) or key
        project = real.rsplit("-", 1)[0]
        offered = self.get(f"/rest/api/3/issue/{urllib.parse.quote(real)}/transitions")
        for transition in offered.get("transitions", []):
            self.transitions[(project, transition["to"]["name"])] = str(transition["id"])
        return self.transitions.get((project, status), "0")


class JiraSurface(HttpSurface):
    def __init__(self, environment: Environment):
        self.back = environment.backstage(environment)
        super().__init__(JiraClient(self.back.address("jira")))

    def start(self) -> None:
        self.restore()

    def reset(self) -> None:
        self.restore()

    def restore(self) -> None:
        client: JiraClient = self.client  # type: ignore[assignment]
        client.forget()
        client.hold(MANAGER, BASIC, self.back.credential())
        client.hold(REVOKED, BASIC, self.back.revoked())
        me = client.get("/rest/api/3/myself")
        client.ids.learn(AccountRecord, MANAGER.handle, me["accountId"])
        client.know("people:manager", me.get("displayName", ""))
        for project in PROJECTS:
            client.ids.learn(ProjectRecord, project.key, project.key)
            self.learn_types_and_fields(client, project.key)
        for board in BOARDS:
            self.learn_board(client, board)

    def learn_types_and_fields(self, client: JiraClient, project: str) -> None:
        types = client.get(f"/rest/api/3/issue/createmeta/{project}/issuetypes").get("issueTypes", [])
        for name in TYPES:
            found = next((t for t in types if t.get("name") == name), None)
            if found is None or f"{project}:{name}" not in SCREENS:
                continue
            client.tokens[f"type[{project}:{name}]"] = str(found["id"])
            client.know(f"issuetype:{project}:{name}", str(found["id"]))
            screen = client.get(f"/rest/api/3/issue/createmeta/{project}/issuetypes/{found['id']}?startAt=0&maxResults=200").get("fields", [])
            for field in screen:
                token = f"cf[{field.get('name')}]"
                if str(field.get("fieldId", "")).startswith("customfield_") and any(f.id == token for f in FIELDS):
                    client.tokens[token] = field["fieldId"]
                    client.names[field["fieldId"]] = token
        for field in FIELDS:
            if field.project == project:
                client.ids.learn(FieldRecord, field.id, field.id)

    def learn_board(self, client: JiraClient, board: BoardRecord) -> None:
        listed = client.get(f"/rest/agile/1.0/board?projectKeyOrId={board.project}").get("values", [])
        found = next((b for b in listed if b.get("name") == board.name), None)
        if found is None:
            raise Unhealthy(f"the site has no board named {board.name}: run the seed")
        client.ids.learn(BoardRecord, board.id, str(found["id"]))
        configuration = client.get(f"/rest/agile/1.0/board/{found['id']}/configuration")
        client.ids.learn(FilterRecord, board.filter, str(configuration["filter"]["id"]))
        if board.type == "scrum":
            sprints = client.get(f"/rest/agile/1.0/board/{found['id']}/sprint?state=active,future").get("values", [])
            for sprint in sprints:
                client.ids.learn(SprintRecord, str(sprint["name"]), str(sprint["id"]))

    def perform(self, step: Any) -> Outcome:
        if isinstance(step, Arrange):
            if isinstance(step, ScreenGoesOnDone):
                self.back.put_screen_on_done()
            elif isinstance(step, ScreenComesOffDone):
                self.back.take_screen_off_done()
            return Done(self.rows(), ())
        return super().perform(step)

    def express(self, request: Any, outcome: Done) -> tuple[object, ...]:
        if isinstance(request, Arrange):
            return ()
        return super().express(request, outcome)
