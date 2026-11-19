# How jira4manager maps onto Jira

jira4manager borrows Linear's look and Jira's model. The screens are dense, calm and keyboard-first, the way Linear's are. Every object on them is a Jira object, named the way Jira names it. A user who knows their Jira site recognises every word in the app.

The API facts behind this note, with their sources, are in [jira-work-model-research-2026-11-18.md](../milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md).

## The Jira world

A site such as `acme-labs.atlassian.net` holds many projects. Each project belongs to one team and has its own key, such as `CASE` for the intake team and `CASE1` for the portal team. The key prefixes every issue number: `CASE-131`, `CASE1-41`.

Each project carries its own configuration:

- **Issue types.** Most projects offer Bug, Story and Task at the standard level. Epic sits one level above them. Sub-tasks sit one level below. A project may add its own standard types, such as Improvement.
- **Workflow.** Each project has its own statuses, such as To Do, In Progress, In Review and Done. Jira puts every status in one of three categories: to do, in progress and done.
- **Board.** A board shows the project's issues in columns. The board configuration maps each column to one or more statuses. A scrum board shows the active sprint. A kanban board shows every issue that is not in its backlog.
- **Backlog.** On a scrum board, the backlog holds the open issues that are in no active or future sprint. On a kanban board with the backlog turned on, it holds the issues in the backlog column's statuses.
- **Epics.** An epic is an issue of type Epic. A Bug, Story or Task joins an epic through its `parent` field. The epic's progress is the share of its children whose status is in the done category.

Two projects on the same site can differ in every point above. `CASE` can run a scrum board with an In Review status. `CASE1` can run a kanban board with a backlog and no review step.

## The same world in jira4manager

The sidebar lists the site's projects. Under each project sit three views. Each view reads one part of that project's configuration.

| Jira | What it is in Jira | In jira4manager | The Linear idea it borrows |
| --- | --- | --- | --- |
| Site | One Jira Cloud instance, such as `acme-labs.atlassian.net` | The name at the top of the sidebar. One site per sign-in. | Workspace |
| Project (`CASE`, `CASE1`) | One team's space, with its own key, types, workflow, board and epics | A sidebar entry with Issues, Epics and Board under it | Team |
| Bug, Story, Task | Standard issue types, at hierarchy level 0 | Rows in Issues and cards on Board, each with its type icon. A type filter narrows both views. | Issue. Linear has no types, so the type icon is the one Jira concept the rows add. |
| Epic | An issue type one level above Bug, Story and Task | A row in Epics with a progress bar, and an epic chip on each child row and card | Project, with its progress bar |
| `parent` field | The link from a child issue to its epic | The Epic property of an issue, and Add existing and remove on an epic | An issue's project |
| Label | Free-text tags on an issue, shared across the site | Chips on rows and cards, a field in the create dialog and the detail pane that adds, removes and creates labels, and a label filter with any-of and all-of matching | Labels |
| Field and custom field | A value on an issue, such as Priority, Due date or a site's own Reviewer or QA engineer. Each project's create and edit screens decide which fields an issue type shows. | The create dialog lists the create screen's fields for the chosen type, with required ones marked. The detail pane lists the edit screen's fields. Each field edits by its kind. A kind the app cannot edit shows read-only with a lock. | Issue properties |
| Status and its category | The project's workflow steps, each in to do, in progress or done | Issues groups rows by status, in category order: in progress, then to do, then done. | Workflow states and their types |
| Transition | A move the workflow allows between two statuses | Changing the status, from the picker, the S key, or a drag on the board. Only the moves the workflow allows are offered. | Changing the state |
| Board and its columns | The board configuration, mapping each column to statuses | Board shows Jira's columns, in Jira's order. Dropping a card in a column runs a transition to that column's status. | Board view |
| Sprint | A time box on a scrum board, active or future | The active sprint's name and end date above a scrum board. In the Backlog tab, one section per active and future sprint, with dates, goal and counts. Issues move between sprints. The sprints themselves are created and started in Jira. | Cycle |
| Backlog | Open work in no sprint, or in the kanban backlog column | The last section of the Backlog tab, in Jira's rank order. Filters, multi-select and drag move issues into a sprint, or onto the board for kanban. | Backlog |
| Sub-task | An issue type one level below Bug, Story and Task | Not shown in release 1 | Sub-issue |

## Rules that follow from the mapping

1. **One project at a time.** Every view shows one project. No view in release 1 mixes issues from two projects.
2. **Jira's words, Jira's order.** The app shows the project's own status names, type names and board column names. It never renames them or invents a status.
3. **The project decides what is offered.** The type picker lists the types the project offers for creation. The status picker lists the transitions the workflow allows from the current status. The epic picker lists the project's open epics. The create dialog shows the fields of the project's create screen for the chosen type, and the detail pane shows the issue's edit screen.
4. **The board is a view of statuses.** A card's column is its status. A status mapped to no column does not appear on the board, though the issue still appears in Issues.
5. **An epic's progress is computed.** Jira has no progress endpoint. The app counts the epic's children by status category.
6. **What the app cannot do, the browser does.** Every issue has Open in browser. The app sends the user there when a description holds content it cannot edit, when a transition needs fields on a Jira screen, and when a field is of a kind the app cannot edit, such as a cascading select.
