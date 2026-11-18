# Platform research, 2026-11-17

The kickoff brief asks to verify GPUI, gpui-component and Jira facts before writing code. This record lists what was read on 2026-11-17 and where. Facts marked UNCONFIRMED were not found on an official page.

## gpui-component

- The latest release on crates.io is 0.10.0, published 2026-11-16. Releases ship about weekly. Source: https://crates.io/api/v1/crates/gpui-component
- 0.10.0 depends on `gpui-pre = "=0.3.12"` from crates.io, not on a git revision of zed. It also pulls `gpui-base` and `gpui-kit-assets` at `^0.10.0`. Source: https://crates.io/api/v1/crates/gpui-component/0.10.0/dependencies
- The README tells apps to depend on `gpui-kit`, which pins a matching GPUI and re-exports base, component and assets. UNCONFIRMED: which `gpui-component` version each `gpui-kit` release pulls in. Source: https://raw.githubusercontent.com/longbridge/gpui-component/main/README.md
- `Root`, `theme`, `sidebar`, `popover`, `list`, `table` and `input` are public. Source: https://raw.githubusercontent.com/longbridge/gpui-component/main/crates/component/src/lib.rs
- `InputState` has no `.multi_line()` any more. Multi-line input is `Textarea` with `TextareaState`. This differs from the kickoff brief. Source: https://raw.githubusercontent.com/longbridge/gpui-component/main/crates/component/src/input/textarea.rs
- `TextView` renders Markdown, with `TextViewState` and `MarkdownPlugin`. Source: https://raw.githubusercontent.com/longbridge/gpui-component/main/crates/component/src/text/mod.rs
- The story crate is `crates/story`. Examples live under `examples/`, for example `examples/markdown` and `examples/sidebar`.
- UNCONFIRMED: the light and dark switching API and custom colour overrides.

## GPUI platform requirements

- Linux needs `gpui_platform` with the `wayland` feature, the `x11` feature or both. Source: https://raw.githubusercontent.com/zed-industries/zed/main/crates/gpui/README.md
- Zed's `script/linux` installs libvulkan1, libwayland-dev, libxkbcommon-x11-dev, libx11-xcb-dev, libfontconfig-dev, libssl-dev, clang, cmake and more. Many of them serve Zed rather than GPUI alone. Source: https://raw.githubusercontent.com/zed-industries/zed/main/script/linux
- macOS needs full Xcode for Metal, `xcode-select --switch`, and the `font-kit` feature or no glyphs draw.
- Windows needs no feature flags. It uses Win32 and DirectWrite.
- GPUI is pre-1.0 and expects breaking changes.

## Jira Cloud REST

Source unless noted: https://dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json

- `POST /rest/api/3/search/jql` takes `jql`, `fields`, `expand`, `maxResults`, `nextPageToken`, `properties`, `fieldsByKeys`, `reconcileIssues` and `includeArchivedProjects`.
- Its response holds `issues`, `nextPageToken` and `isLast`. It has no `total` and no `startAt`. A page token expires after 7 days.
- JQL must be bounded. `assignee = currentUser() ORDER BY updated DESC` is bounded.
- The old `/rest/api/3/search` is removed (CHANGE-2046). Source: https://confluence.atlassian.com/jirakb/run-jql-search-query-using-jira-cloud-rest-api-1289424308.html
- `GET /rest/api/3/myself` returns `accountId`, `displayName`, `avatarUrls`, `timeZone` and `emailAddress`. Privacy settings can hide the email.
- `GET /rest/api/3/project/search` pages with `startAt` and `maxResults` (at most 100) and returns `isLast` and `values`.
- A status carries `statusCategory` with `id`, `key`, `name` and `colorName`. UNCONFIRMED from a page: the keys `new`, `indeterminate` and `done`.
- On 429, `Retry-After` gives the minimum wait in seconds. `RateLimit-Reason` names the quota. Atlassian advises exponential backoff from about 2 s with 0.7 to 1.3 jitter, about 4 attempts, and retries of idempotent requests only. Source: https://developer.atlassian.com/cloud/jira/platform/rate-limiting/
- Basic auth with email and API token still works against the site URL. Source: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
- API tokens last 1 to 365 days. Scoped tokens must call `https://api.atlassian.com/ex/jira/{cloudId}` instead of the site URL. Source: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
- The basic-auth page says apps that collect users' API tokens do not meet Atlassian's security requirements for apps. That rule targets distributed integrations. This client keeps the user's own token on the user's own machine.

## Naming

- Atlassian allows "Acme for Jira" and refuses "Jira Acme". The Atlassian mark must not outrank the product name or appear in its logo. Source: https://www.atlassian.com/legal/trademark
