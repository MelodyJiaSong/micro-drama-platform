# -*- coding: utf-8 -*-
"""一个 shot 的**镜头平面图（overhead）** —— 分层出片的第二层（ai_video.md rule 4j，2026-09-25 修订）。

    ① 场景层  scene blend + 场地平面图 floor plan（`tools/build_floorplan.py`）—— 静态的地方
    ② 本工具  每镜一张 overhead：镜头怎么走、每个人怎么走、建筑与物件在哪——**不管动作细节与形状**
    ③ shot blend + previz MP4：真实动作、走位细节、物件形状、镜头远近变化（从②的同一份数据读，不重填坐标）
    ④ Seedance：色彩、表情、特效、质感
每一层只解决它最擅长、最便宜的那件事；越往下改一次越贵，所以错误要在越上面的层拦住。

**previz MP4 只给复杂镜（2026-09-25 用户定调）**：每镜都必须有 overhead；简单镜不渲 previz，
直接把 Seedance 版 overhead（`{shot}_overhead_ref.png`）当运动与几何参考上传。要不要 previz 由本工具
按 `previz_triggers()` 的四条量化判据判（机位长距离移动 / 镜内多段硬切 / 多人同时走动 / 多对肢体接触），
`[meta] previz = true|false` 可推翻，但与判据相反时必须写 `previz_why`。

输入（唯一出处）：`{shot 目录}/planning/overhead.toml`
    [meta]      scene = "bg19"（挂在哪张场地平面图的坐标系上）· view = [x0, y0, x1, y1]（可选，米）· note ·
                walkable = ["b08"]（本镜机位允许站进的地块 id，只给类型泛用的地块用）·
                previz = true|false（可选，推翻自动判定）· previz_why（推翻时必填）
    [[camera]]  t · xy · h（离地米）· look（瞄准点）· lens（mm）· tag（机位标签，可选）·
                subject（这一刻景别量谁，人物卡键；缺省＝第一个 actor）· cut（true＝硬切到这里，不是运镜走过来）· note
    [[actor]]   key（人物卡目录名）· label · count（群体数，默认 1）· path = [[t, x, y], …]
                （路点可写 [t, x, y, fx, fy]：fx/fy ＝ 此刻面朝的点）· note
    [[object]]  label · xy · size · rot · key（物件卡目录名，可选）· note —— 场地图里没有、本镜才出现的东西
    [[beat]]    t0 · t1 · text —— 时间轴提要（与剧本【a–bs】对齐）
坐标一律用场地平面图的坐标系（米；x 向东、y 向南，与 floor plan 同一张网格）。

产物：`{shot 目录}/planning/{shot}_overhead.png`（给人审：带坐标、时间轴、提示）＋
      `{shot 目录}/planning/{shot}_overhead_ref.png`（给 Seedance：16:9、裁到本镜范围、无标题无侧栏无坐标，
      只有地块、人、机位、箭头与秒数——读图的是视频模型，多一行字就多一分被画进画面的风险）；
      `--all` 另写 `{ep 目录}/overheads.md` 索引（含每镜 previz 要 / 免及理由）。

构建闸门（blocker 不写图）：键名白名单 · 场景能解析 · 时刻落在镜长内且不倒退 ·
**入画人物与 shot md 的 `角色:` 行双向一致**（prompt 说谁在画面里，这张图就得给谁站位）。
提示（warning，印在图上）：机位落在有高度的体块里 · 起幅 / 落幅的机位距离与 `景别档` 按焦距反算的距离差太多。

用法：
    python tools/shot_overhead.py <shot 目录>
    python tools/shot_overhead.py --all <ep 目录>        # 整集，外加 overheads.md 索引
    python tools/shot_overhead.py --all <ep 目录> --check
"""
from __future__ import annotations

import functools
import argparse
import math
import os
import re
import sys
import tomllib
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import build_floorplan  # noqa: E402
from tools.previz import planschema  # noqa: E402
from tools.previz.planstyle import (  # noqa: E402
    ACCENT, INK, MUTED, PAPER, PANEL_BG, SOFT, font, halo, badge, north_arrow, scale_bar, title_block, footer,
)

KEYS = {
    "meta": {"scene", "view", "note", "walkable", "previz", "previz_why", "hostile", "calm", "proxy", "skip"},   # proxy：本镜人偶改色（szzl 057 E3）；skip：与上一镜之间跳过了时间（写理由，8f 站位 4）
    # aim_h：瞄点离地高（m），近景插入瞄手（≈1.0）/ 脚下（≈0.15）时写；缺省按 previz 的统一瞄高（follow-up 043）
    "camera": {"t", "xy", "h", "look", "lens", "tag", "subject", "cut", "note", "aim_h", "axis_ok", "jump_ok"},   # axis_ok / jump_ok：有意跨轴 / 同景别同角度的镜内切（写理由）
    # shield：这一镜手上持盾（"左" / "右"），shield_t = [t0, t1] 只在这段时间持盾（缺省整镜）——follow-up 046
    # enter / gone：这一刻才出场 / 这一刻起不在场（从鼠洞里钻出来、钻回去）——场外不参与任何距离机检，previz 里藏起来（049）
    # idle：打斗里真要等的时段 [[t0, t1, "理由"]]，理由要在 `动作:` 里逐字看得见（051 G11）
    "actor": {"key", "label", "count", "path", "note", "shield", "shield_t", "enter", "gone", "idle", "moved", "alert_t"},   # alert_t：人物第一次察觉这个敌人（听见 / 看见）的时刻，szzl 引擎反应时间闸门读   # moved：与上一镜之间在画外挪了位（写理由，8f 站位 4）
    "object": {"label", "xy", "size", "rot", "key", "note", "h"},       # h：离地高（m），只给 previz 用；缺省 1 m
    "beat": {"t0", "t1", "text"},
    # 护人格挡（follow-up 032）：who 在 [t0, t1] 里必须站在 protects 与 threat 之间、面朝 threat（盾面朝 threat）。
    # who / protects / threat 写 actor 的 key 或 label（同卡多只的怪用 label 区分）。
    "guard": {"t0", "t1", "who", "protects", "threat", "shield", "note"},
    # 反应窗（follow-up 032 第二轮）：who 在 t_cue 察觉、到 t_ready 做完 does 里的动作；时长按 REACT_S 累加，
    # 给的时间不够、或还没做完就被怪碰上，都是 blocker——「一抬头狼已经在一米外、还来得及捡锤」这类错在这里拦。
    "react": {"who", "t_cue", "t_ready", "does", "note"},
    # 命中（follow-up 042：shot05 亚伦的锤一下都没打到狼）：该打中的每一下写清谁、用什么、打谁、几秒、落在哪、结果。
    # 机检：那一刻 who 离 target 在 with 的够得着（REACH）之内、面朝 target；previz 再查锤头真的贴到目标身上（obj ＝ previz 里那件东西的名字）。
    # miss = true 是故意落空（够不着 / 被格开），只进 prompt、不查距离。
    # back = true：反身出手（向后踢、回肘），不查面朝
    # open：打在持盾的人身上、又来自盾那一侧正面时，写盾为什么没挡住（「盾正顶着另一只」）——follow-up 046
    # over：扔出去的光从这个己方的人肩上方飞过（平面图只有两维，挡在连线上的那个人由它豁免；prompt 里写明从谁肩上飞过）
    # stuck：兵器卡在目标身上的秒数（斧刃卡进木盾）——这段时间出手的人在拔，不算干站（049）
    # hurt：打在具名人物身上（不是盾 / 甲 / 兵器）疼多久、怎么疼 [秒数, "怎么疼"]——这段时间伤到的手 / 腿不照常用（051 G12）
    "hit": {"t", "who", "target", "with", "part", "result", "miss", "obj", "back", "open", "over", "stuck", "note", "hurt"},
    # 施法（follow-up 046：「需要时间就在后面施法」）：[t0, t1] 里 who 在念 / 起光；威胁进了 CAST_THREAT_M 以内，
    # 中间得有持盾的人挡着，或被 [[guard]] 护着；故意让他暴露的写 exposed = 理由
    "cast": {"t0", "t1", "who", "skill", "exposed", "note", "over"},   # over：飞行物从这几个人头上飞过（8f 站位 6）
    # 视线目标（follow-up 047：shot09 亚伦数的烛光在镜头身后，画里看不见、背景又是亮的山谷，看着像朝外）：
    # who 在 [t0, t1] 看 at（actor 的 key / label，或平面坐标 [x, y]）。机检：面朝对不对得上目标；
    # key = true（这一拍的意义就在那个东西上）整镜至少一个时刻它在画里；在画外时生成器把「在哪一侧画外」写进 `走位:`。
    "gaze": {"who", "t0", "t1", "at", "label", "key", "note"},
    # 会动的道具（049 G9：shot11 被拖进鼠洞的锤在平面图里是一块不动的方块，previz 里拉锯一拍都没有）：
    # 被拖 / 抢 / 捡 / 扔 / 拽走的东西写这里，path 路点 [t, x, y]；gone＝这一刻起不在场（拖进洞、被捡走拿在手上）；
    # 同一场景接连两镜同 key 的 prop 首尾位置要接得上，画外被人挪过写 moved = 理由。
    "prop": {"key", "label", "path", "size", "h", "gone", "moved", "note"},
}
GAZE_FACE_DEG = 45.0     # 看某样东西时，面朝与「人→目标」的夹角上限
GAZE_CAM_DEG = 60.0      # 面朝与「人→机位」夹角小于它：他看的东西多半在镜头身后——`动作:` 里写了看 / 盯 / 数就得登记 [[gaze]]
# 各种打法的够得着（米，人 / 怪中心之间）；光是扔出去的
REACH = {"锤": 2.0, "斧": 2.0, "剑": 1.9, "镐": 1.6, "棒": 1.8, "盾": 1.5, "拳": 1.1, "脚": 1.3, "咬": 1.3, "爪": 1.3, "撞": 1.2, "光": 15.0, "投": 15.0, "鞭": 3.0, "叉": 1.8}   # 投：扔出去的东西（盾 / 锤）
FRIEND_ARC = 55.0        # G19（用户 2026-10-02：亚伦对着杜克的盾砸）：自己人出手，另一个自己人不许落在「出手→目标」两侧这个角度、够得着的距离之内
HIT_FACE = 70.0          # 出手的人面朝偏离目标超过这个角度（°）＝ 打不到
SHIELD_ARC = (-110.0, 30.0)   # 左手盾护得住的来向（° 相对面朝，负＝左、正＝右）；右手盾取镜像（follow-up 046）
CAST_THREAT_M = 3.0      # 施法时威胁进了这个距离，中间就得有盾
GHOST_S = 1.0            # 跳切之前，新位置已在画里、本人却不在画里超过这么久（s）＝ 模型会先在新位置画一个他
ACTOR_COLORS = [(38, 110, 196), (40, 150, 80), (150, 70, 170), (200, 130, 20), (20, 150, 150),
                (120, 90, 60), (200, 60, 130), (90, 90, 90)]
OBJ_COL = (214, 120, 30)
# Seedance 版底色：比审阅版更淡、更中性，免得模型把底色当成地面颜色去取
GRASS_REF, ROCK_REF, WATER_REF, ROAD_REF = (236, 238, 228), (204, 200, 190), (170, 200, 214), (222, 212, 192)
# 本身就是「人能站进去」的地块：机位落在里面不算扎进体块（内景壳、巷道、藤垄行间、桥面、门洞…）。
# 类型泛用的地块（kind = asset 的营地之类）不在此列——由各镜 `[meta] walkable = ["b08"]` 显式放行。
WALKABLE = {"hall_shell", "chamber", "tunnel", "vineyard", "graveyard", "arch_bridge", "mine_portal",
            "plaza", "yard", "lawn", "tables"}
SENSOR_W = 36.0          # 全画幅；16:9 横向视角由它与焦距算
FRAC = {"远景": 0.12, "全景": 0.3, "中景": 0.6, "近景": 0.9, "特写": 1.3}
SUBJ_H = 1.72
MAP_MAX = (1500, 1250)
# ── previz 要不要：四条判据，任一条成立就要（名字只在这里定义，引擎与索引都从这里读）──
PREVIZ_CAM_TRAVEL_M = 12.0   # 机位连续水平移动：穿行 / 长跟拍——俯视图给得出路线，给不出沿途遮挡与纵深
PREVIZ_SEGMENTS = 4          # 镜内硬切段数：段一多，各段之间的站位连续一张图对不齐（三段定机位一张图还交代得清）
PREVIZ_MOVERS = 3            # 同一时刻在走的人数：谁往哪走、谁先到，散文 + 一张图排不对
PREVIZ_CONTACTS = 2          # 发生肢体接触的人对数（相距 < CONTACT_M 且有人在动）：打斗 / 推搡编排
CONTACT_M = 0.8
MOVE_MPS = 0.3
# 护人格挡的几何闸门：挡的人离威胁比被护的人近、落在「被护者→威胁」连线两侧 GUARD_ANGLE 度以内、面朝威胁偏差 ≤ GUARD_FACE 度
# ── 物理与反应（follow-up 032 第二轮）──
SPEED_MAX = {"c": 8.0, "m": 14.0}      # 路点之间的平均速度上限 m/s：人冲刺 ≈ 8，狼冲刺 ≈ 14；超过就是瞬移
LUNGE_M = 2.0                          # 怪进了这个距离就是一扑就到
REACH_M = 1.7                          # [meta] hostile 点名的持械者（斧 / 剑 / 镐）：这个距离内就是在砍，不算干等
DWELL_MAX = 0.8                        # 扑咬距离内最多停这么久（不碰、也没被挡）——一扑就到的距离不会干等
# 常见反应动作的最短时长（秒，偏保守）；react.does 只许用这里的词
REACT_S = {"惊觉": 0.2, "抬头": 0.2, "转身": 0.3, "跪起": 0.6, "扯断带子": 0.3, "卸下背上的盾": 0.8, "蹲起": 0.5, "起身": 0.6, "抄起身边的兵器": 0.4,
           "捡起地上的兵器": 0.5, "拔剑": 0.6, "退半步": 0.3, "后退一步": 0.4, "举盾": 0.3, "握短兵器": 0.3,
           "起跑": 0.3, "站稳": 0.4, "大抡": 0.8, "短劈": 0.4}

