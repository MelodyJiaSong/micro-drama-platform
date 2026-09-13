"""SPA deep links resolve; unknown /api paths still 404 as JSON.

Every client-side route used to 404 on a direct open or refresh, because
`StaticFiles(html=True)` only falls back to index.html for directory paths. The
research workspace keeps its tab and open series in the URL, so this had to work.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from tests.conftest import make_app, repo_root

HEADERS = {"Origin": "http://127.0.0.1:8766", "Host": "127.0.0.1:8766"}


@pytest.fixture()
def client() -> TestClient:
    app = make_app(
        RepoRoot(path=repo_root()),
        BoundOrigin(host="127.0.0.1", port=8766),
        serve_static=True,
    )
    return TestClient(app)


@pytest.mark.parametrize(
    "route", ["/research", "/workflow", "/actors", "/drama", "/bgm", "/deleted"]
)
def test_spa_routes_serve_the_app_shell(client: TestClient, route: str) -> None:
    r = client.get(route, headers=HEADERS)
    assert r.status_code == 200, r.text
    assert "text/html" in r.headers["content-type"]


def test_spa_route_with_query_string_resolves(client: TestClient) -> None:
    r = client.get("/research?dataset=youtube_series&tab=series", headers=HEADERS)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_root_still_serves_the_app(client: TestClient) -> None:
    assert client.get("/", headers=HEADERS).status_code == 200


def test_real_asset_still_served_as_itself(client: TestClient) -> None:
    r = client.get("/index.html", headers=HEADERS)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_unknown_api_path_stays_a_json_404(client: TestClient) -> None:
    r = client.get("/api/definitely-not-a-route", headers=HEADERS)
    assert r.status_code == 404
    assert "text/html" not in r.headers.get("content-type", "")
