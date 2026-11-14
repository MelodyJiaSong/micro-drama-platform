# -*- coding: utf-8 -*-
"""ep05 夜间守候（follow-up 038）：等 Suno 任务 90bd9426 完成 → 官方下载 → 带配乐重渲母版 → 更新发布稿。

不重新提交、不换幂等键；任务 needs_attention 时只记日志退出（是否恢复由人或下一轮会话判断）。
日志：_build/music_watch.log。最长守候 --hours 小时。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
REPO = EP.parents[3]
JOB = "90bd94269002476b9111c4f7c775b7e9"
PY = str(REPO / ".venv" / "Scripts" / "python.exe")
CLI = str(REPO / "projects" / "suno_browser_service" / "apps" / "cli" / "main.py")
LOG = EP / "_build" / "music_watch.log"


def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def cli(*args: str, timeout: int = 120) -> dict:
    r = subprocess.run([PY, CLI, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO, timeout=timeout)
    try:
        d = json.loads(r.stdout)
        return d.get("result", d)
    except json.JSONDecodeError:
        return {"_raw": (r.stdout + r.stderr)[-400:]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=10)
    a = ap.parse_args()
    end = time.time() + a.hours * 3600
    last = None
    while time.time() < end:
        res = cli("wait", "--job", JOB)
        job = res.get("job") if isinstance(res, dict) else None
        st = (job or {}).get("status", "unreachable")
        if st != last:
            log(f"status={st} next={(job or {}).get('next_action')} err={(job or {}).get('error')}")
            last = st
        if st == "completed":
            break
        if st in ("needs_attention", "needs_login", "uncertain", "failed"):
            log("任务需要人处理，守候结束（不自动重提）")
            return
        time.sleep(15)
    else:
        log("守候超时")
        return
    out = EP / "assets" / "music"
    out.mkdir(parents=True, exist_ok=True)
    res = cli("download", "--job", JOB, "--output", str(out), timeout=600)
    files = [f["path"] for f in (res.get("files") or []) if str(f.get("path", "")).lower().endswith((".mp3", ".wav"))]
    log(f"download: {files or res}")
    if not files:
        return
    rs = REPO / "projects" / "rank_scroll"
    cmd = [sys.executable, "-m", "rank_scroll", "render", str(EP), "--music", *files, "--music-fit", "end"]
    log("render: " + " ".join(cmd))
    r = subprocess.run(cmd, cwd=rs, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log(f"render rc={r.returncode} {r.stdout[-300:]} {r.stderr[-300:]}")
    for step in ("publish", "thumb"):
        r = subprocess.run([sys.executable, "-m", "rank_scroll", step, str(EP)], cwd=rs, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log(f"{step} rc={r.returncode}")
    log("完成：带配乐母版已重渲；需要独立音频审片（qc.md 第 6 项）")


if __name__ == "__main__":
    main()
