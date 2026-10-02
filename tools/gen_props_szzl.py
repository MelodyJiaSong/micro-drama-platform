# -*- coding: utf-8 -*-
"""《圣光刚好够用》物件卡生成器 —— 第一批（北郡山谷 · ep01 实际入画的；2026-09-25 按剧集化后的新 ep01 重排）。

兵器 / 盾 / 甲胄不在这里：p3 旧双手锤、p9 盾与剑、p10 练习锤、p14 阔刃斧已迁入装备库（旧键 e1–e5，今天的层级码见 equipment/registry.toml 的 was）
（`2_世界观人设/equipment/`，生成器 `tools/gen_equipment.py`，follow-up 021）。

用法：python tools/gen_props_szzl.py

契约出处：`ai_video.md` rule 4b-A（路由键必须在可粘贴块首行）· rule 4d（object 走「图先行」五步）·
rule 4g §B（**四问决定用什么建**）· rule 4i ①（多份同构 prompt 走生成器，不手写 N 份）。

## rule 4g §B 四问（按顺序问，决定每个物件怎么建）

1. 有现成资产吗 → 有就**买 / 复用**（本项目：先查 sk2 的 27 张道具卡）
2. 直线 / 模块 / 精确尺寸 → **脚本建**（`build` 字段 = `script`）
3. 有机曲面 + 有界 + 只有图 → **image-to-3D**（`build` = `i23d`）
4. **环境 → 永不用 image-to-3D**（生成式给不出直角、统一地平面与重复开间节奏）

每张卡把这个判定写在明面上，**下游不必再问一遍**。

## 图先行（rule 4e ①，方向不能倒）

锚点图**纯文字自由生成、零参考图**；**绝不拿白模 / 灰模渲图当出图参考**——
那会把生成图的质量上限锁死在方盒子水平。此坑在 object 与 scene 上各踩过一次。
"""
from __future__ import annotations

import io
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools import props_lib  # noqa: E402

ROOT = "ai_videos/shengji_zhilu/2_世界观人设/props"
STYLE_GUIDE = "ai_videos/shengji_zhilu/2_世界观人设/style_guide.md"
FENCE = "`" * 3


def _fence_after(heading: str) -> str:
    """style_guide 里某个标题之后的第一个 ```text 围栏——渲染串与负向基线的唯一出处（rule 4i ①）。
    以前这里是两份手抄副本，style_guide 一改就静默漂。"""
    text = io.open(STYLE_GUIDE, encoding="utf-8").read()
    i = text.find(heading)
    if i < 0:
        raise SystemExit("style_guide.md 里找不到「%s」" % heading)
    a = text.index(FENCE + "text\n", i) + len(FENCE + "text\n")
    return "".join(text[a:text.index("\n" + FENCE, a)].split("\n"))


STYLE = _fence_after("### 全片共用摄影串")
NEG_BASE = _fence_after("## 5. 负向锁定")
NEG_OBJ = "人物，手，环境背景，地面，投影，多个物件同框，比例参照物，标尺"


@dataclass(frozen=True)
class Prop:
    key: str
    name: str
    build: str            # script | i23d | reuse
    why: str              # 四问的判定理由
    size: str
    ep: str
    subject: str
    material: str
    wear: str             # 痕迹——按 16.8 写成名词化冷状态，不写成「正在发生」
    negative: str
    lock: str             # 一句话锁定 ≤30 字
    reuse_from: str = ""
    variants: str = ""    # 状态变体——只进描述符表，不进锚点图 prompt（写进去模型就把裂盾 / 半块盾画成锚点）


