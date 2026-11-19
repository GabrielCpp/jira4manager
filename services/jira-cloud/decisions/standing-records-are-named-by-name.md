story: none
date: 2026-11-19
elements: ProjectRecord, IssueTypeRecord, StatusRecord, BoardRecord, SprintRecord, FieldRecord
sources: docs/milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md, docs/milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md, docs/design/agent-test-environment.md

The book plays the same journeys on the local fake Jira and on the sandbox, and the two number their standing records apart. So the model names a standing record by what a person reads: a project by its key, a board and a sprint by name, a status and an issue type by project and name, a custom field as `cf[<name>]`. At each restore the surface reads the site with the app's own calls and learns each id under its name.

Company-managed projects share issue type and status ids, so an id cannot tell CASE's Bug from OPS's. The book reads those ids as opaque and compares a status by its name and category, and a type by its name and hierarchy level. The app does the same when it groups by category and tells epics from standard types.

The model starts with the world the seed builds, which is the mockup world FakeJira serves: CASE, company-managed with a scrum board and Sprints 14 to 16; CASE1, team-managed with a kanban board whose backlog is on; OPS, company-managed with a kanban board. The app never writes any of it.
