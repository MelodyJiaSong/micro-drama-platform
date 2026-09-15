from typing import Protocol

from libs.common.enums import JobState
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint


class JobRepository(Protocol):
    def get(self, job_id: str) -> GenerationJobEntity | None: ...

    def save(self, job: GenerationJobEntity) -> None: ...

    def list_by_batch(self, batch_id: str) -> list[GenerationJobEntity]: ...

    def list_in_states(self, states: frozenset[JobState]) -> list[GenerationJobEntity]: ...

    def find_by_fingerprint(self, fingerprint: Fingerprint) -> list[GenerationJobEntity]: ...
