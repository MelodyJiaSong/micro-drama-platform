from __future__ import annotations

import os

import pytest
import tomlkit

from libs.domain.errors.config__error import ConfigError
from libs.infrastructure.errors.config_io__error import ConfigConflictError, ConfigParseError, ConfigWriteError
from libs.infrastructure.errors.sandbox__error import SandboxError
from tests.libs.application.config_entities.support import HY3, Harness, config_text, sha256_of


def _data(text: str) -> dict[str, dict[str, object]]:
    return tomlkit.parse(text).unwrap()


def test_save_valid_data_preserves_comments_and_key_order(harness: Harness) -> None:
    text = config_text(harness.mapper)
    path = harness.write_config(HY3, text)
    data = _data(text)
    data["video"]["resolution"] = "480p"
    result = harness.config_command.save(HY3, data, None, sha256_of(path))
    assert path.read_text(encoding="utf-8") == text.replace('resolution = "720p"', 'resolution = "480p"', 1)
    assert "# 视频默认档位，按剧调整" in path.read_text(encoding="utf-8")
    assert result.sha256 == sha256_of(path) and result.drama_rel == HY3


def test_save_text_writes_the_text_verbatim(harness: Harness) -> None:
    text = config_text(harness.mapper)
    result = harness.config_command.save("huangye_shenghuo/hy3", None, text, None)
    assert harness.config_path(HY3).read_text(encoding="utf-8") == text
    assert result.location == f"{HY3}/jimeng_config.toml"


@pytest.mark.parametrize(
    ("section", "key", "value", "field_path"),
    [
        ("video", "count", 9, "video.count"),
        ("video", "negative_prompt", "merge", "video.negative_prompt"),
        ("precheck", "estimate_tolerance_pct", 101, "precheck.estimate_tolerance_pct"),
        ("entities", "name_template", "{abbrev.__class__}", "entities.name_template"),
        ("image", "model", "seedance2.5", "image.model"),
        ("drama", "abbrev", "hy 3", "drama.abbrev"),
    ],
)
def test_save_invalid_value_reports_field_path_and_keeps_the_file(
    harness: Harness, section: str, key: str, value: object, field_path: str
) -> None:
    text = config_text(harness.mapper)
    path = harness.write_config(HY3, text)
    before = path.read_bytes()
    data = _data(text)
    data[section][key] = value
    with pytest.raises(ConfigError) as raised:
        harness.config_command.save(HY3, data, None, sha256_of(path))
    assert raised.value.field_path == field_path
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    ("section", "table", "field_path"),
    [
        ("concurrency", {"max_remote_rendering": 50}, "concurrency"),
        ("pacing", {"min_submit_interval_s": 0}, "pacing"),
        ("cli", {"path": "C:/evil.cmd"}, "cli"),
        ("browser", {"channel": "chrome"}, "browser"),
        ("server", {"port": 80}, "server"),
    ],
)
def test_save_rejects_global_sections(harness: Harness, section: str, table: dict[str, object], field_path: str) -> None:
    data = _data(config_text(harness.mapper))
    data[section] = table
    with pytest.raises(ConfigError) as raised:
        harness.config_command.save(HY3, data, None, None)
    assert raised.value.field_path == field_path
    assert not harness.config_path(HY3).exists()


def test_save_rejects_the_global_snapshot_threshold_inside_entities(harness: Harness) -> None:
    data = _data(config_text(harness.mapper))
    data["entities"]["snapshot_stale_h"] = 1
    with pytest.raises(ConfigError) as raised:
        harness.config_command.save(HY3, data, None, None)
    assert raised.value.field_path == "entities.snapshot_stale_h"


def test_save_text_with_a_global_section_is_rejected_before_writing(harness: Harness) -> None:
    text = config_text(harness.mapper) + "\n[concurrency]\nmax_remote_rendering = 5\n"
    with pytest.raises(ConfigError):
        harness.config_command.save(HY3, None, text, None)
    assert not harness.config_path(HY3).exists()


def test_save_with_a_stale_hash_conflicts(harness: Harness) -> None:
    text = config_text(harness.mapper)
    path = harness.write_config(HY3, text)
    stale = sha256_of(path)
    first = _data(text)
    first["video"]["resolution"] = "480p"
    harness.config_command.save(HY3, first, None, stale)
    after_first = path.read_bytes()
    second = _data(text)
    second["video"]["count"] = 2
    with pytest.raises(ConfigConflictError):
        harness.config_command.save(HY3, second, None, stale)
    assert path.read_bytes() == after_first


def test_create_only_save_conflicts_when_the_file_appeared(harness: Harness) -> None:
    harness.write_config(HY3, config_text(harness.mapper))
    with pytest.raises(ConfigConflictError):
        harness.config_command.save(HY3, None, config_text(harness.mapper), None)


def test_save_requires_exactly_one_of_data_or_text(harness: Harness) -> None:
    with pytest.raises(ConfigError):
        harness.config_command.save(HY3, None, None, None)
    with pytest.raises(ConfigError):
        harness.config_command.save(HY3, _data(config_text(harness.mapper)), config_text(harness.mapper), None)


def test_save_unparseable_text_is_rejected(harness: Harness) -> None:
    with pytest.raises(ConfigParseError):
        harness.config_command.save(HY3, None, "[video\n", None)
    assert not harness.config_path(HY3).exists()


@pytest.mark.parametrize("raw", ["huangye_shenghuo\\hy3", "huangye_shenghuo/../hy3", "C:/x"])
def test_save_rejects_unsafe_drama_paths(harness: Harness, raw: str) -> None:
    with pytest.raises(SandboxError):
        harness.config_command.save(raw, None, config_text(harness.mapper), None)


def test_save_write_failure_is_a_typed_error_and_leaves_the_file(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    text = config_text(harness.mapper)
    path = harness.write_config(HY3, text)
    before = path.read_bytes()
    data = _data(text)
    data["video"]["resolution"] = "480p"

    def refuse(src: object, dst: object) -> None:
        raise PermissionError(13, "held open")

    monkeypatch.setattr(os, "replace", refuse)
    with pytest.raises(ConfigWriteError):
        harness.config_command.save(HY3, data, None, sha256_of(path))
    monkeypatch.undo()
    assert path.read_bytes() == before
    assert sorted(p.name for p in path.parent.iterdir() if p.name.endswith(".tmp")) == []


def test_save_editing_rules_preserves_rule_comments(harness: Harness) -> None:
    text = config_text(harness.mapper).replace('label_glob = "场景参考图*"', '# 场景图规则\nlabel_glob = "场景参考图*"', 1)
    path = harness.write_config(HY3, text)
    data = _data(text)
    rules = data["references"]["rules"]
    assert isinstance(rules, list)
    rules[0]["label_glob"] = "场景参考图2*"
    harness.config_command.save(HY3, data, None, sha256_of(path))
    assert path.read_text(encoding="utf-8") == text.replace('"场景参考图*"', '"场景参考图2*"', 1)
