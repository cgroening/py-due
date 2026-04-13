from pathlib import Path
from termplate.domain.errors import (
    ConfigNotFoundError,
    ConfigParseError,
    TaskNotFoundError,
)


class TestConfigNotFoundError:
    def test_message_contains_path(self) -> None:
        error = ConfigNotFoundError(Path('/some/config.yaml'))
        assert '/some/config.yaml' in str(error)

    def test_is_exception(self) -> None:
        assert isinstance(ConfigNotFoundError(Path('/cfg.yaml')), Exception)

    def test_init_sets_message_via_super(self) -> None:
        error = ConfigNotFoundError(Path('/cfg.yaml'))
        assert str(error) == error.args[0]


class TestConfigParseError:
    def test_message_contains_path_and_detail(self) -> None:
        error = ConfigParseError(Path('/some/config.yaml'), 'bad field')
        assert '/some/config.yaml' in str(error)
        assert 'bad field' in str(error)

    def test_is_exception(self) -> None:
        assert isinstance(ConfigParseError(Path('/cfg.yaml'), 'oops'), Exception)

    def test_init_sets_message_via_super(self) -> None:
        error = ConfigParseError(Path('/cfg.yaml'), 'detail')
        assert str(error) == error.args[0]


class TestTaskNotFoundError:
    def test_message_contains_task_id(self) -> None:
        assert 'abc123' in str(TaskNotFoundError('abc123'))

    def test_is_exception(self) -> None:
        assert isinstance(TaskNotFoundError('x'), Exception)
