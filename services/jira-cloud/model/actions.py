"""What Jira does with each call the app makes. Each action says what it accepts, the rules it checks in the order Jira checks them, and
what it reduces to: a transaction for a write, a show for a read. The caller is `by`."""

from __future__ import annotations

import re
from dataclasses import replace
from typing import Any, Callable, ClassVar
from uuid import uuid4

from ostler.book import Action, Actor, Become, Create, Show, Transaction, Update

from ..fixtures.issues import Editing, Issue, Moving, Opening, Transitioning, TransitionsOf
from ..fixtures.reads import (BoardList, BoardRef, BoardsOf, CreateFields, CreateTypes, FilterRef, Labels, People, ProjectRef, ProjectsPage,
                              Search, SprintList, SprintsOf, Workflow)
from . import rules
from .records import PRIORITIES, PRIORITY_IDS, IssueRecord, LabelRecord
from .state import ScreenOnDone, Serving
from .views import View, issue_row, priority_rank, sprint_view, status_view, user_view, wanted_fields, workflow_place
from .world import INITIAL, WORKFLOWS

LABEL = re.compile(r"labels = (\S+)")
STATUSES_IN = re.compile(r"status in \(([^)]*)\)")


class ReadMyself(Action[Any, Serving]):
    @staticmethod
    def reduce(a: Any, s: Serving, by: Actor | None) -> Show:
        return Show(View(accountId="manager", active=True, accountType="atlassian"))


class ListProjects(Action[ProjectsPage, Serving]):
    accept = ProjectsPage

    @staticmethod
    def reduce(a: ProjectsPage, s: Serving, by: Actor | None) -> Show:
        rows = tuple(View(key=p.key, name=p.name, style=p.style, simplified=p.simplified, projectTypeKey="software")
                     for p in sorted(s.projects, key=lambda p: p.name.lower()))
        return Show(View(values=rows, startAt=a.startAt or 0, maxResults=a.maxResults or 50))


class ListLabels(Action[Labels, Serving]):
    accept = Labels

    @staticmethod
    def reduce(a: Labels, s: Serving, by: Actor | None) -> Show:
        prefix = (a.query or "").lower()
        names = tuple(sorted(label.name for label in s.labels if label.name.lower().startswith(prefix)))
        return Show(View(values=names, maxResults=a.maxResults or 1000))


class ReadProjectStatuses(Action[ProjectRef, Serving]):
    accept = ProjectRef
    rules = (rules.project_missing,)

    @staticmethod
    def reduce(a: ProjectRef, s: Serving, by: Actor | None) -> Show:
        project = a.projectIdOrKey
        statuses = tuple(status_view(s, f"{project}:{name}") for name, _ in WORKFLOWS[project])
        return Show(*(View(name=t.name, subtask=t.subtask, statuses=statuses) for t in s.types.where(project=project)))


class ListCreatableTypes(Action[CreateTypes, Serving]):
    accept = CreateTypes
    rules = (rules.project_missing,)

    @staticmethod
    def reduce(a: CreateTypes, s: Serving, by: Actor | None) -> Show:
        types = tuple(View(name=t.name, hierarchyLevel=t.hierarchyLevel, subtask=t.subtask) for t in s.types.where(project=a.projectIdOrKey))
        return Show(View(issueTypes=types, startAt=0, maxResults=50))


class ReadCreateFields(Action[CreateFields, Serving]):
    accept = CreateFields
    rules = (rules.page_too_large, rules.project_missing)

    @staticmethod
    def reduce(a: CreateFields, s: Serving, by: Actor | None) -> Show:
        held = [f for f in s.fields.where(project=a.projectIdOrKey) if a.type in f.screens]
        rows = tuple(View(fieldId=f.id, name=f.name, required=a.type in f.required, operations=f.operations,
                          schema=View(type=f.type, items=f.items, system=f.system, custom=f.custom)) for f in held)
        start, size = a.startAt or 0, a.maxResults or 50
        return Show(View(fields=rows[start:start + size], startAt=start, maxResults=size))


class ListProjectBoards(Action[BoardsOf, Serving]):
    accept = BoardsOf

    @staticmethod
    def reduce(a: BoardsOf, s: Serving, by: Actor | None) -> Show:
        boards = tuple(View(id=b.id, name=b.name, type=b.type) for b in s.boards if a.projectKeyOrId in (None, b.project))
        return Show(View(values=boards, startAt=0, maxResults=50))


