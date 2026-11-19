"""The issue calls: the JQL search behind every list, the detail pane's read, the transitions a status change reads and runs, and the
create and edit writes."""

from __future__ import annotations

from ostler.book import Answer, Endpoint, Field, Object, Refusal, Refusals, Str

from ..model import actions
from .atlassian import CREATE_FAILS, ENHANCED_SEARCH, EPIC_LINK, ISSUES_GROUP, ISSUE_SEARCH, PLATFORM, SPRINT_ON_CREATE
from .common import AUTH, ISSUE_REFUSALS, NO_ISSUE, NOT_SIGNED, PAYLOAD, REFUSED, UNBOUNDED
from .shapes import CREATE_BODY, CREATED, EDIT_BODY, ISSUE, ISSUE_DETAIL, SEARCH_BODY, SEARCH_PAGE, TRANSITION_BODY, TRANSITIONS

BY_KEY = Object(key=Field(ISSUE, does="the issue key"))


class SearchIssues(Endpoint):
    method = "POST"
    path = "/rest/api/3/search/jql"
    auth = AUTH
    body = SEARCH_BODY
    refusals = Refusals(missing=Refusal(UNBOUNDED, 400), malformed=Refusal(PAYLOAD, 400), wrong_type=Refusal(PAYLOAD, 400))
    answers = (
        Answer(200, SEARCH_PAGE, "one page of the issues the JQL finds, with only the fields asked for; no total and no startAt"),
        REFUSED,
        NOT_SIGNED,
    )
    does = ("Runs the JQL behind the Issues view, the Epics view, the epic chips and an epic's children. It pages by token: the app sends the "
            "previous page's nextPageToken and stops on isLast or a page with no token, at 1,000 issues. The removed /rest/api/3/search is "
            "never called.")
    source = (PLATFORM + "::POST /rest/api/3/search/jql", ISSUE_SEARCH, ENHANCED_SEARCH)
    carries = actions.SearchIssues


class ReadIssue(Endpoint):
    method = "GET"
    path = "/rest/api/3/issue/{key}"
    auth = AUTH
    params = BY_KEY
    query = Object(
        fields=Field(Str(), required=False, does="*all for the detail pane, or the changed field and updated after a write; every navigable field when left out"),
        expand=Field(Str(), required=False, does="names,schema,editmeta for the detail pane"),
    )
    answers = (
        Answer(200, ISSUE_DETAIL, "the issue's values, and with the expansions each field's name, schema and edit metadata"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    refusals = ISSUE_REFUSALS
    does = ("Opens an issue in the detail pane: one call draws the title, the description, the paragraph fields and the properties column. "
            "After a write the app reads the changed field and updated again, to show what Jira kept.")
    source = (PLATFORM + "::GET /rest/api/3/issue/{issueIdOrKey}", ISSUES_GROUP)
    carries = actions.ReadIssue


class ListTransitions(Endpoint):
    method = "GET"
    path = "/rest/api/3/issue/{key}/transitions"
    auth = AUTH
    params = BY_KEY
    query = Object(expand=Field(Str(), required=False, does="transitions.fields, so each transition carries its screen's fields"))
    answers = (Answer(200, TRANSITIONS, "the transitions the workflow allows from the issue's status, each with its target"), NO_ISSUE,
               NOT_SIGNED)
    refusals = ISSUE_REFUSALS
    does = ("Lists the statuses the workflow allows from here. The status picker shows only these, and a board drop picks the first status "
            "of the column that one of them reaches.")
    source = (PLATFORM + "::GET /rest/api/3/issue/{issueIdOrKey}/transitions",)
    carries = actions.ListTransitions


class RunTransition(Endpoint):
    method = "POST"
    path = "/rest/api/3/issue/{key}/transitions"
    auth = AUTH
    params = BY_KEY
    body = TRANSITION_BODY
    answers = (
        Answer(204, None, "the issue moved to the transition's target status"),
        Answer(400, REFUSED.body, "the workflow does not offer that transition from the issue's status, or its screen requires a field the call left out"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    refusals = ISSUE_REFUSALS
    does = ("Changes an issue's status by running one transition. The app never sends screen fields: a transition whose screen requires one "
            "is not sent, and the browser is offered instead. A transition is never retried.")
    source = (PLATFORM + "::POST /rest/api/3/issue/{issueIdOrKey}/transitions",)
    carries = actions.TransitionIssue


class CreateIssue(Endpoint):
    method = "POST"
    path = "/rest/api/3/issue"
    auth = AUTH
    body = CREATE_BODY
    answers = (
        Answer(201, CREATED, "the issue exists, in its workflow's first status, at the bottom of the rank", creates="key"),
        Answer(400, REFUSED.body, "a required field is empty, a field is not on the create screen, or a value is invalid: errors are keyed by field id"),
        NOT_SIGNED,
    )
    does = ("Creates a Bug, Story, Task or Epic with the fields its create screen holds. A child names its epic in parent, in both project "
            "styles. A create is not optimistic and never retried, so an issue is never made twice.")
    source = (PLATFORM + "::POST /rest/api/3/issue", ISSUES_GROUP, CREATE_FAILS, SPRINT_ON_CREATE, EPIC_LINK)
    carries = actions.CreateIssue


class EditIssue(Endpoint):
    method = "PUT"
    path = "/rest/api/3/issue/{key}"
    auth = AUTH
    params = BY_KEY
    body = EDIT_BODY
    answers = (
        Answer(204, None, "the issue holds the new values"),
        Answer(400, REFUSED.body, "a field is not on the edit screen, or a value is invalid: errors are keyed by field id"),
        NO_ISSUE,
        NOT_SIGNED,
    )
    refusals = ISSUE_REFUSALS
    does = ("Edits an issue's fields. Labels change through update with one add or remove each, so two people editing labels at once keep "
            "both changes. The parent is set by key and cleared with update.parent set to none.")
    source = (PLATFORM + "::PUT /rest/api/3/issue/{issueIdOrKey}", ISSUES_GROUP, EPIC_LINK)
    carries = actions.EditIssue


ALL = (SearchIssues, ReadIssue, ListTransitions, RunTransition, CreateIssue, EditIssue)
