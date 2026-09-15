from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox, is_reparse_point
from libs.infrastructure.errors.sandbox__error import LinkRejectedError, SandboxError
from libs.infrastructure.readers.asset_card__reader import AssetCardReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.link_json__reader import LinkJsonReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from tests.libs.infrastructure.support import make_symlink, require_junction, short_path_name, write_file

REJECTED: list[tuple[str, str]] = [
    ("", "empty"),
    ("../x", "traversal"),
    ("ai_videos/../projects/x", "traversal"),
    ("ai_videos/a/../../x", "traversal"),
    ("ai_videos\\..\\..\\x", "traversal"),
    (".\\..\\", "traversal"),
    ("C:\\Windows\\win.ini", "drive_path"),
    ("C:/Windows", "drive_path"),
    ("C:foo", "drive_path"),
    ("\\Windows", "absolute_path"),
    ("/etc/passwd", "absolute_path"),
    ("\\\\server\\share\\a.png", "unc_path"),
    ("//server/share", "unc_path"),
    ("\\\\?\\C:\\x", "device_path"),
    ("\\\\?\\UNC\\server\\share", "device_path"),
    ("\\\\.\\pipe\\x", "device_path"),
    ("\\\\.\\PhysicalDrive0", "device_path"),
    ("\\??\\C:\\x", "device_path"),
    ("ai_videos/CON", "reserved_name"),
    ("ai_videos/nul.png", "reserved_name"),
    ("ai_videos/COM1.txt", "reserved_name"),
    ("ai_videos/COM¹.png", "reserved_name"),
    ("ai_videos/CON .txt", "reserved_name"),
    ("ai_videos/LPT9", "reserved_name"),
    ("ai_videos/AUX.md", "reserved_name"),
    ("ai_videos/CONIN$", "reserved_name"),
    ("ai_videos/hs/shot02.md:evil", "alternate_data_stream"),
    ("ai_videos/a.png::$DATA", "alternate_data_stream"),
    ("ai_videos/renders:$I30:$INDEX_ALLOCATION", "alternate_data_stream"),
    ("ai_videos/shot02.md.", "trailing_dot_or_space"),
    ("ai_videos/shot02.md ", "trailing_dot_or_space"),
    ("ai_videos/renders.\\x", "trailing_dot_or_space"),
    ("ai_videos/hy3 \\x", "trailing_dot_or_space"),
    ("ai_videos_backup/x", "outside_sandbox"),
    ("ai_videos2/x", "outside_sandbox"),
    ("projects/jimeng_web_bridge/.env", "outside_sandbox"),
    ("ai_videos/a\nb", "control_char"),
    ("ai_videos/a\x00b", "control_char"),
    ("ai_videos/..%2f..%2fx", "percent_escape"),
    ("ai_videos/%252e%252e%252f", "percent_escape"),
    ("ai_videos/flat/shot01.md%00.png", "percent_escape"),
    ("ai_videos/..%c0%af..%c0%afx", "percent_escape"),
    ("..%5c..%5cCLAUDE.md", "percent_escape"),
    ("ai_videos//x", "empty_segment"),
    ("ai_videos/flat/", "empty_segment"),
    ("ai_videos/a<b", "invalid_char"),
    ("ai_videos/a?b", "invalid_char"),
]


def separator_forms(raw: str) -> list[str]:
    mixed = raw.replace("/", "\\", 1) if "/" in raw else raw.replace("\\", "/", 1)
    return list(dict.fromkeys([raw, raw.replace("/", "\\"), raw.replace("\\", "/"), mixed]))


@pytest.fixture
def sandbox(tmp_path: Path) -> RepoSandbox:
    (tmp_path / "ai_videos" / "hs" / "hy3").mkdir(parents=True)
    (tmp_path / "ai_videos_backup").mkdir()
    (tmp_path / "projects").mkdir()
    return RepoSandbox(tmp_path, extra_write_roots=(tmp_path / ".data",))


