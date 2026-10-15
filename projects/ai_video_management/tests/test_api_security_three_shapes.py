"""Header-mutating-layer tests cover ALL three Origin/Host shapes.

Without the pre-rewrite case, dropping the Vite proxy `configure` hook silently
re-introduces a cross-port 403 regression.

The PUT cases run against a throwaway repo root (`tmp_path`) holding one drama,
so they never depend on — or risk touching — a real drama folder. (They used to
target `ai_videos/wukong_juexing/`, which no longer exists, so two of them had
been failing with 404 since that drama was deleted.)
"""
from __future__ import annotations

from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from tests.conftest import make_app, repo_root

README = "ai_videos/demo/README.md"


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    readme = tmp_path / README
    readme.parent.mkdir(parents=True)
    readme.write_text("# demo\n", encoding="utf-8")
    return tmp_path


def _client(root: Path) -> TestClient:
    rr = RepoRoot(path=root)
    bound = BoundOrigin(host="127.0.0.1", port=8766)
    return TestClient(make_app(rr, bound, serve_static=False))


def _ius_now() -> str:
    return format_datetime(datetime.now(tz=timezone.utc), usegmt=True)


def test_put_file_pre_rewrite_origin_403(sandbox: Path) -> None:
    """Pre-rewrite shape — browser Origin: http://127.0.0.1:5174 direct to backend → 403."""
    client = _client(sandbox)
    r = client.put(
        "/api/file",
        json={"path": README, "content": "test"},
        headers={
            "Origin": "http://127.0.0.1:5174",
            "Host": "127.0.0.1:5174",
            "If-Unmodified-Since": _ius_now(),
        },
    )
    assert r.status_code == 403, r.text


def test_put_file_loopback_alias_admit(sandbox: Path) -> None:
    """localhost alias at the bound port admits — but stale mtime so we get 409 (proves gate didn't block)."""
    client = _client(sandbox)
    r = client.put(
        "/api/file",
        json={"path": README, "content": "test"},
        headers={
            "Origin": "http://localhost:8766",
            "Host": "localhost:8766",
            "If-Unmodified-Since": "Wed, 01 Jan 1970 00:00:00 GMT",
        },
    )
    # Origin/Host gate passed; write rejected as stale (409). Either way, NOT 403.
    assert r.status_code != 403, r.text
    assert r.status_code == 409, f"unexpected status {r.status_code}: {r.text}"
    assert (sandbox / README).read_text(encoding="utf-8") == "# demo\n"


def test_put_file_wrong_port_8765_403(sandbox: Path) -> None:
    """Any port other than 8766 is foreign — gate must reject."""
    client = _client(sandbox)
    r = client.put(
        "/api/file",
        json={"path": README, "content": "test"},
        headers={
            "Origin": "http://127.0.0.1:8765",
            "Host": "127.0.0.1:8765",
            "If-Unmodified-Since": _ius_now(),
        },
    )
    assert r.status_code == 403, r.text


def test_get_tree_unguarded() -> None:
    """GET is never gated (only methods other than GET/HEAD/OPTIONS are) — no Origin/Host check."""
    client = _client(repo_root())
    r = client.get("/api/tree")
    assert r.status_code == 200
    payload = r.json()
    assert payload["type"] == "section"
    assert [c["name"] for c in payload["children"]] == ["AI Videos"]


def test_put_file_extension_rejected_as_400(sandbox: Path) -> None:
    """Image extensions are NOT writeable — 400 (wrong content kind)."""
    client = _client(sandbox)
    r = client.put(
        "/api/file",
        json={"path": "ai_videos/demo/main.png", "content": "data"},
        headers={
            "Origin": "http://127.0.0.1:8766",
            "Host": "127.0.0.1:8766",
            "If-Unmodified-Since": _ius_now(),
        },
    )
    assert r.status_code == 400, r.text
    assert r.json()["detail"]["kind"] == "extension_not_allowed"
    assert not (sandbox / "ai_videos/demo/main.png").exists()
