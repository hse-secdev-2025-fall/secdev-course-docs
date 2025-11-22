# Сниппеты — P11 (DAST с OWASP ZAP baseline)

## 1) Локальный запуск ZAP baseline (пример)

```bash
# Поднять сервис (пример для FastAPI)
uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# Подождать готовность
until curl -sf http://localhost:8080/healthz; do sleep 1; done

# Запустить ZAP baseline
docker run --rm --network host -v $PWD:/zap/wrk owasp/zap2docker-stable \
  zap-baseline.py \
    -t http://localhost:8080 \
    -r zap_baseline.html \
    -J zap_baseline.json \
    -d || true

mkdir -p EVIDENCE/P11
mv zap_baseline.* EVIDENCE/P11/
```

---

## 2) Фрагмент job для GitHub Actions (вставить в workflow)

```yaml
- name: Ensure evidence dirs
  run: mkdir -p EVIDENCE/P11

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"

- name: Install dependencies
  run: |
    pip install --upgrade pip
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

- name: Run app
  run: |
    uvicorn app.main:app --host 0.0.0.0 --port 8080 &
    timeout 30 bash -c 'until curl -sf http://localhost:8080/healthz; do sleep 1; done'

- name: ZAP Baseline
  run: |
    docker run --rm --network host -v $PWD:/zap/wrk owasp/zap2docker-stable \
      zap-baseline.py \
        -t http://localhost:8080 \
        -r zap_baseline.html \
        -J zap_baseline.json \
        -d || true
    mv zap_baseline.* EVIDENCE/P11/ || true

- name: Upload P11 evidence
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: P11_EVIDENCE
    path: EVIDENCE/P11
```

Не забудьте поменять `app.main:app`, порт и путь health-чека под свой проект.

---

## 3) Мини-шаблон текста для PR

```text
P11 - DAST (ZAP baseline)

Target: http://localhost:8080/
Reports: EVIDENCE/P11/zap_baseline.html, zap_baseline.json
Result: N alerts (High=X, Medium=Y, Low=Z).
Notes: <1–2 предложения про самые интересные предупреждения и план действий>.
```