# 「人站进实心体块」只查这个高度以上的块：矮块（碎石坡、营地、柴垛）在平面图上常是一片区域，人本来就走在里面
SOLID_H_M = 2.5
GUARD_ANGLE = 40.0
GUARD_FACE = 50.0
REF_SIZE = (1920, 1080)      # Seedance 版与成片同为 16:9
# ── 049 打击几何（G7）与施法因果（G8）──
FRONT_PART = re.compile(r"胸|脸|肚|下巴|鼻|额|嘴|面门")          # 只能从正面打到的部位
BACK_PART = re.compile(r"后背|背上|背后|背心|后腰|腿弯|后脑|后颈|(?<![手脚肩])背")   # 只能从背后打到的部位（手背 / 脚背 / 肩背不算）
QUADRUPED = re.compile(r"狼|熊|野猪|豹|犬|狗|马|鹿|虎|蜘蛛")   # 四足：背是顶面、从哪边都砸得到；体重轻，击退上限不按人算
KNOCK_RESULT = re.compile(r"倒|蹬|撞|扫|飞|退")                    # result 里有这些字＝挨了这一下要挪位置
KNOCK_MAX_M = {"锤": 1.2, "斧": 0.8, "剑": 0.6, "镐": 0.6, "棒": 0.8, "盾": 1.2, "拳": 0.8, "脚": 1.5,
               "咬": 0.6, "爪": 0.6, "撞": 1.5, "光": 1.5, "投": 1.5, "鞭": 0.4, "叉": 0.8}         # 挨这一下之后 KNOCK_WIN_S 秒内最多被带出去多远
KNOCK_WIN_S = 0.6
KNOCK_DIR_DEG = 45.0          # 被带出去的方向与「出手的人→挨打的人」夹角上限
LIGHT_CLEAR_M = 0.5           # 扔出去的光离己方各人中心至少这么远，不然就是从他身上穿过去
AGGRO_LEAD_S = 1.0            # 起光前这段时间里敌人朝施法者逼近 ≥ AGGRO_MOVE_M ＝ 先扑后有光
AGGRO_MOVE_M = 1.0
ARMED_IDLE_S = 2.0            # [meta] hostile 的持械者在 REACH_M 内停这么久、这段没有他的 [[hit]] ＝ 干站


class Bad(Exception):
    pass


def _drama_root(shot_dir: Path) -> Path:
    for d in (shot_dir, *shot_dir.parents):
        if (d / "2_世界观人设").is_dir():
            return d
    raise Bad("%s 往上找不到剧目录（没有 2_世界观人设/）" % shot_dir)


@functools.lru_cache(maxsize=None)     # 场景树一次运行里不变（os.walk 全树很慢）
def _bg_dir(scenes: Path, bg: str) -> Path:
    for dirpath, dirs, _ in os.walk(scenes):
        for d in dirs:
            if d.startswith(bg + "_") and (Path(dirpath) / d / (d + ".md")).is_file():
                return Path(dirpath) / d
    raise Bad("场景主体 %s 在 %s 下找不到" % (bg, scenes))


def _shot_md(shot_dir: Path) -> tuple[str, float, str, set[str]]:
    f = shot_dir / (shot_dir.name + ".md")
    if not f.is_file():
        raise Bad("没有 %s —— overhead 的时长与入画人物都从它读" % f.name)
    text = f.read_text(encoding="utf-8")
    title = (re.search(r"^title:\s*(.+)$", text, re.M) or [None, ""])[1]
    secs = float(re.search(r"^duration_s:\s*([0-9.]+)", text, re.M).group(1))
    jb = (re.search(r"\*\*景别档\*\*:\s*(.+)$", text, re.M) or [None, ""])[1]
    role = (re.search(r"^角色: (.*)$", text, re.M) or [None, ""])[1]
    chars = set(re.findall(r"(?:^|；)([cm]\d+_[^＝；]+)＝", role))
    return title, secs, jb, chars


def load(shot_dir: Path) -> dict:
    p = shot_dir / "planning" / "overhead.toml"
    if not p.is_file():
        raise Bad("没有 %s" % p.relative_to(REPO))
    with open(p, "rb") as fh:
        cfg = tomllib.load(fh)
    for sec, body in cfg.items():
        if sec not in KEYS:
            raise Bad("overhead.toml：未知段 [%s]" % sec)
        for item in (body if isinstance(body, list) else [body]):
            bad = set(item) - KEYS[sec]
            if bad:
                raise Bad("overhead.toml [%s] 未知键 %s（拼错不静默忽略）" % (sec, sorted(bad)))
    return cfg


def _inside(b: dict, x: float, y: float) -> bool:
    cs = planschema.corners(b)
    sign = None
    for i in range(4):
        (ax, ay), (bx, by) = cs[i], cs[(i + 1) % 4]
        cr = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        s = cr >= 0
        if sign is None:
            sign = s
        elif s != sign:
            return False
    return True


def gate(cfg: dict, site: dict, secs: float, chars: set[str], jb: str) -> tuple[list[str], list[str]]:
    bad: list[str] = []
    warn: list[str] = []
    cams = cfg.get("camera", [])
    if not cams:
        bad.append("没有 [[camera]] 路点")
    ts = [float(c["t"]) for c in cams]
    if ts != sorted(ts) or (ts and (ts[0] < 0 or ts[-1] > secs + 1e-6)):
        bad.append("机位时刻 %s 须不减且落在 0–%gs" % (ts, secs))
    keys: set[str] = set()
    for a in cfg.get("actor", []):
        keys.add(a["key"])
        pt = [float(p[0]) for p in a["path"]]
        if pt != sorted(pt) or pt[0] < 0 or pt[-1] > secs + 1e-6:
            bad.append("%s 的路点时刻 %s 须不减且落在 0–%gs" % (a["key"], pt, secs))
        for p in a["path"]:
            if len(p) not in (3, 5):
                bad.append("%s 的路点 %s 须是 [t,x,y] 或 [t,x,y,fx,fy]" % (a["key"], p))
    if chars - keys:
        bad.append("shot md 的 `角色:` 里有、平面图没给站位：%s" % "、".join(sorted(chars - keys)))
    if keys - chars:
        bad.append("平面图里有、shot md 的 `角色:` 没有：%s" % "、".join(sorted(keys - chars)))
    bad.extend(guard_errors(cfg))
    bad.extend(hit_errors(cfg))
    bad.extend(shield_errors(cfg))
    bad.extend(cast_errors(cfg))
    bad.extend(gaze_errors(cfg))
    bad.extend(strike_errors(cfg))
    bad.extend(cast_order_errors(cfg))
    bad.extend(prop_errors(cfg, secs))
    bad.extend(ghost_errors(cfg, secs))
    phys = physics_errors(cfg)
    (bad if cfg.get("guard") or cfg.get("react") else warn).extend(phys)
    Wm, Hm = site["meta"]["size_m"]
    open_ids = set(cfg["meta"].get("walkable", []))
    for a in cfg.get("actor", []):        # 人站进实心体块（含构件派生的门塔之类）：画出来就是半截人埋在墙里
        for pt in a["path"]:
            for b in (q for b0 in site.get("block", []) for q in solid_parts(b0)):
                x, y = float(pt[1]), float(pt[2])
                if float(b.get("h_m", 0) or 0) >= SOLID_H_M and b.get("kind") not in WALKABLE \
                        and b.get("id") not in open_ids and _inside(b, x, y) and not _in_opening(b, x, y):
                    bad.append("%s t=%gs 站在「%s」(h%g m) 里面" % (a.get("label", a["key"]), float(pt[0]), b["name"],
                                                                 float(b["h_m"])))
                    break
    for c in cams:
        x, y = c["xy"]
        if not (-5 <= x <= Wm + 5 and -5 <= y <= Hm + 5):
            bad.append("机位 t=%gs 落在场地外 %s（场地 %g×%g m）" % (c["t"], c["xy"], Wm, Hm))
        for b in site.get("block", []):
            h = float(b.get("h_m", 0) or 0)
            if h > float(c.get("h", 1.6)) and b.get("kind") not in WALKABLE \
                    and b.get("id") not in open_ids and _inside(b, x, y):
                warn.append("机位 t=%gs 在「%s」(h%g m) 里面" % (c["t"], b["name"], h))
    # 起幅 / 落幅：按景别档的人占画高与焦距反算机位距离，与图上距离比一下
    m = re.findall(r"(远景|全景|中景|近景|特写)([0-9.]+)", jb)
    acts = {a["key"]: a for a in cfg.get("actor", [])}
    first = next(iter(acts), None)
    for c in cams:
        if c.get("subject") and c["subject"] not in acts:
            bad.append("机位 t=%gs 的 subject %s 不是本镜的 actor" % (c["t"], c["subject"]))
    if m and first and cams:
        for (name, v), c in ((m[0], cams[0]), (m[-1], cams[-1])):
            subj = acts.get(c.get("subject", first), acts[first])
            frac = float(v)
            lens = float(c.get("lens", 35))
            vfov = 2 * math.atan((SENSOR_W * 9 / 16) / (2 * lens))
            want = SUBJ_H / frac / (2 * math.tan(vfov / 2))
            p = _pos_at(subj["path"], float(c["t"]))
            got = math.dist(c["xy"], p)
            if got and not 0.4 <= got / want <= 2.5:
                warn.append("t=%gs %s%s：按 %gmm 该离主体约 %.1fm，图上是 %.1fm" % (
                    c["t"], name, v, lens, want, got))
    return bad, warn


def previz_triggers(cfg: dict, secs: float) -> list[str]:
    """这一镜为什么需要 previz MP4（空 ＝ 简单镜，overhead 图直接进 Seedance）。"""
    out: list[str] = []
    cams = cfg.get("camera", [])
    travel = sum(math.dist(a["xy"], b["xy"]) for a, b in zip(cams, cams[1:]) if not b.get("cut"))
    if travel > PREVIZ_CAM_TRAVEL_M:
        out.append("机位连续移动 %.0fm > %gm" % (travel, PREVIZ_CAM_TRAVEL_M))
    segs = 1 + sum(1 for c in cams[1:] if c.get("cut"))
    if segs >= PREVIZ_SEGMENTS:
        out.append("镜内硬切 %d 段 ≥ %d" % (segs, PREVIZ_SEGMENTS))
    acts = cfg.get("actor", [])
    step = 0.25
    cut_ts = [float(c["t"]) for c in cams if c.get("cut")]
    ts = [k * step for k in range(int(secs / step) + 1)
          if not any(k * step - 0.2 <= c <= (k + 1) * step for c in cut_ts)]     # 8f S12：硬切那一刻整组换站位不算「同时走动」
    movers = max((sum(1 for a in acts if math.dist(_pos_at(a["path"], t), _pos_at(a["path"], t + step)) > MOVE_MPS * step)
                  for t in ts), default=0)
    if movers >= PREVIZ_MOVERS:
        out.append("同时走动 %d 人 ≥ %d" % (movers, PREVIZ_MOVERS))
    pairs = set()
    for i, a in enumerate(acts):
        for j in range(i + 1, len(acts)):
            b = acts[j]
            for t in ts:
                pa, pb = _pos_at(a["path"], t), _pos_at(b["path"], t)
                moving = math.dist(pa, _pos_at(a["path"], t + step)) + math.dist(pb, _pos_at(b["path"], t + step)) > 0.05
                if moving and math.dist(pa, pb) < CONTACT_M:
                    pairs.add((a["key"], b["key"]))
                    break
    if len(pairs) >= PREVIZ_CONTACTS:
        out.append("肢体接触 %d 对 ≥ %d" % (len(pairs), PREVIZ_CONTACTS))
    # 攻防（follow-up 032）：人与怪只要碰上一次就是打斗编排——谁在哪一侧、面朝哪、盾朝哪，散文与俯视图都交代不清
    fights = sorted({"%s×%s" % (a, b) for a, b in pairs if {a[0], b[0]} == {"c", "m"}})
    if fights:
        out.append("人与怪攻防接触 %s" % "、".join(fights))
    if cfg.get("guard"):
        out.append("护人格挡 %d 段" % len(cfg["guard"]))
    if cfg.get("react"):
        out.append("反应窗 %d 段" % len(cfg["react"]))
    return out


def previz_decision(cfg: dict, secs: float) -> tuple[bool, str]:
    """(要不要 previz, 理由)。`[meta] previz` 推翻自动判定时必须写 `previz_why`，否则 raise。"""
    trig = previz_triggers(cfg, secs)
    auto = bool(trig)
    meta = cfg.get("meta", {})
    if "previz" not in meta:
        return auto, "；".join(trig) if trig else "简单镜，overhead 图足够"
    want = bool(meta["previz"])
    why = meta.get("previz_why", "")
    if want != auto and not why:
        raise Bad("[meta] previz = %s 与自动判定（%s）相反，须写 previz_why" % (
            str(want).lower(), "；".join(trig) or "简单镜"))
    return want, why or ("；".join(trig) if trig else "简单镜，overhead 图足够")


def actor_colors(cfg: dict) -> dict[str, tuple]:
    """人物色按卡号固定（c1 永远同一色），跨镜一致——同一个人换一镜换一个颜色，读图的人与模型都会认错。
    同镜撞色的按卡号从小到大顺延到下一个空色。"""
    def num(k: str) -> tuple[int, int]:
        m = re.match(r"([a-z])(\d+)", k)
        return ((0 if m.group(1) == "c" else 1), int(m.group(2))) if m else (2, 0)
    out: dict[str, tuple] = {}
    for a in sorted(cfg.get("actor", []), key=lambda a: num(a["key"])):
        c, n = num(a["key"])
        i = (n - 1 + c * 5) % len(ACTOR_COLORS)
        while ACTOR_COLORS[i] in out.values() and len(out) < len(ACTOR_COLORS):
            i = (i + 1) % len(ACTOR_COLORS)
        out[a["key"]] = ACTOR_COLORS[i]
    return out


def _here(a: dict, t: float) -> bool:
    return (a.get("enter") is None or t >= float(a["enter"]) - 1e-6) and (a.get("gone") is None or t <= float(a["gone"]) + 1e-6)


def _pos_at(path: list, t: float) -> tuple[float, float]:
    pts = [(float(p[0]), float(p[1]), float(p[2])) for p in path]
    if t <= pts[0][0]:
        return pts[0][1], pts[0][2]
    for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return pts[-1][1], pts[-1][2]


def jump_cuts(cfg: dict, min_m: float = 3.0) -> list[float]:
    """跳过了时间的镜内硬切：切点前后 0.2 s 内有人挪了 ≥ 3 m（平面图允许在切点把人放到下一段站位）。"""
    out = []
    for c in cfg.get("camera", []):
        if not c.get("cut"):
            continue
        t = float(c["t"])
        if any(math.dist(_pos_at(a["path"], t - 0.15), _pos_at(a["path"], t + 0.05)) >= min_m for a in cfg.get("actor", [])):
            out.append(t)
    return out


