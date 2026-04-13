from pathlib import Path
import pytest
from termplate.domain.errors import ConfigNotFoundError, ConfigParseError
from termplate.domain.models import Config
from termplate.storage.config.yaml import DEFAULT_CONFIG_PATH, YamlConfigStorage


VALID_YAML = "example_setting: 11\nanother_setting:\n  - 1\n  - 2\n"
VALID_YAML_NO_ANOTHER = "example_setting: 5\n"


class TestYamlConfigStorageInit:
    def test_uses_provided_path(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage(config_path=cfg)
        assert storage.load_config().example_setting == 11

    def test_raises_not_found_for_nonexistent_provided_path(
        self, tmp_path: Path
    ) -> None:
        storage = YamlConfigStorage(config_path=tmp_path / 'missing.yaml')
        with pytest.raises(ConfigNotFoundError):
            storage.load_config()

    @pytest.mark.skipif(
        DEFAULT_CONFIG_PATH.exists(),
        reason='Default config exists, cannot test missing-file behavior'
    )
    def test_uses_default_path_when_none(self) -> None:
        storage = YamlConfigStorage(config_path=None)
        with pytest.raises(ConfigNotFoundError) as exc_info:
            storage.load_config()
        assert str(DEFAULT_CONFIG_PATH) in str(exc_info.value)


class TestSetConfigPath:
    def test_sets_path_from_string(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage()
        storage.set_config_path(str(cfg))
        assert storage.load_config().example_setting == 11

    def test_sets_path_from_path_object(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage()
        storage.set_config_path(cfg)
        assert storage.load_config().example_setting == 11

    def test_does_nothing_when_none(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage(config_path=cfg)
        storage.set_config_path(None)
        assert storage.load_config().example_setting == 11

    def test_does_nothing_when_empty_string(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage(config_path=cfg)
        storage.set_config_path('')
        assert storage.load_config().example_setting == 11


class TestLoadConfig:
    def test_loads_valid_yaml(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage(config_path=cfg)
        result = storage.load_config()
        assert result.example_setting == 11
        assert result.another_setting == [1, 2]

    def test_loads_yaml_without_optional_field(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML_NO_ANOTHER)
        storage = YamlConfigStorage(config_path=cfg)
        result = storage.load_config()
        assert result.example_setting == 5
        assert result.another_setting is None

    def test_raises_config_not_found_error(self, tmp_path: Path) -> None:
        storage = YamlConfigStorage(config_path=tmp_path / 'missing.yaml')
        with pytest.raises(ConfigNotFoundError):
            storage.load_config()

    def test_raises_config_parse_error_on_invalid_yaml(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(': invalid: yaml: {')
        storage = YamlConfigStorage(config_path=cfg)
        with pytest.raises(ConfigParseError):
            storage.load_config()

    def test_raises_config_parse_error_when_example_setting_missing(
        self, tmp_path: Path
    ) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text("another_setting:\n  - 1\n")
        storage = YamlConfigStorage(config_path=cfg)
        with pytest.raises(ConfigParseError):
            storage.load_config()

    def test_raises_config_parse_error_when_example_setting_wrong_type(
        self, tmp_path: Path
    ) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text("example_setting: not_an_int\n")
        storage = YamlConfigStorage(config_path=cfg)
        with pytest.raises(ConfigParseError):
            storage.load_config()

    def test_raises_config_parse_error_when_another_setting_wrong_type(
        self, tmp_path: Path
    ) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text("example_setting: 1\nanother_setting: not_a_list\n")
        storage = YamlConfigStorage(config_path=cfg)
        with pytest.raises(ConfigParseError):
            storage.load_config()

    def test_raises_config_parse_error_when_another_setting_contains_non_int(
        self, tmp_path: Path
    ) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text("example_setting: 1\nanother_setting:\n  - 1\n  - foo\n")
        storage = YamlConfigStorage(config_path=cfg)
        with pytest.raises(ConfigParseError):
            storage.load_config()

    def test_returns_config_instance(self, tmp_path: Path) -> None:
        cfg = tmp_path / 'config.yaml'
        cfg.write_text(VALID_YAML)
        storage = YamlConfigStorage(config_path=cfg)
        assert isinstance(storage.load_config(), Config)
