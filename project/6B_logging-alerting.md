# Логирование и алёрты - минимум, чтобы было полезно

## Структурные логи
- Формат JSON; 1 запись на запрос.
- Поля: `ts`, `level`, `request_id`, `method`, `path`, `status`, `duration_ms`, `user_id` (если есть).
- Не логируйте секреты/ПДн.

### Питон (пример)
```python
import logging, json, time, uuid
logger = logging.getLogger("app")

def log_request(request, status, started):
    rec = {
        "ts": time.time(),
        "level": "INFO",
        "request_id": request.headers.get("X-Request-Id", str(uuid.uuid4())),
        "method": request.method,
        "path": request.path,
        "status": status,
        "duration_ms": int((time.time() - started) * 1000),
    }
    logger.info(json.dumps(rec))
```

## Метрики/алёрты (минимум)
1) **5xx rate > X% за 5 мин** → потенциальная деградация.  
2) **401/403 всплеск на /auth/login** → брутфорс/аномалия.

## Хранение и доступ
- Локально - stdout (dev); в контейнерах - собирать лог-драйвером/агентом.
- Срок хранения логов: разумный (дни/недели), без ПДн.

## Корреляция
- Пробрасывайте `X-Request-Id` в ответы; кореллируйте логи между сервисами.
