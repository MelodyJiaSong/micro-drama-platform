from __future__ import annotations

from pathlib import Path

import pytest

from libs.common import drama_ref
from tests.libs.infrastructure.support import make_symlink, require_junction, require_repo_root, write_file

HY3_SHOT = "ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md"


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return require_repo_root()


@pytest.mark.requires_real_repo
def test_series_member_is_depth_three(repo_root: Path) -> None:
    parts = HY3_SHOT.split("/")
    assert drama_ref.drama_depth(repo_root, parts) == 3
    assert drama_ref.drama_root_rel(repo_root, parts) == "ai_videos/huangye_shenghuo/hy3"
    assert drama_ref.split_drama_rel(repo_root, HY3_SHOT) == (
        "ai_videos/huangye_shenghuo/hy3",
        ["5_6_分镜与prompt", "shots", "shot02", "shot02.md"],
    )


@pytest.mark.requires_real_repo
def test_flat_drama_is_depth_two(repo_root: Path) -> None:
    parts = "ai_videos/wushen_juexing/5_6_分镜与prompt/episodes/ep01/shots/shot03/shot03.md".split("/")
    assert drama_ref.drama_depth(repo_root, parts) == 2


@pytest.mark.requires_real_repo
@pytest.mark.parametrize(
    "rel",
    [
        "ai_videos/huangye_shenghuo/_series/series_bible.md",
        "ai_videos/_deleted/x/shot01.md",
        "ai_videos/huangye_shenghuo",
        "ai_videos/_actors/x.png",
        "ai_videos/huangye_shenghuo\\hy3\\renders",
        "ai_videos\\huangye_shenghuo\\hy3",
        "ai_videos/huangye_shenghuo/hy3\\renders",
    ],
)
def test_not_under_a_drama(repo_root: Path, rel: str) -> None:
    assert drama_ref.drama_root_rel(repo_root, rel.split("/")) is None
    if "\\" in rel:
        assert drama_ref.split_drama_rel(repo_root, rel) is None


@pytest.mark.requires_real_repo
def test_real_drama_dirs_and_listability(repo_root: Path) -> None:
    names = {path.relative_to(repo_root / "ai_videos").as_posix() for path in drama_ref.drama_dirs(repo_root)}
    assert {f"huangye_shenghuo/hy{n}" for n in range(1, 5)} <= names
    assert {"wushen_juexing", "duikang_shangzeng", "rexue_gaoxiao", "xingji_yingjiu"} <= names
    assert "huangye_shenghuo" not in names
    assert not any(name.startswith("_") or "/_" in name for name in names)
    assert "notes" in names
    assert not drama_ref.is_listable_drama(repo_root / "ai_videos" / "notes")
    assert drama_ref.is_listable_drama(repo_root / "ai_videos" / "huangye_shenghuo" / "hy3")
    series = [path.name for path in drama_ref.series_dirs(repo_root)]
    assert "huangye_shenghuo" in series
    # xianjian_yi is a series from the moment series.json lands, before any episode exists.
    assert "xianjian_yi" in series
    # The series root is never itself a drama; everything it contributes is an xjN episode.
    assert "xianjian_yi" not in names
    assert all(
        name.split("/")[1].startswith("xj")
        for name in names
        if name.startswith("xianjian_yi/")
    )


def test_flat_drama_with_hy1_subdir_stays_depth_two(tmp_path: Path) -> None:
    write_file(tmp_path, "ai_videos/flat/hy1/shots/shot01/shot01.md", "x")
    assert drama_ref.drama_depth(tmp_path, ["ai_videos", "flat", "hy1", "shots"]) == 2


