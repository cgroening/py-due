# due – Tasks with @due tags from Markdown files

A terminal CLI that scans Markdown files for tasks carrying a `@due(...)` tag and
presents them in an interactive fuzzy finder. Select a task to open the file at
the exact line in your editor.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PyPI](https://img.shields.io/pypi/v/pydue)](https://pypi.org/project/pydue/)

<img src="https://raw.githubusercontent.com/cgroening/py-due/main/images/logo.png" width="200" alt="Termplate Logo">

![Screenshot](https://raw.githubusercontent.com/cgroening/py-due/main/images/screenshot.png)

## Table of Contents

- [Features](#features)
- [Motivation & Mission](#motivation--mission)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Fuzzy finder** – interactive search across all tasks powered by InquirerPy
- **Two views** – grouped by file (default) or flat list sorted by due date
- **Urgency indicators** – overdue tasks are prefixed with `!!! `, tasks due today with `!   `
- **Flexible filtering** – include undated tasks, closed tasks, or filter to overdue / today / future only
- **Jump to line** – opens the selected file at the exact task line in your editor
- **Path argument** – pass any directory to scan instead of the current working directory
- **Zero-config start** – works out of the box with `nvim`; one-line config to change the editor

### Planned features

- [ ] Support for additional tag formats
- [ ] Multiple path arguments
- [ ] Config option for custom date formats

## Motivation & Mission

Most task managers pull you away from the files where the work actually lives.
`due` stays out of the way: your tasks remain plain Markdown, your editor stays
your editor. `due` just surfaces what needs attention and gets you to the right
line in one keypress.

## Installation

### Requirements

See [pyproject.toml](./pyproject.toml).

### Installation via pip

```zsh
pip install pydue
```

[due on PyPI](https://pypi.org/project/pydue/)

### Installation from Source

1. Clone this repository:
   ```zsh
   git clone https://github.com/cgroening/due.git
   cd due
   ```

2. Install the package to make the `due` command available globally:
   ```zsh
   uv pip install .
   ```

Alternatively, `due` can be run without installation from the project root:

```zsh
python -m due
```

## Configuration

Create `~/.config/due/config.yaml`. The file is optional – without it `due`
falls back to `nvim` (or the `$EDITOR` environment variable).

```yaml
editor: nvim
```

### Configuration Options

| Option | Type | Required | Description | Default |
|--------|------|----------|-------------|---------|
| `editor` | string | No | Editor command used to open files | `nvim` |

## Usage

### Basic Usage

```zsh
due                   # grouped by file, @due tasks only, open tasks only
due ~/notes           # scan ~/notes instead of the current directory
```

### Task Format

`due` recognises standard Markdown checkboxes with a `@due(...)` tag:

```markdown
- [ ] Write release notes @due(2025-05-01)
- [ ] Review PR @due(2025-04-20)
- [x] Deploy to staging @due(2025-04-15)
```

Supported status characters: `[ ]` open, `[x]` done, `[c]` / `[/]` cancelled.

### Command Line Commands and Options

```zsh
due [PATH] [OPTIONS]
due list [PATH] [OPTIONS]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--sort-by-date` | `-s` | Flat list sorted by due date (oldest first) instead of grouped by file |
| `--include-undated` | `-u` | Include tasks that have no `@due` tag |
| `--include-closed` | `-c` | Include completed `[x]` and cancelled `[c]` tasks |
| `--due-filter INT` | `-d` | Show only: `-1` overdue, `0` today, `1` future |

**Examples:**

```zsh
due                            # grouped by file, @due tasks, open only
due --sort-by-date             # flat list sorted by date (oldest first)
due --include-undated          # also show tasks without @due
due --include-closed           # also show [x] and [c] tasks
due --due-filter -1            # only overdue tasks
due --due-filter 0             # only tasks due today
due --due-filter 1             # only future tasks
due list --sort-by-date -u     # explicit list subcommand with flags
due ~/notes --sort-by-date     # scan a specific directory
```

### Without Installation

```zsh
python -m due
```

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) – Rich text and beautiful formatting in the terminal
- [InquirerPy](https://github.com/kazhala/InquirerPy) – Fuzzy finder and interactive prompts
- [Typer](https://github.com/fastapi/typer) – CLI framework based on Python type hints
