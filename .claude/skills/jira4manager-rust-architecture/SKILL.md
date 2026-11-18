---
name: jira4manager-rust-architecture
description: "Architecture rules for a Rust workspace: which crate may depend on which, feature modules inside the core crate, newtype domain values that parse at the boundary, one thiserror enum per feature with anyhow kept in the hosts, record types that keep serde out of the domain, and host crates split into a library and a thin main. The concrete mechanics behind hexagonal-architecture and code-structure for this stack. Load when adding a crate, a feature module, a domain type or an error variant, when a dependency points the wrong way, or when deciding where a type belongs."
metadata:
  name: rust-architecture
  generated_by: farrier
  source: library/skills/stacks/rust/rust-architecture/SKILL.md
  resolve: "farrier source .claude/skills/jira4manager-rust-architecture/SKILL.md"
  do_not_edit: "generated — run the `resolve` command below for this machine's editable source path, edit that, then `make agent-install` to regenerate"
  tags: [rust, backend, standards]
---

# Architecture

The generic contracts are [hexagonal-architecture](~/.claude/skills/hexagonal-architecture/SKILL.md) and [code-structure](~/.claude/skills/code-structure/SKILL.md). This skill states how they land in a Cargo workspace. The crate map is in [jira4manager-rust](../jira4manager-rust/SKILL.md).

## Dependency direction

| Crate | May depend on | Carries |
|---|---|---|
| `tally-core` | `thiserror`, `async-trait`, value crates such as `chrono` and `uuid` | The domain and the ports |
| `tally-infra` | `tally-core`, `serde`, `tokio`, driver crates | The adapters |
| a host (`api`, `cli`, `desktop`) | `tally-core`, `tally-infra`, its own framework, `anyhow` | One delivery surface |

- A crate boundary is the layer boundary. The compiler rejects an import that the manifest does not allow, so the manifest is the rule.
- Keep axum, clap, Slint, serde and the tokio runtime out of `tally-core`. Core lists `tokio` under `[dev-dependencies]` alone, for `#[tokio::test]`.
- Give the package a prefixed name such as `tally-core`. A package named `core` shadows the standard library crate of the same name.
- A host never depends on another host.

## Feature modules

Core groups code by feature, and each feature folder holds its own model, ports, errors and service.

```text
crates/core/src/
  lib.rs
  testing.rs
  tasks/
    mod.rs
    model.rs
    ports.rs
    error.rs
    service.rs
```

```rust
mod error;
mod model;
mod ports;
mod service;

pub use error::TaskError;
pub use model::{Task, TaskId, Title};
pub use ports::{Clock, TaskRepository};
pub use service::TaskService;
```

- Keep the files private and re-export the public names from `mod.rs`. Callers write `tally_core::tasks::TaskService`, and a file can be split later without touching them.
- A feature imports another feature through that feature's `mod.rs` exports.

## Domain values

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Title(String);

impl Title {
    pub const MAX_CHARS: usize = 120;

    pub fn parse(raw: &str) -> Result<Self, TaskError> {
        let trimmed = raw.trim();
        let length = trimmed.chars().count();
        if length == 0 || length > Self::MAX_CHARS {
            return Err(TaskError::InvalidTitle);
        }
        Ok(Self(trimmed.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

- Validate in the constructor and keep the field private. A service that receives a `Title` does no further checks.
- Implement `FromStr` on an identifier newtype. A route writes `id.parse()?` and clap parses the argument with the same code.
- Implement `Display` for the text form. Hosts print with `to_string()` and never reach into the field.

## Errors

```rust
#[derive(Debug, thiserror::Error)]
pub enum TaskError {
    #[error("title must be 1 to 120 characters")]
    InvalidTitle,
    #[error("task id is not a valid identifier")]
    InvalidId,
    #[error("task {0} not found")]
    NotFound(TaskId),
    #[error("task storage failed")]
    Storage(#[source] Box<dyn std::error::Error + Send + Sync>),
}
```

- Write one error enum per feature in core, with `thiserror`. Each variant is a case a host answers differently.
- Carry an adapter failure as a boxed `#[source]`. Core then names no driver error type, and the cause chain still reaches the log.
- Use `anyhow::Result` in host code alone: `main`, config loading and CLI `run`. Add `.context("...")` where the message needs the name of the file, variable or address.
- Map the core enum to the surface in one place per host: a status code in the API, an exit code in the CLI, a message in the desktop app.

## Adapters

```rust
#[derive(Serialize, Deserialize)]
struct TaskRecord {
    id: String,
    title: String,
    done: bool,
    created_at: DateTime<Utc>,
}

impl TryFrom<TaskRecord> for Task {
    type Error = TaskError;

    fn try_from(record: TaskRecord) -> Result<Self, Self::Error> {
        Ok(Self {
            id: record.id.parse()?,
            title: Title::parse(&record.title)?,
            done: record.done,
            created_at: record.created_at,
        })
    }
}

fn storage(error: impl std::error::Error + Send + Sync + 'static) -> TaskError {
    TaskError::Storage(Box::new(error))
}
```

- Give each adapter its own private record type with the serde derives. The stored shape can then change without touching the domain type.
- Convert with `From<&Task>` on the way out and `TryFrom<Record>` on the way in. Stored data passes through the same `parse` as user input.
- Turn every driver error into the feature error with one helper, and call it as `.map_err(storage)`.

## Host crates

- Split each host into `src/lib.rs` and a `src/main.rs` under 40 lines. Integration tests in `tests/` import the library and cannot import a binary.
- `main.rs` reads config, calls the composition root from [jira4manager-rust-di](../jira4manager-rust-di/SKILL.md), starts the surface and maps the final error to an exit code.

## Closing check

```bash
cargo tree -p tally-core -e normal --depth 1
```

The output lists no web, CLI, UI, serde or runtime crate. Then run the closing commands in [jira4manager-rust](../jira4manager-rust/SKILL.md).
