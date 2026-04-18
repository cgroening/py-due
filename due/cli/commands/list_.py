import os
import sys
import subprocess
from typing import Any
from dataclasses import dataclass
from rich.console import Console
from InquirerPy import inquirer
from InquirerPy.utils import get_style  # type: ignore
from InquirerPy.base.control import Choice
from termz.cli.output import print_error, print_warning
from termz.util.string import str_with_fixed_width
from due.domain.models import Config, Task
from due.services.task_service import TaskService
from due.storage.config.yaml import YamlConfigStorage
from due.storage.markdown.filesystem import FilesystemMarkdownStorage


console = Console()

# Visual separator used in rows and the column-header line
_SEP = ' │ '

# Fixed-width urgency prefixes (4 chars each, to keep columns aligned)
_PFX_OVERDUE = '!!! '
_PFX_TODAY   = '!   '
_PFX_NONE    = '    '


@dataclass
class ColumnWidths:
    due: int
    file: int
    status: int
    text: int


class ListCommand:
    """
    Renders due tasks in a fuzzy finder and opens the selected one in the
    configured editor.

    Two views are supported:

    - grouped by file (default) and
    - flat sorted by due date.

    Tasks are loaded from Markdown files in the current working directory via
    `FilesystemMarkdownStorage` and filtered/sorted by `TaskService`.
    Selecting a task row opens the file at the matching line; selecting a file
    header opens it at line 1.

    Attributes:
    -----------
    _FLAT_COLS : tuple[str, str, str, str]
        Column headers for the flat view (sorted by date).
    _GROUPED_COLS : tuple[str, str, str]
        Column headers for the grouped view (by file).
    _storage : FilesystemMarkdownStorage
        Storage instance for loading tasks from Markdown files.
    _service : TaskService
        Service instance for filtering, sorting, and grouping tasks.
    _config_storage : YamlConfigStorage
        Storage instance for loading configuration (e.g., editor settings).
    """
    _FLAT_COLS    = ('Due Date', 'File', 'St.', 'Task')
    _GROUPED_COLS = ('Due Date', 'St.', 'Task')

    _storage: FilesystemMarkdownStorage
    _service: TaskService
    _config_storage: YamlConfigStorage
    _config: Config


    def __init__(
        self,
        storage: FilesystemMarkdownStorage,
        service: TaskService,
        config_storage: YamlConfigStorage,
    ) -> None:
        """
        Initializes the `ListCommand` with the required storage and
        service instances.
        """
        self._storage = storage
        self._service = service
        self._config_storage = config_storage

    def run(
        self,
        sort_tasks_by_date: bool = False,
        include_undated_tasks: bool = False,
        include_closed_tasks: bool = False,
        due_filter: int | None = None,
    ) -> None:
        """
        Main entry point for the command. Loads tasks, applies filters/sorting,
        renders the fuzzy finder and opens the selected task in the editor.

        Parameters:
        -----------
        sort_tasks_by_date : bool
            If `True`, tasks are shown in a flat list sorted by due date.
            If `False` (default), tasks are grouped by file.
        include_undated_tasks : bool
            If `True`, tasks without a @due tag are included in the list.
            By default only tasks with a `@due` tag are shown.
        include_closed_tasks : bool
            If `True`, checked (`[x]`) and cancelled (`[c]`) tasks are included.
            By default these statuses are hidden.
        """
        self._config = self._config_storage.load()

        # Load all tasks from current directory
        tasks = self._load_tasks(
            include_undated_tasks=include_undated_tasks,
            include_checked_and_cancelled_tasks=include_closed_tasks,
            due_filter=due_filter,
        )
        if not tasks:
            print_warning('No tasks found.')
            return

        # Render the fuzzy finder and get the selected task
        chosen = self._show_tasks(tasks, sort_tasks_by_date)
        if chosen is None:
            print_warning('Selection cancelled.')
            return

        self._open_editor(chosen)

    def _load_tasks(
        self,
        include_undated_tasks: bool,
        include_checked_and_cancelled_tasks: bool,
        due_filter: int | None,
    ) -> list[Task]:
        """
        Returns a list of tasks loaded from Markdown files in the current
        directory, filtered according to the provided options.
        """
        cwd = os.getcwd()

        all_file_tasks = self._storage.get_all_tasks(cwd)
        return self._service.filter_tasks(
            all_file_tasks,
            include_undated_tasks=include_undated_tasks,
            include_closed_tasks=include_checked_and_cancelled_tasks,
            due_filter=due_filter,
        )

    def _show_tasks(
        self, tasks: list[Task], sort_tasks_by_date: bool
    ) -> Task | None:
        """
        Renders the list of tasks in a fuzzy finder and returns the
        selected task.
        """
        if sort_tasks_by_date:
            tasks  = self._service.sort_by_date(tasks)
            return self._show_tasks_sorted_by_date(tasks)
        else:
            groups = self._service.group_by_file(tasks)
            return self._show_tasks_grouped_by_file(groups)

    def _show_tasks_sorted_by_date(self, tasks: list[Task]) -> Task | None:
        """
        Renders tasks in a fuzzy finder as a flat list sorted by due date,
        with columns for due date, file path, status and task text.
        Returns the selected task.
        """
        column_widths = self._by_date_widths(tasks)
        header = self._by_date_header(column_widths)
        choices = self._fzf_choices_by_date(tasks, column_widths)

        print()
        try:
            result = self._run_fuzzy(choices, header)
        except KeyboardInterrupt:
            return None

        if not isinstance(result, int):
            return None

        return tasks[result]

    def _by_date_header(self, column_widths: ColumnWidths) -> str:
        """
        Returns the formatted header string for the flat view (sorted by date),
        with columns for due date, file path, status and task text.
        """
        str_fix = str_with_fixed_width
        return (
            f'   {_PFX_NONE}{str_fix(self._FLAT_COLS[0], column_widths.due)}{_SEP}'
            f'{str_fix(self._FLAT_COLS[1], column_widths.file)}{_SEP}'
            f'{str_fix(self._FLAT_COLS[2], column_widths.status)}{_SEP}'
            f'{self._FLAT_COLS[3]}'
        )

    def _fzf_choices_by_date(
        self, tasks: list[Task], column_widths: ColumnWidths
    ) -> list[Choice]:
        """
        Returns a list of `Choice` objects for the flat view (sorted by date),
        with formatted row strings for each task.
        """
        return [
            Choice(
                value=i,
                name=self._by_date_row(task, column_widths),
            )
            for i, task in enumerate(tasks)
        ]

    def _by_date_widths(self, tasks: list[Task]) -> ColumnWidths:
        """
        Calculates the optimal column widths for the flat view (sorted by date)
        based on the content of the tasks and the console width.
        Returns a `ColumnWidths` dataclass instance with the calculated widths.
        """
        col_due    = max(
            10, min(max((len(t.due_date_str) for t in tasks), default=10), 15)
        )
        col_status = max(len(self._FLAT_COLS[2]), 3)  # 'Status' = 6
        max_file   = max((len(t.file_path) for t in tasks), default=5)
        col_file   = min(max(len(self._FLAT_COLS[1]), max_file), 40)

        # 4-char urgency prefix + 3 separators + fuzzy-prompt left padding
        overhead   = 4 + len(_SEP) * 3 + 5
        col_text   = max(
            10, console.width - overhead - col_due - col_file - col_status
        )

        return ColumnWidths(
            due=col_due, file=col_file, status=col_status, text=col_text
        )

    def _by_date_row(self, task: Task, column_widths: ColumnWidths) -> str:
        """
        Returns the formatted row string for a task in the flat view (sorted
        by date), with columns for due date, file path, status and task text.
        """
        prefix = self._urgency_prefix(task)
        due    = str_with_fixed_width(task.due_date_str, column_widths.due)
        file_  = str_with_fixed_width(task.file_path, column_widths.file)
        status = str_with_fixed_width(task.status_display, column_widths.status)
        text   = str_with_fixed_width(task.text, column_widths.text)
        return f'{prefix}{due}{_SEP}{file_}{_SEP}{status}{_SEP}{text}'

    # ------------------------------------------------------------------
    # Grouped view (by file, default)
    # ------------------------------------------------------------------

    def _show_tasks_grouped_by_file(self, groups: dict[str, list[Task]]) -> Task | None:
        """
        Renders tasks in a fuzzy finder grouped by file, with columns for due
        date, status and task text. Returns the selected task.
        """
        all_tasks = [t for ts in groups.values() for t in ts]
        col_due, col_status, col_text = self._grouped_by_file_widths(all_tasks)

        s = str_with_fixed_width
        header = (
            f'   {_PFX_NONE}{s(self._GROUPED_COLS[0], col_due)}{_SEP}'
            f'{s(self._GROUPED_COLS[1], col_status)}{_SEP}'
            f'{self._GROUPED_COLS[2]}'
        )

        task_index: list[Task] = []
        choices: list[Choice]  = []

        total_row_width = 4 + col_due + len(_SEP) + col_status + len(_SEP) + col_text

        for file_path, tasks in groups.items():
            # File headers use the path string as value.
            # Selecting a header opens the file at line 1.
            fill = '─' * max(0, total_row_width - len(file_path) - 4)
            choices.append(Choice(value=file_path, name=f' ── {file_path} {fill}'))

            for task in tasks:
                idx = len(task_index)
                task_index.append(task)
                choices.append(Choice(
                    value=idx,
                    name=self._grouped_by_file_row(task, col_due, col_status, col_text),
                ))

        print()
        try:
            result = self._run_fuzzy(choices, header)
        except KeyboardInterrupt:
            return None

        if isinstance(result, int):
            return task_index[result]
        if isinstance(result, str):
            # File header selected → open the file at line 1
            return Task(file_path=result, line_number=1, status=' ', text='')
        return None


    def _grouped_by_file_widths(self, tasks: list[Task]) -> tuple[int, int, int]:
        col_due    = max(10, min(max((len(t.due_date_str) for t in tasks), default=10), 15))
        col_status = max(len(self._GROUPED_COLS[1]), 3)  # 'Status' = 6

        overhead  = 4 + len(_SEP) * 2 + 5
        col_text  = max(10, console.width - overhead - col_due - col_status)

        return col_due, col_status, col_text

    def _grouped_by_file_row(
        self,
        task: Task,
        col_due: int,
        col_status: int,
        col_text: int,
    ) -> str:
        s      = str_with_fixed_width
        prefix = self._urgency_prefix(task)
        due    = s(task.due_date_str, col_due)
        status = s(task.status_display, col_status)
        text   = s(task.text, col_text)
        return f'{prefix}{due}{_SEP}{status}{_SEP}{text}'

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _urgency_prefix(task: Task) -> str:
        """Return a 4-char urgency indicator prefix for the due-date column."""
        if task.is_overdue:
            return _PFX_OVERDUE  # '!!! '
        if task.is_today:
            return _PFX_TODAY    # '!   '
        return _PFX_NONE         # '    '

    @staticmethod
    def _run_fuzzy(choices: list[Choice], header: str) -> Any:
        """Launch InquirerPy fuzzy finder and return the selected value.

        Raises KeyboardInterrupt if the user presses Ctrl-C.
        Returns an int index if the user selects a task row.
        """
        result = inquirer.fuzzy(  # type: ignore
            message=header,
            choices=choices,
            qmark='',
            default='',
            max_height='90%',
            border=True,
            info=True,
            match_exact=False,
            marker='❯',
            marker_pl=' ',
            style=get_style(
                {'question': 'bold', 'pointer': 'fg:#f4f4f4 bg:#522a37'},
                style_override=False,
            ),
        ).execute()

        # Remove the 2 lines InquirerPy leaves behind after selection
        sys.stdout.write('\033[2A\033[0J')
        sys.stdout.flush()

        return result

    def _open_editor(self, task: Task) -> None:
        """Open the file at the task's line number in the configured editor."""
        abs_path = os.path.abspath(task.file_path)
        editor   = self._config.editor or os.environ.get('EDITOR', 'nvim')

        cmd = [editor, f'+{task.line_number}', abs_path]
        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError:
            print_error(
                f'Editor not found: {editor!r}. '
                'Configure it in ~/.config/due/config.yaml'
            )
        except subprocess.CalledProcessError as e:
            print_error(f'Editor exited with code {e.returncode}.')
