from __future__ import annotations

import json
import os
import time
from pathlib import Path

from libs.common.enums import PipelineStage
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


class PipelineStateWriter:
    """Episode pipeline state lives in the workspace (NFR-A2): pipeline_state.json is
    the source of truth; a lock file gives multi-worker mutual exclusion (atomic
    O_CREAT|O_EXCL). Stale locks (>30min) are reclaimable."""

    _LOCK_STALE_S = 3600  # Claude-CLI understand on a long episode can exceed 30min; step() heartbeats per stage

    def __init__(self, workspace: SafeWorkspace) -> None:
        self._workspace = workspace

    def write(self, episode_rel_dir: str, state: dict) -> None:
        path = Path(self._workspace.resolve(f"{episode_rel_dir}/pipeline_state.json"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def init_state(self, episode_rel_dir: str) -> dict:
        state = {"stage": PipelineStage.INGEST.value, "failed_reason": None,
                 "gate_hold": False, "needs_recompose": False}
        self.write(episode_rel_dir, state)
        return state

    def try_claim(self, episode_rel_dir: str, worker_id: str) -> bool:
        lock = Path(self._workspace.resolve(f"{episode_rel_dir}/.worker_lock"))
        lock.parent.mkdir(parents=True, exist_ok=True)
        if lock.exists() and time.time() - lock.stat().st_mtime > self._LOCK_STALE_S:
            lock.unlink(missing_ok=True)
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(worker_id)
        return True

    def heartbeat(self, episode_rel_dir: str) -> None:
        """Refresh the lock mtime so a legitimately long step is not reclaimed as stale."""
        lock = Path(self._workspace.resolve(f"{episode_rel_dir}/.worker_lock"))
        if lock.exists():
            lock.touch()

    def release(self, episode_rel_dir: str) -> None:
        Path(self._workspace.resolve(f"{episode_rel_dir}/.worker_lock")).unlink(missing_ok=True)
