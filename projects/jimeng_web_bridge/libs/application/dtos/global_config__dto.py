from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from libs.application.dtos.drama_config__dto import ConfigErrorQdto


@dataclass(frozen=True)
class GlobalConfigQdto:
    """Never carries `.env` content, the bearer token or the HMAC key (FR-4, NFR 安全)."""

    location: str
    values: Mapping[str, object]
    raw_text: str | None
    sha256: str | None
    parse_error: str | None
    validation_error: ConfigErrorQdto | None
    overridden_by_env: tuple[str, ...]


@dataclass(frozen=True)
class GlobalConfigSaveCdto:
    location: str
    sha256: str
    changed_keys: tuple[str, ...]
