# P09 — SBOM & уязвимости зависимостей (SCA в CI)

**Цель:** научиться автоматически получать **SBOM** и проводить **SCA-скан** зависимостей в CI, фиксировать артефакты и, при необходимости, оформлять обоснованные **waivers** по найденным уязвимостям.

**Что сдаём:** PR `p09-sbom-sca → main` со следующими артефактами:

- `.github/workflows/ci-sbom-sca.yml` — workflow, который:
  - генерирует SBOM (например, Syft, формат CycloneDX),
  - запускает SCA (например, Grype/Trivy) на основе SBOM,
  - складывает результаты в `EVIDENCE/P09/` и публикует артефакты Actions;
- каталог `EVIDENCE/P09/` с минимум:
  - `sbom.json` — SBOM,
  - `sca_report.json` — отчёт SCA,
  - `sca_summary.md` — краткая сводка по severity;
- (опционально, для уровня «2») `policy/waivers.yml` с примерами вейверов;
- PR с кратким описанием найденных уязвимостей и/или принятых решений (фикс/waiver).

**Критерий «сдано»:**

- Workflow `ci-sbom-sca.yml` успешно отрабатывает в Actions (зелёный job);
- в репозитории присутствуют артефакты в `EVIDENCE/P09/` и они согласованы с логами job;
- в PR есть краткое описание результата (что сканируется, где лежат артефакты, что дальше делать с vulns).

**Итоговая оценка:** 10 баллов (5 критериев × 2) — см. `practices/P09/02_checklist.md`.

**Learning Outcome:** DS1 — **SBOM и уязвимости зависимостей (SCA)** в контексте вашего проекта.

**Связанные материалы курса:**

- `project/69_sbom-vuln-mgmt.md` — политика SBOM & Vulnerability Management;
- `project/67_containerization-guide.md`, `project/68_ci-cd-minimum.md` — для интеграции в существующий CI/CD;
- seed-репозиторий `secdev-seed-s09-s12` — пример готового workflow и структуры `EVIDENCE/S09`.
