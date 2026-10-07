from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def run_tool(root: Path, name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "tools" / name), *args],
        cwd=root, capture_output=True, text=True, encoding="utf-8", check=False,
    )


def copy_tool(root: Path, name: str) -> None:
    (root / "tools").mkdir(exist_ok=True)
    shutil.copyfile(REPO / "tools" / name, root / "tools" / name)


@pytest.fixture
def skill_repo(tmp_path: Path) -> Path:
    copy_tool(tmp_path, "sync_agent_skills.py")
    source = tmp_path / ".agents" / "skills" / "ai-videos-test"
    source.mkdir(parents=True)
    (source / "SKILL.md").write_text(
        "---\nname: ai-videos-test\ndescription: 中文工作流\n---\n\n正文不应复制到入口。\n",
        encoding="utf-8",
    )
    (tmp_path / ".agents" / "skill-aliases.json").write_text(
        json.dumps({"ai-videos-test": "ai_videos__测试"}, ensure_ascii=False), encoding="utf-8",
    )
    return tmp_path


def test_skill_check_is_read_only_and_sync_is_idempotent(skill_repo: Path) -> None:
    check = run_tool(skill_repo, "sync_agent_skills.py", "--check")
    assert check.returncode == 1
    assert not (skill_repo / ".claude").exists()
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    entry = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    assert "中文工作流" in text and "正文不应复制" in text
    claude_entry = skill_repo / ".claude" / "skills" / "ai-videos-test" / "SKILL.md"
    claude_text = claude_entry.read_text(encoding="utf-8")
    assert "name: ai-videos-test" in claude_text
    assert "$ARGUMENTS" in claude_text and "$ARGUMENTS" not in text
    assert "正文不应复制" not in claude_text
    link = "../../../.agents/skills/ai-videos-test/SKILL.md"
    assert (claude_entry.parent / link).resolve().is_file()
    legacy_entry = skill_repo / ".claude" / "skills" / "ai_videos__测试" / "SKILL.md"
    assert (legacy_entry.parent / link).resolve() == entry
    assert "正文不应复制" not in legacy_entry.read_text(encoding="utf-8")
    before = entry.stat().st_mtime_ns
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    assert entry.stat().st_mtime_ns == before
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 0


def test_skill_source_metadata_drift_is_detected(skill_repo: Path) -> None:
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    source.write_text(source.read_text(encoding="utf-8").replace("中文工作流", "更新后的工作流"), encoding="utf-8")
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 1
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 0


def test_skill_sync_preserves_handwritten_entry(skill_repo: Path) -> None:
    entry = skill_repo / ".claude" / "skills" / "ai_videos__测试" / "SKILL.md"
    entry.parent.mkdir(parents=True)
    entry.write_text("user-owned skill", encoding="utf-8")
    result = run_tool(skill_repo, "sync_agent_skills.py")
    assert result.returncode == 1
    assert "refusing to overwrite" in result.stdout
    assert entry.read_text(encoding="utf-8") == "user-owned skill"


def test_claude_entry_drift_and_arguments_are_checked(skill_repo: Path) -> None:
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    source.write_text(
        source.read_text(encoding="utf-8").replace("description:", 'metadata:\n  claude:\n    argument-hint: "<剧名> <ep>"\ndescription:'),
        encoding="utf-8",
    )
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    entry = skill_repo / ".claude" / "skills" / "ai-videos-test" / "SKILL.md"
    content = entry.read_text(encoding="utf-8")
    assert 'argument-hint: "<剧名> <ep>"' in content
    entry.write_text(content + "manual drift\n", encoding="utf-8")
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 1
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 0


def test_skill_sync_preserves_handwritten_claude_alias(skill_repo: Path) -> None:
    entry = skill_repo / ".claude" / "skills" / "ai-videos-test" / "SKILL.md"
    entry.parent.mkdir(parents=True)
    entry.write_text("user-owned Claude entry", encoding="utf-8")
    result = run_tool(skill_repo, "sync_agent_skills.py")
    assert result.returncode != 0
    assert entry.read_text(encoding="utf-8") == "user-owned Claude entry"
    assert not (skill_repo / ".claude" / "skills" / "ai_videos__测试").exists()


@pytest.mark.parametrize("aliases", [
    '{"ai-videos-test": "ai_videos__测试", "ai-videos-test": "ai_videos__测试"}',
    '{"ai-videos-test": "../../outside"}',
    '{"missing": "ai_videos__测试"}',
])
def test_skill_sync_rejects_invalid_aliases_before_writing(skill_repo: Path, aliases: str) -> None:
    (skill_repo / ".agents" / "skill-aliases.json").write_text(aliases, encoding="utf-8")
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode != 0
    assert not (skill_repo / ".claude").exists()


