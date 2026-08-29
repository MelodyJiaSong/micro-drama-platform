from __future__ import annotations

from typing import Protocol

from libs.common.types import DramaId, EpisodeId
from libs.domain.entities.episode__entity import EpisodeEntity


class EpisodeRepository(Protocol):
    def get(self, episode_id: EpisodeId) -> EpisodeEntity | None: ...

    def save(self, episode: EpisodeEntity) -> None: ...

    def list_for_drama(self, drama_id: DramaId) -> list[EpisodeEntity]: ...
