"""Shared route helpers (cross-cutting across aggregate route files)."""
from __future__ import annotations

from urllib.parse import quote


def file_security_headers(filename: str, disposition: str = "attachment") -> dict[str, str]:
    safe = "".join(c for c in filename if 32 <= ord(c) < 127 and c not in '"\\')
    if not safe:
        safe = "file"
    # RFC 5987: the quoted `filename` is ASCII-only, so a Chinese name collapses
    # to "_.pdf". `filename*` carries the real UTF-8 name for clients that read
    # it (all current browsers); `filename` stays as the legacy fallback.
    encoded = quote(filename, safe="")
    return {
        "X-Content-Type-Options": "nosniff",
        "Content-Disposition": f"{disposition}; filename=\"{safe}\"; filename*=UTF-8''{encoded}",
    }
