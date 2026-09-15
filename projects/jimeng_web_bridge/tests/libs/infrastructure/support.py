from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURES_DIR: Path = Path(__file__).resolve().parents[2] / "fixtures"
REAL_SHOTS_DIR: Path = FIXTURES_DIR / "real_shots"
REAL_CARDS_DIR: Path = FIXTURES_DIR / "real_cards"
REQUIRE_REAL_REPO_ENV: str = "JWB_REQUIRE_REAL_REPO"


def find_repo_root() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        if (parent / "ai_videos").is_dir() and (parent / "CLAUDE.md").is_file():
            return parent
    return None


def skip_or_fail(reason: str) -> None:
    """The only way a real-repo test may skip: `JWB_REQUIRE_REAL_REPO=1` turns it into a failure at sign-off."""
    if os.environ.get(REQUIRE_REAL_REPO_ENV) == "1":
        pytest.fail(reason)
    pytest.skip(reason)


def require_repo_root() -> Path:
    root = find_repo_root()
    if root is None:
        skip_or_fail("ai_videos tree absent")
        raise AssertionError("unreachable")
    return root


def write_file(root: Path, rel: str, content: str | bytes = "") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
    return path


def make_junction(link: Path, target: Path) -> bool:
    if sys.platform != "win32":
        return False
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, check=False
    )
    return completed.returncode == 0 and link.is_dir()


def require_junction(link: Path, target: Path) -> None:
    """Junction sandbox cases must really run on Windows; only other platforms may skip."""
    if make_junction(link, target):
        return
    if sys.platform == "win32":
        pytest.fail("mklink /J failed on Windows — junction sandbox tests must run, not skip")
    pytest.skip("NTFS junctions exist only on Windows")


def make_symlink(link: Path, target: Path, is_dir: bool) -> bool:
    try:
        os.symlink(target, link, target_is_directory=is_dir)
    except (OSError, NotImplementedError):
        return False
    return True


def short_path_name(path: Path) -> str | None:
    """The 8.3 short form of an existing path, or None when the volume has short names disabled."""
    if sys.platform != "win32":
        return None
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    length = ctypes.windll.kernel32.GetShortPathNameW(str(path), buffer, len(buffer))
    if length == 0 or buffer.value == str(path):
        return None
    return buffer.value
