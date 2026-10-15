# -*- coding: utf-8 -*-
"""《圣光刚好够用》ep01 s2 修复补立的两件剧情物件卡（p477–p478，follow-up 031，2026-10-11）。

用法（仓库根目录）：
    python tools/gen_props_szzl_ep01c.py
    python tools/gen_bg_assets.py images ai_videos/shengji_zhilu/2_世界观人设/props/p477_红蜡封口的报到信 \
        ai_videos/shengji_zhilu/2_世界观人设/props/p478_父亲的字条

为什么补：ep01 s2 上一轮出片（2026-10-10 夜至 10-11 凌晨的 v8）里，报到信和父亲的字条在画面上是同一张纸——分镜让亚伦把信折起塞进衬衣前襟，
后面从前襟滑出来的又是一张折着的纸，观众分不清掉出来的是不是 s3 要递给维里的那封信（follow-up 030 根因报告 st12：
两件都放在「怀里」、外观一样，「是父亲的字」只在叙述里）。修复后的故事稿把两件分开：报到信红蜡封口、插在腰带里；
字条是撕下来的一角粗纸、揣在衬衣前襟里。两件原先都只有文字、没有参考图，Seedance 每镜自由发挥，又会画成同一张纸。
补成道具卡后，分镜 `props` 字段引用它们，编译器把锚点图放进每镜的参考行（follow-up 031；道具规则见
`.agents/skills/ai-videos-pipeline/resources/assets.md`「道具与装备」）。

两件按「一眼能分开」写成对比（形制都按故事定稿，不加剧情信息）：

| | p477 红蜡封口的报到信 | p478 父亲的字条 |
|---|---|---|
| 纸 | 米黄厚纸，挺括，四边齐整 | 灰黄粗纸，薄软，至少两边撕口毛边 |
| 大小 | 折好约 16 × 11 cm，几层叠着有厚度 | 巴掌大，约 10 × 7 cm，对折一次 |
| 封口 | 一枚鲜红圆形火漆印 | 没有封蜡，没有信封 |
| 字 | 朝外一面无字 | 里面三四行歪斜深褐手写字迹（看得出是手写，不可读） |
| 随身 | 插在腰带里，露出上半截和红蜡 | 贴身揣在衬衣前襟里 |

不复用旧卡：`p11_圣信` 是旧剧情的信（暗金火漆、三折、手撕毛边），`p13_封好的文件` 是麻绳横捆的深红火漆长条公文，
形制都不对；p477 的负向排除暗金火漆、毛边与绳捆，免得画回那两件。

卡模板、`asset.toml`、渲染串与负向基线与 ep01 的 `gen_props_szzl.py` **共用同一个 `card()` / `asset_toml()`**（rule 4i ①），
结构照 `gen_props_szzl_ep01b.py`：只出正面（手持 / 随身剧情物件只当镜头参考、不转 3D，lessons L15），每张卡追加
`## Shot prompt 外观` 一节——视频编译器把它原样写进每镜的「道具」行。两件都是纸、不许有可读字：`asset.toml` 标 `no_text`
（`gen_bg_assets` 不抓、不挂真实照片，照片常带字，lessons L14）；痕迹不写成「划痕 / 刮痕 / 墨点」（ep02 实测会画成符号）。
键由 `props_lib.allocate(…, "story")` 领，这里只引用、不手填。
"""
from __future__ import annotations

import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools import gen_props_szzl as base  # noqa: E402  —— 共用 Prop / Tri / card() / asset_toml()
from tools import gen_bg_assets as gba  # noqa: E402  —— asset.toml 的 views / no_text 键名与取值只在那里定义
from tools import props_lib  # noqa: E402

GENERATOR = "tools/gen_props_szzl_ep01c.py"
Prop, Tri = base.Prop, base.Tri
VIEWS = (gba.VIEW_NAMES[0],)
LOOK_HEAD = "## Shot prompt 外观"
# 禁字物件上这几个词会被画成像字的符号（ep02 第 1 次审图，见 gen_props_szzl_ep02.py 抬头）——痕迹写成磨圆、起毛、晕开的渍
GLYPH_PRONE = ("划痕", "刮痕", "墨点")

