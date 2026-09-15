from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from libs.common.enums import BackendKind, GenerationKind, RefKind, SourceType
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem


class RequestJsonMapper:
    """GenerationRequest / FrozenRequest ↔ JSON-ready dicts, shared by the job and batch stores."""

    def request_to_dict(self, request: GenerationRequest) -> dict[str, object]:
        return {
            "kind": request.kind.value,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "references": [
                {
                    "name": ref.name,
                    "label": ref.label,
                    "kind": ref.kind.value,
                    "resolved_path": ref.resolved_path,
                    "entity_name": ref.entity_name,
                    "sha256": ref.sha256,
                }
                for ref in request.references
            ],
            "params": None if request.params is None else request.params.canonical(),
            "output_slot": request.output_slot,
            "source": {
                "type": request.source.type.value,
                "path": request.source.path,
                "block_key": request.source.block_key,
            },
            "entity_name": request.entity_name,
        }

    def request_from_dict(self, data: Mapping[str, Any]) -> GenerationRequest:
        params: Mapping[str, Any] | None = data["params"]
        source: Mapping[str, Any] = data["source"]
        return GenerationRequest(
            kind=GenerationKind(data["kind"]),
            prompt=data["prompt"],
            negative_prompt=data["negative_prompt"],
            references=tuple(
                ReferenceItem(
                    name=ref["name"],
                    label=ref["label"],
                    kind=RefKind(ref["kind"]),
                    resolved_path=ref["resolved_path"],
                    entity_name=ref["entity_name"],
                    sha256=ref["sha256"],
                )
                for ref in data["references"]
            ),
            params=None if params is None else GenerationParams(**params),
            output_slot=data["output_slot"],
            source=RequestSource(SourceType(source["type"]), source["path"], source["block_key"]),
            entity_name=data["entity_name"],
        )

    def frozen_to_dict(self, frozen: FrozenRequest) -> dict[str, object]:
        return {
            "request": self.request_to_dict(frozen.request),
            "backend": frozen.backend.value,
            "config_digest": frozen.config_digest,
            "credits_estimated": frozen.credits_estimated,
            "estimate_tolerance_pct": frozen.estimate_tolerance_pct,
            "fingerprint": frozen.fingerprint.value,
        }

    def frozen_from_dict(self, data: Mapping[str, Any]) -> FrozenRequest:
        return FrozenRequest(
            request=self.request_from_dict(data["request"]),
            backend=BackendKind(data["backend"]),
            config_digest=data["config_digest"],
            credits_estimated=data["credits_estimated"],
            estimate_tolerance_pct=data["estimate_tolerance_pct"],
            fingerprint=Fingerprint(data["fingerprint"]),
        )

    @staticmethod
    def parse_iso(text: str) -> datetime:
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)
