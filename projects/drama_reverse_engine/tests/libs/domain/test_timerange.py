from __future__ import annotations

import pytest

from libs.domain.errors.shot__error import InvalidTimeRangeError
from libs.domain.value_objects.timerange__valueobject import TimeRange


def test_duration_and_frames_at_24fps() -> None:
    tr = TimeRange(start_s=1.0, end_s=3.5)
    assert tr.duration_s == 2.5
    assert tr.start_frame == 24
    assert tr.end_frame == 84
    assert tr.frame_count == 60


def test_one_frame_tolerance_comparison_is_integer() -> None:
    a = TimeRange(0.0, 2.5)
    b = TimeRange(0.0, 2.542)
    assert a.frames_apart(b) == 1


def test_half_frame_rounding_boundary_at_24fps() -> None:
    base = TimeRange(0.0, 2.5)
    assert base.frames_apart(TimeRange(0.0, 2.5 + 0.0416)) == 1
    assert base.frames_apart(TimeRange(0.0, 2.5 + 0.0417)) == 1
    assert base.frames_apart(TimeRange(0.0, 2.5 + 0.020)) == 0


def test_zero_length_rejected() -> None:
    with pytest.raises(InvalidTimeRangeError):
        TimeRange(2.0, 2.0)


def test_negative_start_rejected() -> None:
    with pytest.raises(InvalidTimeRangeError):
        TimeRange(-0.1, 2.0)
