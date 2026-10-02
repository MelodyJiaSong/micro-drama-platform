"""Downloads land by their prop routing key (follow-up 174).

Every object is a prop, `props/p{N}_{名}/`. A scene object (it carries
`asset.toml`) takes its three views under the card's ```text first lines
(`p15-1_正面` / `-2_侧面` / `-3_背面`) and its one mesh as `mesh/p{N}.glb`.
A story prop (no `asset.toml`) keeps its `p{N}-{M}.{ext}` anchors. A GLB is
imported by prop key only.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer

INN = "p15_两层石木旅店"
INN_CARD = """# p15 两层石木旅店

```text
p15-1_正面
A long two-storey inn, front view
```

```text
p15-2_侧面
side view
```
"""
HAMMER = "p3_父亲的旧双手锤"
HAMMER_CARD = """# 父亲的旧双手锤

```text
p3_父亲的旧双手锤
锚点 prompt
```
"""


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    props = root / "ai_videos" / "d" / "2_世界观人设" / "props"
    (props / INN).mkdir(parents=True)
    (props / INN / f"{INN}.md").write_text(INN_CARD, encoding="utf-8")
    _touch(props / INN / "asset.toml", b'[asset]\nkey = "p15"\n')
    (props / HAMMER).mkdir()
    (props / HAMMER / f"{HAMMER}.md").write_text(HAMMER_CARD, encoding="utf-8")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, props, downloads


def _run(root: Path, downloads: Path):
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    importer = DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)
    return importer.import_drama("ai_videos/d")


def test_object_views_land_under_their_card_first_lines(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    _touch(downloads / "jimeng-2026-09-25-1001-p15-1_正面 A long two-storey.png", b"front")
    # the reference key quoted from the `参考:` line comes second — first key wins
    _touch(downloads / "ElevenLabs_image_gpt-image-2_p15-2_侧面 参考 p15-1_正面.png", b"side")
    _touch(downloads / "p15-3_背面 (1).png", b"back")   # not in the card → convention name

    result = _run(root, downloads)

    assert result.unmatched == [] and result.errors == [], (result.unmatched, result.errors)
    assert {m["kind"] for m in result.moved} == {"prop_object_view"}
    inn = props / INN
    assert (inn / "p15-1_正面.png").read_bytes() == b"front"
    assert (inn / "p15-2_侧面.png").read_bytes() == b"side"
    assert (inn / "p15-3_背面.png").read_bytes() == b"back"


def test_object_view_reroll_replaces_only_that_view(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    inn = props / INN
    _touch(inn / "p15-1_正面.png", b"old front")
    _touch(inn / "p15-2_侧面.png", b"side")
    _touch(downloads / "p15-1_正面.webp", b"new front")

    _run(root, downloads)

    assert not (inn / "p15-1_正面.png").exists()
    assert (inn / "p15-1_正面.webp").read_bytes() == b"new front"
    assert (inn / "p15-2_侧面.png").read_bytes() == b"side"


def test_glb_lands_in_mesh_named_by_the_prop_key(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    mesh = props / INN / "mesh"
    _touch(mesh / "p15.glb", b"old mesh")
    _touch(mesh / "p15_preview_000.png", b"preview")
    _touch(downloads / "rodin_p15_两层石木旅店_base_basic_pbr.glb", b"new mesh")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["prop_mesh"]
    assert (mesh / "p15.glb").read_bytes() == b"new mesh"
    assert (mesh / "p15_preview_000.png").read_bytes() == b"preview"   # rename pass stays out
    assert not list((props / INN).glob("*.glb"))


def test_story_prop_keeps_its_anchor_naming(tmp_path: Path) -> None:
    """No `asset.toml`: a `p3-2` state-variant anchor is `p3-2.png`, not `p3-2_侧面`;
    its mesh still goes by key into `mesh/`."""
    root, props, downloads = _drama(tmp_path)
    _touch(downloads / "ElevenLabs_image_gpt-image-2_p3-2_锤柄斧口 一把旧锤.png", b"variant")
    _touch(downloads / "tripo_p3-1_父亲的旧双手锤.glb", b"mesh")

    result = _run(root, downloads)

    hammer = props / HAMMER
    assert sorted(m["kind"] for m in result.moved) == ["prop", "prop_mesh"]
    assert (hammer / "p3-2.png").read_bytes() == b"variant"
    assert (hammer / "mesh" / "p3.glb").read_bytes() == b"mesh"


def test_glb_without_a_prop_key_is_never_imported(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    char = root / "ai_videos" / "d" / "2_世界观人设" / "characters" / "c1_裴知秋"
    _touch(char / "c1_裴知秋.md", b"card")
    for name in ("两层石木旅店_rodin.glb", "c1_裴知秋.glb", "p99_不存在.glb", "p15.gltf"):
        _touch(downloads / name)

    result = _run(root, downloads)

    assert result.moved == [] and len(result.unmatched) == 4
    assert not list(props.rglob("*.glb")) and not list(props.rglob("*.gltf"))
    assert not list(char.rglob("*.glb"))


def test_prop_number_owned_twice_routes_nowhere(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    _touch(props / "p15_另一个旅店" / "asset.toml")
    _touch(downloads / "p15-1_正面.png")
    _touch(downloads / "p15.glb")

    result = _run(root, downloads)

    assert not (props / INN / "p15-1_正面.png").exists()
    assert not (props / INN / "mesh").exists() and not (props / "p15_另一个旅店" / "mesh").exists()
    assert (downloads / "p15.glb").is_file()


def test_prop_key_beats_a_later_name_word_and_loses_to_an_earlier_scene_key(tmp_path: Path) -> None:
    root, props, downloads = _drama(tmp_path)
    world = root / "ai_videos" / "d" / "2_世界观人设"
    # the character's `霍格酋长` is the longest token hit, but it starts after the key
    _touch(world / "characters" / "c12_霍格酋长" / "c12_霍格酋长.md", b"card")
    _touch(props / "p16_营火" / "asset.toml")
    town = world / "scenes" / "eastern_kingdoms" / "elwynn_forest" / "bg4_闪金镇"
    _touch(town / "bg4_闪金镇.md", b"prompts")
    _touch(downloads / "p16-1_正面 霍格酋长的营火.png", b"fire")
    _touch(downloads / "bg4-1_镇心 参考 p15-1_正面.png", b"town view")

    _run(root, downloads)

    assert (props / "p16_营火" / "p16-1_正面.png").read_bytes() == b"fire"   # no card → convention
    assert (town / "bg4-1.png").read_bytes() == b"town view"
    assert not list((world / "characters" / "c12_霍格酋长").glob("*.png"))
    assert not (props / INN / "p15-1_正面.png").exists()


def test_shot_render_quoting_a_prop_key_stays_in_the_shot(tmp_path: Path) -> None:
    root, _props, downloads = _drama(tmp_path)
    shot = root / "ai_videos" / "d" / "5_6_分镜与prompt" / "episodes" / "ep01" / "shots" / "shot03"
    _touch(shot / "shot03.md", b"shot")
    _touch(downloads / "01集03镜视 参考 p15-1_正面.mp4", b"render")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["shot"]
    assert (shot / "renders" / "01集03镜视 参考 p15-1_正面.mp4").is_file()
