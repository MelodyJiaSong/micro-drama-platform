"""sub_type detection for a STAGED single-piece project (xianjian_yi_mv, 2026-08-02).

`_looks_like_short` / `_count_shots` looked for `script.md` / `shotlist.md` at the
PROJECT ROOT only. The staged pipeline puts them under their stage folders
(`4_剧本/script.md`, `5_6_分镜与prompt/shotlist.md`), so every staged single-piece
project reported `sub_type=None, shot_count=None` — the UI could not tell it was
a short and showed no shot count. Same family as the downloads-import bug: a
consumer that only knew the old layout.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.sub_type_lookup import lookup

SHOTLIST = """| 镜 | 内容 |
|---|---|
| shot01 | a |
| shot02 | b |
| shot03 | c |
"""


def _touch(path: Path, text: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_staged_single_piece_is_detected_as_short(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "mv"
    _touch(drama / "4_剧本" / "script.md")
    _touch(drama / "5_6_分镜与prompt" / "shotlist.md", SHOTLIST)
    for n in ("shot01", "shot02", "shot03"):
        _touch(drama / "5_6_分镜与prompt" / "shots" / n / f"{n}.md")

    meta = lookup(tmp_path, "mv")

    assert meta.sub_type == "short"
    assert meta.shot_count == 3
    assert meta.episode_count is None


def test_flat_shots_tree_alone_is_enough(tmp_path: Path) -> None:
    """No script/shotlist yet — a flat shots tree with no episodes layer is
    itself conclusive evidence of a single-piece project."""
    drama = tmp_path / "ai_videos" / "mv"
    _touch(drama / "5_6_分镜与prompt" / "shots" / "shot01" / "shot01.md")

    meta = lookup(tmp_path, "mv")

    assert meta.sub_type == "short"


def test_staged_multi_episode_still_reads_as_novel(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "drama"
    _touch(drama / "5_6_分镜与prompt" / "episodes" / "ep01" / "shots" / "shot01" / "shot01.md")

    meta = lookup(tmp_path, "drama")

    assert meta.sub_type == "novel"
    assert meta.episode_count == 1
