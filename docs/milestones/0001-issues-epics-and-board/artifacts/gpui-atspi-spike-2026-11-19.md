# GPUI over AT-SPI on headless Linux, spike, 2026-11-19

This spike asks whether an outside process can read and drive a GPUI window through AT-SPI on Linux with no desktop session. An ostler desktop driver would rest on that answer. Every statement below comes from a run on 2026-11-19 unless it names a source file.

## Verdict

Go, with five conditions. An outside process reads the tree, clicks through AT-SPI actions, types through XTest and waits on AT-SPI events. The conditions are listed under "Go or no-go" at the end.

## Setup

- App: `longbridge/gpui-kit` at `a3f473e`, the `gpui-component-story` gallery, `gpui-pre` 0.3.12 from crates.io. The gallery takes a story name as its first argument.
- One scratch change: the Checkbox story gained a probe element, `div().id("spike-probe").role(Role::Button).aria_label("Spike probe").accessibility_id("spike.probe").on_click(...)`. It tests question 4 and prints `SPIKE_PROBE_CLICKED` on click.
- Adapter crates in the build: `accesskit` 0.24.1, `accesskit_unix` 0.22.1, `accesskit_atspi_common` 0.19.1, `accesskit_consumer` 0.38.0.
- Host: Ubuntu with libatspi 2.52, Rust 1.99.1, Mesa lavapipe.
- Debug build: `cargo build -p gpui-component-story --no-default-features`. Release build: the same with `--release`.
- The link failed on `-lxkbcommon-x11` because `libxkbcommon-x11-dev` is not installed. A scratch symlink `libxkbcommon-x11.so -> /usr/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0` and `LIBRARY_PATH=<that dir>` fixed it. No package was installed.
- `xdotool` and `python3-xlib` are not installed. XTest input went through `ctypes` on `libXtst.so.6` and `libX11.so.6`: `XTestFakeMotionEvent`, `XTestFakeButtonEvent`, `XTestFakeKeyEvent`, `XSetInputFocus`, `XMoveWindow`.
- `python3-gi` with `Atspi` 2.0 is installed and read the tree.

The session, with no window manager and no desktop:

```sh
/usr/bin/Xvfb :99 -screen 0 1600x1000x24 -nolisten tcp &
DISPLAY=:99 dbus-run-session -- bash -c '
  /usr/libexec/at-spi-bus-launcher --launch-immediately &
  sleep 1
  /usr/libexec/at-spi2-registryd &
  exec sleep infinity' &
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json DISPLAY=:99 \
  ./target/debug/gpui-component-story checkbox
```

Every later command exported the `DBUS_SESSION_BUS_ADDRESS` that this session printed. The launcher put the accessibility bus at `unix:path=/run/user/1000/at-spi/bus_99`, separate from the host desktop's bus. The registry answered as `org.a11y.atspi.Registry`. D-Bus also activated `xdg-desktop-portal-gtk` in the private session. It appeared as a second application on the AT-SPI desktop and did no harm.

## 1. Does the tree activate and show over AT-SPI?

Yes.

- In a fresh `dbus-run-session`, `org.a11y.Status` read `IsEnabled=false` and `ScreenReaderEnabled=false`. The running app did not appear on the AT-SPI desktop. `Atspi.get_desktop(0)` listed only the portal.
- Setting `IsEnabled` to true made the app appear within three seconds, with no restart. Its tree then held 29 nodes in the Checkbox story.
- Setting `IsEnabled` back to false removed the app from the desktop.
- Setting `ScreenReaderEnabled` to true with `IsEnabled` false also turned it on. The bus launcher set `IsEnabled` to true in response. Setting `ScreenReaderEnabled` back to false left `IsEnabled` true.
- An app launched while `IsEnabled` was already true appeared at startup.
- So `IsEnabled` is the switch. `accesskit_unix` watches only that property (`context.rs` subscribes to `receive_is_enabled_changed`).

