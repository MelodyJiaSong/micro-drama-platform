"""Downloads land by their scene routing key under the nested layout (follow-up 173).

`scenes/{大陆}/{区}/bg{N}_{主体}/` subjects and their `bg{N}-{M}_…/` view folders.
The key is the LEFTMOST one in the name — generators inline the `参考:` line,
which quotes other keys after it. Objects are props (follow-up 174,
`test_downloads_import_prop_keys.py`); the zone keeps only `_plan/`.
"""
from __future__ import annotations

from pathlib import Path

from libs.common import series_shared
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    zone = root / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "eastern_kingdoms" / "elwynn_forest"
    _touch(zone / "elwynn_forest.md", b"zone card")
    _touch(zone / "_plan" / "plan.toml", b"[meta]")
    for subject in ("bg4_闪金镇", "bg1_北郡山谷", "bg172_艾尔文森林全境"):
        _touch(zone / subject / f"{subject}.md", b"prompts")
    _touch(zone / "bg1_北郡山谷" / "bg1-1_谷心_北望修道院" / "bg1-1_谷心_北望修道院.md", b"view prompt")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, zone, downloads


def _run(root: Path, downloads: Path):
    return _importer(root, downloads).import_drama("ai_videos/d")


def test_subject_view_lands_in_its_own_view_folder(tmp_path: Path) -> None:
    """The view card says: 导入按它归位本 folder 并重命名 `{view dir}.png`."""
    root, zone, downloads = _drama(tmp_path)
    _touch(downloads / "jimeng-2026-09-25-2002-bg1-1_谷心_北望修道院 参考_ `bg1_北郡山谷 全局建场底图.png", b"v")
    _touch(downloads / "bg4-2_镇心_十字路口.png", b"no view folder")

    result = _run(root, downloads)

    assert result.unmatched == [], result.unmatched
    view = zone / "bg1_北郡山谷" / "bg1-1_谷心_北望修道院"
    assert (view / "bg1-1_谷心_北望修道院.png").read_bytes() == b"v"
    assert (view / "bg1-1_谷心_北望修道院.md").read_bytes() == b"view prompt"
    assert (zone / "bg4_闪金镇" / "bg4-2.png").read_bytes() == b"no view folder"   # existing contract


def test_subject_anchor_lands_as_the_subject_folder_name(tmp_path: Path) -> None:
    root, zone, downloads = _drama(tmp_path)
    _touch(downloads / "即梦AI_bg4_闪金镇 参考_ `bg1_北郡山谷 世界锚点(图)=_.png", b"anchor")
    _touch(downloads / "bg172_艾尔文森.png", b"truncated")          # the generator cut the name short
    _touch(downloads / "bg4_朝北_主位.png", b"legacy plate id")      # `bg4_` alone names nothing

    result = _run(root, downloads)

    assert (zone / "bg4_闪金镇" / "bg4_闪金镇.png").read_bytes() == b"anchor"
    assert (zone / "bg172_艾尔文森林全境" / "bg172_艾尔文森林全境.png").read_bytes() == b"truncated"
    assert [u["from"].rsplit("/", 1)[-1] for u in result.unmatched] == ["bg4_朝北_主位.png"]


def test_retired_zone_asset_key_routes_nowhere(tmp_path: Path) -> None:
    """`bg{Z}-a{NN}` is gone (follow-up 174): it is not read as scene `bg{Z}`."""
    root, zone, downloads = _drama(tmp_path)
    for name in ("bg172-a01-1_正面.png", "bg172-a01.glb"):
        _touch(downloads / name)

    result = _run(root, downloads)

    assert result.moved == [] and len(result.unmatched) == 2
    assert not list((zone / "bg172_艾尔文森林全境").glob("*.png"))


def test_rename_pass_leaves_tool_folders_alone(tmp_path: Path) -> None:
    """`_blender/`, `planning/`, `ref/`, `mesh/` hold tool-contract names; the
    folder-name rename pass used to collapse them (`_blender/_blender1.png`)."""
    root, zone, downloads = _drama(tmp_path)
    town = zone / "bg4_闪金镇"
    prop = root / "ai_videos" / "d" / "2_世界观人设" / "props" / "p15_两层石木旅店"
    kept = [
        town / "_blender" / "check_plan.png",
        town / "_blender" / "check_bg4-c1.png",
        town / "planning" / "bg4_floorplan.png",
        town / "ref" / "bg4_闪金镇_map_crop.png",
        prop / "ref" / "r1.jpg",
        prop / "mesh" / "p15_preview_090.png",
        *(root / "ai_videos" / "d" / "2_世界观人设" / "characters" / "c2_Duke" / "views" / f"c2_Duke_{r}.png"
          for r in ("front", "side", "back")),
    ]
    for f in kept:
        _touch(f)
    _touch(downloads / "bg4_闪金镇.png")

    _run(root, downloads)

    assert [f for f in kept if not f.is_file()] == []


