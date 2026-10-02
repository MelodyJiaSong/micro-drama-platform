"""Downloads land in an equipment item by its routing key.

An item is any `e{N}_{品质}_{名}/` folder under `equipment/` (under `2_世界观人设/`,
or flat at the drama root), found by its name at any depth: a drama may nest
category and slot (`equipment/板甲/胸/e79_…/`) or a slot alone
(`equipment/主手/e12_…/`), so every layout-shaped test runs on both
(`slot` fixture). `loadouts/` and `_*` / `.*` folders hold no items.
A view download `e{N}-{M}` lands in that item as the card's ```text first line
(`e1-2_侧面_锤头朝左`), else `e{N}-{M}_{正面|侧面|背面}`. Equipment routes by key
only: it is never a name-token candidate, a GLB never lands in it, and an `e{N}`
two item folders own routes nowhere (reported as `series_key_conflict` when the
twins are an episode and its `_series/`).
"""
from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from pathlib import Path

import pytest

from libs.common import series_shared
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter, ImportResult
from libs.infrastructure.writers.media__writer import MediaRenamer

WORLD = "2_世界观人设"
GEN = "ElevenLabs_image_gpt-image-2_"
SERIES_REL = "ai_videos/my_series"
HAMMER = "e1_白_父亲的旧双手锤"
HAMMER_CARD = """# e1 白_父亲的旧双手锤

```text
e1-1_正面
一把旧双手锤，正面
```

```text
e1-2_侧面_锤头朝左
一把旧双手锤，侧面
```
"""
FIST = "e12_蓝_维里甘之拳"
ARMOR = "e3_绿_皮甲"
# Where a slot folder sits: straight under `equipment/`, or under a category.
LAYOUTS: dict[str, dict[str, str]] = {
    "slot": {},
    "category_slot": {"主手": "近战武器", "副手": "近战武器", "胸": "板甲", "头": "皮甲"},
}
Slot = Callable[[Path, str], Path]


@pytest.fixture(params=sorted(LAYOUTS))
def slot(request: pytest.FixtureRequest) -> Slot:
    """`slot(equipment, "主手")` → `equipment/主手` or `equipment/近战武器/主手`."""
    categories = LAYOUTS[request.param]

    def at(equipment: Path, name: str) -> Path:
        category = categories.get(name)
        return equipment / category / name if category is not None else equipment / name

    return at


