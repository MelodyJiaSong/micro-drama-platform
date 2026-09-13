"""Research queries: read-only views over the ai_videos/_research/ datasets."""
from __future__ import annotations

from libs.infrastructure.readers.research__reader import ResearchReader
from libs.infrastructure.writers.research__writer import ResearchWriter


class ResearchQuery:
    def __init__(self, reader: ResearchReader, writer: ResearchWriter) -> None:
        self._reader = reader
        self._writer = writer

    def workspace(self, dataset: str) -> dict[str, object]:
        return self._writer.workspace(dataset)

    def datasets(self) -> dict[str, object]:
        return {"datasets": self._reader.datasets()}

    def dataset(self, dataset: str) -> dict[str, object]:
        return self._reader.dataset(dataset)

    def series(self, dataset: str, slug: str) -> dict[str, object]:
        return self._reader.series(dataset, slug)
