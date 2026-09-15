from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyDao:
    key: str
    content_sha256: str
    response_json: str
    created_at: str


@dataclass(frozen=True)
class QueueStateDao:
    backend: str
    state: str
    reason: str | None
    updated_at: str


@dataclass(frozen=True)
class EntitySnapshotDao:
    name: str
    thumbnail_url: str | None
    modified_at: str | None
    synced_at: str
