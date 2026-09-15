from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from fnmatch import fnmatchcase

from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache
from libs.common.enums import BackendKind, ReferenceResolver, RefKind
from libs.common.paths import RepoSandbox
from libs.domain.errors.config__error import MissingAbbrevError
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.entity_naming__valueobject import EntityNaming
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.precheck_context__valueobject import ReferenceIssue
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.domain.value_objects.reference_routing__valueobject import ReferenceRoute
from libs.infrastructure.daos.drama_tree__dao import CharacterCardDao, ResolveResultDao
from libs.infrastructure.daos.shot_prompt__dao import ReferenceLineDao
from libs.infrastructure.errors.sandbox__error import LinkRejectedError, SandboxError
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.readers.link_json__reader import IMAGE_EXTS

OVERRIDES_KEY: str = "references.overrides"
Resolution = tuple[ReferenceItem | None, ReferenceIssue | None]


@dataclass(frozen=True)
class ResolvedReferences:
    items: tuple[ReferenceItem, ...]
    issues: tuple[ReferenceIssue, ...] = ()
    legacy: tuple[str, ...] = ()
    entity_card_dirs: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MappedRequest:
    request: GenerationRequest
    backend: BackendKind
    settings: DramaSettings
    output_dir: str | None
    references: ResolvedReferences


