from __future__ import annotations

import secrets
from pathlib import Path

from libs.application.dtos.setup__dto import SetupCdto
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from libs.infrastructure.writers.env_file__writer import EnvFileWriter
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter

TOKEN_ENV_KEY: str = "JIMENG_BRIDGE_TOKEN"
TOKEN_MIN_CHARS: int = 32
DATA_SUBDIRS: tuple[str, ...] = ("artifacts", "logs", "tmp", "chrome_profile")


class SetupCommand:
    def __init__(self, env_reader: EnvFileReader, env_writer: EnvFileWriter, secret_key_writer: SecretKeyWriter) -> None:
        self._env_reader = env_reader
        self._env_writer = env_writer
        self._secret_key_writer = secret_key_writer

    def init(self, repo_root: Path, data_dir: Path) -> SetupCdto:
        env_path = repo_root / ".env"
        current = self._env_reader.read(env_path).get(TOKEN_ENV_KEY, "")
        token_created = len(current) < TOKEN_MIN_CHARS
        if token_created:
            self._env_writer.upsert(env_path, TOKEN_ENV_KEY, secrets.token_urlsafe(32))
        created_dirs: list[str] = []
        for name in DATA_SUBDIRS:
            target = data_dir / name
            if not target.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                created_dirs.append(name)
        secret_created = self._secret_key_writer.ensure(data_dir / "secret.key")
        return SetupCdto(
            env_path=str(env_path),
            token_created=token_created,
            data_dir=str(data_dir),
            created_data_dirs=tuple(created_dirs),
            secret_key_created=secret_created,
        )
