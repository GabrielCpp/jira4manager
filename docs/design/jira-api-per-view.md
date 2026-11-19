# The Jira calls behind each view

This note lists every Jira Cloud request the release 1 app makes, view by view. Each view of the [milestone mockups](../milestones/0001-issues-epics-and-board/mockups/) appears here with the reads that draw it and the writes its actions send. A coder builds `jira-api`, `FakeJira` and the wiremock tests from this list. A request that appears nowhere here is a request the app must not make.

The facts behind each call, with their Atlassian sources, are in three research notes:

- [platform-research-2026-11-17.md](../milestones/0001-issues-epics-and-board/artifacts/platform-research-2026-11-17.md): auth, search, rate limits.
- [jira-work-model-research-2026-11-18.md](../milestones/0001-issues-epics-and-board/artifacts/jira-work-model-research-2026-11-18.md): epics, statuses, transitions, boards and sprints.
- [jira-fields-research-2026-11-18.md](../milestones/0001-issues-epics-and-board/artifacts/jira-fields-research-2026-11-18.md): create and edit metadata, field kinds, value shapes, user and label search.

A call marked UNCONFIRMED rests on a fact no official page states. The first story that makes the call checks it on the sandbox site and records the result in `docs/ARCHITECTURE.md`.

## Conventions every call follows

- **Base URL.** `https://<site>.atlassian.net`. In tests, `jira-api` takes any base URL, so wiremock and the local fake Jira answer on `http://127.0.0.1:<port>`.
- **Auth.** HTTP Basic with the email and API token, and `Accept: application/json` on every request. The token never reaches a log.
- **Two paging styles.** Token paging sends `nextPageToken` and stops when the answer has `isLast` set to true or holds no token. It applies to `POST /rest/api/3/search/jql` and the `/rest/software/1.0/` issue lists. Offset paging sends `startAt` and `maxResults` and stops on `isLast` or when `startAt + values` reaches `total`. It applies to every other list.
- **Page size.** Issue lists ask for 100 issues a page and stop at 1,000. createmeta asks for 200 fields a page, its maximum. User and label searches ask for 50.
- **Issue fields.** A list requests only the fields its rows or cards show. These are the row fields: `summary`, `status`, `issuetype`, `priority`, `assignee`, `parent`, `labels` and `updated`. A list of sprint or backlog issues adds the Sprint field's id.
- **Batches.** A sprint move or a backlog move sends at most 50 issues a call. A `parent in (...)` search sends at most 100 keys a query.
- **Retries.** On 429 with `Retry-After`, `HttpJira` retries GET requests, the search POST and PUT edits up to 4 times. It never retries a create, a transition or a move.
- **Errors.** A 4xx answer is read as `{"errorMessages": [...], "errors": {"<fieldId>": "..."}}`. Field errors go to their fields and the rest to the view's error.

## Session

| When | Request | What it gives the view |
| --- | --- | --- |
| Sign in, and each launch | `GET /rest/api/3/myself` | The user's `accountId` and display name for the sidebar footer and the confirmation. A 401 or 403 means rejected credentials. |
| After sign-in | `GET /rest/api/3/project/search?startAt=0&maxResults=100&orderBy=name` | The sidebar's projects: `key`, `name`, `id`, `style` and `simplified`. The app pages until `isLast`. |
| First Labels picker of the session | `GET /rest/api/3/label?startAt=0&maxResults=1000` | The site's labels for the label field. Typing narrows them with `query`. |

## Project configuration

The app reads these once per project, the first time any of its views opens, and keeps them for the session. Refresh reads them again.

| Request | What it gives |
| --- | --- |
| `GET /rest/api/3/project/{key}/statuses` | Each issue type's statuses with their categories. Issues groups by category. The status filter and the status picker list these names. |
| `GET /rest/api/3/issue/createmeta/{key}/issuetypes` | The types the user can create, with their ids and `hierarchyLevel`. Level 0 types fill the type filter and the create dialog. Level 1 types are the epic types. UNCONFIRMED: that each item carries `hierarchyLevel`. If it does not, `GET /rest/api/3/issuetype/project?projectId={id}` supplies it. |
| `GET /rest/agile/1.0/board?projectKeyOrId={key}` | The project's boards: `id`, `name` and `type`. Several boards turn the board line into a picker. |
| `GET /rest/agile/1.0/board/{boardId}/configuration` | The columns with their statuses, the board filter's id, and the estimation field. A kanban board's "Backlog" column holds its backlog statuses. |
| `GET /rest/agile/1.0/board/{boardId}/sprint?state=active,future` | The sprints of a scrum board, with `name`, `state`, `startDate`, `endDate` and `goal`. They fill the header line, the sprint sections and every sprint picker. |

