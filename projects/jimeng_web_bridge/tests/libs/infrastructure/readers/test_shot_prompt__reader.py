from __future__ import annotations

from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.shot_prompt__dao import ShotPromptDao
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import ShotParseError
from libs.infrastructure.readers.shot_prompt__reader import ShotPromptReader
from tests.libs.infrastructure.support import REAL_SHOTS_DIR, write_file

READER = ShotPromptReader(RepoSandbox(REAL_SHOTS_DIR))


def real(name: str) -> ShotPromptDao:
    return READER.parse_bytes((REAL_SHOTS_DIR / name).read_bytes(), name)


def synthetic(markdown: str) -> ShotPromptDao:
    return READER.parse_bytes(markdown.encode("utf-8"), "synthetic.md")


def shot(prompt: str, after: str = "") -> str:
    return f"# shot\n\n## 视频 prompt\n```text\n{prompt}\n```\n{after}"


def pairs(dao: ShotPromptDao) -> list[tuple[str, str]]:
    return [(item.name, item.label) for item in dao.references.items]


def test_hy3_shot02_golden_path() -> None:
    dao = real("hy3__shot02.md")
    assert pairs(dao) == [
        ("bg11-1", "场景参考图"),
        ("砌炉的老人", "Seedance 人物 entity"),
        ("p2-1", "随身装备锚点"),
        ("p3-1", "抹泥板锚点"),
    ]
    refs = dao.references
    assert (refs.line_count, refs.legacy, refs.unrecognized, refs.marker_count) == (1, (), (), 4)
    assert refs.integrity_ok and not refs.declares_none
    assert refs.items[1].raw_token == "砌炉的老人(Seedance 人物 entity)=>@"
    assert (dao.ratio, dao.ratio_raw, dao.duration_s, dao.duration_raw) == ("16:9", "16:9", 22, "22秒")
    assert len(dao.prompt) == 2314
    assert dao.prompt.startswith("shot02\n参考: `bg11-1(场景参考图)=>@`")
    assert dao.prompt.endswith("比例: 16:9\n时长: 22秒")
    assert "```" not in dao.prompt
    assert dao.negative_prompt is not None
    assert dao.negative_prompt.startswith("第二个人, 人群, 路人")
    assert dao.negative_prompt.endswith("垫脚石")
    assert "第二个人, 人群" not in dao.prompt


def test_crlf_cr_and_bom_normalise_to_the_lf_result() -> None:
    lf = real("hy3__shot02.md")
    raw = (REAL_SHOTS_DIR / "hy3__shot02.md").read_bytes()
    variants = [
        real("hy3__shot02.crlf.md"),
        READER.parse_bytes(b"\xef\xbb\xbf" + raw, "bom.md"),
        READER.parse_bytes(raw.replace(b"\n", b"\r"), "cr.md"),
    ]
    for variant in variants:
        assert variant.prompt == lf.prompt
        assert variant.negative_prompt == lf.negative_prompt
        assert variant.references == lf.references
        assert (variant.ratio, variant.duration_s) == (lf.ratio, lf.duration_s)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("xianjian__shot02.md", [("c1_江湖游侠", "角色参考图"), ("c10_市井大娘", "角色参考图"), ("s1_bg4_大堂_房梁室内", "场景参考图"), ("shot02_previz", "3D预演视频")]),
        ("xianjian__shot03.md", [("c1_江湖游侠", "角色参考图"), ("c10_市井大娘", "角色参考图"), ("p1_木剑", "道具参考图"), ("s1_bg4_大堂_房梁室内", "场景参考图"), ("shot03_previz", "3D预演视频")]),
        ("duikang__shot01.md", [("entropy_city_bg1_广场", "场景主体"), ("f80_ferrari", "物件主体"), ("previz_shot01", "previz灰模视频")]),
        ("duikang__shot09.md", [("driver", "人物主体"), ("entropy_city_bg2_主街", "场景主体")]),
        ("duikang__shot20.md", [("本镜首帧", "上一镜末帧"), ("cavallino_horse", "物件主体"), ("entropy_city_bg1_广场", "场景主体"), ("previz_shot20", "previz灰模视频")]),
        ("xingji__shot02.md", [("本镜首帧", "上一镜末帧"), ("bg1_菌毯岩脊", "场景参考图")]),
        ("xingji__shot10.md", [("c4_幽灵特工", "单位参考图"), ("p1_数据核心舱", "道具参考图"), ("bg2_前哨站残骸", "场景参考图")]),
        ("hy2__shot01.md", [("bg2-1", "场景参考图"), ("bg3-1", "场景参考图·第二、三段：步道纵深全景"), ("造家的人", "Seedance 人物 entity"), ("p1_砍刀", "砍刀锚点"), ("p2_随身装备", "随身装备锚点")]),
        ("hy2__shot02.md", [("bg4-1", "场景参考图"), ("bg5-1", "场景参考图·第四段：根盘与坑全景（N1 机位）"), ("造家的人", "Seedance 人物 entity"), ("p1_砍刀", "砍刀锚点"), ("p2_随身装备", "随身装备锚点")]),
    ],
)
def test_current_syntax_items_in_order(name: str, expected: list[tuple[str, str]]) -> None:
    dao = real(name)
    assert pairs(dao) == expected
    assert (dao.references.legacy, dao.references.unrecognized) == ((), ())
    assert dao.references.integrity_ok


