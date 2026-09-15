class BatchError(Exception):
    error_code: str = "batch_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class BatchHasErrorsError(BatchError):
    error_code = "batch_has_errors"


class BatchAlreadyConfirmedError(BatchError):
    error_code = "token_already_used"


class BatchExpiredError(BatchError):
    error_code = "batch_expired"


class BatchNotAwaitingConfirmError(BatchError):
    error_code = "batch_not_awaiting_confirm"


class ConfirmationNotIssuedError(BatchError):
    error_code = "confirmation_not_issued"


class TokenExpiredError(BatchError):
    error_code = "token_expired"


class TokenDigestMismatchError(BatchError):
    error_code = "token_digest_mismatch"


class TokenInvalidError(BatchError):
    error_code = "token_invalid"


class TokenBindingError(BatchError):
    error_code = "token_binding_mismatch"


class InvalidConfirmerError(BatchError):
    error_code = "invalid_confirmer"


class BalanceAlreadyRecordedError(BatchError):
    error_code = "balance_already_recorded"


class EmptyBatchError(BatchError):
    error_code = "batch_empty"


class BatchInvariantError(BatchError):
    error_code = "batch_invariant"
