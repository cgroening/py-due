import logging as lg
from pathlib import Path
from importlib.resources import files
from textual.app import App
from termz.tui.theme_loader import ThemeLoader
from termplate import PACKAGE_NAME, APP_TITLE, APP_SUB_TITLE
from termplate.services.task import TaskService
from termplate.tui.screens.main_screen import MainScreen


state_dir = Path.home() / '.local' / 'state' / PACKAGE_NAME
state_dir.mkdir(parents=True, exist_ok=True)
THEME_CONFIG_FILE = state_dir / 'theme.json'
THEMES_DIR = str(files('termplate.tui.themes'))
DEFAULT_THEME = 'classic-black'
theme_loader = ThemeLoader(THEMES_DIR, include_standard_themes=True)


class TermplateApp(App[None]):
    """
    Main Textual application.

    Sets up the theme, header and pushes the MainScreen on mount. Also handles
    theme changes and updates the header to reflect the current theme.
    Contains logic for global key bindings that are not specific to a screen
    or tab.
    """
    TITLE = APP_TITLE
    SUB_TITLE = APP_SUB_TITLE
    CSS_PATH = 'global.tcss'

    _service: TaskService


    def __init__(self, service: TaskService) -> None:
        """Initializes the app and sets the previous theme."""
        super().__init__()
        self._service = service

    def on_mount(self) -> None:
        """
        Registers themes, sets the previous theme, updates the header
        and pushes the ListScreen.
        """
        theme_loader.register_themes_in_textual_app(self)
        theme_loader.set_previous_theme_in_textual_app(
            self, DEFAULT_THEME, THEME_CONFIG_FILE
        )
        self.update_header_theme_name()
        self.push_screen(MainScreen(self._service))
        lg.info('TermplateApp mounted and ListScreen pushed.')


    def watch_theme(self, theme_name: str) -> None:
        """
        Automatically called when `self.theme` changes.

        Writes the name of the theme to the config file and loads the CSS files.
        """
        self.update_header_theme_name()
        theme_loader.save_theme_to_config(theme_name, THEME_CONFIG_FILE)
        theme_loader.load_theme_css(theme_name, self)

    def update_header_theme_name(self) -> None:
        """Updates the header to reflect the current theme name."""
        self.title = f'{self.TITLE} - Theme: {self.theme}'

    def action_next_theme(self) -> None:
        """Changes to the next theme in the list."""
        theme_loader.change_to_next_or_previous_theme(1, self)

    def action_prev_theme(self) -> None:
        """Changes to the previous theme in the list."""
        theme_loader.change_to_next_or_previous_theme(-1, self)
