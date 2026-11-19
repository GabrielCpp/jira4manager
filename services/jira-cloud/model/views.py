"""What the model says a read answers, in the names Jira's JSON uses. A view carries the fields the book compares; a field the shape marks
opaque, such as a time or an id the site numbers, is left to the app."""

from __future__ import annotations

from typing import Any, Iterable

from .records import PRIORITIES, PRIORITY_IDS, FieldRecord, IssueRecord
from .state import Serving
from .world import SPRINT_GOALS, WORKFLOWS


class View:
    """A JSON object as the model sees it: each attribute is one member."""

    def __init__(self, **members: Any):
        object.__setattr__(self, "_members", members)

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__dict__["_members"][name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("a view is read-only")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, View) and self._members == other._members

    def __hash__(self) -> int:
        return hash(tuple(sorted((k, repr(v)) for k, v in self._members.items())))

    def __repr__(self) -> str:
        return "View(" + ", ".join(f"{k}={v!r}" for k, v in self._members.items()) + ")"


def status_view(s: Serving, key: str) -> View:
    record = s.statuses[key]
    return View(id=record.key, name=record.name, statusCategory=View(key=record.category))


def type_view(s: Serving, key: str) -> View:
    record = s.types[key]
    return View(id=record.key, name=record.name, hierarchyLevel=record.hierarchyLevel, subtask=record.subtask)


def user_view(account: str) -> View:
    return View(accountId=account, active=True, displayName=account)


def priority_view(name: str) -> View:
    return View(id=PRIORITY_IDS[name], name=name)


def sprint_view(s: Serving, name: str) -> View:
    sprint = s.sprints[name]
    return View(id=sprint.id, name=sprint.name, state=sprint.state, boardId=sprint.board, goal=SPRINT_GOALS.get(sprint.name) or None)


def value_view(record: FieldRecord | None, value: Any) -> Any:
    """A custom field's value as Jira reads it back: an option as `{value}`, a user as `{accountId}`, a number as itself."""
    if value is None or record is None:
        return value
    if record.type == "user":
        return user_view(value["accountId"])
    if record.type == "option":
        return View(value=value["value"])
    if record.type == "array" and record.items == "option":
        return tuple(View(value=item["value"]) for item in value)
    return value


def field_of(s: Serving, project: str, field_id: str) -> FieldRecord | None:
    return s.fields.get(f"{project}:{field_id}")


def wanted_fields(s: Serving, record: IssueRecord, asked: str) -> tuple[str, ...]:
    names = tuple(name.strip() for name in asked.split(",") if name.strip())
    if "*all" in names:
        type_name = record.type.split(":")[1]
        held = tuple(f.id for f in s.fields.where(project=record.project) if type_name in f.screens)
        return (*held, "status", "updated", "created", "reporter", "creator")
    return names


def issue_fields(s: Serving, record: IssueRecord, asked: tuple[str, ...]) -> View:
    out: dict[str, Any] = {}
    for name in asked:
        if name == "summary":
            out[name] = record.summary
        elif name == "status":
            out[name] = status_view(s, record.status)
        elif name == "issuetype":
            out[name] = type_view(s, record.type)
        elif name == "priority":
            out[name] = priority_view(record.priority)
        elif name == "assignee":
            out[name] = user_view(record.assignee) if record.assignee else None
        elif name == "parent":
            if record.parent is not None and record.parent in s.issues:
                parent = s.issues[record.parent]
                out[name] = View(key=parent.key, fields=View(summary=parent.summary, status=status_view(s, parent.status),
                                                             issuetype=type_view(s, parent.type)))
        elif name == "labels":
            out[name] = tuple(record.labels)
        elif name == "updated":
            out[name] = str(record.stamp)
        elif name == "description":
            out[name] = record.description
        elif name == "project":
            out[name] = View(key=record.project, name=s.projects[record.project].name)
        elif name in ("created", "reporter", "creator", "issuetype"):
            continue
        elif name.startswith("cf[") or name in ("components", "fixVersions", "duedate", "environment"):
            if name == "cf[Sprint]":
                out[name] = (sprint_view(s, record.sprint),) if record.sprint else None
            else:
                out[name] = value_view(field_of(s, record.project, name), record.value(name))
    return View(**out)


def issue_row(s: Serving, record: IssueRecord, asked: Iterable[str]) -> View:
    return View(key=record.key, fields=issue_fields(s, record, tuple(asked)))


def priority_rank(record: IssueRecord) -> int:
    return PRIORITIES.index(record.priority)


def workflow_place(s: Serving, record: IssueRecord) -> int:
    names = [name for name, _ in WORKFLOWS[record.project]]
    return names.index(s.statuses[record.status].name)

