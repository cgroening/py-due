from textual.app import App, ComposeResult
from textual.widgets import DataTable, TabPane
from termz.tui.custom_widgets.multiline_footer import MultiLineFooter
from termplate.domain.errors import TaskNotFoundError
from termplate.services.task import TaskService


class TasksTab(TabPane):
    """Tab showing pending tasks."""
    app: App[None]

    def __init__(self, service: TaskService) -> None:
        super().__init__('Tasks', id='tasks_tab')
        self.service = service

    def compose(self) -> ComposeResult:
        yield DataTable[str](id='tasks_table')

    def on_mount(self) -> None:
        table = self.query_one(DataTable[str])
        table.cursor_type = 'row'
        table.add_columns('ID', 'Title', 'Created')
        self._load_tasks()

    def _load_tasks(self) -> None:
        table = self.query_one(DataTable[str])
        table.clear()
        for task in self.service.get_all_tasks():
            if not task.done:
                table.add_row(
                    task.id, task.title,
                    task.created_at.strftime('%Y-%m-%d %H:%M')
                )

    def add_task(self) -> None:
        from termplate.tui.screens.add_screen import AddScreen

        self.screen.query_one(MultiLineFooter).display = False

        def on_dismiss(title: str | None) -> None:
            self.screen.query_one(MultiLineFooter).display = True
            if title:
                self.service.add_task(title)
                self._load_tasks()

        self.app.push_screen(AddScreen(), on_dismiss)

    def mark_done(self) -> None:
        from termplate.tui.screens.tabs.done_tab import DoneTab

        table = self.query_one(DataTable[str])
        if not table.row_count:
            return
        row_data = table.get_row_at(table.cursor_row)
        task_id = str(row_data[0])
        try:
            self.service.mark_done(task_id)
            self._load_tasks()
            self.screen.query_one(DoneTab).load_tasks()
        except TaskNotFoundError as e:
            self.notify(str(e), severity='error')
