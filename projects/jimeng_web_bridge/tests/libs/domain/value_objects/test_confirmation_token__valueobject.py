import base64
import json
from datetime import datetime, timedelta

import pytest

from libs.common.enums import TokenVerdict
from libs.domain.errors.batch__error import TokenInvalidError
from libs.domain.value_objects.confirmation_token__valueobject import ConfirmationToken
from tests.libs.domain.builders import KEY, T0

DIGEST = "d" * 64
EXP = ConfirmationToken.expiry(T0, 30)


def token() -> ConfirmationToken:
    return ConfirmationToken.issue("batch-1", DIGEST, 900, EXP, KEY)


def verify(text: str, now: datetime = T0, batch_id: str = "batch-1", digest: str = DIGEST, credits: int = 900, key: bytes = KEY) -> TokenVerdict:
    return ConfirmationToken.verify(text, batch_id, digest, credits, now, key)


def test_roundtrip() -> None:
    assert verify(token().encode()) is TokenVerdict.OK


def test_ttl_is_injected() -> None:
    assert ConfirmationToken.expiry(T0, 1) == T0 + timedelta(minutes=1)
    assert ConfirmationToken.expiry(T0, 30) == T0 + timedelta(minutes=30)


@pytest.mark.parametrize(("delta", "verdict"), [(-1, TokenVerdict.OK), (0, TokenVerdict.EXPIRED), (1, TokenVerdict.EXPIRED)])
def test_expiry_boundary(delta: int, verdict: TokenVerdict) -> None:
    assert verify(token().encode(), now=EXP + timedelta(seconds=delta)) is verdict


def _flip(text: str, index: int) -> str:
    char = text[index]
    return text[:index] + ("A" if char != "A" else "B") + text[index + 1:]


@pytest.mark.parametrize("position", ["payload", "signature", "separator"])
def test_tamper_rejected(position: str) -> None:
    text = token().encode()
    dot = text.index(".")
    tampered = {"payload": _flip(text, 2), "signature": _flip(text, len(text) - 1), "separator": text.replace(".", "-")}[position]
    assert verify(tampered) is TokenVerdict.BAD_SIGNATURE
    assert dot > 0


def test_forged_credits_in_payload_rejected() -> None:
    text = token().encode()
    payload_b64, sig = text.split(".")
    body = json.loads(base64.urlsafe_b64decode(payload_b64 + "=" * (-len(payload_b64) % 4)))
    body["credits"] = 1
    forged = base64.urlsafe_b64encode(json.dumps(body).encode()).decode().rstrip("=")
    assert verify(f"{forged}.{sig}", credits=1) is TokenVerdict.BAD_SIGNATURE


@pytest.mark.parametrize(("field", "value"), [("digest", "e" * 64), ("credits", 901), ("batch_id", "batch-2")])
def test_binding_mismatch(field: str, value: object) -> None:
    kwargs: dict[str, object] = {field: value}
    assert verify(token().encode(), **kwargs) is TokenVerdict.DIGEST_MISMATCH  # type: ignore[arg-type]


def test_wrong_key_rejected() -> None:
    assert verify(token().encode(), key=b"z" * 32) is TokenVerdict.BAD_SIGNATURE


@pytest.mark.parametrize("garbage", ["", ".", "abc", "a.b.c", "!!!.deadbeef"])
def test_garbage_rejected(garbage: str) -> None:
    assert verify(garbage) is TokenVerdict.BAD_SIGNATURE


def test_no_secret_material_in_token() -> None:
    text = token().encode()
    assert KEY.decode() not in text
    assert KEY.decode() not in base64.urlsafe_b64decode(text.split(".")[0] + "==").decode()


def test_single_use_is_not_a_token_property() -> None:
    text = token().encode()
    assert verify(text) is TokenVerdict.OK and verify(text) is TokenVerdict.OK


def test_short_key_and_naive_time_rejected() -> None:
    with pytest.raises(TokenInvalidError):
        ConfirmationToken.issue("b", DIGEST, 1, EXP, b"short")
    with pytest.raises(TokenInvalidError):
        ConfirmationToken.issue("b", DIGEST, 1, EXP.replace(tzinfo=None), KEY)
