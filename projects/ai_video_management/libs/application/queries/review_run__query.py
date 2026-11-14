from typing import Any

from libs.application.dtos.review_run__dto import ReviewRunQdto
from libs.infrastructure.readers.review_run__reader import ReviewRunReader


class ReviewRunQuery:
    def __init__(self, reader: ReviewRunReader) -> None:
        self._reader = reader

    def list(self) -> ReviewRunQdto:
        return ReviewRunQdto(self._reader.list().runs)

    def checklist(self, rel_dir: str) -> dict[str, Any] | None:
        return self._reader.checklist(rel_dir)
