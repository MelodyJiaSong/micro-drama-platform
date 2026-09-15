from __future__ import annotations

import re

from libs.common.enums import RemoteStatus
from libs.infrastructure.daos.jimeng_history__dao import (
    HistoryParseDao,
    HistoryRecordDao,
    ParseOutcome,
    SubjectDao,
    SubjectListParseDao,
    SubmitParseDao,
)
from libs.infrastructure.daos.jimeng_response__dao import JimengEnvelopeDao
from libs.infrastructure.readers.jimeng_response__reader import SUCCESS_RET, JimengResponseReader

PARSER_VERSION: str = "fake-pre-probe.1"
"""requires_probe: every body shape below is the offline fake site's placeholder schema.

Only the `{ret, errmsg, systime, logid, data}` envelope and the login error `ret "1015"` are observed on
the real site. Record fields, status codes, the submit endpoint and its task-id path must be replaced
with the stage-6 probe's desensitised captures before the first real run (bump PARSER_VERSION then).
"""

HISTORY_BY_IDS: str = "history_by_ids"
HISTORY_QUEUE_INFO: str = "history_queue_info"
HISTORY_LIST: str = "history_list"
SUBMIT: str = "submit"
SUBJECT_GET: str = "subject_get"
RESPONSE_PATTERNS: dict[str, str] = {
    HISTORY_BY_IDS: r"/mweb/v1/get_history_by_ids(?:\?|$)",
    HISTORY_QUEUE_INFO: r"/mweb/v1/get_history_queue_info(?:\?|$)",
    HISTORY_LIST: r"/mweb/v1/get_history(?:\?|$)",
    SUBMIT: r"/mweb/v1/aigc_draft/generate(?:\?|$)",
    SUBJECT_GET: r"/mweb/v1/dreamina_subject/get(?:\?|$)",
}
STATUS_KEYS: tuple[str, ...] = (HISTORY_LIST, HISTORY_BY_IDS, HISTORY_QUEUE_INFO)
_STATUS_CODES: dict[int, RemoteStatus] = {
    10: RemoteStatus.QUEUED,
    20: RemoteStatus.GENERATING,
    30: RemoteStatus.FAILED,
    50: RemoteStatus.SUCCEEDED,
}


def compiled_patterns() -> dict[str, re.Pattern[str]]:
    return {key: re.compile(pattern) for key, pattern in RESPONSE_PATTERNS.items()}


