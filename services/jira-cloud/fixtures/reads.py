"""What a caller sends to read: the session's lists, a project's configuration, a JQL search and the board's issue lists.

A search the book sends is the app's JQL narrowed to the label the journey put on its issues, so it reads what the journey made among
everything else the site holds. A custom field travels as `cf[<name>]`, an issue type as `type[<project>:<name>]` and an issue as its fixture's
key; the surface turns each into the site's id as the call goes out."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from ostler.book import Actor, Fixture, Reference

from ..model.records import SPRINT_FIELD
from .issues import BOOK_LABEL, ROW_FIELDS, Issue, type_reference


@dataclass(eq=False)
class Workflow(Fixture):
    """The workflow of a project, which an admin changes outside the app."""

    project: str = "CASE"

    def __str__(self) -> str:
        return f"the {self.project} workflow"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Workflow]:
        yield cls("CASE")


@dataclass(eq=False)
class ProjectsPage(Fixture):
    """One page of the projects the person may browse, by name."""

    startAt: int | None = 0
    maxResults: int | None = 100
    orderBy: str | None = "name"


@dataclass(eq=False)
class Labels(Fixture):
    """One page of the site's labels, narrowed by a prefix when `query` is set."""

    query: str | None = None
    startAt: int | None = 0
    maxResults: int | None = 1000

    def __str__(self) -> str:
        return f"labels starting {self.query!r}" if self.query else "every label"


def labels(query: str | None = None) -> Labels:
    return Labels(query, None if query else 0, 50 if query else 1000)


@dataclass(eq=False)
class People(Fixture):
    """People a user picker offers. `issueKey` asks who may be assigned that issue, `project` who may be assigned a new one there, and
    neither asks for everyone on the site. The query is the standing account's name, which the surface reads from the site."""

    query: Reference = field(default_factory=lambda: Reference("people:manager"))
    maxResults: int = 50
    issueKey: str | None = None
    project: str | None = None


def assignable(issue: Issue) -> People:
    return People(issueKey=issue.key)


def assignable_in(project: str) -> People:
    return People(project=project)


def people() -> People:
    return People()


@dataclass(eq=False)
class ProjectRef(Fixture):
    projectIdOrKey: str = "CASE"

    def __str__(self) -> str:
        return self.projectIdOrKey


@dataclass(eq=False)
class CreateTypes(Fixture):
    """The issue types a person may create in a project."""

    projectIdOrKey: str = "CASE"

    def __str__(self) -> str:
        return f"the creatable types of {self.projectIdOrKey}"


@dataclass(eq=False)
class CreateFields(Fixture):
    """One page of the create screen of a type, at its largest page."""

    projectIdOrKey: str = "CASE"
    type: str = "Bug"
    startAt: int | None = 0
    maxResults: int | None = 200

    @property
    def issueTypeId(self) -> Reference:
        return type_reference(self.projectIdOrKey, self.type)

    def __str__(self) -> str:
        return f"the {self.type} create screen of {self.projectIdOrKey}"

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[CreateFields]:
        yield cls("CASE", "Bug")
        yield cls("OPS", "Bug")


def create_screen(project: str, type: str) -> CreateFields:
    return CreateFields(project, type)


@dataclass(eq=False)
class BoardsOf(Fixture):
    projectKeyOrId: str | None = "CASE"


@dataclass(eq=False)
class BoardRef(Fixture):
    """A board, by the model's name for it."""

    boardId: str = "CASE board"


@dataclass(eq=False)
class SprintsOf(Fixture):
    boardId: str = "CASE board"
    state: str | None = "active,future"


@dataclass(eq=False)
class FilterRef(Fixture):
    """The saved filter behind a board, by the model's name for it."""

    filterId: str = "Filter for CASE1 board"


def jql_list(values: Iterable[str]) -> str:
    return ", ".join(f'"{value}"' for value in values)


