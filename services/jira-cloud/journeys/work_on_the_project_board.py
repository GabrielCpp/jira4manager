from datetime import date

from ostler.book import Journey

from ..endpoints import (CreateIssue, ListBoardBacklog, ListBoardIssues, ListBoardSprints, ListProjectBoards, ListSprintIssues, ListTransitions,
                         MoveToBacklog, MoveToSprint, ReadBoardConfiguration, ReadFilter, RunTransition)
from ..fixtures import (BoardRef, BoardsOf, FilterRef, SprintsOf, backlog_of, board_issues, into_sprint, sprint_issues, story, task, to_backlog,
                        too_many, transition, transitions_of)
from ..model.cast import MANAGER

LABEL = "j4m-board"


class WorkOnTheProjectBoard(Journey):
    """A manager opens the CASE board. The app reads its boards, its columns and its active and future sprints, then the active sprint's
    cards and the backlog. They create three issues, which land in the backlog, select two and drag them into Sprint 15; the sprint
    section lists them in rank order and the backlog keeps the third. They move one back to the backlog. A selection of more than 50
    issues is refused whole, which is why the app sends batches of 50. They plan the third into the active sprint and drag its card to In
    Progress, which runs the column's transition. On the CASE1 kanban board, a new issue sits in the backlog column; Move to board runs the
    transition to the first board column, and the card leaves the backlog for the board. The board filter's JQL is there for the backlog
    fallback."""

    def steps(self, today: date):
        yield ListProjectBoards(query=BoardsOf("CASE"), by=MANAGER)
        yield ReadBoardConfiguration(BoardRef("CASE board"), by=MANAGER)
        yield ListBoardSprints(SprintsOf("CASE board"), by=MANAGER)
        yield ListSprintIssues(sprint_issues("Sprint 14", LABEL), by=MANAGER)
        yield ListBoardBacklog(backlog_of("CASE board", LABEL), by=MANAGER)

        first = task("Retention policy for audit records", labels=(LABEL,))
        second = story("Record who changed a case status and when", labels=(LABEL,))
        third = task("Upgrade the PDF renderer", labels=(LABEL,))
        yield CreateIssue(first, by=MANAGER)
        yield CreateIssue(second, by=MANAGER)
        yield CreateIssue(third, by=MANAGER)
        yield ListBoardBacklog(backlog_of("CASE board", LABEL), by=MANAGER)
        yield MoveToSprint(into_sprint("Sprint 15", first, second), by=MANAGER)
        yield ListSprintIssues(sprint_issues("Sprint 15", LABEL), by=MANAGER)
        yield ListBoardBacklog(backlog_of("CASE board", LABEL), by=MANAGER)
        yield MoveToBacklog(to_backlog(second), by=MANAGER)
        yield MoveToSprint(too_many("Sprint 16", first), by=MANAGER)
        yield ListSprintIssues(sprint_issues("Sprint 15", LABEL), by=MANAGER)

        yield MoveToSprint(into_sprint("Sprint 14", third), by=MANAGER)
        yield ListSprintIssues(sprint_issues("Sprint 14", LABEL), by=MANAGER)
        yield ListTransitions(transitions_of(third), by=MANAGER)
        yield RunTransition(transition(third, "In Progress"), by=MANAGER)
        yield ListSprintIssues(sprint_issues("Sprint 14", LABEL), by=MANAGER)

        yield ListProjectBoards(query=BoardsOf("CASE1"), by=MANAGER)
        yield ReadBoardConfiguration(BoardRef("CASE1 board"), by=MANAGER)
        yield ReadFilter(FilterRef("Filter for CASE1 board"), by=MANAGER)
        contrast = task("Check colour contrast on buttons", project="CASE1", labels=(LABEL,))
        yield CreateIssue(contrast, by=MANAGER)
        yield ListBoardBacklog(backlog_of("CASE1 board", LABEL), by=MANAGER)
        yield ListBoardIssues(board_issues("CASE1 board", ("To Do", "In Progress", "Done"), LABEL), by=MANAGER)
        yield ListTransitions(transitions_of(contrast), by=MANAGER)
        yield RunTransition(transition(contrast, "To Do"), by=MANAGER)
        yield ListBoardBacklog(backlog_of("CASE1 board", LABEL), by=MANAGER)
        yield ListBoardIssues(board_issues("CASE1 board", ("To Do", "In Progress", "Done"), LABEL), by=MANAGER)
