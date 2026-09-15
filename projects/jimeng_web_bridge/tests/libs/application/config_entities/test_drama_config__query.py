from __future__ import annotations

from collections.abc import Sequence

import pytest

from libs.application.dtos.drama_config__dto import ShotReferencePreviewQdto
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError
from libs.infrastructure.errors.sandbox__error import SandboxError
from tests.libs.application.config_entities.support import FLAT, HY1, HY2, HY3, SERIES, Harness, config_text, sha256_of


def _shot(previews: Sequence[ShotReferencePreviewQdto], shot: str) -> ShotReferencePreviewQdto:
    return next(preview for preview in previews if preview.shot == shot)


def test_list_dramas_nests_series_and_excludes_unlistable(ro_harness: Harness) -> None:
    tree = ro_harness.configs.list_dramas()
    assert [(node.name, node.type, node.path) for node in tree.dramas] == [
        ("huangye_shenghuo", "series", SERIES),
        ("solo_drama", "drama", FLAT),
    ]
    assert [(child.name, child.type, child.path, child.children) for child in tree.dramas[0].children] == [
        ("hy1", "drama", HY1, ()),
        ("hy2", "drama", HY2, ()),
        ("hy3", "drama", HY3, ()),
    ]
    assert tree.dramas[1].children == ()


@pytest.mark.parametrize("raw", ["huangye_shenghuo/hy3", "ai_videos/huangye_shenghuo/hy3"])
def test_drama_root_accepts_both_spellings(ro_harness: Harness, raw: str) -> None:
    assert ro_harness.configs.drama_root(raw) == HY3


@pytest.mark.parametrize(
    "raw",
    [
        "../../projects",
        "huangye_shenghuo/../..",
        "..",
        "C:/Windows",
        "//server/share",
        "/ai_videos/huangye_shenghuo/hy3",
        "huangye_shenghuo\\hy3",
        "hy3\x00",
        "huangye_shenghuo/hy3:stream",
        "huangye_shenghuo/%2e%2e",
        "huangye_shenghuo/hy3/",
        "huangye_shenghuo\\hy3\\renders",
        "ai_videos\\huangye_shenghuo/hy3",
        "",
    ],
)
def test_drama_root_rejects_escapes(ro_harness: Harness, raw: str) -> None:
    with pytest.raises(SandboxError):
        ro_harness.configs.drama_root(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "huangye_shenghuo",
        "huangye_shenghuo/_series",
        "_deleted",
        "renders",
        "huangye_shenghuo/hy3/renders",
        "notes/x",
        "nonexistent",
        f"{HY3}/2_世界观人设",
        "ai_videos",
        "huangye_shenghuo/HY3",
    ],
)
def test_drama_root_rejects_non_roots(ro_harness: Harness, raw: str) -> None:
    with pytest.raises(DramaRootNotFoundError):
        ro_harness.configs.drama_root(raw)


def test_get_without_config_previews_the_defaults(ro_harness: Harness) -> None:
    ro_harness.sync("hy3_砌炉的老人")
    view = ro_harness.configs.get("huangye_shenghuo/hy3")
    assert (view.exists, view.data, view.raw_text, view.sha256, view.parse_error) == (False, {}, None, None, None)
    assert view.validation_error is None
    assert view.location == f"{HY3}/jimeng_config.toml"
    shot02 = _shot(view.reference_preview, "shot02")
    assert [(item.name, item.kind, item.status) for item in shot02.items] == [
        ("bg11-1", "image", "found"),
        ("砌炉的老人", "entity", "found"),
        ("p2-1", "image", "found"),
        ("p3-1", "image", "found"),
    ]
    assert shot02.items[0].resolved_path == f"{HY3}/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png"
    assert shot02.items[1].entity_name == "hy3_砌炉的老人"
    assert shot02.integrity_ok and shot02.parse_error is None
    assert not (ro_harness.repo / HY3 / "jimeng_config.toml").exists()


def test_get_existing_config_returns_raw_text_hash_and_naming(harness: Harness) -> None:
    text = config_text(harness.mapper, overrides={"c1_砌炉的老人": "hy3_主角"})
    path = harness.write_config(HY3, text)
    view = harness.configs.get(HY3)
    assert view.exists and view.raw_text == text and view.sha256 == sha256_of(path)
    assert view.data["entities"] == {**view.data["entities"], "overrides": {"c1_砌炉的老人": "hy3_主角"}}
    assert {entity.character_dir: entity.entity_name for entity in view.entities} == {
        "c1_砌炉的老人": "hy3_主角",
        "c2_獾": "hy3_獾",
    }
    assert _shot(view.reference_preview, "shot02").items[1].entity_name == "hy3_主角"


def test_get_invalid_config_reports_the_field_path(harness: Harness) -> None:
    harness.write_config(HY3, config_text(harness.mapper).replace("count = 1", "count = 9", 1))
    view = harness.configs.get(HY3)
    assert view.validation_error is not None
    assert view.validation_error.field_path == "video.count"
    assert view.reference_preview == () and view.needs_confirmation == ()


def test_get_unparseable_config_reports_parse_error(harness: Harness) -> None:
    harness.write_config(HY3, "[video\n")
    view = harness.configs.get(HY3)
    assert view.exists and view.parse_error and view.data == {}


def test_flat_drama_preview_reports_every_failure_kind(ro_harness: Harness) -> None:
    ro_harness.sync("x")
    view = ro_harness.configs.get("solo_drama")
    shot01 = _shot(view.reference_preview, "shot01")
    assert [(item.name, item.status, item.reason, item.suggested_override_key) for item in shot01.items] == [
        ("缺失图", "not_found", "no_match", 'references.overrides."缺失图"'),
        ("双胞胎", "ambiguous", "exact_stem", 'references.overrides."双胞胎"'),
        ("某物", "not_found", "label_unmatched", 'references.overrides."某物"'),
        ("独行者", "found", "character_name", None),
    ]
    assert shot01.items[1].candidates == (f"{FLAT}/props/p1_甲/双胞胎.png", f"{FLAT}/props/p2_乙/双胞胎.png")
    legacy = _shot(view.reference_preview, "shot02").items
    assert [(item.status, item.suggested_override_key) for item in legacy] == [("legacy", None)]
    assert "=>@" in (legacy[0].message or "")
