"""Scriptable stand-in for the official `dreamina` CLI (tests only; never spends credits).

Scenario JSON (path in env FAKE_DREAMINA_SCENARIO):
  {"ledger": "<path>", "commands": {"<subcommand>": {"stdout": "...", "stderr": "...", "exit": 0,
   "sleep_s": 0, "create_files": ["name.png", ...]}}}
Every invocation appends {"argv": [...], "env_keys": [...]} to the ledger. `create_files` are
written into the directory given by `--download_dir=`.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def main() -> int:
    scenario = json.loads(Path(os.environ["FAKE_DREAMINA_SCENARIO"]).read_text(encoding="utf-8"))
    argv = sys.argv[1:]
    with Path(scenario["ledger"]).open("a", encoding="utf-8") as ledger:
        ledger.write(json.dumps({"argv": argv, "env_keys": sorted(os.environ)}, ensure_ascii=False) + "\n")
    command = scenario["commands"].get(argv[0] if argv else "", {"stderr": "unknown command", "exit": 2})
    time.sleep(float(command.get("sleep_s", 0)))
    download_dir = next((arg.split("=", 1)[1] for arg in argv if arg.startswith("--download_dir=")), None)
    if download_dir is not None:
        for name in command.get("create_files", []):
            target = Path(download_dir) / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"\x89PNG\r\n\x1a\nfake")
    sys.stdout.buffer.write(command.get("stdout", "").encode("utf-8"))
    sys.stderr.buffer.write(command.get("stderr", "").encode("utf-8"))
    return int(command.get("exit", 0))


if __name__ == "__main__":
    sys.exit(main())
