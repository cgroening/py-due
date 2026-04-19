import re
from datetime import date, datetime
from pathlib import Path
from due.domain.models import Task
from due.storage.markdown.base import BaseMarkdownStorage


_TASK_REGEX_PATTERN = re.compile(r'^- \[([^\]]*)\] (.*)$')
_DUE_REGEX_PATTERN = re.compile(r'@due\(([^)]+)\)')
_TAG_REGEX_PATTERN = re.compile(r'@\w+\([^)]*\)')
_DATE_FORMATS = [
    '%Y-%m-%d',
    '%d.%m.%Y',
    '%d.%m.%y',
    '%Y/%m/%d',
]


def _parse_date(raw: str) -> date | None:
    """
    Tries to parse a date from the given raw string using multiple formats and
    returns a `date` object if successful, or `None` if parsing fails.
    """
    raw = raw.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


class FilesystemMarkdownStorage(BaseMarkdownStorage):
    """
    Markdown storage implementation that reads tasks from `.md` files in the
    filesystem. It recursively searches for `.md` files under the given root
    directory, parses them for tasks, and returns a list of `Task` objects with
    their file paths, line numbers, statuses, texts and due dates (if any).
    """
    def get_all_tasks(self, root_dir: str) -> list[Task]:
        """
        Recursively searches for `.md` files under `root_dir`, parses them for
        tasks and returns a list of `Task` objects with their file paths, line
        numbers, statuses, texts and due dates (if any). Files inside hidden
        directories (e.g. `.git`) are skipped.
        """
        tasks: list[Task] = []
        root = Path(root_dir)

        for md_file in sorted(root.rglob('*.md')):
            # Skip files inside hidden directories (e.g. .git)
            if any(part.startswith('.') for part in md_file.relative_to(root).parts):
                continue
            try:
                abs_path = str(md_file.resolve())
                tasks.extend(self._parse_file(md_file, abs_path))
            except Exception:
                pass

        return tasks

    def _parse_file(self, file_path: Path, rel_path: str) -> list[Task]:
        """
        Parses the given Markdown file for tasks and returns a list of `Task`
        objects with their file paths, line numbers, statuses, texts and due
        dates (if any). Tasks are identified by lines matching the pattern
        `- [ ] Task text` (open), `- [x] Task text` (completed) or
        `- [c] Task text` (cancelled). Continuation lines that are indented
        with two spaces are included in the task text. The `@due(...)` tag is
        extracted from the first line and all continuation lines and parsed into
        a date if possible. The task text is cleaned of all `@tags` and only the
        first line is kept if it's a multi-line task.
        """
        tasks: list[Task] = []
        lines = file_path.read_text(encoding='utf-8').splitlines()

        i = 0
        while i < len(lines):
            match = _TASK_REGEX_PATTERN.match(lines[i])
            if not match:
                i += 1
                continue

            status = match.group(1)
            first_line_text = match.group(2)
            task_line_number = i + 1  # 1-based

            # Collect indented continuation lines
            j = i + 1
            continuation: list[str] = []
            while j < len(lines):
                next_line = lines[j]
                if next_line.startswith('  ') \
                and not _TASK_REGEX_PATTERN.match(next_line):
                    continuation.append(next_line.strip())
                    j += 1
                else:
                    break

            # Find @due tag across first line and all continuation lines
            all_content = first_line_text + ' ' + ' '.join(continuation)
            due_match = _DUE_REGEX_PATTERN.search(all_content)
            due_date: date | None = None
            due_raw: str | None = None

            if due_match:
                due_raw = due_match.group(1).strip()
                due_date = _parse_date(due_raw)

            # Clean task text: strip all @tags from the first line
            clean_text = _TAG_REGEX_PATTERN.sub('', first_line_text).strip()

            tasks.append(Task(
                file_path=rel_path,
                line_number=task_line_number,
                status=status,
                text=clean_text,
                due_date=due_date,
                due_date_raw=due_raw,
            ))

            i = j

        return tasks
