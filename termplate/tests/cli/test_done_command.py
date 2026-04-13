import pytest
import typer
from termplate.cli.commands.done import DoneCommand
from termplate.services.task import TaskService


@pytest.fixture
def command(service: TaskService) -> DoneCommand:
    return DoneCommand(service=service)


class TestDoneCommandRun:
    def test_marks_task_done(
        self, command: DoneCommand, service: TaskService
    ) -> None:
        task = service.add_task('Finish report')
        command.run(task.id)
        assert service.get_all_tasks()[0].done is True

    def test_outputs_task_id_and_title(
        self,
        command: DoneCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        task = service.add_task('Finish report')
        command.run(task.id)
        captured = capsys.readouterr()
        assert task.id in captured.out
        assert 'Finish report' in captured.out

    def test_output_contains_checkmark(
        self,
        command: DoneCommand,
        service: TaskService,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        task = service.add_task('Test')
        command.run(task.id)
        assert '✓' in capsys.readouterr().out

    def test_raises_exit_1_when_task_not_found(
        self, command: DoneCommand
    ) -> None:
        with pytest.raises(typer.Exit) as exc_info:
            command.run('missing-id')
        assert exc_info.value.exit_code == 1

    def test_prints_error_to_stderr_when_task_not_found(
        self, command: DoneCommand, capsys: pytest.CaptureFixture[str]
    ) -> None:
        with pytest.raises(typer.Exit):
            command.run('missing-id')
        assert 'missing-id' in capsys.readouterr().err
