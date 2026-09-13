"""Research commands: record the user's decisions about a research dataset."""
from __future__ import annotations

from libs.infrastructure.writers.research__writer import ResearchWriter


class ResearchCommand:
    def __init__(self, writer: ResearchWriter) -> None:
        self._writer = writer

    def mark_series(
        self, dataset: str, slug: str, status: str | None, rating: int | None, note: str | None
    ) -> dict[str, object]:
        return self._writer.mark_series(dataset, slug, status, rating, note)

    def mark_video(
        self, dataset: str, video_id: str, bookmarked: bool | None, note: str | None
    ) -> dict[str, object]:
        return self._writer.mark_video(dataset, video_id, bookmarked, note)
