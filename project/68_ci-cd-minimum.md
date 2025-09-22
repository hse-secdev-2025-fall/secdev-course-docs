# Минимальный CI/CD - требования и эталон

## Цели
- «Зелёный CI как билет»: линтеры, форматирование, тесты, базовые хуки pre-commit.
- Required check `CI` в правилах ветки `main`.

## Эталонный workflow (сжатая версия)
```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
jobs:
  ci:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {{ python-version: '3.12' }}
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e .
      - name: Lint (ruff/black/isort)
        run: |
          ruff check .
          black --check .
          isort --check-only .
      - name: Tests
        run: pytest -q
      - name: Pre-commit
        run: pre-commit run --all-files
```

## Права и секреты
- Workflow permissions: `contents: read`. Повышать права - только при необходимости (комментарии в PR, релизы).

## Branch protection / Rulesets
- PR required, 1 approval, required checks = `CI`, запрет пушей в `main`.

## CD (позже)
- Теги `PXX` могут собирать артефакт/образ; доступ в окружения - через Environments с required reviewers.
