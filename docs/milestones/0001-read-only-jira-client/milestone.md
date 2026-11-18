---
type: milestone
id: J4M-01M7P8V07HWEFCWSJTH1C09D24
title: Read-only Jira desktop client
status: proposed
dependsOn: []
sourceItems: []
epics: []
---
# Read-only Jira desktop client

## Epics

## Outcome

A person who works in Jira Cloud opens a native desktop app, connects it to their site with an email and an API token, and reads their work without a browser. They see the issues assigned to them and the issues of any project, grouped by status, and open one to read its description and comments. The list and the detail pane are driven from the keyboard, and the app never freezes while Jira answers.

This release replaces nothing on the user's side yet. It proves the whole stack on a real site: the GPUI shell, the Jira client, the ADF reader and the credential store. Every later release adds writes on top of it. Nothing in this release changes data on the user's Jira site.

## Release Boundary

This is one milestone. It is complete when a user with a free Jira Cloud site can build the app on Linux, macOS or Windows, sign in, browse their issues and projects, and read any issue, with CI green on all three systems.

The kickoff brief's M0 (skeleton), M1 (API client and fakes) and M2 (read-only UI) all land inside this milestone. M0 and M1 alone give a user nothing to recognise, so they are internal steps of this release and not releases of their own.

The first story is a walking skeleton. It proves one journey end to end: the user enters a site, an email and a token, the app checks them against `/rest/api/3/myself`, stores the token in the OS keychain, and shows the user's open assigned issues from `/rest/api/3/search/jql` in a plain list. Every crate in the dependency chain takes part in that first story.

The command-line example that prints "My open issues" against a real site may land before the window shows them. The sidebar, grouping, detail pane, Markdown rendering and the loading, empty, error and rate-limit states may land incrementally after the skeleton.

The kickoff brief asks for a stop for review after M1. That review point is the moment the walking skeleton passes, not a separate release.

## User Journeys

### Sign in to a Jira site

- services: desktop-app, jira-cloud

Mockup: [sign-in-to-a-jira-site.html](mockups/sign-in-to-a-jira-site.html)

1. On first launch, with no saved site, the app opens the sign-in screen.
2. The user enters a site. A bare name (`acme-labs`), a host (`acme-labs.atlassian.net`) and a full URL all resolve to the same site.
3. The user enters their email and pastes an API token. The screen links to where tokens are created and says that tokens expire.
4. The user presses Sign in. The button shows that the app is checking, and the window stays responsive.
5. The app calls `myself` with HTTP Basic auth. On success it saves the site URL and email to the config file, saves the token to the OS keychain, and opens My issues with a short confirmation naming the site and the user's display name.
6. On the next launch, the app reads the config file and the keychain and opens My issues without the sign-in screen.
7. Sign out, from the sidebar footer, deletes the keychain entry and returns to the sign-in screen.

Required states:

- Rejected credentials (401 or 403): an inline error says Jira rejected the email and token, and the token field is marked. The fields keep their values except the token.
- Unknown site (DNS failure, 404, or a host that is not a Jira Cloud site): an inline error names the site the app tried, and the site field is marked.
- Offline or timeout: an inline error says the site could not be reached. Nothing is saved.
- Token rejected later: when any request returns 401 after sign-in, the app returns to the sign-in screen with the site and email filled in and a message that the token stopped working. The rejected token is removed from the keychain.
- Keychain unavailable: the app says it cannot store the token and does not fall back to writing it to disk.

### Browse my issues and projects

- services: desktop-app, jira-cloud

Mockup: [browse-my-issues-and-projects.html](mockups/browse-my-issues-and-projects.html)

1. After sign-in the main window shows the sidebar and the My issues view.
2. The sidebar shows the site name, My issues with its open count, a Projects section listing every project the user can browse, and a footer with the user's avatar initial, display name, a theme toggle and Sign out.
3. My issues runs `assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`. The JQL of the current view is shown in a muted line under the top bar.
4. Issues are grouped by status. Groups follow status category order (in progress, then to do, then done) and sort by priority inside a group. Each group header shows the status icon, name and count, and collapses on click.
5. Each row shows priority, key, status icon, summary, labels, assignee avatar and time since the last update.
6. Open and All tabs switch between hiding and showing issues whose status category is Done.
7. Choosing a project shows `project = KEY` with the same grouping and tabs.
8. J and K, or the arrow keys, move the selection. Enter opens the selected issue.
9. A refresh button reloads the view. The top bar shows when the view last loaded.

Required states:

