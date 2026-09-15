from __future__ import annotations

from pathlib import Path

import pytest

from libs.application.queries.artifact__query import ArtifactQuery
from libs.infrastructure.errors.artifact__error import InvalidArtifactNameError
from tests.libs.infrastructure.support import make_junction, write_file

JOB: str = "job_20260913100000_1a2b3c4d"
OTHER_JOB: str = "job_20260913100000_ffffffff"


@pytest.fixture
def artifacts(tmp_path: Path) -> tuple[ArtifactQuery, Path]:
    root = tmp_path / "artifacts"
    write_file(root, f"{JOB}/preview_composer.jpg", b"jpg")
    write_file(root, f"{JOB}/failure_login.png", b"png")
    write_file(root, f"{JOB}/private/dom_login.html", "<html>")
    write_file(root, f"{JOB}/trace.zip", b"zip")
    write_file(root, f"{OTHER_JOB}/preview_other.jpg", b"jpg")
    write_file(tmp_path, "bridge.db", b"db")
    return ArtifactQuery(root), root


@pytest.mark.parametrize(
    ("name", "content_type"), [("preview_composer.jpg", "image/jpeg"), ("failure_login.png", "image/png")]
)
def test_screenshots_resolve_inside_the_job_dir(artifacts: tuple[ArtifactQuery, Path], name: str, content_type: str) -> None:
    query, root = artifacts
    result = query.get_screenshot(JOB, name)
    assert (result.file_path, result.content_type) == (root / JOB / name, content_type)


@pytest.mark.parametrize(
    "name",
    [
        "private/dom_login.html",
        "private",
        "dom_login.html",
        "trace.zip",
        "../bridge.db",
        "..%2F..%2Fbridge.db",
        "..\\chrome_profile\\Default\\Cookies",
        "../../bridge.db",
        "preview_composer.png",
        "failure_login.jpg",
        "preview_.jpg",
        "preview_composer.jpg\n",
        "PREVIEW_composer.jpg",
        "preview_composer.jpg/..",
        "preview_a:b.jpg",
        "",
    ],
)
def test_non_screenshot_names_are_rejected(artifacts: tuple[ArtifactQuery, Path], name: str) -> None:
    query, _ = artifacts
    with pytest.raises(InvalidArtifactNameError):
        query.get_screenshot(JOB, name)


@pytest.mark.parametrize("job_id", ["../job", "job/..", "..", "job;DROP TABLE jobs", "", f"{JOB}\n", "a" * 65, "_job"])
def test_malformed_job_ids_are_rejected(artifacts: tuple[ArtifactQuery, Path], job_id: str) -> None:
    query, _ = artifacts
    with pytest.raises(InvalidArtifactNameError):
        query.get_screenshot(job_id, "preview_composer.jpg")


def test_unknown_or_foreign_screenshots_are_not_found(artifacts: tuple[ArtifactQuery, Path]) -> None:
    query, _ = artifacts
    with pytest.raises(FileNotFoundError):
        query.get_screenshot(JOB, "preview_missing.jpg")
    with pytest.raises(FileNotFoundError):
        query.get_screenshot(JOB, "preview_other.jpg")


def test_a_junction_job_dir_is_rejected(artifacts: tuple[ArtifactQuery, Path], tmp_path: Path) -> None:
    query, root = artifacts
    outside = tmp_path / "outside"
    write_file(outside, "preview_x.jpg", b"jpg")
    if not make_junction(root / "job_junction", outside):
        pytest.skip("junctions need Windows")
    with pytest.raises(InvalidArtifactNameError):
        query.get_screenshot("job_junction", "preview_x.jpg")
