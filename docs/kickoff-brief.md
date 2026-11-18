# jira4manager — Project Kickoff Brief

> Hand this file to Claude Code at the root of an empty folder.
> Suggested first prompt: *"Read jira4manager-kickoff.md, then do Milestone 0 and Milestone 1. Stop and show me the result before starting Milestone 2."*

---

## 1. What we're building

A **native desktop Jira client written in Rust** with a **Linear-inspired** look and feel: fast, keyboard-first, minimal and calm. It talks to **Jira Cloud** through the official REST API using the user's email + API token.

- **Licence:** GPL-3.0-or-later. Open source from day one.
- **Working name:** `jira4manager`. ⚠️ Atlassian's trademark guidelines want product names to *not start with* "Jira" and to use a referential form ("X for Jira"). Keep the name in one place (workspace metadata + one `const APP_NAME`) so a rename is trivial.
- **Branding:** "Linear-inspired" is fine in the README. Do **not** use Linear's or Atlassian's names in the UI chrome, or their logos, icons, fonts or other assets.

### Hard constraints
- **Native only.** No webview, no Tauri, no Electron, no browser.
- **UI framework:** [GPUI](https://github.com/zed-industries/zed/tree/main/crates/gpui) + [gpui-component](https://github.com/longbridge/gpui-component).
- **Target:** Jira **Cloud** REST API **v3** (plus Agile API 1.0). Data Center/Server is out of scope.
- **Rich text:** Markdown editing in the UI, converted to/from Atlassian Document Format (ADF). No WYSIWYG editor in v1.

---

## 2. Before writing code — verify, don't guess

GPUI and gpui-component move fast, and APIs in older blog posts or training data may be stale.

1. Check the **current** gpui-component README/docs for how to depend on it (crates.io version vs git) and which GPUI revision it expects. Pin both exactly (git `rev =` or exact version) and record the choice in `docs/DEPENDENCIES.md`.
2. Read gpui-component's **examples/story** crate for `Root`, `Input`/`InputState` (incl. `.multi_line()`), list/table, sidebar, popover/command palette, and theming before building UI.
3. Check GPUI's platform build requirements (Linux needs system packages such as xkbcommon/wayland/vulkan dev libs; macOS needs Xcode + Metal). Document them in the README.
4. Verify the Jira endpoints in §4 against developer.atlassian.com. In particular, use the **new JQL search endpoint** (`/rest/api/3/search/jql`, with `nextPageToken`), not the deprecated `/rest/api/3/search`.

---

## 3. Workspace layout

```
jira4manager/
├── Cargo.toml                # [workspace], shared lints, edition 2024 (or latest stable)
├── LICENSE                   # GPL-3.0 full text
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPENDENCIES.md
│   └── ADF.md                # supported ADF subset + Markdown mapping
├── crates/
│   ├── jira-api/             # HTTP client + models. No UI deps.
│   ├── adf/                  # ADF serde types + Markdown <-> ADF. No HTTP, no UI.
│   ├── core/                 # App state, caching, sync, commands. No GPUI.
│   └── app/                  # GPUI binary: views, theme, keybindings.
├── fixtures/                 # Recorded, scrubbed Jira JSON responses for tests
└── .github/workflows/ci.yml
```

Dependency direction: `app → core → (jira-api, adf)`. `jira-api` and `adf` must never depend on GPUI.

---

## 4. Jira API layer (`crates/jira-api`)

### Auth
- Jira Cloud: **HTTP Basic** with `email:api_token` against `https://<site>.atlassian.net`.
- Store the token in the OS keychain via the `keyring` crate. The config file (`directories` crate for the path) holds only the site URL + email.
- Never log tokens or `Authorization` headers. Add a redaction test.

### Design
- `reqwest` (rustls), `serde`, `thiserror`, `tokio`.
- Define a **trait** so the UI and core can run against fakes:

```rust
#[async_trait::async_trait] // or native async fn in traits if the MSRV allows
pub trait JiraApi: Send + Sync {
    async fn myself(&self) -> Result<User>;
    async fn search(&self, jql: &str, fields: &[&str], page: Option<PageToken>) -> Result<Page<Issue>>;
    async fn issue(&self, key: &str) -> Result<Issue>;
    async fn create_issue(&self, req: CreateIssue) -> Result<IssueRef>;
    async fn update_issue(&self, key: &str, req: UpdateIssue) -> Result<()>;
    async fn transitions(&self, key: &str) -> Result<Vec<Transition>>;
    async fn transition(&self, key: &str, transition_id: &str) -> Result<()>;
    async fn comments(&self, key: &str, page: Option<PageToken>) -> Result<Page<Comment>>;
    async fn add_comment(&self, key: &str, body: adf::Doc) -> Result<Comment>;
    async fn projects(&self) -> Result<Vec<Project>>;
    async fn assignable_users(&self, project: &str, query: &str) -> Result<Vec<User>>;
    async fn boards(&self) -> Result<Vec<Board>>;
    async fn sprints(&self, board_id: u64) -> Result<Vec<Sprint>>;
}
```

- Implementations: `HttpJira` (real) and `FakeJira` (in-memory, seeded from `fixtures/`).
- Handle **429 / Retry-After** with backoff, and paginate everything.
- Users are identified by **`accountId`** (Cloud), never username.
- Model only the fields the UI needs, and keep unknown fields as `serde_json::Value` where round-tripping matters (custom fields).

### Endpoints (verify paths/params before use)
| Purpose | Endpoint |
|---|---|
| Current user | `GET /rest/api/3/myself` |
| Search | `POST /rest/api/3/search/jql` (token pagination) |
| Issue | `GET/PUT /rest/api/3/issue/{key}` |
| Create | `POST /rest/api/3/issue` |
| Transitions | `GET/POST /rest/api/3/issue/{key}/transitions` |
| Comments | `GET/POST /rest/api/3/issue/{key}/comment` |
| Projects | `GET /rest/api/3/project/search` |
| Assignable users | `GET /rest/api/3/user/assignable/search` |
| Boards / sprints | `GET /rest/agile/1.0/board`, `/board/{id}/sprint` |

---

## 5. ADF ⇄ Markdown (`crates/adf`)

- Serde enums for ADF nodes + marks. Unknown nodes deserialize into an `Unknown(serde_json::Value)` variant: **never drop data**.
- Markdown parsing with `comrak` (GFM: tables, task lists, strikethrough).

**Supported in v1 (editable):** paragraph, heading 1–6, bulletList, orderedList, listItem, codeBlock (with language), blockquote, rule, hardBreak, text marks (strong, em, code, strike, link), mention, taskList/taskItem.

**Jira-specific Markdown conventions:**
- Mention: `@[Display Name](accountId:5b10ac8d82e05b22cc7d4ef5)` ⇄ ADF `mention` node.
- Bare issue keys (`ABC-123`) render as links in the UI but stay plain text in ADF unless already linked.

**Unsupported nodes** (panel, expand, table with merged cells, media, status, emoji, etc.):
- Render them read-only in the UI as a placeholder block.
- When saving, the converter must **splice the original ADF back in** at the same position. An edit must never silently erase formatting someone made in the web UI.
- If that can't be guaranteed for a document, open it **read-only** and say why.

**Tests:**
- Golden tests: `fixtures/adf/*.json` ⇄ `*.md`.
- Round-trip: ADF → MD → ADF is identical for the supported subset.
- `proptest` generators for the supported subset.
- Document the mapping in `docs/ADF.md`.

---

## 6. UI (`crates/app`): Linear-inspired

**Layout**
- Left **sidebar**: My issues, project list, boards/sprints, saved JQL views.
- Center **issue list**: dense rows (key, priority icon, title, labels, assignee avatar, status), grouped by status, with collapsible groups.
- Right/overlay **detail pane**: title, Markdown description (edit ⇄ preview), properties panel (status, assignee, priority, labels, sprint), comments.

**Interaction (keyboard-first)**
| Key | Action |
|---|---|
| `Cmd/Ctrl+K` | Command palette (search issues, jump to project, run any action) |
| `C` | Quick-create issue |
| `J` / `K` | Move selection |
| `Enter` / `Esc` | Open / close detail |
| `S`, `A`, `P`, `L` | Change status / assignee / priority / labels (popover picker) |
| `/` | Filter current list |
| `Cmd/Ctrl+Enter` | Save / submit comment |

**Feel**
- Optimistic updates with rollback + toast on API failure.
- Local cache (start in-memory; SQLite via `rusqlite` later) so lists render instantly, then refresh in the background.
- Dark and light themes via gpui-component theming; neutral greys, one accent colour, subtle borders, generous spacing, small type.
- Never block the UI thread on network calls.

---

## 7. Testing strategy

| Layer | How |
|---|---|
| `jira-api` | `wiremock` crate serving JSON from `fixtures/`; assert request shape (auth header, JQL body, pagination). |
| `adf` | Golden + round-trip + proptest (see §5). |
| `core` | Unit tests against `FakeJira`. |
| `app` | GPUI's test context (`#[gpui::test]`) for key view logic; manual smoke checklist in `docs/`. |
| Live (opt-in) | `cargo test --features live -- --ignored` hits a real **free Jira Cloud site** (Free plan, ≤10 users) using env vars `JIRA_SITE`, `JIRA_EMAIL`, `JIRA_TOKEN`. Never run in CI by default. |

**Fixtures:** add a small `xtask record` command that pulls real responses from the sandbox site and **scrubs** emails, names, accountIds and URLs before writing to `fixtures/`.

Optional offline mock server: Atlassian publishes an OpenAPI spec for the Cloud platform REST API; it can be served with Prism for exploratory UI work.

---

## 8. Milestones

**M0: Skeleton**
- Workspace, crates, GPL-3.0 `LICENSE`, README (build deps per OS, "Linear-inspired" disclaimer), `docs/` stubs.
- CI: `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test` on Linux + macOS + Windows.
- GPUI window opens with gpui-component `Root` and a themed empty sidebar.

**M1: API client + fakes**
- `JiraApi` trait, `HttpJira`, `FakeJira`, keychain auth, `myself` + `search` + `issue`.
- wiremock tests for auth, pagination and 429 handling.
- Small CLI in `jira-api/examples/` that prints "My open issues" against a real site.

**M2: Read-only UI**
- Login screen (site, email, token → keychain), sidebar, grouped issue list, detail pane with Markdown preview (ADF → MD only).

**M3: ADF converter, full**
- MD → ADF, unsupported-node preservation, golden/round-trip/proptest suites.

**M4: Editing**
- Edit title/description, transitions, assignee/priority/labels pickers, comments, quick-create. Optimistic updates.

**M5: Speed & polish**
- Command palette, all keybindings, local cache, background refresh, themes, empty/loading/error states.

**M6: Agile**
- Boards, sprints, sprint view.

---

## 9. Working rules for Claude Code

- Work milestone by milestone and stop for review at the end of each.
- Keep `jira-api` and `adf` free of UI dependencies; keep `core` free of GPUI.
- Prefer small, well-named modules; add rustdoc on public items.
- Every bug fix comes with a test.
- Do not commit secrets, `.env` files, or unscrubbed fixtures. Add `.gitignore` entries for them.
- When an API (GPUI, gpui-component, Jira) behaves differently than this brief says, trust the current official docs and note the difference in `docs/ARCHITECTURE.md`.
