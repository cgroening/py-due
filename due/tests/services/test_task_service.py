from datetime import date, timedelta
from due.domain.models import Task
from due.services.task_service import TaskService


TODAY  = date.today()
PAST   = TODAY - timedelta(days=1)
FUTURE = TODAY + timedelta(days=1)


def _t(
    status: str = ' ',
    due_date: date | None = None,
    due_date_raw: str | None = None,
    file_path: str = '/f.md',
) -> Task:
    # Mirror real parser behaviour: a parsed date always has a raw string too
    if due_date is not None and due_date_raw is None:
        due_date_raw = due_date.strftime('%Y-%m-%d')
    return Task(
        file_path=file_path,
        line_number=1,
        status=status,
        text='task',
        due_date=due_date,
        due_date_raw=due_date_raw,
    )


class TestFilterTasks:
    def test_excludes_done_by_default(self, service: TaskService) -> None:
        tasks = [_t(status='x', due_date=TODAY), _t(status=' ', due_date=TODAY)]
        assert service.filter_tasks(tasks) == [tasks[1]]

    def test_excludes_cancelled_by_default(self, service: TaskService) -> None:
        tasks = [_t(status='c', due_date=TODAY), _t(status=' ', due_date=TODAY)]
        assert service.filter_tasks(tasks) == [tasks[1]]

    def test_includes_closed_when_requested(self, service: TaskService) -> None:
        tasks = [
            _t(status='x', due_date=TODAY),
            _t(status='c', due_date=TODAY),
            _t(status=' ', due_date=TODAY)
        ]
        assert len(service.filter_tasks(tasks, include_closed_tasks=True)) == 3

    def test_excludes_undated_by_default(self, service: TaskService) -> None:
        tasks = [_t(due_date=TODAY), _t()]
        assert service.filter_tasks(tasks) == [tasks[0]]

    def test_includes_undated_when_requested(self, service: TaskService) -> None:
        tasks = [_t(due_date=TODAY), _t()]
        assert len(service.filter_tasks(tasks, include_undated_tasks=True)) == 2

    def test_due_filter_minus_one_returns_overdue_only(
        self, service: TaskService
    ) -> None:
        tasks = [_t(due_date=PAST), _t(due_date=TODAY), _t(due_date=FUTURE)]
        assert service.filter_tasks(tasks, due_filter=-1) == [tasks[0]]

    def test_due_filter_zero_returns_today_only(
        self, service: TaskService
    ) -> None:
        tasks = [_t(due_date=PAST), _t(due_date=TODAY), _t(due_date=FUTURE)]
        assert service.filter_tasks(tasks, due_filter=0) == [tasks[1]]

    def test_due_filter_one_returns_future_only(
        self, service: TaskService
    ) -> None:
        tasks = [_t(due_date=PAST), _t(due_date=TODAY), _t(due_date=FUTURE)]
        assert service.filter_tasks(tasks, due_filter=1) == [tasks[2]]

    def test_due_filter_excludes_unparseable_dates(
        self, service: TaskService
    ) -> None:
        tasks = [_t(due_date_raw='someday'), _t(due_date=FUTURE)]
        result = service.filter_tasks(tasks, due_filter=1)
        assert tasks[0] not in result
        assert tasks[1] in result

    def test_empty_input_returns_empty(self, service: TaskService) -> None:
        assert service.filter_tasks([]) == []


class TestSortByDate:
    def test_sorts_oldest_first(self, service: TaskService) -> None:
        tasks = [_t(due_date=FUTURE), _t(due_date=PAST), _t(due_date=TODAY)]
        assert service.sort_by_date(tasks) == [tasks[1], tasks[2], tasks[0]]

    def test_unparseable_date_after_dated_tasks(
        self, service: TaskService
    ) -> None:
        dated = _t(due_date=TODAY)
        raw   = _t(due_date_raw='someday')
        assert service.sort_by_date([raw, dated]) == [dated, raw]

    def test_undated_last(self, service: TaskService) -> None:
        dated   = _t(due_date=TODAY)
        undated = _t()
        assert service.sort_by_date([undated, dated]) == [dated, undated]

    def test_empty_input_returns_empty(self, service: TaskService) -> None:
        assert service.sort_by_date([]) == []


class TestGroupByFile:
    def test_groups_tasks_by_file_path(self, service: TaskService) -> None:
        t1 = _t(file_path='/a.md')
        t2 = _t(file_path='/b.md')
        t3 = _t(file_path='/a.md')
        groups = service.group_by_file([t1, t2, t3])
        assert list(groups.keys()) == ['/a.md', '/b.md']
        assert groups['/a.md'] == [t1, t3]
        assert groups['/b.md'] == [t2]

    def test_preserves_task_order_within_group(
        self, service: TaskService
    ) -> None:
        tasks = [
            _t(file_path='/a.md'),
            _t(file_path='/a.md'),
            _t(file_path='/a.md')
        ]
        assert service.group_by_file(tasks)['/a.md'] == tasks

    def test_empty_input_returns_empty_dict(self, service: TaskService) -> None:
        assert service.group_by_file([]) == {}
