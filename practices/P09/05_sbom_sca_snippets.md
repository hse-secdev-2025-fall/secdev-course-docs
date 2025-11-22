# Сниппеты — P09 (SBOM & SCA)

## 1) Эскиз workflow `ci-sbom-sca.yml`

Полный шаблон в `practices/P09/06_templates/.github/workflows/ci-sbom-sca.yml`. Ключевые куски:

```yaml
name: Security - SBOM & SCA

on:
  workflow_dispatch:
  push:
    paths:
      - "**/*.py"
      - "requirements*.txt"
      - ".github/workflows/ci-sbom-sca.yml"

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  sbom_sca:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Ensure evidence dirs
        run: mkdir -p EVIDENCE/P09

      - name: Generate SBOM (Syft CycloneDX)
        run: |
          docker run --rm -v $PWD:/work -w /work anchore/syft:latest \
            packages dir:. -o cyclonedx-json > EVIDENCE/P09/sbom.json

      - name: SCA Scan (Grype)
        run: |
          set -e
          docker run --rm -v $PWD:/work -w /work anchore/grype:latest \
            sbom:/work/EVIDENCE/P09/sbom.json -o json > EVIDENCE/P09/sca_report.json
          echo "# SCA summary" > EVIDENCE/P09/sca_summary.md
          jq '[.matches[].vulnerability.severity] | group_by(.) | map({(.[0]): length}) | add' \
            EVIDENCE/P09/sca_report.json >> EVIDENCE/P09/sca_summary.md || true

      - name: Upload SBOM/SCA evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: P09_EVIDENCE
          path: EVIDENCE/P09
```

---

## 2) Локальные команды (аналог CI)

```bash
# SBOM (CycloneDX JSON)
docker run --rm -v $PWD:/work -w /work anchore/syft:latest \
  packages dir:. -o cyclonedx-json > EVIDENCE/P09/sbom.json

# SCA (Grype) по SBOM
docker run --rm -v $PWD:/work -w /work anchore/grype:latest \
  sbom:/work/EVIDENCE/P09/sbom.json -o json > EVIDENCE/P09/sca_report.json

# Краткая сводка по severity
echo "# SCA summary" > EVIDENCE/P09/sca_summary.md
jq '[.matches[].vulnerability.severity] | group_by(.) | map({(.[0]): length}) | add' \
  EVIDENCE/P09/sca_report.json >> EVIDENCE/P09/sca_summary.md || true
```

---

## 3) Мини-шаблон записи в DS/итоговый отчёт (SBOM & SCA)

```text
P09 - SBOM & SCA: настроен CI-workflow Security - SBOM & SCA.
Артефакты: EVIDENCE/P09/sbom.json, sca_report.json, sca_summary.md.
Инструменты: Syft (SBOM, CycloneDX), Grype (SCA). Actions: <URL успешного job>.
Кратко: выявлены N High/Medium уязвимостей; часть запланирована к фиксу/waivers.
```

---

## 4) Пример `policy/waivers.yml` (минимальный)

Подробности — в `project/69_sbom-vuln-mgmt.md`.

```yaml
# policy/waivers.yml — пример структуры waivers для SCA

waivers:
  - id: "CVE-2024-XXXX"
    package: "example-lib"
    version: "1.2.3"
    severity: "High"
    reason: "Транзитивная зависимость; нет фикса; код не включён в прод-путь."
    issue: "https://github.com/<org>/<repo>/issues/123"
    expires_at: "2025-12-31"
    approved_by: "tutor@example.org"
```

Идея: waiver — это **исключение на минимальный срок**, привязанное к конкретной уязвимости, пакету, Issue/PR.

---

## 5) Расширение: пороги и fail CI (опционально)

Если хотите подтянуться к «боевой» политике:

```yaml
      - name: Fail on high-severity vulns (demo)
        run: |
          high_count=$(jq '[.matches[].vulnerability.severity] | map(select(.=="High" or .=="Critical")) | length' EVIDENCE/P09/sca_report.json)
          echo "High/Critical count: $high_count"
          if [ "$high_count" -gt 0 ]; then
            echo "Found High/Critical vulnerabilities"
            exit 1
          fi
```

Использовать аккуратно — не ломайте себе разработку, если ещё не готовы триажить все находки.

---

## Файлы в `practices/P09/06_templates/`

### 1) `practices/P09/06_templates/.keep`

```text
# Пустой файл, чтобы сохранить каталог в git.
```

### 2) `practices/P09/06_templates/.github/workflows/ci-sbom-sca.yml`

```yaml
name: Security - SBOM & SCA

on:
  workflow_dispatch:
  push:
    paths:
      - "**/*.py"
      - "requirements*.txt"
      - ".github/workflows/ci-sbom-sca.yml"

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  sbom_sca:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Ensure evidence dirs
        run: mkdir -p EVIDENCE/P09

      - name: Generate SBOM (Syft CycloneDX)
        run: |
          docker run --rm -v $PWD:/work -w /work anchore/syft:latest \
            packages dir:. -o cyclonedx-json > EVIDENCE/P09/sbom.json

      - name: SCA Scan (Grype)
        run: |
          set -e
          docker run --rm -v $PWD:/work -w /work anchore/grype:latest \
            sbom:/work/EVIDENCE/P09/sbom.json -o json > EVIDENCE/P09/sca_report.json
          echo "# SCA summary" > EVIDENCE/P09/sca_summary.md
          jq '[.matches[].vulnerability.severity] | group_by(.) | map({(.[0]): length}) | add' \
            EVIDENCE/P09/sca_report.json >> EVIDENCE/P09/sca_summary.md || true

      - name: Upload SBOM/SCA evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: P09_EVIDENCE
          path: EVIDENCE/P09
```

### 3) `practices/P09/06_templates/policy/waivers.yml`

```yaml
# policy/waivers.yml — шаблон файла исключений для SBOM & SCA
# См. project/69_sbom-vuln-mgmt.md для описания политики.

waivers: []
# Пример записи:
# waivers:
#   - id: "CVE-2024-XXXX"
#     package: "example-lib"
#     version: "1.2.3"
#     severity: "High"
#     reason: "Транзитивная зависимость; нет фикса; компонент не в прод-цепочке."
#     issue: "https://github.com/<org>/<repo>/issues/123"
#     expires_at: "2025-12-31"
#     approved_by: "tutor@example.org"

