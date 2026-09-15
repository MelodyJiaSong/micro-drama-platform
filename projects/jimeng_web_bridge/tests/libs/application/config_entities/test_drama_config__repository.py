from __future__ import annotations

import pytest
import tomlkit

from libs.application.repositories.drama_config__repository import DramaConfigFileRepository
from libs.domain.repositories.drama_config__repository import DramaConfigRepository
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.infrastructure.errors.config_io__error import ConfigConflictError, DramaRootNotFoundError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from tests.libs.application.config_entities.support import HY3, Harness, config_text, sha256_of


def _repository(harness: Harness) -> DramaConfigRepository:
    return DramaConfigFileRepository(
        DramaConfigReader(harness.sandbox), DramaConfigWriter(harness.sandbox), harness.mapper
    )


def test_read_of_a_drama_without_config_is_none(harness: Harness) -> None:
    assert _repository(harness).read(HY3) is None


def test_read_returns_data_and_the_content_hash(harness: Harness) -> None:
    path = harness.write_config(HY3, config_text(harness.mapper, overrides={"c1_砌炉的老人": "hy3_主角"}))
    stored = _repository(harness).read(HY3)
    assert stored is not None
    assert stored.content_hash == sha256_of(path)
    assert stored.data["entities"]["overrides"] == {"c1_砌炉的老人": "hy3_主角"}  # type: ignore[index]
    DramaConfig.from_dict(stored.data, harness.configs.model_limits())


def test_write_create_only_then_round_trip_keeps_comments(harness: Harness) -> None:
    repository = _repository(harness)
    created = repository.write(HY3, DramaConfig.defaults("hy3"), None)
    path = harness.config_path(HY3)
    assert created == sha256_of(path)
    text = config_text(harness.mapper)
    path.write_text(text, encoding="utf-8")
    data = tomlkit.parse(text).unwrap()
    data["video"]["resolution"] = "480p"
    updated = repository.write(HY3, data, sha256_of(path))
    assert path.read_text(encoding="utf-8") == text.replace('resolution = "720p"', 'resolution = "480p"', 1)
    assert updated == sha256_of(path)


def test_write_with_a_stale_hash_conflicts_and_keeps_the_file(harness: Harness) -> None:
    repository = _repository(harness)
    path = harness.write_config(HY3, config_text(harness.mapper))
    stale = sha256_of(path)
    repository.write(HY3, DramaConfig.defaults("h3"), stale)
    after = path.read_bytes()
    assert sha256_of(path) != stale
    with pytest.raises(ConfigConflictError):
        repository.write(HY3, DramaConfig.defaults("x3"), stale)
    with pytest.raises(ConfigConflictError):
        repository.write(HY3, DramaConfig.defaults("x3"), None)
    assert path.read_bytes() == after


@pytest.mark.parametrize(
    "drama_root", ["huangye_shenghuo/hy3", "ai_videos\\huangye_shenghuo\\hy3", "ai_videos/huangye_shenghuo", f"{HY3}/renders"]
)
def test_non_canonical_or_non_root_paths_are_refused(harness: Harness, drama_root: str) -> None:
    repository = _repository(harness)
    with pytest.raises(DramaRootNotFoundError):
        repository.read(drama_root)
    with pytest.raises(DramaRootNotFoundError):
        repository.write(drama_root, DramaConfig.defaults("hy3"), None)
    assert not harness.config_path(HY3).exists()
