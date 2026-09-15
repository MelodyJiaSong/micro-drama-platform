from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from typing import cast

import tomlkit

from libs.application.dtos.drama_config__dto import (
    CardEntityQdto,
    ConfigDiffItemCdto,
    ConfigErrorQdto,
    DramaNodeQdto,
    DramaTreeQdto,
    NeedsConfirmationQdto,
    ReferencePreviewItemQdto,
    ShotReferencePreviewQdto,
)
from libs.common.enums import ReferenceResolver, RefKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.repositories.drama_config__repository import StoredDramaConfig
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.reference_routing__valueobject import ENTITY_PREFIX, ReferenceRoute
from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.daos.drama_tree__dao import DramaNodeDao, ResolveResultDao
from libs.infrastructure.daos.shot_prompt__dao import LegacyReferenceDao, ReferenceItemDao

REFERENCE_OVERRIDES: str = "references.overrides"
ENTITY_OVERRIDES: str = "entities.overrides"
SYNC_KEY: str = "entities.sync"
PROPOSAL_HEADER: str = "jimeng_web_bridge 每剧 config（spec v2 FR-2）。由「生成默认 config」提议；先处理需要确认的项，再保存。"
LEGACY_MESSAGE: str = "v1 只支持现行写法，请把该镜 `参考:` 行改为 `{名}({类型})=>@`"

# Empty-by-default maps hold the user's decisions, so a proposal keeps them instead of suggesting their removal.
_CARRY_OVER: tuple[tuple[str, str], ...] = (
    ("entities", "overrides"),
    ("references", "overrides"),
    ("image", "block_overrides"),
)
_FIXABLE: frozenset[str] = frozenset({"not_found", "ambiguous", "link_invalid"})
_REFERENCE_CODES: dict[str, str] = {
    "not_found": "reference_not_found",
    "ambiguous": "ambiguous_reference",
    "link_invalid": "reference_link_invalid",
}


