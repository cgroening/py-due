# 💻 Termplate – A template for terminal applications

A beautiful terminal application template built with Python, Typer, Rich and Textual. Provides a clean structure and reusable components for building interactive CLI tools with a rich user interface. The template uses Layered Architecture to separate concerns and make it easy to maintain and extend. Furthermore, the Command Pattern is used to implement the CLI commands in a modular way.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PyPI](https://img.shields.io/pypi/v/termplate)](https://pypi.org/project/termplate/)

<img src="https://raw.githubusercontent.com/cgroening/py-termplate/main/images/logo.png" width="200" alt="Termplate Logo">

## Table of Contents

- [Features](#features)
- [Motivation & Mission](#motivation-mission)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Feature 1** – ...
- **Feature 2** – ...
- 🎨 **Beautiful UI** – Rich-styled panels and headers with color-coded information
- ...

### Planned features

- [ ] Feature X
- [ ] Feature Y
- [ ] ...

## Motivation & Mission



## Installation

### Requirements

See [pyproject.toml](./pyproject.toml).

### Installation via pip

```zsh
pip install termplate
```

[termplate on PyPI](https://pypi.org/project/termplate/)

### Installation from Source

1. Clone this repository:
   ```zsh
   git clone https://github.com/cgroening/py-termplate.git
   cd py-termplate
   ```

2. Install the package if you want the `tp` command available globally:

```zsh
uv pip install .
```

Alternatively, Termplate can be run without installation, see Section [Without Installation](#without-installation).

## Configuration

Create a `config.yaml` file in `~/.config/termplate/`. Alternatively, you can place the configuration file at a location of a choice and pass the path with the `--config` option.

```yaml
# ...
```

### Configuration Options

| Option | Type | Required | Description | Default |
|--------|------|----------|-------------|---------|
| `setting1` | string | No | Description for setting1 | – |

## Usage

### Basic Usage

```zsh
# Run directly
termplate         # defaults to XXX
termplate XXX
```

### Without Installation

The package can also be run without installation from the project root:

```zsh
python -m termplate
```

### Command Line Commands and Options

```zsh
# ...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) – Rich text and beautiful formatting in the terminal
- [Textual](https://github.com/Textualize/textual) – TUI framework for building terminal applications
- [Typer](https://github.com/fastapi/typer) – CLI framework based on Python type hints
