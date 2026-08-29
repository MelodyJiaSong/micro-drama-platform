import pytest

from libs.common.enums import EvaluatorKind, FieldStatus
from libs.domain.value_objects.grounding__valueobject import CanonSlice, GroundingBundle
from libs.domain.value_objects.rule_check__valueobject import evaluate_rule
from libs.domain.value_objects.rubric__valueobject import RubricField


def _field(rule_id: str, params: dict) -> RubricField:
    return RubricField(
        field_id=f"t_{rule_id}",
        name_cn="测试",
        evaluator=EvaluatorKind.RULE,
        judge_instruction="",
        weight=1.0,
        anchors={"g1": "", "g3": "", "g5": ""},
        rule_id=rule_id,
        rule_params=params,
    )


def _grounding(locked_tag: str | None) -> GroundingBundle:
    slices = ()
    if locked_tag:
        slices = (CanonSlice(name="林小雨", kind="character", text="card", locked_tag=locked_tag),)
    return GroundingBundle(novel_excerpt="", canon_slices=slices)


def _run(rule_id, params, shot, grounding, overrides=None):
    return evaluate_rule(_field(rule_id, params), "d", "s", shot, grounding, overrides)


def test_char_count_max(shot01):
    assert _run("char_count_max", {"max": 2000}, shot01, _grounding(None)).grade == 5.0
    assert _run("char_count_max", {"max": 10}, shot01, _grounding(None)).grade == 1.0


def test_duration_range(shot01, shot02):
    assert _run("duration_range", {"min": 4, "max": 15}, shot01, _grounding(None)).grade == 5.0
    assert _run("duration_range", {"min": 4, "max": 15}, shot02, _grounding(None)).grade == 1.0


def test_aspect_ratio_with_override(shot01):
    assert _run("aspect_ratio", {"expected": "9:16"}, shot01, _grounding(None)).grade == 5.0
    result = _run("aspect_ratio", {"expected": "9:16"}, shot01, _grounding(None), {"aspect_ratio": "16:9"})
    assert result.grade == 1.0


def test_locked_descriptor_match(shot01, shot02):
    tag = "林小雨 — 青衫束发 玉簪 剑眉星目"
    assert _run("locked_descriptor_byte_match", {}, shot01, _grounding(tag)).grade == 5.0
    assert _run("locked_descriptor_byte_match", {}, shot02, _grounding(tag)).grade == 1.0
    result = _run("locked_descriptor_byte_match", {}, shot01, _grounding(None))
    assert result.status is FieldStatus.INCONCLUSIVE


def test_voice_block_when_dialogue(shot01, shot02):
    assert _run("voice_block_when_dialogue", {}, shot01, _grounding(None)).grade == 5.0
    result = _run("voice_block_when_dialogue", {}, shot02, _grounding(None))
    assert result.grade == 1.0
    assert "音色" in result.justification


def test_dialogue_speed_max(shot01, shot02):
    assert _run("dialogue_speed_max", {"max_cps": 5}, shot01, _grounding(None)).grade == 5.0
    assert _run("dialogue_speed_max", {"max_cps": 5}, shot02, _grounding(None)).grade == 1.0


def test_no_hex_colors(shot01, shot02):
    assert _run("no_hex_colors", {}, shot01, _grounding(None)).grade == 5.0
    assert _run("no_hex_colors", {}, shot02, _grounding(None)).grade == 1.0


def test_unknown_rule_raises(shot01):
    from libs.domain.errors.eval__error import RubricError

    with pytest.raises(RubricError):
        _run("nope_rule", {}, shot01, _grounding(None))
