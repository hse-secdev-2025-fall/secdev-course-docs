# CI snippets — P01

Минимальный workflow `CI` (GitHub Actions):

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff black isort pytest pre-commit
      - name: Lint & format
        run: |
          ruff check --output-format=github .
          black --check .
          isort --check-only .
      - name: Tests
        run: pytest -q
      - name: Pre-commit (all files)
        run: pre-commit run --all-files
```

**Required check:** `CI` должен быть включён в защите ветки `main` (см. `scripts/gh/protect-main.sh`).