class DramaConfigMapper:
    def tree(self, nodes: Sequence[DramaNodeDao]) -> DramaTreeQdto:
        return DramaTreeQdto(dramas=tuple(self._node(node) for node in nodes))

    def config_error(self, error: ConfigError) -> ConfigErrorQdto:
        return ConfigErrorQdto(error_code=error.error_code, field_path=error.field_path, message=error.message)

    def stored(self, dao: ConfigFileDao) -> StoredDramaConfig | None:
        if not dao.exists or dao.sha256 is None:
            return None
        return StoredDramaConfig(data=dao.data, content_hash=dao.sha256)

    def carry_over(self, defaults: Mapping[str, object], current: Mapping[str, object]) -> dict[str, object]:
        proposed: dict[str, object] = copy.deepcopy(dict(defaults))
        abbrev = _lookup(current, "drama", "abbrev")
        if isinstance(abbrev, str) and abbrev:
            _table(proposed, "drama")["abbrev"] = abbrev
        for section, key in _CARRY_OVER:
            value = _lookup(current, section, key)
            if isinstance(value, Mapping) and value:
                _table(proposed, section)[key] = copy.deepcopy(dict(value))
        return proposed

    def toml_text(self, data: Mapping[str, object]) -> str:
        document = tomlkit.document()
        document.add(tomlkit.comment(PROPOSAL_HEADER))
        for key, value in data.items():
            document.add(key, value)
        return document.as_string()

    def diff(self, current: Mapping[str, object], proposed: Mapping[str, object]) -> tuple[ConfigDiffItemCdto, ...]:
        left, right = _flatten(current, ""), _flatten(proposed, "")
        items: list[ConfigDiffItemCdto] = []
        for key, value in right.items():
            if key not in left:
                items.append(ConfigDiffItemCdto(key=key, change="added", current=None, proposed=value))
            elif not _same(left[key], value):
                items.append(ConfigDiffItemCdto(key=key, change="changed", current=left[key], proposed=value))
        items.extend(
            ConfigDiffItemCdto(key=key, change="removed", current=value, proposed=None)
            for key, value in left.items()
            if key not in right
        )
        return tuple(items)

    def abbrev_confirmations(self, config: DramaConfig) -> tuple[NeedsConfirmationQdto, ...]:
        naming = config.entity_naming
        if naming.abbrev or "{abbrev}" not in naming.name_template:
            return ()
        return (
            NeedsConfirmationQdto(
                code="drama_abbrev_missing",
                key="drama.abbrev",
                config_key="drama.abbrev",
                reason="独立剧缺少缩写 drama.abbrev，无法按 entities.name_template 生成主体名",
                suggestion="填写 1–16 位字母、数字或下划线组成的缩写",
            ),
        )

    def entity_confirmations(
        self, entities: Sequence[CardEntityQdto], snapshot_names: frozenset[str] | None, max_chars: int
    ) -> tuple[NeedsConfirmationQdto, ...]:
        if snapshot_names is None:
            return (
                NeedsConfirmationQdto(
                    code="entities_never_synced",
                    key=SYNC_KEY,
                    config_key=None,
                    reason="从来没有同步过即梦主体列表，无法检测期望主体名是否与平台上已有的主体冲突",
                    suggestion="先在「主体对账」页同步主体，再重新生成默认 config",
                ),
            )
        mapped = frozenset(entity.entity_name for entity in entities if entity.entity_name is not None)
        items: list[NeedsConfirmationQdto] = []
        for entity in entities:
            name = entity.entity_name
            if name is None:
                continue
            key = key_path(ENTITY_OVERRIDES, entity.character_dir)
            if len(name) > max_chars:
                items.append(
                    NeedsConfirmationQdto(
                        code="entity_name_too_long",
                        key=key,
                        config_key=key,
                        reason=f"期望主体名「{name}」超过 {max_chars} 码点",
                        suggestion=f"在 {key} 填写不超过 {max_chars} 码点的主体名",
                    )
                )
            if name in snapshot_names or not entity.naming_abbrev:
                continue
            others = sorted(
                other for other in snapshot_names if other.startswith(f"{entity.naming_abbrev}_") and other not in mapped
            )
            if others:
                items.append(
                    NeedsConfirmationQdto(
                        code="entity_name_conflict",
                        key=key,
                        config_key=key,
                        reason=f"期望主体名「{name}」不在主体快照里；可能已有同一角色的主体，名称不同，例如 {others[0]}",
                        suggestion=f'如果是同一角色，在 {key} 填写 "{others[0]}"',
                    )
                )
        return tuple(items)

    def reference_confirmations(
        self, previews: Sequence[ShotReferencePreviewQdto]
    ) -> tuple[NeedsConfirmationQdto, ...]:
        grouped: dict[str, tuple[ReferencePreviewItemQdto, list[str]]] = {}
        for preview in previews:
            for item in preview.items:
                if item.suggested_override_key is None:
                    continue
                shots = grouped.setdefault(item.suggested_override_key, (item, []))[1]
                if preview.shot not in shots:
                    shots.append(preview.shot)
        return tuple(
            NeedsConfirmationQdto(
                code=_reference_code(item),
                key=key,
                config_key=key,
                reason=item.message or "",
                suggestion=_reference_suggestion(item, key),
                shots=tuple(shots),
            )
            for key, (item, shots) in grouped.items()
        )

    def unmatched_item(self, reference: ReferenceItemDao) -> ReferencePreviewItemQdto:
        return _item(
            reference,
            status="not_found",
            reason="label_unmatched",
            message=f"类型标签「{reference.label}」没有匹配的 references.rules",
            suggested_override_key=key_path(REFERENCE_OVERRIDES, reference.name),
        )

    def override_item(
        self, reference: ReferenceItemDao, route: ReferenceRoute, resolved_rel: str | None
    ) -> ReferencePreviewItemQdto:
        override = route.override
        entity_name = None if override is None else override.entity_name
        if entity_name is not None or resolved_rel is not None:
            return _item(
                reference, kind=route.kind.value, status="found", resolved_path=resolved_rel,
                entity_name=entity_name, reason="override",
            )
        key = key_path(REFERENCE_OVERRIDES, reference.name)
        return _item(
            reference,
            kind=route.kind.value,
            status="not_found",
            reason="override_target_missing",
            message=f"{key} 指向的文件不存在或不在 ai_videos/ 沙箱内",
            suggested_override_key=key,
        )

    def resolved_item(
        self, reference: ReferenceItemDao, route: ReferenceRoute, result: ResolveResultDao, entity_name: str | None
    ) -> ReferencePreviewItemQdto:
        fixable = result.status in _FIXABLE and route.resolver is not ReferenceResolver.PREV_SHOT_LASTFRAME
        return _item(
            reference,
            kind=route.kind.value,
            resolver=None if route.resolver is None else route.resolver.value,
            status=result.status,
            resolved_path=result.path,
            link_path=result.link_path,
            entity_name=entity_name,
            candidates=result.candidates,
            reason=result.reason or result.step,
            message=_resolve_message(reference.name, route, result),
            suggested_override_key=key_path(REFERENCE_OVERRIDES, reference.name) if fixable else None,
        )

    def legacy_item(self, legacy: LegacyReferenceDao) -> ReferencePreviewItemQdto:
        return ReferencePreviewItemQdto(
            name=legacy.token, label="", kind=None, resolver=None, status="legacy", resolved_path=None,
            link_path=None, entity_name=None, candidates=(), reason=legacy.kind, message=LEGACY_MESSAGE,
            suggested_override_key=None,
        )

    def _node(self, node: DramaNodeDao) -> DramaNodeQdto:
        return DramaNodeQdto(
            name=node.name, path=node.path, type=node.node_type, children=tuple(self._node(c) for c in node.children)
        )


