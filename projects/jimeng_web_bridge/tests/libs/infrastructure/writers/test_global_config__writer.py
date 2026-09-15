from __future__ import annotations

import copy
import shutil
from pathlib import Path

import pytest

from libs.infrastructure.errors.config_io__error import ConfigConflictError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.writers.global_config__writer import GlobalConfigWriter

PROJECT_GLOBAL_TOML: Path = Path(__file__).resolve().parents[4] / "config" / "global.toml"


@pytest.fixture
def global_toml(tmp_path: Path) -> Path:
    target = tmp_path / "global.toml"
    shutil.copyfile(PROJECT_GLOBAL_TOML, target)
    return target


def test_real_global_config_round_trips_byte_identical(global_toml: Path) -> None:
    dao = GlobalConfigReader(global_toml).read()
    GlobalConfigWriter(global_toml).save(copy.deepcopy(dao.data), dao.sha256)
    assert global_toml.read_bytes() == PROJECT_GLOBAL_TOML.read_bytes()


def test_changing_one_threshold_keeps_comments(global_toml: Path) -> None:
    dao = GlobalConfigReader(global_toml).read()
    data = copy.deepcopy(dao.data)
    wait = data["wait"]
    assert isinstance(wait, dict)
    wait["timeout_h"] = 6
    GlobalConfigWriter(global_toml).save(data, dao.sha256)
    before = PROJECT_GLOBAL_TOML.read_text(encoding="utf-8").split("\n")
    after = global_toml.read_text(encoding="utf-8").split("\n")
    assert [(a, b) for a, b in zip(before, after) if a != b] == [("timeout_h = 12", "timeout_h = 6")]
    assert len(before) == len(after)


def test_conflict_on_changed_file(global_toml: Path) -> None:
    dao = GlobalConfigReader(global_toml).read()
    global_toml.write_text(global_toml.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ConfigConflictError):
        GlobalConfigWriter(global_toml).save(dao.data, dao.sha256)
