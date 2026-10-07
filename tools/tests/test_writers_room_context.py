import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from writers_room_context import build_character_packet


def fixture_data():
    return {
        "author_secret": "另一人计划背叛",
        "characters": [
            {"key": "c1", "name": "甲", "initial_knowledge": [{"fact": "自己的童年"}],
             "dimensions": [
                 {"id": "history", "label": "前史", "critical_questions": [
                     {"id": "h1", "question": "自己的秘密？", "answer": "自己的私人前史"}]},
                 {"id": "growth", "label": "未来成长", "critical_questions": [
                     {"id": "g1", "question": "将来？", "answer": "作者安排的觉醒"}]},
             ], "ability_boundary": {"mundane_allowed": ["搬运"],
                                        "policy": "另一人暗中会读心"}},
            {"key": "c2", "name": "乙", "private_history": "另一人计划背叛"},
        ],
    }, {"theme_position": "作者主题", "edges": [
        {"from": "c1", "to": "c2", "social": "陌生", "permitted_first_change": "作者希望结义"},
        {"from": "c2", "to": "c1", "wants": "暗中谋害甲"},
    ]}


def test_packet_keeps_own_private_history_and_excludes_author_and_other_minds():
    bible, relations = fixture_data()
    packet = build_character_packet(bible, relations, "c1")
    text = str(packet)
    assert "自己的私人前史" in text
    for secret in ["计划背叛", "作者安排的觉醒", "暗中会读心", "作者主题", "希望结义", "暗中谋害"]:
        assert secret not in text
    assert packet["outgoing_relationships_at_start"][0]["to"] == "c2"
    packet["own_model"]["initial_knowledge"][0]["fact"] = "改后"
    assert bible["characters"][0]["initial_knowledge"][0]["fact"] == "自己的童年"


def test_rejects_another_characters_dynamic_view():
    bible, relations = fixture_data()
    with pytest.raises(ValueError, match="拒绝混用"):
        build_character_packet(bible, relations, "c1", state_view={"character_id": "c2"})


def test_dynamic_whitelist_excludes_global_facts_and_hidden_states():
    bible, relations = fixture_data()
    view = {"character_id": "c1", "as_of": "已听到报告", "character_state": {
        "knowledge": {"heard": {"text": "亲耳报告", "source_event_id": "event1"}},
        "physical": {"hurt": "自己腕痛"}, "facts": {"secret": "全知真相"},
        "other_characters": {"c2": "他人内心"},
    }}
    packet = build_character_packet(bible, relations, "c1", state_view=view)
    assert packet["own_current_state"]["knowledge"]["heard"]["source_event_id"] == "event1"
    assert "全知真相" not in str(packet)
    assert "他人内心" not in str(packet)


@pytest.mark.parametrize("field,value", [
    ("recent_events", [{"actor": "c2", "value": "他人的秘密事件"}]),
    ("relationships", {"c2->c1": {"trust": 4}}),
])
def test_rejects_other_characters_records_inside_an_own_labeled_view(field, value):
    bible, relations = fixture_data()
    with pytest.raises(ValueError, match="拒绝混用"):
        build_character_packet(bible, relations, "c1", state_view={
            "character_id": "c1", "character_state": {field: value},
        })
