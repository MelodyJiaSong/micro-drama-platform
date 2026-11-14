"""排行榜预览（follow-up 320）：系列总览或单期审片数据。只读。"""
from __future__ import annotations

from libs.application.dtos.rank_preview__dto import RankPreviewQdto
from libs.infrastructure.readers.rank_preview__reader import RankPreviewReader


class RankPreviewQuery:
    def __init__(self, reader: RankPreviewReader) -> None:
        self.reader = reader

    def read(self, path: str) -> RankPreviewQdto:
        return self.reader.read(path)
