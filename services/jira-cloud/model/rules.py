"""Why Jira says no to a call the app makes. A refusal's message is the one the surface reads off Jira's error body: the first of
`errorMessages`, else `<field id>: <message>` for the first entry of `errors`, so a field error stays keyed by its field. A rule reads the
request (`a`), the state (`s`) and the caller (`by`)."""

from __future__ import annotations

from typing import Any

from ostler.book import Rule

from .records import MOVE_LIMIT
from .state import ScreenOnDone, Serving
from .world import NO_TRANSITION

NO_ISSUE = "Issue does not exist or you do not have permission to see it."
NO_BOARD = "Board does not exist or you do not have permission to see it."


def first_missing(a: Any) -> str:
    """The first required field a create leaves empty, worded the way Jira words it."""
    from ..model.world import FIELDS

    sent = a.fields
    for record in FIELDS:
        if record.project == a.project and a.type in record.required and record.id not in ("project", "issuetype", "summary"):
            if sent.get(record.id) in (None, "", [], {}):
                return f"{record.id}: {record.name} is required."
    return ""


def first_off_create(a: Any) -> str:
    """The first field a create sends that the type's create screen does not hold."""
    from ..model.world import FIELDS

    on = {f.id for f in FIELDS if f.project == a.project and a.type in f.screens}
    return next((name for name in a.fields if name not in on), "")


def first_off_screen(a: Any) -> str:
    """The first field an edit sends that the issue's edit screen does not hold."""
    from ..model.world import FIELDS

    on = {f.id for f in FIELDS if f.project == a.issue.project and (a.issue.type in f.screens)}
    for name in (*(a.edit.fields or {}), *(a.edit.update or {})):
        if name not in on:
            return name
    return ""


def _unknown_issue(a: Any, s: Serving, by: Any) -> bool:
    key = getattr(a, "key", None)
    return key is None or key not in s.issues


issue_missing = Rule[Any, Serving](NO_ISSUE, _unknown_issue, 404,
                                   why="Jira answers the same for an issue that does not exist and one the caller may not browse, so a key "
                                       "reveals nothing about a project the caller cannot see")

project_missing = Rule[Any, Serving]("No project could be found with key '{projectIdOrKey}'.",
                                     lambda a, s, by: a.projectIdOrKey not in s.projects, 404)

board_missing = Rule[Any, Serving](NO_BOARD, lambda a, s, by: a.boardId not in s.boards, 404)

summary_missing = Rule[Any, Serving]("summary: You must specify a summary of the issue.", lambda a, s, by: not (a.summary or "").strip(), 400,
                                     why="every issue type requires a summary, and Jira keys the error by the field so the dialog shows it "
                                         "under the field")

required_missing = Rule[Any, Serving]("{missing}", lambda a, s, by: bool(first_missing(a)), 400,
                                      why="a field the project's field configuration marks required blocks the create, and Jira keys the "
                                          "error by the field's id, which for a custom field is its customfield id and never its name")


off_create_screen = Rule[Any, Serving]("{off_create}: Field '{off_create}' cannot be set. It is not on the appropriate screen, or unknown.",
                                       lambda a, s, by: bool(first_off_create(a)), 400,
                                       why="a create may set only the fields of the type's create screen, which is why the app builds its "
                                           "dialog from createmeta")

off_edit_screen = Rule[Any, Serving]("{off_screen}: Field '{off_screen}' cannot be set. It is not on the appropriate screen, or unknown.",
                                     lambda a, s, by: bool(first_off_screen(a)), 400,
                                     why="an edit may set only the fields the issue's edit screen holds, which editmeta lists")


def _forbidden(a: Any, s: Serving, by: Any) -> bool:
    record = s.issues[a.key]
    current = s.statuses[record.status].name
    return a.to == current or (current, a.to) in NO_TRANSITION[record.project] or f"{record.project}:{a.to}" not in s.statuses


transition_forbidden = Rule[Any, Serving]("Transition id '{transition}' is not valid for this issue.", _forbidden, 400,
                                          why="the workflow offers a transition only from the statuses it allows it from, and never into "
                                              "the status the issue holds; CASE's workflow has no way back from In Review to To Do")


def _needs_resolution(a: Any, s: Serving, by: Any) -> bool:
    record = s.issues[a.key]
    target = s.statuses.get(f"{record.project}:{a.to}")
    return isinstance(s, ScreenOnDone) and target is not None and target.category == "done"


transition_needs_screen = Rule[Any, Serving]("resolution: Resolution is required.", _needs_resolution, 400,
                                             why="a transition whose screen requires a field refuses a call that does not send it, and the "
                                                 "app never sends screen fields, so it offers the browser instead")

too_many_moved = Rule[Any, Serving](f"Cannot move more than {MOVE_LIMIT} issues at once.", lambda a, s, by: a.count > MOVE_LIMIT, 400,
                                    why="a sprint or backlog move takes at most 50 issues a call, which is why the app sends a larger "
                                        "selection in batches of 50")


def _unknown_moved(a: Any, s: Serving, by: Any) -> bool:
    return any(key not in s.issues for key in a.issues)


moved_missing = Rule[Any, Serving](NO_ISSUE, _unknown_moved, 404)


sprint_missing = Rule[Any, Serving]("Sprint with id {sprintId} does not exist.", lambda a, s, by: a.sprintId is not None and a.sprintId not in s.sprints, 404)

no_sprints = Rule[Any, Serving]("The board does not support sprints", lambda a, s, by: a.boardId in s.boards and s.boards[a.boardId].type != "scrum",
                                400, why="only a scrum board has sprints; a kanban board's issues come from its board and backlog lists")

page_too_large = Rule[Any, Serving]("Parameter 'maxResults' must not exceed the limit '200'", lambda a, s, by: (a.maxResults or 0) > 200, 400,
                                    why="createmeta pages its fields by at most 200, so the app asks for 200 and pages until total")
