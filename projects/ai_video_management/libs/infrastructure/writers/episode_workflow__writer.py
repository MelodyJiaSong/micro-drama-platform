from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import Any

from libs.common.episode_workflow import MODULES
from libs.common.production_key import first_shot_key
from libs.common.safe_resolve import SafeResolver


class EpisodeWorkflowWriter:
    def __init__(self, repo_root: Path) -> None:
        self.resolver = SafeResolver(repo_root)
        self.lock = RLock()

    def write(self, episode_path: str, module: str, document: dict[str, Any]) -> None:
        if module not in MODULES:
            raise FileNotFoundError("无效模块")
        path = self.resolver.resolve(f"{episode_path}/{module}.json")
        if path is None or not path.parent.is_dir():
            raise FileNotFoundError("无效模块路径")
        outputs: list[tuple[Path, str]] = []
        if module == "prompts":
            for scene in document["content"]["scenes"]:
                for shot in scene["shots"]:
                    key = first_shot_key(shot["id"])
                    if key is None or key.value != shot["id"] or key.episode != int(path.parent.name[2:]):
                        raise ValueError("无效的编译镜头key")
                    folder = key.folder(path.parent)
                    parent = path.parent
                    for part in folder.relative_to(parent).parts:
                        directory = self.resolver.resolve((parent / part).relative_to(self.resolver.root).as_posix())
                        if directory is None:
                            raise FileNotFoundError("无效镜头目录")
                        directory.mkdir(exist_ok=True)
                        parent = directory
                    target = self.resolver.resolve(folder.relative_to(self.resolver.root).as_posix() + "/prompt.txt")
                    if target is None:
                        raise FileNotFoundError("无效镜头输出路径")
                    outputs.append((target, shot["text"] + "\n"))
        for target, text in outputs:
            target.parent.mkdir(parents=True, exist_ok=True)
            self._atomic_write(target, text)
        self._atomic_write(path, json.dumps(document, ensure_ascii=False, indent=2) + "\n")

    @staticmethod
    def _atomic_write(path: Path, text: str) -> None:
        fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".workflow-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
