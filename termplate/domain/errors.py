from pathlib import Path


# TODO: Consider moving this exception to termz
class ConfigNotFoundError(Exception):
    """Raised when the configuration file is not found."""
    _config_path: Path


    def __init__(self, config_path: Path):
        self._config_path = config_path
        super().__init__(str(self))

    def __str__(self) -> str:
        return f'Configuration file not found:\n{str(self._config_path)}'


# TODO: Consider moving this exception to termz
class ConfigParseError(Exception):
    """Raised when there is an error parsing the configuration file."""
    _config_path: Path
    _error_message: str


    def __init__(self, config_path: Path, error_message: str):
        self._config_path = config_path
        self._error_message = error_message
        super().__init__(str(self))

    def __str__(self) -> str:
        return f'Error parsing YAML file:\n{str(self._config_path)}\n\n' \
               + f'{self._error_message}'


class TaskNotFoundError(Exception):
    def __init__(self, task_id: str) -> None:
        super().__init__(f'Task "{task_id}" not found.')
