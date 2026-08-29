from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExportFileCdto:
    rel_path: str
    filename: str
    media_type: str
