from datetime import date
from due.domain.models import Task


HIDDEN_STATUSES = {'x', 'c'}


class TaskService:
    def filter_tasks(
        self,
        tasks: list[Task],
        all_statuses: bool = False,
        all_tasks: bool = False,
        when: int | None = None,
    ) -> list[Task]:
        result = tasks

        # Filter out [x] and [c] unless --all-statuses
        if not all_statuses:
            result = [t for t in result if t.status not in HIDDEN_STATUSES]

        # Filter to only tasks with @due tag unless --all-tasks
        if not all_tasks:
            result = [t for t in result if t.has_due_tag]

        # Filter by date relationship (only applicable if due_date is parseable)
        if when is not None:
            today = date.today()
            if when == -1:
                result = [
                    t for t in result
                    if t.due_date is not None and t.due_date < today
                ]
            elif when == 0:
                result = [
                    t for t in result
                    if t.due_date is not None and t.due_date == today
                ]
            elif when == 1:
                result = [
                    t for t in result
                    if t.due_date is not None and t.due_date > today
                ]

        return result

    def sort_by_date(self, tasks: list[Task]) -> list[Task]:
        """Sort by due date ascending (oldest first).

        Order:
          1. Tasks with parseable due date (oldest first)
          2. Tasks with unparseable @due tag
          3. Tasks without @due tag (only when --all-tasks)
        """
        def sort_key(t: Task) -> tuple[int, date]:
            if t.due_date is not None:
                return (0, t.due_date)
            if t.due_date_raw is not None:
                return (1, date.max)  # unparseable @due → after all dated
            return (2, date.max)      # no @due → last

        return sorted(tasks, key=sort_key)

    def group_by_file(self, tasks: list[Task]) -> dict[str, list[Task]]:
        """Group tasks by file path, preserving original file order."""
        groups: dict[str, list[Task]] = {}
        for task in tasks:
            if task.file_path not in groups:
                groups[task.file_path] = []
            groups[task.file_path].append(task)
        return groups
