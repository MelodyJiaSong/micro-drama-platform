import copy

import pytest

from libs.common.enums import NegativePromptStrategy, OnExisting
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.global_config__valueobject import GLOBAL_SECTIONS
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.reference_rule__valueobject import DEFAULT_REFERENCE_RULES
from tests.libs.domain.builders import GLOBAL_DATA

LIMITS = ModelLimits.from_dict(copy.deepcopy(GLOBAL_DATA["model_limits"]))  # type: ignore[arg-type]
RATIOS = {"characters": "3:4", "scenes": "16:9", "props": "1:1"}
VIDEO_DEFAULT = {"model": "seedance2.5", "resolution": "720p", "ratio": "9:16", "duration_s": 4}

# FR-5 contract table: every FR-2 key -> valid sample + (invalid sample, exact field path) pairs.
CONTRACT: list[tuple[str, object, tuple[tuple[object, str], ...]]] = [
    ("drama.abbrev", "", (("hy-3", "drama.abbrev"), ("a" * 17, "drama.abbrev"), (3, "drama.abbrev"))),
    ("entities.name_template", "{character_name}", (("{abbrev}_{unknown}", "entities.name_template"), ("", "entities.name_template"))),
    ("entities.overrides", {"c1_砌炉的老人": "hy3_主角"}, (
        ({"c1_砌炉的老人": ""}, 'entities.overrides."c1_砌炉的老人"'),
        ({"c1": "x" * 21}, "entities.overrides.c1"),
    )),
    ("entities.source_images", ["{card_dir}/*-1.png"], (
        ([], "entities.source_images"),
        (["../x.png"], "entities.source_images[0]"),
        (["C:/x.png"], "entities.source_images[0]"),
        (["{card_dir}/{foo}.png"], "entities.source_images[0]"),
    )),
    ("entities.description_from", "locked_descriptor", (("none", "entities.description_from"),)),
    ("references.rules", [], (
        ([{"label_glob": "x", "kind": "gif", "resolver": "asset_file"}], "references.rules[0].kind"),
        ([{"label_glob": "x", "kind": "entity", "resolver": "shot_video"}], "references.rules[0].kind"),
    )),
    ("references.overrides", {"砌炉的老人": "entity:hy3_主角", "bg3-1": "ai_videos/hy/bg3-1_远景.png"}, (
        ({"x": "ai_videos/../projects/x.png"}, "references.overrides.x"),
        ({"x": "entity:"}, "references.overrides.x"),
    )),
    ("references.search_exclude", [], (("renders", "references.search_exclude"), (["../x"], "references.search_exclude[0]"))),
    ("video.model", "seedance2.0", (("seedance3", "video.model"), ("seedream5.0", "video.model"))),
    ("video.resolution", "1080p", (("8k", "video.resolution"), ("2k", "video.resolution"))),
    ("video.count", 4, ((0, "video.count"), (5, "video.count"), (1.5, "video.count"))),
    ("video.ratio_source", "shot", (("fixed", "video.ratio_source"),)),
    ("video.duration_source", "shot", (("fixed", "video.duration_source"),)),
    ("video.negative_prompt", "fail", (("merge", "video.negative_prompt"), ("append", "video.negative_prompt"))),
    ("image.model", "seedream3.0", (("5.0", "image.model"), ("seedance2.5", "image.model"))),
    ("image.resolution", "4k", (("8k", "image.resolution"),)),
    ("image.count", 2, ((0, "image.count"),)),
    ("image.ratio_by_subject", RATIOS, (
        ({**RATIOS, "characters": "3x4"}, "image.ratio_by_subject.characters"),
        ({"characters": "3:4", "scenes": "16:9"}, "image.ratio_by_subject.props"),
    )),
    ("image.block_overrides", {"c1-1": {"ratio": "16:9", "reference_keys": ["c1-1"]}}, (
        ({"c1_1": {}}, "image.block_overrides.c1_1"),
        ({"c1-2": {"model": "seedance2.5"}}, "image.block_overrides.c1-2.model"),
        ({"c1-2": {"reference_keys": ["立绘"]}}, "image.block_overrides.c1-2.reference_keys[0]"),
    )),
    ("assets.video_block_match", {"first_line_contains": [], "has_field": ["时长:"]}, (
        ({"first_line_contains": [], "has_field": []}, "assets.video_block_match"),
    )),
    ("assets.video_reference", "{card_dir}/c{N}-1.png", (("c1-1.png", "assets.video_reference"), ("{card_dir}/../x", "assets.video_reference"))),
    ("assets.video_default", {**VIDEO_DEFAULT, "duration_s": 10}, (
        ({**VIDEO_DEFAULT, "duration_s": 0}, "assets.video_default.duration_s"),
        ({**VIDEO_DEFAULT, "ratio": "9x16"}, "assets.video_default.ratio"),
    )),
    ("outputs.video_name", "{shot}_{ts}_jm{suffix}.mp4", (
        ("{shot}{suffix}.mp4", "outputs.video_name"),
        ("{shot}_{ts}{suffix}.mov", "outputs.video_name"),
        ("x/{ts}{suffix}.mp4", "outputs.video_name"),
        ("{shot}_{ts}{_i}.mp4", "outputs.video_name"),
    )),
    ("outputs.image_candidates_dir", "_cand/{key}", (
        ("_candidates", "outputs.image_candidates_dir"),
        ("../{key}", "outputs.image_candidates_dir"),
        ("C:/{key}", "outputs.image_candidates_dir"),
    )),
    ("outputs.on_existing", "fail", (("overwrite", "outputs.on_existing"),)),
    ("precheck.prompt_max_chars", 1, ((0, "precheck.prompt_max_chars"),)),
    ("precheck.entity_name_max_chars", 20, ((0, "precheck.entity_name_max_chars"),)),
    ("precheck.estimate_tolerance_pct", 0, ((-1, "precheck.estimate_tolerance_pct"), ("20%", "precheck.estimate_tolerance_pct"))),
]


