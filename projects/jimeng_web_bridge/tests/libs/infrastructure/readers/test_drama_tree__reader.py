from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from tests.libs.infrastructure.support import write_file

HY1 = "ai_videos/hs/hy1"
HY2 = "ai_videos/hs/hy2"


@pytest.fixture
def tree(tmp_path: Path) -> DramaTreeReader:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, "ai_videos/hs/_series/series_bible.md", "x")
    write_file(tmp_path, f"{HY1}/2_世界观人设/characters/c1_造家的人/c1_造家的人.png", b"face")
    write_file(tmp_path, f"{HY1}/2_世界观人设/characters/c1_造家的人/c1_造家的人.md", "#")
    write_file(tmp_path, f"{HY2}/2_世界观人设/characters/c1_造家的人/c1_造家的人.md", "#")
    write_file(
        tmp_path,
        f"{HY2}/2_世界观人设/characters/c1_造家的人/c1_造家的人.png.link.json",
        json.dumps({"target": f"{HY1}/2_世界观人设/characters/c1_造家的人/c1_造家的人.png"}),
    )
    write_file(tmp_path, f"{HY2}/2_世界观人设/characters/c2_香蕉蛞蝓/c2-1_香蕉蛞蝓锚点.png", b"slug")
    write_file(tmp_path, f"{HY2}/2_世界观人设/characters/_cast/readme.md", "x")
    write_file(tmp_path, f"{HY2}/2_世界观人设/scenes/hongshan/bg1_地窝/bg1_地窝.md", "#")
    write_file(tmp_path, f"{HY2}/2_世界观人设/scenes/hongshan/bg1_地窝/_candidates/bg1-1/x.md", "#")
    write_file(tmp_path, f"{HY2}/2_世界观人设/props/p3_树皮门与顶/p3_树皮门与顶.md", "#")
    write_file(tmp_path, f"{HY2}/2_世界观人设/props/p3_树皮门与顶/notes.md", "#")
    write_file(tmp_path, "ai_videos/flat/characters/driver/driver.md", "#")
    write_file(tmp_path, "ai_videos/flat/characters/c1_x/c1_x.md", "#")
    write_file(tmp_path, "ai_videos/flat/characters/c2_x/c2_x.md", "#")
    write_file(tmp_path, "ai_videos/notes/note.txt", "n")
    write_file(tmp_path, "ai_videos/renders/shots/shot01.md", "x")
    write_file(tmp_path, "ai_videos/empty_series/series.json", "{}")
    write_file(tmp_path, "ai_videos/_deleted/old/shot01.md", "x")
    return DramaTreeReader(RepoSandbox(tmp_path))


def test_list_dramas_nests_series_and_filters_unlistable(tree: DramaTreeReader) -> None:
    nodes = tree.list_dramas()
    assert [(n.name, n.node_type, n.path) for n in nodes] == [
        ("flat", "drama", "ai_videos/flat"),
        ("hs", "series", "ai_videos/hs"),
    ]
    assert [(c.name, c.node_type, c.path, c.children) for c in nodes[1].children] == [
        ("hy1", "drama", HY1, ()),
        ("hy2", "drama", HY2, ()),
    ]


def test_drama_root_of(tree: DramaTreeReader) -> None:
    assert tree.drama_root_of(f"{HY2}/2_世界观人设/props") == HY2
    assert tree.drama_root_of("ai_videos/flat/characters") == "ai_videos/flat"
    assert tree.drama_root_of("ai_videos\\flat\\characters") is None
    assert tree.drama_root_of("ai_videos/flat\\..\\..\\outside") is None
    assert tree.drama_root_of("ai_videos/hs/_series/x.md") is None
    assert tree.search_bases(HY2) == (HY2, "ai_videos/hs/_series")
    assert tree.search_bases("ai_videos/flat") == ("ai_videos/flat",)
    assert tree.search_bases("ai_videos/hs") == ()


def test_character_cards_with_link_source(tree: DramaTreeReader) -> None:
    cards = {card.dir_name: card for card in tree.character_cards(HY2)}
    assert set(cards) == {"c1_造家的人", "c2_香蕉蛞蝓"}
    maker = cards["c1_造家的人"]
    assert (maker.character_name, maker.c_prefix, maker.linked_source_drama) == ("造家的人", "c1", HY1)
    assert maker.dir_rel == f"{HY2}/2_世界观人设/characters/c1_造家的人"
    assert cards["c2_香蕉蛞蝓"].linked_source_drama is None
    assert tree.character_cards(HY1)[0].linked_source_drama is None


def test_find_character_card(tree: DramaTreeReader) -> None:
    by_name = tree.find_character_card(HY2, "造家的人")
    assert (by_name.status, by_name.step, by_name.path) == (
        "found",
        "character_name",
        f"{HY2}/2_世界观人设/characters/c1_造家的人",
    )
    driver = tree.find_character_card("ai_videos/flat", "driver")
    assert (driver.status, driver.step) == ("found", "dir_name")
    assert tree.find_character_card("ai_videos/flat", "x").status == "ambiguous"
    assert tree.find_character_card("ai_videos/flat", "c1_x").status == "found"
    assert tree.find_character_card(HY2, "nobody").status == "not_found"


def test_asset_card_paths(tree: DramaTreeReader) -> None:
    assert set(tree.asset_card_paths(HY2)) == {
        f"{HY2}/2_世界观人设/characters/c1_造家的人/c1_造家的人.md",
        f"{HY2}/2_世界观人设/scenes/hongshan/bg1_地窝/bg1_地窝.md",
        f"{HY2}/2_世界观人设/props/p3_树皮门与顶/p3_树皮门与顶.md",
    }


def test_sha256_and_sandbox(tree: DramaTreeReader, tmp_path: Path) -> None:
    rel = f"{HY1}/2_世界观人设/characters/c1_造家的人/c1_造家的人.png"
    assert tree.sha256(rel) == hashlib.sha256(b"face").hexdigest()
    with pytest.raises(SandboxError):
        tree.sha256("ai_videos/../projects/x")
    with pytest.raises(SandboxError) as caught:
        tree.sha256(f"{HY1}/2_世界观人设/characters")
    assert caught.value.reason == "not_a_file"
    assert str(tmp_path) not in str(caught.value)


def test_list_files_marks_links(tree: DramaTreeReader) -> None:
    entries = {entry.rel: entry for entry in tree.list_files(HY2, [])}
    link = entries[f"{HY2}/2_世界观人设/characters/c1_造家的人/c1_造家的人.png.link.json"]
    assert (link.stem, link.ext, link.is_link, link.parent_name) == ("c1_造家的人", ".png", True, "c1_造家的人")
    assert "ai_videos/hs/_series/series_bible.md" in entries
    assert not any("_candidates" in rel for rel in entries)
