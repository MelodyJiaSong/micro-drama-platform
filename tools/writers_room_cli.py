#!/usr/bin/env python3
"""隔离的 Claude CLI 编剧/审稿调用；不加载项目规则、工具或旧会话。

python tools/writers_room_cli.py --prompt <utf8.md> --schema <json> --out <audit.json>
产物先写审计，不能直接变成已接受故事记忆或审稿章。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def call(prompt: str, schema: dict, output: Path, model: str = "sonnet", timeout: int = 900) -> dict:
    executable = shutil.which("claude")
    if executable is None:
        raise RuntimeError("未找到已登录的 claude CLI。")
    output.parent.mkdir(parents=True, exist_ok=True)
    request_hash = hashlib.sha256((prompt + json.dumps(schema, sort_keys=True) + model).encode()).hexdigest()
    if output.exists():
        saved = json.loads(output.read_text(encoding="utf-8"))
        if saved.get("request_hash") == request_hash and saved.get("exit_code") == 0 and saved["response"].get("structured_output") is not None:
            return saved["response"]["structured_output"]
        raise RuntimeError("审计输出已存在且输入不同/失败；请使用新的轮次文件名，不覆盖旧调用。")
    budget_dir = output.parent / "call_reservations"
    budget_dir.mkdir(exist_ok=True)
    # O_EXCL 的逐号预留跨进程生效；异常/超时也占次数，不因续跑清零。
    slot: Path | None = None
    # CLI 的 schema 收口也可能占一个内部轮次。按每请求4轮保守预留，
    # 100轮预算至多启动25个CLI请求；不能把一次CLI进程称一次模型推理。
    for index in range(1, 26):
        candidate = budget_dir / f"{index:03d}.json"
        try:
            fd = os.open(candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as reservation:
            json.dump({"request_hash": request_hash, "output": output.name, "model": model, "status": "reserved", "reserved_internal_turns": 4}, reservation)
        slot = candidate
        break
    if slot is None:
        raise RuntimeError("本轮100个内部轮次保守预算已耗尽（最多25次CLI请求），未调用模型。")
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="writers-room-isolated-") as cwd:
        command = [executable, "-p", "--output-format", "json", "--json-schema", json.dumps(schema, ensure_ascii=False), "--max-turns", "2", "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands", "--no-session-persistence", "--safe-mode", "--setting-sources", "", "--model", model, "--effort", "medium"]
        env = dict(os.environ)
        env.pop("CLAUDECODE", None)
        try:
            result = subprocess.run(command, input=prompt, text=True, encoding="utf-8", errors="replace", capture_output=True, cwd=cwd, env=env, timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        except subprocess.TimeoutExpired:
            output.write_text(json.dumps({"request_hash": request_hash, "exit_code": -1, "response": {"is_error": True, "error": "CLI timeout"}, "elapsed_s": timeout}, ensure_ascii=False, indent=2), encoding="utf-8")
            raise RuntimeError(f"CLI超时，调用已计入预算，未接受任何产物：{output}") from None
    try:
        body = json.loads(result.stdout)
    except json.JSONDecodeError:
        body = {"unparsed_output": result.stdout, "is_error": True}
    record = {"request_hash": request_hash, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "engine": "claude_cli", "model": model, "elapsed_s": round(time.monotonic()-started, 2), "exit_code": result.returncode, "response": body, "stderr": result.stderr}
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    if result.returncode or body.get("is_error"):
        raise RuntimeError(f"CLI 调用未成功，见 {output}。")
    if body.get("structured_output") is None:
        raise RuntimeError(f"CLI 未返回结构化产物，不能拿普通聊天文本假装契约通过：{output}。")
    return body["structured_output"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default="sonnet")
    args = parser.parse_args()
    call(args.prompt.read_text(encoding="utf-8"), json.loads(args.schema.read_text(encoding="utf-8")), args.out, args.model)


if __name__ == "__main__":
    main()