def test_sync_never_writes_canonical_body(skill_repo: Path) -> None:
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    source = skill_repo / ".agents" / "skills" / "ai-videos-test" / "SKILL.md"
    updated = source.read_text(encoding="utf-8") + "共享流程的新步骤。\n"
    source.write_text(updated, encoding="utf-8")
    before = source.stat().st_mtime_ns
    assert run_tool(skill_repo, "sync_agent_skills.py", "--check").returncode == 0
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    assert source.read_text(encoding="utf-8") == updated and source.stat().st_mtime_ns == before
    for path in (skill_repo / ".claude" / "skills").glob("*/SKILL.md"):
        assert "共享流程的新步骤" not in path.read_text(encoding="utf-8")


def test_obsolete_adapter_fails_without_deleting_or_partial_sync(skill_repo: Path) -> None:
    assert run_tool(skill_repo, "sync_agent_skills.py").returncode == 0
    entry = skill_repo / ".claude" / "skills" / "ai-videos-test" / "SKILL.md"
    content = entry.read_text(encoding="utf-8")
    obsolete = entry.parent.parent / "old-entry" / "SKILL.md"
    obsolete.parent.mkdir()
    obsolete.write_text(content, encoding="utf-8")
    entry.unlink()
    result = run_tool(skill_repo, "sync_agent_skills.py")
    assert result.returncode == 1 and "obsolete generated entry" in result.stdout
    assert obsolete.read_text(encoding="utf-8") == content and not entry.exists()


def test_unmapped_claude_body_is_reported_and_preserved(skill_repo: Path) -> None:
    entry = skill_repo / ".claude" / "skills" / "private-workflow" / "SKILL.md"
    entry.parent.mkdir(parents=True)
    entry.write_text("a separate handwritten workflow", encoding="utf-8")
    result = run_tool(skill_repo, "sync_agent_skills.py")
    assert result.returncode == 1 and "unmapped Claude skill" in result.stdout
    assert entry.read_text(encoding="utf-8") == "a separate handwritten workflow"
    assert not (entry.parent.parent / "ai-videos-test").exists()


@pytest.fixture
def shot_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    copy_tool(tmp_path, "seedance_kit.py")
    drama = tmp_path / "ai_videos" / "test_drama"
    shot = drama / "5_6_分镜与prompt" / "episodes" / "ep01" / "shots" / "shot01" / "shot01.md"
    shot.parent.mkdir(parents=True)
    (drama / "seedance.toml").write_text('entity_prefix = "test"\n', encoding="utf-8")
    shot.write_text(
        "## Reference uploads\n- 图 → [`ref.png`](ref.png)\n\n"
        "## Seedance prompt\n```text\n参考: `图(立绘)=>@`\n画面: 测试\n比例: 16:9\n```\n",
        encoding="utf-8",
    )
    ref = shot.parent / "ref.png"
    ref.write_bytes(b"isolated reference asset")
    return tmp_path, shot, ref


def test_seedance_sync_reports_failure_and_recovers(shot_repo: tuple[Path, Path, Path]) -> None:
    root, shot, ref = shot_repo
    ref.unlink()
    failed = run_tool(root, "seedance_kit.py", "sync", str(shot))
    assert failed.returncode == 1
    assert "修复后 1 个仍未对齐，1 个构建失败" in failed.stdout
    kit = shot.parent / "资料包"
    assert json.loads((kit / "kit.json").read_text(encoding="utf-8"))["version"] == -1
    ref.write_bytes(b"restored asset")
    fixed = run_tool(root, "seedance_kit.py", "sync", str(shot))
    assert fixed.returncode == 0
    assert "修复后 0 个仍未对齐，0 个构建失败" in fixed.stdout
    assert run_tool(root, "seedance_kit.py", "check", str(shot)).returncode == 0
    assert "=>@图片1" in (kit / "prompt.txt").read_text(encoding="utf-8")


def test_seedance_quiet_sync_cannot_hide_missing_reference(shot_repo: tuple[Path, Path, Path]) -> None:
    root, shot, ref = shot_repo
    assert run_tool(root, "seedance_kit.py", "sync", str(shot)).returncode == 0
    ref.unlink()
    failed = run_tool(root, "seedance_kit.py", "sync", "--all", "--quiet")
    assert failed.returncode == 1 and "资料包暂不可用" in failed.stdout
    kit = shot.parent / "资料包"
    assert not list(kit.glob("*.png"))
    assert run_tool(root, "seedance_kit.py", "check", str(shot)).returncode == 1
