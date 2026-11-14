"""Character / prop folders may sit one unkeyed group folder down (follow-up 284).

dota_yingxiong splits its cards by side: `characters/近卫_sentinel/c65_Axe/`,
`props/中立_neutral/p1_极速神符/`. Every place that lists a drama's cards — the
gallery listing, extract-all, the extraction-button guard, Downloads routing,
the shot materials and the series conflict scan — must find grouped cards and
never treat the group itself as an asset. Flat dramas stay exactly as they were.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from libs.common import asset_group, drama_layout, series_shared
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.readers.character__reader import CharacterReader
from libs.infrastructure.readers.shot_materials__reader import ShotMaterialsReader
from libs.infrastructure.readers.tree__reader import TreeReader
from libs.infrastructure.writers.character_video__writer import (
    CharacterViewExtractor,
    is_under_character_folder,
)
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer

DRAMA_REL = "ai_videos/demo"
WORLD = "2_世界观人设"
CHARS_REL = f"{DRAMA_REL}/{WORLD}/characters"
LAYOUTS = {"flat": ("", ""), "grouped": ("近卫_sentinel/", "中立_neutral/")}


def _write(path: Path, data: bytes = b"x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


@pytest.fixture(params=sorted(LAYOUTS))
def drama(request: pytest.FixtureRequest, tmp_path: Path) -> tuple[Path, str, str]:
    char_group, prop_group = LAYOUTS[request.param]
    root = tmp_path / "repo"
    world = root / DRAMA_REL / WORLD
    _write(world / "characters" / f"{char_group}c65_Axe" / "c65_Axe.md", "# Axe · 斧王\n".encode())
    _write(world / "characters" / f"{char_group}c65_Axe" / "c65_Axe_turntable.mp4")
    _write(world / "characters" / "m4_Ghoul" / "m4_Ghoul.md")
    _write(world / "props" / f"{prop_group}p1_极速神符" / "p1_极速神符.md")
    _write(world / "props" / f"{prop_group}p1_极速神符" / "p1_极速神符.png")
    _write(root / DRAMA_REL / "workflow.json", b"{}")
    return root, char_group, prop_group


def test_asset_group_lists_cards_not_groups(drama: tuple[Path, str, str]) -> None:
    root, char_group, _ = drama
    chars = root / CHARS_REL
    assert sorted(d.name for d in asset_group.character_dirs(chars)) == ["c65_Axe", "m4_Ghoul"]
    assert [d.name for d in asset_group.group_dirs(chars, asset_group.is_character_name)] == (
        [char_group.rstrip("/")] if char_group else [])
    assert asset_group.find_character_dir(chars, "c65_Axe") == chars / f"{char_group}c65_Axe"


def test_unkeyed_folder_without_keyed_children_stays_an_asset(tmp_path: Path) -> None:
    props = tmp_path / "props"
    _write(props / "玉佩" / "玉佩.md")
    _write(props / "中立_neutral" / "p2_回复神符" / "p2_回复神符.md")
    names = [d.name for d in asset_group.grouped_dirs(props, lambda n: n.startswith("p2_"))]
    assert names == ["p2_回复神符", "玉佩"]


def test_series_asset_dirs_expand_groups(drama: tuple[Path, str, str]) -> None:
    root, _, _ = drama
    drama_dir = root / DRAMA_REL
    assert sorted(d.name for d in series_shared.asset_dirs(drama_dir, drama_layout.characters_dir)) == ["c65_Axe", "m4_Ghoul"]
    assert [d.name for d in series_shared.asset_dirs(drama_dir, drama_layout.props_dir)] == ["p1_极速神符"]


def test_gallery_listing_and_extract_all_see_grouped_cards(drama: tuple[Path, str, str]) -> None:
    root, char_group, _ = drama
    exposed, resolver = ExposedTree(repo_root=root), SafeResolver(root=root)
    listing = CharacterReader(exposed, resolver).list_latest_videos(CHARS_REL)
    assert [(item.folder, item.latest_video_rel) for item in listing] == [
        ("c65_Axe", f"{CHARS_REL}/{char_group}c65_Axe/c65_Axe_turntable.mp4"),
        ("m4_Ghoul", None),
    ]
    batch = CharacterViewExtractor(exposed, resolver).extract_all(CHARS_REL)
    assert [(item.folder, item.status) for item in batch.items][1] == ("m4_Ghoul", "skipped")
    assert batch.items[0].folder == "c65_Axe"


def test_extraction_guard_accepts_grouped_turntables(drama: tuple[Path, str, str]) -> None:
    root, char_group, _ = drama
    assert is_under_character_folder(root, f"{CHARS_REL}/{char_group}c65_Axe/c65_Axe_turntable.mp4") is True
    assert is_under_character_folder(root, f"{CHARS_REL}/近卫_sentinel/a.mp4") is False


def test_downloads_route_into_a_grouped_card(drama: tuple[Path, str, str], tmp_path: Path) -> None:
    root, char_group, _ = drama
    downloads = tmp_path / "Downloads"
    src = _write(downloads / "ElevenLabs_image_c65-1_斧王立绘 一个_2026-10-18T08_00_00.png", b"axe")
    stamp = time.time() - 30
    os.utime(src, (stamp, stamp))
    exposed, resolver = ExposedTree(repo_root=root), SafeResolver(root=root)
    importer = DownloadsImporter(exposed=exposed, resolver=resolver,
                                 renamer=MediaRenamer(exposed=exposed, resolver=resolver), downloads_dir=downloads)
    result = importer.import_drama(DRAMA_REL)
    assert result.errors == []
    assert (root / CHARS_REL / f"{char_group}c65_Axe" / "c65-1.png").read_bytes() == b"axe"
    assert not any((root / CHARS_REL / "近卫_sentinel").glob("*.png"))


def test_shot_materials_find_grouped_cast_and_props(drama: tuple[Path, str, str]) -> None:
    root, char_group, prop_group = drama
    reader = ShotMaterialsReader(root)
    assert reader._card(root / DRAMA_REL, "c65") == root / CHARS_REL / f"{char_group}c65_Axe"
    errors: list[str] = []
    [prop] = reader._props(root / DRAMA_REL, ["p1"], errors)
    assert prop.image == f"{DRAMA_REL}/{WORLD}/props/{prop_group}p1_极速神符/p1_极速神符.png"


def test_tree_shows_the_group_level(drama: tuple[Path, str, str]) -> None:
    root, char_group, _ = drama
    tree = TreeReader(ExposedTree(repo_root=root)).subtree(CHARS_REL, depth=None)
    children = {c["name"]: c for c in tree["children"]}
    assert sorted(children) == sorted([char_group.rstrip("/") or "c65_Axe", "m4_Ghoul"])
    if char_group:
        assert [c["name"] for c in children[char_group.rstrip("/")]["children"]] == ["c65_Axe"]
