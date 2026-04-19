from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """
    Represents a single task along with its metadata.

    Attributes
    ----------
    file_path : str

    """

    file_path: str        # relative to CWD
    line_number: int      # 1-based, first line of the task
    status: str           # ' ', 'x', '.', 'c', '/'
    text: str             # task text (first line, cleaned of @tags)
    due_date: date | None = None
    due_date_raw: str | None = None  # raw string from @due(...), even if unparseable

    @property
    def status_display(self) -> str:
        return f'[{self.status}]'

    @property
    def has_due_tag(self) -> bool:
        return self.due_date_raw is not None

    @property
    def is_overdue(self) -> bool:
        return self.due_date is not None and self.due_date < date.today()

    @property
    def is_today(self) -> bool:
        return self.due_date is not None and self.due_date == date.today()

    @property
    def is_future(self) -> bool:
        return self.due_date is not None and self.due_date > date.today()

    @property
    def due_date_str(self) -> str:
        if self.due_date is not None:
            return self.due_date.strftime('%Y-%m-%d')
        if self.due_date_raw is not None:
            return f'?{self.due_date_raw}'  # '?' signals unparseable date
        return '-'


@dataclass
class Config:
    editor: str = 'nvim'
