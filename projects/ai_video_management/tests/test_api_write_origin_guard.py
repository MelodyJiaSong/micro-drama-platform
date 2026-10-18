"""Every write endpoint is behind the Origin/Host gate (follow-up 239).

Until follow-up 239 only `PUT /api/file` and `POST /api/episode-workflow` were
checked. Any page open in the browser can send a no-preflight POST to 127.0.0.1
(a plain form post, `fetch(..., {mode: "no-cors"})`), so a foreign page could
archive, delete, hard-delete, empty the recycle bin, import Downloads, re-run
view extraction or overwrite research marks. Now every method except
GET/HEAD/OPTIONS is checked (`libs.common.origin.is_guarded`).

Each write endpoint is exercised twice with the same request:

* a foreign Origin → 403 `origin_blocked`, and nothing on disk changed;
* the app's own Origin → the endpoint's normal 200, with its effect on disk.

Everything runs on a throwaway repo root, and `AI_VIDEO_MGMT_DOWNLOADS_DIR`
points the Downloads import at a temp folder, so neither a passing nor a
regressed run can touch real dramas or the real Downloads folder.
"""
from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any

import imageio_ffmpeg
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from libs.common.episode_workflow import WORKFLOW_ID
from libs.common.origin import BoundOrigin, is_guarded
from libs.common.repo_root import RepoRoot
from libs.infrastructure.writers.downloads__writer import DOWNLOADS_ENV_VAR
from tests.conftest import make_app

# base_url makes every request carry `Host: 127.0.0.1:8766`, the bound address.
BACKEND = "http://127.0.0.1:8766"
OWN = {"Origin": BACKEND}
FOREIGN = {"Origin": "https://evil.example"}

DRAMA = "ai_videos/demo"
README = f"{DRAMA}/README.md"
NEW_README = "# changed\n"
EPISODE = f"{DRAMA}/episodes/ep01"
DRAFT = f"{EPISODE}/scenes/s1/shots/st1/drafts/20261016-200000_aaaa1111"
HERO = f"{DRAMA}/characters/c1_hero"
EXTRA = f"{DRAMA}/characters/c2_extra"
LAMP = f"{DRAMA}/props/v1_lamp"
BIN = "ai_videos/_deleted/demo"
DATASET = {
    "schema_version": 1,
    "title": "t",
    "series": [{"rank": 1, "slug": "alpha", "name_zh": "甲", "videos": [{"video_id": "vid00000001"}]}],
}


@dataclass(frozen=True)
class Sandbox:
    base: Path  # holds both the repo root and the Downloads folder
    repo: Path
    downloads: Path


@pytest.fixture(scope="module")
def turntable(tmp_path_factory: pytest.TempPathFactory) -> bytes:
    """A 4-second 32x32 clip with a tone: long enough for every canonical view (0 / 2 / 3.5 s)."""
    path = tmp_path_factory.mktemp("turntable") / "clip.mp4"
    subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", "testsrc=size=32x32:rate=4:duration=4",
         "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
         "-shortest", "-pix_fmt", "yuv420p", str(path)],
        check=True, timeout=60,
    )
    return path.read_bytes()


@pytest.fixture()
def sandbox(tmp_path: Path, turntable: bytes, monkeypatch: pytest.MonkeyPatch) -> Sandbox:
    repo, downloads = tmp_path / "repo", tmp_path / "downloads"
    files: dict[str, str | bytes] = {
        README: "# demo\n",
        f"{DRAMA}/workflow.json": json.dumps({"workflow": WORKFLOW_ID}),
        f"{HERO}/c1_hero.md": "# hero\n",
        f"{HERO}/c1_hero.png": b"hero",
        f"{HERO}/c1_hero.mp4": turntable,
        f"{HERO}/archive/c1_hero_old.png": b"old take",
        f"{EXTRA}/c2_extra.md": "# extra\n",
        f"{DRAFT}/generation.json": json.dumps({"stage": "draft", "resolution": "480p"}),
        f"{DRAFT}/review.md": "# 审核\n\n状态：待审核\n",
        f"{LAMP}/raw_download.png": b"lamp",
        f"{BIN}/gone.png": b"binned",
        "ai_videos/_research/ds.json": json.dumps(DATASET, ensure_ascii=False),
    }
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    (repo / EPISODE).mkdir(parents=True, exist_ok=True)
    downloads.mkdir()
    (downloads / "c1-2.png").write_bytes(b"new view")  # character view key → the hero's folder
    monkeypatch.setenv(DOWNLOADS_ENV_VAR, str(downloads))
    return Sandbox(base=tmp_path, repo=repo, downloads=downloads)


