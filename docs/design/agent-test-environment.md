# The test environment a coding agent works in

A coding agent builds this app unattended. It must prove each story in the running system without a person at a screen and without a real Jira site in the loop. This note says which layers of tests exist, what each one proves, the exact command that runs it, and what the walking skeleton builds so the later stories can use it.

The facts behind this note, with their sources, are in [test-environment-research-2026-11-19.md](../milestones/0001-issues-epics-and-board/artifacts/test-environment-research-2026-11-19.md). The Jira requests every layer exercises are in [jira-api-per-view.md](jira-api-per-view.md).

## The layers

The layers run fastest first. An agent runs the layers its change touches before it commits. CI runs layers 1 to 5 on every push. Layer 6 is a manual check an agent runs to see a screen. Layer 7 runs only when a person asks for it.

| Layer | What it proves | Where it runs | Command |
| --- | --- | --- | --- |
| 1. Converter | ADF to Markdown and back, for the editable subset | CI, three systems | `cargo test -p adf` |
| 2. Client | The request shape, paging, batches, retries and error mapping of each call | CI, three systems | `cargo test -p jira-api` |
| 3. Core | Caching, optimistic writes, rollback and grouping, over `FakeJira` | CI, three systems | `cargo test -p core` |
| 4. Views | Each screen's states and keyboard paths, over `FakeJira`, with no display | CI, three systems | `cargo test -p app` |
| 5. Screens | Each screen drawn to a PNG, in both themes, with no display | CI, Linux and macOS | `cargo test -p app --test screens` |
| 6. Running app | The real window against a local fake Jira, driven by keys | An agent's machine, Linux | `scripts/headless-app.sh` |
| 7. Live sandbox | The same journeys against a real Jira Cloud site | A person's machine, on request | `saddlebag exec ... -- cargo test --features live -- --ignored` |

The `jira-cloud` book sits beside these layers. It keeps the fake Jira true to Jira, as the last section says.

## 1. Converter

`fixtures/adf/` holds one `.json` and one `.md` per node of the editable subset. Golden tests pin each direction. Round-trip tests check that ADF to Markdown to ADF is identical. `proptest` generates documents inside the subset. A document with a node outside the subset must come back read-only with a placeholder per node.

## 2. Client over wiremock

Each test starts a `wiremock::MockServer` and builds `HttpJira` with its URL as the base URL. The test mounts the answer from `fixtures/jira/<area>/<name>.json` and asserts the request the client sent: method, path, query, body and headers.

- Every request in [jira-api-per-view.md](jira-api-per-view.md) has at least one test that asserts its exact shape.
- Paging tests chain three pages by `nextPageToken`, and three by `startAt`.
- Retry tests answer 429 with `Retry-After: 1` and run on tokio's paused clock, so they take no wall time.
- A redaction test logs a request at trace level and asserts the token and the `Authorization` value appear nowhere in the captured output.

Fixtures are written by hand from the shapes in the research notes. They hold no real email, display name, accountId or site URL. Accounts use ids such as `5b10ac8d82e05b22cc7d4ef5` and names such as Ana Ruiz, and the site is `acme-labs.atlassian.net`.

## 3. Core over FakeJira

`FakeJira` lives in `jira-api` behind the `fake` feature. It holds the world in memory and applies the same rules as a project: workflow transitions, required fields per screen, sprint states, the 50-issue move limit and field errors keyed by field id.

`FakeJira::mockup_world()` builds the world the milestone mockups show:

- `CASE`, company-managed, scrum board, Sprint 14 active, Sprints 15 and 16 future. Its Bug create screen requires Severity. It has Reviewer, QA engineer, Severity, Acceptance criteria and Root cause, a cascading select.
- `CASE1`, team-managed, kanban board with its backlog turned on. It has Story point estimate, Designer and Browsers.
- `OPS`, company-managed, kanban board. Its Bug create screen requires Affected service, a cascading select the app cannot edit.

Tests change the world through knobs that match the mockups' knobs: refuse the next write with a status, refuse a field with Jira's message, delay every answer, and require a field on a transition. A test reads the world back to check what a write did.

## 4. Views over FakeJira

View tests use `#[gpui::test]` with the `test-support` feature on `gpui`. They open a view with `add_window_view`, act with `simulate_keystrokes`, `simulate_input` and `simulate_click`, settle with `run_until_parked`, and drive time with `advance_clock`. They need no display and no GPU, so they run on all three systems.

