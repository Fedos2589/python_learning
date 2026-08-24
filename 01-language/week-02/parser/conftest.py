"""Общие фикстуры для тестов парсера.

`sys.path` правим по той же причине, что и на неделе 1: нормальную структуру
пакета соберём на этапе 2.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest

from parsing import LogRecord

LOG_PATH = Path(__file__).parent / "access-log.csv"


@pytest.fixture
def log_lines() -> list[str]:
    """Строки файла access-log.csv — вместе с битыми и комментарием."""
    return LOG_PATH.read_text(encoding="utf-8").splitlines()


@pytest.fixture
def sample_records() -> list[LogRecord]:
    """Двадцать записей из access-log.csv, разобранных заранее.

    Заданы здесь руками, а не через parse_lines: тесты статистики не должны
    падать из-за незаконченного парсера. Каждый модуль тестируется отдельно —
    это и есть смысл слова «юнит» в «юнит-тестах».
    """
    raw = [
        ("2026-08-17T09:14:02", "GET", "/api/users", 200, 45),
        ("2026-08-17T09:14:03", "GET", "/api/users", 200, 45),
        ("2026-08-17T09:15:10", "GET", "/api/search", 200, 180),
        ("2026-08-17T09:16:00", "GET", "/api/search", 200, 241),
        ("2026-08-17T09:17:40", "GET", "/api/report", 200, 830),
        ("2026-08-17T09:18:01", "POST", "/api/login", 401, 12),
        ("2026-08-17T09:18:30", "POST", "/api/login", 401, 11),
        ("2026-08-17T09:19:00", "POST", "/api/login", 200, 15),
        ("2026-08-17T09:20:00", "GET", "/health", 200, 2),
        ("2026-08-17T09:21:00", "GET", "/health", 200, 3),
        ("2026-08-17T09:22:00", "GET", "/health", 200, 2),
        ("2026-08-17T09:23:00", "GET", "/api/orders", 500, 90),
        ("2026-08-17T10:00:00", "GET", "/api/orders", 200, 60),
        ("2026-08-17T10:01:00", "GET", "/api/orders", 200, 70),
        ("2026-08-17T10:02:00", "GET", "/api/users", 404, 5),
        ("2026-08-17T10:03:00", "GET", "/health", 200, 2),
        ("2026-08-17T11:00:00", "GET", "/api/search", 200, 200),
        ("2026-08-17T11:01:00", "GET", "/api/report", 200, 830),
        ("2026-08-17T11:02:00", "GET", "/api/orders", 503, 88),
        ("2026-08-17T11:03:00", "GET", "/health", 200, 3),
    ]
    return [LogRecord(*row) for row in raw]
