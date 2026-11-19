from datetime import date

from ostler.book import Journey

from ..endpoints import CreateIssue, EditIssue, ListCreatableTypes, ReadIssue, RunTransition, SearchIssues
from ..fixtures import (CreateTypes, adopt, child_of, children_of, confirming, epic, epics, open_issues, opening, orphan, progress_of, story, task,
                        transition)
from ..model.cast import MANAGER

LABEL = "j4m-epics"


class ManageEpicsInAProject(Journey):
    """A manager opens Epics in CASE1, a team-managed project, where epics work the same way as in a company-managed one. The app reads the
    types to tell epics from standard types and lists the open epics. They create an epic, which has no children yet. They create a child
    story inside it, then add an existing task through Add existing, which sets the task's parent. The progress search counts both
    children by status; when the story is done, one of two is done. They remove the task from the epic, which clears its parent, and it
    shows on the Issues view with no epic chip. Finishing the epic moves it out of the open epics and into the list of every epic."""

    def steps(self, today: date):
        yield ListCreatableTypes(CreateTypes("CASE1"), by=MANAGER)
        yield SearchIssues(epics("CASE1", LABEL, open_only=True), by=MANAGER)

        portal = epic("Self-service status page", project="CASE1", labels=(LABEL,))
        yield CreateIssue(portal, by=MANAGER)
        yield SearchIssues(epics("CASE1", LABEL, open_only=True), by=MANAGER)
        yield ReadIssue(opening(portal), by=MANAGER)
        yield SearchIssues(children_of(portal, LABEL), by=MANAGER)

        page = child_of(portal, "Show case status to the claimant without login")
        yield CreateIssue(page, by=MANAGER)
        sitemap = task("Add the status page to the sitemap", project="CASE1", labels=(LABEL,))
        yield CreateIssue(sitemap, by=MANAGER)
        yield EditIssue(adopt(sitemap, portal), by=MANAGER)
        yield ReadIssue(confirming(sitemap, "parent"), by=MANAGER)
        yield SearchIssues(children_of(portal, LABEL), by=MANAGER)
        yield SearchIssues(progress_of(portal, label=LABEL), by=MANAGER)

        yield RunTransition(transition(page, "Done"), by=MANAGER)
        yield SearchIssues(progress_of(portal, label=LABEL), by=MANAGER)

        yield EditIssue(orphan(sitemap), by=MANAGER)
        yield ReadIssue(confirming(sitemap, "parent"), by=MANAGER)
        yield SearchIssues(children_of(portal, LABEL), by=MANAGER)
        yield SearchIssues(open_issues("CASE1", LABEL), by=MANAGER)

        yield RunTransition(transition(portal, "Done"), by=MANAGER)
        yield SearchIssues(epics("CASE1", LABEL, open_only=True), by=MANAGER)
        yield SearchIssues(epics("CASE1", LABEL), by=MANAGER)
        yield CreateIssue(story("Label every form field for screen readers", project="CASE1", labels=(LABEL,), parent=portal), by=MANAGER)