def subj_frac(c: dict, xy) -> float:
    """人占画高：机位 c 下站在 xy 的人（高 SUBJ_H）占画面高的比例（与 FRAC 同一把尺）。"""
    d = max(math.dist(c["xy"], xy), 0.1)
    return SUBJ_H / (2 * d * (SENSOR_W * 9 / 16) / (2 * float(c.get("lens", 35))))


def cam_at(cams: list, t: float) -> dict:
    """t 时刻的机位（位置 / 瞄点 / 焦距 / 高）：相邻两个路点之间线性插值，下一个路点是硬切就保持。"""
    cs = sorted(cams, key=lambda c: float(c["t"]))
    cur = cs[0]
    for c in cs:
        if float(c["t"]) <= t + 1e-6:
            cur = c
    nxt = next((c for c in cs if float(c["t"]) > t + 1e-6), None)
    if nxt is None or nxt.get("cut") or float(nxt["t"]) <= float(cur["t"]):
        return {"xy": cur["xy"], "look": cur.get("look", cur["xy"]), "lens": float(cur.get("lens", 35)), "h": float(cur.get("h", 1.6))}
    k = (t - float(cur["t"])) / (float(nxt["t"]) - float(cur["t"]))
    lerp = lambda a, b: [a[i] + (b[i] - a[i]) * k for i in (0, 1)]
    return {"xy": lerp(cur["xy"], nxt["xy"]), "look": lerp(cur.get("look", cur["xy"]), nxt.get("look", nxt["xy"])),
            "lens": float(cur.get("lens", 35)), "h": float(cur.get("h", 1.6))}


def visibility(cfg: dict, site: dict, t: float) -> dict[str, str]:
    """{actor label: "ok" | "画外" | "被 X 挡住"}——俯视近似：人按 0.22 m 半宽的立柱，挡人的是更近的人与比机位高的实心块
    （含构件派生的门塔）。说台词的人看不见、要看的人被挡，在这里 1 秒就能知道，不必等 previz 渲出来。"""
    cams = cfg.get("camera", [])
    if not cams:
        return {}
    c = cam_at(cams, t)
    cx, cy = c["xy"]
    ax = math.atan2(c["look"][1] - cy, c["look"][0] - cx)
    half = math.atan(SENSOR_W / 2 / c["lens"])
    acts = [(a.get("label", a["key"]), _pos_at(a["path"], t)) for a in cfg.get("actor", []) if _here(a, t)]
    geo = []
    for lb, (x, y) in acts:
        d = max(math.hypot(x - cx, y - cy), 0.05)
        geo.append((lb, x, y, d, math.atan2(y - cy, x - cx), math.atan(0.22 / d)))
    walls = [p for b in site.get("block", []) if float(b.get("h_m", 0) or 0) >= max(SOLID_H_M, c["h"])
             and b.get("kind") not in WALKABLE for p in solid_parts(b) if not _inside(p, cx, cy)]  # 机位在块里（内景）就不算它挡
    out: dict[str, str] = {}
    for lb, x, y, d, ang, w in geo:
        off = abs((ang - ax + math.pi) % (2 * math.pi) - math.pi)
        if off > half + w:
            out[lb] = "画外"
            continue
        who = next((o[0] for o in geo if o[0] != lb and o[3] < d - 0.3
                    and abs((o[4] - ang + math.pi) % (2 * math.pi) - math.pi) < (o[5] + w) * 0.6), None)
        if who is None:
            n = max(2, int(d / 0.2))
            for b in walls:
                if _inside(b, x, y):          # 人自己站在这块里：它是一片区域（营地、院子），不是挡在前面的墙
                    continue
                if any(_inside(b, cx + (x - cx) * k / n, cy + (y - cy) * k / n) and not _in_opening(
                        b, cx + (x - cx) * k / n, cy + (y - cy) * k / n) for k in range(1, n)):
                    who = b["name"]
                    break
        if who is None:                        # 8f 站位 5：矮块（翻倒的货车…）挡不挡看视线在那儿有多高（2.5D）
            open_ids = set(cfg.get("meta", {}).get("walkable", []))
            ch = float(c.get("h", 1.6))
            for b in (p for b0 in site.get("block", []) if 0 < float(b0.get("h_m", 0) or 0) < max(SOLID_H_M, c["h"])
                      and b0.get("kind") not in WALKABLE and b0.get("id") not in open_ids for p in solid_parts(b0)):
                if _inside(b, cx, cy) or _inside(b, x, y):
                    continue
                n = max(2, int(d / 0.2))
                if any(_inside(b, cx + (x - cx) * k / n, cy + (y - cy) * k / n) and not _in_opening(b, cx + (x - cx) * k / n, cy + (y - cy) * k / n)
                       and float(b["h_m"]) >= ch + (FACE_H_M - ch) * k / n for k in range(1, n)):
                    who = b["name"]
                    break
        out[lb] = "被%s挡住" % who if who else "ok"
    return out


PASS_M = 0.35       # 两人中心距小于它＝一个从另一个身上穿过去（肩宽约 0.45 m，8f 站位 7）
LOW_SOLID_H_M = 1.0     # 8f 站位 5：这么高以上的非可走块（翻倒的货车、南瓜堆、柴垛）里也不许站人
STAND_MARGIN_M = 0.1    # 进块这么深才算站进去——贴着边（撞在柴垛上、靠着货车）不算
FACE_H_M = 1.5          # 2.5D 遮挡：视线从机位连到人脸这个高度


def _depth_in(b: dict, x: float, y: float) -> float:
    """点在块里多深（m）：到最近一条边的距离，在块外为负。块按中心 xy、size、rot（度）的矩形算，与 solid_parts 同一口径。"""
    r = math.radians(float(b.get("rot", 0) or 0))
    dx, dy = x - float(b["xy"][0]), y - float(b["xy"][1])
    lx, ly = dx * math.cos(r) + dy * math.sin(r), -dx * math.sin(r) + dy * math.cos(r)
    sx, sy = (float(v) for v in b["size"])
    return min(sx / 2 - abs(lx), sy / 2 - abs(ly))


def low_block_errors(cfg: dict, site: dict) -> list[str]:
    """8f 站位 5：人站进 LOW_SOLID_H_M–SOLID_H_M 高的非可走块（≥ SOLID_H_M 的由 gate 查）。地形类（碎石坡、栈桥）写本镜 [meta] walkable。"""
    out: list[str] = []
    open_ids = set(cfg["meta"].get("walkable", []))
    blocks = [q for b0 in site.get("block", []) for q in solid_parts(b0)
              if LOW_SOLID_H_M <= float(b0.get("h_m", 0) or 0) < SOLID_H_M and b0.get("kind") not in WALKABLE and b0.get("id") not in open_ids]
    for a in cfg.get("actor", []):
        for pt in a["path"]:
            x, y = float(pt[1]), float(pt[2])
            b = next((b for b in blocks if _depth_in(b, x, y) >= STAND_MARGIN_M and not _in_opening(b, x, y)), None)
            if b is not None:
                out.append("%s t=%gs 站在「%s」(h%g m) 里面——挪到它边上；它是能走上去的地形就在本镜 [meta] walkable 写它的 id（%s）（8f 站位 5）"
                           % (a.get("label", a["key"]), float(pt[0]), b["name"], float(b["h_m"]), b.get("id")))
                break
    return out





def path_cross_errors(cfg: dict) -> list[str]:
    """8f 站位 7（ep02 S38 沃尔特从杜克和亚伦中间穿过去）：一个人走一段路（两个路点之间挪了 ≥ 0.3 m），同一时刻离另一个在场的人
    < PASS_M 就是穿人；镜内跳切那一下的瞬移（≤ 0.3 s 的一段、贴着切点）不算。只由 szzl 引擎调用，旧剧不回溯。"""
    cuts = [float(c["t"]) for c in cfg.get("camera", []) if c.get("cut")]
    acts = [a for a in cfg.get("actor", []) if int(a.get("count", 1)) == 1]
    hits: dict[frozenset, tuple[float, float, str, str, float, float]] = {}
    for A in acts:
        pts = [(float(p[0]), float(p[1]), float(p[2])) for p in A["path"]]
        for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
            if t1 <= t0 or math.hypot(x1 - x0, y1 - y0) < 0.3:
                continue
            if t1 - t0 <= 0.3 and any(t0 - 0.05 <= c <= t1 + 0.05 for c in cuts):
                continue
            for B in acts:
                if B is A:
                    continue
                for k in range(11):
                    t = t0 + (t1 - t0) * k / 10
                    if not (_here(A, t) and _here(B, t)):
                        continue
                    dd = math.dist(_pos_at(A["path"], t), _pos_at(B["path"], t))
                    key = frozenset((id(A), id(B)))
                    if dd < PASS_M and (key not in hits or dd < hits[key][0]):
                        hits[key] = (dd, t, A.get("label", A["key"]), B.get("label", B["key"]), t0, t1)
    return ["%s %g–%gs 走的这段在 %.1fs 从%s身上穿过去（中心距 %.2f m < %g m）——绕开他，或让他先让开（8f 站位 7）"
            % (a, t0, t1, t, b, dd, PASS_M) for dd, t, a, b, t0, t1 in sorted(hits.values(), key=lambda h: h[1])]


def solid_parts(b: dict) -> list[dict]:
    """一块在平面图上可能是「一排 N 件」（count + layout = "row"：一排柱子、一排木桶）：
    查遮挡与站位时拆成 N 个单件，件与件之间是空的——整块当实心墙会把柱廊后面的人全判成被挡。"""
    n = int(b.get("count", 1) or 1)
    if n <= 1 or b.get("layout") != "row":
        return [b]
    sx, sy = (float(v) for v in b["size"])
    along_x = sx >= sy
    L, D = (sx, sy) if along_x else (sy, sx)
    r = math.radians(float(b.get("rot", 0)))
    ux, uy = (math.cos(r), math.sin(r)) if along_x else (-math.sin(r), math.cos(r))
    out = []
    for i in range(n):
        off = -L / 2 + L * (i + 0.5) / n
        out.append({**b, "xy": [b["xy"][0] + ux * off, b["xy"][1] + uy * off],
                    "size": [D, D] if along_x else [D, D], "count": 1, "layout": None})
    return out


def _in_opening(b: dict, x: float, y: float) -> bool:
    """块自带的通道：gate_wall 的门洞（build_scene 按 gate_w 在块中心开洞）。"""
    return b.get("kind") == "gate_wall" and abs(x - float(b["xy"][0])) <= float(b.get("gate_w", 5.0)) / 2.0


# 画面相对的朝向（follow-up 036：shot04 两人说话全程背对镜头——平面图与 prompt 只写罗盘方向，模型不知道画面里哪边是东）
FACE_CLASS = ((45.0, "正脸"), (70.0, "3/4 侧脸"), (110.0, "侧脸"), (181.0, "背影"))   # 面朝与「人→机位」的夹角上限
SPEAKER_BACK_DEG, SPEAKER_PROFILE_DEG = 110.0, 70.0   # 说台词的人：超过前者＝背对镜头（blocker），介于两者＝纯侧脸（warning）


def face_vec(path: list, t: float) -> tuple[float, float] | None:
    """t 时刻的面朝，与 previz_config 同一口径：路点写了面朝就用它；没写而在走，就是行进方向；停着就沿用上一个。"""
    pts = sorted(path, key=lambda p: float(p[0]))
    u = None
    for i, p in enumerate(pts):
        if i and float(p[0]) > t + 1e-6:
            break
        nxt = pts[i + 1] if i + 1 < len(pts) else None
        if len(p) >= 5:
            u = (float(p[3]) - float(p[1]), float(p[4]) - float(p[2]))
        elif nxt is not None and math.dist((float(p[1]), float(p[2])), (float(nxt[1]), float(nxt[2]))) > 0.05:
            u = (float(nxt[1]) - float(p[1]), float(nxt[2]) - float(p[2]))
    return u if u and math.hypot(*u) > 1e-6 else None


def screen_view(cfg: dict, t: float) -> dict[str, dict]:
    """t 时刻每个入画的人在画面里的样子：side＝画左 / 画中 / 画右；deg＝面朝与「人→机位」的夹角；
    face＝正脸 / 3/4 侧脸 / 侧脸 / 背影；turn＝正对镜头 / 朝画左 / 朝画右 / 背对镜头。画外的人不在结果里。"""
    cams = cfg.get("camera", [])
    if not cams:
        return {}
    c = cam_at(cams, t)
    cx, cy = c["xy"]
    ax = math.atan2(c["look"][1] - cy, c["look"][0] - cx)
    half = math.atan(SENSOR_W / 2 / c["lens"])
    rx, ry = -math.sin(ax), math.cos(ax)          # 画面右方（y 向南的平面上，面朝方向顺时针转 90°）
    out: dict[str, dict] = {}
    for a in cfg.get("actor", []):
        if not _here(a, t):
            continue
        x, y = _pos_at(a["path"], t)
        d = max(math.hypot(x - cx, y - cy), 0.05)
        off = (math.atan2(y - cy, x - cx) - ax + math.pi) % (2 * math.pi) - math.pi
        if abs(off) > half + math.atan(0.22 / d):
            continue
        side = "画中" if abs(off) < half / 3 else ("画右" if off > 0 else "画左")
        u = face_vec(a["path"], t)
        v = {"key": a["key"], "side": side, "deg": None, "face": "", "turn": ""}
        if u is not None:
            vx, vy = cx - x, cy - y
            cos = (u[0] * vx + u[1] * vy) / (math.hypot(*u) * math.hypot(vx, vy) or 1.0)
            deg = math.degrees(math.acos(max(-1.0, min(1.0, cos))))
            face = next(n for lim, n in FACE_CLASS if deg < lim)
            turn = ("正对镜头" if face == "正脸" else "背对镜头" if face == "背影"
                    else "朝画右" if u[0] * rx + u[1] * ry > 0 else "朝画左")
            v.update(deg=deg, face=face, turn=turn)
        out[a.get("label", a["key"])] = v
    return out


def screen_x(cfg: dict, t: float) -> dict[str, float]:
    """t 时刻每个入画的人在画面里的横向位置：-1 ＝ 画面最左、+1 ＝ 最右（与 screen_view 同一套算法；跨镜轴线闸门用）。"""
    cams = cfg.get("camera", [])
    if not cams:
        return {}
    c = cam_at(cams, t)
    cx, cy = c["xy"]
    ax = math.atan2(c["look"][1] - cy, c["look"][0] - cx)
    half = math.atan(SENSOR_W / 2 / c["lens"])
    out: dict[str, float] = {}
    for a in cfg.get("actor", []):
        if not _here(a, t):
            continue
        x, y = _pos_at(a["path"], t)
        d = max(math.hypot(x - cx, y - cy), 0.05)
        off = (math.atan2(y - cy, x - cx) - ax + math.pi) % (2 * math.pi) - math.pi
        if abs(off) <= half + math.atan(0.22 / d):
            out[a.get("label", a["key"])] = max(-1.0, min(1.0, off / half))
    return out


