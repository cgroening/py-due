from textual.app import ComposeResult
from textual.widgets import DataTable, TabPane
from termplate.services.task import TaskService


class DoneTab(TabPane):
    """Tab showing completed tasks."""

    def __init__(self, service: TaskService) -> None:
        super().__init__('Done', id='done_tab')
        self.service = service

    def compose(self) -> ComposeResult:
        yield DataTable[str](id='done_table')

    def on_mount(self) -> None:
        table = self.query_one(DataTable[str])
        table.cursor_type = 'row'
        table.add_columns('ID', 'Title', 'Created')
        self.load_tasks()

    def load_tasks(self) -> None:
        table = self.query_one(DataTable[str])
        table.clear()
        for task in self.service.get_all_tasks():
            if task.done:
                table.add_row(
                    task.id, task.title,
                    task.created_at.strftime('%Y-%m-%d %H:%M')
                )

    def xxx(self) -> None:
        self.notify('XXX placeholder')
