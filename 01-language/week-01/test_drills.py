"""Тесты к добору недели 1. Читай их как спецификацию."""

import pytest

from drills import (
    count_by_first_letter,
    describe_user,
    find_index,
    format_duration,
    initials,
    invert,
    is_palindrome,
    mask_email,
    only_in_one,
    register,
    resolve_flag,
    rotate,
    running_total,
    sort_by_length,
    truncate,
    without_none,
)


# --- 01 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("full_name", "expected"),
    [
        ("Иван Петров", "И.П."),
        ("  анна   мария петрова ", "А.М.П."),
        ("Ted", "T."),
        ("", ""),
        ("   ", ""),
    ],
)
def test_initials(full_name, expected):
    assert initials(full_name) == expected


# --- 02 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (65, "1:05"),
        (7, "0:07"),
        (0, "0:00"),
        (60, "1:00"),
        (3600, "60:00"),
        (599, "9:59"),
    ],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


# --- 03 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("А роза упала на лапу Азора", True),
        ("Привет", False),
        ("abba", True),
        ("Ab Ba", True),
        ("", True),
        ("a", True),
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected


# --- 04 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("text", "limit", "expected"),
    [
        ("hello", 5, "hello"),
        ("hello", 10, "hello"),
        ("hello world", 8, "hello w…"),
        ("hello", 0, ""),
        ("hello", -3, ""),
        ("hello", 1, "…"),
        ("", 5, ""),
    ],
)
def test_truncate(text, limit, expected):
    assert truncate(text, limit) == expected


def test_truncate_never_exceeds_limit():
    for limit in range(1, 12):
        assert len(truncate("довольно длинная строка", limit)) <= limit


# --- 05 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("alexander@gmail.com", "a***r@gmail.com"),
        ("ted@intch.org", "t***d@intch.org"),
        ("ab@mail.ru", "ab@mail.ru"),
        ("a@mail.ru", "a@mail.ru"),
        ("не адрес", "не адрес"),
    ],
)
def test_mask_email(email, expected):
    assert mask_email(email) == expected


# --- 06 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "step", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [3, 4, 5, 1, 2]),
        ([1, 2, 3], 4, [2, 3, 1]),
        ([1, 2, 3], -1, [3, 1, 2]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([], 3, []),
        ([7], 5, [7]),
    ],
)
def test_rotate(items, step, expected):
    assert rotate(items, step) == expected


def test_rotate_does_not_mutate_input():
    original = [1, 2, 3]
    rotate(original, 1)
    assert original == [1, 2, 3]


# --- 07 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([1, 2, 3], [1, 3, 6]), ([], []), ([5], [5]), ([1, -1, 1], [1, 0, 1])],
)
def test_running_total(numbers, expected):
    assert running_total(numbers) == expected


# --- 08 ---------------------------------------------------------------------
def test_sort_by_length():
    assert sort_by_length(["bbb", "a", "cc"]) == ["a", "cc", "bbb"]


def test_sort_by_length_is_stable():
    """Слова одной длины сохраняют исходный порядок — сортировка стабильная."""
    assert sort_by_length(["bb", "aa", "cc"]) == ["bb", "aa", "cc"]


def test_sort_by_length_does_not_mutate_input():
    original = ["bbb", "a"]
    sort_by_length(original)
    assert original == ["bbb", "a"]


# --- 09 ---------------------------------------------------------------------
def test_invert():
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_invert_empty():
    assert invert({}) == {}


def test_invert_duplicate_values_last_wins():
    assert invert({"a": 1, "b": 1}) == {1: "b"}


# --- 10 ---------------------------------------------------------------------
def test_count_by_first_letter():
    assert count_by_first_letter(["Apple", "avocado", "beet"]) == {"a": 2, "b": 1}


def test_count_by_first_letter_skips_empty():
    assert count_by_first_letter(["", "x"]) == {"x": 1}


def test_count_by_first_letter_empty_list():
    assert count_by_first_letter([]) == {}


# --- 11 ---------------------------------------------------------------------
def test_only_in_one():
    assert only_in_one(["py", "js"], ["js", "go"]) == ["go", "py"]


def test_only_in_one_no_difference():
    assert only_in_one(["py"], ["py"]) == []


def test_only_in_one_one_side_empty():
    assert only_in_one(["py", "js"], []) == ["js", "py"]


def test_only_in_one_deduplicates():
    assert only_in_one(["py", "py"], []) == ["py"]


# --- 12 ---------------------------------------------------------------------
def test_register_new():
    assert register("ted") == {"ted": 1}


def test_register_increments():
    assert register("ted", {"ted": 1}) == {"ted": 2}


def test_register_adds_to_existing():
    assert register("anna", {"ted": 1}) == {"ted": 1, "anna": 1}


def test_register_creates_independent_registries():
    """Изменяемый аргумент по умолчанию: два вызова не должны делить словарь."""
    assert register("a") == {"a": 1}
    assert register("b") == {"b": 1}


def test_register_fills_explicitly_passed_empty_registry():
    """Пустой словарь передан явно — наполняем его, а не создаём новый."""
    registry: dict[str, int] = {}
    result = register("ted", registry)
    assert result == {"ted": 1}
    assert registry == {"ted": 1}, "нужна проверка на None, а не на пустоту"


# --- 13 ---------------------------------------------------------------------
def test_describe_user_sorts_keys():
    assert describe_user(role="dev", name="Ted") == "name=Ted; role=dev"


def test_describe_user_empty():
    assert describe_user() == ""


def test_describe_user_single_field():
    assert describe_user(name="Ted") == "name=Ted"


def test_describe_user_non_string_values():
    assert describe_user(age=37, active=True) == "active=True; age=37"


# --- 14 ---------------------------------------------------------------------
def test_without_none_keeps_falsy():
    assert without_none([0, "", None, [], 1]) == [0, "", [], 1]


def test_without_none_all_none():
    assert without_none([None, None]) == []


def test_without_none_empty():
    assert without_none([]) == []


def test_without_none_keeps_false():
    assert without_none([False, None, True]) == [False, True]


# --- 15 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("local", "default", "expected"),
    [
        (None, True, True),
        (None, False, False),
        (False, True, False),
        (True, False, True),
    ],
)
def test_resolve_flag(local, default, expected):
    assert resolve_flag(local, default) is expected


# --- 16 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "target", "expected"),
    [
        (["a", "b", "a"], "a", 0),
        (["a", "b"], "b", 1),
        (["a"], "z", None),
        ([], "a", None),
    ],
)
def test_find_index(items, target, expected):
    assert find_index(items, target) == expected