def _client(sandbox: Sandbox) -> TestClient:
    app = make_app(RepoRoot(path=sandbox.repo), BoundOrigin(host="127.0.0.1", port=8766))
    return TestClient(app, base_url=BACKEND)


def _snapshot(base: Path) -> dict[str, bytes | None]:
    """Every file (with its bytes) and folder under `base`."""
    return {
        p.relative_to(base).as_posix(): p.read_bytes() if p.is_file() else None
        for p in sorted(base.rglob("*"))
    }


def _flatten_routes(routes: Any) -> list[Any]:
    """Leaf routes, descending through FastAPI's lazy `_IncludedRouter` placeholders."""
    out: list[Any] = []
    for route in routes:
        inner = getattr(route, "original_router", None)
        out.extend(_flatten_routes(inner.routes) if inner is not None else [route])
    return out


def _write_routes(app: FastAPI) -> set[tuple[str, str]]:
    return {
        (method, route.path)
        for route in _flatten_routes(app.routes)
        for method in (getattr(route, "methods", None) or ())
        if is_guarded(method)
    }


def _workspace(client: TestClient) -> dict[str, Any]:
    response = client.get("/api/research/dataset/ds/workspace")
    assert response.status_code == 200, response.text
    return response.json()


def _story_save(client: TestClient) -> dict[str, Any]:
    response = client.get("/api/episode-workflow", params={"episode_path": EPISODE})
    assert response.status_code == 200, response.text
    story = next(m for m in response.json()["modules"] if m["id"] == "story")
    return {"episode_path": EPISODE, "module": "story", "operation": "save", "expected": story["etag"],
            "content": {"brief": "一个普通人的选择", "text": "他把最后一块面包分给陌生人。"}}


def _readme_unmodified_since(sandbox: Sandbox) -> dict[str, str]:
    # What the UI sends: the mtime it last read, as an HTTP date.
    mtime = (sandbox.repo / README).stat().st_mtime
    return {"If-Unmodified-Since": format_datetime(datetime.fromtimestamp(mtime, tz=timezone.utc), usegmt=True)}


# --- what each write leaves on disk ------------------------------------------

def _file_written(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / README).read_text(encoding="utf-8") == NEW_README


def _story_saved(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / EPISODE / "story.json").is_file()


def _reel_started(sb: Sandbox, _client: TestClient, body: dict[str, Any]) -> None:
    # 审片串联（follow-up 260）：开始时同步写下进度文件，拼接本身在后台线程
    assert body["name"] == "ep01_all"
    assert (sb.repo / EPISODE / "review_reel/ep01_all.status.json").is_file()


