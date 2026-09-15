"""Business errors → `{error_code, message, hint, config_key}` with an HTTP status.

One table, walked along the exception's MRO, so the most specific class wins and routes carry no
try/except. Messages come from the errors themselves, which never embed absolute paths or secrets.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from libs.application.errors.batch__error import (
    BatchItemRejectedError,
    BatchNotFoundError,
    BatchRequestError,
    BatchTooLargeError,
    IdempotencyKeyReusedError,
)
from libs.application.errors.lifecycle__error import (
    JobNotFoundError,
    LifecycleError,
    OperationNotFoundError,
    StepNotAllowedError,
)
from libs.domain.errors.batch__error import BatchError, BatchHasErrorsError
from libs.domain.errors.config__error import ConfigError
from libs.domain.errors.job__error import JobError, UiOnlyActionError
from libs.domain.errors.operation__error import OperationError
from libs.domain.errors.precheck__error import PrecheckError
from libs.infrastructure.errors.artifact__error import InvalidArtifactNameError, UnsupportedThumbnailSourceError
from libs.infrastructure.errors.config_io__error import (
    ConfigConflictError,
    ConfigParseError,
    ConfigWriteError,
    DramaRootNotFoundError,
)
from libs.infrastructure.errors.dreamina_cli__error import DreaminaCliError
from libs.infrastructure.errors.output__error import InvalidCandidateError, OutputError, OutputPathRejectedError, PromoteTargetExistsError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import MarkdownParseError

logger = logging.getLogger("jimeng_web_bridge.api")

_TABLE: dict[type[BaseException], tuple[int, str, str | None]] = {
    SandboxError: (403, "path_rejected", "路径必须是 ai_videos/ 下以 / 分隔的相对路径"),
    UiOnlyActionError: (403, "ui_only_action", "请在本地管理网页里操作"),
    OutputPathRejectedError: (403, "output_path_rejected", None),
    DramaRootNotFoundError: (404, "drama_not_found", None),
    FileNotFoundError: (404, "not_found", None),
    InvalidArtifactNameError: (404, "artifact_not_found", None),
    BatchNotFoundError: (404, "batch_not_found", None),
    JobNotFoundError: (404, "job_not_found", None),
    OperationNotFoundError: (404, "operation_not_found", None),
    ConfigConflictError: (409, "config_conflict", "文件已被别处修改，请重新加载后再保存"),
    IdempotencyKeyReusedError: (409, "idempotency_key_reused", "同一个 idempotency_key 不能用于不同内容"),
    PromoteTargetExistsError: (409, "promote_target_exists", None),
    StepNotAllowedError: (409, "step_not_allowed", None),
    BatchError: (409, "batch_error", None),
    JobError: (409, "job_error", None),
    OperationError: (409, "operation_error", None),
    BatchTooLargeError: (413, "batch_too_large", None),
    UnsupportedThumbnailSourceError: (415, "unsupported_media", None),
    ConfigError: (422, "config_invalid", None),
    ConfigParseError: (422, "config_parse_error", "TOML 语法错误，请修正后再保存"),
    MarkdownParseError: (422, "markdown_parse_error", None),
    BatchHasErrorsError: (422, "batch_has_errors", "剔除错误项并重新预检"),
    BatchItemRejectedError: (422, "batch_item_rejected", None),
    BatchRequestError: (422, "batch_request_invalid", None),
    InvalidCandidateError: (422, "invalid_candidate", None),
    PrecheckError: (422, "precheck_error", None),
    LifecycleError: (422, "lifecycle_error", None),
    OutputError: (500, "output_error", None),
    DreaminaCliError: (502, "cli_failed", None),
    ConfigWriteError: (503, "config_write_failed", "文件未改动，可以重试"),
}


def error_body(error: BaseException) -> tuple[int, dict[str, object]]:
    for klass in type(error).__mro__:
        if klass in _TABLE:
            status, default_code, hint = _TABLE[klass]
            code = getattr(error, "error_code", None) or default_code
            message = getattr(error, "message", None) or str(error) or default_code
            config_key = getattr(error, "config_key", None) or getattr(error, "field_path", None)
            return status, {"error_code": code, "message": message, "hint": hint, "config_key": config_key}
    return 500, {"error_code": "internal_error", "message": "服务内部错误", "hint": None, "config_key": None}


def register_error_handlers(app: FastAPI) -> None:
    async def handle_known(_: Request, error: Exception) -> JSONResponse:
        status, body = error_body(error)
        if status >= 500:
            logger.warning("request_failed", extra={"kind": "request_failed", "error_code": body["error_code"]})
        return JSONResponse(status_code=status, content=body)

    async def handle_http(_: Request, error: HTTPException) -> JSONResponse:
        detail = error.detail if isinstance(error.detail, dict) else {"error_code": f"http_{error.status_code}", "message": str(error.detail), "hint": None}
        return JSONResponse(status_code=error.status_code, content={"config_key": None, **detail})

    async def handle_validation(_: Request, error: RequestValidationError) -> JSONResponse:
        first = error.errors()[0] if error.errors() else {}
        location = ".".join(str(part) for part in first.get("loc", ()))
        return JSONResponse(
            status_code=422,
            content={"error_code": "request_invalid", "message": str(first.get("msg", "invalid request")), "hint": None, "config_key": location or None},
        )

    for klass in _TABLE:
        app.add_exception_handler(klass, handle_known)
    app.add_exception_handler(HTTPException, handle_http)
    app.add_exception_handler(RequestValidationError, handle_validation)
