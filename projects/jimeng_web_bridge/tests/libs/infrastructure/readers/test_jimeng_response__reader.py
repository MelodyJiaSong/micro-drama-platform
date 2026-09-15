from __future__ import annotations

from pathlib import Path

import pytest

from libs.infrastructure.readers.jimeng_response__reader import JimengResponseReader

REAL = Path(__file__).resolve().parents[3] / "fixtures" / "real_responses"


def _body(name: str) -> bytes:
    path = REAL / name
    if not path.is_file():
        pytest.skip(f"probe fixture missing: {name}")
    return path.read_bytes()


def test_real_login_error_envelope_is_detected() -> None:
    reader = JimengResponseReader()
    envelope = reader.envelope(_body("envelope_login_error__dreamina_subject_get.json"))
    assert envelope is not None
    assert (envelope.ret, envelope.data) == ("1015", None)
    assert reader.is_login_error(envelope)


def test_real_common_config_is_parsed() -> None:
    reader = JimengResponseReader()
    envelope = reader.envelope(_body("common_config__lip_sync_master__prelogin.json"))
    assert envelope is not None and not reader.is_login_error(envelope)
    config = reader.common_config(envelope)
    assert config is not None
    assert len(config.models) == 2 and config.default_model_index == 1
    assert (config.min_duration_ms, config.max_duration_ms) == (4000, 15000)
    assert "720p" in config.resolutions
    master, quick = config.models
    assert quick.model_req_key == "dreamina_lib_sync_image_quick_1.5"
    assert master.model_req_key == "dreamina_lib_sync_image_master_1.5"
    assert (master.min_audio_duration_s, master.max_audio_duration_s) == (1, 30)
    assert master.aigc_compliance_confirmation_required is False


@pytest.mark.parametrize(
    "body",
    [b"", b"<html>blocked</html>", b"[]", b'{"data": {}}', b"\xff\xfe\x00", b'{"ret": "0", "data": {"model_list": "x"}}'],
)
def test_unexpected_bodies_never_raise(body: bytes) -> None:
    reader = JimengResponseReader()
    envelope = reader.envelope(body)
    if envelope is not None:
        assert reader.common_config(envelope) is None


def test_non_success_envelope_yields_no_config() -> None:
    reader = JimengResponseReader()
    envelope = reader.envelope(b'{"ret": "4001", "errmsg": "invalid param", "data": {"model_list": []}}')
    assert envelope is not None and reader.common_config(envelope) is None and not reader.is_login_error(envelope)
