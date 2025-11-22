# P12 — IaC & Container Security (Hadolint, Checkov, Trivy)

**Цель:** добавить в проект автоматическую проверку Dockerfile и IaC (Infrastructure as Code), а также базовое сканирование контейнерного образа на уязвимости. Всё это должно выполняться в CI и сохранять отчёты в `EVIDENCE/P12/`.

**Что сдаём:** PR `p12-iac-container → main` со следующими артефактами:

- `.github/workflows/ci-p12-iac-container.yml` — workflow для P12;
- конфиги линтеров и сканеров:
  - `security/hadolint.yaml` — базовая конфигурация Hadolint;
  - `security/checkov.yaml` — базовая конфигурация Checkov;
  - `security/trivy.yaml` — (опционально) настройки Trivy;
- каталог `EVIDENCE/P12/` с минимум:
  - `hadolint_report.json` — отчёт Hadolint по Dockerfile;
  - `checkov_report.json` — отчёт Checkov по IaC (K8s/TF/другое);
  - `trivy_report.json` — отчёт Trivy по образу;
  - (опционально) `hardening_summary.md` — короткая сводка по итогам.

**Критерий «сдано»:**

- workflow `ci-p12-iac-container.yml` успешно выполняется в GitHub Actions (зелёный job);
- в `EVIDENCE/P12/` лежат актуальные отчёты по Dockerfile, IaC и образу;
- в описании PR кратко описано, какие меры харднинга вы уже применили/планируете применить.

**Итоговая оценка:** до 10 баллов (5 критериев × 2) — см. `practices/P12/02_checklist.md`.

**Learning Outcome:** базовая безопасность инфраструктуры и контейнеров (IaC & Container Security) как часть DevSecOps-пайплайна.

**Связанные материалы курса:**

- `project/6D_hardening-guide.md` — гайд по харднингу и настройке инфраструктуры;
- `project/68_ci-cd-minimum.md` — минимальные требования к CI/CD;
- seed-репозиторий `secdev-seed-s09-s12` — примеры конфигов (`security/hadolint.yaml`, `security/checkov.yaml`, `security/trivy.yaml`) и workflow для S12 (используется как референс, но не как место сдачи).
