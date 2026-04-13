import pytest
from termplate.domain.models import Config
from termplate.services.output_test import OutputTestService
from termplate.storage.config.base import BaseConfigStorage


class FakeConfigStorage(BaseConfigStorage):
    def __init__(self, config: Config) -> None:
        self._config = config
        self.call_count: int = 0

    def load_config(self) -> Config:
        self.call_count += 1
        return self._config


@pytest.fixture
def config() -> Config:
    return Config(example_setting=7)


@pytest.fixture
def storage(config: Config) -> FakeConfigStorage:
    return FakeConfigStorage(config)


@pytest.fixture
def service(storage: FakeConfigStorage) -> OutputTestService:
    return OutputTestService(config_storage=storage)


class TestGetConfig:
    def test_loads_config_from_storage(
        self,
        service: OutputTestService,
        storage: FakeConfigStorage,
        config: Config,
    ) -> None:
        result = service.get_config()
        assert result == config
        assert storage.call_count == 1

    def test_caches_config_on_second_call(
        self, service: OutputTestService, storage: FakeConfigStorage
    ) -> None:
        service.get_config()
        service.get_config()
        assert storage.call_count == 1

    def test_returns_same_instance_on_repeat_calls(
        self, service: OutputTestService
    ) -> None:
        assert service.get_config() is service.get_config()
