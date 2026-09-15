from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from apps.api.app_factory import create_app
from apps.api.container import Container
from libs.application.queries.app_settings__query import AppSettingsQuery
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from libs.infrastructure.middleware.request_class__middleware import UI_SESSION_COOKIE
from tests.libs.application.config_entities.support import GLOBAL_TOML, build_repo_template

TOKEN = "c" * 40
HY3 = "ai_videos/huangye_shenghuo/hy3"
BEARER = {"authorization": f"Bearer {TOKEN}"}


@pytest.fixture(scope="module")
def api(tmp_path_factory: pytest.TempPathFactory) -> Iterator[tuple[TestClient, str, Path]]:
    root = tmp_path_factory.mktemp("config_routes")
    repo = root / "repo"
    repo.mkdir()
    build_repo_template(repo)
    project = root / "project"
    (project / "config").mkdir(parents=True)
    real_global = GLOBAL_TOML.read_text(encoding="utf-8")
    test_global = real_global.replace(
        'start_url = "https://jimeng.jianying.com/ai-tool/generate?type=video"', 'start_url = "http://127.0.0.1:9/fake-jimeng"'
    )
    assert test_global != real_global, "test mode requires a localhost start_url (hard guard)"
    (project / "config" / "global.toml").write_text(test_global, encoding="utf-8")
    static = project / "apps" / "api" / "static"
    (static / "assets").mkdir(parents=True)
    (static / "index.html").write_text("<!doctype html><title>即梦桥接</title>", encoding="utf-8")
    settings = AppSettingsQuery(EnvFileReader()).load(
        project,
        {
            "JWB_TEST_MODE": "1",
            "JIMENG_BRIDGE_TOKEN": TOKEN,
            "JIMENG_BRIDGE_REPO_ROOT": str(repo),
            "JIMENG_BRIDGE_DATA_DIR": str(root / "data"),
            "DREAMINA_CLI_PATH": "C:/fake/dreamina.exe",
        },
    )
    container = Container(settings=settings)
    container.wire()
    base = f"http://127.0.0.1:{settings.port}"
    with TestClient(create_app(settings, container), base_url=base) as client:
        yield client, base, repo
    container.sqlite_client().close()


def _walk(node: dict[str, object]) -> Iterator[dict[str, object]]:
    yield node
    for child in node["children"]:  # type: ignore[union-attr]
        yield from _walk(child)  # type: ignore[arg-type]


def test_dramas_tree_walks_like_the_ui(api: tuple[TestClient, str, Path]) -> None:
    client, _, _ = api
    body = client.get("/api/dramas", headers=BEARER).json()
    nodes = [node for root in body["dramas"] for node in _walk(root)]
    for node in nodes:
        assert {"name", "path", "type", "children"} <= node.keys()
    series = next(node for node in nodes if node["name"] == "huangye_shenghuo")
    assert series["type"] == "series"
    assert {child["name"] for child in series["children"]} >= {"hy1", "hy2", "hy3"}
    assert not any(node["name"] == "notes" for node in nodes)


@pytest.mark.parametrize("encoded", [HY3, HY3.replace("/", "%2F")])
def test_get_config_accepts_plain_and_percent_encoded_slashes(api: tuple[TestClient, str, Path], encoded: str) -> None:
    client, _, _ = api
    response = client.get(f"/api/dramas/{encoded}/config", headers=BEARER)
    assert response.status_code == 200
    assert response.json()["drama_rel"].endswith("huangye_shenghuo/hy3")


@pytest.mark.parametrize(
    ("path", "statuses"),
    [
        (HY3.replace("/", "%252F"), {403, 404}),
        (HY3.replace("/hy3", "%5Chy3"), {403, 404}),
        ("ai_videos/huangye_shenghuo/hy3/renders", {404}),
        ("..%2F..%2Fsecret", {403, 404}),
    ],
)
def test_unsafe_or_non_root_drama_paths_are_refused(api: tuple[TestClient, str, Path], path: str, statuses: set[int]) -> None:
    client, _, _ = api
    response = client.get(f"/api/dramas/{path}/config", headers=BEARER)
    assert response.status_code in statuses
    assert set(response.json()) >= {"error_code", "message", "hint", "config_key"}


