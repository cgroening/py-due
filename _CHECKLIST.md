# Checklist: New Project from Termplate

Work through this list top to bottom when creating a new project based on this
template. Each section tells you what to change and where.

---

## 1. Project Setup

- [ ] Rename the root directory: `termplate/` → `<your-project>/`
- [ ] Rename the Python package directory: `termplate/termplate/` → `termplate/<your-package>/`
- [ ] Search and replace all occurrences of `termplate` with your package name
      (case-sensitive; cover file contents and file names)
- [ ] Rename `tp` (the CLI entry point) in `pyproject.toml` → scripts to your
      desired command name

---

## 2. `pyproject.toml`

- [ ] `name` – set your project name
- [ ] `version` – set initial version (e.g. `0.1.0`)
- [ ] `description` – write your project description
- [ ] `keywords` – update or remove
- [ ] `authors` – set your name/email
- [ ] `classifiers` – replace with classifiers that match your project
- [ ] `[project.urls]` – set your actual repository URL
- [ ] `[project.scripts]` – rename the entry point key and update the module
      path (e.g. `myapp = "mypackage.main:main"`)
- [ ] `[tool.setuptools.packages.find]` – replace the current
      `packages = ["termplate"]` with package auto-discovery:
      ```toml
      [tool.setuptools.packages.find]
      where = ["."]
      ```
- [ ] Add `[tool.ruff]` configuration if you use Ruff

---

## 3. Package Constants (`__init__.py`)

- [ ] `PACKAGE_NAME` – your package name (used for config/data paths)
- [ ] `APP_TITLE` – display title shown in header and CLI help
- [ ] `APP_SUB_TITLE` – subtitle shown in header and CLI help
- [ ] `APP_ICON` – emoji shown in the TUI header

---

## 4. Domain Layer (`domain/`)

### Models (`models.py`)
- [ ] Replace the `Task` dataclass with your own domain model(s)
- [ ] Replace the `Config` dataclass fields with your actual settings
- [ ] Remove models you do not need

### Errors (`errors.py`)
- [ ] Keep `ConfigNotFoundError` and `ConfigParseError` if you use YAML config
- [ ] Replace `TaskNotFoundError` with domain-specific errors for your models
- [ ] Remove errors that no longer apply

---

## 5. Storage Layer (`storage/`)

### Task/data repository (`storage/task/`)
- [ ] Rename `task/` to match your domain entity (e.g. `storage/entry/`)
- [ ] Update `base.py`: rename `BaseTaskRepository` and adjust the abstract
      methods (`find_all`, `save`, `update`) to match your model
- [ ] Update `json.py`: rename `JsonTaskRepository`, update the default file
      path (currently `~/.termplate/tasks.json`), and update the
      serialization/deserialization logic in `find_all`, `save`, `update`,
      and `_write` to match your model's fields

### Config storage (`storage/config/`)
- [ ] `yaml.py`: update `DEFAULT_CONFIG_PATH` (currently
      `~/.config/termplate/config.yaml`)
- [ ] `yaml.py`: update `_parse_config_data`, `_parse_example_setting`, and
      `_parse_another_setting` to match your `Config` model fields
- [ ] `yaml.py`: update the docstring YAML example to reflect your config
      structure
- [ ] `base.py`: remove or keep `set_config_path` depending on whether you
      need runtime path overriding (currently unused)
- [ ] If you do not need file-based config at all: delete `storage/config/`
      and remove all references to it

---

## 6. Services Layer (`services/`)

### Task service (`task.py`)
- [ ] Rename `TaskService` to match your domain
- [ ] Update or replace `add_task`, `get_all_tasks`, `mark_done` with the
      operations your application needs
- [ ] Update the injected repository type to your new base class

### Output-test service (`output_test.py`)
- [ ] Keep if you want a built-in `output-test` command (useful for verifying
      config and output formatting during development)
- [ ] Delete if not needed and remove all references in `main.py` and
      `cli/commands/`

---

## 7. Entry Point (`main.py`)

- [ ] Move all module-level setup code (logging, AppStateStorage, service
      wiring) inside `main()` so it does not run on import
- [ ] Update service and repository instantiation to match your renamed classes
- [ ] Remove the `output-test` command if you deleted that service
- [ ] Remove the `tui` command if you are building a CLI-only application
- [ ] Change or remove `logger.info("App gestartet")` (currently German)
- [ ] Update or remove `AppStateStorage(package_name=PACKAGE_NAME)` if you do
      not use app state persistence

---

## 8. CLI Commands (`cli/commands/`)

- [ ] Add `__init__.py` to `cli/` if missing
- [ ] Rename/replace `add.py`, `done.py`, `list_.py` with commands that match
      your application's actions