def test_underscore_and_hard_excluded_dirs_are_never_dramas(tmp_path: Path) -> None:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, "ai_videos/hs/_x/shot01.md", "x")
    write_file(tmp_path, "ai_videos/hs/renders/shot01.md", "x")
    write_file(tmp_path, "ai_videos/hs/hy1/shot01.md", "x")
    write_file(tmp_path, "ai_videos/_lib/shot01.md", "x")
    write_file(tmp_path, "ai_videos/renders/shot01.md", "x")
    assert drama_ref.drama_depth(tmp_path, ["ai_videos", "hs", "_x", "shot01.md"]) is None
    assert drama_ref.drama_depth(tmp_path, ["ai_videos", "hs", "renders"]) is None
    assert drama_ref.drama_depth(tmp_path, ["ai_videos", "_lib", "shot01.md"]) is None
    assert drama_ref.drama_depth(tmp_path, ["ai_videos", "renders"]) is None
    assert [p.name for p in drama_ref.drama_dirs(tmp_path)] == ["hy1"]
    assert drama_ref.series_shared_rel("ai_videos/hs/hy1") == "ai_videos/hs/_series"
    assert drama_ref.series_shared_rel("ai_videos/flat") is None


@pytest.mark.parametrize(
    "parts",
    [
        [],
        ["ai_videos"],
        ["x", "y"],
        ["ai_videos", ""],
        ["ai_videos", ".."],
        ["ai_videos", "a:b"],
        ["ai_videos", "CON"],
        ["ai_videos", "flat\\sub"],
        ["ai_videos\\flat"],
    ],
)
def test_degenerate_parts(tmp_path: Path, parts: list[str]) -> None:
    (tmp_path / "ai_videos" / "flat" / "sub").mkdir(parents=True)
    assert drama_ref.drama_depth(tmp_path, parts) is None


def test_canonical_rel_helpers() -> None:
    assert drama_ref.canonical_rel_violation("ai_videos/hs/hy3") is None
    assert drama_ref.canonical_rel_violation("ai_videos/hs\\hy3") == "backslash_separator"
    assert drama_ref.canonical_rel_violation("ai_videos/hs/../x") == "traversal"
    assert drama_ref.inside_hard_excluded("ai_videos/hs/hy3/renders/x")
    assert drama_ref.inside_hard_excluded("ai_videos/_deleted/hs")
    assert not drama_ref.inside_hard_excluded("ai_videos/hs/_series")


def test_listable_rules(tmp_path: Path) -> None:
    write_file(tmp_path, "ai_videos/notes/note.txt", "n")
    write_file(tmp_path, "ai_videos/configured/jimeng_config.toml", "")
    (tmp_path / "ai_videos" / "assets_only" / "2_世界观人设" / "props").mkdir(parents=True)
    write_file(tmp_path, "ai_videos/deep_shots/5_6/shots/shot07/shot07.md", "x")
    write_file(tmp_path, "ai_videos/deleted_only/_deleted/shots/shot01.md", "x")
    root = tmp_path / "ai_videos"
    assert not drama_ref.is_listable_drama(root / "notes")
    assert drama_ref.is_listable_drama(root / "configured")
    assert drama_ref.is_listable_drama(root / "assets_only")
    assert drama_ref.is_listable_drama(root / "deep_shots")
    assert not drama_ref.is_listable_drama(root / "deleted_only")


def test_junctioned_drama_is_skipped(tmp_path: Path) -> None:
    write_file(tmp_path, "elsewhere/shot01.md", "x")
    (tmp_path / "ai_videos").mkdir()
    require_junction(tmp_path / "ai_videos" / "linked", tmp_path / "elsewhere")
    assert drama_ref.drama_dirs(tmp_path) == []


def test_symlinked_drama_is_skipped(tmp_path: Path) -> None:
    write_file(tmp_path, "elsewhere/shot01.md", "x")
    (tmp_path / "ai_videos").mkdir()
    if not make_symlink(tmp_path / "ai_videos" / "linked", tmp_path / "elsewhere", is_dir=True):
        pytest.skip("symlink creation not permitted (Windows needs Developer Mode)")
    assert drama_ref.drama_dirs(tmp_path) == []
