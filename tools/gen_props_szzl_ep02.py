# -*- coding: utf-8 -*-
"""《圣光刚好够用》ep02 剧情物件卡生成器（p465–p473，2026-09-30）。

用法（仓库根目录）：
    python tools/gen_props_szzl_ep02.py

卡模板、`asset.toml`、渲染串与负向基线与 ep01 的 `gen_props_szzl.py` **共用同一个 `card()` / `asset_toml()`**（rule 4i ①）；
本文件只装 ep02 这九件的内容层，`asset.toml` 只在共用那份之后加 `views` / `no_text` 两行（键名与取值读 `gen_bg_assets`）。**不改 ep01 生成器**，也不重写 p1–p13。
键由 `props_lib.allocate(…, "story")` 领（2026-09-30），这里只引用、不手填。

## 复用（不另立卡）

| 剧本里的东西 | 复用 | 理由 |
|---|---|---|
| S01–S03 杜克交给杜汉的信 | `p13_封好的文件` | 就是 ep01 S25 治安官递出的那份公文 |
| S30 / S37 屋角翻倒的货车 | `p349_双轮木板车` | 卡里写明兼作翻倒 / 缺轮板车，已有 GLB；艾尔文与西部荒野同一种农家板车。翻倒靠 bg178 的 plate 与平面图块表达（blocks 只有 yaw，没有翻滚） |

`p45` / `p74` / `p96` / `p159` / `p365` / `p413` 这几只木箱都约 1 m、钉死盖，装不了砂、撒不出来、狗头人也搬不动 → 另立 p473。

## 只出正面（用户 2026-09-30 裁定，lessons L15）

手持剧情物件只出正面当镜头参考；侧 / 背只给要转 3D 的出（rule 4e「派生视图按镜需要才出」）。九件都不转 3D
（p472 / p473 是 build = script，脚本建也不要侧背图）→ `VIEWS` 只有正面。TRI 的侧 / 背正文留作将来要转 3D 时用，
那时先按正面图实际长相改 TRI 再出（rule 4d-A「锚点过验收才派生」）。

## 第 1 次出图审图后（2026-09-30，props-review：8 / 9 不通过）

- 禁字物件（纸 / 铜牌 / 戒指）上的「划痕 / 墨点」会画成符号（‡、+✕、八角星）→ 痕迹一律写成物理破损（划破口、凹坑、晕开），
  prompt 里不许出现 `GLYPH_PRONE`，负面词共用 `NO_GLYPH_NEG`（main() 里查）。
- 禁字物件挂的真实照片把手稿、信、纪念牌、书封上的字带进了图 → asset.toml 标 `no_text`，`gen_bg_assets` 不抓不挂照片（lessons L14）。
- 侧 / 背多半没转机位（与正面相关 ≥ 0.90）→ 侧面开头用 `side()` 写死「看不见什么」，背面用 `back()` 写死「掉转了头，不是照镜子」。
- p467 的形制句与 `m9_Princess` 卡「项圈:」句逐句对齐（main() 里查）。
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools import gen_props_szzl as base  # noqa: E402  —— 共用 Prop / Tri / card() / asset_toml()
from tools import gen_bg_assets as gba  # noqa: E402  —— asset.toml 的 no_text / views 键名与取值只在那里定义
from tools import props_lib  # noqa: E402

GENERATOR = "tools/gen_props_szzl_ep02.py"
Prop, Tri = base.Prop, base.Tri
PAPER = "纸张有机形态 + 有界小件 → **image-to-3D**（字写在里面，永不入画；展开时只拍纸背，G8）"
NO_GLYPH_NEG = "交叉笔画，符号状刻痕，星形，印刷圆点"
# 禁字物件（纸 / 铜牌 / 戒指内圈刻字）：不许有字，痕迹也不许画成像字的笔画；asset.toml 标 no_text（不抓不挂照片）
NO_TEXT_KEYS = ("p465", "p467", "p468", "p469", "p470")
VIEWS = (gba.VIEW_NAMES[0],)   # 九件都只出正面（见抬头「只出正面」）
GLYPH_PRONE = ("划痕", "刮痕", "墨点")               # 这几个词在禁字物件上会被画成符号——写成划破口 / 擦伤 / 墨渍
PAPER_NEG = "可读文字，字母，汉字，印刷体，透过纸背的字迹，" + NO_GLYPH_NEG
M9 = os.path.join(os.path.dirname(base.ROOT), "characters", "m9_Princess", "m9_Princess.md")
BACK_TURN = ("看到的是参考图里看不到的那一面：参考图里离镜头最近的部分现在在画面最远处，左右也对调——"
             "像把参考图掉转了头，不是照镜子。")


def side(edge: str, hidden: str, rest: str) -> str:
    return f"这一张只看得见它的{edge}；参考图里看得见的{hidden}，这里一个都看不见。{rest}"


def back(rest: str) -> str:
    return BACK_TURN + rest

PROPS: tuple[Prop, ...] = (
    Prop(
        key="p465_采金日程表", name="采金日程表（卷纸）", build="i23d", why=PAPER,
        size="展开约 30 × 22 cm；卷起长 22 cm、粗约 4 cm（只卷两圈多，中间空心）",
        ep=("ep02 S15（卷着别在豺狼人腰带上 → 掉在矿车轨道上 → 亚伦捡起）· S16（亚伦就着火把展开念，纸背朝镜头）"
            "· S18（杜汉一把拿过、念最后一行，纸背朝镜头）· S19（杜汉拍在木板上）"),
        subject=("一张偏黄厚纸横着松松卷起的纸卷，整张纸只绕了两圈多，纸卷又短又松、一眼看得出是同一张纸卷起来的，两端都能看见中间一个占满端口的空心大洞，没有任何散出来的单页，中段用一根细皮绳绕两圈、打一个活结；"
                 "卷筒两端露出两三层卷曲的纸边；朝外的一面是纸背，一片空白，看不到任何字迹"),
        material="偏黄的厚纸，纤维粗、有点发硬；皮绳是深褐色软皮",
        wear=("外层纸面一块**旧的**深色油渍和几点干泥；最外一层纸上三道平行的短划破口，口子边起毛翘起、露出下层纸色；"
              "两端纸边卷曲起毛；纸面除此之外干净，没有任何铅笔线、墨线或笔画"),
        negative=PAPER_NEG + "，羊皮卷轴，木轴，卷轴挂绳，火漆，蜡封，丝带，地图，现代纸张，白色打印纸，整卷包装纸，铅笔线，发光",
        lock="偏黄厚纸松卷，细皮绳绕两圈，外层油渍与三道划破口",
        variants="S16 / S18 展开：纸摊平、四角往回卷，只拍纸背（一片空白、透不出字）；锚点只出卷起的样子",
    ),
    Prop(
        key="p466_波尼斯的项链", name="波尼斯的项链", build="i23d",
        why="细链 + 小坠，有界小件 → **image-to-3D**（链子是软的，mesh 只锁坠子；出片靠图）。原典物品无外观，形制按 `c26` 卡「旧细链、拇指大椭圆小坠」",
        size="链长约 45 cm；坠子约 2.5 × 1.8 cm",
        ep="ep02 S16（挂在金牙脖子上 → 被盾撞得甩出去、落地弹一下 → 杜克捡起、举着）· S17（波尼斯接过、攥在胸口，此后戴回她脖子上）",
        subject=("一条细细的旧银链，坠一枚拇指大的椭圆小坠：一圈薄银框包着一块光面的暗红色圆润石头，"
                 "框边一圈细细的绳纹；链子细得像一根线，平摊在台面上绕成一个大圈，长度约是坠子的十八倍；"
                 "链尾是一只手弯的银丝小钩，钩进另一端的小圆环"),
        material="银链与银框都氧化得发暗，只在凸起处磨出一点亮色；石头深暗红、半透、表面光滑",
        wear="链节缝里嵌着**旧的**黑色污垢；坠子背面一块平平的薄银底板、不鼓，被长年贴着皮肤磨得发亮，没有任何刻字",
        negative=("金项链，粗链，侧身链，手链，短链，龙虾扣，弹簧扣，现代首饰扣，珍珠，钻石，心形吊坠，吊坠盒，十字架，挂锁，"
                  "宝石切面闪光，崭新锃亮，现代首饰，可读文字，刻字，发光"),
        lock="氧化发暗的细银链，坠拇指大椭圆银框暗红石",
    ),
    Prop(
        key="p467_公主的黄铜项圈", name="公主的黄铜项圈", build="i23d",
        why="环形有界刚体 → **image-to-3D**。原典物品描述里那行字不入画：正面小圆铜牌光素无字。外观须与 `m9_Princess` 的项圈后缀逐字对得上",
        size="内径约 38 cm；铜带三指宽（约 5 cm）、厚约 3 mm",
        ep=("ep02 S30（套在公主脖子上，远景）· S31（杜克一把抓住 → 舌扣崩开、整只留在他手里 → 塞进挎包）"
            "· S45（从挎包掏出放上桌，斯通菲尔德妈妈拎起来看）"),
        subject=("一只三指宽的实心黄铜片项圈，一整条弯成圈的黄铜板，铜面光滑无孔，平放成一个大圆环；"
                 "上下两道边沿各镶一排圆头铆钉，两排一模一样、绕满整圈；"
                 "正中只铆一块指甲盖大的光素小圆铜牌，一只黄铜舌扣扣合，舌扣在圆环上与铜牌正相对的另一头"),
        material="黄铜，铜色暗金偏褐；圆铆钉颜色更深",
        wear=("铜带内侧被长年磨得发亮、外侧暗沉；凹缝里一点青绿旧锈，积着**旧的**干泥；"
              "外侧铜面几处磕出的小凹坑和一片片磨亮的擦伤，边缘模糊"),
        negative=("狗项圈，皮项圈，尖刺项圈，铃铛，挂锁，锁链，王冠，崭新锃亮，镀金，只有一排铆钉，镂空孔，"
                  "可读文字，字母，刻字，数字，纹章，发光，" + NO_GLYPH_NEG),
        lock="三指宽的旧黄铜项圈，两排圆铆钉，舌扣扣合",
        variants=("S31 镜尾与 S45：舌扣崩开——舌片弯折翘起，项圈从扣处张开一道口子、合不拢；"
                  "锚点只出扣好的样子，S45 要挂图时由锚点派生一张状态图、另立主体（rule 4d-A3）"),
    ),
    Prop(
        key="p468_收货人的戒指", name="收货人的戒指", build="i23d",
        why="有界小件 → **image-to-3D**（内圈刻字永不入画：S43 只拍杜汉的眼睛与戒指侧面）。外观对齐 `c31` 卡「宽面暗黄铜色旧戒指」",
        size="外径约 2.3 cm；戒圈宽约 1 cm（一指节宽）",
        ep="ep02 S30（收货人右手无名指上，阳光里一闪）· S43（杜汉撸下来，眯眼对着光读内圈）",
        subject="一枚宽面的旧戒指：戒圈是一条一指节宽的平带，外面平整、没有戒面、没有宝石，沿两边各一道细凹线绕一周，边沿微微倒圆",
        material="暗黄铜色的旧金属，表面一层柔和的暗光，凸起的边沿磨出亮色",
        wear="外面磨出一层细密的**旧**毛面，几处小磕坑；一侧边沿磨得比另一侧薄",
        negative=("宝石戒指，钻戒，印章戒指，戒面纹章，骷髅戒指，镂空花纹，崭新锃亮，戒指盒，可读文字，字母，刻字，数字，发光，魔法光效，"
                  + NO_GLYPH_NEG),
        lock="一指节宽的暗黄铜旧平带戒，素面两道细凹线",
    ),
    Prop(
        key="p469_梅贝尔的情书", name="梅贝尔的情书", build="i23d", why=PAPER,
        size="折好约 12 × 9 cm（对折再对折，对齐 `c27` 卡「折了两折的信」）",
        ep="ep02 S09（梅贝尔隔着窗台递给杜克）· S12（杜克交给汤米·乔，他解开丝带、展开念一句——纸背朝镜头）",
        subject=("一张淡米白信纸对折再对折成的扁平小长方块：顶面是一整片纸、没有中缝，一边是圆滑的折脊，"
                 "对边露出四层错开的纸边；外面用一根褪色的淡紫细丝带横绕一圈、打一个小活结；朝外的一面空白"),
        material="薄而软的淡米白信纸，比农家粗纸细滑，折处微微鼓起、不挺括；丝带是一根洗褪了色的淡紫窄丝带，软塌、边缘微微起毛",
        wear="一只纸角被手指反复折过、起了软毛边；纸面一滴**旧**墨渍，晕开成不规则的一小团，边缘渗进纸纤维；纸面除此之外干净，没有任何笔画",
        negative=(PAPER_NEG + "，信封，火漆，蜡封，心形，花朵图案，彩色信纸，现代纸张，白色打印纸，"
                  "贺卡，礼品包装，对开门折法，中缝，硬卡纸，机缝缎带，发光"),
        lock="淡米白信纸对折两次，褪色淡紫细丝带横绕打结",
        variants="S12 展开：丝带解开、纸摊平，只拍纸背；锚点只出折好系好的样子",
    ),
    Prop(
        key="p470_老奶奶的便条", name="老奶奶写给匹斯特的便条", build="i23d", why=PAPER,
        size="折好约 7 × 7 cm、厚约半厘米",
        ep="ep02 S12（汤米·乔从屋里跑出来塞给亚伦）· S23（亚伦递给匹斯特，他拆开举到一臂远读——纸背朝镜头）",
        subject=("就是一张从浅褐色厚包装纸上撕下的纸，自己对折再对折成的扁平小方块，里面没包东西，只有四层纸、薄得像一枚铜币，平贴在台面上；"
                 "四边是撕口毛边或折边，没有包装盒式的三角折角；用一根白棉线十字捆住、在正中打一个结；朝外的一面空白"),
        material="浅褐色厚包装纸，纤维粗；白棉线",
        wear="纸面一圈淡褐色的**旧**茶渍圆印；一角蹭着一层薄薄的干面粉白印，擦进了纸纹里",
        negative=(PAPER_NEG + "，信封，火漆，蜡封，丝带，白色打印纸，现代便利贴，"
                  "礼品包裹，纸包，三角折角，鼓起的包裹，面粉堆，发光"),
        lock="撕下的浅褐包装纸折成扁方块，白棉线十字捆住",
        variants="S23 展开：棉线解开、纸摊平，只拍纸背；锚点只出捆好的样子",
    ),
    Prop(
        key="p471_水晶藻叶", name="水晶藻叶", build="i23d",
        why="软体、有界 → **image-to-3D** 只取静态形（它不是刚体，白模只作占位；出片靠图）",
        size="每片长约 40 cm、宽约 4 cm；四片一束",
        ep="ep02 S24（鱼人怀里抱着一把；亚伦抽走、揣进怀里）· S25（亚伦从怀里掏出，手里攥着四片）",
        subject=("四片长长的带状水藻并成一束，根部捏在一起：每片是一条从根到梢几乎一样宽的窄长扁带，长约是宽的十倍，"
                 "梢头圆钝，没有中脉，边缘微微起波浪；叶片薄得透光，能隔着上一片看见下一片的影子，"
                 "迎光处晶莹透亮，里面有细细的平行纵纹；湿漉漉地挂着水珠"),
        material="叶片浅淡的青绿偏冰蓝、半透明、表面光滑有光泽；根部一截颜色转深，带一点墨绿",
        wear="叶缘几处**旧的**小缺口；根部沾着一点湖泥",
        negative=("发光，荧光，自发光，魔法光效，水晶石头，冰块，玻璃制品，塑料，干海带，紫菜，深褐海带，人工染色，"
                  "宽叶，披针形叶，中脉，陆生植物叶子，玉簪叶，韭葱，不透明叶片"),
        lock="四片青绿偏冰蓝的半透明带状水藻，湿亮起波边",
    ),
    Prop(
        key="p472_本的草叉", name="本的草叉", build="script",
        why=("直杆 + 两根弯齿，**长度与齿距决定够不够得着**（S35 叉口卡住收货人的脖子、S39 别住斧枪杆）→ **脚本建**"
             "（圆杆 + 铁箍 + 两根弯铁齿，尺寸照本卡）。农具，不是装备，不进 `loadouts/`"),
        size="全长约 1.7 m；木杆粗约 3.5 cm；叉头两齿长约 30 cm、齿距约 18 cm（刚好卡住一个人的脖子）",
        ep=("ep02 S07（本拄着 → 放下，靠在篱笆边；bg805 标志道具）· S29（沃尔特扛在右肩）· S34（捅一叉逼退强盗）"
            "· S35（叉口卡住收货人的脖子，按在南瓜堆上）· S38–S39（叉头顶退埃尔兰、叉口别住斧枪杆）"
            "· S42（叉杆一绊、赶猪进谷仓）· S45（沃尔特在屋里比划）"),
        subject=("一把两齿的旧草叉，沿画面对角线平放：一根笔直的细长木杆，杆长是杆粗的四十多倍，木杆只有叉口宽度的五分之一粗、一只手就能整把握住，整把竖起来比成年男人还高；"
                 "顶端套一只锻铁叉头——一圈铁箍包住杆头，往上分出两根向前微弯的长铁齿，叉头只占全长约五分之一，"
                 "两齿之间张开一个 U 形的叉口；杆尾平截，没有铁件"),
        material="木杆是白蜡木，浅灰褐、纹理顺直；叉头是黑灰熟铁，铁箍上两颗方头铆钉",
        wear="木杆中段与杆尾两处被手握得颜色更深、发亮；两根齿尖磨得圆钝、不尖，齿身一层薄薄的**旧**锈；铁箍下沿一圈干草屑与旧泥",
        negative="三叉戟，三齿以上的叉，魔鬼叉，长矛，钢叉，短柄手叉，粗木柄，尖利齿尖，不锈钢，塑料柄，现代园艺工具，崭新，发光，武器装饰",
        lock="两齿旧草叉，白蜡木长杆握处发亮，黑铁叉头U形叉口",
    ),
    Prop(
        key="p473_装金砂的小木箱", name="装金砂的小木箱", build="script",
        why=("直线板材、尺寸决定谁搬得动（狗头人抱得动、强盗一手拎一只）→ **脚本建**。"
             "不复用 p45 / p74 / p96 / p159 / p365 / p413：都约 1 m、钉死盖，装不了砂、撒不出来、也搬不动"),
        size="外形约 40 × 25 cm、高 20 cm；板厚约 1.5 cm",
        ep=("ep02 S14（墙根一排摞着；狗头人往里装金砂）· S15（矿工扔下四散）· S30（强盗搬到收货人面前摞起来）"
            "· S31（被滚落的南瓜撞翻，金砂撒进垄沟）——**矿洞与南瓜田同款，是连起两地的那条线**"),
        subject=("一只敞口的小木箱，没有盖：四面是钉在一起的窄木板，两头短板上各穿一根粗麻绳提手；"
                 "箱里装着大半箱深褐带灰的碎砂，砂里夹着星星点点的金色细粒"),
        material=("新刨不久的浅黄松木板，木纹清楚、颜色比旧木器浅得多；每块板两头各一颗手打方头铁钉，"
                  "钉头小、暗灰、略歪、平嵌进木面；麻绳本色"),
        wear="板缝里嵌着**旧的**深褐泥砂；箱沿有几处手抓出的发黑指印",
        negative=("宝箱，铁箍宝箱，金币，金条，珠宝，满箱闪光的金子，发光，箱盖，锁，风化灰朽的旧木箱，大木箱，现代纸箱，塑料箱，"
                  "垫圈，螺钉，十字螺丝，带孔钉头，现代五金，文字，印章，标签"),
        lock="浅黄新松木敞口小木箱，两头麻绳提手，大半箱带金粒的深砂",
        variants="S31 翻倒：箱子侧翻，碎砂从箱口泼进垄沟；S14 墙根也有几只只剩一层砂的空箱；锚点只出装着砂、立着的样子",
    ),
)

TRI: dict[str, Tri] = {
    "p465": Tri(
        obj="卷纸", side_aim="纸卷仍平放，镜头正对它圆圆的一端端口",
        side=side("圆形端口", "横躺的卷筒长边、油渍和划破口",
                  "画面里是一个近乎正圆的端口，卷筒向画面深处缩成很短的一截：两圈多偏黄厚纸卷成的空心螺旋，"
                  "最外层纸边卷曲起毛；端口外缘露出皮绳勒出的一道浅凹和垂下的一截绳头。"),
        back_aim="纸卷仍平放，从对面看过去",
        back=back("纸卷横在画面里，细皮绳绕两圈，活结转到纸卷背面下方、只露出绳圈；"
                  "那块深色油渍与三道划破口转到纸卷下侧，只露出一截。纸背一片空白，没有任何字迹、线条或记号。"),
        size_m=(0.22, 0.04, 0.04),
        queries=("rolled paper tied string", "rolled blank paper sheet", "paper roll leather cord"),
        prompt_en=("A loosely rolled sheet of thick yellowish paper, only two turns and hollow in the middle, tied around "
                   "the middle with a thin dark brown leather cord, a grease stain and three short parallel cuts through "
                   "the outer layer with frayed lifted edges, blank surface with no lines or marks, isolated object"),
        brief=("形制要点：偏黄厚纸松卷两圈多、中间空心，卷起长约 22 cm、粗约 4 cm（展开约 30 × 22 cm），"
               "中段细深褐皮绳绕两圈打活结，外层一块旧油渍、三道划破纸的短口子（口边起毛翘起，不是笔线）；"
               "纸背空白，字永不入画。"),
    ),
    "p466": Tri(
        obj="条项链", side_aim="项链仍平摊，机位压低、从左侧贴着台面平视",
        side=side("厚度", "平摊的大圈",
                  "整条链子的大圈被透视压扁成一道很窄、贴着台面的细椭圆线，链节一粒粒微微反光；椭圆坠子在最近处，"
                  "只露出一道薄薄的银框侧沿，暗红石头在框沿上方鼓出一点弧顶，框边一圈细绳纹。银色氧化发暗，凸起处磨出一点亮色。"),
        back_aim="项链仍平摊，从对面看过去",
        back=back("坠子仍是石头朝上；手弯的银丝小钩与小圆环也随之转到对面。"
                  "链子仍细得像一根线、绕成一个大圈；暗红石头光面半透，银框边一圈细绳纹；链节缝里嵌着旧的黑色污垢。没有任何字迹。"),
        size_m=(0.2, 0.25, 0.01),
        queries=("antique silver necklace hook clasp", "victorian silver cabochon pendant", "fine silver chain pendant"),
        prompt_en=("An old tarnished silver necklace with a very fine thread-thin chain laid flat in a large loop, about "
                   "eighteen times the pendant's length, a thumb-sized oval silver-framed dark red cabochon pendant with a "
                   "rope-twist bezel, closed by a small hand-bent silver wire hook, no spring clasp, isolated object"),
        brief=("形制要点：约 45 cm（坠子长的十八倍）的氧化发暗细银链，细得像一根线、平摊成一个大圈；"
               "坠一枚约 2.5 × 1.8 cm 的椭圆薄银框坠子，框里光面暗红石、框边细绳纹；"
               "链尾手弯银丝小钩钩进小圆环，没有弹簧扣；坠背平银板、不鼓、磨亮无字。"),
    ),
    "p467": Tri(
        obj="只项圈", side_aim="项圈仍平放，机位压低到只比铜带高一点",
        side=side("外侧壁", "小圆铜牌的牌面",
                  "项圈被透视压成一道扁扁的黄铜环带：近处这一段铜带的外侧整面朝着镜头，上沿一排、下沿一排圆头铆钉，"
                  "两排一模一样；远端那一段露出磨亮的内侧。小圆铜牌在画面右端、只剩一道侧边；"
                  "舌扣在画面左端，是叠在铜带外面的一截舌片和扣座。凹缝里的青绿旧锈与干泥同参考图一致。"),
        back_aim="项圈仍平放，从对面看过去",
        back=back("舌扣转到离镜头最近的这一段、正对画面，看得清舌片、扣框和活套；小圆铜牌转到最远处，被铜环挡住、只露出一道边。"
                  "近处这一段外侧同样上下两排圆铆钉、几处小凹坑与擦伤，内侧磨得发亮。没有任何字迹。"),
        size_m=(0.4, 0.4, 0.05),
        queries=("antique brass dog collar", "brass animal collar rivets", "brass livestock collar"),
        prompt_en=("A wide old collar made of one solid three-finger-wide brass plate bent into a ring, smooth with no holes, "
                   "a row of round-head rivets along both the top and bottom edges, a small plain round brass tag in front, "
                   "a brass tongue buckle on the opposite side, green patina in the crevices, small dents and worn patches, "
                   "isolated object"),
        brief=("形制要点：内径约 38 cm 的三指宽实心黄铜片项圈，铜面光滑无孔，上下两道边沿各一排圆头铆钉（两排绕满整圈），"
               "正中一块指甲盖大的光素小圆铜牌，与它正对的另一头是黄铜舌扣；内侧磨亮、凹缝青绿旧锈，外侧只有小凹坑与擦伤。"
               "外观与 m9 卡项圈句逐句一致。S31 起舌扣崩开（状态变体）。"),
    ),
    "p468": Tri(
        obj="枚戒指", side_aim="戒指仍平放，从侧面贴着看过去",
        side=("戒指从侧面看成一道扁扁的横条：一指节宽的平带，两边沿微微倒圆，外面两道细凹线平行绕过去；"
              "暗黄铜色，凸起的边沿磨出亮色，外面一层细密的旧毛面、几处小磕坑。"),
        back_aim="戒指仍平放，从对面看过去",
        back=("同一枚素面平带戒，外面两道细凹线绕一周；左右与参考图对调，参考图里磨得较薄的那一侧边沿转到画面近处。"
              "戒圈内侧光面，看不出任何字迹。"),
        size_m=(0.023, 0.023, 0.01),
        queries=("wide brass band ring", "antique plain band ring", "worn brass ring"),
        prompt_en=("A wide plain antique dark brass band ring with two fine grooves running around it, worn to a fine matte "
                   "surface with a few small dents, no gemstone, no visible engraving, isolated object"),
        brief="形制要点：外径约 2.3 cm、一指节宽的暗黄铜色旧平带戒，外面两道细凹线绕一周，无戒面无宝石；内圈刻字永不入画。",
    ),
    "p469": Tri(
        obj="封信", side_aim="信仍平放，正对它的短边，机位压低到只比纸面高一点",
        side=side("厚度", "顶面和那一滴小墨渍",
                  "画面里是四层薄纸叠起来的纸边与一道圆滑的折脊，整叠只有一指甲厚，顶面只剩一条窄边；"
                  "淡紫细丝带从顶面绕下来、在侧边勒出一道浅凹，小活结和两截软塌的丝带头搭在顶面边上。"
                  "近处一只纸角有反复折过的软毛边。"),
        back_aim="信仍平放，从对面看过去",
        back=back("顶面仍是那一整片淡米白纸、没有中缝，丝带横绕一圈，小活结转到对面；"
                  "起毛的那只纸角与那一滴晕开的小墨渍转到远端。没有任何字迹。"),
        size_m=(0.12, 0.09, 0.01),
        queries=("folded paper packet ribbon", "folded blank paper sheet", "old folded paper tied ribbon"),
        prompt_en=("A small flat packet of thin soft pale cream letter paper folded in half and in half again, one smooth "
                   "folded spine and four staggered paper edges on the opposite side, no center seam, tied once around "
                   "with a thin faded lavender ribbon in a small loose knot, one small irregular ink blot soaked into the "
                   "paper, blank outer side, isolated object"),
        brief=("形制要点：薄软淡米白信纸对折再对折成约 12 × 9 cm 的扁块，顶面一整片、无中缝，一边折脊、对边四层错开的纸边；"
               "褪色淡紫细丝带横绕一圈打小活结；一只纸角起软毛边、一滴晕开渗进纸纤维的小墨渍；外面空白，字永不入画。"),
    ),
    "p470": Tri(
        obj="张便条", side_aim="便条仍平放，正对它的一边，机位压低到只比纸面高一点",
        side=side("厚度", "顶面、茶渍圆印和棉线结",
                  "画面里是扁扁的一叠几层厚纸，只有半厘米厚，撕出来的毛边一层层参差，顶面只剩一条窄边；"
                  "白棉线从顶面十字绕下来，在侧边勒出一道细凹。浅褐色纸纤维粗。"),
        back_aim="便条仍平放，从对面看过去",
        back=back("顶面仍是扁平的浅褐纸方块，白棉线十字、结在正中；淡褐茶渍圆印与蹭了干面粉的那一角转到对面。没有任何字迹。"),
        size_m=(0.07, 0.07, 0.005),
        queries=("folded brown paper square string", "torn brown paper folded", "brown paper tied cotton string"),
        prompt_en=("A flat small square of torn light brown wrapping paper folded twice onto itself, only a few layers thick "
                   "with nothing inside, torn fuzzy edges, tied crosswise with white cotton string knotted in the center, "
                   "a faint tea ring stain and a faint smear of dry flour, blank outer side, isolated object"),
        brief=("形制要点：浅褐厚包装纸撕下后自己对折再对折成约 7 × 7 cm、厚约半厘米的扁平小方块，里面不包东西，"
               "四边撕口毛边或折边、无三角折角；白棉线十字捆住、正中打结；一圈淡褐旧茶渍、一角蹭薄干面粉；"
               "外面空白，字永不入画。"),
    ),
    "p471": Tri(
        obj="束水藻", side_aim="水藻仍平放，从根部那一端看过去，机位压低到贴着台面",
        side=side("根部和顺着长度方向压短的叶带", "整片摊开的叶面",
                  "近处是捏在一起的根部，颜色最深、沾着湖泥；四条窄扁带从这里朝画面深处铺开，被透视压成几道很窄、"
                  "微微交叠的亮带，薄得几乎透明，边缘的波浪起伏清楚。叶面湿亮，挂着水珠。"),
        back_aim="水藻仍平放，从对面看过去",
        back=back("根部从参考图里的一头转到另一头；四条窄扁带叶面半透明，能隔着上一片看见下一片，迎光处晶莹透亮，"
                  "细细的平行纵纹可见，没有中脉；叶缘几处小缺口的位置随之转到对面。"),
        size_m=(0.4, 0.12, 0.02),
        queries=("Vallisneria leaves", "Zostera marina", "eelgrass blades"),
        prompt_en=("Four long translucent pale green-blue aquatic ribbon-like blades gathered at the base, each a narrow flat "
                   "ribbon of nearly even width from base to tip, about ten times longer than wide, no midrib, thin enough "
                   "to see the blade beneath through it, glossy and wet with water droplets, gently wavy edges, isolated object"),
        brief=("形制要点：四片约 40 × 4 cm 的窄长扁带状水藻（从根到梢几乎等宽、无中脉、薄得透光）根部捏成一束，"
               "浅淡青绿偏冰蓝、半透明、湿亮挂水珠，叶缘微波浪；不发光。"),
    ),
    "p472": Tri(
        obj="把草叉", side_aim="草叉仍平放，正对它的长边，机位压低到贴着台面平视",
        side=side("侧面轮廓", "两齿张开的 U 形叉口",
                  "两根铁齿前后叠成一根，只见它们微微上弯的弧线；铁箍包住杆头，两颗方头铆钉露出一颗。"
                  "细长的木杆横贯整个画面，杆长是杆粗的四十多倍，叉头只占全长约五分之一；"
                  "中段与杆尾两处握出来的深色亮痕清楚，杆尾平截。"),
        back_aim="草叉仍平放，从对面看过去",
        back=back("叉头从参考图的一端转到另一端；两根铁齿张开的 U 形叉口同样清楚，齿尖磨得圆钝、带薄锈，"
                  "铁箍下沿一圈干草屑与旧泥。白蜡木杆细长、纹理顺直，握痕位置随之对调。"),
        size_m=(1.7, 0.2, 0.05),
        queries=("pitchfork", "hay fork farm tool", "two tine hay fork"),
        prompt_en=("An old two-tined hay pitchfork taller than a grown man, with a long slender straight ash wood handle about "
                   "forty times as long as it is thick, worn smooth and dark at the grips, a forged black iron head taking "
                   "only a fifth of the length, two slightly curved tines with blunt rounded tips forming a U-shaped fork, "
                   "isolated object"),
        brief=("形制要点：全长约 1.7 m 的两齿旧草叉（比成年男人还高），白蜡木细长杆（粗约 3.5 cm，杆长是杆粗的四十多倍）"
               "中段与杆尾握处发亮，黑铁叉头只占全长约五分之一、铁箍两颗方铆钉，两齿长约 30 cm、齿距约 18 cm、向前微弯，齿尖磨钝。"),
    ),
    "p473": Tri(
        obj="只木箱", side_aim="正对小木箱的一头短板",
        side=side("一头短板", "长板板面",
                  "短板正对画面，比长板窄得多：几块窄的浅黄松木板横拼，板缝里嵌着旧泥砂，每块板两头各一颗小小的手打方头铁钉，"
                  "正中穿过一根粗麻绳提手、两端在板内侧打结；长板被透视压成画面边上一条窄窄的斜边。"
                  "箱沿上方露出一线深褐碎砂的表面，金色细粒星星点点。箱子不深，高比宽矮。"),
        back_aim="正对小木箱的背面长板",
        back=back("这是另一块长板：同样的新刨浅黄松木窄板横拼、每块板两头各一颗手打方头铁钉，"
                  "但木节、泥迹和指印的位置都和参考图那块长板不一样；参考图里靠右的那一头麻绳提手现在在画面左侧。"
                  "箱沿上方露出装到大半箱的深褐碎砂与金色细粒，箱沿几处手抓出的发黑指印。"),
        size_m=(0.4, 0.25, 0.2),
        queries=("small wooden crate rope handles", "old wooden box cut nails", "pine box rope handles"),
        prompt_en=("A small open-top box of freshly planed pale pine boards held with small hand-forged square-headed iron "
                   "nails, no washers or screws, thick rope handles on both short ends, filled most of the way with dark "
                   "brown grit speckled with tiny gold flecks, isolated object"),
        brief=("形制要点：约 40 × 25 × 20 cm 的敞口小木箱（无盖），新刨浅黄松木窄板钉成、每块板两头各一颗手打方头铁钉（无垫圈），"
               "两头短板各穿一根粗麻绳提手，装大半箱带金色细粒的深褐碎砂。矿洞与南瓜田同款。"),
    ),
}

# 共用 card() 里只属于 ep01 的几句，换成 ep02 的；找不到原句就 raise（ep01 模板改了要跟着改这里，别静默失效）
SWAPS: tuple[tuple[str, str], ...] = (
    ("`tools/gen_props_szzl.py`", f"`{GENERATOR}`"),
    ("那会把质量上限锁死在方盒子水平。\n",
     "那会把质量上限锁死在方盒子水平。\n> **本件只出正面**（asset.toml `views`，用户 2026-09-30 裁定：手持剧情物件只当镜头参考、不转 3D）；"
     "下面的侧 / 背块留作将来要转 3D 时用，`gen_bg_assets.py images` 不出。\n"),
    ("（对照 `0_research/map/refs/` 的 c60 原图与微型地下城图）", "（对照本卡锁定描述符与剧本对应镜）"),
    ("把尺寸写进 `tools/build_northshire.py`，**由脚本确定性生成，不手改 blend**", "按本卡尺寸由脚本确定性生成，**不手改 blend**"),
)


def card(p: Prop) -> str:
    text = base.card(p)
    for old, new in SWAPS:
        if old not in text:
            raise SystemExit(f"{p.key}：共用模板里找不到「{old.strip()[:30]}」——ep01 的 card() 改了，同步本文件的 SWAPS")
        text = text.replace(old, new, 1)
    return text


def asset_toml(p: Prop) -> str:
    extra = [f"{gba.VIEWS_KEY} = {props_lib._fmt(list(VIEWS))}"]
    if base._rk(p) in NO_TEXT_KEYS:
        extra.append(f"{gba.NO_TEXT} = true")
    return base.asset_toml(p) + "\n".join(extra) + "\n"


def _m9_collar() -> list[str]:
    """m9 卡「项圈: 」句拆成短句，去掉只在猪身上成立的（套在脖子上、压住颈毛）——p467 必须逐句含有。"""
    line = next((s for s in io.open(M9, encoding="utf-8") if s.startswith("项圈: ")), None)
    if line is None:
        raise SystemExit(f"{M9} 里找不到「项圈: 」那一行——m9 卡改了格式，同步 _m9_collar()")
    body = line.split(": ", 1)[1].strip().removeprefix("脖子上套着一只")
    return [c for c in re.split("[，；。]", body) if c and "颈毛" not in c]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    story = {r["key"] for r in props_lib.registry(base.ROOT) if r.get("kind") == "story"}
    bad = [p.key for p in PROPS if p.key.split("_", 1)[0] not in story]
    if bad:
        raise SystemExit(f"这些键没在 props/registry.toml 登记为剧情物件（kind = \"story\"）：{bad}")
    names = {r["key"]: r["name_zh"] for r in props_lib.registry(base.ROOT)}
    drift = [p.key for p in PROPS if names[p.key.split("_", 1)[0]] != p.key.split("_", 1)[1]]
    if drift:
        raise SystemExit(f"目录名与 registry 的 name_zh 对不上：{drift}")
    missing = {base._rk(p) for p in PROPS} ^ set(TRI)
    if missing:
        raise SystemExit(f"PROPS 与 TRI 的键对不上：{sorted(missing)}")
    clash = set(TRI) & {k for k in base.TRI if k not in TRI}
    if clash:
        raise SystemExit(f"与 ep01 的 TRI 撞键：{sorted(clash)}")
    collar = next(p for p in PROPS if base._rk(p) == "p467")
    miss = [c for c in _m9_collar() if c not in (collar.subject + collar.material + collar.wear).replace("**", "")]
    if miss:
        raise SystemExit(f"p467 与 m9 卡的项圈句逐字对不上，缺：{miss}")
    base.TRI.update(TRI)
    for p in PROPS:
        assert len(p.lock) <= 30, f"{p.key} 锁定串 {len(p.lock)} 字 > 30"
        body = card(p)
        views = body.split("# 三视图 prompt", 1)[1].split("## 负面词")[0].split(base.FENCE + "text")[1:]
        assert len(views) == 3 and not any("状态变体" in v or "**" in v for v in views), \
            f"{p.key} 三视图 prompt 不是三块，或混进了状态变体 / markdown 粗体"
        if base._rk(p) in NO_TEXT_KEYS:
            if NO_GLYPH_NEG not in p.negative:
                raise SystemExit(f"{p.key} 是禁字物件，负面词缺共用的 NO_GLYPH_NEG")
            hit = [w for w in GLYPH_PRONE if any(w in v for v in views)]
            if hit:
                raise SystemExit(f"{p.key} 是禁字物件，prompt 里的「{'、'.join(hit)}」会被画成符号——写成划破口 / 擦伤 / 晕开的墨渍")
        d = os.path.join(base.ROOT, p.key)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, p.key + ".md"), "w", encoding="utf-8", newline="\n").write(body)
        io.open(os.path.join(d, "asset.toml"), "w", encoding="utf-8", newline="\n").write(asset_toml(p))
        front = views[0].split(base.FENCE)[0].strip().split("\n", 1)[1]
        print(f"  {p.key:22} {p.build:7} 锁定串 {len(p.lock):>2} 字 · 正面 prompt {len(front.strip()):>4} 字")
    print(f"\n写出 {len(PROPS)} 张 ep02 物件卡 → {base.ROOT}/")
    print("  复用：S01–S03 的信＝p13_封好的文件；S30 / S37 翻倒的货车＝p349_双轮木板车（见本文件抬头）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
