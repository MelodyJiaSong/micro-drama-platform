"""Previz-aggregate query: poll the render job's progress."""
from __future__ import annotations

from libs.application.dtos.previz__dto import PrevizStatusQdto
from libs.application.mappers.previz__mapper import PrevizMapper
from libs.infrastructure.writers.previz__writer import PrevizRenderer


class PrevizQuery:
    def __init__(self, renderer: PrevizRenderer) -> None:
        self._renderer = renderer

    def status(self, rel_path: str) -> PrevizStatusQdto:
        return PrevizMapper.to_qdto(self._renderer.status(rel_path))
