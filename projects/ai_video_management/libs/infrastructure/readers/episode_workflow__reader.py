from __future__ import annotations

import json
import re
from pathlib import Path

from libs.common.drama_ref import split_drama_rel
from libs.common.episode_workflow import MODULES, WORKFLOW_ID, WORKFLOW_MARKER, empty_document
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.daos.episode_workflow__dao import EpisodeWorkflowDao


class EpisodeWorkflowReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.resolver = SafeResolver(repo_root)

    def resolve(self, episode_path: str) -> Path:
        path = self.resolver.resolve(episode_path)
        split = split_drama_rel(self.root, episode_path)
        if path is None or not path.is_dir() or not split:
            raise FileNotFoundError("找不到剧集")
        drama, parts = split
        if len(parts) != 2 or parts[0] != "episodes" or not re.fullmatch(r"ep\d{2,}", parts[1]):
            raise FileNotFoundError("无效的剧集路径")
        marker = self.resolver.resolve(f"{drama}/{WORKFLOW_MARKER}")
        if marker is None or not marker.is_file():
            raise FileNotFoundError("该剧未使用三模块流程")
        if json.loads(marker.read_text(encoding="utf-8")).get("workflow") != WORKFLOW_ID:
            raise FileNotFoundError("该剧未使用三模块流程")
        return path

    def read(self, episode_path: str) -> EpisodeWorkflowDao:
        directory = self.resolve(episode_path)
        documents = {}
        for module in MODULES:
            file = self.resolver.resolve(f"{episode_path}/{module}.json")
            if file is None:
                raise FileNotFoundError("无效模块路径")
            doc = json.loads(file.read_text(encoding="utf-8")) if file.exists() else empty_document(module)
            if not isinstance(doc, dict) or set(doc) != {"content", "source_revision", "approved_revision"}:
                raise ValueError("无效模块文件")
            if not isinstance(doc["content"], dict) or any(doc[key] is not None and not isinstance(doc[key], str)
                                                       for key in ("source_revision", "approved_revision")):
                raise ValueError("无效模块内容或版本")
            if module == "story":
                if set(doc["content"]) != {"brief", "text"} or not all(isinstance(v, str) for v in doc["content"].values()):
                    raise ValueError("无效故事内容")
            elif not isinstance(doc["content"].get("scenes"), list):
                raise ValueError("无效场次列表")
            documents[module] = doc
        return EpisodeWorkflowDao(directory.relative_to(self.root).as_posix(), documents)
