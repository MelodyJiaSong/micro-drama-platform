from __future__ import annotations

from libs.application.errors.batch__error import BatchItemRejectedError
from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache
from libs.application.mappers.request_reference__mapper import MappedRequest, ReferenceRequestMapper
from libs.common.enums import GenerationKind, SourceType
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config_sections__valueobject import RoutingSection
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader


class ShotRequestMapper:
    def __init__(self, reader: ShotPromptReader, tree: DramaTreeReader, references: ReferenceRequestMapper) -> None:
        self._reader: ShotPromptReader = reader
        self._tree: DramaTreeReader = tree
        self._references: ReferenceRequestMapper = references

    def map(self, shot_path: str, dramas: DramaSettingsCache, routing: RoutingSection) -> MappedRequest:
        shot = self._reader.read(shot_path)
        drama_rel: str | None = self._tree.drama_root_of(shot.source_rel)
        if drama_rel is None:
            raise BatchItemRejectedError("not_in_drama", f"{shot.source_rel} 不在任何剧目录下")
        ratio: str | None = shot.ratio or shot.ratio_raw
        if not ratio:
            raise BatchItemRejectedError("shot_ratio_missing", f"{shot.source_rel} 的 prompt 里没有 `比例:` 字段")
        settings: DramaSettings = dramas.get(drama_rel)
        video = settings.config.video
        shot_dir: str = shot.source_rel.rpartition("/")[0]
        references = self._references.resolve_shot(shot.references, drama_rel, shot_dir, dramas)
        request = GenerationRequest(
            kind=GenerationKind.VIDEO,
            prompt=shot.prompt,
            negative_prompt=shot.negative_prompt,
            references=references.items,
            params=GenerationParams(
                model=video.model,
                ratio=ratio,
                resolution=video.resolution,
                count=video.count,
                duration_s=shot.duration_s,
            ),
            output_slot=shot_dir,
            source=RequestSource(SourceType.SHOT, shot.source_rel),
        )
        return MappedRequest(request, routing.video, settings, shot_dir, references)
