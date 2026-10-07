from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from libs.common.writers_room import interview_questions
from libs.domain.errors.writers_room__error import WritersRoomError


@dataclass
class CharacterInterviewEntity:
    revision: int
    characters: dict[str, dict[str, dict[str, Any]]]

    def answer(self, character: str, question_id: str, answer: dict[str, Any], expected_revision: int) -> None:
        if self.revision != expected_revision:
            raise WritersRoomError("答案已在另一窗口更新，请重新载入。", "stale_answers", 409)
        question = next((q for q in interview_questions() if q["id"] == question_id), None)
        if question is None:
            raise WritersRoomError("问题不存在。")
        options = {item["value"] for item in question["options"]}
        choice = answer.get("choice", "")
        note = answer.get("note", "")
        if choice not in options | {"custom"} or not isinstance(note, str) or len(note) > 5000 or (choice == "custom" and not note.strip()):
            raise WritersRoomError("请选择选项，或填写自己的答案。")
        self.characters.setdefault(character, {})[question_id] = {"choice": choice, "note": note.strip()}
        self.revision += 1
