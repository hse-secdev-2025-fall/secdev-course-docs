# Сниппеты — P06 (Контейнеризация и харднинг)

## 1) Минимальный Dockerfile (Python, multi-stage)
```dockerfile
# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-slim AS build
WORKDIR /app
COPY pyproject.toml poetry.lock* requirements*.txt* ./
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip && \
    pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
# Создать непривилегированного пользователя
RUN groupadd -r app && useradd -r -g app app
COPY --from=build /wheels /wheels
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir /wheels/*
COPY . .
USER app
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -m http.server 8080 --bind 0.0.0.0 >/dev/null 2>&1 || exit 1
EXPOSE 8080
CMD ["python","-m","http.server","8080","--bind","0.0.0.0"]
```

## 2) .dockerignore (минимум)
```
.git
__pycache__/
*.pyc
*.pyo
*.pyd
*.pytest_cache/
dist/
build/
.env
.idea
.vscode
coverage.xml
reports/
```

## 3) docker-compose.yml (каркас)
```yaml
version: "3.9"
services:
  app:
    build: .
    image: ${IMAGE_NAME:-myapp}:latest
    ports: ["8080:8080"]
    environment:
      - APP_ENV=dev
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```

## 4) Проверка «не root»
```bash
docker build -t myapp:dev .
docker run --rm myapp:dev id -u | grep -qv '^0$' && echo "OK: non-root" || echo "BAD: root"
```
