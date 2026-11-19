"""The state of a Jira site as the app sees it: the standing world the seed built, and the issues and labels the book made on it.

`Serving` is the site as the seed leaves it. `ScreenOnDone` is the same site after an admin put a screen with a required Resolution on
every transition into a done status, which is how a person meets a transition the app cannot finish."""

from __future__ import annotations

from datetime import date
from typing import Any, Hashable

from ostler.book import Collection, Create, Endpoint, Index, Rule, State, Transaction, Unique

from .cast import Member
from .records import BoardRecord, FieldRecord, IssueRecord, IssueTypeRecord, LabelRecord, ProjectRecord, SprintRecord, StatusRecord
from .world import BOARDS, FIELDS, ISSUE_TYPES, PROJECTS, SPRINTS, STATUSES


class Serving(State):
    projects = Collection(ProjectRecord, Unique("key"))
    types = Collection(IssueTypeRecord, Unique("key"), Index("project"))
    statuses = Collection(StatusRecord, Unique("key"), Index("project"))
    boards = Collection(BoardRecord, Unique("id"), Index("project"))
    sprints = Collection(SprintRecord, Unique("id"), Index("board"))
    fields = Collection(FieldRecord, Unique("key"), Index("project"))
    labels = Collection(LabelRecord, Unique("name"))
    issues = Collection(IssueRecord, Unique("key"), Index("project"), Index("parent"))

    def status(self, key: str) -> StatusRecord:
        return self.statuses[key]

    def category(self, issue: IssueRecord) -> str:
        return self.statuses[issue.status].category

    def board_of(self, project: str) -> BoardRecord | None:
        found = self.boards.where(project=project)
        return found[0] if found else None

    def next_stamp(self) -> int:
        return max((issue.stamp for issue in self.issues), default=0) + 1

    def next_rank(self) -> int:
        return max((issue.rank for issue in self.issues), default=0) + 1

    def rows(self) -> tuple[Any, ...]:
        return ()

    def key(self) -> Hashable:
        return (type(self).__name__, tuple(self.issues), tuple(self.labels))


class ScreenOnDone(Serving):
    """The site after an admin put a screen with a required Resolution on every transition into a done status."""


def _unauthenticated(call: Any, s: Serving, by: Any) -> bool:
    return isinstance(call, Endpoint) and (by is None or (isinstance(by, Member) and by.revoked))


UNAUTHENTICATED = Rule[Any, Serving](
    "Client must be authenticated to access this resource.", _unauthenticated, 401,
    why="Jira checks the email and API token of every request before it reads anything else, so a revoked token gets the same answer on "
        "every call; the app reads any 401 as the token having stopped working and returns to sign-in")
Serving.rules = (UNAUTHENTICATED,)
ScreenOnDone.rules = (UNAUTHENTICATED,)


def new_model(today: date) -> Serving:
    """A site holding the standing world and nothing the book made."""
    state = Serving(today)
    state.commit(Transaction(*(Create(collection, record) for collection, records in (
        (state.projects, PROJECTS), (state.types, ISSUE_TYPES), (state.statuses, STATUSES), (state.boards, BOARDS), (state.sprints, SPRINTS),
        (state.fields, FIELDS)) for record in records)))
    return state
