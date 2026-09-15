import hashlib
import json


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def canonical_json_bytes(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def sha256_hex(data: bytes | str) -> str:
    raw: bytes = data.encode("utf-8") if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256_hex(canonical_json_bytes(value))
