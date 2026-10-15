# -*- coding: utf-8 -*-
"""《圣光刚好够用》ep01 补立的剧情物件卡：p475–p476（follow-up 231，2026-10-10）与 p476 的状态道具 p479（follow-up 044，2026-10-11）。

用法（仓库根目录）：
    python tools/gen_props_szzl_ep01b.py
    python tools/gen_bg_assets.py images ai_videos/shengji_zhilu/2_世界观人设/props/p475_葡萄手推车 \
        ai_videos/shengji_zhilu/2_世界观人设/props/p476_旧布裹锤长包
    # p475 的锚点图是侧面（车尾）：看图核对后把 p475-2_侧面.png 拷成 p475_葡萄手推车.png（编译器先取 {目录名}.png）
    # p479 的正面挂 p476 正面图作参考（gen_bg_assets 的正面只挂真实照片），单张出：送审稿 ＝ gen_bg_assets.Asset(<p479 目录>).send(0)，
    #   引擎循环同 gen_bg_assets.do_images，只把参考换成 p476-1_正面.png
    #   （2026-10-11 的出图脚本：.audit/adhoc_agents/2026-10-11/s2-regen/props_fix/p479_front.py）

为什么补：ep01 s2 第一轮出片（2026-10-10）推车每镜一个样——带篷大货车、敞开木架车、绳结挂到路边木栅上；
亚伦背上的长包时有时无。两件都只有文字描述、没有参考图，Seedance 每镜自由发挥。补成道具卡后，分镜 `props`
字段引用它们，编译器把锚点图放进每镜的参考行（follow-up 231）。

2026-10-11 s2 第一遍出片审片后（follow-up 044）：
- p475 锚点图换成车尾视角：s2 机位多在车后（南）朝北，正面图车头木支脚朝观者、车把朝后，成片照它把车摆反了。
  加出侧面（正对车斗后端、两根车把朝镜头）拷成锚点图，正面保留。
- p476 外观段只写长包本身、不写背法：成片里长包被画成木柄方头的铁锹，拿在手里时身上又多出一条斜挎带。图不重出。
- 新立 p479：p476 被狼咬破方块那头之后的样子（破口露一角生铁、少一道绳、沾泥），分镜按镜引用 p476 或 p479。

卡模板、`asset.toml`、渲染串与负向基线与 ep01 的 `gen_props_szzl.py` **共用同一个 `card()` / `asset_toml()`**（rule 4i ①），
沿用 ep02 生成器的做法：手持 / 随身剧情物件只当镜头参考、不转 3D，缺省只出正面（lessons L15）。
本文件额外给每张卡追加 `## Shot prompt 外观` 一节——视频编译器把它原样写进每镜的「道具」行。
键由 `props_lib.allocate(…, "story")` 领（p475–p476 2026-10-10，p479 2026-10-11），这里只引用、不手填。
"""
from __future__ import annotations

import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools import gen_props_szzl as base  # noqa: E402  —— 共用 Prop / Tri / card() / asset_toml()
from tools import gen_bg_assets as gba  # noqa: E402  —— asset.toml 的 views 键名与取值只在那里定义
from tools import props_lib  # noqa: E402

GENERATOR = "tools/gen_props_szzl_ep01b.py"
Prop, Tri = base.Prop, base.Tri
LOOK_HEAD = "## Shot prompt 外观"
# 出哪几面：缺省只出正面；p475 加出侧面（车尾），拷成锚点图
VIEWS: dict[str, tuple[str, ...]] = {"p475": gba.VIEW_NAMES[:2]}
ANCHOR_VIEW = {"p475": gba.VIEWS[1]}
# base 的侧面块写「转到正左侧 90°」；p475 正面图是车头斜对镜头，车尾在另一头，直接写机位
SIDE_TURN = {"p475": "车尾后方"}
# 状态道具的正面挂母件正面图作参考（同一条毯卷，只改破口、绳与泥）
FRONT_REF = {"p479": "p476_旧布裹锤长包"}