def test_propose_save_conflict_and_validation_errors(api: tuple[TestClient, str, Path]) -> None:
    client, _, repo = api
    proposal = client.post(f"/api/dramas/{HY3}/config/propose", headers=BEARER).json()
    assert proposal["exists"] is False and proposal["proposed_toml"]
    assert any(item["code"] == "entities_never_synced" for item in proposal["needs_confirmation"])
    assert not (repo / HY3 / "jimeng_config.toml").exists()

    saved = client.put(f"/api/dramas/{HY3}/config", headers=BEARER, json={"text": proposal["proposed_toml"], "expected_sha256": None})
    assert saved.status_code == 200 and saved.json()["sha256"]

    conflict = client.put(f"/api/dramas/{HY3}/config", headers=BEARER, json={"text": proposal["proposed_toml"], "expected_sha256": None})
    assert conflict.status_code == 409 and conflict.json()["error_code"] == "config_conflict"

    data = dict(proposal["proposed_data"])
    data["video"] = {**data["video"], "count": 99}
    invalid = client.put(f"/api/dramas/{HY3}/config", headers=BEARER, json={"data": data, "expected_sha256": saved.json()["sha256"]})
    assert invalid.status_code == 422 and invalid.json()["config_key"] == "video.count"


def test_global_config_is_readable_without_secrets_and_writable_only_by_ui(api: tuple[TestClient, str, Path]) -> None:
    client, base, _ = api
    response = client.get("/api/config/global", headers=BEARER)
    assert response.status_code == 200 and TOKEN not in response.text
    body = response.json()
    assert "cli.path" in body["overridden_by_env"]

    bearer_write = client.put("/ui-api/config/global", headers=BEARER, json={"text": body["raw_text"], "expected_sha256": body["sha256"]})
    assert bearer_write.status_code == 403

    client.get("/")
    assert client.cookies.get(UI_SESSION_COOKIE)
    ui_write = client.put(
        "/ui-api/config/global",
        headers={"sec-fetch-site": "same-origin", "origin": base},
        json={"text": body["raw_text"], "expected_sha256": body["sha256"]},
    )
    assert ui_write.status_code == 200, ui_write.text


def test_reconcile_reports_never_synced(api: tuple[TestClient, str, Path]) -> None:
    client, _, _ = api
    body = client.get("/api/entities/reconcile", headers=BEARER, params={"drama": HY3}).json()
    assert body["never_synced"] is True and body["drama_rel"].endswith("hy3")


def test_thumbnails_and_artifacts_fail_safely(api: tuple[TestClient, str, Path]) -> None:
    client, _, _ = api
    empty_png = f"{HY3}/2_世界观人设/characters/c1_砌炉的老人/c1-1.png"
    assert client.get("/api/thumbs", headers=BEARER, params={"path": empty_png}).status_code == 415
    assert client.get("/api/thumbs", headers=BEARER, params={"path": "../CLAUDE.md"}).status_code == 403
    assert client.get("/api/artifacts/job_1/preview_x.jpg", headers=BEARER).status_code == 404
    traversal = client.get("/api/artifacts/job_1/private%2Fdom_x.html", headers=BEARER)
    assert traversal.status_code == 404 and "<html" not in traversal.text


def test_state_changing_routes_are_not_shadowed_by_the_spa_shell(api: tuple[TestClient, str, Path]) -> None:
    client, _, _ = api
    for method, path in (("POST", f"/api/dramas/{HY3}/config/propose"), ("PUT", f"/api/dramas/{HY3}/config"), ("PUT", "/ui-api/config/global")):
        response = client.request(method, path, headers=BEARER, json={})
        assert response.status_code != 405, (method, path)
