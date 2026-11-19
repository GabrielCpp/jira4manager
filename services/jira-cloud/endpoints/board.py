"""The board and the backlog: the token-paged issue lists of a sprint, a board and a backlog, and the moves between sprints and the
backlog."""

from __future__ import annotations

from ostler.book import Answer, Arrange, Endpoint, Field, Int, Object, Refusal, Refusals, Str

from ..fixtures import Workflow
from ..model import actions
from .atlassian import AGILE, KANBAN_BACKLOG, SOFTWARE_LISTS, SPRINT_GROUP
from .common import AUTH, BOARD_REFUSALS, NO_BOARD, NO_ISSUE, NO_SPRINT, NOT_SIGNED, REFUSED
from .shapes import BOARD, MOVE_BODY, SEARCH_PAGE, SPRINT

LIST_QUERY = Object(
    jql=Field(Str(), required=False, does="narrows the list; the kanban board sends the statuses of its visible columns"),
    fields=Field(Str(), required=False, does="the row fields and the Sprint field, comma separated; every navigable field when left out"),
    maxResults=Field(Int(), required=False, does="100; 50 when left out"),
)


class ListSprintIssues(Endpoint):
    method = "GET"
    path = "/rest/software/1.0/sprint/{sprintId}/issue"
    auth = AUTH
    params = Object(sprintId=Field(SPRINT, does="the sprint's id"))
    query = LIST_QUERY
    answers = (Answer(200, SEARCH_PAGE, "the sprint's issues in rank order, token paged"), NO_SPRINT, NOT_SIGNED)
    does = "Fills a scrum board with the active sprint's cards, and each sprint section of the backlog with its issues, in rank order."
    source = (AGILE + "::GET /rest/software/1.0/sprint/{sprintId}/issue", SOFTWARE_LISTS)
    carries = actions.ListSprintIssues


class ListBoardIssues(Endpoint):
    method = "GET"
    path = "/rest/software/1.0/board/{boardId}/issue"
    auth = AUTH
    params = Object(boardId=Field(BOARD, does="the board's id"))
    query = LIST_QUERY
    answers = (Answer(200, SEARCH_PAGE, "the board's issues outside its backlog, in rank order, token paged"), NO_BOARD, NOT_SIGNED)
    refusals = BOARD_REFUSALS
    does = "Fills a kanban board with the cards outside its backlog. The /rest/agile/1.0/ issue lists it replaces are never called."
    source = (AGILE + "::GET /rest/software/1.0/board/{boardId}/issue", SOFTWARE_LISTS)
    carries = actions.ListBoardIssues


class ListBoardBacklog(Endpoint):
    method = "GET"
    path = "/rest/software/1.0/board/{boardId}/backlog"
    auth = AUTH
    params = Object(boardId=Field(BOARD, does="the board's id"))
    query = LIST_QUERY
    answers = (
        Answer(200, SEARCH_PAGE, "the backlog's issues in rank order: on a scrum board the open issues in no active or future sprint, on a "
                                 "kanban board the issues in its backlog column's statuses"),
        NO_BOARD,
        NOT_SIGNED,
    )
    refusals = BOARD_REFUSALS
    does = "Fills the Backlog section of a scrum board and the backlog rows of a kanban board."
    source = (AGILE + "::GET /rest/software/1.0/board/{boardId}/backlog", SOFTWARE_LISTS, KANBAN_BACKLOG)
    carries = actions.ListBoardBacklog


class MoveToSprint(Endpoint):
    method = "POST"
    path = "/rest/agile/1.0/sprint/{sprintId}/issue"
    auth = AUTH
    params = Object(sprintId=Field(SPRINT, does="an active or future sprint"))
    body = MOVE_BODY
    refusals = Refusals(malformed=Refusal("Sprint does not exist or you do not have permission to see it.", 404))
    answers = (
        Answer(204, None, "every issue named is in the sprint and keeps its rank"),
        Answer(400, REFUSED.body, "more than 50 issues"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    does = ("Moves issues into a sprint, by drag, menu, the M key or the detail pane's sprint picker. The app sends at most 50 a call; a "
            "refused batch rolls the whole move back. A move is never retried.")
    source = (AGILE + "::POST /rest/agile/1.0/sprint/{sprintId}/issue", SPRINT_GROUP)
    carries = actions.MoveToSprint


class MoveToBacklog(Endpoint):
    method = "POST"
    path = "/rest/agile/1.0/backlog/issue"
    auth = AUTH
    body = MOVE_BODY
    answers = (
        Answer(204, None, "every issue named is in no sprint"),
        Answer(400, REFUSED.body, "more than 50 issues"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    does = "Moves issues out of their sprint to the backlog, at most 50 a call."
    source = (AGILE + "::POST /rest/agile/1.0/backlog/issue",)
    carries = actions.MoveToBacklog


class ScreenGoesOnDone(Arrange[Workflow]):
    does = ("An admin puts a screen with a required Resolution on every transition into a done status, so a status change into Done needs "
            "a field the app does not send.")
    carries = actions.PutScreenOnDone


class ScreenComesOffDone(Arrange[Workflow]):
    does = "An admin takes the screen off the transitions into a done status."
    carries = actions.TakeScreenOffDone


ALL = (ListSprintIssues, ListBoardIssues, ListBoardBacklog, MoveToSprint, MoveToBacklog)
