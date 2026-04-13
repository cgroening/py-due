import logging
import typer
from pathlib import Path
from termz.util.logger import setup_logging
from termz.util.version import get_version
from termz.io.app_state_storage import AppStateStorage
from termplate import PACKAGE_NAME, APP_TITLE, APP_SUB_TITLE
from termplate.storage.config.yaml import YamlConfigStorage
from termplate.services.task import TaskService
from termplate.services.output_test import OutputTestService
from termplate.storage.task.json import JsonTaskRepository


# Setup logging and application state storage
setup_logging('termplate')
logger = logging.getLogger(__name__)
logger.info('App is starting...')
_ = AppStateStorage(package_name=PACKAGE_NAME)

# Dependency composition: Wire all layers together
_task_repository     = JsonTaskRepository()
_config_storage      = YamlConfigStorage()
_output_test_service = OutputTestService(_config_storage)
_task_service        = TaskService(repo=_task_repository)

app = typer.Typer(help=f'{APP_TITLE} - {APP_SUB_TITLE}')


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(get_version(PACKAGE_NAME, Path(__file__).parent.parent))
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def default(
    ctx: typer.Context,
    _version: bool = typer.Option(
        False,
        '--version',
        callback=_version_callback,
        is_eager=True,
        help='Show version and exit.',
    ),
    config: Path | None = typer.Option(
        None,
        '-C', '--config',
        help='Path to the config file. If not provided, the default is used.',
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    if config:
        _config_storage.set_config_path(config)

    from termplate.cli.commands.list_ import ListCommand
    if ctx.invoked_subcommand is None:
        ListCommand(_task_service).run()


@app.command()
def add(title: str = typer.Argument(..., help='Title of the new task')):
    """Adds a new task with the given title."""
    from termplate.cli.commands.add import AddCommand
    AddCommand(_task_service).run(title)


@app.command(name='list')
def list_tasks():
    """Lists all tasks."""
    from termplate.cli.commands.list_ import ListCommand
    ListCommand(_task_service).run()


@app.command()
def done(task_id: str = typer.Argument(..., help='ID of the completed task')):
    """Marks a task as done."""
    from termplate.cli.commands.done import DoneCommand
    DoneCommand(_task_service).run(task_id)


@app.command(name='output-test')
def output_test():
    from termplate.cli.commands.output_test import OutputTestCommand
    OutputTestCommand(_output_test_service).run()


@app.command()
def tui():
    """Opens the interactive TUI."""
    from termplate.tui.app import TermplateApp
    TermplateApp(_task_service).run()


def main():
    app()
