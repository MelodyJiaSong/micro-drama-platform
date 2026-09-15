class PrecheckError(Exception):
    error_code: str = "precheck_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class InvalidRequestError(PrecheckError):
    error_code = "invalid_request"


class FrozenRequestIncompleteError(PrecheckError):
    error_code = "frozen_request_incomplete"