def _item(
    reference: ReferenceItemDao,
    *,
    status: str,
    kind: str | None = None,
    resolver: str | None = None,
    resolved_path: str | None = None,
    link_path: str | None = None,
    entity_name: str | None = None,
    candidates: tuple[str, ...] = (),
    reason: str | None = None,
    message: str | None = None,
    suggested_override_key: str | None = None,
) -> ReferencePreviewItemQdto:
    return ReferencePreviewItemQdto(
        name=reference.name, label=reference.label, kind=kind, resolver=resolver, status=status,
        resolved_path=resolved_path, link_path=link_path, entity_name=entity_name, candidates=candidates,
        reason=reason, message=message, suggested_override_key=suggested_override_key,
    )


def _resolve_message(name: str, route: ReferenceRoute, result: ResolveResultDao) -> str | None:
    if result.status == "found":
        return None
    if result.status == "ambiguous":
        return f"参考项「{name}」多重匹配（{len(result.candidates)} 个候选），需要在 references.overrides 指定其一"
    if result.status == "link_invalid":
        return f"参考项「{name}」命中的 .link.json 无效（{result.reason}）"
    if route.resolver is ReferenceResolver.PREV_SHOT_LASTFRAME:
        looked_for = f"：{result.looked_for}" if result.looked_for else ""
        return f"上一镜末帧不可用（{result.reason}）{looked_for}；v1 不支持同批次首帧链式依赖"
    return f"按默认规则找不到参考项「{name}」"


def _reference_code(item: ReferencePreviewItemQdto) -> str:
    if item.reason == "label_unmatched":
        return "reference_label_unmatched"
    if item.reason == "override_target_missing":
        return "reference_override_invalid"
    return _REFERENCE_CODES.get(item.status, "reference_unresolved")


def _reference_suggestion(item: ReferencePreviewItemQdto, key: str) -> str:
    if item.kind == RefKind.ENTITY.value:
        return f'在 {key} 填写 "{ENTITY_PREFIX}{{主体名}}"'
    if item.candidates:
        return f'在 {key} 填写其中一个候选，例如 "{item.candidates[0]}"'
    return f'在 {key} 填写 "ai_videos/…/文件.png" 或 "{ENTITY_PREFIX}{{主体名}}"'


def _lookup(data: Mapping[str, object], section: str, key: str) -> object:
    table = data.get(section)
    return table.get(key) if isinstance(table, Mapping) else None


def _table(data: dict[str, object], name: str) -> dict[str, object]:
    return cast(dict[str, object], data[name])


def _flatten(data: Mapping[str, object], parent: str) -> dict[str, object]:
    flat: dict[str, object] = {}
    for key, value in data.items():
        path = key_path(parent, str(key))
        if isinstance(value, Mapping) and value:
            flat.update(_flatten(value, path))
        else:
            flat[path] = value
    return flat


def _same(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right
