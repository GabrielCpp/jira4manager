"""What every call to Jira shares: HTTP Basic with the email and the API token, and the answers a refused credential or a missing record
gives."""

from __future__ import annotations

import base64
from dataclasses import dataclass

from ostler.book import Answer, Refusal, Refusals

from .shapes import ERRORS, NOT_SIGNED_IN


@dataclass(frozen=True)
class Basic:
    """`Authorization: Basic <base64 of email:token>`, the scheme an unscoped API token uses against the site URL."""

    def describe(self) -> str:
        return "HTTP Basic with an email and an API token"

    def header(self, credential: str) -> tuple[str, str]:
        return "Authorization", "Basic " + base64.b64encode(credential.encode()).decode()


BASIC = Basic()
AUTH = (BASIC,)

NOT_SIGNED = Answer(401, NOT_SIGNED_IN, "the email and token are missing, or Jira no longer accepts the token",
                    why="Jira answers before it reads the request, with a line of text and no error collection")
REFUSED = Answer(400, ERRORS, "Jira refuses the request: errors keyed by field id, or a message under errorMessages")
NO_ISSUE = Answer(404, ERRORS, "no issue has that key, or the caller may not browse it")
NO_PROJECT = Answer(404, ERRORS, "no project has that key, or the caller may not browse it")
NO_BOARD = Answer(404, ERRORS, "no board has that id, or the caller may not see it")
NO_SPRINT = Answer(404, ERRORS, "no sprint has that id")

PAYLOAD = "Invalid request payload. Refer to the REST API documentation and try again."
UNBOUNDED = "Unbounded JQL queries are not allowed here. Please add a search restriction to your query."
SERVICE_REFUSALS = Refusals(
    unknown_id=Refusal("Issue does not exist or you do not have permission to see it.", 404),
    wrong_kind=Refusal("Issue does not exist or you do not have permission to see it.", 404),
    malformed=Refusal(PAYLOAD, 400),
    wrong_type=Refusal(PAYLOAD, 400),
    missing=Refusal(PAYLOAD, 400),
)
ISSUE_REFUSALS = Refusals(unknown_id=Refusal("Issue does not exist or you do not have permission to see it.", 404),
                          wrong_kind=Refusal("Issue does not exist or you do not have permission to see it.", 404))
BOARD_REFUSALS = Refusals(unknown_id=Refusal("Board does not exist or you do not have permission to see it.", 404),
                          wrong_kind=Refusal("Board does not exist or you do not have permission to see it.", 404))
