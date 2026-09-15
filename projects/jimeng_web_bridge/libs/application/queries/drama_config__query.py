from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from libs.application.dtos.drama_config__dto import (
    CardEntityQdto,
    ConfigErrorQdto,
    DramaConfigAnalysisQdto,
    DramaConfigQdto,
    DramaEntitiesQdto,
    DramaTreeQdto,
    ReferencePreviewItemQdto,
    ShotReferencePreviewQdto,
)
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.common.drama_ref import canonical_rel_violation
from libs.common.enums import ReferenceResolver
from libs.common.paths import AI_VIDEOS_DIR_NAME, RepoSandbox
from libs.domain.errors.config__error import ConfigError, MissingAbbrevError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.drama_config_sections__valueobject import parse_drama
from libs.domain.value_objects.entity_naming__valueobject import EntityNaming
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.infrastructure.daos.drama_tree__dao import DramaNodeDao
from libs.infrastructure.daos.shot_prompt__dao import ReferenceItemDao
from libs.infrastructure.errors.config_io__error import ConfigParseError, DramaRootNotFoundError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import ShotParseError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader

_SHOT_STEM = re.compile(r"^shot\d+$")
_SERIES_EPISODE_DEPTH: int = 3

ConfigCache = dict[str, DramaConfig | None]


