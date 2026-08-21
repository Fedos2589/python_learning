"""Неделя 1, добор. Те же темы, другие задачи.

Ни одной новой конструкции здесь нет — только то, что уже было в `tasks.py`:
строки, срезы, списки, словари, множества, аргументы функций, truthiness,
`None`. Смысл в том, чтобы синтаксис уходил из головы в пальцы.

Замени `raise NotImplementedError` на свою реализацию.
Проверка: uv run pytest 01-language/week-01/test_drills.py -v

Как работать:
1. Реализуй по одной функции, после каждой прогоняй тесты.
2. В документацию по синтаксису не заглядывай, пока не застрял на 10 минут.
   Забыл, как называется метод — это нормально, вспоминай, а не гугли сразу.
3. Четыре задачи (06, 12, 14, 15) — повторный заход на грабли, на которых ты
   спотыкался в `tasks.py`. Они специально выглядят иначе, а ломаются так же.
"""


# --- 01. Строки: разбор и сборка ---------------------------------------------
def initials(full_name: str) -> str:
    """Собрать инициалы из полного имени, в верхнем регистре, через точку.

    Лишние пробелы игнорировать. Точка ставится после каждой буквы.

    initials('Иван Петров') -> 'И.П.'
    initials('  анна   мария петрова ') -> 'А.М.П.'
    initials('') -> ''
    """
    return "".join(x[0].upper() + "." for x in full_name.strip().split())


# --- 02. Числа и форматирование ----------------------------------------------
def format_duration(seconds: int) -> str:
    """Перевести секунды в 'минуты:секунды', секунды всегда двумя цифрами.

    Считаем, что seconds >= 0. Минуты не ограничены 59 — 3600 это '60:00'.
    Подсказка: `divmod(a, b)` возвращает кортеж (частное, остаток) за один
    вызов. Для дополнения нулём есть формат `f'{n:02d}'`.

    format_duration(65) -> '1:05'
    format_duration(7) -> '0:07'
    format_duration(0) -> '0:00'
    """
    values = divmod(seconds, 60)
    return f"{values[0]}:{values[1]:02d}"


# --- 03. Строки: сравнение ----------------------------------------------------
def is_palindrome(text: str) -> bool:
    """Проверить, читается ли текст одинаково в обе стороны.

    Регистр и пробелы игнорировать, остальные символы учитывать.
    Пустая строка — палиндром.

    Подсказка: перевернуть строку можно срезом с отрицательным шагом.

    is_palindrome('А роза упала на лапу Азора') -> True
    is_palindrome('Привет') -> False
    """
    plain = text.replace(" ", "").lower()
    return plain == plain[::-1]


# --- 04. Срезы ----------------------------------------------------------------
def truncate(text: str, limit: int) -> str:
    """Обрезать текст до limit символов, добавив '…' если что-то отрезали.

    Многоточие входит в лимит: результат никогда не длиннее limit.
    Если текст короче или равен лимиту — вернуть как есть.
    limit <= 0 -> пустая строка.

    truncate('hello', 5) -> 'hello'
    truncate('hello world', 8) -> 'hello w…'
    truncate('hello', 0) -> ''
    """
    if limit <= 0:
        return ""
    text_len = len(text)
    if text_len <= limit:
        return text
    return f"{text[0 : limit - 1]}…"


# --- 05. Строки: поиск разделителя --------------------------------------------
def mask_email(email: str) -> str:
    """Скрыть середину локальной части адреса, оставив первый и последний символ.

    Домен не трогать. Если локальная часть короче трёх символов — оставить как
    есть. Строку без '@' вернуть без изменений.

    mask_email('alexander@gmail.com') -> 'a***r@gmail.com'
    mask_email('ab@mail.ru') -> 'ab@mail.ru'
    mask_email('не адрес') -> 'не адрес'
    """
    if "@" not in email:
        return "не адрес"
    parts = email.split("@")
    if len(parts[0]) < 3:
        return email
    return f"{parts[0][0]}***{parts[0][-1]}@{parts[1]}"


# --- 06. Срезы и деление по модулю -------------------------------------------
def rotate(items: list[int], step: int) -> list[int]:
    """Сдвинуть список влево на step позиций, по кругу.

    step может быть больше длины списка — тогда сдвиг «по кругу» повторяется.
    Отрицательный step сдвигает вправо.

    Осторожно: `step % len(items)` на пустом списке даст ZeroDivisionError.
    Исходный список менять нельзя.

    rotate([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]
    rotate([1, 2, 3], 4) -> [2, 3, 1]
    rotate([1, 2, 3], -1) -> [3, 1, 2]
    rotate([], 3) -> []
    """
    items_len = len(items)
    if items_len < 1:
        return []
    cur_step = step % items_len
    print(step, cur_step, items[cur_step:items_len], items[0:cur_step])
    if cur_step < 0:
        return items[0:cur_step] + items[cur_step:items_len]
    return items[cur_step:items_len] + items[0:cur_step]


