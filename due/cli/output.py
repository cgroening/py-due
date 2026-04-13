from rich.console import Console
from rich.panel import Panel


console = Console()


def print_error(message: str) -> None:
    """Prints an error message in a red panel."""
    _print_panel(f'✗ {message}', 'red')


def print_warning(message: str) -> None:
    """Prints a warning message in a yellow panel."""
    _print_panel(f'⚠ {message}', 'yellow')


def print_success(message: str) -> None:
    """Prints a success message in a green panel."""
    _print_panel(f'✓ {message}', 'green')


def _print_panel(formatted_message: str, color: str) -> None:
    console.print(Panel(
        f'[{color} bold]{formatted_message}[/{color} bold]',
        border_style=color,
        padding=(1, 2),
    ))


def str_with_fixed_width(text: str, width: int, align: str = 'left') -> str:
    """Return a string truncated or padded to exactly `width` characters.

    If the text exceeds the width it is truncated with a trailing ellipsis (…).
    Supports alignment: 'left', 'right', 'center'.
    """
    if len(text) > width:
        if align == 'right':
            return '…' + text[-(width - 1):]
        return text[:width - 1] + '…'

    if align == 'left':
        return text.ljust(width)
    elif align == 'right':
        return text.rjust(width)
    elif align == 'center':
        return text.center(width)
    else:
        raise ValueError(f'Invalid alignment: {align}')
