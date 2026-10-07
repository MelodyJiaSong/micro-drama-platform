"""手工服务调用也必须带归属并记录；当前支持 Dreamina CLI。"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.service_request import RequestLog


class ServiceCall:
    def run(self) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--target", required=True, type=Path)
        parser.add_argument("command", nargs=argparse.REMAINDER)
        args = parser.parse_args()
        command = args.command
        if command and command[0] == "--":
            command = command[1:]
        if len(command) < 2 or Path(command[0]).name.lower() not in {"dreamina", "dreamina.exe"}:
            parser.error("命令应为 dreamina <子命令>；Cascadeur 使用 casc_run.py --target")
        if command[0] in {"dreamina", "dreamina.exe"} and not shutil.which(command[0]):
            command[0] = str(Path.home() / "bin" / "dreamina.exe")
        result = RequestLog(args.target).cli(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(result.stdout or "", end="")
        print(result.stderr or "", end="", file=sys.stderr)
        return result.returncode


if __name__ == "__main__":
    raise SystemExit(ServiceCall().run())
