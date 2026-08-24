"""Неделя 2. Comprehensions, кортежи, множества, распаковка, args/kwargs.

Замени `raise NotImplementedError` на свою реализацию.
Проверка: uv run pytest 01-language/week-02 -v

Правило недели: там, где на прошлой неделе ты писал цикл с `append`,
почти всегда нужен comprehension. Но не везде — задачи 07 и 12 покажут где.
"""

from collections.abc import Callable, Iterable, Iterator


# --- Задача 01. List comprehension ------------------------------------------
def squares(numbers: list[int]) -> list[int]:
    """Вернуть квадраты чисел.

    Аналог `numbers.map(n => n ** 2)` из JS, но синтаксис читается наоборот:
    сначала что делаем с элементом, потом откуда его берём.

    squares([1, 2, 3]) -> [1, 4, 9]
    squares([]) -> []
    """
    raise NotImplementedError


# --- Задача 02. Comprehension с фильтром ------------------------------------
def even_lengths(words: list[str]) -> list[int]:
    """Вернуть длины только тех слов, у которых длина чётная.

    Это `.filter().map()` в одном выражении, без промежуточного списка.
    Порядок частей: выражение -> for -> if.

    even_lengths(['ab', 'a', 'abcd']) -> [2, 4]
    """
    raise NotImplementedError


# --- Задача 03. Dict comprehension ------------------------------------------
def index_by_length(words: list[str]) -> dict[int, str]:
    """Собрать словарь {длина слова: слово}.

    Если несколько слов одной длины — победит ПОСЛЕДНЕЕ. Так работает
    присваивание в словарь, и это не баг: подумай, почему так, прежде чем
    смотреть в тест.

    index_by_length(['a', 'bb', 'cc']) -> {1: 'a', 2: 'cc'}
    """
    raise NotImplementedError


# --- Задача 04. Set comprehension -------------------------------------------
def unique_domains(emails: list[str]) -> set[str]:
    """Вернуть множество домённых частей адресов, в нижнем регистре.

    Адреса приходят как есть, с любым регистром. Строки без '@' игнорировать.

    unique_domains(['a@Mail.ru', 'b@mail.ru', 'oops']) -> {'mail.ru'}
    """
    raise NotImplementedError


# --- Задача 05. Вложенный comprehension -------------------------------------
def flatten(matrix: list[list[int]]) -> list[int]:
    """Развернуть список списков в плоский список.

    Порядок `for` такой же, как во вложенном цикле: сначала внешний, потом
    внутренний. Если написать наоборот — получишь NameError.

    flatten([[1, 2], [3], []]) -> [1, 2, 3]
    """
    raise NotImplementedError


# --- Задача 06. Кортежи как возвращаемое значение ---------------------------
def min_max(numbers: list[int]) -> tuple[int, int] | None:
    """Вернуть пару (минимум, максимум) или None для пустого списка.

    Кортеж — это способ вернуть несколько значений. В JS ты бы вернул массив
    или объект; в Python возвращают кортеж и распаковывают на месте:
    `low, high = min_max(nums)`.

    min_max([3, 1, 2]) -> (1, 3)
    min_max([5]) -> (5, 5)
    min_max([]) -> None
    """
    raise NotImplementedError


# --- Задача 07. Распаковка в цикле ------------------------------------------
def format_rows(rows: list[tuple[str, int]]) -> list[str]:
    """Превратить пары (имя, количество) в строки 'имя: количество'.

    Распаковывай кортеж прямо в `for`: `for name, count in rows`.
    Обращение через `row[0]` и `row[1]` считается непрочитанной задачей.

    format_rows([('яблоки', 3), ('хлеб', 1)]) -> ['яблоки: 3', 'хлеб: 1']
    """
    raise NotImplementedError


# --- Задача 08. Звёздчатая распаковка ---------------------------------------
def head_and_rest(items: list[int]) -> tuple[int | None, list[int]]:
    """Разделить список на первый элемент и всё остальное.

    Аналог `const [head, ...rest] = items`. Синтаксис: `first, *rest = items`.
    Обрати внимание: `rest` всегда список, даже если элементов не осталось.
    На пустом списке распаковка бросит ValueError — обработай этот случай.

    head_and_rest([1, 2, 3]) -> (1, [2, 3])
    head_and_rest([9]) -> (9, [])
    head_and_rest([]) -> (None, [])
    """
    raise NotImplementedError