def _draft_judged(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    # 草稿条的用户审核（follow-up 265）
    assert "状态：通过（用户 " in (sb.repo / DRAFT / "review.md").read_text(encoding="utf-8")


def _renamed(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / LAMP / "v1_lamp.png").is_file()
    assert not (sb.repo / LAMP / "raw_download.png").exists()


def _archived(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / HERO / "archive/c1_hero.png").is_file()
    assert not (sb.repo / HERO / "c1_hero.png").exists()


def _unarchived(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / HERO / "c1_hero_old.png").is_file()


def _binned(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / "ai_videos/_deleted/demo/characters/c1_hero/c1_hero.png").is_file()
    assert not (sb.repo / HERO / "c1_hero.png").exists()


def _hard_deleted(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert not (sb.repo / BIN / "gone.png").exists()


def _purged(sb: Sandbox, _client: TestClient, body: dict[str, Any]) -> None:
    assert body == {"purged": 1}
    assert not (sb.repo / "ai_videos/_deleted").exists()


def _imported(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / HERO / "c1-2.png").is_file()
    assert not (sb.downloads / "c1-2.png").exists()


def _views_extracted(sb: Sandbox, _client: TestClient, _body: dict[str, Any]) -> None:
    assert (sb.repo / HERO / "views/c1_hero_front.png").is_file()


def _all_views_extracted(sb: Sandbox, _client: TestClient, body: dict[str, Any]) -> None:
    assert {item["folder"]: item["status"] for item in body["items"]} == {"c1_hero": "ok", "c2_extra": "skipped"}
    assert (sb.repo / HERO / "views/c1_hero_back.png").is_file()


def _series_marked(_sb: Sandbox, client: TestClient, _body: dict[str, Any]) -> None:
    assert _workspace(client)["series"] == {"alpha": {"status": "shortlist"}}


def _video_marked(_sb: Sandbox, client: TestClient, _body: dict[str, Any]) -> None:
    assert _workspace(client)["videos"] == {"vid00000001": {"bookmarked": True}}


@dataclass(frozen=True)
class Case:
    method: str
    route: str  # as registered on the router
    url: str
    body: Callable[[TestClient], dict[str, Any] | None]
    done: Callable[[Sandbox, TestClient, dict[str, Any]], None]  # asserts the write took effect
    headers: Callable[[Sandbox], dict[str, str]] = field(default=lambda _sb: {})

    def send(self, sandbox: Sandbox, client: TestClient, origin: dict[str, str], body: dict[str, Any] | None) -> Any:
        return client.request(self.method, self.url, json=body, headers={**self.headers(sandbox), **origin})


CASES: list[Case] = [
    Case("PUT", "/api/file", "/api/file", lambda _c: {"path": README, "content": NEW_README}, _file_written,
         headers=_readme_unmodified_since),
    Case("POST", "/api/episode-workflow", "/api/episode-workflow", _story_save, _story_saved),
    Case("POST", "/api/review-reel", "/api/review-reel", lambda _c: {"episode_path": EPISODE, "scene": None}, _reel_started),
    Case("POST", "/api/shot-take/verdict", "/api/shot-take/verdict", lambda _c: {"take_path": DRAFT, "verdict": "通过"}, _draft_judged),
    Case("POST", "/api/rename-media", "/api/rename-media", lambda _c: {"path": DRAMA}, _renamed),
    Case("POST", "/api/archive-media", "/api/archive-media", lambda _c: {"path": f"{HERO}/c1_hero.png"}, _archived),
    Case("POST", "/api/unarchive-media", "/api/unarchive-media",
         lambda _c: {"path": f"{HERO}/archive/c1_hero_old.png"}, _unarchived),
    Case("POST", "/api/delete-media", "/api/delete-media", lambda _c: {"path": f"{HERO}/c1_hero.png"}, _binned),
    Case("POST", "/api/hard-delete-media", "/api/hard-delete-media", lambda _c: {"path": f"{BIN}/gone.png"}, _hard_deleted),
    Case("POST", "/api/purge-deleted", "/api/purge-deleted", lambda _c: None, _purged),
    Case("POST", "/api/import-from-downloads", "/api/import-from-downloads", lambda _c: {"path": DRAMA}, _imported),
    Case("POST", "/api/extract-character-views", "/api/extract-character-views",
         lambda _c: {"path": f"{HERO}/c1_hero.mp4"}, _views_extracted),
    Case("POST", "/api/extract-all-character-views", "/api/extract-all-character-views",
         lambda _c: {"path": f"{DRAMA}/characters"}, _all_views_extracted),
    Case("PUT", "/api/research/dataset/{dataset}/series/{slug}/mark", "/api/research/dataset/ds/series/alpha/mark",
         lambda _c: {"status": "shortlist"}, _series_marked),
    Case("PUT", "/api/research/dataset/{dataset}/video/{video_id}/mark", "/api/research/dataset/ds/video/vid00000001/mark",
         lambda _c: {"bookmarked": True}, _video_marked),
]
CASE_IDS = [f"{case.method} {case.route}" for case in CASES]


def test_every_write_route_has_a_case(sandbox: Sandbox) -> None:
    """A new write endpoint must come with its own foreign/own Origin case below."""
    registered = _write_routes(_client(sandbox).app)  # type: ignore[arg-type]
    covered = {(case.method, case.route) for case in CASES}
    assert registered == covered, (
        f"write routes without a gate case: {sorted(registered - covered)}; "
        f"cases for routes that no longer exist: {sorted(covered - registered)}"
    )


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_foreign_origin_is_refused_before_the_handler_runs(sandbox: Sandbox, case: Case) -> None:
    client = _client(sandbox)
    body = case.body(client)
    before = _snapshot(sandbox.base)
    response = case.send(sandbox, client, FOREIGN, body)
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": {"kind": "origin_blocked"}}
    assert _snapshot(sandbox.base) == before


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_own_origin_is_admitted_and_the_write_happens(sandbox: Sandbox, case: Case) -> None:
    client = _client(sandbox)
    response = case.send(sandbox, client, OWN, case.body(client))
    assert response.status_code == 200, response.text
    case.done(sandbox, client, response.json())


def test_every_registered_write_route_refuses_a_foreign_origin(sandbox: Sandbox) -> None:
    """Independent of CASES: whatever write route exists, a foreign page gets 403."""
    client = _client(sandbox)
    before = _snapshot(sandbox.base)
    routes = sorted(_write_routes(client.app))  # type: ignore[arg-type]
    assert routes
    for method, path in routes:
        response = client.request(method, re.sub(r"\{[^}]+\}", "x", path), json={}, headers=FOREIGN)
        assert response.status_code == 403, f"{method} {path}: {response.status_code} {response.text}"
    assert _snapshot(sandbox.base) == before


@pytest.mark.parametrize(
    "headers",
    [
        pytest.param({"Origin": "null"}, id="null-origin"),  # sandboxed iframe, file:// page
        pytest.param({"Origin": "http://127.0.0.1:5174"}, id="vite-origin-without-proxy-rewrite"),
        pytest.param({"Origin": "http://127.0.0.1:8765"}, id="wrong-port"),
        pytest.param({"Origin": "http://127.0.0.1:8766.evil.example"}, id="lookalike-prefix"),
        pytest.param({"Origin": BACKEND, "Host": "evil.example:8766"}, id="dns-rebinding-host"),
        pytest.param({"Host": "evil.example:8766"}, id="dns-rebinding-host-without-origin"),
        pytest.param({}, id="no-origin"),  # SEC-ORIGIN-HOST-01: a write without Origin is refused
    ],
)
def test_foreign_shapes_cannot_empty_the_recycle_bin(sandbox: Sandbox, headers: dict[str, str]) -> None:
    response = _client(sandbox).post("/api/purge-deleted", headers=headers)
    assert response.status_code == 403, response.text
    assert (sandbox.repo / BIN / "gone.png").is_file()


@pytest.mark.parametrize(
    "headers",
    [
        pytest.param(OWN, id="own-origin"),
        pytest.param({"Origin": "http://localhost:8766", "Host": "localhost:8766"}, id="localhost-alias"),
    ],
)
def test_own_shapes_are_admitted(sandbox: Sandbox, headers: dict[str, str]) -> None:
    response = _client(sandbox).post("/api/purge-deleted", headers=headers)
    assert response.status_code == 200, response.text
    assert not (sandbox.repo / "ai_videos/_deleted").exists()


def test_unknown_write_paths_are_gated_too(sandbox: Sandbox) -> None:
    """The rule is by method, not by a route list."""
    client = _client(sandbox)
    assert client.post("/api/no-such-route", headers=FOREIGN).status_code == 403
    assert client.post("/api/no-such-route", headers=OWN).status_code == 404


@pytest.mark.parametrize(
    "method,url",
    [("GET", "/api/tree"), ("GET", f"/api/file?path={README}"), ("HEAD", "/api/health"), ("OPTIONS", "/api/purge-deleted")],
)
def test_reads_are_not_gated(sandbox: Sandbox, method: str, url: str) -> None:
    response = _client(sandbox).request(method, url, headers=FOREIGN)
    assert response.status_code != 403, response.text
