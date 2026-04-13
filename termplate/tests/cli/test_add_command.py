import pytest
from termplate.cli.commands.add import AddCommand
from termplate.services.task import TaskService


@pytest.fixture
def command(service: TaskService) -> AddCommand:
    return AddCommand(service=service)


class TestAddCommandRun:
    def test_calls_service_add_task(
        self, command: AddCommand, service: TaskService
    ) -> None:
        command.run('Buy milk')
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == 'Buy milk'

    def test_outputs_task_id_and_title(
        self,
        command: AddCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        command.run('Buy milk')
        captured = capsys.readouterr()
        task = service.get_all_tasks()[0]
        assert task.id in captured.out
        assert 'Buy milk' in captured.out

    def test_output_contains_checkmark(
        self, command: AddCommand, capsys: pytest.CaptureFixture[str]
    ) -> None:
        command.run('Test')
        assert '✓' in capsys.readouterr().out
