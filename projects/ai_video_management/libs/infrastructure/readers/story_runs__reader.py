from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from libs.common.episode_workflow import fingerprint
from libs.common.story_runs import (
    STORY_FRAME_FIELDS, STORY_PROPOSAL_DECISIONS, STORY_RUN_ID_RE,
    STORY_RUN_PATH_RE, STORY_RUN_SCHEMA_VERSION, STORY_RUNS_FILE, STORY_RUN_INPUT_FILE,
)
from libs.infrastructure.daos.story_runs__dao import StoryRunsDao
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.story_run_io__reader import StoryRunIoReader


class StoryRunsReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root.resolve()
        self.episodes = EpisodeWorkflowReader(self.root)

    def _json(self, path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeError, OSError, ValueError) as exc:
            if isinstance(exc, FileNotFoundError):
                raise FileNotFoundError("找不到创作记录") from exc
            raise ValueError("创作记录JSON无法读取") from exc
        if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != STORY_RUN_SCHEMA_VERSION:
            raise ValueError("创作记录版本或结构无效")
        return value

    def index(self, episode_path: str) -> tuple[str, list[dict[str, Any]]]:
        directory = self.episodes.resolve(episode_path)
        canonical = directory.relative_to(self.root).as_posix()
        path = self.episodes.resolver.resolve(f"{canonical}/{STORY_RUNS_FILE}")
        if path is None:
            raise FileNotFoundError("找不到创作记录")
        if not path.exists():
            return canonical, []
        index = self._json(path)
        entries = index.get("runs")
        if not isinstance(entries, list):
            raise ValueError("创作记录索引无效")
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) for key in ("run_id", "audit_path", "created_at")):
                raise ValueError("创作记录索引项无效")
            if not STORY_RUN_ID_RE.fullmatch(entry["run_id"]) or entry["run_id"] in seen:
                raise ValueError("创作记录ID无效或重复")
            self.audit_path(entry)
            seen.add(entry["run_id"])
        return canonical, entries

    def audit_path(self, entry: dict[str, Any]) -> Path:
        match = STORY_RUN_PATH_RE.fullmatch(entry["audit_path"])
        if not match or match[2] != entry["run_id"]:
            raise ValueError("创作记录路径或ID不一致")
        try:
            date.fromisoformat(match[1])
        except ValueError as exc:
            raise ValueError("创作记录日期无效") from exc
        candidate = self.root / entry["audit_path"]
        for part in (candidate, *candidate.parents):
            if part == self.root:
                break
            if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
                raise ValueError("创作记录不允许链接路径")
        resolved = candidate.resolve()
        if resolved != candidate or self.root not in resolved.parents:
            raise ValueError("创作记录路径越界")
        return resolved

    def _strings(self, value: dict[str, Any], keys: tuple[str, ...]) -> bool:
        return all(isinstance(value.get(key), str) for key in keys)

    def _frame(self, value: Any) -> bool:
        return isinstance(value, dict) and self._strings(value, STORY_FRAME_FIELDS)

    def validate(self, run: dict[str, Any], entry: dict[str, Any], episode_path: str) -> None:
        if run.get("run_id") != entry["run_id"] or run.get("episode_path") != episode_path or run.get("created_at") != entry["created_at"]:
            raise ValueError("创作记录与索引或剧集不一致")
        if not self._strings(run, ("status",)) or not all(isinstance(run.get(key), list) for key in ("participants", "events", "proposals", "artifacts")):
            raise ValueError("创作记录结构无效")
        source, candidate = run.get("input"), run.get("candidate")
        if not isinstance(source, dict) or not self._frame(source.get("frame")) or not self._strings(source, ("brief", "input_hash")):
            raise ValueError("创作输入无效")
        if not all(isinstance(source.get(key), list) for key in ("assumptions", "sources", "rules")) or not isinstance(source.get("independence"), dict):
            raise ValueError("创作输入快照无效")
        if fingerprint({key: value for key, value in source.items() if key != "input_hash"}) != source["input_hash"]:
            raise ValueError("冻结输入指纹不一致")
        if not isinstance(candidate, dict) or not self._frame(candidate.get("frame")) or not self._strings(candidate, ("brief", "text")) or not isinstance(candidate.get("state_changes"), list):
            raise ValueError("故事候选版本无效")
        for participant in run["participants"]:
            if not isinstance(participant, dict) or not self._strings(participant, ("id", "name", "role", "status", "prompt", "output")) or participant.get("scope") not in {"story", "implementation"}:
                raise ValueError("参与者记录无效")
            if any(key not in participant or participant[key] is not None and not isinstance(participant[key], str) for key in ("runtime_id", "model", "started_at", "finished_at")):
                raise ValueError("参与者运行信息无效")
        for proposal in run["proposals"]:
            if not isinstance(proposal, dict) or not self._strings(proposal, ("id", "agent_id", "title", "detail", "reason", "location", "decision_reason", "decided_by")) or proposal.get("decision") not in STORY_PROPOSAL_DECISIONS:
                raise ValueError("意见与决策记录无效")
            if not all(isinstance(proposal.get(key), list) for key in ("criteria", "evidence")) or not isinstance(proposal.get("applied_in"), (str, list)):
                raise ValueError("意见证据无效")
        for event in run["events"]:
            if not isinstance(event, dict) or not self._strings(event, ("id", "at", "actor", "type", "title", "body")) or not all(isinstance(event.get(key), list) for key in ("proposal_ids", "artifact_refs")):
                raise ValueError("创作事件记录无效")

    def _read_run(self, entry: dict[str, Any], episode_path: str) -> dict[str, Any]:
        path = self.audit_path(entry)
        run = self._json(path)
        self.validate(run, entry, episode_path)
        frozen = path.parent / STORY_RUN_INPUT_FILE
        if frozen.is_symlink() or getattr(frozen, "is_junction", lambda: False)():
            raise ValueError("冻结输入不允许链接路径")
        if frozen.exists():
            if json.loads(frozen.read_text(encoding="utf-8")) != run["input"]:
                raise ValueError("冻结输入副本不一致")
        return run

    def read(self, episode_path: str) -> StoryRunsDao:
        canonical, entries = self.index(episode_path)
        return StoryRunsDao(canonical, [self._read_run(entry, canonical) for entry in entries])

    def detail(self, episode_path: str, run_id: str) -> dict[str, Any]:
        canonical, entries = self.index(episode_path)
        if not STORY_RUN_ID_RE.fullmatch(run_id):
            raise FileNotFoundError("找不到创作记录")
        entry = next((entry for entry in entries if entry["run_id"] == run_id), None)
        if entry is None:
            raise FileNotFoundError("找不到创作记录")
        return self._read_run(entry, canonical)

    def describe(self, run: dict[str, Any]) -> dict[str, Any]:
        _, entries = self.index(run["episode_path"])
        entry = next(entry for entry in entries if entry["run_id"] == run["run_id"])
        return StoryRunIoReader(self.root).read(run, entry["audit_path"])
