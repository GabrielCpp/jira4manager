from datetime import date

from ostler.book import Journey

from ..endpoints import (CreateIssue, EditIssue, FindAssignableUsers, FindUsers, ListCreatableTypes, ListLabels, ListTransitions, ReadCreateFields,
                         ReadIssue, ReadProjectStatuses, RunTransition, SearchIssues)
from ..fixtures import (CreateTypes, ProjectRef, add_label, assign, assignable, bug, confirming, create_screen, describe, done_issues, labels,
                        open_issues, opening, people, remove_label, reprioritise, retitle, row_of, set_value, story, task, transition,
                        transitions_of)
from ..model.cast import MANAGER

LABEL = "j4m-issues"
TRIAGED = "j4m-triaged"


class ManageIssuesInAProject(Journey):
    """A manager opens CASE. The app reads the project's statuses and the types they may create, then lists the open Bugs, Stories and
    Tasks. They create a Bug: the dialog reads the Bug create screen, and Create without Severity is refused with the error under Severity,
    so they fill it and the Bug is created. They create a Story, open it, retitle it, describe it, raise its priority, assign it to
    themselves from the assignable people, set its Reviewer from the site's people and add a label, reading each change back. The status
    picker offers the workflow's transitions; they start the Story, send it to review and cannot send it back to To Do, because CASE's
    workflow has no such transition. They finish it, and it leaves the open list for the done list. A field the Story's screen lacks is
    refused with Jira's message under the field."""

    def steps(self, today: date):
        yield ReadProjectStatuses(ProjectRef("CASE"), by=MANAGER)
        yield ListCreatableTypes(CreateTypes("CASE"), by=MANAGER)
        yield SearchIssues(open_issues("CASE", LABEL), by=MANAGER)

        yield ReadCreateFields(create_screen("CASE", "Bug"), by=MANAGER)
        unfilled = bug("CASE", "Login fails on Safari", severity=None, labels=(LABEL,))
        yield CreateIssue(unfilled, by=MANAGER)
        login = bug("CASE", "Login fails on Safari", severity="S2 Major", labels=(LABEL,))
        yield CreateIssue(login, by=MANAGER)
        yield ReadIssue(row_of(login), by=MANAGER)
        yield CreateIssue(task("", labels=(LABEL,)), by=MANAGER)

        yield ReadCreateFields(create_screen("CASE", "Story"), by=MANAGER)
        lookup = story("Postcode lookup on the address step", labels=(LABEL,))
        yield CreateIssue(lookup, by=MANAGER)
        yield SearchIssues(open_issues("CASE", LABEL), by=MANAGER)
        yield ReadIssue(opening(lookup), by=MANAGER)

        yield EditIssue(retitle(lookup, "Postcode lookup fills the street and town"), by=MANAGER)
        yield ReadIssue(confirming(lookup, "summary"), by=MANAGER)
        yield EditIssue(describe(lookup, "Typing a postcode lists the matching addresses."), by=MANAGER)
        yield ReadIssue(confirming(lookup, "description"), by=MANAGER)
        yield EditIssue(reprioritise(lookup, "High"), by=MANAGER)
        yield FindAssignableUsers(query=assignable(lookup), by=MANAGER)
        yield EditIssue(assign(lookup, "manager"), by=MANAGER)
        yield FindUsers(query=people(), by=MANAGER)
        yield EditIssue(set_value(lookup, "cf[Reviewer]", {"accountId": "manager"}), by=MANAGER)
        yield ListLabels(query=labels(), by=MANAGER)
        yield EditIssue(add_label(lookup, TRIAGED), by=MANAGER)
        yield ListLabels(query=labels(TRIAGED), by=MANAGER)
        yield ReadIssue(confirming(lookup, "priority", "assignee", "cf[Reviewer]", "labels"), by=MANAGER)
        yield EditIssue(set_value(lookup, "cf[Severity]", {"value": "S1 Critical"}), by=MANAGER)
        yield EditIssue(remove_label(lookup, TRIAGED), by=MANAGER)

        yield ListTransitions(transitions_of(lookup), by=MANAGER)
        yield RunTransition(transition(lookup, "In Progress"), by=MANAGER)
        yield RunTransition(transition(lookup, "In Review"), by=MANAGER)
        yield ListTransitions(transitions_of(lookup), by=MANAGER)
        yield RunTransition(transition(lookup, "To Do"), by=MANAGER)
        yield RunTransition(transition(lookup, "Done"), by=MANAGER)
        yield RunTransition(transition(lookup, "Done"), by=MANAGER)
        yield SearchIssues(open_issues("CASE", LABEL), by=MANAGER)
        yield SearchIssues(done_issues("CASE", LABEL), by=MANAGER)