## Issues view

| When | Request | What it gives |
| --- | --- | --- |
| Open | `POST /rest/api/3/search/jql` with `jql: project = CASE AND issuetype in (<level 0 type ids>) AND statusCategory != Done ORDER BY priority DESC, updated DESC` and the row fields | The rows, grouped and filtered locally. |
| Open | `POST /rest/api/3/search/jql` with `jql: project = CASE AND issuetype in (<level 1 type ids>) ORDER BY updated DESC` and `summary`, `status` | The epic chips on rows, and the values of the epic filter picker. |
| Show done issues | The first search with `statusCategory = Done` and `updated >= -30d` | Done rows, under the same 1,000 cap. |
| Refresh | The reads above, again | Fresh rows. The previous rows stay on screen until the answer arrives. |

The filter bar sends no request. Picker values and counts come from the loaded rows, the project statuses and the epic list. The JQL tooltip is text the app builds and never sends.

## Epics view

| When | Request | What it gives |
| --- | --- | --- |
| Open | `POST /rest/api/3/search/jql` with `jql: project = CASE AND issuetype in (<level 1 type ids>) AND statusCategory != Done ORDER BY updated DESC` and the row fields | The epic rows. |
| Open | `POST /rest/api/3/search/jql` with `jql: parent in (<epic keys>)` and `status` only | The progress bars, counted by status category. Up to 100 keys per query. |
| Show done epics | The first search with `statusCategory = Done` | Done epics, with their children counted the same way. |

## Detail pane

| When | Request | What it gives |
| --- | --- | --- |
| Open an issue | `GET /rest/api/3/issue/{key}?fields=*all&expand=names,schema,editmeta` | The values of every field, each field's display name and schema, and the edit screen's fields with their `allowedValues` and `operations`. This one call draws the title, description, paragraph fields and the properties column. |
| Open an epic | `POST /rest/api/3/search/jql` with `jql: parent = KEY ORDER BY status` and the row fields | The Child issues section and its progress bar. |
| Status picker opens, or S | `GET /rest/api/3/issue/{key}/transitions?expand=transitions.fields` | The statuses the workflow allows from here, and each transition's required screen fields. |
| Assignee picker, typing | `GET /rest/api/3/user/assignable/search?issueKey={key}&query=<text>&maxResults=50` | People who can be assigned this issue. |
| Other user field picker, typing | `GET /rest/api/3/user/search?query=<text>&maxResults=50` | People on the site. Jira can still refuse one when the field is limited to some groups. |
| Labels picker, typing | `GET /rest/api/3/label?query=<text>&maxResults=50` | Matching labels. A new string becomes a new label when saved. UNCONFIRMED: implicit creation and the no-spaces rule. |
| Select, multi-select, priority, components, versions | none | The options come from `allowedValues` in the issue's `editmeta`. |
| Epic picker | none | The project's open epics, from the epic list already loaded. |
| Sprint picker | none | The board's active and future sprints, from project configuration. |

Writes from the detail pane:

| Action | Request |
| --- | --- |
| Edit the title, description, a paragraph or text field, a number, a date, a user, a select, a multi-select, priority, components or versions | `PUT /rest/api/3/issue/{key}` with `fields: {<fieldId>: <value>}`, in the value shape the field research lists. Description and paragraph fields send ADF. Answers 204. |
| Add or remove labels | `PUT /rest/api/3/issue/{key}` with `update: {labels: [{add: "x"}]}` or `{remove: "x"}`. |
| Set the epic | `PUT /rest/api/3/issue/{key}` with `fields: {parent: {key: "CASE-100"}}`. |
| Clear the epic | `PUT /rest/api/3/issue/{key}` with `update: {parent: [{set: {none: true}}]}`. UNCONFIRMED: this exact shape. |
| Change status | `POST /rest/api/3/issue/{key}/transitions` with `transition: {id}`. Answers 204. A transition with a required field and no default is not sent, and the browser is offered. |
| Pick a sprint | `POST /rest/agile/1.0/sprint/{sprintId}/issue` with `issues: [key]`, or `POST /rest/agile/1.0/backlog/issue` for Backlog. |
| Add existing child, remove a child | `PUT /rest/api/3/issue/{childKey}` setting or clearing `parent`, one call per child. |
| After any write | `GET /rest/api/3/issue/{key}?fields=<the changed field>,updated` | Confirms the value Jira kept and the new `updated` time. |