PROPS: tuple[Prop, ...] = (
    Prop(
        key="p475_葡萄手推车", name="葡萄手推车", build="i23d",
        why="有界单件刚体，只当镜头参考、不转 3D → 出正面与车尾（侧面）两张，车尾那张当锚点图",
        size="车斗长约 1.6 m、宽约 0.9 m；车轮直径约 0.9 m；连车把全长约 2.6 m；装满后筐顶离地约 1.5 m",
        ep="ep01 s2（冷开场：陷在车辙里、亚伦重新捆绳、狼来、推出车辙）· s9（尾声：修道院中庭卸葡萄）",
        subject=("一辆敞开的双轮木手推车，没有车篷、没有篷布、没有拱架：一只浅木车斗架在一根木车轴上，"
                 "车轴两头各一只辐条木轮；车斗后端伸出两根长长的木车把，供人站在车后双手推；"
                 "车斗前端低处一根木支脚，车停下时杵在地上；车斗四周是一拃高的矮木栏。"
                 "车斗里码着六只圆口藤编葡萄筐，下层四只、上层两只，每只筐里堆满成串的紫黑色葡萄，冒出筐沿；"
                 "一根旧麻绳从车栏一侧绕过上层两只筐、拉到另一侧车栏上系住"),
        material="风吹雨淋多年的灰褐旧木，铁轮箍与铁钉锈成深褐；藤筐是浅褐偏灰的旧藤条；葡萄紫黑带白霜；麻绳枯黄",
        wear="车把握手处被手磨得发亮；轮辋下半圈和车斗底沾着**旧的**干泥；藤筐口边几根藤条翘起、筐壁有紫色葡萄汁旧渍",
        negative=("车篷，篷布，帆布，拱形篷架，大货车，马车，四轮车，牲口，挽具，车夫，橡胶轮胎，金属车架，"
                  "木桶，麻袋，木箱，绿葡萄，现代器物，发光"),
        lock="敞开双轮木手推车，两根长车把，六只葡萄藤筐",
        variants="s2 st1 一只轮子陷在车辙泥里、车绳松了上层一筐往下滑；s2 st2 重新捆好、绳结勒紧——都是镜头层写，不进锚点图",
    ),
    Prop(
        key="p476_旧布裹锤长包", name="旧布裹锤长包", build="i23d",
        why="软布包裹的有界长件，只当镜头参考 → 只出正面锚点图；包里是父亲的旧双手锤（e5110），锤不露出来",
        size="长约 1.0 m；锤头一端粗约 20 cm，锤柄一端粗约 6 cm；背带长约 1.2 m",
        ep=("ep01 全集亚伦背在背上（s1 进谷、s2 冷开场、s3 报到、s4 武器厅、s5 狗头人营地解开、s9 尾声又裹回去）"),
        subject=("一条约一米长的长布包，用一块褪色的灰褐旧粗毛毯把一柄双手锤整个裹住：一头裹着方方的锤头，"
                 "鼓成一个方块；另一头裹着锤柄，细长；布包上用三道旧麻绳一圈圈捆紧、打着结；"
                 "两头之间系着一条宽的旧布背带，可以从右肩斜背到左腰。布裹得严，看不到任何铁和木头"),
        material="灰褐旧粗毛毯，织纹粗、起球；麻绳枯黄；背带是同色旧粗布",
        wear="毯边磨毛、有一处**旧的**补丁；方块那头布面被锤头棱角顶得发亮；下半截沾着干泥点",
        negative=("露出的锤头，露出的铁器，露出的木柄，刀，剑，枪，弓，箭袋，皮革剑鞘，背包，书包，帆布包，"
                  "现代背包，拉链，塑料扣，发光"),
        lock="灰褐旧毯裹成的一米长包，一头方块，三道麻绳",
        variants=("s2 狼咬破方块那头之后换用状态道具 p479；s4 st5 布滑开一角露出锤头、s5 st4 解开布抡锤"
                  "——镜头层写，不进锚点图"),
    ),
    Prop(
        key="p479_破口的旧布裹锤长包", name="破口的旧布裹锤长包", build="i23d",
        why=("p476 的状态道具：s2 交手时狼咬破方块那头，之后的长包破口露铁、少一道绳、沾泥，和 p476 一眼不同 → "
             "单立一件、只出正面锚点图（挂 p476 正面图作参考），分镜按镜引用 p476 或本件"),
        size="长约 1.0 m，毯卷粗细相近、略方那头略粗；豁口长约 10 cm，露出的铁棱约拇指大小；背带长约 1.2 m",
        ep="ep01 s2 交手中狼咬破方块那头之后（躺在泥里、又斜背回背上）；之后各场用不用由分镜定",
        subject=("一条约一米长的长布包横放着：一块褪色的灰褐旧粗毛毯卷成粗细相近的一卷，一头略鼓、略方，另一头略细；"
                 "略方那头的毯子豁开一道口子，撕破的毯角耷拉下来，豁口里露出拇指大小的一角生铁棱，"
                 "是一块旧铁的一个棱角：粗糙发黑，表面有锻打的坑点和锈斑，哑光、不反光；"
                 "除了这一角，毯卷里的东西都裹着，看不到木柄；略方那头原来那道麻绳没了，"
                 "只剩中段和细头两道旧麻绳一圈圈捆紧、打着结；一条同色的宽旧布背带连着两头，松松搭在一旁"),
        material="灰褐旧粗毛毯，织纹粗、起球；麻绳枯黄；背带是同色旧粗布；豁口里那一角是粗糙发黑的旧生铁",
        wear=("毯边磨毛、有一处**旧的**补丁；豁口边上的毯子纤维被扯得蓬乱；毯面、麻绳和背带沾着深褐色的湿泥，"
              "略方那头和下半截最多，泥还湿着、发亮"),
        negative=("铁锹，铲子，木柄，锤柄，完整露出的锤头，平整的黑色方块，屏幕，手机，平板电脑，光滑金属，镜面反光，"
                  "金属高光，崭新的铁，刀，剑，枪，弓，箭袋，皮革剑鞘，背包，书包，帆布包，拉链，塑料扣，发光"),
        lock="灰褐毯卷方头豁口露一角黑铁，剩两道麻绳，沾泥",
        variants="背在背上、拿在手里、躺在泥里——镜头层写，不进锚点图",
    ),
)

