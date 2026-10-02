"""Scenes- and props-tree labels open with the routing key (follow-ups 173 / 174).

`bg4 闪金镇` / `bg1-1 谷心_北望修道院` / `p15 两层石木旅店` / `p15-1 正面.png`;
a zone shows its zone-level subject's key from `scenes/registry.toml`
(`bg172 艾尔文森林`), a continent shows none. A subject's `_blender/` and its
`assets/` links (into `props/`) are visible with fixed labels, a zone's `_plan/`
is hidden, and `.blend` / `.glb` are leaves.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.application.queries.media__query import MediaQuery
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.readers.scene_registry__reader import SceneRegistryReader
from libs.infrastructure.readers.tree__reader import TreeReader

WORLD_REL = "ai_videos/d/2_世界观人设"
SCENES_REL = f"{WORLD_REL}/scenes"
PROPS_REL = f"{WORLD_REL}/props"
REGISTRY = """
[meta]
next = 200

[[bg]]
n = 4
dir = "bg4_闪金镇"
zone = "elwynn_forest"
continent = "eastern_kingdoms"

[[bg]]
n = 172
dir = "bg172_艾尔文森林全境"
zone = "elwynn_forest"
continent = "eastern_kingdoms"
kind = "zone_whole"
"""


def _write(path: Path, text: str | bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")


def _seed(root: Path) -> Path:
    scenes = root / SCENES_REL
    _write(scenes / "registry.toml", REGISTRY)
    _write(scenes / "eastern_kingdoms" / "eastern_kingdoms.md", "# 东部王国（Eastern Kingdoms）\n")
    zone = scenes / "eastern_kingdoms" / "elwynn_forest"
    _write(zone / "elwynn_forest.md", "# 艾尔文森林（Elwynn Forest）\n")
    _write(zone / "_plan" / "plan.toml", "[meta]\n")
    _write(zone / "_plan" / "apply_report.md", "# apply report\n")
    _write(zone / "bg172_艾尔文森林全境" / "bg172_艾尔文森林全境.md", "# 艾尔文森林全境\n")
    town = zone / "bg4_闪金镇"
    _write(town / "bg4_闪金镇.md", "# 闪金镇 · Seedance 主体\n")   # H1 would read「Seedance 主体」
    _write(town / "_blender" / "bg4.blend", b"BLENDER")
    _write(town / "_blender" / "check_plan.png")
    _write(town / "planning" / "bg4_floorplan.png")
    valley = zone / "bg1_北郡山谷"
    _write(valley / "bg1_北郡山谷.md", "# 北郡山谷\n")
    _write(valley / "bg1-1_谷心_北望修道院" / "bg1-1_谷心_北望修道院.md",
           "# bg1-1_谷心_北望修道院 · 北郡山谷 谷底主路中段朝北（午后斜阳）\n")
    inn = root / PROPS_REL / "p15_两层石木旅店"
    _write(inn / "p15_两层石木旅店.md", "# 两层石木旅店\n")
    _write(inn / "asset.toml", "[asset]\n")
    for i, face in ((1, "正面"), (2, "侧面"), (3, "背面")):
        _write(inn / f"p15-{i}_{face}.png")
    _write(inn / "mesh" / "p15.glb", b"glTF")
    _write(inn / "mesh" / "p15_preview_000.png")
    _write(root / PROPS_REL / "p3_父亲的旧双手锤" / "p3_父亲的旧双手锤.md", "# 父亲的旧双手锤\n")
    link_dir = town / "assets" / "b01_两层旅店（正门朝西）"
    for target in ("p15_两层石木旅店.md", "p15-1_正面.png", "mesh/p15.glb"):
        rel = f"{PROPS_REL}/p15_两层石木旅店/{target}"
        _write(link_dir / f"{Path(target).name}.link.json", json.dumps({"target": rel, "note": "物件库"}))
    return zone


def _child(node: dict[str, Any], name: str) -> dict[str, Any]:
    return next(c for c in node["children"] if c["name"] == name)


def _names(node: dict[str, Any]) -> set[str]:
    return {c["name"] for c in node["children"]}


def _zone_node(root: Path) -> dict[str, Any]:
    reader = TreeReader(ExposedTree(root))
    continents = reader._walk_filtered(root / SCENES_REL, reader._is_allowed_leaf)
    continent = next(c for c in continents if c["name"] == "eastern_kingdoms")
    assert continent["display_name"] == "东部王国"          # a continent carries no key
    return _child(continent, "elwynn_forest")


def _props_node(root: Path) -> dict[str, Any]:
    reader = TreeReader(ExposedTree(root))
    return {"children": reader._walk_filtered(root / PROPS_REL, reader._is_allowed_leaf)}


def test_zone_takes_its_zone_whole_key_from_the_registry(tmp_path: Path) -> None:
    _seed(tmp_path)
    zone = _zone_node(tmp_path)
    assert zone["display_name"] == "bg172 艾尔文森林"
    assert _child(zone, "elwynn_forest.md")["display_name"] == "bg172 艾尔文森林"


def test_zone_plan_folder_is_hidden(tmp_path: Path) -> None:
    _seed(tmp_path)
    zone = _zone_node(tmp_path)
    assert "_plan" not in _names(zone)
    assert "_assets" not in _names(zone)


def test_keyed_folders_are_labelled_from_the_name_not_the_h1(tmp_path: Path) -> None:
    _seed(tmp_path)
    zone = _zone_node(tmp_path)
    town = _child(zone, "bg4_闪金镇")
    assert town["display_name"] == "bg4 闪金镇"
    assert _child(town, "bg4_闪金镇.md")["display_name"] == "bg4 闪金镇.md"
    assert _child(_child(town, "planning"), "bg4_floorplan.png")["display_name"] == "bg4 floorplan.png"
    view = _child(_child(zone, "bg1_北郡山谷"), "bg1-1_谷心_北望修道院")
    assert view["display_name"] == "bg1-1 谷心_北望修道院"


def test_props_are_labelled_by_key_with_views_and_mesh(tmp_path: Path) -> None:
    _seed(tmp_path)
    props = _props_node(tmp_path)
    inn = _child(props, "p15_两层石木旅店")
    assert inn["display_name"] == "p15 两层石木旅店"
    assert _child(inn, "p15_两层石木旅店.md")["display_name"] == "p15 两层石木旅店.md"
    assert _child(inn, "p15-1_正面.png")["display_name"] == "p15-1 正面.png"
    assert _child(inn, "p15-3_背面.png")["display_name"] == "p15-3 背面.png"
    mesh_dir = _child(inn, "mesh")
    glb = _child(mesh_dir, "p15.glb")
    assert glb["type"] == "model" and "display_name" not in glb   # the name IS the key
    assert _child(mesh_dir, "p15_preview_000.png")["display_name"] == "p15 preview_000.png"
    assert _child(props, "p3_父亲的旧双手锤")["display_name"] == "p3 父亲的旧双手锤"   # story prop too


def test_blender_folder_lists_blend_and_checks(tmp_path: Path) -> None:
    _seed(tmp_path)
    blender = _child(_child(_zone_node(tmp_path), "bg4_闪金镇"), "_blender")
    assert blender["display_name"] == "3D 场景"
    assert {c["name"]: c["type"] for c in blender["children"]} == {"bg4.blend": "file", "check_plan.png": "image"}


def test_block_asset_links_render_as_the_prop_files(tmp_path: Path) -> None:
    _seed(tmp_path)
    links = _child(_child(_zone_node(tmp_path), "bg4_闪金镇"), "assets")
    assert links["display_name"] == "本场景资产"
    block = _child(links, "b01_两层旅店（正门朝西）")
    assert "display_name" not in block
    by_name = {c["name"]: c for c in block["children"]}
    card, view, mesh = by_name["p15_两层石木旅店.md"], by_name["p15-1_正面.png"], by_name["p15.glb"]
    assert all(n["is_link"] for n in (card, view, mesh))
    assert card["path"] == f"{PROPS_REL}/p15_两层石木旅店/p15_两层石木旅店.md"
    assert card["display_name"] == "p15 两层石木旅店.md"
    assert (view["type"], view["display_name"]) == ("image", "p15-1 正面.png")
    assert mesh["type"] == "model" and mesh["path"] == f"{PROPS_REL}/p15_两层石木旅店/mesh/p15.glb"


def test_zone_key_needs_a_matching_zone_whole_row(tmp_path: Path) -> None:
    zone = _seed(tmp_path)
    reader = SceneRegistryReader()
    scenes = tmp_path / SCENES_REL
    assert reader.zone_key(scenes, zone) == "bg172"
    # same zone name under another continent is a different zone
    assert reader.zone_key(scenes, scenes / "kalimdor" / "elwynn_forest") is None
    (scenes / "registry.toml").write_text("not = [valid toml", encoding="utf-8")
    assert reader.zone_key(scenes, zone) is None                       # broken registry: no key, no crash


def test_characters_outside_scenes_keep_their_folder_name(tmp_path: Path) -> None:
    char = tmp_path / "ai_videos" / "d" / "2_世界观人设" / "characters" / "c1_裴知秋"
    _write(char / "c1_裴知秋.md", "# 裴知秋\n")
    _write(char / "c1-1_正面.png")
    reader = TreeReader(ExposedTree(tmp_path))
    assert reader._sidecar_zh_label(char) is None
    assert "display_name" not in reader._leaf_for(char / "c1-1_正面.png")


def test_blend_downloads_as_an_attachment(tmp_path: Path) -> None:
    _seed(tmp_path)
    rel = f"{SCENES_REL}/eastern_kingdoms/elwynn_forest/bg4_闪金镇/_blender/bg4.blend"
    result = MediaQuery(ExposedTree(tmp_path), SafeResolver(tmp_path)).serve(rel)
    assert (result.media_type, result.disposition) == ("application/octet-stream", "attachment")
