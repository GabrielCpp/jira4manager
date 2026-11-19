---
type: milestone
id: J4M-01M7P8V07HWEFCWSJTH1C09D24
title: Issues, epics and the project board
status: proposed
dependsOn: []
sourceItems: []
epics: []
---
# Issues, epics and the project board

## Epics

## Outcome

A person who runs work in Jira Cloud opens a native desktop app, connects it to their site with an email and an API token, and manages one team's project at a time without a browser. They create and edit Bugs, Stories and Tasks, move them through the project's workflow, group them under epics, and work the project's board and backlog. The app is fast and keyboard-first, and it never freezes while Jira answers.

The app borrows Linear's look and keeps Jira's model. Each project keeps its own key, issue types, workflow, board, backlog and epics, and the app reads all of them from Jira. The mapping between the two is in [jira-work-model.md](../../design/jira-work-model.md). Anything the app cannot do yet stays one click away through Open in browser.

## Release Boundary

This is one milestone. It is complete when a user with a free Jira Cloud site can build the app on Linux, macOS or Windows, sign in, and do the four journeys below against two projects that differ in setup: a company-managed project with a scrum board and a team-managed project with a kanban board. CI must be green on all three systems.

The kickoff brief's M0 skeleton, M1 API client, M2 read-only UI and the parts of M3, M4 and M6 that issues, epics and boards need all land inside this milestone. None of them alone gives a user something they recognise.

The first story is a walking skeleton. It proves one journey end to end: the user enters a site, an email and a token, and the app checks them against `/rest/api/3/myself` and stores the token in the OS keychain. The app then lists the issues of the first project from `/rest/api/3/search/jql`. The user changes one issue's status through a transition, and the list shows the new status. Every crate in the dependency chain takes part in that first story, and it proves both a read and a write.

After the skeleton, the issue list, issue editing, issue creation, epics and the board may land in any order. Each later story widens one view.

## User Journeys

### Sign in to a Jira site

- services: desktop-app, jira-cloud

Mockup: [sign-in-to-a-jira-site.html](mockups/sign-in-to-a-jira-site.html)

1. On first launch, with no saved site, the app opens the sign-in screen.
2. The user enters a site. A bare name (`acme-labs`), a host (`acme-labs.atlassian.net`) and a full URL all resolve to the same site.
3. The user enters their email and pastes an API token. The screen links to where tokens are created and says that tokens expire.
4. The user presses Sign in. The button shows that the app is checking, and the window stays responsive.
5. The app calls `myself`. On success it saves the site URL and email to the config file and the token to the OS keychain. It then opens the first project's Issues view with a short confirmation naming the site and the user's display name.
6. On the next launch, the app reads the config file and the keychain and opens the last project and view without the sign-in screen.
7. Sign out, from the sidebar footer, deletes the keychain entry and returns to the sign-in screen.

Required states:

- Rejected credentials (401 or 403): an inline error says Jira rejected the email and token, and the token field is marked. The fields keep their values except the token.
- Unknown site (DNS failure, 404, or a host that is not a Jira Cloud site): an inline error names the site the app tried, and the site field is marked.
- Offline or timeout: an inline error says the site could not be reached. Nothing is saved.
- Token rejected later: when any request returns 401 after sign-in, the app returns to the sign-in screen with the site and email filled in and a message that the token stopped working. The rejected token is removed from the keychain.
- Keychain unavailable: the app says it cannot store the token and does not fall back to writing it to disk.

### Manage issues in a project

- services: desktop-app, jira-cloud

Mockup: [manage-issues-in-a-project.html](mockups/manage-issues-in-a-project.html)

