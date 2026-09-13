"""drama_layout resolves assets for both on-disk layouts (legacy flat root +
staged pipeline `2_世界观人设/` & `4_剧本/`). Regression guard for the bug where
assign-actor / import / sub-type broke after a drama was migrated to the
staged structure.
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
    _mk(d, "casting.md", "characters", "scenes", "episodes")
    assert dl.casting_md(d) == d / "casting.md"
    assert dl.characters_dir(d) == d / "characters"
    assert dl.scenes_dir(d) == d / "scenes"
    assert dl.episodes_dir(d) == d / "episodes"


def test_staged_layout(tmp_path: Path) -> None:
    d = tmp_path / "staged"
    _mk(
        d,
        "2_世界观人设/casting.md",
        "2_世界观人设/characters",
        "2_世界观人设/scenes",
        "4_剧本/episodes",
    )
    assert dl.casting_md(d) == d / "2_世界观人设" / "casting.md"
    assert dl.characters_dir(d) == d / "2_世界观人设" / "characters"
    assert dl.scenes_dir(d) == d / "2_世界观人设" / "scenes"
    assert dl.episodes_dir(d) == d / "4_剧本" / "episodes"


def test_shots_stage_episodes_wins_over_script_stage(tmp_path: Path) -> None:
    # The shot/render episodes live under 5_6_分镜与prompt/episodes/ (with
    # shots/shot{NN}/), while 4_剧本/episodes/ is script-only. Render-side
    # consumers (downloads import, episode compose, bgm scan) must resolve to
    # the 5_6 stage — routing to 4_剧本 was the shot-render misroute bug.
    d = tmp_path / "staged_5_6"
    _mk(d, "4_剧本/episodes", "5_6_分镜与prompt/episodes/ep01/shots/shot01")
    assert dl.episodes_dir(d) == d / "5_6_分镜与prompt" / "episodes"


def test_flat_wins_when_both_present(tmp_path: Path) -> None:
    d = tmp_path / "both"
    _mk(d, "characters", "2_世界观人设/characters")
    assert dl.characters_dir(d) == d / "characters"


def test_missing_falls_back_to_flat_root(tmp_path: Path) -> None:
    d = tmp_path / "empty"
    d.mkdir()
    # nothing on disk → default to flat root so first-time create lands sanely
    assert dl.casting_md(d) == d / "casting.md"
    assert dl.characters_dir(d) == d / "characters"


def test_shot_tree_roots_multi_episode(tmp_path: Path) -> None:
    d = tmp_path / "md"
    for ep in ("ep01", "ep02"):
        (d / dl.SHOTS_STAGE / "episodes" / ep / "shots").mkdir(parents=True)

    roots = dl.shot_tree_roots(d)

    assert [r.name for r in roots] == ["ep01", "ep02"]
    assert dl.shot_tree_slug(roots[0], d) == "ep01"


def test_shot_tree_roots_single_piece(tmp_path: Path) -> None:
    """No `episodes/` layer at all — the one shot tree is the stage dir itself,
    and its slug (＝ the stitched master's stem) is the drama name."""
    d = tmp_path / "sp"
    (d / dl.SHOTS_STAGE / "shots" / "shot01").mkdir(parents=True)

    roots = dl.shot_tree_roots(d)

    assert len(roots) == 1 and roots[0].name == dl.SHOTS_STAGE
    assert dl.shot_tree_slug(roots[0], d) == "sp"
    assert not dl.is_episode_root(roots[0])


def test_shot_tree_for_resolves_both_layouts(tmp_path: Path) -> None:
    md = tmp_path / "md"
    (md / dl.SHOTS_STAGE / "episodes" / "ep03" / "shots").mkdir(parents=True)
    hit = dl.shot_tree_for(
        md, "ai_videos/md/5_6_分镜与prompt/episodes/ep03/shots/shot01".split("/")
    )
    assert hit is not None and hit[0].name == "ep03" and hit[1] == "ep03"

    sp = tmp_path / "sp"
    (sp / dl.SHOTS_STAGE / "shots" / "shot01").mkdir(parents=True)
    hit2 = dl.shot_tree_for(sp, "ai_videos/sp/README.md".split("/"))
    assert hit2 is not None and hit2[1] == "sp"


def test_shot_tree_for_returns_none_when_drama_has_no_shots(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    (empty / dl.WORLD_STAGE).mkdir(parents=True)

    assert dl.shot_tree_roots(empty) == []
    assert dl.shot_tree_for(empty, "ai_videos/empty/README.md".split("/")) is None
