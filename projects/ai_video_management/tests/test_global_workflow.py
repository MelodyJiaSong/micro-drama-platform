from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.global_workflow__query import GlobalWorkflowQuery
from libs.common.config_redaction import redact_config
from libs.common.global_workflow import CATALOG_PATH, GLOBAL_MAX_BYTES, GlobalWorkflowError
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.global_workflow__reader import GlobalWorkflowReader
from tests.conftest import make_app, repo_root


def setup_catalog(root: Path, sources: list[dict], discover: list[dict] | None = None) -> None:
    path = root / CATALOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"groups": [{"id": "agents", "title": "代理"}], "sources": sources, "discover": discover or []}), encoding="utf-8")


def test_credentials_are_hidden_in_nested_configs_and_urls() -> None:
    value = {"model": "declared-model", "mcp": {"api_key": "secret1", "auth": "secret2", "env": {"KEY": "secret3"},
        "headers": {"X-Custom": "secret4"}, "args": ["--custom", "secret5"], "command": "curl --data secret6",
        "url": "https://user:secret7@example.com/api?signature=secret8"}, "note": "Bearer secret9"}
    result = json.dumps(redact_config(value))
    assert "declared-model" in result and "example.com/api" in result
    assert all(f"secret{index}" not in result for index in range(1, 10))
    assert "KEY" in result and "X-Custom" in result


def test_private_files_are_never_registered(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": path, "group": "agents"} for path in [".codex/auth.json", ".claude/.credentials.json", ".claude/memory/private.md", ".env"]])
    reader = GlobalWorkflowReader(tmp_path)
    assert all(entry.status == "unavailable" for entry in reader.catalog()[1])


def test_registered_configs_only_and_fail_closed_for_malformed_or_oversized_files(tmp_path: Path) -> None:
    user = tmp_path / "user"
    (user / ".codex").mkdir(parents=True)
    (user / ".codex/config.toml").write_text('model="model-a"\napi_key="NEVER_SEND"', encoding="utf-8")
    setup_catalog(tmp_path, [{"path": ".codex/config.toml", "group": "agents", "scope": "user"}])
    reader = GlobalWorkflowReader(tmp_path, user)
    query = GlobalWorkflowQuery(reader)
    source = query.source("user:.codex/config.toml")
    assert source["redacted"] and "NEVER_SEND" not in source["content"] and "model-a" in source["content"]
    for identity in ["user:.codex/auth.json", "repo:../AGENTS.md", "repo:C:/auth.json", "user:.claude/memory/private.md"]:
        with pytest.raises(GlobalWorkflowError):
            query.source(identity)
    (user / ".codex/config.toml").write_text('api_key="bad', encoding="utf-8")
    assert query.source("user:.codex/config.toml")["status"] == "unavailable"
    (user / ".codex/config.toml").write_bytes(b"x" * (GLOBAL_MAX_BYTES + 1))
    assert query.source("user:.codex/config.toml")["status"] == "unavailable"


def test_missing_config_and_dynamic_discovery_and_symlink_refusal(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "AGENTS.md", "group": "agents"}], [{"glob": ".agents/skills/ai-videos-*/**/*.md", "group": "agents"}])
    reader = GlobalWorkflowReader(tmp_path, tmp_path / "user")
    assert reader.source("repo:AGENTS.md")["status"] == "missing"
    target = tmp_path / ".agents/skills/ai-videos-new/SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("new shared skill", encoding="utf-8")
    assert any(entry.path == target.relative_to(tmp_path).as_posix() for entry in reader.catalog()[1])
    try:
        (tmp_path / "AGENTS.md").symlink_to(target)
    except OSError:
        pytest.skip("symlink creation unavailable on this Windows environment")
    assert reader.source("repo:AGENTS.md")["status"] == "unavailable"


def test_model_defaults_are_read_without_executing_python(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "tools/defaults.py", "group": "agents", "view": "constants"}])
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/defaults.py").write_text('raise RuntimeError("must not execute")\nMODEL="declared"\nAPI_KEY="NEVER_SEND"\nLIMITS={"seconds": 30}\n', encoding="utf-8")
    data = GlobalWorkflowReader(tmp_path).source("repo:tools/defaults.py")
    assert data["status"] == "available" and "NEVER_SEND" not in data["content"]
    assert json.loads(data["content"])["LIMITS"] == {"seconds": 30}


