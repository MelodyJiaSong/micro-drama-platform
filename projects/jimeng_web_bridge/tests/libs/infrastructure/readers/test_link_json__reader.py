from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.sandbox__error import LinkRejectedError
from libs.infrastructure.readers.link_json__reader import MAX_LINK_BYTES, LinkJsonReader
from tests.libs.infrastructure.support import require_junction, short_path_name, write_file

PROP_DIR = "ai_videos/hs/hy1/props/p1_砍刀"
HY1_PNG = f"{PROP_DIR}/p1_砍刀.png"
OTHER_LINK = f"{PROP_DIR}/other.png.link.json"
LINK = "ai_videos/hs/hy2/props/p1_砍刀/p1_砍刀.png.link.json"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, HY1_PNG, b"png")
    write_file(tmp_path, f"{PROP_DIR}/upper.PNG", b"png")
    write_file(tmp_path, f"{PROP_DIR}/turn.mp4", b"mp4")
    write_file(tmp_path, "ai_videos/hs/hy1/jimeng_config.toml", "[drama]\n")
    write_file(tmp_path, OTHER_LINK, json.dumps({"target": HY1_PNG}))
    write_file(tmp_path, "projects/x.png", b"secret")
    for rel in EXCLUDED_TARGETS:
        write_file(tmp_path, rel, b"png")
    return tmp_path


EXCLUDED_TARGETS: tuple[str, ...] = (
    "ai_videos/hs/hy1/shots/shot01/renders/r.png",
    "ai_videos/_deleted/hs/hy1/d.png",
    f"{PROP_DIR}/_candidates/p1-1/c.png",
    "ai_videos/hs/hy1/shots/shot02/Renders/u.png",
    f"{PROP_DIR}/_Candidates/p1-2/u.png",
)


@pytest.mark.parametrize("target", EXCLUDED_TARGETS)
def test_target_inside_excluded_folder_is_rejected(repo: Path, target: str) -> None:
    assert _reason(_link(repo, json.dumps({"target": target}))) == "target_excluded"


def _link(repo: Path, content: str, rel: str = LINK) -> LinkJsonReader:
    write_file(repo, rel, content)
    return LinkJsonReader(RepoSandbox(repo))


def _reason(reader: LinkJsonReader, rel: str = LINK) -> str:
    with pytest.raises(LinkRejectedError) as caught:
        reader.read(rel)
    assert "secret" not in str(caught.value)
    return caught.value.reason


def test_resolves_target_and_note(repo: Path) -> None:
    reader = _link(repo, json.dumps({"target": HY1_PNG, "note": "跨片复用 · 同一把刀，不重出图"}))
    link = reader.read(LINK)
    assert (link.target_rel, link.link_rel, link.note) == (HY1_PNG, LINK, "跨片复用 · 同一把刀，不重出图")


def test_backslash_target_is_normalised(repo: Path) -> None:
    reader = _link(repo, json.dumps({"target": HY1_PNG.replace("/", "\\")}))
    assert reader.read(LINK).target_rel == HY1_PNG


def test_upper_case_media_extension_matches_its_class(repo: Path) -> None:
    reader = _link(repo, json.dumps({"target": f"{PROP_DIR}/upper.PNG"}))
    assert reader.read(LINK).target_rel == f"{PROP_DIR}/upper.PNG"


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        ("{not json", "malformed"),
        ("[1, 2]", "malformed"),
        (json.dumps({"target": 3}), "malformed"),
        (json.dumps({"target": ""}), "malformed"),
        (json.dumps({"note": "x"}), "malformed"),
        (json.dumps({"target": "ai_videos/../projects/x.png"}), "traversal"),
        (json.dumps({"target": "projects/x.png"}), "outside_ai_videos"),
        (json.dumps({"target": "C:\\Windows\\win.ini"}), "outside_ai_videos"),
        (json.dumps({"target": "\\\\host\\share\\a.png"}), "outside_ai_videos"),
        (json.dumps({"target": f"/{HY1_PNG}"}), "outside_ai_videos"),
        (json.dumps({"target": "AI_VIDEOS/hs/hy1/props/p1_砍刀/p1_砍刀.png"}), "outside_ai_videos"),
        (json.dumps({"target": f"{PROP_DIR}/missing.png"}), "target_missing"),
        (json.dumps({"target": PROP_DIR}), "target_missing"),
        (json.dumps({"target": OTHER_LINK}), "chained_link"),
        (json.dumps({"target": LINK}), "chained_link"),
        (json.dumps({"target": f"{PROP_DIR}/other.png.LINK.JSON"}), "chained_link"),
        (json.dumps({"target": "ai_videos/hs/hy1/p1.png:stream"}), "alternate_data_stream"),
        (json.dumps({"target": "ai_videos/hs/hy1/jimeng_config.toml"}), "target_type_mismatch"),
        (json.dumps({"target": f"{PROP_DIR}/turn.mp4"}), "target_type_mismatch"),
    ],
)
def test_rejections(repo: Path, content: str, reason: str) -> None:
    assert _reason(_link(repo, content)) == reason


def test_short_name_chain_is_rejected(repo: Path) -> None:
    short = short_path_name(repo / OTHER_LINK)
    if short is None:
        pytest.skip("8.3 short names are not available on this volume")
    reader = _link(repo, json.dumps({"target": f"{PROP_DIR}/{Path(short).name}"}))
    assert _reason(reader) == "chained_link"


def test_link_without_media_inner_suffix_is_rejected(repo: Path) -> None:
    rel = "ai_videos/hs/hy2/notes.md.link.json"
    assert _reason(_link(repo, json.dumps({"target": HY1_PNG}), rel), rel) == "target_type_mismatch"


def test_oversized_and_directory_links_are_rejected_before_reading(repo: Path) -> None:
    big = "ai_videos/hs/hy2/big.png.link.json"
    padding = " " * (MAX_LINK_BYTES + 1)
    assert _reason(_link(repo, json.dumps({"target": HY1_PNG}) + padding, big), big) == "too_large"
    folder = "ai_videos/hs/hy2/folder.png.link.json"
    (repo / folder).mkdir(parents=True)
    assert _reason(LinkJsonReader(RepoSandbox(repo)), folder) == "not_a_file"


def test_link_file_itself_must_be_in_sandbox(repo: Path) -> None:
    with pytest.raises(LinkRejectedError):
        LinkJsonReader(RepoSandbox(repo)).read("ai_videos/../projects/x.png.link.json")


def test_target_through_junction_is_rejected(repo: Path, tmp_path: Path) -> None:
    write_file(tmp_path, "outside/a.png", b"x")
    require_junction(tmp_path / "ai_videos" / "hs" / "hy1" / "jx", tmp_path / "outside")
    reader = _link(repo, json.dumps({"target": "ai_videos/hs/hy1/jx/a.png"}))
    assert _reason(reader) == "reparse_point"
