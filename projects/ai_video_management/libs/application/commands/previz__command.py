"""Previz-aggregate commands: start / cancel an MP4 render of a previz `.blend`.

Rendering is deliberately decoupled from authoring the `.blend`: the build
script is cheap and re-run constantly while a shot is tuned, the render is
15–30 minutes and only worth paying once. This command is the "now render it"
trigger — nothing here touches the `.blend`'s contents.
"""
from __future__ import annotations

from libs.application.dtos.previz__dto import PrevizStatusQdto
from libs.application.mappers.previz__mapper import PrevizMapper
from libs.infrastructure.writers.previz__writer import PrevizRenderer


class PrevizCommand:
    def __init__(self, renderer: PrevizRenderer) -> None:
        self._renderer = renderer

    def render(self, rel_path: str) -> PrevizStatusQdto:
        return PrevizMapper.to_qdto(self._renderer.start(rel_path))

    def cancel(self, rel_path: str) -> PrevizStatusQdto:
        return PrevizMapper.to_qdto(self._renderer.cancel(rel_path))
