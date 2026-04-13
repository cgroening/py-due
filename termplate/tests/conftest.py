import pytest
from termplate.domain.models import Task
from termplate.services.task import TaskService
from termplate.storage.task.base import BaseTaskRepository


class FakeTaskRepository(BaseTaskRepository):
    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def find_all(self) -> list[Task]:
        return list(self._tasks)

    def save(self, task: Task) -> None:
        self._tasks.append(task)

    def update(self, task: Task) -> None:
        self._tasks = [task if t.id == task.id else t for t in self._tasks]


@pytest.fixture
def repo() -> FakeTaskRepository:
    return FakeTaskRepository()


@pytest.fixture
def service(repo: FakeTaskRepository) -> TaskService:
    return TaskService(repo=repo)