- First load: skeleton rows while the first page arrives.
- Revisit: returning to a view already loaded this session shows the last result at once and refreshes it in the background.
- Empty: a view with no issues says so. On the Open tab it offers to show all issues.
- Fetch error: the list area says the issues could not be loaded, names the HTTP status, says nothing on the site changed, and offers Try again.
- Rate limited: a banner says Jira is limiting requests and when the app retries. The last loaded list stays visible.
- Offline: a banner says the site cannot be reached and how old the shown list is, with Try again.
- Large view: a view stops loading at 1,000 issues and says the list shows the most recently updated ones.

### Read an issue

- services: desktop-app, jira-cloud

Mockup: [read-an-issue.html](mockups/read-an-issue.html)

1. Enter or a click on a row opens the detail pane over the right side of the list. Esc closes it. J and K move to the next or previous issue while it stays open.
2. The pane header shows the project, the issue type and key, and an Open in browser action that opens `https://<site>/browse/<KEY>` in the default browser.
3. The main column shows the summary as a title, then the description rendered from its ADF through Markdown, then the comments oldest first with author, relative time and body.
4. The description and comments render paragraphs, headings, ordered, bullet and task lists, code blocks with their language, block quotes, rules, hard breaks, strong, emphasis, inline code, strike, links and mentions. A mention shows the person's display name. A bare issue key in text renders as a link that opens that issue when it is in the loaded data.
5. Any ADF node outside that subset (panel, expand, table, media, status, emoji and others) renders as a placeholder block that names the node and offers Open in browser. The text around it keeps its order.
6. The side column shows status, priority, assignee, reporter, issue type, labels, created and updated.
7. A note at the bottom says the issue is read-only in this release.

Required states:

- No description: the pane says so.
- No comments: the pane says so.
- Loading: the summary and properties from the list show at once. The description and comments load after.
- Fetch error: the pane keeps the list data and offers Try again for the rest.

## Architecture Decisions

- **Crate boundary.** The workspace holds `jira-api`, `adf`, `core` and `app`, with dependencies only in the direction `app → core → (jira-api, adf)`. `jira-api` and `adf` never depend on GPUI or on each other's internals beyond `adf::Doc`. `core` never depends on GPUI. This keeps the client, the converter and the state usable from tests and the CLI without a window.
- **One API seam.** `jira-api` defines the `JiraApi` trait from the kickoff brief, with `HttpJira` for the network and `FakeJira` seeded from `fixtures/`. `core` and `app` take the trait, so every UI and core test runs against `FakeJira`. Only the methods this release needs are implemented on `HttpJira`: `myself`, `search`, `issue`, `comments` and `projects`. The write methods stay on the trait and return a not-implemented error until their release.
- **Search endpoint.** Every issue query uses `POST /rest/api/3/search/jql` with `nextPageToken`. The removed `/rest/api/3/search` is never called. That endpoint returns no total, so counts come from the loaded issues.
- **Pages and cap.** A view loads pages of 100 issues until `isLast` or until it holds 1,000 issues. Grouping by status needs the whole view in memory, and a bounded cap keeps a large project from blocking the first paint. Projects load from `/rest/api/3/project/search` in pages of 100 until `isLast`.
- **Requested fields.** Search requests only the fields a row needs: summary, status, priority, assignee, labels, issuetype and updated. The detail pane fetches the issue with its description and the comments separately.
- **Async runtime.** `core` owns a multi-threaded tokio runtime on its own threads. `reqwest` with rustls runs there. The app sends commands to `core` and awaits the results on GPUI's foreground executor through runtime-agnostic channels. No Jira call runs on the UI thread.
- **Session cache.** `core` keeps the last result of each view and each opened issue in memory for the session. A revisit renders the cached result first and refreshes it. Nothing is persisted to disk in this release.
- **Rate limits and retries.** On 429, `HttpJira` waits at least `Retry-After` seconds, backs off exponentially with jitter, and gives up after 4 attempts. Only reads are retried, and `POST /search/jql` counts as a read. While it waits, `core` reports the retry time so the UI can show the banner.
- **Credentials.** The token lives only in the OS keychain through the `keyring` crate. The config file, located with the `directories` crate, holds the site URL and email. Auth is HTTP Basic with an unscoped API token against the site URL. Scoped tokens need a different base URL and wait for a later release.
- **Identity.** Users are identified by `accountId` everywhere, including mentions and the current user.
- **ADF reading.** `adf` deserializes the whole document into serde enums with an `Unknown(serde_json::Value)` variant for any node or mark it does not know, so nothing is dropped. It renders a document to a sequence of blocks: Markdown text for runs of the supported subset, and an unsupported block that carries the original node. The app renders Markdown blocks with gpui-component's `TextView` and unsupported blocks as its own placeholder. The same block sequence is what the next release splices back when it writes ADF.
- **UI toolkit pins.** The app depends on gpui-component and its GPUI from crates.io with exact `=` versions, never a git branch. The chosen versions and the reason live in `docs/DEPENDENCIES.md`. An upgrade is its own commit. At the time of writing gpui-component 0.10.0 pins `gpui-pre =0.3.12`.
- **Design tokens.** The theme takes its colours, spacing and density from the mockups' CSS variables (dark and light, one accent, subtle borders, 36 px compact rows). The fonts are the platform's UI font and a monospace font. No Linear or Atlassian assets ship.
- **App name.** The name `jira4manager` lives in the workspace metadata and one `APP_NAME` constant, so a rename touches two places.

