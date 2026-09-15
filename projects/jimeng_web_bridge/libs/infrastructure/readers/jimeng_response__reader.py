from __future__ import annotations

import json

from libs.infrastructure.daos.jimeng_response__dao import (
    JimengCommonConfigDao,
    JimengEnvelopeDao,
    JimengModelConfigDao,
)

PARSER_VERSION: str = "2026-09-13.1"
LOGIN_ERROR_RET: str = "1015"
SUCCESS_RET: str = "0"


class JimengResponseReader:
    """Pure parsers for the page's own responses, observed passively (FR-34).

    Every internal endpoint wraps its payload in `{ret, errmsg, systime, logid, data}`; a body
    that doesn't match returns None so the caller can count it as a parse failure instead of
    crashing on a redesign.
    """

    def envelope(self, body: bytes) -> JimengEnvelopeDao | None:
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict) or "ret" not in payload:
            return None
        logid = payload.get("logid")
        return JimengEnvelopeDao(
            ret=str(payload["ret"]),
            errmsg=str(payload.get("errmsg", "")),
            logid=logid if isinstance(logid, str) else None,
            data=payload.get("data"),
        )

    def is_login_error(self, envelope: JimengEnvelopeDao) -> bool:
        return envelope.ret == LOGIN_ERROR_RET or "login" in envelope.errmsg.lower()

    def common_config(self, envelope: JimengEnvelopeDao) -> JimengCommonConfigDao | None:
        if envelope.ret != SUCCESS_RET or not isinstance(envelope.data, dict):
            return None
        data = envelope.data
        raw_models = data.get("model_list")
        if not isinstance(raw_models, list):
            return None
        duration = data.get("video_duration_display_range")
        duration = duration if isinstance(duration, dict) else {}
        resolutions = data.get("video_resolution_display_list")
        return JimengCommonConfigDao(
            models=tuple(_model(item) for item in raw_models if isinstance(item, dict)),
            default_model_index=_int(data.get("default_model_idx")) or 0,
            min_duration_ms=_int(duration.get("min_duration_ms")),
            max_duration_ms=_int(duration.get("max_duration_ms")),
            resolutions=tuple(
                str(item["value"]) for item in resolutions if isinstance(item, dict) and "value" in item
            )
            if isinstance(resolutions, list)
            else (),
        )


def _model(item: dict[str, object]) -> JimengModelConfigDao:
    extra = item.get("extra")
    extra = extra if isinstance(extra, dict) else {}
    return JimengModelConfigDao(
        model_name=str(item.get("model_name", "")),
        model_req_key=str(item.get("model_req_key", "")),
        mode=extra.get("mode") if isinstance(extra.get("mode"), str) else None,
        aigc_compliance_confirmation_required=bool(extra.get("aigc_compliance_confirmation_required", False)),
        min_audio_duration_s=_int(extra.get("min_audio_duration")),
        max_audio_duration_s=_int(extra.get("max_audio_duration")),
    )


def _int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None
