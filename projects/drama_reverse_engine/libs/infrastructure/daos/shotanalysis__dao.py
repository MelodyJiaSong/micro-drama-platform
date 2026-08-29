from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ShotAnalysisDao:
    index: int
    shot_size: str
    camera_angle: str
    camera_move: str
    blocking: str
    action: str
    performance: str
    scene_desc: str
    lighting: str
    mood: str
    continuous_with_prev: bool
    characters: tuple[str, ...]
    confidences: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class SpeakerAssignmentDao:
    line_index: int
    speaker: str
    dialogue_type: str  # 对白 | 内心独白 | 旁白
    confidence: float


@dataclass(frozen=True)
class EpisodeUnderstandingDao:
    narrative: str
    beats: tuple[str, ...]
    emotion_curve: str
    character_continuity: dict[str, str]
    speaker_assignments: tuple[SpeakerAssignmentDao, ...]
