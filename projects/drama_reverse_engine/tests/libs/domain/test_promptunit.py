from __future__ import annotations

from libs.domain.value_objects.promptunit__valueobject import plan_prompt_units


def _span(index: int, start: float, end: float) -> dict:
    return {"index": index, "start_s": start, "end_s": end}


def test_normal_spans_map_one_to_one() -> None:
    units = plan_prompt_units([_span(1, 0, 8), _span(2, 8, 14)])
    assert [(u.unit_index, u.source_shot_indexes, round(u.duration_s, 2)) for u in units] == [
        (1, (1,), 8.0), (2, (2,), 6.0),
    ]
    assert all(u.segment is None and not u.floor_clamped for u in units)


def test_long_span_split_into_equal_segments_within_bounds() -> None:
    units = plan_prompt_units([_span(1, 0, 32)])
    assert len(units) == 3
    assert all(u.source_shot_indexes == (1,) for u in units)
    assert [u.segment for u in units] == [(1, 3), (2, 3), (3, 3)]
    assert all(4.0 <= u.duration_s <= 15.0 for u in units)
    assert abs(sum(u.duration_s for u in units) - 32.0) < 1e-6
    assert units[1].start_s == units[0].end_s


def test_short_span_merges_into_previous_unit() -> None:
    units = plan_prompt_units([_span(1, 0, 10), _span(2, 10, 12), _span(3, 12, 18)])
    # 2s shot2 merges into shot1's group (10+2=12s); shot3 (6s) stands alone
    assert [(u.source_shot_indexes, round(u.duration_s, 2)) for u in units] == [
        ((1, 2), 12.0), ((3,), 6.0),
    ]


def test_leading_short_spans_absorb_until_min_reached() -> None:
    units = plan_prompt_units([_span(1, 0, 2), _span(2, 2, 3.5), _span(3, 3.5, 9)])
    assert len(units) == 1
    assert units[0].source_shot_indexes == (1, 2, 3)
    assert round(units[0].duration_s, 2) == 9.0


def test_merged_group_exceeding_max_gets_resplit() -> None:
    units = plan_prompt_units([_span(1, 0, 3), _span(2, 3, 17)])
    assert len(units) == 2
    assert all(u.source_shot_indexes == (1, 2) for u in units)
    assert all(4.0 <= u.duration_s <= 15.0 for u in units)


def test_lone_too_short_episode_floor_clamped() -> None:
    units = plan_prompt_units([_span(1, 0, 3.0)])
    assert units[0].floor_clamped and units[0].duration_s == 4.0


def test_durations_are_whole_seconds_rounded_from_real_span() -> None:
    """Follow-up 007: 时长 must be an integer in [4,15], nearest-rounded from the
    covered span; split segments' integers sum back to the rounded total."""
    units = plan_prompt_units([_span(1, 0, 12.9), _span(2, 12.9, 26.9), _span(3, 26.9, 52.0)])
    assert [u.duration_s for u in units] == [13.0, 14.0, 13.0, 12.0]  # 25.1s tail → 13+12
    assert all(u.duration_s.is_integer() and 4 <= u.duration_s <= 15 for u in units)
