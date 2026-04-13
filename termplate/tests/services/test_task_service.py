import pytest
from termplate.domain.errors import TaskNotFoundError
from termplate.domain.models import Task
from termplate.services.task import TaskService
from termplate.storage.task.base import BaseTaskRepository


class TestAddTask:
    def test_creates_task_with_given_title(self, service: TaskService) -> None:
        task = service.add_task('My task')
        assert task.title == 'My task'

    def test_saves_task_to_repo(
        self, service: TaskService, repo: BaseTaskRepository
    ) -> None:
        task = service.add_task('My task')
        assert repo.find_all() == [task]

    def test_returns_task_instance(self, service: TaskService) -> None:
        assert isinstance(service.add_task('Test'), Task)


class TestGetAllTasks:
    def test_returns_all_tasks(self, service: TaskService) -> None:
        service.add_task('A')
        service.add_task('B')
        assert len(service.get_all_tasks()) == 2

    def test_returns_empty_list(self, service: TaskService) -> None:
        assert service.get_all_tasks() == []


class TestMarkDone:
    def test_marks_correct_task_done(self, service: TaskService) -> None:
        task = service.add_task('Finish me')
        result = service.mark_done(task.id)
        assert result.done is True

    def test_persists_done_status(self, service: TaskService) -> None:
        task = service.add_task('Update me')
        service.mark_done(task.id)
        assert service.get_all_tasks()[0].done is True

    def test_raises_task_not_found_for_unknown_id(
        self, service: TaskService
    ) -> None:
        with pytest.raises(TaskNotFoundError):
            service.mark_done('nonexistent')

    def test_does_not_modify_other_tasks(self, service: TaskService) -> None:
        t1 = service.add_task('Target')
        t2 = service.add_task('Other')
        service.mark_done(t1.id)
        tasks = {t.id: t for t in service.get_all_tasks()}
        assert tasks[t2.id].done is False
