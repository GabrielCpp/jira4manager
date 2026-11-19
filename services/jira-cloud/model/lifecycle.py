"""The lifecycle matrices: one for an issue of the book's, one for an epic and its children, one for the sprint an issue sits in, and one
for the standing configuration the app reads. Each scene names its condition and the calls that reach it; each action aims one call at the
record there."""

from __future__ import annotations

from datetime import date
from typing import Any, Callable, Iterable

from ostler.book import Axes, Impossible, Scene

from ..endpoints import (CreateIssue, EditIssue, FindAssignableUsers, FindUsers, GetMyself, ListBoardBacklog, ListBoardIssues, ListBoardSprints,
                         ListCreatableTypes, ListLabels, ListProjectBoards, ListSprintIssues, ListTransitions, MoveToBacklog, MoveToSprint,
                         ReadBoardConfiguration, ReadCreateFields, ReadFilter, ReadIssue, ReadProjectStatuses, RunTransition, ScreenComesOffDone,
                         ScreenGoesOnDone, SearchIssues, SearchProjects)
from ..fixtures import (BoardRef, BoardsOf, CreateTypes, FilterRef, Issue, ProjectRef, ProjectsPage, SprintList, SprintsOf, add_label, adopt, assign,
                        assignable, backlog_of, board_issues, bug, child_of, children_of, confirming, create_screen, done_issues, epic, epics,
                        into_sprint, labels, open_issues, opening, orphan, people, progress_of, remove_label, retitle, set_value, sprint_issues, task,
                        to_backlog, too_many, transition, transitions_of, Workflow)
from ..fixtures.issues import WALK_EPIC_LABEL, WALK_LABEL
from .cast import MANAGER, REVOKED
from .records import IssueRecord
from .state import ScreenOnDone, Serving

TODAY = date(2026, 11, 19)
WALK = WALK_LABEL


def walked(summary: str = "Retire the fax intake", **more: Any) -> Issue:
    return task(summary, labels=(WALK,), **more)


def ours(model: Serving) -> IssueRecord | None:
    return next((record for record in model.issues if WALK in record.labels and record.type == "CASE:Task"), None)


def fixture(record: IssueRecord) -> Issue:
    return Issue(project=record.project, type=record.type.split(":")[1], summary=record.summary, labels=record.labels, key=record.key)


def on_task(build: Callable[[Serving, Issue], object]) -> Callable[[Serving], object]:
    def aim(model: Serving) -> object:
        record = ours(model)
        if record is None:
            return Impossible("no task of the walk exists to aim at")
        return build(model, fixture(record))

    return aim


def created() -> Iterable[object]:
    yield CreateIssue(walked(), by=MANAGER)


def started() -> Iterable[object]:
    issue = walked()
    yield CreateIssue(issue, by=MANAGER)
    yield RunTransition(transition(issue, "In Progress"), by=MANAGER)


def in_review() -> Iterable[object]:
    issue = walked()
    yield CreateIssue(issue, by=MANAGER)
    yield RunTransition(transition(issue, "In Review"), by=MANAGER)


def finished() -> Iterable[object]:
    issue = walked()
    yield CreateIssue(issue, by=MANAGER)
    yield RunTransition(transition(issue, "Done"), by=MANAGER)


def planned() -> Iterable[object]:
    issue = walked()
    yield CreateIssue(issue, by=MANAGER)
    yield MoveToSprint(into_sprint("Sprint 15", issue), by=MANAGER)


def screened() -> Iterable[object]:
    yield ScreenGoesOnDone(Workflow("CASE"))
    yield CreateIssue(walked(), by=MANAGER)


def issue_state(model: Serving) -> str:
    record = ours(model)
    if record is None:
        return "(none)"
    return state_of_issue(model, record)


def state_of_issue(model: Serving, record: IssueRecord) -> str:
    status = model.statuses[record.status].name
    if isinstance(model, ScreenOnDone):
        return "behind a screen" if status != "Done" else "done behind a screen"
    if record.sprint is not None:
        return "planned"
    return {"To Do": "to do", "In Progress": "in progress", "In Review": "in review", "Done": "done"}[status]


