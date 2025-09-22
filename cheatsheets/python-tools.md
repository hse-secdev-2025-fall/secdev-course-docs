# Шпаргалка 3 — Python‑инструменты качества

Общий порядок локальных проверок: **ruff → black → isort → pytest**, а **pre-commit** запускает это автоматически при коммите.

## Быстрый старт
```bash
python -m pip install --upgrade pip
pip install ruff black isort pytest pre-commit

pre-commit install
pre-commit run --all-files   # один прогон по всем файлам
ruff check --fix .
black .
isort .
pytest -q
```

---

## Ruff — линтер (быстрый, с автофиксом)
**Зачем:** находит ошибки/антипаттерны/несоответствия стилю.

Команды:
```bash
ruff check .
ruff check --fix .      # починить по возможности
```

Мини‑конфиг (`ruff.toml` или в `pyproject.toml`):
```toml
# ruff.toml
line-length = 100
target-version = "py311"
select = ["E","F","I","UP","B","W"]
ignore = ["E203","E501"]  # если используете black
```

## Black — автоформаттер
**Зачем:** единый стиль кода «без споров».

Команды:
```bash
black .
black --check .    # только проверка (для CI)
```

Мини‑конфиг (`pyproject.toml`):
```toml
[tool.black]
line-length = 100
target-version = ["py311"]
```

## Isort — сортировка импортов
**Зачем:** упорядочивает импорты по группам.

Команды:
```bash
isort .
isort --check-only .   # проверка без изменений (для CI)
```

Мини‑конфиг (`pyproject.toml`):
```toml
[tool.isort]
profile = "black"
line_length = 100
```

## Pytest — тесты
**Зачем:** проверка функциональности и регрессий.

Команды (частые):
```bash
pytest -q                 # все тесты
pytest tests/test_api.py  # конкретный файл
pytest -k login           # по подстроке имени
pytest -m "slow"          # по маркеру @pytest.mark.slow
```

Мини‑конфиг (`pytest.ini` или `pyproject.toml`):
```ini
[pytest]
addopts = -q
testpaths = tests
pythonpath = app
filterwarnings = ignore::DeprecationWarning
```

## Pre-commit — проверки при коммите
**Зачем:** ловит проблемы **до** попадания в репозиторий/CI.

Команды:
```bash
pre-commit install
pre-commit run --all-files
pre-commit autoupdate
```

Мини‑конфиг (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
      - id: check-merge-conflict
      - id: check-json
      - id: check-yaml
      - id: detect-private-key
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Как читать ошибки pre-commit
Инструмент печатает, какая проверка упала и где (файл/строка). Обычно помогает:
```bash
ruff check --fix . && black . && isort .
git add -A && git commit -m "style: fix lint & format"
```
