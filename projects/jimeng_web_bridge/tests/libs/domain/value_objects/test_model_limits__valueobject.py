import copy

import pytest

from libs.common.enums import BackendKind, GenerationKind, RefKind
from libs.domain.errors.config__error import ConfigError, UnknownModelError
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from tests.libs.domain.builders import GLOBAL_DATA, entity_ref, image_ref

LIMITS_DATA: dict[str, object] = GLOBAL_DATA["model_limits"]  # type: ignore[assignment]


def limits(data: dict[str, object] | None = None) -> ModelLimits:
    return ModelLimits.from_dict(data if data is not None else copy.deepcopy(LIMITS_DATA))


FR1_ROWS: list[tuple[str, set[BackendKind], tuple[int, int] | None, tuple[str, ...], tuple[int, int, int], bool]] = [
    ("seedance2.5", {BackendKind.WEB}, (4, 30), ("480p", "720p"), (30, 10, 10), True),
    ("seedance2.0_vip", {BackendKind.WEB, BackendKind.CLI}, (4, 15), ("720p", "1080p"), (9, 3, 3), True),
    ("seedance2.0fast_vip", {BackendKind.WEB, BackendKind.CLI}, (4, 15), ("720p",), (9, 3, 3), True),
    ("seedance2.0", {BackendKind.WEB, BackendKind.CLI}, (4, 15), ("720p",), (9, 3, 3), True),
    ("seedance2.0fast", {BackendKind.WEB, BackendKind.CLI}, (4, 15), ("720p",), (9, 3, 3), True),
    ("seedream5.0", {BackendKind.CLI}, None, ("2k", "4k"), (10, 0, 0), False),
    *[(f"seedream{v}", {BackendKind.CLI}, None, ("2k", "4k"), (10, 0, 0), False) for v in ("4.7", "4.6", "4.5", "4.1", "4.0")],
    *[(f"seedream{v}", {BackendKind.CLI}, None, ("1k", "2k"), (0, 0, 0), False) for v in ("3.1", "3.0")],
]


def test_tracked_config_has_exactly_the_fr1_models() -> None:
    assert set(limits().models) == {row[0] for row in FR1_ROWS}


@pytest.mark.parametrize(("key", "backends", "duration", "resolutions", "counts", "entities"), FR1_ROWS)
def test_matrix_matches_fr1(key: str, backends: set[BackendKind], duration: tuple[int, int] | None, resolutions: tuple[str, ...], counts: tuple[int, int, int], entities: bool) -> None:
    cap = limits().capability(key)
    assert cap.backends == backends and cap.duration_range == duration and cap.resolutions == resolutions
    assert (cap.max_images, cap.max_videos, cap.max_audios) == counts and cap.entities is entities
    assert cap.kind is (GenerationKind.VIDEO if duration else GenerationKind.IMAGE)
    assert not cap.count_entities_as_images and not cap.negative_prompt_field


def test_as_of_and_resolutions_for() -> None:
    parsed = limits()
    assert parsed.as_of == "2026-09-13"
    assert parsed.resolutions_for(GenerationKind.VIDEO) == {"480p", "720p", "1080p"}
    assert "9:16" in parsed.capability("seedance2.5").ratios and "3:2" not in parsed.capability("seedance2.5").ratios


def test_entities_web_only() -> None:
    vip = limits().capability("seedance2.0_vip")
    assert vip.supports_entities_on(BackendKind.WEB) and not vip.supports_entities_on(BackendKind.CLI)


def test_counting_rules() -> None:
    cap = limits().capability("seedance2.5")
    items = (image_ref("a"), image_ref("f", kind=RefKind.FIRST_FRAME), entity_ref())
    assert cap.image_count(items) == 2
    data = copy.deepcopy(LIMITS_DATA)
    data["models"]["seedance2.5"]["count_entities_as_images"] = True  # type: ignore[index]
    assert limits(data).capability("seedance2.5").image_count(items) == 3


def test_unknown_model() -> None:
    parsed = limits()
    assert parsed.find("seedance3") is None
    with pytest.raises(UnknownModelError) as err:
        parsed.capability("seedance3")
    assert err.value.field_path == "model_limits.models.seedance3"
    with pytest.raises(UnknownModelError) as dotted:
        parsed.capability("seedance3.0")
    assert dotted.value.field_path == 'model_limits.models."seedance3.0"'


def _mutate(path: list[str], value: object) -> dict[str, object]:
    data = copy.deepcopy(LIMITS_DATA)
    node: dict[str, object] = data
    for key in path[:-1]:
        node = node[key]  # type: ignore[assignment]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return data


INVALID: list[tuple[list[str], object, str]] = [
    (["as_of"], KeyError, "model_limits.as_of"),
    (["as_of"], "13/09/2026", "model_limits.as_of"),
    (["models", "seedance2.5", "duration_s"], [30, 4], 'model_limits.models."seedance2.5".duration_s'),
    (["models", "seedance2.5", "duration_s"], [4], 'model_limits.models."seedance2.5".duration_s'),
    (["models", "seedance2.5", "backends"], ["api"], 'model_limits.models."seedance2.5".backends[0]'),
    (["models", "seedance2.5", "backends"], [], 'model_limits.models."seedance2.5".backends'),
    (["models", "seedance2.5", "ratios"], ["2.35:1"], 'model_limits.models."seedance2.5".ratios[0]'),
    (["models", "seedance2.5", "max_images"], -1, 'model_limits.models."seedance2.5".max_images'),
    (["models", "seedance2.5", "entities"], "yes", 'model_limits.models."seedance2.5".entities'),
    (["models", "seedance2.5", "负向输入框"], False, 'model_limits.models."seedance2.5"."负向输入框"'),
    (["models"], {}, "model_limits.models"),
]


@pytest.mark.parametrize(("path", "value", "field_path"), INVALID)
def test_invalid_limits_report_field_path(path: list[str], value: object, field_path: str) -> None:
    with pytest.raises(ConfigError) as err:
        limits(_mutate(path, value))
    assert err.value.field_path == field_path
