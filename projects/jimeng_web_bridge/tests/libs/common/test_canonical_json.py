import hashlib

import pytest

from libs.common.canonical_json import canonical_json, canonical_json_bytes, canonical_sha256, sha256_hex


def test_keys_sorted_no_whitespace() -> None:
    assert canonical_json({"b": 1, "a": [1, 2]}) == '{"a":[1,2],"b":1}'


def test_key_order_does_not_change_output() -> None:
    assert canonical_json({"x": 1, "y": {"b": 2, "a": 3}}) == canonical_json({"y": {"a": 3, "b": 2}, "x": 1})


def test_utf8_not_escaped() -> None:
    assert canonical_json({"名": "砌炉的老人"}) == '{"名":"砌炉的老人"}'
    assert canonical_json_bytes("主角") == '"主角"'.encode("utf-8")


def test_null_differs_from_empty_string() -> None:
    assert canonical_sha256({"n": None}) != canonical_sha256({"n": ""})


def test_nan_rejected() -> None:
    with pytest.raises(ValueError):
        canonical_json({"x": float("nan")})


def test_sha256_hex_accepts_str_and_bytes() -> None:
    assert sha256_hex("abc") == hashlib.sha256(b"abc").hexdigest() == sha256_hex(b"abc")
