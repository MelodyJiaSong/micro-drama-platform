from __future__ import annotations

import pytest

from libs.domain.errors.shot__error import PromptBudgetExceededError, SubtitleContaminationError
from libs.domain.value_objects.promptbudget__valueobject import visible_char_count
from libs.domain.value_objects.shotprompt__valueobject import (
    DialogueForShot,
    ShotPromptFields,
    build_video_prompt_body,
    decide_link,
)

_DESCRIPTOR = "三十岁男子，剑眉星目，玄色劲装，腰束革带，左颊一道浅疤"


def _fields(**overrides: object) -> ShotPromptFields:
    base = dict(
        index=3,
        reference_line="参考: 首帧图=>shot03_firstframe.png；@裴远参考图",
        characters={"裴远": _DESCRIPTOR},
        plot="裴远推门而入，扫视全场",
        scene="夜晚的酒馆内堂，烛火摇曳",
        shot_size="中景", camera_angle="平视", camera_move="固定",
        blocking="裴远自画面右侧入画，行至桌前站定",
        action="表演：眼神冷峻，下颌微收",
        dialogue=(DialogueForShot("裴远", "都别动。", "对白"),),
        lighting="暖黄烛光为主，门口冷月光补边",
        pacing="紧张，节奏快",
        render_style="实拍短剧质感，写实电影感",
        duration_s=5.0, link="硬切", tail_locked=False,
    )
    base.update(overrides)
    return ShotPromptFields(**base)  # type: ignore[arg-type]


def test_body_contains_descriptor_byte_identical() -> None:
    body, _ = build_video_prompt_body(_fields())
    assert _DESCRIPTOR in body


def test_os_and_narration_carry_lip_still_directive() -> None:
    body, _ = build_video_prompt_body(_fields(dialogue=(DialogueForShot("裴远", "此人有诈。", "内心独白"),)))
    assert "口型不动" in body and "画外" in body
    body2, _ = build_video_prompt_body(_fields(dialogue=(DialogueForShot("旁白", "三年前。", "旁白"),)))
    assert "口型不动" in body2


def test_budget_drops_render_style_first_and_keeps_negatives() -> None:
    body, dropped = build_video_prompt_body(_fields(
        plot="剧情" * 390, action="打斗" * 390,
        render_style="实拍短剧质感写实电影感" * 12, lighting="暖黄烛光冷月补边" * 12, pacing="紧张顿挫" * 15,
    ))
    assert visible_char_count(body) <= 2000
    assert dropped[0] == "渲染样式"
    assert "负面词" in body  # standard negative set is the floor, never dropped
    assert "台词:" in body


def test_budget_hard_fails_when_required_alone_overflows() -> None:
    with pytest.raises(PromptBudgetExceededError):
        build_video_prompt_body(_fields(plot="剧情" * 600, action="打斗" * 600))


def test_subtitle_token_in_any_field_is_rejected() -> None:
    with pytest.raises(SubtitleContaminationError):
        build_video_prompt_body(_fields(scene="酒馆内堂，墙上贴着字幕说明"))


def test_normal_prompt_within_budget_drops_nothing() -> None:
    body, dropped = build_video_prompt_body(_fields())
    assert dropped == []
    assert "负面词" in body and "渲染样式" in body and visible_char_count(body) <= 2000


def test_first_shot_is_always_hard_cut() -> None:
    assert decide_link(True, True) == "硬切"
    assert decide_link(False, True) == "承接"
    assert decide_link(False, False) == "硬切"
