"""审查单索引（follow-up 333）：左侧导航「审查单」一类要列出所有剧的审查单。

审查单由 `tools/review_run.py`（短剧）与 `tools/edu_review.py`（教学视频 `edu_videos/<系列>/<知识点>/reviews/lines_rN/`）写在 `ai_videos/<剧>/reviews/<集>_<时间>_<阶段>_r<轮>/checklist.json`
（剧在系列下时多一层：`ai_videos/<系列>/<剧>/reviews/…`）。这里只读、只摘要：标题、状态、轮次、几位审稿人打了勾、
各严重度的问题数；细节由页面再读 checklist.json 与报告。只扫这两层固定位置，不 rglob 整棵 ai_videos。
"""
from __future__ import annotations

import json
import re
from typing import Any

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.daos.review_run__dao import ReviewRunDao

SEVERITIES = ("重出", "可剪", "记录", "存疑")
PATTERNS = ("ai_videos/*/reviews/*/checklist.json", "ai_videos/*/*/reviews/*/checklist.json",
            # 教学视频的台词审（tools/edu_review.py new，用户 2026-11-08「审查结果记录在审查单下面」）
            "edu_videos/*/*/reviews/*/checklist.json")
# 一张审查单的目录（与 PATTERNS 同两层）。checklist.json 会超过通用 /api/file 的 1 MiB 上限（v5 双审单常到 1.5 MB），
# 审查页经 /api/review-runs/checklist 单独读，上限放宽到 16 MiB。
RUN_DIR = re.compile(r"^(?:ai_videos/(?:[^/]+/){1,2}|edu_videos/[^/]+/[^/]+/)reviews/[^/]+$")
CHECKLIST_MAX_BYTES = 16 * 1024 * 1024


class ReviewRunReader:
    def __init__(self, exposed_tree: ExposedTree) -> None:
        self._tree = exposed_tree

    def list(self) -> ReviewRunDao:
        root = self._tree.root
        runs: list[dict[str, Any]] = []
        seen: set[str] = set()
        for pattern in PATTERNS:
            for file in root.glob(pattern):
                rel_dir = file.parent.relative_to(root).as_posix()
                if rel_dir in seen or file.is_symlink() or not self._tree.is_inside(rel_dir):
                    continue
                seen.add(rel_dir)
                try:
                    run = json.loads(file.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    continue
                if isinstance(run, dict):
                    summary = self._summary(rel_dir, run)
                    summary["corrections"] = (file.parent / "corrections.json").is_file()   # 左侧导航每轮的「修复」入口
                    runs.append(summary)
        runs.sort(key=lambda r: r["created_at"], reverse=True)
        return ReviewRunDao(runs)

    def checklist(self, rel_dir: str) -> dict[str, Any] | None:
        """读一张审查单的 checklist.json；不是审查单目录、不在沙箱里、太大或坏 JSON 都返回 None。"""
        rel_dir = rel_dir.strip("/")
        if not RUN_DIR.match(rel_dir) or ".." in rel_dir.split("/") or not self._tree.is_inside(rel_dir):
            return None
        file = self._tree.root / rel_dir / "checklist.json"
        try:
            if file.is_symlink() or not file.is_file() or file.stat().st_size > CHECKLIST_MAX_BYTES:
                return None
            data = json.loads(file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return data if isinstance(data, dict) else None

    @staticmethod
    def _summary(rel_dir: str, run: dict[str, Any]) -> dict[str, Any]:
        items = [i for i in run.get("items", []) if isinstance(i, dict)]
        totals = {s: 0 for s in SEVERITIES}
        for item in items:
            for key, value in (item.get("findings") or {}).items():
                if key in totals and isinstance(value, int):
                    totals[key] += value
        drama = rel_dir.rsplit("/reviews/", 1)[0]
        return {
            "dir": rel_dir, "drama": drama, "drama_name": drama.rsplit("/", 1)[-1],
            "id": str(run.get("id", rel_dir.rsplit("/", 1)[-1])), "title": str(run.get("title", "")),
            "episode": str(run.get("episode", "")), "chain": str(run.get("chain") or run.get("id", "")),
            "loop": int(run.get("loop") or 1), "max_loops": int(run.get("max_loops") or 3),
            "stage": str(run.get("stage", "")), "stage_name": str(run.get("stage_name", "")),
            # 覆盖哪几场：剧页故事板按场显示最新一张出片前审查单（follow-up 336）
            "scenes": [str(s) for s in run.get("scenes") or [] if isinstance(s, str)],
            "state": str(run.get("state", "")), "created_at": str(run.get("created_at", "")),
            "done": sum(1 for i in items if i.get("status") == "done"),
            "failed": sum(1 for i in items if i.get("status") == "failed"), "total": len(items), "totals": totals,
        }
