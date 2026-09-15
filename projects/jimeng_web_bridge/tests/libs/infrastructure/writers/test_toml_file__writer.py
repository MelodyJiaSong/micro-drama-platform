from __future__ import annotations

import codecs
import hashlib
import os
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path

import pytest
import tomlkit

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.config_io__error import ConfigConflictError, ConfigWriteError
from libs.infrastructure.writers import toml_file__writer
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from libs.infrastructure.writers.global_config__writer import GlobalConfigWriter
from libs.infrastructure.writers.toml_file__writer import TomlFileWriter
from tests.libs.infrastructure.support import write_file

RULES_AOT = """[references]
search_exclude = ["_deleted", "_candidates", "renders"]  # 硬排除

# 场景规则
[[references.rules]]
# 场景图走 asset_file
label_glob = "场景参考图*"
kind = "image"  # 图
resolver = "asset_file"

[[references.rules]]
# 人物走主体
label_glob = "Seedance 人物 entity"
kind = "entity"
resolver = "entity"

[[references.rules]]
# 承接镜
label_glob = "上一镜末帧*"
kind = "first_frame"
resolver = "prev_shot_lastframe"

[video]
count = 1
"""
RULES_INLINE = """[references]
rules = [
  # 场景图
  { label_glob = "场景参考图*", kind = "image", resolver = "asset_file" },  # 图
  # 人物走主体
  { label_glob = "Seedance 人物 entity", kind = "entity", resolver = "entity" },
  # 承接镜
  { label_glob = "上一镜末帧*", kind = "first_frame", resolver = "prev_shot_lastframe" },
]
"""
PROP_RULE: dict[str, object] = {"label_glob": "道具参考图", "kind": "image", "resolver": "asset_file"}
Rules = list[dict[str, object]]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _edit(rules: Rules) -> None:
    rules[1]["kind"] = "image"


def _insert(rules: Rules) -> None:
    rules.insert(1, dict(PROP_RULE))


def _delete(rules: Rules) -> None:
    del rules[1]


def _append(rules: Rules) -> None:
    rules.append(dict(PROP_RULE))


EDITS = pytest.mark.parametrize("change", [_edit, _insert, _delete, _append], ids=["edit", "insert", "delete", "append"])


def _save_rules(path: Path, change: Callable[[Rules], None]) -> tuple[str, dict[str, object]]:
    raw = path.read_bytes()
    data = tomlkit.parse(raw.decode("utf-8")).unwrap()
    change(data["references"]["rules"])
    TomlFileWriter().save(path, "test.toml", data, _sha(raw))
    text = path.read_bytes().decode("utf-8")
    assert tomlkit.parse(text).unwrap() == data
    return text, data


@EDITS
def test_array_of_tables_keeps_comments_of_untouched_entries(tmp_path: Path, change: Callable[[Rules], None]) -> None:
    text, data = _save_rules(write_file(tmp_path, "c.toml", RULES_AOT), change)
    for comment in ("# 硬排除", "# 场景规则", "# 场景图走 asset_file", "# 图", "# 承接镜"):
        assert comment in text
    assert ("# 人物走主体" in text) == (change is not _delete)
    rules = data["references"]
    assert isinstance(rules, dict)
    assert text.count("[[references.rules]]") == len(rules["rules"])


def _swap_first_two(rules: Rules) -> None:
    rules[0], rules[1] = rules[1], rules[0]


def _move_last_to_front(rules: Rules) -> None:
    rules.insert(0, rules.pop())


def _reverse(rules: Rules) -> None:
    rules.reverse()


REORDERS = pytest.mark.parametrize(
    "change", [_swap_first_two, _move_last_to_front, _reverse], ids=["swap", "last_to_front", "reverse"]
)
TABLE_COMMENTS: tuple[tuple[str, str], ...] = (
    ("# 场景图走 asset_file", 'label_glob = "场景参考图*"'),
    ("# 人物走主体", 'label_glob = "Seedance 人物 entity"'),
    ("# 承接镜", 'label_glob = "上一镜末帧*"'),
)


