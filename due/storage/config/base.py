from abc import ABC, abstractmethod
from due.domain.models import Config


class BaseConfigStorage(ABC):
    @abstractmethod
    def load(self) -> Config:
        """Loads and returns the application configuration."""
        ...
