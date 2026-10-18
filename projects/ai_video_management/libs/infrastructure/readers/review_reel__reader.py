"""审片串联的读取（follow-up 260）：按分镜顺序列出每镜的生成条（新的在前），以及集目录 review_reel/ 下已有的串联与进度。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.common.production_key import shot_key
from libs.common.review_reel import REEL_DIR
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.shot_renders__reader import ShotRendersReader


class ReviewReelReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.episodes = EpisodeWorkflowReader(repo_root)
        self.renders = ShotRendersReader(repo_root)

    def scenes(self, episode_path: str) -> tuple[str, list[dict[str, Any]]]:
        """(集目录的仓库相对路径, 分镜场次)；路径不是一集或不在沙箱里抛 FileNotFoundError。"""
        dao = self.episodes.read(episode_path)
        return dao.episode_path, dao.documents["filming"]["content"]["scenes"]

    def candidates(self, episode_path: str, scenes: list[dict[str, Any]]) -> list[tuple[str, str, list[dict[str, Any]]]]:
        """[(场, 镜头 key, 有视频的生成条，新的在前)]，顺序同分镜。每条补上视频的大小与修改时间（纳秒）。"""
        episode_id = episode_path.rsplit("/", 1)[-1]
        keyed = [(scene["id"], shot_key(episode_id, scene["id"], shot["id"]).value) for scene in scenes for shot in scene["shots"]]
        takes = self.renders.read(episode_path, {"scenes": [{"id": sid, "shots": [{"id": key}]} for sid, key in keyed]})
        out = []
        for sid, key in keyed:
            usable = []
            for take in takes.get(key, []):
                video = take["videos"][0] if take["videos"] else ""
                stat = (self.root / video).stat() if video and (self.root / video).is_file() else None
                if stat is not None:
                    usable.append({**take, "video": video, "size": stat.st_size, "mtime_ns": stat.st_mtime_ns})
            out.append((sid, key, usable))
        return out

    def folder(self, episode_path: str) -> Path:
        return self.root / episode_path / REEL_DIR

    def load(self, episode_path: str, name: str, kind: str) -> dict[str, Any] | None:
        """kind：manifest（{name}.json）或 status（{name}.status.json）。读不出当作没有。"""
        path = self.folder(episode_path) / (f"{name}.json" if kind == "manifest" else f"{name}.status.json")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return data if isinstance(data, dict) else None
