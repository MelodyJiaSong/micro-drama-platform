"""每镜的首帧图（故事板审阅，follow-up 336）。

单镜的故事板就是它的首帧图 `scenes/sN/shots/stN/planning/stN_first_frame.png`；重画前的旧版放在
`planning/_r1/`、`_r2/`、`_v2_old/` 等子目录，旧镜组板与旧场故事板在 `_obsolete/` 下——这里只认 planning
目录下这一个固定文件名，绝不往子目录里找。返回修改时间（毫秒），页面拿它做缓存版本号，图重画后刷新即见新图。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from libs.common.production_key import shot_key

PLANNING = "planning"


def first_frame_name(shot: str) -> str:
    return f"{shot}_first_frame.png"


class ShotFirstFrameReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def read(self, episode_path: str, filming: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """完整镜头 key → {path, mtime, prompt}；图还没出时 path 为空串、mtime 为 0。"""
        episode = self.root / episode_path
        episode_id = episode.name
        out: dict[str, dict[str, Any]] = {}
        for scene in filming.get("scenes", []):
            for shot in scene.get("shots", []):
                try:
                    key = shot_key(episode_id, scene["id"], shot["id"])
                except (KeyError, ValueError):
                    continue
                planning = key.folder(episode) / PLANNING
                image = planning / first_frame_name(shot["id"])
                prompt = planning / f"{shot['id']}_first_frame_prompt.txt"
                found = image.is_file() and not image.is_symlink()
                out[key.value] = {
                    "path": self._rel(image) if found else "",
                    "mtime": int(image.stat().st_mtime_ns // 1_000_000) if found else 0,
                    "prompt": self._rel(prompt) if prompt.is_file() and not prompt.is_symlink() else "",
                }
        return out

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()