PROPS: tuple[Prop, ...] = (
    Prop(
        key="p477_红蜡封口的报到信", name="红蜡封口的报到信", build="i23d",
        why="纸张有界小件，手持 / 随身，只当镜头参考、不转 3D → 只出正面锚点图；朝外一面无字，字永不入画",
        size="折好约 16 × 11 cm，几层厚纸叠着、厚约半厘米；火漆印直径约 3 cm",
        ep=("ep01 s1 进谷（边走边低头看）· s2 冷开场开头（边走边看；筐歪出车栏时把信往腰带里一插）"
            "· s2 交手后（摸腰带，信还插在那儿）· s3 报到（从腰带里抽出来递给维里）"),
        subject=("一封用米黄色厚纸折成的长方形信，几层厚纸叠在一起、看得出厚度；四边是干净笔直的折边，四角方正，"
                 "平平整整，像一份正式文书；最外一层纸的封口是一道笔直的横向折边，横在信的正面、离上沿约三分之一，"
                 "封口正中压着一枚鲜红色的圆形火漆印，直径约三厘米，印面只有沿边一圈简单的花纹、中间平整；"
                 "纸面朝外的一面没有任何字"),
        material="米黄色厚纸，挺括、纤维细密，边缘是齐整的折边与裁边，不是手撕的毛边；火漆是鲜红色的凝固封蜡",
        wear="四个纸角**旧的**轻微磨圆；其余纸面干净平整，没有皱折与污渍",
        negative=("可读文字，字母，汉字，印刷体，纹章，字母印章，放射纹，星形，信封，三角形封舌，手撕毛边，"
                  "麻绳，细绳捆扎，丝带，现代纸张，白色打印纸，暗金火漆，金色火漆，暗红火漆，褐色火漆，发光"),
        lock="米黄厚纸方正长方信，鲜红圆形火漆封口，外面无字",
        variants="s2 交手后信皮湿了一角、红蜡上糊着泥（他用拇指抹了抹）——镜头层写，不进锚点图",
    ),
    Prop(
        key="p478_父亲的字条", name="父亲的字条", build="i23d",
        why="纸张有界小件，贴身随身，只当镜头参考、不转 3D → 只出正面锚点图；里面的手写字只画成认不出的字迹，永不可读",
        size="巴掌大，展开约 10 × 7 cm，对折一次后约 7 × 5 cm；纸薄",
        ep=("ep01 s2 冷开场（他弯腰用肩顶车尾时从衬衣前襟松着的系带口滑出、落进泥里 → 捡起来、轻声念 → 塞回衬衣里）"),
        subject=("巴掌大的一角灰黄色粗纸，是从账本或包装纸上撕下来的，至少两条边是参差不齐的撕口毛边；"
                 "纸对折过一次，中间一道发软的折痕；半摊开平放着，两半顺着折痕微微拱起，露出里面的一面："
                 "上面有三四行歪斜的深褐色手写字迹，墨色洇开、笔画模糊，看得出是手写，但一个字也认不出；"
                 "没有封蜡，没有信封，就是这么一小片纸"),
        material="灰黄色粗纸，又薄又软，纤维粗、纸面不平；字迹是深褐色的墨",
        wear="折痕处**旧的**发软起毛；一角有一块**旧的**汗渍，颜色发暗、边缘晕开",
        negative=("可读文字，清晰字母，单词，汉字，印刷体，印刷格线，表格，符号，封蜡，火漆，信封，整张信纸，方正齐边，"
                  "白色打印纸，硬卡纸，羊皮纸，丝带，细绳，现代纸张，现代便利贴，发光"),
        lock="巴掌大撕下的灰黄粗纸，两边毛边，对折一道软折痕，无封蜡",
        variants="s2 落进泥里、沾了泥和雨水；捡起后展开念、再折好塞回衬衣——镜头层写，不进锚点图",
    ),
)

TRI: dict[str, Tri] = {
    "p477": Tri(
        obj="封信", side_aim="信仍平放，正对它的短边端头",
        side=("几层米黄厚纸从端面看是一叠齐整的纸边，层层压实、边线笔直，看得出厚度；鲜红火漆印在顶面，"
              "从这个角度只见它圆饼的侧沿高出纸面一点。纸角轻微磨圆。朝外的一面没有任何字迹。"),
        back_aim="信仍平放，从对面看过去",
        back=("顶面仍是那块米黄厚纸，封口折边与鲜红火漆印转到画面下方、离镜头更近，左右与参考图对调；"
              "四边齐整、四角方正。没有任何字迹。"),
        size_m=(0.16, 0.11, 0.005),
        queries=("wax sealed letter red", "folded letter red wax seal", "historic sealed letter packet"),
        prompt_en=("A neat rectangular folded letter of thick cream paper with crisp straight edges and square corners, "
                   "several layers thick, a straight flap edge across the upper third sealed with one bright red round "
                   "wax seal about 3 cm wide with a simple ring border, blank outer side with no writing, isolated object"),
        brief=("形制要点：折好约 16 × 11 cm 的米黄厚纸长方信，四边齐整、四角方正、有厚度；正面上部一道笔直封口折边，"
               "正中一枚鲜红圆形火漆印（约 3 cm，沿边一圈简单花纹）；外面无字。与 p11 圣信（暗金火漆、毛边）、"
               "p478 字条（撕下的粗纸小条）区分。"),
    ),
    "p478": Tri(
        obj="张字条", side_aim="字条仍半摊开平放，正对它折痕的一端",
        side=("对折过的灰黄粗纸从折痕一端看是一个很浅的 V 形，两半顺着发软的折痕微微拱起；撕口毛边参差，纸薄而软。"
              "里面那几行深褐字迹从这个角度看不见。"),
        back_aim="字条仍半摊开平放，从对面看过去",
        back=("两半仍顺着折痕拱起，左右与参考图对调：撕口毛边转到另一侧，那一角旧汗渍转到画面远处；"
              "三四行深褐手写字迹倒着看，同样一个字也认不出。"),
        size_m=(0.1, 0.07, 0.01),
        queries=("torn paper scrap folded", "old torn note coarse paper", "handwritten scrap old paper"),
        prompt_en=("A palm-sized torn corner of thin coarse greyish-yellow paper with ragged torn edges on at least two "
                   "sides, folded once with a soft worn crease, lying half open to show three or four slanted lines of "
                   "blurred dark brown handwriting that cannot be read, an old darker sweat stain on one corner, "
                   "no wax seal, no envelope, isolated object"),
        brief=("形制要点：巴掌大（展开约 10 × 7 cm）从账本或包装纸撕下的一角灰黄粗纸，至少两边撕口毛边；对折一次、"
               "折痕发软起毛；里面三四行歪斜深褐手写字迹（看得出是手写、不可读）；一角旧汗渍；无封蜡、无信封。"
               "与 p477 红蜡方正厚信一眼分开。"),
    ),
}