@pytest.mark.parametrize(("raw", "reason"), REJECTED)
def test_read_rejects(sandbox: RepoSandbox, raw: str, reason: str) -> None:
    verdict = sandbox.check_read(raw)
    assert verdict.path is None
    assert verdict.violation == reason


@pytest.mark.parametrize(("raw", "reason"), REJECTED)
def test_write_rejects(sandbox: RepoSandbox, raw: str, reason: str) -> None:
    verdict = sandbox.check_write(raw)
    assert verdict.path is None
    assert verdict.violation == reason


@pytest.mark.parametrize(("raw", "reason"), REJECTED)
def test_every_separator_form_is_rejected_at_every_entry_point(sandbox: RepoSandbox, raw: str, reason: str) -> None:
    for form in separator_forms(raw):
        assert sandbox.check_read(form).violation is not None, form
        assert sandbox.check_write(form).violation is not None, form
        with pytest.raises(SandboxError):
            ShotPromptReader(sandbox).read(form)
        with pytest.raises(SandboxError):
            AssetCardReader(sandbox).read(form)
        with pytest.raises(SandboxError):
            DramaTreeReader(sandbox).sha256(form)
        with pytest.raises(LinkRejectedError):
            LinkJsonReader(sandbox).read(form)


@pytest.mark.parametrize(
    "rel",
    [
        "ai_videos/hs/hy3/2_世界观人设/characters/c1_砌炉的老人/c1-1.png",
        "ai_videos/hs/hy3/renders/jimeng-2026-09-13-6571-shot01 参考_ `bg9-1(场景参考图)=_`，`bg1-1(场景参考图....mp4",
        "ai_videos/hs",
    ],
)
def test_read_accepts_real_shapes_in_every_separator_form(sandbox: RepoSandbox, rel: str) -> None:
    for form in separator_forms(rel):
        verdict = sandbox.check_read(form)
        assert verdict.ok, form
        assert verdict.rel == rel
        assert verdict.path == (sandbox.repo_root / rel).resolve()
    assert sandbox.check_read("ai_videos").rel == "ai_videos"


@pytest.mark.skipif(sys.platform != "win32", reason="NTFS is case-insensitive; POSIX treats AI_VIDEOS as a sibling")
def test_case_insensitive_root_on_windows(sandbox: RepoSandbox) -> None:
    assert sandbox.check_read("AI_VIDEOS/hs/hy3").rel == "ai_videos/hs/hy3"


def test_short_name_sibling_is_outside(sandbox: RepoSandbox, tmp_path: Path) -> None:
    backup = short_path_name(tmp_path / "ai_videos_backup")
    real = short_path_name(tmp_path / "ai_videos")
    if backup is None or real is None:
        pytest.skip("8.3 short names are not available on this volume")
    assert sandbox.check_read(f"{Path(backup).name}/x.png").violation == "outside_sandbox"
    verdict = sandbox.check_read(f"{Path(real).name}/hs")
    assert (verdict.ok, verdict.rel) == (True, "ai_videos/hs")


def test_write_scope(sandbox: RepoSandbox, tmp_path: Path) -> None:
    assert sandbox.check_write("ai_videos/hs/hy3/renders/shot02_x.mp4").ok
    assert sandbox.check_write("ai_videos/_deleted/hs/hy3/p3-1.20260913-101010.png").ok
    assert sandbox.check_write("ai_videos").violation == "outside_sandbox"
    assert sandbox.check_write("projects/jimeng_web_bridge/config/global.toml").violation == "outside_sandbox"
    assert sandbox.check_read(".data/tmp/a.png").violation == "outside_sandbox"
    assert sandbox.check_write_path(tmp_path / ".data" / "tmp" / "a.png").ok
    assert sandbox.check_write_path(tmp_path / ".data").violation == "outside_sandbox"
    assert sandbox.check_write_path(tmp_path / "projects" / "x").violation == "outside_sandbox"
    assert sandbox.check_write_path(tmp_path / "ai_videos" / "hs" / "hy3" / "renders" / "x.mp4").ok
    assert sandbox.check_write_path(Path("relative") / "x.png").violation == "relative_path"
    device_form = Path("\\\\?\\" + str(tmp_path / ".data" / "tmp" / "a.png"))
    assert sandbox.check_write_path(device_form).path is None