PROPS: tuple[Prop, ...] = (
    Prop(
        key="p1_南墙隘口石门", name="南墙隘口石门", build="script",
        why="平直、模数化、尺寸要精确（它是 ep01 进谷与出谷的构图主体，门洞宽度决定人物剪影占比）→ **脚本建**",
        size="墙体高约 6 m、门洞净宽 2.6 m / 净高 3.4 m", ep="ep01 S02（进谷）· S27（出谷与回望）",
        subject=("一道横跨谷口的厚石墙，正中开一个拱形窄门；墙体由不规则大块灰石干砌，缝隙里塞小石片；"
                 "门洞两侧各立一根略粗的方形门柱，柱顶各压一块外挑的压顶石；门洞上方是半圆拱券，"
                 "拱石一块块呈放射状排列；墙顶做成平顶，外侧比内侧略高，形成一道浅浅的护墙"),
        material="灰白与青灰混杂的石灰岩，表面粗糙有凿痕；门轴处是锈色铁件",
        wear="石面有深浅不一的**旧**水渍与地衣斑块，颜色暗沉；门洞下缘的石头被长年踩踏磨出圆边",
        negative="城堡，吊桥，箭塔，雉堞，金属闸门，砖砌，水泥，现代门框",
        lock="谷口厚灰石墙中开拱形窄门，两侧方柱压顶石",
    ),
    Prop(
        key="p2_石拱桥", name="石拱桥", build="script",
        why="单拱、对称、尺寸由河宽决定 → **脚本建**。⚠ 它的位置是**推定**的（原文只写「过桥」未给位置）",
        size="全长约 16 m、桥面净宽 3.5 m、拱高约 2.8 m", ep="ep01 S18（过桥回望）",
        subject=("一座单拱石桥横跨小河；桥面微微拱起，两侧是齐腰高的实体石栏，栏顶压一排平整压顶石；"
                 "桥拱由楔形拱石砌成，拱脚沉在两岸的石砌桥台里；桥面铺不规则石板，中间被走出一条浅凹"),
        material="与墙体同源的灰白石灰岩；桥面石板颜色更深，因长年踩踏发亮",
        wear="拱腹靠近水面处有一圈**旧**的深色水痕与绿藻印；石栏外侧有几处缺角",
        negative="木桥，铁桥，多拱，廊桥，栏杆花纹雕刻，现代护栏",
        lock="单拱灰石桥，齐腰实体石栏，桥面中央踩出浅凹",
    ),
    Prop(
        key="p4_狗头人蜡烛与矿镐", name="狗头人蜡烛与矿镐", build="i23d",
        why="有机的融蜡形态 + 有界 → **image-to-3D**。它是矿洞里**唯一的光源**，形制必须锁死",
        size="蜡烛高约 12 cm；矿镐全长约 70 cm", ep="ep01 S06（营地）· S10–S13 / S16（回音山矿洞：洞里唯一的光源）",
        subject=("一支粗短的白色蜡烛与一把小号矿镐。蜡烛由多次滴蜡层叠而成、表面凹凸不平，"
                 "底部粘在一块弯折的铁片托上（那是插在破布帽顶的座）；矿镐一头尖、一头扁，"
                 "木柄比常人用的短一截，被磨得发亮"),
        material="蜡是暖白微黄、半透；铁片与镐头是暗灰锈铁；木柄是深褐",
        wear="蜡体侧面挂着**已经凝固**的蜡泪，一层压一层；镐头尖端磨钝、有细小卷刃",
        negative="精美烛台，细长白蜡，教堂蜡烛，现代工具，不锈钢，塑料柄",
        lock="层叠滴蜡的粗短白烛粘在弯铁片托上，配短柄小矿镐",
    ),
    Prop(
        key="p5_红色粗麻面罩", name="红色粗麻面罩", build="i23d",
        why="布料的有机褶皱 + 有界小件 → **image-to-3D**。它是 **L5a 伏笔的载体**，形制要经得起特写",
        size="展开约 50 × 22 cm", ep="ep01 S20（**第十二块的特写定格**）· S22–S25（加瑞克脸上）· S25（交差的面罩袋）",
        subject=("一块蒙下半脸用的长条粗麻布，两端各缝一根系带；布面是织得很松的平纹，能看见经纬；"
                 "中段因长期覆在口鼻处而略微塌陷成形"),
        material="暗血红色粗麻，**洗得发暗、不鲜艳**",
        wear=("边角磨破、露出几根断线；**内侧被汗浸出一圈深色的印子**——"
              "那是长期戴着干活的人才会留下的痕迹。**是陈旧的印子，不是湿的**"),
        negative="鲜红，丝绸，缎面，崭新，整齐，海盗头巾，忍者面罩，印花，图案",
        lock="暗血红粗麻长条面罩，边角磨破，内侧一圈旧汗印",
    ),
    Prop(
        key="p6_葡萄架与木栅", name="葡萄架与木栅", build="script",
        why="重复开间、直线、按模数排 → **脚本建**（rule 4g ②：生成构件，不生成建筑）",
        size="单开间 2.4 m，架高 2.0 m；木栅高 1.1 m", ep="ep01 S19–S21 葡萄园（bg18）",
        subject=("一排木架葡萄藤垄：每隔一个开间立一根方木柱，柱间拉两道横木，藤蔓缠在横木上；"
                 "垄边是一道矮木栅，由削尖的圆木桩与两道横条组成"),
        material="未上漆的浅褐木材，日晒后表面发灰；藤蔓是深褐木质茎",
        wear="木柱根部靠地一段颜色更深；横木上有藤蔓勒出的**旧**压痕",
        negative="金属棚架，水泥柱，现代大棚，塑料绑带，整齐修剪的观赏葡萄",
        lock="方木柱两道横木的葡萄藤垄，垄边削尖圆木矮栅",
    ),
    Prop(
        key="p7_修道院兵器架", name="修道院兵器架", build="script",
        why="直线木构、重复槽位 → **脚本建**", size="长 2.2 m / 高 1.6 m",
        ep="ep01 S09 / S15 / S26 武器大厅（萨缪尔修士那一间）",
        subject=("一排靠墙的木质兵器架：底座是一条带凹槽的厚木，上方一道横木开着一排等距的圆孔与卡槽，"
                 "剑与长戟斜插其中；架子两端各有一根立柱"),
        material="深褐硬木，榫卯接合，不见铁钉",
        wear="卡槽内缘被兵器反复插拔磨出**旧**的亮痕；底座落着一层薄灰",
        negative="金属货架，玻璃展柜，现代武器，霓虹，发光武器",
        lock="靠墙深褐木兵器架，横木开等距圆孔与卡槽",
    ),
    Prop(
        key="p8_商贩区摊台", name="商贩区摊台", build="script",
        why="直线、模块、四个商人一字排开可复制 → **脚本建**", size="单台 1.8 × 0.8 m / 高 0.9 m",
        ep="ep01 暂未入画（保留；新 ep01 没有修装备的戏）",
        subject=("一列简易木摊台：厚木板搭在两组交叉木腿上，台面后侧竖一块矮挡板；"
                 "台下堆着木箱与麻袋；其中一台旁立一个铁砧与淬火水槽"),
        material="浅褐粗木，台面因长期使用颜色更深；铁砧是暗灰熟铁",
        wear="台面有**旧**的刀痕与油渍印；木腿底端被泥水浸成深色",
        negative="现代摊位，遮阳伞，塑料布，金属货架，价签，招牌文字",
        lock="厚木板搭交叉木腿的摊台，后侧矮挡板，台下木箱麻袋",
    ),
    Prop(
        key="p11_圣信", name="圣信（封蜡信）", build="i23d",
        why="纸张的有机形态 + 有界小件 → **image-to-3D**（只作手中道具，字迹永不入画）",
        size="折好约 16 × 11 cm", ep="ep01 S07（治安官递出）· S09（萨缪尔双手接过、折好收进袖子）",
        subject=("一封折成三折的厚纸信，封口压着一枚暗金色火漆印，印面是一个简单的圆形放射纹；"
                 "纸面朝外的一面没有任何字迹——字写在折进去的内侧"),
        material="米黄厚纸，纤维粗，边缘手撕的毛边；火漆是暗金偏褐",
        wear="纸角有**旧**的轻微卷翘与折痕；火漆边缘有一道细裂",
        negative="可读文字，字母，汉字，印刷体，信封，现代纸张，白色打印纸，红色火漆，发光",
        lock="米黄厚纸三折信，暗金火漆圆印，外侧无字",
    ),
    Prop(
        key="p12_葡萄清单", name="米莉的葡萄清单", build="i23d",
        why="纸张有机形态 + 有界 → **image-to-3D**（字迹永不入画）",
        size="折好约 12 × 8 cm", ep="ep01 S21（米莉写、折、塞给亚伦）· S25（尼尔斯展开念）",
        subject=("一张折过好几道的粗纸，折痕发白；展开时纸面上只有几行很小、看不清的铅笔字迹，一角压着一枚葡萄汁的淡紫指印"),
        material="灰黄粗纸，薄而软；铅笔字迹是浅灰",
        wear="折痕处起毛、**旧**的；紫色指印是干透的旧印",
        negative="可读文字，清晰字母，汉字，印刷体，现代纸张，白色打印纸，彩色墨水",
        lock="灰黄粗纸折了好几道，角上一枚淡紫葡萄汁指印",
    ),
    Prop(
        key="p13_封好的文件", name="去闪金镇的封好的文件", build="i23d",
        why="有界小件 → **image-to-3D**（收件行只由后期字卡给出）",
        size="约 22 × 10 cm", ep="ep01 S25（治安官递出，亚伦别进腰带）· S27（杜克抽走、只看封皮、再塞回）",
        subject=("一份长条形的折叠公文，用一道细麻绳横捆，捆结处压一枚深红火漆印；封皮一面空白，看不出字"),
        material="浅褐厚纸，比信纸硬；麻绳是本色；火漆深红",
        wear="封皮边缘有**旧**的轻微磨损与一道折角",
        negative="可读文字，字母，汉字，印刷体，信封，现代文件袋，塑料，发光",
        lock="浅褐长条公文，细麻绳横捆，深红火漆封口",
    ),
)


