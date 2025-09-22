# Контейнеризация - практический гайд

## Dockerfile (минимальный multi-stage, non-root)
```dockerfile
# Build stage
FROM python:3.12-slim AS build
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY src ./src
RUN python -m py_compile $(git ls-files '*.py' || echo src)

# Runtime stage
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
RUN useradd -m appuser
WORKDIR /app
COPY --from=build /app /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',8000))" || exit 1
CMD ["python", "-m", "app"]
```

## .dockerignore (пример)
```
.venv
__pycache__
*.pyc
.git
.github
tests
*.log
.env
```

## Compose для локального запуска (эскиз)
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - APP_ENV=dev
    security_opt:
      - no-new-privileges:true
    cap_drop: [ALL]
```

## Практики безопасности
- **Не root**; минимум пакетов; регулярные обновления базового образа.
- `.dockerignore`; сканирование образов (Trivy/Syft/Grype в P09).
- Ограничение привилегий контейнера (cap_drop, read-only fs - при возможности).
