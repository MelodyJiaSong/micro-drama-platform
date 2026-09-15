from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ThumbnailQdto:
    file_path: Path
    content_type: str
    width: int
    height: int
