"""Previz render endpoint: path resolution, sandboxing, and the busy guard.

Nothing here launches Blender — a real render is 15–30 minutes. The pieces
under test are the ones a caller can actually break: which `.blend` a given
path resolves to, what gets rejected, and that a second render cannot start
on top of a running one.
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.previz__error import (
    InvalidPrevizPathError,
    PrevizBlendNotFoundError,
    PrevizRenderBusyError,
)
from libs.domain.value_objects.previz__valueobject import (
    STATE_DONE,
    STATE_RENDERING,
    PrevizJobSnapshot,
)
from libs.infrastructure.writers.previz__writer import PrevizRenderer
from tests.conftest import make_app, repo_root


def _renderer(root: Path) -> PrevizRenderer:
    resolver = SafeResolver(root=root)
    return PrevizRenderer(exposed=ExposedTree(repo_root=root), resolver=resolver)


def _make_previz(tmp_path: Path) -> tuple[Path, Path]:
    """A minimal exposed tree with one previz folder holding one `.blend`."""
    previz = tmp_path / "ai_videos" / "demo" / "shots" / "shot01" / "previz"
    previz.mkdir(parents=True)
    blend = previz / "shot01_previz.blend"
    blend.write_bytes(b"BLENDER-fake")
    (previz / "README.md").write_text("previz notes", encoding="utf-8")
    return tmp_path, blend


def test_locate_blend_accepts_folder_blend_and_sibling(tmp_path: Path) -> None:
    root, blend = _make_previz(tmp_path)
    renderer = _renderer(root)
    rel_folder = "ai_videos/demo/shots/shot01/previz"
    for rel in (rel_folder, f"{rel_folder}/shot01_previz.blend", f"{rel_folder}/README.md"):
        assert renderer.locate_blend(rel) == blend


def test_locate_blend_rejects_non_previz_folder(tmp_path: Path) -> None:
    root, _ = _make_previz(tmp_path)
    with pytest.raises(InvalidPrevizPathError):
        _renderer(root).locate_blend("ai_videos/demo/shots/shot01")


def test_locate_blend_rejects_escape(tmp_path: Path) -> None:
    root, _ = _make_previz(tmp_path)
    with pytest.raises(InvalidPrevizPathError):
        _renderer(root).locate_blend("../../etc/passwd")


def test_locate_blend_rejects_empty_path(tmp_path: Path) -> None:
    root, _ = _make_previz(tmp_path)
    with pytest.raises(InvalidPrevizPathError):
        _renderer(root).locate_blend("")


def test_locate_blend_rejects_ambiguous_folder(tmp_path: Path) -> None:
    """Two `.blend`s means we cannot tell which one the button should render."""
    root, blend = _make_previz(tmp_path)
    (blend.parent / "other.blend").write_bytes(b"BLENDER-fake")
    with pytest.raises(PrevizBlendNotFoundError):
        _renderer(root).locate_blend("ai_videos/demo/shots/shot01/previz")


def test_status_is_idle_and_reports_existing_mp4(tmp_path: Path) -> None:
    root, blend = _make_previz(tmp_path)
    renderer = _renderer(root)
    rel = "ai_videos/demo/shots/shot01/previz"

    idle = renderer.status(rel)
    assert idle.state == "idle"
    assert idle.mp4_rel is None

    blend.with_suffix(".mp4").write_bytes(b"\x00")
    assert renderer.status(rel).mp4_rel.endswith("shot01_previz.mp4")


def test_start_rejects_a_second_concurrent_render(tmp_path: Path) -> None:
    """Blender saturates every core; two renders make both crawl."""
    root, blend = _make_previz(tmp_path)
    renderer = _renderer(root)
    renderer._job = PrevizJobSnapshot(  # noqa: SLF001 — no public setter by design
        blend_rel="ai_videos/demo/shots/shot01/previz/shot01_previz.blend",
        state=STATE_RENDERING,
        rendered_frames=10,
        total_frames=480,
        started_at=time.time(),
        finished_at=None,
        message="",
        mp4_rel=None,
    )
    with pytest.raises(PrevizRenderBusyError):
        renderer.start("ai_videos/demo/shots/shot01/previz")


def test_percent_never_claims_done_while_muxing() -> None:
    """A bar frozen at 100% while ffmpeg still runs reads as a hang."""
    base = dict(
        blend_rel="x.blend", rendered_frames=480, total_frames=480,
        started_at=0.0, finished_at=None, message="", mp4_rel=None,
    )
    assert PrevizJobSnapshot(state=STATE_RENDERING, **base).percent == 96
    assert PrevizJobSnapshot(state="muxing", **base).percent == 97
    assert PrevizJobSnapshot(state=STATE_DONE, **base).percent == 100


def test_status_endpoint_rejects_paths_outside_previz() -> None:
    rr = RepoRoot(path=repo_root())
    client = TestClient(make_app(rr, BoundOrigin(host="127.0.0.1", port=8766)))
    r = client.get("/api/previz/status", params={"path": "ai_videos"})
    assert r.status_code == 400
    assert r.json()["detail"]["kind"] == "invalid_previz_path"
