---
name: jira4manager-rust-desktop
description: "Native desktop app rules for Rust with Slint 1.x: markup in .slint files compiled by a build script, a presenter in plain Rust that turns an action into a view state, a view module that renders the state and wires callbacks, service calls that run on the tokio runtime and return to the UI thread, design tokens in a Slint global, accessible labels on controls and errors, headless tests through the Slint testing backend, and the Slint licence choice. The concrete mechanics behind ui-design-system, ui-accessibility and ui-context-ownership for this stack. Load when adding or changing a window, a component, a callback, a property or a UI test, when the UI freezes during a call, or when starting a desktop crate."
metadata:
  name: rust-desktop
  generated_by: farrier
  source: library/skills/stacks/rust/rust-desktop/SKILL.md
  resolve: "farrier source .claude/skills/jira4manager-rust-desktop/SKILL.md"
  do_not_edit: "generated — run the `resolve` command below for this machine's editable source path, edit that, then `make agent-install` to regenerate"
  tags: [rust, mobile, standards, tests, entrypoint]
---

# Desktop App

The generic contracts are [ui-design-system](~/.claude/skills/ui-design-system/SKILL.md), [ui-accessibility](~/.claude/skills/ui-accessibility/SKILL.md) and [ui-context-ownership](~/.claude/skills/ui-context-ownership/SKILL.md). This skill states how they land in a Slint app. Load [jira4manager-rust](../jira4manager-rust/SKILL.md) first for the crate map.

Slint draws its own widgets with its own renderer. The app ships as one native binary with no browser engine inside.

## Layout

```text
crates/desktop/
  build.rs            compiles ui/app.slint into Rust
  ui/
    app.slint         the window: properties in, callbacks out
    task-row.slint    one component per file
    tokens.slint      the Tokens global
  src/
    lib.rs            the generated module and the re-exports
    main.rs           runtime, composition root, ui.run()
    presenter.rs      Action in, ViewState out, no Slint type
    view.rs           render(state) and wire(callbacks)
```

## Data flow

1. The markup fires a callback such as `add(title)`.
2. `wire` turns it into an `Action` and spawns the presenter on the tokio runtime.
3. The presenter calls the service and returns a `ViewState`.
4. `render` runs on the UI thread and sets the window properties from that state.

State lives in one place: the service. The window holds the last rendered copy.

## Markup

```slint
export component TaskRow inherits HorizontalLayout {
    in property <TaskItem> task;
    callback complete();
    callback remove();

    spacing: Tokens.space-s;

    CheckBox {
        text: root.task.title;
        checked: root.task.done;
        enabled: !root.task.done;
        toggled => {
            root.complete();
        }
    }

    Button {
        text: "Remove";
        accessible-label: "Remove \{root.task.title}";
        clicked => {
            root.remove();
        }
    }
}
```

- Declare data as `in property` and events as `callback`. A component receives data from its parent and reports events to it.
- Keep markup free of rules about the data. A handler body calls a callback and clears its own input, nothing more.
- Declare a row type as an `export struct` in markup. The build generates the matching Rust struct.
- Show a conditional element with `if condition: Element`, and a list with `for item in root.items: Row` inside a `ListView`.
- A binding re-evaluates when a property it reads changes. Set the property from Rust and write no refresh call.
- Read every size, space and colour from the `Tokens` global. A literal `px` or colour value appears in `tokens.slint` alone, apart from the window's preferred size.

The full `app.slint` and `tokens.slint` are in [references/markup.md](references/markup.md). Copy from there when starting a window.

## Presenter

```rust
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ViewState {
    pub rows: Vec<Row>,
    pub error: Option<String>,
}

pub async fn handle(action: Action, tasks: &TaskService) -> ViewState {
    let failure = perform(action, tasks).await.err();
    match tasks.list().await {
        Ok(listed) => ViewState {
            rows: listed.iter().map(Row::from).collect(),
            error: failure.map(|error| error.to_string()),
        },
        Err(error) => ViewState {
            rows: Vec::new(),
            error: Some(error.to_string()),
        },
    }
}
```

- Write the presenter with no `slint` import. Its tests then run as plain `#[tokio::test]` functions over the fakes.
- Model every user intent as a variant of one `Action` enum, and return the whole `ViewState` each time.
- Carry a failure as text in the state. A rejected action keeps the rows on screen and shows the reason.

## View

