"""Scene SUBJECT folders (`bg{N}_{主体名}`) vs single-image PLATE folders.

A subject folder holds several named views of one place plus one .md with all
their prompts. A plate folder (`bg{N}_{方位}_{描述}`) still holds exactly one
canonical image. Confusing the two is destructive: the plate path clears the
whole folder before every move, so importing the second view deletes the first
— which is exactly what happened in the field.

Routing key = `bg{N}-{M}` — subject N, view M — pure ASCII and digits at position
0 of the download name, so it survives the out-of-image tool naming the download
after the prompt's first characters and truncating. Matching never depends on the
Chinese part of the name.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    scene = root / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "entropy_city"
    for sub in ("bg1_广场", "bg2_主街", "bg6_广场复原"):
        (scene / sub).mkdir(parents=True)
        _touch(scene / sub / (sub + ".md"), b"prompts")   # the md IS the subject marker
    (scene / "_blender").mkdir(parents=True)
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, scene, downloads


def test_subject_is_decided_by_content_not_shape(tmp_path: Path) -> None:
    """Shape cannot decide it — a legacy single-image plate is two segments too
    (`bg5_高位俯瞰`). The discriminator is the folder's own `{folder}.md`."""
    subject = tmp_path / "bg1_广场"
    subject.mkdir()
    _touch(subject / "bg1_广场.md", b"prompts")
    legacy_plate = tmp_path / "bg5_高位俯瞰"          # two segments, no md
    legacy_plate.mkdir()
    described_plate = tmp_path / "bg1_朝北_主位"      # three segments, HAS an md
    described_plate.mkdir()
    _touch(described_plate / "bg1_朝北_主位.md", b"prompt")

    assert DownloadsImporter._is_subject_folder(subject) is True
    assert DownloadsImporter._is_subject_folder(legacy_plate) is False
    assert DownloadsImporter._is_subject_folder(described_plate) is False
    # the plate keeps routing on its 方位 token, untouched
    assert DownloadsImporter._plate_orientation_token("bg5_高位俯瞰") == "高位俯瞰"


def test_several_views_survive_each_other(tmp_path: Path) -> None:
    """The field failure: three downloads went in, one file came out."""
    root, scene, downloads = _drama(tmp_path)
    for name in ("bg1-1_广场正向.png", "bg1-2_广场反向.png", "bg1-3_广场材质.png"):
        _touch(downloads / name)

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert {e["kind"] for e in result.moved} == {"scene_subject"}, result.moved
    assert result.unmatched == []
    got = sorted(p.name for p in (scene / "bg1_广场").iterdir() if p.suffix == ".png")
    assert got == ["bg1-1.png", "bg1-2.png", "bg1-3.png"]


def test_generator_decorated_names_still_route(tmp_path: Path) -> None:
    """The real download name from the field — the key sits in the MIDDLE, wrapped
    in the generator's own prefix and a timestamp suffix. Anchoring the key to
    position 0 silently fell back to naming the file after the folder, which is
    how `bg1_广场.png` appeared instead of `bg1-1.png`."""
    root, scene, downloads = _drama(tmp_path)
    _touch(downloads / "ElevenLabs_image_gpt-image-2_bg1-1_广场正向 参考_ _2026-08-30T09_22_13.png")
    _touch(downloads / "即梦AI_bg2-1_主街正向_8821 (1).png")
    _touch(downloads / "bg1-3_广场材质.png")                  # bare key still works

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert result.unmatched == [], result.unmatched
    assert (scene / "bg1_广场" / "bg1-1.png").is_file()
    assert (scene / "bg2_主街" / "bg2-1.png").is_file()
    assert (scene / "bg1_广场" / "bg1-3.png").is_file()


def test_first_key_wins_when_the_name_carries_two(tmp_path: Path) -> None:
    """Real jimeng names inline the prompt head, which includes the `参考:` line —
    so the filename holds the TARGET key and the REFERENCE key. The target is the
    prompt's first line, so it always comes first; leftmost match must win."""
    root, scene, downloads = _drama(tmp_path)
    _touch(downloads / "jimeng-2026-08-30-2988-bg2-1_主街正向 参考_ `bg1_广场_bg1-1.png(世界基调)=_....png")
    _touch(downloads / "jimeng-2026-08-30-5471-bg6-1_广场复原正向 参考_ `bg1_广场_bg1-1.png(几何与构图....png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert result.unmatched == [], result.unmatched
    assert (scene / "bg2_主街" / "bg2-1.png").is_file()
    assert (scene / "bg6_广场复原" / "bg6-1.png").is_file()
    # the reference key must NOT have pulled either file into bg1_广场
    assert not (scene / "bg1_广场" / "bg1-1.png").exists()


def test_reroll_overwrites_only_that_view(tmp_path: Path) -> None:
    root, scene, downloads = _drama(tmp_path)
    _touch(scene / "bg1_广场" / "bg1-1.png", b"old")
    _touch(scene / "bg1_广场" / "bg1-2.png", b"reverse")
    _touch(downloads / "ElevenLabs_bg1-1_广场正向 (2).png", b"new")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (scene / "bg1_广场" / "bg1-1.png").read_bytes() == b"new"
    assert (scene / "bg1_广场" / "bg1-2.png").read_bytes() == b"reverse"


def test_state_variant_is_its_own_subject(tmp_path: Path) -> None:
    root, scene, downloads = _drama(tmp_path)
    _touch(downloads / "bg6-1_广场复原正向.png")
    _touch(downloads / "bg1-1_广场正向.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (scene / "bg6_广场复原" / "bg6-1.png").is_file()
    assert (scene / "bg1_广场" / "bg1-1.png").is_file()
    assert not (scene / "bg1_广场" / "bg6-1.png").exists()


def test_ambiguous_subject_number_is_refused_not_guessed(tmp_path: Path) -> None:
    root, scene, downloads = _drama(tmp_path)
    other = scene.parent / "ice_plain" / "bg1_冰原"
    other.mkdir(parents=True)
    _touch(other / "bg1_冰原.md", b"prompts")   # also a subject → `bg1` is ambiguous
    _touch(downloads / "bg1-1_广场正向.png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert result.moved == []
    assert [e["kind"] for e in result.unmatched] == ["unmatched"]
    assert (downloads / "bg1-1_广场正向.png").is_file()  # left untouched


def test_md_survives_the_import(tmp_path: Path) -> None:
    root, scene, downloads = _drama(tmp_path)
    _touch(downloads / "bg1-1_广场正向.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (scene / "bg1_广场" / "bg1_广场.md").read_bytes() == b"prompts"
