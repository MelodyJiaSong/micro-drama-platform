"""assets_sync: manifest round-trip, syncability rules, and plan diffing.

No network — R2Store is not exercised here; everything that decides *what*
moves is pure and lives in scanner/plan/manifest.
"""
from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath

import pytest

from tools.assets.manifest import AssetEntry, Manifest
from tools.assets.plan import build, human_bytes, unreferenced_keys
from tools.assets.scanner import is_syncable, scan

A = AssetEntry(sha256="a" * 64, size=10)
B = AssetEntry(sha256="b" * 64, size=20)


def test_key_is_content_addressed_and_sharded() -> None:
    assert A.key == f"objects/aa/{'a' * 64}"


def test_manifest_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "assets.json"
    Manifest(assets={"b.mp4": B, "a.mp4": A}, updated="").save(path)
    # keys are sorted on disk so the tracked file diffs cleanly
    assert path.read_text(encoding="utf-8").index('"a.mp4"') < path.read_text(encoding="utf-8").index('"b.mp4"')
    loaded = Manifest.load(path)
    assert loaded.assets == {"a.mp4": A, "b.mp4": B}
    assert loaded.total_bytes == 30
    assert loaded.updated


def test_manifest_rejects_unknown_version(tmp_path: Path) -> None:
    path = tmp_path / "assets.json"
    path.write_text('{"version": 99, "assets": {}}', encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported manifest version"):
        Manifest.load(path)


def test_missing_manifest_is_empty_not_an_error(tmp_path: Path) -> None:
    assert Manifest.load(tmp_path / "nope.json").assets == {}


@pytest.mark.parametrize(
    "rel,expected",
    [
        ("drama/ep01/shot01.mp4", True),
        ("drama/refs/a.PNG", True),
        ("drama/对抗熵增_分镜.pdf", True),
        ("drama/ep01/shot01.md", False),          # prompts stay in git
        ("_deleted/drama/shot01.mp4", False),      # recycle bin
        ("drama/previz/frames/0001.png", False),   # recomputable from previz_config
        ("drama/previz/scene.mp4", True),          # the render itself is not
    ],
)
def test_is_syncable(rel: str, expected: bool) -> None:
    assert is_syncable(PurePosixPath(rel)) is expected


def test_plan_classifies_each_case() -> None:
    manifest = Manifest(assets={"keep.mp4": A, "changed.mp4": A, "remote_only.mp4": B}, updated="")
    local = {"keep.mp4": A, "changed.mp4": B, "new.mp4": B}
    plan = build(local, manifest)
    assert plan.unchanged == 1
    assert set(plan.upload) == {"changed.mp4", "new.mp4"}
    assert plan.drifted == {"changed.mp4": (A.sha256, B.sha256)}
    assert set(plan.download) == {"remote_only.mp4"}


def test_rename_needs_no_transfer() -> None:
    """Same bytes at a new path: the manifest changes, the object key does not."""
    plan = build({"new/name.mp4": A}, Manifest(assets={"old/name.mp4": A}, updated=""))
    assert plan.upload["new/name.mp4"].key == A.key


def test_unreferenced_keys_are_the_prune_set() -> None:
    manifest = Manifest(assets={"a.mp4": A}, updated="")
    assert unreferenced_keys(manifest, [A.key, B.key]) == [B.key]


def test_scan_skips_git_tracked_media(tmp_path: Path) -> None:
    media = tmp_path / "ai_videos" / "drama"
    media.mkdir(parents=True)
    (media / "tracked.png").write_bytes(b"1")
    (media / "untracked.mp4").write_bytes(b"2")
    (tmp_path / "ai_videos" / "_deleted").mkdir()
    (tmp_path / "ai_videos" / "_deleted" / "gone.mp4").write_bytes(b"3")
    for cmd in (["init", "-q"], ["add", "-f", "ai_videos/drama/tracked.png"]):
        subprocess.run(["git", *cmd], cwd=tmp_path, check=True, capture_output=True)
    result = scan(tmp_path)
    assert set(result.entries) == {"drama/untracked.mp4"}
    assert result.skipped_tracked == 1


def test_human_bytes() -> None:
    assert human_bytes(512) == "512 B"
    assert human_bytes(1536) == "1.5 KB"
    assert human_bytes(3 * 1024**3) == "3.0 GB"
