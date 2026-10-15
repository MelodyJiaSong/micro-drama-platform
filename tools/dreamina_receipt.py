"""Dreamina提交回执分流：任务ID或CLI退出0都不能覆盖明确失败。"""
def classify_receipt(data: dict) -> dict:
    status = data.get("gen_status")
    reason = str(data.get("fail_reason") or "")
    failed = status in ("fail", "failed")
    # Any failure while uploading a resource (apply / upload / commit phase, image or video/audio) happens before the
    # task is charged; retry only when the receipt shows no charge (B-003, ep01 s2 2026-10-11 receipts in the tests).
    upload_failed = failed and "upload resource" in reason.lower() and not data.get("credit_count")
    return {"stage": "submit_failed" if failed else "submitted" if data.get("submit_id") else "submission_unknown",
            "failure_phase": "upload" if upload_failed else "unspecified" if failed else None,
            "may_retry_upload": upload_failed,
            "should_query": bool(data.get("submit_id")) and not failed,
            "credit_count": data.get("credit_count"), "fail_reason": reason or None}