def test_assets_link_folder_is_neither_subject_nor_destination(tmp_path: Path) -> None:
    root, zone, downloads = _drama(tmp_path)
    block = zone / "bg4_闪金镇" / "assets" / "b01_两层旅店（正门朝西）"
    _touch(block / "p15_两层石木旅店.md.link.json", b'{"target": "x"}')
    _touch(downloads / "bg4-1_镇心.png")

    subjects = {p.name for p in series_shared.scene_subject_dirs(root / "ai_videos" / "d")}
    result = _run(root, downloads)

    assert subjects == {"bg4_闪金镇", "bg1_北郡山谷", "bg172_艾尔文森林全境"}
    assert (zone / "bg4_闪金镇" / "bg4-1.png").is_file()
    assert sorted(p.name for p in block.iterdir()) == ["p15_两层石木旅店.md.link.json"]
    assert [m["kind"] for m in result.moved] == ["scene_subject"]


def test_scene_key_beats_a_name_word_that_comes_after_it(tmp_path: Path) -> None:
    """Found on the real shengji_zhilu tree: character `c18_加瑞克` is a word of
    `bg19_加瑞克的小屋`, prop `p2_石拱桥` of `bg1-4_溪岸_石拱桥`. The scene key comes
    first, so it is the routing key; a key-first character file stays put."""
    root, zone, downloads = _drama(tmp_path)
    world = root / "ai_videos" / "d" / "2_世界观人设"
    _touch(zone / "bg19_加瑞克的小屋" / "bg19_加瑞克的小屋.md", b"prompts")
    _touch(world / "characters" / "c18_加瑞克" / "c18_加瑞克.md", b"card")
    _touch(world / "props" / "p2_石拱桥" / "p2_石拱桥.md", b"card")
    _touch(zone / "bg1_北郡山谷" / "bg1-4_溪岸_石拱桥" / "bg1-4_溪岸_石拱桥.md", b"view prompt")
    _touch(downloads / "jimeng-1-bg19_加瑞克的小屋 参考_ `bg1_北郡山谷.png", b"cabin")
    _touch(downloads / "bg1-4_溪岸_石拱桥.png", b"bridge view")
    _touch(downloads / "c18-1_加瑞克正面 参考 bg19_加瑞克的小屋.png", b"character")

    _run(root, downloads)

    assert (zone / "bg19_加瑞克的小屋" / "bg19_加瑞克的小屋.png").read_bytes() == b"cabin"
    assert (zone / "bg1_北郡山谷" / "bg1-4_溪岸_石拱桥" / "bg1-4_溪岸_石拱桥.png").read_bytes() == b"bridge view"
    assert (world / "characters" / "c18_加瑞克" / "c18-1.png").read_bytes() == b"character"
    assert not any(p.suffix == ".png" for p in (world / "props" / "p2_石拱桥").iterdir())


def test_shot_render_quoting_a_scene_key_stays_in_the_shot(tmp_path: Path) -> None:
    root, zone, downloads = _drama(tmp_path)
    shot = root / "ai_videos" / "d" / "5_6_分镜与prompt" / "episodes" / "ep01" / "shots" / "shot03"
    _touch(shot / "shot03.md", b"shot")
    _touch(downloads / "01集03镜视 参考 bg4_闪金镇 全局.mp4", b"render")

    result = _run(root, downloads)

    assert [m["kind"] for m in result.moved] == ["shot"]
    assert (shot / "renders" / "01集03镜视 参考 bg4_闪金镇 全局.mp4").is_file()


def test_glb_never_lands_in_a_scene(tmp_path: Path) -> None:
    """A GLB holds one object (2026-09-25) and every object is a prop: a scene
    key or a scene-name token routes no model file."""
    root, zone, downloads = _drama(tmp_path)
    flat_scene = root / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "jishi_changjie"
    _touch(flat_scene / "jishi_changjie.md", b"scene")
    for name in ("bg4_闪金镇.glb", "bg1-1_谷心_北望修道院.glb", "jishi_changjie_rodin.glb"):
        _touch(downloads / name)

    result = _run(root, downloads)

    assert result.moved == []
    assert len(result.unmatched) == 3
    assert not list(zone.rglob("*.glb")) and not list(flat_scene.rglob("*.glb"))


def test_blend_in_downloads_is_never_picked_up(tmp_path: Path) -> None:
    root, _zone, downloads = _drama(tmp_path)
    _touch(downloads / "bg4.blend", b"BLENDER")

    result = _run(root, downloads)

    assert (result.moved, result.unmatched) == ([], [])
    assert (downloads / "bg4.blend").is_file()
