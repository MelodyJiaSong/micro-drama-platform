"""Run Python inside the live Cascadeur via its in-app MCP script server.

    python casc_run.py path/to/script.py      # run a file
    python casc_run.py -c "print(1+1)"         # run inline code

Prints ok/value, then every event-log message the script produced (print() lands there),
then the traceback on failure. Exit code 1 on failure.
"""
from __future__ import annotations

import json
import sys
import urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

URL = "http://127.0.0.1:8765/run"


def run(code: str, timeout: float = 120.0) -> dict:
    req = urllib.request.Request(
        URL, data=json.dumps({"code": code}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "-c":
        code = sys.argv[2]
    elif len(sys.argv) >= 2:
        code = open(sys.argv[1], encoding="utf-8").read()
    else:
        print(__doc__)
        return 2
    res = run(code)
    print(f"ok={res.get('ok')} value={res.get('value')!r}")
    for m in res.get("messages", []):
        print(f"[{m.get('level')}] {m.get('text')}")
    if not res.get("ok"):
        print("ERROR:\n" + str(res.get("error")))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