LOOKS: dict[str, str] = {
    "p477": ("一封米黄厚纸折成的方正长方信，约 16 × 11 cm，四边齐整、几层纸叠着有厚度，像一份正式文书；"
             "正面上部一道笔直的封口折边，正中压一枚鲜红的圆形火漆印（约 3 cm）；朝外一面没有任何字。"
             "平时插在腰带里，露出上半截和那枚鲜红的火漆。"),
    "p478": ("巴掌大（约 10 × 7 cm）的一角灰黄粗纸，从账本或包装纸上撕下来的，至少两边是参差的撕口毛边，又薄又软；"
             "对折过一次，一道发软起毛的折痕；没有封蜡，没有信封；展开是三四行歪斜的深褐色手写字迹，看不清写的什么。"
             "平时对折着，贴身揣在衬衣前襟里。"),
}
# 外观段说明里举的随镜状态（写在分镜里、不进外观段）
STATES: dict[str, str] = {"p477": "信皮湿了一角、红蜡糊了泥", "p478": "落进泥里、沾了雨水、展开来念"}


def card(p: Prop) -> str:
    text = base.card(p).replace("`tools/gen_props_szzl.py`", f"`{GENERATOR}`", 1)
    text = text.replace("\n> 那会把质量上限锁死在方盒子水平。\n",
                        "\n> 那会把质量上限锁死在方盒子水平。\n> **本件只出正面**（asset.toml `views`）；侧 / 背块留作将来要转 3D 时用。\n", 1)
    rk = base._rk(p)
    return (text.rstrip("\n") + f"\n\n{LOOK_HEAD}\n\n> 视频编译器把这一段原样写进分镜 `props` 引用本件的每镜「道具」行（follow-up 231）。"
            f"只写画面看得见的形制与随身方式；随镜变化的状态（{STATES[rk]}）写在分镜里。\n\n"
            f"{base.FENCE}text\n{LOOKS[rk]}\n{base.FENCE}\n")


def asset_toml(p: Prop) -> str:
    return (base.asset_toml(p) + f"{gba.VIEWS_KEY} = {props_lib._fmt(list(VIEWS))}\n"
            f"{gba.NO_TEXT} = true\n")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    names = {r["key"]: (r["name_zh"], r.get("kind")) for r in props_lib.registry(base.ROOT)}
    for p in PROPS:
        key, name = p.key.split("_", 1)
        if names.get(key) != (name, "story"):
            raise SystemExit(f"{p.key} 没在 props/registry.toml 登记为剧情物件，或名字对不上：{names.get(key)}")
    if {base._rk(p) for p in PROPS} ^ set(TRI) or set(TRI) ^ set(LOOKS) or set(LOOKS) ^ set(STATES):
        raise SystemExit(f"PROPS / TRI / LOOKS / STATES 的键对不上：{sorted(TRI)} · {sorted(LOOKS)} · {sorted(STATES)}")
    clash = set(TRI) & set(base.TRI)
    if clash:
        raise SystemExit(f"与 ep01 的 TRI 撞键：{sorted(clash)}")
    base.TRI.update(TRI)
    for p in PROPS:
        assert len(p.lock) <= 30, f"{p.key} 锁定串 {len(p.lock)} 字 > 30"
        glyph = [w for w in GLYPH_PRONE if w in p.subject + p.material + p.wear]
        assert not glyph, f"{p.key} 禁字物件的 prompt 里有 {glyph}（会被画成符号）——写成磨圆 / 起毛 / 晕开的渍"
        body = card(p)
        front = body.split("# 三视图 prompt", 1)[1].split(base.FENCE + "text")[1].split(base.FENCE)[0]
        assert "状态变体" not in front and "**" not in front, f"{p.key} 正面 prompt 混进了状态变体 / markdown 粗体"
        d = os.path.join(base.ROOT, p.key)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, p.key + ".md"), "w", encoding="utf-8", newline="\n").write(body)
        io.open(os.path.join(d, "asset.toml"), "w", encoding="utf-8", newline="\n").write(asset_toml(p))
        print(f"  {p.key:18} 锁定串 {len(p.lock):>2} 字 · 正面 prompt {len(front.strip()):>4} 字")
    print(f"\n写出 {len(PROPS)} 张物件卡 → {base.ROOT}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
