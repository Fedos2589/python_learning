"""Тесты к report.py. Читай их как спецификацию."""

from report import build_report

EXPECTED = """\
Всего запросов: 20
Уникальных путей: 6
Доля ошибок 5xx: 10.0%
Самый нагруженный час: 09
Коды ответов:
  2xx: 15
  4xx: 3
  5xx: 2
Топ-3 по среднему времени:
  /api/report: 830.0 мс
  /api/search: 207.0 мс
  /api/orders: 77.0 мс"""


def test_build_report(sample_records):
    assert build_report(sample_records) == EXPECTED


def test_build_report_empty_log():
    assert build_report([]) == "Лог пуст"


def test_build_report_has_no_trailing_newline(sample_records):
    assert not build_report(sample_records).endswith("\n")


def test_build_report_line_count(sample_records):
    """Четыре строки сводки, заголовок с тремя кодами, заголовок с тремя путями."""
    assert len(build_report(sample_records).split("\n")) == 12


def test_build_report_indents_nested_lines_with_two_spaces(sample_records):
    nested = [
        line
        for line in build_report(sample_records).split("\n")
        if line.startswith(" ")
    ]
    assert len(nested) == 6
    assert all(line.startswith("  ") and not line.startswith("   ") for line in nested)
