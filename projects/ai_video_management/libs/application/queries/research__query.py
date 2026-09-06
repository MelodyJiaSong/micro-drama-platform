"""Research queries: read-only views over the ai_videos/_research/ datasets."""
from __future__ import annotations

from libs.infrastructure.readers.research__reader import ResearchReader


class ResearchQuery:
    def __init__(self, reader: ResearchReader) -> None:
        self._reader = reader

    def datasets(self) -> dict[str, object]:
        return {"datasets": self._reader.datasets()}

    def dataset(self, dataset: str) -> dict[str, object]:
        return self._reader.dataset(dataset)

    def series(self, dataset: str, slug: str) -> dict[str, object]:
        return self._reader.series(dataset, slug)
