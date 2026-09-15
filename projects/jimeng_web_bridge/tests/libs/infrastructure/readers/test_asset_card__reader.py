from __future__ import annotations

import re
from pathlib import Path

import pytest

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.asset_card__dao import AssetCardDao
from libs.infrastructure.readers.asset_card__reader import AssetCardReader
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.errors.sandbox__error import SandboxError
from tests.libs.infrastructure.support import REAL_CARDS_DIR, write_file

HY = "ai_videos/huangye_shenghuo"
CARD_SOURCES: dict[str, str] = {
    "hy3__c1_砌炉的老人.md": f"{HY}/hy3/2_世界观人设/characters/c1_砌炉的老人/c1_砌炉的老人.md",
    "hy3__p3_抹泥板与黏土壁炉.md": f"{HY}/hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3_抹泥板与黏土壁炉.md",
    "hy3__bg11_崖脚洼地.md": f"{HY}/hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11_崖脚洼地.md",
    "hy2__c1_造家的人.md": f"{HY}/hy2/2_世界观人设/characters/c1_造家的人/c1_造家的人.md",
    "wushen__bg6_空场_无碑.md": "ai_videos/wushen_juexing/2_世界观人设/scenes/镇演武场/bg6_空场_无碑/bg6_空场_无碑.md",
    "xianjian__p1_木剑.md": "ai_videos/xianjian_yi_mv/2_世界观人设/props/p1_木剑/p1_木剑.md",
}
READER = AssetCardReader(RepoSandbox(REAL_CARDS_DIR))
_KEYED_TEXT_FENCE_RE = re.compile(r"^```text\n(?:bg|c|p)\d+-\d+(?!\d)", re.MULTILINE)


def card(name: str) -> AssetCardDao:
    return READER.parse_bytes((REAL_CARDS_DIR / name).read_bytes(), CARD_SOURCES[name])


def test_prop_card_two_blocks_and_bare_fences_ignored() -> None:
    dao = card("hy3__p3_抹泥板与黏土壁炉.md")
    assert (dao.card_dir_name, dao.subject_kind, dao.folder_key) == ("p3_抹泥板与黏土壁炉", "props", "p3")
    assert [block.key for block in dao.blocks] == ["p3-1", "p3-2"]
    first = dao.blocks[0]
    assert first.first_line == "p3-1_抹泥板锚点"
    assert first.body.startswith("p3-1_抹泥板锚点\n")
    assert first.heading == "Seedream 参考图 prompt — 抹泥板"
    assert "负面词:" in first.fields and "时长:" not in first.fields
    assert first.references.line_count == 0
    assert not any(block.body.startswith("木柄旧抹泥板") for block in dao.blocks)


def test_character_card_image_and_turntable_blocks() -> None:
    dao = card("hy3__c1_砌炉的老人.md")
    portrait, turntable = dao.blocks
    assert (portrait.key, turntable.key) == ("c1-1", "c1-2")
    assert "turntable" in turntable.first_line and "turntable" not in portrait.first_line
    assert turntable.heading is not None and turntable.heading.startswith("turntable 说明")
    assert "参考:" in turntable.fields and "参考:" not in portrait.fields
    assert [(item.name, item.label) for item in turntable.references.items] == [("c1-1.png", "脸的唯一标准")]
    assert (turntable.ratio, turntable.duration_s) == (None, None)
    assert not any(block.body.startswith("旧靛蓝粗布") for block in dao.blocks)


def test_scene_card_skips_world_descriptor_and_negative_list() -> None:
    dao = card("hy3__bg11_崖脚洼地.md")
    assert (dao.subject_kind, dao.folder_key) == ("scenes", "bg11")
    assert [block.key for block in dao.blocks] == ["bg11-1"]
    block = dao.blocks[0]
    assert block.heading is not None and block.heading.startswith("视图 1")
    assert [(item.name, item.label) for item in block.references.items] == [("bg1_草崖原始/bg1-1.png", "世界锚点")]


@pytest.mark.parametrize(
    ("name", "folder_key"),
    [("hy2__c1_造家的人.md", "c1"), ("wushen__bg6_空场_无碑.md", None), ("xianjian__p1_木剑.md", "p1")],
)
def test_cards_without_routing_key_blocks(name: str, folder_key: str | None) -> None:
    dao = card(name)
    assert dao.blocks == ()
    assert dao.folder_key == folder_key


def test_only_text_fences_whose_first_line_is_a_key() -> None:
    markdown = (
        "# p3\n```\np3-9_bare\n```\n```text\n负面词清单\np3-1_x\n```\n## A\n"
        "```text\np2-1_其他主体\n时长: 4.5s\n比例: 9:16\n```\n```text\np3-12x\n```\n"
    )
    dao = READER.parse_bytes(markdown.encode("utf-8"), "ai_videos/d/props/p3_x/p3_x.md")
    assert [(b.key, b.heading, b.duration_s, b.ratio) for b in dao.blocks] == [
        ("p2-1", "A", 5, "9:16"),
        ("p3-12", "A", None, None),
    ]
    assert dao.folder_key == "p3"


def test_read_rejects_non_markdown_before_loading(tmp_path: Path) -> None:
    write_file(tmp_path, "ai_videos/d/props/p1_x/c1-2.mp4", b"\x00" * 16)
    with pytest.raises(SandboxError) as caught:
        AssetCardReader(RepoSandbox(tmp_path)).read("ai_videos/d/props/p1_x/c1-2.mp4")
    assert caught.value.reason == "unsupported_type"


@pytest.mark.requires_real_repo
def test_real_card_sweep(real_repo_root: Path, real_sandbox: RepoSandbox) -> None:
    tree = DramaTreeReader(real_sandbox)
    reader = AssetCardReader(real_sandbox)
    cards = blocks = 0
    for drama in drama_ref.drama_dirs(real_repo_root):
        drama_rel = real_sandbox.rel(drama)
        assert drama_rel is not None
        for rel in tree.asset_card_paths(drama_rel):
            dao = reader.read(rel)
            text = (real_repo_root / rel).read_bytes().decode("utf-8").removeprefix("﻿").replace("\r\n", "\n")
            assert len(dao.blocks) == len(_KEYED_TEXT_FENCE_RE.findall(text)), rel
            cards += 1
            blocks += len(dao.blocks)
    assert cards > 0
    print(f"card sweep: {cards} cards, {blocks} routing-key blocks")
