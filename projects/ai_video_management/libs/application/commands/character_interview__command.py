from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libs.common.writers_room_paths import bible_path
from libs.domain.entities.character_interview__entity import CharacterInterviewEntity
from libs.domain.errors.writers_room__error import WritersRoomError
from libs.infrastructure.readers.writers_room__reader import WritersRoomReader
from libs.infrastructure.writers.writers_room__writer import WritersRoomWriter


class CharacterInterviewCommand:
    def __init__(self, reader: WritersRoomReader, writer: WritersRoomWriter) -> None:
        self.reader, self.writer = reader, writer

    def answer(self, slug: str, character: str, question_id: str, answer: dict[str, Any], expected_revision: int) -> dict[str, Any]:
        try:
            with self.writer.lock(slug):
                detail = self.reader.detail(slug)
                if character not in {c["id"] for c in detail["seed"]["characters"]}:
                    raise WritersRoomError("人物不属于该剧。")
                if detail["job"] and detail["job"].get("status") == "running":
                    raise WritersRoomError("编剧室运行时不能修改其输入。", "running", 409)
                entity = CharacterInterviewEntity(**detail["answers"])
                entity.answer(character, question_id, answer, expected_revision)
                payload = asdict(entity)
                self.writer.json(bible_path(self.writer.root, slug) / "answers.json", payload)
                return payload
        except (ValueError, FileNotFoundError, RuntimeError) as exc:
            raise WritersRoomError(str(exc), "interview_write_failed", 409) from exc
