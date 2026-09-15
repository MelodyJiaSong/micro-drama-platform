from __future__ import annotations

import re

from libs.common.enums import PauseReason, RemoteStatus
from libs.infrastructure.errors.dreamina_cli__error import DreaminaFailureKind

RESOLUTION_TYPES: tuple[str, ...] = ("2k", "4k")
KNOWN_GEN_STATUSES: frozenset[str] = frozenset({"success", "fail", "failed", "querying"})

_MODEL_RE = re.compile(r"(?:seedream)?(\d+\.\d+)")
_RATIO_RE = re.compile(r"[1-9]\d*:[1-9]\d*")
_VERSION_RE = re.compile(r"v?(\d+)\.(\d+)(?:\.(\d+))?(?:[-+][0-9A-Za-z.\-]*)?")
_QUEUE_REASONS: dict[DreaminaFailureKind, PauseReason] = {
    DreaminaFailureKind.NOT_LOGGED_IN: PauseReason.CLI_LOGIN_REQUIRED,
    DreaminaFailureKind.COMPLIANCE_CONFIRMATION_REQUIRED: PauseReason.COMPLIANCE_CONFIRMATION_REQUIRED,
}
_TRANSIENT_KINDS: frozenset[DreaminaFailureKind] = frozenset(
    {DreaminaFailureKind.TIMEOUT, DreaminaFailureKind.UNPARSEABLE_OUTPUT}
)


class DreaminaMapper:
    """Bridge vocabulary ↔ `dreamina` CLI vocabulary (spec v2 FR-38 / FR-21; model keys per unit A-10)."""

    @staticmethod
    def model_version(model: str) -> str | None:
        match = _MODEL_RE.fullmatch(model.lower())
        return None if match is None else match.group(1)

    @staticmethod
    def ratio(ratio: str) -> str | None:
        return ratio if _RATIO_RE.fullmatch(ratio) else None

    @staticmethod
    def resolution_type(resolution: str) -> str | None:
        lowered = resolution.lower()
        return lowered if lowered in RESOLUTION_TYPES else None

    @staticmethod
    def remote_status(gen_status: str | None) -> RemoteStatus:
        if gen_status == "success":
            return RemoteStatus.SUCCEEDED
        if gen_status in ("fail", "failed"):
            return RemoteStatus.FAILED
        return RemoteStatus.GENERATING

    @staticmethod
    def is_known_status(gen_status: str | None) -> bool:
        return gen_status in KNOWN_GEN_STATUSES

    @staticmethod
    def queue_reason(kind: DreaminaFailureKind) -> PauseReason | None:
        return _QUEUE_REASONS.get(kind)

    @staticmethod
    def failure_reason(kind: DreaminaFailureKind) -> PauseReason:
        return _QUEUE_REASONS.get(kind, PauseReason.CLI_ERROR)

    @staticmethod
    def is_transient(kind: DreaminaFailureKind) -> bool:
        return kind in _TRANSIENT_KINDS

    @staticmethod
    def parse_version(text: str) -> tuple[int, int, int] | None:
        match = _VERSION_RE.fullmatch(text.strip())
        if match is None:
            return None
        return int(match.group(1)), int(match.group(2)), int(match.group(3) or 0)

    @staticmethod
    def version_below(actual: str, minimum: str) -> bool | None:
        have = DreaminaMapper.parse_version(actual)
        need = DreaminaMapper.parse_version(minimum)
        return None if have is None or need is None else have < need
