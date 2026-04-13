from abc import ABC, abstractmethod
from termplate.domain.models import Task


class BaseTaskRepository(ABC):
    """
    Abstract base class defining the storage interface.
    Allows swapping implementations without touching business logic.
    """

    @abstractmethod
    def find_all(self) -> list[Task]:
        ...

    @abstractmethod
    def save(self, task: Task) -> None:
        ...

    @abstractmethod
    def update(self, task: Task) -> None:
        ...
