from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """
    Represents a single task along with its metadata.

    Attributes
    ----------
    file_path : str
        The absolute path to the file containing the task.
    line_number : int
        The 1-based line number where the task is located in the file.
    status : str
        The status of the task, represented by a single character:
        - ' ' (space): open task
        - 'x': completed task
        - '.': cancelled task
        - 'c': cancelled task (alternative)
        - '/': cancelled task (alternative)
    text : str
        The text of the task, cleaned of any `@tags` and only the first line if
        it's a multi-line task.
    due_date : date | None
        The parsed due date of the task, if available and parseable.
    due_date_raw : str | None
        The raw string from the `@due(...)` tag, even if it couldn't be parsed
        into a date.
    """
    file_path: str
    line_number: int
    status: str
    text: str
    due_date: date | None = None
    due_date_raw: str | None = None


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
