"""Two views of ONE prop must not collapse onto the same filename.

Regression guard for the bug the user hit on 2026-09-13 while importing hy3's
prop anchors: `p3-1_抹泥板锚点` and `p3-2_黏土壁炉锚点` both landed on
`props/p3_抹泥板与黏土壁炉/p3_抹泥板与黏土壁炉.png` and the second silently
destroyed the first.

Cause: the out-of-image tool wraps the prompt head in its own prefix —

    ElevenLabs_image_gpt-image-2_p3-2_黏土壁炉锚点 一座手_2026-09-13T07_26_16.png

— so `_view_key`'s "does the stem START with a folder token" test failed and
both files fell through to the folder's canonical name. Scene subjects already
searched their `bg{N}-{M}` key anywhere in the stem; props and characters did
not. `libs.common.asset_key` is now that logic, shared by BOTH ends:
`DownloadsImporter` (naming on import) and `MediaRenamer` (the normalise pass,
which used to collapse such files onto order-dependent `{folder}{N}`).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.common.asset_key import view_key_in
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer

PROP_DIR = "2_世界观人设/props/p3_抹泥板与黏土壁炉"
DRAMA_REL = "ai_videos/my_series/ep1"

# Exactly what the generator produced, prefix and trailing timestamp included.
DL_P3_1 = "ElevenLabs_image_gpt-image-2_p3-1_抹泥板锚点 一把用_2026-09-13T07_26_16.png"
DL_P3_2 = "ElevenLabs_image_gpt-image-2_p3-2_黏土壁炉锚点 一座手_2026-09-13T08_58_45.png"


@pytest.fixture()
def repo(tmp_path: Path) -> tuple[Path, Path]:
    """A series-nested drama with one multi-view prop, plus a Downloads dir."""
    root = tmp_path / "repo"
    series = root / "ai_videos" / "my_series"
    (series / "ep1" / PROP_DIR).mkdir(parents=True)
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


def test_two_prop_views_import_to_distinct_files(repo: tuple[Path, Path]) -> None:
    root, downloads = repo
    for name, payload in ((DL_P3_1, b"one"), (DL_P3_2, b"two")):
        (downloads / name).write_bytes(payload)

    _importer(root, downloads).import_drama(DRAMA_REL)

    prop = root / "ai_videos" / "my_series" / "ep1" / PROP_DIR
    landed = sorted(p.name for p in prop.iterdir() if p.is_file())
    assert landed == ["p3-1.png", "p3-2.png"], landed
    # …and each kept its OWN bytes (the collision used to lose one of them).
    assert (prop / "p3-1.png").read_bytes() == b"one"
    assert (prop / "p3-2.png").read_bytes() == b"two"


def test_same_key_twice_newest_take_wins(repo: tuple[Path, Path]) -> None:
    """Two takes of the SAME view is a legitimate re-roll — newest must win."""
    root, downloads = repo
    old = downloads / "ElevenLabs_image_gpt-image-2_p3-2_黏土壁炉锚点 A.png"
    new = downloads / "ElevenLabs_image_gpt-image-2_p3-2_黏土壁炉锚点 B.png"
    old.write_bytes(b"old")
    new.write_bytes(b"new")
    # Recent mtimes — the importer only looks at a time window around now.
    import os
    import time
    now = time.time()
    os.utime(old, (now - 120, now - 120))
    os.utime(new, (now - 30, now - 30))

    _importer(root, downloads).import_drama(DRAMA_REL)

    prop = root / "ai_videos" / "my_series" / "ep1" / PROP_DIR
    assert sorted(p.name for p in prop.iterdir()) == ["p3-2.png"]
    assert (prop / "p3-2.png").read_bytes() == b"new"


def test_renamer_keeps_routing_keys_apart(repo: tuple[Path, Path]) -> None:
    """The normalise-names pass must not collapse views onto `{folder}{N}`."""
    root, _ = repo
    prop = root / "ai_videos" / "my_series" / "ep1" / PROP_DIR
    (prop / DL_P3_1).write_bytes(b"one")
    (prop / DL_P3_2).write_bytes(b"two")

    exposed, resolver = ExposedTree(repo_root=root), SafeResolver(root=root)
    MediaRenamer(exposed=exposed, resolver=resolver).rename_drama(DRAMA_REL)

    landed = sorted(p.name for p in prop.iterdir() if p.is_file())
    assert landed == ["p3-1.png", "p3-2.png"], landed
    assert (prop / "p3-1.png").read_bytes() == b"one"
    assert (prop / "p3-2.png").read_bytes() == b"two"


def test_already_canonical_names_are_left_alone(repo: tuple[Path, Path]) -> None:
    root, _ = repo
    prop = root / "ai_videos" / "my_series" / "ep1" / PROP_DIR
    (prop / "p3-1.png").write_bytes(b"one")
    (prop / "p3-2.png").write_bytes(b"two")

    exposed, resolver = ExposedTree(repo_root=root), SafeResolver(root=root)
    MediaRenamer(exposed=exposed, resolver=resolver).rename_drama(DRAMA_REL)

    assert sorted(p.name for p in prop.iterdir() if p.is_file()) == [
        "p3-1.png",
        "p3-2.png",
    ]


def test_generator_prefix_cannot_hide_the_key() -> None:
    """The unit-level guarantee the two ends rely on."""
    assert view_key_in(Path(DL_P3_2).stem, "p3_抹泥板与黏土壁炉") == "p3-2"
    # …and a folder that owns no key never claims one.
    assert view_key_in(Path(DL_P3_2).stem, "c1_砌炉的老人") is None
