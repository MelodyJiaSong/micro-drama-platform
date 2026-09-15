from __future__ import annotations

from collections.abc import Sequence

from libs.application.mappers.job__mapper import JobMapper
from libs.common.clock import Clock
from libs.common.enums import JobState
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.infrastructure.daos.job__dao import JobDao
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.writers.job__writer import JobWriter

# SQLite treats a negative LIMIT as "no limit".
_ALL_ROWS: int = -1


class SqliteJobRepository:
    """Implements domain `JobRepository`. Transitions are append-only: a save writes only the entity's records
    beyond those already stored (the synthetic creation row has no `from_state` and is not part of the entity)."""

    def __init__(
        self, reader: JobReader, writer: JobWriter, mapper: JobMapper, tree: DramaTreeReader, clock: Clock
    ) -> None:
        self._reader: JobReader = reader
        self._writer: JobWriter = writer
        self._mapper: JobMapper = mapper
        self._tree: DramaTreeReader = tree
        self._clock: Clock = clock

    def get(self, job_id: str) -> GenerationJobEntity | None:
        dao: JobDao | None = self._reader.get(job_id)
        return None if dao is None else self._mapper.to_entity(dao, self._reader.transitions(job_id))

    def save(self, job: GenerationJobEntity) -> None:
        existing: JobDao | None = self._reader.get(job.job_id)
        persisted = [] if existing is None else self._reader.transitions(job.job_id)
        drama_rel: str | None = (
            self._tree.drama_root_of(job.request.source.path) if existing is None else existing.drama_rel
        )
        now = self._clock.now()
        self._writer.save(
            self._mapper.to_dao(job, existing, drama_rel, now), self._mapper.new_transitions(job, persisted, now)
        )

    def list_by_batch(self, batch_id: str) -> list[GenerationJobEntity]:
        daos, _ = self._reader.list(None, batch_id, None, None, _ALL_ROWS, 0)
        return self._entities(daos)

    def list_in_states(self, states: frozenset[JobState]) -> list[GenerationJobEntity]:
        if not states:
            return []
        daos, _ = self._reader.list(sorted(state.value for state in states), None, None, None, _ALL_ROWS, 0)
        return self._entities(daos)

    def find_by_fingerprint(self, fingerprint: Fingerprint) -> list[GenerationJobEntity]:
        return self._entities(self._reader.find_by_fingerprint(fingerprint.value))

    def _entities(self, daos: Sequence[JobDao]) -> list[GenerationJobEntity]:
        return [self._mapper.to_entity(dao, self._reader.transitions(dao.job_id)) for dao in daos]
