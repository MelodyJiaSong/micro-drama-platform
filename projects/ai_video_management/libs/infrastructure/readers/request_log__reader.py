from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.daos.request_log__dao import RequestLogDao


class RequestLogReader:
    def __init__(self, exposed_tree: ExposedTree) -> None:
        self._tree = exposed_tree

    def list(self) -> RequestLogDao:
        root = self._tree.root
        logs = []
        for file in (root / "ai_videos").rglob("request_log.md"):
            rel = file.relative_to(root).as_posix()
            if file.is_symlink() or not self._tree.is_inside(rel):
                continue
            stat = file.stat()
            logs.append({"path": rel, "bytes": stat.st_size, "modified_at": stat.st_mtime})
        return RequestLogDao(sorted(logs, key=lambda x: x["modified_at"], reverse=True), [], len(logs))

    def read(self, path: str, offset: int, limit: int) -> RequestLogDao:
        if not path.startswith("ai_videos/") or not self._tree.is_inside(path):
            raise FileNotFoundError(path)
        file = self._tree.root / path
        if file.name != "request_log.md" or file.is_symlink() or not file.is_file():
            raise FileNotFoundError(path)
        tail: deque[dict] = deque(maxlen=offset + limit)
        total, block = 0, None
        with file.open(encoding="utf-8") as f:
            for line in f:
                if line.rstrip() == "```json" and block is None:
                    block = []
                elif line.rstrip() == "```" and block is not None:
                    try:
                        event = json.loads("".join(block))
                    except json.JSONDecodeError:
                        event = {"event": "invalid", "error": "记录JSON格式损坏，查看原始文件"}
                    if not isinstance(event, dict):
                        event = {"event": "invalid", "error": "记录必须是对象"}
                    tail.append(event)
                    total += 1
                    block = None
                elif block is not None:
                    block.append(line)
        return RequestLogDao([], list(reversed(tail))[offset:offset + limit], total)
