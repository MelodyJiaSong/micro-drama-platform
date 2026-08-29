from __future__ import annotations

from dataclasses import dataclass

from libs.common.constants import DEFAULT_ASPECT, DEFAULT_RESOLUTION, DEFAULT_TENANT
from libs.common.types import DramaId


@dataclass
class DramaEntity:
    entity_id: DramaId
    title: str
    tenant_id: str = DEFAULT_TENANT
    gate_a_enabled: bool = False
    gate_b_enabled: bool = False
    resolution: str = DEFAULT_RESOLUTION
    aspect: str = DEFAULT_ASPECT
    authorization_stub_rel_path: str | None = None

    @property
    def is_authorized(self) -> bool:
        return self.authorization_stub_rel_path is not None