ISSUE_SCENES = (
    Scene("(none)", "the walk has made no task", lambda today: ()),
    Scene("to do", "a CASE task of the walk is in To Do, in the backlog", lambda today: created()),
    Scene("in progress", "the task is In Progress", lambda today: started()),
    Scene("in review", "the task is In Review, from which CASE's workflow has no way back to To Do", lambda today: in_review()),
    Scene("done", "the task is Done", lambda today: finished()),
    Scene("planned", "the task is in To Do and in Sprint 15", lambda today: planned()),
    Scene("behind a screen", "an admin put a screen requiring Resolution on the transitions into Done, and the task is in To Do",
          lambda today: screened()),
)

ISSUE_ACTIONS: dict[str, Callable[[Serving], object]] = {
    "create a task": lambda m: CreateIssue(walked(), by=MANAGER),
    "create a task without a summary": lambda m: CreateIssue(walked(summary=""), by=MANAGER),
    "create a CASE bug without Severity": lambda m: CreateIssue(bug("CASE", severity=None, labels=(WALK,)), by=MANAGER),
    "create a task with a field its screen lacks": lambda m: CreateIssue(walked(values={"cf[Severity]": {"value": "S2 Major"}}), by=MANAGER),
    "create a task with a revoked token": lambda m: CreateIssue(walked(), by=REVOKED),
    "open the task": on_task(lambda m, i: ReadIssue(opening(i), by=MANAGER)),
    "confirm the summary": on_task(lambda m, i: ReadIssue(confirming(i, "summary"), by=MANAGER)),
    "open the task with a revoked token": on_task(lambda m, i: ReadIssue(opening(i), by=REVOKED)),
    "retitle the task": on_task(lambda m, i: EditIssue(retitle(i, "Retire the fax intake for good"), by=MANAGER)),
    "assign the task to the manager": on_task(lambda m, i: EditIssue(assign(i, "manager"), by=MANAGER)),
    "set a field the task's screen lacks": on_task(lambda m, i: EditIssue(set_value(i, "cf[Severity]", {"value": "S1 Critical"}), by=MANAGER)),
    "add a label": on_task(lambda m, i: EditIssue(add_label(i, "j4m-triaged"), by=MANAGER)),
    "remove the walk's label": on_task(lambda m, i: EditIssue(remove_label(i, WALK), by=MANAGER)),
    "read the transitions": on_task(lambda m, i: ListTransitions(transitions_of(i), by=MANAGER)),
    "start the task": on_task(lambda m, i: RunTransition(transition(i, "In Progress"), by=MANAGER)),
    "send the task to review": on_task(lambda m, i: RunTransition(transition(i, "In Review"), by=MANAGER)),
    "send the task back to To Do": on_task(lambda m, i: RunTransition(transition(i, "To Do"), by=MANAGER)),
    "finish the task": on_task(lambda m, i: RunTransition(transition(i, "Done"), by=MANAGER)),
    "find who may be assigned the task": on_task(lambda m, i: FindAssignableUsers(query=assignable(i), by=MANAGER)),
    "search the open issues": lambda m: SearchIssues(open_issues("CASE", WALK), by=MANAGER),
    "search the done issues": lambda m: SearchIssues(done_issues("CASE", WALK), by=MANAGER),
    "plan the task into Sprint 15": on_task(lambda m, i: MoveToSprint(into_sprint("Sprint 15", i), by=MANAGER)),
    "plan the task into the active sprint": on_task(lambda m, i: MoveToSprint(into_sprint("Sprint 14", i), by=MANAGER)),
    "move 51 issues into Sprint 15": on_task(lambda m, i: MoveToSprint(too_many("Sprint 15", i), by=MANAGER)),
    "plan the task into a sprint the board never had": on_task(lambda m, i: MoveToSprint(into_sprint("Sprint 99", i), by=MANAGER)),
    "send the task to the backlog": on_task(lambda m, i: MoveToBacklog(to_backlog(i), by=MANAGER)),
    "move 51 issues to the backlog": on_task(lambda m, i: MoveToBacklog(too_many(None, i), by=MANAGER)),
    "list Sprint 15": lambda m: ListSprintIssues(sprint_issues("Sprint 15", WALK), by=MANAGER),
    "list the active sprint": lambda m: ListSprintIssues(sprint_issues("Sprint 14", WALK), by=MANAGER),
    "list the CASE backlog": lambda m: ListBoardBacklog(backlog_of("CASE board", WALK), by=MANAGER),
    "take the screen off Done": lambda m: ScreenComesOffDone(Workflow("CASE")) if isinstance(m, ScreenOnDone) else Impossible("no screen is on Done"),
}

