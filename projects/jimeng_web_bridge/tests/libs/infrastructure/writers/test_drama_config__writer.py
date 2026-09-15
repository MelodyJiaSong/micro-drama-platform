from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.config_io__error import (
    ConfigConflictError,
    ConfigParseError,
    DramaRootNotFoundError,
)
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from tests.libs.infrastructure.support import write_file

DRAMA = "ai_videos/hs/hy3"
COMMENTED = """# hy3 即梦 config（propose 生成，用户已确认）
[drama]
abbrev = "hy3"  # 集缩写

[entities]
name_template = "{abbrev}_{character_name}"
# 角色卡目录 → 已有主体
overrides = { "c1_砌炉的老人" = "hy3_主角" }

[video]
model = "seedance2.5"
count = 1  # 每镜条数
negative_prompt = "platform_field_or_omit"

[[references.rules]]
label_glob = "场景参考图*"
kind = "image"
resolver = "asset_file"
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, f"{DRAMA}/jimeng_config.toml", COMMENTED)
    (tmp_path / "ai_videos" / "hs" / "hy4").mkdir()
    return tmp_path


def _load(repo: Path) -> tuple[dict[str, object], str]:
    dao = DramaConfigReader(RepoSandbox(repo)).read(DRAMA)
    assert dao.sha256 is not None
    return copy.deepcopy(dao.data), dao.sha256


def _config_path(repo: Path) -> Path:
    return repo / DRAMA / "jimeng_config.toml"


def test_unchanged_save_is_byte_identical(repo: Path) -> None:
    data, sha = _load(repo)
    before = _config_path(repo).read_bytes()
    saved = DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    assert _config_path(repo).read_bytes() == before
    assert saved.sha256 == sha


def test_single_value_change_is_a_single_line_diff(repo: Path) -> None:
    data, sha = _load(repo)
    video = data["video"]
    assert isinstance(video, dict)
    video["count"] = 2
    saved = DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    before = COMMENTED.split("\n")
    after = _config_path(repo).read_text(encoding="utf-8").split("\n")
    assert len(before) == len(after)
    assert [(a, b) for a, b in zip(before, after) if a != b] == [("count = 1  # 每镜条数", "count = 2  # 每镜条数")]
    assert saved.sha256 == hashlib.sha256(_config_path(repo).read_bytes()).hexdigest()


def test_added_override_lands_inside_its_table(repo: Path) -> None:
    data, sha = _load(repo)
    entities = data["entities"]
    assert isinstance(entities, dict)
    entities["overrides"] = {"c1_砌炉的老人": "hy3_主角", "c2_獾": "hy3_獾"}
    DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    text = _config_path(repo).read_text(encoding="utf-8")
    assert "# 角色卡目录 → 已有主体" in text
    assert DramaConfigReader(RepoSandbox(repo)).read(DRAMA).data["entities"] == {
        "name_template": "{abbrev}_{character_name}",
        "overrides": {"c1_砌炉的老人": "hy3_主角", "c2_獾": "hy3_獾"},
    }
    assert text.index("c2_獾") < text.index("[video]")


def test_removed_key_is_dropped(repo: Path) -> None:
    data, sha = _load(repo)
    video = data["video"]
    assert isinstance(video, dict)
    del video["negative_prompt"]
    DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    assert "negative_prompt" not in _config_path(repo).read_text(encoding="utf-8")


def test_stale_hash_conflicts_and_keeps_external_edit(repo: Path) -> None:
    data, sha = _load(repo)
    external = COMMENTED.replace("count = 1", "count = 5")
    _config_path(repo).write_bytes(external.encode("utf-8"))
    with pytest.raises(ConfigConflictError) as caught:
        DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    assert caught.value.expected_sha256 == sha
    assert caught.value.current_sha256 == hashlib.sha256(external.encode("utf-8")).hexdigest()
    assert _config_path(repo).read_text(encoding="utf-8") == external


def test_second_save_with_same_read_hash_conflicts(repo: Path) -> None:
    data, sha = _load(repo)
    writer = DramaConfigWriter(RepoSandbox(repo))
    writer.save(DRAMA, {**data, "drama": {"abbrev": "hy3x"}}, sha)
    with pytest.raises(ConfigConflictError):
        writer.save(DRAMA, data, sha)


def test_create_requires_expected_none(repo: Path) -> None:
    writer = DramaConfigWriter(RepoSandbox(repo))
    created = writer.save("ai_videos/hs/hy4", {"drama": {"abbrev": "hy4"}}, None)
    assert created.exists and created.data == {"drama": {"abbrev": "hy4"}}
    with pytest.raises(ConfigConflictError):
        writer.save("ai_videos/hs/hy4", {"drama": {"abbrev": "x"}}, None)
    _, sha = _load(repo)
    with pytest.raises(ConfigConflictError):
        writer.save(DRAMA, {}, None)
    assert sha


def test_crlf_file_stays_crlf(repo: Path) -> None:
    _config_path(repo).write_bytes(COMMENTED.replace("\n", "\r\n").encode("utf-8"))
    data, sha = _load(repo)
    video = data["video"]
    assert isinstance(video, dict)
    video["resolution"] = "720p"
    DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    raw = _config_path(repo).read_bytes()
    assert b'resolution = "720p"\r\n' in raw
    assert raw.count(b"\n") == raw.count(b"\r\n")


def test_unencodable_value_leaves_file_untouched(repo: Path) -> None:
    data, sha = _load(repo)
    before = _config_path(repo).read_bytes()
    data["video"] = {"count": object()}
    with pytest.raises(ConfigParseError):
        DramaConfigWriter(RepoSandbox(repo)).save(DRAMA, data, sha)
    assert _config_path(repo).read_bytes() == before
    assert sorted(p.name for p in (repo / DRAMA).iterdir()) == ["jimeng_config.toml"]


def test_save_text_validates_then_writes_verbatim(repo: Path) -> None:
    _, sha = _load(repo)
    writer = DramaConfigWriter(RepoSandbox(repo))
    with pytest.raises(ConfigParseError):
        writer.save_text(DRAMA, "[video\n", sha)
    assert _config_path(repo).read_text(encoding="utf-8") == COMMENTED
    text = COMMENTED + "\n# 手改\n"
    saved = writer.save_text(DRAMA, text, sha)
    assert _config_path(repo).read_text(encoding="utf-8") == text
    assert saved.raw_text == text
    assert sorted(p.name for p in (repo / DRAMA).iterdir()) == ["jimeng_config.toml"]


@pytest.mark.parametrize("drama_rel", ["ai_videos/hs", "ai_videos/../projects", "ai_videos/hs/_series", "ai_videos/nope"])
def test_only_drama_root_config_is_writable(repo: Path, drama_rel: str) -> None:
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigWriter(RepoSandbox(repo)).save(drama_rel, {}, None)
