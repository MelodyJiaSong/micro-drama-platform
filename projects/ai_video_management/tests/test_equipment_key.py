"""The equipment routing-key grammar (`libs.common.equipment_key`).

Same grammar as props (`libs.common.key_grammar`): `e{N}` is an item, `e{N}-{M}`
its view M, found anywhere in a download stem at an ASCII-alphanumeric boundary;
the quality tier is plain text in the name and never parsed.
"""
from __future__ import annotations

import pytest

from libs.common import drama_layout, equipment_key, prop_key

GEN = "ElevenLabs_image_gpt-image-2_"


@pytest.mark.parametrize(
    "stem",
    ["ep01", "ep01_shot03", "01集03镜视 ep02", f"{GEN}正面 一只拳套", "mp4", "v1e2_x", "e12-3x"],
)
def test_noise_never_reads_as_a_key(stem: str) -> None:
    assert equipment_key.first_key(stem) is None


def test_generator_prefix_cannot_hide_the_key() -> None:
    key = equipment_key.first_key(f"{GEN}e12-1_正面 一只拳套_2026-09-25T07_26_16")
    assert key is not None
    assert (key.number, key.view, key.base, key.text) == (12, 1, "e12", "e12-1")
    assert key.rest.startswith("正面")
    assert key.start == len(GEN)


def test_cut_off_view_number_reads_as_the_bare_item_only() -> None:
    cut = equipment_key.first_key(f"{GEN}e12-")
    assert cut is not None and (cut.text, cut.view) == ("e12", None)
    whole = equipment_key.first_key("e12-1")
    assert whole is not None and (whole.text, whole.view) == ("e12-1", 1)


def test_leftmost_key_is_the_prompt_first_line() -> None:
    stem = f"{GEN}e12-1_正面 参考 p15-1_正面"
    item, prop = equipment_key.first_key(stem), prop_key.first_key(stem)
    assert item is not None and prop is not None and item.start < prop.start
    stem = f"{GEN}p15-2_侧面 参考 e12-1_正面"
    item, prop = equipment_key.first_key(stem), prop_key.first_key(stem)
    assert item is not None and prop is not None and prop.start < item.start


def test_names_parse_and_label_like_props() -> None:
    own = equipment_key.parse_name("e12_蓝_维里甘之拳")
    assert own is not None and (own.number, own.view, own.rest) == (12, None, "蓝_维里甘之拳")
    assert equipment_key.label("e12_蓝_维里甘之拳") == "e12 蓝_维里甘之拳"
    assert equipment_key.label("e12-1_正面.png") == "e12-1 正面.png"
    assert equipment_key.split_name("e1_白_父亲的旧双手锤") == ("e1", "白_父亲的旧双手锤")
    for plain in ("主手", "loadouts", "item.toml", "equipment.toml", "registry.toml", "c1_林问.toml"):
        assert equipment_key.label(plain) is None
    for category in ("布甲", "皮甲", "锁甲", "板甲", "近战武器", "法系与远程"):
        assert equipment_key.parse_name(category) is None


def test_only_tool_owned_folders_are_skipped_by_the_item_walk() -> None:
    for skipped in ("loadouts", "_archive", "_deleted", ".cache"):
        assert drama_layout.is_equipment_tool_dir(skipped), skipped
    for walked in ("板甲", "近战武器", "主手", "胸", "e12_蓝_维里甘之拳"):
        assert not drama_layout.is_equipment_tool_dir(walked), walked


def test_view_names_have_one_definition() -> None:
    assert equipment_key.VIEW_NAMES is prop_key.VIEW_NAMES
    assert equipment_key.VIEW_NAMES == {1: "正面", 2: "侧面", 3: "背面"}
