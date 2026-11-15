from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run_tool(root: Path, name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "tools" / name), *args],
        cwd=root, capture_output=True, text=True, encoding="utf-8", check=False,
    )


@pytest.fixture
def skill_repo(tmp_path: Path) -> Path:
    (tmp_path / "tools").mkdir()
    shutil.copyfile(REPO / "tools" / "check_agent_skills.py", tmp_path / "tools" / "check_agent_skills.py")
    source = tmp_path / ".agents" / "skills" / "ai-videos-test"
    source.mkdir(parents=True)
    (source / "SKILL.md").write_text(
        "---\nname: ai-videos-test\ndescription: 中文工作流\n---\n\n正文直接由 Kimi 发现。\n",
        encoding="utf-8",
    )
    return tmp_path


def test_skill_check_accepts_shared_source_without_writing(skill_repo: Path) -> None:
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    before = source.stat().st_mtime_ns
    result = run_tool(skill_repo, "check_agent_skills.py")
    assert result.returncode == 0 and "1 shared Kimi / Codex skills checked" in result.stdout
    assert source.stat().st_mtime_ns == before
    assert not (skill_repo / ".claude").exists()
    assert not (skill_repo / ".agents" / "skill-aliases.json").exists()


@pytest.mark.parametrize("frontmatter,error", [
    ("name: wrong\ndescription: 中文工作流", "skill name"),
    ("name: ai-videos-test\ndescription: ''", "description"),
    ("name: ai-videos-test\ndescription: 中文工作流\nmetadata:\n  claude:\n    argument-hint: x", "legacy Claude metadata"),
    ("name: ai-videos-test\ndescription: 中文工作流\ntype: unknown", "unsupported Kimi skill type"),
])
def test_skill_check_rejects_invalid_frontmatter(skill_repo: Path, frontmatter: str, error: str) -> None:
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    source.write_text(f"---\n{frontmatter}\n---\n\n正文。\n", encoding="utf-8")
    result = run_tool(skill_repo, "check_agent_skills.py")
    assert result.returncode == 1 and error in result.stdout


def test_skill_check_requires_frontmatter(skill_repo: Path) -> None:
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    source.write_text("没有 frontmatter\n", encoding="utf-8")
    result = run_tool(skill_repo, "check_agent_skills.py")
    assert result.returncode == 1 and "missing frontmatter" in result.stdout


def test_kimi_mcp_and_hook_plugin_are_valid() -> None:
    mcp = json.loads((REPO / ".kimi-code" / "mcp.json").read_text(encoding="utf-8"))
    assert {"codegraph", "suno-browser"} <= set(mcp["mcpServers"])
    manifest = json.loads((REPO / ".kimi-code" / "plugin" / "kimi.plugin.json").read_text(encoding="utf-8"))
    hooks = manifest["hooks"]
    assert {hook["event"] for hook in hooks} == {"UserPromptSubmit", "Stop"}
    assert all(set(hook) <= {"event", "matcher", "command", "timeout"} for hook in hooks)
    assert all(hook["command"].startswith("python ./hooks/repo_hook.py ") for hook in hooks)


def test_shared_mcp_matches_both_runtime_configs() -> None:
    shared = json.loads((REPO / ".agents/mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    kimi = json.loads((REPO / ".kimi-code/mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    codex = tomllib.loads((REPO / ".codex/config.toml").read_text(encoding="utf-8"))["mcp_servers"]
    assert shared == kimi == codex
    assert not (REPO / "CLAUDE.md").exists()
    assert not (REPO / ".claude/settings.json").exists()


def test_config_sync_detects_drift_and_rejects_unknown_fields(tmp_path: Path) -> None:
    from tools.sync_agent_config import render

    (tmp_path / ".agents").mkdir()
    source = tmp_path / ".agents/mcp.json"
    source.write_text(json.dumps({"mcpServers": {"demo": {"command": "python", "args": ["中文", r"C:\a\b"], "env": {"MODE": "local"}}}}), encoding="utf-8")
    result = render(tmp_path)
    assert tomllib.loads(result[".codex/config.toml"])["mcp_servers"] == json.loads(result[".kimi-code/mcp.json"])["mcpServers"]
    (tmp_path / "tools").mkdir()
    shutil.copyfile(REPO / "tools/sync_agent_config.py", tmp_path / "tools/sync_agent_config.py")
    assert run_tool(tmp_path, "sync_agent_config.py", "--check").returncode == 1
    assert run_tool(tmp_path, "sync_agent_config.py", "--fix").returncode == 0
    assert run_tool(tmp_path, "sync_agent_config.py", "--check").returncode == 0
    (tmp_path / ".codex/config.toml").write_text('model="drift"', encoding="utf-8")
    assert run_tool(tmp_path, "sync_agent_config.py", "--check").returncode == 1
    source.write_text('{"mcpServers":{"demo":{"command":"python","unknown":true}}}', encoding="utf-8")
    with pytest.raises(ValueError, match="未知字段"):
        render(tmp_path)


def test_triage_hook_uses_kimi_payload_and_ignores_unrelated_repos(tmp_path: Path) -> None:
    for name in ("AGENTS.md", "CONVENTIONS.md"):
        (tmp_path / name).write_text("rules", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "specs" / "development" / "demo").mkdir(parents=True)
    script = REPO / ".kimi-code" / "plugin" / "hooks" / "repo_hook.py"
    payload = {"cwd": str(tmp_path), "prompt": "Continue spec-driven demo", "session_id": "s1"}
    result = subprocess.run(
        [sys.executable, str(script), "triage"], input=json.dumps(payload),
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "followup.py new" in output["hookSpecificOutput"]["additionalContext"]
    payload["prompt"] = "hello"
    quiet = subprocess.run(
        [sys.executable, str(script), "triage"], input=json.dumps(payload),
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert quiet.returncode == 0 and quiet.stdout == ""
    payload["cwd"] = str(tmp_path / "tools")
    assert subprocess.run(
        [sys.executable, str(script), "triage"], input=json.dumps(payload),
        capture_output=True, text=True, encoding="utf-8", check=False,
    ).returncode == 0