```sh
gdbus call --session --dest org.a11y.Bus --object-path /org/a11y/bus \
  --method org.freedesktop.DBus.Properties.Set org.a11y.Status IsEnabled '<true>'
gdbus call --session --dest org.a11y.Bus --object-path /org/a11y/bus \
  --method org.freedesktop.DBus.Properties.Get org.a11y.Status IsEnabled
```

A debug build can crash on activation. The Input story ran with `IsEnabled` false. It panicked the moment `IsEnabled` turned true: `Duplicate a11y node id: #15007387455317525299. In a release build, this node would be silently discarded from the a11y tree.` The check is a `debug_assert!` in `gpui-pre` `src/window/a11y.rs:415`. The release build of the same story started with the tree active and exposed 77 nodes. See question 2.

## 2. Roles, names, values and states

GPUI flattens the tree. Only elements that set a role appear, so layout divs vanish. In the Input story 63 of 77 nodes sat directly under the `frame`. Only role-bearing containers kept children: the menu bar, an open menu, a list and the message composer. The `frame` is named after the window title.

| Control | AT-SPI role | Name | Value or text | States seen | Actions |
| --- | --- | --- | --- | --- | --- |
| Button with a label | `push button` | the label, "Danger" | none | `enabled`, `focusable`, `sensitive`, `showing`, `visible`, `focused` when focused | `click` |
| Icon button | `push button` | empty | none. The tooltip text is the description, "Hide sidebar" | as above | `click` |
| Toggle button | `toggle button` | the label, "One" | none | as above | `click` |
| Text input | `entry` | the placeholder, "Search…" | Text interface returns the current text, "checkbox" | `editable`, `single-line`, `selectable-text`, `focusable`, `focused` when focused | none |
| Checkbox | `check box` | the label, "Product updates". An unlabelled one has an empty name | none | `checkable`, plus `checked` or `indeterminate` | `click` |
| Disabled checkbox | `check box` | the label | none | `checkable`, `read-only`, and no `enabled`, `sensitive` or `focusable` | none |
| List (List story) | `list` | empty | none | `enabled`, `focusable` | none |
| List row | `list item` with a `label` child | the row is unnamed. The `label` child carries the text, "Rodriguez Inc" | none | `selectable` | `click` |
| Select trigger | `combo box` | empty, or the author label, "Programming language" | none. The visible value "Argentina (AR)" is absent | `enabled`, `focusable`. A disabled one shows `read-only` | `click`, plus the Selection interface |
| Select popup | `list` holding an `entry` "Search…" and `list item` rows | rows unnamed, group headers included | none | `selectable` | `click` |
| Gallery sidebar row | `tree item` | "Checkbox" | none | `selectable`, `selected` | `click` |
| App menu bar | `menu bar` holding `push button`s | "Edit", "Go", "Help" | none | `focusable` | `click` |
| Menu trigger (Menu story) | `push button` | "Edit" | none | `focusable` | none |
| Open popup menu | `dialog` > `menu` > `menu item` | "Copy", "Paste". Separators are unnamed 2 px `menu item`s | none | `menu` is `focused`. Items are `selectable`, some `checkable` | `click` on items |
| Disabled menu item | `menu item` | "Disabled Item" | none | still reports `enabled` | none |
| Progress bar | `progress bar` | empty | Value interface `[0, 25, 100]` | none | none |

The release build of the Input story added these facts about text inputs:

- An input's name is its placeholder ("Enter text here...") or its form label ("Full name"). An input with neither has an empty name.
- The Text interface returns the value: "Jane Doe", "jane.doe@example.com", "Hello 世界，this is GPUI component, this is a long text."
- A password input has the role `password text` and no Text interface. Its value cannot be read.
- `Input::new(...).disabled(true)` and `.readonly(true)` reported `editable`, `enabled` and `focusable`, the same as a normal input. Only the text "This is disabled input" told them apart.
- Inline chips inside the message composer appeared as `push button` children of its `entry`, named "Alice" and "Image 1".

Gaps a driver must live with:

- The select's current value never reaches AT-SPI. gpui-kit sets it: `crates/component/src/select.rs` passes `accessibility_value` to an AccessKit `aria_value`, and its tests assert "Rust". `accesskit_atspi_common` 0.19.1 maps a string value to the name only for `Role::Label`, exposes Text only for nodes with text runs, and exposes Value only for numbers. A combo box value falls through all three.
- Select options and list rows have no name unless the author passes `accessibility_label`. In the List story the text sits on a `label` child. In the Select popup it is not exposed at all.
- Some buttons have no Action interface: the Menu story's "Edit" trigger, "Size: Medium", "Options" and "Send". `do_action` cannot open them. An XTest click can.
- `showing` and `visible` do not mean on screen. Checkboxes at y=1036 in an 850 px tall window reported both.
- A disabled menu item reports `enabled`. Only the missing `click` action shows it is disabled.
- A disabled or read-only text input looks editable. A disabled checkbox, by contrast, drops `enabled` and gains `read-only`.
- A password value cannot be read.

## 3. Do actions work?

Partly. AT-SPI click and focus work. Setting text through AT-SPI does not. XTest clicks and keys work once the window origin is added.

AT-SPI actions, read back from the tree after each one:

- `Atspi.Action.do_action(node, 0)` returned true and acted every time. It toggled "Product updates" to `checked`. It ran the probe's click handler, and the app log printed `SPIKE_PROBE_CLICKED`. It activated the "Copy" menu item and the menu closed. It opened a select's popup.
- The click is synthetic. GPUI turns `Action::Click` into a mouse down and up at the node's centre unless the element registered an action listener (`gpui-pre` `src/window.rs`, `handle_a11y_action`).
- `Atspi.Component.grab_focus(node)` returned true. The `focused` state moved from the entry to the "Danger" button and back.
- No node reported `focused`, and the frame lacked `active`, until the X window held input focus. Xvfb runs no window manager, so nothing gives the window focus. `XSetInputFocus(window)` gave the frame `active` and the focused node `focused`. GPUI forwards X `FocusIn` to `adapter.update_window_focus_state`.
- Setting text failed. The entry exposes Text but not EditableText. `Atspi.EditableText.set_text_contents` raised `Unknown interface 'org.a11y.atspi.EditableText'`. `accesskit_unix` 0.22.1 has no EditableText interface at all.

XTest at the AT-SPI bounds:

- The window sat at (122, 75), read with `xwininfo -name "GPUI Component"`.
- "Cargo.toml" reported extents (767, 622, 104, 18). An XTest click at its centre in those raw coordinates did nothing. An XTest click at the centre plus (122, 75) checked it.
- An XTest click on the search entry, then `Control+a` and the keys `b u t t o n`, set its text to "button". The gallery filtered its sidebar to "Button" and "DropdownButton".
- With the window focused, `grab_focus` on the entry and then XTest keys with no click typed into it.

The bounds ignore the window position. Zed issue #66729 is confirmed:

- The SCREEN and WINDOW coordinate types returned the same extents for every node.
- `XMoveWindow` moved the window from (122, 75) to (300, 20). A combo box reported (667, 260, 280, 32) before and after the move.
- The `frame` reported extents (-1, -1, -1, -1) in both coordinate types.
- Cause, from source: `gpui-pre-linux` 0.3.12 defines `a11y_update_window_bounds`, which would call `adapter.set_root_window_bounds`. A grep of `gpui-pre` and `gpui-pre-linux` finds no caller. The adapter never learns the window origin.

## 4. Do element ids reach `accessible_id`?

Partly. `.id()` does not. `.accessibility_id()` does.

- Every element built with an id and no accessibility id read `accessible_id` "". Examples: `Checkbox::new("updates")` and the story's `Button`s.
- The probe built with `.accessibility_id("spike.probe")` read `accessible_id` "spike.probe". `find(aid="spike.probe")` found it and `do_action` clicked it.
- The method sits on `StatefulInteractiveElement`, so the element needs `.id()` first. It sets AccessKit `author_id`. `accesskit_atspi_common` 0.19.1 returns `author_id` from `accessible_id` (`node.rs:837`).
- gpui-kit forwards an accessibility id only from its input state (`with_accessibility_id`) and textarea. Its Button, Checkbox and Select take none at `a3f473e`. The app would wrap them or extend gpui-kit.