## Compatibility Sources

- Behavioural oracle: Jira Cloud as documented on developer.atlassian.com, and a free Jira Cloud site for live tests. The facts this milestone relies on, with their sources and read date, are in [platform-research-2026-11-17.md](artifacts/platform-research-2026-11-17.md).
- Product brief: [kickoff-brief.md](../../kickoff-brief.md). Where it and the research disagree, the research wins. Two known differences: `InputState::multi_line()` no longer exists in gpui-component, and gpui-component now pins `gpui-pre` from crates.io instead of a zed git revision.
- Look and interaction: the earlier exploration [tracker-mockup.html](../../mockups/tracker-mockup.html) and this milestone's mockups. The mockups' board view, cycles, command palette and create modal are not part of this release.

## Constraints

- Native only. GPUI and gpui-component draw every pixel. No webview, Tauri, Electron or embedded browser, including for Markdown.
- This release sends no request that changes Jira data. `HttpJira` issues only GET requests plus `POST /rest/api/3/search/jql`.
- The API token never appears in the config file, logs, `Debug` output, panic messages, fixtures or test snapshots. The `Authorization` header is redacted wherever requests are logged, and a test proves it.
- No network call runs on the UI thread, and the window keeps handling input while any request is in flight.
- Fixtures under `fixtures/` contain no real email, display name, accountId or site URL.
- Live tests run only with `cargo test --features live -- --ignored` and the `JIRA_SITE`, `JIRA_EMAIL` and `JIRA_TOKEN` variables. CI never runs them.
- Every dependency carries a licence compatible with GPL-3.0-or-later.
- `cargo fmt --check`, `cargo clippy -- -D warnings` and `cargo test` pass on Linux, macOS and Windows in CI.
- No Atlassian or Linear logo, icon or font appears in the app. "Jira" appears only in referential text, such as the sign-in screen's "Connect your Jira site".

## Acceptance

- CI runs format, clippy with warnings denied, and tests on Linux, macOS and Windows, and all three pass.
- The repository holds the GPL-3.0 `LICENSE`, a README with the build dependencies per OS and the "Linear-inspired" disclaimer, and `docs/ARCHITECTURE.md`, `docs/DEPENDENCIES.md` and `docs/ADF.md`.
- `cargo run -p jira-api --example my-open-issues` with the live variables set prints the signed-in user's open issues from a real site.
- wiremock tests prove: the Basic auth header shape, the JQL request body, pagination across at least three pages by `nextPageToken`, the 1,000-issue cap, a 429 with `Retry-After` retried after the wait, and giving up after 4 attempts.
- A test proves the token never appears in logged request output.
- The sign-in journey works against a live site: a valid token opens My issues, a wrong token shows the rejected error, an unknown site shows the site error, a relaunch skips sign-in, and Sign out removes the keychain entry.
- A token revoked while the app runs returns the user to sign-in with site and email kept.
- My issues and every project view show issues grouped by status in category order, with collapsible groups, Open and All tabs, J/K/Enter/Esc navigation and a working refresh.
- With `FakeJira` delaying every response, a GPUI test shows the skeleton state and shows the window still handles input during the delay.
- With `FakeJira` returning an error, a 429 and no network, the list shows the error, rate-limit and offline states.
- An issue whose description holds every supported node renders each one, and golden tests in `fixtures/adf/` pin the ADF to Markdown output for that subset.
- An issue whose description holds a panel, a table and an image shows a placeholder for each, in document order, with the text around them intact.
- The detail pane shows the comments of an issue with more than one page of comments.
- Dark and light themes both render every screen above.

## Non-Goals

- Editing anything: summary, description, status transitions, assignee, priority, labels, comments or issue creation. The next releases add writes.
- Markdown to ADF conversion and the splice of unsupported nodes back into saved ADF.
- The command palette, quick create, the `/` filter and the S, A, P and L pickers.
- A persistent cache. The session cache lives in memory only.
- Boards, sprints and the sprint field.
- Saved JQL views and free-form JQL entry.
- Several sites or accounts at once, scoped API tokens, and OAuth 2.0 sign-in.
- Jira Data Center or Server.
- Rendering media, panels, tables, emoji or status lozenges. They show as placeholders.
- The `xtask record` fixture recorder. Fixtures in this release are scrubbed by hand.
- Notifications, an inbox, or any background sync while the window is closed.
