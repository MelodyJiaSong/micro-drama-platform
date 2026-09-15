# -*- coding: utf-8 -*-
"""《时空旅行》sk1 · 汴京清明一日 —— 游览 vlog 分镜 + 五层 prompt 生成器（阶段 5/6 合一）。

改内容＝改本文件重跑（rule 4i ①）：
    python tools/gen_shots_sk1.py                  # 严格：任何 PENDING: 事实占位直接终止
    python tools/gen_shots_sk1.py --allow-pending  # 调研未齐时：PENDING: 只报 warning
    python tools/gen_shots_sk1.py --traveller c4   # 换旅行者（系列名册 `_series/characters/`，默认 c1）

产物：5_6_分镜与prompt/{shotlist.md, shots/shotNN/shotNN.md, all_shot_prompts.md}
      4_剧本/dialogue.md（由镜表生成，中英两条）；4_剧本/script.md 每镜「时长 / 台词」两段同步覆盖。

形态（系列 follow-up 008 / 009 / 010）：只有林问开口（对镜 `正常台词` / 画外 `内心独白`）；当地人零台词、
不看镜头，只用动作与手势回应；群声是没有可辨字句的环境声；没有人拦她，她守规矩（不走御道、宫里不碰东西）。
旅行者（系列 follow-up 012）：由 `--traveller cN` 从系列名册选，名字 / 两态锁定串 / 声音锁定串 / 视频里说的语种全部读系列卡；
镜表里写「林问 / Lin Wen」是占位名，落盘前换成选中的人。视频直接出声（`声音:` 行 + `cN-2` 声样），另一语种走译配轨，逐句同窗。

构建闸门（不合格直接 raise，分镜生成不出来）：
    ① 单镜 15–30 s、片长 600–900 s；TTS 时长目标之和 ≤ 镜长；中文 ≤ 5.2 字/秒（逐句 + 整镜）；英文 ≤ 2.8 词/秒
    ② 只有林问发声；`正常台词` 必须林问入画、窗口落在露脸的那一段、`动作:` 该拍写明看镜头；台词窗口不重叠；每句必填情绪
       `台词:` 行〔〕只放类型与口型指令（K21 / rule 12.4 v2），时间窗与视线进 `走位:` 的「林问开口与视线时间表」
    ③ 签名开场 / 自报家门 / 签名收尾 / 置顶评论问题中英逐字；固定句 3–5 次且单独成句；原文引语（「」）≥ 6 段
    ④ 时辰 `tod` 单调不减（可选镜除外），`光线:` 必带该时辰词
    ⑤ 史实（K34）：每镜 ≥1 fact；无 ai_draft；❌ 只在 S09；⚠️ 镜必有推测口播（中英同带）
    ⑥ 锁定串（K8/K20）：从卡里**抽出锁定值做相等比较**（人物识别标签、道具锁定串、场景一句话锁定、STYLE_BASE、负向块）
    ⑦ 随身状态：林问入画必写手位 `hands`；柳枝 / 驴 / 布包状态串按镜号区间逐字出现
    ⑧ 镜间切口（tools/shot_seam.py）；唯一承接对 S01→S02，两端机位与景别档必须相同
    ⑨ 正向 prompt ≤ 5000 字（K10）；零 hex（K9）；prompt_light（K32）；shot_logic（K33）
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facts_registry  # noqa: E402
import prompt_light  # noqa: E402
import shot_logic  # noqa: E402
import shot_seam  # noqa: E402

DRAMA = "ai_videos/shikong_lvxing/sk1"
ROOT = DRAMA + "/5_6_分镜与prompt"
ASSETS = "2_世界观人设"
A = DRAMA + "/" + ASSETS
SERIES_CHARS = "ai_videos/shikong_lvxing/_series/characters"
STYLE_GUIDE = A + "/style_guide.md"
NL = "\n"
FENCE = chr(96) * 3
MAX_PROMPT = 5000
MIN_D, MAX_D = 15, 30
TOTAL_LO, TOTAL_HI = 600, 900
MAX_CPS = 5.2
MAX_WPS = 2.8
ALLOW_PENDING = "--allow-pending" in sys.argv[1:]
LANG_ZH = {"zh": "普通话", "en": "英语"}


def _cli_traveller() -> str:
    argv = sys.argv[1:]
    for i, a in enumerate(argv):
        if a.startswith("--traveller="):
            return a.split("=", 1)[1]
        if a == "--traveller" and i + 1 < len(argv):
            return argv[i + 1]
    return "c1"


def _fence_after(text: str, head: str) -> str:
    m = re.search(r"^%s[^\n]*\n(.*?)(?=^#{1,3} |\Z)" % re.escape(head), text, flags=re.S | re.M)
    got = re.findall(r"^```\n(.*?)\n```", m.group(1), flags=re.S | re.M) if m else []
    if len(got) != 1:
        raise SystemExit("旅行者卡缺唯一围栏：%s" % head)
    return got[0]


def load_traveller(key: str) -> dict[str, str]:
    """系列名册里的一张旅行者卡 → 生成器要的全部字段（follow-up 012；卡由 tools/gen_traveller_cards.py 生成）。"""
    folders = [d for d in os.listdir(SERIES_CHARS) if d.split("_")[0] == key]
    if len(folders) != 1:
        raise SystemExit("系列名册里找不到唯一的旅行者 %s：%s" % (key, folders))
    path = "%s/%s/%s.md" % (SERIES_CHARS, folders[0], folders[0])
    text = io.open(path, encoding="utf-8").read()
    y = re.search(r"^```yaml\ntraveller:\n(.*?)\n```", text, flags=re.S | re.M)
    if not y:
        raise SystemExit("%s 缺「生成器读取字段」yaml 块" % path)
    tr = dict(re.findall(r"^  (\w+): (.*)$", y.group(1), flags=re.M))
    tr.update(path=path, modern=_fence_after(text, "### shot 角色行锁定串 · 现代装态"),
              song=_fence_after(text, "### shot 角色行锁定串 · sk1 宋装态"), voice=_fence_after(text, "### 声音锁定串"))
    return tr


TR = load_traveller(_cli_traveller())
KEY, TNAME, TNAME_EN, TLANG, TFOLDER = TR["key"], TR["name_zh"], TR["name_en"], TR["lang"], TR["folder"]
VOICE_LOCK = TR["voice"]


def personalize(text: str) -> str:
    """镜表里的占位名「林问 / Lin Wen」→ 选中的旅行者（落盘前最后一步；幂等）。"""
    return text.replace("c1_林问", TFOLDER).replace("林问", TNAME).replace("Lin Wen", TNAME_EN)

# ───────────────────────────── 签名句与固定件（中英逐字，闸门校验）
OPENING = "今天是宣和二年清明。你在汴京，距今九百零六年。一切都和那天一样——只是，多了一个我。"
EN_OPENING = ("It's the Qingming Festival, second year of Xuanhe. You're in Kaifeng, 906 years ago. "
              "Everything is as it was that day — except I'm here.")
SELF_INTRO = "我是林问，时空考察队的旅行者。"
EN_SELF_INTRO = "I'm Lin Wen, a traveler with the Time Expedition Team."
CLOSER = ("我什么都没改，我只是在场。", "历史不退款——下一站见。")
EN_CLOSER = ("I changed nothing. I was just there.", "History doesn't do refunds. See you at the next stop.")
QUESTION = "给你一贯铜钱，在 1120 年的汴京待一天，你第一文钱花在哪？"  # publish.md 置顶评论，逐字
EN_QUESTION = ("If you had one string of copper coins and one day in Kaifeng in 1120, "
               "what would you spend your first coin on?")
FIXED = "听着像编的，但这是真的。"
EN_FIXED = "Sounds made up, but it's true."
HEDGES = ("史书没写", "推测", "推算", "没查到", "没核实")  # divergence「史书没写 / 按……推算」
EN_HEDGE = re.compile(r"guess|estimat|infer|no record|don't record|doesn't record|not recorded|doesn't say|don't say|"
                      r"never say|didn't find|haven't (?:checked|verified|found)|not sure|unclear|probably|reckon|"
                      r"scholars (?:disagree|haven't|aren't sure)|undecided|my assumption|don't give|isn't recorded|not in the records", re.I)

# ───────────────────────────── 人物锁定描述符（识别标签与卡第 8 行逐字相等；手里拿什么由每镜 `hands` 写）
C1 = TR["song"]
C1_MODERN = TR["modern"]
C2 = ("李十六（参考 c21-1 立绘 + c21-2 turntable · 沉默背景人物，不开口、不看镜头）— 皂巾裹髻补丁短褐灰围布卷裤赤足，肩扛麻袋垫旧布；"
      "三十八岁汴河脚夫：粗麻交领短褐本白泛灰黄多处补丁、前襟撩起掖进皂布腰带、灰布围布、灰褐宽裤卷至小腿、赤足、皂布头巾裹髻、"
      "肩上垫一块旧布、扛麻袋；不赤膊、不八块腹肌")
C3 = ("周四娘（参考 c22-1 立绘 + c22-2 turntable · 沉默背景人物，不开口、不看镜头）— 皂巾包中高髻，灰青褙子皂黑裙青花围巾，守汤茶药担子；"
      "三十一岁汤茶药女摊主：本白交领短襦、皂黑高腰长裙、灰青粗布褙子敞开、青底白花粗布手巾围裙、皂巾包中高髻露额、黑布浅口鞋、"
      "守着汤茶药饮子摊（泥炉铜汤瓶、白瓷缸子、黑釉盏）；不是唐式高髻、不是影楼汉服")
C4 = ("沈十九（参考 c23-1 立绘 + c23-2 turntable · 沉默背景人物，不开口、不看镜头、不拦人）— 黑漆圆顶无脚幞头皂色短衫撩襟裹腿麻鞋，手持木柄骨朵；"
      "二十六岁军巡铺兵：皂色交领窄袖短衫及膝、下摆一角掖进皮带、灰褐窄裤裹腿、麻鞋、黑漆圆顶无脚幞头、手持木柄骨朵；无腰牌、无抹额、无号衣、无铠甲")
DESC = {"c1": C1, "c1m": C1_MODERN, "c21": C2, "c22": C3, "c23": C4}


def _label(desc: str) -> str:
    return re.search(r"— (.*?)；", desc).group(1)


LABEL = {"c1": _label(C1),
         "c1m": _label(C1_MODERN),
         "c21": "皂巾裹髻补丁短褐灰围布卷裤赤足，肩扛麻袋垫旧布",
         "c22": "皂巾包中高髻，灰青褙子皂黑裙青花围巾，守汤茶药担子",
         "c23": "黑漆圆顶无脚幞头皂色短衫撩襟裹腿麻鞋，手持木柄骨朵"}
CHAR_CARD = {"c1": TR["path"], "c1m": TR["path"],
             "c21": A + "/characters/c21_李十六/c21_李十六.md", "c22": A + "/characters/c22_周四娘/c22_周四娘.md",
             "c23": A + "/characters/c23_沈十九/c23_沈十九.md"}
NAME = {"c1": "林问（宋装态）", "c1m": "林问（现代装态）", "c21": "李十六", "c22": "周四娘", "c23": "沈十九"}
TOKEN = {"c1": "%s(Seedance 人物 entity·宋装态)" % TFOLDER, "c1m": "%s(Seedance 人物 entity·现代装态)" % TFOLDER,
         "c21": "c21_李十六(Seedance 人物 entity)", "c22": "c22_周四娘(Seedance 人物 entity)", "c23": "c23_沈十九(Seedance 人物 entity)"}
UPLOAD = {"c1": "**Seedance 人物 entity「%s」宋装态**（系列卡 `_series/characters/%s/%s-1.png` 定脸 + `%s-11.png` 宋装立绘 / `%s-12.mp4` 宋装建立视频）" % (TNAME, TFOLDER, KEY, KEY, KEY),
          "c1m": "**Seedance 人物 entity「%s」现代装态**（系列卡 `_series/characters/%s/%s-1.png` + `%s-2.mp4`）" % (TNAME, TFOLDER, KEY, KEY),
          "c21": "`%s/characters/c21_李十六/c21-1.png` + `c21-2.mp4`（沉默面孔）" % ASSETS,
          "c22": "`%s/characters/c22_周四娘/c22-1.png` + `c22-2.mp4`（沉默面孔）" % ASSETS,
          "c23": "`%s/characters/c23_沈十九/c23-1.png` + `c23-2.mp4`（沉默面孔）" % ASSETS}

VOICE_ZH, VOICE_EN = TR["voice_id_zh"], TR["voice_id_en"]
VOICE_MAIN, VOICE_DUB = (VOICE_ZH, VOICE_EN) if TLANG == "zh" else (VOICE_EN, VOICE_ZH)
TONE_ZH = TR["tone_zh"]
TONE_EN = TR["tone_en"]

# ───────────────────────────── 道具锁定串（与各 p 卡「锁定描述符」围栏逐字相等）
P3_MIC = "无标哑光黑木柄短话筒＝一掌长的短话筒，话筒头是无字黑海绵罩，木柄哑光黑、无漆无标、握位磨出手泽；不是带台标的采访话筒、不是金属网头话筒、不是无线麦克风"
P3_BOOK = "麻布封面线装采访本＝本白粗麻布包硬壳的线装本，书脊麻线明缝，边角磨毛，书脊夹一支短铅笔；不是皮面笔记本、不是螺旋线圈本、不是平板电脑"
P3_EAR = "耳后一枚拇指盖大小的铜色圆片＝哑光黄铜薄圆片，贴在左耳后骨上，只在侧脸与背影露出一线；不是蓝牙耳机、不是耳钉、不是助听器"
P3_BADGE = "素色布质胸牌＝本白粗布小牌，别在左胸，牌面只见几道淡墨笔画痕、没有可读的字；不是塑料工牌、不是挂绳证件、不是印刷体徽章"  # R8 W9：「时空考察队」字样只由后期贴字层加
P1 = ("州桥夜市食摊＝一张矮木案子上架一口平底铁鏊，鏊上现煎的羊白肠切成寸段、表面煎出焦褐、油亮冒热气；案上排开灰褐胎粗陶浅碗与牙白微青的白瓷敞口碗，"
      "碗里分盛腌鱼干（鲊脯）、琥珀色冻透的鱼头冻（㸇冻鱼头）、批切成薄片的羊头肉、姜丝拌萝卜；案后是竹竿撑的黄褐苇席棚，"
      "棚柱上钉的小木托上放一只敞口陶灯盏、案角再放一只敞口陶灯盏，灯盏里一汪油搭一根灯芯、燃着黄豆大的一点火苗，没有纸罩、不是灯笼；"
      "不是辣椒红油、不是玉米番茄土豆、不是孜然烤串、不是塑料盘不锈钢锅")
P2 = "北宋铜钱与钱串＝青褐色圆形方孔铜钱，钱面铸四字年号钱文、钱背光素，串里以熙宁元宝与元丰通宝旧钱为主、政和通宝新钱其次、少数宣和通宝最新钱，钱文为篆隶两体对钱或瘦金体；小平钱径约二点五厘米，间杂几枚三厘米上下的折二与当十大钱；用本色麻绳穿成串，一贯名义一千文、街市实穿七百五十枚上下，麻绳两端打结留头；不是乾隆通宝、不带满文、不是银锭元宝、不是纸币"
P4 = "汤茶药饮子摊＝一把竹骨油纸大伞撑在街边，伞下一副竹挑担落地，一头是带小泥炉的铜汤瓶、炉膛里一点炭火，另一头是三层木架，架上摆一排牙白微青的白瓷缸子与几只黑釉茶盏；担梁上悬一块空白窄木牌（牌面无字）；不是玻璃杯吸管、不是保温桶、不是红灯笼、不是塑料桶"
P6 = "太平车＝两轮大木车，车厢是无盖的平口木栏箱、栏板高与两只大木轮齐平，木轮是实心辐板大轮、径与厢高相当，车厢前板伸出两根二三尺长的方木、驾车人站位就在两木之间，车尾拖着两根斜撑到地的木脚，车底中央悬一只铁铃；原木本色、无漆、边角磨圆、榫卯加铁箍；不是四轮马车、不是欧式 carriage、不是橡胶轮胎铁辐条"
P7 = "彩楼欢门＝酒店门首用长木杆绑扎出的镂空门架、高过店面二层屋檐，杆间以彩帛缠绕、结出花结与垂带，架顶斜插几面素色小旗，架下门面窗棂素木灰褐、门内垂珠帘与绣额；门侧立一块高过人头的空白竖长木立招、门脸横挂一块空白窄条木匾（牌面一律无字）；其余招牌一律无字纹样布幌；不是红灯笼串、不是灯箱、不是印刷体、不是石牌坊"
P9 = "桥尾脚店＝一开间两层木构灰瓦悬山顶小酒铺，面阔约四米、进深约六米、一层檐高约三米，二层临街一圈素木栏杆，木柱不上漆、直棂木窗、一层门板整扇卸下柜台朝街，门首用长木杆绑扎出一座比店面还高的三层镂空彩楼欢门、杆上缠彩帛花结、顶上斜插几面小旗，欢门一侧垂一块空白窄条木牌（牌面无字），临河一侧搭出芦席凉棚、棚下摆桌凳；不是正店那样的三层大酒楼、不是明清式马头墙铺面，屋面无彩绘无琉璃瓦"
PROP = {  # key: (卡锁定串, 卡目录, 参考项)
    "p1": (P1, "p1_旋煎羊白肠与食摊", "p1-1(州桥夜市食摊锚点)"),
    "p2": (P2, "p2_铜钱与钱串", "p2-1(铜钱与钱串锚点)"),
    "p4": (P4, "p4_饮子摊", "p4-1(饮子摊锚点)"),
    "p6": (P6, "p6_太平车与独轮车", "p6-1(太平车与串车锚点)"),
    "p7": (P7, "p7_彩楼欢门与招牌", "p7-1(彩楼欢门锚点)"),
    "p9": (P9, "p9_桥尾脚店单元", "p9-1(桥尾脚店锚点)"),
}
P3_CARD = A + "/props/p3_三件不变物/p3_三件不变物.md"

# ───────────────────────────── 场景一句话锁定（与各 bg 卡锁定表「一句话锁定」一格逐字相等）
BG = {
    "bg0_汴京全城": "汴京全城俯瞰：外城护龙河环绕、皇城居中偏西北、汴河穿城",
    "bg1_虹桥": "东水门外七里朱漆无柱木拱虹桥，桥下漕船放桅过孔",
    "bg2_东水门城门": "跨河夯土水门铁裹闸门高吊，两岸旱门驼队麦车进城",
    "bg3_汴河码头": "城内汴河仓前码头，纲船靠岸袋家扛两石布袋",
    "bg4_州桥御街": "青石低平州桥北望御街，朱杈子御道御沟荷叶初生",
    "bg5_正店酒楼": "三层彩楼高过屋檐、门里烛光门外天光、平头车卸梢桶——不是红灯笼酒楼。",
    "bg6_瓦子勾栏": "席顶看棚一座挨一座、棚外摊市、素木杆——不是明清戏台。",
    "bg7_坊巷民居": "灰瓦素木泥墙、直棂窗席棚、二层栏杆——不是徽派白墙黛瓦。",
    "bg8_郊外清明踏青路": "柳陌田野、轿顶插柳、四野如市、茅檐低伏——不是江南水乡。",
    "bg9_今日州桥遗址": "今日开封州桥考古遗址：很深的考古发掘坑、北宋浮雕石壁、明代砖拱桥",
    "bg10_赵太丞家": "赵太丞家浅色木匾，两块立招高过屋檐，门屋斗拱，不是清式药房",
    "bg11_开封府": "灰瓦素木府门敞开，望进内门庭院与正厅，不是包公戏里的衙门",
    "bg12_宣德楼": "宣德楼五门朱漆金钉，单檐庑殿绿琉璃瓦，朵楼阙亭围成凹字",
    "bg13_相国寺": "相国寺东门书铺街、殿后资圣门书画摊，灰瓦素木北宋寺",
    "bg14_客店房间夜": "客店客房夜里：素木床榻瓷枕、陶油灯、直棂窗，不点蜡烛",
    "bg15_园林雅集": "园池边垂柳下黑漆大案藤墩文士雅集，茶床点茶兔毫建盏",
    "bg16_汴京全城五更": "汴京全城五更天亮：清冷蓝光罩着屋海，街上零星油灯将熄",
    "bg17_州桥夜市": "青石低平州桥南望夜市，两溜食摊只点油灯，无灯笼蜡烛",
}
BG_ID = {k.split("_")[0]: k for k in BG}


def bg_card(key: str) -> str:
    return "%s/scenes/bianjing/%s/%s.md" % (A, key, key)


# ───────────────────────────── 渲染样式与负向（style_guide §6 / §7 逐字）
STYLE_BASE = ("【全程绝对无字幕·画面不烧任何字幕/台词文字/对白文字/caption】"  # K19 高风险档落点（R8 W1），逐字同 hy1–hy4
              "自然纪实影像、实拍质感，光只来自画面里能指出来源的光源；材质细节做满——可辨的木纹与麻绳绑点、灰瓦的哑光、麻布的纤维、"
              "夯土与泥抹墙的粗糙；空气有体积感；35mm 胶片颗粒；不是 CG、不是插画、不是渲染图、不是游戏截图、不是影楼古风；"
              "画面里没有任何字幕、水印、logo。")
NEG_BASE = ("人脸变形, 五官漂移, 多余发光特效, 画面文字, 乱码汉字, 印刷体招牌, 简体字, 让模型自己写字, 字幕, 水印, logo, 畸形肢体, 多余手指, "
            "夸张金光, 现代服饰, 眼镜, 墨镜, 手表, 耳机, 手机, 相机, 拉链, 纽扣, 现代纽扣, 运动鞋, 皮靴, 长筒皮靴, 立领, 盘扣, 比甲, 马褂, "
            "长辫, 瓜皮帽, 旗装, 旗袍, 影楼汉服, 飘带纱裙, 雪纺, 渐变染色, 唐式高髻, 齐胸襦裙, 花钿, 珍珠头面, 高冠, 平民穿紫, 平民衣上金线, "
            "平民戴展脚硬幞头, 披甲戴盔, 统一号衣, 抹额, 腰牌, 红盖头, 三寸金莲, 弓鞋, 小脚蹒跚, 赤膊, 八块腹肌, 银锭, 元宝, 碎银, 银两, "
            "马蹄银, 银子付账, 银票, 纸币, 纸钞, 钞票, 交子, 票号, 钱庄票据, 乾隆通宝, 清代铜钱, 钱面满文, 现代硬币, 辣椒, 红油, 玉米, 番茄, "
            "土豆, 红薯, 花生, 南瓜, 向日葵, 青团, 艾草团子, 绿色糯米团, 粽子, 红灯笼串, 灯箱, 霓虹, 横幅标语, 青砖箭楼, 箭窗, 明清北京式城楼, "
            "欧式城堡, 御街上的木拱桥, 城内虹桥, 四轮马车, 四轮载人马车, 欧式马车, 车夫礼帽, 席地而坐, 跪坐, 蒲团, 矮几, 榻榻米, 满屋蜡烛, "
            "烛台阵列, 吊灯, 宵禁, 坊门, 街鼓, 金吾卫驱人, 空无一人的夜街, 路引, 通关文牒, 身份牌, 城门盘查证件, 塑料感材质, 卡通渲染, 插画风, "
            "CG 感, 国画笔触, 鸟瞰散点透视, 过饱和, HDR 假感, 磨皮, 美颜, 网红脸, 看镜头（受访者对镜答与记者出镜口播除外）")
NEG_ARCH = ("马头墙, 徽派白墙黛瓦, 四合院垂花门, 琉璃瓦, 飞檐翘角过甚, 红柱金匾, 彩画梁枋, 红砖, 整面青砖民居墙, 玻璃窗, 玻璃门, 卷帘门, "
            "石库门, 西式拱廊, 石牌坊, 气球拱门, 明清戏楼, 砖砌剧院, 拔步床, 架子床, 帐幔, 雕花家具, 屏风, 太阳伞, 电线杆, 柏油路, 现代建筑")
NEG_NOFIRE = "火, 火焰, 火把, 篝火, 灯笼, 蜡烛, 烛光, 油灯光, 暖橙光斑, 暖色辉光, 暖色补光, 来源不明的光, 补光痕迹, 镜头光晕特效, 云隙光柱"
NEG_LAMP = "月光直射, 蓝色补光, 提亮的黑位, 路灯, 街灯, 灯笼, 红灯笼, 火把, 篝火, 满屋蜡烛, 烛台阵列, 来源不明的光, 补光痕迹, 镜头光晕特效"
NEG_NOCANDLE = "蜡烛, 烛台, 烛光"
NEG_INDOOR = "瓷砖地面, 木地板, 电灯, 现代床垫, 枕套花纹, 玻璃窗"
NEG_CROWD = "人群超过八个可辨的脸, 整齐划一的群演, 现代游客, 自拍"
NEG_LOCAL = "当地人看镜头, 路人看镜头, 当地人说话, 对口型"
NEG_FALL = "慢动作, slow motion, 子弹时间, 落体滞空, 悬浮下坠, 羽毛般缓降, 掉落物匀速下落"
NEG_DRESS = "现代内衣外露, 拉链, 纽扣, 文胸带, 运动鞋, 袜子花纹"
# 以下是生成器侧条件块（style_guide §6 没有对应行，不做逐字校验；需要时由 style_guide 作者补行）
NEG_TOUR = "古人开口说话, 清晰可辨的古人对白, 路人对口型, 画面里出现无人机"  # follow-up 008 / 010
NEG_SILENT = "人声, 配音, 旁白, 念白, 念出角色名或台词文字, 任何生成人声音轨, no voiceover, no speech, no narration"  # K22：只挂 `台词: 无` 镜
NEG_VOICE = "第二个人声, 声音换人, 电子合成音, 变声, 背景音乐盖过人声"  # follow-up 012：视频直接出声的镜
NEG_NIGHT = "白天的天空, 日光直射"
NEG_NIGHT_MODERN = "电灯, 冷白 LED 光, 手电筒, 冷白光源"  # R4 F32
NEG_SUB_HI = "中文字幕, 对白文字, 台词文字, 字幕条, 弹幕, caption, text overlay"  # K19 高风险档：≥2 句对镜台词
NEG_XUANDE = "金黄琉璃瓦, 北京故宫红墙黄瓦, 重檐"  # style_guide §6 宣德楼例外注
NEG_AERIAL = "无人机影子, 飞行器投影, 镜头投影"  # R3-25
NEG_SKY = "灰白阴天, 灰蒙蒙的天, 雾霾, 浑黄河水, 泥黄色水面"  # follow-up 004：天要蓝、水要绿
NEG_SKY_NIGHT = "灰黑夜空, 浑黄河水"
# 天与水按时段条件化追加进 `光线:`（不进 STYLE_BASE：夜镜没有蓝天，rule 16.9）
SKY_DAY = "；晴天：画面里凡露出天空都是干净通透的蓝天，凡露出水面都是碧绿通透的水，空气透亮、远景清楚，没有灰霾"
SKY_DAWN = "；画面里凡露出天空都是清冷透亮的蓝，凡露出水面都是碧绿的水，没有灰霾"
SKY_NIGHT = "；画面里露出的夜空是深蓝、不是灰黑，露出的水面是深碧绿"
SKY = {"day": SKY_DAY, "dawn": SKY_DAWN, "dawn_lamp": SKY_DAWN}
SKY_AERIAL = "，像天气晴好时无人机航拍的实景（画面里看不到无人机）"
MODERN_DROP = {"现代服饰", "皮靴", "拉链", "纽扣", "现代纽扣"}  # divergence #15：现代装镜不抹她的锁定装束
NEG_BGX = {  # 各地点的误传负向（W7 / W8 调研；❌ 事实只进负向）
    "bg10_赵太丞家": "百子柜, 满墙小抽屉药柜, 药碾, 黑底金字堂号大匾, 某某堂匾额, 中医馆招牌, 清宫剧药铺",
    "bg11_开封府": "鸣冤鼓, 龙头铡, 虎头铡, 狗头铡, 包拯, 黑脸月牙包公, 知府大人牌匾, 明镜高悬匾, 惊堂木, 肃静回避牌, 仿古景区开封府, 清代衙役",
    "bg12_宣德楼": "紫禁城式宫殿, 北京故宫红墙黄瓦, 金黄琉璃瓦, 重檐, 重檐庑殿, 汉白玉三层台基, 龙亭大殿, 明清满铺彩画, 清代侍卫, 太监, 殿内御座, 藻井, 后宫",
    "bg7_坊巷民居": "客栈招牌, 店小二迎客, 肩搭毛巾的伙计, 太师椅, 明清束腰雕花八仙桌, 木枕, 花布棉被",
    "bg14_客店房间夜": "客栈招牌, 店小二迎客, 肩搭毛巾的伙计, 太师椅, 明清束腰雕花八仙桌, 木枕, 花布棉被, 炭盆里的火",
    "bg13_相国寺": "清代重建的大相国寺殿宇, 八角琉璃殿, 明清牌坊式山门, 线装书, 书脊订线, 四眼线装, 函套",
    "bg15_园林雅集": "日式茶道, 抹茶碗, 大碗茶, 长嘴铜壶, 盖碗, 紫砂壶, 醒木, 折扇, 茶坊挂画",
    "bg17_州桥夜市": "纸罩灯, 纸灯笼, 灯串, 玻璃灯罩, 马灯",
}
GRAVITY = "【重力真实】本镜里倒下或落下的%s一律按真实重力加速下坠、越落越快、落定即停，全程实时速度，不慢动作、不滞空"
DAY_TAIL = "；画面里没有任何火、没有任何暖色人工光源、没有灯笼"

# 时辰（tod）：序数只增不减；`光线:` 必带对应时辰词（R4 F02）
TOD = {1: ("卯时",), 2: ("辰时",), 3: ("巳时",), 4: ("午时",), 5: ("未时",), 6: ("申时",), 7: ("酉时",),
       8: ("戌时",), 9: ("三更",), 10: ("五更",), 99: ("今天",)}

# ───────────────────────────── 随身状态串（rule 16.3：成型后逐字复现，成型前反向声明）
WILLOW_NONE = "包髻上此时没有插任何花枝柳枝"
WILLOW = "包髻左侧斜插着一枝嫩柳（一拃半长、嫩叶朝后垂）"
WILLOW_TABLE = "那枝柳已从包髻上取下，横放在桌上油灯旁"
KNOT = "本白布包用一根本色麻绳在床腿上绕两圈、在床腿外侧打一个死结、留一截一拃长的绳头"
BUNDLE_LOOSE = "本白布包放在床上，没有拴在床腿上"
BUNDLE_NONE = "床腿上此时没有任何布包"
DONKEY_BACK = "驴已还给赁驴人牵走，此后她步行"
SONG_POCKET = "话筒柄朝下插在腰前青花手巾里、只露黑海绵头，采访本揣在褙子左襟里、只露麻布书脊"

# ───────────────────────────── 镜表字段
# jb=(起幅人占画高, 起幅景别, 落幅人占画高, 落幅景别)  jbcam=(起幅机位标签, 落幅机位标签)
# lt: day | dawn | dawn_lamp（五更航拍，零星油灯）| lamp（正店灯烛夜）| oil（非正店的夜，只有油灯）
# tod: 见 TOD；hands: 林问入画必填；carry: 随身状态串列表
# lines: L(t0, 类型, 中文, 英文, 时长目标, facts, 情绪, 语速, 视线)；类型 "对镜" | "画外"
S: list[dict] = []


def L(t0: float, kind: str, zh: str, en: str, dur: float, facts: str = "", emo: str = "", speed: str = "中",
      gaze: str = "") -> dict:
    return {"t0": t0, "kind": {"对镜": "正常台词", "画外": "内心独白"}[kind], "zh": zh, "en": en, "dur": dur,
            "facts": facts, "emo": emo, "speed": speed, "gaze": gaze}


def fid(x: str) -> str:
    return x if x.startswith("PENDING:") else "kaifeng." + x


def nchars(text: str) -> int:
    return len(re.sub(r"[，。！？…—、：；“”‘’（）()「」《》\s·\-]", "", text))


def nwords(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", text))


def han(text: str) -> int:
    return len(re.findall(r"[一-鿿]", text))


def num(x: float) -> str:
    return ("%d" % x) if float(x).is_integer() else ("%.1f" % x)


def speaks_on_camera(s: dict) -> bool:
    return any(ln["kind"] == "正常台词" for ln in s["lines"])


def has_lin(s: dict) -> bool:
    return "c1" in s["ch"] or "c1m" in s["ch"]


def previz_done(sid: str) -> bool:
    """白模动画渲出来了没有——镜头卡里的 previz 状态由盘上产物定，不手写（CLAUDE.md § State surfaces 1）。"""
    return os.path.exists(os.path.join(ROOT, "shots", sid, sid + "_previz.mp4"))


def tc(sec: int) -> str:
    return "%02d:%02d" % (sec // 60, sec % 60)


def _read(path: str) -> str:
    return io.open(path, encoding="utf-8").read()


# ───────────────────────────── 锁定值抽取（相等比较，不做子串匹配 —— R7 W10）
def card_label(path: str) -> str | None:
    for line in _read(path).split("\n"):
        if line.startswith("| 8 |") and "角色识别标签" in line:
            m = re.search(r"`([^`]+)`", line.split("|")[3])
            return m.group(1) if m else None
    return None


DESC_HEAD = "### shot 角色行锁定串（逐字，生成器闸门比对）"


def card_desc(path: str) -> str | None:
    m = re.search(r"^%s\n(.*?)(?=^#{1,3} |^---$|\Z)" % re.escape(DESC_HEAD), _read(path), flags=re.S | re.M)
    got = re.findall(r"^```\n(.*?)\n```", m.group(1), flags=re.S | re.M) if m else []
    return got[0] if got else None


def card_locks(path: str) -> list[str]:
    text = _read(path)
    m = re.search(r"^## 锁定描述符[^\n]*\n(.*?)(?=^## )", text, flags=re.S | re.M)
    return re.findall(r"^```\n(.*?)\n```", m.group(1), flags=re.S | re.M) if m else []


def card_scene_lock(path: str) -> list[str]:
    out = []
    for line in _read(path).split("\n"):
        if not line.startswith("|") or "一句话锁定" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for i, c in enumerate(cells[:-1]):
            label = c.replace("*", "")
            if label == "一句话锁定" or label.startswith("一句话锁定（"):
                out.append(cells[i + 1])
    return out


# ───────────────────────────── 闸门
def gate_locks() -> None:
    bad = []
    for c, desc in DESC.items():
        if LABEL[c] not in desc:
            bad.append("%s 描述符里没有识别标签原文" % c)
        if c == "c1":
            continue  # 宋装态锁定串本就逐字读自系列卡（load_traveller）
        got = card_label(CHAR_CARD[c])
        if got != LABEL[c]:
            bad.append("%s 识别标签 ≠ 卡第 8 行：%r" % (c, got))
        if c != "c1m" and card_desc(CHAR_CARD[c]) != desc:
            bad.append("%s 描述符 ≠ 卡「%s」围栏（rule 4i ① · R8 W3）" % (c, DESC_HEAD))
    p3 = card_locks(P3_CARD)
    for name, text in (("P3_MIC", P3_MIC), ("P3_BOOK", P3_BOOK), ("P3_EAR", P3_EAR), ("P3_BADGE", P3_BADGE)):
        if text not in p3:
            bad.append("%s ≠ p3 卡任何一条锁定串" % name)
    for key, (text, folder, _) in PROP.items():
        if text not in card_locks("%s/props/%s/%s.md" % (A, folder, folder)):
            bad.append("%s ≠ 卡锁定串" % key)
    for key, lock in BG.items():
        got = card_scene_lock(bg_card(key))
        if len(set(got)) != 1 or got[0] != lock:
            bad.append("%s 一句话锁定 ≠ 场景卡：%r" % (key, got))
        if han(lock) > 30:
            bad.append("%s 一句话锁定超 30 个汉字" % key)
    sg = _read(STYLE_GUIDE)
    fences = re.findall(r"^```\n(.*?)\n```", sg, flags=re.S | re.M)
    ticks = re.findall(r"`([^`\n]+)`", sg)
    for name, text in (("STYLE_BASE", STYLE_BASE), ("NEG_BASE", NEG_BASE), ("NEG_ARCH", NEG_ARCH)):
        if text not in fences:
            bad.append("%s ≠ style_guide.md 围栏块" % name)
    for name, text in (("NEG_NOFIRE", NEG_NOFIRE), ("NEG_LAMP", NEG_LAMP), ("NEG_NOCANDLE", NEG_NOCANDLE),
                       ("NEG_INDOOR", NEG_INDOOR), ("NEG_CROWD", NEG_CROWD), ("NEG_LOCAL", NEG_LOCAL),
                       ("NEG_FALL", NEG_FALL), ("NEG_DRESS", NEG_DRESS)):
        if text not in ticks:
            bad.append("%s ≠ style_guide.md §6 条件块" % name)
    if bad:
        raise SystemExit("锁定串不一致 %d 处（K8 / K20）：\n  " % len(bad) + "\n  ".join(bad))


def _beats(act: str) -> list[tuple[float, float, str]]:
    ms = list(re.finditer(r"(\d+(?:\.\d+)?)–(\d+(?:\.\d+)?)s", act))
    return [(float(m.group(1)), float(m.group(2)), act[m.end():(ms[i + 1].start() if i + 1 < len(ms) else len(act))])
            for i, m in enumerate(ms)]


LOOK = re.compile(r"(?<![不没])(看|对|朝|面向|转向)(着)?镜头")
FACE_HIDDEN = ("微距", "俯拍", "高位", "背影", "远景", "黑场", "只见", "航拍", "手特写", "高处", "空镜")


def gate_speech(s: dict, errs: list[str]) -> None:
    sid = "shot%02d" % s["n"]
    prev_end = -1.0
    for k, ln in enumerate(s["lines"], 1):
        t0, t1 = ln["t0"], ln["t0"] + ln["dur"]
        tag = "%s 第 %d 句（%s–%ss）" % (sid, k, num(t0), num(t1))
        if t0 < prev_end - 0.01:
            errs.append("%s 与上一句时间窗重叠或顺序颠倒" % tag)
        prev_end = t1
        if t1 > s["d"] + 0.01:
            errs.append("%s 越过镜长" % tag)
        if nchars(ln["zh"]) / ln["dur"] > MAX_CPS + 1e-6:
            errs.append("%s 中文 %.2f 字/秒 > %.1f" % (tag, nchars(ln["zh"]) / ln["dur"], MAX_CPS))
        if nwords(ln["en"]) / ln["dur"] > MAX_WPS + 1e-6:
            errs.append("%s 英文 %.2f 词/秒 > %.1f" % (tag, nwords(ln["en"]) / ln["dur"], MAX_WPS))
        if not ln["en"].strip():
            errs.append("%s 缺英文" % tag)
        if not ln["emo"].strip():
            errs.append("%s 缺情绪（rule 12.4-H 配音块必填）" % tag)
        if any(h in ln["zh"] for h in HEDGES) and not EN_HEDGE.search(ln["en"]):
            errs.append("%s 中文有推测口吻、英文没有：%s" % (tag, ln["en"]))
        if ln["kind"] == "正常台词":
            if not has_lin(s):
                errs.append("%s 是对镜台词却没有林问入画" % tag)
                continue
            if s.get("cuts"):
                seg = [c for c in s["cuts"] if c[0] - 0.01 <= t0 and t1 <= c[1] + 0.01]
                if not seg:
                    errs.append("%s 对镜台词跨了镜内切点" % tag)
                elif any(w in seg[0][2] for w in FACE_HIDDEN) and not s.get("face_ok"):
                    errs.append("%s 对镜台词落在看不到脸的一段：%s" % (tag, seg[0][2]))
            mid = (t0 + t1) / 2
            beat = [b for b in _beats(s["act"]) if b[0] - 0.01 <= mid <= b[1] + 0.01]
            if not beat or not LOOK.search(beat[0][2]):
                errs.append("%s 对镜台词那一拍的 `动作:` 没写看镜头" % tag)
        elif has_lin(s) and not ln["gaze"]:
            errs.append("%s 画外台词没写视线落点" % tag)


def gate_shape() -> None:
    ns = [s["n"] for s in S]
    if ns != list(range(1, len(S) + 1)):
        raise SystemExit("镜号不连续：%s" % ns)
    bad = [(s["n"], s["d"]) for s in S if not (MIN_D <= s["d"] <= MAX_D)]
    if bad:
        raise SystemExit("时长越界（%ds–%ds）：%s" % (MIN_D, MAX_D, bad))
    total = sum(s["d"] for s in S)
    if not (TOTAL_LO <= total <= TOTAL_HI):
        raise SystemExit("片长 %ds 越界（%d–%ds）" % (total, TOTAL_LO, TOTAL_HI))
    errs: list[str] = []
    last_tod = 0
    for s in S:
        sid = "shot%02d" % s["n"]
        tts = sum(ln["dur"] for ln in s["lines"])
        if tts > s["d"]:
            errs.append("%s TTS 时长目标之和 %.1fs > 镜长 %ds" % (sid, tts, s["d"]))
        rate = sum(nchars(ln["zh"]) for ln in s["lines"]) / s["d"]
        if rate > MAX_CPS:
            errs.append("%s 语速 %.2f 字/秒 > %.1f" % (sid, rate, MAX_CPS))
        gate_speech(s, errs)
        if "c1m" in s["ch"] and s["n"] > 8 and s["bg"] != "bg9_今日州桥遗址":
            errs.append("%s 换装之后又出现现代装" % sid)
        if has_lin(s) and not s.get("hands"):
            errs.append("%s 林问入画却没写 `hands`" % sid)
        if not any(w in s["light"] for w in TOD[s["tod"]]):
            errs.append("%s `光线:` 没写时辰词 %s" % (sid, "/".join(TOD[s["tod"]])))
        if not s.get("optional"):
            if s["tod"] < last_tod:
                errs.append("%s 时辰倒退（tod %d < %d）" % (sid, s["tod"], last_tod))
            last_tod = s["tod"]
        carry = " ".join(s.get("carry", [])) + " ".join(s.get("sstate", []))
        if "c1" in s["ch"] and 9 <= s["n"] <= 23 and WILLOW_NONE not in carry:
            errs.append("%s 宋装且尚未插柳，缺反向声明" % sid)
        if "c1" in s["ch"] and 25 <= s["n"] <= 32 and WILLOW not in carry:
            errs.append("%s 柳枝已插上，走位缺柳枝状态串" % sid)
        if s["n"] == 24 and WILLOW not in carry:
            errs.append("shot24 插柳镜的镜内状态缺柳枝状态串")
        if s["n"] in (33, 34) and KNOT not in carry:
            errs.append("%s 缺绳结状态串" % sid)
        if s["n"] == 34 and WILLOW_TABLE not in carry:
            errs.append("shot34 缺桌上柳枝状态串")
        if (s["n"] == 7 and BUNDLE_NONE not in carry) or (s["n"] == 8 and BUNDLE_LOOSE not in carry):
            errs.append("%s 缺布包未拴的反向声明" % sid)
        if s["n"] == 14 and DONKEY_BACK not in carry:
            errs.append("shot14 缺还驴状态串")
    texts = [ln for s in S for ln in s["lines"]]
    s02 = S[1]["lines"]
    if not s02 or s02[-1]["zh"] != OPENING or s02[-1]["en"] != EN_OPENING or s02[-1]["kind"] != "内心独白":
        errs.append("S02 末句必须是画外签名开场（中英逐字）")
    s03 = S[2]["lines"]
    if not s03 or not s03[0]["zh"].startswith(SELF_INTRO) or not s03[0]["en"].startswith(EN_SELF_INTRO):
        errs.append("S03 首句必须以自报家门开头（中英逐字）")
    s34 = S[33]["lines"]
    if [(ln["zh"], ln["en"]) for ln in s34[-2:]] != list(zip(CLOSER, EN_CLOSER)):
        errs.append("S34 最后两句必须是签名收尾两句（中英逐字）")
    if not any(ln["zh"] == QUESTION and ln["en"] == EN_QUESTION for ln in s34):
        errs.append("S34 缺置顶评论问题（中英逐字）")
    if sum(1 for ln in texts if ln["zh"] == OPENING) != 1:
        errs.append("签名开场必须只出现一次")
    k = sum(1 for ln in texts if FIXED in ln["zh"])
    if not (3 <= k <= 5) or any(FIXED in ln["zh"] and (ln["zh"] != FIXED or ln["en"] != EN_FIXED) for ln in texts):
        errs.append("固定句「%s」出现 %d 次（要求 3–5 次、单独成句、英文逐字）" % (FIXED, k))
    q = sum(ln["zh"].count("「") for ln in texts)
    if q < 6:
        errs.append("原文引语只有 %d 段（要求 ≥ 6）" % q)
    if errs:
        raise SystemExit("镜表不合格 %d 处：\n  " % len(errs) + "\n  ".join(errs))


def gate_facts(facts: dict) -> list[str]:
    errs, pending, myth_shots = [], [], []
    for s in S:
        ids = [fid(x) for x in s["facts"]]
        if not ids:
            errs.append("shot%02d 无 fact" % s["n"])
        tags = []
        for f in ids:
            if f.startswith("PENDING:"):
                pending.append("shot%02d %s" % (s["n"], f))
                continue
            rec = facts.get(f)
            if rec is None:
                errs.append("shot%02d 引用了不存在的 fact %s" % (s["n"], f))
                continue
            if rec.get("verified_by") == "ai_draft":
                errs.append("shot%02d 引用了 ai_draft 事实 %s（不得进 prompt）" % (s["n"], f))
            tags.append(rec.get("tag"))
            if rec.get("tag") == "❌":
                myth_shots.append((s["n"], f))
                if s["unit"] != "纠错":
                    errs.append("shot%02d 在非纠错单元引用了 ❌ 事实 %s" % (s["n"], f))
        for ln in s["lines"]:
            for x in ln["facts"].split():
                if x not in s["facts"]:
                    errs.append("shot%02d 台词回指的 %s 不在本镜 facts 里" % (s["n"], x))
        if "⚠️" in tags and not any(h in ln["zh"] for ln in s["lines"] for h in HEDGES):
            errs.append("shot%02d 用了 ⚠️ 事实却没有推测口播" % s["n"])
        s["tag_max"] = "❌" if "❌" in tags else ("⚠️" if "⚠️" in tags else ("✅" if tags else "待定"))
    if myth_shots != [(9, "kaifeng.myth.001")]:
        errs.append("❌ 必须恰好一次、在 S09 的 myth.001：实际 %s" % myth_shots)
    if pending and not ALLOW_PENDING:
        errs.append("仍有 %d 个 PENDING: 占位：%s" % (len(pending), "、".join(pending)))
    if errs:
        raise SystemExit("史实闸门不合格 %d 处（K34）：\n  " % len(errs) + "\n  ".join(errs))
    return pending


def seam_audit() -> list[shot_seam.Seam]:
    pairs = {(s["handoff_from"], s["n"]) for s in S if s.get("handoff_from")}
    if pairs != {(1, 2)}:
        raise SystemExit("承接对只允许 S01→S02：实际 %s" % sorted(pairs))
    out, bad = [], []
    for a, b in zip(S, S[1:]):
        if b.get("handoff_from") == a["n"]:
            if a["jbcam"][1] != b["jbcam"][0] or tuple(a["jb"][2:4]) != tuple(b["jb"][0:2]):
                raise SystemExit("承接对 shot%02d→shot%02d 两端机位标签或景别档不一致（R3-24）" % (a["n"], b["n"]))
            r = a["jb"][2] / b["jb"][0]
            out.append(shot_seam.Seam(a["n"], b["n"], a["jb"][2], a["jb"][3], b["jb"][0], b["jb"][1],
                                      a["jbcam"][1], b["jbcam"][0], r, "🔗 承接（handoff_from 豁免跳档）", True, None))
            continue
        sm = shot_seam.verdict(a, b)
        out.append(sm)
        if not sm.ok:
            bad.append(sm)
    core = [s for s in S if not s.get("optional")]
    for a, b in zip(core, core[1:]):
        if not b.get("handoff_from") and not shot_seam.verdict(a, b).ok:
            bad.append(shot_seam.verdict(a, b))
    if bad:
        raise SystemExit("镜间切口不合格 %d 处：" % len(bad) + "；".join(
            "shot%02d→shot%02d %.2f %s" % (x.prev_n, x.next_n, x.ratio, x.verdict) for x in bad))
    return out


# ───────────────────────────── 拼装
def negatives(s: dict) -> str:
    drop = set(s.get("neg_drop", []))
    add: list[str] = []
    if speaks_on_camera(s):
        drop |= {"看镜头（受访者对镜答与记者出镜口播除外）", "对口型"}  # R7 F02 · style_guide §6 注
        if sum(1 for ln in s["lines"] if ln["kind"] == "正常台词") >= 2:
            add.append(NEG_SUB_HI)
    if "c1m" in s["ch"]:
        drop |= MODERN_DROP
        add.append("路人穿现代服饰")
    if s.get("xuande"):
        drop |= {"琉璃瓦", "红柱金匾"}
        add += [NEG_XUANDE, NEG_BGX["bg12_宣德楼"]]
    if "p2" in s["pr"]:
        drop.add("元宝")  # 不压 p2 钱文「熙宁元宝」（R7 W17）
        add.append("金银元宝")
    out = [NEG_BASE, NEG_ARCH, NEG_TOUR] + add
    if s["lt"] in ("day", "dawn"):
        out += [NEG_NOFIRE, NEG_SKY]
    elif s["lt"] == "dawn_lamp":
        out += [NEG_LAMP, NEG_SKY]
        drop.add("提亮的黑位")
    else:
        out += [NEG_LAMP, NEG_NIGHT, NEG_NIGHT_MODERN, NEG_SKY_NIGHT]
        if s["lt"] == "oil":
            out.append(NEG_NOCANDLE)
    for flag, block in (("indoor", NEG_INDOOR), ("crowd", NEG_CROWD), ("local", NEG_LOCAL), ("dress", NEG_DRESS)):
        if s.get(flag):
            out.append(block)
    if s.get("fall"):
        out.append(NEG_FALL)
    if s.get("aerial"):
        out.append(NEG_AERIAL)
    if s["bg"] in NEG_BGX and not s.get("xuande"):
        out.append(NEG_BGX[s["bg"]])
    if s.get("neg_add"):
        out.append(s["neg_add"])
    if not s["lines"]:
        out.append(NEG_SILENT)
    else:
        out.append(NEG_VOICE + ", 说" + ("英文" if TLANG == "zh" else "中文"))
    seen, toks = set(), []
    for tok in ", ".join(out).split(", "):
        if tok not in drop and tok not in seen:
            seen.add(tok)
            toks.append(tok)
    return ", ".join(toks)


def scene_items(s: dict) -> list[tuple[str, str, str]]:
    """(路由键, 主体目录, 说明)。"""
    items = [(s["v"], s["bg"], s["bg"])]
    for v2, note in s.get("vx", []):
        items.append((v2, BG_ID[v2.split("-")[0]], note))
    return items


def refs_for(s: dict, sid: str) -> list[str]:
    items = []
    if s.get("handoff_from"):
        items.append("本镜首帧(上一镜末帧)")
    items.append("%s_previz.mp4(白模动画·运动与几何参考，不取长相)" % sid)
    for v, bg, note in scene_items(s):
        items.append("%s(场景主体·%s)" % (v, note))
    lin = [c for c in s["ch"] if c in ("c1", "c1m")]
    for c in s["ch"]:
        items.append(TOKEN[c])
        if s["lines"] and lin and c == lin[-1]:
            items.append("林问声音(%s-2 声样·voice_id %s)" % (KEY, VOICE_MAIN))  # K29：紧跟她最后一个视觉 token（R8 B2）
    if has_lin(s):
        items.append("p3-1(三件不变物锚点)")
    for p in s["pr"]:
        items.append(PROP[p][2])
    if s["lines"] and not has_lin(s):
        items.append("林问声音(%s-2 声样·voice_id %s)" % (KEY, VOICE_MAIN))
    return items


TAG_ON = "正常台词·口型对林问"
TAG_OS = "内心独白·画外，嘴唇不动、不对口型"
TAG_OS_OFF = "内心独白·台词系林问画外，画面里任何人都嘴唇不动、不对口型"
LINE_RE = re.compile(r"^· 林问〔(%s|%s|%s)〕：[^〔〕]+$" % tuple(re.escape(x) for x in (TAG_ON, TAG_OS, TAG_OS_OFF)))


def win_of(ln: dict) -> str:
    return "%s–%ss" % (num(ln["t0"]), num(ln["t0"] + ln["dur"]))


def line_tag(s: dict, ln: dict) -> str:
    """K21 / rule 12.4 v2：〔〕里只放类型与口型指令；时间窗与视线在 `走位:` 的时间表里（R8 B1）。"""
    if ln["kind"] == "正常台词":
        return TAG_ON
    return TAG_OS if has_lin(s) else TAG_OS_OFF


def gaze_plan(s: dict) -> str:
    if not (has_lin(s) and s["lines"]):
        return ""
    return "林问开口与视线时间表：" + "；".join(
        ("%s 正脸看镜头开口" % win_of(ln)) if ln["kind"] == "正常台词"
        else ("%s 视线落在%s、嘴唇不动" % (win_of(ln), ln["gaze"])) for ln in s["lines"])


def gate_line_tags(s: dict, pos: str) -> None:
    rows = [x for x in pos.split(NL) if x.startswith("· ")]
    bad = [x for x in rows if not LINE_RE.match(x)]
    got = [LINE_RE.match(x).group(1) for x in rows if LINE_RE.match(x)]
    want = [line_tag(s, ln) for ln in s["lines"]]
    if bad or got != want:
        raise SystemExit("shot%02d `台词:` 行〔〕不合格（K21：只许类型与口型指令三种写法）：%s" % (s["n"], bad or list(zip(got, want))))


def emit(s: dict, i: int, start: int, seams: list, facts: dict) -> tuple[str, str, int, float]:
    sid = "shot%02d" % s["n"]
    lines = s["lines"]
    n_chars = sum(nchars(ln["zh"]) for ln in lines)
    rate = n_chars / s["d"]

    usage = ["白模动画决定运动与几何：机位路径、走位、人物到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。",
             "场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰拍的，光的方向、天色与明暗一律不从它取，以本镜 `光线:` 为准。"]
    if s.get("vx"):
        usage.append("本镜有 %d 张场景参考，按 `分镜:` / `镜头:` 的时间段各自生效。" % (1 + len(s["vx"])))
    if s.get("handoff_from"):
        usage.append("首帧就是本镜第 0 帧，镜头运动与光自该帧那一刻续起，不重新开始。")
    if has_lin(s):
        usage.append("林问的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。")
    if any(c in s["ch"] for c in ("c21", "c22", "c23")):
        usage.append("沉默面孔以其 entity 为唯一脸源，不开口、不看镜头、不美颜。")
    if s["pr"] or has_lin(s):
        usage.append("物件锚点锁形制，入画时按 `道具:` 行照搬。")
    if s.get("cuts"):
        usage.append("本镜内部允许切镜（`分镜:` 行写死每段起止秒与切法）：标「切」的段之间是干净的硬切、无任何转场特效；"
                     + ("切镜可以省略中间过程（换衣、走路、进门上楼），但光与环境音连续。" if s.get("cuts_elide")
                        else "切镜不改变时间线，环境音与光连续。"))
    if lines:
        usage.append("台词由视频直接出声：林问的声音照 `声音:` 行与「林问声音」参考（%s-2 建立视频前 2 秒声样）生成，台词说%s；对镜的句子对口型，画外的句子嘴唇不动、声音照样出；画面里不出现任何文字。" % (KEY, LANG_ZH[TLANG]))
    if speaks_on_camera(s):
        usage.append("画面里只有林问会开口，而且只在 `走位:`「林问开口与视线时间表」里标了「正脸看镜头开口」的时间窗里开口；其余所有人不说话、不对口型、不看镜头，人群只是听不清字句的环境声。")
    elif has_lin(s):
        usage.append("本镜林问不开口（台词全是画外，她的视线按 `走位:`「林问开口与视线时间表」走）；其余所有人也不说话、不对口型、不看镜头，人群只是听不清字句的环境声。")
    else:
        usage.append("画面里没有任何人开口、没有人看镜头，人群只是听不清字句的环境声。")

    p = [sid, "参考: " + "，".join("`%s=>@`" % it for it in refs_for(s, sid))]
    if s.get("handoff_from"):
        p.append("首帧: 画面以首帧为起始、自首帧那一刻续起自然顺接展开、起始不重新缩放/不重新定位/不重摆姿")
    p += ["参考用法: " + "".join(usage),
          "情节: `%s`" % s["plot"],
          "场景: `%s — %s`" % (s["bg"], BG[s["bg"]])]
    if s["ch"]:
        p.append("角色: `%s`" % "；".join(DESC[c] for c in s["ch"]))
        bind = "；".join("%s＝参考 `%s`·%s" % (NAME[c], TOKEN[c], LABEL[c]) for c in s["ch"])
        if s.get("bind"):
            bind += "；" + s["bind"]
        p.append("角色识别 / 参考图: `%s；同一个人在画面里只出现一次`" % bind)
    else:
        p += ["角色: 无", "角色识别 / 参考图: 无"]
    props = []
    if has_lin(s):
        props += [P3_MIC, P3_BOOK, P3_BADGE] + ([P3_EAR] if s.get("ear") else [])
    props += [PROP[k][0] for k in s["pr"]]
    if props:
        p.append("道具: `%s`" % "；".join(props))
    if s.get("cuts"):
        p.append("分镜: `%s`" % "；".join("%d–%ds %s ｜ %s" % c for c in s["cuts"]))
    if s.get("sstate"):
        p.append("镜内状态: `以下是每一段画面里东西的样子，只能前进、绝不倒退，后一段必须包含前一段已完成的全部：%s`"
                 % "；".join("%d–%ds %s" % (c[0], c[1], st) for c, st in zip(s["cuts"], s["sstate"])))
    block = s["block"]
    if s.get("carry"):
        block = "；".join(s["carry"]) + "；" + block
    if has_lin(s):
        block = "本镜手里：%s；%s" % (s["hands"], block)
    plan = gaze_plan(s)
    if plan:
        block = "%s；%s" % (block, plan)
    fall = ("。" + GRAVITY % "、".join(s["fall"])) if s.get("fall") else ""
    p += ["镜头: `%s`" % s["cam"], "走位: `%s`" % block, "动作: `%s`" % (s["act"] + fall)]
    if lines:
        p.append("台词:")
        for ln in lines:
            p.append("· 林问〔%s〕：%s" % (line_tag(s, ln), ln["zh"] if TLANG == "zh" else ln["en"]))
        p.append("声音: `%s`；本镜人声由视频直接生成，全片只有林问一个人声；当地人和人群没有可辨字句" % VOICE_LOCK)
    else:
        p.append("台词: 无")
    tail = s.get("day_tail", DAY_TAIL) if s["lt"] in ("day", "dawn", "dawn_lamp") else ""
    sky = SKY.get(s["lt"], SKY_NIGHT) + (SKY_AERIAL if s.get("aerial") else "")
    p += ["光线: `%s`" % (s["light"] + tail + sky), "节奏: " + s["pace"], "渲染样式: " + STYLE_BASE, "比例: 16:9",
          "时长: %d秒" % s["d"]]
    pos = NL.join(p)
    gate_line_tags(s, pos)
    pos = personalize(pos)

    end = start + s["d"]
    y = ["---", "shot_id: " + sid, "segment: " + s["seg"], "section: " + s["sec"],
         "timecode: %s–%s" % (tc(start), tc(end)), "duration: %ds" % s["d"], "time_of_day: " + TOD[s["tod"]][0],
         "scene: " + s["bg"], "view: " + s["v"], "characters: [" + ", ".join({"c1": KEY, "c1m": KEY + "m"}.get(c, c) for c in s["ch"]) + "]",
         "props: [" + ", ".join((["p3"] if has_lin(s) else []) + s["pr"]) + "]",
         "unit: " + s["unit"], "dialogue: " + ("yes" if lines else "none"),
         "previz_tier: " + s["tier"], "optional: " + ("yes" if s.get("optional") else "no"),
         "status: 已出prompt", "---"]
    if i == 0:
        seam = "本镜是**首镜**，无上一镜。"
    elif s.get("handoff_from"):
        sm = seams[i - 1]
        seam = ("上一镜 shot%02d 落幅 **%s %.2f**（机位 `%s`）→ 本镜起幅 **%s %.2f**（机位 `%s`），比值 %.2f — "
                "**承接对，豁免跳档**：本镜首帧就是上一镜成片末帧，接缝要看不出来（jingbie §2.0.3：承接与跳档互斥）。"
                % (sm.prev_n, sm.out_name, sm.out_v, sm.out_cam, sm.in_name, sm.in_v, sm.in_cam, sm.ratio))
    else:
        seam = seams[i - 1].context()
    fact_line = "、".join("`%s`%s" % (f, "" if f.startswith("PENDING:") else "（%s）" % facts[f].get("tag"))
                         for f in (fid(x) for x in s["facts"]))
    words = sum(nwords(ln["en"]) for ln in lines)
    ctx = ["", "# %s · %s" % (sid, s["title"]), "", "## Shot context",
           "- **Summary**：" + s["summary"],
           "- **Characters**：" + ("；".join(NAME[c] for c in s["ch"]) if s["ch"] else "无具名人物（空镜或远景剪影）"),
           "- **Scene**：`%s` — %s（视图 `%s`）" % (s["bg"], BG[s["bg"]], "` + `".join(v for v, _, _ in scene_items(s))),
           "- **Duration**：%ds（%s–%s，%s）｜ 中文台词 %d 字 ≈ %.2f 字/秒 ｜ 英文 %d 词 ≈ %.2f 词/秒" % (
               s["d"], tc(start), tc(end), TOD[s["tod"]][0], n_chars, rate, words, words / s["d"]),
           "- 衔接: " + ("承接 shot%02d 末帧（首帧＝上一镜末帧）" % s["handoff_from"] if s.get("handoff_from") else "硬切（独立首帧）")]
    if s.get("tail_lock"):
        ctx.append("- 尾帧锁定: " + s["tail_lock"])
    ctx += ["- 景别档: %s%.2f → %s%.2f（机位 `%s` → `%s`）。**与前一镜的切口**：%s" % (
                s["jb"][1], s["jb"][0], s["jb"][3], s["jb"][2], s["jbcam"][0], s["jbcam"][1], seam),
            "- 史实: %s ｜ 本镜最高不确定度 `%s` ｜ 栏目 `unit: %s`" % (fact_line, s["tag_max"], s["unit"]),
            "- previz: `previz 档: %s` · 白模动画 `5_6_分镜与prompt/shots/%s/%s_previz.mp4`（%s）；关键帧 `t` 须与 `动作:` 时间轴逐拍对齐（rule 4h）" % (
                s["tier"], sid, sid, "已渲" if previz_done(sid) else "待渲"),
            "- **空间核验**：" + s["spatial"],
            "- **首末帧反差**：" + s["contrast"],
            "- **决定性瞬间**：" + s["moment"]]
    if s.get("cuts"):
        ctx.append("- **镜内分段**（%d 段）：" % len(s["cuts"]) + " → ".join("**%d–%ds** %s〔%s〕" % c for c in s["cuts"]))
    if s.get("post"):
        ctx.append("- **后期层**（不进 prompt）：" + s["post"])
    if s.get("judge"):
        ctx.append("- **判断**：" + s["judge"])
    if s.get("optional"):
        ctx.append("- **可选实验**：本镜进不进成片，出片后看 feedback 再定；不进时 shot35 的航拍悬停就是全片最后一帧。")
    ctx.append("- **Reference uploads**：")
    if s.get("handoff_from"):
        ctx.append("  - [ ] 上一镜末帧 `shot%02d_lastframe.png`（从 shot%02d 成片截取最后一帧，进本镜首帧槽）" % (s["handoff_from"], s["handoff_from"]))
    ctx.append("  - [%s] `5_6_分镜与prompt/shots/%s/%s_previz.mp4`（白模动画，%s）" % (
        "x" if previz_done(sid) else " ", sid, sid, "已渲" if previz_done(sid) else "待渲"))
    for v, bg, note in scene_items(s):
        ctx.append("  - [ ] `%s/scenes/bianjing/%s/%s.png`（场景主体·%s）" % (ASSETS, bg, v, note))
    for c in s["ch"]:
        ctx.append("  - [ ] " + UPLOAD[c])
    if has_lin(s):
        ctx.append("  - [ ] `%s/props/p3_三件不变物/p3-1.png`（三件不变物）" % ASSETS)
    for k in s["pr"]:
        ctx.append("  - [ ] `%s/props/%s/%s-1.png`" % (ASSETS, PROP[k][1], k))
    if lines:
        ctx.append("  - [ ] 林问声音：`_series/characters/%s/%s-2.mp4` 前 2 秒声样（`views/_trim2s.mp4` / `_audio.mp3`）· 视频原声说%s（voice_id `%s`），译配轨 `%s`（casting.md）" % (
            TFOLDER, KEY, LANG_ZH[TLANG], VOICE_MAIN, VOICE_DUB))

    body = (NL.join(y) + NL + NL.join(ctx) + NL + NL + "## 视频 prompt" + NL + FENCE + "text" + NL + pos + NL + FENCE + NL + NL +
            "> **反向提示词**（粘进平台负向框，**不要并进正向 prompt**）：" + NL + FENCE + "text" + NL + negatives(s) + NL + FENCE + NL)
    if lines:
        zh, en = [], []
        for k, ln in enumerate(lines, 1):
            win = "%s–%ss" % (num(ln["t0"]), num(ln["t0"] + ln["dur"]))
            typ = "对镜说话，口型对林问" if ln["kind"] == "正常台词" else "画外，嘴唇不动"
            zh.append(NL.join([
                "%s · 台词配音 · 中文 · 第 %d 句" % (sid, k),
                "角色: 林问 ｜ 音色(锁定·全站复用): zh `%s`（%s）" % (VOICE_ZH, TONE_ZH),
                "情绪: %s ｜ 语速: %s" % (ln["emo"], ln["speed"]),
                "类型: %s（%s）｜ 时间窗: %s" % (ln["kind"], typ, win),
                "台词: %s" % ln["zh"],
                "时长目标: %.1fs" % ln["dur"]]))
            en.append(NL.join([
                "%s · 台词配音 · 英文 · 第 %d 句" % (sid, k),
                "角色: 林问 ｜ 音色(锁定·全站复用): en `%s`（%s）" % (VOICE_EN, TONE_EN),
                "情绪: %s ｜ 语速: %s" % (ln["emo"], ln["speed"]),
                "类型: %s（%s）｜ 时间窗: %s（与中文第 %d 句同窗）" % (ln["kind"], typ, win, k),
                "台词: %s" % ln["en"],
                "时长目标: %.1fs ｜ %d 词" % (ln["dur"], nwords(ln["en"]))]))
        role = {"zh": "视频原声补录（只在成片人声漂移时用）", "en": "整轨译配（去掉视频原声、保留环境音后 mux）"}
        if TLANG == "en":
            role = {"zh": role["en"], "en": role["zh"]}
        body += (NL + "## 台词配音 prompt" + NL +
                 "> **视频已直接出声**（系列 follow-up 012 · `specs/ai_video/sk1/divergence.md` #20）：本节不是默认产物。中文块＝%s；英文块＝%s。" % (role["zh"], role["en"]) + NL + NL +
                 FENCE + "text" + NL + (NL + "---" + NL).join(zh) + NL + FENCE + NL + NL +
                 "> **英文轨**（%s；逐句与中文同一时间窗，≤ 2.8 词/秒）：" % role["en"] + NL +
                 FENCE + "text" + NL + (NL + "---" + NL).join(en) + NL + FENCE + NL)
    if re.search(r"#[0-9A-Fa-f]{6}\b", body):
        raise SystemExit("%s 出现 hex 色值（K9）" % sid)
    return personalize(body), pos, n_chars, rate


def script_lines(s: dict) -> str:
    if not s["lines"]:
        return "- 台词: 无"
    out = ["- 台词:"]
    for ln in s["lines"]:
        out.append("  - [%s %s–%ss] 林问: \"%s\"%s" % (
            "对白" if ln["kind"] == "正常台词" else "OS", num(ln["t0"]), num(ln["t0"] + ln["dur"]), ln["zh"],
            "（%s）" % " ".join("`%s`" % x for x in ln["facts"].split()) if ln["facts"] else ""))
        out.append("    - en: \"%s\"" % ln["en"])
    return NL.join(out)


def sync_script() -> None:
    """script.md 每镜「时长」「台词」两段与镜表逐字一致（三处同步：shot / dialogue / script）。"""
    path = os.path.join(DRAMA, "4_剧本", "script.md")
    text = _read(path)
    for s in S:
        m = re.search(r"(### 镜 %02d · [^\n]*\n)(.*?)(?=\n### 镜 |\n---\n## |\Z)" % s["n"], text, flags=re.S)
        if not m:
            raise SystemExit("script.md 缺镜块：### 镜 %02d" % s["n"])
        block = m.group(2)
        new, k1 = re.subn(r"- 时长: \d+s", "- 时长: %ds" % s["d"], block, count=1)
        new, k2 = re.subn(r"- 台词:.*?(?=\n- 情绪氛围)", lambda _: personalize(script_lines(s)), new, count=1, flags=re.S)
        if not (k1 and k2):
            raise SystemExit("script.md 镜 %02d 缺「- 时长:」或「- 台词: … - 情绪氛围」结构" % s["n"])
        text = text[:m.start(2)] + new + text[m.end(2):]
    io.open(path, "w", encoding="utf-8", newline=NL).write(text)


def build() -> None:
    facts, probs = facts_registry.load(DRAMA)
    hard = [x for x in probs if x.level == "blocker"]
    if hard:
        raise SystemExit("事实注册表有 blocker：%s" % hard)
    gate_locks()
    gate_shape()
    pending = gate_facts(facts)
    seams = seam_audit()

    os.makedirs(os.path.join(ROOT, "shots"), exist_ok=True)
    emitted, rows, oversize, stats = {}, [], [], []
    dialogue = ["# sk1 · 纯台词（由 tools/gen_shots_sk1.py 生成，改内容＝改生成器重跑）", "",
                "> 只有林问开口，视频直接出声（说%s）。`OS` ＝ 画外内心独白（嘴不动、声音照出）；其余是对镜说话。当地人零台词。每句下一行是同一时间窗的英文句。" % LANG_ZH[TLANG], ""]
    t = on_cam = off_cam = 0
    for i, s in enumerate(S):
        sid = "shot%02d" % s["n"]
        body, pos, n_chars, rate = emit(s, i, t, seams, facts)
        t += s["d"]
        if len(pos) > MAX_PROMPT:
            oversize.append((sid, len(pos)))
        d = os.path.join(ROOT, "shots", sid)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, sid + ".md"), "w", encoding="utf-8", newline=NL).write(body)
        emitted[sid] = body
        wps = sum(nwords(ln["en"]) for ln in s["lines"]) / s["d"]
        stats.append((sid, rate, len(pos), wps))
        for ln in s["lines"]:
            if ln["kind"] == "正常台词":
                on_cam += nchars(ln["zh"])
            else:
                off_cam += nchars(ln["zh"])
        rows.append("| %s | %ds | %s | %s | %s | `%s` | %s | %s | %s | %.2f | %.2f | %d | %s |" % (
            sid, s["d"], tc(t), TOD[s["tod"]][0], s["sec"], s["bg"].split("_")[0], s["title"], s["unit"],
            "首镜" if i == 0 else ("🔗 承接" if s.get("handoff_from") else "%.2f ✅" % seams[i - 1].ratio),
            rate, wps, len(pos), s["tier"]))
        dialogue.append("## 镜 %02d · %s%s" % (s["n"], s["title"], "（可选实验）" if s.get("optional") else ""))
        for ln in s["lines"]:
            dialogue.append("林问: \"%s\" (%s%s · %s–%ss)" % (ln["zh"], "OS·" if ln["kind"] == "内心独白" else "", ln["emo"],
                                                         num(ln["t0"]), num(ln["t0"] + ln["dur"])))
            dialogue.append("  en: \"%s\"" % ln["en"])
        if not s["lines"]:
            dialogue.append("（无台词·空镜）")
        dialogue.append("")
    if oversize:
        raise SystemExit("正向 prompt 超 %d 字（K10）：%s" % (MAX_PROMPT, oversize))
    logic = shot_logic.gate(emitted, legacy=set())
    light = prompt_light.gate(emitted, legacy=set())

    total = t
    opt = sum(s["d"] for s in S if s.get("optional"))
    head = [
        "# 镜头清单 · 时空旅行 · 汴京清明一日（sk1）",
        "",
        "> **16:9 · %ds · %d shots · 游览 vlog · 单站成片** · 单镜 15–30 s · 镜内允许切镜。" % (total, len(S)),
        "> **只有林问开口**（对镜说话 %d 字 ≈ %.0f%% ／ 画外 %d 字 ≈ %.0f%%）；当地人零台词、不看镜头，群声没有可辨字句。视频原声说%s（`声音:` 行 + `%s-2` 声样），另一语种走译配（`%s`）。" % (
            on_cam, 100.0 * on_cam / (on_cam + off_cam), off_cam, 100.0 * off_cam / (on_cam + off_cam), LANG_ZH[TLANG], KEY, VOICE_DUB),
        "> **切口**：%d 个接缝里，唯一的承接对是 shot01→shot02（航拍连续，shot01 尾帧锁定）；其余全部硬切 + 景别跳档（≥2.0 或 ≤0.5 且两端机位标签不同）。" % (len(S) - 1),
        "> **时辰**：卯时开场 → 次日五更航拍收束，逐镜只进不退（`tod` 闸门）。",
        "> **previz**：每镜一条白模动画（`shotNN_previz.mp4`，待渲）进 `参考:`；S 档＝shot01 / 02 / 04 / 26 / 35，其余 A 档。",
        "> **史实**：每镜 `史实:` 回指 `0_research/parts`；❌ 只在 shot09（纠错）；⚠️ 镜口播「史书没写 / 推测 / 推算」。",
        "> shot36「今天的州桥遗址」是**可选实验**。本文件由 `tools/gen_shots_sk1.py` 生成，**改内容＝改生成器重跑**。",
        "",
        "**时长合计：%ds** ∈ [%d, %d] ✔（不含可选 shot36：%ds）" % (total, TOTAL_LO, TOTAL_HI, total - opt),
        "",
        "| # | 时长 | 累计 | 时辰 | 段 | 主体 | 内容 | 栏目 | 与上一镜 | 字/秒 | 词/秒 | prompt 字数 | previz |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    tail = ["", "---", "", "## 史实占位", ""] + (["- " + x for x in pending] if pending else ["- 无"])
    io.open(os.path.join(ROOT, "shotlist.md"), "w", encoding="utf-8", newline=NL).write(
        personalize(NL.join(head + rows + shot_seam.table(seams, "tools/gen_shots_sk1.py") + tail)) + NL)
    io.open(os.path.join(ROOT, "all_shot_prompts.md"), "w", encoding="utf-8", newline=NL).write(
        "# sk1 · 全部视频 prompt 与台词配音 prompt（复制用；由 tools/gen_shots_sk1.py 生成）" + NL + NL +
        NL.join("## %s" % sid + NL + emitted[sid][emitted[sid].index("## 视频 prompt"):] for sid in sorted(emitted)) + NL)
    io.open(os.path.join(DRAMA, "4_剧本", "dialogue.md"), "w", encoding="utf-8", newline=NL).write(personalize(NL.join(dialogue)) + NL)
    sync_script()

    rates, lens, wpss = [x[1] for x in stats], [x[2] for x in stats], [x[3] for x in stats]
    spk = [x for x in stats if x[1] > 0]
    print("shots: %d  total: %ds (core %ds)  prompt range: %d–%d  cps range: %.2f–%.2f  wps range: %.2f–%.2f  on-camera: %.0f%%" % (
        len(S), total, total - opt, min(lens), max(lens), min(x[1] for x in spk), max(rates),
        min(x[3] for x in spk), max(wpss), 100.0 * on_cam / (on_cam + off_cam)))
    for sid, r, n, w in stats:
        print("  %s  %.2f 字/秒  %.2f 词/秒  prompt %d" % (sid, r, w, n))
    for sm in seams:
        print("  shot%02d->shot%02d  %.2f  %s  (%s -> %s)" % (sm.prev_n, sm.next_n, sm.ratio, sm.verdict, sm.out_cam, sm.in_cam))
    for x in pending:
        print("  ⚠ PENDING " + x)
    for x in logic + light:
        print("  ⚠ %s [%s] %s" % (x.shot, x.code, x.detail[:120]))


# ═══════════════════════════════════════ 镜表
S += [
 dict(n=1, seg="序", sec="航拍长镜", d=30, bg="bg0_汴京全城", v="bg0-2", vx=[("bg1-1", "12–16s 掠过虹桥")], lt="day", tod=1, tier="S",
      ch=[], pr=[], unit="航拍", crowd=True, local=True, fall=("桅杆",), aerial=True,
      neg_add="明清青砖城墙, 一圈青砖城墙, 正南正北对齐的方格城市",
      facts=["route.004", "bridge.001", "boat.003", "route.002", "route.003", "city.033", "city.035"],
      jb=(0.02, "远景", 0.02, "远景"), jbcam=("汴河水面低空航拍", "汴河上空一百五十米悬停远眺东水门"),
      tail_lock=("本镜是 shot02 的交接源。按格式契约 K26 ④ 首次生成豁免：第一次出片不挂 `本镜末帧=>@` 与 `末帧:`（末帧此时还不存在）。"
                 "**重生成**时把已存的 `shot01_lastframe.png` 上传进模型的尾帧槽，并在 `参考:` 行末尾追加 `本镜末帧=>@`、"
                 "其下加一行 `末帧: 画面以末帧为结束、收束至末帧`，保证 shot02 的首帧参考不失效。末 3 秒镜头悬停，只剩水面反光与柳梢微动，接缝落在静定 beat 上（shouweizhen §3.3）"),
      title="【航拍】汴河低飞 · 虹桥放桅",
      summary="**全片第一个画面，一条航拍式连续长镜的前半段。** 卯时贴着汴河水面自东向西飞，离桥一个船身远的纲船放倒桅杆，镜头从虹桥桥面上方掠过，过桥后边飞边拔高到约一百五十米，末 3 秒悬停在汴河上空，远望约三公里外雾里显形的东水门，交给 shot02 接着飞。无台词。",
      plot="宣和二年清明日卯时，太阳刚离地平线一掌高，镜头像一只鸟贴着碧绿的汴河水面自东向西飞：两岸新绿的垂柳、泊着的平底纲船一一向后掠过；前方出现一座没有桥柱的朱漆木拱桥，离桥还有一个船身远的一条纲船上，水手拽着绳、抱住桅杆根部把桅杆放倒；镜头从桥面上方擦过，过桥后沿河继续西飞、越飞越高，穿出贴水的晨雾，远处外城东墙与东水门的夯土城台从雾后显出来，镜头最后悬停在汴河上空远望东水门",
      cam="一个连续运镜、不切，24mm，全景深：0–12s 离水面约八米、镜头平视，自东向西沿汴河越飞越快地冲向虹桥，像贴水低飞的鸟；12–16s 抬高到约二十米，从虹桥桥面上方掠过，镜头略俯约十度看桥下刚放平桅杆的船；16–27s 过桥后边沿河西飞边拔高到约一百五十米，镜头回到平视略俯，远处东水门城台与外城东墙在画面深处露出来；27–30s 减速、悬停，镜头朝西北远望约三公里外的东水门。飞行像一只快鸟、画面平稳不拖影。画面里没有任何飞行器，也没有飞行器的影子",
      block="画面里没有具名人物；桥上人流为逆光剪影、不可辨面孔；纲船上两名水手在船中抱桅杆、一名在船尾撑篙；两岸远处行人为剪影；可辨主体不超过八个，所有人都不看镜头",
      act="0–8s 水面与两岸垂柳向后流过，一条泊岸的纲船从画左掠过；8–12s 前方虹桥越来越大，离桥还有一个船身远的纲船上，两名水手拽着绳、抱住桅杆根部，桅杆绕根部的转轴向船尾转动放倒；12–14s 桅杆最后半秒明显加速、落到船篷上顿一下停住，船头随即钻进桥洞；14–16s 镜头从桥面上方擦过；16–24s 过桥后沿河西飞拔高，河道在下方变窄，两岸屋舍渐密；24–27s 镜头穿出贴水的晨雾层，远处东水门城台从雾后的淡土黄剪影变成被低斜日光照亮的夯土实体；27–30s 悬停：雾在城台脚下慢慢散开，只有水面反光与柳梢微动",
      lines=[],
      light="卯时，太阳刚离地平线一掌高、在镜头右后方的东方低空：低斜的暖光从画右后方擦过河面，右岸垂柳的长影一道道横铺在水上；虹桥朱漆拱木受光的一侧是发旧的暖赭红，桥腹与船篷背光处是蓝天反射的冷蓝，放倒的桅杆被勾出一道暖亮边；贴水浮着一层极薄的晨雾，远处东水门城台起初只是雾后一块淡土黄的剪影",
      pace="流（低飞）→ 放桅 → 擦（过桥）→ 升（穿雾）→ 停（悬停远望）",
      spatial="机位＝汴河水面上空自东向西连续飞行、逐渐拔高；在画主体＝河道 → 放桅的船与虹桥 → 远处东水门；飞行方向＝画面深处（西），最后悬停在虹桥以西约六百米的河道上空",
      contrast="首帧＝贴水低飞的河面与柳（远景 0.02）→ 末帧＝悬停在汴河上空、雾后显形的东水门（远景 0.02）。**从一条河飞到能望见这座城的门。**",
      moment="**26s 镜头穿出雾层、东水门城台从剪影变成受光的实体**（12s 桅杆放平是中段事件）",
      post="片名与开头黑场由后期加；环境音＝河水 + 远处号子（没有可辨字句）+ 桅杆倒下的木头摩擦声",
      judge="航线按 R3-01 修正：WP1 虹桥东约四百六十米、离水八米 → 过桥二十米 → 虹桥以西约六百米、离水一百五十米悬停远望东水门（B_city 按此重设 WP2），各段飞速不超过约五十五米每秒；hero（放桅）在 12s 而非镜尾——末 3 秒必须静定悬停交给 shot02（尾帧锁定），是结构性取舍；水手在离桥一个船身远处就放桅（R2-05：到了桥下再放来不及）；光改为画右后方低斜暖光与冷暖双色（R4 F04），镜尾事件改为穿雾显形（R4 F05）；场景参考 bg0-2（0–12s）+ bg1-1（过桥段）"),

 dict(n=2, seg="序", sec="航拍长镜", d=30, bg="bg0_汴京全城", v="bg0-1", vx=[("bg4-1", "14–26s 御街低飞"), ("bg12-1", "26–30s 宣德楼前")],
      lt="day", tod=1, tier="S", handoff_from=1, aerial=True, xuande=True,
      ch=[], pr=[], unit="航拍", crowd=True, local=True, neg_add="明清青砖城墙, 一圈青砖城墙, 正南正北对齐的方格城市, 潘杨湖",
      facts=["city.001", "city.021", "city.022", "palace.010", "city.024", "route.003", "city.005", "city.030", "route.009", "city.018", "city.038", "palace.002", "palace.004", "festival.001"],
      jb=(0.02, "远景", 0.02, "远景"), jbcam=("汴河上空一百五十米悬停远眺东水门", "宣德楼前低空仰视航拍"),
      cuts=[(0, 14, "起升后退：极高处斜俯三圈城墙", "开场"),
            (14, 30, "御街上空向北低飞，停在宣德楼前仰视", "切（换到御街中段上空）")],
      title="【航拍】拔高看全城 · 顺御街到宣德楼",
      summary="**承接 shot01 末帧**：从汴河上空的悬停继续起升后退，像延时航拍一样越升越高，三圈城墙一圈套一圈（外城与墙外宽宽的护龙河、旧城、城中偏西北的宫城），城墙微微斜着不是正南正北，汴河斜穿全城、南边蔡河绕弯，东北角艮岳还是工地，远处两座高塔；14 秒切到御街上空，沿中轴向北低飞，停在宣德楼正前方仰视。末 11 秒画外签名开场。",
      plot="首帧是悬停在汴河上空、远望东水门的画面；镜头继续起升并向后退，越升越高，整座汴京在晨光里展开：三圈城墙一圈套一圈——最外一圈是外城的夯土城墙，墙外一道四十来米宽的护龙河，里面一圈旧城，城中偏西北是一圈小小的宫城；整座城并不是正南正北，城墙微微斜着；汴河从西往东南斜穿全城，南边蔡河绕一个弯；旧城东北角一片堆土堆石的大工地；东南和东北远处各立着一座高塔；画面一切，镜头已在宫城正南的御街上空，顺着宽阔的御街向北低飞，两边黑漆杈子、路心两行朱漆杈子向后飞退，最后减速停在宫城正门宣德楼的正前方，从低处仰视城楼",
      cam="0–14s 一个连续运镜：0–3s 自悬停缓缓起升（首帧就是悬停画面，不重新构图），24mm，镜头平视略俯；3–14s 边拔高边向后退，像延时航拍一样越升越快（地面缩小得很快，但画面平稳、不拖影、不跳帧），升到极高处，镜头始终朝西北望着城、下俯约二十五度，三圈城墙一圈套一圈占满画面宽度；14–30s 切到御街上空：14–26s 自宣德楼正南约七百米、离地约五十米起，沿御街中轴向北快速低飞并降到约八米，24mm，镜头平视，两边杈子向后飞退；26–30s 减速停在宣德楼正南约一百四十米、离地约八米处，镜头上仰约十度，城楼与两侧朵楼占满画面宽度、上缘留一线天。画面里没有任何飞行器，也没有飞行器的影子",
      block="画面里没有具名人物；御街两侧行人为剪影、不可辨面孔；御街中间两行朱漆杈子围出的御道里空无一人；可辨主体不超过八个，所有人都不看镜头",
      act="0–3s 自悬停缓慢起升，东水门与汴河在画面下方变小；3–14s 越升越高：近处一段外城夯土城墙像一道长堤，墙外护龙河宽得能并排走几条船，汴河上的纲船只有米粒大；晴天里远处依旧清楚，旧城与城中偏西北的宫城轮廓分明，城墙微微斜着；汴河斜穿全城，南边蔡河绕弯，旧城东北角一片工地，远处两座高塔；14–26s 切到御街上空向北低飞，两边黑漆杈子与路心两行朱漆杈子向后飞退，御沟水面一闪一闪；26–30s 减速，宣德楼越来越大，停住仰视：五个门洞、朱漆门扇、墩台上的砖石雕饰、单檐庑殿门楼与两侧朵楼，门楼屋面是发暗的绿琉璃瓦、不是金黄，门扇上一排排暗哑的铜金色门钉",
      lines=[L(19, "画外", OPENING, EN_OPENING, 10.5, "festival.001", "平、慢，像念一个日期", "慢")],
      light="卯时刚过，低斜的日光自东方照来，全城屋顶东侧受光、西侧拖着长影，晴天蓝天下远景清楚；宣德楼正面被东侧低光斜照，绿琉璃瓦在斜光里是哑一点的深绿",
      pace="升（全城）→ 切 → 飞（御街）→ 停（仰视宣德楼）",
      spatial="机位＝汴河上空悬停处起升后退 → 全城极高处斜俯 → 切到御街上空自南向北低飞 → 宣德楼前低空仰视；运动方向＝先向上向后，切后向正北",
      contrast="首帧＝汴河上空悬停远望东水门（远景 0.02，与 shot01 末帧同一画面）→ 末帧＝宣德楼正面仰视（远景 0.02）。**从城门外看见整座城，最后停在它的正门前。**",
      moment="**29s 停在宣德楼正前方仰视的那一帧**（封面候选）",
      post="签名开场画外落在 19–29.5s（R3-04：放慢到 10.5 秒）；开头 0.3 秒不出声（承接缝静默，ai_video.md (J)）；14s 的镜内切换不加任何转场",
      judge="按 R3-02 方案 A：镜内一切（14s）、删去 W11 WP4，WP5→WP6 改在宣德楼正南约七百米起飞、约五十米每秒；州桥不在飞越路线（它是 shot16 的主体，飞越要约八十五米每秒）；「马面」无 fact，不写；宣德楼绿琉璃瓦例外延伸到本镜末段（style_guide §6 注），挂 bg12 负向组并加「潘杨湖」（R6 W16 / R4 F06）；格局取 city.001 / 021 / 022、palace.010、city.024、route.003 与 city.005、city.030、city.018、city.038；场景参考 bg0-1（0–14s）+ bg4-1（御街）+ bg12-1（宣德楼前）"),

 dict(n=3, seg="起", sec="开场", d=28, bg="bg1_虹桥", v="bg1-1", lt="day", tod=1, tier="A",
      ch=["c1m"], pr=["p2"], unit="逛单", crowd=True, local=True,
      facts=["price.022", "price.023", "price.024", "money.006", "money.001", "money.003", "money.008"],
      jb=(0.75, "近景", 0.50, "中景"), jbcam=("虹桥桥头台阶下正面平视", "桥头正面平视·拉开"),
      hands="右手握话筒在胸前；采访本夹在左腋下，左手空出来点数、掏钱串",
      title="【开场】桥头出镜 · 今天的逛单",
      summary="现代装的林问站在虹桥桥头对镜头：自报家门、四项逛单、两个按前后几年推算的物价锚；身后桥上一片号子喊声（听不清字句），她缩脖子回头；转回来掏出一贯铜钱晃一晃。",
      plot="清明清晨，现代装的林问站在虹桥桥头台阶下，正对镜头说话，身后是桥面上的人流与河面；身后桥上忽然一片号子喊声，她缩了一下脖子，回头看了一眼；转回来，从夹克口袋里拿出一串麻绳穿着的铜钱举到镜头前晃了晃，又收回口袋，抿嘴一笑",
      cam="一个机位。桥头台阶下正对她，眼平，50mm，f2.8，背景桥面人流柔焦；0–21s 近景（胸口以上），机位固定；21–28s 机位平稳后退约一米、拉开成中景，让她身后的桥面入画",
      block="林问站在画面中央、正面朝镜头、说话时看镜头；19.5–21.5s 回头看画面后方的桥面；桥上人群在她身后画面上半部、柔焦剪影、不看镜头",
      act="0–5.5s 她正脸看镜头开口，右手话筒在胸前、采访本夹在左腋下；5.5–12.5s 边看镜头说边用左手手指一样一样点数；12.5–19.5s 看着镜头报两个数；19.5–21.5s 身后桥上一片号子喊声，她缩了一下脖子、回头看一眼；21.5–25.5s 转回来正脸看镜头，左手从夹克口袋掏出一串麻绳穿的铜钱举到镜头前晃一下，说完收回口袋；25.5–28s 抿嘴一笑",
      lines=[L(0, "对镜", SELF_INTRO + "今天带你逛一整天北宋汴京。", EN_SELF_INTRO + " Today, we tour Song-dynasty Kaifeng.", 5.5, "", "利落，有精神"),
             L(5.5, "对镜", "单子就四样：吃早市夜市，住一晚客店，能进的地方都进去看，再赶上清明出城。",
               "My list: morning and night markets, a night at an inn, every place that's open, and the Qingming outing.", 7.0, "", "掰手指"),
             L(12.5, "对镜", "先记两个数，按前后几年推算：米一斗两百五十文上下，扛活的一天挣一百文左右。",
               "Two numbers, estimated from nearby years: rice, about 250 wen a peck; a laborer's day, about 100.", 7.0, "price.022 price.023 price.024", "报数，稍慢"),
             L(21.5, "对镜", "我兜里揣着一贯钱，街上买东西，认的是铜钱。", "One string of coins in my pocket. Shops here take copper.", 4.0, "money.006 money.001", "举钱串")],
      light="卯时的清明清晨，低斜的暖光自画右照在她脸的一侧，另一侧是蓝天反射的冷蓝柔光；背景柔焦里桥上朱漆受光发暖、桥腹背光是冷蓝，河面浮着一层薄雾、反出一道碎光",
      pace="说（稳）→ 点数 → 报数 → 喊声（缩脖回头）→ 举钱 → 笑",
      spatial="机位＝桥头台阶下正面眼平（末段平稳后退）；在画主体＝林问；她正面对镜头，19.5–21.5s 回头看画面后方的桥面",
      contrast="首帧＝她正面开口的近景（近景 0.75）→ 末帧＝拉开后她抿嘴笑、身后桥面入画（中景 0.50）。**逛单说完，这座城先喊了她一嗓子。**",
      moment="**20s 号子喊声里她缩脖子回头**",
      judge="米价取 price.022（宣和四年 250–300）与 price.023（大观年间 250），工钱取 price.024（北宋一般约百文），口播「按前后几年推算」（R6 W02）；「只认铜钱」收窄为「街上买东西，认的是铜钱」（money.006，R6 W03）；钱串形制回指 money.001 / 003 / 008（⚠️ 旧钱为主是铸量推断）；动作重排为先喊声回头、后掏钱串（R2-06）；时长 24→28 s（R3-08）；英文「文」译作 wen，与 shot09 的省陌同一口径"),

 dict(n=4, seg="起", sec="城外", d=28, bg="bg1_虹桥", v="bg1-1", lt="day", tod=1, tier="S", ear=True,
      ch=["c1m"], pr=["p9"], unit="行", crowd=True, local=True,
      facts=["route.004", "bridge.001", "bridge.004", "bridge.006", "bridge.007", "shop.004", "shop.001"],
      jb=(0.20, "全景", 0.30, "全景"), jbcam=("桥头台阶低角侧跟", "脚店门口斜前方低角仰摇"),
      hands="右手握话筒垂在身侧；采访本塞进夹克左内袋，左手空着，桥中扶栏",
      title="【一镜到底】桥头 → 桥面 → 桥尾脚店",
      summary="**本站的一镜到底。** 低角度侧跟：桥头台阶 → 桥面摊棚人流 → 桥中扶栏回望河面（四分之三侧脸，封面候选）→ 桥尾脚店门口抬头，三层彩楼欢门逆光压进画面。画外点名《东京梦华录》与《清明上河图》，尺寸与木杆两条口播「推测 / 史书没写」。",
      plot="清明清晨，现代装的林问从虹桥桥头台阶走上桥面，两侧是席棚、大伞、挑担和蹲着的小贩，人从她身边擦过；桥中她扶着木栏回头看河面，一条船正从桥洞出来，她再抬眼望向桥头那对顶上有木鸟的高木杆；她继续走到桥尾，停在脚店门口，门首一块空白窄条木牌，她抬头看高过屋檐的彩楼欢门",
      cam="一镜到底、不切。稳定器低角度侧跟：机位高约零点六米、在她左侧约两米、与她同速，35mm，f4；0–6s 桥头台阶起跟；6–16s 桥面跟行，席棚与伞沿从画面上缘掠过；16–20s 她在桥中停步扶栏，机位绕到她侧前方约四十五度，她回头看河面时四分之三侧脸朝镜头，身后河面与桥洞里出来的船入画；20–26s 继续跟到桥尾；26–28s 机位停在脚店门口斜前方，随她抬头向上摇约二十五度",
      block="林问自画右向画左沿桥面走，始终在画面中央偏右、侧对镜头，不看镜头；桥上可辨人物不超过八个（两名挑担、两名蹲着的小贩低头摆弄摊上的货、一名撑伞的、三名行人），其余是远处剪影，所有人都不看镜头、不说话；6–16s 挑担的竹筐与伞沿不时从镜头前极近处掠过，虚成暗色块；桥中她面朝画右上方的河面、侧脸朝镜头；桥尾脚店门口无人挡路",
      act="0–6s 她一步一步上台阶；6–12s 桥面上人从她身边擦过，她侧身让一次挑担的；12–16s 一把大伞从她头顶掠过，她低头钻过；16–20s 停在桥中木栏边，左手扶栏回头看河面，一条船正从桥洞出来，再抬眼望向桥头那对顶上有木鸟的高木杆；20–26s 继续往前走，经过两个蹲着的小贩；26–28s 走到桥尾脚店门口站定，抬头，门首三层镂空彩楼欢门高过屋檐压进画面上半，杆上褪色的彩帛被低斜的晨光从背后照透。全程单向前进，不往回走",
      lines=[L(0, "画外", "这座桥在东水门外七里。《东京梦华录》里说它「无柱」——底下没有一根桥柱，拿大木头凌空架起来，刷成朱红，「宛如飞虹」。", "Seven li outside the East Water Gate. The Dreams of the Eastern Capital says: no pillars, just timbers arched in the air, painted red, like a flying rainbow.", 10.5, "route.004 bridge.001", "边走边说", "中", "脚下台阶与桥面"),
             L(10.5, "画外", "有学者照着《清明上河图》算过，长二十来米，宽七八米。这是推测，不是量出来的。",
               "Scholars measured it off the Qingming scroll: about twenty meters long, eight wide. That's an estimate, not a survey.", 7.0, "bridge.004", "补一句", "中", "身边的摊棚和人流"),
             L(17.5, "画外", "桥头那对高木杆顶上有只木鸟，干什么用的，史书没写，我不瞎猜。", "Poles with a wooden bird on top — what for? The records don't say; I won't guess.", 6, "bridge.007", "轻", "中", "桥头那对高木杆"),
             L(23.5, "画外", "桥面就是个集市。桥尾这家，叫「十千脚店」。", "The bridge is a market. At the end: the Shiqian tavern.", 4.5, "bridge.006 shop.004", "收", "中", "脚店门首的彩楼欢门")],
      light="卯时的清晨，低斜日光自画右（河面方向）照来，席棚在桥面投下长影，伞下透光，桥面被脚步踩起的细尘在低斜光里看得见，桥下河面浮着一层薄雾、碎光闪动；她在明暗之间穿行",
      pace="上（台阶）→ 挤 → 停（回望）→ 走 → 停（抬头看欢门）",
      spatial="机位＝她左侧两米低角侧跟（连续运动，桥中绕到侧前方）；在画主体＝她与桥面人流 → 桥中河面与木杆 → 桥尾脚店与欢门；她自画右向画左前进，桥中回望画右上方",
      contrast="首帧＝桥头台阶下的她（全景 0.20）→ 末帧＝她站在脚店门口抬头、欢门逆光压顶（全景 0.30）。**从桥的一头走到另一头，这座桥的日常从她身边过了一遍。**",
      moment="**27s 她抬头，三层彩楼欢门逆光压进画面**（18s 桥中回望的四分之三侧脸是封面候选）",
      post="「十千脚店」木牌在画面里是空白的，字由后期贴原画字样（shop.004）；尺寸不叠数字卡（dossier §14 #10）",
      judge="招牌一律空白、只口播店名（R6 F09 / 协调者裁定 9）；挂 p9 锁定脚店门脸（R7 W13，prompt 用空白木牌版）；首次点名《清明上河图》（R1 R09 / R5 F06），《东京梦华录》点名并解释「无柱」（R1 R29）；16–20s 机位绕到侧前方，封面帧能拿到四分之三侧脸（R5 F09）；OS 视线跟着讲的东西走（R2-07）；镜尾改为欢门逆光（R4 F20）；景别档起幅 0.20（上一镜落幅 0.50）"),

 dict(n=5, seg="起", sec="城外", d=24, bg="bg1_虹桥", v="bg1-1", lt="day", tod=1, tier="A",
      ch=["c1m"], pr=["p9"], unit="吃", local=True, neg_add="金属镜面反光, 亮银, 镀银反光",
      facts=["food.006", "shop.002", "food.026", "price.002"],
      jb=(0.75, "近景", 0.90, "近景"), jbcam=("脚店门口桌边平视", "银注碗前近景"),
      hands="右手握话筒、左手拿采访本；碰碗和写字前先把话筒插回夹克右口袋，右手从书脊抽出铅笔",
      title="【脚店】正店和脚店 · 银器是借来的",
      summary="脚店门口，伙计擦着桌子朝她点点头；桌上一副银注碗。她讲正店七十二户、脚店从正店批酒、银酒具是正店借的；下酒菜十五文以内，记一笔不买。",
      plot="清明清晨，虹桥桥尾脚店门口，一名三十来岁的伙计正擦桌子，看见林问，朝她点了点头，又低头继续擦；桌上摆着一副银注碗、两副盘盏；现代装的林问站在桌边对镜头说话，伸手碰一下银注碗又缩回，拿起采访本记了一笔，合上本子摇摇头",
      cam="一个机位。桌边正对她，眼平，50mm，f2.8，近景（胸口以上），背景欢门与桥面柔焦；0–14s 机位固定；14–24s 极缓推近，末帧银注碗在画面下缘",
      block="林问站在桌边画面右侧、说话时正面朝镜头；伙计在画面左后方桌后、侧身擦桌、不看镜头、不说话；桌上银注碗在她身前画面下缘",
      act="0–1s 伙计抬头朝她点头，她侧头点头回礼；1–7s 转回正脸看镜头开口；7–10s 嘴停下，回头指一指身后门首；10–14s 先把话筒插进夹克右口袋，然后伸右手指尖轻碰一下银注碗、立刻缩回；14–18s 从采访本书脊抽出铅笔写一笔；18–24s 合上本子，正脸看镜头说完，摇摇头表示不买",
      lines=[L(1, "对镜", "书上说「在京正店七十二户」，自己能酿酒的就这七十二家，剩下的都叫脚店。",
               "The book says the capital had seventy-two licensed brewers. Every other tavern was a jiaodian.", 6.0, "food.006", "介绍"),
             L(7, "画外", "脚店的酒，是从正店批来的。", "A jiaodian buys its wine from them.", 2.5, "shop.002", "补充", "中", "身后脚店门首"),
             L(9.5, "画外", "桌上这副银酒具，是正店借的——脚店来打过两三回酒，正店就敢借。", "This silver is on loan from a big brewer — buy wine there a few times and they'll lend it.", 7.5, "food.026", "轻快", "中", "桌上的银注碗"),
             L(18, "对镜", "下酒菜一份不过十五文。记下，先不吃，这一贯钱得撑到晚上。", "Side dishes: fifteen wen, tops. Noted — not buying. This string has to last till night.", 5.5, "price.002", "合本子", "中", "")],
      light="卯时末的清晨，低斜的日光从画右越过桥面照到桌上：她半张脸在光里、半张落进席棚的斜影，脚店欢门的彩帛在她身后逆光透亮；银注碗受光一侧是发暗的银白、背光一侧映着天光的冷灰，不是镜面；背景是蓝天下碧绿的河面",
      pace="点头 → 说 → 指门首 → 碰碗 → 记 → 摇头",
      spatial="机位＝桌边正对（末段极缓推近）；在画主体＝林问近景与银注碗；她说话时正面对镜头，伙计在她身后画左",
      contrast="首帧＝她与伙计互相点头（近景 0.75）→ 末帧＝她合上本子摇头、银注碗在画面下缘（近景 0.90）。**先记账，不花钱。**",
      moment="**21s 合上本子摇头不买**",
      judge="「银器是酒具不是钱」只在 shot31 讲，本镜删去「不是钱」与 money.007（R5 F10）；「人家」改清楚是正店借给脚店（R1 R24）；手位与开口窗重排（R2-08）；景别档改 0.75 → 0.90 与推近一致（R3-27）；光改为清晨低斜（R4 F03，上午→清晨，协调者裁定 1）；时长 20→24 s（R3-09）；「十千脚店」木牌空白（p9 派生版）"),
]

S += [
 dict(n=6, seg="承", sec="入城", d=26, bg="bg2_东水门城门", v="bg2-1", lt="day", tod=2, tier="A",
      ch=["c1m"], pr=["p6"], unit="行", crowd=True, local=True,
      facts=["gate.002", "route.002", "route.003", "festival.006", "job.002", "gate.006"],
      jb=(0.10, "远景", 0.50, "中景"), jbcam=("东水门外河岸高位远眺", "旱门门洞内侧平视"),
      hands="话筒与采访本都攥在两只手里，捂耳朵时是两只拳头贴着耳朵",
      cuts=[(0, 8, "东水门外远眺：水门闸门吊起、两岸旱门、出城人潮", "开场"),
            (8, 26, "旱门门洞内侧：她逆着出城人流进门，太平车铁铃在她身边一响，驼队穿门", "切（换到门洞内侧）")],
      title="【入城】东水门 · 太平车的铁铃",
      summary="东水门：跨河水门、铁裹闸门吊起、两岸旱门；汴河从这里流出城，东南来的粮船也从这里进城。清明一早人往外涌，她逆行往里走；一辆太平车前面二十多头骡驴，车底铁铃在她身边一响；驼队穿门。",
      plot="清明辰时初，汴河东水门：一座夯土城台横跨汴河，包铁皮的闸门高高吊起，两岸各一座旱门；人潮往城外涌，现代装的林问逆着人流从旱门往城里走；一辆太平车拉着一袋袋麦面进城，前面二十多头骡驴分两行，车底挂的铁铃一晃一响，正好擦着她过去；两峰骆驼从旱门穿过",
      cam="0–8s 门外河岸高处、俯角十度朝水门，28mm，f8，机位固定，画面右侧前景是岸边一截垂柳枝，离镜头很近、虚成嫩黄绿的色块随风轻晃；8–26s 切到旱门门洞里侧，眼平，35mm，f4，机位固定：出城人流自画左（门内）向画右（门外）涌出，太平车、骡驴与她自画右（门外）向画左（门内）逆着人流进门",
      block="0–8s 无具名人物，人潮为逆光剪影、可辨者不超过八个；8–26s 林问自画右门洞口侧身逆着出城人流挤进来，太平车与骡驴从她右侧同向超过她，她被挤到门洞边；只在 19–21s 捂着耳朵转脸看镜头说话，其余时间不看镜头；驼队在她身后穿门；所有当地人都不看镜头、不说话",
      act="0–4s 闸门吊在水门上方，闸门下沿比河上纲船的船篷还高出好几人，城台上走动的人只有城垛那么高，河水从门下流过；4–8s 人潮向画右（城外）涌动；8–12s 门洞里她侧身逆着人流挤进来；12–15s 骡驴一对一对从她右侧同向走过；15–19s 太平车擦着她过去，车底挂的铁铃就在她腰边一晃一响，她一缩头、两只拳头捂住耳朵；19–21s 捂着耳朵转脸看镜头说话；21–26s 她靠在门洞边喘口气，两峰骆驼从她身后穿过门洞",
      lines=[L(0, "画外", "东水门，汴河从这儿流出城；东南来的粮船，也是从这儿进城。", "The East Water Gate. The Bian River flows out here; southeast grain boats come in.", 6, "gate.002 route.002 route.003", "解说", "中", "远处横跨河面的水门"),
             L(6, "画外", "清明一早，书上说「士庶阗塞诸门」，全城往外挤，我往里走，就是逆行。",
               "Qingming morning — the book says crowds jam every gate. Everyone's heading out; I'm going in.", 6.0, "festival.006", "被挤着", "中", "迎面涌来的人流"),
             L(12, "画外", "这叫太平车，前头二十多头骡子驴子，车底下挂一只铁铃，一响，对面的车就知道让道。",
               "A taiping cart: twenty-odd mules and donkeys, and an iron bell underneath so oncoming carts make way.", 7.0, "job.002", "解说", "中", "身边走过的骡驴和车底的铁铃"),
             L(19, "对镜", "……这铃铛，就贴着耳朵响。", "That bell — right in my ear.", 2.5, "", "捂着耳朵", "快", ""),
             L(21.5, "画外", FIXED, EN_FIXED, 2.5, "", "笑一下", "中", "从身后穿过门洞的骆驼")],
      light="辰时初的清晨，低斜的日光自画右（门外）照进门洞，门洞里是冷灰的暗、门外亮；骡驴蹄子和车轮扬起的黄土尘在门口那道斜光里翻滚发亮，人、车、骆驼穿过这团亮尘时被勾出暖边；夯土城台受光一侧是土黄色",
      pace="远眺（静）→ 挤（乱）→ 铃（惊）→ 对镜一句 → 喘",
      spatial="机位＝门外河岸高位（固定）→ 旱门门洞内侧眼平（固定）；在画主体＝水门与人潮 → 她与太平车骡驴；出城人流自画左（城内）向画右（城外），她与车队自画右向画左",
      contrast="首帧＝远眺水门与出城人潮（远景 0.10）→ 末帧＝她靠在门洞边、驼队在身后（中景 0.50）。**从城外看城门，到被城门吞进去。**",
      moment="**17s 铁铃擦着她响、她捂耳朵**",
      post="固定句「听着像编的，但这是真的」配 ✅ 音效（后期）",
      judge="「汴河从这儿进城」说反了：东水门是汴河下游出城水门（gate.002 / route.002 / city.035），改为出城，并补「东南粮船由此入京」route.003（R6 F01 / 协调者裁定 9）；人流方向单一化（R2-09 / R3-10）；「听见了」像在答车夫，改成对镜说铃声（R1 R23）；铁铃挂在车底、擦过腰边（R2-10）；门洞逆光扬尘与闸门尺度参照（R4 F21）；时长 24→26 s（R3-11）"),

 dict(n=7, seg="承", sec="住", d=26, bg="bg7_坊巷民居", v="bg7-2", lt="day", tod=2, tier="A",
      ch=["c1m"], pr=[], unit="住", indoor=True, local=True,
      facts=["house.003", "inn.016", "inn.010", "house.001", "inn.026", "inn.027", "inn.030"],
      jb=(0.20, "全景", 0.80, "近景"), jbcam=("客店房门口平视全景", "床榻边近景"),
      hands="话筒插在夹克右口袋、采访本塞进夹克左内袋，两手空着",
      carry=[BUNDLE_NONE],
      cuts=[(0, 6, "房门口全景：伙计比了个请的手势退出去，她进门", "开场"),
            (6, 26, "她照旅客守则查房：按墙、看床底、看墙角、关门，坐到椅子上敲瓷枕", "同段延续（缓推到床榻边近景）")],
      title="【住】客店入住 · 照守则查房",
      summary="沿城客店的一间房：新换的草垫席子、白地黑花瓷枕、高桌靠背椅、没点的油灯、屋角空炭盆。她照北宋县官写的旅客守则查房——看墙、看床底、看墙角、再关门；坐椅子、敲瓷枕。房价与客店摆不摆瓷枕都口播标明史书没写、推测。",
      plot="清明辰时，沿城客店里的一间房：素木床榻上是新换的草垫和席子、一只白地黑花的长方瓷枕，靠墙一张高桌、两把靠背椅，桌上一盏没点的陶油灯，屋角一只空炭盆；伙计在门口比了个请的手势就退了出去；现代装的林问进门先按了按墙，蹲下看床底，再看两个墙角，回身把门关上，最后坐到椅子上，伸手敲了敲瓷枕",
      cam="0–6s 房门口平视全景，眼平，24mm，f5.6，机位固定；6–26s 机位自房门口向床榻边缓推约一米五、同时由 24mm 缓变焦到 50mm，眼平，末段停在她敲瓷枕的近景",
      block="伙计只在门口露背影与手、不看镜头、不说话；林问自画右门口进屋，沿墙走一圈，最后坐在床榻边的靠背椅上、侧脸对镜头，说话时转正脸看镜头；房里只有她一个人",
      act="0–3s 伙计在门口比一个请的手势，然后退出画外；3–6s 她进门站住，环视四面墙；6–8s 走到墙边用手按了按墙面；8–10s 蹲下看床底；10–13s 站起来，正脸看镜头说话；13–15s 看两个墙角；15–17s 回身把门关上；17–20s 坐到靠背椅上，拍了拍扶手；20–26s 伸手敲一敲瓷枕、缩一下手，转脸看镜头说话",
      lines=[L(0, "画外", "北宋县官写的旅客守则：进屋先看墙破没破，再看床底下、墙角藏没藏人，看完再关门。",
               "A Song magistrate's advice for travelers: check the walls for holes, check under the bed and the corners, then shut the door.", 8.0, "inn.016", "照着做", "中", "四面墙和床底"),
             L(10.5, "对镜", "床底下，没人。墙，没破。行。", "Nobody under the bed. Walls are fine.", 2.5, "inn.016", "蹲下看完站起来", "中", ""),
             L(13, "画外", "住一晚多少钱，史书没写；客店配瓷枕，也是我的推测。", "Room price? Not recorded. Porcelain pillows at an inn? My guess.", 4.5, "inn.026 inn.027", "收", "中", "墙角"),
             L(17.5, "画外", "椅子、高桌都有，宋朝人早就不坐地上了。", "Chairs, a real table. Nobody sits on the floor.", 3.5, "house.001", "坐下", "中", "靠背椅的扶手"),
             L(21, "对镜", "瓷枕，又硬又凉。张耒写它「持之入室凉风生」——我脑门要凉一宿了。", "Porcelain pillow: hard and cold. A poet called it a cool breeze. Brr.", 5, "inn.026", "敲一下瓷枕", "中", "")],
      light="辰时的清晨，散射天光从直棂窗斜进来，床榻一侧受光、墙角偏暗；油灯没点，屋角那只炭盆是空的",
      pace="进（看）→ 查（墙、床底）→ 对镜 → 墙角 → 关门 → 坐 → 敲枕",
      spatial="机位＝房门口全景（固定）→ 缓推至床榻边；在画主体＝房间陈设 → 查房的她 → 坐在椅上的她；她先沿墙走一圈，最后侧身朝画左的床榻",
      contrast="首帧＝伙计在门口比请（全景 0.20）→ 末帧＝她坐在椅上敲瓷枕（近景 0.80）。**照九百年前的旅客守则查一遍房，才敢住。**",
      moment="**23s 她敲瓷枕缩手**",
      judge="房价（house.004 / price.017 是 ai_draft）不报数；客店配瓷枕是推测，瓷枕形制补 inn.027（R6 W12 + R1 R28 合并）；台词顺序与动作重排，瓷枕那句挪到敲枕时（R2-11）；推近＋变焦写清（R3-28）；清明已过取暖季（inn.030），炭盆是空的；布包到 shot33 才拴上床腿（rule 16.3 反向声明）；上午→清晨（协调者裁定 1）"),

 dict(n=8, seg="承", sec="穿", d=28, bg="bg7_坊巷民居", v="bg7-2", lt="day", tod=2, tier="A", ear=True,
      ch=["c1m", "c1"], pr=["p2"], unit="穿", indoor=True, local=True, dress=True, cuts_elide=True,
      neg_add="换衣服时手里拿着话筒, 双手干活时仍握着话筒和本子, 多出来的手",
      facts=["dress.002", "dress.015", "dress.005", "dress.009", "dress.013", "dress.014", "money.001"],
      jb=(0.35, "全景", 0.75, "近景"), jbcam=("客店窗边正面全景", "窗边正面近景"),
      hands="0–24s 话筒与采访本放在床上，两手空着换衣服；24s 起右手拿回话筒、左手拿回采访本",
      carry=[BUNDLE_LOOSE],
      bind="换装前后是同一个林问：0–5s 是现代装态，5s 起逐件变成宋装态，林问在画面里只出现一次、两种装束不同时出现；另有客店娘子只露手与背影、不露脸",
      cuts=[(0, 5, "窗边正面全景：娘子递来本白布包裹，她解开", "开场"),
            (5, 11, "左前方中景：已穿好短襦长裙，娘子从背后罩上灰青褙子，她拉开腋下对镜头讲", "切"),
            (11, 17, "右后侧近景：系上青花手巾、把钱串系在手巾下，娘子的手把头发绾成低髻用皂巾包住", "切"),
            (17, 22, "侧面特写：搭上本白盖头，她点一点耳后铜片、转眼看镜头", "切"),
            (22, 28, "正面近景：胸牌别上褙子左外襟，她拿回话筒和本子对镜头转半圈", "切")],
      sstate=["她还是现代装（黑 T、工装夹克、低马尾），宋装衣物叠在布包裹里；话筒与采访本放在床上",
              "已穿上本白交领短襦、皂黑长裙并罩上灰青褙子；现代衣物已叠进布包放在床上；钱串已从夹克口袋取出放在床上；手巾、包髻、盖头、胸牌还没穿戴；头发仍是低马尾",
              "在前段基础上已系上青花手巾、钱串系在手巾下的腰带上、头发已包成包髻露额；盖头、胸牌还没上身",
              "在前段基础上本白盖头已搭在髻后披于背；胸牌还没别",
              "在前段基础上胸牌已别在褙子左外襟，全套宋装完成；布包放在床上、没有拴在床腿上；话筒回到右手、采访本回到左手"],
      title="【穿】穿搭检查 · 换宋装",
      summary="客店娘子帮她换：短襦长裙 → 褙子 → 手巾（钱串系在手巾下）→ 包髻 → 盖头 → 胸牌，镜内逐段切、衣物只增不减；她讲端拱二年诏令、北宋宽袖褙子、包髻与盖头。换装完成态从本镜起锁定。",
      plot="辰时，客店房间窗边，一名只露手与背影的客店娘子递来一个本白布包裹；林问解开，换上本白交领短襦、皂黑高腰长裙系到胸下，娘子从背后给她罩上灰青直领对襟褙子，宽袖、腋下不缝自然敞开；她把夹克口袋里的钱串取出来，系腰前青底白花粗布手巾时把钱串一并系在手巾下；娘子的手把她的头发绾成低髻，用皂布巾包成包髻、露出额头，再把一块本白盖头搭在髻后；最后她把素色布胸牌别在褙子左外襟，把换下的现代衣服叠进布包放到床上，拿回话筒和本子，对镜头转了半圈",
      cam="0–5s 窗边正面全景，眼平，28mm，f4，机位固定；5–11s 切到她左前方约四十五度中景（腰以上），眼平，35mm，机位固定；11–17s 切到她右后侧近景，眼平略高，50mm，看手巾与包髻，娘子的手在画左；17–22s 切到她侧面特写，眼平，85mm，包髻、盖头与耳后铜片；22–28s 切回正面近景，眼平，50mm，机位固定，胸牌，她转半圈",
      block="林问站在窗前画面中央，按娘子的手势转身；客店娘子只在画面边缘露出手与背影、不露脸、不说话、不看镜头；不给脚部特写",
      act="0–5s 娘子递来本白布包裹，她解开，拎起褙子看袖子；5–7s 娘子从背后给她罩上褙子；7–11s 她正脸看镜头，拉开腋下敞开处给你看；11–17s 系上腰前手巾、把钱串系在手巾下，低头，娘子的手把头发绾成低髻、用皂巾包住、露出额头；17–19s 娘子把盖头搭在髻后；19–22s 她侧过脸、手指点一点耳后铜片，转眼看镜头说话；22–25s 把胸牌别在褙子左外襟；25–28s 拿回床上的话筒和采访本，对镜头转半圈。衣物只增不减，穿上的不再脱下",
      lines=[L(0, "画外", "换装。端拱二年下过诏令，老百姓只许穿黑白，不许穿紫；街上多是本白、皂黑、灰褐。", "Costume change. A 989 decree: commoners in black or white, never purple. Streets are undyed white, black and grey-brown.", 7, "dress.002", "解说", "中", "解开的布包裹里的衣服"),
             L(7, "对镜", "北宋的褙子，袖子是宽的，腋下这儿不缝，就敞着。", "Northern Song beizi: wide sleeves, open under the arm.", 4, "dress.015", "拉开腋下", "中", ""),
             L(11, "画外", "头发全绾起来，拿皂布一包，叫包髻。额头露出来，不戴冠，不插珠子。", "Hair up, wrapped in black cloth — a baoji. Forehead bare, no crown, no pearls.", 5.5, "dress.005 dress.009", "解说", "中", "低头时自己的衣襟"),
             L(16.5, "画外", "出门再搭一块盖头，披在背后。", "Plus a head cloth down the back.", 2.5, "dress.013 dress.014", "轻", "中", "搭上来的盖头"),
             L(19, "对镜", "耳朵后头这个铜片还在，别问原理。", "The copper disc stays. Don't ask how.", 3, "", "指耳后", "中", "")],
      light="辰时，窗边散射天光自画右照来，麻布织纹在侧光里清楚；油灯没点",
      pace="拎 → 罩（讲褙子）→ 系包 → 盖头（铜片）→ 别胸牌 → 转",
      spatial="机位＝窗边五个机位逐段切（正面 → 左前 → 右后 → 侧面 → 正面）；在画主体＝她与逐件上身的衣物；讲褙子与铜片两句时转脸看镜头",
      contrast="首帧＝现代装的她拎起褙子（全景 0.35）→ 末帧＝全套宋装、胸牌在外襟、对镜转身（近景 0.75）。**换装＝把考据一件件穿在身上。**",
      moment="**20s 盖头搭上、她点一点耳后铜片**",
      judge="删去「不是明朝的立领、清朝的辫子」——只有 ❌ 兼 ai_draft 的 myth.005 支撑（R6 F02 / 协调者裁定 9）；端拱二年诏改为诏令＋街面实况，不再说「就两个颜色」（R6 W04）；分镜按 R2-13 重排使每句落在对应衣物上身之后、R3-06 改为五个机位（固定机位切景别不成立）；钱串在本镜转移到手巾下（R2-12 / R5 F18）；`bind` 不再写「只有她一个人」（R2-14）；镜内切镜省略穿衣中间过程（R3-31）；时长 26→28 s（R3-07）"),

 dict(n=9, seg="承", sec="吃·早市", d=26, bg="bg4_州桥御街", v="bg4-1", lt="day", tod=2, tier="A",
      ch=["c1"], pr=["p2"], unit="纠错", crowd=True, local=True, fall=("铜钱",), neg_drop=["碎银", "银子付账"],
      facts=["food.012", "lang.020", "food.013", "price.003", "money.002", "money.009", "money.006", "myth.001", "money.001", "money.008"],
      jb=(0.30, "全景", 1.40, "特写"), jbcam=("早市街口纵深平视", "案板上方俯拍双手"),
      hands="话筒柄朝下插在腰前青花手巾里、只露黑海绵头，采访本揣在褙子左襟里；两手空着，碎银从袖口里摸出、钱串从手巾下解下",
      carry=[WILLOW_NONE],
      cuts=[(0, 7, "早市尾声纵深：瓠羹店门口坐着个小孩，粥饭摊冒着白汽，低斜的晨光把人影拉长", "开场"),
            (7, 15, "粥饭摊前侧面中景：她递出碎银，摊主摇头、指她腰前的钱串，她转向镜头认错", "切"),
            (15, 26, "俯拍她的手：解开钱串一枚一枚数到十五，摊主的手伸过来收下", "切（换到案板上方俯拍）")],
      sstate=["钱串系在她腰前手巾下、没解开；案板上没有钱",
              "她手里多了一块碎银，被摇头后收回袖口；钱串仍系在腰前；案板上没有钱",
              "钱串已解开，案板上的铜钱一枚一枚只增不减，数到十五枚后被推过去收走；碎银不再出现"],
      title="【吃·纠错 ❌】早市尾声 · 掏银子被摇头",
      summary="**本站唯一的 ❌ 出场位。** 辰时，早市还没散：瓠羹店门口坐着个小孩，粥饭摊冒白汽。她掏出碎银，摊主摇头、指了指她腰前的钱串——她对镜认错；按七十五陌的比例推算，二十文数十五枚，摊主收下。",
      plot="辰时的早市还没散，一家瓠羹店门口坐着一个小孩，街边粥饭摊的锅里冒着白汽；宋装的林问走到粥饭摊前比了个一份，从袖口里摸出一块碎银递过去，摊主摇摇头，伸手指了指她腰前手巾下系着的钱串；她把碎银收回袖口，转向镜头认错；然后解开钱串，一枚一枚往案板上数，数到第十五枚停下推过去，摊主的手伸过来收下",
      cam="0–7s 街口平视全景，28mm，f4，机位固定，早市纵深与逆光的白汽；7–15s 摊前侧面中景，眼平，35mm，f4，机位固定，她在画左、摊主在画右隔着案板；15–26s 切到案板上方俯拍：离案板约一米、俯角六十度对着她的双手与钱串，85mm，f2.8，机位固定，末段让摊主伸过来的手入画",
      block="林问在案板前画左、面朝画右的摊主，认错时转向镜头；摊主在画右、侧身对镜头、不说话、不看镜头，只摇头、点头、用手指；小孩远远坐在画面后方瓠羹店门口，只是小小的侧影；数钱段只见她的双手、钱串、案板与摊主的手",
      act="0–4s 早市纵深，低斜晨光里一团团白汽往上翻；4–7s 行人从画面前经过；7–8s 她在摊前站定，比了个一份；8–10s 然后才从袖口里摸出一块碎银递过去；10–12s 摊主摇头，伸手指了指她腰前的钱串；12–15s 她先把碎银收回袖口，然后转向镜头开口认错；15–18s 俯拍：她解开钱串的麻绳；18–24s 一枚一枚往案板上数，一共十五枚，每枚落到案板上即停；24–26s 数到第十五枚停手，把钱推过去，摊主的手伸过来收下",
      lines=[L(0, "画外", "早市五更就开了，天亮了还没散。书上说，瓠羹店门口坐个小孩吆喝「饶骨头」，就是白送骨头。", "Opens before dawn, runs past sunrise. The book says a kid at the soup shop yells 'free bones.'", 7, "food.012 lang.020", "轻快", "中", "瓠羹店门口的小孩"),
             L(7, "画外", "粥饭点心，书上说一份「不过二十文」。", "Porridge and snacks: no more than twenty wen a serving.", 4, "food.013 price.003", "解说", "中", "冒白汽的粥锅"),
             L(12, "对镜", "好，我错了。这儿不收银子，认铜钱。", "My mistake. No silver here — copper.", 3, "myth.001 money.006", "认错，憋着笑", "中", ""),
             L(15, "画外", "街上一百文只数七十五枚，叫「街市通用七十五」。按这个比例推算，二十文大概十五枚——零钱怎么数，书上没写。", "A hundred wen on the street was seventy-five coins. By that ratio I'd guess fifteen for twenty — the book doesn't say.", 8.5, "money.002 money.009", "得意一点", "中", "案板上一枚枚落下的铜钱"),
             L(23.5, "画外", "……十三，十四，十五。齐了。", "…Thirteen, fourteen, fifteen. Done.", 2.5, "", "边数边小声念", "慢", "数到最后几枚的手")],
      light="辰时，太阳离地一竿高、从街口东侧（画左）低低斜照进来，早市的摊子与行人拖着很长的影子；粥锅与蒸笼冒出的白汽被逆光照亮、一团一团往上翻；摊棚下与屋檐下是天光反射的冷灰阴影，受光的席棚与素木案板是暖黄；俯拍段的主光是从画左低斜照到案板上的日光，铜钱受光的一侧青褐发亮、另一侧落进她手的影子里",
      pace="早（尾声）→ 递银 → 摇头 → 认错 → 数 → 收",
      spatial="机位＝街口平视（固定）→ 摊前侧面中景（固定）→ 案板上方俯拍（固定）；在画主体＝早市纵深 → 她与摊主 → 她的手与钱串；她面朝画右的摊主，认错时转向镜头",
      contrast="首帧＝低斜晨光与白汽里的早市纵深（全景 0.30）→ 末帧＝俯拍她数完十五枚推过去（特写 1.40）。**这座城不认银子，认的是一枚一枚数出来的铜钱。**",
      moment="**11s 摊主摇头、指她腰前的钱串**",
      post="本站唯一 ❌ 出场位：认错那句叠 ❌ 卡与正解「宋人日常买卖用铜钱」（后期层，prompt 零文字）",
      judge="时辰由五更前挪到辰时早市尾声、日光无火（R4 F01 / R5 F01 / 协调者裁定 1）；二十文数十五枚是按比例推算，口播带推测口吻并挂 money.009 ⚠️（W12 已登记，R2-15 / R5 F02 / R6 W05）；「给」是对摊主说话，改为画外小声数「齐了」（R1 R03 / R2-16）；「饶骨头」改为书上记载的叫卖、补 lang.020（R1 R20 / R6 W18）；碎银从袖口摸出、钱串系在手巾下（R2-12）；负向去掉「碎银, 银子付账」——本镜要画出她掏碎银被拒"),

 dict(n=10, seg="承", sec="吃·早市", d=20, bg="bg4_州桥御街", v="bg4-1", lt="day", tod=2, tier="A",
      ch=["c1"], pr=[], unit="吃", local=True,
      facts=["house.012", "food.012", "job.008"],
      jb=(0.50, "中景", 0.35, "全景"), jbcam=("早市摊边长凳侧前方平视", "摊边双人全景平视"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；左手端碗、右手拿筷子",
      carry=[WILLOW_NONE],
      cuts=[(0, 2, "太阳照上街面，她端着碗坐在摊边长凳上", "开场"),
            (2, 5, "食物微距：冒热气的粥、白瓷碗、筷子夹起一段灌肺", "切"),
            (5, 10, "她的正面近景：嚼两下咽下、皱眉、点头，然后看镜头打分", "切"),
            (10, 20, "一个闲汉笑着凑过来比划要不要替她跑腿，她愣住；双人全景", "切")],
      title="【吃】试吃打分 · 宋朝的跑腿",
      summary="食物微距 → 反应镜硬切（不拍连续入口）；咽下后对镜打分灌肺七分；一个闲汉凑过来比划要不要替她跑腿——「宋朝的外卖小哥」。",
      plot="太阳照上街面了，早市摊边，宋装的林问端着一只白瓷碗坐在长凳上，碗里是粥，旁边小碟里是切段的灌肺；她夹起一段嚼了嚼，皱眉又点头；一名二十来岁的闲汉笑着凑到她身边，嘴闭着，指了指街那头又指了指自己，比划着要不要替她跑腿买东西，她端着碗愣住",
      cam="0–2s 摊边长凳侧前方中景，眼平，35mm，机位固定；2–5s 食物微距，离碗约三十厘米、俯角三十度，100mm，f2.8，机位极缓前移；5–10s 她的正面近景，眼平，50mm，机位固定；10–20s 双人全景，眼平，35mm，机位固定，闲汉自画左入画",
      block="林问坐在长凳上，前三段在画面中央、侧身朝画右的摊子；闲汉段她在画右、闲汉在画左侧身朝她、不看镜头、不说话，只用手比划；她转头看他",
      act="0–2s 她端碗坐下；2–5s 微距：粥冒热气，筷子夹起一段灌肺；5–6s 她嚼两下咽下、皱一下眉；6–10s 嘴里已经没有东西，点点头，正脸看镜头打分；10–14s 闲汉笑着凑过来（嘴闭着笑、不张嘴），指街那头、再指自己；14–20s 她端着碗愣住，转头看他。不拍食物入口的连续动作，不边嚼边说",
      lines=[L(1.5, "画外", "碗是白瓷的，街边小摊也用这个。", "White porcelain bowls, even at a street stall.", 3.0, "house.012", "看碗", "中", "手里的白瓷碗"),
             L(6, "对镜", "灌肺，有点腥，蘸了汁还行。粥就是粥。给个七分。", "Stuffed lung: gamey, fine with sauce. Porridge: porridge. Seven.", 3.5, "food.012", "咽下后说", "中", ""),
             L(9.5, "画外", "他凑过来比划着，意思是要不要替我跑腿——宋朝管这种人叫「闲汉」，跑一趟给几个钱。", "He's miming: need an errand run? The Song called them xianhan — a few coins a trip.", 6.5, "job.008", "好笑", "中", "凑过来比划的闲汉"),
             L(16, "画外", "宋朝的外卖小哥。", "Song-dynasty delivery guy.", 1.5, "job.008", "憋笑", "中", "闲汉指着的街那头"),
             L(17.5, "画外", FIXED, EN_FIXED, 2.5, "", "笑一下", "中", "闲汉")],
      light="辰时，太阳已升高一些，斜光从画左照过摊边，她脸上一侧受光；食物微距以画左低斜的晨光为主光，粥和灌肺的热气被逆光照亮往上散",
      pace="坐 → 看（食物）→ 嚼 → 评 → 被凑 → 愣",
      spatial="机位＝长凳侧前方中景 → 食物微距 → 她正面近景 → 双人全景（三次硬切）；在画主体＝她 → 食物 → 她 → 她与闲汉；闲汉自画左入画",
      contrast="首帧＝她端碗坐下（中景 0.50）→ 末帧＝她端着碗愣看闲汉（全景 0.35）。**从「吃什么」到「谁在旁边等着替你跑腿」。**",
      moment="**15s 闲汉比划跑腿，她端着碗愣住**",
      post="固定句配 ✅ 音效（后期），单独一句便于卡点（R1 R47）",
      judge="打分段改为咽下后看镜头说、不边嚼边说（R2-17）；闲汉那句补上「意思是」（R1 R35），固定句拆成单独一句（R1 R47）；时辰「天亮了」改为太阳照上街面（R5 F01），光改辰时斜光（R4 F27）；闲汉不开口，只比划（follow-up 008）；景别档 0.50 → 0.35"),
]

S += [
 dict(n=11, seg="承", sec="吃·早市", d=20, bg="bg4_州桥御街", v="bg4-1", lt="day", tod=2, tier="A",
      ch=["c1", "c22"], pr=["p4", "p2"], unit="吃", local=True, neg_drop=["火", "火焰"],
      day_tail="；除了汤瓶下小泥炉里那一点炭火，画面里没有别的火、没有灯笼、没有暖色人工光源",
      facts=["food.013", "house.012", "money.001", "money.008"],
      jb=(0.80, "近景", 0.75, "近景"), jbcam=("饮子摊伞下正对汤瓶", "伞下她的侧前方近景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；指汤瓶用右手，接碗时两手捧碗，放钱时腾出右手",
      carry=[WILLOW_NONE],
      bind="画左伞下担子后＝周四娘（摊主，不说话）；画右摊前＝林问",
      title="【吃】汤茶药摊 · 买卖不用说话",
      summary="伞下的汤茶药摊：她指一指汤瓶，周四娘点头舀一碗递过来；她放下两枚钱，周四娘低头收了；她喝一口烫得吸气，对镜打八分。一碗多少钱史书没写，两枚够不够她也不知道。",
      plot="辰时的清晨，早市边一把竹骨油纸大伞下的汤茶药摊，周四娘守着担子，汤瓶在小泥炉上冒着热气，担梁上悬一块空白窄木牌；宋装的林问指了指汤瓶，周四娘点点头，舀了一碗递过来；林问在担子上放下两枚铜钱，周四娘低头把钱收了；林问捧着碗喝了一口，烫得直吸气",
      cam="一个机位。伞下摊前，眼平，50mm，f2.8，近景（胸口以上）；0–11s 以林问为主，汤瓶在画面下缘冒热气，机位固定；11–20s 极缓横移到她侧前方，周四娘在她身后柔焦",
      block="林问在画右摊前、侧身朝画左的担子，打分时转正脸看镜头；周四娘在画左伞下担子后、侧身、不看镜头、不说话，只点头、舀汤、递碗、收钱；两人隔着担子约一臂远",
      act="0–2s 林问指了指汤瓶；2–5s 周四娘点点头，拿勺从汤瓶舀一碗；5–7s 周四娘把碗递过来，林问两手捧住；7–9s 林问腾出右手在担子上放下两枚铜钱，周四娘低头把钱收进担子；9–11s 林问吹一吹、喝一口，烫得吸气；11–14s 正脸看镜头开口打分；14–20s 她捧着碗低头看碗里的汤，周四娘接着舀下一碗",
      lines=[L(0, "画外", "早市还有卖洗脸水、煎汤茶药的，书上说一直卖到「直至天明」，这会儿还剩几摊。", "The market also sold wash water and herbal brews till dawn. A few stalls remain.", 6, "food.013", "解说", "中", "伞下冒热气的汤瓶"),
             L(6, "画外", "一碗多少钱，史书没写。我放下两枚，够不够我也不知道。", "The records don't give a price. Two coins — enough? No idea.", 5, "", "轻", "中", "担子上放下的两枚铜钱"),
             L(11, "对镜", "烫——甜的，有股药味。汤，八分。", "Hot — sweet, a bit medicinal. Eight.", 3, "", "吸气", "中", ""),
             L(15, "画外", "碗是白瓷缸子，跟早上粥摊一个样。", "White porcelain again, same as the porridge stall.", 3.0, "house.012", "喝着", "中", "手里的白瓷缸子")],
      light="辰时的清晨，散射天光透过油纸伞变得柔和偏黄，她脸上是伞下的柔光；汤瓶口的热气在光里可见",
      pace="指 → 舀 → 递 → 放钱 → 喝（烫）→ 说",
      spatial="机位＝伞下摊前（末段极缓横移）；在画主体＝林问与汤瓶，周四娘在担子后；林问朝画左的担子",
      contrast="首帧＝她指着冒热气的汤瓶（近景 0.80）→ 末帧＝她捧碗低头、周四娘在身后舀下一碗（近景 0.75）。**买卖一句话不说也做成了。**",
      moment="**10s 她喝一口烫得吸气**",
      post="p4 担梁木牌在画面里空白，「香饮子」字样由后期贴原画并加 ⚠️ 角标（R6 F11：清明是否供应饮子 ⚠️）",
      judge="「焌糟」解释挪到 shot31 真正的焌糟入画处，本镜删去（R5 F05）；「她点点头收了」会被读成认可两文，改为「够不够我也不知道」、摊主低头收钱不点头（R6 W06，price.018 是 ai_draft）；台词顺序按动作重排（R2-18）；「直至天明」与辰时对上，补「这会儿还剩几摊」（R5 F01 / R1 R25）；担梁木牌空白（p4 派生版）；泥炉炭火来自 p4 锁定串，本镜光线与负向对这一点炭火单独放行；上午→清晨（协调者裁定 1）"),

 dict(n=12, seg="承", sec="人们怎么活动", d=24, bg="bg3_汴河码头", v="bg3-1", lt="day", tod=3, tier="A",
      ch=["c1", "c21"], pr=[], unit="行", crowd=True, local=True,
      facts=["travel.003", "travel.001", "job.001", "job.005"],
      jb=(0.15, "远景", 0.50, "中景"), jbcam=("码头仓前高位远景", "仓门口侧面中景"),
      hands="右手握话筒垂在身侧、左手拿采访本贴在腰前",
      carry=[WILLOW_NONE],
      bind="画面中央扛袋的＝李十六（不说话）；画右仓门边站着的＝林问",
      cuts=[(0, 8, "码头高位远景：纲船靠岸，脚夫排队扛袋进仓", "开场"),
            (8, 24, "仓门口侧面中景：李十六扛着一袋粮走过、放下、喘气，再扛起走进仓门，她站在一旁不挡道", "切（换到仓门口）")],
      title="【人们怎么活动】仓前码头 · 袋家",
      summary="城里汴河边的仓前码头：纲船靠岸，脚夫一人肩两石布袋走进仓门，仓前挤成集市；李十六扛完一段喘口气，把刚放下的那袋重新扛上肩进仓，她站在一旁不挡道。",
      plot="巳时，城里汴河边的仓前码头，几条平底纲船靠岸，厚跳板搭到岸上，脚夫一个接一个扛着粗布粮袋从船上下来走进仓门，仓前人来人往像集市；李十六扛着一袋粮走到仓门口，放下袋子直起腰喘气，抹一把汗，又把刚放下的那袋重新扛上肩走进仓门；宋装的林问站在仓门旁边，往后让半步不挡道",
      cam="0–8s 码头高处、俯角十五度，28mm，f8，机位固定；8–24s 仓门口侧面，眼平，35mm，f4，机位固定，扛袋的人自画左向画右走进仓门",
      block="0–8s 无具名人物特写，扛袋的人排成一行，可辨者不超过八个；8–24s 李十六自画左扛袋走来、在画面中央放下袋子，侧身、不看镜头、不说话；林问在画右仓门边、侧身看他、往后让半步；所有人都不看镜头",
      act="0–4s 高位：纲船靠岸，跳板上一个接一个的人扛着袋子下船；4–8s 队伍走进仓门，仓前人挤成一片；8–12s 李十六扛着袋子走过来，身体前倾、脚步稳，林问往后让半步；12–15s 他把袋子放到地上，直起腰喘气；15–18s 他抹一把汗，林问看着他肩上垫的旧布；18–24s 他弯腰把刚放下的那袋重新扛上肩，走进仓门",
      lines=[L(0, "画外", "城里汴河边的仓前码头。东南运来的粮食，全靠汴河进京。", "A granary wharf inside the city. Southeast grain all comes in on this river.", 5, "travel.003", "解说", "中", "靠岸的纲船"),
             L(5, "画外", "景德四年定下的数：一年六百万石。", "Quota set in 1007: six million dan a year.", 3.5, "travel.001", "报数", "中", "排队扛袋的队伍"),
             L(8.5, "画外", "扛袋的叫「袋家」，一个人肩上扛两石的布袋。仓里一发粮，门口就挤成集市，书上叫「仓前成市」。",
               "The porters were called daijia, two dan on each shoulder. When the granary paid out, a market formed at the gate.", 8.5, "job.001", "解说", "中", "走过来的李十六"),
             L(18, "画外", "想雇人不用上街拉，各行都有「行老」管着，找他就行。", "Need workers? Every trade had a hanglao who found them for you.", 5.0, "job.005", "补充", "中", "李十六肩上垫的旧布")],
      light="巳时，上午顶侧光，粗布袋的织纹清楚，脚夫脸上有汗光，仓门口有檐影，河面反光",
      pace="远（队伍）→ 近（一个人一趟活）→ 放 → 喘 → 再扛",
      spatial="机位＝码头高位（固定）→ 仓门口侧面（固定）；在画主体＝纲船与扛袋队伍 → 李十六与仓门；扛袋的人自画左向画右进仓",
      contrast="首帧＝码头高位远景（远景 0.15）→ 末帧＝李十六把那袋重新扛上肩、林问在旁（中景 0.50）。**一趟扛完，下一趟已经开始。**",
      moment="**13s 他放下袋子直起腰喘气**",
      judge="李十六作沉默面孔（c2，不开口）；重新扛起的是刚放下的那袋，林问早一拍让道（R2-19）；「一人肩上两石布袋」补动词（R1 R36）；时辰定为巳时（tod 3，R4 F02）；工钱当天结没有 fact，不说"),

 dict(n=13, seg="承", sec="人们怎么活动", d=22, bg="bg7_坊巷民居", v="bg7-1", lt="day", tod=3, tier="A", ear=True,
      ch=["c1"], pr=["p2"], unit="我试试", crowd=True, local=True,
      facts=["job.013", "dress.001", "job.018", "cart.004", "money.001", "money.008"],
      jb=(0.20, "全景", 0.55, "中景"), jbcam=("坊巷街口平视全景", "驴右侧中景跟拍"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，递钱用右手，骑上驴后两手抓鞍",
      carry=[WILLOW_NONE],
      cuts=[(0, 8, "街口全景：戴帽披背子的香铺伙计、皂衫角带的当铺管事从她身前走过", "开场"),
            (8, 14, "赁驴人牵驴过来，她伸一根手指比一百、从钱串上捋下一小串递过去", "切"),
            (14, 22, "她骑上驴，晃得抓紧鞍子，转脸看镜头；驴右侧跟拍", "切（换到驴右侧跟拍）")],
      title="【我试试】看行头 · 租一头驴",
      summary="街口：香铺伙计戴帽子披背子、当铺管事皂衫角带——各行衣装一眼认得出；路远，她伸一根手指比一百、租了一头驴，赁驴人牵着缰绳让她上驴，驴一迈步她晃得抓紧鞍子。「鞍马」是马是驴，口播标推测。",
      plot="巳时的坊巷街口，行人穿什么一眼就看出是哪一行：一个头戴帽子、身上披着一件背子的香料店伙计，一个穿皂衫系角带、不戴帽的典当店管事，先后从宋装的林问身前走过；她朝路边牵着一头配鞍的驴的赁驴人招手，伸出一根手指比了个一百，从腰前钱串上捋下一小串铜钱递过去，赁驴人点头收下，牵着缰绳让她上驴；她踩着镫爬上驴背，驴一走她晃得赶紧抓住鞍子",
      cam="0–8s 街口平视全景，眼平，28mm，f5.6，机位固定；8–14s 中景，眼平，35mm，机位固定，她与赁驴人；14–22s 驴右侧中景跟拍，机位高约一米六、眼平，在驴右侧约两米与驴同速，35mm",
      block="0–8s 林问站在画面右侧街边，两名行人自画左向画右从她身前走过、不看镜头；8–14s 赁驴人在画左牵驴、侧身、不说话，只点头；她在画右；14–22s 她骑在驴背上侧对镜头、20–22s 转脸看镜头，赁驴人牵着缰绳在驴头前走；所有当地人都不看镜头",
      act="0–4s 戴帽子、披着背子的香料店伙计从她身前走过；4–8s 皂衫角带的典当店管事走过，她回头看；8–10s 她朝赁驴人招手，伸出一根手指比一百；10–12s 从腰前钱串上捋下一小串铜钱递过去，赁驴人点头收下；12–14s 赁驴人牵着缰绳，让她踩镫；14–17s 她爬上驴背；17–20s 驴一迈步，她晃了一下，赶紧两手抓住鞍子；20–22s 抓着鞍子慌慌地转脸看镜头说话",
      lines=[L(0, "画外", "看衣服就知道干哪行。书上说「各有本色，不敢越外」：香铺的伙计戴帽子、披背子，当铺管事穿黑衫系角带，不戴帽。",
               "You can tell a trade by its clothes. Incense-shop hands wear a cap and cape; pawnshop managers wear black with a horn belt, no cap.", 10.0, "job.013 dress.001", "跟着看", "中", "从身前走过的两个行人"),
             L(10, "画外", "路远走不动？街口就能租鞍马，书上说「不过百钱」。", "Too far? Corner stands rent mounts, under a hundred wen.", 4, "job.018", "解说", "中", "赁驴人和驴"),
             L(14, "画外", "书上写的是鞍马，没说是马是驴，我挑了头驴——这个算推测。", "The book says saddle animals, not horse or donkey. A donkey's my guess.", 5.0, "cart.004", "嘀咕", "中", "驴背上的鞍子"),
             L(20, "对镜", "哎，哎——它自己会走。", "Whoa — it just goes!", 2.0, "", "抓紧鞍子", "快")],
      light="巳时，上午顶侧光，街面有屋檐的影，驴身上的鞍具有柔和高光",
      pace="看（行人）→ 招手 → 比一百 → 递钱 → 骑上 → 晃",
      spatial="机位＝街口全景（固定）→ 中景（固定）→ 驴右侧跟拍；在画主体＝过路的两个行人 → 她与赁驴人 → 骑驴的她；行人自画左向画右，驴向画右前进",
      contrast="首帧＝街口两个不同行当的人从她身前走过（全景 0.20）→ 末帧＝她在驴背上抓紧鞍子看镜头（中景 0.55）。**看完别人的行头，自己租了头驴。**",
      moment="**18s 驴一迈步她晃一下抓紧鞍子**",
      post="驴钱一百文记进 shot32 总账",
      judge="「背上披着布」是「顶帽披背」的误读，改为披背子（R6 W13 / R1 R37）；缰绳不交给她、赁驴人牵着走（R5 F15）；驴在跟拍画面里向画右（R2-20）；对镜台词那一拍转脸看镜头；钱从手巾下钱串上捋下（R2-20）；「鞍马」原文没分马驴，口播标推测"),

 dict(n=14, seg="承", sec="医馆", d=26, bg="bg10_赵太丞家", v="bg10-1", lt="day", tod=3, tier="A",
      ch=["c1"], pr=[], unit="看", local=True,
      facts=["medic.001", "medic.002", "medic.003", "medic.006", "medic.009", "medic.010", "medic.014", "medic.007"],
      jb=(0.15, "远景", 0.50, "中景"), jbcam=("赵太丞家街对面平视", "门前立招旁略仰中景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，下驴时扶鞍，缰绳递还赁驴人",
      carry=[WILLOW_NONE, DONKEY_BACK],
      cuts=[(0, 8, "街对面远景：街市最后一家，门前柳树，檐下横匾，门两侧高高的立招；她骑驴入画", "开场"),
            (8, 26, "立招旁中景：她下驴、还驴，仰头看立招，病人进出", "切（换到门前）")],
      title="【医馆】赵太丞家 · 比屋檐还高的招牌",
      summary="骑驴到「赵太丞家」门前：檐下浅色横匾，门两侧两块比屋檐还高的立招（画面无字）。她下驴、把驴还给赁驴人，念出立招上的两句成药广告，讲太丞大概是太医局的丞、汴京医家爱把头衔挂上招牌；「三进院」是解读，口播标推测。",
      plot="巳时，汴京城里一条街的尽头，一家叫赵太丞家的医馆，门前有柳树，檐下两根门柱之间横挂一块浅色木匾，门两侧各立一块比屋檐还高的竖长木立招，匾和立招上都是空白的；宋装的林问骑着驴、赁驴人牵着，到门前停下，她下了驴，把缰绳交还，赁驴人牵着驴走开；她仰头看两块立招；一名抱着孩子的妇人从她身边走进门去",
      cam="0–8s 街对面平视远景，眼平，35mm，f8，机位固定，医馆门面与两块立招完整入画；8–26s 切到门前立招旁，眼平略仰，35mm，f4：8–13s 极缓上摇到立招上半截；13–17.5s 摇回她的脸；17.5–26s 机位不动",
      block="0–8s 赁驴人牵着驴在前、她骑在驴上自画右入画、向画左走到门前停住；8–26s 她站在画右立招下仰头看，说那句对镜台词时转回脸看镜头；赁驴人牵着驴从画左走出画；病人进出门口，不看镜头、不说话",
      act="0–4s 远景：门前柳树、横匾、两块立招，行人经过；4–8s 她骑驴自画右入画，停在门前；8–10s 她先扶着鞍子下驴站稳，把缰绳递还赁驴人，赁驴人牵着驴转身走开；10–13s 她走到立招下，仰头从上往下看左右两块立招；13–17.5s 转回脸，笑着正脸看镜头说话；17.5–22s 再仰头细看右边那块；22–26s 一名抱着孩子的妇人从她身边走进门，她侧身让开",
      lines=[L(0, "画外", "画卷最左边、城里最后一家店，就是这家「赵太丞家」。", "Far left of the scroll, the last shop in town: Zhao Taicheng's.", 4.5, "medic.001 medic.002", "指给你看", "中", "街对面医馆的门面"),
             L(4.5, "画外", "门口两块立招比屋檐还高，一块写「治酒所伤真方集香丸」，一块写「大理中丸医肠胃」。",
               "Two signs taller than the eaves: one sells pills for hangovers, one for stomach trouble.", 8.5, "medic.003", "念招牌", "中偏慢", "两块立招"),
             L(13, "对镜", "专门给喝酒喝伤的人立一块招牌。看病、卖成药，一家全包。", "A whole sign just for hangovers. Doctor and pharmacy in one.", 4.5, "medic.006", "笑"),
             L(17.5, "画外", "太丞，大概就是太医局里的丞，医家爱把头衔挂上招牌。说这家有三进院子的，是推测。",
               "Taicheng was probably a medical bureau title; doctors liked titles on signs. The three courtyards are a guess.", 7.0, "medic.009 medic.010 medic.014 medic.007", "解说", "中", "右边那块立招")],
      light="巳时，上午的日光自画右照来，立招木板受光，檐下偏暗，柳树影落在门前",
      pace="远（门面）→ 到 → 下驴还驴 → 仰看 → 对镜 → 让路",
      spatial="机位＝街对面远景（固定）→ 门前立招旁略仰（上摇再摇回）；在画主体＝医馆门面 → 仰头的她与立招；她自画右骑驴到门前，与上一镜骑驴方向一致",
      contrast="首帧＝街对面看整座门面（远景 0.15）→ 末帧＝她在立招下侧身给病人让路（中景 0.50）。**两块比房子还高的广告牌。**",
      moment="**15s 她转回脸笑着对镜说招牌**",
      post="「赵太丞家」木匾与两块立招在画面里一律无字（生成模型不写字），字由后期贴原画字样；立招内容由她口播",
      judge="「医肠胃冷」只是一家释读，未核原画前按光明日报读「医肠胃」（R6 W14）；「太丞」补 medic.010 并改为「大概就是」（R6 W14 / R1 R14）；驴在本镜还掉、此后步行（R5 F15 / R2-22）；骑驴方向接上一镜向画右（R3-29 取「自画右入画」）；对镜台词摇回脸（R2-21）；时长 24→26 s（R3-12）"),

 dict(n=15, seg="承", sec="医馆", d=26, bg="bg10_赵太丞家", v="bg10-2", lt="day", tod=3, tier="A",
      ch=["c1"], pr=[], unit="看", indoor=True, local=True, neg_add="太师椅",
      facts=["medic.005", "medic.013", "medic.021", "medic.033"],
      jb=(0.20, "全景", 1.50, "特写"), jbcam=("店堂门里侧全景", "怀里孩子小手特写"),
      hands="右手话筒垂在身侧、左手采访本贴在身前",
      carry=[WILLOW_NONE],
      cuts=[(0, 20, "店堂全景：妇人抱着孩子坐着，老先生弯腰看孩子，后面是柜台，旁边一把靠背椅；她站在门里侧不打扰", "开场"),
            (20, 26, "特写：妇人怀里孩子的小手抓着母亲衣襟", "切（换到孩子小手特写）")],
      title="【医馆】店堂里 · 画里的那一幕",
      summary="店堂里就是画卷里那一幕：妇人抱着孩子坐着、身旁的人扶着椅背、老先生弯腰看孩子、后面是柜台。她站在门边不打扰，讲马行街往北成排分科的药铺、政和四年改名的惠民局与和剂局；满墙小抽屉的药柜画里看不出，不编。",
      plot="巳时，赵太丞家的店堂里，后面是一道横着的柜台，旁边一把靠背椅；一位妇人坐着，怀里抱着一个小孩，旁边一人弯腰扶着椅背跟着看孩子；对面一位上了年纪的先生弯下腰看孩子；宋装的林问站在门里侧，远远看着，不上前；孩子的小手抓着母亲的衣襟",
      cam="0–20s 门里侧全景，眼平，28mm，f4，机位极缓推近约半米，整间店堂入画；20–26s 切到孩子小手特写，略俯，85mm，f2.8，机位固定",
      block="妇人坐在画面中央偏左、抱着孩子；老先生在画右、弯腰朝孩子；另一人站在妇人身旁，弯腰扶着椅背、跟着看孩子的脸；柜台在画面后方横贯；林问在画面左前方门边、侧身朝店堂、不上前；所有当地人都不看镜头、不说话",
      act="0–7s 全景：妇人抱着孩子坐着，老先生弯腰看孩子的脸；7–13s 他看了一会儿，轻轻点头，妇人身旁的人跟着轻轻松一口气；13–20s 林问站在门边一动不动，把采访本贴在身前；20–23s 特写：孩子的小手抓着母亲衣襟，轻轻动了动；23–26s 母亲的手覆上孩子的小手",
      lines=[L(0, "画外", "画里就是这一幕：妇人抱着孩子坐着，老先生弯腰给孩子看病，后面是柜台。", "Just like the painting: a mother and child, an old man bending to look, a counter behind.", 6.5, "medic.005", "轻声", "中", "弯腰看孩子的老先生"),
             L(6.5, "画外", "马行街往北，一整排医官开的药铺，还分科：看口齿咽喉的、看小孩的、看生孩子的。",
               "North of Mahang Street, a row of doctors' shops, each with a specialty: throats, children, childbirth.", 6.5, "medic.013", "解说", "中", "店堂后面的柜台"),
             L(13, "画外", "官府也开药局，政和四年起一个叫「惠民局」、一个叫「和剂局」，一个卖药，一个做药。",
               "The state ran pharmacies too. From 1114, one sold medicine, the other made it.", 6.5, "medic.021", "解说", "中", "店堂里的母子"),
             L(20.5, "画外", "满墙小抽屉的药柜？画里看不出，史书没写，我不编。", "Tiny-drawer medicine walls? Not in the painting, not in the records.", 5, "medic.033", "摇头", "中", "孩子抓着衣襟的小手")],
      light="巳时，上午天光从门口照进店堂，门口一侧亮、柜台那边偏暗",
      pace="静（看诊）→ 点头 → 她不动 → 小手",
      spatial="机位＝门里侧全景（极缓推近）→ 孩子小手特写（固定）；在画主体＝整间店堂 → 孩子的手；老先生朝画左的孩子，林问在画左前方侧身朝店堂",
      contrast="首帧＝整间店堂与门边不上前的她（全景 0.20）→ 末帧＝母亲的手覆上孩子的小手（特写 1.50）。**看病这件事，九百年都差不多。**",
      moment="**24s 母亲的手覆上孩子的小手**",
      judge="只画画卷里看得见的：坐着抱孩子的妇人、身旁站立者、弯腰看孩子的老先生、柜台、靠背椅（medic.005）；不画诊脉、碾药、药柜抽屉（medic.033 无证据），百子柜与药碾进负向、补「太师椅」（R6 W17）；身旁站立者不再干站（R2-23）；全景段极缓推近防静帧（R3-13）；时长 24→26 s，第 4 句放宽（R1 R16 / R3-13）；景别档全景 0.20 → 特写 1.50"),
]

S += [
 dict(n=16, seg="转", sec="皇城一线", d=22, bg="bg4_州桥御街", v="bg4-1", lt="day", tod=4, tier="A",
      ch=["c1"], pr=[], unit="行", crowd=True, local=True,
      facts=["route.007", "zhouqiao.001", "route.008", "travel.005", "travel.006"],
      jb=(0.10, "远景", 0.75, "近景"), jbcam=("州桥下游河岸远眺", "桥上栏边近景"),
      hands="右手握话筒；采访本揣进褙子左襟，左手扶栏",
      carry=[WILLOW_NONE],
      cuts=[(0, 8, "州桥全貌：低平青石桥、石梁石笋栏杆、两岸石壁浮雕、桥西方头船与铁索", "开场"),
            (8, 22, "她走上桥扶栏往下看石壁，再抬头看铁索，直起身对镜头说", "切（换到桥上栏边）")],
      title="【皇城一线】州桥 · 石头的桥",
      summary="州桥全貌 → 她扶栏看石壁。画外：正名天汉桥、正对御街、桥低不通大船、青石柱、石壁海马水兽飞云、桥西铁索夜里拦河；她对镜提醒：虹桥是木拱，州桥是石平。",
      plot="午时近午，州桥：一座低平的青石桥几乎贴着水面，石梁搁在石笋形的望柱上，两岸是整面青石壁，刻着海马、水兽和飞云；桥西泊着两只船头竖着铁枪杆的方头浅船，岸上三条粗铁索；宋装的林问走上桥，扶着栏杆往下看石壁，再抬头看桥西的船与铁索",
      cam="0–8s 河岸下游约三十米、眼平略高，28mm，f8，机位固定，桥横贯画面；8–22s 桥上栏边，她身侧一米、眼平，50mm，f2.8，近景，她俯身时机位跟着微微下压",
      block="0–8s 桥上行人剪影可辨不超过八个；8–22s 她在桥中栏边、身体朝画左的河面、侧脸对镜头，视线先落在下方石壁的浮雕上，最后直起身转正脸看镜头；行人从她身后经过、不看镜头",
      act="0–4s 桥全貌，一只平底小船从桥下穿过；4–8s 画面沿石壁浮雕缓缓看过去；8–12s 她走上桥、走到栏边；12–16s 俯身扶栏往下看石壁上的海马；16–17.5s 抬头看桥西的方头船与岸上铁索；17.5–22s 直起身，正脸看镜头说话",
      lines=[L(0, "画外", "州桥，正名「天汉桥」，正对皇城的御街。桥身低平，大船过不去。", "Zhou Bridge, formally Tianhan Bridge, faces the imperial avenue. It sits low; big boats can't pass.", 6, "route.007", "解说", "中", "河上的州桥全貌"),
             L(6, "画外", "桥柱全是青石，两岸石壁上刻着海马、水兽、飞云。", "Bluestone pillars, and the embankments carved with sea horses, water beasts and clouds.", 5.0, "zhouqiao.001", "俯身看", "中", "石壁上的海马浮雕"),
             L(11.5, "画外", "桥西泊着两只方头船，岸上三条铁索，夜里绞起来拦住河，防船丢。", "West side: two flat boats, three iron chains raised at night so boats don't drift off.", 6, "route.008", "解说", "中", "桥西的方头船与铁索"),
             L(17.5, "对镜", "早上那座虹桥是木头拱的，这座是石头平的。", "This morning's bridge was a timber arch. This one's flat stone.", 4.5, "travel.005 travel.006", "直起身", "中", "")],
      light="午时近午的顶侧光，青石桥面发亮，石壁浮雕在侧光里有清楚的阴影，河面反光",
      pace="看（全貌）→ 上桥 → 俯看 → 抬头 → 对镜",
      spatial="机位＝下游河岸远眺（固定）→ 桥上栏边（微跟）；在画主体＝州桥全貌 → 她与栏下石壁；她侧身朝画左的河面，最后转正脸",
      contrast="首帧＝州桥全貌（远景 0.10）→ 末帧＝她扶栏直起身的近景（近景 0.75）。**从桥的样子看到桥上的人。**",
      moment="**14s 她俯身看石壁上的海马**",
      judge="OS 视线跟着讲的东西走、对镜台词单独留出直起身看镜头的一拍（R2-24）；时辰定为午时（tod 4）；景别档落幅近景 0.75（下一镜起幅全景 0.30）"),

 dict(n=17, seg="转", sec="皇城一线", d=26, bg="bg4_州桥御街", v="bg4-1", lt="day", tod=4, tier="A", ear=True, xuande=True,
      ch=["c1"], pr=[], unit="行", crowd=True, local=True, neg_add="人走进朱漆杈子里的御道, 翻越杈子, 扶着朱杈子探身",
      facts=["route.009", "street.001", "route.010", "job.023", "palace.002"],
      jb=(0.30, "全景", 0.10, "远景"), jbcam=("御街朱杈子外侧跟拍", "御道中轴长焦平视"),
      hands="右手话筒垂在身侧、左手采访本贴在腰前",
      carry=[WILLOW_NONE],
      cuts=[(0, 16, "她走在朱漆杈子外侧，杈子里的御道空着，御沟冒着小荷叶", "开场"),
            (16, 26, "御道中轴长焦：两行朱杈子压成平行线，焦点从近处开裂的朱漆拉到路尽头的宣德楼", "切（换到长焦远望）")],
      title="【皇城一线】御街 · 中间不能走",
      summary="御街两百多步宽：黑漆杈子、中间两行朱漆杈子围出御道，「中心御道，不得人马行往」；她沿朱杈子外侧走、隔着杈子看一眼、不跨进去；御沟里种着荷，岸边桃李梨杏，书上说「春夏之间，望之如绣」；长焦下宣德楼在热霭尽头清楚起来。",
      plot="午时近午，御街往北：一条两百多步宽的大街，两边御廊前是黑漆杈子，路中间两行朱漆杈子围出空无一人的御道，杈子里两道砖石御沟，水面只浮着刚冒出来的小荷叶，岸边桃李开着白花和淡粉花；宋装的林问走在朱漆杈子外侧的行人道上，朱杈子就在她右手边一步远，她隔着朱杈子看了一眼御道，身体和手都不越过杈子；路的尽头，宣德楼的轮廓在热霭里",
      cam="0–16s 她右后方约两米侧跟，眼平，35mm，f4，与她同速向北；16–26s 切到御道正中轴线、离地约一米六平视，200mm 长焦，f8，机位固定：两行朱漆杈子与两道御沟被压成向画面深处收束的平行线，热霭让远处一层比一层淡，宣德楼浮在御道尽头；16–21s 焦点在前景约三米处一截朱漆杈子上，21–26s 焦点缓缓拉到路尽头的宣德楼，前景杈子虚成一块朱红色块",
      block="0–16s 她在画面左侧沿朱漆杈子外侧向北走、背对或侧对镜头，朱杈子在她右手边一步远；她的身体和手始终在朱杈子外、不扶不跨；10–12.5s 转脸看镜头；行人都在杈子外的廊下走、可辨者不超过八个、不看镜头；16–26s 无具名人物特写，画面里只有杈子、御沟与远处的宣德楼",
      act="0–5s 她沿朱杈子外侧向北走；5–10s 停下，侧头看一眼空着的御道；10–12.5s 转过脸看镜头说话（镜头在她右后方）；12.5–16s 隔着朱杈子低头看御沟里的小荷叶，不探身越过杈子，然后继续向北走；16–21s 长焦：前景一截朱杈子开裂的旧漆清清楚楚，御道向北伸；21–26s 焦点拉远，宣德楼在热霭里从模糊变清楚",
      lines=[L(0, "画外", "御街，从宣德楼往南，宽两百多步。", "The imperial avenue: over two hundred paces wide.", 3, "route.009", "解说", "中", "向北伸去的御街"),
             L(3, "画外", "两边黑漆杈子，中间两行朱漆杈子，书上写「中心御道，不得人马行往」。", "Black barriers on the sides, two red rows in the middle. The center lane: no people, no horses.", 6.5, "route.009 street.001", "解说", "中", "空着的御道"),
             L(10, "对镜", "所以我走外头。规矩就是规矩。", "So I walk outside. Rules are rules.", 2.5, "", "侧头看御道"),
             L(13, "画外", "杈子里两道砖砌的御沟，宣和年间种了荷花，岸边是桃李梨杏，书上说「春夏之间，望之如绣」。", "Inside, two brick channels planted with lotus, peach and plum on the banks — like embroidery in spring, the book says.", 7.5, "route.010", "低头看", "中", "御沟里的小荷叶"),
             L(20.5, "画外", "早朝那会儿，御街到州桥这一段，卖药卖吃的吆喝声不断。", "At dawn, vendors cried their wares all the way to Zhou Bridge.", 5, "job.023", "解说", "中", "路尽头的宣德楼")],
      light="午时近午顶侧光，朱漆杈子是这一天里最饱和的朱红偏橙、旧漆开裂处露出木色，黑漆杈子是哑光皂黑；御沟水面碧绿、映着蓝天；街面上被车马扬起一层很低的淡黄细尘",
      pace="走 → 停（看御道）→ 对镜 → 看荷叶 → 远（长焦宣德楼）",
      spatial="机位＝她右后方侧跟 → 御道中轴长焦平视（固定）；在画主体＝朱杈子外侧的她与空御道 → 御街纵深与宣德楼；她自南向北走在画面左侧",
      contrast="首帧＝朱杈子外侧行走的她（全景 0.30）→ 末帧＝长焦尽头清楚起来的宣德楼（远景 0.10）。**不走中间，照样走到它跟前。**",
      moment="**24s 焦点拉远，宣德楼在热霭尽头清楚起来**",
      judge="她沿朱漆杈子外侧走（route.009「行人皆在廊下朱杈子之外」），身体和手不越杈子（R2-25）；对镜台词转脸看镜头（R2-26）；清明物候不断言，改引「春夏之间，望之如绣」（R6 W15），画面小荷叶是调度选择；「鲜红」改锁定色名、薄雾改热霭、长焦压缩（R4 F10 / F11）；末段远看宣德楼，按宣德楼例外删「琉璃瓦 / 红柱金匾」并挂 bg12 负向组（R6 W16）；决定性瞬间挪到镜尾（R2-04）"),

 dict(n=18, seg="转", sec="皇城一线", d=26, bg="bg12_宣德楼", v="bg12-1", lt="day", tod=4, tier="A", xuande=True,
      ch=["c1"], pr=[], unit="看", crowd=True, local=True,
      facts=["palace.002", "palace.003", "palace.004", "palace.005", "palace.007"],
      jb=(1.30, "特写", 0.75, "近景"), jbcam=("宣德门朱漆门扇金钉特写", "她身后低位过肩仰拍城楼"),
      hands="右手话筒垂在身侧、左手采访本贴在腰前",
      carry=[WILLOW_NONE],
      cuts=[(0, 4, "朱漆门扇上一排排暗哑的铜金色门钉特写", "开场"),
            (4, 12, "宣德楼正面大远景：五门墩台、单檐庑殿门楼、朵楼与阙楼；她自画面下方走入", "切（拉到楼前广场正中）"),
            (12, 26, "她身后过肩仰拍：她仰头，城楼压满画面上方", "切（换到她身后低位）")],
      title="【皇城一线】宣德楼 · 皇城正门",
      summary="**本站 hero 之一。** 门钉特写 → 宣德楼正面大远景 → 她身后过肩仰拍：五门洞、朱漆金钉、龙凤飞云墩台、单檐庑殿绿琉璃瓦、朵楼阙亭；书上说雕梁画栋、学者说木构只刷土红，两说可能不是同一处，是推测；她得把脖子仰到头才看得全。",
      plot="午时，宣德楼正前方：朱漆门扇上一排排暗哑的铜金色门钉；一座高大的砖石墩台上开着五个门洞，墩台壁面砖石相间，雕着龙凤和飞云；台上是单檐庑殿顶的门楼，屋顶是发暗的深绿琉璃瓦，正脊两端立着鸱吻，檐下是很大的斗拱，木构只刷土红、不画满彩画；门楼两侧曲尺形的朵楼，朵楼向前伸出长廊连着两座阙楼，整体围成凹字形；楼前朱红杈子围隔；宋装的林问走到楼前站定，仰头看",
      cam="0–4s 门扇金钉特写，眼平略仰，85mm，f4，机位固定；4–12s 楼前广场正中、眼平，24mm，f8，机位固定，整座城楼与两侧阙楼完整入画、人在画面底部很小，门洞前的禁卫剪影只有门扇的四分之一高；12–26s 切到她身后约一米、低位仰角二十度，35mm，f5.6，她的后脑与肩在画面下方，城楼压满画面上方，机位极缓上摇到正脊",
      block="4–12s 楼前广场上零星行人为剪影、不可辨面孔，门洞前远远站着两排禁卫、只是小小的剪影；12–26s 她在画面下方正中背对镜头仰头，全程不回头看镜头；所有当地人都不看镜头",
      act="0–4s 特写：门钉在侧光里一颗颗凸起，朱漆有细细的开裂；4–8s 大远景静止，旗与树梢微动；8–12s 她自画面下方走入，站定；12–17s 过肩仰拍：她仰起头；17–22s 机位极缓上摇，从门洞看到门楼斗拱；22–26s 摇到正脊两端的鸱吻，她仍仰着头、慢慢侧过半张脸看向鸱吻，嘴不动",
      lines=[L(0.5, "画外", "宣德楼，皇城正门。五个门洞，朱漆门扇钉着金钉，墩台上雕着龙凤飞云。", "Xuande Tower, the palace's front gate. Five doorways, red lacquer, gold studs, dragons and clouds carved on the base.", 8.0, "palace.002", "仰头", "慢", "门扇上的金钉"),
             L(8.5, "画外", "屋顶单檐，绿琉璃瓦，两边是朵楼——照宋徽宗画的《瑞鹤图》复原的。", "A single-eave roof of green glazed tile, side towers — rebuilt from Emperor Huizong's Auspicious Cranes.", 6.0, "palace.003 palace.004", "解说", "中", "整座城楼"),
             L(14.5, "画外", "书上说雕梁画栋，学者照画说木头只刷土红。两边说的可能不是同一处，这是推测。",
               "The book says painted beams; scholars reading the painting say plain red timber. They may mean different parts. My guess.", 7.5, "palace.007", "实话", "中", "门楼的斗拱"),
             L(22.5, "画外", "我得把脖子仰到头，才看得全。", "Head all the way back just to see it.", 3.5, "", "仰着头，轻", "中", "正脊两端的鸱吻")],
      light="午时的日光自画右偏高处照来，墩台壁面的浮雕有清楚的阴影；琉璃瓦面是哑光的深绿、只在瓦垄上有一线细高光、不发光；门扇是发暗的朱红偏橙，门钉是暗哑的铜金色、不反光；楼前广场被车马踩起的极薄黄土尘，让城楼比近处的人淡一层",
      pace="特写（门钉）→ 远（整座城楼）→ 走入 → 仰 → 上摇 → 侧脸",
      spatial="机位＝门扇特写（固定）→ 楼前广场正中远景（固定）→ 她身后低位仰拍（极缓上摇）；在画主体＝门钉 → 宣德楼全貌 → 她的背影与压在头顶的城楼；她背对镜头面朝正北的城楼",
      contrast="首帧＝朱漆门扇上的门钉特写（特写 1.30）→ 末帧＝她仰头侧脸、城楼压满画面上方（近景 0.75）。**站在它跟前，才知道什么叫皇城。**",
      moment="**24s 摇到正脊鸱吻、她侧过半张脸**",
      judge="上一镜落幅是长焦远望同一座楼，两端都是远景会读成跳变，按 rule 16.5 拆出门钉特写开场（R3-05，接缝 0.10/1.30 = 0.08）；太极门一句删掉——palace.006 注明口播不讲太极门（R1 R07），末句改画外（R2-27）；雕梁画栋与土红两说改为「可能不是同一处」（R1 R19）；琉璃瓦与门钉不写成发光、补尘与尺度参照（R4 F08 / F09）；宣德楼例外同时删「琉璃瓦」「红柱金匾」（R4 F07）；时长 24→26 s（R3-14）"),

 dict(n=19, seg="转", sec="皇城一线", d=28, bg="bg12_宣德楼", v="bg12-2", lt="day", tod=4, tier="A", xuande=True,
      ch=["c1"], pr=[], unit="看", crowd=True, local=True, neg_add="殿内陈设, 屏风宝座, 进膳宫女特写",
      facts=["palace.019", "palace.008", "palace.009", "palace.013", "palace.015", "palace.020"],
      jb=(0.30, "全景", 0.12, "远景"), jbcam=("宣德门门洞内侧平视", "大庆殿殿庭高位远景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手交叠贴在身前，什么都不碰",
      carry=[WILLOW_NONE],
      cuts=[(0, 10, "门洞内侧：她放轻脚步穿过门洞走进来", "开场"),
            (10, 28, "殿庭高位远景：大庆殿台基、廊庑、殿庭里两座报时小楼，东边廊庑方向远远有人下马步行", "切（换到殿庭高位）")],
      title="【皇城一线】进宣德门 · 什么都不碰",
      summary="她放轻脚步穿过门洞：史书里老百姓离宫里最近也就是挤到宣德楼下看热闹，她今天破例、东西一样不碰。殿庭大得能站几万人，两座小楼上太史局看刻漏报时，进门往东那条街的横门前大官下马步行；禁卫平时穿什么史书没写，只远远看；殿里不进。",
      plot="午时，宣德楼的门洞里侧，宋装的林问放轻脚步从门洞走进来，两手交叠贴在身前，什么也不碰；进门是大庆殿前的殿庭，地面开阔得能站下几万人，正北是青砖包边的高大台基，四周一圈长长的廊庑；殿庭里立着两座像寺院钟楼一样的小楼；画面右侧东边廊庑的方向远远有几个人下了马步行；殿前远远站着两排禁卫，只是小小的剪影",
      cam="0–10s 门洞内侧，眼平，28mm，f5.6，机位固定，她自门洞深处走向画面；10–28s 切到殿庭一角高处约十五米，俯角十度，24mm，f8，机位极缓向右平移",
      block="0–10s 她在画面中央、放轻脚步走来、两手交叠贴在身前、不看镜头；10–28s 她是画面左下方小小的背影，站在殿庭边上不往前走；禁卫两排远在殿前、只是剪影、不看镜头；下马的人在画面右上远处的东边廊庑方向",
      act="0–4s 门洞深处，她放轻脚步走进来；4–10s 她走出门洞，停住，抬头环视，两手交叠贴在身前；10–16s 高位：空旷的殿庭、正北的台基与廊庑；16–22s 画面扫过殿庭里两座小楼；22–28s 画面右侧东边廊庑方向远远有几个人下马步行，她站在殿庭边上一动不动",
      lines=[L(0, "画外", "说实话，史书里老百姓离宫里最近，也就是挤到宣德楼下看热闹，里头是看不到的。我今天破个例，东西一样不碰。",
               "Honestly, the closest commoners got was crowding under the gate tower at festivals. I'm making an exception today, and touching nothing.", 9.5, "palace.019", "压低声音", "慢", "门洞外的殿庭"),
             L(10, "画外", "一进门就是大庆殿，殿前这院子，大得能站下几万人。", "Inside: the Daqing Hall. This courtyard held tens of thousands.", 4.5, "palace.008", "轻", "中", "空旷的殿庭"),
             L(14.5, "画外", "院里这两座小楼，太史局的人在上面看刻漏，到点就报时。", "Astronomers in those two towers watched water clocks and called the hours.", 5, "palace.008", "轻", "中", "殿庭里的两座小楼"),
             L(19.5, "画外", "进门往东的街上有横门，大官也得在那儿下马走进去。禁卫平时穿什么，史书没写，我只远远看。殿里头，我不进。", "East of the gate, even top officials walked in on foot. Guards' everyday dress? The records don't say. I'm not going in.", 8.5, "palace.013 palace.015 palace.020", "轻", "中", "东边廊庑方向下马的人")],
      light="午时的日光把殿庭晒得发白，台基与廊庑在正北受光，门洞里偏暗",
      pace="进（门洞）→ 停 → 远（殿庭）→ 看（小楼）→ 下马的人",
      spatial="机位＝门洞内侧（固定）→ 殿庭高位（极缓右移）；在画主体＝走进来的她 → 殿庭、台基、廊庑与两座小楼；她自门洞向北走来，停在殿庭南边；横门在进门往东的街上，画面里只在东边廊庑方向远远露出",
      contrast="首帧＝门洞里放轻脚步的她（全景 0.30）→ 末帧＝空旷殿庭边小小的她（远景 0.12）。**站在这里，才知道人有多小。**",
      moment="**25s 远处有人下马步行，她一动不动**",
      judge="palace.019 只记元宵百姓在楼下观看、没有「规矩」条文，改口播为「史书里最近也就是挤到楼下看热闹」（R6 W08，优先于 R1 R11）；横门在「入门东去」的街上，下马挪到画面东边廊庑方向，并补 palace.020（R6 W08）；不进殿、不画殿内（palace.027 ai_draft）；bg12 例外负向照带；时长 26→28 s（R3-15）"),

 dict(n=20, seg="转", sec="官府", d=24, bg="bg11_开封府", v="bg11-1", lt="day", tod=5, tier="A",
      ch=["c1"], pr=[], unit="看", crowd=True, local=True,
      facts=["gov.001", "gov.005", "gov.025", "gov.004", "gov.011", "gov.014", "gov.008"],
      jb=(0.30, "全景", 0.55, "中景"), jbcam=("开封府府门对面街边平视", "府门边中景"),
      hands="右手话筒垂在身侧、左手采访本贴在腰前",
      carry=[WILLOW_NONE],
      cuts=[(0, 8, "府门前街面全景：府门临街，吏人进出，行人往来", "开场"),
            (8, 24, "府门边中景：她站在街边看府门，一个吏人抱着文书从她身边走进去", "切（换到府门边）")],
      title="【官府】开封府门前 · 包拯来不了",
      summary="开封府在皇城西南、尚书省南边，府门临街；管京城官司、捕盗、户口赋税。1104 年改制后长官叫开封尹，宣和二年是谁在任没查到确切的，不点名；府门长相是照宋代州府的格局推测（全片只在这里说一次）；想见包拯——他去世五十多年了。",
      plot="未时的午后，皇城西南的开封府，府门临着街，门口是开放的街面，行人照常往来；几个吏人抱着文书进出府门；宋装的林问站在街边看着府门，一个吏人抱着一叠文书从她身边走过进了门，她侧身让开",
      cam="0–8s 府门对面街边平视全景，眼平，28mm，f5.6，机位固定，府门居中；8–24s 切到府门边，眼平，35mm，f4，机位固定，她在画右、府门在画左",
      block="0–8s 无具名人物特写，行人与吏人可辨者不超过八个、不看镜头；8–24s 她在画右街边、侧身朝画左的府门，说对镜台词时转脸看镜头；吏人自画右走过她身边进门，不看镜头、不说话；府门口没有人拦她",
      act="0–4s 府门前街面，行人往来；4–8s 两个吏人抱着文书走进府门；8–12s 她站在街边抬头看府门；12–16s 一个吏人抱着一叠文书从她身边走过，她侧身让开；16–20s 她望着吏人进门的背影；20–24s 她回头望一眼府门里，转脸看镜头说话、笑着摇摇头",
      lines=[L(0, "画外", "开封府，在皇城西南、尚书省南边，离宣德楼不远。", "Kaifeng Prefecture: southwest of the palace, south of the Secretariat.", 4.0, "gov.001", "解说", "中", "临街的府门"),
             L(4, "画外", "京城里打官司、抓贼、户口赋税，都归它管。", "Lawsuits, thieves, households, taxes — all theirs.", 3.5, "gov.005", "解说", "中", "进出府门的吏人"),
             L(7.5, "画外", "长官叫开封尹，不叫知府；宣和二年是谁在任，我没查到确切的，不瞎说。", "The head: the Kaifeng yin. The 1120 holder — I didn't find him, so no name.", 5.5, "gov.025 gov.004", "实话", "中", "府门上方的屋檐"),
             L(13, "画外", "开封府长什么样没有留下画，这府门是照宋代州府的格局推测的。", "No picture of this office survives. The gate is my guess, based on other Song prefectures.", 6.0, "gov.011 gov.014", "实话", "中", "从身边走过的吏人"),
             L(20.5, "对镜", "想来见包拯？别找了，他去世五十多年了。", "Looking for Judge Bao? He's been dead fifty-some years.", 3.5, "gov.008", "摇头笑")],
      light="未时的午后日光自画左偏高处照来，府门檐下一道影，街面晒得发白",
      pace="看（府门）→ 让路 → 望 → 对镜 → 摇头",
      spatial="机位＝府门对面全景（固定）→ 府门边中景（固定）；在画主体＝府门与街面 → 她与进门的吏人；她侧身朝画左府门",
      contrast="首帧＝府门前街面全景（全景 0.30）→ 末帧＝她在府门边笑着摇头（中景 0.55）。**找包青天的，都来晚了。**",
      moment="**22s 她转脸对镜说包拯、摇头笑**",
      judge="1120 年长官称开封尹（gov.025 / gov.002）；在任者姓名是本站没查到，不是史书没写（R6 W07）；类比格局的推测口播只在本镜说一次（协调者裁定 3）；第 4 句放宽时长（R1 R15 / R3-16）；吏人进门后她望背影、镜尾回头看府门（R2-28）；时辰定为未时（tod 5）"),

 dict(n=21, seg="转", sec="官府", d=26, bg="bg11_开封府", v="bg11-2", lt="day", tod=5, tier="A",
      ch=["c1"], pr=["p2"], unit="看", crowd=True, local=True, fall=("铜钱",), cuts_elide=True,
      facts=["gov.025", "gov.013", "ent.014", "money.001"],
      jb=(0.20, "全景", 0.15, "远景"), jbcam=("开封府内门里侧沿中轴平视", "府前街市关扑摊高位远景"),
      jbnote="换 plate：府内庭院 → 府门外街市，机位由院内平视换到街边高位",
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，最后按一按手巾下的钱串",
      carry=[WILLOW_NONE],
      cuts=[(0, 12, "内门里侧：她穿过府门走进庭院，庭院尽头是正厅，两侧廊房里吏人伏案", "开场"),
            (12, 26, "府门外街市高位：几处关扑摊围着人，瓦盆里掷铜钱，她站在人群外看", "切（换到府门外街市高处）")],
      title="【官府】进开封府 · 门外清明放关扑",
      summary="她穿过府门走进庭院：正厅、廊房、抱文书的吏人；1104 年改制后府里是开封尹、左右少尹，下面分士户仪兵刑工六曹，刑曹户曹最忙。镜内一切到府门外：寒食清明这几天开封府放开「关扑」，路边掷铜钱赌东西，她只看不下场。",
      plot="未时的午后，宋装的林问穿过开封府敞开的府门，走进内门，庭院方整，尽头正中一座宽大的厅堂，两侧长长的廊房里吏人伏在长案前抄写，一个吏人抱着一摞卷册穿过庭院；画面一切，是府门外的街市，路边几处关扑摊：地上摆着瓦盆和几件拿来赌的梳子、花朵、小玩物，有人把几枚铜钱往瓦盆里一掷，围着的人伸头看钱面，有人赢了拿起一件小物件；林问站在人群外面看，有人朝她招一招手，她笑着摆摆手，不下场",
      cam="0–12s 内门里侧沿中轴平视，眼平，28mm，f5.6，机位极缓前推，她自画面下方走入庭院、背影朝正厅；12–26s 切到府门外街边高处约八米、俯角二十度，35mm，f5.6，机位极缓后拉，关扑摊在画面中下部，开封府府门在画面上方",
      block="0–12s 她自画面下方沿中轴走进庭院、背对镜头，停在庭院前段不再往前，不进厅堂；廊房吏人伏案、不看镜头、不说话；12–26s 关扑摊围着的人可辨不超过八个、都低头看瓦盆、不看镜头、不说话；林问在画右人群外侧，侧身朝摊子",
      act="0–4s 她穿过内门走进庭院；4–8s 一个吏人抱着一摞卷册从她前面穿过庭院，她停步让开；8–12s 她站在庭院前段望着正厅，两手空着，不往前走；12–16s 府门外高位：街边几处关扑摊各围着一圈人，一只手把几枚铜钱掷进瓦盆，铜钱在盆里转两圈停下；16–20s 有人赢了，拿起一把梳子，旁边的人拍他肩膀；20–23s 一个摊主朝人群外的林问招一招手（不出声），她笑着摆摆手；23–26s 她隔着衣服按一按腰前手巾下的钱串，站在人群外看着",
      lines=[L(0, "画外", "进来看看。宣和年间，府里是开封尹，下面左右两个少尹。", "Let's go in. A yin ran it, with two deputies, left and right.", 5, "gov.025", "轻", "中", "庭院尽头的正厅"),
             L(5, "画外", "办事分六曹：士户仪兵刑工，打官司的刑曹、管户口田产的户曹最忙。", "Six bureaus did the work; the criminal and household bureaus were the busiest.", 6.5, "gov.025", "解说", "中", "廊房里伏案的吏人"),
             L(12.5, "画外", "关扑，就是掷铜钱赌东西。寒食清明这几天，开封府放开让玩。", "Guanpu: toss coins, win a prize. For Cold Food and Qingming, it was allowed.", 5, "gov.013", "解说", "中", "瓦盆里转着的铜钱"),
             L(17.5, "画外", "彩头是梳子、花朵、小玩物，往瓦盆里掷铜钱来赌。我只看，不下场。", "Prizes are combs, flowers and trinkets, won by tossing coins in a basin. I'm only watching.", 6.0, "ent.014 gov.013", "笑", "中", "朝她招手的摊主")],
      light="未时的午后日光自画左偏高处照来，庭院地面晒得发白、廊房檐下是灰凉的阴影；府门外瓦盆里的铜钱有一点反光，人群投下短影",
      pace="进（庭院）→ 让路 → 望 → 切 → 掷 → 赢 → 她只看",
      spatial="机位＝内门里侧沿中轴平视（极缓前推）→ 府门外街边高位（极缓后拉）；在画主体＝庭院与正厅、伏案的吏人 → 街边几圈关扑的人与府门；她先在庭院前段背对镜头，再在画右人群外侧",
      contrast="首帧＝她走进开封府庭院的背影（全景 0.20）→ 末帧＝府门外关扑摊几圈人与人群外的她（远景 0.15）。**府里忙着审案，府门外过节放开玩三天。**",
      moment="**21s 摊主朝她招手，她笑着摆手**",
      judge="按协调者裁定 3：她真的走进开封府院子（bg11-2），推测口播只在 S20 说一次，本镜不重复；官名只用 1104 年改制后的开封尹、少尹、六曹（gov.025，W12 登记），不说判官推官、不说小事在厢里判（R6 F08）；删去「一贯钱撑到晚上」重复句（R5 F11 / R1 R05）；「钱面朝上算赢」无 fact 支撑，不说；两段是不同地点，镜内切省略出府门的过程；她在人群外摆手不开口（R2-29）；p2 钱串只挂 money.001，不挂 ⚠️ 的 money.008（本镜无推测口播，裁定只在 S20 推测一次）；两端景别 0.20 → 0.15，与上一镜 0.55 / 下一镜的切口由生成器校验"),
]

S += [
 dict(n=22, seg="转", sec="文人", d=24, bg="bg13_相国寺", v="bg13-1", vx=[("bg13-2", "8–24s 资圣门前书画摊")], lt="day", tod=5, tier="A",
      ch=["c1"], pr=[], unit="看", crowd=True, local=True, cuts_elide=True,
      facts=["literati.011", "literati.001", "literati.005", "literati.026"],
      jb=(0.35, "全景", 0.80, "近景"), jbcam=("相国寺东门大街平视全景", "资圣门前书摊侧前方近景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着翻书",
      carry=[WILLOW_NONE],
      cuts=[(0, 8, "寺东门大街全景：一溜卖幞头、腰带、书籍的铺子", "开场"),
            (8, 24, "资圣门前书摊：糨糊粘背的册子、系带的卷轴、经折本混摆，她拿起一本册子翻开又放回，对镜头说", "切（换到资圣门前书摊）")],
      title="【文人】大相国寺 · 书铺和书画摊",
      summary="相国寺东门大街上幞头腰带铺挨着书铺；要是赶上开集，大殿后资圣门前全是书籍、古玩、图画摊；开集日两说对不上，清明赶没赶上史书没写。摊上的书是糨糊粘背的蝴蝶装册子、卷轴和经折本，还没有线装；她翻一本看不懂的册子。",
      plot="未时的午后，大相国寺东门外的大街上，一溜店面卖幞头、腰带、书籍和冠朵；进了寺，大殿后面资圣门前摆着卖书籍、古玩、图画的摊子，摊板和草席上混摆着一叠叠对折后糨糊粘背、书背上看不到订线的薄册子，几卷系着带子的卷轴，一两本一折一折叠起来的经折本；宋装的林问在一个书摊前拿起一本册子，两页像蝴蝶翅膀一样向左右展开，她看了看，又轻轻放回去",
      cam="0–8s 东门大街平视全景，眼平，28mm，f5.6，机位固定；8–24s 切到资圣门前书摊，她侧前方，眼平，50mm，f2.8，近景，机位固定，书页不给特写",
      block="0–8s 行人与铺主可辨者不超过八个、不看镜头、不说话；8–24s 她在画面中央书摊前、侧身朝画左的摊子，说对镜台词时转正脸看镜头；摊主坐在摊后，抬眼看她一下又低下头，不看镜头；书页与卷轴上没有可读的字",
      act="0–4s 东门大街上人来人往，店门口挂着幞头与腰带；4–8s 她自画右走过书店门口；8–12s 资圣门前书摊，她拿起一本薄册子，摊主抬眼看她一下又低下头；12–18s 她把册子摊开，两页向左右展开，眉头挑一下；18–20s 把册子轻轻放回去；20–24s 转正脸看镜头说话",
      lines=[L(0, "画外", "大相国寺东门这条街，卖幞头腰带的铺子挨着卖书的。", "By the temple's east gate, hat shops sit next to bookshops.", 4.5, "literati.011", "解说", "中", "街边的书铺和冠带铺"),
             L(4.5, "画外", "要是赶上开集，大殿后面资圣门前全是卖书籍、古玩、图画的摊子。", "On market days, the court behind the hall filled with books, curios and paintings.", 5.5, "literati.001", "解说", "中", "资圣门前的书摊"),
             L(10, "画外", "寺里一个月开几回集，书上两种说法对不上；今天清明赶没赶上，史书没写。", "Sources disagree on how often the market ran, and the records don't say about today.", 6, "literati.005", "实话", "中", "手里摊开的册子"),
             L(16, "画外", "书是糨糊粘背的册子，翻开像蝴蝶；线装还得等几百年。", "Books are glue-bound, opening like butterfly wings. Thread binding is centuries away.", 4.5, "literati.026", "解说", "中", "像蝴蝶一样展开的两页"),
             L(20.5, "对镜", "这本……我看不懂，但纸是真好。", "This one… can't read it, but lovely paper.", 3.0, "", "放回书")],
      light="未时的午后，日光自画左照在东门大街上，资圣门前廊檐下偏暗，册子纸面有柔和的反光",
      pace="街（铺子）→ 进 → 翻册子 → 放回 → 对镜",
      spatial="机位＝东门大街全景（固定）→ 资圣门前书摊近景（固定）；在画主体＝街边书铺 → 翻书的她；她自画右走过书铺",
      contrast="首帧＝东门大街的书铺与冠带铺（全景 0.35）→ 末帧＝她在资圣门前放下册子对镜说话（近景 0.80）。**全城淘书淘画的地方，开在一座寺里。**",
      moment="**15s 册子两页像蝴蝶一样展开，她挑一下眉**",
      judge="线装是明代以后的装帧，摊上改为蝴蝶装册子、卷轴、经折本混摆，不给书页特写，负向挂线装书 / 书脊订线 / 四眼线装 / 函套（R6 F07，W12 登记 literati.026）；「读书人买帽子顺手买书」是编的，删（R6 W10）；资圣门前摊子口播改为「要是赶上开集」，与开集两说对齐（R6 W10）；摊主抬眼看她一下（R2-30）；场景主体 bg13（新卡锁定串，R7 F03），近景段挂 bg13-2（R7 W08 / S2_bg13 D4）；东门街与资圣门前是两处，镜内切省略走进寺的过程"),

 dict(n=23, seg="转", sec="文人", d=24, bg="bg15_园林雅集", v="bg15-1", lt="day", tod=5, tier="A",
      ch=["c1"], pr=[], unit="看", local=True,
      facts=["literati.020", "literati.018", "literati.024", "literati.015", "literati.022", "festival.007", "dress.010"],
      jb=(2.00, "特写", 0.30, "全景"), jbcam=("建盏微距", "园边曲栏外远处全景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；一只手扶着曲栏，另一只手揉小腿",
      carry=[WILLOW_NONE],
      cuts=[(0, 6, "微距：兔毫纹茶盏里点出的白沫高过盏沿，竹茶筅停在盏边", "开场"),
            (6, 24, "园边曲栏外远处全景：池边垂柳下黑漆大案边几位读书人坐在藤墩上，侍童在小茶床边点茶，她站在曲栏外远远看", "切（拉到园边曲栏外）")],
      title="【文人】园池边 · 读书人点茶",
      summary="城郊私园春天放人游赏：池边垂柳下读书人雅集照《文会图》——黑漆大案、藤墩、瓶花、茶床，侍童点茶、白沫高过盏沿；手里是团扇不是折扇；冷知识：汴京挂画的是熟食店、不是茶坊。她站在园边曲栏外远远看，不凑过去。",
      plot="未时的午后，城郊一座春天放人游赏的私家园子，园池岸边两株老垂柳下，一张黑漆大案旁几位穿白细布大袖衫的读书人坐在藤条鼓墩上，案上摆着瓶花和果子；前面一张小茶床，侍童从短直嘴的汤瓶往青黑色兔毫纹茶盏里注水，用竹茶筅击拂，白沫浮起高过盏沿；一位读书人手里拿着圆形素绢团扇；宋装的林问站在园边另一道木曲栏外，扶着栏杆揉了揉小腿，远远看着，不凑过去",
      cam="0–6s 茶盏微距，俯角约三十度、离盏约二十厘米，100mm，f2.8，机位固定；6–24s 切到园边曲栏外离大案约十五步，眼平，50mm，f4，机位固定，雅集在画面中景、她在画面右前方曲栏边",
      block="读书人不超过五个，围坐在画面中景的黑漆大案边、侧身朝案、不看镜头、不说话；侍童在案前小茶床边；林问站在画右前方曲栏外、侧身朝他们、不凑近、不看镜头",
      act="0–3s 微距：竹茶筅在盏里击拂几下后停住，白沫浮起高过盏沿；3–6s 一只手把茶盏端起；6–12s 远处：侍童把茶盏递到案上，一位读书人接过；12–18s 另一位摇着团扇点点头；18–24s 林问在曲栏外扶着栏杆揉了揉小腿，远远看着",
      lines=[L(0, "画外", "宋徽宗写过怎么点茶：青黑色兔毫纹的盏最好，末茶打出白沫，要浮到高过盏沿。", "Emperor Huizong wrote the rules: a dark hare's-fur bowl, tea whisked till foam rises past the rim.", 6.5, "literati.020", "解说", "中", "远处茶床上的茶盏"),
             L(6.5, "画外", "黑漆大案、藤墩、花、茶床，跟《文会图》里画的一个样。", "Lacquer table, rattan stools, flowers, tea stand — just like Literary Gathering.", 4.5, "literati.018", "对照", "中", "池边的黑漆大案"),
             L(11, "画外", "他们手里是团扇，不是折扇。", "Round silk fans, not folding fans.", 2.5, "literati.024", "轻", "中", "读书人手里的团扇"),
             L(13.5, "画外", "还有个冷知识：汴京的茶坊不挂画，挂画的是卖熟食的饭馆，给等菜的人解闷。", "Fun fact: in Kaifeng, teahouses didn't hang paintings. Cooked-food restaurants did, for diners waiting.", 6.5, "literati.015", "好笑", "中", "案边摇团扇的读书人"),
             L(20.5, "画外", "我不凑过去，在这儿歇歇脚。", "I'll keep my distance and rest my feet.", 3, "", "揉腿", "中", "自己揉着的小腿")],
      light="未时的午后，日光从柳枝间斜照到园池边，柳荫下斑驳光斑，案面黑漆有柔和反光，池水微光，茶盏白沫在光里细腻；风炉膛里只有一点暗红炭，没有火苗、不照亮任何东西",
      day_tail="；除了风炉膛里那一点不发光的暗红炭，画面里没有任何火、没有任何暖色人工光源、没有灯笼",
      neg_drop=["火"],
      pace="静（茶沫）→ 递盏 → 摇扇 → 她歇脚",
      spatial="机位＝建盏微距（固定）→ 园边曲栏外远处（固定）；在画主体＝茶盏 → 案边雅集与曲栏外的她；机位朝西北，园池在画面后方",
      contrast="首帧＝白沫高过盏沿的茶盏微距（特写 2.00）→ 末帧＝池边的雅集与曲栏外歇脚的她（全景 0.30）。**画里的雅集，原来是这样喝茶的。**",
      moment="**22s 她在曲栏外揉着小腿远远看着雅集**",
      post="读书人不开口；雅集环境声只有茶筅击拂与风过柳枝",
      judge="主体改挂 bg15_园林雅集（S2_bg13 D3 / 协调者裁定 6）：不再写寺廊、挂画、台阶，改为城郊私园池边、她站在园边曲栏外（literati.022 私园春天放人游赏）；负向补盖碗 / 紫砂壶 / 醒木 / 折扇（R6 W17，走 bg15 组）；台词时长放宽（R1 R17 / R40）；风炉暗红炭按 bg15 卡写死不发光，光线与负向单独放行；决定性瞬间挪到镜尾（R2-04）；景别档起幅茶盏微距 2.00（上一镜落幅 0.80）"),

 dict(n=24, seg="转", sec="当天大事", d=24, bg="bg8_郊外清明踏青路", v="bg8-1", lt="day", tod=6, tier="A",
      ch=["c1"], pr=[], unit="我试试", crowd=True, local=True, cuts_elide=True,
      facts=["festival.006", "festival.007", "festival.008", "cart.006", "food.023"],
      jb=(0.10, "远景", 0.50, "中景"), jbcam=("城门外路口高位远景", "踏青路边平视中景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着折柳插髻",
      cuts=[(0, 8, "城门外路口高位：人潮出城，街边纸马铺当街叠出一座座纸楼阁，地平线上一线夯土城墙", "开场"),
            (8, 24, "郊外踏青路边：前景一乘插满柳枝的轿子横过，树下人家摆酒；她折一枝柳插在包髻上，转身对镜头", "切（换到郊外路边）")],
      sstate=["城门外路口，还没出郊；她不在画面里", "折柳之前" + WILLOW_NONE + "；插上以后" + WILLOW + "，此后一直在"],
      title="【当天大事】出城 · 插一枝柳",
      summary="出城门口：人潮挤着出城，纸马铺当街用纸叠出楼阁；到了郊外「四野如市」，树下摆酒、轿顶插满杨柳杂花，坊市卖稠饧麦糕乳酪乳饼；**我试试**：她折一枝柳插在包髻左侧，对镜头转半圈。",
      plot="申时，城门外的路口人潮往外涌，街边纸马铺当街用纸叠出一座座小楼阁；出了城，四野像集市：树下、园子里摆着杯盘，人们互相劝酒；一乘轿子顶上插满杨柳和杂花、四面垂下来，从路上经过；宋装的林问走在踏青路边，转头看轿顶，从路边柳树上折下一枝柳，插在包髻左侧，然后转身对镜头说话，再转半圈",
      cam="0–8s 城门外路口旁土坡略高机位、俯角十度，35mm，f8，机位固定：纸马铺的纸楼阁在画面中下部，出城人潮从画右向画面深处走，远处地平线上横着一线淡土黄的夯土城墙；8–24s 踏青路边平视，35mm，f4，机位固定：前景一乘轿顶插满柳枝杂花的轿子从画面右下极近处横过、柳枝扫过镜头边缘，中景树下摆酒的人家是逆光剪影，她在画面中央",
      block="0–8s 无具名人物特写，可辨人物不超过八个、其余剪影；8–24s 她在画面中央，轿子从她身旁画左经过；她折柳时面朝画右的柳树，插好后转身正对镜头；路人不看镜头、不说话",
      act="0–4s 城门外路口：人潮往外涌，纸马铺门口当街摆着纸叠的楼阁；4–8s 纸楼阁的白纸在斜光里半透明，人从旁边挤过；8–12s 郊外路边：一乘插满柳枝的轿子从她身旁画左经过，她转头看轿顶；12–16s 她走到路边柳树下，伸手折下一枝柳；16–20s 把柳枝插进包髻左侧；20–22s 转身正对镜头说话；22–24s 说完再转半圈让你看柳枝",
      lines=[L(0, "画外", "清明一出城门，纸马铺在当街用纸叠出一座座楼阁，是给上坟的人家用的。", "At the city gate, paper shops fold paper pavilions right on the street, for families visiting graves.", 6.5, "festival.006", "解说", "中", "城门外的人潮"),
             L(8, "画外", "出了城，书上四个字：「四野如市」。树底下摆酒，傍晚才回。", "Beyond the walls, the fields are like a market. Picnics till dusk.", 4.5, "festival.007", "解说", "中", "经过身边的轿子"),
             L(12.5, "画外", "轿子顶上插满杨柳和杂花，四面垂下来。", "Sedan roofs piled with willow and flowers.", 3.5, "festival.008 cart.006", "看轿子", "中", "轿顶垂下的柳枝"),
             L(16, "画外", "清明坊市卖的是稠饧、麦糕、乳酪、乳饼。", "Street stalls sell malt syrup, wheat cakes, cheese and milk cakes.", 4.0, "food.023", "解说", "中", "手里折下的柳枝"),
             L(20, "对镜", "我也插一枝。怎么样？", "My turn. How's this?", 2.0, "", "转身")],
      light="申时，太阳偏西低斜、从画面深处偏右照来：柳叶被照透成嫩黄绿，人与轿拖着朝镜头方向的长影，路上被脚步与轿夫踩起的黄土细尘在逆光里发亮；纸楼阁的白纸在斜光下半透明",
      pace="出城（纸楼阁）→ 郊外（轿子）→ 折 → 插 → 对镜 → 转",
      spatial="机位＝城门外路口高位（固定）→ 郊外路边平视（固定）；在画主体＝出城人潮与纸马铺 → 她与轿子；她折柳朝画右，插好后正对镜头",
      contrast="首帧＝城门外人潮与纸楼阁（远景 0.10）→ 末帧＝她插着柳枝转半圈（中景 0.50）。**全城的清明，落到她头上一枝柳。**",
      moment="**18s 柳枝插进包髻左侧**",
      judge="青团那半句是 ❌ myth.010 的正解，删去（R6 F03 / 协调者裁定 9），青团只留负向；纸马铺按原文放在城门口当街（R6 W19），镜头由城门外路口切到郊外路边；前景轿子与地平线城墙（R4 F22）；对镜台词先说完再转半圈（R2-31）；柳枝状态串从本镜起逐字锁定（R2-32 / R5 F03 / 协调者裁定 7）；时辰定为申时（tod 6）"),

 dict(n=25, seg="转", sec="当天大事", d=20, bg="bg8_郊外清明踏青路", v="bg8-1", lt="day", tod=6, tier="A",
      ch=["c1"], pr=[], unit="大事", crowd=True, local=True,
      facts=["route.014", "festival.011", "festival.009", "festival.001"],
      jb=(0.20, "全景", 0.08, "远景"), jbcam=("人潮边缘平视", "骑队远景高位"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着",
      carry=[WILLOW],
      cuts=[(0, 10, "人潮边缘：她站着看人往城南涌，踮脚又退半步", "开场"),
            (10, 20, "高位远景：一队禁军骑马奏乐出城，旗子在风里展开", "切（换到高位远景）")],
      title="【当天大事】迎祥池一年开一天 · 禁军摔脚",
      summary="人潮往城南涌：迎祥池一年只在清明开一天；远处一队禁军骑马奏乐出城，叫「摔脚」，可不是摔跤；上坟出城一连三天，书上说一百五日——大寒食那天——人最多，寒食第三天才是清明。她不往前挤。",
      plot="申时，人潮往城南涌，宋装的林问站在人潮边缘看，不往前挤；远处一队禁军骑着马、一路奏乐出城，旗子在风里展开，其余人只是剪影",
      cam="0–10s 人潮边缘平视，35mm，f4，她在画左、人流在画右向画面深处涌，机位固定；10–20s 切到土坡高处、俯角十五度，70mm，f8，机位固定不摇，骑队自画左入画、自画右出画，可辨骑手不超过八个",
      block="0–10s 她站在画左路边、侧身看画右的人流、不看镜头；路人不看镜头、不说话；10–20s 无具名人物特写，骑队自画左向画右横过，旗在前、乐手在中间，其余剪影",
      act="0–4s 人流从她身边涌过，她站着不动；4–10s 她踮脚往人潮深处看，又退半步；10–14s 远景：旗手先入画，马队跟上，鼓乐手在中间；14–20s 队伍横过画面，旗子在风里展开，渐渐远去",
      lines=[L(0, "画外", "人都往城南涌——迎祥池一年只开放一天，就是今天清明。", "Everyone's heading south. Yingxiang Pond opens one day a year: today.", 4.5, "route.014", "解说", "中", "往城南涌的人潮"),
             L(4.5, "画外", FIXED, EN_FIXED, 2.5, "", "笑", "中", "人潮深处"),
             L(7, "画外", "那边骑着马一路奏乐出城的是禁军，书上叫「摔脚」，可不是摔跤。", "Mounted guards playing music on the way out — the book calls it shuaijiao. Not wrestling.", 5.5, "festival.011", "解说", "中", "远处出城的骑队"),
             L(12.5, "画外", "上坟出城一连三天，书上说「一百五日最盛」——大寒食那天人最多；寒食第三天才是清明。", "Grave visits run three days. Busiest, the book says, is day 105, the Great Cold Food; Qingming is day three.", 7.5, "festival.009 festival.001", "解说", "中", "渐渐远去的骑队")],
      light="申时偏西的日光，人潮逆光带亮边，骑队旗子的绸面在侧光里反光、随风展开，远处地平线泛白",
      pace="看（人潮）→ 踮脚 → 远（骑队横过）",
      spatial="机位＝路边平视（固定）→ 土坡高位远景（固定）；在画主体＝她与人流 → 骑队；人流向画面深处，骑队自画左向画右",
      contrast="首帧＝她在人潮边缘踮脚看（全景 0.20）→ 末帧＝骑队远去的远景（远景 0.08）。**她不挤，她看。**",
      moment="**12s 旗手入画、马队跟上**",
      post="固定句配 ✅ 音效；城市俯视图角标由后期加",
      judge="「清明这一天人最多」是 festival.009 旧误读，按 W12 更正改为引「一百五日最盛」＝大寒食，并说清寒食第三天才是清明（R6 W01 / W20，协调者裁定 9）；「摔脚」加一句「可不是摔跤」防听错（R1 R30）；旗子不写「鲜亮」（R4 F29）；柳枝状态串照带；后段 12 s 空转缩到 10 s、镜长 22→20 s（R3-32）"),

 dict(n=26, seg="转", sec="当天大事", d=26, bg="bg1_虹桥", v="bg1-1", lt="day", tod=6, tier="S",
      ch=["c23"], pr=[], unit="大事", crowd=True, local=True, fall=("桅杆",), neg_add="定格, 画面冻结",
      facts=["boat.003", "boat.002", "bridge.006", "job.011", "house.011", "dress.021", "doubt.001"],
      jb=(0.25, "全景", 2.00, "特写"), jbcam=("虹桥河岸中位横移", "船头甲板低位仰拍桅根与桥洞"),
      cuts=[(0, 20, "一条纲船桅杆没放倒冲向桥洞，岸上顶篙、船上扑去放桅，铺兵在桥头挥手让人靠边", "开场"),
            (20, 26, "船头甲板低位仰拍：桅杆倒平的一瞬，桥洞拱底从头顶掠过", "切（换到船头甲板上）")],
      title="【当天大事】虹桥险情 · 桅杆没放",
      summary="**本站奇观 hero。** 申时沿城外汴河堤回到虹桥：一条纲船桅杆没放倒冲向桥洞，桥上一片惊叫，岸上顶篙、水手扑上去却抱不住，桅杆越倒越快，沈十九在桥头挥手让人靠边；桅杆砸平的一瞬船头擦着桥洞钻过。零笑点。",
      plot="申时，太阳偏西，虹桥下一条纲船的桅杆还立着，顺着水冲向桥洞；桥上的人一片惊叫（听不清字句），岸上几个人拿长篙死死顶住船头，船上两个水手扑上去抱住桅杆往下放，却抱不住；桥头一个军巡铺兵挥着手让桥上的人往两边靠；桅杆越倒越快，砸平落定的一瞬，船头擦着桥洞钻了过去",
      cam="0–20s 一个连续运镜：河岸中位、眼平略高，35mm 缓推到 50mm，机位随船顺流方向缓慢横移跟船，f5.6；20–26s 切到船头甲板上低位仰拍，24mm，f5.6，机位固定在船上随船前进：桅杆根部与抱桅的手占画面下半，桥洞拱底从画面上方压过来、擦着倒平的桅杆掠过，画面实时继续",
      block="沈十九在桥头画右、面朝桥面、举起骨朵挥动让人靠边，不说话、不看镜头；桥上的人往两侧让，可辨不超过八个，其余剪影；0–20s 画面下缘前景是岸上顶船的一根长篙，离镜头很近、虚成一条暗色，随顶篙的人用力而弯；船自画左向画右冲向桥洞；两名水手抱桅杆、一名在船尾撑篙，岸上两个人顶篙；林问不入画",
      act="0–4s 船冲近，桅杆还立着，桥上有人先叫起来；4–10s 桥上一片惊叫，岸上的人用长篙顶住船头，船速稍缓；10–15s 两名水手扑上去抱住桅杆根部往下放，沈十九在桥头挥手，桥上的人往两边让开，带起桥面的细尘；15–20s 两个水手抱不住，桅杆绕根部的转轴越倒越快，船头推出一道泛白的浪头拍上岸边，桅杆倒下带起的风把船篷上的席子掀起一角；20–23s 船头仰拍：最后半秒明显加速、砸平落定在船篷上、弹一下停住，抱桅的手被带得一沉；23–26s 桥洞木拱的阴影从画面上方一掠而下、扫过桅杆根部和手——船头正擦着桥洞钻过，画面照常实时继续",
      lines=[L(0, "画外", "沿着城外的汴河堤走回虹桥，出事了——一条纲船的桅杆没放倒，正往桥洞冲。", "Back at the Rainbow Bridge — trouble. A boat's heading for the arch, mast still up.", 6, "boat.003", "紧", "快", ""),
             L(6, "画外", "岸上的人拿长篙顶住船，船上的人扑上去放桅。", "Bank poles brace it; the crew lunge for the mast.", 4, "boat.003 boat.002", "紧", "快", ""),
             L(10, "画外", "桥头那个铺兵在挥手让人往边上靠。铺兵白天管不管这种事，史书没写，是我的推测。", "A patrol soldier waves people aside. Whether they handled this by day, the records don't say. My guess.", 7.0, "job.011 house.011", "压着", "中"),
             L(20, "画外", "画里也有一条正在放桅的船——这种险情，汴河上大概天天都有。", "The scroll shows a boat dropping its mast too. On this river, probably an everyday scare.", 6, "bridge.006", "轻", "慢", "")],
      light="申时，太阳已偏西、低低地在画左（西面）：船、桅杆与桥拱被逆光压成偏暗的剪影，朱漆只在拱木边缘亮出一道暖赭红的细边；画左半边河面反出一大片橙黄色的碎光；桅杆的长影斜投在水面上，随桅杆倒下从画左向画右扫过水面；20–26s 仰拍段逆光，桅杆与抱桅的手被勾出一道暖亮边，溅起的水花在逆光里一粒粒发亮",
      pace="冲（紧）→ 叫 → 顶 → 放 → 倒（越来越快）→ 一瞬",
      spatial="机位＝河岸中位横移跟船（连续）→ 船头甲板低位仰拍（随船）；在画主体＝船与桥洞、让路的人、桥头的沈十九 → 桅杆根部与掠过的桥洞；船自画左向画右",
      contrast="首帧＝桅杆还立着的船冲向桥洞（全景 0.25）→ 末帧＝桅杆砸平、桥洞阴影扫过桅根（特写 2.00）。**画里那一秒，每天都在发生。**",
      moment="**24s 桥洞的阴影扫过刚倒平的桅杆根部**",
      post="零笑点；桥上惊叫是没有可辨字句的环境声（casting.md 铁律 4）",
      judge="「画的就是这样的一天」与 doubt.001（画的是不是清明存疑）冲突，改为「大概天天都有」（R6 W11，优先于 R1 R42）；沈十九的骨朵依据 dress.021 白沙宋墓持骨朵护卫（R6 W18② 回应，卡锁定串不改）；从城南回虹桥写明沿汴河堤走回（R5 F16）；机位换到船头甲板、hero 在画框内、不定格（R3-22 / R2-33）；光换到西侧逆光、补环境反应（R4 F12 / F13）；林问不入画、只有画外"),

 dict(n=27, seg="转", sec="当天大事", d=20, bg="bg1_虹桥", v="bg1-1", lt="day", tod=6, tier="A", ear=True,
      ch=["c1"], pr=[], unit="大事", local=True,
      facts=["travel.004", "boat.002"],
      jb=(0.80, "近景", 0.15, "远景"), jbcam=("桥头她侧前方近景", "桥头高位河面远景"),
      hands="右手握话筒垂在身侧；采访本揣在褙子左襟里，左手扶栏",
      carry=[WILLOW],
      cuts=[(0, 12, "桥头近景：她看着岸上拉纤的人", "开场"),
            (12, 20, "高位河面远景：纤夫把船拉回正道，船慢慢走远", "切（换到高位）")],
      title="【当天大事】拉纤的人 · 老死河路",
      summary="险情过去，纤夫把船拉回正道；她讲纲船上的人是管船队的小吏一批批雇来的、史书里「终身不还其家，老死河路」；这条河以后的事她知道，不说。零笑点。",
      plot="申时，险情过去，虹桥桥头，宋装的林问站在栏边，看着岸上几个纤夫弓着身子把那条纲船拉回正道，纤绳勒在他们肩上；船慢慢顺着河走远",
      cam="0–12s 桥头她侧前方一米半，眼平，50mm，f2.8，近景，机位固定；12–20s 切到桥头高处俯角十五度，35mm，f8，机位固定",
      block="0–12s 她在画面右侧、侧身朝画左的河岸、不看镜头；纤夫在画左远处岸上、背对镜头、不说话；12–20s 无具名人物特写，纤夫与船在画面中景，她是桥头一个小小的身影",
      act="0–4s 她扶着栏杆看岸上；4–8s 纤夫弓着身子一步一步往前拉，纤绳绷紧；8–12s 她垂下眼，停了一会儿又抬起来；12–16s 高位：船被拉回河道正中；16–20s 船顺着河慢慢走远，纤夫停下来喘气",
      lines=[L(0, "画外", "船拉回正道了。纲船上的人，是管船队的小吏一批一批雇来的。", "The boat's back on course. Crews were hired in batches by the convoy's clerks.", 5.5, "travel.004", "轻", "中", "岸上拉纤的人"),
             L(5.5, "画外", "史书里有一句：「终身不还其家，老死河路」。有的人，一辈子没回过家。", "The record says some never went home, and died on the river road.", 7.0, "travel.004", "慢", "慢", "勒在纤夫肩上的纤绳"),
             L(13, "画外", "这条河以后会怎么样，我知道。我不说。", "I know what happens to this river later. I won't say.", 4.5, "", "压着", "慢", "走远的船")],
      light="申时，西斜的低光从画左来：画左半边河面反出一片橙黄碎光，纤夫弓着的背被勾出一道暖亮边，她的侧脸在逆光的柔光里",
      pace="看 → 拉 → 垂眼 → 远（船去）",
      spatial="机位＝桥头侧前方近景（固定）→ 桥头高位（固定）；在画主体＝看着河岸的她 → 纤夫与船；她朝画左的河岸",
      contrast="首帧＝她扶栏看岸上（近景 0.80）→ 末帧＝船走远、纤夫停下喘气（远景 0.15）。**险情过去了，拉纤的人还在喘。**",
      moment="**18s 船走远、纤夫停下喘气**",
      post="零笑点",
      judge="「一纲一纲雇来的」听不懂，改为「管船队的小吏一批一批雇来的」（R1 R12，travel.004「给付主纲吏雇募」）；慢句放宽时长（R3-34）；光与 shot26 同为西斜逆光（R4 F34）；柳枝状态串照带；决定性瞬间挪到镜尾（R2-04）；「这条河以后」不展开（站与站独立）"),
]

S += [
 dict(n=28, seg="合", sec="娱乐", d=24, bg="bg6_瓦子勾栏", v="bg6-1", lt="day", tod=7, tier="A",
      ch=["c1"], pr=[], unit="看", crowd=True, local=True, neg_add="京剧脸谱, 京剧行头, 售票窗口",
      facts=["shop.006", "ent.013", "ent.014"],
      jb=(0.35, "全景", 0.50, "中景"), jbcam=("瓦子门口平视全景", "摊市间中景跟拍"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，摆手用右手，掀帘用左手",
      carry=[WILLOW],
      cuts=[(0, 8, "瓦子门口全景：一座挨一座的席顶看棚，门口一圈摊子", "开场"),
            (8, 24, "摊市间中景：卖药、算卦、剃头的摊子，彩棚下的关扑彩头；她摆手笑着对镜头说，最后掀起看棚口的芦席帘", "切（换到摊市间跟拍）")],
      title="【娱乐】瓦子门口 · 看戏前先逛摊",
      summary="桑家瓦子：大小勾栏五十多座，最大的棚「可容数千人」；门口一圈卖药、算卦、剃头的摊子，彩棚下摆着梳子鞋子当关扑彩头；算卦的朝她招手，她转向镜头说今天的单子早排满了；瓦子的「瓦」是聚散都快、不是瓦房；她掀帘往看棚里看。",
      plot="酉时前，桑家瓦子门口，用素木杆和芦席搭起的看棚一座挨一座，棚口挂着无字的布招子；门口挤着卖药的、算卦的、剃头的、卖纸画的摊子，一处彩棚下摆着梳子、珠翠头面、鞋子当关扑的彩头；宋装的林问从摊子中间穿过，算卦的朝她抬手示意，她笑着摆摆手，转向镜头说话，继续往看棚走，掀起看棚口的芦席帘往里看",
      cam="0–8s 瓦子门口平视全景，28mm，f5.6，机位固定；8–24s 摊市间中景，她左侧约两米、眼平，35mm，f4，与她同速跟拍",
      block="0–8s 可辨人物不超过八个、不看镜头、不说话；8–24s 她自画右向画左从摊子中间穿过、侧对镜头，15–18s 转脸看镜头；摊主各忙各的，算卦的朝她抬手示意、不出声；彩棚在画左",
      act="0–4s 看棚一座挨一座，棚口布招子被风吹动；4–8s 门口人来人往；8–12s 她走过卖药、剃头的摊子；12–15s 经过彩棚下的关扑摊，看一眼摆着的梳子和鞋子；15–18s 算卦的朝她抬手示意（不出声），她笑着摆摆手、转脸看镜头说话；18–21s 往看棚方向走去；21–24s 她掀起看棚口的芦席帘往里看，棚里的昏暗和一片笑声扑出来",
      lines=[L(0, "画外", "瓦子，汴京人看戏的地方。这一片大小勾栏五十多座，最大的棚书上说「可容数千人」。", "The wazi, Kaifeng's show district. Over fifty playhouses here; the biggest held thousands.", 7.0, "shop.006", "解说", "中", "一座挨一座的看棚"),
             L(7, "画外", "门口一圈摊子：卖药的、算卦的、剃头的。彩棚底下这些梳子鞋子，是关扑的彩头。", "Stalls all around the entrance: medicine, fortune-telling, haircuts. Those combs and shoes are gambling prizes.", 7.0, "shop.006 ent.014", "解说", "中", "彩棚下的梳子和鞋子"),
             L(15, "对镜", "算卦的在招手——不算了，今天排满了。", "Fortune-teller's waving. No thanks — fully booked.", 3, "", "摆手，转回镜头笑", "中", ""),
             L(18.5, "画外", "瓦子的瓦，是聚得快、散得也快的意思，不是瓦房。", "Wa means crowds gather and scatter fast — not roof tiles.", 4.0, "ent.013", "解说", "中", "看棚口的芦席帘")],
      light="酉时前，太阳已低，暖黄的斜光自画右低低照来：棚外土场被照成暖黄，每个人身后拖着很长的影子，人群踩起的细尘在斜光里浮着；席顶看棚下一片灰凉的阴影",
      pace="热闹（门口）→ 穿行 → 看彩头 → 摆手对镜 → 往里走 → 掀帘",
      spatial="机位＝瓦子门口全景（固定）→ 她左侧跟拍；在画主体＝看棚与门口摊市 → 穿过摊子的她；她自画右向画左走向看棚",
      contrast="首帧＝一座挨一座的看棚（全景 0.35）→ 末帧＝她掀起看棚口的帘子往里看（中景 0.50）。**戏还没看，门口先热闹上了。**",
      moment="**16s 算卦的朝她抬手，她摆手笑着对镜头说**",
      judge="「算卦？不用了」是在回答入画的算卦人，改为转向镜头说「算卦的在招手——不算了」，并去掉压过 S27 的「我知道结局」（R1 R01 blocker / R5 F13）；「寒食这几天放开」已在 S21 讲过，删去并去掉 gov.013（R5 F12）；台词顺序按动作重排（R2-34）；光改酉时低暖斜光、镜尾掀帘接下一镜（R4 F23）；柳枝状态串照带"),

 dict(n=29, seg="合", sec="娱乐", d=26, bg="bg6_瓦子勾栏", v="bg6-1", lt="day", tod=7, tier="A",
      ch=["c1"], pr=[], unit="看", crowd=True, local=True, neg_add="京剧脸谱, 京剧行头, 座椅剧场, 字幕屏, 折扇, 手指含嘴吹哨",
      facts=["ent.015", "ent.022", "ent.023", "ent.005", "daily.006", "literati.024"],
      jb=(1.20, "特写", 0.15, "远景"), jbcam=("看棚里她的脸特写", "看棚后排高位远景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；右手抬起捂一下嘴又放下",
      carry=[WILLOW],
      cuts=[(0, 8, "她的脸特写：她跟着笑出声，放下手转脸看镜头", "开场"),
            (8, 26, "看棚后排高位远景：台上四五个杂剧艺人比划，台边一座小彩楼傀儡棚，台下人挤人一起笑", "切（拉到后排高位）")],
      title="【娱乐】看棚里 · 满棚一起笑",
      summary="**hero：满棚一起笑。** 台上四五个杂剧艺人只比划不出词：扮官的一本正经、诨裹丑角挤眉弄眼装傻逗笑、簪花戴幞头腰插团扇的扮相（丁都赛雕砖）；台边小彩楼傀儡棚三扇小门。杂剧分工是南宋书里记的，套到这里是推测；演哪一出史书没写。",
      plot="酉时前，席顶看棚里，台下人挤人；台上四五个杂剧艺人正在比划：一个戴长翅幞头扮官的一本正经，一个裹诨裹的丑角挤眉弄眼、装傻出怪相逗笑；一个艺人头裹幞头簪着花枝、穿圆领开衩长衫、脚穿筒靴、腰里插一把团扇；台边一座小彩楼样的傀儡棚，下面开着三个小门；台下的人一起哄笑，宋装的林问也跟着笑出了声",
      cam="0–8s 她的脸特写，侧前方、眼平，85mm，f2，机位固定，背景台上艺人柔焦；8–26s 切到看棚后排高处，俯角十五度，28mm，f5.6，机位极缓后拉，全场入画",
      block="0–8s 她在画面中央、侧身朝画左的戏台，5–8s 转过脸看镜头说话；8–26s 台在画面上半、四五个艺人在台上比划、不出声对白；台下观众背对镜头、可辨不超过八个，其余是后脑与肩的剪影；她在画面右下方人群里",
      act="0–3s 她盯着台上；3–5s 忍不住笑出声，抬手捂一下嘴；5–8s 放下手，笑着转过脸看镜头说话；8–14s 远景：扮官的艺人一本正经踱步，丑角挤眉弄眼、装傻作怪相；14–20s 台下一片哄笑，前排有人拍腿；20–26s 镜头慢慢后拉，满棚的人一起笑，傀儡棚的小门里探出一个木偶",
      lines=[L(5.5, "对镜", "哈哈……不行，我没绷住。", "Ha… sorry, I lost it.", 2.0, "", "笑"),
             L(8, "画外", "这是杂剧，一场四五个人：扮官的一本正经，丑角装傻逗笑。这套分工是南宋书里记的，我按它推测；演哪一出，史书没写。", "Zaju: four or five players, a straight-faced official, a clown playing dumb. That lineup is from a Southern Song book — my guess. The play isn't recorded.", 10, "ent.015", "解说", "中", "台上比划的艺人"),
             L(18, "画外", "那个簪花戴幞头、腰插团扇的扮相，有女艺人丁都赛的雕砖作证。", "Flowered cap, fan at the waist — like the carved brick of Ding Dusai.", 5, "ent.022 literati.024", "解说", "中", "腰插团扇的艺人"),
             L(23, "画外", "带三个小门的小彩楼，是傀儡戏棚。", "Three little doors: a puppet booth.", 3, "ent.005", "解说", "中", "傀儡棚的小门")],
      light="酉时前，席顶看棚里是灰凉的阴影；棚口透进一道低斜的暖光照亮台口一角，芦席顶的缝隙里漏下一道道细细的斜光落在台下人的肩背与幞头上，人群里浮起的细尘让光的走向看得清楚；台上艺人一半在光里一半在阴影里",
      pace="笑（她）→ 对镜 → 远（台上）→ 哄笑 → 满棚",
      spatial="机位＝她的脸特写（固定）→ 看棚后排高位（极缓后拉）；在画主体＝她 → 戏台、傀儡棚与满棚观众；她朝画左的戏台",
      contrast="首帧＝她笑出声的特写（特写 1.20）→ 末帧＝满棚人一起笑的远景（远景 0.15）。**九百年前的人笑起来，跟我们也差不多。**",
      moment="**24s 满棚一起笑、傀儡棚小门里探出木偶**",
      judge="丑角「手指含嘴吹哨」只有 ai_draft 的逐人描述支撑，改为挤眉弄眼装傻出怪相并挂负向（R6 F05 / 协调者裁定 9）；杂剧分工口播标为南宋书里记的推测（R6 F06，优先于 R1 R08）；团扇补 literati.024、负向挂折扇（R6 W17）；「天天如此」改口语（R1 R41）；对镜台词挪到放下手之后（R2-35）；光写席缝斜光（R4 F24）；景别档特写 1.20 → 远景 0.15"),

 dict(n=30, seg="合", sec="夜·吃", d=24, bg="bg17_州桥夜市", v="bg17-1", vx=[("bg17-2", "17–24s 摊面近看")], lt="oil", tod=8, tier="A",
      ch=["c1"], pr=["p1", "p2"], unit="吃", crowd=True, local=True,
      facts=["food.005", "street.002", "price.001", "food.002", "food.003", "house.005", "money.001", "money.008"],
      jb=(0.35, "全景", 2.00, "特写"), jbcam=("州桥南头往南夜市纵深", "包子与羊白肠微距"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，数钱后接包子",
      carry=[WILLOW],
      cuts=[(0, 7, "州桥南头往南的夜市纵深：摊上一只只敞口陶灯盏连成一条", "开场"),
            (7, 17, "包子摊前侧面中景：她伸两根手指，数出二十来枚铜钱，摊主递来两个包子，她咬一口咽下后对镜头打分", "切"),
            (17, 24, "微距：包子冒热气，旁边铁鏊上煎着羊白肠", "切（换到食物微距）")],
      title="【夜·吃】州桥夜市 · 猜一个包子多少钱",
      summary="戌时天黑，州桥往南一溜夜市开到「直至三更」，摊上只点敞口陶灯盏；猜价格暂停卡：一个包子多少钱——每个不过十五文；她买了两个打八分；旋煎羊白肠史书没写价，她没买，不报价。",
      plot="戌时天黑后的州桥夜市，从州桥往南，每个摊的棚柱上与案角各放一只敞口陶灯盏，一点点火苗连成一条暖黄的线，摊上有水饭、爊肉、干脯；宋装的林问在一家包子摊前伸出两根手指，从腰前钱串上数出二十来枚铜钱放到案上，摊主点点头收下，递来两个冒热气的包子；她咬一口；旁边一张矮木案上的铁鏊里煎着羊白肠",
      cam="0–7s 站在州桥南头往南沿街纵深平视，85mm 长焦，f2.8，机位固定：一盏盏豆大的灯火沿街往南排成一条越来越小、越来越密的暖点，画面左侧前景是近处摊棚的苇席边，虚成暗色剪影；7–17s 摊前侧面中景，眼平，35mm，f2.8，机位固定；17–24s 微距，离案约三十厘米、俯角三十度，100mm，先是包子，末段机位横移到旁边铁鏊上的羊白肠",
      block="她在摊前画面中央、面朝画右的摊主，打分时转正脸看镜头；摊主只露手与半身、不说话、不看镜头；夜市人流在她身后柔焦、可辨不超过六个",
      act="0–4s 夜市纵深，灯火一点点，煎肠的油烟与包子笼的白汽在灯前发亮；4–7s 她走进灯光里；7–9s 她朝摊主伸两根手指（不说话）；9–12s 从腰前钱串上数出二十来枚铜钱放到案上，摊主点点头收下、递来两个包子；12–14s 她咬一口、嚼两下咽下；14–17s 嘴里已经没有东西，点点头，正脸看镜头打分；17–21s 微距：包子冒热气，皮薄；21–24s 画面移到旁边铁鏊，羊白肠滋滋冒油",
      lines=[L(0, "画外", "天黑了，州桥往南一溜都是夜市，书上说开到「直至三更」。", "Night stalls run south from Zhou Bridge till the third watch.", 4.5, "food.005 street.002", "解说", "中", "沿街排开的灯火"),
             L(4.5, "画外", "猜猜，一个包子多少钱？", "Guess: how much is a bun?", 2.5, "price.001", "卖关子", "慢", "包子摊的笼屉"),
             L(9.5, "画外", "每个不过十五文，鹅鸭鸡兔、肚肺鳝鱼，什么馅儿都有。", "Fifteen wen each, tops: goose, duck, rabbit, tripe, eel.", 4.5, "price.001 food.002", "揭晓", "中", "案上数出来的铜钱"),
             L(14.5, "对镜", "买了两个。……皮薄，八分。", "Bought two. …Thin skin. Eight.", 2.5, "", "咽下后说"),
             L(17.5, "画外", "旁边煎的是旋煎羊白肠，史书没写价，我没买，不报价。", "Next door: fried mutton sausage. The records don't give a price, so I skipped it.", 5.5, "food.003", "解说", "中", "铁鏊上的羊白肠")],
      light="戌时，天上只剩最后一线深蓝、很快转成深蓝近黑；每个摊子棚柱上和案角的敞口陶灯盏是全部光源，豆大的火苗暖黄、一小簇一小簇，只照亮摊面与近处的手和脸，鏊下泥炉口一线暗红炭火只照亮炉口一圈；煎肠的油烟与包子笼的白汽在灯前被照亮、往上散；灯与灯之间是看不清的黑，黑位不提亮；没有月光直射、没有任何冷白光源",
      pace="亮（纵深）→ 买 → 咬 → 对镜 → 看（微距）→ 羊白肠",
      spatial="机位＝州桥南头长焦纵深（固定）→ 摊前侧面中景（固定）→ 食物微距；在画主体＝夜市灯火 → 她与包子摊 → 包子与羊白肠；她面朝画右的摊主",
      contrast="首帧＝灯火连成一条的夜市纵深（全景 0.35）→ 末帧＝铁鏊上冒油的羊白肠微距（特写 2.00）。**这座城天黑了才最香。**",
      moment="**16s 她咽下点头，对镜打分**",
      post="猜价格暂停卡：「猜猜，一个包子多少钱？」之后停约 2 秒（7–9.5s）叠问题卡，9.5s 揭晓「每个不过十五文」（price.001）；卡片全在后期层，prompt 零文字",
      judge="主体改挂 bg17_州桥夜市、摊面段挂 bg17-2（S2_bg16 / 协调者裁定 6）；灯是敞口陶灯盏、没有纸罩，删 keep_candle、挂非正店夜镜蜡烛负向（协调者裁定 4 / R4 F15 / F16）；「两个」是对摊主点单，改为对镜「买了两个」、咽下后说（R1 R02 / R2-36）；两个包子三十文按七十五陌约二十来枚（R5 F17）；羊白肠没吃，改「我没买，不报价」（R1 R13，与 R5 F08 同解，总账不再漏记）；光补鏊下炭火、长焦纵深（R4 F17 / S2_bg16）；p2 旧钱为主的推测由「史书没写」口播兜住"),

 dict(n=31, seg="合", sec="夜·吃", d=26, bg="bg5_正店酒楼", v="bg5-1", lt="lamp", tod=8, tier="A",
      ch=["c1"], pr=["p7"], unit="吃", local=True, indoor=True, cuts_elide=True, neg_add="太师椅, 金属镜面反光, 亮银, 镀银反光",
      facts=["shop.001", "food.025", "money.007", "job.007", "food.008", "house.006"],
      jb=(0.15, "远景", 0.75, "近景"), jbcam=("正店街对面远景", "阁子桌边近景"),
      hands="话筒柄朝下插在腰前青花手巾里、采访本揣在褙子左襟里；两手空着，掂银注碗用右手，最后抽出采访本划一笔",
      carry=[WILLOW],
      cuts=[(0, 7, "正店门首远景：彩楼欢门高过屋檐，门里烛光门外天光", "开场"),
            (7, 26, "阁子桌边：焌糟摆上注碗盘盏果菜碟，她掂一掂银注碗，对镜头说", "切（换到阁子内）")],
      title="【夜·吃】正店 · 桌上一百两银子",
      summary="正店门首彩楼欢门、门里烛光门外天光；阁子里腰系青花手巾的焌糟摆上注碗一副、盘盏两副、果菜碟五只——「即银近百两」；她掂银注碗：是酒具不是钱；银瓶酒按遇仙正店七十二文「一角」记，打九分。",
      plot="戌时入夜，正店门首用长木杆扎出的彩楼欢门高过屋檐，门额一块空白窄匾，门里烛光从珠帘缝往外漏；宋装的林问走进门，在二楼廊边一间小阁子里坐下；一位腰系青花布手巾的焌糟一样样摆上一副银注碗、两副盘盏和五只果菜碟，不说话，退出去；林问拿起银注碗掂了掂，放下，转正脸对镜头说话，最后抽出采访本划一笔",
      cam="0–7s 街对面远景，眼平，28mm，f2.8，机位固定，欢门占画面上半；7–26s 阁子桌边，她侧前方，眼平，50mm，f2.8，近景，机位固定，银器在画面下缘",
      block="0–7s 门口进出的人为剪影、不看镜头；7–26s 她坐在阁子桌前画面中央、侧身对镜头，15s 起转正脸看镜头；焌糟自画右摆器皿、只露半身、不说话、不看镜头；帘子在她身后",
      act="0–4s 欢门静止，门里的烛焰稳稳立着，只在有人掀帘进出时被风压歪一下又立直；4–7s 她走进门；7–9s 阁子里坐下，帘子垂下；9–13s 焌糟一样样摆上注碗、盘盏、果菜碟，然后退出画外；13–15s 她拿起银注碗掂了掂，放下；15–24s 转正脸看镜头说话；24–26s 从褙子里抽出采访本，在上面划一笔",
      lines=[L(0, "画外", "门口扎的这个叫彩楼欢门，京城的酒店门口都有。", "That tall frame is a festoon gate. Every tavern had one.", 4, "shop.001", "解说", "中", "高过屋檐的彩楼欢门"),
             L(4, "画外", "两个人对坐喝酒，也得上一副注碗、两副盘盏、五只果菜碟，书上说「即银近百两」。", "Even two drinkers get a warmer, two cups and five dishes — nearly a hundred taels of silver.", 6.5, "food.025", "解说", "中", "摆上桌的银器"),
             L(10.5, "画外", "给我摆碗的这位，腰系青花手巾，宋朝叫「焌糟」。", "The woman setting my table, blue-print apron — they called her a juncao.", 4.5, "job.007", "解说", "中", "退出去的焌糟"),
             L(15, "对镜", "这是酒具，不是钱。", "This is tableware, not money.", 2.0, "money.007", "掂银注碗"),
             L(17, "对镜", "遇仙正店的银瓶酒，书上写七十二文「一角」，我按这个记。这顿，九分。", "At Yuxian, silver-flask wine was seventy-two wen a jug. I'll book that. Nine.", 5.5, "food.008", "点头"),
             L(22.5, "画外", FIXED, EN_FIXED, 2.5, "", "笑", "中", "手里的采访本")],
      light="戌时，天上还剩最后一层深蓝，街面与欢门木杆在这层天光里是冷灰的剪影；暖黄的烛光只从门里的珠帘缝与二楼吊窗漏出来，在门口地面投下一块暖色的光；进了阁子，桌上的烛火是主光，银器是发暗的银白、只有一点烛光的小高光；没有月光直射、没有冷白光源",
      pace="亮（欢门）→ 进 → 坐 → 摆器皿（焌糟）→ 掂 → 说 → 记",
      spatial="机位＝街对面远景（固定）→ 阁子桌边近景（固定）；在画主体＝彩楼欢门 → 她与桌上银器；她侧身对镜头，焌糟在画右",
      contrast="首帧＝烛光从珠帘缝漏出的彩楼欢门（远景 0.15）→ 末帧＝她掂完银注碗对镜说完、划一笔（近景 0.75）。**两个人喝顿酒，桌上摆着快一百两银子。**",
      moment="**14s 她掂银注碗**",
      post="固定句配 ✅ 音效；「孙羊正店」匾在画面里空白，字由后期贴原画字样（shop.004）",
      judge="门额匾与立招一律空白（R6 F12，p7 用空白派生版）；焌糟解释从 shot11 挪到真正的焌糟入画处（R5 F05）；「酒具不是钱」只在本镜讲（R5 F10，不采 R1 R26）；「一角」放进引号防听成钱（R1 R27）；台词与动作窗口对齐（R2-37），镜尾抽本子划一笔（R5 F19）；光改门里烛光门外天光（R4 F18）；负向补太师椅与银器非镜面（R6 W17 / R4 F28）；时长 22→26 s（R3-18）；酒价取遇仙正店（food.008），画面是另一家正店，口播写明「按这个记」"),

 dict(n=32, seg="合", sec="夜·吃", d=28, bg="bg5_正店酒楼", v="bg5-1", lt="lamp", tod=8, tier="A",
      ch=["c1"], pr=[], unit="收", indoor=True, neg_add="太师椅, 金属镜面反光, 亮银, 镀银反光",
      facts=["price.003", "job.018", "price.001", "food.008", "money.002", "price.022", "price.024", "travel.012", "money.006", "job.008", "doubt.001", "house.006"],
      jb=(0.30, "全景", 0.75, "近景"), jbcam=("阁子门口全景", "阁子内正前近景"),
      hands="话筒放在桌角；左手按着摊开的采访本，右手捏铅笔",
      carry=[WILLOW],
      title="【夜·收】今日总账单 · 本站存疑",
      summary="阁子里逐笔念账：早饭二十、汤给了两枚、驴一百、包子三十、酒七十二，一共两百二十来文，按七十五陌实掏一百六十多枚；住店钱史书没写先空着；按北宋一般工钱算是扛活的人两天多的收入；三句话；本站存疑一条（《清明上河图》画的是不是清明）。零笑点。",
      plot="戌时，正店阁子里，桌上银注碗、酒和果菜碟，一支蜡烛；宋装的林问把话筒放在桌角，翻开采访本，用铅笔尾一笔一笔点着念账，念完合上本子，看着镜头说话",
      cam="阁子门口，她正前方略侧，眼平，35mm，f2.8；0–8s 全景（她与整张桌子），机位固定；8–28s 机位向她推进约一米半到近景（胸口以上），她在画面右三分之一，帘子与阁子纵深在画左，桌上银器在前景下缘虚化",
      block="她坐在阁子桌前、正面略侧对镜头，说话时看镜头、念账时看本子；桌上银器与酒在画面下缘；帘子在身后；阁子里只有她一个人",
      act="0–6.5s 她翻开本子，铅笔尾一笔一笔点着念，抬眼看镜头；6.5–10s 嘴停下，低头用铅笔在本子上划一道；10–13s 抬头看镜头说住店钱；13–17s 看着镜头说工钱；17–21.5s 对镜头说三句话，每说一句伸一根手指；21.5–28s 手停在本子上，放慢看着镜头说存疑那一条，最后合上本子",
      lines=[L(0, "对镜", "算账：早饭二十，汤给了两枚，驴一百，包子三十，酒七十二，一共两百二十来文。", "The tally: breakfast twenty, two coins for soup, donkey a hundred, buns thirty, wine seventy-two. About two-twenty.", 6.5, "price.003 job.018 price.001 food.008", "念本子"),
             L(6.5, "画外", "按七十五陌，实际掏出去一百六十多枚铜钱。", "Seventy-five to the hundred: about 160 coins.", 3.5, "money.002", "补一句", "中", "本子上划掉的一行"),
             L(10, "对镜", "住店钱史书没写，先空着。", "Room price isn't recorded. Leaving it blank.", 2.5, "", "点本子"),
             L(13, "对镜", "两百多文，按北宋一般工钱，是扛活的人两天多的收入。", "Two hundred-odd wen: roughly two days' pay for a porter.", 4.5, "price.024", "抬头", "中", ""),
             L(17.5, "对镜", "三句话：夜里随便逛，买东西认铜钱，跑腿也是生意。", "Three things: open all night, pay in copper, errands for hire.", 4, "travel.012 money.006 job.008", "伸手指", "中", ""),
             L(21.5, "对镜", "本站存疑：《清明上河图》画的是不是清明，学者没定论；搬到今天，是推测。", "Open question: does the Qingming scroll show Qingming? Unsettled. Setting it today is my guess.", 6, "doubt.001", "平", "中", "")],
      light="戌时，阁子桌上一支蜡烛与帘外透进的店里烛光是全部光源，暖调、低照度，她的脸一侧受光；桌上银注碗是发暗的银白，只映一点烛光；没有月光、没有冷白光源",
      pace="念（稳）→ 划 → 空着 → 工钱 → 三句 → 慢（存疑）→ 合上",
      spatial="机位＝阁子门口正前略侧（向她推进）；在画主体＝她与桌上的本子银器；她正面略侧对镜头",
      contrast="首帧＝她翻开本子念账的全景（全景 0.30）→ 末帧＝她合上本子看镜头的近景（近景 0.75）。**一天的账，一贯钱花了不到四分之一。**",
      moment="**27s 合上本子，看着镜头**",
      post="零笑点；逐笔账单角标由后期叠",
      judge="「汤两文」改「汤给了两枚」、总数改「两百二十来文」（R5 F17 / R6 W06）；工钱按北宋一般推算、「只认铜钱」收窄（R6 W02 / W03，与 R1 R43 合并）；存疑句点名《清明上河图》、说清推测的是什么（R1 R10）；羊白肠在 shot30 没买，账上不再漏记（R5 F08 解决方式）；中间一句 OS 留出嘴停下的动作（R2-38），去掉无动作的 p2；蜡烛补 house.006（R6 W18）；机位推进而不是变焦（R3-19）；时长 26→28 s（R3-20）"),
]

S += [
 dict(n=33, seg="合", sec="住·过夜", d=28, bg="bg14_客店房间夜", v="bg14-1", lt="oil", tod=9, tier="A",
      ch=["c1"], pr=[], unit="住", indoor=True,
      neg_add="更夫敲锣打梆, 手臂过长, 橡皮手, 坐在床上够到地上的床腿, 四肢比例失真, 睡觉时手里握着话筒",
      facts=["house.005", "inn.015", "food.031", "job.011", "house.011", "daily.012", "inn.030"],
      jb=(0.30, "全景", 0.30, "全景"), jbcam=("客店房间门口夜全景", "客店房间床尾吹灯全景"),
      hands="进门先把话筒与采访本放到桌上油灯旁，此后两手空着",
      carry=[WILLOW + "（进门时）→ " + WILLOW_TABLE + "（坐下前取下）"],
      cuts=[(0, 8, "房门口夜全景：她推门进来，把话筒本子和柳枝放到桌上", "开场"),
            (8, 20, "床尾近处：她蹲在床腿旁把布包拴到床腿上", "同段延续（缓推到床尾）"),
            (20, 28, "床尾全景：她坐回床边侧耳听窗外，然后俯身吹灭油灯", "切（换到床尾）")],
      sstate=["布包还放在床上，没有拴；床腿上没有任何绳子；" + WILLOW + "，到本段末已放到桌上",
              "布包已提到床尾床腿边；麻绳先一圈圈绕上床腿，到本段末已打成死结拉紧；" + WILLOW_TABLE,
              "布包已拴好：" + KNOT + "；此后一直拴着；油灯先亮着，本段最后被吹灭"],
      title="【住·过夜】回客店 · 拴好行李 · 吹灯",
      summary="三更回客店：油灯点着，窗外夜市还没散；照旅客守则把布包拴在床腿上；三更以后提瓶卖茶的出来了，军巡铺的兵在巡警；春天淘沟的泥坑夜里敞着，回来得看脚下；她俯身吹灭油灯。",
      plot="三更，沿城客店的房间，桌上一盏陶油灯亮着；宋装的林问推门进来，先把话筒和采访本放到桌上油灯旁，把包髻上那枝柳取下放在旁边，揉着腿在床边坐了一下；然后起身从桌上拿起一截麻绳，把床上装着白天换下衣服的本白布包提下来，蹲到床尾那条床腿旁，用麻绳绕两圈，打了个死结；她坐回床边，侧耳听窗外，远处有人提着瓶子走过，更远处有兵在巡警，听不清喊的是什么；最后她俯身吹灭了油灯",
      cam="0–8s 房门口夜全景，眼平，24mm，f2.8，机位固定，油灯在画面中心；8–20s 机位缓推到床尾近处，眼平略俯，同时由 24mm 缓变焦到 35mm；20–28s 切到床尾全景，眼平，24mm，机位固定",
      block="她先在门口，然后到桌边、床边；油灯在桌上；直棂窗在她身后画右，窗外近黑；房里只有她一个人；窗外提瓶的人与巡警的兵不入画",
      act="0–3s 门推开，她进来，把门关上；3–6s 先把话筒和采访本放到桌上油灯旁，再把包髻上的柳枝取下放在旁边；6–8s 揉着小腿在床边坐一下；8–10s 先站起身，从桌上拿起一截本色麻绳，把床上的本白布包提下来，然后才蹲到床尾那条床腿旁——身体正对床腿、相距约一小臂，肩、上臂、前臂到手是一条完整可见的连线；10–15s 用麻绳在床腿上绕两圈；15–20s 在床腿外侧打一个死结、拉紧、留一截一拃长的绳头，两只手都收回来；20–22s 然后才扶着床沿站起，坐回床边；22–25s 侧耳听窗外；25–28s 俯身吹灭桌上的油灯，灯焰一晃熄灭，升起一缕细烟，屋里暗下去",
      lines=[L(0, "画外", "回到客店，灯点上。窗外夜市还没散。", "Back at the inn. Lamp lit. The night market's still on.", 4, "house.005", "解说", "中", "桌上亮着的油灯"),
             L(4, "画外", "那本旅客守则还说，夜里行李要锁好拴牢。我没带锁，先拴在床腿上。", "The guide says lock and tie down bags at night. No lock, so: bed leg.", 6, "inn.015", "照着做", "中", "手里绕着的麻绳"),
             L(10, "画外", "听，外头提着瓶卖茶的，三更以后才出来——京城人忙到半夜才回家。", "Listen — the tea sellers come out after midnight. People here work till late.", 5.5, "food.031", "侧耳听", "中", "床腿上刚打好的结"),
             L(16, "画外", "外头是军巡铺的兵在夜里巡警。春天城里淘沟的泥坑夜里敞着，走回来得看脚下。", "Patrol soldiers are on watch. Spring drain pits stay open at night — watch your step.", 7, "job.011 house.011 daily.012", "轻", "中", "窗外"),
             L(23, "画外", "睡了。", "Bedtime.", 1.0, "", "轻", "慢", "桌上的油灯")],
      light="三更，夜里，桌上一盏陶油灯是唯一光源，暖调低照度，只照亮她的脸、床边与布包，屋角在黑里；窗外近黑，窗棂缝里只透进一点极暗的灰，不是月光、不是蓝色的光；屋角炭盆是空的；吹灭后屋里全暗",
      pace="进 → 放下 → 拴 → 打结 → 听 → 吹灯",
      spatial="机位＝房门口全景（固定）→ 缓推至床尾近处 → 床尾全景（固定）；在画主体＝油灯下的房间 → 床腿边拴布包的她 → 吹灯的她；窗在她身后画右",
      contrast="首帧＝推门进来、油灯亮着的房间（全景 0.30）→ 末帧＝她俯身吹灭油灯、屋里暗下去（全景 0.30）。**一天逛完，先把东西拴好，再把灯吹了。**",
      moment="**27s 灯焰一晃熄灭**",
      judge="「邻里巡夜吆喝」出自县里的规矩，汴京夜巡改军巡铺（R6 W09，inn.014 换 job.011 / house.011），负向补更夫（R6 W17）；「三更尽」已在 shot30 讲过，删（R5 F20）；「我没锁」改「我没带锁」（R1 R44）；绳结状态账本拆成三段、打结在第二段完成（R2-39），先站起再蹲到床腿旁、写明身体与床腿距离（R2-40）；吹灯挪到本镜镜尾、shot34 只拍五更醒来（R2-41 / R3-21），切到床尾全景，两端景别相同但下一镜起幅是俯拍近景；柳枝在进门后取下放桌上（R2-32 / R5 F03）；窗外近黑不写深蓝（R4 F30）；时长 24→28 s"),

 dict(n=34, seg="合", sec="住·收", d=24, bg="bg14_客店房间夜", v="bg14-2", lt="dawn", tod=10, tier="A",
      ch=["c1"], pr=[], unit="收", indoor=True, neg_add="更夫敲锣打梆, 窗纸, 睡觉时手里握着话筒",
      facts=["job.012", "daily.002", "inn.026", "inn.027"],
      jb=(0.90, "近景", 0.75, "近景"), jbcam=("床头侧上方俯拍她躺着的脸", "床边正面近景"),
      hands="话筒与采访本放在桌上灭了的油灯旁、不在手里；揉后脑勺用右手",
      carry=[WILLOW_TABLE, "床腿上的布包仍拴着：" + KNOT],
      cuts=[(0, 4, "五更：窗棂间透出极淡的清冷蓝色天光，铁牌声一下一下，她睁开眼", "开场"),
            (4, 24, "她坐起来揉后脑勺，正对镜头说话", "切（换到床边正面）")],
      sstate=["油灯早已灭着、不再点亮；布包拴在床腿上；那枝柳横放在桌上",
              "与上一段相同：油灯灭着，布包仍拴着，柳枝仍在桌上；天光比上一段略亮"],
      title="【住·收】五更报晓 · 打分 · 签名收尾",
      summary="五更，铁牌一下一下报晓，窗棂间透出极淡的清冷蓝色天光；她坐起来给客店打七分；问置顶评论问题，签名收尾两句。桌上是那枝柳和话筒本子，床腿上的布包还拴着。",
      plot="五更将尽，外面传来一下一下敲铁牌的声音，直棂窗的窗棂间透出极淡的清冷蓝色天光；宋装的林问躺在床上睁开眼，坐起来，揉了揉后脑勺，对着镜头说话；桌上灭了的油灯旁放着那枝柳和她的话筒、采访本，床腿上的布包还拴着",
      cam="0–4s 床头侧上方俯拍近景，俯角三十度，50mm，机位固定，她躺着的脸与枕头；4–24s 切到床边正面，眼平，50mm，f2，近景（胸口以上），机位固定",
      block="她在画面中央的床上；0–4s 躺着、闭眼到睁眼；4–24s 坐起来正面朝镜头、看镜头说话；睡下不卸盖头与胸牌；房里只有她一个人",
      act="0–2s 铁牌声里她还闭着眼；2–4s 睁开眼；4–8s 她坐起来，揉着后脑勺看镜头给客店打分；8–16.5s 看着镜头认真问你；16.5–24s 看着镜头说签名收尾两句，最后微微一笑",
      lines=[L(0, "画外", "五更了，外头有人敲铁牌报晓。书上说「闻此而起」——该起床了。", "Fifth watch: the iron plate. The book says hear it, get up.", 4.5, "job.012 daily.002", "刚醒", "慢", "窗棂间清冷的蓝色天光"),
             L(4.5, "对镜", "床硬，瓷枕真凉，但睡着了。七分。", "Hard bed, cold pillow, but I slept. Seven.", 3.0, "inn.026 inn.027", "揉后脑勺"),
             L(8, "对镜", QUESTION, EN_QUESTION, 8.5, "", "认真问你"),
             L(16.5, "对镜", CLOSER[0], EN_CLOSER[0], 3.0, "", "平", "慢"),
             L(19.5, "对镜", CLOSER[1], EN_CLOSER[1], 4.0, "", "笑一下", "慢")],
      light="五更末，窗棂间透出极淡的清冷蓝色天光，冷而柔、很暗，只勾出她半边脸的轮廓；油灯不再点亮，画面里没有任何火；屋角炭盆是空的",
      pace="醒（铁牌声）→ 坐起 → 打分 → 问 → 签名收尾",
      spatial="机位＝床头侧上方俯拍（固定）→ 床边正面近景（固定）；在画主体＝醒来的她 → 坐起来对镜说话的她；窗在她身后",
      contrast="首帧＝铁牌声里闭着眼的脸（近景 0.90）→ 末帧＝窗棂间清冷的蓝色天光里她对镜头微笑（近景 0.75）。**灯昨晚就灭了，这一天亮了。**",
      moment="**23s 她说完「下一站见」微微一笑**",
      post="签名收尾两句逐字；8–24s 的评论问题与 publish.md 置顶评论逐字一致；零笑点；铁牌声进音床（daily.002）",
      judge="吹灯挪到 shot33，本镜只拍五更醒来，镜内不再有 4 秒纯黑段（R3-21 / R2-41）；铁牌与天光之间隔了一两个时辰，本镜从五更将尽起（R5 F21）；天光写暗（R4 F31）；「闻此而起」补一句白话（R1 R31）；打分拆成画外感受＋对镜打分，评论问题放宽到 6 秒（R1 R32）；瓷枕补 inn.027（R6 W12）；睡下不卸盖头与胸牌：五样恒定符号优先于起居真实（R2-42，判断）；柳枝与绳结状态串照带；景别档起幅俯拍近景 0.90（上一镜落幅全景 0.30，比值 0.33）"),

 dict(n=35, seg="收", sec="航拍收束", d=20, bg="bg16_汴京全城五更", v="bg16-1", lt="dawn_lamp", tod=10, tier="S", aerial=True, xuande=True,
      ch=[], pr=[], unit="收", crowd=True, local=True, neg_add="明清青砖城墙, 一圈青砖城墙, 正南正北对齐的方格城市",
      day_tail="；除了街巷里几点正在熄灭的油灯，画面里没有别的火、没有灯笼",
      facts=["route.001", "travel.016", "city.021", "city.024", "city.038", "job.012", "street.003", "house.005"],
      jb=(0.02, "远景", 0.02, "远景"), jbcam=("客店屋脊低空航拍", "全城高空斜俯航拍"),
      title="【航拍收束】五更天亮 · 退回整座城",
      summary="五更天亮，镜头从客店屋脊起飞，边退边升：屋脊下巷子里还剩两三点油灯，一点点淡下去；汴河上几条船开始撑篙；升到约六百米，外城城墙与护龙河是远处一圈细线，两座高塔的塔尖先被第一道光照到。无台词；后期叠考证卡。",
      plot="五更天亮，镜头从沿城客店的灰瓦屋脊上方起飞，边往后退边拔高，屋脊下的巷子里还亮着两三点豆大的油灯；天一点点变亮，那几点油灯越来越淡；汴河露出来，几条船开始撑篙；镜头一路拉远升高，外城城墙与墙外宽宽的护龙河在远处成一圈细线，城墙微微斜着、不是正南正北，东南和东北远处两座高塔；第一道低平的暖光先照到塔尖与城墙顶，贴地的薄雾从受光的地方开始变薄",
      cam="一个连续运镜、不切，24mm：0–6s 离屋脊约十四米，沿屋脊缓缓向后退并抬升；6–16s 边向后退边升到约六百米，镜头下俯约二十度朝西北；16–20s 减速悬停，整座城在画面里展开到地平线，外城城墙与护龙河是远处一圈细线，两座高塔立在远处。飞速平稳、不拖影。画面里没有任何飞行器，也没有飞行器的影子",
      block="画面里没有具名人物；早起的行人与船工只是远处剪影、不可辨面孔；可辨主体不超过八个，都不看镜头",
      act="0–6s 灰瓦屋脊在画面下方后退，屋脊下巷子里两三点油灯还亮着；6–11s 天色一点点变亮，那几点油灯在天光里越来越淡，其中一盏被人吹灭；11–16s 汴河露出来，几条船开始撑篙，船只有米粒大，河面是碧绿的、映着渐亮的蓝天；16–20s 第一道直射的暖光先照亮两座高塔的塔尖和外城城墙顶，贴地的薄雾从受光的地方开始散开，露出下面一格一格的街巷，镜头悬停；宫城正门远远只是一点深绿的屋顶",
      lines=[],
      light="五更末，东方天边从清冷的深蓝转成透亮的浅蓝、近地平线一线浅金，太阳还没出来，整座城先笼在清冷的蓝色天光里，屋脊下的巷子里还剩两三点豆大的暖黄油灯光；16–20s 太阳上沿刚露出地平线，第一道低平的暖光从画右（东面）先落在两座高塔的塔尖与城墙顶上，其余屋面仍在清冷的蓝光里；薄雾贴着地面",
      pace="起（屋脊）→ 升 → 灯淡 → 远（全城）→ 第一道光 → 停",
      spatial="机位＝客店屋脊上方连续后退拔高到全城高空斜俯；在画主体＝屋脊与巷灯 → 屋顶群与汴河 → 全城；运动方向＝向后、向上",
      contrast="首帧＝清冷蓝光里屋脊下还亮着的两三点油灯（远景 0.02）→ 末帧＝第一道暖光照上塔尖与城墙、雾正在散的整座城（远景 0.02）。**城里最后几盏灯灭掉，第一道光落在城墙上。**",
      moment="**17s 第一道直射光落在塔尖与城墙顶，巷子里最后一点油灯已灭**",
      post="考证卡与「本站 N 条事实 · M 条存疑」由后期叠在本镜；环境音＝远处报晓铁牌声 + 早起的零星人声（没有可辨字句）；可选的 shot36 不入片时，本镜末帧就是全片最后一帧",
      judge="片尾顺序改为客店过夜 → 本镜五更航拍 → 可选的今日遗址（R5 F07 / 协调者裁定 2），镜号 36→35；主体改挂 bg16_汴京全城五更、锁定串照卡（协调者裁定 6）；有零星油灯，挂有灯负向、去掉「提亮的黑位」，不挂蜡烛组（bg16 卡判断：酒店灯烛 street.003 ✅）；高度按 R3-26 改为约六百米、城墙是远处细线，不再写看得清护城河两岸杨柳；灯熄与第一道光（R4 F19）；远处宫城门楼按宣德楼例外处理；B_city 渲 `shots/shot35/shot35_previz.*`"),

 dict(n=36, seg="收", sec="可选实验", d=24, bg="bg9_今日州桥遗址", v="bg9-1", lt="day", tod=99, tier="A", optional=True,
      ch=["c1m"], pr=[], unit="看一眼",
      hands="右手握话筒；采访本塞进夹克左内袋，左手扶着坑沿栏杆",
      neg_drop=["现代建筑", "电线杆", "柏油路", "玻璃窗", "玻璃门", "塑料感材质"],
      neg_add="保护棚, 钢结构大棚, 博物馆展厅, 玻璃地板, 玻璃罩, 脚手架, 古装人物, 展示灯, 冷白 LED 光, 发掘坑里的人, 游客在坑底行走触摸石壁, 仿古复原的州桥楼阁, 景区大门牌坊, 可读文字标牌, 彩绘浮雕, 龙纹凤纹, 石狮, 完整的北宋平桥桥身, 兽角特写",
      facts=["zhouqiao.002", "zhouqiao.004", "zhouqiao.001"],
      jb=(0.30, "全景", 0.80, "近景"), jbcam=("遗址坑沿侧后方全景", "坑沿边侧脸近景"),
      title="【可选实验】带你看一眼 · 今天的州桥",
      summary="**可选实验。** 现代装的林问站在今天开封州桥遗址的探方边，像来参观的人一样往下看：很深的发掘坑、刻着瑞兽、双鹤与祥云的北宋石壁，和一座明代早期在宋代桥基上重修的砖拱桥。白天在州桥上扶栏看的，就是这种石壁。",
      plot="今天的河南开封，城市街区地面下挖开一片很深的方形考古发掘区，坑壁是一层层叠压的土层剖面；坑底一侧露出青灰色大条石砌成的河岸石壁，石面上是浅浮雕：一匹像马又像鹿、昂首四蹄腾空的瑞兽，前后两只伸长脖子飞翔的鹤，四周是卷曲的云纹，浮雕整体高过两个成年人；石壁旁是一座青砖拱券的单孔桥体；现代装的林问站在坑沿边，扶着栏杆往下看，最后转头看向镜头",
      cam="一个机位。坑沿参观处，她侧后方约三米、眼平略俯，f4；0–6s 全景（她与发掘坑），28mm，机位固定；6–24s 机位沿坑沿向她推近约一米，同时由 28mm 缓变焦到 50mm，到她侧脸近景，石壁浮雕在她身后柔焦；20s 起她转头时机位不动，让她的正脸进画",
      block="林问站在坑沿边画面右侧、侧身朝画左下方的发掘坑、不看镜头，20s 起转头看镜头说话；画面里没有其他人",
      act="0–6s 她扶着坑沿栏杆往坑里看；6–12s 视线顺着石壁上的瑞兽浮雕移过去；12–16s 看向石壁旁的青砖拱桥；16–20s 抬头看坑壁一层层的土；20–24s 转过头看镜头，轻声说话",
      lines=[L(0, "画外", "走之前，带你看一眼这里今天的样子：开封城底下，挖开了一个很深的坑。", "Before we go, here's this spot today: a deep excavation under modern Kaifeng.", 6.0, "zhouqiao.004", "轻", "中", "发掘坑"),
             L(6, "画外", "坑边的石壁上刻着瑞兽、仙鹤和云。白天我在州桥上扶栏看的，就是这种石壁。", "The wall is carved with a beast, cranes and clouds — like the one I leaned over this afternoon.", 6.5, "zhouqiao.002 zhouqiao.001", "轻", "中", "石壁上的瑞兽浮雕"),
             L(12.5, "画外", "旁边那座砖拱桥，考古报告说是明代早期在宋桥的桥基上重修的，不是北宋的州桥。", "The brick arch beside it is an early Ming rebuild on the Song foundations — not the Northern Song bridge.", 7.5, "zhouqiao.002", "实话", "中", "青砖拱桥"),
             L(20.5, "对镜", "九百年，就压在这层土底下。", "Nine hundred years, right under this soil.", 3.0, "", "轻，落定")],
      light="今天白天的天光，从坑口斜照进来，坑壁和坑底石壁上有几块边缘清楚的光斑，其余在柔和的阴影里",
      pace="看（坑）→ 看（浮雕）→ 看（砖桥）→ 抬头 → 转头",
      spatial="机位＝坑沿参观处侧后方（向她推近并变焦）；在画主体＝发掘坑与坑沿的她；她朝画左下方的坑，最后转头看镜头",
      contrast="首帧＝很深的发掘坑与坑沿的她（全景 0.30）→ 末帧＝她转头看镜头、浮雕石壁在身后柔焦（近景 0.80）。**九百年，一层土。**",
      moment="**21s 她转头看镜头**",
      judge="W12 已把 zhouqiao.002 升为 ai_read、新增 zhouqiao.004（2018–2022 发掘、公众考古研学示范基地开放、观众站在探方边）；按 W12 边界：画探方、瑞兽双鹤祥云石壁、明代早期在宋桥基上重修的砖拱桥，她像参观者一样站在坑沿；不画保护棚与博物馆（zhouqiao.005 ai_draft），不报石壁长度、不给兽角特写、不说遗址仍深埋（R6 F04）；bg9 卡锁定串已改为「很深的考古发掘坑」（2026-09-14 SYNC_sk1 删去「钢棚下」与生成器替换表）；石壁一句回扣 shot16（R5 F14）；开场句接在签名收尾之后要有过渡（R1 R22）；对镜台词转头看镜头（R2-43）；推近与变焦写清（R3-23）；时长 20→24 s；时辰是今天（tod 99，可选镜不进时辰闸门）；负向删去「现代建筑」等今天应有的东西"),
]

# ═══ 镜表结束

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build()
