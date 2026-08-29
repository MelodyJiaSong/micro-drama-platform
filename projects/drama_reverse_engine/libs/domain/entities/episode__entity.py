from __future__ import annotations

from dataclasses import dataclass, field

from libs.common.enums import PipelineStage
from libs.common.types import DramaId, EpisodeId
from libs.domain.errors.episode__error import InvalidStageTransitionError

_ORDER: tuple[PipelineStage, ...] = (
    PipelineStage.INGEST,
    PipelineStage.EXTRACT,
    PipelineStage.ASSETS,
    PipelineStage.UNDERSTAND,
    PipelineStage.COMPOSE,
    PipelineStage.GATE_A,
    PipelineStage.GATE_B,
    PipelineStage.DONE,
)


def next_stage(stage: PipelineStage) -> PipelineStage | None:
    idx = _ORDER.index(stage)
    return _ORDER[idx + 1] if idx + 1 < len(_ORDER) else None


@dataclass
class EpisodeEntity:
    entity_id: EpisodeId
    drama_id: DramaId
    index: int
    source_rel_path: str
    stage: PipelineStage = PipelineStage.INGEST
    failed_reason: str | None = None
    gate_hold: bool = False
    ordered_stages: tuple[PipelineStage, ...] = field(default=_ORDER, repr=False)

    @property
    def is_failed(self) -> bool:
        return self.failed_reason is not None

    def advance(self) -> PipelineStage:
        if self.is_failed:
            raise InvalidStageTransitionError(f"episode {self.entity_id} is failed; retry() first")
        if self.gate_hold:
            raise InvalidStageTransitionError(f"episode {self.entity_id} is held at gate {self.stage}")
        nxt = next_stage(self.stage)
        if nxt is None:
            raise InvalidStageTransitionError(f"episode {self.entity_id} already at {self.stage}")
        self.stage = nxt
        return self.stage

    def hold_at_gate(self) -> None:
        if self.stage not in (PipelineStage.GATE_A, PipelineStage.GATE_B):
            raise InvalidStageTransitionError(f"cannot hold at non-gate stage {self.stage}")
        self.gate_hold = True

    def release_gate(self) -> None:
        self.gate_hold = False

    def fail(self, reason: str) -> None:
        self.failed_reason = reason

    def retry(self) -> None:
        self.failed_reason = None
