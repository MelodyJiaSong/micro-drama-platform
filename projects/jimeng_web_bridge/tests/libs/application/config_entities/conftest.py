from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from tests.libs.application.config_entities.support import Harness, build_harness, build_repo_template


@pytest.fixture(scope="session")
def repo_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("impl05_repo")
    build_repo_template(root)
    return root


@pytest.fixture
def ro_harness(repo_template: Path, tmp_path: Path) -> Iterator[Harness]:
    """Shares the session repo copy: tests using it must not write under `ai_videos/`."""
    harness = build_harness(repo_template, tmp_path)
    yield harness
    harness.db.close()


@pytest.fixture
def harness(repo_template: Path, tmp_path: Path) -> Iterator[Harness]:
    repo = tmp_path / "repo"
    shutil.copytree(repo_template, repo)
    built = build_harness(repo, tmp_path)
    yield built
    built.db.close()
