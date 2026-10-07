"""Dreamina提交回执分流：任务ID或CLI退出0都不能覆盖明确失败。"""
def classify_receipt(data: dict) -> dict:
    status = data.get("gen_status")
    reason = str(data.get("fail_reason") or "")
    failed = status in ("fail", "failed")
    upload_failed = failed and "upload resource" in reason.lower() and "upload phase" in reason.lower()
    return {"stage": "submit_failed" if failed else "submitted" if data.get("submit_id") else "submission_unknown",
            "failure_phase": "upload" if upload_failed else "unspecified" if failed else None,
            "may_retry_upload": upload_failed,
            "should_query": bool(data.get("submit_id")) and not failed,
            "credit_count": data.get("credit_count"), "fail_reason": reason or None}
