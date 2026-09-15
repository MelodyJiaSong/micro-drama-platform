from __future__ import annotations

import re
from pathlib import PurePosixPath

from libs.application.errors.batch__error import BatchItemRejectedError
from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache
from libs.application.mappers.request_reference__mapper import (
    MappedRequest,
    ReferenceRequestMapper,
    ResolvedReferences,
)
from libs.common.enums import GenerationKind, RefKind, SourceType
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.drama_config_generation__valueobject import ImageBlockOverride, VideoBlockMatch
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config_sections__valueobject import RoutingSection
from libs.domain.value_objects.precheck_context__valueobject import ReferenceIssue
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.daos.asset_card__dao import AssetBlockDao, AssetCardDao
from libs.infrastructure.readers.asset_card__reader import AssetCardReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader

VIDEO_REFERENCE_KEY: str = "assets.video_reference"
_FOLDER_NUMBER_RE = re.compile(r"^(?:bg|c|p)(\d+)$", re.IGNORECASE)
_FIELD_MARKS: str = ":："
DEFAULT_VIDEO_REFERENCE_LABEL: str = "同卡立绘"
IMAGE_REFERENCE_LABEL: str = "image2image 参考图"


class AssetRequestMapper:
    """One routing-key block of a subject card → an image (CLI) or turntable video (routing.video) request (FR-9)."""

    def __init__(self, reader: AssetCardReader, tree: DramaTreeReader, references: ReferenceRequestMapper) -> None:
        self._reader: AssetCardReader = reader
        self._tree: DramaTreeReader = tree
        self._references: ReferenceRequestMapper = references

    def map(self, card_path: str, key: str, dramas: DramaSettingsCache, routing: RoutingSection) -> MappedRequest:
        card: AssetCardDao = self._reader.read(card_path)
        drama_rel: str | None = self._tree.drama_root_of(card.source_rel)
        if drama_rel is None:
            raise BatchItemRejectedError("not_in_drama", f"{card.source_rel} 不在任何剧目录下")
        blocks: list[AssetBlockDao] = [block for block in card.blocks if block.key == key]
        if len(blocks) != 1:
            reason = "asset_block_not_found" if not blocks else "asset_block_duplicate"
            raise BatchItemRejectedError(reason, f"{card.source_rel} 里以 {key} 开头的块有 {len(blocks)} 个，必须恰好 1 个")
        block: AssetBlockDao = blocks[0]
        settings: DramaSettings = dramas.get(drama_rel)
        config: DramaConfig = settings.config
        card_dir: str = card.source_rel.rpartition("/")[0]
        line_issues, legacy = self._references.line_issues(block.references)
        slot: str = f"{card_dir}#{key}"
        if _is_video_block(block, config.assets.video_block_match):
            references, issues = self._video_reference(card, card_dir, block, config)
            default = config.assets.video_default
            params = GenerationParams(
                model=default.model,
                ratio=block.ratio or default.ratio,
                resolution=default.resolution,
                count=config.video.count,
                duration_s=block.duration_s or default.duration_s,
            )
            kind, source_type, backend = GenerationKind.VIDEO, SourceType.ASSET_VIDEO, routing.video
        else:
            if card.subject_kind is None:
                raise BatchItemRejectedError(
                    "asset_subject_kind_unknown", f"{card.source_rel} 不在 characters/ props/ scenes/ 下，无法确定比例"
                )
            override: ImageBlockOverride | None = config.image.block_overrides.get(key)
            references, issues = self._image_references(drama_rel, key, override, config)
            params = GenerationParams(
                model=override.model if override is not None and override.model else config.image.model,
                ratio=override.ratio if override is not None and override.ratio else config.image.ratio_by_subject[card.subject_kind],
                resolution=config.image.resolution,
                count=config.image.count,
            )
            kind, source_type, backend = GenerationKind.IMAGE, SourceType.ASSET_IMAGE, routing.image
        request = GenerationRequest(
            kind=kind,
            prompt=block.body,
            negative_prompt=None,
            references=references,
            params=params,
            output_slot=slot,
            source=RequestSource(source_type, card.source_rel, key),
        )
        resolved = ResolvedReferences(references, (*line_issues, *issues), legacy)
        return MappedRequest(request, backend, settings, card_dir, resolved)

    def _video_reference(
        self, card: AssetCardDao, card_dir: str, block: AssetBlockDao, config: DramaConfig
    ) -> tuple[tuple[ReferenceItem, ...], tuple[ReferenceIssue, ...]]:
        template: str = config.assets.video_reference
        match = _FOLDER_NUMBER_RE.match(card.folder_key or "")
        if match is None and "{N}" in template:
            message = f"{card.card_dir_name} 不是 c{{N}}_… 形式的主体目录，无法按 {VIDEO_REFERENCE_KEY} 找同卡立绘"
            return (), (ReferenceIssue("reference_not_found", message, None, VIDEO_REFERENCE_KEY),)
        pattern: str = template.format(card_dir=card_dir, N=match.group(1) if match else "")
        hits: tuple[str, ...] = self._references.card_images(pattern)
        if len(hits) != 1:
            code = "reference_not_found" if not hits else "ambiguous_reference"
            detail = "找不到" if not hits else f"命中多个文件（{'、'.join(hits)}）"
            message = f"同卡立绘 {pattern} {detail}"
            return (), (ReferenceIssue(code, message, None, VIDEO_REFERENCE_KEY),)
        items = block.references.items
        label: str = items[0].label if len(items) == 1 else DEFAULT_VIDEO_REFERENCE_LABEL
        reference = self._references.file_reference(PurePosixPath(hits[0]).stem, label, RefKind.IMAGE, hits[0])
        return (reference,), ()

    def _image_references(
        self, drama_rel: str, key: str, override: ImageBlockOverride | None, config: DramaConfig
    ) -> tuple[tuple[ReferenceItem, ...], tuple[ReferenceIssue, ...]]:
        if override is None or not override.reference_keys:
            return (), ()
        config_key: str = key_path(key_path("image.block_overrides", key), "reference_keys")
        items: list[ReferenceItem] = []
        issues: list[ReferenceIssue] = []
        for reference_key in override.reference_keys:
            found = self._tree.resolve_asset_file(drama_rel, reference_key, config.references.search_exclude)
            item, issue = self._references.from_result(found, IMAGE_REFERENCE_LABEL, RefKind.IMAGE, config_key)
            if item is not None:
                items.append(item)
            if issue is not None:
                issues.append(issue)
        return tuple(items), tuple(issues)


def _is_video_block(block: AssetBlockDao, match: VideoBlockMatch) -> bool:
    first_line: str = block.first_line.casefold()
    if any(needle.casefold() in first_line for needle in match.first_line_contains):
        return True
    fields: set[str] = {name.rstrip(_FIELD_MARKS) for name in block.fields}
    return any(wanted.rstrip(_FIELD_MARKS) in fields for wanted in match.has_field)
