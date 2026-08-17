"""Тесты к заданиям недели 1. Читай их как спецификацию."""

import pytest

from tasks import (
    add_item,
    build_url,
    common_tags,
    count_words,
    describe_flag,
    first_non_empty,
    format_price,
    get_nested,
    middle_elements,
    second_largest,
    slugify,
    word_frequency,
)


# --- 01 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("amount", "currency", "expected"),
    [
        (1234.5, "USD", "1234.50 USD"),
        (10, "EUR", "10.00 EUR"),
        (0, "USD", "0.00 USD"),
        (19.999, "GEL", "20.00 GEL"),
    ],
)
def test_format_price(amount, currency, expected):
    assert format_price(amount, currency) == expected


def test_format_price_default_currency():
    assert format_price(5) == "5.00 USD"


# --- 02 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("  Hello   Full Stack World ", "hello-full-stack-world"),
        ("Python", "python"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_slugify(title, expected):
    assert slugify(title) == expected


# --- 03 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("text", "expected"),
    [("раз два три", 3), ("", 0), ("   ", 0), ("one", 1), ("a  b", 2)],
)
def test_count_words(text, expected):
    assert count_words(text) == expected


# --- 04 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([1, 2, 3, 4, 5], [2, 3, 4]),
        ([1, 2], []),
        ([1], []),
        ([], []),
        ([1, 2, 3], [2]),
    ],
)
def test_middle_elements(items, expected):
    assert middle_elements(items) == expected


def test_middle_elements_does_not_mutate_input():
    original = [1, 2, 3]
    middle_elements(original)
    assert original == [1, 2, 3]


# --- 05 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([5, 1, 9, 9, 3], 5),
        ([7, 7, 7], None),
        ([], None),
        ([1], None),
        ([-1, -5], -5),
        ([2, 1], 1),
    ],
)
def test_second_largest(numbers, expected):
    assert second_largest(numbers) == expected


# --- 06 ---------------------------------------------------------------------
def test_word_frequency():
    assert word_frequency("a b A") == {"a": 2, "b": 1}


def test_word_frequency_empty():
    assert word_frequency("") == {}


def test_word_frequency_case_insensitive():
    assert word_frequency("Python python PYTHON") == {"python": 3}


# --- 07 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("data", "keys", "default", "expected"),
    [
        ({"a": {"b": 1}}, ["a", "b"], None, 1),
        ({"a": {}}, ["a", "b"], 0, 0),
        ({}, ["a"], "нет", "нет"),
        ({"a": {"b": {"c": "глубоко"}}}, ["a", "b", "c"], None, "глубоко"),
        ({"a": 1}, ["a", "b"], None, None),
    ],
)
def test_get_nested(data, keys, default, expected):
    assert get_nested(data, keys, default) == expected


# --- 08 ---------------------------------------------------------------------
def test_common_tags():
    assert common_tags(["py", "js", "css"], ["js", "py", "go"]) == ["js", "py"]


def test_common_tags_no_overlap():
    assert common_tags(["py"], ["go"]) == []


def test_common_tags_deduplicates():
    assert common_tags(["py", "py"], ["py"]) == ["py"]


# --- 09 ---------------------------------------------------------------------
def test_add_item_to_existing_basket():
    basket = ["a"]
    assert add_item("b", basket) == ["a", "b"]


def test_add_item_creates_independent_baskets():
    """Главная проверка недели: изменяемый аргумент по умолчанию."""
    assert add_item("x") == ["x"]
    assert add_item("y") == ["y"]


# --- 10 ---------------------------------------------------------------------
def test_build_url_sorts_params():
    assert build_url("/api", page=2, limit=10) == "/api?limit=10&page=2"


def test_build_url_without_params():
    assert build_url("/api") == "/api"


def test_build_url_single_param():
    assert build_url("/users", id=7) == "/users?id=7"


# --- 11 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([0, "", None, "ok", "no"], "ok"),
        ([0, ""], None),
        ([], None),
        ([[], {}, [1]], [1]),
        ([False, 0, 42], 42),
    ],
)
def test_first_non_empty(values, expected):
    assert first_non_empty(values) == expected


# --- 12 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("flag", "expected"),
    [(None, "не задан"), (True, "включён"), (False, "выключен")],
)
def test_describe_flag(flag, expected):
    assert describe_flag(flag) == expected
