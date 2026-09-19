# -*- coding: utf-8 -*-
"""《时空旅行》sk2 · 暴风城的一天 —— 分镜 + 五层 prompt 生成器（阶段 5/6 合一）。

改内容＝改本文件重跑（rule 4i ①）：
    python tools/gen_shots_sk2.py                 # 严格：任何闸门不过直接终止
    python tools/gen_shots_sk2.py --allow-pending # 资产卡未齐时：缺锁定串只报 warning
    python tools/gen_shots_sk2.py --check         # 只跑闸门，不写盘

产物：5_6_分镜与prompt/{shotlist.md, shots/shotNN/shotNN.md, all_shot_prompts.md}
      4_剧本/{script.md, dialogue.md}（中英两条，由镜表生成）

形态（系列 follow-up 008 / 009 / 014 / 015 + divergence #112 / #113）：
  · 只有艾拉解说（对镜 `正常台词` / 画外 `内心独白`），视频原声英语、中文走译配轨
  · 当地人**有逐字原文才能开口**，本片只有四句（面包小贩 / 旅店老板 / 卫兵 / 酒馆老板）
  · 偶尔的 NPC 互动分三档；**知识只由艾拉讲，NPC 不是解说员**
  · 本站**不设当天大事**，张力由玩家共同记忆 + 三类麻烦 + 王座厅的戏剧反讽承担

构建闸门（不合格直接 raise，分镜生成不出来）：
  ① 单镜 15–30 s；片长 860–900 s
  ② 英文 ≤ 2.8 词/秒（逐镜）
  ③ 正向 prompt ≤ 5000 字（K10）；零 hex（K9）
  ④ `tod` 单调不减
  ⑤ 相邻镜景别档：比值 ≥ 2.0 或 ≤ 0.5，**且机位标签不同**；唯一豁免是承接对 S01→S02
  ⑥ 锁定串从卡里抽出做相等比较（style_guide / 人物卡 / 场景卡）
  ⑦ 装束态按镜号区间切换（S01–S12 现代装，S13 换装镜，S14+ 平民装）
  ⑧ 色温三角条件化：非矮人区镜必须反向声明无炉火；非月亮井镜无自发光；非法师区夜镜无紫光
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRAMA = REPO / "ai_videos" / "shikong_lvxing" / "sk2"
A = DRAMA / "2_世界观人设"
ROOT = DRAMA / "5_6_分镜与prompt"
SERIES_CHARS = REPO / "ai_videos" / "shikong_lvxing" / "_series" / "characters"
NL = "\n"
FENCE = "`" * 3

MAX_PROMPT = 5000
MIN_D, MAX_D = 15, 30
TOTAL_LO, TOTAL_HI = 860, 900
MAX_WPS = 2.8
TOD_ORDER = ["清晨", "上午", "正午", "午后", "傍晚", "日落", "入夜", "夜"]

STYLE_BASE = (
    # 2026-09-19 用户：「画面太像劣质游戏 CG，我们要真实感」。
    # 旧串以「半写实」开头、又写「忠于原作」——而原作是一款游戏，正面在要求游戏美术，
    # 负面挂再多「游戏引擎渲染」也没用（正面永远赢负面，同侏儒五指、同东亚脸）。
    # 根子是把两个独立的轴混成一个：形制/配色按暴风城设定（该保），影像真实度被一起降了（不该降）。
    # 口径与 `gen_scene_prompts_sk2.py` 的 look 层、`ai_video.md` §18 逐字同源。
    "**实拍电影画面，不是渲染图、不是游戏截图、不是概念原画**——拍的是按设定搭出来的实景与真人演员；"
    "ARRI ALEXA + Cooke S4/i 定焦实拍，1/48 秒自然运动模糊；"
    "《权力的游戏》那一路的影调：高光柔滚不死白，暗部厚实该黑就黑，不抬亮不补蓝，"
    "受光面与阴影差三档、**阴影里只留很少细节**；颜色压过、偏灰偏实，不是纯色块；"
    "**不是全景深**——最近的主体最实，每往深一层软一档，最远一层只剩偏蓝灰的轮廓，**空气看得见**；"
    "做旧按材质写死：石有凹坑与缝里积灰、木起毛刺与霉斑、铁起麻点又被手磨亮、布洗到发白有补丁，"
    "**同类构件绝不重复、不是崭新的、不是重复贴图**；"
    "边缘略松、淡暗角、轻微色散与柔光晕，细腻不匀的胶片颗粒；画面内不出现任何文字"
)

NEG_TEXT = "任何文字, 字母, 汉字, 数字, 印刷体, 手写体, 招牌文字, 碑文, 门牌号, logo, 二维码, 价目表, 灯箱, 霓虹"
NEG_STYLE = ("游戏截图, 游戏引擎渲染, UI 界面, 血条, 名字牌, 低多边形, 卡通渲染, 赛璐璐描边, 塑料高光, "
             "过饱和, 3D 建模预览, 白模, 灰模, 灰褐色石城, 米那斯提力斯, 通用中世纪城堡, 哥特尖顶群, "
             "红瓦屋顶, 茅草屋顶")
NEG_VERSION = ("暴风城港口, 码头, 栈桥, 泊位, 帆船, 桅杆, 船帆, 船锚, 水手, 跳板, 灯塔, 攻城器械, "
               "公园废墟, 焦黑巨坑, 塌陷地面, 龙的爪痕, 狮王之息, 瓦里安·乌瑞恩, 成年国王坐在王座上, "
               "乌瑟尔雕像, 持战锤的圣骑士雕像, 传送门大厅, 一排排发光的传送门, 暴风城大使馆, "
               "矮人区的拍卖行, 矮人区的银行, 淤泥半淤浅的运河, 倒塌的雕像, 塔楼上的爪痕, 理发店")
NEG_RACE = ("德莱尼, 血精灵, 狼人, 熊猫人, 虚空精灵, 地精, 狐人, 兽人, 巨魔, 牛头人, 亡灵, "
            "部落旗帜, 部落纹章")
NEG_MODERN = ("电灯, 路灯杆, 灯泡, 玻璃幕墙, 平板玻璃窗, 金属栏杆, 交通指示牌, 井盖, 沥青路面, 水泥, "
              "空调外机, 电线, 电线杆, 拉链, 手表, 手机, 相机, 运动鞋")
NEG_BIO = ("五指的侏儒, 净面的矮人, 山羊胡矮人, 缩小版人类比例的矮人, 净面的暗夜精灵男性, "
           "头顶鹿角的暗夜精灵, 眼睛向外射光, 眼周光斑, 女性卫兵")
NEG_SKY = "满天飞行坐骑, 龙, 飞行扫帚, 飞行地毯, 悬停在广场上空的坐骑, 空中交通"
NEG_NPC = "自编的 NPC 台词, 无出处的对白, 路人对口型, 旅行者与当地人交谈, NPC 讲解设定"
NEG_FIRE = "炉火, 锻炉, 明火, 暖橙色光源, 火星, 篝火, 火把照亮整条街"
NEG_GLOW = "自发光的水面, 魔法光源, 发光符文, 悬浮光点"
NEG_PURPLE = "紫色光源, 奥术灯光, 紫色辉光"

NEG_BASE = ", ".join([NEG_TEXT, NEG_STYLE, NEG_VERSION, NEG_RACE, NEG_MODERN, NEG_BIO, NEG_SKY, NEG_NPC])

# 装束态切换（divergence：段 3 在旅店换装）
MODERN_UNTIL = 12          # S01–S12 现代装
CHANGE_SHOT = 13           # S13 是换装镜（镜内由现代装变平民装）

# 色温三角的归属（style_guide §4）
FIRE_BG = {"bg4"}          # 仅矮人区允许暖橙炉火
GLOW_BG = {"bg8"}          # 仅月亮井允许自发光乳白冷蓝
PURPLE_BG = {"bg9"}        # 仅法师区夜镜允许紫色奥术灯
DARK_BG = {"bg5", "bg6"}   # 全封闭地下，无天光

BG_NAME = {
    "bg0": "暴风城全城", "bg1": "英雄谷", "bg2": "贸易区", "bg3": "旧城区",
    "bg4": "矮人区", "bg5": "矿道地铁站台", "bg6": "矿道地铁水下段",
    "bg7": "教堂广场与光明大教堂", "bg8": "花园区月亮井", "bg9": "法师区",
    "bg10": "王座厅", "bg11": "运河", "bg12": "镀金玫瑰旅店堂屋",
}

# NPC 逐字原文（divergence #113；tag 只能是 ✅，一个字不得自编）
NPC_LINES = {
    "S09": ("面包小贩 Thomas Miller", "Rolls, buns and bread. Baked fresh!", "en-m-sw-baker-01"),
    "S11": ("旅店老板奥里森 Allison", "Welcome to my Inn, weary traveler.", "en-f-sw-allison-01"),
    "S18": ("酒馆老板 Reese Langston", "Grab a drink my friend and pull up a seat, the more the merrier!", "en-m-sw-tavern-01"),
    "S41": ("暴风城卫兵", "Light be with you, sir.", "en-m-sw-guard-01"),
}


def S(sid, tod, d, bg, jb, jbcam, sf, plot, block, act, vo_en, vo_zh, light,
      facts, kind="内心独白", hero=False, seam="硬切（独立首帧）", extra_ref=(), note=""):
    """一条镜的数据。sf = (起幅人占画高, 落幅人占画高)。"""
    return dict(id=sid, tod=tod, d=d, bg=bg, jb=jb, jbcam=jbcam, sf=sf, plot=plot,
                block=block, act=act, vo_en=vo_en, vo_zh=vo_zh, light=light, facts=facts,
                kind=kind, hero=hero, seam=seam, extra_ref=list(extra_ref), note=note)


SHOTS = [
    S("S01", "清晨", 25, "bg0", "极远→远", "航拍低空前飞", (0.09, 0.09),
      "无人机高度贴着艾尔文森林的石板大道向北低飞，前方城墙自树冠后升起，镜头对准城门洞笔直穿过去，门洞内壁的石纹从画框两侧飞速掠过，出洞后英雄谷豁然展开",
      "画面里没有人；镜头始终沿大道中轴前进，高度约在树冠上沿",
      "0–9s 掠过林间大道；9–16s 穿过城门洞，光线由亮转暗再转亮；16–25s 出洞，英雄谷的巨像依次从两侧掠过",
      "", "", "清晨低角度暖金侧逆光，长影铺在石板路上，薄晨雾贴地；穿过门洞时短暂的暗，出洞一瞬强烈的逆光",
      ["arch.006", "landmark.001", "district.*"], kind="无台词", seam="尾帧锁定（交接源 → S02）",
      note="I-14 航拍开场第一镜；末帧须存为 shot01_lastframe.png 供 S02 承接"),

    S("S02", "清晨", 28, "bg0", "远→中远", "航拍拔高后退", (0.38, 0.09),
      "承接上一镜末帧继续起升后退，暴风城的八个城区连同串联它们的运河在画面里一圈圈铺开，最后镜头回落到英雄谷石桥头的高度",
      "画面里没有人；航线沿运河逆时针绕城一周",
      "0–18s 拔高后退，城区依次入画；18–28s 回落到石桥头高度，末 8–10 s 叠签名开场画外",
      "Nothing special about today. You're in Stormwind — a place millions have walked through, and no one has ever been to. Everything is as the lore says — except I'm here.",
      "今天没什么特别的。你在暴风城——一座几千万人走过、却从没有人真的去过的城。一切都和设定里一样——只是，多了一个我。",
      "清晨暖金侧逆光；城区的蓝色屋顶在逆光里压成剪影，运河水面反出一条亮带",
      ["district.*", "arch.002"], kind="内心独白", hero=True,
      seam="承接 shot01 末帧（首帧＝上一镜末帧）", extra_ref=("本镜首帧(上一镜末帧)=>@",),
      note="I-2 签名开场叠在末 8–10 s"),

    S("S03", "清晨", 21, "bg1", "中景", "地面平机位正对", (0.38, 0.38),
      "艾拉站在英雄谷石桥头对着镜头，身后是夹道的巨像与远处的城",
      "她站在桥面中线偏右，正面朝镜头；巨像在她身后左右各一尊，形成对称框",
      "0–4s 她把采访本收进臂弯；4–18s 对镜说逛单；18–21s 转身朝城里走，镜头留在原位",
      "I'm Ella, with the Timeline Survey. One gold piece, one day. Eight districts, three meals, one night — on a day when nothing happens. Bread: one silver twenty-five. A laborer earns about a silver a day — my estimate, not the lore's.",
      "我是艾拉，时空考察队的旅行者。一枚金币，一天。我要走完八个城区、吃三顿、住一晚——看看在什么都没发生的一天里，这座城长什么样。一条面包一银二十五铜。一个平民一天挣大约一银——这个数字是我推的，设定里没写。",
      "清晨暖金侧逆光从她左后方来，脸的右侧留一道亮边；背景的城在薄雾里发亮",
      ["price.*", "lore.024"], kind="正常台词",
      note="I-3 逛单 + 两个物价锚；⚠️ 日薪是推算，口播已明说"),

    S("S04", "清晨", 19, "bg1", "远→中", "桥面低机位正跟", (0.09, 0.38),
      "一镜到底第一段：镜头贴着桥面在她身后低位跟进，两侧巨像依次从画框上方掠过",
      "她沿桥面中线向北走，步速平稳；镜头始终在她身后约三米、高度约膝",
      "0–7s 起幅大远景，她在画面下方很小；7–19s 镜头推近，走过前两尊巨像，落幅中景",
      "Every single person who ever entered this city walked in under these. Five statues. All of them heroes of the Second War.",
      "所有进过这座城的人，都从这几尊像脚下走过。五尊。全是第二次战争的英雄。",
      "清晨暖金逆光，巨像在逆光里是浅灰白的剪影，金色嵌线偶尔反出一点光",
      ["lore.024", "lore.025"]),

    S("S05", "清晨", 19, "bg1", "紧→全", "侧机位平跟", (0.9, 0.38),
      "一镜到底第二段：硬切到侧面紧取景跟她的脸，随后镜头后拉，法师像与狮鹫像进入画面",
      "她继续向北走，镜头在她左侧与她同速平移；巨像在画面右侧依次进入",
      "0–5s 紧取景跟脸，她边走边讲；5–19s 镜头后拉成全景，法师像与展翅的狮鹫像入画",
      "This one's a mage — you can tell by the staff. And that's a gryphon, mid-take-off, carved in stone. Nobody does subtle here.",
      "这尊是法师，看法杖就知道。那是一只狮鹫，正要起飞，用石头刻的。这座城不讲含蓄。",
      "清晨暖金侧光打在她脸的左侧；巨像的浅灰白石在逆光里泛暖",
      ["lore.024"]),

    S("S06", "清晨", 26, "bg1", "极远→中近", "高机位俯拍", (0.09, 0.9),
      "一镜到底第三段：硬切到高机位俯拍整条石桥，随后镜头下降推进，落到她在铭牌前停下的中近景",
      "她走到第三尊像的基座前停住，侧身面向铭牌；镜头由高处下降到她侧后方",
      "0–10s 高机位俯拍，她在画面中很小；10–20s 下降推进；20–26s 落幅中近景，她伸手摸了一下铭牌的边",
      "Five plaques. Four of them end with the same two words: presumed deceased. Only one doesn't — hers. Alleria's. Nobody ever wrote her off.",
      "五块铭牌。四块用同样两个词收尾：推定已故。只有一块没有——她的。奥蕾莉亚。没有人把她算作失踪。",
      "清晨暖金逆光；俯拍段桥面反光成一条亮带，落幅时她的手在铭牌上投下一道短影",
      ["lore.024", "lore.025"], hero=True,
      note="铭牌上不许出现可读文字，字由后期贴"),

    S("S07", "清晨", 17, "bg1", "中景", "地面平机位侧向", (0.38, 0.38),
      "乔纳森将军骑在披蓝金马衣的白色战马上立于桥中段，艾拉走过时停下向他敬了个礼",
      "将军在画面右侧、马头朝画面左；她从画面左侧进入、在马前三步停住、正身面向他",
      "0–5s 她走近停住；5–10s 她抬手敬礼，他回礼；10–14s 她挥了挥手，他点头回挥；14–17s 她继续朝前走",
      "He doesn't say anything. He doesn't have to. That's the whole exchange — and honestly, that's most of my conversations today.",
      "他一句话没说。也不用说。整个交流就这些——老实讲，我今天大部分对话都是这样。",
      "清晨暖金侧光；白马的毛在逆光里发亮，板甲反出冷白高光",
      ["person.015", "person.016"],
      note="档 1 无声互动（divergence #113）；将军全程零台词"),

    S("S08", "上午", 21, "bg2", "全→中", "手持跟随", (0.09, 0.38),
      "贸易区喷泉边，她穿过人群依次走过银行、拍卖行、邮箱三处门脸，喷泉始终在前景",
      "她沿广场弧线走，镜头手持在她侧后方跟随；喷泉在画面近处作前景层，人群在中景",
      "0–7s 全景，喷泉水柱前景，她自画面右侧进入；7–16s 跟随她走过三处门脸；16–21s 她在邮箱前停住回头对镜",
      "Bank. Auction house. Mailbox. Three stops, twenty paces apart. If you ever played here, this was your whole routine — and you never once looked up at the roofs.",
      "银行。拍卖行。邮箱。三站，相隔二十步。你要是在这儿待过，这就是你的全部日常——而你一次都没抬头看过屋顶。",
      "上午高位偏白日光，影子短而硬；喷泉水花在逆光里发白",
      ["lore.014", "lore.015", "lore.016", "lore.017", "lore.018", "lore.019"]),

    S("S09", "上午", 19, "bg2", "中→近", "俯拍手部", (0.09, 0.9),
      "面包小贩沿街走过来吆喝，她叫住他买下最便宜那档的面包，镜头俯拍她数铜币的手",
      "小贩自画面左侧走来、在她面前侧身停住；她正面朝他、镜头在她右肩上方俯视她的手掌",
      "0–5s 小贩走近吆喝；5–12s 她指了指托盘、伸手；12–19s 俯拍她把铜币一枚枚数进小贩掌心，数到一半停下重数",
      "Twenty-five copper for the cheap one. And yes — I just lost count. Twice.",
      "最便宜那档二十五个铜板。是的——我刚数错了。两次。",
      "上午偏白日光；她掌心的铜币反出暗红褐的光",
      ["food.001", "food.002", "price.*"],
      note="档 2 互动：小贩说逐字原文；**她不与他交谈**，只用手势与点头"),

    S("S10", "上午", 20, "bg2", "近景", "地面平机位正对", (0.38, 0.9),
      "她在一处布摊前拿起一件苔绿色粗纺长袍，付钱后愣了一下，转头对镜说这笔账",
      "她侧身站在摊前、正面转向镜头；摊主在画面左侧背对镜头整理货",
      "0–8s 她把长袍展开在身前比了比、付钱；8–20s 她看看手里的袍子、看看刚买的面包、转向镜头",
      "Thirty-five copper. This whole robe. The loaf of bread I just bought cost one silver twenty-five — that's three and a half times more. In this city, dressing yourself is cheaper than feeding yourself.",
      "三十五个铜板。整整一件袍子。我刚买的那条面包一银二十五——是它的三倍半。在这座城里，穿的比吃的便宜。",
      "上午偏白日光从她右前方来，布料的织纹被侧光带出",
      ["price.*"], kind="正常台词", hero=True, note="爽点②"),

    S("S11", "上午", 19, "bg12", "全景", "室内低机位广角", (0.38, 0.38),
      "她推门进入镀金玫瑰堂屋，木梁、双楼梯、长吧台与木环烛台一次入画，老板奥里森在吧台后招呼她",
      "她自画面右侧的门进入、朝吧台走；奥里森在吧台后正面朝门；镜头在门内低位广角",
      "0–5s 门开、外面的光泼进来；5–12s 她走向吧台，堂屋全貌展开；12–19s 奥里森抬头招呼，她点头回应",
      "One inn. In the entire city, there is exactly one inn — and this is it. Every single traveller who ever slept in Stormwind slept right here.",
      "一家旅店。整座城里就这么一家——就是这儿。所有在暴风城睡过的人，都睡在这间屋子里。",
      "室内暖褐，光源只有壁炉、木环烛台上的一圈蜡烛、以及门口泼进来的一道日光；画面里没有电光",
      ["house.001", "house.002", "myth.018"],
      note="档 2 互动：奥里森说逐字原文"),

    S("S12", "上午", 26, "bg12", "近→特写", "壁炉侧光近景", (0.9, 0.9),
      "她在壁炉边把一块掌心大的扁石放在桌上，石头正面的凹槽纹样在侧光里显出来，石体内部透出极淡的暖光",
      "她坐在壁炉侧的长凳上，身体略前倾；石头放在桌面正中；镜头从她手的斜上方压下来",
      "0–10s 她从布包里取出扁石、放在桌上、指尖沿凹槽纹摸了一圈；10–20s 镜头推成特写，石体内部的暖光在暗处显出来；20–26s 她收手，光仍在",
      "This is a hearthstone. You bind it to an inn, and from anywhere in the world it brings you back here. One hour between uses. Every player who ever rolled Alliance bound theirs in this room — which makes this, statistically, the most homesick building in the world.",
      "这是炉石。你把它绑在一家旅店，从世界任何地方它都能把你带回这儿。一小时用一次。每一个联盟玩家都把炉石绑在这间屋里——所以从统计上说，这是全世界最想家的一栋房子。",
      "壁炉的暖光从她左侧来，桌面右半在暗处；石体内透的暖光**不外放、不投射、周围不形成光晕**",
      ["lore.001", "lore.002", "lore.010"], hero=True,
      note="玩家共同记忆第一位；光必须内透不外放"),

    S("S13", "上午", 17, "bg12", "中景", "室内平机位正对", (0.38, 0.38),
      "换装：她把现代装换成刚买的苔绿色粗纺长裙与本白短斗篷，逐件短切",
      "她站在楼梯旁的暗处，正面朝镜头；镜头固定不动",
      "0–4s 她把短斗篷披上、扣上黄铜圆扣；4–10s 系编绳束带；10–14s 换上深棕系带皮靴；14–17s 她把胸牌别到斗篷左襟、抬头看镜头",
      "Right. When in Stormwind.",
      "好吧。入乡随俗。",
      "室内暖褐，壁炉的光在她身后；她在半逆光里",
      ["dress.*"], kind="正常台词",
      note="**装束态切换镜**：本镜之前现代装、之后平民装"),

    S("S14", "上午", 17, "bg11", "中景", "水面低机位", (0.09, 0.38),
      "她在运河石沿上坐下来吃那条面包；旁边不远有人在垂钓，浮标浮在水面上",
      "她坐在石栏内侧的石沿上、侧身朝画面右；垂钓者在画面更远处的石阶上，背对镜头",
      "0–5s 她找地方、坐下；5–14s 掰面包、吃；14–17s 她抬头看水面上的浮标",
      "You cannot eat standing up here. Not won't — cannot. Every piece of food in this world says the same thing: you must remain seated while eating. So here I am. Sitting.",
      "在这儿你不能站着吃。不是不想——是不能。这个世界里每一样食物都写着同一句话：吃东西时必须保持坐姿。所以我就坐下了。",
      "上午偏白日光；水面反光在她脸的下半打出一层跳动的亮斑",
      ["myth.019", "food.003"],
      note="进食铁律，直接决定构图"),

    S("S15", "上午", 26, "bg11", "远景", "水平面低机位长镜", (0.09, 0.09),
      "镜头贴着运河水面沿河道缓缓前推，两岸的白石护岸与拱桥依次掠过，河面上空无一船",
      "画面里她不入画（画外解说）；镜头沿河道中线前推",
      "0–12s 沿河前推，第一座拱桥从画面上方掠过；12–26s 继续前推，河面始终没有一条船",
      "Look at this canal. Beautiful. Completely empty. There were supposed to be gondolas — they built the whole waterway for them, even made it so you could swim and climb back out. Then the technology turned out to be, and I quote, prohibitively esoteric. So the boats never came. The canal stayed.",
      "看看这条运河。漂亮。空空荡荡。本来这儿该跑贡多拉的——整条水道就是为它修的，连「能下水再爬上岸」都做好了。后来那项技术被认定——原话是——过于晦涩难成。船没来。运河留下了。",
      "上午偏白日光；水面明净偏蓝绿，护岸白石反光；堤顶到水面有明显落差",
      ["lore.042"], hero=True, note="最好用的冷知识之一"),

    S("S16", "上午", 17, "bg3", "紧取景", "手持窄巷跟随", (0.9, 0.9),
      "她穿过旧城区的窄巷，两侧墙面斑驳、屋顶是暗红褐色，墙根坐着几个衣衫破旧的人",
      "她沿巷子中线向前走、镜头手持在她身后近距跟随；巷口的光在远处",
      "0–7s 手持跟随进巷，光线一下暗下来；7–14s 走过墙根坐着的人，她放慢脚步但没停；14–17s 走向巷口的亮处",
      "Two bridges from the fountain and the roofs go from blue to dark red. That's how you know you've left the nice part.",
      "离喷泉两座桥，屋顶就从蓝色变成暗红褐色。你就是这么知道自己走出了体面的那半边城。",
      "上午日光只从巷口与头顶的缝隙进来，巷内大部分在阴影里；亮与暗的反差很大",
      ["myth.021", "house.008", "house.009"]),

    S("S17", "上午", 17, "bg3", "中→近", "平机位正对", (0.38, 0.9),
      "巷子尽头一道大铁闸门后面是一个从未启用的入口，门后一片漆黑；她隔着栅栏往里看",
      "她站在铁闸门前一臂远、正面朝门；镜头在她侧后方，随后切到她的正面近景",
      "0–7s 她走到门前停住、手扶栅栏；7–12s 镜头推近，栅栏后是纯黑；12–17s 她转向镜头",
      "This door has never opened. Not once. It was built for a player housing district that never shipped. It's still here, still locked, still leading nowhere. Remember it — there's another one like it, and we'll get there tonight.",
      "这道门从来没开过。一次都没有。它是为一个从未上线的玩家住宅区修的。它还在这儿，还锁着，还是通向什么都没有。记住它——城里还有一道一样的门，今晚我们会走到。",
      "上午日光斜射进巷子，铁栅栏在她脸上投下一道道竖影",
      ["lore.041"], note="线③上半，与 S41 收成一对"),

    S("S18", "正午", 17, "bg3", "全→中", "室内平机位", (0.38, 0.38),
      "她推门进入猪和哨声酒馆，老板在吧台后招呼；吧台上并排立着五种不同的酒器，角落里一个醉汉已经趴下了",
      "她自门进入、朝吧台走；老板在吧台后；醉汉在画面右侧角落的桌上趴着",
      "0–5s 进门；5–12s 老板招呼，她点头；12–17s 她在吧台边坐下，镜头带过五种酒器与趴下的醉汉",
      "Bottle. Skin. Flask. Flagon. Jug. Five different things to drink out of, all on the same counter. And one gentleman who has clearly worked his way through several of them.",
      "瓶、皮囊、扁壶、大酒壶、罐。五种喝酒的家伙什，全摆在同一张台子上。还有一位显然已经把其中几样都试过了的先生。",
      "室内暖褐，光源只有壁炉、桌上的烛台与窗；画面里没有电光",
      ["food.008", "food.010", "house.004"],
      note="档 2 互动：酒馆老板说逐字原文"),

    S("S19", "正午", 17, "bg3", "近→特写", "俯拍餐桌", (0.9, 0.9),
      "炉边一整排烤肋排在慢慢转，她要了一份坐下来吃",
      "她坐在靠炉的长桌边、侧身朝画面左；肋排在她身后的炉架上",
      "0–7s 炉架上的肋排特写，油滴落进炭里爆出一小簇火星；7–14s 她接过木盘、坐下、咬一口；14–17s 她抬头，嘴里还含着",
      "This is the only cooked dish in the entire city with a name and a person attached to it. Stephen Ryback's ribs. His own recipe. Eight out of ten — would have been nine if I hadn't burned my mouth.",
      "这是全城唯一有名有姓的熟食。史蒂芬·赖巴克的烤肋排。他自己的方子。八分——要不是烫了嘴，能给九分。",
      "炉火的暖橙光从她身后来，脸的轮廓有一道暖边；**本镜的火只是炉架的小火，不是矮人区的锻炉**",
      ["food.015"], note="评分③；笑点"),

    S("S20", "正午", 19, "bg10", "远→中远", "地面平机位前推", (0.09, 0.09),
      "她走过要塞吊桥进入庭院，再从封闭的室内通道走向王座厅门道",
      "她沿吊桥中线向前走、镜头在她身后前推；两侧卫兵成对立定不动",
      "0–9s 过吊桥，脚下木板与铁链在画面下缘；9–16s 进入庭院，两侧卫兵；16–19s 走进通往王座厅的室内通道，光线转暗",
      "Nobody stops me. Nobody asks what I'm doing here. I just walk in.",
      "没人拦我。没人问我来干什么。我就这么走进去了。",
      "正午顶光在庭院里反差最大，石面反光强；进入通道后光只从高处的细长券窗斜落",
      ["landmark.030", "landmark.031"],
      note="**Vanilla 是封闭室内通道**，不画露天步道、不画入口大喷泉、不画瓦里安雕像"),

    S("S21", "正午", 30, "bg10", "大全景", "长焦压缩大全景", (0.38, 0.09),
      "王座厅：穹顶石厅，高处细长券窗斜落光柱。台基上的王座里坐着一个约十岁的金发男孩；台阶下偏左立着一位全身板甲的男人；男孩右手边半步站着一位深紫近黑曳地长裙的女士",
      "她站在厅门内侧靠墙、画面最下缘只露半个肩；三个人在画面深处的台基一带，长焦把距离压平",
      "0–10s 长焦大全景建立；10–22s 镜头极缓慢前推，三个人的相对位置不变；22–30s 停住，男孩转头看了一眼身旁的女士",
      "That's the king. He's ten. His father went missing, so they put the crown on a boy. The man in the armour runs the kingdom for him. And the lady standing half a step to his right — she advises them both on how to spend the kingdom's resources. She looks more relaxed than anyone else in this room.",
      "那是国王。他十岁。他父亲失踪了，于是他们把王冠给了一个孩子。穿板甲的那位替他治理王国。而站在他右手边半步的那位女士——她给他们两个出主意，怎么调配这个王国的资源。她看上去比这屋里任何人都放松。",
      "正午顶光；光柱从高处细长券窗斜落，在台基石面上切出几道亮带，三个人一半在光里一半在暗里",
      ["person.001", "person.002", "person.003", "person.005", "person.006"], hero=True,
      note="**全片最高点·戏剧反讽**。绝不揭穿：不给暗示性特写、不给异色瞳、不给龙影、不给任何超自然视觉、不给音乐提示"),

    S("S22", "午后", 19, "bg10", "极远", "高机位俯瞰", (0.38, 0.09),
      "要塞外墙的高处俯瞰全城，八个城区与串联它们的运河一次入画",
      "她背对镜头站在垛口边、占画面很小；城在她面前铺开",
      "0–7s 建立俯瞰全景；7–16s 镜头极缓慢横移，她抬手依次指过几个方向；16–19s 停住",
      "Eight districts, one canal holding them together. Six hundred metres across. You could walk the whole thing in twenty-two minutes — if you never stopped. I have stopped about forty times.",
      "八个城区。一条运河把它们串起来。贸易区、旧城区、法师区、矮人区、教堂广场、公园区——加上我脚下这座要塞和我进来时那条谷地。横跨六百米。要是一次不停，二十二分钟能走完。我大概停了四十次。",
      "午后暖白偏黄日光，影子拉长；蓝色屋顶连成一片",
      ["district.*"], note="唯一能把八区一次讲完的位置；笑点"),

    S("S23", "午后", 17, "bg4", "中→特写", "手持近景", (0.38, 0.9),
      "矮人区露天锻造点：炉膛里烧着通红的炭火，一位矮人铁匠抡锤砸在铁砧上的红热坯料上，火星迸起",
      "铁匠在画面右侧正面朝砧；她站在画面左侧稍后，被火星吓得往后半步",
      "0–7s 建立中景，锤落；7–12s 特写火星迸起——**加速下坠、落地即灭，不滞空不慢放**；12–17s 切回她后退半步的反应",
      "The whole district smells like this. Hot metal and coal smoke, all day, every day. There are more dwarves living in this one corner of Stormwind than — okay that was close.",
      "整个城区都是这个味儿。热铁和煤烟，一整天，天天如此。住在暴风城这一角的矮人比——好吧那个有点近。",
      "**本镜是全片唯一允许暖橙炉火的场景之一**：炉火的暖橙光是主光，灰白烟霭悬在街面上方把天光滤成暖褐",
      ["landmark.022", "landmark.023", "person.023"],
      note="火星必须加速下坠（rule 16 ①）；笑点"),

    S("S24", "午后", 15, "bg4", "中景", "平机位正对门洞", (0.38, 0.38),
      "她走到一处矮人式门洞前，门楣明显低，她必须低头才进得去",
      "她正面朝门洞、镜头在她侧后方；门洞的上沿在她眉毛的高度",
      "0–7s 她走近、抬头看门楣；7–12s 低头钻进去、又退出来；12–15s 转向镜头",
      "Ceilings here are about two metres eighty. Doorways, two. That is not decoration — that's the single most reliable way to know which district you're standing in, without looking at anything else.",
      "这儿的层高大概两米八。门洞两米。这不是装饰——这是不看别的东西、光凭一点就能判断自己站在哪个区的最可靠办法。",
      "午后暖白日光在街上，门洞内是暗的；她在明暗交界处",
      ["district.*"], kind="正常台词", note="矮人区识别特征；笑点"),

    S("S25", "午后", 22, "bg5", "远→中", "低机位仰拍", (0.09, 0.38),
      "矿道地铁隧道口：一枚直径数倍于人高的巨型铸铁齿轮竖立套在洞口外圈缓慢转动，齿轮正中是通向地下的拱形洞口",
      "她自画面右下进入、朝洞口走；镜头在地面低位仰拍，齿轮几乎填满画面上半",
      "0–10s 齿轮缓慢转动的仰拍建立，齿牙从画外转入；10–18s 她走进画面、身形被齿轮衬得很小；18–22s 她走进洞口那团黑里",
      "The second entrance to this city isn't a gate. It's this. Straight down, under the sea, all the way to Ironforge.",
      "这座城的第二个入口不是城门。是这个。一直往下，从海底下穿过去，直通铁炉堡。",
      "午后暖白日光只到洞口为止，洞内是纯黑；**齿轮的金属面反出冷光，与街上的暖调形成对比**",
      ["landmark.024", "tram.016", "tram.017"], hero=True),

    S("S26", "午后", 15, "bg5", "全景", "站台平机位", (0.09, 0.38),
      "站台上矮人、人类、侏儒混杂站着等车，没有闸机、没有售票口、没有卫兵",
      "她站在站台中段偏右；其他候车的人零散分布在站台上",
      "0–7s 站台全景建立；7–12s 她左右看了看、找不到任何可以买票的地方；12–15s 她耸了耸肩站定",
      "No gates. No ticket office. No guards. Nobody checks anything, because it's free. This is a public transit line connecting two capital cities, and it has never charged anyone a copper.",
      "没有闸机。没有售票处。没有卫兵。没人查任何东西，因为它是免费的。这是一条连接两座首都的公共交通线，从来没收过任何人一个铜板。",
      "**全封闭地下，无天光、无天空**；光只来自隧道自身的灯具，光斑之间留有暗段",
      ["tram.003", "tram.030"], note="**反向声明无日光无天空**"),

    S("S27", "午后", 15, "bg5", "近景", "低机位近景", (0.9, 0.9),
      "站台一角：地上摞着两只铁丝捕鼠笼，旁边一块粗木摊板上插着一排细铁扦穿的烤串，板下一只小炭盆",
      "她蹲在摊板前、侧身朝画面右；捕鼠笼在她脚边",
      "0–7s 捕鼠笼与摊板的近景；7–12s 她拿起一根串看了看；12–15s 放下，站起来",
      "There's a rat problem down here. There has been for nineteen years. The man who catches them works the Ironforge end — and his brother sells them, on a stick, at this end.",
      "下面有鼠患。已经十九年了。抓老鼠的那位在铁炉堡那头干活——他弟弟在这头，把老鼠串成串卖。",
      "同 S26：全封闭地下，光只来自隧道灯具；炭盆里的炭是暗红的，不明火",
      ["event.007", "tram.041", "tram.043", "tram.044"]),

    S("S28", "午后", 17, "bg5", "紧→中", "贴轨面低机位", (0.38, 0.38),
      "矿车进站：三节铆接钢板车厢自画面上方掠过，轮轨之间迸出火星，随后停稳",
      "镜头贴着轨面、几乎与轨同高；她在站台上，进站时被车厢挡住又露出来",
      "0–7s 远处隧道里的灯光由远及近；7–14s 三节车厢自上方掠过、火星迸溅；14–17s 停稳，她上车",
      "Three cars. No engine, no driver, no smoke. It just goes.",
      "三节车厢。没有车头，没有司机，没有烟。它就是会走。",
      "同上；车厢金属面反出隧道灯具的一串移动光点",
      ["tram.023", "tram.024"],
      note="⚠️ 矿车的动力与有无司机在设定中空白，口播已用「它就是会走」回避断言"),

    S("S29", "午后", 19, "bg6", "中景", "车内侧向", (0.09, 0.38),
      "车内视角向侧前方：隧道壁在画面两侧被拉成速度线，灯具一盏盏掠过形成明暗节拍，纵深收束成一点",
      "她坐在车厢靠外侧、侧身朝画面右看出去；镜头在她斜后方，同时带到她和窗外",
      "0–9s 隧道壁的速度线与灯具节拍建立；9–19s 节拍逐渐变慢，前方的暗变得更深",
      "Sixty seconds, end to end. Which is the single strangest thing about it — this tunnel runs under an ocean, and it takes about as long as boiling an egg.",
      "全程六十秒。这是它最奇怪的一点——这条隧道从一片海底下穿过去，花的时间和煮个鸡蛋差不多。",
      "全封闭无天光；光只有隧道灯具，明暗节拍是画面的主要节奏",
      ["tram.001", "tram.025", "tram.027"]),

    S("S30", "午后", 24, "bg6", "中→远", "车内侧向后拉", (0.09, 0.09),
      "入水一刻：岩壁两侧忽然退开，通道外侧从石头换成深墨绿的水，沉船残骸与半埋在淤泥里的木箱缓缓向后掠去，光一下变冷",
      "她仍坐在原位、转头朝外；镜头由她的中景缓缓后拉，让水体占据画面大部",
      "0–8s 岩壁；8–14s **岩壁退开的一瞬**，画面外侧换成水；14–24s 水下的沉船残骸、带黄铜包角的木箱、半开的巨蚌壳依次掠过",
      "Oh — oh that's the bit. That's the bit everybody remembers.",
      "哦——就是这一段。这就是所有人都记得的那一段。",
      "**光在入水一刻由暖转冷**：水色深墨绿转青黑，无天光、无阳光光柱、无波浪；光只来自隧道内部，越往水体深处越暗",
      ["tram.031", "tram.033"], hero=True,
      note="全片的决定性瞬间之一；⚠️「玻璃穹顶」不可写死，只写「隔着通道边界看见水下景物」"),

    S("S31", "午后", 17, "bg6", "远景", "车内长焦透水", (0.38, 0.09),
      "远处水里一道长颈剪影缓慢横穿，始终不清晰、不靠近、不张口；它游出画外，几拍之后又从同一个方向再来一次",
      "她整个人贴到通道边缘朝外看；镜头长焦越过她的肩透过水体拍那道剪影",
      "0–7s 剪影缓慢横穿、游出画外；7–12s 她转头追着看、没了；12–17s 剪影又从同一个方向再来一次，她笑出声",
      "There she is. Nessy. She does a lap. If you look away at the wrong moment you'll swear the people who told you about her made her up — and then she comes round again.",
      "她来了。Nessy。她会绕一圈。要是你在不该走神的时候走了神，你会赌咒说跟你讲她的人是编的——然后她又绕回来了。",
      "同 S30：水体无天光，剪影的轮廓被水雾软化，自始至终看不清全貌",
      ["tram.034", "tram.035"], note="彩蛋；笑点"),

    S("S32", "傍晚", 19, "bg7", "极远→远", "地面大仰角", (0.38, 0.09),
      "光明大教堂正面大仰角：主体两侧伸出多组侧翼，屋脊之上林立着数量众多的细长尖塔，高低错落、越靠中心越高",
      "她站在广场石阶下、背对镜头仰头看；镜头从她身后越过她的头顶仰向教堂",
      "0–9s 大仰角建立，尖塔森林顶到画框上缘；9–16s 镜头缓慢升起；16–19s 她走上台阶",
      "It's not one spire. It's a forest of them. And the whole thing looks like it shouldn't be able to stand up.",
      "它不是一根尖塔。是一片尖塔的森林。而且整个看上去像是根本立不住。",
      "傍晚橙金低光从侧后方来，尖塔在天光里成剪影；**本镜画面里没有任何炉火，也没有任何暖橙色光源**",
      ["landmark.016", "landmark.017"], note="反向声明无炉火"),

    S("S33", "傍晚", 26, "bg7", "全→中", "室内广角", (0.38, 0.38),
      "教堂内厅：浅暖白石砌墙面嵌着饱和的钴蓝色石材条带与几何镶嵌，空间高敞，光自高窗斜落成柱；钟室里一口巨大的青铜钟悬在粗木梁下",
      "她沿中殿走向深处、镜头在她身后；光柱一道道从她身上扫过",
      "0–10s 内厅全景建立，光柱斜切；10–18s 跟她走过几道光柱；18–26s 仰拍钟室里的青铜钟，钟体表面是矮人风格的錾刻纹样与铆接感边饰",
      "Blue and white, even in here. And that bell — that bell wasn't made in this city. It was cast in the Great Forge at Ironforge and carried here. The dwarves made the loudest thing in the human capital.",
      "蓝和白，连这儿也是。还有那口钟——那口钟不是这座城造的。它是在铁炉堡的大熔炉里铸的，然后运过来。矮人造了人类首都里最响的东西。",
      "傍晚橙金低光自高窗斜落成柱，柱外的厅内是冷白与钴蓝的暗调；**本镜画面里没有任何炉火，也没有任何暖橙色光源**",
      ["landmark.018", "landmark.019", "lore.054", "lore.055"], hero=True),

    S("S34", "傍晚", 15, "bg7", "中景", "广场平机位", (0.09, 0.38),
      "广场上立着一座朴素的教士纪念碑——三级石台阶上一块竖立的素面石碑，碑面全空白、没有任何文字；石阶下三四个孩子挤在一级台阶上分一块面包",
      "她站在碑前一侧、侧身朝碑；孩子们在画面右下的石阶上",
      "0–7s 素面石碑的中景；7–12s 镜头下摇带到石阶上的孩子；12–15s 她在石阶边蹲下来看了一会儿",
      "The monument on this square is Alonsus Faol. A priest. Not the paladin with the hammer — he comes much later, and he replaces this. Right now, it's the quiet one.",
      "广场上这座纪念碑纪念的是阿隆索斯·法奥。一位教士。不是那位拿战锤的圣骑士——他要晚得多才来，而且是他换掉了这一座。现在站在这儿的，是安静的那位。",
      "傍晚橙金低光；碑体在逆光里偏冷；**本镜画面里没有任何炉火，也没有任何暖橙色光源**",
      ["myth.005", "job.016"],
      note="最隐蔽的版本坑；⚠️ 碑体形制无来源，按 best effort 设计成朴素立碑"),

    S("S35", "日落", 15, "bg8", "远→中", "林间平机位前推", (0.09, 0.38),
      "她走进花园区：石城里唯一的一块绿地，高大乔木的树冠在头顶合拢，日落的光从叶隙里穿下来",
      "她沿林间小径向里走、镜头在她身后前推；树影在她身上移动",
      "0–7s 从石板街进入草地，脚感与声音都变了；7–15s 穿过树影走向深处",
      "Stone, stone, stone — and then this. One block of the city they just left as trees.",
      "石头、石头、石头——然后是这儿。整座城里唯一一块他们直接留成树林的地方。",
      "日落强逆光从树后来，叶隙筛下光斑；地面是厚草与零星小花",
      ["landmark.035", "travel.004"]),

    S("S36", "日落", 28, "bg8", "中景环绕", "环绕轨道", (0.09, 0.38),
      "月亮井：一圈环形石台围出一池静水，台沿雕着藤蔓与叶形连续纹样，环外立着六根叶形柱头的细长石柱；水面自身发出乳白偏冷蓝的微光。镜头绕井一周",
      "她站在井的对侧、隔着井面朝镜头；镜头沿井外圈缓慢环绕一周，她始终在画面另一侧",
      "0–12s 环绕开始，逆光穿过叶隙；12–22s 绕到侧面，水面的冷光与天上的暖光在她脸上对撞；22–28s 绕回起点，她低头看水",
      "This is a moonwell. Night elf. There is exactly one in the whole of the Eastern Kingdoms, and it's sitting in the corner of a human city — because the night elves were given this block, and they planted it. It is, I think, the single most beautiful thing in Stormwind.",
      "这是月亮井。暗夜精灵的。整个东部王国就这一口，而它坐落在一座人类城市的角落里——因为这一块地给了暗夜精灵，他们把它种成了这样。我觉得，这是暴风城里最好看的一样东西。",
      "**本镜是全片唯一允许「自发光乳白冷蓝」的场景**：日落强逆光在树冠上缘，池水自身的乳白冷蓝微光是画面下半唯一的光源，两种光在她脸上一冷一暖对撞；光要柔、要弱，只照亮池沿一圈",
      ["landmark.036", "lore.043", "lore.044", "lore.045"], hero=True,
      note="**本片最好的一张画**"),

    S("S37", "入夜", 19, "bg9", "远→中", "街面前推", (0.09, 0.38),
      "法师区入夜：地面是厚草地带零星小花，屋顶是紫色，街灯与奥术灯柱先后亮起；巫师圣殿的塔身外壁盘着一道向上的石径绕塔而上",
      "她沿石板小径穿过草地走向塔底、镜头在她身后前推；塔在画面深处",
      "0–9s 草地与紫顶建立，灯一盏盏亮；9–19s 推近到塔底，仰头看那道绕塔而上的石径",
      "No elevator. No stairs inside that you can use. If you want to get to the top of the highest building in Stormwind, you walk around the outside of it.",
      "没有电梯。里面也没有你能走的楼梯。你想上暴风城最高那栋楼的顶，就得绕着它的外墙走上去。",
      "**本镜是全片唯一允许紫色奥术灯光的场景**：入夜深蓝天空，街灯的暖黄点与奥术灯柱的紫光并存，塔身在两种光里",
      ["landmark.012", "landmark.013"],
      note="**塔里绝不能画成传送门大厅**（8.1.5 才有）"),

    S("S38", "入夜", 15, "bg9", "近景", "室内近景", (0.9, 0.9),
      "塔底门内，一名法师学徒反复练同一个手势：双掌相对、掌间凝出一点光又散掉，再来一次",
      "学徒在画面中央侧身；她在画面边缘靠门框看着",
      "0–7s 学徒双掌相对、光点凝出又散；7–12s 再来一次、又散；12–15s 她忍住没笑、转身走开",
      "He's been doing that since I walked past the first time. Still not working.",
      "从我第一次路过起他就在练这个。还是没成。",
      "同 S37：入夜，塔内是暖黄烛光，门外是紫色奥术光；学徒掌间的光点**弱、不外放、不照亮周围**",
      ["job.009"], note="笑点"),

    S("S39", "入夜", 15, "bg9", "中→紧", "室内低照度", (0.38, 0.9),
      "已宰的羔羊：一层空荡阴冷，只有酒保一个人；地板上一处向下的开口通往地下，她只在口子上方看了一眼就退回来",
      "她站在下行口一步之外、侧身朝口；酒保在画面深处的吧台后",
      "0–7s 空荡的一层，酒保抬头看了她一眼；7–12s 她走到下行口边往下看；12–15s 她退开、摇头、转身出门",
      "There's a room under this pub. Officially. In the middle of the capital city. I'm going to look at it from up here and then leave, like a sensible person.",
      "这家酒馆底下有个房间。正儿八经登记在册的。就在首都正中间。我打算从这儿看一眼就走，像个明白人一样。",
      "入夜；室内低照度，光只有吧台一盏烛与下行口透上来的一点冷光；**本镜画面里没有紫色光源**",
      ["house.010", "lore.046"],
      note="平台合规：不拍血祭、不拍邪教视觉、不下去"),

    S("S40", "夜", 21, "bg11", "远景", "水面低机位", (0.09, 0.09),
      "夜里的运河：水面低机位，两座从水里立起来的石堡一前一后成纵深，两座顶上都有钟楼；监狱门口的石阶上立着一块齐腰高的集合石",
      "她在近岸的石阶上、背对镜头面朝水；两座石堡在画面深处",
      "0–9s 水面低机位建立纵深；9–16s 长焦带到两座钟楼；16–21s 镜头下摇到岸边的集合石",
      "Two fortresses, standing in the water, in the middle of the city. One of them is a prison — and right now the prisoners are running it. The guards were thrown out. Nobody on this bank seems especially bothered.",
      "两座从水里立起来的堡垒，就在城正中间。其中一座是监狱——而此刻里面是囚犯说了算。守卫被赶出来了。这岸上好像没什么人特别在意。",
      "夜；光源只有岸边街灯的暖黄点与窗内透出的光，水面反出一串抖动的光斑；**本镜画面里没有任何炉火**",
      ["lore.035", "lore.037", "travel.013"]),

    S("S41", "夜", 19, "bg11", "中→仰", "平机位后转仰拍", (0.38, 0.38),
      "金库那扇落闸栅门正面：栅栏后是纯黑，门从没开过。一名提油灯的卫兵巡夜走过她身后。随后她抬头看天",
      "她站在栅门前一臂远；卫兵自画面右侧走入、经过她身后、走出画面左侧；随后镜头随她仰起",
      "0–7s 栅门正面定镜，栅后纯黑；7–12s 卫兵提灯走过，灯光在甲面上滑过，他侧头说了一句；12–19s 她抬头，镜头仰向夜空",
      "That's the second one. Two doors in this city that have never opened, and the city just built itself around both of them. And look up — the sky is completely empty. No mounts, no dragons, nothing. Just dark.",
      "这是第二道。这座城里有两道从没开过的门，而这座城就绕着它们俩长起来了。抬头看——天空完全是空的。没有坐骑，没有龙，什么都没有。只有黑。",
      "夜；卫兵油灯的暖黄光是移动光源，在板甲上滑过；天空是深蓝近黑、只有星，**空中没有任何飞行物**",
      ["lore.040", "travel.012", "myth.010"],
      note="线③下半，与 S17 收成一对；档 2 互动：卫兵说逐字原文"),

    S("S42", "夜", 21, "bg9", "中景", "室内平机位正对", (0.09, 0.38),
      "蓝色隐士的桌边：她把采访本摊开，就着烛光把一天的账逐笔念出来",
      "她坐在桌边正面朝镜头，采访本摊在桌上；背景是餐馆的暖光与人影",
      "0–7s 她坐下、摊开本子；7–18s 逐笔念账，手指在纸上点过；18–21s 她合上本子，靠回椅背",
      "Bread, twenty-five copper. Ribs, one silver. This meal, two silver. The robe, thirty-five copper. The tram — free. The bed tonight — also free. And the one thing I actually paid a premium for? Sending a letter. Thirty copper a slot. In a city where sleeping is free, the post office is the expensive part.",
      "面包，二十五铜。肋排，一银。这顿饭，二银。袍子，三十五铜。地铁——免费。今晚的床——也免费。而我真正多花钱的那一项？寄一封信。一格三十铜。在一个睡觉不要钱的城里，邮局才是贵的那部分。",
      "夜；室内暖光，烛光在她脸上，背景的人影虚化；**本镜画面里没有紫色光源，也没有任何炉火**",
      ["price.*", "house.005", "travel.007"], kind="正常台词", note="爽点①·夜账"),

    S("S43", "夜", 22, "bg12", "中→近", "室内低照度", (0.09, 0.9),
      "回到镀金玫瑰，她把布包放在床边，吹灭桌上的蜡烛",
      "她坐在床沿、侧身朝画面右；蜡烛在她面前的小桌上",
      "0–10s 她进屋、把布包放下、坐到床沿；10–18s 她看了一眼桌上的炉石；18–22s 俯身吹灭蜡烛，画面只剩壁炉的余光",
      "Same room. Same innkeeper. Same stone on the table. Goodnight, Stormwind.",
      "同一间屋。同一个老板。桌上同一块石头。晚安，暴风城。",
      "夜；光源只有桌上一支蜡烛与远处壁炉的余光；吹灭后画面只剩壁炉的暗红余光",
      ["house.001", "lore.001"], hero=True, note="镜尾吹灯"),

    S("S44", "清晨", 30, "bg12", "中→极远", "室内转航拍拉远", (0.38, 0.09),
      "次晨：她在旅店门口对镜给这一晚打分，说完签名收尾两句；随后镜头自屋脊起飞，边退边升回到整座城",
      "她站在旅店门口正面朝镜头；说完最后一句后她转身走进街里，镜头升起",
      "0–6s 打分；6–14s 反差收尾；14–20s 置顶评论问题；20–24s 签名收尾两句；24–30s 镜头自屋脊起飞拉远，全城入画",
      "The bed: free, quiet, nine out of ten. One last thing — everyone thinks this was the Alliance capital. It wasn't. Back then people hung around Ironforge, where the auction house was. They called it Lagforge. Tell me in the comments: which locked door would you open? I changed nothing. I was just there. History doesn't do refunds — see you at the next stop.",
      "床：免费、安静，我比老板醒得还早。九分。最后一件事——所有人都以为这儿是联盟的首都。不是。那会儿大家其实都泡在铁炉堡，因为拍卖行在那儿。他们管它叫「卡炉堡」。暴风城要到后来才真正热闹起来。评论里告诉我：这座城里那些空房间，你会搬进哪一间？我什么都没改，我只是在场。历史不退款——下一站见。",
      "清晨暖金低角度侧逆光；拉远时第一道光落在尖塔与城墙上",
      ["lore.077", "lore.078", "lore.079"], kind="正常台词", hero=True,
      note="I-4 签名收尾逐字不变；反差收尾＋置顶评论问题"),
]


def read_lock(path: Path, head: str) -> str:
    """从卡里抽出 `head` 小节后的唯一裸围栏，作为锁定串。"""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^%s[^\n]*\n(.*?)(?=^#{1,3} |\Z)" % re.escape(head), text, flags=re.S | re.M)
    if not m:
        return ""
    got = re.findall(r"^```\n(.*?)\n```", m.group(1), flags=re.S | re.M)
    return got[0].strip() if len(got) == 1 else ""


def traveller() -> dict:
    path = SERIES_CHARS / "c4_艾拉" / "c4_艾拉.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    y = re.search(r"^```yaml\ntraveller:\n(.*?)\n```", text, flags=re.S | re.M)
    tr = dict(re.findall(r"^  (\w+): (.*)$", y.group(1), flags=re.M)) if y else {}
    tr["modern"] = read_lock(path, "### shot 角色行锁定串 · 现代装态")
    tr["local"] = read_lock(path, "### shot 角色行锁定串 · sk2 暴风城平民装态")
    tr["voice"] = read_lock(path, "### 声音锁定串")
    return tr


def scene_lock(bg: str) -> str:
    """场景卡的锁定描述符。卡用「**一句话锁定**：`...`」承载，兜底读裸围栏。"""
    base = A / "scenes" / "stormwind"
    hits = sorted(base.glob(f"{bg}_*/{bg}_*.md")) if base.exists() else []
    if not hits:
        return ""
    text = hits[0].read_text(encoding="utf-8")
    m = re.search(r"\*\*一句话锁定\*\*[：:]\s*`([^`]+)`", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"\|\s*\*\*一句话锁定\*\*\s*\|\s*([^|]+?)\s*\|", text)
    if m:
        return m.group(1).strip().strip("`")
    return read_lock(hits[0], "## 锁定描述符")


def negatives(sh: dict) -> str:
    neg = [NEG_BASE]
    if sh["bg"] not in FIRE_BG:
        neg.append(NEG_FIRE)
    if sh["bg"] not in GLOW_BG:
        neg.append(NEG_GLOW)
    if sh["bg"] not in PURPLE_BG:
        neg.append(NEG_PURPLE)
    if sh["bg"] in DARK_BG:
        neg.append("日光, 天空, 云, 太阳, 阳光光柱, 天光")
    return ", ".join(neg)


def counter_declare(sh: dict) -> str:
    """色温三角的反向声明（ai_video.md 16.9）。"""
    outs = []
    if sh["bg"] not in FIRE_BG:
        outs.append("本镜画面里没有任何炉火，也没有任何暖橙色光源")
    if sh["bg"] not in GLOW_BG:
        outs.append("画面里没有自发光的水面或魔法光源")
    if sh["bg"] not in PURPLE_BG:
        outs.append("画面里没有紫色光源")
    if sh["bg"] in DARK_BG:
        outs.append("全封闭地下，画面里没有任何日光、没有天空")
    return "；".join(outs)


def costume(sh: dict, tr: dict) -> str:
    n = int(sh["id"][1:])
    if n < CHANGE_SHOT:
        return tr.get("modern", "") or "（现代装锁定串 PENDING）"
    if n == CHANGE_SHOT:
        m, l = tr.get("modern", ""), tr.get("local", "")
        return f"{m}　→（镜内换装）→　{l}"
    return tr.get("local", "") or "（平民装锁定串 PENDING）"


# ── 参考层 ────────────────────────────────────────────────────────────────────
# sk1 已确立的参考行标准：previz 在第一位，其次场景主体、人物 entity、物件锚点、声样。
# 每个 handle 的路由键必须**与盘上文件名逐字前缀一致**（CLAUDE.md「全部 handle ⊆ 全部产物路径」），
# 由 gate_refs() 机检——本文件第一版把场景写成 `bg1_英雄谷锚点`（盘上没有这个名字）、
# 又把 bg0 整个排除在外，就是因为当时没有这道闸门。

BG_VIEW = {
    "bg0-1": "全城高空俯瞰", "bg0-2": "全城北向反打",
    "bg1-1": "英雄谷石桥锚点", "bg1-2": "城门外仰拍",
    "bg2-1": "贸易区喷泉广场锚点", "bg2-2": "镀金玫瑰门脸街景",
    "bg3-1": "旧城区窄巷锚点", "bg3-2": "猪和哨声门脸", "bg3-3": "永远打不开的副本门",
    "bg4-1": "矮人区露天锻造广场锚点", "bg4-2": "金酒桶与街心水井",
    "bg5-1": "齿轮洞口锚点", "bg5-2": "站台与三节车厢",
    "bg6-1": "入水一刻锚点", "bg6-2": "长颈巨兽掠过与水底潜水侏儒",
    "bg7-1": "教堂广场与法奥纪念碑锚点", "bg7-2": "大教堂内厅钴蓝光柱",
    "bg8-1": "月亮井锚点", "bg8-2": "石街入园界线",
    "bg9-1": "法师区锚点", "bg9-2": "塔脚仰角盘旋石阶",
    "bg10-1": "王座厅锚点", "bg10-2": "穹顶与光柱广角",
    "bg11-1": "运河上午锚点", "bg11-2": "双钟石堡夜",
    "bg12-1": "堂屋上午锚点", "bg12-2": "壁炉角夜",
}

PROP_NAME = {
    "p1": "街灯", "p2": "悬挂店招", "p3": "木花槽", "p4": "石砌圆井",
    "p5": "木桶与板条箱堆", "p6": "苹果树", "p7": "弧形石凳", "p8": "矮人锻炉与铁砧",
    "p9": "矿道地铁矿车", "p10": "地铁隧道口巨型齿轮", "p11": "捕鼠笼与鼠肉串摊",
    "p12": "木环烛台吊灯", "p13": "长木桌与高背椅", "p14": "酒器组",
    "p15": "钱袋与金银铜币", "p16": "炉石", "p17": "麻布采访本与短话筒",
    "p18": "面包与牛奶", "p19": "月亮井", "p20": "集合石", "p21": "拍卖行长台", "p22": "狮鹫",
}

CHAR_NAME = {
    "c21": "安杜因·乌瑞恩", "c22": "大领主伯瓦尔", "c23": "普瑞斯托女士",
    "c24": "旅店老板奥里森", "c25": "乔纳森将军", "c26": "狮鹫管理员杜加尔",
    "c27": "大主教本尼迪塔斯", "c31": "暴风城卫兵", "c32": "平民男性",
    "c33": "平民女性", "c34": "矮人铁匠", "c35": "侏儒技师",
    "c36": "圣光牧师", "c37": "法师", "c38": "暗夜精灵", "c39": "街头孩子", "c42": "酒馆老板 Reese Langston",
}


def R(ella=True, bgs=(), props=(), npcs=()):
    return dict(ella=ella, bgs=list(bgs), props=list(props), npcs=list(npcs))


# ella=False 只有三镜：S01/S02 走位写死「画面里没有人」，S15 写死「她不入画」。
# 第一版对全部 44 镜无条件挂了艾拉的人物 entity，连这三镜也挂——那是把一张脸
# 塞进一个根本没有人的画面里，模型多半会凭空加一个人进去。
SHOT_REFS = {
    "S01": R(ella=False, bgs=("bg0-1",)),
    "S02": R(ella=False, bgs=("bg0-1", "bg0-2")),
    "S03": R(bgs=("bg1-1",), props=("p17",)),
    "S04": R(bgs=("bg1-1",), props=("p17",)),
    "S05": R(bgs=("bg1-1",)),
    "S06": R(bgs=("bg1-1",)),
    "S07": R(bgs=("bg1-1",), npcs=("c25",)),
    "S08": R(bgs=("bg2-1",), props=("p2",), npcs=("c32", "c33")),
    "S09": R(bgs=("bg2-1",), props=("p18", "p15"), npcs=("c32",)),
    "S10": R(bgs=("bg2-1",), props=("p15",), npcs=("c32",)),
    "S11": R(bgs=("bg12-1",), props=("p12",), npcs=("c24",)),
    "S12": R(bgs=("bg12-2",), props=("p16",)),
    "S13": R(bgs=("bg12-1",)),
    "S14": R(bgs=("bg11-1",), props=("p18",)),
    "S15": R(ella=False, bgs=("bg11-1",)),
    "S16": R(bgs=("bg3-1",), npcs=("c32",)),
    "S17": R(bgs=("bg3-3",)),
    "S18": R(bgs=("bg3-2",), props=("p13", "p14"), npcs=("c42",)),
    "S19": R(bgs=("bg3-2",), props=("p13",)),
    "S20": R(bgs=("bg10-1",), npcs=("c31",)),
    "S21": R(bgs=("bg10-1", "bg10-2"), npcs=("c21", "c22", "c23")),
    "S22": R(bgs=("bg10-1", "bg0-1")),
    "S23": R(bgs=("bg4-1",), props=("p8",), npcs=("c34",)),
    "S24": R(bgs=("bg4-1",)),
    "S25": R(bgs=("bg5-1",), props=("p10",)),
    "S26": R(bgs=("bg5-2",), props=("p9",), npcs=("c34", "c35", "c32")),
    "S27": R(bgs=("bg5-2",), props=("p11",)),
    "S28": R(bgs=("bg5-2",), props=("p9",)),
    "S29": R(bgs=("bg6-1",), props=("p9",)),
    "S30": R(bgs=("bg6-1",)),
    "S31": R(bgs=("bg6-2",)),
    "S32": R(bgs=("bg7-1",)),
    "S33": R(bgs=("bg7-2",)),
    "S34": R(bgs=("bg7-1",), npcs=("c39",)),
    "S35": R(bgs=("bg8-2",)),
    "S36": R(bgs=("bg8-1",), props=("p19",)),
    "S37": R(bgs=("bg9-1",), props=("p1",)),
    "S38": R(bgs=("bg9-2",), npcs=("c37",)),
    "S39": R(bgs=("bg9-1",), npcs=("c32",)),
    "S40": R(bgs=("bg11-2",), props=("p20",)),
    "S41": R(bgs=("bg11-2",), npcs=("c31",)),
    "S42": R(bgs=("bg9-1",), props=("p17", "p15")),
    "S43": R(bgs=("bg12-2",)),
    "S44": R(bgs=("bg12-1", "bg0-1")),
}


def costume_state(sid: str) -> str:
    n = int(sid[1:])
    if n < CHANGE_SHOT:
        return "现代装态"
    if n == CHANGE_SHOT:
        return "镜内换装：现代装态 → 暴风城平民装态"
    return "暴风城平民装态"


def ref_items(sh: dict, tr: dict) -> list[tuple[str, str]]:
    """返回 [(handle, 说明)]，顺序即 `参考:` 行顺序、也即上传清单顺序。"""
    r = SHOT_REFS[sh["id"]]
    nn = sh["id"][1:]
    items: list[tuple[str, str]] = [
        (f"shot{nn}_previz.mp4", "白模动画·运动与几何参考，不取长相"),
    ]
    for x in sh["extra_ref"]:
        items.append((x.replace("=>@", ""), ""))
    for b in r["bgs"]:
        items.append((b, f"场景主体·{BG_VIEW[b]}"))
    if r["ella"]:
        items.append(("c4_艾拉", f"Seedance 人物 entity·{costume_state(sh['id'])}"))
    for c in r["npcs"]:
        items.append((f"{c}-1", f"{CHAR_NAME[c]}·Seedance 人物 entity"))
    for p in r["props"]:
        items.append((f"{p}-1", f"{PROP_NAME[p]}锚点"))
    if sh["kind"] != "无台词":
        vid = tr.get("voice_id_en", "en-f-vlogger-ella-01")
        items.append(("艾拉声音", f"c4-2 声样·voice_id {vid}"))
    if sh["id"] in NPC_LINES:
        who, _line, vid = NPC_LINES[sh["id"]]
        items.append((f"{who} 声音", f"声样·voice_id {vid}"))
    return items


def ref_line(sh: dict, tr: dict) -> str:
    out = []
    for h, note in ref_items(sh, tr):
        out.append(f"`{h}({note})=>@`" if note else f"`{h}=>@`")
    return "，".join(out)


def build_prompt(sh: dict, tr: dict) -> str:
    lines = [sh["id"].lower().replace("s", "shot") + "_" + BG_NAME[sh["bg"]]]
    lines.append("参考: " + ref_line(sh, tr))
    lines.append("参考用法: previz 只取运镜路径、几何关系与动作时刻表，不取长相、不取材质、不取光线；"
                 "人物 entity 只定这张脸与锁定装束；场景主体与物件锚点只取形制与影像基调，"
                 "构图与机位以下面的文字为准。槽位一律留空，上传时手填。")
    lines.append("")
    if sh["kind"] != "无台词":
        lines.append(f"角色: {costume(sh, tr)}")
    lines.append(f"情节: {sh['plot']}")
    lines.append(f"场景: {BG_NAME[sh['bg']]}。{scene_lock(sh['bg']) or '（场景锁定串 PENDING）'}")
    lines.append(f"镜头: {sh['jbcam']}；景别 {sh['jb']}；16:9")
    lines.append(f"走位: {sh['block']}")
    lines.append(f"动作: {sh['act']}")
    if sh["kind"] != "无台词":
        lines.append(f"台词: 艾拉〔{sh['kind']}{'，画外不露口型' if sh['kind'] == '内心独白' else '，入画对镜说话'}〕{sh['vo_en']}")
        lines.append(f"声音: {tr.get('voice', '（声音锁定串 PENDING）')}")
    if sh["id"] in NPC_LINES:
        who, line, _vid = NPC_LINES[sh["id"]]
        lines.append(f"台词: {who}〔正常台词，逐字原文，一个字不得自编〕{line}")
    lines.append(f"光线: {sh['light']}。{counter_declare(sh)}")
    lines.append(f"节奏: {sh['d']} 秒一镜；{'节奏放慢、给画面留时间' if sh['hero'] else '节奏平稳'}")
    lines.append(f"渲染样式: {STYLE_BASE}")
    lines.append("比例: 16:9")
    lines.append(f"时长: {sh['d']} 秒")
    lines.append(f"负面词: {negatives(sh)}")
    return NL.join(lines)


def build_shot_md(sh: dict, tr: dict, prev: dict | None) -> str:
    p = build_prompt(sh, tr)
    out = []
    out.append("---")
    out.append(f"shot_id: {sh['id']}")
    out.append(f"bg: {sh['bg']}")
    out.append(f"tod: {sh['tod']}")
    out.append(f"duration: {sh['d']}")
    out.append(f"hero: {'true' if sh['hero'] else 'false'}")
    out.append(f"jb: \"{sh['jb']}\"")
    out.append(f"jbcam: \"{sh['jbcam']}\"")
    out.append(f"subj_frac: [{sh['sf'][0]}, {sh['sf'][1]}]")
    out.append("---")
    out.append("")
    out.append(f"# {sh['id']} · {BG_NAME[sh['bg']]}")
    out.append("")
    out.append("## Shot context")
    out.append("")
    out.append(f"- 景别档: {sh['jb']}（起幅人占画高 {sh['sf'][0]} → 落幅 {sh['sf'][1]}）")
    out.append(f"- 机位标签: {sh['jbcam']}")
    out.append(f"- 衔接: {sh['seam']}")
    out.append(f"- 时辰: {sh['tod']}　时长: {sh['d']} s")
    out.append(f"- 设定: {', '.join(sh['facts'])}")
    nn = sh["id"][1:]
    out.append(f"- previz: 白模动画 `5_6_分镜与prompt/shots/shot{nn}/shot{nn}_previz.mp4`"
               "；关键帧 `t` 须与 `动作:` 时间轴逐拍对齐（rule 4h ②）")
    if sh["note"]:
        out.append(f"- 备注: {sh['note']}")
    out.append("")
    out.append("### 参考上传清单")
    out.append("")
    for h, note in ref_items(sh, tr):
        out.append(f"- [ ] `{h}`" + (f" — {note}" if note else ""))
    out.append("")
    out.append("## 视频 prompt")
    out.append("")
    out.append(FENCE + "text")
    out.append(p)
    out.append(FENCE)
    out.append("")
    if sh["kind"] != "无台词":
        out.append("## 台词配音 prompt")
        out.append("")
        out.append(FENCE + "text")
        out.append(f"角色: 艾拉 / Ella Hart")
        out.append(f"音色: {tr.get('voice_id_en', 'en-f-vlogger-ella-01')}（锁定，全剧复用）")
        out.append(f"情绪: {'放慢、收住' if sh['hero'] else '轻快、好奇'}")
        out.append("语速: 英语 ≤ 2.8 词/秒")
        out.append(f"类型: {sh['kind']}")
        out.append(f"台词: {sh['vo_en']}")
        out.append(f"中文译配: {sh['vo_zh']}")
        out.append(f"时长目标: {sh['d']} 秒以内")
        out.append(FENCE)
        out.append("")
    if sh["id"] in NPC_LINES:
        who, line, vid = NPC_LINES[sh["id"]]
        out.append("## 台词配音 prompt · NPC（逐字原文）")
        out.append("")
        out.append(FENCE + "text")
        out.append(f"角色: {who}")
        out.append(f"音色: {vid}（锁定，全剧复用）")
        out.append("类型: 正常台词")
        out.append(f"台词: {line}")
        out.append("出处: divergence #113 台词表（作品内逐字原文，一个字不得自编）")
        out.append(FENCE)
        out.append("")
    return NL.join(out)



# 盘上产物索引。闸门 K-ref 用它把 `参考:` 行的每个路由键对回真实文件——
# CLAUDE.md：「`参考:` 行写与盘上逐字一致的完整路径；可机检：全部 handle ⊆ 全部产物路径。」
def on_disk_keys() -> set[str]:
    keys: set[str] = set()
    for pat, root in (("bg*/*.png", A / "scenes" / "stormwind"),
                      ("c*/*.png", A / "characters"),
                      ("p*/*.png", A / "props")):
        if root.exists():
            for f in root.glob(pat):
                keys.add(f.stem.split("_")[0])
    if SERIES_CHARS.exists():
        for d in SERIES_CHARS.glob("c*"):
            if d.is_dir():
                keys.add(d.name)                      # 人物 entity：只有卡，没有图
                for f in d.glob("*.png"):
                    keys.add(f.stem.split("_")[0])
    for f in (ROOT / "shots").glob("shot*/shot*_previz.mp4"):
        keys.add(f.name)
    return keys


def gate_refs(shots: list[dict], tr: dict) -> list[str]:
    """每镜的参考必须①非空②每个路由键在盘上真的有文件③人不入画的镜不许挂人物 entity。"""
    errs: list[str] = []
    disk = on_disk_keys()
    for s in shots:
        items = ref_items(s, tr)
        if not items:
            errs.append(f"{s['id']} `参考:` 行为空")
        if not any(h.endswith("_previz.mp4") for h, _ in items):
            errs.append(f"{s['id']} 没有挂 previz 白模动画")
        if not any(h.startswith("bg") for h, _ in items):
            errs.append(f"{s['id']} 没有挂任何场景主体参考")
        for h, _ in items:
            if h.endswith("声音") or h.endswith(" 声音") or "首帧" in h or "末帧" in h:
                continue
            if h not in disk:
                errs.append(f"{s['id']} 参考 `{h}` 在盘上找不到对应产物")
        no_person = "画面里没有人" in s["block"] or "她不入画" in s["block"]
        has_ella = any(h == "c4_艾拉" for h, _ in items)
        if no_person and has_ella:
            errs.append(f"{s['id']} 走位写明画面里没有人，却挂了艾拉的人物 entity")
        if not no_person and not has_ella:
            errs.append(f"{s['id']} 有人入画，却没挂艾拉的人物 entity")
    return errs

def gate(shots: list[dict], tr: dict, allow_pending: bool) -> list[str]:
    errs: list[str] = []
    total = sum(s["d"] for s in shots)
    for s in shots:
        if not (MIN_D <= s["d"] <= MAX_D):
            errs.append(f"{s['id']} 时长 {s['d']} 不在 {MIN_D}–{MAX_D}")
        # rule 4h ②：`动作:` 时间轴与 previz 关键帧逐拍对齐。时间轴的末点超过 d
        # ＝先天对不齐——previz 根本渲不到那一拍，这类错不该靠人眼在成片里发现。
        ts = [int(x) for x in re.findall(r"(\d+)\s*s", s["act"])]
        if ts and max(ts) > s["d"]:
            errs.append(f"{s['id']} `动作:` 时间轴到 {max(ts)}s，超过时长 {s['d']}s")
        if s["kind"] != "无台词":
            words = len(s["vo_en"].split())
            if words / s["d"] > MAX_WPS:
                errs.append(f"{s['id']} 英文语速 {words}/{s['d']} = {words/s['d']:.2f} > {MAX_WPS} 词/秒")
        p = build_prompt(s, tr)
        if len(p) > MAX_PROMPT:
            errs.append(f"{s['id']} prompt {len(p)} 字 > {MAX_PROMPT}")
        if re.search(r"#[0-9A-Fa-f]{6}", p):
            errs.append(f"{s['id']} prompt 含 hex 色值")
        if "PENDING" in p and not allow_pending:
            errs.append(f"{s['id']} 有未解析的锁定串（PENDING）——先跑完阶段 2 资产卡，或加 --allow-pending")
    if not (TOTAL_LO <= total <= TOTAL_HI):
        errs.append(f"片长 {total} s 不在 {TOTAL_LO}–{TOTAL_HI}")
    # tod 单调不减
    last = -1
    for s in shots[:-1]:          # 末镜是次晨，允许回到「清晨」
        i = TOD_ORDER.index(s["tod"])
        if i < last:
            errs.append(f"{s['id']} 时辰倒走：{s['tod']}")
        last = max(last, i)
    # 景别档：相邻镜比值 + 机位标签
    for a, b in zip(shots, shots[1:]):
        if b["seam"].startswith("承接"):
            continue
        end_a, start_b = a["sf"][1], b["sf"][0]
        if end_a <= 0 or start_b <= 0:
            continue
        r = max(end_a, start_b) / min(end_a, start_b)
        if r < 2.0:
            errs.append(f"{a['id']}→{b['id']} 景别档比值 {r:.2f} < 2.0（{end_a} → {start_b}）")
        if a["jbcam"] == b["jbcam"]:
            errs.append(f"{a['id']}→{b['id']} 机位标签相同：{a['jbcam']}")
    errs += gate_refs(shots, tr)
    return errs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只跑闸门不写盘")
    ap.add_argument("--allow-pending", action="store_true", help="资产卡未齐时降级为 warning")
    args = ap.parse_args()

    tr = traveller()
    errs = gate(SHOTS, tr, args.allow_pending)
    total = sum(s["d"] for s in SHOTS)
    out = sys.stdout.buffer
    out.write(f"镜数 {len(SHOTS)} · 片长 {total} s ({total/60:.1f} min)\n".encode())
    if errs:
        out.write(f"闸门未过 {len(errs)} 条：\n".encode())
        for e in errs:
            out.write(("  ✗ " + e + "\n").encode())
        if not args.allow_pending:
            raise SystemExit(1)
    else:
        out.write("闸门全过\n".encode())
    if args.check:
        return

    (ROOT / "shots").mkdir(parents=True, exist_ok=True)
    (DRAMA / "4_剧本").mkdir(parents=True, exist_ok=True)
    allp = ["# sk2 · 全部分镜 prompt（由 tools/gen_shots_sk2.py 生成，勿手改）", ""]
    rows = ["| # | 时辰 | 时长 | 地点 | 景别档 | 机位 | 内容 |", "|---|---|---|---|---|---|---|"]
    dia_en, dia_zh, script = [], [], []
    prev = None
    for sh in SHOTS:
        d = ROOT / "shots" / sh["id"].lower().replace("s", "shot")
        d.mkdir(parents=True, exist_ok=True)
        (d / (d.name + ".md")).write_text(build_shot_md(sh, tr, prev), encoding="utf-8")
        allp += [f"## {sh['id']} · {BG_NAME[sh['bg']]}", "", FENCE + "text", build_prompt(sh, tr), FENCE, ""]
        rows.append(f"| {sh['id']} | {sh['tod']} | {sh['d']}s | {BG_NAME[sh['bg']]} | {sh['jb']} | {sh['jbcam']} | {sh['plot'][:40]}… |")
        if sh["kind"] != "无台词":
            dia_en.append(f"**{sh['id']}**〔{sh['kind']}〕{sh['vo_en']}")
            dia_zh.append(f"**{sh['id']}**〔{sh['kind']}〕{sh['vo_zh']}")
        if sh["id"] in NPC_LINES:
            who, line, _ = NPC_LINES[sh["id"]]
            dia_en.append(f"**{sh['id']}**〔{who}·逐字原文〕{line}")
            dia_zh.append(f"**{sh['id']}**〔{who}·逐字原文〕{line}")
        script += [f"### {sh['id']} · {BG_NAME[sh['bg']]}（{sh['tod']} / {sh['d']}s）", "",
                   f"{sh['plot']}", "",
                   (f"> 艾拉〔{sh['kind']}〕{sh['vo_zh']}" if sh["kind"] != "无台词" else "> （无台词）"), ""]
        prev = sh

    (ROOT / "all_shot_prompts.md").write_text(NL.join(allp), encoding="utf-8")
    (ROOT / "shotlist.md").write_text(
        NL.join([f"# sk2 · 镜表（{len(SHOTS)} 镜 / {total} s）", "",
                 "> 由 `tools/gen_shots_sk2.py` 生成，**勿手改**；改内容＝改生成器重跑。", ""] + rows),
        encoding="utf-8")
    (DRAMA / "4_剧本" / "dialogue.md").write_text(
        NL.join(["# sk2 · 台词（中英两条）", "", "## English（视频原声）", ""] + dia_en +
                ["", "## 中文（译配轨）", ""] + dia_zh), encoding="utf-8")
    (DRAMA / "4_剧本" / "script.md").write_text(
        NL.join(["# sk2 · 文学剧本", "",
                 "> 由 `tools/gen_shots_sk2.py` 生成，**勿手改**。", ""] + script), encoding="utf-8")
    out.write(f"写盘完成：{len(SHOTS)} 个 shot 目录 + shotlist + all_shot_prompts + script + dialogue\n".encode())


if __name__ == "__main__":
    main()
