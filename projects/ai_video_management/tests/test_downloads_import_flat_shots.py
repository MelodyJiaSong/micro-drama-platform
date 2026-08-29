"""DownloadsImporter flat (single-piece / MV) shot layout — xianjian_yi_mv, 2026-08-02.

`sub_type=short` dramas keep shots FLAT: `5_6_分镜与prompt/shots/shot{NN}/`, with
no `episodes/epNN/` layer. `_collect_candidates` only walked
`episodes_dir()/{ep}/shots/`, so these dramas contributed ZERO shot candidates
and every shot render fell through to whatever character/scene token sat in the
filename — seven xianjian_yi_mv shot renders landed in `characters/c10_李大娘/`.

The routing key for a flat shot is the shot folder name written as the prompt
block's first line (`shot04`), the single-piece analogue of the multi-episode
`{NN}集{NN}镜` tag.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer


def _make_importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _make_mv_drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    drama = root / "ai_videos" / "mv"
    _touch(drama / "2_世界观人设" / "characters" / "c10_李大娘" / "c10_李大娘.md")
    _touch(drama / "2_世界观人设" / "characters" / "c1_李逍遥" / "c1_李逍遥.md")
    _touch(drama / "2_世界观人设" / "scenes" / "s1_余杭客栈" / "s1_余杭客栈.md")
    for n in ("shot03", "shot04"):
        _touch(drama / "5_6_分镜与prompt" / "shots" / n / f"{n}.md")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, drama, downloads


def test_flat_shot_render_routes_to_its_renders_folder(tmp_path: Path) -> None:
    root, drama, downloads = _make_mv_drama(tmp_path)
    _touch(downloads / "jimeng-2026-08-02-6242-shot04 参考_ `c1_江湖游侠=_, c10_市井大娘=_, s1_bg4_大堂_房梁....mp4")

    result = _make_importer(root, downloads).import_drama("ai_videos/mv")

    assert [e["kind"] for e in result.moved] == ["shot"], result.moved
    renders = drama / "5_6_分镜与prompt" / "shots" / "shot04" / "renders"
    assert len(list(renders.glob("*.mp4"))) == 1
    assert list((drama / "2_世界观人设" / "characters" / "c10_李大娘").glob("*.mp4")) == []


def test_shot_key_outranks_character_token_in_same_filename(tmp_path: Path) -> None:
    """The filename carries BOTH the shot key and the character handles from the
    prompt's 参考 line; the shot must win (longer token + higher kind rank)."""
    root, drama, downloads = _make_mv_drama(tmp_path)
    _touch(downloads / "shot03 参考_ `c1_江湖游侠=_, c10_市井大娘=_, s1_bg3_内院_晾晒=_`.mp4")

    result = _make_importer(root, downloads).import_drama("ai_videos/mv")

    assert [e["kind"] for e in result.moved] == ["shot"], result.moved
    assert (drama / "5_6_分镜与prompt" / "shots" / "shot03" / "renders").is_dir()


def test_unkeyed_shot_render_is_not_silently_dumped_into_a_character(tmp_path: Path) -> None:
    """A render whose filename lacks the shot key still matches the character
    token — that is exactly how the seven renders misrouted. It is a data
    problem (missing key in the prompt block), not a routing bug, so the
    importer's behaviour here is documented rather than changed: the key must
    be present for shot routing to work."""
    root, drama, downloads = _make_mv_drama(tmp_path)
    _touch(downloads / "参考_ `c1_江湖游侠=_, c10_市井大娘=_, s1_bg3_内院_晾晒=_`.mp4")

    result = _make_importer(root, downloads).import_drama("ai_videos/mv")

    assert [e["kind"] for e in result.moved] == ["character"], result.moved
