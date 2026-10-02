# -*- coding: utf-8 -*-
"""ep02 各分段镜表共用的键与措辞。只放两个以上分段都用得到的东西；某一镜独有的写在那一镜里。

分段模块一律 `from szzl_ep02.common import *`，要加共用项就加在这里（按类别追加，别改已有的值——别的分段在用）。
"""
from szzl_shot_engine import carry

# ── 人物卡键（characters/ 目录名）──
A, D = "c1_Aaron", "c2_Duke"
DUG = "c8_Marshal_Dughan"
WIL, LYR = "c19_Brother_Wilhelm", "c20_Lyria_DuLac"
WALT, NELL, BEN, GRAN = "c21_Walt", "c22_Nell", "c23_Ben", "c24_Grandad"
MA, BERN, MAY, TOMMY, BILLY = ("c25_Ma_Stonefield", "c26_Bernice_Stonefield", "c27_Maybell_Maclure",
                               "c28_Tommy_Joe_Stonefield", "c29_Billy_Maclure")
PESTLE = "c30_William_Pestle"
COLL, ERLAN, SUR = "c31_Morgan_the_Collector", "c32_Erlan_Drudgemoor", "c33_Surena_Caledon"
GREY = "c34_Grey_Coat"      # 只远景、不建 Seedance entity（卡头）；引擎给 chars 里每个人都挂 entity——S41 写成人形 [[prop]]、不进 chars
KO, GN, MU, TH, SOW = "m1_Kobold", "m2_Gnoll", "m3_Murloc", "m4_Defias_Bandit", "m9_Princess"

# ── 装备键（equipment/registry.toml；身上穿什么以 loadouts/*.toml 的 ep02 分段为准）──
# 亚伦 L05a（S01–S47）/ L05b（S48–S49）
HAMMER, TUNIC, PANTS, BELT, BRACERS, BOOTS = "e5110", "e2404", "e2802", "e3702", "e2502", "e3902"
GLOVES_A, MAIL_GLOVES = "e3604", "e3602"          # 锈橙皮连指手套（S01–S47）→ 暴风城链甲手套（S43 接过、S48 戴上）
# 杜克 L05a（S01–S16）/ L05b（S17–S47）/ L05c（S48–S49）
VEST, CLOAK, STEEL, SWORD = "e3403", "e4302", "e5205", "e5112"
GLOVES_D, LION_GLOVES = "e1603", "e2603"           # 石板灰露指布手套（S01–S16）→ 狮纹露指皮手套（S17 起）
LANCER = "e5204"                                   # 长枪兵之盾：S04 右手拎着、S05 交给沃尔特、S48 挂上谷仓墙
BRASS = "e3502"                                    # 黄铜护腕：S45 放上桌、S48 两人都戴上

# ── 物件卡（props/ 目录名）──
LETTER, CART = "p13_封好的文件", "p349_双轮木板车"
SCHEDULE, NECKLACE, COLLAR, RING = "p465_采金日程表", "p466_波尼斯的项链", "p467_公主的黄铜项圈", "p468_收货人的戒指"
LOVE_LETTER, NOTE, KELP, FORK, GOLD_BOX = ("p469_梅贝尔的情书", "p470_老奶奶的便条", "p471_水晶藻叶", "p472_本的草叉",
                                          "p473_装金砂的小木箱")

# ── 条件负向（按镜挑；`@组名` 由引擎从 style_guide §5 读，`@卡:m7_Wolf` 读怪物卡的负向节）──
ELW, BEHAVE, NOHOLY = "@版本·艾尔文", "@玩家行为", "@无圣光镜"
ARMOR_MIX = "护肩，头盔，全身板甲，华丽装备"          # 杜克穿链甲短背心、披风：不能挂「胸甲 / 锁子甲 / 披风」
AURA_ON = "治疗光柱，护盾泡泡，武器持续发光，锤头常亮，金色光柱"
AURA_HL = "护盾泡泡，武器持续发光，锤头常亮"          # 圣光术镜：光柱是正文要的，不能进负向（rule 45 闸门）
FIGHT = "喷血，伤口特写，刃口入肉，断肢，血泊"
BODY = "尸体，躺倒不动的人，死亡特写，倒地特写"       # G2：本集没有死亡
TEXT = "可读的字迹，信纸上的文字，清晰字母"           # G8：信 / 卷纸 / 便条 / 戒指只拍背面或侧面
FALL = "慢动作，落体滞空，碎片缓慢飘散，掉落物匀速下落"

# ── 身上的东西（本镜状态逐字引用；拿法一律经 carry()，G3）──
HAM = "父亲的旧双手锤"
HAM_SH = HAM + carry(HAMMER, "扛肩")
HAM_2H = HAM + "：" + carry(HAMMER, "双手握")
STL = "竖长十边形冷灰钢盾"
GRIP = "把手缠着祖父木盾上拆下的那条旧皮条"         # 看得见盾背面时接在盾那一句后面，用「，」连（单独成句会被判「提到盾却没写怎么拿」）
STEEL_ON = STL + "：" + carry(STEEL, "在用")
STEEL_DOWN = STL + "：" + carry(STEEL, "垂放")         # 赶路、说话时
SWORD_SH = "旧短剑" + carry(SWORD, "入鞘")
SAT = "右胯一只磨白的帆布挎包"
BAG = "背上小布包"                                  # 亚伦赶路时背着；进屋 / 打斗前镜内卸下（rule 16.1–16.3）
# 一身行头（entity 已锁外观，这里只点名、写短——精简稿 ≤ 2000 字，【人物】段最占字数）。
# L16：手套形制易画错——这里写明形制，露得出手的镜在 props 另挂该手套的装备正面图（GLOVES_A / GLOVES_D / LION_GLOVES）
AARON_KIT = ("身穿夹层外衣，腕上狼皮护腕，手上锈橙皮连指手套（四指并在一个皮套里，只分出拇指），"
             "腰系红褐皮带，腿上橄榄土黄粗皮长裤，脚上交叉绑带靴")                               # S01–S47
DUKE_KIT_A = "身穿链甲短背心，背后白灰短披风，手上石板灰露指布手套（四指与拇指从指根起露在外面）"   # S01–S16
DUKE_KIT_B = "身穿链甲短背心，背后白灰短披风，手上露指短皮手套（五个指套只到第一个指节，手指露在外面）"  # S17–S47：挂 c2-4 + e2603 正面图（L05b known_issue）
SH_BAND = "左肩缠着布条，布条从链甲领口露出一截"      # states.toml：S01–S10 每镜写到「左肩」；S11 拆掉

# ── 光（天光按剧本头部第 11 条：第一天午后 → 黄昏 → 月夜；第二天上午 → 午后 → 傍晚；
#        第三天清早 → 正午 → 午后 → 黄昏 → 夜；第四天清晨。用到哪一档再在这里加一档）──
AFTERNOON = "午后，暖白阳光从西南中高角度斜照，阴影清晰"   # 照 bg4 / bg6 卡锁定 #5；写成「斜阳暖金」黄昏就没台阶、学会本事的金光会和日光同色（qc5 光线 M2）
AFTERNOON_STYLE = "外景午后日光"