TRI: dict[str, Tri] = {
    "p475": Tri(
        obj="辆手推车", side_aim="正对车斗后端、两根车把朝镜头",
        side=("近处是两根伸向镜头的长木车把，车把之间是车斗后端的矮木栏；车斗两侧各露出一只辐条木轮的侧影；"
              "前端那根木支脚在车斗远端、被车斗挡住；车斗敞开、没有车篷，六只藤筐的筐口朝上，"
              "上层两只压在下层上面，那根麻绳横过上层两只筐。"),
        back_aim="正对车斗的另一条长边",
        back=("车把改朝画面左侧伸出，前端的木支脚在画面右侧杵地；靠机位这只辐条木轮完整入画，"
              "麻绳的结在这一侧车栏上。"),
        size_m=(2.6, 1.2, 1.5),
        queries=("wooden hand cart two wheels", "historic handcart wicker baskets", "grape harvest cart baskets"),
        prompt_en=("An open two-wheeled wooden handcart with no canvas cover, two long push handles at the rear, "
                   "a low slatted bed holding six round wicker baskets heaped with dark purple grapes in two tiers, "
                   "an old hemp rope tied over the top baskets, weathered grey-brown wood, isolated object"),
        brief="形制要点：敞开、无篷的双轮木手推车，后端两根长车把，车斗六只藤筐（下四上二）满装紫黑葡萄，一根麻绳横过上层。",
    ),
    "p476": Tri(
        obj="个长布包", side_aim="正对布包方块那一头",
        side="近处是布包裹着锤头的方块端面，三道麻绳一圈圈勒在布上，背带从两侧垂下；锤柄那一段在后面收细。",
        back_aim="正对布包的另一面",
        back="方块那头改在画面左侧，锤柄那头在右侧，背带搭在布包上，麻绳的结在这一面。",
        size_m=(1.0, 0.2, 0.2),
        queries=("bundle wrapped in old blanket tied rope", "long cloth bundle with shoulder strap", "wrapped tool in wool cloth"),
        prompt_en=("A long bundle about one metre long made of a faded grey-brown wool blanket wrapped tightly around a "
                   "two-handed hammer, one end square and bulky, the other end thin, bound with three hemp cords, "
                   "a wide old cloth shoulder strap, no metal or wood visible, isolated object"),
        brief="形制要点：灰褐旧毛毯裹成的一米长包，一头鼓成方块（锤头）、一头细长（锤柄），三道麻绳，宽布背带；不露铁和木。",
    ),
    "p479": Tri(
        obj="个长布包", side_aim="正对布包略方的那一头",
        side=("近处是略方那头的端面：毯子豁开的口子和耷拉下来的撕破毯角，豁口里那一角粗糙发黑、不反光的生铁棱；"
              "这一头没有麻绳，中段和细头两道麻绳在后面；背带从两侧垂下，毯面沾着湿泥。"),
        back_aim="正对布包的另一面",
        back=("略方那头改在画面左侧、细头在右侧；豁口在这一面被毯卷挡住大半，只露出耷拉的毯角；"
              "中段和细头两道麻绳的结在这一面，背带搭在布包上，毯面沾着湿泥。"),
        size_m=(1.0, 0.2, 0.2),
        queries=("torn wool blanket bundle", "muddy bundle tied with rope", "rusty forged iron corner"),
        prompt_en=("A long bundle about one metre long made of a faded grey-brown wool blanket rolled to an even thickness, "
                   "one end slightly squarer and torn open, a ripped flap hanging down, a thumb-sized corner of rough "
                   "blackened forged iron with pits and rust showing through the gash, matte, two hemp cords left in the "
                   "middle and at the thin end, a wide old cloth shoulder strap, smeared with wet mud, lying flat, "
                   "isolated object"),
        brief=("形制要点：p476 被狼咬破之后——同一条灰褐毯卷（粗细相近、一头略方），略方那头豁口、毯角耷拉，"
               "露出拇指大小一角粗糙发黑、不反光的生铁棱；那头的麻绳没了，剩中段与细头两道；沾湿泥。"),
    ),
}