1. The sidebar lists every project the user can browse. Each project expands to Issues, Epics and Board.
2. Issues shows the project's open issues at the standard level, Bug, Story, Task and any other standard type the project offers, grouped by status. Groups follow status category order: in progress, then to do, then done. Inside a group, issues sort by priority. Group headers collapse on click.
3. Each row shows priority, key, status, type, summary, the epic as a chip, the assignee and the time since the last update. A click on the epic chip opens the epic.
4. A type filter narrows the list to one type. An epic filter narrows it to one epic or to issues with no epic. A toggle shows done issues. The count at the right shows the JQL the view runs as a tooltip.
5. J and K, or the arrow keys, move the selection. Enter opens the issue in the detail pane. Esc closes it.
6. C, or the New issue button, opens the create dialog for the current project. The user picks a type from the types the project offers, writes a summary, a Markdown description, a priority, an assignee and an epic, and presses Create or Ctrl+Enter. The new issue appears in the list, and a toast names its key with an Open action. When the list is filtered to one epic, the dialog starts with that epic chosen.
7. In the detail pane, a click on the title edits it in place. Enter saves and Esc cancels.
8. The description's Edit button opens a Markdown editor with Write and Preview tabs. Save, or Ctrl+Enter, sends the description to Jira as ADF.
9. Status, assignee, priority and epic each open a picker, from the properties column or with the S, A, P and E keys. The status picker lists only the statuses the workflow allows from the current one. The assignee picker lists the people who can be assigned in the project. The epic picker lists the project's open epics and None.
10. Every change shows at once and is marked as saving until Jira confirms it.
11. Open in browser opens `https://<site>/browse/<KEY>`.

Required states:

- First load: skeleton rows while the first page arrives.
- Empty project: the list says the project has no open issues and offers New issue.
- Filtered to nothing: the list says no issue matches and offers Clear filters.
- Fetch error: the list says the issues could not be loaded, names the HTTP status, and offers Try again.
- Write rejected: when Jira refuses an edit, the change is undone, and a toast names the issue and the HTTP status.
- Transition needs a screen: when the chosen transition needs fields on a Jira screen that the app does not show, such as Resolution, the status stays as it was. A toast names the field and offers to finish in the browser.
- Description the app cannot edit: when the description holds a node outside the editable subset, such as a panel, a table or an image, the description renders with a placeholder for each such node. Edit is replaced by a note naming those nodes and pointing to the browser.
- Create fails: the dialog stays open with the user's text, and an inline error names the HTTP status. Nothing is created twice.
- Create needs more fields: when the project requires a field on create that the dialog does not show, the dialog names the field and offers to create the issue in the browser.

### Manage epics in a project

- services: desktop-app, jira-cloud

Mockup: [manage-epics-in-a-project.html](mockups/manage-epics-in-a-project.html)

1. Epics lists the project's open epics, grouped by status like Issues. A toggle shows done epics.
2. Each row shows the epic's key, status, summary, a progress bar and "n of m" done, the assignee and the time since the last update. The bar splits the children into done and in progress by status category.
3. Enter or a click opens the epic in the detail pane. The pane shows the summary, the description and a Child issues section with the progress bar and one row per child: type, key, status, summary and assignee.
4. Add existing opens a picker of the project's open Bugs, Stories and Tasks that are not in this epic. A child of another epic shows which epic it leaves. Picking one sets its parent to this epic.
5. Each child row has a remove action that clears the child's parent. A click on a child row opens that child.
6. New child issue opens the create dialog with this epic chosen and the Epic type left out.
7. New epic, or C in the Epics view, opens the create dialog with the Epic type chosen.
8. The epic's title, description, status, assignee and priority edit the same way as an issue's.

Required states:

- No epics: the view explains what an epic groups and offers New epic.
- Epic with no children: the Child issues section says so and offers Add existing and New child issue.
- Child change rejected: the child returns to where it was, and a toast names the issue.
- Done epics hidden: done epics appear only when the toggle is on.

### Work on the project board

- services: desktop-app, jira-cloud

Mockup: [work-on-the-project-board.html](mockups/work-on-the-project-board.html)

1. Board shows the project's Jira board with the board's own columns, in the board's order. Each column header shows its name and its card count.
2. A scrum board shows the issues of the active sprint, with the sprint's name and end date above the columns. A kanban board shows the issues that are not in its backlog.
3. Each card shows type, key, assignee, summary, priority and the epic as a chip. The type and epic filters from Issues apply here too.
4. Dragging a card to another column changes its status to the column's first status. Arrow keys or H, J, K and L move the card selection, and Shift with Left or Right moves the selected card one column. Enter opens the card in the detail pane.
5. A move the workflow does not allow snaps back, and a toast says which move is missing.
6. The Backlog tab lists the backlog in Jira's rank order. On a scrum board, each row offers Move to the active sprint. On a kanban board, it offers Move to board, which changes the status to the first board column's status.
7. When the project has several boards, a picker above the columns switches between them. The app remembers the choice per project.