class ReadBoardConfiguration(Action[BoardRef, Serving]):
    accept = BoardRef
    rules = (rules.board_missing,)

    @staticmethod
    def reduce(a: BoardRef, s: Serving, by: Actor | None) -> Show:
        board = s.boards[a.boardId]
        columns = tuple(View(name=c.name, statuses=tuple(View(name=name) for name in c.statuses)) for c in board.columns)
        return Show(View(id=board.id, name=board.name, type=board.type, filter=View(id=board.filter), columnConfig=View(columns=columns)))


class ListBoardSprints(Action[SprintsOf, Serving]):
    accept = SprintsOf
    rules = (rules.board_missing, rules.no_sprints)

    @staticmethod
    def reduce(a: SprintsOf, s: Serving, by: Actor | None) -> Show:
        states = set(a.state.split(",")) if a.state else {"active", "future", "closed"}
        sprints = tuple(replace_origin(sprint_view(s, sprint.id)) for sprint in s.sprints.where(board=a.boardId) if sprint.state in states)
        return Show(View(values=sprints, startAt=0, maxResults=50))


def replace_origin(view: View) -> View:
    members = dict(view._members)
    members["originBoardId"] = members.pop("boardId")
    return View(**members)


filter_missing = rules.Rule[Any, Serving]("The selected filter is not available to you, perhaps it has been deleted or had its permissions changed.",
                                          lambda a, s, by: not any(b.filter == a.filterId for b in s.boards), 400)


class ReadFilter(Action[FilterRef, Serving]):
    accept = FilterRef
    rules = (filter_missing,)

    @staticmethod
    def reduce(a: FilterRef, s: Serving, by: Actor | None) -> Show:
        board = next(b for b in s.boards if b.filter == a.filterId)
        return Show(View(id=board.filter, name=board.filter, jql=board.filter_jql))


def matches(s: Serving, record: IssueRecord, q: Search) -> bool:
    if q.project is not None and record.project != q.project:
        return False
    if q.types and record.type.split(":")[1] not in q.types:
        return False
    done = s.category(record) == "done"
    if q.category == "open" and done or q.category == "done" and not done:
        return False
    if q.parents and record.parent not in {parent.key for parent in q.parents}:
        return False
    return q.label in record.labels


def search_order(s: Serving, q: Search):
    if q.order == "priority":
        return lambda r: (priority_rank(r), -r.stamp)
    if q.order == "status":
        return lambda r: (workflow_place(s, r), r.rank)
    return lambda r: -r.stamp


page_token_unknown = rules.Rule[Any, Serving]("The provided next page token is invalid or expired.", lambda a, s, by: bool(a.nextPageToken), 400,
                                              why="a token comes only from the page before it, and the book never pages past one page")


class SearchIssues(Action[Search, Serving]):
    accept = Search
    rules = (page_token_unknown,)

    @staticmethod
    def reduce(a: Search, s: Serving, by: Actor | None) -> Show:
        found = sorted((r for r in s.issues if matches(s, r, a)), key=search_order(s, a))
        size = a.maxResults or 50
        return Show(View(issues=tuple(issue_row(s, r, a.fields or ()) for r in found[:size]), isLast=len(found) <= size))


class ReadIssue(Action[Opening, Serving]):
    accept = Opening
    rules = (rules.issue_missing,)

    @staticmethod
    def reduce(a: Opening, s: Serving, by: Actor | None) -> Show:
        record = s.issues[a.key]
        row = issue_row(s, record, wanted_fields(s, record, a.fields or "*all"))
        return Show(row)


def offered(s: Serving, record: IssueRecord) -> tuple[str, ...]:
    current = s.statuses[record.status].name
    from .world import NO_TRANSITION

    return tuple(name for name, _ in WORKFLOWS[record.project] if name != current and (current, name) not in NO_TRANSITION[record.project])


class ListTransitions(Action[TransitionsOf, Serving]):
    accept = TransitionsOf
    rules = (rules.issue_missing,)

    @staticmethod
    def reduce(a: TransitionsOf, s: Serving, by: Actor | None) -> Show:
        record = s.issues[a.key]
        screened = isinstance(s, ScreenOnDone)
        rows = tuple(View(name=name, to=status_view(s, f"{record.project}:{name}"), isAvailable=True,
                          hasScreen=screened and s.statuses[f"{record.project}:{name}"].category == "done")
                     for name in offered(s, record))
        return Show(View(transitions=rows))


