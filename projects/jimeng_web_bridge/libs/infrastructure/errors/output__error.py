from __future__ import annotations

from libs.infrastructure.daos.output__dao import FinalizedOutputDao


class OutputError(Exception):
    error_code: str = "output_error"

    def __init__(self, message: str, config_key: str | None = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.config_key: str | None = config_key


class OutputPathRejectedError(OutputError):
    error_code = "output_path_rejected"


class DownloadSizeMismatchError(OutputError):
    error_code = "download_size_mismatch"


class DownloadShaMismatchError(OutputError):
    error_code = "download_sha_mismatch"


class FfprobeUnavailableError(OutputError):
    error_code = "ffprobe_unavailable"


class FfprobeFailedError(OutputError):
    error_code = "ffprobe_failed"


class MediaMismatchError(OutputError):
    error_code = "media_mismatch"


class OutputExistsError(OutputError):
    error_code = "output_exists"


class InvalidCandidateError(OutputError):
    error_code = "invalid_candidate"


class PromoteTargetExistsError(OutputError):
    error_code = "promote_target_exists"


class TimezoneUnavailableError(OutputError):
    error_code = "timezone_unavailable"


class SidecarWriteError(OutputError):
    """The verified media is already in place; only its sidecar could not be written (it is kept, not rolled back)."""

    error_code = "sidecar_missing"

    def __init__(self, message: str, output: FinalizedOutputDao) -> None:
        super().__init__(message)
        self.output: FinalizedOutputDao = output
