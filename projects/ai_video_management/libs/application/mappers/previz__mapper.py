"""Previz-aggregate mapper: PrevizJobSnapshot (domain VO) → PrevizStatusQdto."""
from __future__ import annotations

import time

from libs.application.dtos.previz__dto import PrevizStatusQdto
from libs.domain.value_objects.previz__valueobject import PrevizJobSnapshot


class PrevizMapper:
    @staticmethod
    def to_qdto(job: PrevizJobSnapshot) -> PrevizStatusQdto:
        end = job.finished_at if job.finished_at is not None else time.time()
        elapsed = int(end - job.started_at) if job.started_at > 0.0 else 0
        return PrevizStatusQdto(
            blend=job.blend_rel,
            state=job.state,
            rendered_frames=job.rendered_frames,
            total_frames=job.total_frames,
            percent=job.percent,
            message=job.message,
            mp4=job.mp4_rel,
            elapsed_seconds=elapsed,
        )
