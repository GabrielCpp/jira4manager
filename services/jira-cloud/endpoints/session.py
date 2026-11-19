"""The session's reads: who the token belongs to, the projects in the sidebar, and the site's labels and people for the pickers."""

from __future__ import annotations

from ostler.book import Answer, Endpoint, Field, Id, Int, Object, Refusal, Refusals, Str

from ..model import actions
from .atlassian import BASIC_AUTH, LABELS, PLATFORM, USER_SEARCH
from ..model.records import IssueRecord, LabelRecord
from .common import AUTH, NO_ISSUE, NOT_SIGNED, ISSUE_REFUSALS
from .shapes import ERRORS, LABELS_PAGE, PEOPLE, PROJECTS_PAGE, USER

PEOPLE_QUERY = Object(
    query=Field(Str(classes={"the standing account's name": "manager"}), does="text the person types; Jira matches it against names and email addresses"),
    maxResults=Field(Int(), required=False, does="50 for a picker"),
)


class GetMyself(Endpoint):
    method = "GET"
    path = "/rest/api/3/myself"
    auth = AUTH
    answers = (
        Answer(200, USER, "the account the email and token belong to"),
        NOT_SIGNED,
    )
    does = ("Says whose token the app holds. Sign-in calls it to check the credentials before it stores anything, and every launch calls it "
            "again; a 401 means the token was refused or stopped working.")
    source = (PLATFORM + "::GET /rest/api/3/myself", BASIC_AUTH)
    carries = actions.ReadMyself


class SearchProjects(Endpoint):
    method = "GET"
    path = "/rest/api/3/project/search"
    auth = AUTH
    query = Object(
        startAt=Field(Int(), required=False, does="0, then the next page's start"),
        maxResults=Field(Int(), required=False, does="at most 100; 50 when left out"),
        orderBy=Field(Str(), required=False, does="name; key when left out"),
    )
    answers = (Answer(200, PROJECTS_PAGE, "one page of the projects the caller may browse, by name"), NOT_SIGNED)
    does = "Fills the sidebar with the projects the person may browse. The app pages by offset until isLast."
    source = (PLATFORM + "::GET /rest/api/3/project/search",)
    carries = actions.ListProjects


class ListLabels(Endpoint):
    method = "GET"
    path = "/rest/api/3/label"
    auth = AUTH
    query = Object(
        query=Field(Id(LabelRecord, of=Str(), minted="a label is one record of the whole site and every run adds its own"), required=False,
                    does="a case-insensitive prefix, applied before paging"),
        startAt=Field(Int(), required=False),
        maxResults=Field(Int(), required=False, does="1000 for the session's first read, 50 while the person types; 1000 when left out"),
    )
    answers = (Answer(200, LABELS_PAGE, "the site's labels, or those that start with the query"), NOT_SIGNED)
    does = "Lists the site's labels for the label pickers. A label exists once an issue carries it; nothing creates one on its own."
    source = (PLATFORM + "::GET /rest/api/3/label", LABELS)
    carries = actions.ListLabels


class FindAssignableUsers(Endpoint):
    method = "GET"
    path = "/rest/api/3/user/assignable/search"
    auth = AUTH
    query = Object(
        query=Field(Str(classes={"the standing account's name": "manager"}), required=False, does="text the person types; everyone assignable when left out"),
        maxResults=Field(Int(), required=False, does="50"),
        issueKey=Field(Id(IssueRecord, of=Str()), required=False, does="the issue being assigned, in the detail pane"),
        project=Field(Str(), required=False, does="the project of a new issue, in the create dialog"),
    )
    answers = (
        Answer(200, PEOPLE, "the people who hold Assign issues on the issue or project and match the query; a page may hold fewer than asked"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    refusals = ISSUE_REFUSALS
    does = "Offers the people the Assignee picker may choose: only those who may be assigned the issue."
    source = (PLATFORM + "::GET /rest/api/3/user/assignable/search", USER_SEARCH)
    carries = actions.FindAssignable


class FindUsers(Endpoint):
    method = "GET"
    path = "/rest/api/3/user/search"
    auth = AUTH
    query = PEOPLE_QUERY
    answers = (Answer(200, PEOPLE, "the active people of the site who match the query"), Answer(400, ERRORS, "the query is left out"), NOT_SIGNED)
    refusals = Refusals(missing=Refusal("One of the following query parameters must be provided: query, accountId, property.", 400))
    does = ("Offers the people a custom user field such as Reviewer may choose. Jira can still refuse one of them on save when the field is "
            "limited to some groups.")
    source = (PLATFORM + "::GET /rest/api/3/user/search", USER_SEARCH)
    carries = actions.FindPeople


ALL = (GetMyself, SearchProjects, ListLabels, FindAssignableUsers, FindUsers)
