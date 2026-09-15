from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

HOST: str = "127.0.0.1"
TOKEN_MIN_CHARS: int = 32


class StartupConfigError(Exception):
    pass


@dataclass(frozen=True)
class AppSettings:
    port: int
    bearer_token: str = field(repr=False)
    ui_session: str = field(repr=False)
    project_root: Path
    repo_root: Path
    data_dir: Path
    global_config_path: Path
    static_dir: Path
    test_mode: bool
    env_overrides: tuple[tuple[str, str], ...] = field(default=(), repr=False)

    @property
    def env_overridden_keys(self) -> tuple[str, ...]:
        """Dotted global-config keys whose effective value comes from the environment (shown read-only in the UI)."""
        return tuple(key for key, _ in self.env_overrides)
