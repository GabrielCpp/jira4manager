story: none
date: 2026-11-19
elements: ListSprintIssues, ListBoardIssues, ListBoardBacklog, ReadBoardConfiguration, ReadFilter, BoardRecord
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md

The board's cards, a sprint's issues and the backlog come from `/rest/software/1.0/`, which RFC-127 introduced in 2026 to replace the deprecated `/rest/agile/1.0/` issue lists. Each answers in rank order. A scrum board shows its active sprint, and its backlog is the open issues in no active or future sprint. A kanban board with its backlog on keeps the statuses of its first column, Backlog, out of the board, and its backlog list holds exactly those.

Whether the backlog list answers for a kanban board is UNCONFIRMED: a community report says it answers 400. The book claims it answers, so the first live run settles it. If it does not, the app reads the board filter's JQL and searches it narrowed to the backlog column's statuses, which is why the book reads the filter.
