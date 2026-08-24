"""Тесты к parsing.py. Читай их как спецификацию."""

import pytest

from parsing import LogRecord, count_valid_and_broken, parse_line, parse_lines

VALID = "2026-08-17T09:14:02,GET,/api/users,200,45"


# --- Задача 1: parse_line, годные строки ------------------------------------
def test_parse_line_returns_log_record():
    result = parse_line(VALID)
    assert result == LogRecord("2026-08-17T09:14:02", "GET", "/api/users", 200, 45)


def test_parse_line_converts_numbers_to_int():
    result = parse_line(VALID)
    assert isinstance(result.status, int)
    assert isinstance(result.duration_ms, int)


def test_parse_line_strips_spaces_around_fields():
    result = parse_line(" 2026-08-17T09:14:02 , GET , /api/users , 200 , 45 ")
    assert result == LogRecord("2026-08-17T09:14:02", "GET", "/api/users", 200, 45)


def test_parse_line_uppercases_method():
    assert parse_line("2026-08-17T09:14:02,get,/x,200,1").method == "GET"


def test_parse_line_result_is_a_tuple():
    """NamedTuple остаётся кортежем: его можно распаковать."""
    timestamp, method, path, status, duration = parse_line(VALID)
    assert (method, path, status, duration) == ("GET", "/api/users", 200, 45)
    assert timestamp.startswith("2026")


# --- Задача 1: негодные строки ----------------------------------------------
@pytest.mark.parametrize(
    ("line", "why"),
    [
        ("", "пустая строка"),
        ("   ", "только пробелы"),
        ("# комментарий", "строка-комментарий"),
        ("  # с отступом", "комментарий с отступом"),
        ("2026-08-17T09:14:02,GET,/api/users,200", "четыре поля вместо пяти"),
        ("2026-08-17T09:14:02,GET,/api/users,200,45,extra", "шесть полей"),
        ("2026-08-17T09:14:02,GET,/api/users,abc,45", "status не число"),
        ("2026-08-17T09:14:02,GET,/api/users,200,xx", "duration не число"),
        ("2026-08-17T09:14:02,,/api/users,200,45", "пустой method"),
        ("2026-08-17T09:14:02,GET,,200,45", "пустой path"),
        ("совсем не строка лога", "мусор"),
    ],
)
def test_parse_line_returns_none_for_bad_lines(line, why):
    assert parse_line(line) is None, why


def test_parse_line_does_not_raise_on_bad_input():
    """Битая строка — не авария. Исключений быть не должно."""
    for line in ("", "мусор", "a,b,c,d,e", "#"):
        parse_line(line)


# --- Задача 2: parse_lines ---------------------------------------------------
def test_parse_lines_skips_bad_ones():
    lines = ["# заголовок", VALID, "мусор", "", VALID]
    assert len(list(parse_lines(lines))) == 2


def test_parse_lines_keeps_order():
    lines = [
        "2026-08-17T09:00:00,GET,/first,200,1",
        "мусор",
        "2026-08-17T09:00:01,GET,/second,200,2",
    ]
    assert [record.path for record in parse_lines(lines)] == ["/first", "/second"]


def test_parse_lines_is_a_generator():
    """Функция с yield: работа не начинается до первого запроса элемента."""
    result = parse_lines([VALID])
    assert not isinstance(result, list)
    assert next(iter(result)).path == "/api/users"


def test_parse_lines_is_lazy():
    """Генератор читает по одной строке, а не всё сразу.

    Здесь источник бесконечный: список-comprehension повесил бы тест навсегда.
    """

    def endless():
        while True:
            yield VALID

    records = parse_lines(endless())
    first = next(iter(records))
    assert first.path == "/api/users"


def test_parse_lines_empty_input():
    assert list(parse_lines([])) == []


def test_parse_lines_handles_trailing_newlines():
    """Строки из файла приходят с '\\n' на конце — это не должно ломать разбор."""
    assert len(list(parse_lines([VALID + "\n", VALID + "\n"]))) == 2


# --- Задача 3: count_valid_and_broken ---------------------------------------
def test_count_valid_and_broken():
    lines = ["# заголовок", "", VALID, "мусор", VALID, "a,b,c,d,e"]
    assert count_valid_and_broken(lines) == (2, 2)


def test_count_valid_and_broken_ignores_comments_and_blanks():
    """Комментарий и пустая строка — не данные, битыми они не считаются."""
    assert count_valid_and_broken(["# заголовок", "", "   ", "мусор"]) == (0, 1)


def test_count_valid_and_broken_empty_input():
    assert count_valid_and_broken([]) == (0, 0)


def test_count_valid_and_broken_returns_tuple():
    result = count_valid_and_broken([VALID])
    assert isinstance(result, tuple)
    valid, broken = result
    assert (valid, broken) == (1, 0)


# --- Разбор реального файла --------------------------------------------------
def test_parses_the_sample_log(log_lines):
    """access-log.csv: 20 годных записей и 3 битые строки."""
    assert count_valid_and_broken(log_lines) == (20, 3)
    assert len(list(parse_lines(log_lines))) == 20