GPUI offers no way to find an element in a window. The test module of `gpui-kit` adds one: `find(id)`, `find_by_label`, `find_all_by_role`, `within(scope)` and `click(id)`. Each returns a snapshot with the element's role, label, value, checked and focused state, disabled state, bounds and visibility. `app` takes `gpui-kit` as a dev-dependency with `test-support` for this.

The query layer only finds what the code names. So every interactive element carries a role, an accessible label, and an `.id()` with the same value as its `accessibility_id`. In-process tests cannot read GPUI's own accessibility tree, because a test window never turns it on. A screen reader, or an outside driver, reads that tree over AT-SPI and sees only the `accessibility_id`. [gpui-atspi-spike-2026-11-19.md](../milestones/0001-issues-epics-and-board/artifacts/gpui-atspi-spike-2026-11-19.md) shows such a driver working under Xvfb.

A view test names its journey and state, as in `manage_issues__required_field_empty`. The milestone's required states are the list of view tests to write.

## 5. Screens to PNG

`app/tests/screens.rs` is a test target with `test = false`, so a plain `cargo test` skips it. It opens each view on `HeadlessAppContext` with `gpui_platform::current_headless_renderer`, which needs `test-support` on `gpui-pre-platform`. `capture_screenshot` returns the window as an image. The test writes `target/screens/<journey>/<state>-<theme>.png` and asserts a few pixels in code, such as the theme's background and the accent colour of the selected row.

- Linux renders through wgpu on Mesa's lavapipe, a software Vulkan driver. It needs `mesa-vulkan-drivers` and no display server.
- macOS renders through Metal.
- Windows has no headless renderer, so the target skips there.

CI uploads `target/screens/` as an artifact. No baseline images are stored. An agent opens a PNG with its image reader and compares it with the same state of the journey's mockup, which the mockup's knobs reach.

## 6. The running app against a local fake Jira

Layers 4 and 5 prove the views in a test harness. Layer 6 starts the real binary, with its real `HttpJira`, and points it at a local server.

`cargo xtask fake-jira --port 8787` serves `FakeJira::mockup_world()` over HTTP on `127.0.0.1`. It answers exactly the requests in [jira-api-per-view.md](jira-api-per-view.md). Any other request gets a 404 with `fake-jira does not serve <method> <path>` and a line on stderr, so a request missing from the note shows at once. Flags match the knobs of layer 3: `--refuse-writes <status>`, `--refuse-field <field id>`, `--delay-ms <n>` and `--transition-screen`.

Debug builds of the app read three variables:

- `JIRA4MANAGER_SITE`, which may be a loopback `http://` URL;
- `JIRA4MANAGER_EMAIL` and `JIRA4MANAGER_TOKEN`;
- `JIRA4MANAGER_CONFIG_DIR`, so a run never touches the user's own config.

With the first three set, the app skips the sign-in screen and the keychain and stores no credential. Release builds ignore all four and refuse any `http://` site.

`scripts/headless-app.sh` runs one session on Linux:

1. It starts `Xvfb :99 -screen 0 1440x900x24`.
2. It starts `cargo xtask fake-jira` and waits for its port.
3. It starts the app's debug build with `DISPLAY=:99`, `VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json` and the variables above.
4. It reads key steps from its arguments, sends each with `xdotool`, and saves `import -window root target/headless/<n>.png` after each.

```bash
scripts/headless-app.sh "c" "type:Login fails on Safari" "ctrl+Return"
```

A window that draws fully transparent is a known GPUI defect on some software Vulkan setups. The script then hides the Vulkan driver by pointing `VK_ICD_FILENAMES` at an empty file, and GPUI falls back to GL on llvmpipe. The machine needs `xvfb`, `xdotool`, `imagemagick` and `mesa-vulkan-drivers`.

## 7. The live sandbox

The sandbox is a Jira Cloud site on the Free plan. The plan is free for up to 10 users and makes every user an admin, so one API token can both seed the site and run the tests. A developer instance would do too, but no official page states how long one lasts.

### The site's content

`cargo xtask seed-sandbox` builds the same world as `FakeJira::mockup_world()` on the site. It reads before it writes, creates only what is missing, and never deletes. A rerun is safe, and a deactivated site is rebuilt by running it on a new one.

