from datetime import datetime
import termz.cli.output as out
from termz.io.app_state_storage import AppStateStorage
from termplate.domain.errors import ConfigNotFoundError, ConfigParseError
from termplate.domain.models import Config
from termplate.services.output_test import OutputTestService


class OutputTestCommand:
    _service: OutputTestService
    _config: Config | None = None


    def __init__(self, _service: OutputTestService) -> None:
        self._service = _service

    def run(self) -> None:
        self._read_config()
        self._print_config()
        if self._config:
            self._save_time_of_last_run()

    def _read_config(self) -> None:
        try:
            self._config = self._service.get_config()
        except (ConfigNotFoundError, ConfigParseError) as e:
            out.print_error(str(e))
            return
        except Exception as e:
            out.print_error(f'Unexpected error while reading config: {str(e)}')
            return

    def _print_config(self) -> None:
        out.print_info('I\'m a custom panel created with termz.')

        if not self._config:
            return
        out.print_success(
            'Settings from config file:\n'
            f'Example Setting: {self._config.example_setting}\n'
            f'Another Setting: {self._config.another_setting}\n'
        )

    @staticmethod
    def _save_time_of_last_run() -> None:
        AppStateStorage().set('output_test_last_run', str(datetime.now()))
