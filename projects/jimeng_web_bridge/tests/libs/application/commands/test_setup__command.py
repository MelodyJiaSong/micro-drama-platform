from __future__ import annotations

from pathlib import Path

from libs.application.commands.setup__command import TOKEN_ENV_KEY, SetupCommand
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from libs.infrastructure.writers.env_file__writer import EnvFileWriter
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter


def _command() -> SetupCommand:
    return SetupCommand(EnvFileReader(), EnvFileWriter(), SecretKeyWriter())


def test_init_creates_token_data_dirs_and_secret_key(tmp_path: Path) -> None:
    repo, data = tmp_path / "repo", tmp_path / "data"
    repo.mkdir()
    (repo / ".env").write_text("# keep me\nR2_ACCESS_KEY=abc\n", encoding="utf-8")
    result = _command().init(repo, data)
    env = EnvFileReader().read(repo / ".env")
    assert result.token_created and len(env[TOKEN_ENV_KEY]) >= 32
    assert env["R2_ACCESS_KEY"] == "abc"
    assert "# keep me" in (repo / ".env").read_text(encoding="utf-8")
    assert {"artifacts", "logs", "tmp", "chrome_profile"} <= {p.name for p in data.iterdir()}
    assert (data / "secret.key").stat().st_size == 32
    assert env[TOKEN_ENV_KEY] not in repr(result)


def test_init_is_idempotent_and_keeps_an_existing_strong_token(tmp_path: Path) -> None:
    repo, data = tmp_path / "repo", tmp_path / "data"
    repo.mkdir()
    strong = "k" * 40
    (repo / ".env").write_text(f"{TOKEN_ENV_KEY}={strong}\n", encoding="utf-8")
    first = _command().init(repo, data)
    key_bytes = (data / "secret.key").read_bytes()
    second = _command().init(repo, data)
    assert not first.token_created and not second.token_created
    assert EnvFileReader().read(repo / ".env")[TOKEN_ENV_KEY] == strong
    assert not second.secret_key_created and (data / "secret.key").read_bytes() == key_bytes
    assert second.created_data_dirs == ()


def test_init_replaces_a_too_short_token(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".env").write_text(f'export {TOKEN_ENV_KEY}="short"\n', encoding="utf-8")
    result = _command().init(repo, tmp_path / "data")
    text = (repo / ".env").read_text(encoding="utf-8")
    assert result.token_created and text.count(TOKEN_ENV_KEY) == 1 and "short" not in text
