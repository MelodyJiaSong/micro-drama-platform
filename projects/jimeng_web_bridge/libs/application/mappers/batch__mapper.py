from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from libs.application.dtos.batch__dto import (
    BatchCheckQdto,
    BatchItemQdto,
    BatchParamsQdto,
    BatchPrecheckCdto,
    BatchQdto,
    BatchReferenceQdto,
)
from libs.application.mappers.request_json__mapper import RequestJsonMapper
from libs.common.clock import iso
from libs.common.enums import BackendKind, BatchState, CheckSeverity, Confirmer, PrecheckCheck
from libs.domain.entities.batch__entity import BatchEntity
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.precheck_result__valueobject import PrecheckItem, PrecheckResult
from libs.domain.value_objects.price_estimate__valueobject import PriceEstimate
from libs.infrastructure.daos.batch__dao import BatchDao

CONFIRM_PATH: str = "/batches/{batch_id}"
_TOKEN_SPENT_STATES: frozenset[BatchState] = frozenset({BatchState.CONFIRMED, BatchState.REJECTED})


@dataclass(frozen=True)
class BatchItemMeta:
    """Per-item facts the entity does not carry: routed backend, config digest, and the input for re-precheck."""

    backend: BackendKind
    config_digest: str
    estimate_tolerance_pct: int
    drama_rel: str | None
    reroll: bool
    input: Mapping[str, object]


@dataclass(frozen=True)
class StoredBatch:
    entity: BatchEntity
    metas: tuple[BatchItemMeta, ...]
    idempotency_key: str | None


class BatchMapper:
    """`items_json` is an envelope `{token_signature, consumed_token_signature, items[]}` — the batches table has no
    column for either signature. `token_used` is set once the token can no longer be used (confirmed or rejected)."""

    def __init__(self, requests: RequestJsonMapper) -> None:
        self._requests: RequestJsonMapper = requests

    def to_dao(
        self, batch: BatchEntity, metas: Sequence[BatchItemMeta], idempotency_key: str | None, now: datetime
    ) -> BatchDao:
        envelope: dict[str, object] = {
            "token_signature": batch.token_signature,
            "consumed_token_signature": batch.consumed_token_signature,
            "items": [
                {
                    "index": item.index,
                    "fingerprint": item.fingerprint.value,
                    "request": self._requests.request_to_dict(item.request),
                    "precheck": _precheck_to_dict(item.precheck),
                    "meta": _meta_to_dict(meta),
                }
                for item, meta in zip(batch.items, metas, strict=True)
            ],
        }
        return BatchDao(
            batch_id=batch.batch_id,
            state=batch.state.value,
            idempotency_key=idempotency_key,
            content_digest=batch.content_digest,
            estimated_credits=batch.estimated_credits,
            items_json=json.dumps(envelope, ensure_ascii=False, sort_keys=True),
            token_used=batch.state in _TOKEN_SPENT_STATES,
            expires_at=_iso(batch.token_expires_at),
            confirmed_at=_iso(batch.confirmed_at),
            confirmer=None if batch.confirmer is None else batch.confirmer.value,
            balance_start=batch.balance_start,
            balance_end=batch.balance_end,
            created_at=iso(batch.created_at),
            updated_at=iso(now),
        )

    def to_stored(self, dao: BatchDao) -> StoredBatch:
        envelope: dict[str, Any] = json.loads(dao.items_json)
        rows: list[dict[str, Any]] = envelope["items"]
        entity = BatchEntity(
            dao.batch_id,
            [
                BatchItem(
                    index=row["index"],
                    request=self._requests.request_from_dict(row["request"]),
                    precheck=_precheck_from_dict(row["precheck"]),
                    fingerprint=Fingerprint(row["fingerprint"]),
                )
                for row in rows
            ],
            RequestJsonMapper.parse_iso(dao.created_at),
            state=BatchState(dao.state),
            token_expires_at=_parse(dao.expires_at),
            token_signature=envelope["token_signature"],
            confirmed_at=_parse(dao.confirmed_at),
            confirmer=None if dao.confirmer is None else Confirmer(dao.confirmer),
            consumed_token_signature=envelope["consumed_token_signature"],
            balance_start=dao.balance_start,
            balance_end=dao.balance_end,
        )
        return StoredBatch(entity, tuple(_meta_from_dict(row["meta"]) for row in rows), dao.idempotency_key)

    def precheck_cdto(self, batch: BatchEntity) -> BatchPrecheckCdto:
        counts: dict[CheckSeverity, int] = batch.severity_counts()
        return BatchPrecheckCdto(
            batch_id=batch.batch_id,
            state=batch.state.value,
            ok_count=counts[CheckSeverity.OK],
            warning_count=counts[CheckSeverity.WARNING],
            error_count=counts[CheckSeverity.ERROR],
            estimated_credits=batch.estimated_credits,
            has_unestimated=batch.has_unestimated,
            existing_job_ids=_existing_job_ids(batch),
            confirm_path=CONFIRM_PATH.format(batch_id=batch.batch_id),
        )

    def precheck_cdto_to_json(self, cdto: BatchPrecheckCdto) -> str:
        return json.dumps(asdict(cdto), ensure_ascii=False, sort_keys=True)

    def precheck_cdto_from_json(self, text: str) -> BatchPrecheckCdto:
        data: dict[str, Any] = json.loads(text)
        data["existing_job_ids"] = tuple(data["existing_job_ids"])
        return BatchPrecheckCdto(**data)

    def batch_qdto(self, stored: StoredBatch, job_ids: Sequence[str], page: int, page_size: int) -> BatchQdto:
        batch: BatchEntity = stored.entity
        counts: dict[CheckSeverity, int] = batch.severity_counts()
        start: int = (page - 1) * page_size
        pairs = list(zip(batch.items, stored.metas, strict=True))[start : start + page_size]
        return BatchQdto(
            batch_id=batch.batch_id,
            state=batch.state.value,
            created_at=iso(batch.created_at),
            expires_at=_iso(batch.token_expires_at),
            confirmed_at=_iso(batch.confirmed_at),
            confirmer=None if batch.confirmer is None else batch.confirmer.value,
            ok_count=counts[CheckSeverity.OK],
            warning_count=counts[CheckSeverity.WARNING],
            error_count=counts[CheckSeverity.ERROR],
            estimated_credits=batch.estimated_credits,
            has_unestimated=batch.has_unestimated,
            existing_job_ids=_existing_job_ids(batch),
            job_ids=tuple(job_ids),
            balance_start=batch.balance_start,
            balance_end=batch.balance_end,
            confirm_path=CONFIRM_PATH.format(batch_id=batch.batch_id),
            page=page,
            page_size=page_size,
            total_items=len(batch.items),
            items=tuple(_item_qdto(item, meta) for item, meta in pairs),
        )