- [ ] Update the output strings in each command (currently task-specific)
- [ ] Delete `output_test.py` if you removed the output-test service
- [ ] `commands/__init__.py` – export your command classes if needed

---

## 9. TUI (`tui/`)

### App (`app.py`)
- [ ] `THEME_CONFIG_FILE`: move to `~/<your-package>/theme.json` to be
      consistent with other data paths (currently `~/.termplate_config.json`)
- [ ] `DEFAULT_THEME`: set the theme that loads on first run
- [ ] Remove the duplicate `set_previous_theme_in_textual_app` call in
      `__init__` (it is already called in `on_mount`)
- [ ] Rename `TermplateApp` to `<YourApp>App`

### Key bindings (`bindings.yaml`)
- [ ] Replace `tasks_tab` group with bindings for your actual tab(s)
- [ ] Replace `done_tab` group or remove it
- [ ] Keep/update `add_screen` group if you have a modal add-screen, otherwise
      rename or remove
- [ ] Keep `_global` bindings; add or remove entries as needed
- [ ] For each binding: update `key`, `action`, `description`, and `tooltip`

### Main screen (`screens/main_screen.py`)
- [ ] Rename action delegation methods to match your new binding action names
      (e.g. `action_tasks_tab_add_task` → `action_<tab>_<action>`)
- [ ] Replace `action_done_tab_xxx` with a real action or remove it
- [ ] Add/remove `TabPane` instances in `compose` and `__init__` to match your
      tabs

### Tabs (`screens/tabs/`)
- [ ] Rename `tasks_tab.py` and `TasksTab` to match your domain
- [ ] Update `TasksTab.__init__`: the `id` passed to `super().__init__` must
      match the group name in `bindings.yaml`
- [ ] Replace the `DataTable` columns and row data to match your model
- [ ] Replace `add_task` and `mark_done` with your tab's actions
- [ ] Replace `done_tab.py` / `DoneTab` entirely or remove it
- [ ] Replace `DoneTab.xxx()` with a real method or delete it

### Modal screens (`screens/`)
- [ ] Keep `add_screen.py` as a reference for modal screens; rename or replace
      for your actual use case
- [ ] Fix `on_button_pressed` in `add_screen.py`: when btn-add is pressed,
      `self.dismiss(None)` must not be called unconditionally after `_submit()`
      — use `else: self.dismiss(None)` instead

### Themes (`tui/themes/`)
- [ ] Rename `custom-classic-black/` to your theme name
- [ ] In `theme.py`: update `name` (currently `'termplate-test-theme'`) to
      your theme's name; adjust colors
- [ ] In `style.css`: adjust widget styles to match your design
- [ ] `DEFAULT_THEME` in `app.py` must match the theme name exactly
- [ ] Add additional theme directories following the same structure if needed

### CSS
- [ ] `global.tcss` is currently empty – add global TUI styles as needed
- [ ] `screens/add.tcss` – update for your modal screen layout

---

## 10. Tests (`tests/`)

- [ ] Move `FakeTaskRepository` from `tests/services/test_task_service.py` and
      `tests/cli/conftest.py` into a shared `tests/conftest.py` to avoid
      duplication; update all imports
- [ ] Rename and update `tests/services/test_task_service.py` to test your
      service
- [ ] Rename and update `tests/storage/task/test_json_task_repository.py` to
      test your repository
- [ ] Rename and update `tests/cli/` test files to cover your commands
- [ ] Update `tests/domain/test_errors.py` if you changed the error classes
- [ ] Remove `tests/services/test_output_test_service.py` if you removed that
      service
- [ ] Remove `tests/cli/test_output_test_command.py` if you removed that
      command

---

## 11. Documentation & Metadata

- [ ] `README.md` – rewrite for your project
- [ ] `CHANGELOG.md` – reset to your initial version entry
- [ ] `LICENSE` – update the copyright holder name and year
- [ ] `images/logo.png` – replace with your project's logo
- [ ] `_TEMPLATE_GUIDE.md` – keep as developer reference or delete once the
      team is familiar with the patterns
- [ ] This file (`_CHECKLIST.md`) – delete once all items are checked off

---

## 12. Housekeeping

- [ ] Delete committed cache directories if present:
      `termplate/tui/themes/custom-classic-black/.mypy_cache/`
- [ ] Verify `.gitignore` covers all generated files for your toolchain
- [ ] Run the full test suite: `pytest`
- [ ] Run the linter: `ruff check .`
- [ ] Run the type checker: `mypy termplate/` or `pyright`
- [ ] Install the package in editable mode and smoke-test the CLI and TUI:
      `pip install -e .`
