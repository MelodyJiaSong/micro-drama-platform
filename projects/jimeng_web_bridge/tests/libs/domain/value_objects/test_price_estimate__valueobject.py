import copy

import pytest

from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.price_estimate__valueobject import PriceTable
from tests.libs.domain.builders import GLOBAL_DATA, entity_create_request, image_request, video_request

LIMITS = ModelLimits.from_dict(copy.deepcopy(GLOBAL_DATA["model_limits"]))  # type: ignore[arg-type]


def table(**changes: object) -> PriceTable:
    data: dict[str, object] = copy.deepcopy(GLOBAL_DATA["price_table"])  # type: ignore[arg-type]
    data.update(changes)
    return PriceTable.from_dict(data, LIMITS)


def test_video_is_duration_times_rate_times_count() -> None:
    assert table().estimate(video_request(duration=26)).credits == 520
    assert table().estimate(video_request(duration=22, count=3)).credits == 1320


def test_fractional_rate_rounds_up_to_whole_credits() -> None:
    rows = [{"model": "seedance2.5", "resolution": "720p", "credits_per_second": 13.5}]
    assert table(video=rows).estimate(video_request(duration=3)).credits == 41


def test_image_is_rate_times_count() -> None:
    assert table().estimate(image_request(count=4)).credits == 4


def test_entity_create_is_free() -> None:
    assert table().estimate(entity_create_request()).credits == 0


def test_missing_price_is_unknown_with_warning() -> None:
    video = table().estimate(video_request(resolution="480p"))
    assert video.credits is None and not video.known and video.config_key == "price_table.video" and video.warning
    image = table().estimate(image_request(resolution="4k"))
    assert image.credits is None and image.config_key == "price_table.image"


@pytest.mark.parametrize(
    ("changes", "field_path"),
    [
        ({"as_of": ""}, "price_table.as_of"),
        ({"video": [{"model": "seedance3", "resolution": "720p", "credits_per_second": 1}]}, "price_table.video[0].model"),
        ({"video": [{"model": "seedance2.5", "resolution": "720p", "credits_per_second": -1}]}, "price_table.video[0].credits_per_second"),
        ({"video": [{"model": "seedance2.5", "resolution": "720p", "credits_per_image": 1}]}, "price_table.video[0].credits_per_image"),
        ({"image": [{"model": "seedream5.0", "resolution": "2k", "credits_per_image": 1}] * 2}, "price_table.image[1]"),
        ({"image": "1"}, "price_table.image"),
        ({"audio": []}, "price_table.audio"),
    ],
)
def test_invalid_price_table(changes: dict[str, object], field_path: str) -> None:
    with pytest.raises(ConfigError) as err:
        table(**changes)
    assert err.value.field_path == field_path
