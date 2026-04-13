import typer
from termplate.domain.errors import TaskNotFoundError
from termplate.services.task import TaskService


class DoneCommand:
    _service: TaskService


    def __init__(self, service: TaskService) -> None:
        self._service = service

    def run(self, task_id: str) -> None:
        try:
            task = self._service.mark_done(task_id)
            typer.echo(f'[{task.id}] ✓ "{task.title}" marked as done.')
        except TaskNotFoundError as e:
            typer.echo(f'Error: {e}', err=True)
            raise typer.Exit(1)
