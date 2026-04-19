from abc import ABC, abstractmethod
from due.domain.models import Task


class BaseMarkdownStorage(ABC):
    @abstractmethod
    def get_all_tasks(self, root_dir: str) -> list[Task]:
        """Returns all tasks found in `.md` files under `root_dir`."""
        ...
