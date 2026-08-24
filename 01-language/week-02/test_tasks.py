"""Тесты к заданиям недели 2. Читай их как спецификацию."""

from itertools import count

import pytest

from tasks import (
    call_twice,
    chunks,
    even_lengths,
    first_matching,
    flatten,
    format_rows,
    head_and_rest,
    index_by_length,
    longest,
    merge_configs,
    min_max,
    numbered_pairs,
    squares,
    top_by_score,
    unique_domains,
)


# --- 01 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([1, 2, 3], [1, 4, 9]), ([], []), ([-2], [4]), ([0], [0])],
)
def test_squares(numbers, expected):
    assert squares(numbers) == expected


def test_squares_does_not_mutate_input():
    original = [1, 2]
    squares(original)
    assert original == [1, 2]


# --- 02 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["ab", "a", "abcd"], [2, 4]),
        (["a", "abc"], []),
        ([], []),
        (["", "xy"], [0, 2]),
    ],
)
def test_even_lengths(words, expected):
    assert even_lengths(words) == expected


# --- 03 ---------------------------------------------------------------------
def test_index_by_length():
    assert index_by_length(["a", "bb", "cc"]) == {1: "a", 2: "cc"}


def test_index_by_length_empty():
    assert index_by_length([]) == {}


def test_index_by_length_last_wins():
    """Одинаковая длина — последнее слово перетирает предыдущее."""
    assert index_by_length(["one", "two", "six"]) == {3: "six"}


# --- 04 ---------------------------------------------------------------------
def test_unique_domains():
    assert unique_domains(["a@Mail.ru", "b@mail.ru", "oops"]) == {"mail.ru"}


def test_unique_domains_several():
    assert unique_domains(["a@x.com", "b@y.org"]) == {"x.com", "y.org"}


def test_unique_domains_empty():
    assert unique_domains([]) == set()


def test_unique_domains_ignores_strings_without_at():
    assert unique_domains(["nope", "also nope"]) == set()


# --- 05 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        ([[1, 2], [3], []], [1, 2, 3]),
        ([], []),
        ([[]], []),
        ([[1], [2], [3]], [1, 2, 3]),
    ],
)
def test_flatten(matrix, expected):
    assert flatten(matrix) == expected


def test_flatten_does_not_mutate_inner_lists():
    inner = [1, 2]
    flatten([inner])
    assert inner == [1, 2]


# --- 06 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [([3, 1, 2], (1, 3)), ([5], (5, 5)), ([], None), ([-4, -1], (-4, -1))],
)
def test_min_max(numbers, expected):
    assert min_max(numbers) == expected


def test_min_max_returns_tuple_not_list():
    """Кортеж, а не список: результат неизменяем и его можно распаковать."""
    result = min_max([1, 2])
    assert isinstance(result, tuple)
    low, high = result
    assert (low, high) == (1, 2)


# --- 07 ---------------------------------------------------------------------
def test_format_rows():
    assert format_rows([("яблоки", 3), ("хлеб", 1)]) == ["яблоки: 3", "хлеб: 1"]


def test_format_rows_empty():
    assert format_rows([]) == []


def test_format_rows_zero_count():
    assert format_rows([("вода", 0)]) == ["вода: 0"]


# --- 08 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "expected"),
    [([1, 2, 3], (1, [2, 3])), ([9], (9, [])), ([], (None, []))],
)
def test_head_and_rest(items, expected):
    assert head_and_rest(items) == expected


def test_head_and_rest_returns_list_for_rest():
    """`*rest` при распаковке даёт список, а не кортеж."""
    _, rest = head_and_rest([1, 2])
    assert isinstance(rest, list)


# --- 09 ---------------------------------------------------------------------
def test_merge_configs_overrides():
    assert merge_configs({"a": 1}, {"a": 2, "b": 3}) == {"a": 2, "b": 3}


def test_merge_configs_single():
    assert merge_configs({"a": 1}) == {"a": 1}


def test_merge_configs_many():
    assert merge_configs({"a": 1}, {"a": 2}, {"a": 3}) == {"a": 3}


def test_merge_configs_does_not_mutate_base():
    """Главная проверка задачи: `.update()` испортил бы аргумент вызывающего."""
    base = {"a": 1}
    merge_configs(base, {"b": 2})
    assert base == {"a": 1}


# --- 10 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (("a", "abc", "ab"), "abc"),
        (("ab", "cd"), "ab"),
        ((), None),
        (("one",), "one"),
    ],
)
def test_longest(words, expected):
    assert longest(*words) == expected


# --- 11 ---------------------------------------------------------------------
def test_call_twice_positional():
    assert call_twice(len, "abc") == [3, 3]


def test_call_twice_keyword():
    assert call_twice(sorted, [3, 1], reverse=True) == [[3, 1], [3, 1]]


def test_call_twice_no_args():
    assert call_twice(dict) == [{}, {}]


def test_call_twice_calls_exactly_twice():
    calls = []

    def spy(x):
        calls.append(x)
        return x

    assert call_twice(spy, 7) == [7, 7]
    assert calls == [7, 7]


# --- 12 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "prefix", "expected"),
    [
        (["ab", "cd"], "c", "cd"),
        (["ab"], "z", None),
        ([], "a", None),
        (["ab", "ac"], "a", "ab"),
    ],
)
def test_first_matching(items, prefix, expected):
    assert first_matching(items, prefix) == expected


def test_first_matching_is_lazy():
    """Главная проверка недели: решение не должно обходить всю последовательность.

    Здесь последовательность бесконечная. Список-comprehension повесит тест
    навсегда, генераторное выражение остановится на первом совпадении.
    """
    endless = (f"item-{n}" for n in count())
    assert first_matching(endless, "item-0") == "item-0"


# --- 13 ---------------------------------------------------------------------
def test_numbered_pairs():
    assert numbered_pairs(["a", "b"], [10, 20]) == ["1. a = 10", "2. b = 20"]


def test_numbered_pairs_truncates_to_shortest():
    assert numbered_pairs(["a", "b"], [10]) == ["1. a = 10"]


def test_numbered_pairs_empty():
    assert numbered_pairs([], []) == []


# --- 14 ---------------------------------------------------------------------
def test_top_by_score():
    assert top_by_score({"a": 5, "b": 9}, 1) == [("b", 9)]


def test_top_by_score_ties_sorted_by_name():
    assert top_by_score({"b": 5, "a": 5}, 2) == [("a", 5), ("b", 5)]


def test_top_by_score_limit_bigger_than_data():
    assert top_by_score({"a": 1}, 10) == [("a", 1)]


def test_top_by_score_zero_limit():
    assert top_by_score({"a": 1}, 0) == []


def test_top_by_score_full_order():
    scores = {"dima": 3, "anna": 7, "boris": 7, "kate": 1}
    assert top_by_score(scores, 4) == [
        ("anna", 7),
        ("boris", 7),
        ("dima", 3),
        ("kate", 1),
    ]


# --- 15 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("items", "size", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1], 5, [[1]]),
        ([], 2, []),
    ],
)
def test_chunks(items, size, expected):
    assert list(chunks(items, size)) == expected


def test_chunks_is_a_generator():
    """Функция с yield возвращает генератор: работа не начинается до первого next()."""
    result = chunks([1, 2], 1)
    assert not isinstance(result, list)
    assert next(iter(result)) == [1]


@pytest.mark.parametrize("size", [0, -1])
def test_chunks_rejects_bad_size(size):
    with pytest.raises(ValueError):
        list(chunks([1, 2], size))
