"""push resumability: an interrupted upload must not re-send what already landed.

The first full push of this repo died partway (a Chinese path hit a cp1252
console), leaving ~1000 objects in the bucket and an empty manifest. Re-sending
7 GB to recover from that is the failure this guards.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import tools.assets_sync as assets_sync


class FakeStore:
    def __init__(self, present: dict[str, int]) -> None:
        self.present = present
        self.uploaded: list[str] = []
        self.copied: list[tuple[str, str]] = []

    def list_objects(self, prefix: str = "") -> list[tuple[str, int]]:
        return sorted(self.present.items())

    def exists(self, key: str) -> bool:
        return key in self.present

    def upload(self, key: str, path: Path) -> None:
        self.uploaded.append(key)
        self.present[key] = path.stat().st_size

    def copy(self, src: str, dst: str) -> None:
        self.copied.append((src, dst))
        self.present[dst] = self.present[src]


def _repo(tmp_path: Path, files: dict[str, bytes]) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    for rel, blob in files.items():
        target = tmp_path / "ai_videos" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    return tmp_path


def _wire(monkeypatch: pytest.MonkeyPatch, root: Path, store: FakeStore) -> None:
    monkeypatch.setattr(assets_sync, "REPO_ROOT", root)
    monkeypatch.setattr(assets_sync, "MEDIA_ROOT", root / "ai_videos")
    monkeypatch.setattr(assets_sync, "MANIFEST_PATH", root / "ai_videos" / "assets.json")
    monkeypatch.setattr(assets_sync.R2Store, "from_env", classmethod(lambda cls, _root: store))


def test_objects_already_in_the_bucket_are_not_re_sent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _repo(tmp_path, {"ep01/landed.mp4": b"x" * 100, "ep01/fresh.png": b"y" * 50})
    store = FakeStore({"ep01/landed.mp4": 100})
    _wire(monkeypatch, root, store)

    assert assets_sync._push(stage_manifest=False) == 0

    assert store.uploaded == ["ep01/fresh.png"]
    manifest = assets_sync.Manifest.load(root / "ai_videos" / "assets.json")
    assert set(manifest.assets) == {"ep01/landed.mp4", "ep01/fresh.png"}


def test_a_bucket_object_of_a_different_size_is_re_sent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A truncated upload leaves a short object — size mismatch must re-send it."""
    root = _repo(tmp_path, {"ep01/truncated.mp4": b"x" * 100})
    store = FakeStore({"ep01/truncated.mp4": 12})
    _wire(monkeypatch, root, store)

    assert assets_sync._push(stage_manifest=False) == 0
    assert store.uploaded == ["ep01/truncated.mp4"]


def test_manifest_is_checkpointed_so_a_crash_keeps_its_progress(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {f"ep01/{i:03d}.png": b"z" * (i + 1) for i in range(assets_sync._SAVE_EVERY + 2)}
    root = _repo(tmp_path, files)
    manifest_path = root / "ai_videos" / "assets.json"

    class DyingStore(FakeStore):
        def upload(self, key: str, path: Path) -> None:
            if len(self.uploaded) == assets_sync._SAVE_EVERY + 1:
                raise RuntimeError("connection reset")
            super().upload(key, path)

    store = DyingStore({})
    _wire(monkeypatch, root, store)
    with pytest.raises(RuntimeError):
        assets_sync._push(stage_manifest=False)

    survived = assets_sync.Manifest.load(manifest_path).assets
    assert len(survived) == assets_sync._SAVE_EVERY
    assert set(survived) <= set(files)


def test_entries_absent_from_this_machine_survive_a_push(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A partial checkout must not erase other machines' media from the index."""
    root = _repo(tmp_path, {"ep01/here.mp4": b"x" * 100})
    manifest_path = root / "ai_videos" / "assets.json"
    elsewhere = assets_sync.AssetEntry(sha256="c" * 64, size=999)
    assets_sync.Manifest(assets={"ep02/not_pulled.mp4": elsewhere}, updated="").save(manifest_path)
    store = FakeStore({})
    _wire(monkeypatch, root, store)

    assert assets_sync._push(stage_manifest=False) == 0

    assets = assets_sync.Manifest.load(manifest_path).assets
    assert assets == {"ep01/here.mp4": assets["ep01/here.mp4"], "ep02/not_pulled.mp4": elsewhere}


def test_prune_missing_drops_them_when_asked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _repo(tmp_path, {"ep01/here.mp4": b"x" * 100})
    manifest_path = root / "ai_videos" / "assets.json"
    assets_sync.Manifest(
        assets={"ep02/deleted.mp4": assets_sync.AssetEntry(sha256="c" * 64, size=9)}, updated=""
    ).save(manifest_path)
    _wire(monkeypatch, root, FakeStore({}))

    assert assets_sync._push(stage_manifest=False, prune_missing=True) == 0
    assert set(assets_sync.Manifest.load(manifest_path).assets) == {"ep01/here.mp4"}
