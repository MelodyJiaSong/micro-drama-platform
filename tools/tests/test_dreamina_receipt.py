from tools.dreamina_receipt import classify_receipt


def test_task_id_does_not_override_explicit_upload_failure():
    receipt = classify_receipt({"submit_id":"local-id","gen_status":"fail","fail_reason":"upload resource x: upload image: upload phase, no file upload"})
    assert receipt["stage"] == "submit_failed"
    assert receipt["may_retry_upload"] and not receipt["should_query"]
    assert receipt["credit_count"] is None


def test_timeout_without_id_is_unknown_and_must_not_retry():
    receipt = classify_receipt({"error":"timeout"})
    assert receipt["stage"] == "submission_unknown"
    assert not receipt["may_retry_upload"]


def test_failed_generation_is_not_upload_retry():
    receipt = classify_receipt({"submit_id":"server-id","gen_status":"fail","fail_reason":"generation failed","credit_count":384})
    assert not receipt["may_retry_upload"] and not receipt["should_query"]
    assert receipt["credit_count"] == 384


def test_successful_receipt_preserves_actual_fee():
    receipt = classify_receipt({"submit_id":"server-id","credit_count":384})
    assert receipt["stage"] == "submitted" and receipt["should_query"]
    assert receipt["credit_count"] == 384


# Real receipts from 2026-10-11 (ep01 s2): every upload-side failure left the task uncharged (credit_count empty),
# but only the literal "upload phase" counted as retryable (B-003 in the s2 RCA).
APPLY_TIMEOUT = ('upload resource "C:\\s2-regen\\inputs\\ep1_s2_st7\\upload\\06_image5.jpg": upload image: apply phase, '
                 'ApplyImageUpload: do request, Get "http://imagex.bytedanceapi.com/?Action=ApplyImageUpload": context deadline exceeded')
AUDIO_TIMEOUT = 'upload resource "C:\\s2-regen\\inputs\\ep1_s2_st19\\upload\\08_audio1.mp3": upload video/audio: context deadline exceeded'


def test_upload_side_timeouts_without_charge_may_retry():
    for reason in (APPLY_TIMEOUT, AUDIO_TIMEOUT):
        receipt = classify_receipt({"submit_id": "server-id", "gen_status": "fail", "fail_reason": reason})
        assert receipt["stage"] == "submit_failed" and receipt["failure_phase"] == "upload"
        assert receipt["may_retry_upload"] and not receipt["should_query"]


def test_upload_failure_that_was_charged_must_not_retry():
    receipt = classify_receipt({"submit_id": "server-id", "gen_status": "fail", "fail_reason": APPLY_TIMEOUT, "credit_count": 144})
    assert not receipt["may_retry_upload"]


def test_insufficient_credit_is_not_an_upload_retry():
    receipt = classify_receipt({"submit_id": "server-id", "gen_status": "fail",
                                "fail_reason": "api error: ret=1006, message=CreditPreDeductNotEnough"})
    assert receipt["stage"] == "submit_failed" and not receipt["may_retry_upload"]
