from __future__ import annotations


class LifecycleError(Exception):
    error_code: str = "lifecycle_error"

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.hint: str | None = hint


class JobNotFoundError(LifecycleError):
    error_code = "job_not_found"


class OperationNotFoundError(LifecycleError):
    error_code = "operation_not_found"


class InvalidWaitTargetError(LifecycleError):
    error_code = "invalid_wait_target"


class InvalidStepOpError(LifecycleError):
    error_code = "invalid_step_op"


class StepNotAllowedError(LifecycleError):
    error_code = "step_not_allowed"


class InvalidQueueReasonError(LifecycleError):
    error_code = "invalid_queue_reason"


class InvalidQueryFilterError(LifecycleError):
    error_code = "invalid_query_filter"


class ExecutorKeyInUseError(LifecycleError):
    error_code = "executor_key_in_use"
