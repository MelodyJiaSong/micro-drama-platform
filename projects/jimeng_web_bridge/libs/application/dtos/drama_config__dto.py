from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class DramaNodeQdto:
    name: str
    path: str
    type: str
    children: tuple[DramaNodeQdto, ...]


@dataclass(frozen=True)
class DramaTreeQdto:
    dramas: tuple[DramaNodeQdto, ...]


@dataclass(frozen=True)
class ConfigErrorQdto:
    error_code: str
    field_path: str
    message: str


@dataclass(frozen=True)
class NeedsConfirmationQdto:
    """`key` identifies the item for the UI; `config_key` is the TOML key to fill, None when the fix is not a config edit."""

    code: str
    key: str
    config_key: str | None
    reason: str
    suggestion: str | None
    shots: tuple[str, ...] = ()


@dataclass(frozen=True)
class CardEntityQdto:
    """Expected platform entity name of one character card; `entity_name` is None when it cannot be computed."""

    character_dir: str
    card_rel: str
    entity_name: str | None
    naming_abbrev: str
    source_drama_rel: str | None
    in_snapshot: bool | None
    error_code: str | None
    config_key: str | None


@dataclass(frozen=True)
class ReferencePreviewItemQdto:
    """`status`: found | not_found | ambiguous | link_invalid | legacy."""

    name: str
    label: str
    kind: str | None
    resolver: str | None
    status: str
    resolved_path: str | None
    link_path: str | None
    entity_name: str | None
    candidates: tuple[str, ...]
    reason: str | None
    message: str | None
    suggested_override_key: str | None


@dataclass(frozen=True)
class ShotReferencePreviewQdto:
    shot_rel: str
    shot: str
    parse_error: str | None
    integrity_ok: bool
    unrecognized: tuple[str, ...]
    items: tuple[ReferencePreviewItemQdto, ...]


@dataclass(frozen=True)
class DramaConfigAnalysisQdto:
    drama_rel: str
    validation_error: ConfigErrorQdto | None
    needs_confirmation: tuple[NeedsConfirmationQdto, ...]
    entities: tuple[CardEntityQdto, ...]
    reference_preview: tuple[ShotReferencePreviewQdto, ...]


@dataclass(frozen=True)
class DramaEntitiesQdto:
    """Card naming for one drama under its effective config (stored, or defaults when absent/invalid)."""

    drama_rel: str
    config_error: ConfigErrorQdto | None
    entities: tuple[CardEntityQdto, ...]
    reference_entity_names: tuple[str, ...]


@dataclass(frozen=True)
class DramaConfigQdto:
    drama_rel: str
    location: str
    exists: bool
    data: Mapping[str, object]
    raw_text: str | None
    sha256: str | None
    parse_error: str | None
    validation_error: ConfigErrorQdto | None
    needs_confirmation: tuple[NeedsConfirmationQdto, ...]
    entities: tuple[CardEntityQdto, ...]
    reference_preview: tuple[ShotReferencePreviewQdto, ...]


@dataclass(frozen=True)
class ConfigDiffItemCdto:
    """`change`: added | removed | changed. Values are plain TOML-compatible data."""

    key: str
    change: str
    current: object
    proposed: object


@dataclass(frozen=True)
class ProposeCdto:
    drama_rel: str
    location: str
    exists: bool
    current_sha256: str | None
    current_parse_error: str | None
    proposed_data: Mapping[str, object]
    proposed_toml: str
    diff: tuple[ConfigDiffItemCdto, ...]
    validation_error: ConfigErrorQdto | None
    needs_confirmation: tuple[NeedsConfirmationQdto, ...]
    entities: tuple[CardEntityQdto, ...]
    reference_preview: tuple[ShotReferencePreviewQdto, ...]


@dataclass(frozen=True)
class SaveConfigCdto:
    drama_rel: str
    location: str
    sha256: str
