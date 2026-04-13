# Termplate – Template Guide

This document describes the structure of this template and explains what to keep,
what to replace, and which naming rules must be followed.

---

## TUI

The TUI is built with [Textual](https://github.com/Textualize/textual) and the
`termz` library, which provides `CustomBindings` and `MultiLineFooter`.

### File structure

```
termplate/tui/
├── app.py                        # App entry point
├── bindings.py                   # Creates the shared CUSTOM_BINDINGS instance
├── bindings.yaml                 # All key binding definitions
├── global.tcss                   # Global CSS
├── themes/                       # Custom Textual themes
└── screens/
    ├── main_screen.py            # Main screen (holds TabbedContent + footer)
    ├── add_screen.py             # Example modal screen
    ├── add.tcss                  # CSS for AddScreen
    └── tabs/
        ├── __init__.py
        ├── tasks_tab.py          # Example tab: pending tasks
        └── done_tab.py           # Example tab: completed tasks
```

---

### App (`app.py`)

`TermplateApp` is the Textual `App` subclass. It has no `BINDINGS` – all bindings
are owned by the screens. Its responsibilities are:

- Registering themes and persisting the active theme
- Pushing the initial screen (`MainScreen`) on mount
- Providing action methods for **global** bindings (those defined under `_global`
  in `bindings.yaml`). These methods must be named `action_global_<action>`:

```python
def action_global_quit(self) -> None: ...
def action_global_next_theme(self) -> None: ...
def action_global_prev_theme(self) -> None: ...
```

Global bindings are always dispatched on the `App` because screens include them
with an `app.` prefix via `get_bindings(for_screen=True)`.

---

### Main screen (`main_screen.py`)

`MainScreen` is the central screen. It owns the `TabbedContent`, the
`MultiLineFooter`, and the `BINDINGS`.

**Key responsibilities:**

1. **`BINDINGS`** – loaded once at class definition time:
   ```python
   BINDINGS = CUSTOM_BINDINGS.get_bindings(for_screen=True)
   ```
   This includes all tab-specific bindings and global bindings (prefixed with
   `app.` so they dispatch on the `App`).

2. **`check_action`** – filters which bindings the footer shows based on the
   currently active tab:
   ```python
   def check_action(self, action, parameters):
       active_tab = self.query_one(TabbedContent).active
       return CUSTOM_BINDINGS.handle_check_action(
           action.removeprefix('app.'), parameters, active_group=active_tab
       )
   ```
   Textual calls this automatically whenever bindings are re-evaluated.
   Call `self.refresh_bindings()` to trigger a re-evaluation (e.g. on tab change).

3. **Action delegation** – `MainScreen` has thin `action_*` methods that delegate
   to the corresponding tab:
   ```python
   def action_tasks_tab_add_task(self) -> None:
       self.query_one(TasksTab).add_task()
   ```
   The method name must match the action name produced by `bindings.yaml`
   (see naming rules below).

4. **`MultiLineFooter`** – placed at the bottom, uses the row layout from the
   YAML:
   ```python
   yield MultiLineFooter(
       auto_wrap=False,
       row_map=CUSTOM_BINDINGS.get_row_map(for_screen=True)
   )
   ```

**When hiding the footer** (e.g. while a modal is open):
```python
self.query_one(MultiLineFooter).display = False  # before push_screen
self.query_one(MultiLineFooter).display = True   # in on_dismiss callback
```

---

### Modal screens (`add_screen.py`)

Modal screens are `ModalScreen` subclasses. They get their own `MultiLineFooter`
which overlays the main screen's footer.

**Key responsibilities:**

1. **`BINDINGS`**:
   ```python
   BINDINGS = CUSTOM_BINDINGS.get_bindings(screen_name='add', for_screen=True)
   ```
   Only the screen's own bindings + global bindings (with `app.` prefix) are
   included.

2. **`MultiLineFooter`**:
   ```python
   yield MultiLineFooter(
       auto_wrap=False,
       row_map=CUSTOM_BINDINGS.get_row_map(screen_name='add', for_screen=True)
   )
   ```

3. **Action methods** – named after the action as-is (no prefix), since
   `_screen` groups are not prefixed:
   ```python
   def action_cancel(self) -> None:
       self.dismiss(None)
   ```

---

### Tab classes (`tabs/`)

Each tab is a `TabPane` subclass. It receives the service via its constructor,
owns its own UI widgets and business logic, and exposes plain (non-`action_`)
methods that `MainScreen` delegates to.

```python
class TasksTab(TabPane):
    def __init__(self, service: TaskService) -> None:
        super().__init__('Tasks', id='tasks_tab')  # id must match YAML group name
        self.service = service

    def add_task(self) -> None: ...   # called by MainScreen.action_tasks_tab_add_task
    def mark_done(self) -> None: ...  # called by MainScreen.action_tasks_tab_mark_done
```

The `id` passed to `super().__init__` must exactly match the tab group name in
`bindings.yaml` (e.g. `tasks_tab`).

---

### Key bindings (`bindings.yaml`)

All bindings are defined in `bindings.yaml`. The file is a YAML mapping of
**group names** to lists of binding definitions.

#### Group naming rules

| Group name        | Convention          | Action name produced          |
|-------------------|---------------------|-------------------------------|
| `_global`         | starts with `_`     | `global_<action>`             |
| `<name>_tab`      | ends with `_tab`    | `<name>_tab_<action>`         |
| `<name>_screen`   | ends with `_screen` | `<action>` (no prefix)        |

#### Per-binding fields

| Field         | Required | Description                                              |
|---------------|----------|----------------------------------------------------------|
| `key`         | yes      | Key to bind, e.g. `q`, `escape`, `ctrl+s`               |
| `action`      | yes      | Action name (prefixed according to group, see above)     |
| `description` | yes      | Short label shown in the footer                          |
| `row`         | no       | Footer row index, 0-based (default: `0`)                 |
| `tooltip`     | no       | Longer description shown on hover                        |
| `key_display` | no       | Override how the key is rendered in the footer           |
| `priority`    | no       | `true` = shown even when a widget captures the key       |
| `show`        | no       | `false` = register the binding but hide it in the footer |

#### Example

```yaml
# Always shown – action dispatched on App as action_global_<action>
_global:
  - key: q
    action: quit
    description: Quit
    priority: true
    row: 1

# Shown only when "tasks_tab" is active – action: tasks_tab_add_task
tasks_tab:
  - key: a
    action: add_task
    description: Add
    tooltip: Add a new task
    row: 0

# Shown only on AddScreen – action: cancel (no prefix)
add_screen:
  - key: escape
    action: cancel
    description: Cancel
    priority: true
    row: 0
```

#### How the action name maps to a Python method

| YAML group   | YAML action | Produced action name  | Python method (where)            |
|--------------|-------------|-----------------------|----------------------------------|
| `_global`    | `quit`      | `global_quit`         | `App.action_global_quit`         |
| `tasks_tab`  | `add_task`  | `tasks_tab_add_task`  | `MainScreen.action_tasks_tab_add_task` |
| `add_screen` | `cancel`    | `cancel`              | `AddScreen.action_cancel`        |

#### Steps when adding a new binding

1. Add the entry to the correct group in `bindings.yaml`
2. Add the action method in the right class (see table above)
3. For tab bindings: add a delegation method in `MainScreen`
4. For a new tab: create a `TabPane` subclass with `id='<name>_tab'`
5. For a new screen: create a `ModalScreen` subclass with `check_action` and
   `MultiLineFooter`; hide the main footer before `push_screen` and restore it
   in the `on_dismiss` callback
