from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from libs.common.episode_workflow import fingerprint
from libs.common.story_runs import STORY_PROMOTABLE_STATUSES, STORY_RUN_SCHEMA_VERSION, StoryRunsError
from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity


@dataclass
class StorySelectionEntity:
    selection: dict[str, Any] | None

    def promote(self, run: dict[str, Any], workflow: EpisodeWorkflowEntity, promoted_at: str) -> dict[str, Any]:
        candidate = run["candidate"]
        if run["status"] not in STORY_PROMOTABLE_STATUSES or not candidate["text"].strip():
            raise StoryRunsError("候选故事尚未完整或未进入可审状态")
        workflow.save("story", {"brief": candidate["brief"], "text": candidate["text"]})
        workflow.documents["story"]["approved_revision"] = None
        entry = {"run_id": run["run_id"], "candidate_hash": fingerprint(candidate),
                 "input_hash": run["input"]["input_hash"], "story_revision": workflow.revision("story"),
                 "promoted_at": promoted_at}
        previous = self.selection.get("history", []) if self.selection else []
        self.selection = {"schema_version": STORY_RUN_SCHEMA_VERSION, **entry, "history": [*previous, entry]}
        return self.selection

    def status(self, workflow: EpisodeWorkflowEntity, run: dict[str, Any] | None) -> str:
        if not self.selection or run is None:
            return "stale"
        current = self.selection
        matches = (current["story_revision"] == workflow.revision("story")
                   and current["candidate_hash"] == fingerprint(run["candidate"])
                   and current["input_hash"] == run["input"]["input_hash"])
        return "selected" if matches else "stale"
