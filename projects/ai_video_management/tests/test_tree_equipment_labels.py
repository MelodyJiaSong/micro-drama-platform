"""The equipment tree is labelled like `props/`: keyed names show `{key} {rest}`.

An item is any `e{N}_{品质}_{名}/` folder under `equipment/`, at any depth — a
drama may nest category and slot (`equipment/板甲/胸/e3_…/`) or a slot alone
(`equipment/胸/e3_…/`), so the layout-shaped tests run on both (`slot` fixture).
An item folder, its card and its views read `e12 蓝_维里甘之拳`,
`e12 蓝_维里甘之拳.md`, `e12-1 正面.png`; the `equipment/` folder, its category
and slot folders, `loadouts/`, the tool-owned `equipment.toml` / `registry.toml` /
`item.toml`, and every name inside `loadouts/` or a `_*` / `.*` folder keep their own.
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader

WORLD_REL = "ai_videos/d/2_世界观人设"
FIST = "e12_蓝_维里甘之拳"
ARMOR = "e3_绿_皮甲"
# Where a slot folder sits: straight under `equipment/`, or under a category.
LAYOUTS: dict[str, dict[str, str]] = {"slot": {}, "category_slot": {"主手": "近战武器", "胸": "板甲"}}
Slot = Callable[[str], tuple[str, ...]]


@pytest.fixture(params=sorted(LAYOUTS))
def slot(request: pytest.FixtureRequest) -> Slot:
    """`slot("主手")` → `("主手",)` or `("近战武器", "主手")`, relative to `equipment/`."""
    categories = LAYOUTS[request.param]
    return lambda name: (categories[name], name) if name in categories else (name,)


def _write(path: Path, text: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed(root: Path, slot: Slot) -> None:
    equipment = root / WORLD_REL / "equipment"
    _write(equipment / "equipment.toml", "[slots]\n")
    _write(equipment / "registry.toml", "[meta]\n")
    _write(equipment / "equipment_index.md", "# 装备索引\n")
    _write(equipment / "loadouts" / "c1_林问.toml", "[loadout]\n")
    _write(equipment / "loadouts" / "c1_林问.md", "# 林问 · 装备表\n")
    fist = equipment.joinpath(*slot("主手"), FIST)
    _write(fist / f"{FIST}.md", "# 维里甘之拳 · 装备卡\n")   # H1 would read「装备卡」
    _write(fist / "item.toml", "[item]\n")
    for i, face in ((1, "正面"), (2, "侧面"), (3, "背面")):
        _write(fist / f"e12-{i}_{face}.png")
    _write(equipment.joinpath(*slot("胸"), ARMOR, f"{ARMOR}.md"), "# 皮甲\n")


def _child(node: dict[str, Any], name: str) -> dict[str, Any]:
    return next(c for c in node["children"] if c["name"] == name)


def _at(node: dict[str, Any], *names: str) -> dict[str, Any]:
    for name in names:
        node = _child(node, name)
    return node


def _equipment_node(root: Path) -> dict[str, Any]:
    reader = TreeReader(ExposedTree(root))
    return _child({"children": reader._walk_filtered(root / WORLD_REL, reader._is_allowed_leaf)}, "equipment")


def test_items_views_and_cards_are_labelled_by_key(tmp_path: Path, slot: Slot) -> None:
    _seed(tmp_path, slot)
    equipment = _equipment_node(tmp_path)
    fist = _at(equipment, *slot("主手"), FIST)
    assert fist["display_name"] == "e12 蓝_维里甘之拳"
    assert _child(fist, f"{FIST}.md")["display_name"] == "e12 蓝_维里甘之拳.md"
    assert _child(fist, "e12-1_正面.png")["display_name"] == "e12-1 正面.png"
    assert _child(fist, "e12-3_背面.png")["type"] == "image"
    assert _at(equipment, *slot("胸"), ARMOR)["display_name"] == "e3 绿_皮甲"


def test_categories_slots_loadouts_and_tool_files_keep_their_names(tmp_path: Path, slot: Slot) -> None:
    _seed(tmp_path, slot)
    equipment = _equipment_node(tmp_path)
    assert "display_name" not in equipment
    for name in ("loadouts", "equipment.toml", "registry.toml", "equipment_index.md"):
        assert "display_name" not in _child(equipment, name), name
    for path in (slot("主手"), slot("胸")):
        for depth in range(1, len(path) + 1):
            assert "display_name" not in _at(equipment, *path[:depth]), path[:depth]
    loadouts = _child(equipment, "loadouts")
    assert all("display_name" not in c for c in loadouts["children"])
    item_toml = _at(equipment, *slot("主手"), FIST, "item.toml")
    assert item_toml["type"] == "file" and "display_name" not in item_toml


def test_items_are_labelled_at_any_depth_but_never_inside_tool_owned_folders(tmp_path: Path) -> None:
    equipment = tmp_path / WORLD_REL / "equipment"
    labelled = {
        ("e7_白_护身符",): "e7 白_护身符",
        ("颈", "e8_绿_项链"): "e8 绿_项链",
        ("板甲", "胸", "e79_蓝_光铸胸甲"): "e79 蓝_光铸胸甲",
        ("近战武器", "双手", "锤", "e80_紫_巨锤"): "e80 紫_巨锤",
    }
    kept = [
        ("loadouts", "e90_白_配装"),
        ("板甲", "loadouts", "e91_白_配装"),
        ("_archive", "e79_蓝_旧版胸甲"),
        ("板甲", "_old", "e92_白_旧甲"),
        (".cache", "e93_白_缓存"),
    ]
    for parts in (*labelled, *kept):
        _write(equipment.joinpath(*parts, f"{parts[-1]}.md"), "# 卡\n")
        _write(equipment.joinpath(*parts, f"{parts[-1].split('_', 1)[0]}-1_正面.png"))
    node = _equipment_node(tmp_path)

    for parts, label in labelled.items():
        item = _at(node, *parts)
        assert item["display_name"] == label
        assert _child(item, f"{parts[-1]}.md")["display_name"] == f"{label}.md"
        view = parts[-1].split("_", 1)[0]
        assert _child(item, f"{view}-1_正面.png")["display_name"] == f"{view}-1 正面.png"
        for depth in range(1, len(parts)):
            assert "display_name" not in _at(node, *parts[:depth]), parts[:depth]
    for parts in kept:
        folder = _at(node, *parts)
        assert "display_name" not in folder, parts
        assert all("display_name" not in c for c in folder["children"]), parts
