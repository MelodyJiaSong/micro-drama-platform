"""Drama-level production-console ops:
  - DramaTakesSelector: drama-wide 定版 — lock every episode's newest takes to
    shot{NN}.mp4 in one pass (delegates to the per-episode selector).
  - DramaEpisodesReader: list a drama's shot trees (shot count, locked count,
    whether the stitched master exists) for the dashboard's per-row concat button.

Both must work for **single-piece dramas too** (`sub_type=short`: no `episodes/`
layer at all, shots at `5_6_分镜与prompt/shots/`). They used to glob `episodes/`
directly and silently no-op'd on those — 全局定版 / 全剧烧字幕 / 剧集列表 all did
nothing for 荒野造家 and 热血高校. Layout resolution now lives in
`drama_layout.shot_tree_roots`, and these tests pin both layouts.

Pure file ops — no ffmpeg; dummy bytes stand in for the mp4s."""
from __future__ import annotations

from pathlib import Path

import pytest

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.subtitle__error import InvalidBatchScopeError
from libs.infrastructure.readers.drama_episodes__reader import DramaEpisodesReader
from libs.infrastructure.writers.drama_takes__writer import DramaTakesSelector
from libs.infrastructure.writers.episode_takes__writer import EpisodeTakesSelector


def _takes(root: Path) -> DramaTakesSelector:
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    return DramaTakesSelector(exposed, resolver, EpisodeTakesSelector(exposed, resolver))


def _reader(root: Path) -> DramaEpisodesReader:
    return DramaEpisodesReader(ExposedTree(root), SafeResolver(root))


def _shot(root: Path, drama: str, ep: str, shot: str) -> Path:
    d = root / "ai_videos" / drama / "5_6_分镜与prompt" / "episodes" / ep / "shots" / shot
    d.mkdir(parents=True, exist_ok=True)
    return d


def _render(shot_dir: Path, name: str, data: bytes = b"v") -> None:
    renders = shot_dir / "renders"
    renders.mkdir(parents=True, exist_ok=True)
    (renders / name).write_bytes(data)


def test_select_all_locks_every_episode(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "ai_videos" / "td").mkdir(parents=True, exist_ok=True)
    (root / "ai_videos" / "td" / "README.md").write_text("# td", encoding="utf-8")
    _render(_shot(root, "td", "ep01", "shot01"), "take_a.mp4")
    _render(_shot(root, "td", "ep01", "shot02"), "take_b.mp4")
    _render(_shot(root, "td", "ep02", "shot01"), "take_c.mp4")
    _shot(root, "td", "ep02", "shot02")  # no render → skipped, not fatal

    r = _takes(root).select_all("ai_videos/td/README.md")

    by_ep = {o.episode: o for o in r.outcomes}
    assert by_ep["ep01"].ok and by_ep["ep01"].selected == 2 and by_ep["ep01"].skipped == 0
    assert by_ep["ep02"].ok and by_ep["ep02"].selected == 1 and by_ep["ep02"].skipped == 1
    # the locked canonical shot{NN}.mp4 now exists for rendered shots
    base = root / "ai_videos" / "td" / "5_6_分镜与prompt" / "episodes"
    assert (base / "ep01" / "shots" / "shot01" / "shot01.mp4").is_file()
    assert (base / "ep02" / "shots" / "shot01" / "shot01.mp4").is_file()


def test_select_all_reports_episode_with_no_renders_as_failed(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "ai_videos" / "td").mkdir(parents=True, exist_ok=True)
    _render(_shot(root, "td", "ep01", "shot01"), "take_a.mp4")
    _shot(root, "td", "ep02", "shot01")  # ep02 has a shot but NO render anywhere

    r = _takes(root).select_all("ai_videos/td")

    by_ep = {o.episode: o for o in r.outcomes}
    assert by_ep["ep01"].ok
    assert not by_ep["ep02"].ok and by_ep["ep02"].reason == "NoShotVideosError"


def test_select_all_rejects_bad_drama_path(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "ai_videos").mkdir(parents=True, exist_ok=True)
    with pytest.raises(InvalidBatchScopeError):
        _takes(root).select_all("ai_videos/_actors")  # system folder, not a drama


