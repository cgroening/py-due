import json
from datetime import datetime
from pathlib import Path
from typing import cast
from termplate.domain.models import Task
from termplate.storage.task.base import BaseTaskRepository


class JsonTaskRepository(BaseTaskRepository):
    def __init__(
        self, path: Path = Path.home() / '.termplate' / 'tasks.json'
    ) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text('[]')

    def find_all(self) -> list[Task]:
        raw = cast(list[dict[str, object]], json.loads(self._path.read_text()))
        tasks: list[Task] = []
        for item in raw:
            tasks.append(Task(
                id=str(item['id']),
                title=str(item['title']),
                done=bool(item['done']),
                created_at=datetime.fromisoformat(str(item['created_at']))
            ))
        return tasks

    def save(self, task: Task) -> None:
        tasks = self.find_all()
        tasks.append(task)
        self._write(tasks)

    def update(self, task: Task) -> None:
        tasks = self.find_all()
        self._write([t if t.id != task.id else task for t in tasks])

    def _write(self, tasks: list[Task]) -> None:
        data: list[dict[str, object]] = [
            {
                'id': t.id,
                'title': t.title,
                'done': t.done,
                'created_at': t.created_at.isoformat()
            }
            for t in tasks
        ]
        self._path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
