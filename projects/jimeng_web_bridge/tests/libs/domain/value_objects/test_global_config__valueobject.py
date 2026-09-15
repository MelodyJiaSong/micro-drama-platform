import tomllib
from dataclasses import fields, is_dataclass
from pathlib import Path

import pytest

from libs.common.enums import BackendKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from tests.libs.domain.builders import GLOBAL_DATA, global_data

# FR-5 contract table: every FR-1 key -> one valid sample + invalid samples (rejected with that exact field path).
CONTRACT: list[tuple[str, object, tuple[object, ...]]] = [
    ("server.port", 8790, (0, 70000, "8790")),
    ("routing.video", "cli", ("api", "")),
    ("concurrency.max_remote_rendering", 5, (0, 6, 1.5)),
    ("pacing.min_submit_interval_s", 5, (4, "15s", True)),
    ("wait.timeout_h", 48, (0, 49)),
    ("retries.set_params", 0, (6, -1)),
    ("retries.upload", 5, (-1,)),
    ("retries.download", 0, (6,)),
    ("retries.fill", 2, (3,)),
    ("confirm.token_ttl_min", 5, (4, 241)),
    ("idempotency.retention_h", 168, (0, 169)),
    ("status.parse_failure_threshold", 50, (0, 51)),
    ("entities.snapshot_stale_h", 1, (0, 169)),
    ("download.duration_tolerance_s", 0.1, (0.05, 2.5)),
    ("api.max_call_s", 60, (0, 86)),
    ("api.progress_interval_s", 85, (0, 86)),
    ("api.page_size_default", 200, (0, 201)),
    ("api.page_size_max", 1000, (0,)),
    ("api.max_body_bytes", 1, (0,)),
    ("api.max_batch_items", 1, (0,)),
    ("mcp.thumbnail_max_px", 64, (0,)),
    ("ui.reference_thumb_max_px", 64, ("320",)),
    ("artifacts.preview_max_bytes", 1024, (0,)),
    ("artifacts.preview_retention_days", 1, (0,)),
    ("time.timezone", "UTC", ("Asia Shanghai", "")),
    ("browser.channel", "chromium", ("msedge", "firefox")),
    ("browser.profile_dir", ".data/profile", ("../x", "C:/x", "ai_videos/p", "/abs")),
    ("browser.start_url", "https://jimeng.jianying.com/ai-tool/x", ("http://jimeng.jianying.com/", "https://evil.com/")),
    ("canary.interval_min", 1, (0, -5)),
    ("cli.path", "C:/tools/dreamina.EXE", ("~/bin/dreamina.cmd", "~/bin/dreamina.bat", "~/bin/dreamina.ps1", "~/bin/dreamina", "")),
    ("cli.min_version", "1.4.18", ("1.4", "v1.4.5", "latest")),
    ("notifications.toast", False, ("yes", 1)),
]

VALID = [(key, valid) for key, valid, _ in CONTRACT]
INVALID = [(key, bad) for key, _, bads in CONTRACT for bad in bads]


def with_value(key: str, value: object) -> dict[str, object]:
    data = global_data()
    section, leaf = key.split(".")
    data[section][leaf] = value  # type: ignore[index]
    return data


def test_meta_contract_table_equals_schema() -> None:
    schema: set[str] = set()
    for section in fields(GlobalConfig):
        if is_dataclass(section.type) and section.name not in {"model_limits", "price_table"}:
            schema |= {f"{section.name}.{leaf.name}" for leaf in fields(section.type)}
    assert schema == {key for key, _, _ in CONTRACT}


@pytest.mark.parametrize(("key", "value"), VALID)
def test_valid_sample_accepted(key: str, value: object) -> None:
    config = GlobalConfig.from_dict(with_value(key, value))
    section, leaf = key.split(".")
    assert getattr(getattr(config, section), leaf) == value


@pytest.mark.parametrize(("key", "value"), INVALID)
def test_invalid_sample_rejected_with_field_path(key: str, value: object) -> None:
    with pytest.raises(ConfigError) as err:
        GlobalConfig.from_dict(with_value(key, value))
    assert err.value.field_path == key


def test_defaults_parse() -> None:
    config = GlobalConfig.from_dict(global_data())
    assert config.routing.video is BackendKind.WEB and config.routing.image is BackendKind.CLI
    assert config.api.max_call_s == 85 and config.retries.fill == 1


def test_tracked_global_toml_is_the_test_source() -> None:
    path = Path(__file__).resolve().parents[4] / "config" / "global.toml"
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    assert data == GLOBAL_DATA
    config = GlobalConfig.from_dict(data)
    assert "seedream3.0" in config.model_limits.models and "seedance2.5" in config.model_limits.models


@pytest.mark.parametrize(
    ("mutate", "field_path"),
    [
        (lambda d: d["server"].update(host="0.0.0.0"), "server.host"),
        (lambda d: d["server"].update(token="x"), "server.token"),
        (lambda d: d["routing"].update(image="web"), "routing.image"),
        (lambda d: d.update(budget={"auto_confirm_daily_credits": 0}), "budget"),
        (lambda d: d["confirm"].update(allow_http_auto=True), "confirm.allow_http_auto"),
        (lambda d: d["retries"].pop("fill"), "retries.fill"),
        (lambda d: d.pop("cli"), "cli"),
        (lambda d: d.update(cli="x"), "cli"),
    ],
)
def test_unknown_missing_and_retired_keys(mutate: object, field_path: str) -> None:
    data = global_data()
    mutate(data)  # type: ignore[operator]
    with pytest.raises(ConfigError) as err:
        GlobalConfig.from_dict(data)
    assert err.value.field_path == field_path


def test_test_mode_start_url() -> None:
    local = with_value("browser.start_url", "http://127.0.0.1:9911/")
    assert GlobalConfig.from_dict(local, test_mode=True).browser.start_url == "http://127.0.0.1:9911/"
    with pytest.raises(ConfigError):
        GlobalConfig.from_dict(global_data(), test_mode=True)
    with pytest.raises(ConfigError):
        GlobalConfig.from_dict(local)