EPIC_LABEL = WALK_EPIC_LABEL


def epic_of(model: Serving) -> IssueRecord | None:
    return next((r for r in model.issues if EPIC_LABEL in r.labels and r.type == "CASE:Epic"), None)


def child_records(model: Serving) -> list[IssueRecord]:
    return [r for r in model.issues if EPIC_LABEL in r.labels and r.type != "CASE:Epic"]


def the_epic() -> Issue:
    return epic("Intake form v3", labels=(EPIC_LABEL,))


def lone_epic() -> Iterable[object]:
    yield CreateIssue(the_epic(), by=MANAGER)


def epic_with_child() -> Iterable[object]:
    parent = the_epic()
    yield CreateIssue(parent, by=MANAGER)
    yield CreateIssue(child_of(parent), by=MANAGER)


def epic_with_stray() -> Iterable[object]:
    parent = the_epic()
    stray = task("Copy legacy attachments", labels=(EPIC_LABEL,))
    yield CreateIssue(parent, by=MANAGER)
    yield CreateIssue(stray, by=MANAGER)


def on_epic(build: Callable[[Serving, Issue, list[Issue]], object]) -> Callable[[Serving], object]:
    def aim(model: Serving) -> object:
        record = epic_of(model)
        if record is None:
            return Impossible("no epic of the walk exists to aim at")
        return build(model, fixture(record), [fixture(child) for child in child_records(model)])

    return aim


def epic_state(model: Serving) -> str:
    record = epic_of(model)
    if record is None:
        return "(none)"
    children = child_records(model)
    if not children:
        return "no children"
    return "with a child" if any(child.parent == record.key for child in children) else "with a stray task"


EPIC_SCENES = (
    Scene("(none)", "the walk has made no epic", lambda today: ()),
    Scene("no children", "a CASE epic of the walk exists and no issue names it as its parent", lambda today: lone_epic()),
    Scene("with a child", "the epic has one story as its child", lambda today: epic_with_child()),
    Scene("with a stray task", "the epic has no child, and a task of the walk sits in no epic", lambda today: epic_with_stray()),
)


def first(children: list[Issue]) -> Issue | Impossible:
    return children[0] if children else Impossible("the epic has no issue beside it to aim at")


EPIC_ACTIONS: dict[str, Callable[[Serving], object]] = {
    "create an epic": lambda m: CreateIssue(the_epic(), by=MANAGER),
    "create a child story": on_epic(lambda m, e, c: CreateIssue(child_of(e), by=MANAGER)),
    "list the open epics": lambda m: SearchIssues(epics("CASE", EPIC_LABEL, open_only=True), by=MANAGER),
    "list every epic": lambda m: SearchIssues(epics("CASE", EPIC_LABEL), by=MANAGER),
    "count the children": on_epic(lambda m, e, c: SearchIssues(progress_of(e, label=EPIC_LABEL), by=MANAGER)),
    "list the children": on_epic(lambda m, e, c: SearchIssues(children_of(e, EPIC_LABEL), by=MANAGER)),
    "add the issue beside it": on_epic(lambda m, e, c: EditIssue(adopt(c[0], e), by=MANAGER) if c else Impossible("nothing beside the epic")),
    "remove the child": on_epic(lambda m, e, c: EditIssue(orphan(c[0]), by=MANAGER) if c else Impossible("the epic has no child")),
    "finish the epic": on_epic(lambda m, e, c: RunTransition(transition(e, "Done"), by=MANAGER)),
}

