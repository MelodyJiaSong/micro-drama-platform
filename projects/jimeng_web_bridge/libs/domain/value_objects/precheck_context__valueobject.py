from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from types import MappingProxyType

from libs.common.enums import BackendKind, NegativePromptStrategy
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.price_estimate__valueobject import PriceTable


@dataclass(frozen=True)
class ReferenceIssue:
    error_code: str
    message: str
    reference_name: str | None = None
    config_key: str | None = None


@dataclass(frozen=True)
class EntitySnapshotFacts:
    names: frozenset[str]
    synced_at: datetime | None

    @property
    def never_synced(self) -> bool:
        return self.synced_at is None

    def is_stale(self, now: datetime, stale_after: timedelta) -> bool:
        return self.synced_at is not None and now - self.synced_at > stale_after


@dataclass(frozen=True)
class PrecheckContext:
    backend: BackendKind
    limits: ModelLimits
    price_table: PriceTable
    prompt_max_chars: int
    entity_name_max_chars: int
    negative_prompt_strategy: NegativePromptStrategy
    snapshot: EntitySnapshotFacts
    snapshot_stale_after: timedelta
    now: datetime
    output_dir_writable: bool
    reference_issues: tuple[ReferenceIssue, ...] = ()
    legacy_reference_fragments: tuple[str, ...] = ()
    fingerprint_hit_job_id: str | None = None
    reroll: bool = False
    entity_card_dirs: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_card_dirs", MappingProxyType(dict(self.entity_card_dirs)))