def _touch(path: Path, payload: bytes = b"x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def _drop(downloads: Path, name: str, payload: bytes = b"x", age_s: int = 30) -> Path:
    """A download with a recent mtime — older `age_s` is processed first."""
    src = _touch(downloads / name, payload)
    stamp = time.time() - age_s
    os.utime(src, (stamp, stamp))
    return src


def _item(folder: Path, card: str | None = None) -> Path:
    _touch(folder / f"{folder.name}.md", (card or f"# {folder.name}\n").encode("utf-8"))
    _touch(folder / "item.toml", b"[item]\n")
    return folder


def _files(folder: Path) -> set[str]:
    return {p.name for p in folder.iterdir() if p.is_file()}


def _drama(tmp_path: Path, slot: Slot) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    world = root / "ai_videos" / "d" / WORLD
    equipment = world / "equipment"
    _touch(equipment / "equipment.toml", b"[slots]\n")
    _touch(equipment / "registry.toml", b"[meta]\nnext = 13\n")
    _touch(equipment / "equipment_index.md", "# 装备索引\n".encode("utf-8"))
    _touch(equipment / "loadouts" / "c1_林问.toml", b"[loadout]\n")
    _item(slot(equipment, "主手") / HAMMER, HAMMER_CARD)
    _item(slot(equipment, "主手") / FIST)
    _item(slot(equipment, "胸") / ARMOR)
    _touch(world / "characters" / "c1_林问" / "c1_林问.md", "# 林问\n".encode("utf-8"))
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, equipment, downloads


def _series(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """A series whose episode and `_series/` each have an (empty) equipment tree."""
    root = tmp_path / "repo"
    series = root / SERIES_REL
    (series / "ep1" / WORLD / "equipment").mkdir(parents=True)
    (series / "_series" / "equipment").mkdir(parents=True)
    (series / "series.json").write_text(json.dumps({"name_zh": "系列", "slug": "my_series"}), encoding="utf-8")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, series / "ep1" / WORLD / "equipment", series / "_series" / "equipment", downloads


def _run(root: Path, downloads: Path, drama_rel: str = "ai_videos/d") -> ImportResult:
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    importer = DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)
    return importer.import_drama(drama_rel)


def test_views_land_in_the_item_under_their_card_first_lines(tmp_path: Path, slot: Slot) -> None:
    root, equipment, downloads = _drama(tmp_path, slot)
    _drop(downloads, f"{GEN}e1-1_正面 一把旧双手锤_2026-09-25T07_26_16.png", b"front")
    # the reference key quoted from the `参考:` line comes second — first key wins
    _drop(downloads, "jimeng-2026-09-25-1001-e1-2_侧面 参考 e1-1_正面.png", b"side")
    _drop(downloads, "e1-3_背面 (1).webp", b"back")   # not in the card → convention name
    _drop(downloads, f"{GEN}e12-1_正面 一只拳套.jpg", b"fist")

    result = _run(root, downloads)

    assert result.unmatched == [] and result.errors == [], (result.unmatched, result.errors)
    assert {m["kind"] for m in result.moved} == {"equipment_view"}
    hammer = slot(equipment, "主手") / HAMMER
    assert _files(hammer) == {f"{HAMMER}.md", "item.toml", "e1-1_正面.png", "e1-2_侧面_锤头朝左.png", "e1-3_背面.webp"}
    assert (hammer / "e1-1_正面.png").read_bytes() == b"front"
    assert (hammer / "e1-2_侧面_锤头朝左.png").read_bytes() == b"side"
    assert (hammer / "e1-3_背面.webp").read_bytes() == b"back"
    assert (slot(equipment, "主手") / FIST / "e12-1_正面.jpg").read_bytes() == b"fist"


def test_view_reroll_replaces_only_that_view(tmp_path: Path, slot: Slot) -> None:
    root, equipment, downloads = _drama(tmp_path, slot)
    hammer = slot(equipment, "主手") / HAMMER
    _touch(hammer / "e1-1_正面.png", b"old front")
    _touch(hammer / "e1-2_侧面_锤头朝左.png", b"side")
    _drop(downloads, "e1-1_正面.webp", b"new front")

    _run(root, downloads)

    assert not (hammer / "e1-1_正面.png").exists()
    assert (hammer / "e1-1_正面.webp").read_bytes() == b"new front"
    assert (hammer / "e1-2_侧面_锤头朝左.png").read_bytes() == b"side"


def test_leftmost_key_wins_across_equipment_prop_scene_and_character(tmp_path: Path, slot: Slot) -> None:
    root, equipment, downloads = _drama(tmp_path, slot)
    world = root / "ai_videos" / "d" / WORLD
    inn = world / "props" / "p15_两层石木旅店"
    _touch(inn / "asset.toml")
    town = world / "scenes" / "bg4_闪金镇"
    _touch(town / "bg4_闪金镇.md", "# 闪金镇\n".encode("utf-8"))
    _drop(downloads, f"{GEN}e12-1_正面 参考 p15-1_正面.png", b"fist", age_s=50)
    _drop(downloads, f"{GEN}p15-2_侧面 参考 e12-2_侧面.png", b"inn side", age_s=40)
    _drop(downloads, "bg4-1_镇心 参考 e12-3_背面.png", b"town", age_s=30)
    _drop(downloads, f"{GEN}c1-1_林问立绘 参考 e3-1_正面.png", b"portrait", age_s=20)
    # the character's `c1_林问` is the longest token hit, but it starts after the key
    _drop(downloads, f"{GEN}e3-1_正面 皮甲 参考 c1_林问.png", b"armor", age_s=10)

    result = _run(root, downloads)

    assert result.unmatched == [] and result.errors == [], (result.unmatched, result.errors)
    fist, armor = slot(equipment, "主手") / FIST, slot(equipment, "胸") / ARMOR
    assert _files(fist) == {f"{FIST}.md", "item.toml", "e12-1_正面.png"}
    assert (fist / "e12-1_正面.png").read_bytes() == b"fist"
    assert (inn / "p15-2_侧面.png").read_bytes() == b"inn side"
    assert (town / "bg4-1.png").read_bytes() == b"town"
    assert (world / "characters" / "c1_林问" / "c1-1.png").read_bytes() == b"portrait"
    assert _files(armor) == {f"{ARMOR}.md", "item.toml", "e3-1_正面.png"}
    assert (armor / "e3-1_正面.png").read_bytes() == b"armor"


def test_equipment_routes_by_key_only(tmp_path: Path, slot: Slot) -> None:
    """No item folder is a name-token candidate, and a download whose leftmost key
    is an equipment key no item takes is not handed to a word match instead."""
    root, equipment, downloads = _drama(tmp_path, slot)
    before = sorted(p.relative_to(equipment).as_posix() for p in equipment.rglob("*"))
    left = [
        _drop(downloads, "维里甘之拳 特写 电影级.png"),                 # an item's name words
        _drop(downloads, "主手 全部武器.png"),                           # a slot's name
        _drop(downloads, "近战武器 板甲 全部.png"),                       # category names
        _drop(downloads, "kling_render_final.mp4"),                       # an ordinary video
        _drop(downloads, f"{GEN}e12_蓝_维里甘之拳 锚点.png"),              # a bare item key is no view
        _drop(downloads, f"{GEN}e12-.png"),                               # a cut-off view number
        _drop(downloads, f"{GEN}e12-1_正面 转台.mp4"),                    # a video is no view
        _drop(downloads, f"{GEN}e99-1_正面 参考 c1_林问.png"),              # no such item: not c1's
    ]

    result = _run(root, downloads)

    assert result.moved == [] and result.errors == []
    assert len(result.unmatched) == len(left)
    assert all(src.is_file() for src in left)
    assert sorted(p.relative_to(equipment).as_posix() for p in equipment.rglob("*")) == before
    assert _files(root / "ai_videos" / "d" / WORLD / "characters" / "c1_林问") == {"c1_林问.md"}


def test_glb_is_never_routed_into_equipment(tmp_path: Path, slot: Slot) -> None:
    root, equipment, downloads = _drama(tmp_path, slot)
    inn = root / "ai_videos" / "d" / WORLD / "props" / "p15_两层石木旅店"
    _touch(inn / "asset.toml")
    left = [
        _drop(downloads, "tripo_e12_维里甘之拳.glb"),
        _drop(downloads, "e12-1_正面.glb"),
        _drop(downloads, "e1.gltf"),
        # the equipment key comes first: an equipment model, not the prop's mesh
        _drop(downloads, "rodin_e12-1_正面 参考 p15_两层石木旅店.glb"),
    ]
    _drop(downloads, "rodin_p15_两层石木旅店 参考 e12-1_正面.glb", b"mesh")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["prop_mesh"]
    assert (inn / "mesh" / "p15.glb").read_bytes() == b"mesh"
    assert result.errors == [] and len(result.unmatched) == len(left)
    assert all(src.is_file() for src in left)
    assert not list(equipment.rglob("*.glb")) and not list(equipment.rglob("*.gltf"))


def test_item_number_owned_twice_routes_nowhere(tmp_path: Path, slot: Slot) -> None:
    root, equipment, downloads = _drama(tmp_path, slot)
    twin = _item(slot(equipment, "副手") / "e12_紫_另一只拳")
    src = _drop(downloads, "e12-1_正面.png")

    result = _run(root, downloads)

    assert result.moved == [] and result.errors == []
    assert src.is_file()
    assert "e12-1_正面.png" not in _files(slot(equipment, "主手") / FIST) | _files(twin)


def test_item_number_owned_at_two_depths_routes_nowhere(tmp_path: Path) -> None:
    """Nesting never tells two items apart: `板甲/胸/e79_…` and `胸/e79_…` are twins."""
    root = tmp_path / "repo"
    equipment = root / "ai_videos" / "d" / WORLD / "equipment"
    deep = _item(equipment / "板甲" / "胸" / "e79_蓝_光铸胸甲")
    shallow = _item(equipment / "胸" / "e79_蓝_另一件胸甲")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    src = _drop(downloads, f"{GEN}e79-1_正面.png")

    result = _run(root, downloads)

    assert result.moved == [] and result.errors == [] and len(result.unmatched) == 1
    assert src.is_file()
    assert "e79-1_正面.png" not in _files(deep) | _files(shallow)


def test_items_are_found_by_name_at_any_depth(tmp_path: Path) -> None:
    """Whatever unkeyed folders sit above an item are walked through; `loadouts/`,
    `_*` and `.*` folders are never entered, an item's children are never items,
    and a view-keyed folder is no item — so none of those is a twin either."""
    root = tmp_path / "repo"
    drama = root / "ai_videos" / "d"
    equipment = drama / WORLD / "equipment"
    charm = _item(equipment / "e7_白_护身符")                               # no category, no slot
    necklace = _item(equipment / "颈" / "e8_绿_项链")                        # slot only
    chest = _item(equipment / "板甲" / "胸" / "e79_蓝_光铸胸甲")              # category + slot
    maul = _item(equipment / "近战武器" / "双手" / "锤" / "e80_紫_巨锤")       # deeper still
    for not_an_item in (
        equipment / "loadouts" / "e90_白_配装",
        equipment / "板甲" / "loadouts" / "e91_白_配装",
        equipment / "_archive" / "e79_蓝_旧版胸甲",
        equipment / "板甲" / "_old" / "e92_白_旧甲",
        equipment / ".cache" / "e93_白_缓存",
        chest / "e94_白_部件",
        equipment / "板甲" / "e95-1_正面",
    ):
        _item(not_an_item)
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    _drop(downloads, f"{GEN}e7-1_正面.png", b"charm")
    _drop(downloads, f"{GEN}e8-2_侧面.png", b"necklace")
    _drop(downloads, f"{GEN}e79-1_正面 参考 e8-2_侧面.png", b"chest")
    _drop(downloads, f"{GEN}e80-3_背面.png", b"maul")
    left = [_drop(downloads, f"{GEN}e{n}-1_正面.png") for n in (90, 91, 92, 93, 94, 95)]

    assert series_shared.equipment_item_dirs(drama) == sorted([charm, necklace, chest, maul])
    result = _run(root, downloads)

    assert result.errors == [] and len(result.unmatched) == len(left), (result.errors, result.unmatched)
    assert all(src.is_file() for src in left)
    assert (charm / "e7-1_正面.png").read_bytes() == b"charm"
    assert (necklace / "e8-2_侧面.png").read_bytes() == b"necklace"
    assert (chest / "e79-1_正面.png").read_bytes() == b"chest"
    assert (maul / "e80-3_背面.png").read_bytes() == b"maul"


def test_shot_render_quoting_an_equipment_key_stays_in_the_shot(tmp_path: Path, slot: Slot) -> None:
    root, _equipment, downloads = _drama(tmp_path, slot)
    shot = root / "ai_videos" / "d" / "5_6_分镜与prompt" / "episodes" / "ep01" / "shots" / "shot03"
    _touch(shot / "shot03.md", b"shot")
    _drop(downloads, "01集03镜视 参考 e12-1_正面.mp4", b"render")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["shot"]
    assert (shot / "renders" / "01集03镜视 参考 e12-1_正面.mp4").is_file()


def test_flat_legacy_layout_routes_too(tmp_path: Path, slot: Slot) -> None:
    root = tmp_path / "repo"
    cap = _item(slot(root / "ai_videos" / "d" / "equipment", "头") / "e2_灰_皮帽")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    _drop(downloads, f"{GEN}e2-1_正面.png", b"cap")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["equipment_view"]
    assert (cap / "e2-1_正面.png").read_bytes() == b"cap"


def test_series_member_imports_into_shared_equipment_beside_its_own(tmp_path: Path, slot: Slot) -> None:
    root, episode, shared, downloads = _series(tmp_path)
    own = _item(slot(episode, "主手") / "e21_白_短剑")
    # one category / slot name on both sides is no conflict
    common = _item(slot(shared, "主手") / "e5_紫_铜锤")
    _drop(downloads, f"{GEN}e21-1_正面.png", b"own", age_s=40)
    _drop(downloads, f"{GEN}e5-2_侧面 参考 e21-1_正面.png", b"common")

    result = _run(root, downloads, f"{SERIES_REL}/ep1")

    assert result.errors == [] and result.unmatched == [], (result.errors, result.unmatched)
    assert (own / "e21-1_正面.png").read_bytes() == b"own"
    assert (common / "e5-2_侧面.png").read_bytes() == b"common"
    assert series_shared.equipment_item_dirs(root / SERIES_REL / "ep1") == [own, common]


def test_one_item_number_on_both_sides_is_reported(tmp_path: Path, slot: Slot) -> None:
    root, episode, shared, downloads = _series(tmp_path)
    mine = _item(slot(episode, "主手") / "e5_紫_另一把锤")
    theirs = _item(slot(shared, "主手") / "e5_紫_铜锤")
    free = _item(slot(episode, "胸") / "e21_白_布衣")
    blocked = _drop(downloads, f"{GEN}e5-1_正面.png", b"blocked", age_s=40)
    _drop(downloads, f"{GEN}e21-1_正面.png", b"free")

    result = _run(root, downloads, f"{SERIES_REL}/ep1")

    assert blocked.read_bytes() == b"blocked"
    assert result.unmatched == []
    [error] = result.errors
    assert error["message"].startswith("series_key_conflict:")
    assert mine.relative_to(root).as_posix() in error["message"]
    assert theirs.relative_to(root).as_posix() in error["message"]
    assert (free / "e21-1_正面.png").read_bytes() == b"free"


def test_series_conflict_ignores_nesting_and_tool_owned_folders(tmp_path: Path) -> None:
    """The same number at two depths is still one number on both sides; a copy
    under `_series/`'s `_archive/` or `loadouts/` owns nothing."""
    root, episode, shared, downloads = _series(tmp_path)
    mine = _item(episode / "板甲" / "胸" / "e5_紫_另一件胸甲")
    theirs = _item(shared / "胸" / "e5_紫_铜胸甲")
    free = _item(episode / "板甲" / "胸" / "e21_白_布衣")
    _item(shared / "_archive" / "e21_白_布衣")
    _item(shared / "loadouts" / "e21_白_布衣")
    blocked = _drop(downloads, f"{GEN}e5-1_正面.png", b"blocked", age_s=40)
    _drop(downloads, f"{GEN}e21-1_正面.png", b"free")

    result = _run(root, downloads, f"{SERIES_REL}/ep1")

    assert blocked.read_bytes() == b"blocked"
    assert result.unmatched == []
    [error] = result.errors
    assert error["message"].startswith("series_key_conflict:")
    assert mine.relative_to(root).as_posix() in error["message"]
    assert theirs.relative_to(root).as_posix() in error["message"]
    assert (free / "e21-1_正面.png").read_bytes() == b"free"