@REORDERS
def test_reordered_tables_carry_their_own_comments(tmp_path: Path, change: Callable[[Rules], None]) -> None:
    text, _ = _save_rules(write_file(tmp_path, "c.toml", RULES_AOT), change)
    lines = text.split("\n")
    for comment, first_key in TABLE_COMMENTS:
        assert lines[lines.index(first_key) - 1] == comment
    assert text.count("# 图") == 1 and 'kind = "image"  # 图' in text


@REORDERS
def test_reordered_inline_array_round_trips_and_stays_inline(tmp_path: Path, change: Callable[[Rules], None]) -> None:
    text, _ = _save_rules(write_file(tmp_path, "c.toml", RULES_INLINE), change)
    assert "rules = [" in text and "[[references.rules]]" not in text


def test_editing_one_table_rule_is_a_one_line_diff(tmp_path: Path) -> None:
    text, _ = _save_rules(write_file(tmp_path, "c.toml", RULES_AOT), _edit)
    before, after = RULES_AOT.split("\n"), text.split("\n")
    assert len(before) == len(after)
    assert [(a, b) for a, b in zip(before, after) if a != b] == [('kind = "entity"', 'kind = "image"')]


@EDITS
def test_inline_array_stays_inline_and_keeps_comments(tmp_path: Path, change: Callable[[Rules], None]) -> None:
    text, _ = _save_rules(write_file(tmp_path, "c.toml", RULES_INLINE), change)
    assert "rules = [" in text
    assert "[[references.rules]]" not in text
    for comment in ("# 场景图", "# 图", "# 承接镜"):
        assert comment in text


def test_editing_one_inline_rule_is_a_one_line_diff(tmp_path: Path) -> None:
    text, _ = _save_rules(write_file(tmp_path, "c.toml", RULES_INLINE), _edit)
    before, after = RULES_INLINE.split("\n"), text.split("\n")
    assert [(a, b) for a, b in zip(before, after) if a != b] == [
        (
            '  { label_glob = "Seedance 人物 entity", kind = "entity", resolver = "entity" },',
            '  { label_glob = "Seedance 人物 entity", kind = "image", resolver = "entity" },',
        )
    ]


def test_scalar_array_insert_keeps_trailing_comment(tmp_path: Path) -> None:
    path = write_file(tmp_path, "c.toml", RULES_AOT)
    raw = path.read_bytes()
    data = tomlkit.parse(raw.decode("utf-8")).unwrap()
    data["references"]["search_exclude"].insert(1, "frames")
    TomlFileWriter().save(path, "c.toml", data, _sha(raw))
    text = path.read_bytes().decode("utf-8")
    assert 'search_exclude = ["_deleted", "frames", "_candidates", "renders"]  # 硬排除' in text
    assert "# 场景图走 asset_file" in text


def test_emptying_an_array_of_tables_round_trips(tmp_path: Path) -> None:
    path = write_file(tmp_path, "c.toml", RULES_AOT)
    raw = path.read_bytes()
    data = tomlkit.parse(raw.decode("utf-8")).unwrap()
    data["references"]["rules"] = []
    saved = TomlFileWriter().save(path, "c.toml", data, _sha(raw))
    assert saved.data == data
    assert tomlkit.parse(path.read_bytes().decode("utf-8")).unwrap() == data


def _race(saves: tuple[Callable[[], object], Callable[[], object]], monkeypatch: pytest.MonkeyPatch) -> list[str]:
    real_fsync = os.fsync

    def slow_fsync(descriptor: int) -> None:
        time.sleep(0.3)
        real_fsync(descriptor)

    monkeypatch.setattr(toml_file__writer.os, "fsync", slow_fsync)
    barrier = threading.Barrier(len(saves))
    outcomes: list[str] = []
    guard = threading.Lock()

    def run(save: Callable[[], object]) -> None:
        barrier.wait()
        try:
            save()
            outcome = "ok"
        except ConfigConflictError:
            outcome = "conflict"
        except Exception as error:  # noqa: BLE001 — any other outcome must fail the assertion below
            outcome = f"error:{type(error).__name__}"
        with guard:
            outcomes.append(outcome)

    threads = [threading.Thread(target=run, args=(save,)) for save in saves]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return sorted(outcomes)


