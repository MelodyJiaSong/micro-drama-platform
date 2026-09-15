from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SetupCdto:
    env_path: str
    token_created: bool
    data_dir: str
    created_data_dirs: tuple[str, ...]
    secret_key_created: bool
