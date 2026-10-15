"""drama_layout resolves assets for both on-disk layouts (folders directly at the
drama root, or under `2_世界观人设/`), and finds shot folders only in the
six-module layout `episodes/epNN/scenes/sN/shots/stN/`.

The old stage layouts (`4_剧本/`, `5_6_分镜与prompt/`, `shots/shotNN/`,
single-piece `shots/`) and `casting.md` went with the old pipeline (follow-up 233).
"""
from __future__ import annotations

from pathlib import Path

from libs.common import drama_layout as dl


def _mk(base: Path, *rel: str) -> None:
    for r in rel:
        p = base / r
        if r.endswith(".md"):
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x", encoding="utf-8")
        else:
            p.mkdir(parents=True, exist_ok=True)


def test_flat_layout(tmp_path: Path) -> None:
    d = tmp_path / "legacy"
    _mk(d, "characters", "scenes", "episodes")
    assert dl.characters_dir(d) == d / "characters"
    assert dl.scenes_dir(d) == d / "scenes"
    assert dl.episodes_dir(d) == d / "episodes"


def test_world_stage_layout(tmp_path: Path) -> None:
    d = tmp_path / "staged"
    _mk(d, "2_世界观人设/characters", "2_世界观人设/background", "2_世界观人设/props")
    assert dl.characters_dir(d) == d / "2_世界观人设" / "characters"
    assert dl.background_dir(d) == d / "2_世界观人设" / "background"
    assert dl.props_dir(d) == d / "2_世界观人设" / "props"


def test_episodes_live_at_the_drama_root_only(tmp_path: Path) -> None:
    # The removed stage folders are no longer consulted.
    d = tmp_path / "old_stages"
    _mk(d, "4_剧本/episodes", "5_6_分镜与prompt/episodes/ep01/shots/shot01")
    assert dl.episodes_dir(d) == d / "episodes"


def test_flat_wins_when_both_present(tmp_path: Path) -> None:
    d = tmp_path / "both"
    _mk(d, "characters", "2_世界观人设/characters")
    assert dl.characters_dir(d) == d / "characters"


def test_missing_falls_back_to_flat_root(tmp_path: Path) -> None:
    d = tmp_path / "empty"
    d.mkdir()
    # nothing on disk → default to flat root so first-time create lands sanely
    assert dl.characters_dir(d) == d / "characters"


def test_episode_shot_dirs_ignores_old_shot_folders(tmp_path: Path) -> None:
    ep = tmp_path / "drama" / "episodes" / "ep01"
    _mk(ep, "shots/shot01", "prompts/shot02")
    assert dl.episode_shot_dirs(ep) == []
    _mk(ep, "scenes/s2/shots/st1", "scenes/s1/shots/st10", "scenes/s1/shots/st2")
    assert [p.relative_to(ep).as_posix() for p in dl.episode_shot_dirs(ep)] == [
        "scenes/s1/shots/st2", "scenes/s1/shots/st10", "scenes/s2/shots/st1",
    ]
