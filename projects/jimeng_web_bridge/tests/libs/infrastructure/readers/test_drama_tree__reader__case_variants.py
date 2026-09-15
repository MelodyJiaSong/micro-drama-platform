"""U2-SEC-06: hard-excluded folder names are excluded in any case; NTFS names are case-insensitive."""
from __future__ import annotations

from pathlib import Path

import pytest

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from tests.libs.infrastructure.support import write_file

EXCLUDE: list[str] = ["_deleted", "_candidates", "renders", "frames", "_blender"]
HY3 = "ai_videos/hs/hy3"
SHOT01 = f"{HY3}/shots/shot01"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, f"{SHOT01}/shot01.md", "x")
    write_file(tmp_path, f"{SHOT01}/Renders/bg5-1.png", b"render")
    write_file(tmp_path, f"{SHOT01}/Renders/shot01_render.mp4", b"render")
    write_file(tmp_path, f"{SHOT01}/FRAMES/bg8-1.png", b"frame")
    write_file(tmp_path, f"{HY3}/props/p2_y/_Candidates/p2-1/p2-1.png", b"candidate")
    write_file(tmp_path, f"{HY3}/scenes/x/_DELETED/bg6-1.png", b"deleted")
    write_file(tmp_path, f"{HY3}/characters/c1_老人/c1_老人.md", "#")
    write_file(tmp_path, f"{HY3}/RENDERS/characters/c9_r/c9_r.md", "#")
    write_file(tmp_path, f"{HY3}/characters/Renders/Renders.md", "#")
    write_file(tmp_path, "ai_videos/RENDERS/shots/shot01.md", "x")
    write_file(tmp_path, "ai_videos/RENDERS/bg7-1.png", b"x")
    write_file(tmp_path, "ai_videos/hs/Renders/shot01.md", "x")
    return tmp_path


def test_name_helpers_casefold() -> None:
    assert drama_ref.is_hard_excluded_name("_CANDIDATES")
    assert drama_ref.is_hard_excluded_name("Renders")
    assert drama_ref.inside_hard_excluded("ai_videos/hs/hy3/shots/shot01/Renders/x.png")
    assert drama_ref.inside_hard_excluded("ai_videos/_Deleted/x.png")
    assert not drama_ref.inside_hard_excluded("ai_videos/hs/hy3/renderings/x.png")


def test_case_variant_folders_are_never_listed_as_dramas(repo: Path) -> None:
    nodes = {node.name: node for node in DramaTreeReader(RepoSandbox(repo)).list_dramas()}
    assert set(nodes) == {"hs"}
    assert [child.name for child in nodes["hs"].children] == ["hy3"]
    assert [path.name for path in drama_ref.drama_dirs(repo)] == ["hy3"]


@pytest.mark.parametrize("rel", ["ai_videos/RENDERS", "ai_videos/hs/Renders"])
def test_case_variant_folder_is_not_a_drama_root_or_write_target(repo: Path, rel: str) -> None:
    sandbox = RepoSandbox(repo)
    assert drama_ref.drama_root_rel(repo, rel.split("/")) is None
    assert DramaTreeReader(sandbox).search_bases(rel) == ()
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigReader(sandbox).read(rel)
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigWriter(sandbox).save(rel, {"drama": {"abbrev": "x"}}, None)
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigWriter(sandbox).save_text(rel, "[drama]\n", None)
    assert list(repo.rglob("jimeng_config.toml")) == []


@pytest.mark.parametrize("name", ["bg5-1", "p2-1", "bg6-1"])
def test_asset_resolver_ignores_case_variant_excluded_folders(repo: Path, name: str) -> None:
    result = DramaTreeReader(RepoSandbox(repo)).resolve_asset_file(HY3, name, EXCLUDE)
    assert (result.status, result.reason) == ("not_found", "no_match")


def test_file_index_never_leaks_case_variant_excluded_entries(repo: Path) -> None:
    sandbox = RepoSandbox(repo)
    entries = DramaTreeReader(sandbox).list_files(HY3, EXCLUDE)
    assert entries
    assert not [entry.rel for entry in entries if drama_ref.inside_hard_excluded(entry.rel) or "/FRAMES/" in entry.rel]
    index = FileIndexReader(sandbox)
    assert index.list_files(f"{SHOT01}/Renders", []) == ()
    assert index.list_files(f"{HY3}/props/p2_y/_Candidates", []) == ()
    assert index.list_files(f"{HY3}/scenes/x/_DELETED", []) == ()


def test_config_search_exclude_is_case_insensitive(repo: Path) -> None:
    tree = DramaTreeReader(RepoSandbox(repo))
    assert tree.resolve_asset_file(HY3, "bg8-1", []).status == "found"
    assert tree.resolve_asset_file(HY3, "bg8-1", ["frames"]).status == "not_found"
    assert tree.resolve_asset_file(HY3, "bg8-1", ["Frames"]).status == "not_found"


def test_shot_video_resolver_ignores_case_variant_renders(repo: Path) -> None:
    tree = DramaTreeReader(RepoSandbox(repo))
    inside = tree.resolve_shot_video(SHOT01, "shot01_render", EXCLUDE)
    assert (inside.status, inside.reason) == ("not_found", "no_match")
    as_base = tree.resolve_shot_video(f"{SHOT01}/Renders", "shot01_render", EXCLUDE)
    assert (as_base.status, as_base.reason) == ("not_found", "invalid_path")
    frame = tree.resolve_prev_shot_lastframe(f"{HY3}/RENDERS/shot02", "本镜首帧")
    assert (frame.status, frame.reason) == ("not_found", "invalid_path")


def test_cards_under_case_variant_excluded_folders_are_ignored(repo: Path) -> None:
    tree = DramaTreeReader(RepoSandbox(repo))
    assert [card.dir_name for card in tree.character_cards(HY3)] == ["c1_老人"]
    assert tree.asset_card_paths(HY3) == (f"{HY3}/characters/c1_老人/c1_老人.md",)
