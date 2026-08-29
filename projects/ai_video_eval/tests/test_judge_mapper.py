import json

import pytest

from libs.application.mappers.judge__mapper import JudgeMapper
from libs.infrastructure.errors.judge__error import JudgeSchemaError


def test_output_schema_constrains_field_ids():
    schema = JudgeMapper.output_schema(["x", "y"])
    props = schema["properties"]["judgments"]["items"]["properties"]
    assert props["field_id"]["enum"] == ["x", "y"]
    assert props["grade"]["enum"] == [1, 2, 3, 4, 5]
    assert schema["additionalProperties"] is False


def test_parse_valid_and_clamps_confidence():
    text = json.dumps(
        {
            "judgments": [
                {"field_id": "x", "grade": 4, "confidence": 1.7, "justification": "j",
                 "evidence": ["e"], "revision_hint": ""},
                {"field_id": "y", "grade": 2, "confidence": -0.2, "justification": "j2",
                 "evidence": [], "revision_hint": "h"},
            ]
        }
    )
    parsed = JudgeMapper.parse(text, ["x", "y"])
    assert parsed["x"].confidence == 1.0
    assert parsed["y"].confidence == 0.0
    assert parsed["y"].grade == 2


def test_parse_missing_field_raises():
    text = json.dumps(
        {"judgments": [{"field_id": "x", "grade": 4, "confidence": 0.5,
                        "justification": "", "evidence": [], "revision_hint": ""}]}
    )
    with pytest.raises(JudgeSchemaError):
        JudgeMapper.parse(text, ["x", "y"])


def test_parse_garbage_raises():
    with pytest.raises(JudgeSchemaError):
        JudgeMapper.parse("not json", ["x"])


def test_shared_blocks_cache_control(shot01):
    from libs.domain.value_objects.grounding__valueobject import GroundingBundle

    blocks = JudgeMapper().shared_blocks(shot01, GroundingBundle(novel_excerpt="x"))
    assert blocks[-1]["cache_control"] == {"type": "ephemeral"}
    assert shot01.raw_text in blocks[0]["text"]
