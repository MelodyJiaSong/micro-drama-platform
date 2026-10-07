from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.common.story_runs import STORY_INPUT_FILE, STORY_PROFILE_ID_RE, STORY_RUN_SCHEMA_VERSION
from libs.infrastructure.daos.story_input__dao import StoryInputDao
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader


class StoryInputReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root.resolve()
        self.episodes = EpisodeWorkflowReader(self.root)

    def _json(self, path: Path) -> dict[str, Any]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("共享输入必须是JSON对象")
        return value

    def _path(self, episode_path: str, rel: str) -> Path:
        if not isinstance(rel, str) or not rel.startswith("shared/") or "." in rel.split("/"):
            raise ValueError("共享输入路径必须位于本集shared目录")
        path = self.episodes.resolver.resolve(f"{episode_path}/{rel}")
        if path is None:
            raise ValueError("共享输入路径无效或越界")
        return path

    def _compose(self, file: Path, shared_root: Path | None = None, expected_rules: Path | None = None) -> dict[str, Any]:
        document = self._json(file)
        if "rules_path" not in document:
            if expected_rules is not None:
                raise ValueError("共享输入缺少显式rules_path")
            return document
        rel = document.pop("rules_path")
        if not isinstance(rel, str) or not rel or "/" in rel or "\\" in rel or ":" in rel or rel in {".", ".."}:
            raise ValueError("rules_path只能引用输入文件同目录的文件")
        rules_file = file.parent / rel
        if rules_file.is_symlink() or getattr(rules_file, "is_junction", lambda: False)():
            raise ValueError("规则文件不能使用链接")
        if rules_file.resolve() != rules_file or shared_root is not None and shared_root not in rules_file.parents:
            raise ValueError("规则文件路径越界")
        if expected_rules is not None and rules_file != expected_rules:
            raise ValueError("规则路径与profile索引不一致")
        if "rules" in document:
            raise ValueError("输入不能同时包含rules和rules_path")
        rules = self._json(rules_file)
        if type(rules.get("schema_version")) is not int or rules["schema_version"] != STORY_RUN_SCHEMA_VERSION or not isinstance(rules.get("rules"), list):
            raise ValueError("规则文件版本或内容无效")
        document["rules"] = rules["rules"]
        return document

    def read_file(self, episode_path: str, file_path: str | Path) -> dict[str, Any]:
        directory = self.episodes.resolve(episode_path)
        raw = Path(file_path)
        if raw.is_symlink() or getattr(raw, "is_junction", lambda: False)():
            raise ValueError("输入文件不能使用链接")
        candidate = raw if raw.is_absolute() else self.root / raw
        candidate = candidate.absolute()
        if self.root / "ai_videos" in candidate.parents and directory / "shared" not in candidate.parents:
            raise ValueError("共享输入必须属于本集shared目录")
        for part in (candidate, *candidate.parents):
            if part == self.root:
                break
            if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
                raise ValueError("输入文件不能使用链接")
        if candidate.resolve() != candidate:
            raise ValueError("输入文件路径无效")
        return self._compose(candidate)

    def read(self, episode_path: str) -> StoryInputDao:
        directory = self.episodes.resolve(episode_path)
        canonical = directory.relative_to(self.root).as_posix()
        index = self._json(self._path(canonical, STORY_INPUT_FILE))
        if type(index.get("schema_version")) is not int or index["schema_version"] != STORY_RUN_SCHEMA_VERSION or not isinstance(index.get("profiles"), list):
            raise ValueError("共享输入索引无效")
        inputs: dict[str, dict[str, Any]] = {}
        profiles = []
        for profile in index["profiles"]:
            if not isinstance(profile, dict) or not all(isinstance(profile.get(key), str) for key in ("id", "label", "input_path", "rules_path")):
                raise ValueError("共享输入profile无效")
            key = profile["id"]
            if not STORY_PROFILE_ID_RE.fullmatch(key) or key in inputs:
                raise ValueError("共享输入profile ID无效或重复")
            file = self._path(canonical, profile["input_path"])
            rules_file = self._path(canonical, profile["rules_path"])
            inputs[key] = self._compose(file, directory / "shared", rules_file)
            profiles.append(profile)
        selected = index.get("selected_profile")
        if not isinstance(selected, str) or selected not in inputs:
            raise ValueError("默认共享输入profile不存在")
        return StoryInputDao(canonical, selected, profiles, inputs)