def _face_at(path: list, t: float) -> tuple[float, float] | None:
    """t 时刻的面朝：取 t 以前最后一个写了面朝的路点（[t,x,y,fx,fy] 的 fx,fy 是「看向的点」）。"""
    got = None
    for p in path:
        if float(p[0]) <= t + 1e-6 and len(p) == 5:
            got = (float(p[3]) - float(p[1]), float(p[4]) - float(p[2]))
    return got


def _actor(cfg: dict, ref: str) -> dict | None:
    hits = [a for a in cfg.get("actor", []) if ref in (a["key"], a.get("label"))]
    return hits[0] if len(hits) == 1 else None


def _between(b: tuple, m: tuple, h: tuple, half_w: float = 0.6) -> bool:
    """b 站在 m→h 那条扑击线上（离线 ≤ half_w、在两端之间）：怪得先过 b 这一关。"""
    dx, dy = h[0] - m[0], h[1] - m[1]
    L2 = dx * dx + dy * dy
    if L2 < 1e-9:
        return False
    k = ((b[0] - m[0]) * dx + (b[1] - m[1]) * dy) / L2
    if not 0.0 < k < 1.0:
        return False
    return math.dist(b, (m[0] + dx * k, m[1] + dy * k)) <= half_w


def physics_errors(cfg: dict) -> list[str]:
    """速度上限、怪在扑咬距离内干等、反应来不及。只对有 [[guard]] 或 [[react]] 的镜（按新做法编排的攻防镜）当 blocker，
    其余镜由 physics_warnings 只报不拦（规则不回溯旧镜）。"""
    out: list[str] = []
    acts = cfg.get("actor", [])
    # 镜内硬切处平面图允许人「跳到」下一段的站位（中间的时间剪掉了）：跨切点的路段不查速度，扑咬计时也在切点清零
    cuts = [float(c["t"]) for c in cfg.get("camera", []) if c.get("cut")]
    for a in acts:
        lim = SPEED_MAX.get(a["key"][0])
        pts = [(float(p[0]), float(p[1]), float(p[2])) for p in a["path"]]
        for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
            if any(t0 - 0.15 < c <= t1 + 0.15 for c in cuts):   # 切点前后换位（跳过了时间）不算瞬移
                continue
            if lim and t1 > t0 and math.hypot(x1 - x0, y1 - y0) / (t1 - t0) > lim:
                out.append("%s %g–%gs 平均 %.1f m/s > %g m/s（瞬移）" % (
                    a.get("label", a["key"]), t0, t1, math.hypot(x1 - x0, y1 - y0) / (t1 - t0), lim))
    guards = cfg.get("guard", [])
    step = 0.1
    end = max((float(p[0]) for a in acts for p in a["path"]), default=0.0)
    humans = [a for a in acts if a["key"].startswith("c")]
    # 只有本镜里真碰过人的怪才算威胁（门卫、围观的群体不算）
    declared = set(cfg.get("meta", {}).get("hostile", []))      # 持械的人（加瑞克之类）在这里点名
    calm = set(cfg.get("meta", {}).get("calm", []))             # 碰到人也不是威胁的（缩成一团接蜡烛的小矿工）
    humans = [a for a in humans if a["key"] not in declared and a.get("label") not in declared]
    hostile = [m for m in acts if m.get("label") not in calm and m["key"] not in calm and (m["key"] in declared or m.get("label") in declared) or (m.get("label") not in calm and m["key"].startswith("m") and any(
        math.dist(_pos_at(m["path"], k * step), _pos_at(h["path"], k * step)) < CONTACT_M
        for h in humans for k in range(int(end / step) + 1)))]
    for m in hostile:
        armed = m["key"] in declared or m.get("label") in declared
        lo = REACH_M if armed else CONTACT_M
        hi = max(LUNGE_M, lo + 0.8)
        for h in humans:
            run = 0.0
            t = 0.0
            while t <= end + 1e-6:
                if any(abs(t - c) < step / 2 for c in cuts):
                    run = 0.0
                d = math.dist(_pos_at(m["path"], t), _pos_at(h["path"], t))
                if not _here(m, t) or any(o is not h and math.dist(_pos_at(m["path"], t), _pos_at(o["path"], t)) < lo
                                          for o in humans):     # 049：正跟别人贴身打着，不算在这个人身前干等
                    run, t = 0.0, t + step
                    continue
                shielded = any(float(g["t0"]) <= t <= float(g["t1"]) and g["threat"] in (m.get("label"), m["key"])
                               for g in guards) or any(
                    _between(_pos_at(b["path"], t), _pos_at(m["path"], t), _pos_at(h["path"], t))
                    for b in humans if b is not h)
                if lo <= d <= hi and not shielded:
                    run += step
                    if run > DWELL_MAX + 1e-6:
                        out.append("%s 在 %s 身前 %.1f m 停了 %.1f s 还没扑（%.1fs 前后）——一扑就到的距离不会干等"
                                   % (m.get("label", m["key"]), h.get("label", h["key"]), d, run, t))
                        break
                else:
                    run = 0.0
                t += step
    for r in cfg.get("react", []):
        who = _actor(cfg, r["who"])
        bad_words = [w for w in r["does"] if w not in REACT_S]
        if who is None or bad_words:
            out.append("[[react]] who=%s 不是唯一 actor，或 does 有表外动作 %s（可用：%s）"
                       % (r["who"], bad_words, "、".join(REACT_S)))
            continue
        t0, t1 = float(r["t_cue"]), float(r["t_ready"])
        need = sum(REACT_S[w] for w in r["does"])
        if t1 - t0 + 1e-6 < need:
            out.append("%s %g→%gs 要做完「%s」至少 %.1f s，只给了 %.1f s" % (
                r["who"], t0, t1, "＋".join(r["does"]), need, t1 - t0))
        t = t0
        while t <= t1 + 1e-6:
            hit = next((m for m in acts if m["key"].startswith("m")
                        and math.dist(_pos_at(m["path"], t), _pos_at(who["path"], t)) < CONTACT_M), None)
            if hit:
                out.append("%s 还没准备好（%gs 才做完「%s」）就在 %.1fs 被 %s 碰上了" % (
                    r["who"], t1, "＋".join(r["does"]), t, hit.get("label", hit["key"])))
                break
            t += step
    return out


def hit_errors(cfg: dict) -> list[str]:
    """命中：那一刻够得着、面朝目标。只写「一锤砸下去」而不算距离，出片里锤子挥在空气里（follow-up 042）。"""
    out: list[str] = []
    for h in cfg.get("hit", []):
        who, tgt = _actor(cfg, h["who"]), _actor(cfg, h["target"])
        if who is None or tgt is None:
            out.append("[[hit]] who=%s / target=%s 不是唯一的 actor key / label" % (h["who"], h["target"]))
            continue
        if h.get("with") not in REACH:
            out.append("[[hit]] %gs with=%s 不在够得着表里（可用：%s）" % (float(h["t"]), h.get("with"), "、".join(REACH)))
            continue
        if h.get("miss"):
            continue
        t = float(h["t"])
        P, T = _pos_at(who["path"], t), _pos_at(tgt["path"], t)
        reach = REACH[h["with"]] + (1.0 if int(tgt.get("count", 1)) > 1 else 0.0)   # 一群的路径是群心，打的是最近那几只
        d, why = math.dist(P, T), []
        if d > reach:
            why.append("相距 %.1f m，%s够不着（≤ %.1f m）" % (d, h["with"], reach))
        f = _face_at(who["path"], t)
        if f is None:                                   # 没写面朝：按前 0.3 s 的走向；站着没动就不查
            q = _pos_at(who["path"], t - 0.3)
            f = (P[0] - q[0], P[1] - q[1]) if math.dist(P, q) > 0.05 else None
        if f is not None and d > 1e-6 and not h.get("back"):
            v = (T[0] - P[0], T[1] - P[1])
            off = math.degrees(abs(math.atan2(f[0] * v[1] - f[1] * v[0], f[0] * v[0] + f[1] * v[1])))
            if off > HIT_FACE:
                why.append("面朝偏离目标 %.0f° > %g°" % (off, HIT_FACE))
        if why:
            out.append("[[hit]] %gs %s 用%s打 %s：%s" % (t, h["who"], h["with"], h["target"], "；".join(why)))
        out += friend_line_errors(cfg, h, who, tgt, P, T, t)
    return out


def friend_actors(cfg: dict) -> list[dict]:
    """自己人＝c 开头的角色，且不在 meta.hostile 里（加瑞克这类敌方具名人物不算）。"""
    hostile = set(cfg.get("meta", {}).get("hostile", []))
    return [a for a in cfg.get("actor", []) if str(a.get("key", "")).startswith("c") and a.get("label") not in hostile and a.get("path")]


def friend_line_errors(cfg: dict, h: dict, who: dict, tgt: dict, P: tuple, T: tuple, t: float) -> list[str]:
    """G19 友方不入挥击线：近战（够得着表里非光 / 投 / 身体部位）、出手的是自己人、目标不是自己人时，
    另一个自己人（含他的盾）落在「出手→目标」±FRIEND_ARC 内、且在够得着的距离内，就是挥击线上有自己人——出片会砸到他的盾 / 身上。"""
    fr = {a["label"] for a in friend_actors(cfg)}
    if h.get("miss") or h.get("with") in ("光", "投") or who.get("label") not in fr or tgt.get("label") in fr:
        return []
    v = (T[0] - P[0], T[1] - P[1])
    if math.hypot(*v) < 1e-6:
        return []
    out = []
    for a in friend_actors(cfg):
        if a is who or a.get("label") == who.get("label"):
            continue
        F = _pos_at(a["path"], t)
        w = (F[0] - P[0], F[1] - P[1])
        d = math.hypot(*w)
        if d < 1e-6 or d > REACH[h["with"]]:
            continue
        off = math.degrees(abs(math.atan2(v[0] * w[1] - v[1] * w[0], v[0] * w[0] + v[1] * w[1])))
        if off <= FRIEND_ARC:
            out.append("[[hit]] %gs %s 用%s打 %s：自己人 %s 就在挥击线上（%.1f m、偏 %.0f° ≤ %g°）——会砸到他 / 他的盾；换站位（站到他侧后方 / 让怪绕到侧面）或换面朝（G19）"
                       % (t, h["who"], h["with"], h["target"], a["label"], d, off, FRIEND_ARC))
    return out


def strike_errors(cfg: dict) -> list[str]:
    """G7 打击几何（049：S11 矿工从正背后撞、亚伦却朝它跌坐；S20 一脚蹬出去的方向与脚差 92°、2.2 m）：
    part 只能从正面 / 背后打到的，出手的人得在那一侧；result 写倒 / 蹬 / 撞 / 扫 / 飞 / 退的，挨打的人随后
    KNOCK_WIN_S 秒顺着「出手→挨打」方向（≤ KNOCK_DIR_DEG）移动、不超过 KNOCK_MAX_M。一群（count > 1）不查。"""
    out: list[str] = []
    cuts = [float(c["t"]) for c in cfg.get("camera", []) if c.get("cut")]
    for h in cfg.get("hit", []):
        who, tgt = _actor(cfg, h["who"]), _actor(cfg, h["target"])
        if who is None or tgt is None or h.get("miss") or int(tgt.get("count", 1)) > 1:
            continue
        t = float(h["t"])
        P, T = _pos_at(who["path"], t), _pos_at(tgt["path"], t)
        part = str(h.get("part", ""))
        quad = bool(QUADRUPED.search(str(tgt.get("label", ""))))
        b = None if quad else _bearing(tgt, P, t)
        if b is not None:
            if BACK_PART.search(part) and abs(b) < 90:
                out.append("[[hit]] %gs %s 打在 %s 的%s，但人在他%s（%+.0f°）——打背 / 腿弯得从背后来，要么改 part、要么改站位"
                           % (t, h["who"], h["target"], part, "正前" if abs(b) < 30 else "侧前", b))
            elif FRONT_PART.search(part) and not BACK_PART.search(part) and abs(b) > 90:
                out.append("[[hit]] %gs %s 打在 %s 的%s，但人在他背后（%+.0f°）——正面的部位只能从正面打到"
                           % (t, h["who"], h["target"], part, b))
        if not KNOCK_RESULT.search(str(h.get("result", ""))) or any(t - 0.05 < c <= t + KNOCK_WIN_S for c in cuts):
            continue
        T1 = _pos_at(tgt["path"], t + KNOCK_WIN_S)
        dv = (T1[0] - T[0], T1[1] - T[1])
        m = math.hypot(*dv)
        v = (T[0] - P[0], T[1] - P[1])
        if m > 0.2 and math.hypot(*v) > 1e-6:
            off = math.degrees(abs(math.atan2(v[0] * dv[1] - v[1] * dv[0], v[0] * dv[0] + v[1] * dv[1])))
            if off > KNOCK_DIR_DEG:
                out.append("[[hit]] %gs %s 挨了 %s 这一下，随后 %gs 却朝偏离出招方向 %.0f° 的地方挪了 %.1f m——被打出去要顺着出招方向"
                           % (t, h["target"], h["who"], KNOCK_WIN_S, off, m))
        cap = KNOCK_MAX_M.get(str(h.get("with")), 1.2)
        if m > cap and not quad:
            out.append("[[hit]] %gs %s 用%s这一下把 %s 在 %gs 里带出去 %.1f m（> %g m）——超出这一招的力气，改成踉跄几步再倒"
                       % (t, h["who"], h.get("with"), h["target"], KNOCK_WIN_S, m, cap))
    return out


IDLE_MAX_S = 3.0      # 打斗窗里参战的友方最多这么久没有出手 / 格挡 / 施法 / 挨打 / 倒地（051 G11）
BOUT_GAP_S = 6.0      # 敌我两下之间停了这么久＝打完一场、下一场另算（S02 狼逃走、说完话、回头又咬一口）
HURT_MIN_S = 1.0      # 打在具名人物身上至少疼这么久（051 G12）
RUN_MPS = 1.6         # 腿疼的时候超过这个速度＝在跑
REFLEX_S = 0.3        # 挨打后这么快的还手是条件反射（被咬的脚一甩），不算疼着还出手
GEAR_PART = re.compile(r"盾|甲|锤|斧|镐|剑|棒|草叉|叉股|兵器|烛|木撑|靴|手套|护腕|盔|包")
DOWN_RESULT = re.compile(r"倒|跌坐|仰面|扑跪|跪下|砸在碎石")
ARM_PART = {"左": re.compile(r"左(肩|臂|胳膊|手|小臂|前臂)"), "右": re.compile(r"右(肩|臂|胳膊|手|小臂|前臂)")}
LEG_PART = re.compile(r"腿|膝|脚|踝|胯")
WEAK_RESULT = re.compile(r"撑不住|垂|松|掉|歪|软|抖|咬牙|举不")


