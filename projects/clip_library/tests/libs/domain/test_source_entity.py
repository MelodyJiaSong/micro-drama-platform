import pytest

from libs.common.options import LicenseKind
from libs.domain.entities.source__entity import SourceEntity
from libs.domain.errors.clip__error import ClipOutOfRangeError, ClipTooLongError, EmptyRangeError, InvalidTimeError
from libs.domain.value_objects.license__valueobject import License
from libs.domain.value_objects.time_range__valueobject import TimeRange, parse_seconds


@pytest.mark.parametrize(("text", "seconds"), [("75", 75.0), ("1:15", 75.0), ("1:01:15.5", 3675.5)])
def test_parse_seconds(text: str, seconds: float) -> None:
    assert parse_seconds(text) == seconds


def test_bad_times_are_rejected() -> None:
    with pytest.raises(InvalidTimeError):
        parse_seconds("1分2秒")
    with pytest.raises(EmptyRangeError):
        TimeRange.parse("10", "5")


def test_quote_clip_is_capped() -> None:
    source = SourceEntity("abc", 600, License(LicenseKind.QUOTE))
    assert source.plan_clip(TimeRange.parse("1:00", "1:08"), True).clip_id == "abc_60000-68000_v"
    with pytest.raises(ClipTooLongError):
        source.plan_clip(TimeRange.parse("1:00", "1:30"), True)


def test_cc_clip_is_uncapped_but_inside_video() -> None:
    source = SourceEntity("abc", 600, License(LicenseKind.CC_BY, "cc"))
    assert source.plan_clip(TimeRange.parse("0", "5:00"), False).time_range.seconds == 300
    with pytest.raises(ClipOutOfRangeError):
        source.plan_clip(TimeRange.parse("9:00", "10:30"), False)
