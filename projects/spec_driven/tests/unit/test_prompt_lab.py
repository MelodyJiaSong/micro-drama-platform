from __future__ import annotations

import shutil
from typing import Iterator

import pytest

from libs.common.repo_root import RepoRoot

_TEST_CATEGORY = "__zz_prompt_lab_test__"
_FLOW = "prompt_lab/generative_art/flow_field_art/prompt.md"


@pytest.fixture()
def temp_category(repo_root: RepoRoot) -> Iterator[str]:
    yield _TEST_CATEGORY
    d = repo_root.path / "prompt_lab" / _TEST_CATEGORY
    if d.exists():
        shutil.rmtree(d, ignore_errors=True)


def test_overview_lists_categories_and_parses_entries(client):
    r = client.get("/api/prompt-lab")
    assert r.status_code == 200
    cats = {c["name"]: c for c in r.json()["categories"]}
    assert "generative_art" in cats
    assert "classic_games" in cats  # new category
    entry = next(e for e in cats["generative_art"]["entries"] if e["name"] == "flow_field_art")
    assert entry["title"].startswith("Flow Field Art")
    assert entry["path"] == _FLOW
    assert entry["source"]["url"].startswith("http")
    assert entry["expected"]["url"].startswith("http")
    assert "PHASE 1" in entry["prompt"]
    assert "run_state" in entry  # null until executed


def test_read_prompt_via_generic_file_api(client):
    r = client.get(f"/api/file?path={_FLOW}")
    assert r.status_code == 200
    assert "COPY-PASTE PROMPT" in r.json()["content"]


def test_create_then_delete_roundtrip(client, good_headers, temp_category):
    create = client.post(
        "/api/prompt-lab/file",
        json={"category": temp_category, "filename": "demo.md", "content": "# Demo\n"},
        headers=good_headers,
    )
    assert create.status_code == 200
    rel = create.json()["path"]
    assert rel == f"prompt_lab/{temp_category}/demo/prompt.md"

    overview = client.get("/api/prompt-lab").json()
    assert temp_category in {c["name"] for c in overview["categories"]}

    dup = client.post(
        "/api/prompt-lab/file",
        json={"category": temp_category, "filename": "demo.md", "content": "x"},
        headers=good_headers,
    )
    assert dup.status_code == 409

    delete = client.request("DELETE", "/api/prompt-lab/file", json={"path": rel}, headers=good_headers)
    assert delete.status_code == 200
    assert delete.json() == {"path": f"prompt_lab/{temp_category}/demo", "deleted": True}


def test_delete_missing_is_404(client, good_headers):
    r = client.request(
        "DELETE", "/api/prompt-lab/file",
        json={"path": "prompt_lab/generative_art/does_not_exist/prompt.md"},
        headers=good_headers,
    )
    assert r.status_code == 404


def test_delete_outside_prompt_lab_is_rejected(client, good_headers):
    r = client.request(
        "DELETE", "/api/prompt-lab/file",
        json={"path": "specs/development/spec_driven/final_specs/spec.md"},
        headers=good_headers,
    )
    assert r.status_code == 400


def test_create_rejects_bad_slug(client, good_headers):
    r = client.post(
        "/api/prompt-lab/file",
        json={"category": "../evil", "filename": "x.md", "content": "x"},
        headers=good_headers,
    )
    assert r.status_code == 400


def test_create_rejects_non_md(client, good_headers, temp_category):
    r = client.post(
        "/api/prompt-lab/file",
        json={"category": temp_category, "filename": "x.txt", "content": "x"},
        headers=good_headers,
    )
    assert r.status_code == 400


def test_generic_file_delete_still_405(client, good_headers):
    r = client.request("DELETE", "/api/file", json={"path": "prompt_lab/x.md"}, headers=good_headers)
    assert r.status_code == 405


# --- execution endpoints (no real spawn in unit tests) ---