def _fighter(cfg: dict, name: str) -> bool:
    a = _actor(cfg, name)
    declared = set(cfg.get("meta", {}).get("hostile", []))
    return name in declared or (a is not None and (a["key"] in declared or a["key"].startswith("m")))


def ally_idle_errors(cfg: dict) -> list[str]:
    """G11（051：S11 杜克堵着过道口挡了七秒，亚伦全程站在他身后）：敌我有来往的第一下到最后一下之间，
    参战的具名友方（本镜有他的 hit / guard / cast / react）任何 > IDLE_MAX_S 秒都得有事：自己出手、格挡、施法、反应、
    用盾挡下的挨打、挨打后的疼、倒地；真要等写 actor idle = [[t0, t1, "理由"]]。"""
    hits = cfg.get("hit", [])
    fight = sorted(float(h["t"]) for h in hits if _fighter(cfg, h["who"]) or _fighter(cfg, h["target"]))
    bouts, out = [], []
    for t in fight:
        if bouts and t - bouts[-1][1] <= BOUT_GAP_S:
            bouts[-1][1] = t
        else:
            bouts.append([t, t])
    for w0, w1 in bouts:
        out += _idle_in(cfg, hits, w0, w1)
    return out


def _idle_in(cfg: dict, hits: list, w0: float, w1: float) -> list[str]:
    out: list[str] = []
    for a in cfg.get("actor", []):
        lb = a.get("label", a["key"])
        me = (a["key"], lb)
        if not a["key"].startswith("c") or _fighter(cfg, lb):
            continue
        cov = [(float(h["t"]) - 1.0, float(h["t"]) + 1.0 + float(h.get("stuck", 0) or 0)) for h in hits if h["who"] in me]
        cov += [(float(c["t0"]), float(c["t1"])) for c in cfg.get("cast", []) if c.get("who") in me]
        cov += [(float(g["t0"]), float(g["t1"])) for g in cfg.get("guard", []) if g.get("who") in me]
        cov += [(float(r["t_cue"]), float(r["t_ready"])) for r in cfg.get("react", []) if r.get("who") in me]
        if not cov:
            continue            # 没参战的（坐在石头上看的伊根）不查
        own = sorted(c0 for c0, _ in cov)
        for h in hits:
            if h["target"] not in me or h.get("miss"):
                continue
            t = float(h["t"])
            if GEAR_PART.search(str(h.get("part", ""))):
                cov.append((t - 1.0, t + 1.0))                       # 用盾 / 兵器挡下
            elif DOWN_RESULT.search(str(h.get("result", ""))):
                cov.append((t, next((c for c in own if c > t), w1)))  # 倒在地上，到他再动手为止
            else:
                cov.append((t, t + float((h.get("hurt") or [HURT_MIN_S])[0])))
        cov += [(float(i[0]), float(i[1])) for i in a.get("idle", [])]
        lo = max(w0, float(a.get("enter", w0)))
        hi = min(w1, float(a.get("gone", w1)))
        t = lo
        while t < hi - 1e-6:
            inside = [c1 for c0, c1 in cov if c0 <= t < c1]
            if inside:
                t = max(inside)
                continue
            e = min([c0 for c0, _ in cov if c0 > t] + [hi])
            if e - t > IDLE_MAX_S:
                out.append("「%s」%.1f–%.1fs 在打斗里干站（没有出手 / 格挡 / 施法 / 挨打 / 倒地）——写出他在干什么（[[hit]] / [[guard]] / [[cast]]），"
                           "真要等写 actor idle = [[t0, t1, \"理由\"]]、理由在动作里看得见（051 G11）" % (lb, t, e))
            t = e
    return out


def hurt_errors(cfg: dict) -> list[str]:
    """G12（051：S11 杜克左肩挨一镐「闷哼一声，没退」，接着照样一下下挡满——伤得假）：打在具名人物身上（不是盾 / 甲 / 兵器）
    要写 hurt = [秒数 ≥ HURT_MIN_S, "怎么疼"]；疼的这段不出手，盾臂挨了打不照常挡满（result 写出撑不住 / 垂下），腿挨了打不跑。"""
    out: list[str] = []
    hits = cfg.get("hit", [])
    for h in hits:
        tgt = _actor(cfg, h["target"])
        part = str(h.get("part", ""))
        if tgt is None or h.get("miss") or not tgt["key"].startswith("c") or not part or GEAR_PART.search(part):
            continue
        t = float(h["t"])
        me = (tgt["key"], tgt.get("label", tgt["key"]))
        hurt = h.get("hurt")
        if not hurt or float(hurt[0]) < HURT_MIN_S or not str(hurt[1]).strip():
            out.append("[[hit]] %gs %s 的%s挨了这一下，没写疼——hurt = [≥ %g 秒, \"怎么疼\"]：疼多久、哪只手 / 哪条腿不好使（051 G12）"
                       % (t, me[1], part, HURT_MIN_S))
            continue
        t1 = t + float(hurt[0])
        for g in hits:
            if g["who"] in me and t + REFLEX_S < float(g["t"]) < t1 and not g.get("miss"):
                out.append("[[hit]] %s %gs 挨打、疼到 %gs，%gs 却出手了——疼的这段先缓、再动手（051 G12）" % (me[1], t, t1, float(g["t"])))
        side = next((k for k, rx in ARM_PART.items() if rx.search(part)), None)
        if side and tgt.get("shield") == side:
            for g in hits:
                if g["target"] in me and t < float(g["t"]) < t1 and "盾" in str(g.get("part", "")) \
                        and not WEAK_RESULT.search(str(g.get("result", ""))):
                    out.append("[[hit]] %s 的%s %gs 刚挨了一下（疼到 %gs），%gs 却照常用那只手的盾挡满——result 写出撑不住 / 垂下，或挪到疼过以后（051 G12）"
                               % (me[1], part, t, t1, float(g["t"])))
        if LEG_PART.search(part):
            for k in range(int((t1 - t) / 0.25)):
                a0, a1 = t + k * 0.25, t + (k + 1) * 0.25
                v = math.dist(_pos_at(tgt["path"], a0), _pos_at(tgt["path"], a1)) / 0.25
                if v > RUN_MPS:
                    out.append("[[hit]] %s 的%s %gs 挨了一下，%.1fs 前后却在跑（%.1f m/s）——腿疼的这段只能踉跄 / 挪（051 G12）"
                               % (me[1], part, t, a0, v))
                    break
    return out


def _seg_dist(p: tuple, a: tuple, b: tuple) -> float:
    ax, ay = b[0] - a[0], b[1] - a[1]
    L2 = ax * ax + ay * ay
    u = 0.0 if L2 < 1e-9 else max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L2))
    return math.dist(p, (a[0] + u * ax, a[1] + u * ay))


def cast_order_errors(cfg: dict) -> list[str]:
    """G8 施法因果（049：S21 加瑞克在光亮起之前就起跑；扔出去的光从杜克身上穿过去、还早于放光；S20 / S21 加瑞克够得着却干站）：
    ① with＝光 的命中不早于同一人最近一段 [[cast]] 放完，弹道离己方各人中心 ≥ LIGHT_CLEAR_M；
    ② 起光前 AGGRO_LEAD_S 秒里敌人朝施法者逼近（走了 ≥ AGGRO_MOVE_M、近了 ≥ 0.5 m）＝ 先扑后有光；
    ③ [meta] hostile 的持械者在 REACH_M 内停 > ARMED_IDLE_S 秒、这段没有他的 [[hit]]。"""
    out: list[str] = []
    acts = cfg.get("actor", [])
    casts = cfg.get("cast", [])
    hits = cfg.get("hit", [])
    declared = set(cfg.get("meta", {}).get("hostile", []))
    calm = set(cfg.get("meta", {}).get("calm", []))
    cuts = [float(c["t"]) for c in cfg.get("camera", []) if c.get("cut")]

    def armed(a: dict) -> bool:
        return a["key"] in declared or a.get("label") in declared

    def hostile(a: dict) -> bool:
        return (armed(a) or a["key"].startswith("m")) and a["key"] not in calm and a.get("label") not in calm

    for h in hits:
        if h.get("with") != "光" or h.get("miss"):
            continue
        who, tgt = _actor(cfg, h["who"]), _actor(cfg, h["target"])
        if who is None or tgt is None:
            continue
        t = float(h["t"])
        mine = [c for c in casts if _actor(cfg, c["who"]) is who and float(c["t0"]) <= t + 1e-6]
        if not mine:
            out.append("[[hit]] %gs %s 的光打中 %s，之前没有他的 [[cast]]——光扔出去之前得先起光" % (t, h["who"], h["target"]))
        else:
            c = max(mine, key=lambda c: float(c["t0"]))
            if t < float(c["t1"]) - 0.05:
                out.append("[[hit]] %gs 光打中 %s，早于 [[cast]] %g–%gs 放完——光还没扔出去就打中了"
                           % (t, h["target"], float(c["t0"]), float(c["t1"])))
        P, T = _pos_at(who["path"], t), _pos_at(tgt["path"], t)
        for a in acts:
            if a is who or a is tgt or hostile(a) or int(a.get("count", 1)) > 1 or h.get("over") in (a["key"], a.get("label")):
                continue
            dd = _seg_dist(_pos_at(a["path"], t), P, T)
            if dd < LIGHT_CLEAR_M:
                out.append("[[hit]] %gs %s 扔向 %s 的光从 %s 身上穿过去（离弹道 %.2f m < %g m）——他先让开，或动作写明从他肩外飞过并让路点让开"
                           % (t, h["who"], h["target"], a.get("label", a["key"]), dd, LIGHT_CLEAR_M))
    for c in casts:
        cw = _actor(cfg, c["who"])
        if cw is None:
            continue
        a1 = float(c["t0"])
        a0 = a1 - AGGRO_LEAD_S
        if a0 < 0:
            continue
        for m in acts:
            if m is cw or not hostile(m):
                continue
            lim = SPEED_MAX.get(m["key"][0], 8.0)       # 这段里跳了位置（镜内硬切剪掉了时间）就不算逼近
            seg = [(float(q[0]), float(q[1]), float(q[2])) for q in m["path"]]
            if any(t0_ < a1 and t1_ > a0 and t1_ > t0_ and math.hypot(x1_ - x0_, y1_ - y0_) / (t1_ - t0_) > lim
                   for (t0_, x0_, y0_), (t1_, x1_, y1_) in zip(seg, seg[1:])):
                continue
            p0, p1 = _pos_at(m["path"], a0), _pos_at(m["path"], a1)
            closer = math.dist(p0, _pos_at(cw["path"], a0)) - math.dist(p1, _pos_at(cw["path"], a1))
            # 冲的是不是施法者：路点写了面朝就看面朝指着谁；没写就看起光那一刻离谁最近
            # （S16 矿工冲的是堵在巷口的杜克，亚伦只是站在他身后同一条线上）
            faced = [q for q in m["path"] if len(q) == 5 and a0 - 1e-6 <= float(q[0]) <= a1 + 0.6]
            if faced:
                aims = any(math.dist((float(q[3]), float(q[4])), _pos_at(cw["path"], float(q[0]))) < 0.8 for q in faced)
            else:
                near = min((v for v in acts if v["key"].startswith("c") and not hostile(v)),
                           key=lambda v: math.dist(p1, _pos_at(v["path"], a1)), default=None)
                aims = near is cw
            if math.dist(p0, p1) >= AGGRO_MOVE_M and closer >= 0.5 and aims:
                out.append("%s 在起光（%gs）之前 %gs 里就朝 %s 逼近了 %.1f m——谁出光扑谁：先有光、再扑（把起跑挪到起光之后）"
                           % (m.get("label", m["key"]), a1, AGGRO_LEAD_S, c["who"], closer))
    step = 0.1
    end = max((float(p[0]) for a in acts for p in a["path"]), default=0.0)
    for m in (a for a in acts if armed(a) and hostile(a)):
        mine_hits = [float(h["t"]) for h in hits if _actor(cfg, h["who"]) is m]
        stuck = [(float(h["t"]), float(h["t"]) + float(h["stuck"])) for h in hits if _actor(cfg, h["who"]) is m and h.get("stuck")]
        for v in acts:
            if v is m or hostile(v) or not v["key"].startswith("c"):
                continue
            since, t = None, 0.0
            while t <= end + 1e-6:
                if any(abs(t - x) < step / 2 for x in cuts):
                    since = None
                if _here(m, t) and _here(v, t) and math.dist(_pos_at(m["path"], t), _pos_at(v["path"], t)) <= REACH_M:
                    since = t if since is None else since
                    last = max([since] + [x for x in mine_hits if since - 1e-6 <= x <= t + 1e-6]
                               + [min(t, b) for a_, b in stuck if a_ <= t + 1e-6])
                    if t - last > ARMED_IDLE_S + 1e-6:
                        out.append("%s 在 %s 够得着的距离（≤ %g m）里从 %.1fs 起 %.1f s 没出手——在砍就把每一下写成 [[hit]]，不砍就退开"
                                   % (m.get("label", m["key"]), v.get("label", v["key"]), REACH_M, last, t - last))
                        break
                else:
                    since = None
                t += step
    return out


def prop_pos(p: dict, t: float) -> tuple[float, float] | None:
    """会动的道具 t 时刻在哪；gone 之后不在场返回 None。"""
    if p.get("gone") is not None and t > float(p["gone"]) + 1e-6:
        return None
    return _pos_at(p["path"], t)


MOVING_OBJ = re.compile(r"拽走|拖走|拖进|拖回|甩落|甩在|脱手|滑出|落地|被抢|扔|踢飞|捡起|拎起|抱回|滚落|掉在|砸落|被拽|被拖")
FIXED_FEATURE = re.compile(r"洞|墙|壁|门|窗|柱|架|台|垛|桌|井|坑|树|木撑|栅|栏|篱")


