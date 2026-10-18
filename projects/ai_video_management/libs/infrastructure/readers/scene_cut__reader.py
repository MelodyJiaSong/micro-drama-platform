"""剪辑决定的读取（follow-up 269）：一集各场 edit/{draft,final}/cut_v{N}.json 原样读出，附上仓库相对路径。"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from libs.common.scene_cut import CUT_FILE_PATTERN, CUT_STAGES, EDIT_DIR, GALLERY_PATTERN
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader


class SceneCutReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.episodes = EpisodeWorkflowReader(repo_root)

    def scenes(self, episode_path: str) -> tuple[str, list[dict[str, Any]]]:
        """(集目录的仓库相对路径, 分镜场次)；不是一集或不在沙箱里抛 FileNotFoundError。"""
        dao = self.episodes.read(episode_path)
        return dao.episode_path, dao.documents["filming"]["content"]["scenes"]

    def cuts(self, episode_path: str, scene: str | None) -> dict[str, list[dict[str, Any]]]:
        """{阶段: [剪辑决定，带 _path / _dir / _file_version]}；读不出的文件也列出，带 _error。
        scene 为 None 时读集级剪辑 `{集}/edit/{阶段}/`（follow-up 278）。"""
        out: dict[str, list[dict[str, Any]]] = {}
        for stage in CUT_STAGES:
            base = self.root / episode_path if scene is None else self.root / episode_path / "scenes" / scene
            folder = base / EDIT_DIR / stage
            found = []
            if folder.is_dir() and not folder.is_symlink():
                for file in folder.iterdir():
                    match = re.fullmatch(CUT_FILE_PATTERN, file.name)
                    if not match or not file.is_file() or file.is_symlink():
                        continue
                    try:
                        data = json.loads(file.read_text(encoding="utf-8"))
                        if not isinstance(data, dict):
                            raise ValueError("不是 JSON 对象")
                    except (OSError, ValueError) as exc:
                        data = {"_error": f"读不出：{exc}"}
                    found.append({**data, "_path": file.relative_to(self.root).as_posix(),
                                  "_dir": folder.relative_to(self.root).as_posix(), "_file_version": int(match.group(1))})
            out[stage] = found
        return out

    def exists(self, rel_path: str) -> bool:
        target = self.root / rel_path
        return target.is_file() and not target.is_symlink()

    def galleries(self, episode_path: str, stage: str) -> list[tuple[str, str, str, str]]:
        """集级剪辑目录里的转场样片：[(视频仓库相对路径, 前一场, 后一场, 时间索引文本)]，按文件名排。"""
        folder = self.root / episode_path / EDIT_DIR / stage
        if not folder.is_dir() or folder.is_symlink():
            return []
        out = []
        for file in sorted(folder.iterdir(), key=lambda f: f.name):
            match = re.fullmatch(GALLERY_PATTERN, file.name)
            if not match or not file.is_file() or file.is_symlink():
                continue
            index = file.with_suffix(".txt")
            text = index.read_text(encoding="utf-8") if index.is_file() and not index.is_symlink() else ""
            out.append((file.relative_to(self.root).as_posix(), match.group(1), match.group(2), text))
        return out