@dataclass(eq=False)
class Search(Fixture):
    """A JQL search, held as the parts the app builds it from. `category` is `open`, `done` or None; `parents` are epics by their
    fixtures; `label` narrows the search to the issues a journey made; `order` names the ORDER BY the app sends."""

    project: str | None = "CASE"
    types: tuple[str, ...] = ()
    category: str | None = "open"
    recent: bool = False
    parents: tuple[Issue, ...] = ()
    label: str = BOOK_LABEL
    order: str = "priority"
    wanted: tuple[str, ...] = ROW_FIELDS
    maxResults: int | None = 100
    nextPageToken: str | None = None
    jql: str | None = None
    fields: list[str] | None = None

    def __post_init__(self) -> None:
        if self.jql is None:
            self.jql = self.query()
        if self.fields is None:
            self.fields = list(self.wanted)

    def query(self) -> str:
        """The JQL the app builds from these parts. An epic's key is read when the search is built, after the step that made the epic."""
        clauses: list[str] = []
        if self.project is not None:
            clauses.append(f"project = {self.project}")
        if self.types:
            clauses.append("issuetype in (" + ", ".join(f"type[{self.project}:{name}]" for name in self.types) + ")")
        if self.category == "open":
            clauses.append("statusCategory != Done")
        elif self.category == "done":
            clauses.append("statusCategory = Done")
        if self.recent:
            clauses.append("updated >= -30d")
        if len(self.parents) == 1:
            clauses.append(f"parent = {self.parents[0].key}")
        elif self.parents:
            clauses.append("parent in (" + ", ".join(str(parent.key) for parent in self.parents) + ")")
        clauses.append(f"labels = {self.label}")
        orders = {"priority": "priority DESC, updated DESC", "updated": "updated DESC", "status": "status ASC"}
        return " AND ".join(clauses) + " ORDER BY " + orders[self.order]

    def __str__(self) -> str:
        return self.jql or ""

    @classmethod
    def examples(cls, state: Any, by: Actor | None) -> Iterable[Search]:
        yield open_issues("CASE")


def open_issues(project: str, label: str = BOOK_LABEL) -> Search:
    """The Issues view's first search: the open issues of the standard types."""
    return Search(project, ("Bug", "Story", "Task"), "open", label=label)


def done_issues(project: str, label: str = BOOK_LABEL) -> Search:
    """Show done issues: the same search over the done issues of the last 30 days."""
    return Search(project, ("Bug", "Story", "Task"), "done", recent=True, label=label)


def epics(project: str, label: str = BOOK_LABEL, open_only: bool = False) -> Search:
    """The epic list: every epic for the chips and the picker, or only the open ones for the Epics view."""
    return Search(project, ("Epic",), "open" if open_only else None, label=label, order="updated",
                  wanted=ROW_FIELDS if open_only else ("summary", "status"))


def progress_of(*parents: Issue, label: str = BOOK_LABEL) -> Search:
    """The children of the visible epics, with their status only, for the progress bars."""
    return Search(None, (), None, parents=tuple(parents), label=label, order="updated", wanted=("status",))


def children_of(parent: Issue, label: str = BOOK_LABEL) -> Search:
    """The Child issues section of an epic."""
    return Search(None, (), None, parents=(parent,), label=label, order="status")


@dataclass(eq=False)
class SprintList(Fixture):
    """The issues of one sprint, in rank order."""

    sprintId: str = "Sprint 14"
    jql: str | None = None
    fields: str | None = ",".join((*ROW_FIELDS, SPRINT_FIELD))
    maxResults: int | None = 100

    def __str__(self) -> str:
        return f"the issues of {self.sprintId} ({self.jql})"


def sprint_issues(sprint: str, label: str = BOOK_LABEL) -> SprintList:
    return SprintList(sprint, f"labels = {label}")


@dataclass(eq=False)
class BoardList(Fixture):
    """The issues of a board outside its backlog, or of its backlog, in rank order."""

    boardId: str = "CASE board"
    jql: str | None = None
    fields: str | None = ",".join((*ROW_FIELDS, SPRINT_FIELD))
    maxResults: int | None = 100

    def __str__(self) -> str:
        return f"the issues of {self.boardId} ({self.jql})"


def board_issues(board: str, statuses: tuple[str, ...], label: str = BOOK_LABEL) -> BoardList:
    return BoardList(board, f"status in ({jql_list(statuses)}) AND labels = {label}")


def backlog_of(board: str, label: str = BOOK_LABEL) -> BoardList:
    return BoardList(board, f"labels = {label}")