Required states:

- First load: skeleton rows while the board arrives.
- Scrum board with no active sprint: the board says no sprint is active and points to the browser to start one. The Backlog tab still works.
- Board without a backlog: a kanban board with its backlog turned off shows no Backlog tab.
- Empty backlog: the tab says every open issue is on the board or in the sprint.
- Project with no board: Board says the project has no board and points to the browser.
- Transition needs a screen: the card returns to its column, and the toast offers to finish in the browser.
- Fetch error: the board says it could not be loaded and offers Try again.

## Architecture Decisions

- **Crate boundary.** The workspace holds `jira-api`, `adf`, `core` and `app`, with dependencies only in the direction `app → core → (jira-api, adf)`. `jira-api` and `adf` never depend on GPUI. `core` never depends on GPUI. This keeps the client, the converter and the state usable from tests and a CLI without a window.
- **One API seam.** `jira-api` defines the `JiraApi` trait, with `HttpJira` for the network and `FakeJira` seeded from `fixtures/`. `core` and `app` take the trait, so every UI and core test runs against `FakeJira`. The trait grows only the methods these journeys call, and `FakeJira` implements each one with the same workflow rules as a real project, including forbidden transitions.
- **Jira's model, not Linear's.** The app's domain types are Jira's: site, project, issue type with its hierarchy level, status with its category, transition, board with its columns, sprint and epic. The UI shows Jira's own names for each and never invents a status or a type. [jira-work-model.md](../../design/jira-work-model.md) holds the full mapping.
- **One project at a time.** Every view is scoped to one project key. Nothing in this release merges data from two projects.
- **Project configuration is read, never assumed.** The app reads a project's statuses from `/rest/api/3/project/{key}/statuses`, its creatable types from `/rest/api/3/issue/createmeta/{key}/issuetypes`, and each type's create fields from `/rest/api/3/issue/createmeta/{key}/issuetypes/{id}`, paging through both. The deprecated `GET /rest/api/3/issue/createmeta` with `expand` is never called. Standard types are those with hierarchy level 0, and epics are hierarchy level 1. Sub-tasks, at level -1, are left out.
- **Epic link.** A child joins an epic through `fields.parent` on create and edit, in both company-managed and team-managed projects. Removing it sends `update.parent.set.none`. The deprecated Epic Link and Parent Link fields and the agile `epic/{key}/issue` calls are never used, because they fail for team-managed projects. Children are found with JQL `parent = KEY`.
- **Epic progress is computed.** Jira has no progress endpoint. `core` loads the children of the visible epics in one search with `parent in (...)` and counts them by status category.
- **Epic Name.** On create, the app sends Epic Name only when the project's create metadata marks it required, and fills it with the summary. The field became optional in 2023, but some sites may still require it.
- **Status categories.** Grouping follows the status category key: in progress, then to do, then done. A status with an unknown or missing category sorts after to do and before done. The keys are observed behaviour and no official page lists them.
- **Transitions.** A status change reads `/rest/api/3/issue/{key}/transitions?expand=transitions.fields` and runs the transition whose target is the chosen status. When that transition has a required field without a default, the app does not run it and sends the user to the browser instead. A board drop picks the first status of the target column that has an available transition.
- **Board data.** Boards come from `/rest/agile/1.0/board?projectKeyOrId=KEY` and their columns from `/rest/agile/1.0/board/{id}/configuration`. The active sprint comes from `/rest/agile/1.0/board/{id}/sprint?state=active`. Board, sprint and backlog issues come from the token-paged `/rest/software/1.0/board/{id}/issue`, `/rest/software/1.0/sprint/{id}/issue` and `/rest/software/1.0/board/{id}/backlog`. Atlassian deprecated the `/rest/agile/1.0/` issue lists in 2026. Moving into a sprint uses `POST /rest/agile/1.0/sprint/{id}/issue`. Whether the backlog call works on a kanban board is unconfirmed, so the first board story checks it on the live site and records the result in `docs/ARCHITECTURE.md`. If it fails, the app reads the kanban backlog through the board's filter and the statuses of its backlog column.
- **Search endpoint.** Issue lists and epic children use `POST /rest/api/3/search/jql` with `nextPageToken`. The removed `/rest/api/3/search` is never called. Counts come from the loaded issues.
- **Pages and cap.** A view loads pages of 100 until the last page or until it holds 1,000 issues, and requests only the fields a row or card needs. Grouping needs the whole view in memory, and the cap keeps a large project from blocking the first paint.
- **Async runtime.** `core` owns a multi-threaded tokio runtime on its own threads, with `reqwest` and rustls. The app sends commands to `core` and awaits the results on GPUI's foreground executor through runtime-agnostic channels. No Jira call runs on the UI thread.
- **Optimistic writes.** `core` applies an edit, a transition, a parent change or a sprint move to its cached state at once and marks the issue as saving. When Jira refuses it, `core` restores the previous value and reports the error. A create is not optimistic: the issue appears once Jira returns its key.
- **Retries.** On 429 with `Retry-After`, `HttpJira` retries GET requests, the search POST and PUT edits, which set fields to values. It waits at least `Retry-After`, backs off exponentially with jitter, and gives up after 4 attempts. It never retries a create, a transition or a sprint move on its own, because a repeat could duplicate an issue or move it twice.
- **Session cache.** `core` keeps the last result of each view in memory and renders it first on revisit, then refreshes. Nothing is persisted to disk except the config file.
- **ADF.** `adf` deserializes the whole document into serde enums with an `Unknown(serde_json::Value)` variant, so nothing is dropped on read. It converts the editable subset both ways with `comrak`: paragraph, headings, bullet, ordered and task lists, code blocks with their language, block quotes, rules, hard breaks, the strong, em, code, strike and link marks, and mentions. A document that holds any node outside the subset renders with placeholders and stays read-only. This release does not splice unknown nodes back into saved ADF, so no save can erase them.
- **Credentials.** The token lives only in the OS keychain through the `keyring` crate. The config file, found with the `directories` crate, holds the site URL, the email, the last project and view, and the chosen board per project. Auth is HTTP Basic with an unscoped API token against the site URL.
- **Identity.** Users are identified by `accountId` everywhere, including assignees and mentions. Assignee pickers use `/rest/api/3/user/assignable/search` with the project or the issue key.
- **UI toolkit pins.** The app depends on gpui-component and its GPUI from crates.io with exact `=` versions. The chosen versions and the reason live in `docs/DEPENDENCIES.md`. An upgrade is its own commit.
- **Design tokens.** The theme takes its colours, spacing and density from the mockups' CSS variables. It has dark and light themes, one accent colour, subtle borders and 36 px compact rows. The fonts are the platform's UI font and a monospace font.
- **App name.** The name `jira4manager` lives in the workspace metadata and one `APP_NAME` constant.

