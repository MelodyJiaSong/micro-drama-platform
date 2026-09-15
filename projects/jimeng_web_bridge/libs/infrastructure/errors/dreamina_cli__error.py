from __future__ import annotations

from enum import Enum


class DreaminaFailureKind(str, Enum):
    NOT_LOGGED_IN = "not_logged_in"
    COMPLIANCE_CONFIRMATION_REQUIRED = "compliance_confirmation_required"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    EXECUTABLE_REJECTED = "executable_rejected"
    UNPARSEABLE_OUTPUT = "unparseable_output"
    UNKNOWN = "unknown"


class DreaminaCliError(Exception):
    def __init__(self, kind: DreaminaFailureKind, message: str, exit_code: int | None, output_tail: str) -> None:
        super().__init__(f"{kind.value}: {message}")
        self.kind = kind
        self.exit_code = exit_code
        self.output_tail = output_tail
