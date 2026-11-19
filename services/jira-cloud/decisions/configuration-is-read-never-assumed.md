story: none
date: 2026-11-19
elements: ReadProjectStatuses, ListProjectBoards, ListBoardSprints, ReadIssue, FindAssignableUsers, FindUsers
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/milestone.md

The app keeps no list of statuses, boards, sprints, field names or people. It reads each project's statuses with their categories, its boards, each board's active and future sprints, and an issue's fields with their names, schemas and edit metadata in one read of `fields=*all&expand=names,schema,editmeta`. The book reads the same calls and compares what the seeded world fixes: status names and categories, board names and types, sprint names, states and goals, and the values of the fields a journey set.

People are known by account id. The Assignee picker reads only who may be assigned the issue or the project, and any other user field reads everyone on the site, so Jira can still refuse a person a field limits to some groups. The book knows one person, the standing account, and finds it by its name in both searches. Other people's rows drop out of the comparison, because the environment names its accounts.

The detail read's names, schemas and edit metadata are maps over every field of the site, which may hold fields the mockup world leaves out. The book leaves them to the site and checks the create screens field by field instead.
