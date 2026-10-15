"""The sandbox exposes `ai_videos/` only (follow-up 233).

`downloaded_novels/` and `my_novel/` were admitted by follow-ups 096 / 113 for
the novel browsing, which went with the old pipeline; their data stays on disk
but is no longer reachable through the API or listed in the tree.
"""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.common.safe_resolve import SafeResolver
from tests.conftest import make_app

NOVEL_FILES = ("my_novel/feng_shou_lu/README.md", "downloaded_novels/xianxia/fanren/ch001.md")


def _repo(tmp_path: Path) -> Path:
    for rel in ("ai_videos/demo/README.md", *NOVEL_FILES):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# x\n", encoding="utf-8")
    return tmp_path


def test_novel_roots_are_outside_the_sandbox(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    assert exposed.is_inside("ai_videos/demo/README.md")
    assert resolver.resolve("ai_videos/demo/README.md") is not None
    for rel in NOVEL_FILES:
        assert not exposed.is_inside(rel), rel
        assert resolver.resolve(rel) is None, rel


def test_api_serves_ai_videos_and_404s_the_novel_roots(tmp_path: Path) -> None:
    app = make_app(RepoRoot(path=_repo(tmp_path)), BoundOrigin(host="127.0.0.1", port=8766), serve_static=False)
    with TestClient(app) as client:
        assert client.get("/api/file", params={"path": "ai_videos/demo/README.md"}).status_code == 200
        for rel in NOVEL_FILES:
            assert client.get("/api/file", params={"path": rel}).status_code == 404, rel
        sections = client.get("/api/tree").json()["children"]
    assert [s["name"] for s in sections] == ["AI Videos"]
