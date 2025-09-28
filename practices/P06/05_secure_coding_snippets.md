# Сниппеты — P06 (Secure Coding)

## 1) Валидация + Decimal/UTC (Pydantic v2)
```python
from pydantic import BaseModel, Field, ValidationError
from decimal import Decimal
from datetime import datetime, timezone

class Payment(BaseModel):
    model_config = dict(extra='forbid')
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    occurred_at: datetime

def normalize(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc).replace(tzinfo=None)

# parse JSON без float
import json
data = json.loads(raw_json, parse_float=str)
Payment.model_validate(data)
```

## 2) RFC 7807
```python
from uuid import uuid4
from starlette.responses import JSONResponse

def problem(status: int, title: str, detail: str, type_: str="about:blank"):
    cid = str(uuid4())
    return JSONResponse({"type":type_, "title":title, "status":status, "detail":detail, "correlation_id":cid}, status_code=status)
```

## 3) Файлы: magic bytes + канонизация
```python
from pathlib import Path
import uuid
MAX=5_000_000; PNG=b"\x89PNG\r\n\x1a\n"; SOI=b"\xff\xd8"; EOI=b"\xff\xd9"

def sniff(data: bytes) -> str|None:
    if data.startswith(PNG): return "image/png"
    if data.startswith(SOI) and data.endswith(EOI): return "image/jpeg"
    return None

def secure_save(root: Path, data: bytes) -> Path:
    if len(data)>MAX: raise ValueError("too_big")
    mt = sniff(data); 
    if not mt: raise ValueError("bad_type")
    root = root.resolve(strict=True)
    ext = ".png" if mt=="image/png" else ".jpg"
    p = (root / f"{uuid.uuid4()}{ext}").resolve()
    if not str(p).startswith(str(root)): raise ValueError("path_traversal")
    if any(x.is_symlink() for x in p.parents): raise ValueError("symlink_parent")
    p.write_bytes(data); return p
```

## 4) HTTP‑клиент (httpx) — таймауты/ретраи
```python
import httpx, time
TIMEOUT = httpx.Timeout(5.0, read=5.0, connect=3.0)
for attempt in range(3):
    try:
        with httpx.Client(timeout=TIMEOUT) as c:
            r = c.get("https://api.example.com/health", follow_redirects=True)
            r.raise_for_status()
            break
    except Exception:
        if attempt==2: raise
        time.sleep(0.5*(attempt+1))
```

## 5) Параметризация SQL (psycopg/asyncpg)
```python
cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
```