@pytest.mark.parametrize(
    ("parts", "reason"),
    [
        ((".data", "x."), "trailing_dot_or_space"),
        ((".data", "x "), "trailing_dot_or_space"),
        ((".data", "x.."), "trailing_dot_or_space"),
        ((".data", "a.", "b"), "trailing_dot_or_space"),
        ((".data", "tmp", "nul "), "trailing_dot_or_space"),
        (("ai_videos", "hs", "hy3", "renders", "shot01.mp4."), "trailing_dot_or_space"),
        ((".data", "..", "projects", "x"), "traversal"),
        ((".data", "CON"), "reserved_name"),
        ((".data", "tmp", "a.png:ads"), "alternate_data_stream"),
        ((".data", "a\nb"), "control_char"),
        ((".data", "a\tb"), "control_char"),
        ((".data", "a\x00b"), "control_char"),
        ((".data", "tmp", "a\x7fb.png"), "control_char"),
    ],
)
def test_write_path_checks_raw_segments_before_normalisation(
    sandbox: RepoSandbox, tmp_path: Path, parts: tuple[str, ...], reason: str
) -> None:
    assert sandbox.check_write_path(tmp_path.joinpath(*parts)).violation == reason


def test_junction_anywhere_in_chain_is_rejected(sandbox: RepoSandbox, tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    write_file(outside, "secret.png", b"x")
    escape = tmp_path / "ai_videos" / "hs" / "escape"
    inward = tmp_path / "ai_videos" / "hs" / "inward"
    require_junction(escape, outside)
    require_junction(inward, tmp_path / "ai_videos" / "hs" / "hy3")
    assert is_reparse_point(escape)
    for form in separator_forms("ai_videos/hs/escape/secret.png"):
        assert sandbox.check_read(form).violation == "reparse_point"
    assert sandbox.check_read("ai_videos/hs/escape").violation == "reparse_point"
    assert sandbox.check_write("ai_videos/hs/escape/new.png").violation == "reparse_point"
    assert sandbox.check_read("ai_videos/hs/inward/x.png").violation == "reparse_point"
    assert sandbox.check_write_path(escape / "new.png").violation == "reparse_point"


def test_junction_as_data_root_is_rejected(tmp_path: Path) -> None:
    real_data = tmp_path / "real_data"
    real_data.mkdir()
    (tmp_path / "ai_videos").mkdir()
    require_junction(tmp_path / ".data", real_data)
    sandbox = RepoSandbox(tmp_path, extra_write_roots=(tmp_path / ".data",))
    assert sandbox.check_write_path(tmp_path / ".data" / "tmp" / "x").violation in {"reparse_point", "outside_sandbox"}


def test_hardlink_is_accepted_without_crashing(sandbox: RepoSandbox, tmp_path: Path) -> None:
    outside = write_file(tmp_path, "outside/secret.png", b"x")
    try:
        os.link(outside, tmp_path / "ai_videos" / "hs" / "hy3" / "hard.png")
    except OSError:
        pytest.skip("hardlinks are not supported on this filesystem")
    # Accepted risk R-5: a hardlink is indistinguishable from a regular file by path.
    assert sandbox.check_read("ai_videos/hs/hy3/hard.png").ok
    assert DramaTreeReader(sandbox).sha256("ai_videos/hs/hy3/hard.png") == hashlib.sha256(b"x").hexdigest()


def test_symlink_is_rejected(sandbox: RepoSandbox, tmp_path: Path) -> None:
    target = write_file(tmp_path, ".env", "JIMENG_BRIDGE_TOKEN=x")
    link = tmp_path / "ai_videos" / "hs" / "hy3" / "env.png"
    if not make_symlink(link, target, is_dir=False):
        pytest.skip("symlink creation not permitted (Windows needs Developer Mode)")
    assert sandbox.check_read("ai_videos/hs/hy3/env.png").violation == "reparse_point"
