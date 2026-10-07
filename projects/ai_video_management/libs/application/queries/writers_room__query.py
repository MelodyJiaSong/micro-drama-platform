from __future__ import annotations

from typing import Any
from libs.common.writers_room import interview_questions
from libs.domain.errors.writers_room__error import WritersRoomError
from libs.infrastructure.readers.writers_room__reader import WritersRoomReader


class WritersRoomQuery:
    def __init__(self, reader: WritersRoomReader) -> None:
        self.reader = reader

    def list(self) -> list[dict[str, Any]]:
        return self.reader.list()

    def detail(self, slug: str) -> dict[str, Any]:
        try:
            return dict(self.reader.detail(slug), questions=interview_questions())
        except FileNotFoundError as exc:
            raise WritersRoomError(str(exc), "not_found", 404) from exc
        except ValueError as exc:
            raise WritersRoomError(str(exc)) from exc

    def script(self, slug: str, revision: str) -> str:
        try:
            return self.reader.script(slug, revision)
        except (ValueError, FileNotFoundError) as exc:
            raise WritersRoomError(str(exc)) from exc
