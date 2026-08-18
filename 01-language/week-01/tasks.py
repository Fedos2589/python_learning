"""Неделя 1. Базовый синтаксис.

Замени `raise NotImplementedError` на свою реализацию.
Проверка: uv run pytest 01-language/week-01 -v
"""


# --- Задача 01. Числа и f-strings -------------------------------------------
def format_price(amount: float, currency: str = "USD") -> str:
    """Вернуть цену, округлённую до 2 знаков, в виде '1234.50 USD'.

    format_price(1234.5) -> '1234.50 USD'
    format_price(10, 'EUR') -> '10.00 EUR'
    """
    return f"{amount:.2f} {currency}"


# --- Задача 02. Строки ------------------------------------------------------
def slugify(title: str) -> str:
    """Превратить заголовок в slug: нижний регистр, пробелы -> дефисы.

    Лишние пробелы по краям убрать, несколько пробелов подряд считать одним.

    slugify('  Hello   Full Stack World ') -> 'hello-full-stack-world'
    """
    return "-".join(title.strip().lower().split())


# --- Задача 03. Списки и циклы ----------------------------------------------
def count_words(text: str) -> int:
    """Посчитать количество слов в тексте. Пустая строка -> 0.

    count_words('раз два три') -> 3
    count_words('   ') -> 0
    """
    if not text:
        return 0
    return len(text.strip().split())


# --- Задача 04. Срезы -------------------------------------------------------
def middle_elements(items: list[int]) -> list[int]:
    """Вернуть список без первого и последнего элемента.

    Если элементов 2 или меньше — вернуть пустой список.

    middle_elements([1, 2, 3, 4, 5]) -> [2, 3, 4]
    middle_elements([1, 2]) -> []
    """
    le = len(items)
    if le < 3:
        return []
    return items[1:-1]


# --- Задача 05. Поиск в списке ----------------------------------------------
def second_largest(numbers: list[int]) -> int | None:
    """Вернуть второе по величине УНИКАЛЬНОЕ значение или None.

    second_largest([5, 1, 9, 9, 3]) -> 5
    second_largest([7, 7, 7]) -> None
    second_largest([]) -> None
    """
    unique_sorted = sorted(set(numbers))
    if len(unique_sorted) < 2:
        return None
    else:
        return unique_sorted[-2]


# --- Задача 06. Словари -----------------------------------------------------
def word_frequency(text: str) -> dict[str, int]:
    """Посчитать, сколько раз встречается каждое слово. Регистр игнорировать.

    word_frequency('a b A') -> {'a': 2, 'b': 1}
    """
    frequency = {}
    words = text.strip().lower().split()
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


# --- Задача 07. Словари: безопасный доступ ----------------------------------
def get_nested(data: dict, keys: list[str], default=None):
    """Достать значение по цепочке ключей, не падая на отсутствующих.

    Аналог optional chaining: data?.a?.b

    get_nested({'a': {'b': 1}}, ['a', 'b']) -> 1
    get_nested({'a': {}}, ['a', 'b'], 0) -> 0
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


# --- Задача 08. Множества ---------------------------------------------------
def common_tags(first: list[str], second: list[str]) -> list[str]:
    """Вернуть теги, встречающиеся в обоих списках, отсортированные по алфавиту.

    common_tags(['py', 'js', 'css'], ['js', 'py', 'go']) -> ['js', 'py']
    """
    return sorted(set(first) & set(second))


# --- Задача 09. Аргументы функции -------------------------------------------
def add_item(item: str, basket: list[str] | None = None) -> list[str]:
    """Добавить элемент в корзину и вернуть её.

    Если корзина не передана — создать НОВУЮ. Важно: два вызова без корзины
    должны вернуть независимые списки. Это та самая ловушка с изменяемым
    аргументом по умолчанию.

    add_item('x') -> ['x']
    add_item('y') -> ['y']   # не ['x', 'y']
    """
    if not basket:
        return [item]
    else:
        basket.append(item)
        return basket


# --- Задача 10. Именованные аргументы ---------------------------------------
def build_url(base: str, **params) -> str:
    """Собрать URL с query-параметрами, отсортированными по имени ключа.

    Если параметров нет — вернуть base как есть.

    build_url('/api', page=2, limit=10) -> '/api?limit=10&page=2'
    build_url('/api') -> '/api'
    """
    if not params:
        return base
    else:
        query = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
        return f"{base}?{query}"


# --- Задача 11. Truthiness --------------------------------------------------
def first_non_empty(values: list) -> object | None:
    """Вернуть первое «истинное» значение из списка, иначе None.

    Помни: 0, '', [], {} и None — ложные.

    first_non_empty([0, '', None, 'ok', 'no']) -> 'ok'
    first_non_empty([0, '']) -> None
    """
    for value in values:
        if value:
            return value


# --- Задача 12. None vs False -----------------------------------------------
def describe_flag(flag: bool | None) -> str:
    """Различить три состояния флага.

    None -> 'не задан'
    True -> 'включён'
    False -> 'выключен'

    Проверь себя: почему `if not flag` здесь не сработает?
    """
    if flag is None:
        return "не задан"
    elif flag:
        return "включён"
    else:
        return "выключен"
