from datetime import datetime
from pathlib import Path
import pytest
from termplate.domain.models import Task
from termplate.storage.task.json import JsonTaskRepository


@pytest.fixture
def repo(tmp_path: Path) -> JsonTaskRepository:
    return JsonTaskRepository(path=tmp_path / 'tasks.json')


class TestJsonTaskRepositoryInit:
    def test_creates_file_if_missing(self, tmp_path: Path) -> None:
        path = tmp_path / 'tasks.json'
        assert not path.exists()
        JsonTaskRepository(path=path)
        assert path.exists()

    def test_initial_file_is_empty_list(self, tmp_path: Path) -> None:
        path = tmp_path / 'tasks.json'
        JsonTaskRepository(path=path)
        assert path.read_text() == '[]'

    def test_does_not_overwrite_existing_file(self, tmp_path: Path) -> None:
        path = tmp_path / 'tasks.json'
        repo = JsonTaskRepository(path=path)
        repo.save(Task(title='existing'))
        JsonTaskRepository(path=path)
        assert len(JsonTaskRepository(path=path).find_all()) == 1


class TestFindAll:
    def test_returns_empty_list_initially(self, repo: JsonTaskRepository) -> None:
        assert repo.find_all() == []

    def test_returns_saved_tasks(self, repo: JsonTaskRepository) -> None:
        repo.save(Task(title='Test task'))
        tasks = repo.find_all()
        assert len(tasks) == 1
        assert tasks[0].title == 'Test task'

    def test_deserializes_created_at(self, repo: JsonTaskRepository) -> None:
        repo.save(Task(title='Datetime test'))
        assert isinstance(repo.find_all()[0].created_at, datetime)


class TestSave:
    def test_saves_task(self, repo: JsonTaskRepository) -> None:
        repo.save(Task(title='New task'))
        assert len(repo.find_all()) == 1

    def test_saves_multiple_tasks(self, repo: JsonTaskRepository) -> None:
        repo.save(Task(title='First'))
        repo.save(Task(title='Second'))
        assert len(repo.find_all()) == 2

    def test_saved_task_has_correct_title(self, repo: JsonTaskRepository) -> None:
        repo.save(Task(title='Hello'))
        assert repo.find_all()[0].title == 'Hello'


class TestUpdate:
    def test_updates_task_done_status(self, repo: JsonTaskRepository) -> None:
        task = Task(title='Update me')
        repo.save(task)
        task.done = True
        repo.update(task)
        assert repo.find_all()[0].done is True

    def test_does_not_change_other_tasks(self, repo: JsonTaskRepository) -> None:
        t1 = Task(title='First')
        t2 = Task(title='Second')
        repo.save(t1)
        repo.save(t2)
        t1.done = True
        repo.update(t1)
        tasks = {t.id: t for t in repo.find_all()}
        assert tasks[t1.id].done is True
        assert tasks[t2.id].done is False

    def test_update_nonexistent_id_leaves_list_unchanged(
        self, repo: JsonTaskRepository
    ) -> None:
        repo.save(Task(title='Existing'))
        repo.update(Task(title='Ghost'))
        titles = [t.title for t in repo.find_all()]
        assert 'Existing' in titles
        assert 'Ghost' not in titles
