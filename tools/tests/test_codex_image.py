from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import codex_image  # noqa: E402


def events(path):
    return [json.loads(x) for x in re.findall(r"```json\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex_home"))
    monkeypatch.setattr(codex_image, "codex_executable", lambda: "codex")
    return tmp_path


def fake_run(thread: str, root: Path, log: Path, *, write: bool = True):
    def run(argv, **kwargs):
        first = events(log)[0]
        assert first["event"] == "request"  # 先落盘再调用
        assert first["request"]["prompt"] == "一只橘猫"
        assert kwargs["input"].count("一只橘猫") == 1 and "image_gen" in kwargs["input"]
        assert not (Path(kwargs["cwd"]) / "AGENTS.md").exists()
        if write:
            (root / thread).mkdir(parents=True)
            (root / thread / "exec-1.png").write_bytes(b"png-bytes")
        lines = [{"type": "thread.started", "thread_id": thread},
                 {"type": "item.completed", "item": {"type": "Extension", "kind": "image_gen.generation", "id": "exec-1",
                                                     "status": "completed", "revisedPrompt": "一只橘猫", "result": "QUFB"}},
                 {"type": "turn.completed", "usage": {"input_tokens": 10}}]
        return subprocess.CompletedProcess(argv, 0, "\n".join(json.dumps(x) for x in lines), "")
    return run


def test_logs_before_call_and_copies_thread_image(env, monkeypatch):
    out = env / "ai_videos/demo/characters/c1/front.png"
    ref = env / "ref.png"
    ref.write_bytes(b"ref")
    log = codex_image.RequestLog(out).path
    monkeypatch.setattr(codex_image, "run_codex", fake_run("t-1", codex_image.generated_root(), log))
    result = codex_image.generate(out, "一只橘猫", [ref])
    assert out.read_bytes() == b"png-bytes"
    rows = events(log)
    assert [r["event"] for r in rows] == ["request", "result"]
    assert rows[0]["request"]["files"][0]["sha256"] and "--image" in rows[0]["request"]["argv"]
    assert rows[0]["request"]["sandbox"] == "read-only"
    assert rows[1]["response"]["thread_id"] == "t-1"
    assert rows[1]["response"]["images"][0]["revisedPrompt"] == "一只橘猫"
    assert "QUFB" not in log.read_text(encoding="utf-8")  # 不把 base64 写进日志


def test_no_image_logs_error_and_does_not_retry(env, monkeypatch):
    out = env / "ai_videos/demo/props/p1/view.png"
    log = codex_image.RequestLog(out).path
    calls = []
    run = fake_run("t-2", codex_image.generated_root(), log, write=False)
    monkeypatch.setattr(codex_image, "run_codex", lambda *a, **k: calls.append(1) or run(*a, **k))
    with pytest.raises(RuntimeError):
        codex_image.generate(out, "一只橘猫", [])
    assert len(calls) == 1 and not out.exists()
    assert [r["event"] for r in events(log)] == ["request", "error"]


def test_refuses_existing_output_and_non_png(env):
    out = env / "ai_videos/demo/props/p1/view.png"
    out.parent.mkdir(parents=True)
    out.write_bytes(b"old")
    with pytest.raises(FileExistsError):
        codex_image.generate(out, "x", [])
    with pytest.raises(ValueError):
        codex_image.generate(out.with_suffix(".jpg"), "x", [])
    assert not codex_image.RequestLog(out).path.exists()


@pytest.mark.parametrize("thread_id", ["t-2", None])
def test_does_not_collect_images_from_other_sessions(env, monkeypatch, thread_id):
    out = env / "ai_videos/demo/props/p1/view.png"
    log = codex_image.RequestLog(out).path
    run = fake_run("other-session", codex_image.generated_root(), log)

    def other_run(argv, **kwargs):
        done = run(argv, **kwargs)
        lines = done.stdout.splitlines()
        lines[0] = json.dumps({"type": "thread.started", "thread_id": thread_id})
        done.stdout = "\n".join(lines)
        return done

    monkeypatch.setattr(codex_image, "run_codex", other_run)
    with pytest.raises(RuntimeError):
        codex_image.generate(out, "一只橘猫", [])
    assert not out.exists()
    assert [r["event"] for r in events(log)] == ["request", "error"]


def test_uses_rollout_saved_path_and_records_revised_prompt(env, monkeypatch):
    out = env / "ai_videos/demo/characters/c2/front.png"
    log = codex_image.RequestLog(out).path
    image = codex_image.generated_root() / "t-3" / "exec-9.png"
    def run(argv, **kwargs):
        image.parent.mkdir(parents=True)
        image.write_bytes(b"from-rollout")
        session = codex_image.codex_home() / "sessions/2026/10/11/rollout-x-t-3.jsonl"
        session.parent.mkdir(parents=True)
        item = {"type": "Extension", "kind": "image_gen.generation", "id": "exec-9", "status": "completed",
                "revisedPrompt": "改写后的", "failure": None, "savedPath": str(image), "result": "QUFB"}
        session.write_text(json.dumps({"type": "event_msg", "payload": {"type": "item_completed", "item": item}}), encoding="utf-8")
        stdout = "\n".join(json.dumps(x) for x in [{"type": "thread.started", "thread_id": "t-3"},
                                                    {"type": "error", "message": "transient"}])
        return subprocess.CompletedProcess(argv, 0, stdout, "")
    monkeypatch.setattr(codex_image, "run_codex", run)
    codex_image.generate(out, "一只橘猫", [])
    assert out.read_bytes() == b"from-rollout"
    response = events(log)[1]["response"]
    assert response["images"][0]["revisedPrompt"] == "改写后的"
    assert response["errors"] == [{"message": "transient"}]
    assert "QUFB" not in log.read_text(encoding="utf-8")


def test_timeout_kills_the_whole_process_tree(tmp_path):
    """Windows: killing only the codex.CMD shell left node/codex holding the pipes for 24–40 min (follow-up 263)."""
    import time
    marker = tmp_path / "grandchild.pid"
    child = ("import subprocess, sys, time; "
             "p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)']); "
             f"open({str(marker)!r}, 'w').write(str(p.pid)); time.sleep(120)")
    start = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        codex_image.run_codex([sys.executable, "-c", child], input="", cwd=str(tmp_path), timeout=3)
    assert time.monotonic() - start < 30
    pid = int(marker.read_text())
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and _alive(pid):
        time.sleep(0.2)
    assert not _alive(pid)


def _alive(pid: int) -> bool:
    if sys.platform == "win32":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    import os
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