def test_windows_junctions_are_refused_without_symlink_privilege(tmp_path: Path) -> None:
    import os
    import subprocess
    if os.name != "nt":
        pytest.skip("Windows junction behavior")
    target = tmp_path / "inside"
    target.mkdir()
    (target / "settings.json").write_text('{"model":"should-not-read"}', encoding="utf-8")
    link = tmp_path / ".codex"
    result = subprocess.run(["powershell", "-NoProfile", "-Command", "New-Item", "-ItemType", "Junction", "-Path", str(link), "-Target", str(target)], capture_output=True)
    if result.returncode:
        pytest.skip("junction creation unavailable")
    setup_catalog(tmp_path, [{"path": ".codex/settings.json", "group": "agents"}])
    try:
        reader = GlobalWorkflowReader(tmp_path)
        assert reader.source("repo:.codex/settings.json")["status"] == "unavailable"
    finally:
        os.rmdir(link)  # Remove only this test's junction, never its target tree.


def test_routes_registered_and_unknown_sources_are_404(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "AGENTS.md", "group": "agents"}])
    (tmp_path / "AGENTS.md").write_text("shared instructions", encoding="utf-8")
    (tmp_path / "ai_videos").mkdir()
    app = make_app(RepoRoot(tmp_path), BoundOrigin("127.0.0.1", 8766))
    with TestClient(app, base_url="http://127.0.0.1:8766") as client:
        assert client.get("/api/global-workflow").status_code == 200
        assert client.get("/api/global-workflow/coverage").status_code == 200
        response = client.get("/api/global-workflow/source", params={"source_id": "repo:AGENTS.md"})
        assert response.status_code == 200 and response.json()["content"] == "shared instructions"
        assert client.get("/api/global-workflow/source", params={"source_id": "user:.codex/auth.json"}).status_code == 404


def test_reference_numbers_survive_discovery_insertions_and_title_changes(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "AGENTS.md", "group": "agents", "title": "Old title"}], [{"glob": ".agents/*.md", "group": "agents"}])
    path = tmp_path / CATALOG_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    data["source_numbers"] = {"repo:AGENTS.md": "2.1.4"}
    path.write_text(json.dumps(data), encoding="utf-8")
    reader = GlobalWorkflowReader(tmp_path)
    assert reader.source("repo:AGENTS.md")["number"] == "2.1.4"
    (tmp_path / ".agents/aaa.md").write_text("new discovered source", encoding="utf-8")
    data["sources"][0]["title"] = "New title"
    path.write_text(json.dumps(data), encoding="utf-8")
    entries = {source.id: source for source in reader.catalog()[1]}
    assert entries["repo:AGENTS.md"].number == "2.1.4"
    assert entries["repo:.agents/aaa.md"].number == ""
    data["source_numbers"]["repo:.agents/aaa.md"] = "2.1.4"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate global source numbers"):
        reader.catalog()


def test_function_cli_defaults_and_environment_names_are_static_and_redacted(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "tools/defaults.py", "group": "agents", "view": "constants"}])
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/defaults.py").write_text('''
raise RuntimeError("never execute")
def generate(*, seconds=8, api_key="DO_NOT_EXPOSE"):
    MODEL = "nested-model"
    model = os.environ.get("MODEL_OVERRIDE", "fallback")
