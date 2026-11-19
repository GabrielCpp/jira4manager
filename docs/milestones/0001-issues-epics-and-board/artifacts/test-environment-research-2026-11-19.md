# Test environment research, 2026-11-19

Coding agents will build jira4manager unattended. This record answers what they can use to test it without a human: in-process UI tests, a screenshot of the running app, and a live Jira sandbox. Each fact names its source by number (see Sources). Facts marked UNCONFIRMED were not found in an official source.

Versions read: the `gpui-pre` 0.3.12 crate family from crates.io, `gpui-kit`/`gpui-component`/`gpui-base` 0.10.0 from crates.io, the gpui-kit repo at `a3f473e`, and zed `main` at `4a4c815` (2026-11-19).

## Correction to the brief

- `gpui-pre` is not published by Zed. Its only crates.io owner is Jason Lee (`huacnlee`), the gpui-component author. Its description reads "gpui-pre snapshot of zed@125ca86". [S1]
- The Linux renderer in 0.3.12 is wgpu (`gpui_wgpu`, wgpu 30), not blade. It asks wgpu for the Vulkan and GL backends only. [S2] [S11]
- The platform layer is a separate crate, `gpui-pre-platform` (`gpui_platform`). It pulls `gpui-pre-linux`, `gpui-pre-wgpu`, `gpui-pre-macos` or `gpui-pre-windows` per target. [S3]
- The gpui-component repo is now `longbridge/gpui-kit`. `gpui-kit` 0.10.0 re-exports `gpui-component`, `gpui-base` and GPUI. [S4]

## 1. GPUI test contexts

- Everything below needs the `test-support` feature on `gpui` (the `gpui-pre` package). The feature exists in 0.3.12. [S5]
- Screenshots also need `test-support` on `gpui_platform` (`gpui-pre-platform`). That feature exposes `current_headless_renderer()`. [S3]
- docs.rs builds `gpui-pre` without `test-support`, so the test types are absent from docs.rs. Read the crate source instead. [S6]
- `#[gpui::test]` builds a `TestAppContext` per argument. It also accepts `StdRng` and `BackgroundExecutor` arguments. Attributes: `iterations`, `seed`, `seeds(...)`, `retries`, `on_failure`. [S7]
- Determinism: every test runs on a `TestDispatcher` seeded from `SEED` (default 0). `ITERATIONS` overrides the iteration count. `#[gpui::property_test]` bridges `SEED` into proptest. [S8]
- `TestAppContext` runs on `TestPlatform`. It has no display, no GPU and, by default, `NoopTextSystem`, so text is laid out without real glyphs. `build_with_text_system` swaps in a real text system. [S9]
- `TestAppContext` offers `add_window`, `add_window_view`, `add_empty_window`, `open_window`, `run_until_parked`, `dispatch_action`, `simulate_keystrokes`, `simulate_input`, `dispatch_keystroke`, clipboard, prompt and path-picker simulation, window resize, display and scale-factor simulation, `condition`, `notifications`, `events`. [S9]
- `VisualTestContext` is the per-window handle that `add_window_view` returns. It runs on `TestPlatform` on every OS. It offers `simulate_click`, `simulate_mouse_move/down/up`, `simulate_keystrokes`, `simulate_input`, `simulate_modifiers_change`, `simulate_resize`, `simulate_event`, `draw`, `window_title`, `debug_bounds`. [S9]
- `debug_bounds(selector)` returns an element's laid-out bounds. The element must carry `.debug_selector(...)`. Selectors record only in debug builds with `test-support`. [S9] [S10]
- Executor and timers: `advance_clock`, `advance_clock_to_next_timer`, `run_until_parked`, `tick`, `simulate_random_delay`, `allow_parking`, `forbid_parking`, `timer`, `rng`. [S8]
- GPUI has no generic element-tree query API. `gpui-kit`'s `test` module (feature `test-support`) adds one: `window.find(id)`, `find_by_label`, `find_all_by_role`, `within(scope)`, `click(id)`, pointer and key helpers. An `ElementSnapshot` holds role, label, value, checked, selected, expanded, focused, disabled, bounds and visibility. It is in the published 0.10.0 crate. [S12] [S13]
- `HeadlessAppContext` and `VisualTestAppContext` render pixels. See question 3.

## 2. Display, GPU and CI

