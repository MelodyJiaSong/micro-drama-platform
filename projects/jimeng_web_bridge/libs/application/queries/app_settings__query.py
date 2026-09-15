from __future__ import annotations

import secrets
from collections.abc import Mapping
from pathlib import Path

from libs.common.app_settings import TOKEN_MIN_CHARS, AppSettings, StartupConfigError
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader

DEFAULT_PORT: int = 8790
_ENV_OVERRIDES: tuple[tuple[str, str], ...] = (
    ("JIMENG_BRIDGE_PROFILE_DIR", "browser.profile_dir"),
    ("DREAMINA_CLI_PATH", "cli.path"),
)


class AppSettingsQuery:
    """Resolves boot settings. Fails closed: no strong bearer token, no service.

    In test mode (`JWB_TEST_MODE=1`) the repo-root `.env` is never read, so a test can't
    silently pick up the real token or the real logged-in browser profile.
    """

    def __init__(self, env_reader: EnvFileReader) -> None:
        self._env_reader = env_reader

    def load(self, project_root: Path, environ: Mapping[str, str]) -> AppSettings:
        test_mode = environ.get("JWB_TEST_MODE") == "1"
        repo_root = Path(environ.get("JIMENG_BRIDGE_REPO_ROOT", str(project_root.parents[1])))
        file_values = {} if test_mode else self._env_reader.read(repo_root / ".env")
        merged = {**file_values, **environ}
        token = merged.get("JIMENG_BRIDGE_TOKEN", "")
        if len(token) < TOKEN_MIN_CHARS:
            raise StartupConfigError(
                f"JIMENG_BRIDGE_TOKEN missing or shorter than {TOKEN_MIN_CHARS} characters — run `make init`"
            )
        global_config_path = Path(merged.get("JIMENG_BRIDGE_GLOBAL_CONFIG", str(project_root / "config" / "global.toml")))
        server = GlobalConfigReader(global_config_path).read().data.get("server", {})
        port = server.get("port", DEFAULT_PORT) if isinstance(server, dict) else DEFAULT_PORT
        if not isinstance(port, int) or not 1024 <= port <= 65535:
            raise StartupConfigError(f"server.port must be an integer in 1024–65535, got {port!r}")
        return AppSettings(
            port=port,
            bearer_token=token,
            ui_session=secrets.token_urlsafe(32),
            project_root=project_root,
            repo_root=repo_root,
            data_dir=Path(merged.get("JIMENG_BRIDGE_DATA_DIR", str(project_root / ".data"))),
            global_config_path=global_config_path,
            static_dir=project_root / "apps" / "api" / "static",
            test_mode=test_mode,
            env_overrides=tuple((key, merged[env]) for env, key in _ENV_OVERRIDES if merged.get(env)),
        )