| Step | Request |
| --- | --- |
| `CASE`, company-managed scrum | `POST /rest/api/3/project` with `projectTemplateKey: com.pyxis.greenhopper.jira:gh-simplified-scrum-classic` |
| `CASE1`, team-managed kanban | the same with `gh-simplified-agility-kanban` |
| `OPS`, company-managed kanban | the same with `gh-simplified-kanban-classic` |
| `CASE` and `OPS` custom fields | `POST /rest/api/3/field`, then a context and its options under `/rest/api/3/field/{id}/context` |
| Fields on the screens | `POST /rest/api/3/screens/{screenId}/tabs/{tabId}/fields` |
| Required Severity and Affected service | `PUT /rest/api/3/fieldconfiguration/{id}/fields` with `isRequired` |
| Versions and components | `POST /rest/api/3/version`, `POST /rest/api/3/component` |
| Sprints 14 to 16 on `CASE` | `POST /rest/agile/1.0/sprint`, then `POST /rest/agile/1.0/sprint/{id}` with `state: active` for Sprint 14 |
| Issues, epics and labels | `POST /rest/api/3/issue/bulk`, with `parent` and `labels` set on create |
| Sprint membership | `POST /rest/agile/1.0/sprint/{id}/issue`, 50 at a time |

These requests live in `xtask` only. The app never makes them.

Three steps are done once by hand in the browser, because Jira offers no API for them:

- The `CASE1` fields Story point estimate, Designer and Browsers. Team-managed fields can be created only in the UI.
- The `CASE1` board's backlog, turned on in the board settings.
- A second user, so user pickers have two people to offer.

UNCONFIRMED, and checked by the first run of the seed: that the template keys above give company-managed and team-managed projects as stated, that the `classic` templates create a board, the field configuration call, and starting a sprint by setting its state. Only community posts state the template pairing. The kickoff brief pairs them the other way round. The seed prints each project's `style` after creating it.

### The credentials

The token lives in saddlebag, never in a file. The person who owns the site registers it once:

```bash
saddlebag secret create jira_sandbox --var JIRA_TOKEN --username <sandbox email> --meta site=<name>.atlassian.net --tag environment=jira-sandbox --description "API token of the jira4manager sandbox site"
```

saddlebag then asks them for the token. An agent runs the live tests with:

```bash
saddlebag exec --env JIRA_TOKEN=jira_sandbox --env JIRA_EMAIL=jira_sandbox.username --env JIRA_SITE=jira_sandbox.meta.site -- cargo test --features live -- --ignored --test-threads=1
```

The seed takes the same prefix in front of `cargo xtask seed-sandbox`. The values reach the command's environment and never the agent's transcript.

### What a live test may do

- It writes only in `CASE`, `CASE1` and `OPS` of the sandbox site.
- It creates the issues it changes, labelled `j4m-live` and the run's id, and leaves the seeded issues as they are.
- It runs one test at a time. Jira allows 20 writes to one issue per 2 seconds and 100 per 30 seconds, and an API token is exempt from the hourly quota but not from these.
- It never runs in CI, and it never tests the rate limits. Atlassian asks that nobody load its tenants on purpose.

The live check of the kanban backlog call, and every other UNCONFIRMED fact in [jira-api-per-view.md](jira-api-per-view.md), runs at this layer. The story that first depends on one records the result in `docs/ARCHITECTURE.md`.

## The jira-cloud book keeps the fake honest

Layers 2 to 6 trust `FakeJira`. A fake that drifts from Jira lets every one of them pass while the app fails on a real site. The ostler book `services/jira-cloud/` models the requests in [jira-api-per-view.md](jira-api-per-view.md), with their answers and refusals. It plays the same journeys against `cargo xtask fake-jira` and against the sandbox, and it compares both with its model. A difference is a defect in the fake or in the book, and the story that finds it fixes it.

## What the walking skeleton builds

The first story makes every layer exist, each with one test, so later stories only add tests:

- `fixtures/adf/` with one paragraph pair, and a golden and a round-trip test.
- A wiremock test for `GET /rest/api/3/myself` and for one page of `POST /rest/api/3/search/jql`.
- `FakeJira` with `mockup_world()`, and a core test of one transition.
- One `#[gpui::test]` view test of the issue list, and one screen in `app/tests/screens.rs`.
- `cargo xtask fake-jira`, the debug-build variables and `scripts/headless-app.sh`, with one PNG of the issue list.
- The live test of the skeleton journey: sign in, list `CASE`, change one status.
- The CI workflow: format, clippy and tests on three systems, the screens target on Linux with `mesa-vulkan-drivers` and on macOS, and the PNGs uploaded.

## What an agent runs to close a story

1. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and `cargo test` for the crates it changed.
2. `cargo test -p app --test screens` when it changed a view, then a look at each new or changed PNG beside the mockup.
3. `scripts/headless-app.sh` with the story's key path when the story changes a screen, and a look at the PNGs.
4. The live tests the story added, only when a person has asked for a live run.
