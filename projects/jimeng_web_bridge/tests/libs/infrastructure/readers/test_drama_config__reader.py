from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.config_io__error import ConfigParseError, DramaRootNotFoundError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from tests.libs.infrastructure.support import write_file

CONFIG = '[drama]\nabbrev = "hy3"  # 集缩写\n\n[entities]\noverrides = { "c1_砌炉的老人" = "hy3_主角" }\n'


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    (tmp_path / "ai_videos" / "hs" / "hy2").mkdir()
    write_file(tmp_path, "ai_videos/hs/hy3/jimeng_config.toml", CONFIG)
    write_file(tmp_path, "ai_videos/broken/jimeng_config.toml", "[drama\n")
    return tmp_path


def test_reads_existing_config(repo: Path) -> None:
    dao = DramaConfigReader(RepoSandbox(repo)).read("ai_videos/hs/hy3")
    assert dao.exists
    assert dao.location == "ai_videos/hs/hy3/jimeng_config.toml"
    assert dao.data == {"drama": {"abbrev": "hy3"}, "entities": {"overrides": {"c1_砌炉的老人": "hy3_主角"}}}
    assert dao.sha256 == hashlib.sha256(CONFIG.encode("utf-8")).hexdigest()
    assert dao.raw_text == CONFIG


def test_missing_config_is_not_an_error(repo: Path) -> None:
    dao = DramaConfigReader(RepoSandbox(repo)).read("ai_videos/hs/hy2")
    assert (dao.exists, dao.data, dao.sha256, dao.raw_text) == (False, {}, None, None)


@pytest.mark.parametrize(
    "drama_rel",
    ["ai_videos/hs", "ai_videos/hs/_series", "ai_videos/../projects", "ai_videos/hs/hy3/shots", "ai_videos/nope", "x/y"],
)
def test_non_drama_roots_are_rejected(repo: Path, drama_rel: str) -> None:
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigReader(RepoSandbox(repo)).read(drama_rel)


def test_invalid_toml(repo: Path) -> None:
    with pytest.raises(ConfigParseError) as caught:
        DramaConfigReader(RepoSandbox(repo)).read("ai_videos/broken")
    assert caught.value.location == "ai_videos/broken/jimeng_config.toml"
