"""A project's configuration, read once per session: its statuses, the types a person may create and their create screens, its boards,
each board's columns and sprints, and the saved filter behind a board."""

from __future__ import annotations

from ostler.book import Answer, Endpoint, Field, Int, Object, Str

from ..model import actions
from .atlassian import AGILE, BACKLOG_COLUMN, CREATEMETA, ISSUES_GROUP, KANBAN_BACKLOG, PLATFORM, STATUS_CATEGORIES
from .common import AUTH, BOARD_REFUSALS, NO_BOARD, NO_PROJECT, NOT_SIGNED, REFUSED
from .shapes import BOARD, BOARD_CONFIG, PROJECT, TYPE_ID, BOARDS_PAGE, CREATE_FIELDS, CREATE_TYPES, FILTER, FILTER_DETAIL, PROJECT_STATUSES, SPRINTS_PAGE

BY_PROJECT = Object(projectIdOrKey=Field(Str(), does="the project key, such as CASE"))
BY_BOARD = Object(boardId=Field(BOARD, does="the board's id"))


class ReadProjectStatuses(Endpoint):
    method = "GET"
    path = "/rest/api/3/project/{projectIdOrKey}/statuses"
    auth = AUTH
    params = BY_PROJECT
    answers = (
        Answer(200, PROJECT_STATUSES, "one entry per issue type, each with the statuses its workflow holds and their categories"),
        NO_PROJECT,
        NOT_SIGNED,
    )
    does = "Gives each issue type's statuses with their categories. The Issues view groups by category and the status filter lists these names."
    source = (PLATFORM + "::GET /rest/api/3/project/{projectIdOrKey}/statuses", STATUS_CATEGORIES)
    carries = actions.ReadProjectStatuses


class ListCreatableTypes(Endpoint):
    method = "GET"
    path = "/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes"
    auth = AUTH
    params = BY_PROJECT
    answers = (
        Answer(200, CREATE_TYPES, "the types the caller may create in the project, with their hierarchy level"),
        NO_PROJECT,
        NOT_SIGNED,
    )
    does = ("Lists the types the person may create. Level 0 types fill the type filter and the create dialog, and level 1 types are the epic "
            "types. The deprecated createmeta with expand is never called.")
    source = (PLATFORM + "::GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes", CREATEMETA)
    carries = actions.ListCreatableTypes


class ReadCreateFields(Endpoint):
    method = "GET"
    path = "/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}"
    auth = AUTH
    params = Object(projectIdOrKey=Field(Str(), does="the project key"), issueTypeId=Field(TYPE_ID, does="the site's id of the issue type"))
    query = Object(startAt=Field(Int(), required=False, does="0 when left out"), maxResults=Field(Int(), required=False, does="200, the largest page; 50 when left out"))
    answers = (
        Answer(200, CREATE_FIELDS, "the create screen's fields in the screen's order, each with required, its schema and its operations"),
        Answer(400, REFUSED.body, "maxResults is over 200"),
        NO_PROJECT,
        NOT_SIGNED,
    )
    does = ("Gives the create screen of one type, field by field. The create dialog lists exactly these fields in this order and marks the "
            "required ones; the app pages until total.")
    source = (PLATFORM + "::GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}", ISSUES_GROUP, CREATEMETA)
    carries = actions.ReadCreateFields


class ListProjectBoards(Endpoint):
    method = "GET"
    path = "/rest/agile/1.0/board"
    auth = AUTH
    query = Object(projectKeyOrId=Field(PROJECT, required=False, does="the project whose boards to list; every board when left out"))
    answers = (Answer(200, BOARDS_PAGE, "the boards whose filter names the project; several turn the board line into a picker"), NOT_SIGNED)
    does = "Lists the project's boards with their id, name and type."
    source = (AGILE + "::GET /rest/agile/1.0/board",)
    carries = actions.ListProjectBoards


class ReadBoardConfiguration(Endpoint):
    method = "GET"
    path = "/rest/agile/1.0/board/{boardId}/configuration"
    auth = AUTH
    params = BY_BOARD
    answers = (Answer(200, BOARD_CONFIG, "the board's columns with their statuses and the id of its filter"), NO_BOARD, NOT_SIGNED)
    refusals = BOARD_REFUSALS
    does = "Gives the board's columns in order and the statuses each holds. A kanban board's Backlog column holds its backlog statuses."
    source = (AGILE + "::GET /rest/agile/1.0/board/{boardId}/configuration", BACKLOG_COLUMN)
    carries = actions.ReadBoardConfiguration


class ListBoardSprints(Endpoint):
    method = "GET"
    path = "/rest/agile/1.0/board/{boardId}/sprint"
    auth = AUTH
    params = BY_BOARD
    query = Object(state=Field(Str(), required=False, does="active,future; every state when left out"))
    answers = (
        Answer(200, SPRINTS_PAGE, "the board's active and future sprints with their names, goals and dates"),
        Answer(400, REFUSED.body, "the board is a kanban board, which has no sprints"),
        NO_BOARD,
        NOT_SIGNED,
    )
    refusals = BOARD_REFUSALS
    does = "Gives a scrum board's active and future sprints. They fill the board header, the sprint sections and every sprint picker."
    source = (AGILE + "::GET /rest/agile/1.0/board/{boardId}/sprint",)
    carries = actions.ListBoardSprints


class ReadFilter(Endpoint):
    method = "GET"
    path = "/rest/api/3/filter/{filterId}"
    auth = AUTH
    params = Object(filterId=Field(FILTER, does="the board filter's id, from the board configuration"))
    answers = (Answer(200, FILTER_DETAIL, "the filter's JQL"), Answer(400, REFUSED.body, "the filter does not exist or the caller may not see it"),
               NOT_SIGNED)
    does = ("Gives a board filter's JQL. It is the kanban backlog's fallback: if the backlog list refuses a kanban board, the app searches "
            "the filter's JQL narrowed to the backlog column's statuses.")
    source = (PLATFORM + "::GET /rest/api/3/filter/{id}", KANBAN_BACKLOG)
    carries = actions.ReadFilter


ALL = (ReadProjectStatuses, ListCreatableTypes, ReadCreateFields, ListProjectBoards, ReadBoardConfiguration, ListBoardSprints, ReadFilter)