class DramaConfigQuery:
    """Read side of per-drama config: drama tree, stored config, and what a config would resolve to (FR-3, FR-8)."""

    def __init__(
        self,
        sandbox: RepoSandbox,
        tree_reader: DramaTreeReader,
        config_reader: DramaConfigReader,
        global_reader: GlobalConfigReader,
        shot_reader: ShotPromptReader,
        snapshot_reader: EntitySnapshotReader,
        mapper: DramaConfigMapper,
    ) -> None:
        self._sandbox = sandbox
        self._tree = tree_reader
        self._configs = config_reader
        self._global = global_reader
        self._shots = shot_reader
        self._snapshots = snapshot_reader
        self._mapper = mapper

    def list_dramas(self) -> DramaTreeQdto:
        return self._mapper.tree(self._tree.list_dramas())

    def drama_root(self, drama_rel: str) -> str:
        """Canonical `/`-joined drama root (already URL-decoded once by the caller); the `ai_videos/` prefix is optional.

        Escapes raise SandboxError (403); anything that is not exactly a drama root raises DramaRootNotFoundError (404).
        """
        violation = canonical_rel_violation(drama_rel)
        if violation is not None:
            raise SandboxError(violation, None)
        rel = drama_rel if drama_rel.split("/", 1)[0] == AI_VIDEOS_DIR_NAME else f"{AI_VIDEOS_DIR_NAME}/{drama_rel}"
        verdict = self._sandbox.check_read(rel)
        if verdict.path is None or verdict.rel is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        self._configs.config_rel(rel)
        if verdict.rel != rel or not verdict.path.is_dir() or not self._tree.search_bases(rel):
            raise DramaRootNotFoundError(rel)
        return rel

    def model_limits(self) -> ModelLimits:
        return ModelLimits.from_table(ConfigTable.of(self._global.read().data).table("model_limits"))

    def default_data(self, drama_rel: str) -> dict[str, object]:
        parts = self.drama_root(drama_rel).split("/")
        abbrev = parts[-1] if len(parts) == _SERIES_EPISODE_DEPTH else ""
        try:
            parse_drama(ConfigTable.of({"drama": {"abbrev": abbrev}}))
        except ConfigError:
            abbrev = ""
        return DramaConfig.defaults(abbrev)

    def get(self, drama_rel: str) -> DramaConfigQdto:
        root = self.drama_root(drama_rel)
        location = self._configs.config_rel(root)
        try:
            stored = self._configs.read(root)
        except ConfigParseError as error:
            return DramaConfigQdto(root, location, True, {}, None, None, error.detail, None, (), (), ())
        analysis = self.analyze(root, stored.data if stored.exists else self.default_data(root))
        return DramaConfigQdto(
            drama_rel=root,
            location=location,
            exists=stored.exists,
            data=stored.data,
            raw_text=stored.raw_text,
            sha256=stored.sha256,
            parse_error=None,
            validation_error=analysis.validation_error,
            needs_confirmation=analysis.needs_confirmation,
            entities=analysis.entities,
            reference_preview=analysis.reference_preview,
        )

    def analyze(self, drama_rel: str, data: Mapping[str, object]) -> DramaConfigAnalysisQdto:
        """What `data` would mean for this drama: validation, needs-confirmation items, naming, reference preview."""
        root = self.drama_root(drama_rel)
        limits = self.model_limits()
        try:
            config = DramaConfig.from_dict(data, limits)
        except ConfigError as error:
            return DramaConfigAnalysisQdto(root, self._mapper.config_error(error), (), (), ())
        snapshot = self._snapshot_names()
        entities = self._card_entities(root, config, limits, snapshot, {})
        preview = self._reference_preview(root, config, entities)
        confirmations = (
            *self._mapper.abbrev_confirmations(config),
            *self._mapper.entity_confirmations(entities, snapshot, config.precheck.entity_name_max_chars),
            *self._mapper.reference_confirmations(preview),
        )
        return DramaConfigAnalysisQdto(root, None, confirmations, entities, preview)

    def all_card_entities(self) -> tuple[DramaEntitiesQdto, ...]:
        """Expected entity names of every listable drama (FR-48); references are not resolved, so this stays cheap."""
        limits = self.model_limits()
        cache: ConfigCache = {}
        results: list[DramaEntitiesQdto] = []
        for drama_rel in _drama_paths(self._tree.list_dramas()):
            config, issue = self._effective_config(drama_rel, limits)
            overrides = config.references.routing.overrides.values()
            results.append(
                DramaEntitiesQdto(
                    drama_rel=drama_rel,
                    config_error=issue,
                    entities=self._card_entities(drama_rel, config, limits, None, cache),
                    reference_entity_names=tuple(sorted({o.entity_name for o in overrides if o.entity_name})),
                )
            )
        return tuple(results)

    def _effective_config(self, drama_rel: str, limits: ModelLimits) -> tuple[DramaConfig, ConfigErrorQdto | None]:
        issue: ConfigErrorQdto | None = None
        try:
            stored = self._configs.read(drama_rel)
            if stored.exists:
                return DramaConfig.from_dict(stored.data, limits), None
        except ConfigParseError as error:
            issue = ConfigErrorQdto("config_parse_error", error.location, error.detail)
        except ConfigError as error:
            issue = self._mapper.config_error(error)
        return DramaConfig.from_dict(self.default_data(drama_rel), limits), issue

    def _stored_config(self, drama_rel: str, limits: ModelLimits, cache: ConfigCache) -> DramaConfig | None:
        if drama_rel not in cache:
            try:
                stored = self._configs.read(drama_rel)
                cache[drama_rel] = DramaConfig.from_dict(stored.data, limits) if stored.exists else None
            except (ConfigParseError, ConfigError, DramaRootNotFoundError, SandboxError):
                cache[drama_rel] = None
        return cache[drama_rel]

    def _card_entities(
        self,
        drama_rel: str,
        config: DramaConfig,
        limits: ModelLimits,
        snapshot: frozenset[str] | None,
        cache: ConfigCache,
    ) -> tuple[CardEntityQdto, ...]:
        own = config.entity_naming
        results: list[CardEntityQdto] = []
        for card in self._tree.character_cards(drama_rel):
            naming = own
            source = card.linked_source_drama
            if source is not None and card.dir_name not in own.overrides:
                source_config = self._stored_config(source, limits, cache)
                naming = EntityNaming.for_linked_card(
                    None if source_config is None else source_config.entity_naming,
                    source.rsplit("/", 1)[-1],
                    own.name_template,
                )
            try:
                name = naming.entity_name(card.dir_name)
            except MissingAbbrevError as error:
                results.append(
                    CardEntityQdto(
                        card.dir_name, card.dir_rel, None, naming.abbrev, source, None, error.error_code, error.field_path
                    )
                )
                continue
            in_snapshot = None if snapshot is None else name in snapshot
            results.append(CardEntityQdto(card.dir_name, card.dir_rel, name, naming.abbrev, source, in_snapshot, None, None))
        return tuple(results)

    def _snapshot_names(self) -> frozenset[str] | None:
        if self._snapshots.last_synced_at() is None:
            return None
        return frozenset(record.name for record in self._snapshots.all())

    def _reference_preview(
        self, drama_rel: str, config: DramaConfig, entities: Sequence[CardEntityQdto]
    ) -> tuple[ShotReferencePreviewQdto, ...]:
        prefix = f"{drama_rel}/"
        shots = [
            entry.rel
            for entry in self._tree.list_files(drama_rel, config.references.search_exclude)
            if entry.ext == ".md" and not entry.is_link and _SHOT_STEM.match(entry.stem) and entry.rel.startswith(prefix)
        ]
        names = {entity.card_rel: entity.entity_name for entity in entities}
        return tuple(self._shot_preview(drama_rel, rel, config, names) for rel in shots)

    def _shot_preview(
        self, drama_rel: str, shot_rel: str, config: DramaConfig, names: Mapping[str, str | None]
    ) -> ShotReferencePreviewQdto:
        shot_dir, file_name = shot_rel.rsplit("/", 1)
        shot = file_name.removesuffix(".md")
        try:
            parsed = self._shots.read(shot_rel)
        except ShotParseError as error:
            return ShotReferencePreviewQdto(shot_rel, shot, error.code, False, (), ())
        except SandboxError as error:
            return ShotReferencePreviewQdto(shot_rel, shot, error.reason, False, (), ())
        line = parsed.references
        items = [self._item(drama_rel, shot_dir, reference, config, names) for reference in line.items]
        items.extend(self._mapper.legacy_item(legacy) for legacy in line.legacy)
        return ShotReferencePreviewQdto(shot_rel, shot, None, line.integrity_ok, line.unrecognized, tuple(items))

    def _item(
        self,
        drama_rel: str,
        shot_dir: str,
        reference: ReferenceItemDao,
        config: DramaConfig,
        names: Mapping[str, str | None],
    ) -> ReferencePreviewItemQdto:
        route = config.references.routing.route(reference.name, reference.label)
        if route is None:
            return self._mapper.unmatched_item(reference)
        if route.override is not None:
            return self._mapper.override_item(reference, route, self._existing_file(route.override.target_path))
        exclude = config.references.search_exclude
        if route.resolver is ReferenceResolver.ASSET_FILE:
            result = self._tree.resolve_asset_file(drama_rel, reference.name, exclude)
        elif route.resolver is ReferenceResolver.SHOT_VIDEO:
            result = self._tree.resolve_shot_video(shot_dir, reference.name, exclude)
        elif route.resolver is ReferenceResolver.PREV_SHOT_LASTFRAME:
            result = self._tree.resolve_prev_shot_lastframe(shot_dir, reference.name)
        else:
            card = self._tree.find_character_card(drama_rel, reference.name)
            entity_name = None if card.path is None else names.get(card.path)
            return self._mapper.resolved_item(reference, route, card, entity_name)
        return self._mapper.resolved_item(reference, route, result, None)

    def _existing_file(self, target_rel: str | None) -> str | None:
        if target_rel is None:
            return None
        verdict = self._sandbox.check_read(target_rel)
        if verdict.path is None or not verdict.path.is_file():
            return None
        return verdict.rel


def _drama_paths(nodes: Sequence[DramaNodeDao]) -> list[str]:
    paths: list[str] = []
    for node in nodes:
        if node.node_type == "series":
            paths.extend(_drama_paths(node.children))
        else:
            paths.append(node.path)
    return paths
