"""`is_under_character_folder` accepts both drama depths and both layouts.

Regression guard for the bug that took out **every** character-video button
(truncate / extract-views / extract-all) after the 2026-09-09 series-nesting
refactor: the predicate was a `@staticmethod` whose body reached for
`self._resolver.root`, so every call raised
`NameError: name 'self' is not defined`, surfacing in the UI as
"extraction failed". Found 2026-09-13 while extracting hy3's turntable views.

The predicate needs the repo root because the owning folder is **two or three**
segments (`ai_videos/{drama}` vs `ai_videos/{series}/{drama}`) and only the
filesystem knows which — `libs.common.drama_ref` is the single place allowed
to answer that (CLAUDE.md forbids re-deriving it from path depth).

Second regression, found 2026-09-20 extracting 艾拉's views: the predicate asked
`drama_ref.drama_depth`, which answers None for `ai_videos/{series}/_series/`
because `_series` is not a drama. That is right for anything keyed to an episode
and wrong here — a character several episodes share has its ONLY home under
`_series/characters/` (CLAUDE.md § AI video rules, 2026-09-15), so every button
on a shared character's turntable video returned `not_a_character_video`. It now
asks `drama_ref.asset_root_depth`, which accepts both owners.

Note what is deliberately NOT policed: the one intermediate segment between the
owning folder and `characters/` may be named anything, because that is the stage
folder (`2_世界观人设`). So `ai_videos/flat_drama/_series/characters/c1_x/` is
accepted in a drama that is not a series member — `_series` is just a folder
name there, and singling it out would be arbitrary while `_junk` still passed.

Third, 2026-09-27: monster and crowd-NPC cards are `mN_` folders (m1_Kobold) and
get a turntable like the cast, but the folder test only knew `cN_`, so their
videos came back `not_a_character_video` and the UI never offered extraction.
The folder test now lives once in `libs.common.character_dir`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.infrastructure.writers.character_video__writer import (
    is_under_character_folder,
)


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    """A repo root holding one flat drama and one series with two members."""
    ai = tmp_path / "ai_videos"
    (ai / "flat_drama" / "characters" / "c1_legacy").mkdir(parents=True)
    (ai / "flat_drama" / "2_世界观人设" / "characters" / "c4_staged").mkdir(parents=True)
    (ai / "flat_drama" / "2_世界观人设" / "characters" / "m1_Kobold").mkdir(parents=True)
    series = ai / "my_series"
    (series / "ep1" / "2_世界观人设" / "characters" / "c1_老人").mkdir(parents=True)
    (series / "_series" / "characters" / "c4_艾拉").mkdir(parents=True)
    (series / "series.json").write_text(
        json.dumps({"name_zh": "系列", "slug": "my_series"}), encoding="utf-8"
    )
    (ai / "_actors" / "characters" / "c1_x").mkdir(parents=True)
    return tmp_path


ACCEPTED = [
    # series member + staged layout — the shape that was failing (hy3)
    "ai_videos/my_series/ep1/2_世界观人设/characters/c1_老人/c1_老人.mp4",
    # flat drama + staged layout
    "ai_videos/flat_drama/2_世界观人设/characters/c4_staged/c4-2_turntable.mp4",
    # flat drama + legacy layout (characters/ at the drama root)
    "ai_videos/flat_drama/characters/c1_legacy/video.mp4",
    # series-SHARED character — the only home for one several episodes reuse
    "ai_videos/my_series/_series/characters/c4_艾拉/c4-2.mp4",
    # monster / crowd-NPC card (`mN_`) — they get a turntable too (rule 22.2)
    "ai_videos/flat_drama/2_世界观人设/characters/m1_Kobold/m1_Kobold.mp4",
]

REJECTED = [
    # system library, never a drama
    "ai_videos/_actors/characters/c1_x/a.mp4",
    # `_series` owns characters/ directly — not a `characters/` two levels down
    "ai_videos/my_series/_series/a/b/characters/c1_x/a.mp4",
    # the series folder itself is not a drama
    "ai_videos/my_series/characters/c1_x/a.mp4",
    # `characters/` present but no cN_ / mN_ child
    "ai_videos/flat_drama/2_世界观人设/characters/props/a.mp4",
    "ai_videos/flat_drama/2_世界观人设/characters/p1_prop/a.mp4",
    # a folder that merely happens to be named `characters`, buried deeper
    "ai_videos/flat_drama/a/b/c/characters/c1_x/a.mp4",
    # outside ai_videos/
    "specs/ai_video/hy3/characters/c1_x/a.mp4",
    "",
]


@pytest.mark.parametrize("rel", ACCEPTED)
def test_accepts_character_videos(root: Path, rel: str) -> None:
    assert is_under_character_folder(root, rel) is True


@pytest.mark.parametrize("rel", REJECTED)
def test_rejects_everything_else(root: Path, rel: str) -> None:
    assert is_under_character_folder(root, rel) is False


def test_predicate_needs_no_instance(root: Path) -> None:
    """It is a plain function — calling it must not touch `self`/`cls`.

    This is the exact failure mode: the old `@staticmethod` body referenced
    `self`, so the call blew up before any path logic ran.
    """
    assert is_under_character_folder(
        root, "ai_videos/my_series/ep1/2_世界观人设/characters/c1_老人/x.mp4"
    ) is True
