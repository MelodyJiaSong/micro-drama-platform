from __future__ import annotations

from collections.abc import Callable

from libs.application.dtos.candidate__dto import ArchivedFileCdto, PromoteCdto
from libs.common.clock import Clock
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.writers.output__writer import OutputWriter, timestamp_label


class CandidateCommand:
    """Promotes a `_candidates/{key}/` file to `{subject_dir}/{key}.{ext}` (FR-43, FR-44). No credits are spent."""

    def __init__(
        self,
        output_writer: OutputWriter,
        drama_config_provider: Callable[[str], DramaConfig],
        global_config_provider: Callable[[], GlobalConfig],
        clock: Clock,
    ) -> None:
        self._output_writer = output_writer
        self._drama_config_provider = drama_config_provider
        self._global_config_provider = global_config_provider
        self._clock = clock

    def promote(self, candidate_rel: str) -> PromoteCdto:
        on_existing = self._drama_config_provider(candidate_rel).outputs.on_existing
        label = timestamp_label(self._clock.now(), self._global_config_provider().time.timezone)
        promoted = self._output_writer.promote(candidate_rel, on_existing, label)
        return PromoteCdto(
            candidate_rel=promoted.candidate_rel,
            target_rel=promoted.target_rel,
            sidecar_rel=promoted.sidecar_rel,
            sha256=promoted.sha256,
            size=promoted.size,
            archived=tuple(ArchivedFileCdto(item.from_rel, item.to_rel) for item in promoted.archived),
        )
