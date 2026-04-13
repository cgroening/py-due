import pytest
from termplate.cli.commands.list_ import ListCommand
from termplate.services.task import TaskService


@pytest.fixture
def command(service: TaskService) -> ListCommand:
    return ListCommand(service=service)


class TestListCommandRun:
    def test_prints_no_tasks_message_when_empty(
        self, command: ListCommand, capsys: pytest.CaptureFixture[str]
    ) -> None:
        command.run()
        assert 'No tasks' in capsys.readouterr().out

    def test_prints_each_task(
        self,
        command: ListCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        service.add_task('First')
        service.add_task('Second')
        command.run()
        output = capsys.readouterr().out
        assert 'First' in output
        assert 'Second' in output

    def test_output_contains_task_title(
        self,
        command: ListCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        service.add_task('Buy groceries')
        command.run()
        assert 'Buy groceries' in capsys.readouterr().out

    def test_output_contains_task_id(
        self,
        command: ListCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        task = service.add_task('Some task')
        command.run()
        assert task.id in capsys.readouterr().out

    def test_done_task_shows_checkmark(
        self,
        command: ListCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        task = service.add_task('Done task')
        service.mark_done(task.id)
        command.run()
        assert '✓' in capsys.readouterr().out

    def test_pending_task_shows_circle(
        self,
        command: ListCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        service.add_task('Pending task')
        command.run()
        assert '○' in capsys.readouterr().out
