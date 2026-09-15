from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from libs.common.canonical_json import sha256_hex
from libs.common.enums import GenerationKind, RefKind, SourceType
from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem

_SOURCES_BY_KIND: Mapping[GenerationKind, frozenset[SourceType]] = MappingProxyType({
    GenerationKind.VIDEO: frozenset({SourceType.RAW, SourceType.SHOT, SourceType.ASSET_VIDEO}),
    GenerationKind.IMAGE: frozenset({SourceType.RAW, SourceType.ASSET_IMAGE}),
    GenerationKind.ENTITY: frozenset({SourceType.ENTITY_CREATE}),
})


@dataclass(frozen=True)
class RequestSource:
    type: SourceType
    path: str
    block_key: str | None = None


@dataclass(frozen=True)
class GenerationRequest:
    kind: GenerationKind
    prompt: str
    negative_prompt: str | None
    references: tuple[ReferenceItem, ...]
    params: GenerationParams | None
    output_slot: str
    source: RequestSource
    entity_name: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.references, tuple):
            raise InvalidRequestError("references 必须是有序 tuple")
        if not self.output_slot:
            raise InvalidRequestError("output_slot 不能为空")
        if self.source.type not in _SOURCES_BY_KIND[self.kind]:
            raise InvalidRequestError(f"{self.kind} 请求不能来自 {self.source.type}")
        if self.kind is GenerationKind.ENTITY:
            self._check_entity_create()
        else:
            if self.params is None:
                raise InvalidRequestError(f"{self.kind} 请求必须带 params")
            if self.entity_name is not None:
                raise InvalidRequestError("只有 entity_create 请求可以带 entity_name")

    def _check_entity_create(self) -> None:
        if not self.entity_name:
            raise InvalidRequestError("entity_create 请求必须带 entity_name")
        if self.params is not None:
            raise InvalidRequestError("entity_create 请求不带 params")
        if any(ref.kind is not RefKind.IMAGE for ref in self.references):
            raise InvalidRequestError("entity_create 的参考项只能是图片")

    def prompt_sha256(self) -> str:
        return sha256_hex(self.prompt)

    def negative_prompt_sha256(self) -> str | None:
        return None if self.negative_prompt is None else sha256_hex(self.negative_prompt)

    def prompt_codepoints(self) -> int:
        return len(self.prompt)

    @property
    def entity_references(self) -> tuple[ReferenceItem, ...]:
        return tuple(ref for ref in self.references if ref.is_entity)

    @property
    def upload_references(self) -> tuple[ReferenceItem, ...]:
        return tuple(ref for ref in self.references if not ref.is_entity)

    @property
    def mentioned_entity_names(self) -> tuple[str, ...]:
        return tuple(ref.entity_name for ref in self.references if ref.entity_name is not None)