_ROLL = "约一米长、粗细相近的一卷灰褐旧粗毛毯卷：一头略鼓、略方，另一头略细"
_STRAP = "连着一条同色的宽旧布背带"
LOOKS: dict[str, str] = {
    "p475": ("一辆敞开的双轮木手推车，没有车篷和篷布：灰褐旧木车斗架在一根车轴上，两只辐条木轮包锈铁箍，"
             "车斗后端伸出两根长木车把、人站在车后双手推，前端一根木支脚；车斗四周一拃高的矮木栏；"
             "车里码着六只圆口藤编筐（下层四只、上层两只），筐里堆满紫黑色葡萄；一根旧麻绳从车栏一侧绕过上层两只筐系到另一侧。"
             "整辆车只比推车的人略高，一个小个子女人推得动。"),
    "p476": f"{_ROLL}，两头都裹在毯子里，看不到木柄或铁；三道旧麻绳一圈圈捆紧；{_STRAP}。平时布裹得严，毯卷里的东西不露出来。",
    "p479": (f"{_ROLL}；略方那头的毯子豁开一道口子，撕破的毯角耷拉着，豁口里露出拇指大小的一角生铁棱："
             f"粗糙发黑、有锻打坑点和锈斑、不反光，不是平整的方块或屏幕；除了这一角，毯卷里的东西都裹着，看不到木柄；"
             f"略方那头的麻绳没了，只剩中段和细头两道旧麻绳一圈圈捆紧；{_STRAP}；毯面和麻绳沾着湿泥。"),
}
# 外观段说明：这一段只写什么，随镜的东西交给分镜
LOOK_NOTES: dict[str, str] = {
    "p475": "只写画面看得见的形制；随镜变化的状态（陷进泥里、绳松了）写在分镜里。",
    "p476": ("只写这条长包本身，不写背法：背在哪、拿在哪由各镜分镜写（2026-10-11 s2 第一遍出片："
             "外观写了锤头锤柄与斜背，长包被画成木柄方头的铁锹，拿在手里时身上又多出一条斜挎带）。"),
    "p479": "只写这条长包本身，不写背法：背在哪、拿在哪、躺在哪由各镜分镜写。它是 p476 被狼咬破方块那头之后的样子。",
}