- `TestAppContext` and `VisualTestContext` need no display and no GPU. They run on `TestPlatform` on Linux, macOS and Windows. [S9]
- Zed's CI runs `cargo nextest run --workspace` on Linux (Ubuntu 22.04), macOS and Windows runners. The Linux job installs packages with `script/linux` and sets up no Xvfb and no `DISPLAY`. [S14]
- gpui-kit's CI runs `cargo test --workspace` with `test-support` on `ubuntu-latest`, `macos-latest` and `windows-latest`. It sets up no Xvfb. [S15]

## 3. Rendering a window to an image without a screen

- Yes, on Linux and macOS. `HeadlessAppContext::with_platform(text_system, assets, gpui_platform::current_headless_renderer)` opens windows on `TestPlatform` and renders them offscreen. `capture_screenshot(window)` returns an `image::RgbaImage`. [S16] [S3]
- `current_headless_renderer()` returns a Metal renderer on macOS and `WgpuHeadlessRenderer` on Linux. On Windows it returns `None`, so Windows has no screenshot path. [S3]
- The Linux headless renderer tries every wgpu adapter, software included. Mesa lavapipe therefore qualifies, and no display server is needed. [S11]
- gpui-kit's CI runs these screenshot tests on `ubuntu-latest` after `apt-get install mesa-vulkan-drivers`, and on `macos-latest`. Windows skips them. The test file is `crates/kit/tests/rendering.rs`, marked `test = false` and run with `--test rendering`. [S15] [S17]
- Those tests compare pixel values in code. No baseline image store was found. [S17]
- `VisualTestAppContext` is a second, macOS-only path that uses the real `MacPlatform` with offscreen windows. Its tests are `#[ignore]` because AppKit needs the main thread. [S18] [S3]
- Zed's own visual regression runner (`zed-visual-test-runner`, feature `visual-tests`) is macOS-only. Its baselines are gitignored and generated locally with `UPDATE_BASELINE=1`. [S19] [S20]
- `TestScreenCaptureSource` exists, but it fakes screen-share sources. It does not capture windows. [S5]
- No screenshot code was found in gpui-kit's story crate. [S17]

## 4. The real app on headless Linux

- With no `DISPLAY` and no `WAYLAND_DISPLAY`, or with `ZED_HEADLESS` set, GPUI on Linux starts headless. Headless windows lay out and take input but draw nothing. [S21] [S22]
- So a screenshot of the real app needs a display server. GPUI picks Wayland when `WAYLAND_DISPLAY` is set, then X11 when `DISPLAY` is set. [S23]
- Xvfb with lavapipe works. A gpui-pre 0.3.11 user measured a GPUI app "on Xvfb, with lavapipe drawing" in a comment on zed issue #63327. [S24]
- Risk: zed issue #66309 (open) reports a fully transparent window with llvmpipe Vulkan on an Xorg dummy display with KWin compositing. Hiding the Vulkan ICD made Zed fall back to GL llvmpipe, which rendered. [S25]
- Lavapipe forced with `VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.x86_64.json` rendered Zed correctly where a hardware GPU failed, per zed issue #63565. [S26]
- Env vars that steer the adapter: `VK_ICD_FILENAMES` or `VK_DRIVER_FILES` pick the Vulkan driver. `MESA_VK_DEVICE_SELECT` and `ZED_DEVICE_ID` pick a device. [S25] [S26] [S27]
- GPUI ranks adapters Discrete > Integrated > Other > Virtual > Cpu. A software adapter wins only when nothing else is present. After a device loss it rejects software adapters. [S11]
- `WGPU_BACKEND` has no effect. GPUI hardcodes `VULKAN | GL` and never reads wgpu's env overrides. [S11]
- UNCONFIRMED: GPUI under weston `--backend=headless`, cage or sway headless. No report was found.
- UNCONFIRMED: a report of GPUI in Docker. The Xvfb report above does not say whether it ran in a container.

## 5. Accessibility tree