CONFIG_SCENES = (Scene("(standing)", "the site holds the seeded world", lambda today: ()),)

CONFIG_ACTIONS: dict[str, Callable[[Serving], object]] = {
    "read who signed in": lambda m: GetMyself(by=MANAGER),
    "read who signed in, with a revoked token": lambda m: GetMyself(by=REVOKED),
    "read who signed in, with no credential": lambda m: GetMyself(by=None),
    "list the projects": lambda m: SearchProjects(query=ProjectsPage(), by=MANAGER),
    "list the labels": lambda m: ListLabels(query=labels(), by=MANAGER),
    "list the labels starting with the walk's": lambda m: ListLabels(query=labels(WALK), by=MANAGER),
    "find people": lambda m: FindUsers(query=people(), by=MANAGER),
    "read CASE's statuses": lambda m: ReadProjectStatuses(ProjectRef("CASE"), by=MANAGER),
    "read the statuses of a project that does not exist": lambda m: ReadProjectStatuses(ProjectRef("NOPE"), by=MANAGER),
    "list CASE1's creatable types": lambda m: ListCreatableTypes(CreateTypes("CASE1"), by=MANAGER),
    "read the CASE Bug create screen": lambda m: ReadCreateFields(create_screen("CASE", "Bug"), by=MANAGER),
    "read the OPS Bug create screen": lambda m: ReadCreateFields(create_screen("OPS", "Bug"), by=MANAGER),
    "read a create screen 201 fields a page": lambda m: ReadCreateFields(create_screen("CASE", "Task").but(maxResults=201), by=MANAGER),
    "list CASE's boards": lambda m: ListProjectBoards(query=BoardsOf("CASE"), by=MANAGER),
    "read the CASE board": lambda m: ReadBoardConfiguration(BoardRef("CASE board"), by=MANAGER),
    "read the CASE1 board": lambda m: ReadBoardConfiguration(BoardRef("CASE1 board"), by=MANAGER),
    "list the CASE board's sprints": lambda m: ListBoardSprints(SprintsOf("CASE board"), by=MANAGER),
    "list the OPS board's sprints": lambda m: ListBoardSprints(SprintsOf("OPS board"), by=MANAGER),
    "read the CASE1 board filter": lambda m: ReadFilter(FilterRef("Filter for CASE1 board"), by=MANAGER),
    "read a filter no board uses": lambda m: ReadFilter(FilterRef("Filter nobody saved"), by=MANAGER),
    "list a sprint the board never had": lambda m: ListSprintIssues(SprintList("Sprint 99"), by=MANAGER),
    "list the CASE1 board": lambda m: ListBoardIssues(board_issues("CASE1 board", ("To Do", "In Progress", "Done"), WALK), by=MANAGER),
    "list the CASE1 backlog": lambda m: ListBoardBacklog(backlog_of("CASE1 board", WALK), by=MANAGER),
}


def standing(model: Serving) -> str:
    return "(standing)"


MATRICES = (
    Axes[Serving]("issue", TODAY, ISSUE_SCENES, ISSUE_ACTIONS, issue_state,
                  state_of=lambda m, r: state_of_issue(m, r), entities=lambda m: [r for r in m.issues if WALK in r.labels and r.type == "CASE:Task"]),
    Axes[Serving]("epic", TODAY, EPIC_SCENES, EPIC_ACTIONS, epic_state,
                  state_of=lambda m, r: epic_state(m), entities=lambda m: [r for r in m.issues if EPIC_LABEL in r.labels and r.type == "CASE:Epic"]),
    Axes[Serving]("configuration", TODAY, CONFIG_SCENES, CONFIG_ACTIONS, standing,
                  state_of=lambda m, r: "(standing)", entities=lambda m: list(m.projects)),
)
