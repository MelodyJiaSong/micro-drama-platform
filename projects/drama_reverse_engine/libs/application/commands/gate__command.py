from __future__ import annotations

import time

from libs.common.enums import PipelineStage
from libs.domain.entities.episode__entity import next_stage
from libs.domain.errors.episode__error import InvalidStageTransitionError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter

_GATE_STAGES = (PipelineStage.GATE_A.value, PipelineStage.GATE_B.value)
_RECOMPOSE_TRIGGERS = ("dialogue.json", "script.md", "dialogue.md")


class GateCommand:
    """FR-6: gate release + versioned artifact editing with downstream dirty marking."""

    def __init__(self, reader: PipelineStateReader, states: PipelineStateWriter,
                 writer: ArtifactWriter, artifacts: ArtifactReader, workspace: SafeWorkspace) -> None:
        self._reader = reader
        self._states = states
        self._writer = writer
        self._artifacts = artifacts
        self._workspace = workspace

    def release(self, episode_rel_dir: str) -> dict:
        state = self._reader.read(episode_rel_dir)
        if state is None or state["stage"] not in _GATE_STAGES or not state["gate_hold"]:
            raise InvalidStageTransitionError(f"{episode_rel_dir} is not held at a gate")
        state.update(gate_hold=False, stage=next_stage(PipelineStage(state["stage"])).value)
        self._states.write(episode_rel_dir, state)
        return state

    def edit_artifact(self, episode_rel_dir: str, artifact_rel_path: str, content: str) -> dict:
        """FR-6.4: previous version preserved under .versions/; edits to dialogue/script
        mark compose dirty (FR-6.1) so the next compose pass regenerates prompts."""
        if not self._workspace.within(episode_rel_dir, artifact_rel_path) or artifact_rel_path == episode_rel_dir:
            raise InvalidStageTransitionError("artifact must resolve inside the episode directory")
        stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
        name = artifact_rel_path.rsplit("/", 1)[-1]
        version_rel = f"{episode_rel_dir}/.versions/{stamp}-{name}"
        if self._artifacts.exists(artifact_rel_path):
            self._writer.write_text(version_rel, self._artifacts.read_text(artifact_rel_path))
        self._writer.write_text(artifact_rel_path, content)
        state = self._reader.read(episode_rel_dir)
        dirty = any(name == trigger for trigger in _RECOMPOSE_TRIGGERS)
        if state is not None and dirty:
            state["needs_recompose"] = True
            self._states.write(episode_rel_dir, state)
        return {"versioned_as": version_rel, "needs_recompose": dirty}
