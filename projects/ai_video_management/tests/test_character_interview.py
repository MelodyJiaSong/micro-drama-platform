from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from threading import Barrier

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.character_interview__command import CharacterInterviewCommand
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.common.writers_room import interview_questions
from libs.common.writers_room_paths import bible_path, room_path
from libs.domain.entities.character_interview__entity import CharacterInterviewEntity
from libs.domain.errors.writers_room__error import WritersRoomError
from libs.infrastructure.readers.writers_room__reader import WritersRoomReader
from libs.infrastructure.writers.writers_room__writer import WritersRoomWriter
from tests.conftest import make_app


@pytest.fixture
def room(tmp_path: Path):
    writer = WritersRoomWriter(tmp_path)
    writer.create({"slug": "alpha", "characters": [{"id": "a", "name": "甲"}, {"id": "b", "name": "乙"}]}, {})
    reader = WritersRoomReader(tmp_path)
    return tmp_path, writer, reader, CharacterInterviewCommand(reader, writer)


def test_answer_persists_per_character_and_can_be_modified(room):
    root, _, reader, command = room
    command.answer("alpha", "a", "identity_1", {"choice": "A", "note": " 经历 "}, 0)
    command.answer("alpha", "b", "identity_1", {"choice": "B", "note": ""}, 1)
    command.answer("alpha", "a", "identity_1", {"choice": "custom", "note": "自己的选择"}, 2)
    answers = WritersRoomReader(root).detail("alpha")["answers"]
    assert answers == {"revision": 3, "characters": {"a": {"identity_1": {"choice": "custom", "note": "自己的选择"}}, "b": {"identity_1": {"choice": "B", "note": ""}}}}
    assert reader.detail("alpha")["answers"] == answers


def test_stale_revision_cannot_overwrite_disk(room):
    root, _, reader, command = room
    command.answer("alpha", "a", "identity_1", {"choice": "A", "note": "原答案"}, 0)
    before = (bible_path(root, "alpha") / "answers.json").read_bytes()
    with pytest.raises(WritersRoomError) as failure:
        command.answer("alpha", "a", "identity_1", {"choice": "B", "note": "覆盖"}, 0)
    assert failure.value.kind == "stale_answers"
    assert (bible_path(root, "alpha") / "answers.json").read_bytes() == before
    assert reader.detail("alpha")["answers"]["revision"] == 1


@pytest.mark.parametrize("question,answer", [("missing", {"choice": "A", "note": ""}), ("identity_1", {"choice": "Z", "note": ""}), ("identity_1", {"choice": "custom", "note": "  "}), ("identity_1", {"choice": "A", "note": "x" * 5001})])
def test_invalid_answers_do_not_mutate_entity(question, answer):
    entity = CharacterInterviewEntity(0, {})
    before = deepcopy(entity)
    with pytest.raises(WritersRoomError):
        entity.answer("a", question, answer, 0)
    assert entity == before


@pytest.mark.parametrize("reason", ["unknown_character", "running"])
def test_input_changes_rejected_for_unknown_character_or_running_job(room, reason):
    root, writer, reader, command = room
    if reason == "running":
        writer.json(room_path(root, "alpha") / "job.json", {"status": "running"})
    with pytest.raises(WritersRoomError):
        command.answer("alpha", "ghost" if reason == "unknown_character" else "a", "identity_1", {"choice": "A", "note": ""}, 0)
    assert reader.detail("alpha")["answers"] == {"revision": 0, "characters": {}}


def test_two_concurrent_clients_cannot_both_overwrite_revision_zero(room):
    _, _, reader, command = room
    barrier = Barrier(2)
    def save(choice):
        barrier.wait(timeout=5)
        try:
            return command.answer("alpha", "a", "identity_1", {"choice": choice, "note": ""}, 0)
        except WritersRoomError as error:
            return error
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(save, ["A", "B"]))
    assert sum(isinstance(result, dict) for result in results) == 1
    assert reader.detail("alpha")["answers"]["revision"] == 1


@pytest.mark.parametrize("serve_static", [False, True])
def test_api_consumer_walk_and_revision_conflict(room, serve_static):
    root, _, _, _ = room
    with TestClient(make_app(RepoRoot(root), BoundOrigin("127.0.0.1", 8766), serve_static), base_url="http://127.0.0.1:8766") as client:
        assert client.get("/api/writers-room").json()[0]["slug"] == "alpha"
        detail = client.get("/api/writers-room/alpha").json()
        assert detail["seed"]["characters"][0]["id"] == "a"
        assert detail["answers"] == {"revision": 0, "characters": {}}
        for question in detail["questions"]:
            assert question["id"] and question["dimension"] and question["title"]
            assert isinstance(question["multiple"], bool)
            assert all(option["value"] and option["label"] for option in question["options"])
        body = {"character": "a", "question_id": interview_questions()[0]["id"], "choice": "C", "note": "保留", "expected_revision": 0}
        headers = {"Origin": "http://127.0.0.1:8766"}
        saved = client.put("/api/writers-room/alpha/answers", json=body, headers=headers)
        assert saved.status_code == 200, saved.text
        assert saved.json()["characters"]["a"][body["question_id"]] == {"choice": "C", "note": "保留"}
        stale = client.put("/api/writers-room/alpha/answers", json={**body, "choice": "B"}, headers=headers)
        assert stale.status_code == 409, stale.text
        assert client.get("/api/writers-room/alpha").json()["answers"] == saved.json()
        for invalid in [{key: value for key, value in body.items() if key != "expected_revision"}, {**body, "unexpected": True}]:
            assert client.put("/api/writers-room/alpha/answers", json=invalid, headers=headers).status_code == 422
