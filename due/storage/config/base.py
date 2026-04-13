from abc import ABC, abstractmethod
from due.domain.models import Config


class BaseConfigStorage(ABC):
    @abstractmethod
    def load(self) -> Config:
        """Load and return the application configuration."""
        ...