def _item_qdto(item: BatchItem, meta: BatchItemMeta) -> BatchItemQdto:
    request = item.request
    params = request.params
    return BatchItemQdto(
        index=item.index,
        kind=request.kind.value,
        backend=meta.backend.value,
        source_type=request.source.type.value,
        source_path=request.source.path,
        block_key=request.source.block_key,
        drama_rel=meta.drama_rel,
        output_slot=request.output_slot,
        entity_name=request.entity_name,
        prompt_codepoints=request.prompt_codepoints(),
        has_negative_prompt=request.negative_prompt is not None,
        params=None if params is None else BatchParamsQdto(
            params.model, params.ratio, params.resolution, params.count, params.duration_s, params.reference_mode
        ),
        references=tuple(
            BatchReferenceQdto(ref.name, ref.label, ref.kind.value, ref.resolved_path, ref.entity_name, ref.sha256)
            for ref in request.references
        ),
        severity=item.precheck.severity.value,
        checks=tuple(
            BatchCheckQdto(c.check.value, c.severity.value, c.error_code, c.message, c.config_key, c.reference_name)
            for c in item.precheck.items
        ),
        estimated_credits=item.precheck.estimate.credits,
        existing_job_id=item.precheck.existing_job_id,
        reroll=meta.reroll,
    )


def _existing_job_ids(batch: BatchEntity) -> tuple[str, ...]:
    return tuple(item.precheck.existing_job_id for item in batch.items if item.precheck.existing_job_id is not None)


def _precheck_to_dict(result: PrecheckResult) -> dict[str, object]:
    return {
        "items": [
            {
                "check": item.check.value,
                "severity": item.severity.value,
                "error_code": item.error_code,
                "message": item.message,
                "config_key": item.config_key,
                "reference_name": item.reference_name,
            }
            for item in result.items
        ],
        "estimate": {
            "credits": result.estimate.credits,
            "warning": result.estimate.warning,
            "config_key": result.estimate.config_key,
        },
        "existing_job_id": result.existing_job_id,
    }


def _precheck_from_dict(data: Mapping[str, Any]) -> PrecheckResult:
    estimate: Mapping[str, Any] = data["estimate"]
    return PrecheckResult(
        items=tuple(
            PrecheckItem(
                check=PrecheckCheck(row["check"]),
                severity=CheckSeverity(row["severity"]),
                error_code=row["error_code"],
                message=row["message"],
                config_key=row["config_key"],
                reference_name=row["reference_name"],
            )
            for row in data["items"]
        ),
        estimate=PriceEstimate(estimate["credits"], estimate["warning"], estimate["config_key"]),
        existing_job_id=data["existing_job_id"],
    )


def _meta_to_dict(meta: BatchItemMeta) -> dict[str, object]:
    return {
        "backend": meta.backend.value,
        "config_digest": meta.config_digest,
        "estimate_tolerance_pct": meta.estimate_tolerance_pct,
        "drama_rel": meta.drama_rel,
        "reroll": meta.reroll,
        "input": dict(meta.input),
    }


def _meta_from_dict(data: Mapping[str, Any]) -> BatchItemMeta:
    return BatchItemMeta(
        backend=BackendKind(data["backend"]),
        config_digest=data["config_digest"],
        estimate_tolerance_pct=data["estimate_tolerance_pct"],
        drama_rel=data["drama_rel"],
        reroll=data["reroll"],
        input=data["input"],
    )


def _iso(moment: datetime | None) -> str | None:
    return None if moment is None else iso(moment)


def _parse(text: str | None) -> datetime | None:
    return None if text is None else RequestJsonMapper.parse_iso(text)
