"""MCP 宿主代为调用的外部服务：两段式请求日志（ai_video_management follow-up 354）。

外部 MCP（例如 Codex 桌面版里的 CapCut 插件）由宿主直接发请求，本仓库拦不到。
代理必须在每次调用前先跑 `request` 落盘、拿到 request_id，调用后再用同一个 id 跑
`result` 或 `error`。日志写不进就不调用。与 `RequestLog.invoke` 同一格式、同一归属规则。

    python tools/mcp_request_log.py request --target <归属路径> --provider capcut \
        --operation capcut_ailab_start_edit --request '{"query": "...", "assets": [...]}' \
        [--file <本地文件> ...]
    python tools/mcp_request_log.py result --target <同上> --provider capcut \
        --operation capcut_ailab_start_edit --request-id <id> --response '{"session_id": "..."}'
    python tools/mcp_request_log.py error  --target <同上> ... --request-id <id> --error "<原样错误>"

`--request` / `--response` 可给 JSON 字符串，或 `@文件路径` 读 JSON 文件。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.service_request import RequestLog
for _stream in (sys.stdout, sys.stderr):    # Windows 非 UTF-8 控制台打印中文会崩（chuanyue_yiri follow-up 043）
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def load_json(value: str | None) -> Any:
    if value is None:
        return None
    if value.startswith("@"):
        return json.loads(Path(value[1:]).read_text(encoding="utf-8"))
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def clock() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="event", required=True)
    for name in ("request", "result", "error"):
        s = sub.add_parser(name)
        s.add_argument("--target", required=True, type=Path, help="归属路径（剧 / 集 / 资产下），决定写进哪份 request_log.md")
        s.add_argument("--provider", required=True)
        s.add_argument("--operation", required=True, help="MCP 工具名")
        if name == "request":
            s.add_argument("--request", required=True, help="完整参数：JSON 或 @文件")
            s.add_argument("--file", action="append", default=[], type=Path, help="随请求上传的本地文件，记路径、大小、SHA256")
        else:
            s.add_argument("--request-id", required=True)
            if name == "result":
                s.add_argument("--response", required=True, help="原样返回：JSON 或 @文件；没有费用字段即未知")
            else:
                s.add_argument("--error", required=True)
    a = p.parse_args(argv)

    log = RequestLog(a.target)
    common = {"provider": a.provider, "operation": a.operation, "target": str(log.target),
              "pid": os.getpid(), "via": "mcp_host"}
    if a.event == "request":
        request = load_json(a.request)
        if a.file:
            missing = [str(f) for f in a.file if not f.is_file()]
            if missing:
                p.error(f"文件不存在：{missing}")
            request = {"params": request, "files": [RequestLog.file(f) for f in a.file]}
        fingerprint = hashlib.sha256(json.dumps(RequestLog.sanitize(request), sort_keys=True,
                                                ensure_ascii=False).encode()).hexdigest()
        rid = uuid.uuid4().hex
        log.append({"request_id": rid, **common, "request_fingerprint": fingerprint,
                    "time": clock(), "event": "request", "request": request})
        print(rid)
        print(f"已记入 {log.path}", file=sys.stderr)
        return 0

    text = log.path.read_text(encoding="utf-8") if log.path.is_file() else ""
    if f'"request_id": "{a.request_id}"' not in text:
        p.error(f"{log.path} 里没有 request_id {a.request_id} 的请求事件；先记请求再调用")
    event: dict[str, Any] = {"request_id": a.request_id, **common, "time": clock(), "event": a.event}
    if a.event == "result":
        event["response"] = load_json(a.response)
    else:
        event["error"] = a.error
    log.append(event)
    print(f"已记入 {log.path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
