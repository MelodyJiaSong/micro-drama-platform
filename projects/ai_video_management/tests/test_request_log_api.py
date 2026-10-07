from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.request_log__reader import RequestLogReader
from tests.conftest import make_app


def write_log(tmp_path, name="demo/episodes/ep01/request_log.md", count=5):
    file = tmp_path / "ai_videos" / name
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("# 请求日志\n" + "".join("```json\n" + json.dumps({"event": "request", "n": i}) + "\n```\n" for i in range(count)), encoding="utf-8")
    return file.relative_to(tmp_path).as_posix()


def test_reader_pages_newest_first_and_rejects_path_escape(tmp_path):
    path = write_log(tmp_path)
    reader = RequestLogReader(ExposedTree(tmp_path))
    assert reader.list().logs[0]["path"] == path
    result = reader.read(path, 1, 2)
    assert result.total == 5 and [e["n"] for e in result.entries] == [3, 2]
    for invalid in ("../request_log.md", "ai_videos/../../outside/request_log.md", "ai_videos/demo/other.md"):
        with pytest.raises(FileNotFoundError):
            reader.read(invalid, 0, 5)


def test_logs_larger_than_generic_file_limit_remain_readable(tmp_path):
    path = write_log(tmp_path, count=70000)
    file = tmp_path / path
    assert file.stat().st_size > 1048576
    assert RequestLogReader(ExposedTree(tmp_path)).read(path, 0, 2).total == 70000


def test_api_lists_pages_and_disallows_overwrite(tmp_path):
    path = write_log(tmp_path)
    client = TestClient(make_app(RepoRoot(path=tmp_path), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    assert client.get("/api/request-logs").status_code == 200
    response = client.get("/api/request-log", params={"path": path, "offset": 1, "limit": 2})
    assert response.status_code == 200
    assert [e["n"] for e in response.json()["entries"]] == [3, 2]
    assert client.get("/api/request-log", params={"path": path, "limit": 200}).status_code == 422
    assert client.get("/api/request-log", params={"path": "../request_log.md"}).status_code == 404
    response = client.put("/api/file", json={"path": path, "content": "erase"}, headers={"Origin": "http://127.0.0.1:8766"})
    assert response.status_code == 400
    assert "erase" not in (tmp_path / path).read_text(encoding="utf-8")
    response = client.put("/api/file", json={"path": path.replace("request_log.md", "REQUEST_LOG.MD"), "content": "erase"},
        headers={"Origin": "http://127.0.0.1:8766"})
    assert response.status_code == 400
