"""Read-only configuration projection; never return credentials or launch arguments."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit, urlunsplit

HIDDEN = "[已隐藏]"
SENSITIVE = re.compile(r"secret|password|passwd|token|credential|cookie|authorization|api.?key|access.?key|private.?key|^auth$|^key$", re.I)
OPAQUE = frozenset({"env", "env_vars", "environment", "headers", "http_headers", "args", "notify"})


def redact_text(text: str) -> str:
    text = re.sub(r"(?i)\b(?:sk-[\w-]{8,}|Bearer\s+[\w./+=-]+)\b", HIDDEN, text)
    text = re.sub(r"(?i)((?:api[_-]?key|password|secret|token|authorization)\s*[=:]\s*)([^\s,;]+)", r"\1" + HIDDEN, text)
    def url(match: re.Match[str]) -> str:
        try:
            value = urlsplit(match[0])
            host = value.netloc.rsplit("@", 1)[-1]
            return urlunsplit((value.scheme, host, value.path, "[已隐藏查询参数]" if value.query else "", ""))
        except ValueError:
            return HIDDEN
    return re.sub(r"https?://[^\s\"'<>]+", url, text)


def redact_config(value: Any, key: str = "") -> Any:
    if SENSITIVE.search(key):
        return HIDDEN
    if key.lower() in OPAQUE:
        return {str(name): HIDDEN for name in value} if isinstance(value, dict) else HIDDEN
    if isinstance(value, dict):
        return {str(name): redact_config(item, str(name)) for name, item in value.items()}
    if isinstance(value, list):
        return [redact_config(item, key) for item in value]
    if isinstance(value, str):
        if key.lower() == "command":
            # Hooks retain their script locator, but shell expressions / arguments are opaque.
            locator = re.match(r"^(?:python(?:3)?|node)\s+([\w./\\-]+\.(?:py|js))$", value)
            return value if locator else HIDDEN
        return redact_text(value)
    return value