@dataclass(frozen=True)
class Tri:
    """三视图（2026-09-25 起剧情物件与场景物件同一格式，`tools/gen_bg_assets.py` 出侧 / 背）+ asset.toml 字段。
    侧 / 背正文按正面图（`p{N}-1_正面.png`）实际长相写：资产坐标正面朝南，侧视机位在西、背视机位在北。"""
    obj: str                          # 开场句「与参考图完全是同一{obj}」
    side_aim: str
    side: str
    back_aim: str
    back: str
    size_m: tuple[float, float, float]  # [东西, 南北, 高]
    queries: tuple[str, str, str]     # Wikimedia Commons 英文检索词
    prompt_en: str
    brief: str
    single: str = ""                  # 名字读起来是几样东西时必填（gen_bg_assets MULTI）


SINGLE_STORY = "剧情物件：三视图按剧中成组出现的样子出；建 GLB 前按 rule 4h-K ① 拆成单物体"
TRI_CLOSE = ("纯中性灰无缝背景，无地面、无投影面、无环境元素；均匀柔和的散射光，物体下方没有投影，没有戏剧光；"
             "保持与参考图相同的轻微俯角，单主体居中、完整入画不裁切；画面里没有任何人物、手、文字、水印。")

TRI: dict[str, Tri] = {
    "p1": Tri(
        obj="道石门", side_aim="正对这道厚石墙左端的端面",
        side=("墙从这里看只剩一道厚墙的截面：约两米厚、六米高的竖直端面，同样是不规则大块灰石干砌、缝里塞着小石片，"
              "灰白与青灰石块混杂，灰绿地衣斑与深浅旧水渍的分布和参考图一致。墙顶外侧那道浅护墙比内侧高一截，"
              "端面顶上看得出这个高低差和两道护墙之间凹下去的浅槽。拱门洞被墙身挡住看不到，"
              "只在端面右缘露出门柱那块外挑压顶石的一小角。墙根一圈稍宽的基石。"),
        back_aim="正对厚石墙的另一面（谷内一侧）",
        back=("墙面同样是不规则大块灰石干砌，正中同一个半圆拱门洞，拱石一块块呈放射状排列；门洞两侧各一根方形门柱，"
              "柱顶压着外挑的压顶石。左右与参考图对调：参考图里靠左的门柱现在在右。门洞内侧立着旧木门框，"
              "框边几处锈色铁门轴。这一面墙顶是内侧、比外侧略矮，护墙边沿在墙顶后方露出一线。"
              "门洞下缘的石头同样被长年踩踏磨出圆边，石面有旧水渍与地衣斑块。"),
        size_m=(10, 2, 6),
        queries=("dry stone wall arched gateway", "medieval stone gate arch", "rubble masonry archway"),
        prompt_en=("A thick dry-laid grey limestone wall with a narrow round-arched gateway, square stone jambs "
                   "with projecting capstones, weathered lichen patches, isolated object"),
        brief=("形制要点：横跨谷口约 6 m 高的厚灰石干砌墙，正中半圆拱窄门（净宽 2.6 m），两侧方门柱压外挑压顶石，"
               "墙顶外高内低的浅护墙；旧木门框与锈铁门轴。ep01 进谷 / 出谷的构图主体。"),
    ),
    "p2": Tri(
        obj="座石拱桥", side_aim="正对桥头、顺着桥身方向看过去",
        side=("画面近处是桥头石砌桥台的端面与桥面入口，两侧齐腰高的实体石栏各以一块方形端柱收头；"
              "栏顶一排平整压顶石顺着桥面向远处升高、过了桥顶再落下，两道石栏在透视里向远处收拢。"
              "桥面铺不规则石板，中央那条被踩出的深色浅凹从脚下一直延伸到远端桥顶。"
              "桥拱在这个角度被桥台挡住，只在两侧边缘露出一点拱背外弧。"),
        back_aim="正对桥的另一侧立面，整座桥横在画面里",
        back=("单拱居中，楔形拱石一圈呈放射状排列，拱脚沉在两端的石砌桥台里；拱腹靠下的部位一圈旧的深色水痕与绿藻印。"
              "这一侧石栏外面同样有几处缺角，栏顶压顶石连成一道平缓的弧线；桥面在石栏后面微微拱起，只看得到栏顶。"
              "左右与参考图对调：参考图里近处的那一端桥头现在在画面右侧。"),
        size_m=(16, 4.5, 4.5),
        queries=("single arch stone footbridge", "medieval stone arch bridge", "packhorse bridge"),
        prompt_en=("A single-arch grey limestone footbridge with solid waist-high parapets and an irregular flagstone "
                   "deck worn into a shallow groove, isolated object"),
        brief="形制要点：单拱灰石桥，全长约 16 m、桥面净宽 3.5 m，齐腰实体石栏压顶石，桥面中央踩出浅凹；拱腹旧水痕绿藻印。",
    ),
    "p4": Tri(
        obj="组蜡烛与矿镐", side_aim="从左侧看过去",
        side=("粗短白烛离镜头最近、在画面左前：多层滴蜡叠出的凹凸烛身，侧面一道道已经凝固的蜡泪一层压一层挂到底，"
              "底部粘在那块带锈的方形弯铁片托上，铁片托一角折弯翘起；烛芯上一朵小火苗与参考图一致。"
              "蜡烛下面是那顶深褐色破布帽，隆起的帽顶与磨出毛边和破洞的帽檐从侧面看成一个低矮的布丘。"
              "短柄小矿镐斜搭在布帽右后方，镐头在更远处、扁头与尖头前后叠在一起，深褐木柄从帽边伸向画面右侧。"),
        back_aim="正对这组物件的背面",
        back=("左右与参考图对调：矿镐在画面左侧，蜡烛在画面右后方。矿镐短木柄深褐、被磨得发亮，"
              "暗灰锈铁镐头一头尖一头扁，尖头磨钝、带细小卷刃，从这面看尖头朝左上、扁头朝右。"
              "深褐破布帽背面同样粗布起毛、边缘破烂。蜡烛立在帽顶铁片托上，烛身背面同样挂满凝固的蜡泪，"
              "烛芯同一朵小火苗。"),
        size_m=(0.7, 0.4, 0.22),
        queries=("dripping candle stub", "old miner pick axe", "melted wax candle"),
        prompt_en=("A stubby dripping white candle stuck on a bent rusty iron plate atop a ragged dark cloth cap, with a "
                   "small short-handled mining pick lying beside it, isolated objects"),
        brief=("形制要点：层叠滴蜡的粗短白烛（约 12 cm）粘在弯铁片托上、托插在深褐破布帽顶；旁边一把短柄小矿镐（约 70 cm），"
               "一头尖一头扁。矿洞里唯一的光源。"),
        single=SINGLE_STORY,
    ),
    "p5": Tri(
        obj="块面罩", side_aim="正对面罩的一侧",
        side=("面罩从侧面看是一道弯弧，像一片包住下半脸的弧形布壳：外侧鼓出、中线鼻梁处最高，下缘收成一个钝尖，"
              "上沿略向里卷。靠镜头这一端的系带从布边缝口垂下，带头磨出毛须；另一端的系带从布壳后面露出一截。"
              "织得很松的平纹粗麻，经纬清晰，边角磨破、露出几根断线；暗血红色洗得发暗、不鲜艳。"),
        back_aim="正对面罩贴脸的里侧",
        back=("看到的是面罩凹进去的里面，像一个浅浅的布兜，中段被口鼻长年顶出的形状略微塌陷。"
              "里侧正中一圈深色的旧汗印，是陈旧干透的印子，不是湿的。两端系带从左右垂下，左右与参考图对调。"
              "麻布里侧颜色比外侧略深，布边同样磨破起毛。"),
        size_m=(0.5, 0.15, 0.22),
        queries=("burlap face mask", "hessian cloth mask", "coarse linen face covering"),
        prompt_en=("A dark blood-red coarse burlap half-face mask with frayed edges and tie strings on both ends, "
                   "faded and worn, isolated object"),
        brief="形制要点：约 50 × 22 cm 的暗血红粗麻长条面罩，两端系带，边角磨破，内侧一圈旧汗印。L5a 伏笔载体。",
    ),
    "p6": Tri(
        obj="排葡萄架", side_aim="正对这排葡萄架的一端",
        side=("最近的两根方木柱一左一右立在画面中，柱顶架着两道纵向长横木的端头，柱间一道矮横木；"
              "后面一对对方木柱依次排远、越来越小，成一条长廊。深褐枯藤缠满横木、从柱脚爬上来。"
              "架下中间一条木板铺的窄道伸向深处。画面右侧削尖圆木矮栅从近处沿架子向远处排去，"
              "近端也有一小段矮栅收口。木柱根部靠地一段颜色更深，横木上有藤蔓勒出的旧压痕。"),
        back_aim="正对葡萄架的背面长边，整排横在画面里",
        back=("一排方木柱等距排开，柱顶长横木、柱间横木，深褐枯藤缠绕其间。这一侧靠镜头没有矮栅，看过去是敞开的；"
              "削尖圆木矮栅在架子远侧，从柱间缝隙里露出一排尖头。左右与参考图对调：参考图左端那一小段矮栅现在在画面右端。"
              "木材未上漆、日晒发灰，柱脚一段颜色更深。"),
        size_m=(12, 3, 2),
        queries=("vineyard trellis wooden posts", "wooden grapevine pergola", "pointed stake picket fence"),
        prompt_en=("A row of weathered wooden grapevine trellis posts and rails with bare dark vines, edged by a low fence "
                   "of sharpened round stakes, isolated object"),
        brief="形制要点：单开间 2.4 m、架高 2.0 m 的方木柱横木葡萄藤垄，缠深褐枯藤；垄边 1.1 m 削尖圆木矮栅。bg18 葡萄园。",
        single=SINGLE_STORY,
    ),
    "p7": Tri(
        obj="座兵器架", side_aim="正对兵器架的左端",
        side=("看到的是一根厚立柱的侧面，立在带台阶的厚木底座脚上，柱前后各一块三角斜撑木；"
              "上下两道开孔横木的端头从立柱里穿出、露出榫头。兵器架很薄，前后不到半米。"
              "插在架上的剑与长戟从这个角度前后叠成一列，只见最近那把长戟的尖头和后面一排剑柄顶端层层高出架顶。"
              "深褐硬木、榫卯接合、不见铁钉，底座落着一层薄灰。"),
        back_aim="正对兵器架的背面",
        back=("同样的上下两道开孔横木，一排等距的圆孔与卡槽，剑与长戟从孔里斜插，剑柄护手与戟尖露在架顶上方；"
              "左右次序与参考图对调，长戟那一头现在在画面左侧。两端各一根立柱落在带台阶的厚木底座上；"
              "正面那根贴地的长底木从这面在架后、被下横木挡去大半。卡槽内缘有插拔磨出的旧亮痕。"),
        size_m=(2.2, 0.6, 1.6),
        queries=("medieval weapon rack", "wooden sword rack", "polearm rack armoury"),
        prompt_en=("A dark hardwood freestanding weapon rack with two drilled crossbeams holding swords and polearms, "
                   "isolated object"),
        brief="形制要点：长 2.2 m、高 1.6 m 的深褐硬木兵器架，上下两道横木开等距圆孔与卡槽，剑与长戟斜插，榫卯不见铁钉。",
    ),
    "p8": Tri(
        obj="座摊台", side_aim="正对摊台的左端",
        side=("交叉木腿在画面前成一个大大的 X，厚木台面的端头压在上面，台面后侧竖着的矮挡板从端面看是一道立起的木板；"
              "台下木箱与鼓鼓的麻袋从腿缝间露出。铁砧和淬火水槽在摊台远端右侧，被摊台挡住大半，"
              "只露出铁砧的尖角和方槽的一角。台面有旧刀痕与油渍印，木腿底端被泥水浸成深色。"),
        back_aim="正对摊台背面",
        back=("画面里先是矮挡板的背面：几块横钉的旧木板，挡住了台面；两组交叉木腿立在挡板下，台下的木箱与麻袋从背面也看得到。"
              "左右与参考图对调：铁砧和淬火水槽现在在画面左侧远处，从摊台下与挡板旁露出。"
              "浅褐粗木，铁砧是暗灰熟铁，水槽是暗灰铁皮。"),
        size_m=(2.6, 1.0, 1.3),
        queries=("rustic trestle table", "medieval market stall", "blacksmith anvil"),
        prompt_en=("A rustic trestle market table with a low backboard, crates and sacks beneath and an iron anvil and "
                   "quenching trough beside it, isolated object"),
        brief="形制要点：1.8 × 0.8 m、高 0.9 m 的厚木板交叉腿摊台，后侧矮挡板，台下木箱麻袋；旁立铁砧与淬火水槽。",
    ),
    "p11": Tri(
        obj="封信", side_aim="信仍平放，正对它的短边端头",
        side=("三折厚纸从端面看是一叠三层的纸边，最上一层的折边压在下面两层上，手撕的毛边一层叠一层；"
              "暗金火漆印在顶面，从这个角度只见它压扁的圆饼侧沿高出纸面一点，印边那道细裂在顶上。"
              "米黄厚纸纤维粗，纸角有轻微卷翘。纸面朝外的一面没有任何字迹。"),
        back_aim="信仍平放，从对面看过去",
        back=("顶面仍是那块米黄厚纸，火漆印转到画面右侧偏下，暗金偏褐、印面是简单的圆形放射纹；"
              "靠镜头这一边是三折叠出的圆滑折背，手撕毛边的开口边转到远侧。纸面有淡淡的旧折痕，没有任何字迹。"),
        size_m=(0.16, 0.11, 0.02),
        queries=("wax sealed letter", "folded letter wax seal", "historic sealed letter"),
        prompt_en=("A thick cream paper letter folded in three with deckle edges, sealed with a dull gold wax seal "
                   "with a radiating pattern, no writing visible, isolated object"),
        brief="形制要点：折好约 16 × 11 cm 的米黄厚纸三折信，暗金火漆圆形放射纹印（边缘一道细裂），外侧无字、毛边。",
    ),
    "p12": Tri(
        obj="张粗纸", side_aim="纸仍平摊，从左侧看过去",
        side=("同一张摊开的灰黄粗纸在透视里向画面右上方伸展；三乘三的发白折痕纵横交错，折痕处起毛、微微拱起，纸面不完全平整。"
              "几行很小的浅灰铅笔字迹模糊看不清。那枚干透的淡紫葡萄汁指印现在在画面右侧远端的纸角上。"
              "纸薄而软，边缘有几处毛糙的小缺口。"),
        back_aim="纸仍平摊，从对面看过去",
        back=("整张纸左右上下都与参考图对调：淡紫指印转到画面左上方远端的纸角。发白的三乘三折痕与起毛的折线同样清晰，"
              "纸面几行浅灰铅笔字迹模糊、倒着看也读不出。灰黄粗纸薄软，折痕处颜色更浅。"),
        size_m=(0.24, 0.36, 0.01),
        queries=("old folded paper sheet", "creased old paper", "pencil note old paper"),
        prompt_en=("A worn greyish-yellow sheet of coarse paper with whitened fold creases in a three-by-three grid, "
                   "faint illegible pencil marks and a pale purple fingerprint stain, isolated object"),
        brief="形制要点：灰黄粗纸（折好约 12 × 8 cm，展开三乘三折痕发白起毛），几行看不清的浅灰铅笔字，一角淡紫葡萄汁旧指印。",
    ),
    "p13": Tri(
        obj="份公文", side_aim="公文仍平放，正对它的短边端头",
        side=("浅褐厚纸从端面看是几层折叠压在一起的纸边，最上一层的斜折角翘起一点；细麻绳从顶面横绕下去、在端面看得见绳圈勒进纸边。"
              "深红火漆印在顶面正中，从这角度只见它圆饼的侧沿，麻绳结与两截绳头搭在火漆上。封皮空白、看不出字。"),
        back_aim="公文仍平放，从对面看过去",
        back=("顶面仍是浅褐长条封皮，深红火漆印与麻绳结在正中，麻绳绕过火漆横捆一圈；"
              "左右与参考图对调：参考图左端那处磨损翘起的纸角现在在画面右端，右端的斜折封舌转到左侧。"
              "封皮边缘有旧的轻微磨损与一道折角，没有任何字迹。"),
        size_m=(0.22, 0.1, 0.03),
        queries=("sealed document twine", "wax sealed parcel string", "folded document wax seal"),
        prompt_en=("A long folded tan document tied across with thin twine and sealed with dark red wax, blank cover, "
                   "isolated object"),
        brief="形制要点：约 22 × 10 cm 的浅褐长条折叠公文，细麻绳横捆，捆结处深红火漆封口，封皮空白。",
    ),
}


