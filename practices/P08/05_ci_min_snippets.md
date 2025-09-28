# Сниппеты — P08 (CI/CD Minimal)

## 1) Минимальный GitHub Actions `ci.yml`
```yaml
name: CI (minimal)

on:
  push:
  pull_request:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install ruff black isort pytest

      - name: Lint
        run: |
          ruff check .
          black --check .
          isort --check-only .

      - name: Tests
        run: |
          mkdir -p reports
          pytest -q --maxfail=1 --disable-warnings --junitxml=reports/junit.xml

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: reports
          path: reports/**
```

## 2) Бейдж в README.md
```
![CI](https://github.com/<org>/<repo>/actions/workflows/ci.yml/badge.svg)
```

## 3) Советы по стабильности
- Фиксируйте **мажорные версии** экшенов (`@v4`/`@v5`) и держите `timeout-minutes` разумным.
- Держите зависимости и шаги минимальными — это «minimal», не тащите лишнего.
- Для приватных репозиториев и форков учитывайте правила секрета: на PR из форка секреты не доступны.
```
