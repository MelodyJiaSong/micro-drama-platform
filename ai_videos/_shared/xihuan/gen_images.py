"""按 library.json 为未出图条目调用 tools/codex_image.py（它先写 request_log 再调用 Codex 内置 image_gen）。

已有 PNG 跳过；尝试过但没拿到图的条目记入 qc/gen_attempts.json，默认不再自动重提（结果未知规则），
核实后用 --retry ID 显式重提。

    python ai_videos/_shared/xihuan/gen_images.py --jobs 3 [--only RC01,CL02] [--retry RC01] [--limit 10]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
ATTEMPTS = ROOT / "qc" / "gen_attempts.json"
LOCK = threading.Lock()


def load_attempts() -> dict[str, list[dict[str, str]]]:
    return json.loads(ATTEMPTS.read_text(encoding="utf-8")) if ATTEMPTS.is_file() else {}


def record(aid: str, anchor: str, outcome: str, detail: str) -> None:
    with LOCK:
        data = load_attempts()
        data.setdefault(aid, []).append({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "anchor": anchor, "outcome": outcome, "detail": detail[-600:]})
        ATTEMPTS.parent.mkdir(parents=True, exist_ok=True)
        ATTEMPTS.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def run(asset: dict) -> str:
    img = asset["image"]
    out, prompt = ROOT / img["anchor"], ROOT / img["prompt"]
    cmd = [sys.executable, str(REPO / "tools" / "codex_image.py"), "--out", str(out), "--prompt-file", str(prompt)]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = proc.returncode == 0 and out.is_file()
    record(asset["id"], img["anchor"], "ok" if ok else "no_image", (proc.stdout + proc.stderr).strip())
    msg = f"{asset['id']} {'OK' if ok else 'FAILED'}"
    print(msg, flush=True)
    return msg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--only", default="")
    ap.add_argument("--retry", default="", help="逗号分隔；已核实上次没出图的条目")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    lib = json.loads((ROOT / "library.json").read_text(encoding="utf-8"))
    only = {x for x in args.only.split(",") if x}
    retry = {x for x in args.retry.split(",") if x}
    attempts = load_attempts()
    todo = []
    for a in lib["assets"]:
        img = a["image"]
        if img["status"] == "not_applicable" or (ROOT / img["anchor"]).is_file():
            continue
        if only and a["id"] not in only:
            continue
        last = [t for t in attempts.get(a["id"], []) if t.get("anchor", "entries/" + a["id"].lower() + "/anchor_v1.png") == img["anchor"]]
        if last and last[-1]["outcome"] != "ok" and a["id"] not in retry:
            print(f"{a['id']} 跳过：已有未出图的尝试记录，核实后用 --retry", flush=True)
            continue
        todo.append(a)
    if args.limit:
        todo = todo[: args.limit]
    print(f"待出图 {len(todo)}", flush=True)
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(run, todo))
    print(f"完成 {sum(r.endswith('OK') for r in results)}/{len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
