# Сниппеты — P10 (SAST & Secrets)

## 1) Эскиз workflow `ci-sast-secrets.yml`

Полный шаблон — в `practices/P10/06_templates/.github/workflows/ci-sast-secrets.yml`. Ключевая идея:

```yaml
name: Security - SAST & Secrets

on:
  workflow_dispatch:
  push:
    paths:
      - "**/*.py"
      - "security/semgrep/**"
      - "security/.gitleaks.toml"
      - ".github/workflows/ci-sast-secrets.yml"

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  sast_secrets:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Ensure evidence dirs
        run: mkdir -p EVIDENCE/P10

      - name: Semgrep CI (SARIF)
        run: |
          docker run --rm -v $PWD:/src returntocorp/semgrep:latest \
            semgrep ci --config p/ci --config /src/security/semgrep/rules.yml \
              --sarif --output /src/EVIDENCE/P10/semgrep.sarif --metrics=off || true

      - name: Gitleaks detect
        run: |
          docker run --rm -v $PWD:/repo zricethezav/gitleaks:latest \
            detect --no-banner --config=/repo/security/.gitleaks.toml \
              --source=/repo --report-format=json \
              --report-path=/repo/EVIDENCE/P10/gitleaks.json || true

      - name: Upload SAST & Secrets evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: P10_EVIDENCE
          path: EVIDENCE/P10
```

---

## 2) Локальные команды (Semgrep + Gitleaks)

```bash
# Semgrep (SARIF)
docker run --rm -v $PWD:/src returntocorp/semgrep:latest \
  semgrep ci --config p/ci --config /src/security/semgrep/rules.yml \
    --sarif --output /src/EVIDENCE/P10/semgrep.sarif --metrics=off || true

# Gitleaks (JSON)
docker run --rm -v $PWD:/repo zricethezav/gitleaks:latest \
  detect --no-banner --config=/repo/security/.gitleaks.toml \
    --source=/repo --report-format=json \
    --report-path=/repo/EVIDENCE/P10/gitleaks.json || true
```

---

## 3) Мини-шаблон записи в DS/итоговый отчёт (SAST & Secrets)

```text
P10 - SAST & Secrets: настроены Semgrep (SARIF) и Gitleaks (JSON) в CI.
Артефакты: EVIDENCE/P10/semgrep.sarif, EVIDENCE/P10/gitleaks.json.
Actions: <ссылка на успешный job>. Кратко: рассмотрены N findings Semgrep и M предупреждений Gitleaks,
часть заведена в backlog / исправлена, ложноположительные внесены в allowlist.
```

---

## 4) Минимальный шаблон правил Semgrep (`security/semgrep/rules.yml`)

```yaml
rules:
  - id: py-unsafe-html-echo
    languages: [python]
    message: "Потенциально небезопасный вывод пользовательских данных в HTMLResponse"
    severity: WARNING
    patterns:
      - pattern: |
          HTMLResponse(f"...{$X}...")
    metadata:
      category: security
      cwe: "CWE-79: Cross-site Scripting"
```

Это просто пример «своего» правила; вы можете заменить его чем-то более релевантным вашему коду.

---

## 5) Минимальный шаблон Gitleaks (`security/.gitleaks.toml`)

```toml
title = "course default gitleaks config"

[extend]
# Используем встроенные правила по умолчанию

[allowlist]
description = "ignore non-sensitive patterns"
paths = [
  "EVIDENCE/",   # отчёты и артефакты
]
commits = []
regexes = [
  '''TEST_SECRET_DO_NOT_USE''',
]
```

Начните с такой заготовки и постепенно добавляйте реальные allowlist-паттерны по мере появления ложных срабатываний.
