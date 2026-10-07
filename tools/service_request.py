"""先记录请求再执行；日志不可写时禁止调用外部服务。"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import uuid
import urllib.request
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from projects.ai_video_management.libs.common.production_key import BACKGROUND_DIR_NAME

T = TypeVar("T")
REQUEST_LOG_NAME = "request_log.md"


class RequestLog:
    def __init__(self, target: Path | str) -> None:
        self.target = Path(target).resolve()
        self.path = self.resolve(self.target)

    @staticmethod
    def resolve(target: Path) -> Path:
        parts = target.parts
        if "ai_videos" not in parts:
            raise ValueError("请求缺少剧/集/资产归属；指定 ai_videos 下的目标路径")
        start = parts.index("ai_videos") + 1
        if start >= len(parts):
            raise ValueError("不能把请求记在 ai_videos 根目录")
        for i in range(start, len(parts)):
            if re.fullmatch(r"ep\d+", parts[i]):
                return Path(*parts[:i + 1]) / REQUEST_LOG_NAME
        for i in range(start, len(parts)):
            if parts[i] in {"characters", BACKGROUND_DIR_NAME, "scenes", "props", "equipment", "voices", "music", "skills", "bgm"}:
                return Path(*parts[:i + 1]) / REQUEST_LOG_NAME
        owner = Path(*parts[:start + 1])
        if (owner / "series.json").is_file() and len(parts) > start + 1:
            owner /= parts[start + 1]
        return owner / REQUEST_LOG_NAME

    @classmethod
    def sanitize(cls, value: Any, name: str = "") -> Any:
        if re.search(r"(?:api.?key|authorization|cookie|access.?token|secret|password)", name, re.I):
            return "[REDACTED]"
        if isinstance(value, dict):
            return {str(k): cls.sanitize(v, str(k)) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls.sanitize(v) for v in value]
        if isinstance(value, bytes):
            return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
        if isinstance(value, io.IOBase):
            position = value.tell()
            try:
                value.seek(0)
                h, size = hashlib.sha256(), 0
                while chunk := value.read(1024 * 1024):
                    data = chunk.encode() if isinstance(chunk, str) else chunk
                    h.update(data)
                    size += len(data)
                return {"name": str(getattr(value, "name", "inline")), "bytes": size, "sha256": h.hexdigest()}
            finally:
                value.seek(position)
        if isinstance(value, Path):
            return cls.file(value)
        if isinstance(value, str):
            if name.endswith("base64"):
                return cls.sanitize(base64.b64decode(value))
            value = re.sub(r"(?i)(Bearer\s+|(?:xi-api-key|api_key|access_token|secret|password)[\"']?\s*[:=]\s*[\"']?)[^\s\"']+", r"\1[REDACTED]", value)
            for key, secret in os.environ.items():
                if secret and len(secret) > 8 and re.search(r"(?:API_KEY|SECRET|ACCESS_TOKEN)$", key):
                    value = value.replace(secret, "[REDACTED]")
            def redact_url(match: re.Match[str]) -> str:
                u = urlsplit(match.group())
                safe = [(k, "[REDACTED]" if re.search(r"token|signature|credential|secret|key|sig$", k, re.I) else v) for k, v in parse_qsl(u.query)]
                netloc = "[REDACTED]@" + u.netloc.rsplit("@", 1)[1] if "@" in u.netloc else u.netloc
                return urlunsplit((u.scheme, netloc, u.path, urlencode(safe), u.fragment))
            return re.sub(r"https?://[^\s\"'<>\\)]+", redact_url, value)
        if value is None or isinstance(value, (int, float, bool)):
            return value
        return str(value)

    @staticmethod
    def file(path: Path) -> dict[str, Any]:
        resolved = path.resolve()
        item: dict[str, Any] = {"path": str(resolved), "exists": resolved.is_file()}
        if resolved.is_file():
            h = hashlib.sha256()
            with resolved.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            item.update(bytes=resolved.stat().st_size, sha256=h.hexdigest())
        return item

    def append(self, event: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        event = self.sanitize(event)
        body = (f"\n## {event['time']} — {event['provider']} / {event['operation']} — {event['event']}\n\n"
                + "```json\n" + json.dumps(event, ensure_ascii=False, indent=2) + "\n```\n").encode("utf-8")
        with self.path.open("a+b") as f:
            if os.name == "nt":
                import msvcrt
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0:
                    f.write("# 外部服务请求日志\n\n请求先落盘，结果按 request_id 追加关联；未确认的费用记为未知。\n".encode("utf-8"))
                f.write(body)
                f.flush()
                os.fsync(f.fileno())
            finally:
                if os.name == "nt":
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def invoke(self, provider: str, operation: str, request: dict[str, Any], call: Callable[[], T]) -> T:
        op = operation.lower()
        if provider.lower() == "dreamina" and (op in {"text2image", "image2image", "imagegen", "generate_image"} or op.startswith("post ") and "image" in op):
            from tools.image_engine import reject_dreamina_scene
            reject_dreamina_scene(self.target, str(request.get("prompt", "")))
        common = {"request_id": uuid.uuid4().hex, "provider": provider, "operation": operation,
                  "target": str(self.target), "pid": os.getpid()}
        clock = lambda: datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        fingerprint = hashlib.sha256(json.dumps(self.sanitize(request), sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        common["request_fingerprint"] = fingerprint
        self.append({**common, "time": clock(), "event": "request", "request": request})
        started = time.monotonic()
        try:
            result = call()
        except BaseException as e:
            self.append({**common, "time": clock(), "event": "error", "elapsed_s": round(time.monotonic() - started, 3),
                         "error_type": type(e).__name__, "error": str(e)})
            raise
        response: Any = result
        if isinstance(result, subprocess.CompletedProcess):
            response = {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        elif hasattr(result, "status_code"):
            try:
                body = result.json()
            except ValueError:
                body = result.content
            response = {"http_status": result.status_code, "headers": dict(result.headers), "body": body}
        self.append({**common, "time": clock(), "event": "result", "elapsed_s": round(time.monotonic() - started, 3),
                     "response": response})
        return result

    def http(self, provider: str, request: urllib.request.Request, *, timeout: float, context: Any = None) -> tuple[bytes, dict[str, str], int]:
        def call() -> tuple[bytes, dict[str, str], int]:
            options = {"context": context} if context is not None else {}
            with urllib.request.urlopen(request, timeout=timeout, **options) as r:
                return r.read(), dict(r.headers.items()), r.status
        return self.invoke(provider, request.get_method() + " " + urlsplit(request.full_url).path,
            {"url": request.full_url, "headers": dict(request.header_items()),
             "body": json.loads(request.data) if request.data else None, "timeout_s": timeout}, call)

    def download(self, provider: str, url: str, dest: Path, *, timeout: int, attempt: int = 1) -> int:
        def call() -> dict[str, Any]:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(req, timeout=timeout) as r, dest.open("wb") as f:
                status, headers = r.status, dict(r.headers.items())
                while chunk := r.read(1024 * 1024):
                    f.write(chunk)
            return {"http_status": status, "headers": headers, "file": self.file(dest)}
        response = self.invoke(provider, "GET artifact",
            {"url": url, "output": str(dest), "timeout_s": timeout, "attempt": attempt}, call)
        return response["file"]["bytes"]

    def cli(self, command: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        if len(command) > 1 and command[1] in {"text2image", "image2image"}:
            from tools.image_engine import reject_dreamina_scene
            prompt = next((a.split("=", 1)[1] for a in command if a.startswith("--prompt=")), "")
            if not prompt and "--prompt" in command:
                i = command.index("--prompt")
                prompt = command[i + 1] if i + 1 < len(command) else ""
            reject_dreamina_scene(self.target, prompt)
        files = []
        for i, arg in enumerate(command):
            flag, _, value = arg.partition("=")
            if flag in {"--image", "--images", "--video", "--audio", "--first_frame", "--last_frame"}:
                value = value or (command[i + 1] if i + 1 < len(command) else "")
                files.extend(Path(p) for p in value.split(",") if p)
        return self.invoke("dreamina", command[1], {"argv": command, "files": files, "timeout_s": kwargs.get("timeout"),
                           "attempt": 1, "internal_polling": "CLI --poll 参数控制；内部HTTP不可逐条观测"},
                           lambda: subprocess.run(command, **kwargs))