def with_value(key: str, value: object) -> dict[str, object]:
    data = DramaConfig.defaults("hy3")
    section, leaf = key.split(".")
    data[section][leaf] = copy.deepcopy(value)  # type: ignore[index]
    return data


def test_meta_contract_table_equals_default_structure() -> None:
    defaults = DramaConfig.defaults("hy3")
    schema = {f"{section}.{leaf}" for section, table in defaults.items() for leaf in table}  # type: ignore[attr-defined]
    assert schema == {key for key, _, _ in CONTRACT}


@pytest.mark.parametrize(("key", "value"), [(k, v) for k, v, _ in CONTRACT])
def test_valid_sample_accepted(key: str, value: object) -> None:
    DramaConfig.from_dict(with_value(key, value), LIMITS)


@pytest.mark.parametrize(("key", "value", "field_path"), [(k, bad, path) for k, _, bads in CONTRACT for bad, path in bads])
def test_invalid_sample_rejected_with_field_path(key: str, value: object, field_path: str) -> None:
    with pytest.raises(ConfigError) as err:
        DramaConfig.from_dict(with_value(key, value), LIMITS)
    assert err.value.field_path == field_path


def test_defaults_roundtrip() -> None:
    config = DramaConfig.from_dict(DramaConfig.defaults("hy3"), LIMITS)
    assert config.drama.abbrev == "hy3"
    assert config.entity_naming.entity_name("c1_砌炉的老人") == "hy3_砌炉的老人"
    assert config.references.routing.rules == DEFAULT_REFERENCE_RULES
    assert config.video.negative_prompt is NegativePromptStrategy.PLATFORM_FIELD_OR_OMIT
    assert config.outputs.on_existing is OnExisting.ARCHIVE
    assert config.image.ratio_by_subject == RATIOS
    assert DramaConfig.from_dict(DramaConfig.defaults(""), LIMITS).drama.abbrev == ""


@pytest.mark.parametrize("section", [s for s in GLOBAL_SECTIONS if s != "entities"])
def test_global_sections_rejected(section: str) -> None:
    data = DramaConfig.defaults("hy3")
    data[section] = {}
    with pytest.raises(ConfigError) as err:
        DramaConfig.from_dict(data, LIMITS)
    assert err.value.field_path == section and "全局" in err.value.message


def test_global_entities_key_rejected() -> None:
    data = with_value("entities.snapshot_stale_h", 24)
    with pytest.raises(ConfigError) as err:
        DramaConfig.from_dict(data, LIMITS)
    assert err.value.field_path == "entities.snapshot_stale_h" and "全局" in err.value.message


@pytest.mark.parametrize(("key", "field_path"), [("video", "video"), ("precheck.prompt_max_chars", "precheck.prompt_max_chars"), ("video.reference_mode", "video.reference_mode")])
def test_missing_or_unknown_keys(key: str, field_path: str) -> None:
    data = DramaConfig.defaults("hy3")
    if key == "video.reference_mode":
        data["video"]["reference_mode"] = "全能参考"  # type: ignore[index]
    elif "." in key:
        section, leaf = key.split(".")
        del data[section][leaf]  # type: ignore[attr-defined]
    else:
        del data[key]
    with pytest.raises(ConfigError) as err:
        DramaConfig.from_dict(data, LIMITS)
    assert err.value.field_path == field_path
