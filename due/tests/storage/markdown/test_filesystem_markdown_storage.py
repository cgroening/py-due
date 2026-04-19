from datetime import date
from pathlib import Path
import pytest
from due.storage.markdown.filesystem import FilesystemMarkdownStorage


@pytest.fixture
def storage() -> FilesystemMarkdownStorage:
    return FilesystemMarkdownStorage()


class TestGetAllTasks:
    def test_finds_tasks_in_md_file(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'notes.md').write_text('- [ ] My task\n')
        assert len(storage.get_all_tasks(str(tmp_path))) == 1

    def test_collects_tasks_from_multiple_files(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'a.md').write_text('- [ ] Task A\n')
        (tmp_path / 'b.md').write_text('- [ ] Task B\n- [ ] Task C\n')
        assert len(storage.get_all_tasks(str(tmp_path))) == 3

    def test_skips_hidden_directories(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        hidden = tmp_path / '.hidden'
        hidden.mkdir()
        (hidden / 'notes.md').write_text('- [ ] Should be skipped\n')
        assert storage.get_all_tasks(str(tmp_path)) == []

    def test_ignores_non_md_files(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'notes.txt').write_text('- [ ] Not a markdown task\n')
        assert storage.get_all_tasks(str(tmp_path)) == []

    def test_returns_empty_list_for_empty_directory(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        assert storage.get_all_tasks(str(tmp_path)) == []

    def test_scans_subdirectories_recursively(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        sub = tmp_path / 'sub'
        sub.mkdir()
        (sub / 'notes.md').write_text('- [ ] Nested task\n')
        assert len(storage.get_all_tasks(str(tmp_path))) == 1


class TestTaskParsing:
    def test_open_task_status(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Open\n')
        assert storage.get_all_tasks(str(tmp_path))[0].status == ' '

    def test_done_task_status(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [x] Done\n')
        assert storage.get_all_tasks(str(tmp_path))[0].status == 'x'

    def test_cancelled_task_status(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [c] Cancelled\n')
        assert storage.get_all_tasks(str(tmp_path))[0].status == 'c'

    def test_extracts_due_tag(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Task @due(2025-05-01)\n')
        task = storage.get_all_tasks(str(tmp_path))[0]
        assert task.due_date == date(2025, 5, 1)
        assert task.due_date_raw == '2025-05-01'

    def test_strips_tags_from_text(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Clean text @due(2025-05-01)\n')
        assert storage.get_all_tasks(str(tmp_path))[0].text == 'Clean text'

    def test_no_due_tag_sets_has_due_tag_false(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] No due date\n')
        assert storage.get_all_tasks(str(tmp_path))[0].has_due_tag is False

    def test_unparseable_due_date_sets_raw_only(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Task @due(someday)\n')
        task = storage.get_all_tasks(str(tmp_path))[0]
        assert task.due_date is None
        assert task.due_date_raw == 'someday'

    def test_correct_line_number(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('# Header\n\n- [ ] Third line task\n')
        assert storage.get_all_tasks(str(tmp_path))[0].line_number == 3

    def test_due_tag_in_continuation_line(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        content = '- [ ] Task text\n  @due(2025-06-01)\n'
        (tmp_path / 'f.md').write_text(content)
        task = storage.get_all_tasks(str(tmp_path))[0]
        assert task.due_date == date(2025, 6, 1)

    def test_non_task_lines_are_skipped(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        content = '# Heading\nSome text\n- [ ] Only task\n'
        (tmp_path / 'f.md').write_text(content)
        assert len(storage.get_all_tasks(str(tmp_path))) == 1

    def test_parses_german_date_format(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Task @due(01.05.2025)\n')
        assert storage.get_all_tasks(str(tmp_path))[0].due_date == date(2025, 5, 1)

    def test_parses_slash_date_format(
        self, storage: FilesystemMarkdownStorage, tmp_path: Path
    ) -> None:
        (tmp_path / 'f.md').write_text('- [ ] Task @due(2025/05/01)\n')
        assert storage.get_all_tasks(str(tmp_path))[0].due_date == date(2025, 5, 1)
