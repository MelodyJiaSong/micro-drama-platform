from collections.abc import Mapping
from enum import StrEnum
from types import MappingProxyType


class JobState(StrEnum):
    QUEUED = "queued"
    PREPARING = "preparing"
    SUBMITTING = "submitting"
    GENERATING = "generating"
    DOWNLOADING = "downloading"
    DONE = "done"
    PAUSED_NEEDS_HUMAN = "paused_needs_human"
    FAILED = "failed"
    CANCELLED = "cancelled"


TERMINAL_JOB_STATES: frozenset[JobState] = frozenset({JobState.DONE, JobState.FAILED, JobState.CANCELLED})


class PreparingStep(StrEnum):
    SET_PARAMS = "set_params"
    UPLOAD = "upload"
    FILL = "fill"
    PREVIEW = "preview"
    VERIFY = "verify"


PREPARING_STEP_ORDER: tuple[PreparingStep, ...] = (
    PreparingStep.SET_PARAMS,
    PreparingStep.UPLOAD,
    PreparingStep.FILL,
    PreparingStep.PREVIEW,
    PreparingStep.VERIFY,
)


class BlockedOn(StrEnum):
    SLOT = "slot"
    INTERVAL = "interval"
    QUEUE_PAUSED = "queue_paused"
    NONE = "none"


class PauseReason(StrEnum):
    MODERATION_REJECT = "moderation_reject"
    REAL_FACE_REJECTED = "real_face_rejected"
    UPLOAD_REJECTED = "upload_rejected"
    FILL_MISMATCH = "fill_mismatch"
    STEP_FAILED = "step_failed"
    INPUTS_CHANGED = "inputs_changed"
    WAIT_TIMEOUT = "wait_timeout"
    DOWNLOAD_FAILED = "download_failed"
    RESTART_DURING_SUBMIT = "restart_during_submit"
    SUBMIT_REJECTED = "submit_rejected"
    SUBMIT_UNCONFIRMED = "submit_unconfirmed"
    ESTIMATE_EXCEEDS_CONFIRMED = "estimate_exceeds_confirmed"
    CLI_ERROR = "cli_error"
    LOGIN_EXPIRED = "login_expired"
    CAPTCHA_OR_RISK_POPUP = "captcha_or_risk_popup"
    INSUFFICIENT_CREDIT = "insufficient_credit"
    PAGE_CONTRACT_BROKEN = "page_contract_broken"
    BROWSER_LOST = "browser_lost"
    CLI_LOGIN_REQUIRED = "cli_login_required"
    COMPLIANCE_CONFIRMATION_REQUIRED = "compliance_confirmation_required"


class PauseTier(StrEnum):
    QUEUE = "queue"
    JOB = "job"


class ResumeAllowance(StrEnum):
    API = "api"
    UI_ONLY = "ui_only"
    NEVER = "never"


class ResumeVia(StrEnum):
    API = "api"
    UI = "ui"


class Adjudication(StrEnum):
    LINK_EXISTING = "link_existing"
    CONFIRM_NOT_SUBMITTED = "confirm_not_submitted"
    CANCEL = "cancel"


class BackendKind(StrEnum):
    WEB = "web"
    CLI = "cli"


PREPARING_STEPS_BY_BACKEND: Mapping[BackendKind, tuple[PreparingStep, ...]] = MappingProxyType(
    {BackendKind.WEB: PREPARING_STEP_ORDER, BackendKind.CLI: (PreparingStep.VERIFY,)}
)


class GenerationKind(StrEnum):
    VIDEO = "video"
    IMAGE = "image"
    ENTITY = "entity"


class RefKind(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ENTITY = "entity"
    FIRST_FRAME = "first_frame"


class ReferenceResolver(StrEnum):
    ASSET_FILE = "asset_file"
    ENTITY = "entity"
    SHOT_VIDEO = "shot_video"
    PREV_SHOT_LASTFRAME = "prev_shot_lastframe"


class SourceType(StrEnum):
    RAW = "raw"
    SHOT = "shot"
    ASSET_IMAGE = "asset_image"
    ASSET_VIDEO = "asset_video"
    ENTITY_CREATE = "entity_create"


class QueueState(StrEnum):
    RUNNING = "running"
    PAUSED = "paused"


class Confirmer(StrEnum):
    UI_HUMAN = "ui_human"


class BatchState(StrEnum):
    AWAITING_CONFIRM = "awaiting_confirm"
    CONFIRMED = "confirmed"
    EXPIRED = "expired"
    REJECTED = "rejected"


class TokenVerdict(StrEnum):
    OK = "ok"
    EXPIRED = "expired"
    DIGEST_MISMATCH = "digest_mismatch"
    BAD_SIGNATURE = "bad_signature"


class CheckSeverity(StrEnum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"


class PrecheckCheck(StrEnum):
    REFERENCES = "references"
    REFERENCE_COUNTS = "reference_counts"
    PARAMS = "params"
    BACKEND = "backend"
    PROMPT_LENGTH = "prompt_length"
    ENTITIES = "entities"
    OUTPUT = "output"
    FINGERPRINT = "fingerprint"
    NEGATIVE_PROMPT = "negative_prompt"
    ENTITY_CREATE = "entity_create"
    PRICE = "price"


class NegativePromptStrategy(StrEnum):
    PLATFORM_FIELD_OR_OMIT = "platform_field_or_omit"
    OMIT = "omit"
    FAIL = "fail"


class OnExisting(StrEnum):
    ARCHIVE = "archive"
    FAIL = "fail"


class OperationKind(StrEnum):
    CANARY = "canary"
    ENTITY_SYNC = "entity_sync"
    ENTITY_CREATE = "entity_create"
    STEP = "step"
    STEP_SUBMIT = "step_submit"
    RESUME_QUEUE = "resume_queue"
    CLI_VERSION = "cli_version"


class OperationState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class RemoteStatus(StrEnum):
    QUEUED = "queued"
    GENERATING = "generating"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


class EntityReconcileState(StrEnum):
    MAPPED = "mapped"
    MISSING_ON_PLATFORM = "missing_on_platform"
    UNMAPPED_ON_PLATFORM = "unmapped_on_platform"
