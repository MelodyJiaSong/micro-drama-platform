from __future__ import annotations

from collections.abc import Callable

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from tests.libs.infrastructure.support import skip_or_fail

H = "ai_videos/huangye_shenghuo"
EXCLUDE: list[str] = ["_deleted", "_candidates", "renders", "frames", "_blender"]
HY3_BG11 = f"{H}/hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png"

pytestmark = pytest.mark.requires_real_repo


@pytest.fixture(scope="module")
def tree(real_sandbox: RepoSandbox) -> DramaTreeReader:
    return DramaTreeReader(real_sandbox)


def test_listing_nests_series_and_excludes_notes(tree: DramaTreeReader) -> None:
    nodes = {node.name: node for node in tree.list_dramas()}
    series = nodes["huangye_shenghuo"]
    assert series.node_type == "series"
    children = [child.name for child in series.children]
    assert {"hy1", "hy2", "hy3", "hy4"} <= set(children)
    assert "_series" not in children
    flat = {"wushen_juexing", "duikang_shangzeng", "rexue_gaoxiao", "xianjian_yi_mv", "xingji_yingjiu"}
    assert flat <= set(nodes)
    assert all(nodes[name].node_type == "drama" for name in flat)
    assert "notes" not in nodes
    assert not any(name.startswith("_") for name in nodes)


def test_hy3_shot02_resolves_to_hy3_files_only(
    tree: DramaTreeReader, real_sandbox: RepoSandbox, require_media: Callable[[str], None]
) -> None:
    expected = {
        "bg11-1": HY3_BG11,
        "p2-1": f"{H}/hy3/2_世界观人设/props/p2_随身装备/p2-1.png",
        "p3-1": f"{H}/hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3-1.png",
    }
    for rel in expected.values():
        require_media(rel)
    dao = ShotPromptReader(real_sandbox).read(f"{H}/hy3/5_6_分镜与prompt/shots/shot02/shot02.md")
    drama = tree.drama_root_of(dao.source_rel)
    assert drama == f"{H}/hy3"
    images = {
        item.name: tree.resolve_asset_file(drama, item.name, EXCLUDE)
        for item in dao.references.items
        if item.label != "Seedance 人物 entity"
    }
    assert {name: (result.status, result.path) for name, result in images.items()} == {
        name: ("found", path) for name, path in expected.items()
    }
    assert all(len(tree.sha256(path)) == 64 for path in expected.values())
    card = tree.find_character_card(drama, "砌炉的老人")
    assert (card.status, card.path) == ("found", f"{H}/hy3/2_世界观人设/characters/c1_砌炉的老人")


def test_same_named_files_in_sibling_episodes_are_not_ambiguity(
    tree: DramaTreeReader, real_sandbox: RepoSandbox, require_media: Callable[[str], None]
) -> None:
    require_media(HY3_BG11)
    siblings = [
        entry.rel
        for episode in ("hy1", "hy2", "hy4")
        for entry in tree.list_files(f"{H}/{episode}", EXCLUDE)
        if entry.stem == "bg11-1" and entry.ext == ".png"
    ]
    if not siblings:
        skip_or_fail("sibling bg11-1.png traps not present in this checkout")
    result = tree.resolve_asset_file(f"{H}/hy3", "bg11-1", EXCLUDE)
    assert (result.status, result.path) == ("found", HY3_BG11)


