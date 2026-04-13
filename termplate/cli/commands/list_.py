import typer
from termplate.services.task import TaskService


class ListCommand:
    _service: TaskService


    def __init__(self, service: TaskService) -> None:
        self._service = service

    def run(self) -> None:
        tasks = self._service.get_all_tasks()
        if not tasks:
            typer.echo('No tasks found.')
            return
        for task in tasks:
            status = '✓' if task.done else '○'
            typer.echo(f'  {status} [{task.id}] {task.title}')
