from typing import Optional
import typer
from termz.cli.output import print_error
from due.services.task_service import TaskService
from due.storage.config.yaml import YamlConfigStorage
from due.storage.markdown.filesystem import FilesystemMarkdownStorage


# Composition root
_storage        = FilesystemMarkdownStorage()
_service        = TaskService()
_config_storage = YamlConfigStorage()

app = typer.Typer(
    help=(
        'Show tasks with @due tags from Markdown files '
        'in the current directory.'
    ),
    invoke_without_command=True,
)

_SORT_HELP     = 'Sort by due date (oldest first) instead of grouping by file.'
_INCLUDE_UNDATED_HELP = (
    'Include tasks without a @due tag. '
    'By default only tasks with a @due tag are shown.'
)
_INCLUDE_CLOSED_HELP = (
    'Include checked [x] and cancelled [c] tasks. '
    'By default these statuses are hidden.'
)
_DUE_FILTER_HELP = (
    'Filter tasks by date relation. Valid values: '
    '-1 = overdue, 0 = today, 1 = future. '
    'Tasks with unparseable @due dates are excluded when this flag is set.'
)


def _validate_due_filter(due_filter: int | None) -> None:
    if due_filter is not None and due_filter not in (-1, 0, 1):
        print_error(
            f'Invalid value for --due-filter/-w: {due_filter}. '
            'Valid values are: -1 (overdue), 0 (today), 1 (future).'
        )
        raise typer.Exit(1)


def _run(
    sort_tasks_by_date: bool,
    include_undated_tasks: bool,
    include_checked_and_cancelled_tasks: bool,
    due_filter: int | None,
) -> None:
    _validate_due_filter(due_filter)
    from due.cli.commands.list_ import ListCommand
    ListCommand(_storage, _service, _config_storage).run(
        sort_tasks_by_date=sort_tasks_by_date,
        include_undated_tasks=include_undated_tasks,
        include_checked_and_cancelled_tasks=include_checked_and_cancelled_tasks,
        due_filter=due_filter,
    )


@app.callback()
def callback(
    ctx: typer.Context,
    sort_by_date: bool = typer.Option(
        False, '--sort-by-date', '-s', help=_SORT_HELP
    ),
    include_undated_tasks: bool = typer.Option(
        False, '--include-undated', '-u', help=_INCLUDE_UNDATED_HELP
    ),
    include_checked_and_cancelled_tasks: bool = typer.Option(
        False, '--include-closed', '-c', help=_INCLUDE_CLOSED_HELP
    ),
    due_filter: Optional[int] = typer.Option(
        None, '--when', '-w', help=_DUE_FILTER_HELP
    ),
) -> None:
    """due – Lists tasks with @due tags from Markdown files."""
    if ctx.invoked_subcommand is None:
        _run(
            sort_by_date,
            include_undated_tasks,
            include_checked_and_cancelled_tasks,
            due_filter
        )


@app.command(name='list')
def list_cmd(
    sort_by_date: bool = typer.Option(
        False, '--sort-by-date', '-s', help=_SORT_HELP
    ),
    include_undated_tasks: bool = typer.Option(
        False, '--include-undated', '-u', help=_INCLUDE_UNDATED_HELP
    ),
    include_checked_and_cancelled_tasks: bool = typer.Option(
        False, '--include-closed', '-c', help=_INCLUDE_CLOSED_HELP
    ),
    due_filter: Optional[int] = typer.Option(
        None, '--when', '-w', help=_DUE_FILTER_HELP
    )
) -> None:
    """Lists tasks with @due tags (default command)."""
    _run(
        sort_by_date,
        include_undated_tasks,
        include_checked_and_cancelled_tasks,
        due_filter
    )


def main() -> None:
    app()
