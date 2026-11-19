story: none
date: 2026-11-19
elements: SearchIssues
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md

Jira has no endpoint for an epic's progress. The app searches the children of the visible epics in one query, `parent in (...)` with at most 100 keys, asking for their status alone, and counts them by status category. The book's epics journey reads that count before and after a child is done.

`ORDER BY status`, which the Child issues section sends, has no documented order; QUESTIONS.md asks it.
