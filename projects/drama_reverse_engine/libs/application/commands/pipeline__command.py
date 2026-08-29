from __future__ import annotations

import time

from libs.application.commands.assets__command import AssetsCommand
from libs.application.commands.compose__command import ComposeCommand
from libs.application.commands.extract__command import ExtractCommand
from libs.application.commands.understand__command import UnderstandCommand
from libs.common.enums import PipelineStage
from libs.domain.entities.episode__entity import EpisodeEntity
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter


class PipelineCommand:
    """FR-10: drives one episode through the reverse-engineering stage machine, one
    stage per step(). Terminal deliverables are the three text layers (script, novel,
    shot prompts). State + events live in the workspace; every step appends a job
    event (FR-10.3)."""

    def __init__(
        self, extract: ExtractCommand, assets: AssetsCommand, understand: UnderstandCommand,
        compose: ComposeCommand,
        reader: ArtifactReader, writer: ArtifactWriter,
        state_reader: PipelineStateReader, state_writer: PipelineStateWriter,
    ) -> None:
        self._extract = extract
        self._assets = assets
        self._understand = understand
        self._compose = compose
        self._reader = reader
        self._writer = writer
        self._state_reader = state_reader
        self._state_writer = state_writer

    def step(self, drama_id: str, episode_rel_dir: str) -> dict:
        state = self._state_reader.read(episode_rel_dir)
        if state is None:
            raise FileNotFoundError(f"no pipeline state at {episode_rel_dir}")
        episode = self._to_entity(drama_id, episode_rel_dir, state)
        if episode.is_failed or state["gate_hold"] or episode.stage is PipelineStage.DONE:
            return state
        self._state_writer.heartbeat(episode_rel_dir)
        drama = self._reader.read_json(f"{drama_id}/drama.json")
        started = time.time()
        try:
            detail = self._run_stage(drama_id, episode_rel_dir, episode.stage, drama, state)
            if state.get("gate_hold"):
                state.update(failed_reason=None)  # held at the gate; release() advances past it
            else:
                episode.advance()
                state.update(stage=episode.stage.value, failed_reason=None)
        except Exception as exc:
            episode.fail(f"{type(exc).__name__}: {exc}")
            state.update(failed_reason=episode.failed_reason)
            detail = {"error": episode.failed_reason}
        self._state_writer.write(episode_rel_dir, state)
        self._event(drama_id, episode_rel_dir, episode.stage.value, started, detail)
        return state

    def run_to_completion(self, drama_id: str, episode_rel_dir: str, max_steps: int = 16) -> dict:
        state = self._state_reader.read(episode_rel_dir) or {}
        for _ in range(max_steps):
            new_state = self.step(drama_id, episode_rel_dir)
            if new_state == state and (new_state.get("failed_reason") or new_state.get("gate_hold")):
                break
            state = new_state
            if state.get("stage") == PipelineStage.DONE.value:
                break
        return state

    def rerun_stage(self, drama_id: str, episode_rel_dir: str, stage: str) -> dict:
        """FR-10.1: forced rerun rewinds the state machine to the named stage; the
        stage command's force=True path recomputes its artifacts."""
        state = self._state_reader.read(episode_rel_dir)
        if state is None:
            raise FileNotFoundError(episode_rel_dir)
        state.update(stage=stage, failed_reason=None, force_next=True)
        self._state_writer.write(episode_rel_dir, state)
        return self.step(drama_id, episode_rel_dir)

    def _run_stage(self, drama_id: str, episode_rel_dir: str, stage: PipelineStage,
                   drama: dict, state: dict) -> dict:
        force = state.pop("force_next", False)
        if stage is PipelineStage.INGEST:
            return {"note": "source registered at upload time"}
        if stage is PipelineStage.EXTRACT:
            r = self._extract.run(episode_rel_dir, force=force)
            return {"shots": r.shot_count, "flagged_lines": r.flagged_line_count, "degradations": r.degradations}
        if stage is PipelineStage.ASSETS:
            r = self._assets.build_reference_library(drama_id, [episode_rel_dir], force=force)
            return {"characters": r.character_count, "degradations": r.degradations}
        if stage is PipelineStage.UNDERSTAND:
            r = self._understand.run(drama_id, episode_rel_dir, force=force)
            return {"low_confidence": r.low_confidence_count, "speaker_low": r.speaker_low_confidence_count}
        if stage is PipelineStage.COMPOSE:
            r = self._compose.run(drama_id, episode_rel_dir, force=force or state.pop("needs_recompose", False))
            return {"shot_files": len(r.shot_files), "degradations": r.degradations}
        if stage is PipelineStage.GATE_A:
            if drama.get("gate_a_enabled"):
                state["gate_hold"] = True
            return {"gate": "A", "held": bool(drama.get("gate_a_enabled"))}
        if stage is PipelineStage.GATE_B:
            if drama.get("gate_b_enabled"):
                state["gate_hold"] = True
            return {"gate": "B", "held": bool(drama.get("gate_b_enabled"))}
        raise RuntimeError(f"no runner for stage {stage}")

    def _to_entity(self, drama_id: str, episode_rel_dir: str, state: dict) -> EpisodeEntity:
        index = int(episode_rel_dir.rsplit("ep", 1)[-1])
        entity = EpisodeEntity(entity_id=episode_rel_dir, drama_id=drama_id, index=index,
                               source_rel_path=f"{episode_rel_dir}/source.mp4",
                               stage=PipelineStage(state["stage"]),
                               failed_reason=state.get("failed_reason"))
        entity.gate_hold = bool(state.get("gate_hold"))
        return entity

    def _event(self, drama_id: str, episode_rel_dir: str, stage: str, started: float, detail: dict) -> None:
        self._writer.append_jsonl(f"{drama_id}/job_events.jsonl", {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "episode": episode_rel_dir, "stage": stage,
            "elapsed_s": round(time.time() - started, 2), "detail": detail,
        })
