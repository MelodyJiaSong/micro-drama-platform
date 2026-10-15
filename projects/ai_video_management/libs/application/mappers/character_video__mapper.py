"""Mappers for character-video results: infra dataclasses → application CDTOs."""
from __future__ import annotations

from libs.application.dtos.character_video__dto import (
    CharacterAudioCdto,
    CharacterTrimCdto,
    CharacterViewCdto,
    CharacterViewFailureCdto,
    ExtractAllCharacterViewsItemCdto,
    ExtractAllCharacterViewsResultCdto,
    ExtractCharacterViewsResultCdto,
)
from libs.infrastructure.writers.character_video__writer import (
    BatchViewExtractResult,
    ViewExtractResult,
)


class CharacterVideoMapper:
    @staticmethod
    def views_to_cdto(r: ViewExtractResult) -> ExtractCharacterViewsResultCdto:
        views = tuple(
            CharacterViewCdto(timestamp=v.timestamp, role=v.role, path=v.out_rel)
            for v in r.views
        )
        audio = CharacterAudioCdto(path=r.audio.out_rel) if r.audio is not None else None
        trim = (
            CharacterTrimCdto(path=r.trim.out_rel, duration_seconds=r.trim.duration_seconds)
            if r.trim is not None
            else None
        )
        failures = tuple(
            CharacterViewFailureCdto(target=t, error=e) for (t, e) in r.failures
        )
        return ExtractCharacterViewsResultCdto(
            src_rel=r.src_rel,
            views=views,
            audio=audio,
            trim=trim,
            failures=failures,
        )

    @staticmethod
    def extract_all_to_cdto(r: BatchViewExtractResult) -> ExtractAllCharacterViewsResultCdto:
        items = tuple(
            ExtractAllCharacterViewsItemCdto(
                folder=item.folder,
                status=item.status,
                result=(
                    CharacterVideoMapper.views_to_cdto(item.result)
                    if item.result is not None
                    else None
                ),
                reason=item.reason,
            )
            for item in r.items
        )
        return ExtractAllCharacterViewsResultCdto(characters_dir=r.characters_rel, items=items)
