from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ShotItemInput:
    shot_path: str
    reroll: bool = False


@dataclass(frozen=True)
class AssetItemInput:
    card_path: str
    key: str
    reroll: bool = False


@dataclass(frozen=True)
class RawItemInput:
    kind: str
    prompt: str
    reference_paths: tuple[str, ...]
    entity_names: tuple[str, ...]
    params: Mapping[str, object]
    output_dir: str
    negative_prompt: str | None = None
    reroll: bool = False


@dataclass(frozen=True)
class EntityCreateItemInput:
    drama_rel: str
    character_dir: str
    description: str | None = None


BatchItemInput = ShotItemInput | AssetItemInput | RawItemInput | EntityCreateItemInput


@dataclass(frozen=True)
class BatchPrecheckCdto:
    batch_id: str
    state: str
    ok_count: int
    warning_count: int
    error_count: int
    estimated_credits: int
    has_unestimated: bool
    existing_job_ids: tuple[str, ...]
    confirm_path: str


@dataclass(frozen=True)
class BatchConfirmCdto:
    batch_id: str
    job_ids: tuple[str, ...]
    confirmed_at: str


@dataclass(frozen=True)
class BatchCheckQdto:
    check: str
    severity: str
    code: str
    message: str
    config_key: str | None
    reference_name: str | None


@dataclass(frozen=True)
class BatchReferenceQdto:
    name: str
    label: str
    kind: str
    path: str | None
    entity: str | None
    sha256: str | None


@dataclass(frozen=True)
class BatchParamsQdto:
    model: str
    ratio: str
    resolution: str
    count: int
    duration_s: int | None
    reference_mode: str | None


@dataclass(frozen=True)
class BatchItemQdto:
    index: int
    kind: str
    backend: str
    source_type: str
    source_path: str
    block_key: str | None
    drama_rel: str | None
    output_slot: str
    entity_name: str | None
    prompt_codepoints: int
    has_negative_prompt: bool
    params: BatchParamsQdto | None
    references: tuple[BatchReferenceQdto, ...]
    severity: str
    checks: tuple[BatchCheckQdto, ...]
    estimated_credits: int | None
    existing_job_id: str | None
    reroll: bool


@dataclass(frozen=True)
class BatchQdto:
    batch_id: str
    state: str
    created_at: str
    expires_at: str | None
    confirmed_at: str | None
    confirmer: str | None
    ok_count: int
    warning_count: int
    error_count: int
    estimated_credits: int
    has_unestimated: bool
    existing_job_ids: tuple[str, ...]
    job_ids: tuple[str, ...]
    balance_start: int | None
    balance_end: int | None
    confirm_path: str
    page: int
    page_size: int
    total_items: int
    items: tuple[BatchItemQdto, ...]


@dataclass(frozen=True)
class BatchConfirmationQdto:
    batch_id: str
    token: str = field(repr=False)
    expires_at: str
    seconds_left: int
    estimated_credits: int
    today_confirmed_credits: int