def test_two_drama_writer_instances_race_to_exactly_one_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = write_file(tmp_path, "ai_videos/flat/jimeng_config.toml", "[video]\ncount = 1\n").read_bytes()
    first, second = DramaConfigWriter(RepoSandbox(tmp_path)), DramaConfigWriter(RepoSandbox(tmp_path))
    outcomes = _race(
        (
            lambda: first.save("ai_videos/flat", {"video": {"count": 2}}, _sha(raw)),
            lambda: second.save("ai_videos/flat", {"video": {"count": 3}}, _sha(raw)),
        ),
        monkeypatch,
    )
    assert outcomes == ["conflict", "ok"]


def test_drama_and_global_writers_share_the_path_lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = write_file(tmp_path, "ai_videos/flat/jimeng_config.toml", "[video]\ncount = 1\n")
    sha = _sha(path.read_bytes())
    drama, global_writer = DramaConfigWriter(RepoSandbox(tmp_path)), GlobalConfigWriter(path)
    outcomes = _race(
        (
            lambda: drama.save("ai_videos/flat", {"video": {"count": 2}}, sha),
            lambda: global_writer.save_text("[video]\ncount = 9\n", sha),
        ),
        monkeypatch,
    )
    assert outcomes == ["conflict", "ok"]


def test_save_text_keeps_crlf_and_bom(tmp_path: Path) -> None:
    original = codecs.BOM_UTF8 + "[video]\r\ncount = 1  # 条数\r\n".encode("utf-8")
    path = write_file(tmp_path, "c.toml", original)
    saved = TomlFileWriter().save_text(path, "c.toml", "[video]\ncount = 2  # 条数\n", _sha(original))
    raw = path.read_bytes()
    assert raw == codecs.BOM_UTF8 + "[video]\r\ncount = 2  # 条数\r\n".encode("utf-8")
    assert saved.sha256 == _sha(raw)


def test_save_text_on_lf_file_normalises_crlf_input(tmp_path: Path) -> None:
    original = b"[video]\ncount = 1\n"
    path = write_file(tmp_path, "c.toml", original)
    TomlFileWriter().save_text(path, "c.toml", "﻿[video]\r\ncount = 2\r\n", _sha(original))
    assert path.read_bytes() == b"[video]\ncount = 2\n"


def test_replace_failure_is_a_typed_error_without_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = write_file(tmp_path, "c.toml", "[video]\ncount = 1\n")
    before = path.read_bytes()

    def deny(source: str, target: str) -> None:
        raise PermissionError(13, "Access is denied", str(target))

    monkeypatch.setattr(toml_file__writer.os, "replace", deny)
    with pytest.raises(ConfigWriteError) as caught:
        TomlFileWriter().save(path, "c.toml", {"video": {"count": 2}}, _sha(before))
    assert caught.value.detail == "PermissionError: Access is denied"
    assert str(tmp_path) not in str(caught.value)
    assert path.read_bytes() == before
    assert [child.name for child in tmp_path.iterdir()] == ["c.toml"]


@pytest.mark.skipif(sys.platform != "win32", reason="only Windows refuses to replace a file another handle holds open")
def test_target_held_open_maps_to_config_write_error(tmp_path: Path) -> None:
    path = write_file(tmp_path, "c.toml", "[video]\ncount = 1\n")
    before = path.read_bytes()
    with path.open("rb"), pytest.raises(ConfigWriteError):
        TomlFileWriter().save(path, "c.toml", {"video": {"count": 2}}, _sha(before))
    assert path.read_bytes() == before
    assert [child.name for child in tmp_path.iterdir()] == ["c.toml"]