## 5. Do change events fire?

Yes. A driver can wait on events.

An `Atspi.EventListener` on `object:` events recorded these, each with the trigger's own timestamp before it:

| Trigger | Events | Delay |
| --- | --- | --- |
| `grab_focus` on "Danger" | `state-changed:focused` 1 on "Danger", then 0 on the entry | 0.23 s |
| `grab_focus` on the entry | `state-changed:focused` 1 on the entry, `text-caret-moved`, `focused` 0 on "Danger" | 0.17 s |
| XTest key `x` in the entry | `text-changed:insert` with `any='x'`, `text-caret-moved` | 0.17 s |
| XTest BackSpace | `text-changed:delete` with `any='x'`, `text-caret-moved` | 0.11 s |
| `do_action` on "Product updates" | `state-changed:checked` 1 | 0.33 s |
| The same `x` filtered the Button story away, and BackSpace brought it back | 60 `children-changed:remove` on the frame and 64 `state-changed:defunct` after `x`, then one `children-changed:add` per node after BackSpace | 0.24 s to the first remove, 0.20 s to the first add |

The delays include the trigger script's own tree walk to find the node. They bound the event latency from above.

libatspi 2.52 printed `AT-SPI: AddAccessible with unknown signature (so)(so)(so)iiassusau` and `Unknown signature so for RemoveAccessible` once per changed node. The warnings come from the cache signals `accesskit_unix` emits. Queries and events kept working while they printed. A driver should silence that log domain.

## 6. Does the window render under Xvfb with lavapipe?

Yes. The window rendered fully and was not transparent.

- `import -window root shot.png` captured the Select story with its popup open. See `gpui-atspi-spike-2026-11-19-select.png` beside this note.
- The window region had a mean brightness of 0.986 and 7,920 distinct colours. A transparent window would show the black root.
- Lavapipe drew it. The process mapped `libvulkan_lvp.so` and no DRI GL driver. It ran Mesa's `WSI swapchain` threads and `llvmpipe-N` worker threads.
- The story's logger drops `log` crate records, so GPUI's "Testing adapter" line never printed. The library map is the evidence instead.
- Mesa printed `libEGL warning: DRI3 error: Could not get DRI3 device`. It came from the GL backend probe and changed nothing.

## Go or no-go

Go for an ostler desktop driver that reads AT-SPI, clicks through `do_action` and types through XTest. It holds under these conditions:

1. The driver owns the session. It starts Xvfb, a private `dbus-run-session`, `at-spi-bus-launcher` and `at-spi2-registryd`. It sets `IsEnabled` to true before it launches the app.
2. The driver gives the window X input focus with `XSetInputFocus`. Without a window manager nothing else does, and `focused` never appears.
3. The driver adds the window origin, read from X, to every extent before an XTest click. The fix belongs upstream: GPUI should call `a11y_update_window_bounds`.
4. jira4manager sets a stable `accessibility_id` on every element a journey targets. Names alone break on unnamed rows, icon buttons and select options. gpui-kit's Button, Checkbox and Select need a wrapper or a patch to take one.
5. Journeys run a release build, or the app keeps AccessKit ids unique. A debug build panics on the first duplicate once the tree is active. That panic could also serve as a test that ids are unique.

Two gaps stay open under a go:

- Text goes in through XTest keys only. AT-SPI has no EditableText here. Typing needs the target focused first, through `grab_focus` or a click.
- A select's current value cannot be read. A journey that checks a chosen value must read it elsewhere, for example from an author `accessibility_label` that includes the value, or after an `accesskit_atspi_common` fix.
- A disabled text input cannot be told from an enabled one. A journey that asserts a field is locked needs gpui-kit to expose the state.

The fallback, a debug-only control socket built on gpui-kit's test queries, is not needed for these reads and actions. It stays the answer if the select value or text entry gaps block a journey that matters.
