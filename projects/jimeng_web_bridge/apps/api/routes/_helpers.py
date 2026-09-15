import dataclasses
from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from pathlib import Path

from fastapi import HTTPException, Request

from libs.infrastructure.middleware.request_class__middleware import REQUEST_CLASS_KEY, UI


def to_json(value: object) -> object:
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {field.name: to_json(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, Mapping):
        return {str(key): to_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_json(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def request_class(request: Request) -> str:
    return str(request.scope.get("state", {}).get(REQUEST_CLASS_KEY, ""))


def require_ui(request: Request) -> None:
    """Human-only actions: confirmation, adjudication, global config writes (spec v2 FR-14, FR-4)."""
    if request_class(request) != UI:
        raise HTTPException(
            status_code=403,
            detail={"error_code": "ui_only_action", "message": "此操作只能在本地管理网页由人完成", "hint": None},
        )
