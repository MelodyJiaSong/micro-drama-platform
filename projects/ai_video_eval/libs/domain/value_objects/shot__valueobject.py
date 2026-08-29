import hashlib
import re
from dataclasses import dataclass, field

from libs.common.constants import (
    COMBAT_HINTS,
    SEAM_HARD_CUT,
    SEAM_LAST_FRAME,
    SEAM_MOTION,
    VFX_HINTS,
)
from libs.common.enums import SubType


@dataclass(frozen=True)
class DialogueLine:
    speaker: str
    dtype: str
    text: str


@dataclass(frozen=True)
class VoiceBlock:
    speaker: str
    timbre: str
    emotion: str
    speed: str
    vtype: str
    line: str
    duration_target_s: float | None
    raw: str


@dataclass(frozen=True)
class ShotUnit:
    project: str
    sub_type: SubType
    ep: str | None
    shot_id: str
    path: str
    raw_text: str
    title: str
    novel_excerpt: str
    shot_context: dict[str, str] = field(compare=False)
    prompt_title: str = ""
    prompt_fields: dict[str, str] = field(default_factory=dict, compare=False)
    prompt_body: str = ""
    voice_blocks: tuple[VoiceBlock, ...] = ()
    dialogue_lines: tuple[DialogueLine, ...] = ()
    duration_s: float | None = None
    aspect_ratio: str | None = None
    index_in_scope: int = 0
    total_in_scope: int = 1

    @property
    def unit_id(self) -> str:
        return f"{self.project}/{self.ep or 'flat'}/{self.shot_id}"

    @property
    def unit_hash(self) -> str:
        return hashlib.sha256(self.raw_text.encode("utf-8")).hexdigest()

    @property
    def has_dialogue(self) -> bool:
        return len(self.dialogue_lines) > 0

    @property
    def dialogue_types(self) -> frozenset[str]:
        return frozenset(line.dtype for line in self.dialogue_lines)

    @property
    def seam_mode(self) -> str:
        seam = self.shot_context.get("衔接", "")
        if seam.startswith(SEAM_MOTION) or seam.startswith("运动"):
            return SEAM_MOTION
        if seam.startswith("承接"):
            return SEAM_LAST_FRAME
        return SEAM_HARD_CUT

    @property
    def has_combat(self) -> bool:
        haystack = self.prompt_fields.get("动作", "") + self.prompt_fields.get("情节", "")
        return any(hint in haystack for hint in COMBAT_HINTS)

    @property
    def has_vfx(self) -> bool:
        return any(hint in self.prompt_body for hint in VFX_HINTS)

    @property
    def prompt_char_count(self) -> int:
        return len(re.sub(r"\s+", "", self.prompt_body.strip()))

    def applicability_vars(self) -> dict[str, object]:
        return {
            "sub_type": self.sub_type.value,
            "has_dialogue": self.has_dialogue,
            "dialogue_types": set(self.dialogue_types),
            "seam_mode": self.seam_mode,
            "has_combat": self.has_combat,
            "has_vfx": self.has_vfx,
            "is_first_shot": self.index_in_scope == 0,
            "is_last_shot": self.index_in_scope == self.total_in_scope - 1,
            "has_prev_shot": self.index_in_scope > 0,
            "has_next_shot": self.index_in_scope < self.total_in_scope - 1,
        }
