---
name: jira4manager-rust-cli
description: "Command line rules for Rust with clap 4 derive: one Cli struct with global flags and a Command enum, arguments parsed straight into domain types, a run function that takes the service and a Write handle, a main that owns the runtime and the exit code, data on stdout and errors on stderr, a --format flag for JSON and a --dry-run flag on destructive commands. Load when adding or changing a subcommand, a flag, an output format or an exit code, or when starting a CLI crate."
metadata:
  name: rust-cli
  generated_by: farrier
  source: library/skills/stacks/rust/rust-cli/SKILL.md
  resolve: "farrier source .claude/skills/jira4manager-rust-cli/SKILL.md"
  do_not_edit: "generated — run the `resolve` command below for this machine's editable source path, edit that, then `make agent-install` to regenerate"
  tags: [rust, cli, standards, entrypoint]
---

# Command Line

Load [jira4manager-rust](../jira4manager-rust/SKILL.md) first for the crate map and the closing commands. The CLI is a host: it parses arguments, calls the same services as the API and prints the result.

## Layout

```text
crates/cli/
  src/
    lib.rs        re-exports Cli, Command, Format, compose, run
    main.rs       parse, runtime, exit code
    cli.rs        the clap types
    compose.rs    the composition root
    run.rs        one match arm per command
  tests/
    cli.rs        the built binary, end to end
```

Name the binary with a `[[bin]]` table, so the package stays `tally-cli` and the user types `tally`.

## Arguments

```rust
#[derive(Debug, Parser)]
#[command(name = "tally", version, about = "Track tasks in a local file")]
pub struct Cli {
    #[arg(
        long,
        env = "TALLY_DATA_FILE",
        default_value = "tally.json",
        global = true
    )]
    pub data_file: PathBuf,

    #[arg(long, value_enum, default_value_t = Format::Text, global = true)]
    pub format: Format,

    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, ValueEnum)]
pub enum Format {
    Text,
    Json,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Add a task
    Add { title: String },
    /// List tasks, oldest first
    List {
        /// Show only tasks that are not done
        #[arg(long)]
        pending: bool,
    },
    /// Mark a task done
    Done { id: TaskId },
    /// Remove a task
    Rm {
        id: TaskId,
        /// Print what would be removed and change nothing
        #[arg(long)]
        dry_run: bool,
    },
}
```

- Declare the whole surface as one `Cli` struct and one `Command` enum. The `///` line above a variant or a field is its `--help` text, so write it for the user.
- Type an argument as the domain type when that type implements `FromStr`. clap then rejects a malformed value as a usage error before any code runs.
- Mark a flag that every subcommand accepts as `global = true`.
- Bind a setting to an environment variable with `env = "..."`. The flag wins over the variable, and the variable wins over the default.
- Give every command that deletes or overwrites a `--dry-run` flag.

## Run

```rust
pub async fn run(
    command: Command,
    format: Format,
    tasks: &TaskService,
    out: &mut impl Write,
) -> anyhow::Result<()> {
    match command {
        Command::Add { title } => {
            let task = tasks.add(&title).await?;
            render(out, format, &[task])
        }
        Command::Rm { id, dry_run } => {
            let task = tasks.get(id).await?;
            if dry_run {
                writeln!(out, "would remove {} {}", task.id, task.title.as_str())?;
            } else {
                tasks.remove(id).await?;
                writeln!(out, "removed {}", task.id)?;
            }
            Ok(())
        }
    }
}
```

The block shows two of the four arms.

- Take the service and the output handle as parameters. A test passes fakes and a `Vec<u8>`, and asserts on the exact text.
- Write with `writeln!(out, ...)`. The lint set rejects `println!`, which would also bypass the handle.
- Render every command through one function that switches on `Format`.

## Main

```rust
fn main() -> ExitCode {
    let cli = Cli::parse();
    match execute(cli) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("error: {error:#}");
            ExitCode::FAILURE
        }
    }
}

fn execute(cli: Cli) -> anyhow::Result<()> {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()?;
    let tasks = compose(&cli.data_file);
    let mut out = std::io::stdout().lock();
    runtime.block_on(run(cli.command, cli.format, &tasks, &mut out))
}
```

- Return `ExitCode` from `main` and print the error yourself. Returning the `Result` from `main` prints the `Debug` form, which users cannot read.
- Format the error with `{error:#}`. That prints the message and each cause on one line, such as `error: task storage failed: expected value at line 1 column 1`.
- Build a current-thread runtime. A command runs one task, and worker threads would only slow the start.

## Output contract

| Stream or code | Carries |
|---|---|
| stdout | The result alone. Text is one record per line. `--format json` is one JSON value on one line |
| stderr | `error: ...` and nothing else |
| exit 0 | Success |
| exit 1 | The command ran and failed |
| exit 2 | Bad usage, reported by clap |

- Keep stdout free of progress text and decoration, so a pipe into `jq` or `grep` works.
- Serialize JSON from a private output struct in `run.rs`, converted with `From<&Task>`.

## Tests

- Add one unit test that calls `Cli::command().debug_assert()`. It fails on a duplicate flag or a broken default.
- Test each `run` arm with the fakes and a `Vec<u8>`.
- Test the binary in `tests/cli.rs` with `assert_cmd` for one success path, exit 1 and exit 2. [jira4manager-rust-testing](../jira4manager-rust-testing/SKILL.md) shows the harness.

## Closing check

```bash
cargo test -p tally-cli
cargo run -p tally-cli -- --help
```

The help output lists the new command or flag with its description. Then run the closing commands in [jira4manager-rust](../jira4manager-rust/SKILL.md).
