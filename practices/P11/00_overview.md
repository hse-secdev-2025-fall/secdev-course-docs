# P11 — DAST (OWASP ZAP baseline) для курсового сервиса

**Цель:** встроить минимальное DAST-сканирование (OWASP ZAP baseline) в CI курсового сервиса: поднять приложение на раннере, прогнать ZAP baseline, сохранить отчёты в `EVIDENCE/P11/` и кратко зафиксировать результат в описании PR.

**Что сдаём:** PR `p11-dast-zap → main` со следующими артефактами:

- `.github/workflows/ci-p11-dast.yml` — workflow с job для ZAP baseline;
- каталог `EVIDENCE/P11/` с отчётами:
  - `zap_baseline.html` — человекочитаемый HTML-отчёт;
  - `zap_baseline.json` — JSON-отчёт;
- описание в PR:
  - какой URL сканировался (`http://localhost:PORT/...`);
  - сколько предупреждений нашёл ZAP (High/Medium/Low);
  - что вы с ними планируете делать (исправить / принять / игнорировать как FP).

**Критерий «сдано»:**

- workflow `ci-p11-dast.yml` **успешно отрабатывает** в GitHub Actions (зелёный job);
- в репозитории есть актуальные отчёты `EVIDENCE/P11/zap_baseline.*`;
- в описании PR есть короткое резюме результатов DAST-сканирования.

**Итоговая оценка:** до 10 баллов (5 критериев × 2) — см. `practices/P11/02_checklist.md`.

**Learning Outcome:** DAST-проверки HTTP-сервиса (OWASP ZAP baseline) как часть DevSecOps-контуров проекта.

**Связанные материалы курса:**

- `project/6A_sast-dast-playbook.md` — общая методика SAST/DAST;
- seed-репозиторий `secdev-seed-s09-s12` — пример workflow `ci-s11-dast.yml` и структуры `EVIDENCE/S11` (используется как референс, но не как место сдачи).
