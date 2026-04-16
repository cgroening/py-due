from typing import Optional
import typer
from due.cli.output import print_error
from due.services.task_service import TaskService
from due.storage.config.yaml import YamlConfigStorage
from due.storage.markdown.filesystem import FilesystemMarkdownStorage


to = typer.Option


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
_ALL_TASKS_HELP = (
    'Show all tasks, including those without a @due tag. '
    'By default only tasks with a @due tag are shown.'
)
_ALL_STAT_HELP = (
    'Show all tasks, including checked [x] and cancelled [c]. '
    'By default these statuses are hidden.'
)
_WHEN_HELP = (
    'Filter tasks by date relation. Valid values: '
    '-1 = overdue, 0 = today, 1 = future. '
    'Tasks with unparseable @due dates are excluded when this flag is set.'
)


def _validate_when(when: int | None) -> None:
    if when is not None and when not in (-1, 0, 1):
        print_error(
            f'Invalid value for --when/-w: {when}. '
            'Valid values are: -1 (overdue), 0 (today), 1 (future).'
        )
        raise typer.Exit(1)


def _run(
    sort_by_date: bool,
    all_tasks: bool,
    all_statuses: bool,
    when: int | None,
) -> None:
    _validate_when(when)
    from due.cli.commands.list_ import ListCommand
    ListCommand(_storage, _service, _config_storage).run(
        sort_by_date=sort_by_date,
        all_tasks=all_tasks,
        all_statuses=all_statuses,
        when=when,
    )


@app.callback()
def callback(
    ctx: typer.Context,
    sort_by_date: bool  = to(False, '--sort', '-s', help=_SORT_HELP),
    all_tasks: bool     = to(False, '--all-tasks', '-a', help=_ALL_TASKS_HELP),
    all_statuses: bool  = to(False, '--all-statuses', '-A', help=_ALL_STAT_HELP),
    when: Optional[int] = to(None, '--when', '-w', help=_WHEN_HELP),
) -> None:
    """due – Lists tasks with @due tags from Markdown files."""
    if ctx.invoked_subcommand is None:
        _run(sort_by_date, all_tasks, all_statuses, when)


@app.command(name='list')
def list_cmd(
    sort_by_date: bool  = to(False, '--sort', '-s', help=_SORT_HELP),
    all_tasks: bool     = to(False, '--all-tasks', '-a', help=_ALL_TASKS_HELP),
    all_statuses: bool  = to(False, '--all-statuses', '-A', help=_ALL_STAT_HELP),
    when: Optional[int] = to(None, '--when', '-w', help=_WHEN_HELP),
) -> None:
    """Lists tasks with @due tags (default command)."""
    _run(sort_by_date, all_tasks, all_statuses, when)


def main() -> None:
    app()
