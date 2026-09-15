from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from libs.common.enums import BackendKind, PreparingStep


@dataclass(frozen=True)
class OperationRunners:
    """Background bodies supplied by the container; each returns a JSON-able result dict or raises."""

    canary: Callable[[BackendKind], dict[str, object]]
    resume_queue: Callable[[BackendKind], dict[str, object]]
    entity_sync: Callable[[], dict[str, object]]
    step: Callable[[str, PreparingStep], dict[str, object]]
    step_submit: Callable[[str], dict[str, object]]


@dataclass(frozen=True)
class OperationCdto:
    operation_id: str
    kind: str
    state: str


@dataclass(frozen=True)
class OperationQdto:
    operation_id: str
    kind: str
    state: str
    subject_id: str | None
    job_id: str | None
    step: str | None
    created_at: str
    started_at: str | None
    finished_at: str | None
    result: dict[str, object] | None
    error_code: str | None
    error_message: str | None
