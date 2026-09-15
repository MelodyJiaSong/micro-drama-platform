from __future__ import annotations

import re
import secrets
from datetime import datetime, timezone

_PREFIX = re.compile(r"^[a-z]{2,8}$")


def new_id(prefix: str, at: datetime | None = None) -> str:
    """`job_20260913120000_1a2b3c4d` — sortable, path-segment safe (artifact dirs use it)."""
    if not _PREFIX.match(prefix):
        raise ValueError(f"invalid id prefix: {prefix!r}")
    moment = (at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return f"{prefix}_{moment:%Y%m%d%H%M%S}_{secrets.token_hex(4)}"