def _rk(p: Prop) -> str:
    return p.key.split("_", 1)[0]


def _tri_block(p: Prop, view: str, turn: str, aim: str, body: str) -> str:
    t = TRI[_rk(p)]
    return (f"{FENCE}text\n{_rk(p)}-{view}\n与参考图完全是同一{t.obj}，只把机位绕物体水平转到{turn}，{aim}；"
            f"形制、比例、材质、配色、破损位置一律不变。\n{body}\n{TRI_CLOSE}\n{FENCE}")


def asset_toml(p: Prop) -> str:
    t = TRI[_rk(p)]
    num = lambda v: str(int(v)) if float(v).is_integer() else str(v)  # noqa: E731
    lines = ["[asset]", f"key = {props_lib._fmt(_rk(p))}", f"name_zh = {props_lib._fmt(p.key.split('_', 1)[1])}",
             "size_m = [" + ", ".join(num(v) for v in t.size_m) + "]",
             f"queries = {props_lib._fmt(list(t.queries))}", f"prompt_en = {props_lib._fmt(t.prompt_en)}",
             "yaw_deg = 0", f"brief = {props_lib._fmt(t.brief)}"]
    if t.single:
        lines.append(f"single = {props_lib._fmt(t.single)}")
    return "\n".join(lines) + "\n"


