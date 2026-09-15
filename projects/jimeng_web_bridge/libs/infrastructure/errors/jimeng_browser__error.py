from __future__ import annotations

from enum import StrEnum

from libs.common.enums import PauseReason


class LaunchFailureKind(StrEnum):
    PROFILE_IN_USE = "profile_in_use"
    BROWSER_MISSING = "browser_missing"
    LAUNCH_TIMEOUT = "launch_timeout"
    UNSAFE_START_URL = "unsafe_start_url"
    LAUNCH_FAILED = "launch_failed"


class StepFailureKind(StrEnum):
    SELECTOR_MISSING = "selector_missing"
    READBACK_MISMATCH = "readback_mismatch"
    UPLOAD_REJECTED = "upload_rejected"
    REAL_FACE_REJECTED = "real_face_rejected"
    UPLOAD_TIMEOUT = "upload_timeout"
    CAPTCHA_OR_RISK = "captcha_or_risk"
    LOGIN_REQUIRED = "login_required"
    INSUFFICIENT_CREDIT = "insufficient_credit"
    RECORD_NOT_FOUND = "record_not_found"
    DOWNLOAD_FAILED = "download_failed"
    RESPONSE_TIMEOUT = "response_timeout"
    ENTITY_FORM_FAILED = "entity_form_failed"
    PAGE_ERROR = "page_error"


class JimengBrowserError(Exception):
    pass


class BrowserLaunchError(JimengBrowserError):
    def __init__(self, kind: LaunchFailureKind, detail: str) -> None:
        super().__init__(f"{kind.value}: {detail}")
        self.kind = kind
        self.detail = detail


class BrowserNotStartedError(JimengBrowserError):
    pass


class BrowserLostError(JimengBrowserError):
    def __init__(self, reason: str) -> None:
        super().__init__(f"browser lost: {reason}")
        self.reason = reason


class BrowserCommandTimeoutError(JimengBrowserError):
    pass


class FillPlanError(JimengBrowserError):
    """The prompt has no `{name}({label})=>@` marker for a reference, so no mention position exists."""


class PageStepError(JimengBrowserError):
    def __init__(self, kind: StepFailureKind, step: str, detail: str = "") -> None:
        super().__init__(f"{kind.value} at {step}: {detail}" if detail else f"{kind.value} at {step}")
        self.kind = kind
        self.step = step
        self.detail = detail


class WebBackendError(Exception):
    """Raised by the web backend where the port has no error slot (download, entity gateway).

    `retryable` says whether the caller's retry budget applies before pausing with `reason`.
    """

    def __init__(self, reason: PauseReason, retryable: bool, message: str) -> None:
        super().__init__(f"{reason.value}: {message}")
        self.reason = reason
        self.retryable = retryable
        self.message = message
