from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from tests.libs.infrastructure.support import require_repo_root, skip_or_fail


@pytest.fixture(scope="session")
def real_repo_root() -> Path:
    return require_repo_root()


@pytest.fixture(scope="session")
def real_sandbox(real_repo_root: Path) -> RepoSandbox:
    return RepoSandbox(real_repo_root)


@pytest.fixture
def require_media(real_repo_root: Path) -> Callable[[str], None]:
    def check(rel: str) -> None:
        if not (real_repo_root / rel).is_file():
            skip_or_fail(f"media not pulled: {rel} (python tools/assets_sync.py pull)")

    return check
