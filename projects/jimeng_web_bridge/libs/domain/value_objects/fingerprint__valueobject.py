import re
from dataclasses import dataclass

from libs.common.canonical_json import canonical_sha256
from libs.common.enums import GenerationKind
from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Fingerprint:
    value: str

    def __post_init__(self) -> None:
        if not _HEX64.match(self.value):
            raise InvalidRequestError("fingerprint 必须是 64 位小写十六进制")

    @classmethod
    def of(cls, request: GenerationRequest) -> "Fingerprint":
        body: dict[str, object] = {
            "kind": request.kind.value,
            "prompt_sha256": request.prompt_sha256(),
            "negative_prompt_sha256": request.negative_prompt_sha256(),
            "references": [ref.canonical() for ref in request.references],
            "params": None if request.params is None else request.params.canonical(),
            "output_slot": request.output_slot,
        }
        if request.kind is GenerationKind.ENTITY:
            body["entity_name"] = request.entity_name
        return cls(canonical_sha256(body))

    def __str__(self) -> str:
        return self.value