def test_list_episodes_reports_shots_locked_and_master(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "ai_videos" / "td").mkdir(parents=True, exist_ok=True)
    s1 = _shot(root, "td", "ep01", "shot01")
    s2 = _shot(root, "td", "ep01", "shot02")
    (s1 / "shot01.mp4").write_bytes(b"locked")     # 定版-locked
    # s2 not locked; ep01 has a stitched master
    ep01 = root / "ai_videos" / "td" / "5_6_分镜与prompt" / "episodes" / "ep01"
    (ep01 / "ep01.mp4").write_bytes(b"master")
    _shot(root, "td", "ep02", "shot01")            # ep02: 1 shot, none locked, no master

    r = _reader(root).list("ai_videos/td/README.md")

    by_ep = {e.episode: e for e in r.episodes}
    assert by_ep["ep01"].shots == 2 and by_ep["ep01"].locked == 1 and by_ep["ep01"].has_master
    assert by_ep["ep02"].shots == 1 and by_ep["ep02"].locked == 0 and not by_ep["ep02"].has_master
    # the concat target path is the ep folder, usable by /api/concat-episode
    assert by_ep["ep01"].episode_rel.endswith("episodes/ep01")


def test_list_episodes_empty_drama(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "ai_videos" / "td").mkdir(parents=True, exist_ok=True)

    r = _reader(root).list("ai_videos/td")

    assert r.episodes == ()


def _single_piece_shot(root: Path, drama: str, shot: str) -> Path:
    """A single-piece drama's shot dir: no `episodes/` layer at all."""
    d = root / "ai_videos" / drama / "5_6_分镜与prompt" / "shots" / shot
    d.mkdir(parents=True, exist_ok=True)
    return d


def _single_piece_drama(root: Path, drama: str) -> None:
    (root / "ai_videos" / drama).mkdir(parents=True, exist_ok=True)
    (root / "ai_videos" / drama / "README.md").write_text("# d", encoding="utf-8")


def test_select_all_locks_a_single_piece_drama(tmp_path: Path) -> None:
    """Regression: a drama with no `episodes/` layer used to yield zero outcomes,
    so 全局定版 silently did nothing."""
    root = tmp_path / "repo"
    _single_piece_drama(root, "sp")
    _render(_single_piece_shot(root, "sp", "shot01"), "take_a.mp4")
    _render(_single_piece_shot(root, "sp", "shot02"), "take_b.mp4")
    _single_piece_shot(root, "sp", "shot03")  # no render → skipped, not fatal

    r = _takes(root).select_all("ai_videos/sp/README.md")

    assert len(r.outcomes) == 1
    only = r.outcomes[0]
    assert only.ok and only.selected == 2 and only.skipped == 1
    assert only.episode == "sp"  # slug falls back to the drama name
    for shot in ("shot01", "shot02"):
        assert (root / "ai_videos" / "sp" / "5_6_分镜与prompt" / "shots" / shot
                / f"{shot}.mp4").is_file()


def test_reader_lists_a_single_piece_drama_as_one_row(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _single_piece_drama(root, "sp")
    _render(_single_piece_shot(root, "sp", "shot01"), "take_a.mp4")
    _single_piece_shot(root, "sp", "shot02")
    (root / "ai_videos" / "sp" / "5_6_分镜与prompt" / "shots" / "shot01"
     / "shot01.mp4").write_bytes(b"v")

    r = _reader(root).list("ai_videos/sp/README.md")

    assert len(r.episodes) == 1
    row = r.episodes[0]
    assert row.episode == "sp" and row.shots == 2 and row.locked == 1
    assert row.episode_rel == "ai_videos/sp/5_6_分镜与prompt"
    assert row.has_master is False


def test_reader_reports_single_piece_master_named_after_the_drama(tmp_path: Path) -> None:
    """The stitched master for a single-piece drama is `{drama}.mp4`, not
    `ep{NN}.mp4` — the row's 已出片 badge keys off that name."""
    root = tmp_path / "repo"
    _single_piece_drama(root, "sp")
    _render(_single_piece_shot(root, "sp", "shot01"), "take_a.mp4")
    (root / "ai_videos" / "sp" / "5_6_分镜与prompt" / "sp.mp4").write_bytes(b"v")

    assert _reader(root).list("ai_videos/sp/README.md").episodes[0].has_master is True


def test_episodes_layer_still_wins_when_both_shapes_exist(tmp_path: Path) -> None:
    """A drama that has `episodes/ep{NN}/` is a multi-episode drama even if a
    stray `shots/` sits beside it — the episodes layer must not be shadowed."""
    root = tmp_path / "repo"
    _single_piece_drama(root, "both")
    _render(_shot(root, "both", "ep01", "shot01"), "take_a.mp4")
    (root / "ai_videos" / "both" / "5_6_分镜与prompt" / "shots" / "shot01").mkdir(
        parents=True, exist_ok=True
    )

    rows = _reader(root).list("ai_videos/both/README.md").episodes

    assert [e.episode for e in rows] == ["ep01"]
