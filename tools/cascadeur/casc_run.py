"""Run Python inside the live Cascadeur via its in-app MCP script server.

    python casc_run.py --target <ai_videos/剧/集目录> path/to/script.py
    python casc_run.py --target <ai_videos/剧/集目录> -c "print(1+1)"

Prints ok/value, then every event-log message the script produced (print() lands there),
then the traceback on failure. Exit code 1 on failure.
"""
from __future__ import annotations

import json
import sys
import urllib.request
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.service_request import RequestLog

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

URL = "http://127.0.0.1:8765/run"


def run(code: str, timeout: float = 120.0, *, target: Path | str | None = None) -> dict:
    target = target or os.environ.get("REQUEST_LOG_TARGET")
    if not target:
        raise ValueError("Cascadeur 调用必须指定 --target 或 REQUEST_LOG_TARGET，以记录剧/集归属")
    return RequestLog(target).invoke("cascadeur", "POST /run",
        {"url": URL, "body": {"code": code}, "timeout_s": timeout, "billing": "本地软件接口；未确认逐次费用"},
        lambda: _run_once(code, timeout))


def _run_once(code: str, timeout: float) -> dict:
    req = urllib.request.Request(
        URL, data=json.dumps({"code": code}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    target = None
    if "--target" in sys.argv:
        index = sys.argv.index("--target")
        target = sys.argv[index + 1]
        del sys.argv[index:index + 2]
    if len(sys.argv) >= 3 and sys.argv[1] == "-c":
        code = sys.argv[2]
    elif len(sys.argv) >= 2:
        code = open(sys.argv[1], encoding="utf-8").read()
    else:
        print(__doc__)
        return 2
    res = run(code, target=target)
    print(f"ok={res.get('ok')} value={res.get('value')!r}")
    for m in res.get("messages", []):
        print(f"[{m.get('level')}] {m.get('text')}")
    if not res.get("ok"):
        print("ERROR:\n" + str(res.get("error")))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
