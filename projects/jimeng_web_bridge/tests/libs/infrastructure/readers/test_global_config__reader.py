from __future__ import annotations

import hashlib
from pathlib import Path

from libs.infrastructure.readers.global_config__reader import GlobalConfigReader

PROJECT_GLOBAL_TOML: Path = Path(__file__).resolve().parents[4] / "config" / "global.toml"


def test_reads_project_global_config() -> None:
    dao = GlobalConfigReader(PROJECT_GLOBAL_TOML).read()
    assert dao.exists
    assert dao.location == "config/global.toml"
    assert dao.sha256 == hashlib.sha256(PROJECT_GLOBAL_TOML.read_bytes()).hexdigest()
    server = dao.data["server"]
    assert isinstance(server, dict) and server["port"] == 8790
    model_limits = dao.data["model_limits"]
    assert isinstance(model_limits, dict) and "seedance2.5" in model_limits["models"]


def test_missing_global_config(tmp_path: Path) -> None:
    dao = GlobalConfigReader(tmp_path / "global.toml", location="test/global.toml").read()
    assert (dao.exists, dao.location, dao.data) == (False, "test/global.toml", {})