def prop_errors(cfg: dict, secs: float) -> list[str]:
    """G9：[[prop]] 的格式（路点 [t, x, y]、时刻不减且落在 0–secs、gone 在镜内）；
    静态 [[object]] 的 label 写着它会被拖 / 扔 / 落地（049：S11「锤落地处…被拖走」是一块不动的方块）即 raise。"""
    out: list[str] = []
    for o in cfg.get("object", []):
        if MOVING_OBJ.search(o["label"]) and not FIXED_FEATURE.search(o["label"].split("（")[0]):
            out.append("[[object]]「%s」写的是会动的东西——改成 [[prop]]，出场 / 被拖走 / 落地都写进 path 与 gone（049 G9）" % o["label"])
    for p in cfg.get("prop", []):
        lb = p.get("label") or p.get("key")
        if not lb or not p.get("path"):
            out.append("[[prop]] 要有 label 与 path：%s" % p)
            continue
        ts = [float(q[0]) for q in p["path"]]
        if ts != sorted(ts) or ts[0] < 0 or ts[-1] > secs + 1e-6 or any(len(q) != 3 for q in p["path"]):
            out.append("[[prop]] %s 的路点须是 [t, x, y]、时刻不减且落在 0–%gs" % (lb, secs))
        if p.get("gone") is not None and not 0 <= float(p["gone"]) <= secs:
            out.append("[[prop]] %s 的 gone=%s 不在 0–%gs" % (lb, p["gone"], secs))
    return out


def _shield_side(a: dict, t: float) -> str | None:
    side = a.get("shield")
    if not side:
        return None
    w = a.get("shield_t")
    return side if not w or float(w[0]) - 1e-6 <= t <= float(w[1]) + 1e-6 else None


def _bearing(frm: dict, to: tuple[float, float], t: float) -> float | None:
    """to 相对 frm 面朝的来向（°，负＝左、正＝右；平面图 y 朝南）。"""
    P = _pos_at(frm["path"], t)
    f = _face_at(frm["path"], t)
    if f is None:
        q = _pos_at(frm["path"], t - 0.3)
        f = (P[0] - q[0], P[1] - q[1]) if math.dist(P, q) > 0.05 else None
    v = (to[0] - P[0], to[1] - P[1])
    if f is None or math.hypot(*v) < 1e-6:
        return None
    return math.degrees(math.atan2(f[0] * v[1] - f[1] * v[0], f[0] * v[0] + f[1] * v[1]))


def shield_errors(cfg: dict) -> list[str]:
    """持盾挨打要有理由（follow-up 046：S10 一镐从正前方啄在杜克左肩上——左臂的盾正该挡在那儿）。"""
    out: list[str] = []
    for h in cfg.get("hit", []):
        who, tgt = _actor(cfg, h["who"]), _actor(cfg, h["target"])
        if who is None or tgt is None:
            continue
        t = float(h["t"])
        if h.get("with") == "盾" and not _shield_side(who, t):
            out.append("[[hit]] %gs %s 用盾出手，但 [[actor]] 没写 shield（左 / 右）" % (t, h["who"]))
        side = _shield_side(tgt, t)
        if "盾" in h.get("part", "") and not side:
            out.append("[[hit]] %gs 打在 %s 的盾上，但 [[actor]] 没写 shield（左 / 右）" % (t, h["target"]))
        if not side or "盾" in h.get("part", "") or h.get("miss") or h.get("open"):
            continue
        b = _bearing(tgt, _pos_at(who["path"], t), t)
        if b is None:
            continue
        lo, hi = SHIELD_ARC if side == "左" else (-SHIELD_ARC[1], -SHIELD_ARC[0])
        if lo <= b <= hi:
            out.append("[[hit]] %gs %s 从%s（%+.0f°）打在 %s 的%s上——%s手的盾正护着这一侧：改成打在盾上、从没盾的一侧或背后来，"
                       "或写 open = 盾为什么没挡住" % (t, h["who"], "正前" if abs(b) < 30 else ("左侧" if b < 0 else "右前"), b,
                                                   h["target"], h.get("part") or "身上", side))
    for g in cfg.get("guard", []):
        who = _actor(cfg, g["who"])
        if g.get("shield") and who is not None and not _shield_side(who, float(g["t0"])):
            out.append("[[guard]] %s 举盾挡，但 [[actor]] 没写 shield（左 / 右）" % g["who"])
    return out


def _gaze_xy(cfg: dict, g: dict, t: float) -> tuple[float, float] | None:
    at = g.get("at")
    if isinstance(at, str):
        a = _actor(cfg, at)
        return _pos_at(a["path"], t) if a else None
    return (float(at[0]), float(at[1])) if at else None


def _gaze_times(g: dict) -> list[float]:
    """窗内取三个时刻（四分点），避开窗两端——窗常贴着跳切，端点上的路点插值是半路上的假位置。"""
    t0, t1 = float(g["t0"]), float(g["t1"])
    return [t0 + (t1 - t0) * k for k in (0.25, 0.5, 0.75)]


def gaze_errors(cfg: dict) -> list[str]:
    """视线目标（follow-up 047）：看的方向对不对，关键看点有没有入过画。"""
    out: list[str] = []
    cams = cfg.get("camera", [])
    t_end = max((float(c["t"]) for c in cams), default=0.0)
    for g in cfg.get("gaze", []):
        who = _actor(cfg, g["who"])
        lb = g.get("label") or str(g.get("at"))
        if who is None or _gaze_xy(cfg, g, float(g["t0"])) is None:
            out.append("[[gaze]] who=%s / at=%s 解析不到唯一的 actor 或坐标" % (g["who"], g.get("at")))
            continue
        for t in _gaze_times(g):
            b = _bearing(who, _gaze_xy(cfg, g, t), t)
            if b is not None and abs(b) > GAZE_FACE_DEG:
                out.append("[[gaze]] %gs %s 看「%s」，面朝却偏了 %+.0f°（> %g°）——路点写成 [t,x,y,fx,fy]、fx,fy 填目标点"
                           % (t, g["who"], lb, b, GAZE_FACE_DEG))
                break
        if g.get("key") and cams:
            ts = [i * 0.25 for i in range(int(t_end / 0.25) + 1)]
            if not any(in_view(cfg, t, _gaze_xy(cfg, g, t)) for t in ts):
                out.append("[[gaze]] 「%s」是这一拍的看点（key），整镜没有一个时刻在画里——加一段让它入画（侧面同框 / 过肩 / 反打插入）" % lb)
    return out


def gaze_notes(cfg: dict, t0: float, t1: float) -> list[str]:
    """[t0, t1] 这段机位下，被看的东西在画里的哪一侧、还是在画外（哪一侧）——生成器写进 `走位:`，模型才不会自己把它摆进画面、
    再让人转身去看它（shot09 数烛光「头朝外」）。"""
    out: list[str] = []
    for g in cfg.get("gaze", []):
        a, b = max(t0, float(g["t0"])), min(t1, float(g["t1"]))
        if b - a < 0.3:
            continue
        t = (a + b) / 2
        xy = _gaze_xy(cfg, g, t)
        who = _actor(cfg, g["who"])
        if xy is None or who is None:
            continue
        c = cam_at(cfg.get("camera", []), t)
        cx, cy = c["xy"]
        ax = math.atan2(c["look"][1] - cy, c["look"][0] - cx)
        off = (math.atan2(xy[1] - cy, xy[0] - cx) - ax + math.pi) % (2 * math.pi) - math.pi
        rx, ry = -math.sin(ax), math.cos(ax)
        side = "右" if (xy[0] - cx) * rx + (xy[1] - cy) * ry > 0 else "左"
        name, lb = who.get("label", who["key"]), g.get("label") or str(g.get("at"))
        if in_view(cfg, t, xy):
            out.append("%s看的%s在画%s" % (name, lb, "中" if abs(off) < math.atan(SENSOR_W / 2 / c["lens"]) / 3 else side))
        elif abs(off) > math.pi / 2:
            out.append("%s看的%s在镜头身后（画外），视线从镜头%s侧越过，画里看不见%s，不回头、不转身去找它" % (name, lb, side, lb))
        else:
            out.append("%s看的%s在画%s边之外，画里看不见%s，视线朝画%s边缘外" % (name, lb, side, lb, side))
    return out


def cast_errors(cfg: dict) -> list[str]:
    """打斗里施法要站在盾后面（follow-up 046）：威胁进了 CAST_THREAT_M，中间得有持盾的人、或 [[guard]] 正护着他。"""
    out: list[str] = []
    acts = cfg.get("actor", [])
    declared = set(cfg.get("meta", {}).get("hostile", []))
    calm = set(cfg.get("meta", {}).get("calm", []))
    for c in cfg.get("cast", []):
        who = _actor(cfg, c["who"])
        if who is None:
            out.append("[[cast]] who=%s 不是唯一的 actor key / label" % c["who"])
            continue
        if c.get("exposed"):
            continue
        threats = [m for m in acts if m is not who and m["key"] not in calm and m.get("label") not in calm
                   and (m["key"].startswith("m") or m["key"] in declared or m.get("label") in declared)]
        t = float(c["t0"])
        while t <= float(c["t1"]) + 1e-6:
            W = _pos_at(who["path"], t)
            for m in threats:
                M = _pos_at(m["path"], t)
                d = math.dist(M, W) - (1.0 if int(m.get("count", 1)) > 1 else 0.0)
                if d > CAST_THREAT_M:
                    continue
                walls = [b for b in acts if b is not who and _shield_side(b, t)]
                guarded = any(float(g["t0"]) <= t <= float(g["t1"]) and g["protects"] in (who["key"], who.get("label"))
                              and g["threat"] in (m["key"], m.get("label")) for g in cfg.get("guard", []))
                if not guarded and not any(_between(_pos_at(b["path"], t), M, W, 0.8) for b in walls):
                    out.append("[[cast]] %.1fs %s 施法时 %s 离他 %.1f m、中间没有持盾的人——站到盾后面施法，或写 exposed = 理由"
                               % (t, c["who"], m.get("label", m["key"]), max(d, 0.0)))
                    break
            else:
                t += 0.1
                continue
            break
    return out


def in_view(cfg: dict, t: float, xy: tuple[float, float]) -> bool:
    """t 时刻地面上的点 xy 在不在机位的水平视野里（与 screen_view 同一套算法）。"""
    c = cam_at(cfg.get("camera", []), t)
    cx, cy = c["xy"]
    ax = math.atan2(c["look"][1] - cy, c["look"][0] - cx)
    d = max(math.hypot(xy[0] - cx, xy[1] - cy), 0.05)
    off = (math.atan2(xy[1] - cy, xy[0] - cx) - ax + math.pi) % (2 * math.pi) - math.pi
    return abs(off) <= math.atan(SENSOR_W / 2 / c["lens"]) + math.atan(0.22 / d)


def ghost_errors(cfg: dict, secs: float) -> list[str]:
    """镜内跳切防分身（follow-up 042：shot04 出片里两个亚伦、两个杜克）：切点把人放到新位置，而切之前那一段里
    新位置早就在画里、本人却还不在画里——模型照文字「他们站在治安官面前」先在那儿画一对，再画走进来的那一对。"""
    out: list[str] = []
    cuts = sorted(float(c["t"]) for c in cfg.get("camera", []) if c.get("cut"))
    for tc in jump_cuts(cfg):
        t0 = max([0.0] + [c for c in cuts if c < tc - 1e-6])
        for a in cfg.get("actor", []):
            old, new = _pos_at(a["path"], tc - 0.15), _pos_at(a["path"], tc + 0.05)
            if math.dist(old, new) < 3.0:
                continue
            lone, t = 0.0, t0
            while t < tc - 1e-6:
                if in_view(cfg, t, new) and not in_view(cfg, t, _pos_at(a["path"], t)):
                    lone += 0.25
                t += 0.25
            if lone >= GHOST_S:
                out.append("%gs 跳切：%s 的新位置 %s 在切之前 %.1f s 就在画里、他本人却不在画里——模型会先在新位置画一个他（分身）；"
                           "让他从头就在画里，或让新位置切前不入画，或拆成两镜" % (tc, a.get("label", a["key"]), _xy(new), lone))
    return out


def guard_errors(cfg: dict) -> list[str]:
    """护人格挡：挡的人必须在被护者与威胁之间、面朝威胁。只写「冲上来挡」而不写几何，模型会让盾朝着被护的人。"""
    out: list[str] = []
    for g in cfg.get("guard", []):
        who, pro, thr = (_actor(cfg, g[k]) for k in ("who", "protects", "threat"))
        for k, a in (("who", who), ("protects", pro), ("threat", thr)):
            if a is None:
                out.append("[[guard]] %s = %s 不是唯一的 actor key / label" % (k, g[k]))
        if None in (who, pro, thr):
            continue
        t0, t1 = float(g["t0"]), float(g["t1"])
        t = t0
        while t <= t1 + 1e-6:
            P, Q, T = (_pos_at(a["path"], t) for a in (who, pro, thr))
            qt, qp, pt = (T[0] - Q[0], T[1] - Q[1]), (P[0] - Q[0], P[1] - Q[1]), (T[0] - P[0], T[1] - P[1])
            why = []
            if math.hypot(*pt) >= math.hypot(*qt):
                why.append("离威胁不比被护者近")
            elif math.hypot(*qp) > 1e-6:
                ang = math.degrees(abs(math.atan2(qt[0] * qp[1] - qt[1] * qp[0], qt[0] * qp[0] + qt[1] * qp[1])))
                if ang > GUARD_ANGLE:
                    why.append("偏出「被护者→威胁」连线 %.0f° > %g°" % (ang, GUARD_ANGLE))
            f = _face_at(who["path"], t)
            if f is None:
                why.append("没写面朝")
            elif math.hypot(*pt) > 1e-6:
                off = math.degrees(abs(math.atan2(f[0] * pt[1] - f[1] * pt[0], f[0] * pt[0] + f[1] * pt[1])))
                if off > GUARD_FACE:
                    why.append("面朝偏离威胁 %.0f° > %g°（%s）" % (off, GUARD_FACE, "盾面没朝威胁" if g.get("shield") else "没面对威胁"))
            if why:
                out.append("[[guard]] t=%.2fs %s 护 %s 挡 %s：%s" % (
                    t, who.get("label", who["key"]), pro.get("label", pro["key"]), thr.get("label", thr["key"]), "；".join(why)))
                break
            t += 0.25
    return out


def _dashed(d: ImageDraw.ImageDraw, a, b, col, w: int = 2, dash: int = 12) -> None:
    n = max(1, int(math.dist(a, b) / dash))
    for k in range(0, n, 2):
        t0, t1 = k / n, min(1.0, (k + 1) / n)
        d.line([a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0,
                a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1], fill=col, width=w)


