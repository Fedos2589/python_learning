"""Позволяет импортировать tasks.py напрямую при запуске из корня проекта.

Позже, на этапе 2, разберём нормальную структуру пакетов и этот файл уйдёт.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
