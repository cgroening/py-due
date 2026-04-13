import yaml
from typing import cast
from pathlib import Path
from termplate import PACKAGE_NAME
from termplate.domain.errors import ConfigNotFoundError, ConfigParseError
from termplate.domain.models import Config
from termplate.storage.config.base import BaseConfigStorage


DEFAULT_CONFIG_PATH = Path.home() / '.config' / PACKAGE_NAME / 'config.yaml'


class YamlConfigStorage(BaseConfigStorage):
    """
    Storage class for loading config from a YAML file.
    Implements the ConfigStorage interface.

    The YAML file should have the following structure:

    ```yaml
    example_setting: 11
    another_setting:
      - 1
      - 2
      - 3
    ```
    """
    _config_path: Path = DEFAULT_CONFIG_PATH


    def __init__(self, config_path: Path | None = None):
        """Sets the config path to default value if not provided."""
        if config_path:
            self._config_path = config_path

    def load_config(self) -> Config:
        """Loads the config from the YAML file and returns a Config object."""
        raw_data = self._get_raw_data()
        return self._parse_config_data(raw_data)

    def _get_raw_data(self) -> dict[str, object]:
        """Reads the YAML file and returns the raw data as a dictionary."""
        try:
            with open(self._config_path, 'r') as f:
                return cast(dict[str, object], yaml.safe_load(f))
        except FileNotFoundError:
            raise ConfigNotFoundError(self._config_path)
        except yaml.YAMLError as e:
            raise ConfigParseError(self._config_path, str(e))

    def _parse_config_data(self, data: dict[str, object]) -> Config:
        """
        Parses the raw data from the YAML file and returns a Config object.
        """
        try:
            example_setting = YamlConfigStorage._parse_example_setting(
                data.get('example_setting', None)
            )
            another_setting = YamlConfigStorage._parse_another_setting(
                data.get('another_setting', None)
            )
        except KeyError as e:
            raise ConfigParseError(
                self._config_path, f'Missing required field: {str(e)}'
            )
        except ValueError as e:
            raise ConfigParseError(self._config_path, str(e))

        return Config(
            example_setting=example_setting,
            another_setting=another_setting
        )

    @staticmethod
    def _parse_example_setting(value: int | object | None) -> int:
        """Parses the example_setting value from the YAML file."""
        if not isinstance(value, int):
            raise ValueError('example_setting must be an integer')
        return value

    @staticmethod
    def _parse_another_setting(value: list[int] | object | None) \
    -> list[int] | None:
        """Parses the another_setting value from the YAML file."""
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError(
                'another_setting must be a list of integers or None'
            )
        if not all(isinstance(item, int) for item in cast(list[object], value)):
            raise ValueError(
                'another_setting must be a list of integers or None'
            )
        return cast(list[int], value)
