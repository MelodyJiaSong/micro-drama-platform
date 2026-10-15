"""`OBSOLETE.md` marks a drama (or a series / library folder) as obsolete.

Follow-up 233: the old 0–7 stage pipeline was removed and its dramas are kept
only for reference, each marked with an `OBSOLETE.md` at the drama root or at
the series root above it. The tree carries `obsolete: true` plus
`obsolete_note` (the marker's path) so the sidebar and the drama page can show
an「已过时」badge and open the note. A drama inherits its series' marker; its
own marker, when it has one, is the note it points at.
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from libs.common.episode_workflow import WORKFLOW_ID, WORKFLOW_MARKER
from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.tree__reader import OBSOLETE_MARKER_NAME, TreeReader
from tests.conftest import make_app


def _write(path: Path, text: str = "# x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _nodes(root: Path) -> dict[str, dict]:
    """Every tree node by path."""
    out: dict[str, dict] = {}

    def walk(node: dict) -> None:
        if node.get("path"):
            out.setdefault(node["path"], node)
        for child in node.get("children", []):
            walk(child)

    walk(TreeReader(ExposedTree(root)).build())
    return out


def _series(root: Path, name: str) -> Path:
    series = root / "ai_videos" / name
    _write(series / "series.json", json.dumps({"name_zh": "系列"}))
    return series


def test_flat_drama_with_marker_is_obsolete(tmp_path: Path) -> None:
    _write(tmp_path / "ai_videos/old_drama/README.md")
    _write(tmp_path / "ai_videos/old_drama" / OBSOLETE_MARKER_NAME)
    node = _nodes(tmp_path)["ai_videos/old_drama"]
    assert node["is_drama"] is True
    assert node["obsolete"] is True
    assert node["obsolete_note"] == "ai_videos/old_drama/OBSOLETE.md"


def test_drama_without_marker_carries_no_flag(tmp_path: Path) -> None:
    _write(tmp_path / "ai_videos/new_drama/README.md")
    _write(tmp_path / "ai_videos/old_drama" / OBSOLETE_MARKER_NAME)
    node = _nodes(tmp_path)["ai_videos/new_drama"]
    assert "obsolete" not in node and "obsolete_note" not in node


def test_series_marker_is_inherited_by_members_and_shared_folder(tmp_path: Path) -> None:
    series = _series(tmp_path, "old_series")
    _write(series / OBSOLETE_MARKER_NAME)
    _write(series / "ep1/README.md")
    _write(series / "ep2/README.md")
    _write(series / "_series/characters/c1_x/c1_x.md")
    nodes = _nodes(tmp_path)
    assert nodes["ai_videos/old_series"]["type"] == "series"
    assert nodes["ai_videos/old_series"]["obsolete"] is True
    for path in ("ai_videos/old_series/ep1", "ai_videos/old_series/ep2", "ai_videos/old_series/_series"):
        assert nodes[path]["obsolete"] is True, path
        assert nodes[path]["obsolete_note"] == "ai_videos/old_series/OBSOLETE.md", path
    # Only the folders that own or inherit a marker are flagged — not their contents.
    assert "obsolete" not in nodes["ai_videos/old_series/_series/characters"]


def test_member_marker_wins_over_series_marker_as_the_note(tmp_path: Path) -> None:
    series = _series(tmp_path, "old_series")
    _write(series / OBSOLETE_MARKER_NAME)
    _write(series / "ep1" / OBSOLETE_MARKER_NAME)
    node = _nodes(tmp_path)["ai_videos/old_series/ep1"]
    assert node["obsolete"] is True
    assert node["obsolete_note"] == "ai_videos/old_series/ep1/OBSOLETE.md"


def test_member_marker_alone_does_not_flag_the_series(tmp_path: Path) -> None:
    series = _series(tmp_path, "live_series")
    _write(series / "ep1" / OBSOLETE_MARKER_NAME)
    _write(series / "ep2/README.md")
    nodes = _nodes(tmp_path)
    assert "obsolete" not in nodes["ai_videos/live_series"]
    assert nodes["ai_videos/live_series/ep1"]["obsolete"] is True
    assert "obsolete" not in nodes["ai_videos/live_series/ep2"]


def test_six_module_drama_is_flagged_although_its_children_are_narrowed(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos/six_module"
    _write(drama / WORKFLOW_MARKER, json.dumps({"workflow": WORKFLOW_ID}))
    _write(drama / OBSOLETE_MARKER_NAME)
    (drama / "episodes/ep01").mkdir(parents=True)
    node = _nodes(tmp_path)["ai_videos/six_module"]
    assert node["workflow"] == WORKFLOW_ID
    assert node["obsolete"] is True
    assert node["obsolete_note"] == "ai_videos/six_module/OBSOLETE.md"


def test_library_and_nested_folders_with_a_marker_are_flagged(tmp_path: Path) -> None:
    _write(tmp_path / "ai_videos/_actors" / OBSOLETE_MARKER_NAME)
    _write(tmp_path / "ai_videos/_research/2026-09.json", "{}")
    _write(tmp_path / "ai_videos/_research/xianxia" / OBSOLETE_MARKER_NAME)
    nodes = _nodes(tmp_path)
    assert nodes["ai_videos/_actors"]["obsolete"] is True
    assert "is_drama" not in nodes["ai_videos/_actors"]
    assert nodes["ai_videos/_research/xianxia"]["obsolete"] is True
    assert "obsolete" not in nodes["ai_videos/_research"]


def test_api_tree_payload_carries_the_flag(tmp_path: Path) -> None:
    _write(tmp_path / "ai_videos/old_drama" / OBSOLETE_MARKER_NAME)
    _write(tmp_path / "ai_videos/new_drama/README.md")
    app = make_app(RepoRoot(path=tmp_path), BoundOrigin(host="127.0.0.1", port=8766), serve_static=False)
    with TestClient(app) as client:
        payload = client.get("/api/tree").json()
    dramas = {c["name"]: c for c in payload["children"][0]["children"]}
    assert dramas["old_drama"]["obsolete"] is True
    assert dramas["old_drama"]["obsolete_note"] == "ai_videos/old_drama/OBSOLETE.md"
    assert "obsolete" not in dramas["new_drama"]
