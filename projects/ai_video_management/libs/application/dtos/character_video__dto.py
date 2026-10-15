"""Character-video aggregate DTOs: view + audio + trim extraction results
(single turntable and the whole-drama batch). Renamed from the former
`character_video__cdto.py`."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CharacterViewCdto:
    timestamp: float
    role: str
    path: str

    def to_payload(self) -> dict[str, Any]:
        return {"timestamp": self.timestamp, "role": self.role, "path": self.path}


@dataclass(frozen=True)
class CharacterAudioCdto:
    path: str

    def to_payload(self) -> dict[str, Any]:
        return {"path": self.path}


@dataclass(frozen=True)
class CharacterTrimCdto:
    path: str
    duration_seconds: float

    def to_payload(self) -> dict[str, Any]:
        return {"path": self.path, "duration_seconds": self.duration_seconds}


@dataclass(frozen=True)
class CharacterViewFailureCdto:
    target: str
    error: str

    def to_payload(self) -> dict[str, Any]:
        return {"target": self.target, "error": self.error}


@dataclass(frozen=True)
class ExtractCharacterViewsResultCdto:
    src_rel: str
    views: tuple[CharacterViewCdto, ...]
    audio: CharacterAudioCdto | None
    trim: CharacterTrimCdto | None
    failures: tuple[CharacterViewFailureCdto, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "src": self.src_rel,
            "views": [v.to_payload() for v in self.views],
            "audio": self.audio.to_payload() if self.audio is not None else None,
            "trim": self.trim.to_payload() if self.trim is not None else None,
            "failures": [f.to_payload() for f in self.failures],
        }


@dataclass(frozen=True)
class ExtractAllCharacterViewsItemCdto:
    folder: str
    status: str  # "ok" | "skipped" | "error"
    result: ExtractCharacterViewsResultCdto | None
    reason: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "folder": self.folder,
            "status": self.status,
            "result": self.result.to_payload() if self.result is not None else None,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ExtractAllCharacterViewsResultCdto:
    characters_dir: str
    items: tuple[ExtractAllCharacterViewsItemCdto, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "characters_dir": self.characters_dir,
            "items": [i.to_payload() for i in self.items],
        }
