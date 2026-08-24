"""Тесты к stats.py. Читай их как спецификацию.

Записи приходят из фикстуры sample_records (см. conftest.py) — двадцать строк
из access-log.csv, заданных вручную. Тесты статистики не зависят от парсера:
каждый модуль проверяется отдельно.
"""

import pytest

from parsing import LogRecord
from stats import (
    busiest_hour,
    count_by_status_class,
    error_rate,
    requests_per_path,
    slowest_paths,
    unique_paths,
)


def rec(
    path: str = "/x", status: int = 200, ms: int = 10, hour: str = "09"
) -> LogRecord:
    """Короткий конструктор записи для точечных тестов."""
    return LogRecord(f"2026-08-17T{hour}:00:00", "GET", path, status, ms)


# --- Задача 4. unique_paths --------------------------------------------------
def test_unique_paths(sample_records):
    assert unique_paths(sample_records) == {
        "/api/users",
        "/api/search",
        "/api/report",
        "/api/login",
        "/health",
        "/api/orders",
    }


def test_unique_paths_empty():
    assert unique_paths([]) == set()


def test_unique_paths_deduplicates():
    assert unique_paths([rec("/a"), rec("/a"), rec("/b")]) == {"/a", "/b"}


# --- Задача 5. requests_per_path ---------------------------------------------
def test_requests_per_path(sample_records):
    assert requests_per_path(sample_records) == {
        "/api/users": 3,
        "/api/search": 3,
        "/api/report": 2,
        "/api/login": 3,
        "/health": 5,
        "/api/orders": 4,
    }


def test_requests_per_path_empty():
    assert requests_per_path([]) == {}


def test_requests_per_path_returns_plain_dict():
    """Counter — деталь реализации, наружу отдаём обычный dict."""
    result = requests_per_path([rec("/a")])
    assert type(result) is dict


# --- Задача 6. count_by_status_class ----------------------------------------
def test_count_by_status_class(sample_records):
    assert count_by_status_class(sample_records) == {"2xx": 15, "4xx": 3, "5xx": 2}


def test_count_by_status_class_skips_absent_classes():
    """Классов, которых нет в логе, в результате быть не должно."""
    assert count_by_status_class([rec(status=200)]) == {"2xx": 1}


def test_count_by_status_class_empty():
    assert count_by_status_class([]) == {}


@pytest.mark.parametrize(
    ("status", "expected"),
    [(200, "2xx"), (204, "2xx"), (301, "3xx"), (404, "4xx"), (503, "5xx")],
)
def test_count_by_status_class_boundaries(status, expected):
    assert count_by_status_class([rec(status=status)]) == {expected: 1}


# --- Задача 7. error_rate ----------------------------------------------------
def test_error_rate(sample_records):
    assert error_rate(sample_records) == pytest.approx(0.1)


def test_error_rate_empty_log_is_zero():
    """Пустой лог: 0.0, а не ZeroDivisionError."""
    assert error_rate([]) == 0.0


def test_error_rate_all_errors():
    assert error_rate([rec(status=500), rec(status=503)]) == 1.0


def test_error_rate_no_errors():
    assert error_rate([rec(status=200), rec(status=404)]) == 0.0


def test_error_rate_counts_only_5xx():
    """4xx — это ошибка клиента, в долю ошибок сервиса она не входит."""
    assert error_rate([rec(status=404), rec(status=500)]) == pytest.approx(0.5)


# --- Задача 8. slowest_paths -------------------------------------------------
def test_slowest_paths(sample_records):
    assert slowest_paths(sample_records, 3) == [
        ("/api/report", 830.0),
        ("/api/search", pytest.approx(207.0)),
        ("/api/orders", 77.0),
    ]


def test_slowest_paths_averages_not_sums():
    """Считаем среднее, а не сумму: два запроса по 10 мс медленнее одного в 15."""
    records = [rec("/slow", ms=10), rec("/slow", ms=10), rec("/fast", ms=15)]
    assert slowest_paths(records, 1) == [("/fast", 15.0)]


def test_slowest_paths_ties_sorted_by_name():
    records = [rec("/b", ms=100), rec("/a", ms=100)]
    assert slowest_paths(records, 2) == [("/a", 100.0), ("/b", 100.0)]


def test_slowest_paths_limit_bigger_than_data(sample_records):
    assert len(slowest_paths(sample_records, 99)) == 6


def test_slowest_paths_zero_limit(sample_records):
    assert slowest_paths(sample_records, 0) == []


def test_slowest_paths_empty():
    assert slowest_paths([], 3) == []


# --- Задача 9. busiest_hour --------------------------------------------------
def test_busiest_hour(sample_records):
    assert busiest_hour(sample_records) == "09"


def test_busiest_hour_empty_is_none():
    assert busiest_hour([]) is None


def test_busiest_hour_returns_two_digit_string():
    assert busiest_hour([rec(hour="07")]) == "07"


def test_busiest_hour_ignores_date():
    """Час суток, а не конкретный час конкретного дня."""
    records = [
        LogRecord("2026-08-17T14:00:00", "GET", "/a", 200, 1),
        LogRecord("2026-08-18T14:30:00", "GET", "/a", 200, 1),
        LogRecord("2026-08-18T09:00:00", "GET", "/a", 200, 1),
    ]
    assert busiest_hour(records) == "14"


def test_busiest_hour_tie_goes_to_earlier():
    records = [rec(hour="15"), rec(hour="08")]
    assert busiest_hour(records) == "08"