```rust
pub fn wire(ui: &AppWindow, tasks: TaskService, runtime: Handle) {
    let weak = ui.as_weak();
    let dispatch = move |action: Action| {
        if let Some(ui) = weak.upgrade() {
            ui.set_busy(true);
        }
        let weak = weak.clone();
        let tasks = tasks.clone();
        runtime.spawn(async move {
            let state = presenter::handle(action, &tasks).await;
            let _ = weak.upgrade_in_event_loop(move |ui| render(&ui, state));
        });
    };

    ui.on_add({
        let dispatch = dispatch.clone();
        move |title| dispatch(Action::Add(title.into()))
    });
    dispatch(Action::Load);
}
```

The block shows one of the three callbacks.

- Run every service call on the tokio runtime with `runtime.spawn`. A call made inside the callback itself freezes the window until it returns.
- Return to the UI thread with `weak.upgrade_in_event_loop`. The window handle is not `Send`, so the task carries the `Weak` handle.
- Capture `ui.as_weak()` in every callback. A strong handle inside its own callback keeps the window alive forever.
- Set `busy` before the spawn and clear it in `render`. Markup binds `enabled: !root.busy` on the controls that must not fire twice.
- Fill a list property with `ModelRc::new(VecModel::from(items))`.
- Convert between `String` and Slint's `SharedString` with `.into()`.

## Build and lints

```rust
fn main() -> Result<(), slint_build::CompileError> {
    let debug = std::env::var("PROFILE").is_ok_and(|profile| profile == "debug");
    let config = slint_build::CompilerConfiguration::new().with_debug_info(debug);
    slint_build::compile_with_config("ui/app.slint", config)
}
```

```rust
#[allow(
    unsafe_code,
    clippy::all,
    clippy::pedantic,
    clippy::unwrap_used,
    clippy::expect_used
)]
mod ui {
    slint::include_modules!();
}
pub use ui::*;
```

- Compile the root `.slint` file in `build.rs`. A markup error then fails `cargo build` with a file and line.
- Turn debug info on for debug builds. The test API finds elements only when the markup was compiled with it.
- Include the generated code inside one module that carries the `allow` list. The workspace lints then apply to your code and skip the generated code.
- Keep `unsafe_code = "deny"` in the workspace lints. `forbid` cannot be overridden and breaks the build of this crate.

## Accessibility

- Set `accessible-label` on every control whose visible text does not name its target: a repeated "Remove" button, an icon button, a text field with only a placeholder.
- Give an error text `accessible-role: text` and a label that starts with "Error:". A screen reader then announces what a sighted user sees in red.
- Use the `std-widgets.slint` controls. They carry keyboard focus, roles and default actions that a hand-drawn `Rectangle` with a `TouchArea` lacks.

## Tests

```rust
fn window() -> AppWindow {
    i_slint_backend_testing::init_no_event_loop();
    AppWindow::new().unwrap()
}

#[test]
fn the_remove_button_reports_the_task_id() {
    let ui = window();
    let removed = Rc::new(RefCell::new(Vec::new()));
    ui.on_remove({
        let removed = removed.clone();
        move |id| removed.borrow_mut().push(id.to_string())
    });
    render(&ui, state(None));

    let button = ElementHandle::find_by_accessible_label(&ui, "Remove buy milk")
        .next()
        .unwrap();
    button.invoke_accessible_default_action();

    assert_eq!(*removed.borrow(), vec!["id-1".to_owned()]);
}
```

- Test the presenter for every state: success, rejected action, failed load. [jira4manager-rust-testing](../jira4manager-rust-testing/SKILL.md) covers the fakes.
- Test the view with `i-slint-backend-testing`. It runs with no display, so the tests pass in CI.
- Call `init_no_event_loop()` before creating the window in each test.
- Find elements by accessible label and act through `invoke_accessible_default_action()`. A test that passes this way proves the control is reachable by assistive technology.
- Pin the testing backend with `=` to the exact version of `slint` in `Cargo.lock`. Its API is internal and changes between minor releases.

## Licence

Slint ships under three licences: GPLv3, a royalty-free licence that requires attribution, and a paid one. Ask the project owner which applies before the first release build, and record the answer in the repo README.

## Closing check

```bash
cargo test -p tally-desktop
cargo run -p tally-desktop
```

The window opens, the changed control works with the keyboard alone, and a failed action shows its reason. Then run the closing commands in [jira4manager-rust](../jira4manager-rust/SKILL.md).
