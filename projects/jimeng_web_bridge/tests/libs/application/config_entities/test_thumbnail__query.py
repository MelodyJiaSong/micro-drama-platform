from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from PIL import Image

from libs.application.queries.thumbnail__query import ThumbnailQuery
from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.artifact__error import UnsupportedThumbnailSourceError
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.thumbnail__reader import ThumbnailReader
from tests.libs.application.config_entities.support import GLOBAL_TOML
from tests.libs.infrastructure.support import make_junction, write_file

IMAGE: str = "ai_videos/d/characters/c1_x/c1-1.png"


@pytest.fixture
def setup(tmp_path: Path) -> tuple[ThumbnailQuery, Path]:
    repo = tmp_path / "repo"
    data = tmp_path / "data"
    Image.new("RGB", (1200, 800), (200, 120, 40)).save(write_file(repo, IMAGE, b""))
    write_file(repo, "ai_videos/d/notes.md", "# notes")
    write_file(repo, "ai_videos/d/fake.png", b"not an image")
    write_file(repo, "ai_videos/d/c1.png.link.json", '{"target": "ai_videos/d/characters/c1_x/c1-1.png"}')
    Image.new("RGB", (10, 10)).save(write_file(repo, "secret.png", b""))
    Image.new("RGB", (10, 10)).save(write_file(repo, "ai_videos_backup/x.png", b""))
    global_path = tmp_path / "global.toml"
    shutil.copyfile(GLOBAL_TOML, global_path)
    query = ThumbnailQuery(RepoSandbox(repo, (data,)), ThumbnailReader(data / "thumbs"), GlobalConfigReader(global_path), False)
    return query, tmp_path


def test_thumbnail_is_a_jpeg_capped_by_the_ui_config(setup: tuple[ThumbnailQuery, Path]) -> None:
    query, root = setup
    result = query.get(IMAGE)
    assert result.content_type == "image/jpeg"
    assert (result.width, result.height) == (320, 213)
    assert result.file_path.is_file() and result.file_path.parent == root / "data" / "thumbs"


@pytest.mark.parametrize(("requested", "edge"), [(100, 100), (5000, 320), (1, 16)])
def test_thumbnail_requested_edge_is_clamped(setup: tuple[ThumbnailQuery, Path], requested: int, edge: int) -> None:
    query, _ = setup
    result = query.get(IMAGE, requested)
    assert max(result.width, result.height) == edge


@pytest.mark.parametrize(
    "raw",
    [
        "ai_videos/../secret.png",
        "../secret.png",
        "secret.png",
        "ai_videos_backup/x.png",
        "C:/Windows/x.png",
        "//server/share/x.png",
        "ai_videos\\d\\characters\\c1_x\\c1-1.png",
        "ai_videos/d/characters/c1_x/c1-1.png:stream",
        "/ai_videos/d/characters/c1_x/c1-1.png",
        "",
    ],
)
def test_thumbnail_rejects_paths_outside_ai_videos(setup: tuple[ThumbnailQuery, Path], raw: str) -> None:
    query, _ = setup
    with pytest.raises(SandboxError):
        query.get(raw)


@pytest.mark.parametrize("raw", ["ai_videos/d/notes.md", "ai_videos/d/fake.png", "ai_videos/d/c1.png.link.json"])
def test_thumbnail_rejects_non_images(setup: tuple[ThumbnailQuery, Path], raw: str) -> None:
    query, _ = setup
    with pytest.raises(UnsupportedThumbnailSourceError):
        query.get(raw)


def test_thumbnail_of_a_missing_file_is_not_found(setup: tuple[ThumbnailQuery, Path]) -> None:
    query, _ = setup
    with pytest.raises(FileNotFoundError):
        query.get("ai_videos/d/missing.png")


def test_thumbnail_rejects_a_junction_inside_ai_videos(setup: tuple[ThumbnailQuery, Path]) -> None:
    query, root = setup
    outside = root / "outside"
    Image.new("RGB", (10, 10)).save(write_file(outside, "x.png", b""))
    if not make_junction(root / "repo" / "ai_videos" / "j", outside):
        pytest.skip("junctions need Windows")
    with pytest.raises(SandboxError):
        query.get("ai_videos/j/x.png")
