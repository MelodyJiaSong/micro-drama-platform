from collections.abc import Mapping
from dataclasses import dataclass

from libs.common.enums import BackendKind
from libs.domain.errors.precheck__error import FrozenRequestIncompleteError
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem


@dataclass(frozen=True)
class FrozenRequest:
    request: GenerationRequest
    backend: BackendKind
    config_digest: str
    credits_estimated: int | None
    estimate_tolerance_pct: int
    fingerprint: Fingerprint

    def __post_init__(self) -> None:
        if not self.config_digest:
            raise FrozenRequestIncompleteError("冻结请求必须带 config digest")
        if self.credits_estimated is not None and (isinstance(self.credits_estimated, bool) or self.credits_estimated < 0):
            raise FrozenRequestIncompleteError("冻结的预计积分必须是非负整数")
        if isinstance(self.estimate_tolerance_pct, bool) or not 0 <= self.estimate_tolerance_pct <= 100:
            raise FrozenRequestIncompleteError("冻结的积分容差必须在 0–100 之间")
        for ref in self.request.upload_references:
            if ref.resolved_path is None or ref.sha256 is None:
                raise FrozenRequestIncompleteError(f"参考项 {ref.name} 未解析出文件或 sha256，不能冻结")
        if self.fingerprint != Fingerprint.of(self.request):
            raise FrozenRequestIncompleteError("冻结请求的 fingerprint 与内容不一致")

    @classmethod
    def freeze(
        cls,
        request: GenerationRequest,
        backend: BackendKind,
        config_digest: str,
        credits_estimated: int | None,
        estimate_tolerance_pct: int,
    ) -> "FrozenRequest":
        return cls(request, backend, config_digest, credits_estimated, estimate_tolerance_pct, Fingerprint.of(request))

    @classmethod
    def from_item(cls, item: BatchItem, backend: BackendKind, config_digest: str, estimate_tolerance_pct: int) -> "FrozenRequest":
        return cls.freeze(item.request, backend, config_digest, item.precheck.estimate.credits, estimate_tolerance_pct)

    @property
    def entity_names(self) -> tuple[str, ...]:
        return self.request.mentioned_entity_names

    def changed_references(self, current_sha256_by_path: Mapping[str, str | None]) -> tuple[ReferenceItem, ...]:
        return tuple(
            ref
            for ref in self.request.upload_references
            if ref.resolved_path is None or current_sha256_by_path.get(ref.resolved_path) != ref.sha256
        )
