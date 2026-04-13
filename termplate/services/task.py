from termplate.domain.errors import TaskNotFoundError
from termplate.domain.models import Task
from termplate.storage.task.base import BaseTaskRepository


class TaskService:
    _repo: BaseTaskRepository


    def __init__(self, repo: BaseTaskRepository) -> None:
        self._repo = repo

    def add_task(self, title: str) -> Task:
        task = Task(title=title)
        self._repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self._repo.find_all()

    def mark_done(self, task_id: str) -> Task:
        tasks = self._repo.find_all()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self._repo.update(task)
                return task
        raise TaskNotFoundError(task_id)
