"""A series member's Downloads import also routes into the series' `_series/` assets.

Regression guard for sk1 (2026-09-14): the shared character card
`ai_videos/shikong_lvxing/_series/characters/c1_林问/` (prompt head
`c1-1_林问立绘`) could never receive its download. `_series` is not a drama, so
`DownloadsImporter._collect_candidates` only saw the episode's own
`2_世界观人设/{characters,scenes,props}` — and an episode-local `c1_林问/`
duplicate silently took the file instead.

Shared assets now join the candidate pool. An episode folder that shadows a
shared one (same routing prefix, or same folder name) blocks that download with
a `series_key_conflict:` error rather than guessing which of the two it is for.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from libs.common import series_shared
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter, _token_hit
from libs.infrastructure.writers.media__writer import MediaRenamer

SERIES_REL = "ai_videos/my_series"
DRAMA_REL = f"{SERIES_REL}/ep1"
SHARED_REL = f"{SERIES_REL}/_series"
WORLD = "2_世界观人设"
# What the out-of-image tool wraps around the prompt head.
GEN = "ElevenLabs_image_gpt-image-2_"
STAMP = "_2026-09-14T08_00_00.png"


@pytest.fixture()
def repo(tmp_path: Path) -> tuple[Path, Path]:
    """A series with one episode and an empty `_series/`, plus a Downloads dir."""
    root = tmp_path / "repo"
    series = root / SERIES_REL
    (series / "ep1" / WORLD).mkdir(parents=True)
    (series / "_series").mkdir()
    (series / "series.json").write_text(
        json.dumps({"name_zh": "系列", "slug": "my_series"}), encoding="utf-8"
    )
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, downloads


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed, resolver = ExposedTree(repo_root=root), SafeResolver(root=root)
    return DownloadsImporter(
        exposed=exposed,
        resolver=resolver,
        renamer=MediaRenamer(exposed=exposed, resolver=resolver),
        downloads_dir=downloads,
    )


def _dir(root: Path, rel: str) -> Path:
    path = root / rel
    path.mkdir(parents=True, exist_ok=True)
    return path


def _drop(downloads: Path, name: str, payload: bytes, age_s: int = 30) -> Path:
    """A download with a recent mtime — the importer only scans a window around now."""
    src = downloads / name
    src.write_bytes(payload)
    stamp = time.time() - age_s
    os.utime(src, (stamp, stamp))
    return src


def _files(folder: Path) -> list[str]:
    return sorted(p.name for p in folder.iterdir() if p.is_file())


@pytest.mark.parametrize("layout", ["", f"{WORLD}/"], ids=["flat_shared", "staged_shared"])
def test_series_character_download_lands_in_series_folder(
    repo: tuple[Path, Path], layout: str
) -> None:
    root, downloads = repo
    card_rel = f"{SHARED_REL}/{layout}characters/c2_x"
    card = _dir(root, card_rel)
    src = _drop(downloads, f"{GEN}c2-1_x立绘 一个{STAMP}", b"series")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert result.errors == []
    assert _files(card) == ["c2-1.png"]
    assert (card / "c2-1.png").read_bytes() == b"series"
    assert not src.exists()
    assert [(m["to"], m["kind"]) for m in result.moved] == [
        (f"{card_rel}/c2-1.png", "character")
    ]


def test_prefix_sharing_keys_route_to_their_own_side(repo: tuple[Path, Path]) -> None:
    """Episode `c21_y` and shared `c2_x` are different keys, not a conflict."""
    root, downloads = repo
    episode_card = _dir(root, f"{DRAMA_REL}/{WORLD}/characters/c21_y")
    series_card = _dir(root, f"{SHARED_REL}/characters/c2_x")
    _drop(downloads, f"{GEN}c21-1_y立绘 一个{STAMP}", b"episode", age_s=60)
    _drop(downloads, f"{GEN}c2-1_x立绘 一个{STAMP}".replace("08_00", "08_01"), b"series")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert result.errors == []
    assert _files(episode_card) == ["c21-1.png"]
    assert (episode_card / "c21-1.png").read_bytes() == b"episode"
    assert _files(series_card) == ["c2-1.png"]
    assert (series_card / "c2-1.png").read_bytes() == b"series"


def test_short_key_does_not_match_inside_a_longer_one() -> None:
    assert not _token_hit("c2", f"{GEN}c21-1_y立绘{STAMP}".lower())
    assert _token_hit("c2", f"{GEN}c2-1_x立绘{STAMP}".lower())


@pytest.mark.parametrize(
    ("episode_rel", "shared_rel", "download"),
    [
        ("characters/c1_林问", "characters/c1_林问", f"{GEN}c1-1_林问立绘 一个{STAMP}"),
        ("characters/c1_林问", "characters/c1_少年林问", f"{GEN}c1-1_林问立绘 一个{STAMP}"),
        ("scenes/集市长街", "scenes/集市长街", "集市长街 全景 电影级.png"),
    ],
    ids=["same_folder", "same_key", "same_name_no_key"],
)
def test_episode_duplicate_of_series_asset_blocks_the_import(
    repo: tuple[Path, Path], episode_rel: str, shared_rel: str, download: str
) -> None:
    root, downloads = repo
    episode_card = _dir(root, f"{DRAMA_REL}/{WORLD}/{episode_rel}")
    series_card = _dir(root, f"{SHARED_REL}/{shared_rel}")
    free_card = _dir(root, f"{DRAMA_REL}/{WORLD}/characters/c3_z")
    blocked = _drop(downloads, download, b"blocked", age_s=60)
    _drop(downloads, f"{GEN}c3-1_z立绘 一个{STAMP}", b"free")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert blocked.read_bytes() == b"blocked"
    assert _files(episode_card) == []
    assert _files(series_card) == []
    [error] = result.errors
    assert error["message"].startswith("series_key_conflict:")
    assert f"{DRAMA_REL}/{WORLD}/{episode_rel}" in error["message"]
    assert f"{SHARED_REL}/{shared_rel}" in error["message"]
    assert result.unmatched == []
    assert _files(free_card) == ["c3-1.png"]


def test_series_prop_download_lands_in_series_folder(repo: tuple[Path, Path]) -> None:
    root, downloads = repo
    prop = _dir(root, f"{SHARED_REL}/props/p5_铜镜")
    _drop(downloads, f"{GEN}p5-1_铜镜锚点 一面{STAMP}", b"mirror")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert result.errors == []
    assert _files(prop) == ["p5-1.png"]
    assert [m["kind"] for m in result.moved] == ["prop"]


def test_series_scene_subject_view_lands_in_series_folder(repo: tuple[Path, Path]) -> None:
    """A subject view carries only its `bg{N}-{M}` key, so it routes through the
    any-scene fallback — which must see the shared scenes too."""
    root, downloads = repo
    subject = _dir(root, f"{SHARED_REL}/scenes/汴河/bg7_虹桥")
    (subject / "bg7_虹桥.md").write_text("# bg7_虹桥\n", encoding="utf-8")
    _drop(downloads, f"{GEN}bg7-1_虹桥正向 参考{STAMP}", b"bridge")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert result.errors == []
    assert _files(subject) == ["bg7-1.png", "bg7_虹桥.md"]
    assert [m["kind"] for m in result.moved] == ["scene_subject"]


def test_subject_number_owned_on_both_sides_is_reported(repo: tuple[Path, Path]) -> None:
    root, downloads = repo
    episode_subject = _dir(root, f"{DRAMA_REL}/{WORLD}/scenes/汴河/bg7_虹桥")
    (episode_subject / "bg7_虹桥.md").write_text("# bg7_虹桥\n", encoding="utf-8")
    shared_subject = _dir(root, f"{SHARED_REL}/scenes/城门/bg7_城楼")
    (shared_subject / "bg7_城楼.md").write_text("# bg7_城楼\n", encoding="utf-8")
    blocked = _drop(downloads, f"{GEN}bg7-1_虹桥正向 参考{STAMP}", b"bridge")

    result = _importer(root, downloads).import_drama(DRAMA_REL)

    assert blocked.exists()
    assert result.unmatched == []
    [error] = result.errors
    assert error["message"].startswith("series_key_conflict:")
    assert f"{DRAMA_REL}/{WORLD}/scenes/汴河/bg7_虹桥" in error["message"]
    assert f"{SHARED_REL}/scenes/城门/bg7_城楼" in error["message"]


def test_flat_drama_never_sees_a_series_shared_dir(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    flat = _dir(root, "ai_videos/flat_drama")
    card = _dir(root, f"ai_videos/flat_drama/{WORLD}/characters/c2_x")
    series = _dir(root, SERIES_REL)
    (series / "series.json").write_text(json.dumps({"slug": "my_series"}), encoding="utf-8")
    foreign = _dir(root, f"{SHARED_REL}/characters/c9_q")
    downloads = _dir(tmp_path, "Downloads")
    _drop(downloads, f"{GEN}c2-1_x立绘 一个{STAMP}", b"flat", age_s=60)
    left = _drop(downloads, f"{GEN}c9-1_q立绘 一个{STAMP}".replace("08_00", "08_01"), b"q")

    result = _importer(root, downloads).import_drama("ai_videos/flat_drama")

    assert series_shared.asset_roots(flat) == [flat]
    assert result.errors == []
    assert _files(card) == ["c2-1.png"]
    assert _files(foreign) == []
    assert left.read_bytes() == b"q"
    assert [u["kind"] for u in result.unmatched] == ["unmatched"]
