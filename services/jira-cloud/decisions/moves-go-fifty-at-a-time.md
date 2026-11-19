story: none
date: 2026-11-19
elements: MoveToSprint, MoveToBacklog
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md

A move into a sprint or to the backlog takes at most 50 issues a call, so the app sends a larger selection in batches of 50, and a move of 120 issues is three calls. Jira refuses a call that names more, and moves nothing.

The book shows the limit with one issue named 51 times. That way the run needs no 51 issues on the sandbox, where every write counts against the per-issue and burst limits. It assumes Jira counts the issues before it looks any of them up; QUESTIONS.md asks it, with the message.

A move keeps each issue's rank. A move into a closed sprint is refused too, but the seeded world has no closed sprint and the app offers only active and future ones, so the book holds no rule for it.
