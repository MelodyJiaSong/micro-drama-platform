from __future__ import annotations

import json
import subprocess

import pytest

import libs.infrastructure.clients.claudecli__client as mod
from libs.infrastructure.clients.claudecli__client import ClaudeCliClient, extract_json_object
from libs.infrastructure.errors.claudecli__error import ClaudeCliError


def _ok_envelope(result: str = "ok") -> str:
    return json.dumps({"result": result, "is_error": False})


class _Recorder:
    def __init__(self, stdout: str = _ok_envelope(), returncode: int = 0) -> None:
        self.stdout = stdout
        self.returncode = returncode
        self.calls: list[dict] = []

    def __call__(self, args, **kwargs):
        self.calls.append({"args": args, **kwargs})
        return subprocess.CompletedProcess(args, self.returncode, stdout=self.stdout, stderr="")


def test_run_text_pipes_prompt_and_parses_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    rec = _Recorder(stdout=_ok_envelope("生成结果"))
    monkeypatch.setattr(mod.shutil, "which", lambda b: "C:/tools/claude.EXE")
    monkeypatch.setattr(mod.subprocess, "run", rec)
    out = ClaudeCliClient(model="sonnet").run_text("写一段小说")
    assert out == "生成结果"
    call = rec.calls[0]
    assert call["input"] == "写一段小说"
    assert call["args"][:2] == ["C:/tools/claude.EXE", "-p"]
    assert ["--output-format", "json"] == call["args"][2:4]
    assert "--model" in call["args"] and "sonnet" in call["args"]
    assert "--allowedTools" not in call["args"]


def test_cmd_shim_is_invoked_through_cmd_slash_c(monkeypatch: pytest.MonkeyPatch) -> None:
    rec = _Recorder()
    monkeypatch.setattr(mod.shutil, "which", lambda b: "C:/npm/claude.CMD")
    monkeypatch.setattr(mod.subprocess, "run", rec)
    ClaudeCliClient().run_text("hi")
    assert rec.calls[0]["args"][:3] == ["cmd", "/c", "C:/npm/claude.CMD"]


def test_read_dirs_enable_read_tool_and_add_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    rec = _Recorder()
    monkeypatch.setattr(mod.shutil, "which", lambda b: "C:/tools/claude.exe")
    monkeypatch.setattr(mod.subprocess, "run", rec)
    ClaudeCliClient().run_text("看帧", read_dirs=("C:/ws/frames",), max_turns=40)
    args = rec.calls[0]["args"]
    assert args[args.index("--allowedTools") + 1] == "Read"
    assert args[args.index("--add-dir") + 1] == "C:/ws/frames"
    assert args[args.index("--max-turns") + 1] == "40"


def test_missing_binary_is_unavailable_and_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mod.shutil, "which", lambda b: None)
    cli = ClaudeCliClient()
    assert cli.available is False
    with pytest.raises(ClaudeCliError, match="not found"):
        cli.run_text("hi")


def test_nonzero_exit_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mod.shutil, "which", lambda b: "claude.exe")
    monkeypatch.setattr(mod.subprocess, "run", _Recorder(stdout="boom", returncode=3))
    with pytest.raises(ClaudeCliError, match="exited 3"):
        ClaudeCliClient().run_text("hi")


def test_error_envelope_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mod.shutil, "which", lambda b: "claude.exe")
    monkeypatch.setattr(mod.subprocess, "run",
                        _Recorder(stdout=json.dumps({"result": "credit exhausted", "is_error": True})))
    with pytest.raises(ClaudeCliError, match="reported an error"):
        ClaudeCliClient().run_text("hi")


def test_timeout_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="claude", timeout=1)

    monkeypatch.setattr(mod.shutil, "which", lambda b: "claude.exe")
    monkeypatch.setattr(mod.subprocess, "run", _boom)
    with pytest.raises(ClaudeCliError, match="timed out"):
        ClaudeCliClient(timeout_s=1).run_text("hi")


def test_extract_json_object_strips_fences_and_prose() -> None:
    text = "看完了帧，结论如下：\n```json\n{\"narrative\": \"复仇\", \"beats\": []}\n```\n以上。"
    assert extract_json_object(text)["narrative"] == "复仇"


def test_extract_json_object_rejects_no_json() -> None:
    with pytest.raises(ClaudeCliError, match="no JSON object"):
        extract_json_object("全是散文没有对象")