def test_run_status_idle_for_unexecuted_item(client):
    r = client.get(f"/api/prompt-lab/run?path={_FLOW}")
    assert r.status_code == 200
    body = r.json()
    assert body["state"] in {"idle", "succeeded", "failed", "running", "stopped"}
    assert "decisions" in body and isinstance(body["decisions"], list)
    assert "output" in body


def test_execute_rejects_path_outside_prompt_lab(client, good_headers):
    r = client.post(
        "/api/prompt-lab/execute",
        json={"path": "specs/development/spec_driven/final_specs/spec.md"},
        headers=good_headers,
    )
    assert r.status_code == 400


def test_execute_not_found(client, good_headers):
    r = client.post(
        "/api/prompt-lab/execute",
        json={"path": "prompt_lab/generative_art/nope/prompt.md"},
        headers=good_headers,
    )
    assert r.status_code == 404


@pytest.mark.parametrize("runtime", ["kimi", "codex"])
def test_executor_builds_runtime_prompt_command(tmp_path, monkeypatch, runtime):
    from libs.common.exposed_tree import ExposedTree
    from libs.common.safe_resolve import SafeResolver
    from libs.infrastructure import prompt_lab__executor as executor_module

    item = tmp_path / "prompt_lab" / "generative_art" / "demo"
    item.mkdir(parents=True)
    (item / "prompt.md").write_text("```text\nBuild a tiny page.\n```\n", encoding="utf-8")
    monkeypatch.setenv("PROMPT_LAB_RUNTIME", runtime)
    monkeypatch.setattr(executor_module, "_which_runtime", lambda name: name)
    monkeypatch.setattr(executor_module.threading, "Thread", lambda *args, **kwargs: type("NoThread", (), {"start": lambda self: None})())
    captured = {}

    class FakeProcess:
        pid = 123

        def __init__(self, cmd, **kwargs):
            captured["cmd"] = cmd
            captured["kwargs"] = kwargs

    monkeypatch.setattr(executor_module.subprocess, "Popen", FakeProcess)
    executor = executor_module.PromptLabExecutor(ExposedTree(tmp_path), SafeResolver(tmp_path))
    result = executor.execute("prompt_lab/generative_art/demo/prompt.md")
    assert result["state"] == "running"
    assert result["runtime"] == runtime
    assert executor.status("prompt_lab/generative_art/demo/prompt.md")["runtime"] == runtime
    cmd = captured["cmd"]
    if runtime == "kimi":
        assert cmd[cmd.index("--prompt") + 1].startswith("Read ")
        assert cmd[cmd.index("--output-format") + 1] == "text"
    else:
        assert "exec" in cmd and cmd[-1].startswith("Read ")
        assert cmd[cmd.index("--sandbox") + 1] == "workspace-write"
        assert "--dangerously-bypass-approvals-and-sandbox" not in cmd
    assert "bypassPermissions" not in cmd
    assert captured["kwargs"]["stdin"] is executor_module.subprocess.DEVNULL
    captured["kwargs"]["stdout"].close()


@pytest.mark.parametrize("runtime", ["claude", "unknown"])
def test_executor_rejects_unsupported_runtime_before_spawning(tmp_path, monkeypatch, runtime):
    from libs.common.exposed_tree import ExposedTree
    from libs.common.safe_resolve import SafeResolver
    from libs.domain.prompt_lab__error import PromptLabExecUnavailable
    from libs.infrastructure.prompt_lab__executor import PromptLabExecutor

    item = tmp_path / "prompt_lab/generative_art/demo"
    item.mkdir(parents=True)
    (item / "prompt.md").write_text("```text\nBuild a page.\n```", encoding="utf-8")
    monkeypatch.setenv("PROMPT_LAB_RUNTIME", runtime)
    with pytest.raises(PromptLabExecUnavailable):
        PromptLabExecutor(ExposedTree(tmp_path), SafeResolver(tmp_path)).execute("prompt_lab/generative_art/demo/prompt.md")
    assert not (item / "workspace").exists()
