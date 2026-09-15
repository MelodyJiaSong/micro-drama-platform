from __future__ import annotations

import os
import secrets
from pathlib import Path

SECRET_KEY_BYTES: int = 32


class SecretKeyWriter:
    """Owns `.data/secret.key` — the HMAC key for confirmation tokens. Created once, never logged."""

    def ensure(self, path: Path) -> bool:
        if path.is_file() and path.stat().st_size >= SECRET_KEY_BYTES:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_bytes(secrets.token_bytes(SECRET_KEY_BYTES))
        os.replace(temp, path)
        return True

    def read(self, path: Path) -> bytes:
        return path.read_bytes()