assignable_issue_missing = rules.Rule[Any, Serving](rules.NO_ISSUE, lambda a, s, by: a.issueKey is not None and a.issueKey not in s.issues, 404)


class FindAssignable(Action[People, Serving]):
    accept = People
    rules = (assignable_issue_missing,)

    @staticmethod
    def reduce(a: People, s: Serving, by: Actor | None) -> Show:
        return Show(user_view("manager"))


class FindPeople(Action[People, Serving]):
    accept = People

    @staticmethod
    def reduce(a: People, s: Serving, by: Actor | None) -> Show:
        return Show(user_view("manager"))


def new_labels(s: Serving, names: tuple[str, ...]) -> list[Create]:
    made: list[Create] = []
    seen: set[str] = set()
    for name in names:
        if name not in s.labels and name not in seen:
            made.append(Create(s.labels, LabelRecord(name)))
            seen.add(name)
    return made


def custom_values(sent: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
    kept = {k: v for k, v in sent.items() if k.startswith("cf[") or k in ("components", "fixVersions", "duedate", "environment")}
    return tuple(sorted(kept.items()))


class CreateIssue(Action[Issue, Serving]):
    accept = Issue
    rules = (rules.summary_missing, rules.off_create_screen, rules.required_missing)

    @staticmethod
    def reduce(a: Issue, s: Serving, by: Actor | None) -> Transaction:
        a.set(key=str(uuid4()))
        sent = a.fields
        record = IssueRecord(
            key=a.key or "", project=a.project, type=f"{a.project}:{a.type}", summary=a.summary or "", status=f"{a.project}:{INITIAL[a.project]}",
            priority=a.priority or "Medium", assignee=a.assignee, parent=a.parent.key if a.parent is not None else None, labels=tuple(a.labels),
            sprint=None, rank=s.next_rank(), stamp=s.next_stamp(), description=sent.get("description"), values=custom_values(sent))
        return Transaction(*new_labels(s, tuple(a.labels)), Create(s.issues, record))


def edited(s: Serving, record: IssueRecord, a: Editing) -> IssueRecord:
    sent = a.edit.fields or {}
    changes: dict[str, Any] = {"stamp": s.next_stamp()}
    values = dict(record.values)
    for name, value in sent.items():
        if name == "summary":
            changes["summary"] = value
        elif name == "description":
            changes["description"] = value
        elif name == "priority":
            changes["priority"] = next(p for p in PRIORITIES if PRIORITY_IDS[p] == value["id"])
        elif name == "assignee":
            changes["assignee"] = value["accountId"] if value else None
        elif name == "parent":
            changes["parent"] = value["key"] if value else None
        elif value is None:
            values.pop(name, None)
        else:
            values[name] = value
    labels = list(record.labels)
    for name, operations in (a.edit.update or {}).items():
        for operation in operations:
            if name == "labels" and "add" in operation and operation["add"] not in labels:
                labels.append(operation["add"])
            elif name == "labels" and "remove" in operation and operation["remove"] in labels:
                labels.remove(operation["remove"])
            elif name == "parent" and operation.get("set", {}).get("none"):
                changes["parent"] = None
    changes["labels"] = tuple(labels)
    changes["values"] = tuple(sorted(values.items()))
    return replace(record, **changes)


class EditIssue(Action[Editing, Serving]):
    accept = Editing
    rules = (rules.issue_missing, rules.off_edit_screen)

    @staticmethod
    def reduce(a: Editing, s: Serving, by: Actor | None) -> Transaction:
        record = edited(s, s.issues[a.key], a)
        return Transaction(*new_labels(s, record.labels), Update(s.issues, record.key, record))


class TransitionIssue(Action[Transitioning, Serving]):
    accept = Transitioning
    rules = (rules.issue_missing, rules.transition_forbidden, rules.transition_needs_screen)

    @staticmethod
    def reduce(a: Transitioning, s: Serving, by: Actor | None) -> Transaction:
        record = s.issues[a.key]
        moved = replace(record, status=f"{record.project}:{a.to}", stamp=s.next_stamp())
        return Transaction(Update(s.issues, record.key, moved))


def moved(s: Serving, a: Moving) -> Transaction:
    changes = []
    for key in dict.fromkeys(a.issues):
        record = s.issues[key]
        changes.append(Update(s.issues, key, replace(record, sprint=a.sprintId, stamp=s.next_stamp() + len(changes))))
    return Transaction(*changes)


class MoveToSprint(Action[Moving, Serving]):
    accept = Moving
    rules = (rules.too_many_moved, rules.sprint_missing, rules.moved_missing)

    @staticmethod
    def reduce(a: Moving, s: Serving, by: Actor | None) -> Transaction:
        return moved(s, a)


class MoveToBacklog(Action[Moving, Serving]):
    accept = Moving
    rules = (rules.too_many_moved, rules.moved_missing)

    @staticmethod
    def reduce(a: Moving, s: Serving, by: Actor | None) -> Transaction:
        return moved(s, a)


def narrowed(q: str | None, record: IssueRecord, s: Serving) -> bool:
    text = q or ""
    label = LABEL.search(text)
    if label and label.group(1) not in record.labels:
        return False
    statuses = STATUSES_IN.search(text)
    if statuses:
        names = {name.strip().strip('"') for name in statuses.group(1).split(",")}
        if s.statuses[record.status].name not in names:
            return False
    return True


def board_rows(s: Serving, found: list[IssueRecord], a: Any) -> Show:
    ranked = sorted(found, key=lambda r: r.rank)
    size = a.maxResults or 50
    return Show(View(issues=tuple(issue_row(s, r, wanted_fields(s, r, a.fields or "*all")) for r in ranked[:size]), isLast=len(ranked) <= size))


sprint_issues_missing = rules.Rule[Any, Serving]("Sprint with id {sprintId} does not exist.", lambda a, s, by: a.sprintId not in s.sprints, 404)


class ListSprintIssues(Action[SprintList, Serving]):
    accept = SprintList
    rules = (sprint_issues_missing,)

    @staticmethod
    def reduce(a: SprintList, s: Serving, by: Actor | None) -> Show:
        return board_rows(s, [r for r in s.issues if r.sprint == a.sprintId and narrowed(a.jql, r, s)], a)


def on_board(s: Serving, board: Any, record: IssueRecord) -> bool:
    """The issue is a card of the board: in one of its board columns, and on a scrum board in the active sprint."""
    if record.project != board.project or s.statuses[record.status].name not in board.board_statuses:
        return False
    return board.type == "kanban" or record.sprint is not None and s.sprints[record.sprint].state == "active"


def in_backlog(s: Serving, board: Any, record: IssueRecord) -> bool:
    """The issue is in the board's backlog: on a kanban board in its backlog column, on a scrum board open and in no sprint."""
    if record.project != board.project:
        return False
    if board.type == "kanban":
        return s.statuses[record.status].name in board.backlog_statuses
    done_column = board.columns[-1].statuses
    return record.sprint is None and s.statuses[record.status].name not in done_column


class BoardListing(Action[BoardList, Serving]):
    """A board's issue list in rank order: the issues `holds` keeps, narrowed by the list's JQL."""

    accept = BoardList
    rules = (rules.board_missing,)
    holds: ClassVar[Callable[[Serving, Any, IssueRecord], bool]]

    @classmethod
    def reduce(cls, a: BoardList, s: Serving, by: Actor | None) -> Show:
        board = s.boards[a.boardId]
        return board_rows(s, [r for r in s.issues if cls.holds(s, board, r) and narrowed(a.jql, r, s)], a)


class ListBoardIssues(BoardListing):
    holds = staticmethod(on_board)


class ListBoardBacklog(BoardListing):
    holds = staticmethod(in_backlog)


class PutScreenOnDone(Action[Workflow, Serving]):
    accept = Workflow

    @staticmethod
    def reduce(a: Any, s: Serving, by: Actor | None) -> Transaction:
        return Transaction(Become(ScreenOnDone))


class TakeScreenOffDone(Action[Workflow, Serving]):
    accept = Workflow

    @staticmethod
    def reduce(a: Any, s: Serving, by: Actor | None) -> Transaction:
        return Transaction(Become(Serving))