- GPUI 0.3.12 builds an AccessKit tree (`accesskit` 0.24). Linux uses `accesskit_unix` over AT-SPI on both X11 and Wayland. macOS and Windows have their own adapters. [S5] [S28] [S29]
- An element joins the tree only with an id and a role: `div().id(...).role(Role::Button)`. `.aria_label(...)` sets its name. [S28] [S10]
- The tree is built only after assistive technology activates it. `Window::debug_a11y_tree_json()` returns `None` until then. [S30] [S31]
- `TestPlatform` windows never activate it, because `TestWindow` keeps the default no-op `a11y_init`. In-process tests cannot read GPUI's AccessKit tree. Derived from source. [S9] [S32]
- In-process tests should use gpui-kit's `ElementSnapshot` queries instead. They expose role, label and state per element id. [S12] [S13]
- An external AT-SPI reader can read the running app on Linux. Zed issue #66729 reads node extents over AT-SPI from a GPUI app on X11. The same issue reports that screen coordinates ignore the window position. [S33]
- UNCONFIRMED: AT-SPI reading under Xvfb with no desktop session. An AT-SPI bus must be running.

## 6. How gpui-kit tests its components

- Unit tests sit inside the source files with `#[gpui::test]`. The repo holds about 2,000 of them. [S17]
- They open a view with `add_window_view`, act with `simulate_click`, `simulate_keystrokes` and `simulate_input`, settle with `run_until_parked`, drive time with `advance_clock`, and assert layout with `debug_bounds`. [S17]
- `crates/kit/tests/ui.rs` and `tests/integration` use the `gpui_kit::test` query layer: find by id, label or role, click, then assert state. [S13]
- `crates/kit/tests/rendering.rs` captures real pixels through `HeadlessAppContext`. See question 3. [S17]
- The dev-dependency turns on the feature: `gpui = { ..., features = ["test-support"] }`. [S17]

## 7. Free Jira sandboxes

- Cloud developer instance: sign up at go.atlassian.com/cloud-dev. It redirects to the cloud signup with `developer=true`. [S34] [S35]
- It includes Jira Software for 5 users, Confluence for 5 users and Jira Service Management for 1 agent. [S34]
- It may be used only for development and testing. [S34]
- UNCONFIRMED: how long a developer instance lasts, whether it renews, and its inactivity rule. No official page states them.
- UNCONFIRMED: Free sites are deactivated after 120 days without activity. Only Atlassian Community posts say so. [S36]
- Jira Free plan: free forever for up to 10 users, 2 GB storage, Community support. [S37]
- Free plan: 150 automation steps per month for the whole subscription. [S37]
- Free plan: "every user is a admin". Project-level permission settings are only on paid plans. [S37]
- Forge demo site: `forge site provision` creates a site with seeded data and enterprise editions of Jira, Confluence, JSM and Rovo. It is active for 90 days, one per developer, and the CLI cannot extend it. [S38]
- UNCONFIRMED: whether a Forge demo site accepts API-token REST calls.

## 8. Seeding a sandbox through REST

Sources: the platform OpenAPI spec [S39] and the agile OpenAPI spec [S40], unless noted.

| Step | Endpoint | Permission |
|---|---|---|
| Create project | `POST /rest/api/3/project` with `key`, `name`, `leadAccountId`, `projectTypeKey: software`, `projectTemplateKey` | Administer Jira |
| Create custom field | `POST /rest/api/3/field` with `name`, `type`, `searcherKey` | Administer Jira |
| List contexts | `GET /rest/api/3/field/{fieldId}/context` | Administer Jira |
| Create context | `POST /rest/api/3/field/{fieldId}/context` | Administer Jira |
| Add options | `POST /rest/api/3/field/{fieldId}/context/{contextId}/option` | Administer Jira |
| List screens, tabs | `GET /rest/api/3/screens`, `GET /rest/api/3/screens/{screenId}/tabs` | Administer Jira (tabs also Administer projects) |
| Add field to screen | `POST /rest/api/3/screens/{screenId}/tabs/{tabId}/fields` | Administer Jira |
| Create version | `POST /rest/api/3/version` | Administer Jira or Administer projects |
| Create component | `POST /rest/api/3/component` | Administer Jira or Administer projects |
| Create board | `POST /rest/agile/1.0/board` with `name`, `type`, `filterId` | Not stated |
| Create sprint | `POST /rest/agile/1.0/sprint` with `name`, `originBoardId` | Not stated. Jira's Manage sprints permission covers create, start and complete [S41] |
| Issues into sprint | `POST /rest/agile/1.0/sprint/{sprintId}/issue`, max 50, open or active sprints only | Not stated |
| Rank issues | `PUT /rest/agile/1.0/issue/rank`, max 50 | Not stated |
| Create issues | `POST /rest/api/3/issue`, `POST /rest/api/3/issue/bulk` | Browse projects and Create issues |
| Delete project, field | `DELETE /rest/api/3/project/{key}`, `DELETE /rest/api/3/field/{id}` | Administer Jira |

