"""Сборка отчёта. Модуль 3 из 3.

Этот модуль ничего не вычисляет сам — он вызывает `parsing` и `stats` и
превращает результат в текст. Тонкий слой поверх логики: ровно так же будет
устроен слой роутов в FastAPI на этапе 3.

Импорты из `stats` тебе придётся дописать сам — какие именно, решишь, когда
будешь писать `build_report`. Это часть темы «модули»: импортируем то, что
используем, и ничего лишнего. Ruff подскажет, если импортируешь неиспользуемое.
"""

import sys
from collections.abc import Sequence
from pathlib import Path

from parsing import LogRecord, count_valid_and_broken, parse_lines


# --- Задача 10 --------------------------------------------------------------
def build_report(records: Sequence[LogRecord]) -> str:
    """Собрать текстовый отчёт по логу.

    Формат — ровно такой, тест сверяет построчно:

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
          /api/search: 210.5 мс
          /api/users: 45.0 мс

    Правила:
      - коды ответов перечислять по возрастанию класса
      - процент ошибок — одна цифра после запятой; `f'{value:.1%}'` сделает
        это сам, вместе со знаком процента — посмотри, как работает формат
      - среднее время — одна цифра после запятой
      - отступ во вложенных строках — два пробела
      - для пустого лога вернуть ровно 'Лог пуст'
      - строки склеивать через '\\n', в конце перевода строки нет

    Собирай список строк, потом `'\\n'.join(lines)`. Складывать строки в цикле
    через `+=` в Python дорого: строки неизменяемы, каждое сложение создаёт
    новую. Это заметно на тысячах итераций.
    """
    raise NotImplementedError


def main() -> int:
    """Точка входа: `uv run python 01-language/week-02/parser/report.py access-log.csv`.

    Этот код уже написан — читать его полезно, менять не нужно. `pathlib` и работа
    с файлами — тема недели 4, пока просто прими как данность.
    """
    args = sys.argv[1:]
    if not args:
        print("Использование: report.py <путь-до-лога>", file=sys.stderr)
        return 1

    path = Path(args[0])
    try:
        with path.open(encoding="utf-8") as handle:
            lines = handle.readlines()
    except FileNotFoundError:
        print(f"Файл не найден: {path}", file=sys.stderr)
        return 1

    _valid, broken = count_valid_and_broken(lines)
    records = list(parse_lines(lines))

    print(build_report(records))
    if broken:
        print(f"\nБитых строк пропущено: {broken}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
