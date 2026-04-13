from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch
from termplate.cli.commands.output_test import OutputTestCommand
from termplate.domain.errors import ConfigNotFoundError, ConfigParseError
from termplate.domain.models import Config
from termplate.services.output_test import OutputTestService
from termplate.storage.config.base import BaseConfigStorage


@dataclass
class FakeOut:
    errors: list[str] = field(default_factory=list)
    successes: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)

    def print_error(self, msg: str) -> None:
        self.errors.append(msg)

    def print_success(self, msg: str) -> None:
        self.successes.append(msg)

    def print_info(self, msg: str) -> None:
        self.infos.append(msg)


class FixedConfigStorage(BaseConfigStorage):
    def __init__(self, config: Config) -> None:
        self._config = config

    def load_config(self) -> Config:
        return self._config


class FailingConfigStorage(BaseConfigStorage):
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def load_config(self) -> Config:
        raise self._exc


def _make_command(storage: BaseConfigStorage) -> tuple[OutputTestCommand, FakeOut]:
    fake_out = FakeOut()
    service = OutputTestService(storage)
    command = OutputTestCommand(_service=service)
    return command, fake_out


class TestOutputTestCommandRun:
    def test_calls_service_get_config(self) -> None:
        config = Config(example_setting=1)
        command, fake_out = _make_command(FixedConfigStorage(config))
        with patch('termplate.cli.commands.output_test.out', fake_out), \
             patch('termplate.cli.commands.output_test.AppStateStorage'):
            command.run()
        assert len(fake_out.successes) == 1

    def test_prints_success_with_config_values(self) -> None:
        config = Config(example_setting=42, another_setting=[1, 2])
        command, fake_out = _make_command(FixedConfigStorage(config))
        with patch('termplate.cli.commands.output_test.out', fake_out), \
             patch('termplate.cli.commands.output_test.AppStateStorage'):
            command.run()
        assert '42' in fake_out.successes[0]
        assert '[1, 2]' in fake_out.successes[0]

    def test_prints_error_on_config_not_found(self) -> None:
        exc = ConfigNotFoundError(Path('/cfg.yaml'))
        command, fake_out = _make_command(FailingConfigStorage(exc))
        with patch('termplate.cli.commands.output_test.out', fake_out):
            command.run()
        assert len(fake_out.errors) == 1
        assert len(fake_out.successes) == 0

    def test_prints_error_on_config_parse_error(self) -> None:
        exc = ConfigParseError(Path('/cfg.yaml'), 'bad field')
        command, fake_out = _make_command(FailingConfigStorage(exc))
        with patch('termplate.cli.commands.output_test.out', fake_out):
            command.run()
        assert len(fake_out.errors) == 1
        assert len(fake_out.successes) == 0

    def test_prints_error_on_unexpected_exception(self) -> None:
        exc = RuntimeError('unexpected')
        command, fake_out = _make_command(FailingConfigStorage(exc))
        with patch('termplate.cli.commands.output_test.out', fake_out):
            command.run()
        assert len(fake_out.errors) == 1
        assert 'unexpected' in fake_out.errors[0]
