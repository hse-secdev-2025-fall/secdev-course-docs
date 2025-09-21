# CI snippets — P01

Минимальный workflow (GitHub Actions):

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt || true
          pip install -r requirements-dev.txt || true
          pip install ruff black isort pytest pre-commit
      - name: Lint & format
        run: |
          ruff check --output-format=github .
          black --check .
          isort --check-only .
      - name: Tests
        run: pytest -q
      - name: Pre-commit (all files)
        run: pre-commit run --all-files --show-diff-on-failure
```

**Важно:** добавь required-check `CI / build` в защите ветки `main`.