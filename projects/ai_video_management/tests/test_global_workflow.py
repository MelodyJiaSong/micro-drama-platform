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
from libs.common.global_workflow import global_source_id
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.global_workflow__reader import GlobalWorkflowReader
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
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


def test_cross_drama_paths_are_classified_and_private_files_are_never_registered(tmp_path: Path) -> None:
    episode = "ai_videos/demo/episodes/ep01"
    assert global_source_id("shared/new-rule.md", episode=episode) == "repo:shared/new-rule.md"
    assert global_source_id("ai_videos/demo/world.md", episode=episode) is None
    assert global_source_id("specs/ai_video/demo/rules.md", episode=episode) is None
    assert global_source_id(".audit/run/input.json", episode=episode) is None
    setup_catalog(tmp_path, [{"path": path, "group": "agents"} for path in [".codex/auth.json", ".claude/.credentials.json", ".claude/memory/private.md", ".env"]])
    reader = GlobalWorkflowReader(tmp_path)
    assert all(entry.status == "unavailable" for entry in reader.catalog()[1])


def test_registered_configs_only_and_fail_closed_for_malformed_or_oversized_files(tmp_path: Path) -> None:
    user = tmp_path / "user"
    (user / ".codex").mkdir(parents=True)
    (user / ".codex/config.toml").write_text('model="model-a"\napi_key="NEVER_SEND"', encoding="utf-8")
    setup_catalog(tmp_path, [{"path": ".codex/config.toml", "group": "agents", "scope": "user"}])
    reader = GlobalWorkflowReader(tmp_path, user)
    query = GlobalWorkflowQuery(reader, StoryRunsReader(tmp_path))
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


def test_real_wow_two_runs_have_all_six_global_bindings_and_keep_frozen_bytes(tmp_path: Path) -> None:
    actual = repo_root()
    shutil.copytree(actual / ".agents", tmp_path / ".agents")
    ep = "ai_videos/shengji_zhilu/episodes/ep01"
    (tmp_path / ep).mkdir(parents=True)
    shutil.copyfile(actual / ep / "story_runs.json", tmp_path / ep / "story_runs.json")
    shutil.copyfile(actual / "ai_videos/shengji_zhilu/workflow.json", tmp_path / "ai_videos/shengji_zhilu/workflow.json")
    hashes = {}
    for entry in json.loads((tmp_path / ep / "story_runs.json").read_text(encoding="utf-8"))["runs"]:
        for name in ("run.json", "input.json"):
            relative = Path(entry["audit_path"]).parent / name
            target = tmp_path / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(actual / relative, target)
            hashes[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
    runs = StoryRunsReader(tmp_path)
    query = GlobalWorkflowQuery(GlobalWorkflowReader(tmp_path, tmp_path / "empty-user"), runs)
    coverage = query.coverage()
    assert len(coverage["links"]) == 6 and not coverage["gaps"]
    assert all(link["status"] == "available" for link in coverage["links"])
    assert len({link["source_id"] for link in coverage["links"]}) == 3
    for run in runs.read(ep).runs:
        items = runs.describe(run)["items"]
        assert len([item for item in items if item.get("global_source_id")]) == 3
        assert all(item["source_status"]["status"] == "changed" for item in items if item.get("global_source_id"))
    assert all(hashlib.sha256((tmp_path / path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())


def test_unknown_history_sources_are_reported_as_gaps(tmp_path: Path) -> None:
    # Use an actual validated frozen run, then deliberately omit its sources from the current catalog.
    actual = repo_root()
    ep = "ai_videos/shengji_zhilu/episodes/ep01"
    (tmp_path / ep).mkdir(parents=True)
    shutil.copyfile(actual / ep / "story_runs.json", tmp_path / ep / "story_runs.json")
    shutil.copyfile(actual / "ai_videos/shengji_zhilu/workflow.json", tmp_path / "ai_videos/shengji_zhilu/workflow.json")
    for entry in json.loads((tmp_path / ep / "story_runs.json").read_text(encoding="utf-8"))["runs"]:
        target = tmp_path / entry["audit_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(actual / entry["audit_path"], target)
    setup_catalog(tmp_path, [])
    data = GlobalWorkflowQuery(GlobalWorkflowReader(tmp_path), StoryRunsReader(tmp_path)).coverage()
    assert len(data["links"]) == 6 and all(link["status"] == "unregistered" for link in data["links"])


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


def test_series_episode_indexes_are_included_and_library_indexes_are_excluded(tmp_path: Path) -> None:
    series = tmp_path / "ai_videos/series"
    series.mkdir(parents=True)
    (series / "series.json").write_text("{}", encoding="utf-8")
    for relative in ["ai_videos/flat/episodes/ep01", "ai_videos/series/member/episodes/ep02", "ai_videos/series/_series/episodes/ep03", "ai_videos/_deleted/episodes/ep04"]:
        path = tmp_path / relative / "story_runs.json"
        path.parent.mkdir(parents=True)
        path.write_text("{}", encoding="utf-8")
    assert GlobalWorkflowReader(tmp_path).episodes() == ["ai_videos/flat/episodes/ep01", "ai_videos/series/member/episodes/ep02"]


def test_repository_workflow_sources_are_numbered_and_reference_closure_is_registered(tmp_path: Path) -> None:
    reader = GlobalWorkflowReader(repo_root(), tmp_path / "no-user-config")
    groups, sources = reader.catalog()
    group_numbers = {group["id"]: group["number"] for group in groups}
    assert all(source.number.startswith(group_numbers[source.group] + ".") for source in sources)
    inventory = reader.inventory()
    assert not inventory["references"]
    assert not [issue for issue in inventory["issues"] if issue["kind"] != "missing"]