class JimengHistoryReader:
    """Pure, versioned parsers for passively observed status / submit / subject bodies (FR-34).

    A body that is not the expected shape yields `MALFORMED` so the caller counts a parse failure
    toward `status.parse_failure_threshold` instead of crashing on a page redesign.
    """

    def __init__(self, envelopes: JimengResponseReader | None = None) -> None:
        self._envelopes = envelopes or JimengResponseReader()

    def status_body(self, key: str, body: bytes | None) -> HistoryParseDao:
        envelope, outcome = self._open(body)
        if envelope is None or outcome is not ParseOutcome.OK:
            return HistoryParseDao(outcome, (), None, None, "" if envelope is None else envelope.errmsg)
        data = envelope.data
        if key == HISTORY_LIST:
            items = data.get("records_list") if isinstance(data, dict) else None
            records = _records(items if isinstance(items, list) else None)
            return _history(records, None, None)
        if key == HISTORY_BY_IDS:
            values = list(data.values()) if isinstance(data, dict) else None
            return _history(_records(values), None, None)
        if key == HISTORY_QUEUE_INFO and isinstance(data, dict):
            infos = data.get("queue_infos")
            if not isinstance(infos, dict):
                return _malformed()
            records = tuple(
                HistoryRecordDao(str(record_id), _status(info.get("status")), _int(info.get("progress")), "", None,
                                 None, None, None, None, None, None)
                for record_id, info in infos.items()
                if isinstance(info, dict)
            )
            return _history(records, _int(data.get("running_count")), _int(data.get("running_limit")))
        return _malformed()

    def submit_body(self, body: bytes | None) -> SubmitParseDao:
        envelope, outcome = self._open(body)
        if envelope is None or outcome is not ParseOutcome.OK:
            return SubmitParseDao(outcome, None, "" if envelope is None else envelope.errmsg)
        data = envelope.data
        aigc = data.get("aigc_data") if isinstance(data, dict) else None
        task_id = aigc.get("history_record_id") if isinstance(aigc, dict) else None
        if not isinstance(task_id, (str, int)) or isinstance(task_id, bool) or str(task_id) == "":
            return SubmitParseDao(ParseOutcome.MALFORMED, None, envelope.errmsg)
        return SubmitParseDao(ParseOutcome.OK, str(task_id), envelope.errmsg)

    def subjects_body(self, body: bytes | None) -> SubjectListParseDao:
        envelope, outcome = self._open(body)
        if envelope is None or outcome is not ParseOutcome.OK:
            return SubjectListParseDao(outcome, (), "" if envelope is None else envelope.errmsg)
        data = envelope.data
        items = data.get("subject_list") if isinstance(data, dict) else None
        if not isinstance(items, list):
            return SubjectListParseDao(ParseOutcome.MALFORMED, (), envelope.errmsg)
        subjects: list[SubjectDao] = []
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                return SubjectListParseDao(ParseOutcome.MALFORMED, (), envelope.errmsg)
            subjects.append(
                SubjectDao(
                    subject_id=str(item.get("subject_id", "")),
                    name=item["name"],
                    description=str(item.get("description") or ""),
                    updated_at=_int(item.get("update_time")),
                )
            )
        return SubjectListParseDao(ParseOutcome.OK, tuple(subjects), envelope.errmsg)

    def _open(self, body: bytes | None) -> tuple[JimengEnvelopeDao | None, ParseOutcome]:
        if body is None:
            return None, ParseOutcome.MALFORMED
        envelope = self._envelopes.envelope(body)
        if envelope is None:
            return None, ParseOutcome.MALFORMED
        if self._envelopes.is_login_error(envelope):
            return envelope, ParseOutcome.LOGIN_ERROR
        if envelope.ret != SUCCESS_RET:
            return envelope, ParseOutcome.ERROR_ENVELOPE
        return envelope, ParseOutcome.OK


def _history(records: tuple[HistoryRecordDao, ...] | None, running: int | None, limit: int | None) -> HistoryParseDao:
    if records is None:
        return _malformed()
    return HistoryParseDao(ParseOutcome.OK, records, running, limit, "")


def _malformed() -> HistoryParseDao:
    return HistoryParseDao(ParseOutcome.MALFORMED, (), None, None, "")


def _records(items: list[object] | None) -> tuple[HistoryRecordDao, ...] | None:
    if items is None:
        return None
    records: list[HistoryRecordDao] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("history_record_id"), (str, int)):
            return None
        video = _first_video(item.get("item_list"))
        prompt = item.get("prompt")
        created = item.get("created_time")
        records.append(
            HistoryRecordDao(
                record_id=str(item["history_record_id"]),
                status=_status(item.get("status")),
                progress_pct=_int(item.get("progress")),
                fail_msg=str(item.get("fail_msg") or ""),
                created_time=float(created) if isinstance(created, (int, float)) and not isinstance(created, bool) else None,
                prompt_text=prompt if isinstance(prompt, str) else None,
                video_size=_int(video.get("file_size")),
                duration_ms=_int(video.get("duration_ms")),
                width=_int(video.get("width")),
                height=_int(video.get("height")),
                credits=_int(item.get("credits")),
            )
        )
    return tuple(records)


def _first_video(items: object) -> dict[str, object]:
    if isinstance(items, list) and items and isinstance(items[0], dict) and isinstance(items[0].get("video"), dict):
        return items[0]["video"]
    return {}


def _status(value: object) -> RemoteStatus | None:
    code = _int(value)
    return None if code is None else _STATUS_CODES.get(code, RemoteStatus.UNKNOWN)


def _int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None