def _arrow(d: ImageDraw.ImageDraw, a, b, col, w: int = 4, head: int = 16) -> None:
    d.line([a, b], fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (-1, 1):
        d.line([b, (b[0] - head * math.cos(ang + s * 0.45), b[1] - head * math.sin(ang + s * 0.45))],
               fill=col, width=w)


def render(shot_dir: Path) -> tuple[Path | None, list[str], list[str]]:
    cfg = load(shot_dir)
    drama = _drama_root(shot_dir)
    bg = cfg["meta"]["scene"]
    bg_dir = _bg_dir(drama / "2_世界观人设" / "scenes", bg)
    owner, _ptr = planschema.resolve(str(bg_dir))
    site = planschema.load(owner)
    title, secs, jb, chars = _shot_md(shot_dir)
    bad, warn = gate(cfg, planschema.with_derived(site), secs, chars, jb)
    if bad:
        return None, bad, warn
    need_pv, pv_why = previz_decision(cfg, secs)

    Wm, Hm = site["meta"]["size_m"]
    vx0, vy0, vx1, vy1 = cfg["meta"].get("view", [0, 0, Wm, Hm])
    PX = min(MAP_MAX[0] / (vx1 - vx0), MAP_MAX[1] / (vy1 - vy0))
    map_w, map_h = int((vx1 - vx0) * PX), int((vy1 - vy0) * PX)
    pad, top, panel_w, gap = 90, 210, 660, 40
    W = pad + map_w + gap + panel_w + pad
    H = top + max(map_h, 1180) + 170
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    def P(x: float, y: float) -> tuple[float, float]:
        return pad + (x - vx0) * PX, top + (y - vy0) * PX

    build_floorplan.draw_site(d, site, P, PX, W, H, inline=True)
    # 构件派生体块（门塔之类）：平面图上没有、却会挡人挡镜头——虚线框 + 名字，不编圆牌号
    for b in (x for b0 in site.get("block", []) for x in planschema.derived(b0)):
        cs = [P(*q) for q in planschema.corners(b)]
        for k in range(4):
            _dashed(d, cs[k], cs[(k + 1) % 4], INK, 3, 10)
        cx, cy = P(*b["xy"])
        halo(d, (cx, cy), "%s（构件派生 h%g m）" % (b["name"], b["h_m"]), font(15), INK)
    for box in ((0, 0, W, top), (0, top + map_h, W, H), (0, top, pad, top + map_h),
                (pad + map_w, top, W, top + map_h)):
        d.rectangle(box, fill=PAPER)
    d.rectangle([pad, top, pad + map_w, top + map_h], outline=INK, width=3)

    f_s, f_m, f_b = font(17), font(20), font(22, bold=True)
    # 本镜物件
    for o in cfg.get("object", []):
        b = {"xy": o["xy"], "size": o.get("size", [0.6, 0.6]), "rot": o.get("rot", 0)}
        cs = [P(*p) for p in planschema.corners(b)]
        d.polygon(cs, fill=OBJ_COL + (90,), outline=OBJ_COL)
        cx, cy = P(*o["xy"])
        halo(d, (cx, cy - 16), "◆" + o["label"], f_s, OBJ_COL)
    for pr in cfg.get("prop", []):          # 会动的道具：虚线路线 + 起点方块 + 终点圈
        pts = [P(float(q[1]), float(q[2])) for q in pr["path"]]
        for a_, b_ in zip(pts, pts[1:]):
            d.line([a_, b_], fill=OBJ_COL, width=3)
        x0_, y0_ = pts[0]
        d.rectangle([x0_ - 6, y0_ - 6, x0_ + 6, y0_ + 6], fill=OBJ_COL)
        x1_, y1_ = pts[-1]
        d.ellipse([x1_ - 7, y1_ - 7, x1_ + 7, y1_ + 7], outline=OBJ_COL, width=3)
        halo(d, (x0_, y0_ - 16), "◇%s（%g–%gs）" % (pr["label"], float(pr["path"][0][0]), float(pr.get("gone", pr["path"][-1][0]))),
             f_s, OBJ_COL)
    # 人物走位
    colors = actor_colors(cfg)
    for i, a in enumerate(cfg.get("actor", [])):
        col = colors[a["key"]]
        pts = [P(float(p[1]), float(p[2])) for p in a["path"]]
        n = int(a.get("count", 1))
        if len(pts) > 1:
            for j in range(len(pts) - 1):
                if pts[j] == pts[j + 1]:
                    continue
                # 切点瞬间换位置（Δt ≤ 0.2s）是镜内硬切的时间压缩，不是真的走过去——画虚线
                if float(a["path"][j + 1][0]) - float(a["path"][j][0]) <= 0.2:
                    _dashed(d, pts[j], pts[j + 1], col + (120,))
                else:
                    _arrow(d, pts[j], pts[j + 1], col + (220,), 4, 14)
        for j, (p, raw) in enumerate(zip(pts, a["path"])):
            r = 9 if j == 0 else 6
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col, outline=(255, 255, 255))
            if n > 1 and j == 0:
                for k in range(1, min(n, 6)):
                    ang = k * 2 * math.pi / min(n, 6)
                    q = (p[0] + 18 * math.cos(ang), p[1] + 18 * math.sin(ang))
                    d.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=col + (170,))
            if len(raw) == 5:
                fx, fy = P(float(raw[3]), float(raw[4]))
                ang = math.atan2(fy - p[1], fx - p[0])
                d.line([p, (p[0] + 26 * math.cos(ang), p[1] + 26 * math.sin(ang))], fill=col, width=3)
            halo(d, (p[0] + 14, p[1] + 14), "%gs" % float(raw[0]), f_s, col, anchor="lm")
        name = a.get("label", a["key"]) + (" ×%d" % n if n > 1 else "")
        halo(d, (pts[0][0], pts[0][1] - 22), name, f_m, col)
    # 机位
    cams = cfg["camera"]
    cp = [P(*c["xy"]) for c in cams]
    for j in range(len(cp) - 1):
        if cp[j] == cp[j + 1]:
            continue
        if cams[j + 1].get("cut"):          # 硬切：机位不是走过去的
            _dashed(d, cp[j], cp[j + 1], ACCENT + (110,))
            mx, my = (cp[j][0] + cp[j + 1][0]) / 2, (cp[j][1] + cp[j + 1][1]) / 2
            halo(d, (mx, my), "切", f_s, ACCENT)
        else:
            _arrow(d, cp[j], cp[j + 1], ACCENT, 6, 20)
    for j, (c, p) in enumerate(zip(cams, cp)):
        lens = float(c.get("lens", 35))
        hf = 2 * math.atan(SENSOR_W / 2 / lens)
        lk = P(*c.get("look", c["xy"]))
        ang = math.atan2(lk[1] - p[1], lk[0] - p[0])
        # 扇形只示意朝向与视角宽窄：长度封顶，否则广角镜的扇形会盖住半张图
        L = max(50.0, min(math.dist(p, lk), 130.0))
        wedge = [p, (p[0] + L * math.cos(ang - hf / 2), p[1] + L * math.sin(ang - hf / 2)),
                 (p[0] + L * math.cos(ang + hf / 2), p[1] + L * math.sin(ang + hf / 2))]
        d.polygon(wedge, fill=ACCENT + (16,), outline=ACCENT + (90,))
        d.line([p, (p[0] + L * math.cos(ang), p[1] + L * math.sin(ang))], fill=ACCENT + (150,), width=2)
    for j, (c, p) in enumerate(zip(cams, cp)):
        # 同一位置的路点（静止段）只标一次，免得圆牌叠圆牌
        if j and cp[j - 1] == p:
            continue
        badge(d, p[0], p[1], j + 1, ACCENT)
        halo(d, (p[0] + 20, p[1] - 20), "%gs" % float(c["t"]), f_m, ACCENT, anchor="lm")

    # 右栏
    x0, y = pad + map_w + gap, top
    d.rectangle([x0, y, x0 + panel_w, H - 150], fill=PANEL_BG)
    x, y = x0 + 22, y + 18

    def line(txt: str, f=f_s, col=INK, dy: int = 26) -> None:
        nonlocal y
        for chunk in _wrap(d, txt, f, panel_w - 44):
            d.text((x, y), chunk, font=f, fill=col)
            y += dy

    line("机位（红）", f_b, ACCENT, 32)
    for j, c in enumerate(cams, 1):
        line("%d  %gs  %s  h%gm  %gmm  %s" % (j, float(c["t"]), _xy(c["xy"]), float(c.get("h", 1.6)),
                                               float(c.get("lens", 35)), c.get("tag", "")), f_s, INK)
        if c.get("note"):
            line("    " + c["note"], f_s, SOFT)
    y += 10
    line("人物走位", f_b, INK, 32)
    for i, a in enumerate(cfg.get("actor", [])):
        col = colors[a["key"]]
        line("● %s（%s）%s" % (a.get("label", a["key"]), a["key"],
                               " ×%d" % int(a.get("count", 1)) if int(a.get("count", 1)) > 1 else ""), f_m, col, 28)
        line("    " + " → ".join("%gs%s" % (float(p[0]), _xy(p[1:3])) for p in a["path"]), f_s, SOFT)
        if a.get("note"):
            line("    " + a["note"], f_s, SOFT)
    if cfg.get("guard"):
        y += 10
        line("护人格挡（机检：挡的人在中间、面朝威胁）", f_b, ACCENT, 32)
        for g in cfg["guard"]:
            line("▲ %g–%gs  %s 挡在 %s 与 %s 之间，面朝%s%s" % (
                float(g["t0"]), float(g["t1"]), g["who"], g["protects"], g["threat"], g["threat"],
                "，盾面朝它" if g.get("shield") else ""), f_s, INK)
    if cfg.get("react"):
        y += 10
        line("反应窗（机检：动作时长够、做完之前没被碰上）", f_b, ACCENT, 32)
        for r in cfg["react"]:
            line("◷ %s %g→%gs：%s（至少 %.1f s）" % (r["who"], float(r["t_cue"]), float(r["t_ready"]), "＋".join(r["does"]),
                                                    sum(REACT_S.get(w, 0) for w in r["does"])), f_s, INK)
    if cfg.get("hit"):
        y += 10
        line("命中（机检：够得着、面朝目标；previz 查贴到身上）", f_b, ACCENT, 32)
        for h in cfg["hit"]:
            line("✦ %gs %s 用%s%s %s%s%s" % (float(h["t"]), h["who"], h["with"], "（落空）" if h.get("miss") else "打", h["target"],
                                            ("的" + h["part"]) if h.get("part") else "", ("：" + h["result"]) if h.get("result") else ""), f_s, INK)
    if cfg.get("object") or cfg.get("prop"):
        y += 10
        line("本镜物件（橙）", f_b, OBJ_COL, 32)
        for o in cfg.get("object", []):
            line("◆ %s %s%s" % (o["label"], _xy(o["xy"]), ("  " + o["key"]) if o.get("key") else ""), f_s, INK)
        for pr in cfg.get("prop", []):
            line("◇ %s %s → %s%s" % (pr["label"], _xy(pr["path"][0][1:3]), _xy(pr["path"][-1][1:3]),
                                     ("  %gs 起不在场" % float(pr["gone"])) if pr.get("gone") is not None else ""), f_s, INK)
    if cfg.get("beat"):
        y += 10
        line("时间轴", f_b, INK, 32)
        for b in cfg["beat"]:
            line("%g–%gs  %s" % (float(b["t0"]), float(b["t1"]), b["text"]), f_s, INK)
    y += 10
    line("previz：%s" % ("要" if need_pv else "免"), f_b, ACCENT if need_pv else INK, 32)
    line("    " + pv_why, f_s, SOFT)
    if warn:
        y += 10
        line("⚠ 提示", f_b, (176, 60, 44), 32)
        for w_ in warn:
            line("· " + w_, f_s, (176, 60, 44))

    north_arrow(d, pad + map_w - 50, top + 44)
    scale_bar(d, pad, H - 118, PX, meters=_nice(vx1 - vx0))
    title_block(d, pad, 40, "%s《%s》 · 镜头平面图（overhead）" % (shot_dir.name, title),
                "%gs ｜ %s（%s）｜ 景别档 %s" % (secs, site["meta"].get("name_zh", bg), bg, jb or "—"),
                cfg["meta"].get("note", ""))
    halo(d, (pad, H - 72), "红＝机位（实线箭头＝运镜、虚线「切」＝硬切；圆牌号＝路点顺序、旁边是秒数，扇形＝朝向与视角）"
         "　彩色＝人物走位（点旁数字＝秒，短线＝面朝）　橙＝本镜物件", f_s, MUTED, anchor="lm")
    footer(d, pad, H - 40, "由 tools/shot_overhead.py 从 planning/overhead.toml 生成 · 位置的唯一出处，shot blend 从同一份读"
           " · 底图＝%s 场地平面图 blocks.toml@%s" % (bg, planschema.sha(owner)))
    out = shot_dir / "planning" / ("%s_overhead.png" % shot_dir.name)
    img.save(out)
    render_ref(shot_dir, cfg, planschema.with_derived(site), secs)
    return out, bad, warn


def ref_path(shot_dir: Path) -> Path:
    return shot_dir / "planning" / ("%s_overhead_ref.png" % shot_dir.name)


def _short(label: str) -> str:
    return re.split(r"[（(]", label, maxsplit=1)[0].strip()


def _ref_view(cfg: dict) -> tuple[float, float, float, float]:
    """裁到本镜真正用到的范围（机位 + 人 + 物件），外扩后撑成 16:9。"""
    pts = [tuple(c["xy"]) for c in cfg["camera"]]
    pts += [(float(p[1]), float(p[2])) for a in cfg.get("actor", []) for p in a["path"]]
    pts += [tuple(o["xy"]) for o in cfg.get("object", [])]
    pts += [(float(q[1]), float(q[2])) for pr in cfg.get("prop", []) for q in pr["path"]]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    m = max(3.0, 0.18 * max(x1 - x0, y1 - y0))
    x0, x1, y0, y1 = x0 - m, x1 + m, y0 - m, y1 + m
    w, h = max(x1 - x0, 10.0), max(y1 - y0, 10.0 * 9 / 16)
    aspect = REF_SIZE[0] / REF_SIZE[1]
    if w / h < aspect:
        w = h * aspect
    else:
        h = w / aspect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2