## Compatibility Sources

- Behavioural oracle: Jira Cloud as documented on developer.atlassian.com, and a free Jira Cloud site for live tests. The API facts behind this milestone, with sources and read dates, are in [platform-research-2026-11-17.md](artifacts/platform-research-2026-11-17.md) and [jira-work-model-research-2026-11-18.md](artifacts/jira-work-model-research-2026-11-18.md). Facts marked UNCONFIRMED there are checked on the live site by the story that first depends on them.
- Domain mapping: [jira-work-model.md](../../design/jira-work-model.md) defines how each Jira concept appears in the app.
- Product brief: [kickoff-brief.md](../../kickoff-brief.md). Where it and the research disagree, the research wins. Known differences: `InputState::multi_line()` no longer exists in gpui-component, gpui-component pins `gpui-pre` from crates.io, and the agile board issue lists the brief implies are deprecated.
- Look and interaction: this milestone's mockups, and the earlier exploration [tracker-mockup.html](../../mockups/tracker-mockup.html) for visual tone only. The exploration's cycles, command palette and cross-project views are not part of this release.

## Constraints

- Native only. GPUI and gpui-component draw every pixel. No webview, Tauri, Electron or embedded browser, including for Markdown.
- Writes to Jira are limited to: create issue, edit the summary, description, assignee, priority and parent, run a transition, and move an issue into a sprint. No other request changes data on the site.
- No save may erase content. A description that holds a node outside the editable subset is never sent back to Jira.
- Every view and every write is scoped to one project. The app never moves an issue between projects.
- The API token never appears in the config file, logs, `Debug` output, panic messages, fixtures or test snapshots. The `Authorization` header is redacted wherever requests are logged, and a test proves it.
- No network call runs on the UI thread, and the window keeps handling input while any request is in flight.
- Fixtures under `fixtures/` contain no real email, display name, accountId or site URL.
- Live tests run only with `cargo test --features live -- --ignored` and the `JIRA_SITE`, `JIRA_EMAIL` and `JIRA_TOKEN` variables. CI never runs them. Live tests that write create their issues in a sandbox project and leave every other project untouched.
- Every dependency carries a licence compatible with GPL-3.0-or-later.
- `cargo fmt --check`, `cargo clippy -- -D warnings` and `cargo test` pass on Linux, macOS and Windows in CI.
- No Atlassian or Linear logo, icon or font appears in the app. "Jira" appears only in referential text, such as "Connect your Jira site".

