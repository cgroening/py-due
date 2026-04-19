import pytest
from due.services.task_service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService()
