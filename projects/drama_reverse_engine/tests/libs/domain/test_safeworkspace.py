from __future__ import annotations

import pytest

from libs.domain.errors.workspace__error import PathEscapeError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


WS = SafeWorkspace(root="C:/ws")


def test_normal_relative_path_resolves_under_root() -> None:
    assert SafeWorkspace(root="C:/ws").resolve("d1/ep01/source.mp4").replace("\\", "/") == "C:/ws/d1/ep01/source.mp4"


def test_parent_traversal_rejected() -> None:
    with pytest.raises(PathEscapeError):
        WS.resolve("../outside.txt")


def test_embedded_traversal_rejected() -> None:
    with pytest.raises(PathEscapeError):
        WS.resolve("d1/../../etc/passwd")


def test_absolute_path_rejected() -> None:
    with pytest.raises(PathEscapeError):
        WS.resolve("/etc/passwd")


def test_windows_drive_path_rejected() -> None:
    with pytest.raises(PathEscapeError):
        WS.resolve("C:\\Windows\\system32")


def test_within_accepts_subtree_and_self() -> None:
    assert WS.within("d1/ep01", "d1/ep01/script.md")
    assert WS.within("d1/ep01", "d1/ep01")


def test_within_rejects_traversal_out_of_subtree() -> None:
    assert not WS.within("d1/ep01", "d1/ep01/../../d2/x.md")
    assert not WS.within("d1/ep01", "d1/ep02/x.md")


def test_within_rejects_escaping_target() -> None:
    with pytest.raises(PathEscapeError):
        WS.within("d1/ep01", "../outside.md")
