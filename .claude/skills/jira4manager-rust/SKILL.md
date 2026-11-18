---
name: jira4manager-rust
description: "Entry point for Rust work: one Cargo workspace with a core crate and thin API, CLI and desktop hosts. Holds the crate map, the language rules that a C++ or C# habit gets wrong (ownership, errors, enums, async), the workspace lint set, the sibling skill hierarchy and the cargo closing commands. Siblings cover architecture, di, api, cli, desktop and testing. Load when starting any Rust task, before the sibling that matches the files you touch."
metadata:
  name: rust
  generated_by: farrier
  source: library/skills/stacks/rust/rust/SKILL.md
  resolve: "farrier source .claude/skills/jira4manager-rust/SKILL.md"
  do_not_edit: "generated — run the `resolve` command below for this machine's editable source path, edit that, then `make agent-install` to regenerate"
  tags: [rust, backend, standards, runbook, entrypoint]
---

# Rust Workspace

This is the root skill for a Rust workspace. Load it first, then load the sibling that matches the files you will touch. Examples use an app named `tally`.

## Crate map

| Crate | Package | Holds |
|---|---|---|
| `crates/core` | `tally-core` | Domain types, port traits, services, fakes behind the `test-support` feature |
| `crates/infra` | `tally-infra` | Adapters that implement the ports: files, databases, HTTP clients, the system clock |
| `crates/api` | `tally-api` | The axum host: routes, error mapping, config, composition root |
| `crates/cli` | `tally-cli` | The clap host: argument tree, `run`, composition root |
| `crates/desktop` | `tally-desktop` | The Slint host: markup, presenter, view wiring, composition root |

A feature lands in `tally-core` first. A host changes only to expose the feature on its own surface.

## Sibling skills

- Crates, feature modules, domain types and errors: [jira4manager-rust-architecture](../jira4manager-rust-architecture/SKILL.md)
- Ports, services and composition roots: [jira4manager-rust-di](../jira4manager-rust-di/SKILL.md)
- HTTP API with axum: [jira4manager-rust-api](../jira4manager-rust-api/SKILL.md)
- Command line with clap: [jira4manager-rust-cli](../jira4manager-rust-cli/SKILL.md)
- Desktop app with Slint: [jira4manager-rust-desktop](../jira4manager-rust-desktop/SKILL.md)
- Tests, fakes and harnesses: [jira4manager-rust-testing](../jira4manager-rust-testing/SKILL.md)

When two rules conflict, the more specific sibling wins within its domain.

## Language rules

- Take `&str`, `&[T]` and `&Path` as parameters. Return owned values.
- Share a service or a port by cloning its `Arc`. Clone data only when two owners must change it apart from each other.
- Return `Result<T, E>` from every function that can fail, and pass the error up with `?`. Keep `unwrap`, `expect` and `panic!` inside tests.
- Model a missing value with `Option<T>`. Model "one of several shapes" with an `enum`.
- Write a `match` on your own enum with one arm per variant. A new variant then fails the build at every site that must handle it.
- Wrap a validated value in a newtype with a private field and a `parse` constructor. Code that holds the type then holds a valid value.
- Share behaviour with a trait and composition. Rust has no class inheritance.
- Derive `Debug, Clone, PartialEq, Eq` on data types, so tests can compare them and logs can print them.
- When the borrow checker rejects code, change who owns the value first: pass a reference, end the borrow sooner, or move the value. Reach for `.clone()`, `Rc<RefCell<T>>` or a lifetime parameter on a struct last.
- Inside `async` code call the async form: `tokio::fs`, `tokio::time::sleep`, `tokio::sync`. A blocking call stalls every task on that worker thread. Send CPU-heavy work to `tokio::task::spawn_blocking`.
- Drop a `std::sync::Mutex` guard before the next `.await`. Use `tokio::sync::Mutex` when the lock must span one.
- Write output through a `Write` handle or `tracing`. The lint set rejects `println!` and `dbg!`.

## Workspace rules

- Declare every dependency version once in `[workspace.dependencies]` in the root `Cargo.toml`. A member crate writes `name.workspace = true`.
- End every member `Cargo.toml` with `[lints] workspace = true`.
- The workspace lints deny `unsafe_code`, `clippy::all`, `unwrap_used`, `expect_used`, `dbg_macro` and `print_stdout`, and warn on `clippy::pedantic`.
- Fix a lint in the code. Add `#[allow(...)]` on the smallest item only for generated code or a test file, and never in the root `Cargo.toml`.
- Commit `Cargo.lock`.

The full root `Cargo.toml`, `clippy.toml`, `rust-toolchain.toml` and a member manifest are in [references/workspace.md](references/workspace.md). Copy from there when starting a workspace or adding a crate.

## Running a host

```bash
cargo run -p tally-api
cargo run -p tally-cli -- list --format json
cargo run -p tally-desktop
```

## Closing commands

Run these from the workspace root before reporting a change done. Each must exit 0.

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

`cargo fmt --all` rewrites the files when the first command fails.
