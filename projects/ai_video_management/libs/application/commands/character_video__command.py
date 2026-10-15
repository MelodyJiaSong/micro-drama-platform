"""Character-video aggregate commands: extract a character turntable's views +
audio + trim (one video, or every character folder of a drama)."""
from __future__ import annotations

from libs.application.dtos.character_video__dto import (
    ExtractAllCharacterViewsResultCdto,
    ExtractCharacterViewsResultCdto,
)
from libs.application.mappers.character_video__mapper import CharacterVideoMapper
from libs.infrastructure.writers.character_video__writer import CharacterViewExtractor


class CharacterVideoCommand:
    def __init__(self, extractor: CharacterViewExtractor) -> None:
        self._extractor = extractor

    def extract_views(self, rel_path: str) -> ExtractCharacterViewsResultCdto:
        return CharacterVideoMapper.views_to_cdto(self._extractor.extract(rel_path))

    def extract_all_views(self, rel_path: str) -> ExtractAllCharacterViewsResultCdto:
        return CharacterVideoMapper.extract_all_to_cdto(self._extractor.extract_all(rel_path))
