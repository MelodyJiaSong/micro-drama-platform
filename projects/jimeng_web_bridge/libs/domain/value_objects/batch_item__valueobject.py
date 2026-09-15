from dataclasses import dataclass

from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.precheck_result__valueobject import PrecheckResult


@dataclass(frozen=True)
class BatchItem:
    index: int
    request: GenerationRequest
    precheck: PrecheckResult
    fingerprint: Fingerprint

    def __post_init__(self) -> None:
        if self.fingerprint != Fingerprint.of(self.request):
            raise InvalidRequestError(f"批次条目 {self.index} 的 fingerprint 与内容不一致")

    @classmethod
    def of(cls, index: int, request: GenerationRequest, precheck: PrecheckResult) -> "BatchItem":
        return cls(index=index, request=request, precheck=precheck, fingerprint=Fingerprint.of(request))

    @property
    def spends_credits(self) -> bool:
        return self.precheck.existing_job_id is None

    def canonical(self) -> dict[str, object]:
        source = self.request.source
        return {
            "index": self.index,
            "fingerprint": self.fingerprint.value,
            "source": {"type": source.type.value, "path": source.path, "block_key": source.block_key},
            "credits": self.precheck.estimate.credits,
            "existing_job_id": self.precheck.existing_job_id,
        }
