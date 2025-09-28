# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN groupadd -r app && useradd -r -g app app
COPY --from=build /wheels /wheels
RUN --mount=type=cache,target=/root/.cache pip install --no-cache-dir /wheels/*
COPY . .
USER app
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD python -m http.server 8080 --bind 0.0.0.0 >/dev/null 2>&1 || exit 1
EXPOSE 8080
CMD ["python","-m","http.server","8080","--bind","0.0.0.0"]
