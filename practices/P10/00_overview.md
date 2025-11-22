# P10 — SAST & Secrets (Semgrep + Gitleaks)

**Цель:** настроить статический анализ кода (SAST) и сканирование секретов как часть CI, собрать отчёты и зафиксировать решения по найденным проблемам.

**Что сдаём:** PR `p10-sast-secrets → main` со следующими артефактами:

- `.github/workflows/ci-sast-secrets.yml` — workflow SAST & Secrets;
- `security/semgrep/rules.yml` — (минимальный) набор правил Semgrep под проект;
- `security/.gitleaks.toml` — базовая конфигурация Gitleaks/allowlist;
- каталог `EVIDENCE/P10/` с:
  - `semgrep.sarif` — отчёт SAST,
  - `gitleaks.json` — отчёт по секретам,
  - (опционально) `sast_summary.md` — короткая сводка;
- краткая запись в проектной документации / DS-разделе (как минимум — в описании PR).

**Критерий «сдано»:**

- workflow `ci-sast-secrets.yml` успешно отрабатывает в GitHub Actions (зелёный job);
- артефакты присутствуют в `EVIDENCE/P10/` и соответствуют логам workflow;
- в PR описано, какие профили/правила использованы и что сделано с найденными проблемами (игнор / фикс / перенос в backlog).

**Итоговая оценка:** до 10 баллов (5 критериев × 2) — см. `practices/P10/02_checklist.md`.

**Связанные материалы курса:**

- `project/6A_sast-dast-playbook.md` — общая методика SAST & DAST;
- `project/65_secure-coding-standards.md` — чек-лист безопасного кода;
- seed-репозиторий `secdev-seed-s09-s12` — пример workflow `ci-s10-sast-secrets.yml` и структуры `EVIDENCE/S10`.