## Acceptance

- CI runs format, clippy with warnings denied, and tests on Linux, macOS and Windows, and all three pass.
- The repository holds the GPL-3.0 `LICENSE`, a README with the build dependencies per OS and the "Linear-inspired" disclaimer, and `docs/ARCHITECTURE.md`, `docs/DEPENDENCIES.md` and `docs/ADF.md`.
- wiremock tests prove: the Basic auth header shape, the search body, pagination across at least three pages by `nextPageToken`, the 1,000-issue cap, a 429 retried after `Retry-After` on a read and on an edit, giving up after 4 attempts, and no retry of a create or a transition after a 429.
- wiremock tests prove the request shape of create with a parent, edit, clearing a parent with `update.parent.set.none`, a transition by id, and a move into a sprint.
- A test proves the token never appears in logged request output.
- The sign-in journey works against a live site: a valid token opens the last project, a wrong token shows the rejected error, an unknown site shows the site error, a relaunch skips sign-in, and Sign out removes the keychain entry.
- Against a live company-managed project with a scrum board and a live team-managed project with a kanban board, a reviewer can: create a Bug, a Story, a Task and an Epic; edit a summary and a description; change status, assignee, priority and epic; add an issue to an epic and remove it; drag a card across the board; and move a backlog issue onto the board. Each change shows in Jira's web UI afterwards.
- With `FakeJira` refusing a write, a GPUI test shows the change undone and the error shown. With `FakeJira` requiring a field on a transition, a test shows the status unchanged and the browser offered.
- A board test against `FakeJira` shows a forbidden move snapping back with its reason.
- An epic's progress bar matches its children's status categories, and adding or removing a child updates it.
- Golden tests in `fixtures/adf/` pin ADF to Markdown and Markdown to ADF for every node in the editable subset, and round-trip tests show ADF to Markdown to ADF is identical for that subset.
- An issue whose description holds a panel, a table and an image renders a placeholder for each in document order, offers no Edit, and sends no description in any request.
- The live check of the kanban backlog call is recorded in `docs/ARCHITECTURE.md` with the path the app takes.
- With `FakeJira` delaying every response, a GPUI test shows the skeleton state and shows the window still handles input during the delay.
- Dark and light themes both render every screen above.

## Non-Goals

- Comments, reading or writing.
- Labels, components, fix versions, due dates, story points and custom fields beyond what create requires.
- Sub-tasks, and changing an issue's type.
- Cross-project views: My issues, saved views, free-form JQL and search across projects.
- Sprint planning: creating, starting or completing a sprint, and moving issues between future sprints.
- Ranking the backlog or the board by drag.
- Board swimlanes, WIP limits and quick filters.
- Splicing unknown ADF nodes back into a saved description. Those descriptions stay read-only.
- Moving an issue to another project, and epics whose children live in other projects being managed from here.
- The command palette, rate-limit and offline banners, and a persistent cache.
- Several sites or accounts at once, scoped API tokens, and OAuth 2.0 sign-in.
- Jira Data Center or Server.
- The `xtask record` fixture recorder. Fixtures in this release are scrubbed by hand.
