from __future__ import annotations


class BatchRequestError(Exception):
    error_code: str = "batch_request_invalid"

    def __init__(self, message: str, config_key: str | None = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.config_key: str | None = config_key


class BatchNotFoundError(BatchRequestError):
    error_code = "batch_not_found"


class BatchTooLargeError(BatchRequestError):
    error_code = "batch_too_large"


class IdempotencyKeyReusedError(BatchRequestError):
    error_code = "idempotency_key_reused"


class BatchItemRejectedError(BatchRequestError):
    """An input item that cannot become a request at all (bad path, unknown card/key, unparsable md)."""

    error_code = "batch_item_rejected"

    def __init__(self, reason: str, message: str, index: int | None = None, config_key: str | None = None) -> None:
        super().__init__(message, config_key)
        self.reason: str = reason
        self.index: int | None = index