def card(p: Prop) -> str:
    reuse = (f"\n> **可复用**：{p.reuse_from}——先看它能不能直接用，别重复出图（rule 4i ①）。\n"
             if p.reuse_from else "")
    t = TRI[_rk(p)]
    rk = _rk(p)
    return f"""# {p.name}

> **本文件由 `tools/gen_props_szzl.py` 生成，不要手改。** 改 prompt ＝ 改生成器重跑（rule 4i ①）。
> 路由键 `{rk}-1_正面` / `{rk}-2_侧面` / `{rk}-3_背面`（rule 4b-A：**键必须在可粘贴块的首行**，否则出的图永远落不进本目录）。
{reuse}
## 怎么建（rule 4g §B 四问的判定）

**{p.build}** —— {p.why}

## 锁定描述符

| # | 字段 | 值 |
|---|---|---|
| 1 | 尺寸 | {p.size} |
| 2 | 主体形制 | {p.subject} |
| 3 | 材质 | {p.material} |
| 4 | 使用痕迹 | {p.wear}{("。状态变体（不进锚点图）：" + p.variants) if p.variants else ""} |
| 5 | 出现集 | {p.ep} |
| 6 | **一句话锁定**（≤30 字 · byte-identical 进 shot 的 `道具:` 行） | `{p.lock}` |

## 负向

{FENCE}text
{NEG_BASE}，
{NEG_OBJ}，
{p.negative}
{FENCE}

---

# 三视图 prompt — {p.name}

> **正面纯文字自由生成、零参考图**（rule 4e ①）；侧 / 背只挂正面图作参考、钉死同一件东西只换机位
> （`python tools/gen_bg_assets.py images <本目录>`）。**绝不拿白模 / 灰模渲图当参考**——
> 那会把质量上限锁死在方盒子水平。

{FENCE}text
{rk}-1_正面

主体: {p.subject.replace("**", "")}

材质: {p.material.replace("**", "")}

使用痕迹: {p.wear.replace("**", "")}

视角: 四分之三俯视，单主体居中，完整入画不裁切

背景: 纯中性灰无缝背景，无地面、无投影面、无环境元素——本图只锁形制，不建场

渲染样式: {STYLE}

比例: 1:1
{FENCE}

{_tri_block(p, "2_侧面", "正左侧 90°", t.side_aim, t.side)}

{_tri_block(p, "3_背面", "正背面 180°", t.back_aim, t.back)}

## 负面词

{FENCE}text
{NEG_BASE}，
{NEG_OBJ}，
{p.negative}
{FENCE}

---

## 出图后

1. 三视图落盘为 `{rk}-1_正面.png` / `{rk}-2_侧面.png` / `{rk}-3_背面.png`；人眼过一遍形制对不对（对照 `0_research/map/refs/` 的 c60 原图与微型地下城图）。
2. `build = i23d` 的：用户在生成平台出 mesh → **必过闸门**
   `blender -b --factory-startup --python tools/whitemodel_normalize.py -- --src <glb> --spec {p.key}.toml --out {p.key}.blend`
3. `build = script` 的：把尺寸写进 `tools/build_northshire.py`，**由脚本确定性生成，不手改 blend**（rule 4h ④）。
"""


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(ROOT, exist_ok=True)
    # 场景物件并进 props 后（follow-up 013）全剧共用一套 p 编号，唯一出处是 props/registry.toml：
    # 本表的每个键都必须在那里登记为 story，否则会和场景物件撞号。新剧情物件先 `props_lib.py new … story` 领号。
    story = {r["key"] for r in props_lib.registry(ROOT) if r.get("kind") == "story"}
    if story:
        bad = [p.key for p in PROPS if p.key.split("_", 1)[0] not in story]
        if bad:
            raise SystemExit(f"这些键没在 props/registry.toml 登记为剧情物件（kind = \"story\"）：{bad}")
    missing = {_rk(p) for p in PROPS} ^ set(TRI)
    if missing:
        raise SystemExit(f"PROPS 与 TRI 的键对不上：{sorted(missing)}")
    by_build: dict[str, int] = {}
    for p in PROPS:
        d = os.path.join(ROOT, p.key)
        os.makedirs(d, exist_ok=True)
        body = card(p)
        assert len(p.lock) <= 30, f"{p.key} 锁定串 {len(p.lock)} 字 > 30"
        views = body.split("# 三视图 prompt", 1)[1].split("## 负面词")[0].split(FENCE + "text")[1:]
        assert len(views) == 3 and not any("状态变体" in v or "**" in v for v in views), \
            f"{p.key} 三视图 prompt 不是三块，或混进了状态变体 / markdown 粗体"
        io.open(os.path.join(d, p.key + ".md"), "w", encoding="utf-8", newline="\n").write(body)
        io.open(os.path.join(d, "asset.toml"), "w", encoding="utf-8", newline="\n").write(asset_toml(p))
        by_build[p.build] = by_build.get(p.build, 0) + 1
        print(f"  {p.key:22} {p.build:7} 锁定串 {len(p.lock):>2} 字")
    print(f"\n写出 {len(PROPS)} 张物件卡 → {ROOT}/")
    print("  按建法分：" + " · ".join(f"{k} {v}" for k, v in sorted(by_build.items())))
    print("  提醒：sk2 已有 27 张道具卡（炉石 / 钱袋 / 木桶 / 石井 / 苹果树 / 石凳 / 街灯…），")
    print("        建新卡前先查 `0_research/sk2_reuse.md`，能复用的不要重复出图。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
