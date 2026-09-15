from libs.common.enums import JobState, PauseReason


class JobError(Exception):
    error_code: str = "job_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class IllegalJobTransitionError(JobError):
    error_code = "illegal_job_transition"

    def __init__(self, from_state: JobState, command: str) -> None:
        super().__init__(f"作业处于 {from_state}，不能执行 {command}")
        self.from_state: JobState = from_state
        self.command: str = command


class JobAlreadyTerminalError(IllegalJobTransitionError):
    error_code = "job_already_terminal"


class UnconfirmedJobError(JobError):
    error_code = "job_not_confirmed"


class ConfirmationMismatchError(JobError):
    error_code = "confirmation_mismatch"


class StepOrderError(JobError):
    error_code = "step_order"


class MissingPlatformTaskIdError(JobError):
    error_code = "platform_task_id_missing"


class InvalidJobReasonError(JobError):
    error_code = "invalid_job_reason"

    def __init__(self, reason: PauseReason, message: str) -> None:
        super().__init__(message)
        self.reason: PauseReason = reason


class ResumeNotAllowedError(JobError):
    error_code = "resume_not_allowed"


class AdjudicationRequiredError(JobError):
    error_code = "adjudication_required"


class UiOnlyActionError(JobError):
    error_code = "ui_only_action"


class JobInvariantError(JobError):
    error_code = "job_invariant"


class EstimateApprovalMismatchError(JobError):
    error_code = "estimate_approval_mismatch"


class EstimateNotRecordedError(JobError):
    error_code = "page_estimate_missing"


class EstimateNotApprovedError(JobError):
    error_code = "estimate_not_approved"
