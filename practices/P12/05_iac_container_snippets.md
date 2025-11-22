# Сниппеты — P12 (IaC & Container Security)

## 1) Локальный запуск Hadolint

```bash
# Проверка Dockerfile в корне проекта
docker run --rm -i hadolint/hadolint < Dockerfile \
  | tee hadolint_output.txt

# Вариант с отчётом в JSON (пример)
docker run --rm -v $PWD:/work hadolint/hadolint \
  hadolint -f json /work/Dockerfile > EVIDENCE/P12/hadolint_report.json
```

---

## 2) Локальный запуск Checkov

```bash
# Сканирование каталога iac/ (или k8s/)
docker run --rm -v $PWD:/work bridgecrew/checkov \
  -d /work/iac \
  -o json \
  --compact > EVIDENCE/P12/checkov_report.json
```

---

## 3) Локальный запуск Trivy по образу

```bash
# Сборка образа (пример)
docker build -t myapp:local .

# Сканирование образа
docker run --rm -v $PWD:/work aquasec/trivy \
  image myapp:local \
    --format json \
    --output /work/EVIDENCE/P12/trivy_report.json
```

---

## 4) Мини-шаблон `security/hadolint.yaml`

```yaml
# Пример минимальной конфигурации Hadolint
ignored:
  - DL3008   # пример: игнорировать конкретное правило (при необходимости)
  - DL3018
```

---

## 5) Мини-шаблон `security/checkov.yaml`

```yaml
# Мини-конфиг Checkov (можно расширять)
quiet: false
compact: true
framework:
  - kubernetes
  - terraform
  - dockerfile
skip-check:
  # Список check_id, которые вы сознательно пропускаете
  # - CKV_K8S_9999
```

---

## 6) Мини-шаблон `security/trivy.yaml`

```yaml
# Пример конфига Trivy (опционально)
scan:
  scanners:
    - vuln
    - config
  severity:
    - CRITICAL
    - HIGH
format: "json"
```

---

## 7) Мини-шаблон для описания в PR

```text
P12 - IaC & Container Security

Hadolint: EVIDENCE/P12/hadolint_report.json (Dockerfile, основные замечания)
Checkov: EVIDENCE/P12/checkov_report.json (iac/, K8s/TF)
Trivy: EVIDENCE/P12/trivy_report.json (образ <имя:тег>)

Applied hardening:
- Dockerfile: убран latest, добавлен non-root user
- IaC: ослаблен доступ/привилегии, ускорен старт/healthcheck
```