def render_ref(shot_dir: Path, cfg: dict, site: dict, secs: float) -> Path:
    """Seedance 版 overhead：视频模型读的是「图形」，所以只留图形——
    地块（灰，深浅＝高低）、人（彩色圆 + 朝向尖角 + 路线箭头 + 到达秒数）、机位（红色机身 + 视野扇形 + 段号与秒数）。
    无标题 / 侧栏 / 坐标 / 图例：图例在 prompt 的 `参考用法:` 里用文字交代，不画在图上。
    标签先收齐再统一避让摆放——字压字的图，模型与人都读不出谁是谁。"""
    W, H = REF_SIZE
    vx0, vy0, vx1, vy1 = _ref_view(cfg)
    PX = W / (vx1 - vx0)
    img = Image.new("RGB", (W, H), GRASS_REF)
    d = ImageDraw.Draw(img, "RGBA")
    taken: list[tuple[float, float, float, float]] = []      # 已被图形 / 标签占住的矩形
    labels: list[tuple[tuple[float, float], str, object, tuple, float]] = []   # (锚点, 文字, 字体, 颜色, 最小离开距离)

    def P(x: float, y: float) -> tuple[float, float]:
        return (x - vx0) * PX, (y - vy0) * PX

    def occupy(p, r: float) -> None:
        taken.append((p[0] - r, p[1] - r, p[0] + r, p[1] + r))

    for r in site.get("ridge", []):
        d.polygon([P(*q) for q in r["poly"]], fill=ROCK_REF)
    for w_ in site.get("water", []):
        d.line([P(*q) for q in w_["path"]], fill=WATER_REF, width=int(w_.get("width_m", 6) * PX), joint="curve")
    for r in site.get("road", []):
        d.line([P(*q) for q in r["path"]], fill=ROAD_REF, width=int(r.get("width_m", 4) * PX), joint="curve")
    blocks = site.get("block", [])
    for b in blocks:
        h_m = float(b.get("h_m", 0) or 0)
        # 高块里面的东西（屋内木桌）俯视看不见，画出来只会和屋名叠在一起
        if any(o is not b and float(o.get("h_m", 0) or 0) > h_m and _inside(o, *b["xy"]) for o in blocks):
            continue
        cs = [P(*q) for q in planschema.corners(b)]
        if max(q[0] for q in cs) < 0 or min(q[0] for q in cs) > W or max(q[1] for q in cs) < 0 or min(q[1] for q in cs) > H:
            continue
        g = 222 - int(min(h_m, 15.0) / 15.0 * 90)
        if h_m <= 0:
            d.polygon(cs, fill=(g, g, g - 6, 90), outline=(150, 150, 140))
        else:
            d.polygon(cs, fill=(g, g, g - 6), outline=INK, width=3)
        # 块名放在块的可见部分中间
        xs = sorted(min(max(q[0], 0), W) for q in cs)
        ys = sorted(min(max(q[1], 0), H) for q in cs)
        labels.append((((xs[0] + xs[-1]) / 2, (ys[0] + ys[-1]) / 2), _short(b["name"]), font(26), (70, 70, 64), 0))

    for o in cfg.get("object", []):
        bb = {"xy": o["xy"], "size": o.get("size", [0.6, 0.6]), "rot": o.get("rot", 0)}
        d.polygon([P(*q) for q in planschema.corners(bb)], fill=OBJ_COL + (150,), outline=OBJ_COL, width=3)
        labels.append((P(*o["xy"]), _short(o["label"]), font(24), OBJ_COL, 26))
    for pr in cfg.get("prop", []):
        pts = [P(float(q[1]), float(q[2])) for q in pr["path"]]
        for a_, b_ in zip(pts, pts[1:]):
            d.line([a_, b_], fill=OBJ_COL, width=4)
        d.rectangle([pts[0][0] - 9, pts[0][1] - 9, pts[0][0] + 9, pts[0][1] + 9], fill=OBJ_COL)
        labels.append((pts[0], _short(pr["label"]), font(24), OBJ_COL, 26))

    # 机位：按硬切分段，每段一个号；段的结束时刻 ＝ 下一段开始或镜尾
    cams = cfg["camera"]
    segs: list[list[dict]] = [[]]
    for i, c in enumerate(cams):
        if i and c.get("cut"):
            segs.append([])
        segs[-1].append(c)
    ends = [float(segs[k + 1][0]["t"]) for k in range(len(segs) - 1)] + [secs]
    for k, seg in enumerate(segs, 1):
        pts = [P(*c["xy"]) for c in seg]
        for c, p in zip(seg, pts):
            lk = P(*c.get("look", c["xy"]))
            ang = math.atan2(lk[1] - p[1], lk[0] - p[0])
            hf = 2 * math.atan(SENSOR_W / 2 / float(c.get("lens", 35)))
            L = max(160.0, min(math.dist(p, lk), 420.0))
            d.polygon([p, (p[0] + L * math.cos(ang - hf / 2), p[1] + L * math.sin(ang - hf / 2)),
                       (p[0] + L * math.cos(ang + hf / 2), p[1] + L * math.sin(ang + hf / 2))],
                      fill=ACCENT + (34,), outline=ACCENT + (170,))
        for a_, b_ in zip(pts, pts[1:]):
            if math.dist(a_, b_) > 4:
                _arrow(d, a_, b_, ACCENT, 7, 22)
        moving = any(math.dist(pts[0], q) > 4 for q in pts)
        for c, p in zip(seg, pts):
            lk = P(*c.get("look", c["xy"]))
            _camera_glyph(d, p, math.atan2(lk[1] - p[1], lk[0] - p[0]))
            occupy(p, 28)
            if moving:
                labels.append((p, "%gs 离地%gm" % (float(c["t"]), float(c.get("h", 1.6))), font(24), ACCENT, 32))
        hs = [float(c.get("h", 1.6)) for c in seg]
        hs = [h for i, h in enumerate(hs) if not i or h != hs[i - 1]]
        labels.append((pts[0], "机位%d  %g–%gs  离地%sm" % (k, float(seg[0]["t"]), ends[k - 1], "→".join("%g" % h for h in hs)),
                       font(28, bold=True), ACCENT, 40))

    # 人
    colors = actor_colors(cfg)
    for i, a in enumerate(cfg.get("actor", [])):
        col = colors[a["key"]]
        raw = a["path"]
        pts = [P(float(q[1]), float(q[2])) for q in raw]
        for j in range(len(pts) - 1):
            if math.dist(pts[j], pts[j + 1]) > 4:
                if float(raw[j + 1][0]) - float(raw[j][0]) <= 0.2:
                    _dashed(d, pts[j], pts[j + 1], col + (160,), 4)
                else:
                    _arrow(d, pts[j], pts[j + 1], col + (235,), 6, 20)
        # 同一位置连续的路点合成一个「a–bs」
        groups: list[list[int]] = []
        for j, p in enumerate(pts):
            if groups and math.dist(pts[groups[-1][-1]], p) <= 4:
                groups[-1].append(j)
            else:
                groups.append([j])
        for g in groups:
            p = pts[g[0]]
            face = next((raw[j] for j in reversed(g) if len(raw[j]) == 5), None)
            if face is not None:
                fx, fy = P(float(face[3]), float(face[4]))
                ang = math.atan2(fy - p[1], fx - p[0])
            elif g[-1] + 1 < len(pts):
                q = pts[g[-1] + 1]
                ang = math.atan2(q[1] - p[1], q[0] - p[0])
            elif g[0] > 0:
                q = pts[g[0] - 1]
                ang = math.atan2(p[1] - q[1], p[0] - q[0])
            else:
                ang = None
            _person_glyph(d, p, ang, col, big=(g is groups[0] or g is groups[-1]))
            occupy(p, 30)
            t0, t1 = float(raw[g[0]][0]), float(raw[g[-1]][0])
            labels.append((p, ("%gs" % t0) if t0 == t1 else ("%g–%gs" % (t0, t1)), font(24), col, 30))
        n = int(a.get("count", 1))
        labels.insert(0, (pts[0], _short(a.get("label", a["key"])) + (" ×%d" % n if n > 1 else ""),
                          font(30, bold=True), col, 34))

    for anchor, txt, f, col, gap in labels:
        _place(d, taken, anchor, txt, f, col, gap, W, H)
    north_arrow(d, W - 70, 40, 60)
    scale_bar(d, 40, H - 60, PX, meters=_nice(vx1 - vx0))
    out = ref_path(shot_dir)
    img.save(out)
    return out


def _place(d: ImageDraw.ImageDraw, taken: list, anchor, txt: str, f, col, gap: float, W: int, H: int) -> None:
    """在锚点周围 8 个方位里挑第一个不压别人的位置写字；都压就放离得最少的那个。"""
    w, h = d.textlength(txt, font=f), f.size * 1.25
    best, best_hit = None, None
    for rad in (gap, gap + 30, gap + 70):
        for k in (6, 2, 0, 4, 7, 5, 1, 3):          # 上、下、右、左，再四个斜角
            ang = k * math.pi / 4
            cx = anchor[0] + math.cos(ang) * (rad + (w / 2 if k in (0, 4, 1, 3, 5, 7) else 0))
            cy = anchor[1] + math.sin(ang) * (rad + h / 2)
            cx, cy = min(max(cx, w / 2 + 6), W - w / 2 - 6), min(max(cy, h / 2 + 4), H - h / 2 - 4)
            box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            hit = sum(max(0, min(box[2], t[2]) - max(box[0], t[0])) * max(0, min(box[3], t[3]) - max(box[1], t[1]))
                      for t in taken)
            if best_hit is None or hit < best_hit:
                best, best_hit = (cx, cy, box), hit
            if hit == 0:
                break
        if best_hit == 0:
            break
    cx, cy, box = best
    taken.append(box)
    halo(d, (cx, cy), txt, f, col)


def _camera_glyph(d: ImageDraw.ImageDraw, p, ang: float) -> None:
    """俯视的摄影机：机身方块 + 朝拍摄方向的镜头梯形。"""
    ca, sa = math.cos(ang), math.sin(ang)

    def R(dx: float, dy: float) -> tuple[float, float]:
        return p[0] + dx * ca - dy * sa, p[1] + dx * sa + dy * ca
    d.polygon([R(-26, -17), R(8, -17), R(8, 17), R(-26, 17)], fill=ACCENT, outline=(255, 255, 255), width=3)
    d.polygon([R(8, -8), R(26, -15), R(26, 15), R(8, 8)], fill=ACCENT, outline=(255, 255, 255), width=3)


def _person_glyph(d: ImageDraw.ImageDraw, p, ang: float | None, col, big: bool) -> None:
    """人：实心圆 + 朝面向伸出的尖角（没有朝向信息就只画圆）。"""
    r = 20 if big else 13
    if ang is not None:
        ca, sa = math.cos(ang), math.sin(ang)
        tip = (p[0] + (r + 20) * ca, p[1] + (r + 20) * sa)
        l = (p[0] + r * 0.9 * math.cos(ang + 0.75), p[1] + r * 0.9 * math.sin(ang + 0.75))
        rr = (p[0] + r * 0.9 * math.cos(ang - 0.75), p[1] + r * 0.9 * math.sin(ang - 0.75))
        d.polygon([l, tip, rr], fill=col, outline=(255, 255, 255))
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col, outline=(255, 255, 255), width=3)


def _xy(p) -> str:
    return "(%g,%g)" % (float(p[0]), float(p[1]))


def _nice(span: float) -> int:
    for m in (1, 2, 5, 10, 20, 50, 100, 200):
        if m >= span / 6:
            return m
    return 500


def _wrap(d: ImageDraw.ImageDraw, txt: str, f, width: int) -> list[str]:
    out, cur = [], ""
    for ch in txt:
        if d.textlength(cur + ch, font=f) > width:
            out.append(cur)
            cur = "    " + ch
        else:
            cur += ch
    return out + [cur]


def run_all(ep_dir: Path, check_only: bool) -> int:
    shots = sorted(p for p in (ep_dir / "shots").iterdir() if p.is_dir())
    rows, nbad = [], 0
    for sd in shots:
        pv = "—"
        try:
            cfg = load(sd)
            if check_only:
                drama = _drama_root(sd)
                owner, _ = planschema.resolve(str(_bg_dir(drama / "2_世界观人设" / "scenes", cfg["meta"]["scene"])))
                title, secs, jb, chars = _shot_md(sd)
                bad, warn = gate(cfg, planschema.with_derived(planschema.load(owner)), secs, chars, jb)
                out = None
            else:
                out, bad, warn = render(sd)
                secs = _shot_md(sd)[1]
            need, why = previz_decision(cfg, secs)
            pv = ("**要**：" if need else "免：") + why
        except Bad as e:
            bad, warn, out = [str(e)], [], None
        nbad += len(bad)
        for b in bad:
            print("  ✗ %s: %s" % (sd.name, b))
        for w_ in warn:
            print("  ⚠ %s: %s" % (sd.name, w_))
        rows.append((sd.name, out, bad, warn, pv))
    if not check_only:
        md = ["# %s 镜头平面图（overhead）索引" % ep_dir.name, "",
              "> 生成物：`python tools/shot_overhead.py --all %s`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。"
              % ep_dir.relative_to(REPO).as_posix(),
              "> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**",
              "> 每镜两张：`_overhead.png` 给人审，`_overhead_ref.png` 给 Seedance。**previz 免** 的镜不做 shot blend，"
              "`_ref` 图直接当运动与几何参考上传；**要** 的镜照旧渲 previz MP4（判据见 `tools/shot_overhead.py` `previz_triggers`）。", "",
              "| 镜 | 状态 | 审阅图 | Seedance 图 | previz |", "|---|---|---|---|---|"]
        for name, out, bad, warn, pv in rows:
            st = "❌ %d" % len(bad) if bad else ("⚠ %d" % len(warn) if warn else "✅")
            ref = ref_path(ep_dir / "shots" / name)
            md.append("| %s | %s | %s | %s | %s |" % (
                name, st, "[%s](shots/%s/planning/%s)" % (out.name, name, out.name) if out else "—",
                "[%s](shots/%s/planning/%s)" % (ref.name, name, ref.name) if out else "—", pv))
        (ep_dir / "overheads.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("%d 镜 · blocker %d · warning %d · previz 要 %d" % (
        len(rows), nbad, sum(len(r[3]) for r in rows), sum(1 for r in rows if r[4].startswith("**要"))))
    return 1 if nbad else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="镜头平面图（overhead）")
    ap.add_argument("target", type=Path, help="shot 目录；--all 时是 ep 目录")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true", help="只跑闸门，不画图")
    a = ap.parse_args()
    target = a.target.resolve()
    if a.all:
        return run_all(target, a.check)
    try:
        out, bad, warn = render(target)
    except Bad as e:
        print("  ✗ " + str(e))
        return 1
    for b in bad:
        print("  ✗ " + b)
    for w_ in warn:
        print("  ⚠ " + w_)
    if out:
        print("  → " + str(out.relative_to(REPO)))
        print("  → " + str(ref_path(target).relative_to(REPO)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
