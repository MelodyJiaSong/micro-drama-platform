"""Fill planning and editor verification — pure (UT-W-FILL-01..09)."""
from __future__ import annotations

import pytest

from libs.infrastructure.clients.jimeng_page_verify__steps import (
    build_fill_segments,
    compare_snapshot,
    expected_snapshot,
    normalize_editor_text,
    prompt_prefix,
)
from libs.infrastructure.daos.jimeng_page__dao import EditorSnapshotDao, FillSegmentDao, MentionMarkerDao
from libs.infrastructure.errors.jimeng_browser__error import FillPlanError

SHOT02_LINE = "shot02\n参考: `bg11-1(场景参考图)=>@`，`砌炉的老人(Seedance 人物 entity)=>@`，`p2-1(随身装备锚点)=>@`，`p3-1(抹泥板锚点)=>@`\n情节: 他走到沟边"
MARKERS = (
    MentionMarkerDao("bg11-1", "场景参考图", "bg11-1"),
    MentionMarkerDao("砌炉的老人", "Seedance 人物 entity", "hy3_主角"),
    MentionMarkerDao("p2-1", "随身装备锚点", "p2-1"),
    MentionMarkerDao("p3-1", "抹泥板锚点", "p3-1"),
)


def test_shot02_splits_into_text_and_four_mentions_in_prompt_order() -> None:
    segments = build_fill_segments(SHOT02_LINE, MARKERS)
    assert [s.mention for s in segments if s.mention] == ["bg11-1", "hy3_主角", "p2-1", "p3-1"]
    assert segments[0] == FillSegmentDao("shot02\n参考: `bg11-1(场景参考图)=>")
    assert len([s for s in segments if s.mention is None]) == 5
    expected = expected_snapshot(segments)
    assert expected.text.startswith("shot02\n参考: `bg11-1(场景参考图)=>bg11-1`，`砌炉的老人(Seedance 人物 entity)=>hy3_主角`")
    assert "@" not in expected.text


def test_other_at_signs_stay_literal_text() -> None:
    segments = build_fill_segments("参考: `bg11-1(场景参考图)=>@` 例如 @图1 模仿", MARKERS[:1])
    assert [s.mention for s in segments if s.mention] == ["bg11-1"]
    assert segments[-1].text == "` 例如 @图1 模仿"


def test_missing_marker_is_a_plan_error() -> None:
    with pytest.raises(FillPlanError):
        build_fill_segments("参考: `bg11-1(场景参考图)=>`", MARKERS[:1])


def test_identical_snapshot_passes() -> None:
    expected = expected_snapshot(build_fill_segments(SHOT02_LINE, MARKERS))
    assert compare_snapshot(expected, EditorSnapshotDao(expected.text, expected.mentions)) is None


@pytest.mark.parametrize("variant", ["{t}\n", "{t}\r\n", "{t}\n\n", "​{t}", "{t}  "])
def test_editor_whitespace_artifacts_normalise(variant: str) -> None:
    expected = EditorSnapshotDao(normalize_editor_text("甲 乙\n丙"), ())
    assert compare_snapshot(expected, EditorSnapshotDao(variant.format(t="甲 乙\n丙"), ())) is None


def test_blank_lines_collapse_like_the_editor_renders_them() -> None:
    assert normalize_editor_text("a\n\n\nb") == "a\nb"


def test_ideographic_and_repeated_spaces_are_kept() -> None:
    expected = EditorSnapshotDao(normalize_editor_text("他  走　到"), ())
    assert compare_snapshot(expected, EditorSnapshotDao("他 走 到", ())) is not None


def test_missing_text_segment_reports_position() -> None:
    expected = EditorSnapshotDao("abcdef", ())
    problem = compare_snapshot(expected, EditorSnapshotDao("abdef", ()))
    assert problem is not None and "第 2 个字符" in problem


@pytest.mark.parametrize(
    "mentions",
    [("hy3_主角", "bg11-1", "p2-1", "p3-1"), ("bg11-1", "hy3_主角", "p2-1"), ("bg11-1.png", "hy3_主角", "p2-1", "p3-1")],
)
def test_mention_sequence_is_checked_independently_of_text(mentions: tuple[str, ...]) -> None:
    expected = expected_snapshot(build_fill_segments(SHOT02_LINE, MARKERS))
    problem = compare_snapshot(expected, EditorSnapshotDao(expected.text, mentions))
    assert problem is not None and "mention" in problem


def test_appended_draft_is_a_mismatch() -> None:
    expected = expected_snapshot(build_fill_segments(SHOT02_LINE, MARKERS))
    assert compare_snapshot(expected, EditorSnapshotDao("上次的草稿" + expected.text, expected.mentions)) is not None


def test_prompt_prefix_collapses_whitespace() -> None:
    assert prompt_prefix(EditorSnapshotDao("shot02\n参考:  `bg11-1", ()), chars=12) == "shot02 参考: `"
