# Сниппеты — P05 (Secure Coding & ADR)

## 1) ADR — каркас
```md
# ADR-001: <краткое название>
Дата: 2025-09-22
Статус: Accepted

## Context
Проблема/варианты/ограничения (почему это важно).

## Decision
Принятое решение (кто/что/где). Параметры/пороги/конфиги (если есть).

## Consequences
Плюсы/минусы, компромиссы, влияние на DX/стоимость/производительность.

## Links
- NFR-03 (ошибки RFC7807), NFR-05 (ротация секретов)
- F1, R2 из Threat Model
- tests/test_errors.py::test_rfc7807_contract
```

## 2) RFC 7807 — пример обработчика (Starlette/FastAPI-совместимый)
```python
from typing import Any, Dict
from uuid import uuid4
from starlette.responses import JSONResponse

def problem(status: int, title: str, detail: str, type_: str = "about:blank", extras: Dict[str, Any] | None = None):
    cid = str(uuid4())
    payload = {"type": type_, "title": title, "status": status, "detail": detail, "correlation_id": cid}
    if extras:
        payload.update(extras)
    return JSONResponse(payload, status_code=status)
```

## 3) Загрузка файла — magic bytes + канонизация путей (без внешних библиотек)
```python
import os, uuid
from pathlib import Path

MAX_BYTES = 5_000_000
ALLOWED = {"image/png", "image/jpeg"}

PNG = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"; JPEG_EOI = b"\xff\xd9"

def sniff_image_type(data: bytes) -> str | None:
    if data.startswith(PNG):
        return "image/png"
    if data.startswith(JPEG_SOI) and data.endswith(JPEG_EOI):
        return "image/jpeg"
    return None

def secure_save(base_dir: str, filename_hint: str, data: bytes) -> tuple[bool, str]:
    if len(data) > MAX_BYTES:
        return False, "too_big"
    mt = sniff_image_type(data)
    if mt not in ALLOWED:
        return False, "bad_type"
    root = Path(base_dir).resolve(strict=True)
    # имя — UUID, расширение по типу
    ext = ".png" if mt == "image/png" else ".jpg"
    name = f"{uuid.uuid4()}{ext}"
    path = (root / name).resolve()
    if not str(path).startswith(str(root)):
        return False, "path_traversal"
    # запрет симлинков вдоль пути (safe на обычных FS)
    if any(p.is_symlink() for p in path.parents):
        return False, "symlink_parent"
    with open(path, "wb") as f:
        f.write(data)
    return True, str(path)
```

## 4) Pytest — негативные тесты
```python
import os
from pathlib import Path
from myapp.upload import secure_save

def test_rejects_big_file(tmp_path: Path):
    ok, reason = secure_save(tmp_path, "x.png", b"\x89PNG\r\n\x1a\n" + b"0"*5_000_001)
    assert not ok and reason == "too_big"

def test_sniffs_bad_type(tmp_path: Path):
    ok, reason = secure_save(tmp_path, "x.png", b"not_an_image")
    assert not ok and reason == "bad_type"
```
