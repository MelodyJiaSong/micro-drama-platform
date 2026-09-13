"""DTOs for the BGM-mux tool."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MuxOptions:
    """Knobs mirrored 1:1 from `tools/mux_av.py`'s CLI flags."""

    bgm_volume: float = 0.6
    no_loop: bool = False
    keep_source_audio: bool = False
    source_volume: float = 1.0
    duck_source: bool = False
    bgm_start: float = 0.0
    fade_in: float = 0.0
    fade_out: float = 0.0


@dataclass(frozen=True)
class MuxResult:
    """`output` is a durable absolute path the user can go open, not a temp file."""

    output: Path
    download_name: str
