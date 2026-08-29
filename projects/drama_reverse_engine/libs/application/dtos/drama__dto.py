from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DramaCdto:
    drama_id: str
    title: str


@dataclass(frozen=True)
class EpisodeStatusQdto:
    episode_rel_dir: str
    stage: str
    failed_reason: str | None
    gate_hold: bool
    busy: bool = False
    shot_count: int = 0
    degradations: list[str] = field(default_factory=list)
    artifacts: dict[str, bool] = field(default_factory=dict)


@dataclass(frozen=True)
class DramaTreeQdto:
    drama_id: str
    title: str
    gate_a_enabled: bool
    gate_b_enabled: bool
    children: list[EpisodeStatusQdto] = field(default_factory=list)
