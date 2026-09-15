from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationDao:
    operation_id: str
    kind: str
    state: str
    job_id: str | None
    payload_json: str
    result_json: str | None
    error_json: str | None
    created_at: str
    updated_at: str
