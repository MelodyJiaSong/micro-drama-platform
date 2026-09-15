import base64
import binascii
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

from libs.common.canonical_json import canonical_json_bytes
from libs.common.enums import TokenVerdict
from libs.domain.errors.batch__error import TokenInvalidError

MIN_KEY_BYTES = 32


@dataclass(frozen=True)
class ConfirmationToken:
    batch_id: str
    content_digest: str
    estimated_credits: int
    expires_at: datetime
    signature: str

    @staticmethod
    def expiry(now: datetime, ttl_min: int) -> datetime:
        _require_aware(now)
        return now + timedelta(minutes=ttl_min)

    @classmethod
    def issue(
        cls, batch_id: str, content_digest: str, estimated_credits: int, expires_at: datetime, key: bytes
    ) -> "ConfirmationToken":
        _require_aware(expires_at)
        payload: bytes = _payload(batch_id, content_digest, estimated_credits, expires_at)
        return cls(batch_id, content_digest, estimated_credits, expires_at, _sign(payload, key))

    def encode(self) -> str:
        payload: bytes = _payload(self.batch_id, self.content_digest, self.estimated_credits, self.expires_at)
        return f"{base64.urlsafe_b64encode(payload).decode('ascii').rstrip('=')}.{self.signature}"

    @classmethod
    def verify(
        cls,
        text: str,
        batch_id: str,
        content_digest: str,
        estimated_credits: int,
        now: datetime,
        key: bytes,
    ) -> TokenVerdict:
        _require_aware(now)
        decoded: "ConfirmationToken | None" = cls._decode_signed(text, key)
        if decoded is None:
            return TokenVerdict.BAD_SIGNATURE
        if (decoded.batch_id, decoded.content_digest, decoded.estimated_credits) != (
            batch_id,
            content_digest,
            estimated_credits,
        ):
            return TokenVerdict.DIGEST_MISMATCH
        if now >= decoded.expires_at:
            return TokenVerdict.EXPIRED
        return TokenVerdict.OK

    @classmethod
    def _decode_signed(cls, text: str, key: bytes) -> "ConfirmationToken | None":
        parts: list[str] = text.split(".")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None
        try:
            payload: bytes = base64.urlsafe_b64decode(parts[0] + "=" * (-len(parts[0]) % 4))
        except (binascii.Error, ValueError):
            return None
        if not hmac.compare_digest(parts[1].encode("ascii", "replace"), _sign(payload, key).encode("ascii")):
            return None
        try:
            body: object = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(body, dict):
            return None
        batch_id, digest, credits, exp = body.get("batch_id"), body.get("digest"), body.get("credits"), body.get("exp")
        if not isinstance(batch_id, str) or not isinstance(digest, str) or not isinstance(exp, str):
            return None
        if isinstance(credits, bool) or not isinstance(credits, int):
            return None
        try:
            expires_at: datetime = datetime.fromisoformat(exp)
        except ValueError:
            return None
        return cls(batch_id, digest, credits, expires_at, parts[1])


def _payload(batch_id: str, content_digest: str, estimated_credits: int, expires_at: datetime) -> bytes:
    return canonical_json_bytes(
        {"batch_id": batch_id, "digest": content_digest, "credits": estimated_credits, "exp": expires_at.isoformat()}
    )


def _sign(payload: bytes, key: bytes) -> str:
    if len(key) < MIN_KEY_BYTES:
        raise TokenInvalidError(f"HMAC key 至少 {MIN_KEY_BYTES} 字节")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def _require_aware(moment: datetime) -> None:
    if moment.tzinfo is None:
        raise TokenInvalidError("时间必须带时区")
