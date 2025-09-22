# SAST & DAST Playbook - практические рецепты

## SAST (статический анализ)
- **Semgrep**: базовые наборы правил (`p/ci`, `p/security-audit`), + кастомные правила под курс.
- **Secret scanning**: `gitleaks` или `detect-secrets` (pre-commit и/или CI).
- **Порог**: блокировать PR при High/CRITICAL без оправданий.

### Пример шага CI (Semgrep)
```yaml
- name: Semgrep
  run: |
    pip install semgrep
    semgrep ci --config p/ci --config p/security-audit
```

### Пример шага CI (Gitleaks)
```yaml
- name: Gitleaks
  run: |
    curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-amd64 -o gitleaks
    chmod +x gitleaks
    ./gitleaks detect --no-banner --report-format sarif --report-path gitleaks.sarif
```

## DAST (динамика)
- **OWASP ZAP Baseline** против локально поднятого сервиса (Docker Compose).
- Контекст ZAP ограничьте своим хостом; исключите логины и stateful-пути.
- Отчёт - артефакт CI; пороги - по согласованию (обычно предупреждения не блокируют на ранних этапах).

### Пример шага CI (ZAP baseline)
```yaml
- name: Start app
  run: docker compose up -d --build
- name: ZAP Baseline
  run: |
    docker run --rm -t owasp/zap2docker-stable zap-baseline.py       -t http://host.docker.internal:8000 -r zap_report.html -m 1
- name: Upload ZAP report
  uses: actions/upload-artifact@v4
  with:
    name: zap_report
    path: zap_report.html
```

## Триаж результатов
- Ложные срабатывания помечайте и документируйте (короткий комментарий/waiver).
- Безопасность всегда в связке с тестами: добавляйте негативные кейсы там, где фиксите уязвимость.
