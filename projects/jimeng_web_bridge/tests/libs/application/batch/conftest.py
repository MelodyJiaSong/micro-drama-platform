from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from libs.common.clock import FrozenClock
from tests.libs.application.batch.support import (
    HY3,
    PROJECT_ROOT,
    T0,
    BatchEnv,
    build_env,
    build_template,
    hy3_config,
)
from tests.libs.infrastructure.support import require_repo_root, skip_or_fail


@pytest.fixture(scope="session")
def repo_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    template = tmp_path_factory.mktemp("batch_repo")
    build_template(
        require_repo_root(),
        template,
        lambda rel: skip_or_fail(f"real file missing: {rel} (python tools/assets_sync.py pull)"),
    )
    return template


@pytest.fixture
def env(repo_template: Path, tmp_path: Path) -> Iterator[BatchEnv]:
    repo = tmp_path / "repo"
    shutil.copytree(repo_template, repo)
    global_path = tmp_path / "global.toml"
    shutil.copy2(PROJECT_ROOT / "config" / "global.toml", global_path)
    built = build_env(repo, tmp_path / ".data", global_path, FrozenClock(T0))
    built.write_drama_config(HY3, hy3_config())
    built.seed_snapshot("hy3_主角")
    yield built
    built.client.close()
