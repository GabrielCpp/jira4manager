story: none
date: 2026-11-19
elements: LabelRecord, ListLabels, SearchIssues, ListSprintIssues, ListBoardIssues, ListBoardBacklog, CreateIssue, EditIssue
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md, docs/design/agent-test-environment.md

Every issue the book makes carries a label of its journey, and every label is minted per run. Each search and board list the book sends is the app's query narrowed with `labels = <label>`. The sandbox holds the seeded issues and every earlier run's issues, so a run finds what it made by its label and never counts a list other people write to. This is the live tests' own rule: they label the issues they make with `j4m-live` and the run's id.

A label exists once an issue carries it. Jira has no call that creates one, so the label list grows by the creates and edits that send a new string. That implicit creation is UNCONFIRMED on an official page; QUESTIONS.md asks it. Labels change through `update.labels` with one add or remove each, so two people editing labels at once keep both changes.
