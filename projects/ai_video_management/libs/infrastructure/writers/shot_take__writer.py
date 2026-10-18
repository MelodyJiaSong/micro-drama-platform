"""Write the user's verdict into a take's `review.md` (follow-up 265).

A take is a folder `…/shots/stN/renders/<take>/` holding `generation.json`; only its `状态：` line changes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.shot_take__error import ShotTakeError

TAKE_RE = re.compile(r"^ai_videos/.+/shots/st\d+/(?:renders|drafts)/[^/]+$")   # 草稿在 drafts/（follow-up 266）
STATUS_RE = re.compile(r"^状态[:：].*$", re.M)
REVIEW_FILE = "review.md"
NEW_REVIEW = "# 审核：{key} · {take}\n\n状态：{status}\n\nVision：\n\n## 对的\n\n-\n\n## 不对的\n\n-\n\n## 结论\n\n\n## 怎么看的\n\n"


class ShotTakeWriter:
    def __init__(self, repo_root: Path) -> None:
        self.resolver = SafeResolver(repo_root)

    def folder(self, take_path: str) -> Path:
        folder = self.resolver.resolve(take_path) if isinstance(take_path, str) and TAKE_RE.match(take_path) else None
        if folder is None or not (folder / "generation.json").is_file():
            raise ShotTakeError("不是一条生成记录：%s" % take_path)
        return folder

    def record(self, folder: Path) -> dict[str, Any]:
        return json.loads((folder / "generation.json").read_text(encoding="utf-8"))

    def set_status(self, folder: Path, status: str) -> None:
        review = folder / REVIEW_FILE
        line = "状态：" + status
        if review.is_file():
            text = review.read_text(encoding="utf-8")
            text = STATUS_RE.sub(lambda _m: line, text, count=1) if STATUS_RE.search(text) else text.rstrip("\n") + "\n\n" + line + "\n"
        else:
            text = NEW_REVIEW.format(key=self.record(folder).get("key", ""), take=folder.name, status=status)
        review.write_text(text, encoding="utf-8", newline="\n")
