from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from contextlib import contextmanager
from collections.abc import Iterator
from typing import Any

from libs.common.story_runs import STORY_RUN_SCHEMA_VERSION, STORY_RUNS_FILE, STORY_RUN_INPUT_FILE, STORY_SELECTION_FILE
from libs.common.episode_workflow import fingerprint, empty_document
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader


class StoryRunsWriter:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root.resolve()
        self.reader = StoryRunsReader(self.root)
        self.lock = RLock()

    def _atomic(self, path: Path, value: dict[str, Any]) -> None:
        encoded = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(encoded)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def begin(self, run: dict[str, Any]) -> str:
        with self.episode_lock(run["episode_path"]):
            return self._begin_locked(run)

    @contextmanager
    def episode_lock(self, episode_path: str) -> Iterator[None]:
        with self.lock:
            directory = self.reader.episodes.resolve(episode_path)
            lock_path = directory / ".story_runs.lock"
            descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            try:
                os.close(descriptor)
                yield
            finally:
                lock_path.unlink()

    def promote(self, episode_path: str, story: dict[str, Any], selection: dict[str, Any], expected: str) -> None:
        resolver = self.reader.episodes.resolver
        story_path = resolver.resolve(f"{episode_path}/story.json")
        selection_path = resolver.resolve(f"{episode_path}/{STORY_SELECTION_FILE}")
        if story_path is None or selection_path is None:
            raise ValueError("故事选择写入路径无效")
        current = json.loads(story_path.read_text(encoding="utf-8")) if story_path.exists() else empty_document("story")
        if fingerprint(current) != expected:
            raise ValueError("故事已被其他会话修改")
        self._atomic(story_path, story)
        self._atomic(selection_path, selection)

    def _begin_locked(self, run: dict[str, Any]) -> str:
        canonical, entries = self.reader.index(run["episode_path"])
        created_date = run["created_at"][:10]
        audit_path = f".audit/adhoc_agents/{created_date}/{run['run_id']}/run.json"
        entry = {"run_id": run["run_id"], "audit_path": audit_path, "created_at": run["created_at"]}
        path = self.reader.audit_path(entry)
        self.reader.validate(run, entry, canonical)
        path.parent.mkdir(parents=True, exist_ok=False)
        self._atomic(path.parent / STORY_RUN_INPUT_FILE, run["input"])
        self._atomic(path, run)
        self._atomic(self.root / canonical / STORY_RUNS_FILE,
                     {"schema_version": STORY_RUN_SCHEMA_VERSION, "runs": [*entries, entry]})
        return audit_path
