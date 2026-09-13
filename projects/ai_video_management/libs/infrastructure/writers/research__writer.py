"""Writes the research workspace — the user's decisions about a research dataset.

Kept in a SEPARATE file from the dataset (`{dataset}.workspace.json` next to
`{dataset}.json`) for the same reason `promoted.md` is separate from a stage's
output: re-running the research regenerates the dataset, and a shortlist the
user built by hand must not be destroyed by that. The workspace references
series by slug and videos by id, so it survives a regeneration that changes
metrics, ordering, or prose.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.infrastructure.errors.research__error import ResearchError
from libs.infrastructure.readers.research__reader import WORKSPACE_SUFFIX, ResearchReader

STATUSES: frozenset[str] = frozenset({"none", "shortlist", "doing", "rejected"})
MAX_NOTE_CHARS: int = 4000


class ResearchWriter:
    def __init__(self, repo_root: Path, reader: ResearchReader) -> None:
        self._reader = reader
        self._root = repo_root / "ai_videos" / "_research"

    def _path(self, dataset: str) -> Path:
        self._reader.dataset(dataset)  # existence + name validation
        return self._root / f"{dataset}{WORKSPACE_SUFFIX}"

    def workspace(self, dataset: str) -> dict[str, Any]:
        path = self._path(dataset)
        if not path.is_file():
            return {"dataset": dataset, "series": {}, "videos": {}}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ResearchError("bad_json", f"{dataset}.workspace.json 解析失败: {exc}") from exc
        data.setdefault("series", {})
        data.setdefault("videos", {})
        return data

    def _save(self, dataset: str, data: dict[str, Any]) -> dict[str, Any]:
        path = self._path(dataset)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data

    def mark_series(
        self,
        dataset: str,
        slug: str,
        status: str | None,
        rating: int | None,
        note: str | None,
    ) -> dict[str, Any]:
        self._reader.series(dataset, slug)  # 404s on an unknown slug
        if status is not None and status not in STATUSES:
            raise ResearchError("bad_status", f"不合法的状态: {status}")
        if rating is not None and not 0 <= rating <= 5:
            raise ResearchError("bad_rating", f"评分需在 0-5 之间: {rating}")
        if note is not None and len(note) > MAX_NOTE_CHARS:
            raise ResearchError("note_too_long", f"笔记超过 {MAX_NOTE_CHARS} 字")

        data = self.workspace(dataset)
        entry = dict(data["series"].get(slug, {}))
        if status is not None:
            entry["status"] = status
        if rating is not None:
            entry["rating"] = rating
        if note is not None:
            entry["note"] = note
        if entry.get("status", "none") == "none" and not entry.get("rating") and not entry.get("note"):
            data["series"].pop(slug, None)
        else:
            data["series"][slug] = entry
        self._save(dataset, data)
        return data

    def mark_video(
        self, dataset: str, video_id: str, bookmarked: bool | None, note: str | None
    ) -> dict[str, Any]:
        known = {
            v["video_id"]
            for s in self._reader.dataset(dataset)["series"]  # type: ignore[union-attr]
            for v in s.get("videos", [])
        }
        if video_id not in known:
            raise ResearchError("not_found", f"样本不存在于该数据集: {video_id}")
        if note is not None and len(note) > MAX_NOTE_CHARS:
            raise ResearchError("note_too_long", f"笔记超过 {MAX_NOTE_CHARS} 字")

        data = self.workspace(dataset)
        entry = dict(data["videos"].get(video_id, {}))
        if bookmarked is not None:
            entry["bookmarked"] = bookmarked
        if note is not None:
            entry["note"] = note
        if not entry.get("bookmarked") and not entry.get("note"):
            data["videos"].pop(video_id, None)
        else:
            data["videos"][video_id] = entry
        self._save(dataset, data)
        return data
