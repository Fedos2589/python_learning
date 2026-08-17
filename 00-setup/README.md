# Этап 0. Окружение (~40 минут)

Цель: чтобы дальше инструменты не отвлекали. Аналогии с фронтендом — в скобках.

## 1. Устанавливаем `uv`

`uv` — менеджер версий Python, пакетов и виртуальных окружений в одном (примерно
как `pnpm` + `nvm`). Быстрый, современный, стандарт де-факто в 2026.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Перезапусти терминал и проверь:

```bash
uv --version
```

## 2. Ставим Python 3.12

Системный Python на macOS трогать не надо — он нужен самой системе.

```bash
uv python install 3.12
uv python list
```

## 3. Создаём окружение проекта

Из корня `python-learning`:

```bash
uv init --python 3.12
uv add --dev pytest ruff mypy
```

Что произошло:

| Файл | Аналог из JS-мира |
|------|-------------------|
| `pyproject.toml` | `package.json` |
| `uv.lock` | `pnpm-lock.yaml` |
| `.venv/` | `node_modules/` |

Дальше всё запускаем через `uv run` — он сам подхватывает окружение
(как `npx` / `pnpm exec`).

## 4. Проверяем

```bash
uv run python -c "import sys; print(sys.version)"
uv run pytest --version
uv run ruff --version
```

## 5. VS Code

Установить расширения:

- **Python** (Microsoft)
- **Pylance** — типы и автодополнение
- **Ruff** (Astral) — линт и форматирование

Затем `Cmd+Shift+P` → «Python: Select Interpreter» → выбрать `.venv` из проекта.

Создай `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff",
  "python.testing.pytestEnabled": true,
  "python.analysis.typeCheckingMode": "basic"
}
```

## 6. Отладчик

Важное правило на все 32 недели: **отлаживаем точками останова, а не `print`.**
Ты это уже умеешь в DevTools — здесь то же самое.

Проверка: поставь точку останова в любом файле, нажми F5, убедись, что
выполнение остановилось и переменные видны в панели.

## 7. Git

```bash
git init
git add .
git commit -m "chore: настроил окружение"
```

Коммит после каждой темы. К концу пути история git — часть портфолио.

---

## Чек-лист

- [ ] `uv --version` работает
- [ ] Python 3.12 установлен через uv
- [ ] `uv run pytest --version` работает
- [ ] VS Code видит интерпретатор из `.venv`
- [ ] Точка останова срабатывает
- [ ] Первый коммит сделан

Отметь пункты в `PROGRESS.md` и переходи к `01-language/week-01/README.md`.
