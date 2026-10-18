"""Each shot's generations for the UI (follow-up 230).

`renders/` holds one folder per generation (`tools/shot_take.py`, or the downloads importer): the video, `generation.json`
(model, credits, submit id, references), `prompt.txt` (the text that was sent) and `review.md` (what is right / wrong,
verdict, how it was checked). Videos left directly in `renders/` by older flows are listed as takes without a record.
Newest first; `archive/` is skipped like the take selector does. Drafts live beside it in `drafts/` (follow-up 266) and are
listed together with the finals.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from libs.common.production_key import first_shot_key

RENDERS = "renders"
DRAFTS = "drafts"
ARCHIVE = "archive"
VIDEO_EXTS = {".mp4", ".mov", ".webm"}
STATUS_RE = re.compile(r"^状态[:：]\s*(.+)$", re.M)


class ShotRendersReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def read(self, episode_path: str, prompts: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
        episode = self.root / episode_path
        out: dict[str, list[dict[str, Any]]] = {}
        for scene in prompts.get("scenes", []):
            for shot in scene["shots"]:
                key = first_shot_key(shot["id"])
                if key is not None:
                    folder = key.folder(episode)
                    takes = self._takes(folder / DRAFTS) + self._takes(folder / RENDERS)
                    out[shot["id"]] = [t for _, t in sorted(takes, key=lambda t: (t[0], t[1]["id"]), reverse=True)]
        return out

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def _takes(self, renders: Path) -> list[tuple[float, dict[str, Any]]]:
        if not renders.is_dir():
            return []
        takes: list[tuple[float, dict[str, Any]]] = []
        for entry in renders.iterdir():
            if entry.name == ARCHIVE or entry.name.startswith("."):
                continue
            if entry.is_dir():
                videos = sorted(p for p in entry.iterdir() if p.suffix.lower() in VIDEO_EXTS and p.is_file())
                review_file = entry / "review.md"
                review = review_file.read_text(encoding="utf-8") if review_file.is_file() else ""
                status = STATUS_RE.search(review)
                record_file = entry / "generation.json"
                record = json.loads(record_file.read_text(encoding="utf-8")) if record_file.is_file() else {}
                stamp = max((p.stat().st_mtime for p in videos), default=entry.stat().st_mtime)
                takes.append((stamp, {
                    "id": entry.name, "path": self._rel(entry),
                    "videos": [self._rel(p) for p in videos],
                    "review": review, "review_path": self._rel(review_file) if review_file.is_file() else "",
                    "review_status": status.group(1).strip() if status else ("" if review else "没有审核"),
                    "generation": {k: record.get(k) for k in ("submit_id", "model", "stage", "duration_s", "ratio", "resolution",
                                                              "credits", "downloaded_at", "from_take") if k in record},
                    "prompt_path": self._rel(entry / "prompt.txt") if (entry / "prompt.txt").is_file() else "",
                }))
            elif entry.suffix.lower() in VIDEO_EXTS and entry.is_file():
                takes.append((entry.stat().st_mtime, {
                    "id": entry.stem, "path": self._rel(entry), "videos": [self._rel(entry)], "review": "",
                    "review_path": "", "review_status": "没有审核（旧版平铺在 renders/）", "generation": {}, "prompt_path": ""}))
        return takes
