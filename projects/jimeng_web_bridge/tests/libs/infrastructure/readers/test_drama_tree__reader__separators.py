"""U2-SEC-01: every drama-facing entry point accepts only the canonical `/`-joined form."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError
from libs.infrastructure.readers.drama_config__reader import DramaConfigReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.writers.drama_config__writer import DramaConfigWriter
from tests.libs.infrastructure.support import write_file

EXCLUDE: list[str] = ["_deleted", "_candidates", "renders", "frames", "_blender"]
HY3 = "ai_videos/hs/hy3"
SHOTS = f"{HY3}/5_6/shots"
NOT_DRAMA_ROOTS: list[str] = [
    f"{HY3}/renders",
    f"{HY3}/renders/shots",
    f"{HY3}/props/p1_x/_candidates",
    f"{HY3}/_deleted",
    "ai_videos/hs/_series",
    "ai_videos/notes/sub/deeper",
    "ai_videos/renders",
]
EXCLUDED_BASES: list[str] = [f"{HY3}/renders", f"{HY3}/props/p1_x/_candidates", f"{HY3}/_deleted", "ai_videos/_deleted/hs"]
EXCLUDED_SHOT_DIRS: list[str] = [f"{HY3}/renders/shots/shot03", f"{HY3}/_deleted/shots/shot03"]


def forms(rel: str) -> list[str]:
    head, _, rest = rel.partition("/")
    return [rel, rel.replace("/", "\\"), f"{head}/{rest.replace('/', chr(92))}"]


def cases(targets: list[str], skip_slash: bool = False) -> list[tuple[str, str]]:
    return [(target, form) for target in targets for form in forms(target)[1 if skip_slash else 0 :]]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, "ai_videos/hs/_series/bg1-1.png", b"shared")
    write_file(tmp_path, f"{HY3}/2_世界观人设/characters/c1_老人/c1_老人.md", "#")
    write_file(tmp_path, f"{HY3}/renders/bg1-1.png", b"render")
    write_file(tmp_path, f"{HY3}/renders/characters/c9_r/c9_r.md", "#")
    write_file(tmp_path, f"{HY3}/props/p1_x/_candidates/p1-1/p1-1.png", b"candidate")
    write_file(tmp_path, f"{HY3}/_deleted/bg2-1.png", b"deleted")
    for base in (f"{HY3}/renders/shots", f"{HY3}/_deleted/shots", SHOTS):
        write_file(tmp_path, f"{base}/shot02/shot02_lastframe.png", b"frame")
        write_file(tmp_path, f"{base}/shot03/shot03_previz.mp4", b"video")
    (tmp_path / "ai_videos" / "notes" / "sub" / "deeper").mkdir(parents=True)
    write_file(tmp_path, "ai_videos/renders/shots/shot01/shot01.md", "x")
    write_file(tmp_path, "ai_videos/_deleted/hs/x.png", b"x")
    return tmp_path


@pytest.mark.parametrize(("target", "rel"), cases(NOT_DRAMA_ROOTS))
def test_config_reader_rejects(repo: Path, target: str, rel: str) -> None:
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigReader(RepoSandbox(repo)).read(rel)


@pytest.mark.parametrize(("target", "rel"), cases(NOT_DRAMA_ROOTS))
def test_config_writer_rejects_and_writes_nothing(repo: Path, target: str, rel: str) -> None:
    writer = DramaConfigWriter(RepoSandbox(repo))
    with pytest.raises(DramaRootNotFoundError):
        writer.save(rel, {"drama": {"abbrev": "x"}}, None)
    with pytest.raises(DramaRootNotFoundError):
        writer.save_text(rel, "[drama]\n", None)
    assert list(repo.rglob("jimeng_config.toml")) == []


@pytest.mark.parametrize(("target", "rel"), cases(NOT_DRAMA_ROOTS))
def test_tree_entry_points_reject(repo: Path, target: str, rel: str) -> None:
    tree = DramaTreeReader(RepoSandbox(repo))
    assert tree.search_bases(rel) == ()
    assert tree.list_files(rel, EXCLUDE) == ()
    assert tree.character_cards(rel) == ()
    assert tree.asset_card_paths(rel) == ()
    assert tree.find_character_card(rel, "r").status == "not_found"
    for name in ("bg1-1", "p1-1", "bg2-1"):
        result = tree.resolve_asset_file(rel, name, EXCLUDE)
        assert (result.status, result.reason) == ("not_found", "not_a_drama")


@pytest.mark.parametrize(("target", "rel"), cases([*NOT_DRAMA_ROOTS, HY3], skip_slash=True))
def test_backslash_forms_never_yield_a_drama_root(repo: Path, target: str, rel: str) -> None:
    assert drama_ref.split_drama_rel(repo, rel) is None
    assert drama_ref.drama_root_rel(repo, rel.split("/")) is None
    assert DramaTreeReader(RepoSandbox(repo)).drama_root_of(rel) is None


@pytest.mark.parametrize(("target", "rel"), cases(EXCLUDED_BASES))
def test_file_index_refuses_bases_inside_excluded_dirs(repo: Path, target: str, rel: str) -> None:
    assert FileIndexReader(RepoSandbox(repo)).list_files(rel, []) == ()


@pytest.mark.parametrize(("target", "rel"), [*cases(EXCLUDED_SHOT_DIRS), *cases([f"{SHOTS}/shot03"], skip_slash=True)])
def test_shot_resolvers_refuse_excluded_or_backslash_dirs(repo: Path, target: str, rel: str) -> None:
    tree = DramaTreeReader(RepoSandbox(repo))
    video = tree.resolve_shot_video(rel, "shot03_previz", EXCLUDE)
    frame = tree.resolve_prev_shot_lastframe(rel, "本镜首帧")
    assert (video.status, video.reason) == ("not_found", "invalid_path")
    assert (frame.status, frame.reason) == ("not_found", "invalid_path")


def test_canonical_forms_still_work(repo: Path) -> None:
    sandbox = RepoSandbox(repo)
    tree = DramaTreeReader(sandbox)
    assert tree.search_bases(HY3) == (HY3, "ai_videos/hs/_series")
    assert tree.resolve_asset_file(HY3, "bg1-1", EXCLUDE).path == "ai_videos/hs/_series/bg1-1.png"
    assert tree.resolve_asset_file(HY3, "bg2-1", EXCLUDE).status == "not_found"
    assert tree.resolve_shot_video(f"{SHOTS}/shot03", "shot03_previz", EXCLUDE).path == f"{SHOTS}/shot03/shot03_previz.mp4"
    assert tree.resolve_prev_shot_lastframe(f"{SHOTS}/shot03", "本镜首帧").path == f"{SHOTS}/shot02/shot02_lastframe.png"
    created = DramaConfigWriter(sandbox).save(HY3, {"drama": {"abbrev": "hy3"}}, None)
    assert created.location == f"{HY3}/jimeng_config.toml"
    for rel in forms(HY3)[1:]:
        with pytest.raises(DramaRootNotFoundError):
            DramaConfigWriter(sandbox).save(rel, {}, created.sha256)
    assert [p.relative_to(repo).as_posix() for p in repo.rglob("jimeng_config.toml")] == [f"{HY3}/jimeng_config.toml"]
    assert "renders" not in [node.name for node in tree.list_dramas()]


@pytest.mark.skipif(sys.platform != "win32", reason="a case variant only aliases the same directory on NTFS")
def test_case_variant_root_is_not_canonical(repo: Path) -> None:
    sandbox = RepoSandbox(repo)
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigReader(sandbox).read("ai_videos/HS/hy3")
    with pytest.raises(DramaRootNotFoundError):
        DramaConfigWriter(sandbox).save("ai_videos/HS/hy3", {}, None)
    assert DramaTreeReader(sandbox).search_bases("ai_videos/HS/hy3") == ()