parser.add_argument("--duration", default=12)
parser.add_argument("--api-key", default="DO_NOT_EXPOSE")
''', encoding="utf-8")
    detail = GlobalWorkflowReader(tmp_path).source("repo:tools/defaults.py")
    content = detail["content"]
    assert "DO_NOT_EXPOSE" not in content and detail["status"] == "available"
    values = json.loads(content)
    assert values["MODEL"] == "nested-model"
    assert next(iter(values["FUNCTION_DEFAULTS"].values()))["seconds"] == 8
    assert values["CLI_DEFAULTS"][0]["default"] == 12
    assert values["ENVIRONMENT_NAMES"] == ["MODEL_OVERRIDE"]


def test_inventory_reports_unreadable_unnumbered_and_unregistered_references(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [{"path": "AGENTS.md", "group": "agents"}, {"path": ".codex/config.toml", "group": "agents"}])
    (tmp_path / "AGENTS.md").write_text("Use `tools/new.py`. [local](specs/ai_video/demo/rules.md)", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/new.py").write_text("MODEL = 'new'", encoding="utf-8")
    local = tmp_path / "specs/ai_video/demo/rules.md"
    local.parent.mkdir(parents=True)
    local.write_text("local facts", encoding="utf-8")
    data = GlobalWorkflowReader(tmp_path).inventory()
    assert data["total"] == 2 and data["available"] == 1 and data["numbered"] == 0
    assert {issue["kind"] for issue in data["issues"]} == {"missing", "unnumbered"}
    assert [reference["path"] for reference in data["references"]] == ["tools/new.py"]
    (tmp_path / ".codex").mkdir()
    (tmp_path / ".codex/config.toml").write_text('model="broken', encoding="utf-8")
    assert "unavailable" in {issue["kind"] for issue in GlobalWorkflowReader(tmp_path).inventory()["issues"]}


def test_repository_workflow_sources_are_numbered_and_reference_closure_is_registered(tmp_path: Path) -> None:
    reader = GlobalWorkflowReader(repo_root(), tmp_path / "no-user-config")
    groups, sources = reader.catalog()
    group_numbers = {group["id"]: group["number"] for group in groups}
    assert all(source.number.startswith(group_numbers[source.group] + ".") for source in sources)
    for category in {group["category"] for group in groups}:
        numbers = [group["number"] for group in groups if group["category"] == category and not group.get("overview")]
        assert numbers == [f"{numbers[0].split('.')[0]}.{index}" for index in range(1, len(numbers) + 1)]
    for group in groups:
        numbers = [source.number for source in sources if source.group == group["id"] and source.scope == "repo"]
        assert numbers == sorted(numbers, key=lambda number: tuple(map(int, number.split("."))))
    numbered = json.loads((repo_root() / ".agents/references/project/workflow_catalog.json").read_text(encoding="utf-8"))["source_numbers"]
    for group in groups:
        indexes = sorted(int(number.rsplit(".", 1)[1]) for number in numbered.values() if number.rsplit(".", 1)[0] == group["number"])
        assert indexes == list(range(1, len(indexes) + 1)), group["id"]
    inventory = reader.inventory()
    assert not inventory["references"]
    assert not [issue for issue in inventory["issues"] if issue["kind"] != "missing"]


def test_formats_and_adaptations_pass_through_the_catalog(tmp_path: Path) -> None:
    setup_catalog(tmp_path, [
        {"path": "acts.md", "group": "agents"},
        {"path": "film.md", "group": "agents", "formats": ["film"], "adapts": [{"source": "acts.md", "section": "节点位置"}]},
    ])
    path = tmp_path / CATALOG_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    data["formats"] = [{"id": "film", "title": "电影"}]
    path.write_text(json.dumps(data), encoding="utf-8")
    read = GlobalWorkflowQuery(GlobalWorkflowReader(tmp_path)).read()
    assert read.formats == [{"id": "film", "title": "电影"}]
    sources = {source["path"]: source for source in read.sources}
    assert sources["acts.md"]["formats"] == () and sources["acts.md"]["adapts"] == ()
    assert sources["film.md"]["formats"] == ("film",)
    assert sources["film.md"]["adapts"] == ({"source_id": "repo:acts.md", "section": "节点位置"},)


def test_repository_story_sources_split_shared_principles_from_formats(tmp_path: Path) -> None:
    _, sources = GlobalWorkflowReader(repo_root(), tmp_path / "no-user-config").catalog()
    story = [source for source in sources if source.group == "story"]
    assert story and all(source.status == "available" for source in story)
    formats = {source.title: source.formats for source in story if source.formats}
    assert formats == {"电影": ("film",), "连续剧": ("series",)}
    shared = {source.id for source in story if not source.formats}
    assert all(entry["source_id"] in shared for source in story for entry in source.adapts)