# --- Задача 09. Распаковка словарей -----------------------------------------
def merge_configs(
    base: dict[str, object], *overrides: dict[str, object]
) -> dict[str, object]:
    """Слить словари: каждый следующий перекрывает предыдущие.

    Аналог `{...base, ...a, ...b}`. В Python это `{**base, **a}` или `a | b`
    (Python 3.9+). Исходные словари менять нельзя — возвращай новый.

    merge_configs({'a': 1}, {'a': 2, 'b': 3}) -> {'a': 2, 'b': 3}
    merge_configs({'a': 1}) -> {'a': 1}
    """
    raise NotImplementedError


# --- Задача 10. *args -------------------------------------------------------
def longest(*words: str) -> str | None:
    """Вернуть самое длинное слово. При равной длине — то, что встретилось раньше.

    `*words` собирает позиционные аргументы в КОРТЕЖ. Вызовов без аргументов
    никто не запрещал: `longest()` -> None.

    longest('a', 'abc', 'ab') -> 'abc'
    longest('ab', 'cd') -> 'ab'
    longest() -> None
    """
    raise NotImplementedError


# --- Задача 11. **kwargs и прокидывание аргументов --------------------------
def call_twice(
    func: Callable[..., object], *args: object, **kwargs: object
) -> list[object]:
    """Вызвать функцию дважды с теми же аргументами и вернуть оба результата.

    Здесь `*args`/`**kwargs` работают в обе стороны: на входе СОБИРАЮТ
    аргументы, при вызове `func(*args, **kwargs)` — РАСПАКОВЫВАЮТ обратно.
    Одна и та же звёздочка, два противоположных смысла — по месту написания.

    call_twice(len, 'abc') -> [3, 3]
    """
    raise NotImplementedError


# --- Задача 12. Генераторное выражение --------------------------------------
def first_matching(items: Iterable[str], prefix: str) -> str | None:
    """Вернуть первый элемент, начинающийся с prefix, или None.

    Здесь comprehension в квадратных скобках — плохое решение: он обойдёт ВСЮ
    последовательность, даже если ответ был первым элементом. Нужны круглые
    скобки — генераторное выражение, оно считает элементы по одному:
    `next((x for x in items if ...), None)`.

    Разница видна на бесконечной последовательности — в тестах есть такой случай.

    first_matching(['ab', 'cd'], 'c') -> 'cd'
    first_matching(['ab'], 'z') -> None
    """
    raise NotImplementedError


# --- Задача 13. zip и enumerate ---------------------------------------------
def numbered_pairs(names: list[str], scores: list[int]) -> list[str]:
    """Собрать строки вида '1. имя = очки', нумерация с единицы.

    `zip` склеивает две последовательности в пары и молча обрезает по короткой.
    `enumerate(x, start=1)` даёт индекс — вручную счётчик не веди.

    numbered_pairs(['a', 'b'], [10, 20]) -> ['1. a = 10', '2. b = 20']
    numbered_pairs(['a', 'b'], [10]) -> ['1. a = 10']
    """
    raise NotImplementedError


# --- Задача 14. sorted с ключом ---------------------------------------------
def top_by_score(scores: dict[str, int], limit: int) -> list[tuple[str, int]]:
    """Вернуть limit пар (имя, очки), отсортированных по убыванию очков.

    При равных очках — по имени по алфавиту. Подсказка: ключ сортировки может
    быть кортежем, а минус перед числом переворачивает порядок для этого поля.

    top_by_score({'a': 5, 'b': 9}, 1) -> [('b', 9)]
    top_by_score({'b': 5, 'a': 5}, 2) -> [('a', 5), ('b', 5)]
    """
    raise NotImplementedError


# --- Задача 15. Генератор через yield ---------------------------------------
def chunks(items: list[int], size: int) -> Iterator[list[int]]:
    """Порезать список на куски по size элементов. Последний кусок может быть короче.

    Функция с `yield` возвращает генератор: она не считает всё сразу, а отдаёт
    куски по запросу. Ближайший аналог в JS — `function*`.
    При size <= 0 брось ValueError с любым сообщением.

    list(chunks([1, 2, 3, 4, 5], 2)) -> [[1, 2], [3, 4], [5]]
    """
    raise NotImplementedError
