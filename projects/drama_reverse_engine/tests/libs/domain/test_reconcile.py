from __future__ import annotations

from libs.domain.value_objects.dialogueline__valueobject import RawLine, reconcile_lines


def test_identical_lines_match_and_unflagged() -> None:
    out = reconcile_lines([RawLine("你还敢回来？", 1.0, 2.5)], [RawLine("你还敢回来？", 1.05, 2.4)])
    assert len(out) == 1
    assert out[0].status == "match" and not out[0].flagged


def test_single_char_difference_flags_mismatch_and_keeps_ocr_text() -> None:
    out = reconcile_lines([RawLine("我不去了", 0.0, 1.0)], [RawLine("我不趣了", 0.1, 1.1)])
    assert out[0].status == "mismatch"
    assert out[0].text == "我不去了"


def test_ocr_only_and_asr_only_lines_flagged() -> None:
    out = reconcile_lines(
        [RawLine("哥哥救我", 0.0, 1.0)],
        [RawLine("三年之期已到", 5.0, 6.5)],
    )
    statuses = {r.status for r in out}
    assert statuses == {"ocr_only", "asr_only"}
    assert all(r.flagged for r in out)


def test_time_misaligned_pairs_do_not_pair_below_overlap_floor() -> None:
    out = reconcile_lines([RawLine("走吧", 0.0, 1.0)], [RawLine("走吧", 1.9, 3.0)])
    assert {r.status for r in out} == {"ocr_only", "asr_only"}


def test_punctuation_difference_is_not_a_mismatch() -> None:
    out = reconcile_lines([RawLine("走吧。", 0.0, 1.0)], [RawLine("走吧", 0.1, 1.0)])
    assert out[0].status == "match" and not out[0].flagged


def test_global_assignment_prevents_pair_stealing() -> None:
    ocr = [RawLine("甲句", 0.0, 2.5), RawLine("乙句完全一致", 2.0, 3.0)]
    asr = [RawLine("乙句完全一致", 2.0, 3.0)]
    out = reconcile_lines(ocr, asr)
    by_text = {r.text: r for r in out}
    assert by_text["乙句完全一致"].status == "match"
    assert by_text["甲句"].status == "ocr_only"


def test_single_source_episode_suppresses_per_line_flags() -> None:
    asr_only = reconcile_lines([], [RawLine("三年之期已到", 0.0, 2.0), RawLine("恭迎龙王", 2.5, 4.0)])
    assert all(r.status == "asr_only" and not r.flagged for r in asr_only)
    ocr_only = reconcile_lines([RawLine("哥哥救我", 0.0, 1.0)], [])
    assert ocr_only[0].status == "ocr_only" and not ocr_only[0].flagged


def test_output_sorted_by_start_time() -> None:
    out = reconcile_lines(
        [RawLine("后句", 5.0, 6.0), RawLine("前句", 1.0, 2.0)],
        [],
    )
    assert [r.text for r in out] == ["前句", "后句"]
