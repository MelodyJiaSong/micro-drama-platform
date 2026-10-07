from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.common.writers_room_paths import bible_path, room_path


class WritersRoomReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    @staticmethod
    def json(path: Path, default: Any = None) -> Any:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

    def list(self) -> list[dict[str, Any]]:
        return [self.json(p) for p in sorted((self.root / "ai_videos").glob("*/2_世界观人设/writers_room/seed.json"))]

    def detail(self, slug: str) -> dict[str, Any]:
        bible, room = bible_path(self.root, slug), room_path(self.root, slug)
        seed = self.json(bible / "seed.json")
        if seed is None:
            raise FileNotFoundError("尚未创建该剧的编剧室。")
        head = self.json(room / "head.json", {"revision": None, "memory": {}, "scenes": []})
        revision = self.json(room / "revisions" / f"{head['revision']}.json", head) if head["revision"] else head
        return {"seed": seed, "answers": self.json(bible / "answers.json", {"revision": 0, "characters": {}}), "story_bible": self.json(bible / "story_bible.json"), "character_bibles": self.json(bible / "character_bibles.json", {}), "head": head, "memory": revision["memory"], "scenes": revision["scenes"], "episodes": self.json(room / "episodes.json", {}), "job": self.json(room / "job.json"), "config": self.json(bible / "config.json", {})}

    def script(self, slug: str, revision: str) -> str:
        if not revision.isalnum() or len(revision) != 64:
            raise ValueError("无效的剧本版本。")
        return (room_path(self.root, slug) / "revisions" / f"{revision}.md").read_text(encoding="utf-8")