## Create dialog

| When | Request | What it gives |
| --- | --- | --- |
| A type is chosen the first time this session | `GET /rest/api/3/issue/createmeta/{key}/issuetypes/{typeId}?startAt=0&maxResults=200` | The create screen's fields in order, with `required`, `schema`, `allowedValues`, `hasDefaultValue` and `defaultValue`. The app pages until `total`. |
| A user, label, select or epic field opens | The same reads as the detail pane, with `project={key}` in place of `issueKey` for the assignee | The picker's options. |
| Create | `POST /rest/api/3/issue` with `fields: {project: {key}, issuetype: {id}, summary, description (ADF), <each filled field>}` | Answers 201 with `id` and `key`. A 400 maps `errors` to fields and `errorMessages` to the dialog. |
| After 201 | `GET /rest/api/3/issue/{key}?fields=<row fields>` | The new row, inserted into the open view. |

The dialog sends Epic Name only when createmeta lists it as required. It sends the Sprint field only when the create screen holds it. The app finds the Sprint field by `schema.custom` `com.pyxis.greenhopper.jira:gh-sprint`, never by name.

## Board view

| When | Request | What it gives |
| --- | --- | --- |
| Open a scrum board | `GET /rest/software/1.0/sprint/{activeSprintId}/issue?fields=<row fields>&maxResults=100` | The cards of the active sprint, in rank order. |
| Open a kanban board | `GET /rest/software/1.0/board/{boardId}/issue?jql=status in (<statuses of the visible columns>)&fields=<row fields>&maxResults=100` | The cards outside the backlog. UNCONFIRMED: whether the board's kanban sub-filter applies to this list. |
| Drop a card on a column | `GET /rest/api/3/issue/{key}/transitions?expand=transitions.fields`, then `POST /rest/api/3/issue/{key}/transitions` | The transition to the first status of the column that has one. |
| Switch boards | The configuration and sprint reads for the chosen board, then its issues | The other board's columns and cards. |

## Backlog tab

| When | Request | What it gives |
| --- | --- | --- |
| Open on a scrum board | `GET /rest/software/1.0/sprint/{sprintId}/issue?fields=<row fields>` for each active and future sprint | One section per sprint, in rank order. |
| Open on a scrum board | `GET /rest/software/1.0/board/{boardId}/backlog?fields=<row fields>` | The Backlog section. |
| Open on a kanban board | `GET /rest/software/1.0/board/{boardId}/backlog?fields=<row fields>` | The backlog rows. UNCONFIRMED: a community report says this answers 400 on kanban. The fallback reads the board filter with `GET /rest/api/3/filter/{filterId}` and searches `(<filter jql>) AND status in (<backlog column statuses>)`. The first board story settles which path runs. |
| Move to a sprint, by drag, menu or M | `POST /rest/agile/1.0/sprint/{sprintId}/issue` with `issues: [...]`, at most 50 a call | Answers 204. A refused batch rolls the whole move back. |
| Move to the backlog | `POST /rest/agile/1.0/backlog/issue` with `issues: [...]`, at most 50 a call | Answers 204. |
| Move to board, kanban | The transition reads and write of the board drop | The issue's status becomes the first board column's status. |

## Requests the app never makes

- `GET /rest/api/3/search` and `GET /rest/api/3/issue/createmeta` with `expand`. Both are removed or deprecated.
- `/rest/agile/1.0/board/{id}/issue`, `/board/{id}/backlog` and `/sprint/{id}/issue`. The `/rest/software/1.0/` lists replace them.
- `/rest/agile/1.0/epic/...` calls, the Epic Link and Parent Link fields, and Rank. Rank is internal to Jira Software.
- Any request that creates or edits a project, a board, a sprint, a field, a screen or a version.
