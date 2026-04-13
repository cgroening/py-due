import typer
from termplate.services.task import TaskService


class AddCommand:
    _service: TaskService


    def __init__(self, service: TaskService) -> None:
        self._service = service

    def run(self, title: str) -> None:
        task = self._service.add_task(title)
        typer.echo(f'[{task.id}] ✓ "{task.title}" added.')