# --- 07. Списки и накопление --------------------------------------------------
def running_total(numbers: list[int]) -> list[int]:
    """Вернуть список накопительных сумм.

    На каждом шаге — сумма всех элементов с начала до текущего включительно.

    running_total([1, 2, 3]) -> [1, 3, 6]
    running_total([]) -> []
    running_total([5]) -> [5]
    """
    if len(numbers) < 1:
        return []
    res = []
    cur = 0
    for number in numbers:
        cur += number
        res.append(cur)
    return res


# --- 08. Сортировка с ключом --------------------------------------------------
def sort_by_length(words: list[str]) -> list[str]:
    """Отсортировать слова по длине, от коротких к длинным.

    Слова одинаковой длины должны сохранить исходный порядок. Специально ничего
    для этого делать не надо: сортировка в Python стабильная. Проверь, что
    понимаешь, что это значит — в тестах есть такой случай.

    Исходный список менять нельзя — вернуть новый.

    sort_by_length(['bbb', 'a', 'cc']) -> ['a', 'cc', 'bbb']
    """
    return sorted(words, key=len)


# --- 09. Словари: разворот ----------------------------------------------------
def invert(mapping: dict[str, int]) -> dict[int, str]:
    """Поменять ключи и значения местами.

    Если одно значение встречается дважды — победит последняя пара.

    invert({'a': 1, 'b': 2}) -> {1: 'a', 2: 'b'}
    invert({}) -> {}
    """
    res = {}
    for key, value in mapping.items():
        res[value] = key
    return res


# --- 10. Словари: группировка -------------------------------------------------
def count_by_first_letter(words: list[str]) -> dict[str, int]:
    """Посчитать, сколько слов начинается с каждой буквы. Регистр игнорировать.

    Пустые строки пропускать.

    count_by_first_letter(['Apple', 'avocado', 'beet']) -> {'a': 2, 'b': 1}
    count_by_first_letter(['', 'x']) -> {'x': 1}
    """
    res = {}
    for word in words:
        if not word:
            continue
        letter = word[0].lower()
        res[letter] = res.get(letter, 0) + 1
    return res


# --- 11. Множества ------------------------------------------------------------
def only_in_one(first: list[str], second: list[str]) -> list[str]:
    """Вернуть теги, которые есть РОВНО в одном из списков, по алфавиту.

    То есть всё, кроме общих. У множеств для этого есть отдельная операция —
    найди её сам, через `dir(set())` или документацию.

    only_in_one(['py', 'js'], ['js', 'go']) -> ['go', 'py']
    only_in_one(['py'], ['py']) -> []
    """
    return sorted(set(first) ^ set(second))


# --- 12. Изменяемый аргумент по умолчанию ------------------------------------
def register(name: str, registry: dict[str, int] | None = None) -> dict[str, int]:
    """Отметить имя в реестре: если оно уже есть — увеличить счётчик.

    Если реестр не передан — создать новый. Два вызова без реестра должны
    вернуть независимые словари.

    Отдельно: если передан ПУСТОЙ словарь, наполнить именно его, а не подменить
    новым. Ровно на этом ты споткнулся в `add_item` — проверка на «пустое»
    вместо проверки на «отсутствует».

    register('ted') -> {'ted': 1}
    register('ted', {'ted': 1}) -> {'ted': 2}
    """
    reg = registry
    if reg is None:
        reg = {}
    reg[name] = reg.get(name, 0) + 1
    return reg


# --- 13. **kwargs -------------------------------------------------------------
def describe_user(**fields: object) -> str:
    """Собрать описание пользователя: 'ключ=значение', пары через '; '.

    Ключи отсортированы по алфавиту. Без аргументов — пустая строка.

    describe_user(role='dev', name='Ted') -> 'name=Ted; role=dev'
    describe_user() -> ''
    """
    if not fields:
        return ""
    return "; ".join(f"{key}={value}" for key, value in sorted(fields.items()))


# --- 14. None против ложных значений -----------------------------------------
def without_none(values: list[object]) -> list[object]:
    """Убрать из списка ТОЛЬКО None. Ноль, пустая строка и пустой список остаются.

    Здесь `if value` не подходит — он выбросит и ноль, и пустую строку.
    Нужна проверка именно на None.

    without_none([0, '', None, [], 1]) -> [0, '', [], 1]
    without_none([None, None]) -> []
    """
    return list(filter(lambda x: x is not None, values))


# --- 15. Три состояния --------------------------------------------------------
def resolve_flag(local: bool | None, default: bool) -> bool:
    """Вернуть local, если он задан, иначе default.

    `None` значит «не задан» и должен уступить значению по умолчанию.
    `False` — это заданное значение, и оно должно победить `default=True`.

    resolve_flag(None, True) -> True
    resolve_flag(False, True) -> False
    """
    if local is None:
        return default
    return local


# --- 16. Поиск с явным возвратом ---------------------------------------------
def find_index(items: list[str], target: str) -> int | None:
    """Вернуть индекс первого вхождения target или None, если его нет.

    Метод `.index()` бросает ValueError, когда элемента нет, — здесь он не
    подходит. Пиши цикл и не забудь явный `return None` в конце.

    find_index(['a', 'b', 'a'], 'a') -> 0
    find_index(['a'], 'z') -> None
    """
    for index, item in enumerate(items):
        if item == target:
            return index
    return None