def _views_note(p: Prop) -> str:
    rk = base._rk(p)
    if rk not in VIEWS:
        return "> **本件只出正面**（asset.toml `views`）；侧 / 背块留作将来要转 3D 时用。"
    shown = "与".join(VIEWS[rk])
    return (f"> **本件出{shown}**（asset.toml `views`），其余块留作将来要转 3D 时用。\n"
            f"> **锚点图 `{p.key}.png` 是 `{rk}-{ANCHOR_VIEW[rk]}.png`（车尾视角）的拷贝**，编译器先取它："
            f"s2 机位多在车后（南）朝北，正面图车头木支脚朝观者、车把朝后，2026-10-11 s2 第一遍出片照它把车摆反了。"
            f"侧面重出后要重新拷贝。")


def card(p: Prop) -> str:
    rk = base._rk(p)
    t = TRI[rk]
    text = base.card(p).replace("`tools/gen_props_szzl.py`", f"`{GENERATOR}`", 1)
    text = text.replace("\n> 那会把质量上限锁死在方盒子水平。\n",
                        f"\n> 那会把质量上限锁死在方盒子水平。\n{_views_note(p)}\n", 1)
    if rk in SIDE_TURN:
        text = text.replace(f"转到正左侧 90°，{t.side_aim}", f"转到{SIDE_TURN[rk]}，{t.side_aim}", 1)
    if rk in FRONT_REF:
        parent = FRONT_REF[rk]
        text = text.replace("**正面纯文字自由生成、零参考图**（rule 4e ①）",
                            f"**正面挂 `{parent}` 的正面图作参考**（状态道具：同一条毯卷，只改破口、麻绳与泥；"
                            f"gen_bg_assets 的正面只挂真实照片，这张单张出，命令见 `{GENERATOR}` 抬头）", 1)
        text = text.replace(f"{rk}-1_正面\n\n主体: ",
                            f"{rk}-1_正面\n\n参考: 第 1 张参考图是同一条长包完好时的样子：毯子的颜色、织纹、补丁、麻绳和背带都照它，"
                            f"只改下面写到的破口、麻绳与泥\n\n主体: ", 1)
    return (text.rstrip("\n") + f"\n\n{LOOK_HEAD}\n\n> 视频编译器把这一段原样写进分镜 `props` 引用本件的每镜「道具」行（follow-up 231）。"
            f"{LOOK_NOTES[rk]}\n\n{base.FENCE}text\n{LOOKS[rk]}\n{base.FENCE}\n")


def asset_toml(p: Prop) -> str:
    views = VIEWS.get(base._rk(p), gba.VIEW_NAMES[:1])
    return base.asset_toml(p) + f"{gba.VIEWS_KEY} = {props_lib._fmt(list(views))}\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    names = {r["key"]: (r["name_zh"], r.get("kind")) for r in props_lib.registry(base.ROOT)}
    for p in PROPS:
        key, name = p.key.split("_", 1)
        if names.get(key) != (name, "story"):
            raise SystemExit(f"{p.key} 没在 props/registry.toml 登记为剧情物件，或名字对不上：{names.get(key)}")
    keys = {base._rk(p) for p in PROPS}
    if keys ^ set(TRI) or keys ^ set(LOOKS) or keys ^ set(LOOK_NOTES):
        raise SystemExit(f"PROPS / TRI / LOOKS / LOOK_NOTES 的键对不上：{sorted(TRI)} · {sorted(LOOKS)} · {sorted(LOOK_NOTES)}")
    if set(VIEWS) ^ set(ANCHOR_VIEW) or not set(VIEWS) | set(SIDE_TURN) | set(FRONT_REF) <= keys:
        raise SystemExit("VIEWS / ANCHOR_VIEW / SIDE_TURN / FRONT_REF 里有对不上的键")
    clash = set(TRI) & set(base.TRI)
    if clash:
        raise SystemExit(f"与 ep01 的 TRI 撞键：{sorted(clash)}")
    base.TRI.update(TRI)
    for p in PROPS:
        assert len(p.lock) <= 30, f"{p.key} 锁定串 {len(p.lock)} 字 > 30"
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