@pytest.mark.parametrize(
    ("name", "ratio", "ratio_raw", "duration_s", "duration_raw"),
    [
        ("xianjian__shot02.md", "16:9", "16:9（项目 divergence·style_guide 画幅节）", 12, "12秒"),
        ("xianjian__shot14.md", "16:9", "16:9", 16, "16s"),
        ("wushen__ep03_shot05.md", "9:16", "9:16", 9, "9秒"),
        ("rexue__shot01.md", "9:16", "9:16", 2, "1.5s"),
        ("rexue__shot21.md", "9:16", "9:16", 2, "2.0s"),
        ("duikang__shot01.md", "2.35:1", "2.35:1", 12, "12秒"),
    ],
)
def test_lenient_ratio_and_duration(name: str, ratio: str, ratio_raw: str, duration_s: int, duration_raw: str) -> None:
    dao = real(name)
    assert (dao.ratio, dao.ratio_raw, dao.duration_s, dao.duration_raw) == (ratio, ratio_raw, duration_s, duration_raw)


@pytest.mark.parametrize(
    ("name", "starts_with"),
    [
        ("hy3__shot02.md", "第二个人, 人群"),
        ("xianjian__shot02.md", "人脸变形、五官漂移"),
        ("xianjian__shot14.md", "人脸变形、五官漂移"),
        ("xianjian__shot17.md", "人脸变形、五官漂移"),
        ("xingji__shot02.md", "可见人物, 士兵实体"),
        ("duikang__shot01.md", "字幕、文字、水印"),
    ],
)
def test_negative_prompt_heading_variants(name: str, starts_with: str) -> None:
    dao = real(name)
    assert dao.negative_prompt is not None
    assert dao.negative_prompt.startswith(starts_with)
    assert dao.negative_prompt not in dao.prompt


@pytest.mark.parametrize("name", ["xianjian__shot23.md", "wushen__ep01_shot03.md", "rexue__shot01.md"])
def test_no_negative_fence_yields_none(name: str) -> None:
    assert real(name).negative_prompt is None


def test_inline_negative_words_stay_in_prompt() -> None:
    assert "负面词:" in real("rexue__shot01.md").prompt
    assert "负面词" in real("wushen__ep01_shot03.md").prompt


def test_legacy_slot_number_without_paren() -> None:
    refs = real("rexue__shot01.md").references
    assert refs.items == ()
    assert [(f.kinds, f.token) for f in refs.legacy] == [(("slot_number", "no_paren"), "学校泳池_bg2_水面_俯拍=>@1")]
    assert not refs.integrity_ok


def test_legacy_slot_numbers_all_reported() -> None:
    refs = real("wushen__ep06_shot01.md").references
    assert [f.kind for f in refs.legacy] == ["slot_number"] * 5
    assert refs.legacy[2].token == "c12_围观武者乙声音=>@3"
    assert (refs.items, refs.marker_count) == ((), 5)


def test_legacy_arrow_without_at_is_never_an_empty_ok() -> None:
    refs = real("wushen__ep01_shot03.md").references
    assert refs.items == () and refs.marker_count == 0
    assert [f.kind for f in refs.legacy] == ["no_at"] * 6
    assert [f.token for f in refs.legacy][:2] == ["裴昭=>", "裴知秋=>"]
    assert real("wushen__ep03_shot05.md").references.legacy[-1].token == "本镜末帧=>"


@pytest.mark.parametrize(
    ("name", "tokens"),
    [
        ("xianjian__shot01.md", ["c1_江湖游侠=>@", "s7_bg3_云上_俯冲视角=>@"]),
        ("xianjian__shot17.md", ["s5_bg1_塔基_仰拍全塔=>@"]),
        ("xianjian__shot23.md", ["c1_江湖游侠=>@", "s6_bg1_寒潭_天光石台=>@"]),
    ],
)
def test_legacy_no_paren(name: str, tokens: list[str]) -> None:
    refs = real(name).references
    assert [(f.kinds, f.token) for f in refs.legacy] == [(("no_paren",), token) for token in tokens]
    assert refs.items == ()


def test_explicit_none_declaration() -> None:
    refs = real("rexue__shot21.md").references
    assert (refs.declares_none, refs.line_count, refs.items, refs.legacy, refs.unrecognized) == (True, 1, (), (), ())


