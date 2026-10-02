"""Where a prop-keyed download lands (follow-up 174)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

KIND_PROP_VIEW: str = "prop_object_view"     # `props/p{N}_{名}/` — a scene object's view
KIND_PROP_MESH: str = "prop_mesh"            # `props/p{N}_{名}/mesh/p{N}.glb`


@dataclass(frozen=True)
class PropRouteDao:
    folder: Path
    kind: str
    name: str   # destination file name, extension included
