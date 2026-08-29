from __future__ import annotations

from enum import Enum


class PipelineStage(str, Enum):
    INGEST = "ingest"
    EXTRACT = "extract"
    ASSETS = "assets"
    UNDERSTAND = "understand"
    COMPOSE = "compose"
    GATE_A = "gate_a"
    GATE_B = "gate_b"
    DONE = "done"


class DialogueType(str, Enum):
    DIALOGUE = "对白"
    OS = "内心独白"
    NARRATION = "旁白"


class ShotLink(str, Enum):
    CONTINUE = "承接"
    HARD_CUT = "硬切"


class GateId(str, Enum):
    GATE_A = "gate_a"
    GATE_B = "gate_b"


class Severity(str, Enum):
    CRITICAL = "critical"
    BLOCKER = "blocker"
    WARNING = "warning"