@pytest.mark.parametrize(
    ("line", "expected_items", "expected_unrecognized"),
    [
        ("参考: 见上一镜", [], ("见上一镜",)),
        ("参考:", [], ("参考:",)),
        ("参考: `a(x)=>@` 还有 `b(y)=>@`", [("a", "x"), ("b", "y")], ("还有",)),
        ("参考: `a(x)=>@`，`b(y)=>@` 附注", [("a", "x"), ("b", "y")], ("附注",)),
        ("参考: `(x)=>@`", [], ("(x)=>@",)),
        ("参考: `a()=>@`", [], ("a()=>@",)),
        ("参考：`c1-1.png(脸的唯一标准)=>@`", [("c1-1.png", "脸的唯一标准")], ()),
    ],
)
def test_reference_line_fragments(
    line: str, expected_items: list[tuple[str, str]], expected_unrecognized: tuple[str, ...]
) -> None:
    dao = synthetic(shot(f"shot01\n{line}\n比例: 9:16\n时长: 5秒"))
    assert pairs(dao) == expected_items
    assert dao.references.unrecognized == expected_unrecognized


def test_zero_references_without_line_or_marker() -> None:
    refs = synthetic(shot("shot01\n情节: 他走开\n时长: 5秒")).references
    assert (refs.line_count, refs.items, refs.marker_count, refs.integrity_ok) == (0, (), 0, True)


def test_stray_marker_breaks_integrity() -> None:
    refs = synthetic(shot("shot01\n参考: `a(x)=>@`\n情节: 他看向 b=>@ 那边")).references
    assert (len(refs.items), refs.marker_count, refs.integrity_ok) == (1, 2, False)


@pytest.mark.parametrize(
    "ratio_line", ["`比例`: 9:16", "**比例**: 9:16", "- 比例: 9:16", "`比例: 9:16`", "比例：`9:16`"]
)
def test_field_key_forms(ratio_line: str) -> None:
    dao = synthetic(shot(f"shot01\n{ratio_line}\n- 时长: `7 s`"))
    assert (dao.ratio, dao.ratio_raw, dao.duration_s, dao.duration_raw) == ("9:16", "9:16", 7, "7 s")


def test_read_checks_type_and_size_before_loading(tmp_path: Path) -> None:
    write_file(tmp_path, "ai_videos/d/renders/bg1-1.png", b"\x89PNG")
    (tmp_path / "ai_videos" / "d" / "folder.md").mkdir(parents=True)
    write_file(tmp_path, "ai_videos/d/huge.md", b"#" * (2 * 1024 * 1024 + 1))
    reader = ShotPromptReader(RepoSandbox(tmp_path))
    for rel, reason in [
        ("ai_videos/d/renders/bg1-1.png", "unsupported_type"),
        ("ai_videos/d/folder.md", "not_a_file"),
        ("ai_videos/d/huge.md", "too_large"),
    ]:
        with pytest.raises(SandboxError) as caught:
            reader.read(rel)
        assert caught.value.reason == reason
        assert str(tmp_path) not in str(caught.value)


def test_missing_fields_are_none() -> None:
    dao = synthetic(shot("shot01\n情节: x"))
    assert (dao.ratio, dao.ratio_raw, dao.duration_s, dao.duration_raw) == (None, None, None, None)


@pytest.mark.parametrize(
    ("markdown", "code"),
    [
        ("# x\n## Shot context\n", "prompt_heading_missing"),
        ("## 视频 prompt\n没有围栏\n## 台词配音 prompt\n```text\nx\n```\n", "prompt_fence_missing"),
        ("## 视频 prompt\n```text\nshot01\n", "prompt_fence_unterminated"),
    ],
)
def test_structure_errors(markdown: str, code: str) -> None:
    with pytest.raises(ShotParseError) as caught:
        synthetic(markdown)
    assert caught.value.code == code


def test_non_utf8_is_structured_error() -> None:
    with pytest.raises(ShotParseError) as caught:
        READER.parse_bytes(b"## \xff\xfe", "bad.md")
    assert caught.value.code == "not_utf8"


def test_bare_fence_before_text_fence_is_skipped() -> None:
    assert synthetic("## 视频 prompt\n```\nnote\n```\n```text\nshot01\n```\n").prompt == "shot01"


@pytest.mark.parametrize(
    "after",
    [
        "\n> 备注\n```text\n不是负向\n```\n",
        "\n## 台词配音 prompt\n> **反向提示词**\n```text\nx\n```\n",
        "\n反向提示词 写在普通行里\n```text\nx\n```\n",
    ],
)
def test_fence_without_negative_marker_is_not_negative(after: str) -> None:
    assert synthetic(shot("shot01", after)).negative_prompt is None


def test_read_goes_through_sandbox(tmp_path: Path) -> None:
    rel = "ai_videos/d/shots/shot01/shot01.md"
    write_file(tmp_path, rel, shot("shot01\n参考: `bg1-1(场景参考图)=>@`\n比例: 9:16\n时长: 5秒"))
    reader = ShotPromptReader(RepoSandbox(tmp_path))
    dao = reader.read(rel)
    assert dao.source_rel == rel
    assert pairs(dao) == [("bg1-1", "场景参考图")]
    with pytest.raises(SandboxError):
        reader.read("ai_videos/../x.md")