- Software template keys: `gh-simplified-agility-kanban`, `gh-simplified-agility-scrum`, `gh-simplified-basic`, `gh-simplified-kanban-classic`, `gh-simplified-scrum-classic`, all prefixed `com.pyxis.greenhopper.jira:`. The spec does not say which are team-managed.
- Community reports: `gh-simplified-scrum-classic` and `gh-simplified-kanban-classic` create company-managed projects. `gh-simplified-agility-scrum` and `gh-simplified-agility-kanban` create team-managed projects. UNCONFIRMED in official docs. [S42]
- The brief's pairing of team-managed with `gh-simplified-scrum-classic` is the reverse of those reports.
- `POST /rest/api/3/project-template` creates a project from custom capabilities. It is Enterprise only.
- Supported custom field types include `select`, `multiselect`, `multicheckboxes`, `radiobuttons`, `cascadingselect`, `labels`, `datepicker`, `datetime`, `float`, `textfield`, `textarea`, `url`, `userpicker`, `multiuserpicker`, `version`, `multiversion`, `project`. Each needs its matching searcher or the field is not searchable.
- A field holds at most 10,000 options. One request creates at most 1,000.
- Labels have no create endpoint. Set them through `fields.labels` on issue create or edit. `GET /rest/api/3/label` lists them.
- `POST /rest/agile/1.0/epic/{epic}/issue` does not work for team-managed epics. Set `parent` on the issue instead.
- Team-managed project fields cannot be created through the API. Atlassian's suggestion JRACLOUD-91386 says field management there "is restricted to UI". It is open, status Gathering Interest. [S43]
- `POST /rest/api/3/field/{id}/context/mapping` does not work on team-managed projects. Atlassian closed JRACLOUD-80743 as Won't Do. [S44]
- On the Free plan every user is an admin, so an API token of any site user can call the admin endpoints. [S37]
- UNCONFIRMED: whether the `*-classic` templates create a board automatically.
- UNCONFIRMED: whether the agile sprint endpoints work on team-managed scrum boards.

## 9. Rate limits for a test suite

Source: [S45].

- Three limits apply: an hourly points quota, per-second burst limits and per-issue write limits.
- API-token traffic is exempt from the points quota. Burst limits still apply to it.
- Burst defaults per tenant and endpoint: GET 100, POST 100, PUT 50, DELETE 50 requests per second.
- Per-issue writes: 20 per 2 seconds and 100 per 30 seconds. A test that edits one issue in a tight loop can hit this.
- Apps (Forge, Connect, OAuth 3LO) on a Free tenant get 65,000 points per hour. The quota resets at the top of each UTC hour.
- Every limit answers HTTP 429. Read `Retry-After` and `RateLimit-Reason`. Back off exponentially with jitter, and retry only idempotent requests.
- Atlassian asks that no one run rate-limit tests against its cloud tenants.
- Agile move and rank calls take at most 50 issues each. [S40]

## Sources

