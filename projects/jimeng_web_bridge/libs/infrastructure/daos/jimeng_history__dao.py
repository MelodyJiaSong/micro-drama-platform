from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from libs.common.enums import RemoteStatus


class ParseOutcome(StrEnum):
    OK = "ok"
    LOGIN_ERROR = "login_error"
    ERROR_ENVELOPE = "error_envelope"
    MALFORMED = "malformed"


@dataclass(frozen=True)
class HistoryRecordDao:
    record_id: str
    status: RemoteStatus | None
    progress_pct: int | None
    fail_msg: str
    created_time: float | None
    prompt_text: str | None
    video_size: int | None
    duration_ms: int | None
    width: int | None
    height: int | None
    credits: int | None


@dataclass(frozen=True)
class HistoryParseDao:
    outcome: ParseOutcome
    records: tuple[HistoryRecordDao, ...]
    running_count: int | None
    running_limit: int | None
    errmsg: str


@dataclass(frozen=True)
class SubmitParseDao:
    outcome: ParseOutcome
    task_id: str | None
    errmsg: str


@dataclass(frozen=True)
class SubjectDao:
    subject_id: str
    name: str
    description: str
    updated_at: int | None


@dataclass(frozen=True)
class SubjectListParseDao:
    outcome: ParseOutcome
    subjects: tuple[SubjectDao, ...]
    errmsg: str
