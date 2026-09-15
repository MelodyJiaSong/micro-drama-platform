from __future__ import annotations

from dataclasses import dataclass

from libs.application.dtos.drama_config__dto import ConfigErrorQdto


@dataclass(frozen=True)
class EntityUsageQdto:
    """`via`: card (a character card maps to the name) | reference_override (`references.overrides` = `entity:{name}`)."""

    drama_rel: str
    character_dir: str | None
    card_rel: str | None
    source_drama_rel: str | None
    via: str


@dataclass(frozen=True)
class ReconcileRowQdto:
    """`state`: mapped | missing_on_platform | unmapped_on_platform."""

    name: str
    state: str
    usages: tuple[EntityUsageQdto, ...]
    thumbnail_url: str | None
    modified_at: str | None


@dataclass(frozen=True)
class UnnamedCardQdto:
    drama_rel: str
    character_dir: str
    card_rel: str
    error_code: str
    config_key: str | None


@dataclass(frozen=True)
class DramaConfigIssueQdto:
    drama_rel: str
    error: ConfigErrorQdto


@dataclass(frozen=True)
class ReconcileQdto:
    drama_rel: str | None
    snapshot_synced_at: str | None
    snapshot_age_h: float | None
    stale: bool
    never_synced: bool
    mapped_count: int
    missing_count: int
    unmapped_count: int
    rows: tuple[ReconcileRowQdto, ...]
    unnamed_cards: tuple[UnnamedCardQdto, ...]
    config_issues: tuple[DramaConfigIssueQdto, ...]


@dataclass(frozen=True)
class EntitySnapshotEntryCdto:
    name: str
    thumbnail_url: str | None = None
    modified_at: str | None = None
