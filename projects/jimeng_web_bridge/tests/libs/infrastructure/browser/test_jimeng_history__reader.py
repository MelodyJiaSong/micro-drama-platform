from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from libs.common.enums import RemoteStatus
from libs.infrastructure.daos.jimeng_history__dao import ParseOutcome
from libs.infrastructure.readers.jimeng_history__reader import (
    HISTORY_BY_IDS,
    HISTORY_LIST,
    HISTORY_QUEUE_INFO,
    RESPONSE_PATTERNS,
    SUBJECT_GET,
    SUBMIT,
    JimengHistoryReader,
)

REAL_RESPONSES: Path = Path(__file__).resolve().parents[3] / "fixtures" / "real_responses"
READER = JimengHistoryReader()


def envelope(data: object, ret: str = "0", errmsg: str = "success") -> bytes:
    return json.dumps({"ret": ret, "errmsg": errmsg, "systime": "1", "logid": "x", "data": data}, ensure_ascii=False).encode()


def record(record_id: str = "7000000000000001", status: int = 20, progress: int = 50, **extra: object) -> dict[str, object]:
    return {"history_record_id": record_id, "status": status, "progress": progress, "fail_msg": "", "created_time": 1789290000.5,
            "prompt": "shot02\n参考: `bg11-1(场景参考图)=>bg11-1`", "item_list": [], **extra}


def test_by_ids_body_parses_records() -> None:
    body = envelope({"7000000000000001": record(status=50, progress=100, item_list=[{"video": {"file_size": 1234, "duration_ms": 22000, "width": 320, "height": 180}}])})
    parsed = READER.status_body(HISTORY_BY_IDS, body)
    assert parsed.outcome is ParseOutcome.OK
    (only,) = parsed.records
    assert (only.record_id, only.status, only.progress_pct, only.video_size, only.duration_ms) == ("7000000000000001", RemoteStatus.SUCCEEDED, 100, 1234, 22000)


def test_list_body_and_queue_info_body() -> None:
    listed = READER.status_body(HISTORY_LIST, envelope({"records_list": [record(), record("7000000000000002", status=30, fail_msg="内容审核未通过")]}))
    assert [r.status for r in listed.records] == [RemoteStatus.GENERATING, RemoteStatus.FAILED]
    assert listed.records[1].fail_msg == "内容审核未通过"
    queue = READER.status_body(HISTORY_QUEUE_INFO, envelope({"running_count": 2, "running_limit": 3, "queue_infos": {"7": {"status": 10, "progress": 0}}}))
    assert (queue.running_count, queue.running_limit, queue.records[0].status) == (2, 3, RemoteStatus.QUEUED)


def test_unknown_status_code_is_unknown_not_a_failure() -> None:
    parsed = READER.status_body(HISTORY_BY_IDS, envelope({"1": record(status=99)}))
    assert parsed.outcome is ParseOutcome.OK and parsed.records[0].status is RemoteStatus.UNKNOWN


@pytest.mark.parametrize(
    ("key", "body"),
    [
        (HISTORY_BY_IDS, b"<html>502 bad gateway</html>"),
        (HISTORY_BY_IDS, None),
        (HISTORY_LIST, envelope({"records": []})),
        (HISTORY_QUEUE_INFO, envelope({"running_count": 1})),
        (HISTORY_BY_IDS, envelope({"1": {"status": 20}})),
    ],
)
def test_malformed_bodies_are_counted_not_raised(key: str, body: bytes | None) -> None:
    assert READER.status_body(key, body).outcome is ParseOutcome.MALFORMED


def test_real_login_error_envelope_is_login_error() -> None:
    body = (REAL_RESPONSES / "envelope_login_error__dreamina_subject_get.json").read_bytes()
    assert READER.subjects_body(body).outcome is ParseOutcome.LOGIN_ERROR
    assert READER.status_body(HISTORY_BY_IDS, body).outcome is ParseOutcome.LOGIN_ERROR
    assert READER.submit_body(body).outcome is ParseOutcome.LOGIN_ERROR


def test_submit_body_task_id_and_rejection() -> None:
    ok = READER.submit_body(envelope({"aigc_data": {"history_record_id": "7000000000000009"}}))
    assert (ok.outcome, ok.task_id) == (ParseOutcome.OK, "7000000000000009")
    rejected = READER.submit_body(envelope(None, "1310", "并行任务已达上限，请稍后再试"))
    assert (rejected.outcome, rejected.task_id, rejected.errmsg) == (ParseOutcome.ERROR_ENVELOPE, None, "并行任务已达上限，请稍后再试")
    assert READER.submit_body(envelope({"aigc_data": {}})).outcome is ParseOutcome.MALFORMED


def test_subjects_body() -> None:
    parsed = READER.subjects_body(envelope({"subject_list": [{"subject_id": "s1", "name": "hy3_主角", "update_time": 5}]}))
    assert [(s.subject_id, s.name, s.updated_at) for s in parsed.subjects] == [("s1", "hy3_主角", 5)]


@pytest.mark.parametrize(
    ("url", "key"),
    [
        ("https://jimeng.jianying.com/mweb/v1/get_history_by_ids?aid=513695", HISTORY_BY_IDS),
        ("https://jimeng.jianying.com/mweb/v1/get_history_queue_info?aid=513695", HISTORY_QUEUE_INFO),
        ("http://127.0.0.1:1/mweb/v1/get_history?aid=1", HISTORY_LIST),
        ("http://127.0.0.1:1/mweb/v1/aigc_draft/generate?aid=1", SUBMIT),
        ("https://jimeng.jianying.com/mweb/v1/dreamina_subject/get?aid=1", SUBJECT_GET),
    ],
)
def test_each_url_matches_exactly_one_pattern(url: str, key: str) -> None:
    matches = [name for name, pattern in RESPONSE_PATTERNS.items() if re.search(pattern, url)]
    assert matches == [key]


def test_patterns_ignore_neighbouring_endpoints() -> None:
    for url in ("https://x/mweb/v1/aigc_draft/generate_accelerate?aid=1", "http://x/mweb/v1/aigc_draft/generate_alt?aid=1"):
        assert not any(re.search(pattern, url) for pattern in RESPONSE_PATTERNS.values())
