from datetime import date
from due.domain.models import Task


class TestStatusDisplay:
    def test_open_task(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).status_display == '[ ]'

    def test_done_task(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status='x', text='T'
        ).status_display == '[x]'

    def test_cancelled_task(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status='c', text='T'
        ).status_display == '[c]'


class TestHasDueTag:
    def test_true_when_raw_is_set(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date_raw='2025-01-01'
        )
        assert task.has_due_tag is True

    def test_false_when_raw_is_none(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).has_due_tag is False


class TestIsOverdue:
    def test_true_for_past_date(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date(2000, 1, 1)
        )
        assert task.is_overdue is True

    def test_false_for_today(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date.today()
        )
        assert task.is_overdue is False

    def test_false_when_no_date(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).is_overdue is False


class TestIsToday:
    def test_true_for_today(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date.today()
        )
        assert task.is_today is True

    def test_false_for_past(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date(2000, 1, 1)
        )
        assert task.is_today is False

    def test_false_when_no_date(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).is_today is False


class TestIsFuture:
    def test_true_for_future_date(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date(2099, 12, 31)
        )
        assert task.is_future is True

    def test_false_for_past(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date(2000, 1, 1)
        )
        assert task.is_future is False

    def test_false_when_no_date(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).is_future is False


class TestDueDateStr:
    def test_formatted_date(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date=date(2025, 5, 1)
        )
        assert task.due_date_str == '2025-05-01'

    def test_raw_with_question_mark_prefix_when_unparseable(self) -> None:
        task = Task(
            file_path='/a.md', line_number=1, status=' ', text='T',
            due_date_raw='someday'
        )
        assert task.due_date_str == '?someday'

    def test_dash_when_no_date(self) -> None:
        assert Task(
            file_path='/a.md', line_number=1, status=' ', text='T'
        ).due_date_str == '-'