- S1: https://crates.io/api/v1/crates/gpui-pre/owners and https://crates.io/api/v1/crates/gpui-pre
- S2: https://docs.rs/crate/gpui-pre-wgpu/0.3.12/source/Cargo.toml
- S3: https://docs.rs/crate/gpui-pre-platform/0.3.12/source/src/gpui_platform.rs and https://docs.rs/crate/gpui-pre-platform/0.3.12/source/Cargo.toml
- S4: https://github.com/longbridge/gpui-kit/blob/a3f473e855ae8041351ed962bc5186a885c3d612/Cargo.toml
- S5: https://docs.rs/crate/gpui-pre/0.3.12/source/Cargo.toml and https://docs.rs/crate/gpui-pre/0.3.12/source/src/platform.rs
- S6: https://docs.rs/gpui-pre/0.3.12/gpui/all.html
- S7: https://docs.rs/crate/gpui-pre-macros/0.3.12/source/src/test.rs
- S8: https://docs.rs/crate/gpui-pre/0.3.12/source/src/test.rs, https://docs.rs/crate/gpui-pre/0.3.12/source/src/seeds.rs, https://docs.rs/crate/gpui-pre/0.3.12/source/src/executor.rs
- S9: https://docs.rs/crate/gpui-pre/0.3.12/source/src/app/test_context.rs and https://docs.rs/crate/gpui-pre/0.3.12/source/src/platform/test/platform.rs
- S10: https://docs.rs/crate/gpui-pre/0.3.12/source/src/elements/div.rs
- S11: https://docs.rs/crate/gpui-pre-wgpu/0.3.12/source/src/wgpu_context.rs and https://docs.rs/crate/gpui-pre-wgpu/0.3.12/source/src/wgpu_renderer.rs
- S12: https://docs.rs/crate/gpui-base/0.10.0/source/src/test_support.rs
- S13: https://docs.rs/crate/gpui-kit/0.10.0/source/src/test.rs and https://github.com/longbridge/gpui-kit/blob/a3f473e855ae8041351ed962bc5186a885c3d612/crates/kit/tests/ui.rs
- S14: https://github.com/zed-industries/zed/blob/4a4c8150f03ef3c5e0c4f837dc0263c137f5b0ce/.github/workflows/run_tests.yml
- S15: https://github.com/longbridge/gpui-kit/blob/a3f473e855ae8041351ed962bc5186a885c3d612/.github/workflows/ci.yml
- S16: https://docs.rs/crate/gpui-pre/0.3.12/source/src/app/headless_app_context.rs
- S17: https://github.com/longbridge/gpui-kit/tree/a3f473e855ae8041351ed962bc5186a885c3d612/crates (see `kit/tests/rendering.rs`, `kit/Cargo.toml`, `base/src`)
- S18: https://docs.rs/crate/gpui-pre/0.3.12/source/src/app/visual_test_context.rs
- S19: https://github.com/zed-industries/zed/blob/4a4c8150f03ef3c5e0c4f837dc0263c137f5b0ce/crates/zed/src/visual_test_runner.rs
- S20: https://github.com/zed-industries/zed/blob/4a4c8150f03ef3c5e0c4f837dc0263c137f5b0ce/docs/src/development/macos.md
- S21: https://docs.rs/crate/gpui-pre-linux/0.3.12/source/src/linux.rs
- S22: https://docs.rs/crate/gpui-pre-linux/0.3.12/source/src/linux/headless/window.rs
- S23: https://docs.rs/crate/gpui-pre-linux/0.3.12/source/src/linux/display_connection.rs
- S24: https://github.com/zed-industries/zed/issues/63327
- S25: https://github.com/zed-industries/zed/issues/66309
- S26: https://github.com/zed-industries/zed/issues/63565
- S27: https://github.com/zed-industries/zed/blob/4a4c8150f03ef3c5e0c4f837dc0263c137f5b0ce/docs/src/linux.md
- S28: https://docs.rs/crate/gpui-pre/0.3.12/source/src/_accessibility.rs
- S29: https://docs.rs/crate/gpui-pre-linux/0.3.12/source/Cargo.toml
- S30: https://docs.rs/crate/gpui-pre/0.3.12/source/src/window.rs
- S31: https://github.com/zed-industries/zed/blob/4a4c8150f03ef3c5e0c4f837dc0263c137f5b0ce/crates/zed/src/zed.rs
- S32: https://docs.rs/crate/gpui-pre/0.3.12/source/src/platform/test/window.rs
- S33: https://github.com/zed-industries/zed/issues/66729
- S34: https://developer.atlassian.com/platform/marketplace/getting-started/
- S35: http://go.atlassian.com/cloud-dev (redirects to https://www.atlassian.com/try/cloud/signup?product=confluence.ondemand,jira-software.ondemand,jira-servicedesk.ondemand,jira-core.ondemand&developer=true)
- S36: https://community.atlassian.com/forums/Jira-questions/Is-there-an-expiration-date-for-a-free-Jira-instance/qaa-p/3199694 (community, not official)
- S37: https://www.atlassian.com/software/jira/pricing
- S38: https://developer.atlassian.com/platform/forge/provision-a-demo-development-site/
- S39: https://developer.atlassian.com/cloud/jira/platform/swagger-v3.v3.json
- S40: https://developer.atlassian.com/cloud/jira/software/swagger.v3.json
- S41: https://support.atlassian.com/jira-cloud-administration/docs/permissions-for-company-managed-projects/
- S42: https://community.atlassian.com/forums/Jira-questions/Company-Managed-Project-created-via-API/qaq-p/1866481 (community, not official)
- S43: https://jira.atlassian.com/browse/JRACLOUD-91386
- S44: https://jira.atlassian.com/browse/JRACLOUD-80743
- S45: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
