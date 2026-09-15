from __future__ import annotations

import json
from datetime import datetime

from libs.application.dtos.operation__dto import OperationCdto, OperationQdto
from libs.common.clock import iso
from libs.common.enums import OperationKind, OperationState
from libs.domain.entities.operation__entity import OperationEntity
from libs.infrastructure.daos.operation__dao import OperationDao

_STEP_SEPARATOR: str = "#"
_JOB_KINDS: frozenset[OperationKind] = frozenset({OperationKind.STEP, OperationKind.STEP_SUBMIT})


class OperationMapper:
    """OperationEntity ↔ OperationDao ↔ Operation DTOs.

    A step operation's subject is `{job_id}#{op}` (same `#` convention as asset output slots), so the op name is
    visible while the operation is still running without widening the entity.
    """

    @staticmethod
    def step_subject(job_id: str, op: str) -> str:
        return f"{job_id}{_STEP_SEPARATOR}{op}"

    @staticmethod
    def to_dao(operation: OperationEntity) -> OperationDao:
        moments = [m for m in (operation.created_at, operation.started_at, operation.finished_at) if m is not None]
        payload = {
            "subject_id": operation.subject_id,
            "started_at": _iso(operation.started_at),
            "finished_at": _iso(operation.finished_at),
        }
        error = None if operation.error_code is None else {"error_code": operation.error_code, "message": operation.error_message}
        return OperationDao(
            operation_id=operation.operation_id,
            kind=operation.kind.value,
            state=operation.state.value,
            job_id=_job_id(operation.kind, operation.subject_id),
            payload_json=json.dumps(payload, ensure_ascii=False, sort_keys=True),
            result_json=None if operation.result is None else json.dumps(dict(operation.result), ensure_ascii=False, sort_keys=True, default=str),
            error_json=None if error is None else json.dumps(error, ensure_ascii=False, sort_keys=True),
            created_at=iso(operation.created_at),
            updated_at=iso(max(moments)),
        )

    @staticmethod
    def to_entity(dao: OperationDao) -> OperationEntity:
        payload = _object(dao.payload_json)
        error = _object(dao.error_json)
        return OperationEntity(
            operation_id=dao.operation_id,
            kind=OperationKind(dao.kind),
            created_at=datetime.fromisoformat(dao.created_at),
            subject_id=_str(payload.get("subject_id")),
            state=OperationState(dao.state),
            started_at=_parse(payload.get("started_at")),
            finished_at=_parse(payload.get("finished_at")),
            result=None if dao.result_json is None else _object(dao.result_json),
            error_code=_str(error.get("error_code")),
            error_message=_str(error.get("message")),
        )

    @staticmethod
    def to_qdto(dao: OperationDao) -> OperationQdto:
        payload = _object(dao.payload_json)
        error = _object(dao.error_json)
        subject = _str(payload.get("subject_id"))
        step = subject.split(_STEP_SEPARATOR, 1)[1] if subject and dao.kind == OperationKind.STEP.value and _STEP_SEPARATOR in subject else None
        return OperationQdto(
            operation_id=dao.operation_id,
            kind=dao.kind,
            state=dao.state,
            subject_id=subject,
            job_id=dao.job_id,
            step=step,
            created_at=dao.created_at,
            started_at=_str(payload.get("started_at")),
            finished_at=_str(payload.get("finished_at")),
            result=None if dao.result_json is None else _object(dao.result_json),
            error_code=_str(error.get("error_code")),
            error_message=_str(error.get("message")),
        )

    @staticmethod
    def to_cdto(operation: OperationEntity) -> OperationCdto:
        return OperationCdto(operation.operation_id, operation.kind.value, operation.state.value)


def _job_id(kind: OperationKind, subject_id: str | None) -> str | None:
    if kind not in _JOB_KINDS or subject_id is None:
        return None
    return subject_id.split(_STEP_SEPARATOR, 1)[0]


def _iso(at: datetime | None) -> str | None:
    return None if at is None else iso(at)


def _parse(value: object) -> datetime | None:
    return datetime.fromisoformat(value) if isinstance(value, str) else None


def _str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _object(text: str | None) -> dict[str, object]:
    if not text:
        return {}
    data = json.loads(text)
    return data if isinstance(data, dict) else {}