def test_routing_key_prefix_in_hy2(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    path = f"{H}/hy2/2_世界观人设/props/p3_树皮门与顶/p3-1_树皮门板锚点.png"
    require_media(path)
    result = tree.resolve_asset_file(f"{H}/hy2", "p3-1", EXCLUDE)
    assert (result.status, result.step, result.path) == ("found", "routing_key_prefix", path)


def test_subject_dir_main_image_in_hy1(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    path = f"{H}/hy1/2_世界观人设/props/p2_随身装备/p2_随身装备.png"
    require_media(path)
    result = tree.resolve_asset_file(f"{H}/hy1", "p2_随身装备", EXCLUDE)
    assert (result.status, result.path) == ("found", path)


def test_hy2_links_resolve_to_hy1(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    kit = f"{H}/hy1/2_世界观人设/props/p2_随身装备/p2_随身装备.png"
    face = f"{H}/hy1/2_世界观人设/characters/c1_造家的人/c1_造家的人.png"
    require_media(kit)
    require_media(face)
    kit_result = tree.resolve_asset_file(f"{H}/hy2", "p2_随身装备", EXCLUDE)
    assert (kit_result.path, kit_result.link_path) == (
        kit,
        f"{H}/hy2/2_世界观人设/props/p2_随身装备/p2_随身装备.png.link.json",
    )
    assert tree.resolve_asset_file(f"{H}/hy2", "c1_造家的人", EXCLUDE).path == face
    maker = next(card for card in tree.character_cards(f"{H}/hy2") if card.dir_name == "c1_造家的人")
    assert maker.linked_source_drama == f"{H}/hy1"


def test_video_only_asset_is_not_an_image(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    require_media(f"{H}/hy1/2_世界观人设/scenes/yulin/bg9_林冠光柱/bg9-1.mp4")
    assert tree.resolve_asset_file(f"{H}/hy1", "bg9-1", EXCLUDE).status == "not_found"


@pytest.mark.parametrize(
    ("drama", "stem", "count"),
    [("ai_videos/wushen_juexing", "shot10_lastframe", 3), ("ai_videos/xianjian_yi_mv", "views1", 10)],
)
def test_real_duplicate_stems_are_ambiguous(tree: DramaTreeReader, drama: str, stem: str, count: int) -> None:
    result = tree.resolve_asset_file(drama, stem, EXCLUDE)
    if result.status == "not_found":
        skip_or_fail(f"{drama} media not pulled ({stem})")
    assert (result.status, len(result.candidates)) == ("ambiguous", count)


def test_previz_alias_and_subdir(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    duikang = "ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot01"
    xianjian = "ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot02"
    require_media(f"{duikang}/shot01_previz.mp4")
    require_media(f"{xianjian}/previz/shot02_previz.mp4")
    alias = tree.resolve_shot_video(duikang, "previz_shot01", EXCLUDE)
    assert (alias.status, alias.step, alias.path) == ("found", "swapped_alias", f"{duikang}/shot01_previz.mp4")
    subdir = tree.resolve_shot_video(xianjian, "shot02_previz", EXCLUDE)
    assert (subdir.status, subdir.path) == ("found", f"{xianjian}/previz/shot02_previz.mp4")


def test_prev_shot_lastframe_real(tree: DramaTreeReader, require_media: Callable[[str], None]) -> None:
    xingji = "ai_videos/xingji_yingjiu/5_6_分镜与prompt/shots"
    missing = tree.resolve_prev_shot_lastframe(f"{xingji}/shot02", "本镜首帧")
    assert (missing.status, missing.looked_for) == ("not_found", f"{xingji}/shot01/shot01_lastframe.png")
    assert tree.resolve_prev_shot_lastframe(f"{xingji}/shot01", "本镜首帧").reason == "first_shot"
    wushen = "ai_videos/wushen_juexing/5_6_分镜与prompt/episodes/ep01/shots"
    require_media(f"{wushen}/shot05/shot05_lastframe.png")
    found = tree.resolve_prev_shot_lastframe(f"{wushen}/shot06", "本镜首帧")
    assert (found.status, found.path) == ("found", f"{wushen}/shot05/shot05_lastframe.png")


def test_entity_card_without_c_prefix(tree: DramaTreeReader) -> None:
    result = tree.find_character_card("ai_videos/duikang_shangzeng", "driver")
    assert (result.status, result.step, result.path) == (
        "found",
        "dir_name",
        "ai_videos/duikang_shangzeng/2_世界观人设/characters/driver",
    )
