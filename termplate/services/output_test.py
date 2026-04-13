from termplate.domain.models import Config
from termplate.storage.config.base import BaseConfigStorage


class OutputTestService:
    _config_storage: BaseConfigStorage
    _config: Config | None = None

    def __init__(self, config_storage: BaseConfigStorage) -> None:
        self._config_storage = config_storage

    def get_config(self) -> Config:
        """
        Returns the configuration object, loading it from storage if not already
        cached.
        """
        if self._config:
            return self._config

        self._config = self._config_storage.load_config()
        return self._config
