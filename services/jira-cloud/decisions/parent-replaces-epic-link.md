story: none
date: 2026-11-19
elements: CreateIssue, EditIssue, SearchIssues, IssueRecord
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md

A child joins its epic through the parent field, on create as `fields.parent.key` and on edit the same way, and leaves it through `update.parent` set to none. Children are found with the JQL `parent = KEY` or `parent in (...)`.

Atlassian deprecated the Epic Link and Parent Link fields in 2021 and took them out of createmeta and editmeta. The agile calls that move issues into an epic or out of one do not work for team-managed projects. The parent field works in both project styles, so the book plays the epics journey on CASE1, a team-managed project, to show that one path serves both.

The exact shape that clears a parent is UNCONFIRMED; QUESTIONS.md asks it.