class ReferenceRequestMapper:
    """`参考:` items → ReferenceItems via config routing and the U2 resolvers; failures become ReferenceIssues."""

    def __init__(self, sandbox: RepoSandbox, tree: DramaTreeReader, files: FileIndexReader) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._tree: DramaTreeReader = tree
        self._files: FileIndexReader = files

    def line_issues(self, line: ReferenceLineDao) -> tuple[list[ReferenceIssue], tuple[str, ...]]:
        legacy: tuple[str, ...] = tuple(entry.token for entry in line.legacy)
        issues: list[ReferenceIssue] = [
            ReferenceIssue("reference_line_unrecognized", f"`参考:` 行里有无法识别的片段：{fragment}")
            for fragment in line.unrecognized
        ]
        if not legacy and not line.unrecognized and not line.integrity_ok:
            issues.append(
                ReferenceIssue(
                    "reference_marker_mismatch",
                    f"prompt 里有 {line.marker_count} 个 `=>@`，`参考:` 行解析出 {len(line.items)} 项，两者必须相等",
                )
            )
        return issues, legacy

    def resolve_shot(
        self, line: ReferenceLineDao, drama_rel: str, shot_dir: str, dramas: DramaSettingsCache
    ) -> ResolvedReferences:
        config: DramaConfig = dramas.get(drama_rel).config
        issues, legacy = self.line_issues(line)
        items: list[ReferenceItem] = []
        card_dirs: dict[str, str] = {}
        for entry in line.items:
            item, issue, card_dir = self._resolve(entry.name, entry.label, drama_rel, shot_dir, config, dramas)
            if item is not None:
                items.append(item)
                if card_dir is not None and item.entity_name is not None:
                    card_dirs[item.entity_name] = card_dir
            if issue is not None:
                issues.append(issue)
        return ResolvedReferences(tuple(items), tuple(issues), legacy, card_dirs)

    def from_result(self, found: ResolveResultDao, label: str, kind: RefKind, config_key: str) -> Resolution:
        name: str = found.name
        if found.status == "found" and found.path is not None:
            return self.file_reference(name, label, kind, found.path), None
        placeholder = ReferenceItem(name=name, label=label, kind=kind)
        if found.status == "ambiguous":
            message = f"参考项 {name} 命中多个文件：{'、'.join(found.candidates)}；请在 config 里指定 {config_key}"
            return placeholder, ReferenceIssue("ambiguous_reference", message, name, config_key)
        if found.status == "link_invalid":
            message = f"参考项 {name} 的 {found.link_path} 无效（{found.reason}）"
            return placeholder, ReferenceIssue("reference_link_invalid", message, name, config_key)
        if kind is RefKind.FIRST_FRAME:
            message = (
                "本镜是第一镜，没有上一镜末帧"
                if found.reason == "first_shot"
                else f"上一镜末帧 {found.looked_for or ''} 不存在（v1 不支持同批次内的首帧链式依赖，请先完成上一镜）"
            )
            return placeholder, ReferenceIssue("first_frame_unavailable", message, name, config_key)
        return placeholder, ReferenceIssue("reference_not_found", f"找不到参考项 {name} 对应的文件", name, config_key)

    def file_reference(self, name: str, label: str, kind: RefKind, rel: str) -> ReferenceItem:
        return ReferenceItem(name=name, label=label, kind=kind, resolved_path=rel, sha256=self._sha256(rel))

    def naming_for(self, card: CharacterCardDao, config: DramaConfig, dramas: DramaSettingsCache) -> EntityNaming:
        source: str | None = card.linked_source_drama
        if source is None:
            return config.entity_naming
        source_settings: DramaSettings = dramas.get(source)
        source_naming: EntityNaming | None = (
            source_settings.config.entity_naming if source_settings.has_usable_file else None
        )
        return EntityNaming.for_linked_card(source_naming, source.split("/")[-1], config.entity_naming.name_template)

    def card_images(self, pattern: str) -> tuple[str, ...]:
        """Image files directly inside a card dir matching `{dir}/{glob}`; `.link.json` entries yield their target."""
        dir_rel, _, name_glob = pattern.rpartition("/")
        hits: list[str] = []
        for entry in self._files.list_files(dir_rel, ()):
            if entry.rel.rpartition("/")[0] != dir_rel or entry.ext not in IMAGE_EXTS:
                continue
            if not fnmatchcase(f"{entry.stem}{entry.ext}", name_glob):
                continue
            if not entry.is_link:
                hits.append(entry.rel)
                continue
            try:
                hits.append(self._tree.read_link(entry.rel).target_rel)
            except LinkRejectedError:
                continue
        return tuple(hits)

    def _resolve(
        self, name: str, label: str, drama_rel: str, shot_dir: str, config: DramaConfig, dramas: DramaSettingsCache
    ) -> tuple[ReferenceItem | None, ReferenceIssue | None, str | None]:
        # Bound first: the NFR static-ban test greps service source for Playwright's request-interception call token.
        route_for = config.references.routing.route
        route: ReferenceRoute | None = route_for(name, label)
        override_key: str = key_path(OVERRIDES_KEY, name)
        if route is None:
            message = f"参考项 {name}（{label}）的类型没有命中 references.rules"
            return None, ReferenceIssue("reference_label_unmatched", message, name, override_key), None
        if route.override is not None:
            item, issue = self._override(name, label, route, override_key)
            return item, issue, None
        if route.resolver is ReferenceResolver.ENTITY:
            return self._entity(name, label, drama_rel, config, dramas, override_key)
        excludes: tuple[str, ...] = config.references.search_exclude
        if route.resolver is ReferenceResolver.ASSET_FILE:
            found: ResolveResultDao = self._tree.resolve_asset_file(drama_rel, name, excludes)
        elif route.resolver is ReferenceResolver.SHOT_VIDEO:
            found = self._tree.resolve_shot_video(shot_dir, name, excludes)
        else:
            found = self._tree.resolve_prev_shot_lastframe(shot_dir, name)
        item, issue = self.from_result(found, label, route.kind, override_key)
        return item, issue, None

    def _override(self, name: str, label: str, route: ReferenceRoute, override_key: str) -> Resolution:
        override = route.override
        assert override is not None
        if override.entity_name is not None:
            return ReferenceItem(name=name, label=label, kind=RefKind.ENTITY, entity_name=override.entity_name), None
        target: str = override.target_path or ""
        verdict = self._sandbox.check_read(target)
        if verdict.rel is None or verdict.path is None or not verdict.path.is_file():
            message = f"{override_key} 指向的 {target} 不存在或不在 ai_videos/ 里"
            return ReferenceItem(name=name, label=label, kind=route.kind), ReferenceIssue(
                "reference_override_invalid", message, name, override_key
            )
        return self.file_reference(name, label, route.kind, verdict.rel), None

    def _entity(
        self, name: str, label: str, drama_rel: str, config: DramaConfig, dramas: DramaSettingsCache, override_key: str
    ) -> tuple[ReferenceItem | None, ReferenceIssue | None, str | None]:
        found: ResolveResultDao = self._tree.find_character_card(drama_rel, name)
        if found.status == "ambiguous":
            message = f"主体参考项 {name} 命中多个角色卡：{'、'.join(found.candidates)}"
            return None, ReferenceIssue("ambiguous_reference", message, name, override_key), None
        card: CharacterCardDao | None = next(
            (c for c in self._tree.character_cards(drama_rel) if c.dir_rel == found.path), None
        ) if found.status == "found" else None
        if card is None:
            message = f"找不到主体参考项 {name} 对应的角色卡"
            return None, ReferenceIssue("entity_card_not_found", message, name, override_key), None
        try:
            entity_name: str = self.naming_for(card, config, dramas).entity_name(card.dir_name)
        except MissingAbbrevError as error:
            return None, ReferenceIssue(error.error_code, error.message, name, error.field_path), card.dir_name
        item = ReferenceItem(name=name, label=label, kind=RefKind.ENTITY, entity_name=entity_name)
        return item, None, card.dir_name

    def _sha256(self, rel: str) -> str | None:
        try:
            return self._tree.sha256(rel)
        except SandboxError:
            return None
