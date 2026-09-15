from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JimengEnvelopeDao:
    ret: str
    errmsg: str
    logid: str | None
    data: object


@dataclass(frozen=True)
class JimengModelConfigDao:
    model_name: str
    model_req_key: str
    mode: str | None
    aigc_compliance_confirmation_required: bool
    min_audio_duration_s: int | None
    max_audio_duration_s: int | None


@dataclass(frozen=True)
class JimengCommonConfigDao:
    models: tuple[JimengModelConfigDao, ...]
    default_model_index: int
    min_duration_ms: int | None
    max_duration_ms: int | None
    resolutions: tuple[str, ...]
