from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from termz.tui.custom_widgets.multiline_footer import MultiLineFooter
from termplate.tui.bindings import CUSTOM_BINDINGS


class AddScreen(ModalScreen[str | None]):
    """Modal screen for adding a new task."""

    CSS_PATH = 'add.tcss'
    BINDINGS = CUSTOM_BINDINGS.get_bindings(screen_name='add', for_screen=True)

    def compose(self) -> ComposeResult:
        yield MultiLineFooter(
            auto_wrap=False,
            row_map=CUSTOM_BINDINGS.get_row_map(
                screen_name='add', for_screen=True
            )
        )
        with Vertical(id='dialog'):
            yield Label('New Task', id='dialog-title')
            yield Input(placeholder='Task title ...', id='task-input')
            with Horizontal(id='buttons'):
                yield Button('Add', variant='primary', id='btn-add')
                yield Button('Cancel', variant='default', id='btn-cancel')

    def on_mount(self) -> None:
        self.query_one('#task-input', Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'btn-add':
            self._submit()
        else:
            self.dismiss(None)

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self._submit()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _submit(self) -> None:
        title = self.query_one('#task-input', Input).value.strip()
        if title:
            self.dismiss(title)
