from __future__ import annotations

import dataclasses
import json
import logging
import shutil
from pathlib import Path

import pytest
import tomlkit

from libs.application.commands.global_config__command import AUDIT_LOGGER_NAME, GlobalConfigCommand
from libs.application.mappers.drama_config__mapper import DramaConfigMapper
from libs.application.queries.global_config__query import GlobalConfigQuery
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.global_config__valueobject import GLOBAL_SECTIONS
from libs.infrastructure.errors.config_io__error import ConfigConflictError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.toml_file__reader import TomlFileReader
from libs.infrastructure.writers.global_config__writer import GlobalConfigWriter
from tests.libs.application.config_entities.support import GLOBAL_TOML, sha256_of

TOKEN: str = "sentinel-token-0123456789abcdefghijklmnopqrstuv"


@pytest.fixture
def global_path(tmp_path: Path) -> Path:
    target = tmp_path / "config" / "global.toml"
    target.parent.mkdir(parents=True)
    shutil.copyfile(GLOBAL_TOML, target)
    (tmp_path / ".env").write_text(f"JIMENG_BRIDGE_TOKEN={TOKEN}\n", encoding="utf-8")
    (tmp_path / "config" / ".env").write_text(f"JIMENG_BRIDGE_TOKEN={TOKEN}\n", encoding="utf-8")
    return target


def _command(path: Path) -> GlobalConfigCommand:
    return GlobalConfigCommand(
        GlobalConfigReader(path), GlobalConfigWriter(path), TomlFileReader(), DramaConfigMapper(), test_mode=False
    )


def _data(path: Path) -> dict[str, dict[str, object]]:
    return tomlkit.parse(path.read_text(encoding="utf-8")).unwrap()


def _dump(value: object) -> str:
    return json.dumps(dataclasses.asdict(value), ensure_ascii=False, default=str)  # type: ignore[call-overload]


def test_query_returns_values_and_raw_text_without_secrets(global_path: Path) -> None:
    query = GlobalConfigQuery(
        GlobalConfigReader(global_path), DramaConfigMapper(), test_mode=False, env_overridden_keys=("cli.path",)
    )
    result = query.get()
    assert set(result.values) <= set(GLOBAL_SECTIONS)
    assert result.values["cli"] == {"path": "~/bin/dreamina.exe", "min_version": "1.4.5"}
    assert result.validation_error is None and result.sha256 == sha256_of(global_path)
    assert result.overridden_by_env == ("cli.path",)
    assert TOKEN not in _dump(result) and TOKEN not in repr(result)


def test_query_redacts_a_secret_that_leaked_into_the_file(global_path: Path) -> None:
    global_path.write_text(global_path.read_text(encoding="utf-8") + f"\n# pasted by mistake: {TOKEN}\n", encoding="utf-8")
    query = GlobalConfigQuery(GlobalConfigReader(global_path), DramaConfigMapper(), test_mode=False, secret_values=(TOKEN,))
    result = query.get()
    assert TOKEN not in _dump(result)
    assert "[redacted]" in (result.raw_text or "")


def test_query_drops_unknown_top_level_tables_and_reports_them(global_path: Path) -> None:
    global_path.write_text(global_path.read_text(encoding="utf-8") + '\n[secrets]\ntoken = "abc"\n', encoding="utf-8")
    result = GlobalConfigQuery(GlobalConfigReader(global_path), DramaConfigMapper(), test_mode=False).get()
    assert "secrets" not in result.values
    assert result.validation_error is not None and result.validation_error.field_path == "secrets"


@pytest.mark.parametrize(
    ("section", "key", "value", "field_path"),
    [
        ("concurrency", "max_remote_rendering", 6, "concurrency.max_remote_rendering"),
        ("pacing", "min_submit_interval_s", 4, "pacing.min_submit_interval_s"),
        ("api", "max_call_s", 86, "api.max_call_s"),
        ("confirm", "token_ttl_min", 4, "confirm.token_ttl_min"),
        ("retries", "fill", 3, "retries.fill"),
        ("cli", "path", "C:/tools/dreamina.cmd", "cli.path"),
        ("browser", "start_url", "https://evil.example/", "browser.start_url"),
    ],
)
def test_save_out_of_bounds_is_rejected_and_the_file_is_unchanged(
    global_path: Path, section: str, key: str, value: object, field_path: str
) -> None:
    before = global_path.read_bytes()
    data = _data(global_path)
    data[section][key] = value
    with pytest.raises(ConfigError) as raised:
        _command(global_path).save(data, None, sha256_of(global_path))
    assert raised.value.field_path == field_path
    assert global_path.read_bytes() == before


@pytest.mark.parametrize("extra", ["token", "JIMENG_BRIDGE_TOKEN", "env"])
def test_save_rejects_secret_like_keys(global_path: Path, extra: str) -> None:
    data: dict[str, object] = dict(_data(global_path))
    data[extra] = {"value": TOKEN}
    with pytest.raises(ConfigError):
        _command(global_path).save(data, None, sha256_of(global_path))
    assert TOKEN not in global_path.read_text(encoding="utf-8")


def test_save_logs_an_audit_line_when_cli_path_changes(global_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    data = _data(global_path)
    data["cli"]["path"] = "D:/bin/dreamina.exe"
    with caplog.at_level(logging.INFO, logger=AUDIT_LOGGER_NAME):
        result = _command(global_path).save(data, None, sha256_of(global_path))
    assert result.changed_keys == ("cli.path",)
    events = [json.loads(record.getMessage()) for record in caplog.records if record.name == AUDIT_LOGGER_NAME]
    cli = [event for event in events if event["event"] == "global_config.cli_path_changed"]
    assert cli == [{"event": "global_config.cli_path_changed", "before": "~/bin/dreamina.exe", "after": "D:/bin/dreamina.exe"}]
    assert '"D:/bin/dreamina.exe"' in global_path.read_text(encoding="utf-8")
    assert "# 只有 UI 身份可以修改本文件" in global_path.read_text(encoding="utf-8")


def test_save_without_a_cli_path_change_writes_no_cli_audit(global_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    data = _data(global_path)
    data["pacing"]["min_submit_interval_s"] = 20
    with caplog.at_level(logging.INFO, logger=AUDIT_LOGGER_NAME):
        result = _command(global_path).save(data, None, sha256_of(global_path))
    assert result.changed_keys == ("pacing.min_submit_interval_s",)
    assert "cli_path_changed" not in caplog.text


def test_save_text_and_stale_hash_conflict(global_path: Path) -> None:
    stale = sha256_of(global_path)
    text = global_path.read_text(encoding="utf-8").replace("timeout_h = 12", "timeout_h = 13")
    result = _command(global_path).save(None, text, stale)
    assert global_path.read_text(encoding="utf-8") == text and result.sha256 == sha256_of(global_path)
    with pytest.raises(ConfigConflictError):
        _command(global_path).save(None, text.replace("timeout_h = 13", "timeout_h = 14"), stale)
