from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubtitleLineDao:
    text: str
    start_s: float
    end_s: float
    source: str  # "ocr" | "asr"
    confidence: float = 1.0
