from __future__ import annotations

from libs.application.dtos.drama__dto import DramaTreeQdto, EpisodeStatusQdto
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader


class DramaQuery:
    """Read side of the overview tree the UI walks (drama -> children[episodes])."""

    def __init__(self, states: PipelineStateReader, artifacts: ArtifactReader) -> None:
        self._states = states
        self._artifacts = artifacts

    def tree(self) -> list[DramaTreeQdto]:
        return [self._drama_node(d) for d in self._states.list_drama_ids()]

    def _drama_node(self, drama_id: str) -> DramaTreeQdto:
        drama = self._artifacts.read_json(f"{drama_id}/drama.json")
        children = []
        for ep_dir in self._states.list_episode_dirs(drama_id):
            state = self._states.read(ep_dir) or {}
            degradations: list[str] = []
            shot_count = 0
            if self._artifacts.exists(f"{ep_dir}/compose_manifest.json"):
                manifest = self._artifacts.read_json(f"{ep_dir}/compose_manifest.json")
                degradations = manifest["degradations"]
                shot_count = len(manifest["shot_files"])
            children.append(EpisodeStatusQdto(
                episode_rel_dir=ep_dir, stage=state.get("stage", "unknown"),
                failed_reason=state.get("failed_reason"), gate_hold=bool(state.get("gate_hold")),
                busy=self._artifacts.exists(f"{ep_dir}/.worker_lock"),
                shot_count=shot_count,
                degradations=degradations,
                artifacts={
                    name: self._artifacts.exists(f"{ep_dir}/{rel}")
                    for name, rel in (("script", "script.md"), ("dialogue", "dialogue.md"),
                                      ("novel", "novel.md"), ("prompts", "all_shot_prompts.md"))
                },
            ))
        return DramaTreeQdto(
            drama_id=drama_id, title=drama["title"],
            gate_a_enabled=bool(drama.get("gate_a_enabled")),
            gate_b_enabled=bool(drama.get("gate_b_enabled")),
            children=children,
        )
