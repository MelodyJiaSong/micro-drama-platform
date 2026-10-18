"""Lazy sidebar tree (follow-up 280).

`/api/tree?lazy=1` returns the navigation skeleton plus the first real folder
levels; deeper folders are `lazy` stubs (no children) that the sidebar fills
with `/api/tree/subtree?path=…` when opened. The full walk had grown to ~47k
nodes / 8.8 MB / 10 s and was repeated on every page load.
"""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.tree__reader import OBSOLETE_MARKER_NAME, TreeReader
from tests.conftest import make_app


def _write(path: Path, text: str = "# x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _find(node: dict, path: str) -> dict | None:
    if node.get("path") == path:
        return node
    for child in node.get("children", []):
        hit = _find(child, path)
        if hit is not None:
            return hit
    return None


def _drama(tmp_path: Path) -> Path:
    drama = tmp_path / "ai_videos/old_drama"
    _write(drama / "README.md")
    _write(drama / "assets/characters/c1_hero/c1_hero.md")
    _write(drama / "assets/characters/c1_hero/views/front.png", "png")
    _write(drama / "assets/characters/c2_empty/notes.bin", "x")   # nothing visible inside
    return drama


def test_full_build_is_unchanged(tmp_path: Path) -> None:
    _drama(tmp_path)
    tree = TreeReader(ExposedTree(tmp_path)).build()
    node = _find(tree, "ai_videos/old_drama/assets/characters/c1_hero/views/front.png")
    assert node is not None and node["type"] == "image"
    stack = [tree]
    while stack:
        node = stack.pop()
        assert "lazy" not in node
        stack.extend(node.get("children", []))


def test_lazy_build_stops_two_folders_below_a_drama(tmp_path: Path) -> None:
    _drama(tmp_path)
    tree = TreeReader(ExposedTree(tmp_path)).build(lazy=True)
    characters = _find(tree, "ai_videos/old_drama/assets/characters")
    assert characters is not None and characters.get("lazy") is None
    hero = _find(tree, "ai_videos/old_drama/assets/characters/c1_hero")
    assert hero is not None and hero["type"] == "directory"
    assert hero["lazy"] is True and hero["children"] == []
    # A folder a full walk would drop (nothing visible inside) is not stubbed either.
    assert _find(tree, "ai_videos/old_drama/assets/characters/c2_empty") is None
    assert _find(tree, "ai_videos/old_drama/assets/characters/c1_hero/c1_hero.md") is None


def test_stub_carries_its_obsolete_marker(tmp_path: Path) -> None:
    drama = _drama(tmp_path)
    _write(drama / "assets/characters/c1_hero" / OBSOLETE_MARKER_NAME)
    hero = _find(TreeReader(ExposedTree(tmp_path)).build(lazy=True), "ai_videos/old_drama/assets/characters/c1_hero")
    assert hero["obsolete"] is True
    assert hero["obsolete_note"] == f"ai_videos/old_drama/assets/characters/c1_hero/{OBSOLETE_MARKER_NAME}"


def test_subtree_lists_one_level_with_stubs_below(tmp_path: Path) -> None:
    _drama(tmp_path)
    reader = TreeReader(ExposedTree(tmp_path))
    hero = reader.subtree("ai_videos/old_drama/assets/characters/c1_hero")
    names = {c["name"]: c for c in hero["children"]}
    assert names["c1_hero.md"]["type"] == "file"
    assert names["views"]["lazy"] is True and names["views"]["children"] == []
    full = reader.subtree("ai_videos/old_drama/assets/characters/c1_hero", depth=None)
    views = next(c for c in full["children"] if c["name"] == "views")
    assert "lazy" not in views and views["children"][0]["name"] == "front.png"


def test_subtree_api_and_path_guard(tmp_path: Path) -> None:
    _drama(tmp_path)
    app = make_app(RepoRoot(path=tmp_path), BoundOrigin(host="127.0.0.1", port=8766), serve_static=False)
    with TestClient(app) as client:
        lazy = client.get("/api/tree", params={"lazy": 1}).json()
        assert _find(lazy, "ai_videos/old_drama/assets/characters/c1_hero")["lazy"] is True
        full = client.get("/api/tree").json()
        assert _find(full, "ai_videos/old_drama/assets/characters/c1_hero/views/front.png") is not None
        ok = client.get("/api/tree/subtree", params={"path": "ai_videos/old_drama/assets/characters/c1_hero"})
        assert ok.status_code == 200 and {c["name"] for c in ok.json()["children"]} == {"c1_hero.md", "views"}
        deep = client.get("/api/tree/subtree", params={"path": "ai_videos/old_drama/assets", "depth": 0}).json()
        assert _find(deep, "ai_videos/old_drama/assets/characters/c1_hero/views/front.png") is not None
        assert client.get("/api/tree/subtree", params={"path": "ai_videos/../secrets"}).status_code == 400
        assert client.get("/api/tree/subtree", params={"path": "projects"}).status_code == 400
        assert client.get("/api/tree/subtree", params={"path": "ai_videos/nope"}).status_code == 404
