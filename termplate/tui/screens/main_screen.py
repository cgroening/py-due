from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, TabbedContent
from termz.tui.custom_widgets.multiline_footer import MultiLineFooter
from termplate import APP_ICON
from termplate.services.task import TaskService
from termplate.tui.bindings import CUSTOM_BINDINGS
from termplate.tui.screens.tabs import TasksTab, DoneTab


class MainScreen(Screen[None]):
    """Main screen: shows tasks split across tabs."""
    BINDINGS = CUSTOM_BINDINGS.get_bindings(for_screen=True)

    app: App[None]
    _service: TaskService
    _tasks_tab: TasksTab
    _done_tab: DoneTab

    def __init__(self, service: TaskService) -> None:
        super().__init__()
        self._service = service
        self._tasks_tab = TasksTab(service)
        self._done_tab = DoneTab(service)

    def compose(self) -> ComposeResult:
        yield Header(icon=APP_ICON)
        with TabbedContent(initial='tasks_tab'):
            yield self._tasks_tab
            yield self._done_tab
        yield MultiLineFooter(
            auto_wrap=False,
            row_map=CUSTOM_BINDINGS.get_row_map(for_screen=True)
        )

    def on_tabbed_content_tab_activated(
        self, _event: TabbedContent.TabActivated
    ) -> None:
        self.refresh_bindings()

    def check_action(
        self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:
        try:
            active_tab = self.query_one(TabbedContent).active
        except Exception:
            active_tab = 'tasks_tab'
        return CUSTOM_BINDINGS.handle_check_action(
            action.removeprefix('app.'), parameters, active_group=active_tab
        )

    def action_tasks_tab_add_task(self) -> None:
        self._tasks_tab.add_task()

    def action_tasks_tab_mark_done(self) -> None:
        self._tasks_tab.mark_done()

    def action_done_tab_xxx(self) -> None:
        self._done_tab.xxx()
