from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactDao:
    path: Path
    size_bytes: int
    width: int
    height: int
