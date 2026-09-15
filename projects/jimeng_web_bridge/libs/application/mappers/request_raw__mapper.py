from __future__ import annotations

from collections.abc import Mapping
from pathlib import PurePosixPath

from libs.application.dtos.batch__dto import RawItemInput
from libs.application.errors.batch__error import BatchItemRejectedError
from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache
from libs.application.mappers.request_reference__mapper import (
    MappedRequest,
    ReferenceRequestMapper,
    ResolvedReferences,
)
from libs.common.enums import GenerationKind, RefKind, SourceType
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config_sections__valueobject import RoutingSection
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.link_json__reader import AUDIO_EXTS, IMAGE_EXTS, VIDEO_EXTS

RAW_REFERENCE_LABEL: str = "原始参考"
RAW_ENTITY_LABEL: str = "主体"
_KINDS: Mapping[str, GenerationKind] = {"video": GenerationKind.VIDEO, "image": GenerationKind.IMAGE}
_REF_KIND_BY_EXT: Mapping[str, RefKind] = {
    **{ext: RefKind.IMAGE for ext in IMAGE_EXTS},
    **{ext: RefKind.VIDEO for ext in VIDEO_EXTS},
    **{ext: RefKind.AUDIO for ext in AUDIO_EXTS},
}
_PARAM_KEYS: frozenset[str] = frozenset({"model", "ratio", "resolution", "count", "duration_s", "reference_mode"})


class RawRequestMapper:
    """FR-7 raw input: ordered files (sandboxed by the caller), then explicit entity names, in `=>@` order."""

    def __init__(self, tree: DramaTreeReader, references: ReferenceRequestMapper) -> None:
        self._tree: DramaTreeReader = tree
        self._references: ReferenceRequestMapper = references

    def map(self, item: RawItemInput, dramas: DramaSettingsCache, routing: RoutingSection) -> MappedRequest:
        kind: GenerationKind | None = _KINDS.get(item.kind)
        if kind is None:
            raise BatchItemRejectedError("raw_kind_invalid", f"kind 只能是 video 或 image，实际 {item.kind!r}")
        settings: DramaSettings = dramas.get(self._tree.drama_root_of(item.output_dir))
        references: tuple[ReferenceItem, ...] = (
            *(self._file(path) for path in item.reference_paths),
            *(ReferenceItem(name=name, label=RAW_ENTITY_LABEL, kind=RefKind.ENTITY, entity_name=name) for name in item.entity_names),
        )
        request = GenerationRequest(
            kind=kind,
            prompt=item.prompt,
            negative_prompt=item.negative_prompt,
            references=references,
            params=_params(item.params, kind, settings.config),
            output_slot=item.output_dir,
            source=RequestSource(SourceType.RAW, item.output_dir),
        )
        backend = routing.video if kind is GenerationKind.VIDEO else routing.image
        return MappedRequest(request, backend, settings, item.output_dir, ResolvedReferences(references))

    def _file(self, rel: str) -> ReferenceItem:
        path = PurePosixPath(rel)
        ref_kind: RefKind | None = _REF_KIND_BY_EXT.get(path.suffix.lower())
        if ref_kind is None:
            raise BatchItemRejectedError("reference_kind_unknown", f"{rel} 不是支持的图片 / 视频 / 音频文件")
        return self._references.file_reference(path.stem, RAW_REFERENCE_LABEL, ref_kind, rel)


def _params(raw: Mapping[str, object], kind: GenerationKind, config: DramaConfig) -> GenerationParams:
    unknown: list[str] = sorted(set(raw) - _PARAM_KEYS)
    if unknown:
        raise BatchItemRejectedError("raw_params_invalid", f"params 里有未知键 {unknown[0]}")
    video: bool = kind is GenerationKind.VIDEO
    ratio: str | None = _text(raw, "ratio")
    if ratio is None:
        raise BatchItemRejectedError("raw_params_invalid", "params.ratio 必填")
    count: int | None = _integer(raw, "count")
    default_count: int = config.video.count if video else config.image.count
    return GenerationParams(
        model=_text(raw, "model") or (config.video.model if video else config.image.model),
        ratio=ratio,
        resolution=_text(raw, "resolution") or (config.video.resolution if video else config.image.resolution),
        count=default_count if count is None else count,
        duration_s=_integer(raw, "duration_s"),
        reference_mode=_text(raw, "reference_mode"),
    )


def _text(raw: Mapping[str, object], key: str) -> str | None:
    value: object = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise BatchItemRejectedError("raw_params_invalid", f"params.{key} 必须是字符串")
    return value


def _integer(raw: Mapping[str, object], key: str) -> int | None:
    value: object = raw.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise BatchItemRejectedError("raw_params_invalid", f"params.{key} 必须是整数")
    return value
