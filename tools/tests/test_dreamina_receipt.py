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
