"""UT-S-MARK-01: `JWB_REQUIRE_REAL_REPO=1` must turn every real-repo skip into a failure."""
from __future__ import annotations

from pathlib import Path

import pytest

from tests.libs.infrastructure import support

REAL_ONLY_TEST_FILES: tuple[str, ...] = (
    "readers/test_drama_tree__reader__real.py",
    "readers/test_shot_prompt__reader__sweep.py",
)


def test_skip_or_fail_skips_without_the_switch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(support.REQUIRE_REAL_REPO_ENV, raising=False)
    with pytest.raises(pytest.skip.Exception):
        support.skip_or_fail("media not pulled")


def test_skip_or_fail_fails_with_the_switch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(support.REQUIRE_REAL_REPO_ENV, "1")
    with pytest.raises(pytest.fail.Exception):
        support.skip_or_fail("media not pulled")


def test_missing_repo_root_honours_the_switch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(support, "find_repo_root", lambda: None)
    monkeypatch.delenv(support.REQUIRE_REAL_REPO_ENV, raising=False)
    with pytest.raises(pytest.skip.Exception):
        support.require_repo_root()
    monkeypatch.setenv(support.REQUIRE_REAL_REPO_ENV, "1")
    with pytest.raises(pytest.fail.Exception):
        support.require_repo_root()


def test_real_only_tests_never_skip_directly() -> None:
    base = Path(support.__file__).resolve().parent
    for rel in REAL_ONLY_TEST_FILES:
        assert "pytest.skip(" not in (base / rel).read_text(encoding="utf-8"), rel
