from typing import Any, Dict
from uuid import uuid4
from starlette.responses import JSONResponse  # или эквивалентный Response

def problem(status: int, title: str, detail: str, type_: str = "about:blank", extras: Dict[str, Any] | None = None):
    cid = str(uuid4())
    payload = {"type": type_, "title": title, "status": status, "detail": detail, "correlation_id": cid}
    if extras:
        payload.update(extras)
    return JSONResponse(payload, status_code=status)
