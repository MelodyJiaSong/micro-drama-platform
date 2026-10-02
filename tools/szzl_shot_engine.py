# -*- coding: utf-8 -*-
"""《圣光刚好够用》(shengji_zhilu) 分镜 + prompt 引擎（阶段 5/6 合一）。

每集一个薄数据文件 `tools/gen_shots_szzl_epNN.py`（只放本集的 SHOTS 表），版式、闸门、回读校验住在这里一份。

**单一出处**（rule 4i ①）——引擎不抄任何内容，一律在构建时从源头读：
  · 台词            ← `4_剧本/episodes/epNN/script.md`（`tools/script_tools.py` 解析；镜号 ＝ 剧本镜号）
  · 角色锁定串      ← 各人物卡 `角色识别标签` / `一句话锁定` 行
  · 场景锁定串      ← 各 bg 主体卡 `一句话锁定` 行；plate 路由键按盘上目录名解析
  · 物件锁定串      ← 各物件卡 `一句话锁定` 行
  · voice_id        ← `casting.md`
  · 渲染串 / 负向基线 / 条件负向组 ← `style_guide.md` §1 / §5

构建闸门（不合格直接终止，分镜生成不出来——ai_video.md 16.7 ③「审计左移进生成器」）：
  ① 镜号与时长逐镜等于剧本；台词全部来自剧本（时间窗念白已由 script_tools 逐窗核过）
  ② 相邻镜切口（`tools/shot_seam.py`，K31）③ 共用串不点名光源（`tools/prompt_light.py`，K32）
  ④ 镜内自洽（`tools/shot_logic.py`，K33）⑤ 版本红线（`tools/wow_version_gate.py`，F6）
  ⑥ prompt ≤ 5000 字、零 hex、`参考:` 只用裸 `=>@`、红级 IP 名零出现、黄级专名不进叙事字段（concept C3）
  ⑦ 参考行（rule 23）：每镜有一份运动与几何参考——**previz MP4 只给复杂镜**，简单镜直接挂 Seedance 版镜头平面图
     （`planning/shotNN_overhead_ref.png`；要不要 previz 由 `shot_overhead.previz_decision` 从 overhead.toml 判，2026-09-25）——
     与至少一个场景主体；入画的人都有锁定串、不入画的人不挂；路由键在盘上有目录
  ⑧ `动作:` 时间轴铺满镜长；有 `分镜:` 的镜，段数与时间轴自洽
  · 剧本的 `- 场景展示:` 行（新地方先给景，follow-up 011）原样并进 `镜头:`，数据文件里不另写
写盘后 `verify()` 再从产物回读一遍（CLAUDE.md：闸门从最终产物回读，不校验中间变量）。
"""
from __future__ import annotations

import dataclasses
import functools
import argparse
import statistics
import io
import json
import os
import math
import re
import tomllib
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import check_stage2  # noqa: E402
import equipment_lib  # noqa: E402
import prompt_light  # noqa: E402
import prompt_compact  # noqa: E402
import shot_overhead  # noqa: E402
import script_tools  # noqa: E402
import skills_lib  # noqa: E402
import shot_logic  # noqa: E402
import shot_seam  # noqa: E402
import wow_version_gate  # noqa: E402
from previz import seedance_ref  # noqa: E402
from previz.planschema import BODY_HITS, HIT_OBJ, PREVIZ_ENGINE, PREVIZ_STAMP, STILLS_STAMP, hit_part_obj, render_inputs  # noqa: E402
import beat_logic  # noqa: E402
import seedance_kit  # noqa: E402
import scene_review  # noqa: E402
import dialogue_review  # noqa: E402
import goal_ledger  # noqa: E402
import facts_registry  # noqa: E402

DRAMA = REPO / "ai_videos" / "shengji_zhilu"
A = DRAMA / "2_世界观人设"
CHARS, PROPS, SCENES = A / "characters", A / "props", A / "scenes"
EQUIP = A / equipment_lib.ROOT_NAME       # 装备（rule 4m）：镜表里写 e{N} 键，锁定串 / 句柄 / 正面图 / 空槽声明都从装备库取
STYLE_GUIDE, CASTING = A / "style_guide.md", A / "casting.md"
FENCE = "`" * 3

PROMPT_MAX = 5000
PREVIZ_RES = (1280, 720)    # Seedance 参考视频下限 409600 像素（ai_video.md rule 24）
PREVIZ_FPS = 24
# previz 色块 proxy：颜色取 build_previz.py 的 COLORS 名；身高按卡（狗头人一米二）
PROXY: dict[str, tuple[str, float]] = {
    "c1_Aaron": ("蓝", 1.75), "c2_Duke": ("绿", 1.72), "m1_Kobold": ("橙", 1.2), "m4_Defias_Bandit": ("红", 1.75),
    "c18_Garrick_Padfoot": ("深灰", 1.85), "m7_Wolf": ("紫", 0.7), "m8_Northshire_Guard": ("青", 1.85),
}
PROXY_OTHERS = ("紫", "青", "黄", "粉", "白")


def _proxy_of(ov: dict) -> dict[str, tuple[str, float]]:
    """本镜每个 actor 的色块与身高：表里没有的人从 PROXY_OTHERS 里挑本镜没被占的色（shot05 伊根与狼同为紫，分不清）。
    平面图 [meta] proxy = { 卡键 = "色" } 只给这一镜改色（057 E3：人偶色与同镜施法的色相带错开）。"""
    acts = ov.get("actor", [])
    over = ov.get("meta", {}).get("proxy", {})
    base = {k: ((over[k], v[1]) if k in over else v) for k, v in PROXY.items()}
    taken = {base[a["key"]][0] for a in acts if a["key"] in base}
    others = iter([c for c in PROXY_OTHERS if c not in taken])
    return {a["key"] + "|" + a.get("label", ""): base.get(a["key"]) or (next(others, "白"), 1.75) for a in acts}
QUADRUPED = {"m7_Wolf"}     # previz 用四足代理，PROXY 的身高读作肩高
DUB_WPS = 2.5               # 配音时长目标按自然语速估；念不念得完由 script_tools 的 ≤3 词/秒闸门管；慢嗓角色见 dub_wps()
SPEAK_SAMPLES = 5           # 049：说话人看不看得见脸，在台词窗里取这么多个点逐点量（不只量中点）
TINY_FRAC = 0.2             # 人占画高低于它（远景里只有一点大）：看不清嘴，画外配音时他在画里也不算穿帮
# 049 之前定稿、本轮没动过台词与走位的镜：仍只量窗中点（规则不回溯；只减不增——动到哪一镜就从这里删掉）
SPEAK_WINDOW_LEGACY: frozenset[str] = frozenset({"S06", "S19"})   # S02 059 重写，退出
RATIO = "16:9"              # concept G9 ⑤

# 剧本说话人 → (人物卡目录 | None, casting.md 里的名字)
SPEAKERS: dict[str, tuple[str | None, str]] = {
    "Aaron": ("c1_Aaron", "Aaron"),
    "Duke": ("c2_Duke", "Duke"),
    "McBride": ("c7_Marshal_McBride", "Marshal McBride"),
    "Willem": ("c13_Deputy_Willem", "Deputy Willem"),
    "Sammuel": ("c14_Brother_Sammuel", "Brother Sammuel"),
    "Eagan": ("c15_Eagan_Peltskinner", "Eagan Peltskinner"),
    "Milly": ("c16_Milly_Osworth", "Milly Osworth"),
    "Neals": ("c17_Brother_Neals", "Brother Neals"),
    "Garrick": ("c18_Garrick_Padfoot", "Garrick Padfoot"),
    "Kobold": ("m1_Kobold", "Kobold"),
    "Kobold Worker": ("m1_Kobold", "Kobold"),
    "Kobold Laborer": ("m1_Kobold", "Kobold"),
    "Llane Beshere": (None, "Llane Beshere"),
    "Guard": ("m8_Northshire_Guard", "Northshire Guard"),
}
# 叙事字段里点名的生物 → 必须挂的卡（follow-up 032：狼没有卡，Seedance 只拿到几个形容词，画成了家狗）。
# 物种判别位与负向都在卡里；不挂卡就等于把长相交给模型去猜。
CREATURES: dict[str, re.Pattern[str]] = {
    "m7_Wolf": re.compile(r"(?<!被)狼(?!皮|肉|牙|排|人|咬过)"),   # 「被狼咬过的脚」是回指上一镜，画面里没有狼
}
# 正常台词要有听的人：画里除说话人外还得有别人，或者注明对着画外的谁（follow-up 032：一个人对着空气说 Hi）
_TO_OFFSCREEN = re.compile(r"冲画外|对画外|冲隔壁|对隔壁")
# 有意的背影台词（follow-up 036）：剧本行尾写「背影：理由」——说话人朝向闸门放行，口型指令改成看不见嘴
_BACK_OK = re.compile(r"背影[：:]")
# 背影台词中途切到说话人的脸（059 S21 高潮近景）：行尾再写「Ns 起近景对口型」——N 秒前不对口型、N 秒起对口型
_BACK_SWITCH = re.compile(r"(\d+(?:\.\d+)?)s 起近景对口型")
# 红级（concept C3）：游戏名 / 公司名，任何地方都不许出现
IP_RED: tuple[str, ...] = ("魔兽世界", "魔兽", "暴雪", "Warcraft", "Blizzard", "WoW", "World of Warcraft")
# 黄级：世界内专名，text-only 实测前不进叙事字段（台词 / 角色键 / 参考行除外）
IP_YELLOW: tuple[str, ...] = ("暴风城", "北郡", "艾尔文", "圣骑士", "迪菲亚", "狗头人", "闪金镇", "联盟")
# `场景:` 是场景卡一句话锁定的逐字粘贴（卡里自带地名），不在此列；原词实测见 pending_user #3
NARRATIVE = ("情节", "镜头", "分镜", "镜内状态", "走位", "动作", "光线", "节奏")

_SPAN = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s")
_HEX = re.compile(r"#[0-9a-fA-F]{6}")
_OFFSCREEN = re.compile(r"(?<!冲)(?:画外|隔壁)|信 ·")


# ─────────────────────────── 单一出处的读取器 ───────────────────────────

def _read(p: Path) -> str:
    return io.open(p, encoding="utf-8").read()


def _fence_after(text: str, heading: str) -> str:
    i = text.find(heading)
    if i < 0:
        raise SystemExit("style_guide.md 里找不到「%s」" % heading)
    a = text.index(FENCE + "text\n", i) + len(FENCE + "text\n")
    return "".join(text[a:text.index("\n" + FENCE, a)].split("\n"))


def style_base() -> str:
    return _fence_after(_read(STYLE_GUIDE), "### 全片共用摄影串")


def neg_base() -> str:
    return _fence_after(_read(STYLE_GUIDE), "## 5. 负向锁定")


def neg_group(name: str) -> str:
    """style_guide §5 条件负向组表里某组的内容（行里第一个反引号串）。"""
    for ln in _read(STYLE_GUIDE).split("\n"):
        if ln.startswith("|") and ("**%s**" % name) in ln.split("|")[1]:
            m = re.search(r"`([^`]+)`", ln.split("|")[3])
            if m:
                return m.group(1)
    raise SystemExit("style_guide §5 没有条件负向组「%s」" % name)


def _card(folder: Path, key: str) -> str:
    p = folder / key / (key + ".md")
    if not p.is_file():
        raise SystemExit("卡不存在：%s" % p)
    return _read(p)


def char_lock(key: str) -> str:
    lock = check_stage2._lock_string(_card(CHARS, key))
    if not lock:
        raise SystemExit("%s 卡里没有角色识别标签 / 一句话锁定" % key)
    return lock


def prop_lock(key: str) -> str:
    lock = check_stage2._lock_string(_card(PROPS, key))
    if not lock:
        raise SystemExit("%s 卡里没有一句话锁定" % key)
    return lock


def is_equip(k: str) -> bool:
    return bool(equipment_lib.KEY.match(k))


def _equip_dir(k: str) -> Path:
    d = equipment_lib.find(EQUIP, k)
    if d is None:
        raise SystemExit("装备 %s 没有目录（先跑 tools/gen_equipment.py build）" % k)
    return d


def asset_label(k: str) -> str:
    """镜表里的物件 / 装备 → 句柄名：装备用它的目录名（e5110_白_父亲的旧双手锤），物件就是目录名本身。"""
    return _equip_dir(k).name if is_equip(k) else k


def asset_lock(k: str) -> str:
    if not is_equip(k):
        return prop_lock(k)
    cf = equipment_lib.confusable(EQUIP, k)
    size = equipment_lib.item(EQUIP, k).get("size", "").split("；")[0].strip()   # 尺寸进锁（follow-up 043：长柄双手锤出片成了短锤）
    return equipment_lib.lock(EQUIP, k) + ("，" + size if size else "") + (("；不是" + "、不是".join(cf)) if cf else "")


def carry(k: str, mode: str) -> str:
    """装备的一种拿法（item.toml [carry]，follow-up 042）：生成器写 `本镜状态` 时逐字引用，扛 / 背一律带手或带子。"""
    return equipment_lib.carry(EQUIP, k, mode)


def confusable_negatives(s: "Shot") -> list[str]:
    """本镜装备的易混物进负面词（锤 → 斧子）；本镜真有那样东西（加瑞克的斧）就不压（follow-up 042）。"""
    eq = [k for k in s.props if is_equip(k)]
    nouns = {k: equipment_lib.item(EQUIP, k)["noun"] for k in eq}
    nouns.update({k: k for k in s.props if not is_equip(k)})     # 物件卡也算（049：矿工手里的镐是 p4，锤的易混词「镐」被压进负面词）
    out = []
    for k in eq:
        for w in equipment_lib.confusable(EQUIP, k):
            if not any(w.rstrip("子头")[-1] in n for o, n in nouns.items() if o != k) and w not in out:   # 按中心字比：本镜有斧，「斧子」「战斧」都不压
                out.append(w)
    return out


def worn_clause(ep: str, c: str, shot: str) -> str:
    """有装备表的角色：本镜所在阶段里看得见却空着的槽 → 反向声明（rule 4m ③ / concept C7）；没有装备表的返回空。
    装备表一集内按镜分段时（阶段带 `shots`），按镜号落段——ep01 一集里换六七次装（follow-up 030）。"""
    if not (EQUIP / equipment_lib.LOADOUTS / (c + ".toml")).is_file():
        return ""
    return equipment_lib.wearing(EQUIP, c, ep, shot)[2]


@functools.lru_cache(maxsize=None)     # 场景树一次运行里不变；每次 os.walk 全树占了 --check 大半时间
def _bg_dir(bg: str) -> Path:
    for dirpath, dirs, files in os.walk(SCENES):
        for d in dirs:
            if d.startswith(bg + "_") and (Path(dirpath) / d / (d + ".md")).is_file():
                return Path(dirpath) / d
    raise SystemExit("场景主体 %s 在 %s 下找不到" % (bg, SCENES))


def scene_lock(plate: str) -> str:
    """plate 卡自己有一句话锁定就用它，没有就用所属主体卡的（8f：ep02 后院 bg4-1 写成了 bg4 主街）。"""
    d = _bg_dir(plate.split("-")[0])
    if "-" in plate:
        pf = d / plate_stem(plate) / (plate_stem(plate) + ".md")
        own = check_stage2._lock_string(_read(pf)) if pf.is_file() else None
        if own:
            return own
    lock = check_stage2._lock_string(_read(d / (d.name + ".md")))
    if not lock:
        raise SystemExit("%s 卡里没有一句话锁定" % d.name)
    return lock


def plate_stem(plate: str) -> str:
    """`bg2-1` → 盘上 plate 目录名 `bg2-1_院前_立面石阶`；锚点级主体（无 plate）传 `bg175` → 主体目录名。"""
    bg = plate.split("-")[0]
    d = _bg_dir(bg)
    if "-" not in plate:
        return d.name
    hits = [x.name for x in d.iterdir() if x.is_dir() and x.name.startswith(plate + "_")]
    if len(hits) != 1:
        raise SystemExit("plate %s 在 %s 下找到 %d 个目录" % (plate, d.name, len(hits)))
    return hits[0]


def voice_id(speaker: str) -> str:
    name = SPEAKERS[speaker][1]
    for ln in _read(CASTING).split("\n"):
        if ln.startswith("| **%s**" % name):
            m = re.search(r"`(en-[mfx]-szzl-[a-z0-9]+-\d{2})`", ln)
            if m:
                return m.group(1)
    raise SystemExit("casting.md 里没有 %s 的 voice_id" % name)


# ─────────────────────────── 数据结构 ───────────────────────────

@dataclass(frozen=True)
class Shot:
    key: str                          # 剧本镜号 S01…；shot 编号 ＝ 其数字
    title: str
    plates: tuple[str, ...]           # 场景主体路由键（bg2-1 / bg175）；第一个的主体给 `场景:` 锁定串
    chars: tuple[str, ...]            # 入画角色卡目录（含 m 类）
    state: dict[str, str]             # 角色 → 本镜状态后缀（伤、盾、锤、光环）
    props: tuple[str, ...]            # 入画物件卡目录
    jb: tuple[float, str, float, str]
    jbcam: tuple[str, str]
    emotion: str
    plot: str
    camera: str
    blocking: str
    action: str
    light: str
    rhythm: str
    holy: str = ""                    # 本镜圣光表现的条件分句（空 ＝ 无圣光镜）
    cut: str = ""                     # `分镜:` 行（无镜内切镜留空）
    ledger: str = ""                  # `镜内状态:` 行
    style_extra: str = ""             # 本镜条件渲染分句（时段 / 光源 / 室内外）
    neg: tuple[str, ...] = ()         # 本镜追加负向（条件组名用 `@组名`）
    jbnote: str | None = None
    moods: dict[int, str] = field(default_factory=dict)   # 台词序号(1 起) → 配音情绪 / 语速
    # shot blend 层补的东西（overhead 只管位置）：poses ＝ ((角色键, t, 姿态), …)，heights ＝ {物件 label: 高 m}
    previz: dict = field(default_factory=dict)
    gs: bool = False                  # 绿幕小人偶 previz（follow-up 085）：没有场景、纯色小人偶，只给人物位置与大概动作
    kf: tuple = ()                    # 状态图（follow-up 084）：不用 previz 视频，三张状态图指导视频；每张 {name, at, prompt, refs}
    pv_end: float = 0.0              # 白模参考只覆盖 0–pv_end 秒（0＝整镜）：腾出 30 s 参考视频预算给技能样片（用户 2026-10-01）
    axis_ok: str = ""                # 这一镜开头有意跨轴（和上一镜左右对调）的理由；空 ＝ 不许对调（follow-up 044）
    dub_note: str = ""
    casts: tuple = ()                 # rule 45：本镜的施放（skills_lib.Cast）；施法的样子 / 手势 / 口令 / 样片全从技能卡来，镜表不手写
    hero: tuple = ()                  # 059 G18：高潮镜的关键那一刻 (角色卡目录, 秒)——那一刻要有他的脸部近景

    @property
    def n(self) -> int:
        return int(self.key[1:])


@dataclass(frozen=True)
class Line:
    who: str
    kind: str        # 正常台词 / 内心独白 / 画外
    text: str
    gloss: str
    win: tuple[float, float] | None
    tail: str = ""


def script_scenery(ep: str) -> dict[str, list[tuple[float, float, str]]]:
    """剧本 `- 场景展示:` 行（follow-up 011）——并进 prompt 的 `镜头:`，生成器数据里不再另写一份。"""
    path = DRAMA / "4_剧本" / "episodes" / ep / "script.md"
    shots, _ = script_tools.parse(str(path))
    return {s.key: [(float(a), float(b), txt.strip()) for a, b, txt in script_tools._SCENERY.findall(s.body)]
            for s in shots}


def script_blocks(ep: str) -> dict[str, str]:
    """剧本每镜正文（`备注:` 里的「旧件在用：理由」之类放行条件从这里读）。"""
    shots, _ = script_tools.parse(str(DRAMA / "4_剧本" / "episodes" / ep / "script.md"))
    return {s.key: s.body for s in shots}


def script_lines(ep: str) -> dict[str, tuple[float, list[Line]]]:
    path = DRAMA / "4_剧本" / "episodes" / ep / "script.md"
    shots, _ = script_tools.parse(str(path))
    out: dict[str, tuple[float, list[Line]]] = {}
    for s in shots:
        lines: list[Line] = []
        for (k, who, txt, tail), gloss in zip(s.lines, s.glosses):
            if k not in ("对白", "OS"):
                continue
            w = script_tools._WIN.search(tail)
            # 「冲画外吼」「冲隔壁喊」是人在画里、朝画外喊——照样对口型；只有说话人自己在画外才算画外
            off = bool(_OFFSCREEN.search(tail))
            kind = "画外" if off else ("内心独白" if k == "OS" else "正常台词")
            lines.append(Line(who, kind, txt, gloss,
                              (float(w.group(1)), float(w.group(2))) if w else None, tail))
        out[s.key] = (s.dur, lines)
    return out


# ─────────────────────────── 渲染 ───────────────────────────

# follow-up 047：主角脚下不再有常驻光环（原 C5 ① 出自 w07 §7 一条没核过实机的草稿；用户裁定删除）
SELF_LIGHT = "人物本身不自发光"
NEG_RING = "脚下光圈，脚下光环，贴地光环，地上的光圈"
_FEET_RING = re.compile(r"脚下[^，。；：]{0,8}[环圈]")     # 施法的样子本身在脚下出一圈（k203 符文环）：这一镜不挂 NEG_RING


def previz_needed(ep: str, s: Shot, secs: float) -> tuple[bool, str]:
    """(要不要 previz MP4, 理由)——判据只在 shot_overhead 里定义一份。没有 overhead 直接 raise：每镜都必须先有它。"""
    if s.gs:
        return True, "绿幕小人偶 previz（follow-up 085：纯色小人偶 + 绿幕背景，只给位置与大概动作）"
    if s.kf:
        return False, "状态图（follow-up 084）"
    return shot_overhead.previz_decision(shot_overhead.load(_shot_dir(ep, s)), secs)


def _overhead_site(ov: dict) -> dict:
    """overhead 挂的场地平面图（带构件派生体块）。"""
    from tools.previz import planschema
    owner, _ = planschema.resolve(str(shot_overhead._bg_dir(SCENES, ov["meta"]["scene"])))
    return planschema.with_derived(planschema.load(owner))


def _previz_parts(ep: str, s: Shot, secs: float) -> list[tuple[float, float]]:
    """previz 要切成几段上传（Seedance 单条参考视频 ≤ 15 s）；段界与 build_previz 同一个函数算。"""
    cams = shot_overhead.load(_shot_dir(ep, s)).get("camera", [])
    return seedance_ref.parts(s.pv_end or secs, [float(c["t"]) for c in cams if c.get("cut")])


DOLL_COLOR = {"c1_Aaron": "蓝", "c2_Duke": "绿", "c14_Brother_Sammuel": "黄", "c18_Garrick_Padfoot": "红", "m4_Defias_Bandit": "橙", "m1_Kobold": "粉",
              "m7_Wolf": "紫", "c13_Deputy_Willem": "青", "c16_Milly_Osworth": "白", "c17_Brother_Neals": "棕", "c7_Marshal_McBride": "灰", "m8_Northshire_Guard": "灰"}


def kf_legend(ep: str, s: "Shot") -> str:
    """状态图里小人偶的颜色对照：只是标记，不是服装颜色。"""
    names = _labels(ep, s)
    fb = {"m1_Kobold": "鼠面矿工", "m4_Defias_Bandit": "红面罩暴徒", "m7_Wolf": "狼", "m8_Northshire_Guard": "卫兵"}
    return "绿幕上的小人偶：" + "、".join("%s＝%s" % (DOLL_COLOR.get(c, "灰"), fb.get(c) or names.get(c) or c) for c in s.chars)


def kf_path(ep: str, s: Shot, name: str) -> Path:
    return _shot_dir(ep, s) / "状态图" / ("%s.png" % name)


def _geo_handles(ep: str, s: Shot, need_pv: bool, secs: float) -> list[tuple[str, Path]]:
    sd = _shot_dir(ep, s)
    if s.kf:
        return [("`状态图%d·第%g秒%s=>@`" % (i, k["at"], ("(" + kf_legend(ep, s) + "；只取姿势与站位)") if i == 1 else ""), kf_path(ep, s, k["name"]))
                for i, k in enumerate(s.kf, 1)]
    if not need_pv:
        return [("`shot%02d_overhead_ref.png(镜头平面图·俯视示意，只锁机位与站位，不是画面)=>@`" % s.n, shot_overhead.ref_path(sd))]
    mp4 = sd / "previz" / ("shot%02d_previz.mp4" % s.n)
    segs = _previz_parts(ep, s, secs)
    if len(segs) == 1:
        return [("`shot%02d_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`" % s.n, mp4)]
    return [("`%s(白模动画第%d段·本镜 %g–%gs，不取长相)=>@`" % (seedance_ref.part_path(mp4, i).name, i, a, b_),
             seedance_ref.part_path(mp4, i)) for i, (a, b_) in enumerate(segs, 1)]


def _entity(who: str) -> str:
    """说话人 → 它在 Seedance 资产包里的 entity 名：有卡用卡目录名，无卡（只闻其声）用 casting 名。"""
    card, name = SPEAKERS[who]
    return card or name.replace(" ", "_")


def _char_handle(c: str) -> str:
    voiced = c in {card for card, _ in SPEAKERS.values()}
    return "`%s(Seedance 角色 entity·%s)=>@`" % (c, "长相与声音" if voiced else "长相，不出声")


# ─────────────────────────── 技能（rule 45 · follow-up 053） ───────────────────────────

_SKILLS: dict = {}
SKILL_USAGE = "；技能参考只取手势、光与时长"   # follow-up 065
REF_VIDEO_MAX = 30.0          # Seedance 2.5：全部参考视频合计 ≤ 30 s（previz 分段 + 技能样片）
_MEDIA_SECS: dict[str, float] = {}


def skill_cards() -> dict:
    if not _SKILLS:
        _SKILLS.update(skills_lib.load(DRAMA))
    return _SKILLS


def _labels(ep: str, s: "Shot") -> dict[str, str]:
    sd = _shot_dir(ep, s)
    if not (sd / "planning" / "overhead.toml").is_file():
        return {}
    return {a["key"]: a.get("label", a["key"]) for a in shot_overhead.load(sd).get("actor", [])}


def _bounds(s: "Shot", secs: float) -> list[tuple[float, float]]:
    """施法分句的分段：机位段，再在 `动作:` 手写的时刻处切开——长镜里施法的几拍之间夹着别的事（S21 一斧一挡），
    切开后各拍带自己的时刻、按先后插回去；同一段里的几拍照旧并成一句。"""
    b = [(float(a), float(c)) for a, c in re.findall(r"(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s", s.cut)] if s.cut else []
    pts = sorted({float(m.group(1)) for m in _AT.finditer(s.action)})
    out: list[tuple[float, float]] = []
    for a, c in (b or [(0.0, secs)]):
        cuts = [a] + [t for t in pts if a < t < c] + [c]
        out += list(zip(cuts, cuts[1:]))
    return out


def hard_cuts(cut: str) -> list[float]:
    """`分镜:` 里标了【切】的段首＝硬切时刻（生成器按 Shot.cut 写、闸门从产物的 `分镜:` 回读，同一个函数）。"""
    out: list[float] = []
    for part in re.sub(r"^分镜:\s*", "", cut or "").split("。")[0].split("｜"):
        m = re.match(r"\s*(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s", part)
        if m and "【切】" in part and float(m.group(1)) > 0:
            out.append(float(m.group(1)))
    return out


def cast_chunks(ep: str, s: "Shot", secs: float, short: bool = False) -> list[str]:
    """本镜每次施放按技能卡拼成 `动作:` 的时刻分句——施法的样子只从卡来（rule 45），镜表里不许手写。
    short＝精简稿用卡的短串（8f #17）；分句的个数与先后和全串一一对应。"""
    names = _labels(ep, s)
    out: list[str] = []
    for c in s.casts:
        card = skills_lib.find(skill_cards(), c.key)
        out += skills_lib.chunks(skills_lib.compose(card, c, names, short), _bounds(s, secs))
    return out


def cast_restates(ep: str, s: "Shot") -> list[tuple[float, str]]:
    """跨硬切还在的施法阶段（蓄着的光、光壳、余晖）在新机位段开头重述（w28 ⑦）。"""
    names, cuts = _labels(ep, s), hard_cuts(s.cut)
    return [r for c in s.casts for r in skills_lib.restates(skills_lib.find(skill_cards(), c.key), c, names, cuts)]


HOLY_PACE = "；圣光术蓄光到放光的快慢严格照参考视频的节奏、不得加快，光柱只罩在被救治的那个人身上"


def binding_text(ep: str, s: "Shot") -> str:
    """精简稿【技能】（057 E2）：同一个人、同一道光、落在同一个人身上的几次并成一句，秒段逗号并列；末尾一句管其他人。"""
    names = _labels(ep, s)
    groups: dict[str, list[str]] = {}
    for c in s.casts:
        cl = skills_lib.binding_clause(skills_lib.find(skill_cards(), c.key), c, names)
        if cl:
            head, span = cl.rsplit("，只在", 1)
            groups.setdefault(head, []).append(span.rstrip("秒"))
    if not groups:
        return ""
    tail = skills_lib.BINDING_TAIL
    if any(c.key == "k201" and c.outcome != "空" for c in s.casts):
        tail += HOLY_PACE          # 用户 2026-10-01：圣光术快慢照参考、光柱落在被救治的人身上
    return "；".join("%s，只在%s秒" % (h, "、".join(v)) for h, v in groups.items()) + "；" + tail


def composed_action(ep: str, s: "Shot", secs: float) -> str:
    """`动作:` 成品：镜表手写的动作 + 技能卡拼的施法分句 + 跨切重述（写产物与闸门回读同一个函数）。"""
    return _with_casts(s.action, cast_chunks(ep, s, secs), cast_restates(ep, s))


_AT = re.compile(r"[，；]\s*(\d+(?:\.\d+)?)s(?![–\-\d.])")


SLOT = "〔施法〕"


def _insert_by_time(piece: str, chunk: str, t: float) -> str:
    """施法分句落在段里的〔施法〕占位上（镜表里写在哪、就接在哪，后面的话照常接着写）；没有占位时插在
    第一个比它晚的时刻前面——段内先后不乱。"""
    if SLOT in piece:
        return piece.replace(SLOT, chunk, 1)
    for m in _AT.finditer(piece):
        if float(m.group(1)) > t + 1e-6:
            return piece[:m.start()] + "；" + chunk + "；" + piece[m.start() + 1:].lstrip()
    return piece.rstrip("；") + "；" + chunk


def _with_casts(action: str, extra: list[str], restate: list[tuple[float, str]] | tuple = ()) -> str:
    """施法分句插进它所在的那个机位段、段内按时刻排（052 G14 的密度按段算，不能都堆在最后一段）；
    restate：跨切重述接在新机位段的时间标签后面、不带时刻（不算 G14 的节拍）。"""
    if not extra:
        if SLOT in action:
            raise SystemExit("`动作:` 里写了%s，本镜却没有 casts——占位只给技能卡的施法分句（rule 45）" % SLOT)
        return action
    marks = list(re.finditer(r"(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s\s", action))
    if not marks:
        return "；".join([action.rstrip("；")] + extra)
    cuts = [m.start() for m in marks[1:]] + [len(action)]
    pieces = [action[:cuts[0]]] + [action[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]
    spans = [(float(m.group(1)), float(m.group(2))) for m in marks]
    for ch in sorted(extra, key=lambda c: float(re.match(r"(\d+(?:\.\d+)?)s", c).group(1))):
        t = float(re.match(r"(\d+(?:\.\d+)?)s", ch).group(1))
        k = next((i for i, (a, b) in enumerate(spans) if a - 1e-6 <= t < b - 1e-6), len(spans) - 1)
        pieces[k] = _insert_by_time(pieces[k], ch, t)
    for t, text in restate:
        k = next((i for i, (a, _b) in enumerate(spans) if abs(a - t) < 1e-6), None)
        lab = re.match(r"\s*\d+(?:\.\d+)?[–-]\d+(?:\.\d+)?s\s", pieces[k]) if k is not None else None
        if lab is None:
            raise SystemExit("跨切重述落在 %gs，`动作:` 在那里没有分段——分段在切点断开（w28 ⑦）" % t)
        pieces[k] = pieces[k][:lab.end()] + text + "，" + pieces[k][lab.end():]
    out = "；".join(p.rstrip("；") for p in pieces)
    if SLOT in out:
        raise SystemExit("`动作:` 里的%s比本镜的施法分句多——每个占位对一段施法（rule 45）" % SLOT)
    return out


def cast_poses(ep: str, s: "Shot") -> tuple:
    """技能卡的姿势键 → previz 关键帧。Cascadeur 体（choreo.toml 列了的人）跳过：他们的施法动作写在 choreo 里。"""
    names = _labels(ep, s)
    choreo = _shot_dir(ep, s) / "cascadeur" / "choreo.toml"
    baked: set[str] = set()
    if choreo.is_file():
        import tomllib
        baked = set(tomllib.loads(choreo.read_text(encoding="utf-8")).get("actor", {}))
    manual = [(w, float(t)) for w, t, _ in s.previz.get("poses", ())]
    out: list = []
    last: dict[str, float] = {}
    for c in sorted(s.casts, key=lambda c: c.t):
        who = names.get(c.who, c.who)
        if who in baked:
            continue
        card = skills_lib.find(skill_cards(), c.key)
        # 镜表在这之前给这个人手写了姿势（S08 两手摊开）：不钉回原姿势，从那个姿势直接进手势
        lead = not any(w in (c.who, who) and last.get(who, 0.0) <= t < c.t for w, t in manual)
        out += skills_lib.poses(card, c, who, lead)
        last[who] = skills_lib.end_time(card, c)
    return tuple(out)


def _media_secs(f: Path) -> float:
    if str(f) not in _MEDIA_SECS:
        import subprocess
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                           capture_output=True, text=True)
        _MEDIA_SECS[str(f)] = float(r.stdout.strip() or 0)
    return _MEDIA_SECS[str(f)]


def skill_refs(ep: str, s: "Shot", need_pv: bool, secs: float) -> tuple[list[tuple[str, Path]], str]:
    """用到的技能的样片 / 峰值图（定稿了才有）。参考视频合计超 30 s 时样片放不下，只挂峰值图——写进 Shot context，不静默。"""
    used = sum(b - a for a, b in _previz_parts(ep, s, secs)) if need_pv else 0.0
    out: list[tuple[str, Path]] = []
    notes: list[str] = []
    for key in dict.fromkeys(c.key for c in s.casts):
        card = skills_lib.find(skill_cards(), key)
        callers = tuple(c.who for c in s.casts if c.key == key and c.outcome != "空")
        got_video = False
        for name, f in skills_lib.refs(card, callers):
            if f.suffix.lower() in (".mp4", ".mov"):
                d = _media_secs(f) if f.is_file() else card.sample_window[1] - card.sample_window[0]    # 还没收进来：按 window 预算
                if used + d > REF_VIDEO_MAX:
                    notes.append("%s样片 %gs 放不下（参考视频已用 %gs，上限 %gs），只挂峰值图" % (card.name, d, used, REF_VIDEO_MAX))
                    continue
                used += d
                got_video = True
            elif got_video and f.suffix.lower() == ".png":
                continue            # 挂上了施法片段就不再挂同一技能的峰值图（065：参考行与上传件都少一项）
            out.append((name, f))
    return out, "；".join(notes)


_FX_CHARS = "光火焰烟电冰霜雷"
_FX_DEGREE = ("夸张", "过曝", "刺眼", "满屏", "漫天", "大片", "泛滥", "铺满")


def skill_errors(ep: str, s: "Shot", secs: float, lines: list["Line"]) -> list[str]:
    """rule 45：会不会（学会在前）、等级够不够（装备表的等级段）、时长 / 档位 / 结局合不合卡、口令一字不差。"""
    tag = "shot%02d" % s.n
    out: list[str] = []
    order = sorted(p.name for p in (DRAMA / "4_剧本" / "episodes").iterdir() if p.is_dir())
    legacy = ep in seedance_kit.config(DRAMA).get("legacy_eps", [])
    names = _labels(ep, s)
    for c in s.casts:
        try:
            card = skills_lib.find(skill_cards(), c.key)
            beats = skills_lib.compose(card, c, names)
        except SystemExit as e:
            out.append("%s: %s" % (tag, e))
            continue
        who = names.get(c.who, c.who)
        if c.outcome != "空" and not skills_lib.knows(card, c.who, ep, s.key, order):     # 没学会时试一次、没出来，正是学之前的戏
            out.append("%s: %s 在 %s %s 还不会%s——谁何时学会只写在技能卡 [[learned]]（rule 45）" % (tag, who, ep, s.key, card.name))
        if (EQUIP / equipment_lib.LOADOUTS / (c.who + ".toml")).is_file():
            st = equipment_lib.stage_for(equipment_lib.loadout(EQUIP, c.who), ep, s.key)
            if st.levels and st.levels[1] < card.level:
                out.append("%s: %s 这一段 %d–%d 级，%s 要 %d 级才学得到（1.12，w26）" % (tag, who, st.levels[0], st.levels[1], card.name, card.level))
        end = skills_lib.end_time(card, c)
        if end > secs + 0.05:
            out.append("%s: %s 施放到 %gs，超出镜长 %gs" % (tag, card.name, end, secs))
        if c.outcome in ("成", "挡"):
            body = "".join(b.text for b in beats)
            for n in dict.fromkeys(x.strip() for x in _negatives(s).split("，")):
                head = n[-2:]
                if n.startswith(_FX_DEGREE):          # 「夸张金光」「过曝光柱」只压强度，不否定有没有
                    continue
                if len(n) >= 2 and any(ch in head for ch in _FX_CHARS) and head in body:
                    out.append("%s: 负向词「%s」把%s要出的「%s」也否定了（技能卡 [look]）——这一镜的负向去掉它（rule 45）"
                               % (tag, n, card.name, head))
        call = skills_lib.call_line(card, c.who)
        if call and c.outcome in ("成", "挡"):            # 放出去的那次必须念；被打断 / 没出来的可以念一半或没念
            g_end = beats[1].t if len(beats) > 1 else c.t + 3.0
            said = [l for l in lines if SPEAKERS.get(l.who, (None, ""))[0] == c.who and l.text.strip() == call
                    and (l.win is None or (l.win[0] < g_end + 0.5 and l.win[1] > c.t - 0.5))]
            if not said:
                msg = ("%s: %s 蓄%s时要念口令「%s」（技能卡 [call]，一字不差、落在蓄光那几秒），剧本这一镜没有（rule 45）"
                       % (tag, who, card.name, call))
                if legacy:
                    print("  ⚠ " + msg + "——legacy_eps，只警告")
                else:
                    out.append(msg)
    return out


def skill_forbid_errors(tag: str, s: "Shot", md: str) -> list[str]:
    """技能卡的禁写（审判「脱锤飞出」、冲锋「撞翻」…）出现在产物里即 raise——负面词行不算。"""
    body = "\n".join(ln for ln in md.split("\n") if not ln.startswith(("负面词:", "【不要】")))
    out: list[str] = []
    for key in dict.fromkeys(c.key for c in s.casts):
        card = skills_lib.find(skill_cards(), key)
        out += ["%s: 用到%s，产物里却写了技能卡禁写的「%s」（rule 45）" % (tag, card.name, w) for w in card.forbid if w in body]
    return out


CAST_PLAN_TOL_S = 0.15     # follow-up 065：平面图 [[cast]] 的 t0 与镜表 casts 起手差多少以内算同一次


def cast_plan_errors(ep: str, tag: str, s: "Shot") -> list[str]:
    """平面图 [[cast]]（护人覆盖、弹道、仇恨闸门读它）是手写的第二份施法时刻；技能时长一改它就漂（065 把 S21 的光挪到 14.9s，
    平面图还写着 11.8s）。每条 [[cast]] 的 t0 必须对上同一施法者在镜表 casts 里的一次起手。"""
    sd = _shot_dir(ep, s)
    if not (sd / "planning" / "overhead.toml").is_file():
        return []
    names = _labels(ep, s)
    out: list[str] = []
    for c in shot_overhead.load(sd).get("cast", []):
        starts = [k.t for k in s.casts if c["who"] in (k.who, names.get(k.who, k.who))]
        if not any(abs(float(c["t0"]) - t) <= CAST_PLAN_TOL_S for t in starts):
            out.append("%s: 平面图 [[cast]] %s %gs 起，镜表 casts 里他的起手是 %s——两份施法时刻对不上（follow-up 065）"
                       % (tag, c["who"], float(c["t0"]), "、".join("%gs" % t for t in starts) or "没有"))
    return out


def _handles(ep: str, s: Shot, lines: list[Line], need_pv: bool, secs: float) -> list[str]:
    """角色一律挂 Seedance 资产包 entity（一个 entity 同时锁长相与声音，2026-09-25），只挂入画的人：
    follow-up 046——S07 给隔壁喊一声的杜克挂了「只用声音」的 entity，出片里入画的成了杜克；Seedance 不认这个注明，
    挂了谁、谁就进画。画外台词不进 Seedance，后期按 voice_id 配音（mux_av）。"""
    h = [g for g, _f in _geo_handles(ep, s, need_pv, secs)]
    h += ["`%s=>@`" % name for name, _f in skill_refs(ep, s, need_pv, secs)[0]]
    h += ["`%s(场景主体)=>@`" % plate_stem(p) for p in s.plates]
    h += [_char_handle(c) for c in s.chars]
    h += ["`%s(%s锚点)=>@`" % (asset_label(p), "装备" if is_equip(p) else "物件") for p in s.props]
    return h


def _lines_field(lines: list[Line]) -> str:
    if not lines:
        return "本镜无台词。"
    parts = []
    for l in lines:
        if l.kind == "画外":        # follow-up 046：画外的人此刻不入画、不靠 entity 出声，人声后期按 voice_id 配（Seedance 自带音全去掉）
            parts.append("%s %s（画外·这个人此刻不在画面里，画里无人对口型，人声后期配音）：%s"
                         % ("%g–%gs" % l.win if l.win else "", l.who, l.text))
            continue
        lip = {"正常台词": "口型对说话人", "内心独白": "嘴唇不动"}[l.kind]
        if l.kind == "正常台词" and _BACK_OK.search(l.tail):
            sw = _BACK_SWITCH.search(l.tail)
            lip = ("%ss 前背对镜头、看不见嘴，%ss 起切到说话人的脸、口型对说话人" % (sw.group(1), sw.group(1)) if sw
                   else "背对镜头说，看不见嘴，不对口型")
        at = "%g–%gs" % l.win if l.win else ""
        parts.append("%s %s（%s·%s）：%s" % (at, l.who, l.kind, lip, l.text))
    return "；".join(parts) + "。台词只供口型与配音参考，画面不出现任何文字。"


def card_tier(card: str, tier: str) -> str:
    """群体卡的档位后缀（卡里 `- {档}：`…`` 一行）——shot 的 `本镜状态` 从卡里读，不在生成器里另抄。"""
    m = re.search(r"^- %s：`([^`]+)`" % re.escape(tier), _read(CHARS / card / (card + ".md")), re.M)
    if not m:
        raise SystemExit("%s 卡里没有档位后缀「- %s：`…`」" % (card, tier))
    return m.group(1)


def card_negatives(card: str) -> str:
    """怪物卡 `## 负向` 下除基线外的全部组（`@卡:m7_Wolf`）——负向词只在卡里写一份（rule 4i ①）。"""
    text = _read(CHARS / card / (card + ".md"))
    i = text.find("\n## 负向")
    if i < 0:
        raise SystemExit("%s 卡里没有 `## 负向` 节" % card)
    sec = text[i + 1:]
    j = sec.find("\n## ", 4)
    blocks = re.findall(FENCE + r"text\n(.*?)\n" + FENCE, sec[:j] if j > 0 else sec, re.S)
    if len(blocks) < 2:
        raise SystemExit("%s 的 `## 负向` 节只有基线、没有本卡专属组" % card)
    return "，".join("".join(b.split("\n")).strip("，") for b in blocks[1:])


NEG_SPEAKER = "说话的人背对镜头，对话时只拍到后脑勺"   # follow-up 036


NEG_GHOST = "分身，同一个人在画面里同时出现两次，双胞胎"   # follow-up 042：跳切镜
MUSIC_FADE, MUSIC_END, TAIL_QUIET = 1.5, 0.3, 0.8          # follow-up 044：镜尾前多少秒开始收、多少秒落定；最后一句台词离镜尾至少多少秒
NEG_MUSIC = "音乐在镜尾戛然而止，乐句被切断"
NEG_STIFF = "机器人般僵硬的动作，木偶感，滑步"     # 052：previz 白模人偶的僵硬被照搬进成片


def music_line(secs: float) -> str:
    """每镜的配乐在本镜内收尾（follow-up 044：出片配乐常在镜尾被硬切，还差半个乐句）。"""
    return ("本镜配乐从 0 秒轻轻淡入；%gs 起开始收束，%gs 前落在一个完整的收尾上（落回主音或自然衰减完），"
            "最后 %g 秒只剩环境声；不在乐句中间结束，不在镜尾突然断掉" % (secs - MUSIC_FADE, secs - MUSIC_END, MUSIC_END))


def _feet_ring(s: Shot) -> bool:
    for c in s.casts:
        if c.outcome in ("成", "挡"):
            card = skills_lib.find(skill_cards(), c.key)
            if any(_FEET_RING.search(v) for v in skills_lib.looks(card, c).values()):
                return True
    return False


def _negatives(s: Shot) -> str:
    out = [neg_base()] + ([] if _feet_ring(s) else [NEG_RING]) + [NEG_STIFF] + confusable_negatives(s)
    for n in s.neg:
        if n.startswith("@卡:"):
            out.append(card_negatives(n[3:]))
        else:
            out.append(neg_group(n[1:]) if n.startswith("@") else n)
    return "，".join(out)


def guard_clause(ep: str, s: Shot) -> str:
    """overhead `[[guard]]`（已由 shot_overhead 机检几何）→ `走位:` 里的一句：谁在中间、背对谁、面朝谁、盾面朝谁。"""
    f = _shot_dir(ep, s) / "planning" / "overhead.toml"
    if not f.is_file():
        return ""
    out = []
    for g in shot_overhead.load(_shot_dir(ep, s)).get("guard", []):
        out.append("%g–%gs %s挡在%s与%s之间：背对%s，%s都朝着它%s" % (
            float(g["t0"]), float(g["t1"]), g["who"], g["protects"], g["threat"], g["protects"],
            "身体正面和盾的外凸面" if g.get("shield") else "身体正面", "，盾的背带那面贴着自己" if g.get("shield") else ""))
    return ("；护人格挡：" + "；".join(out)) if out else ""




def hit_clause(ep: str, s: Shot) -> str:
    """overhead `[[hit]]`（已机检够得着、面朝目标）→ prompt 的 `命中:` 行：几秒、谁的什么、落在谁的哪、结果（follow-up 042）。"""
    f = _shot_dir(ep, s) / "planning" / "overhead.toml"
    if not f.is_file():
        return ""
    groups: dict[tuple[str, str], list[float]] = {}      # 同一个人同一件家伙打同一处、同一个结果：时刻并成一条（049：一镐一镐写全之后命中行太长）
    ov = shot_overhead.load(_shot_dir(ep, s))
    for h in sorted(ov.get("hit", []), key=lambda h: float(h["t"])):
        if h.get("miss"):
            what = "%s的%s落空，没碰到%s" % (h["who"], h["with"], h["target"])
        elif h["with"] == "光":
            raise SystemExit("%s：overhead [[hit]] with = \"光\" 已废——审判没有飞行物（技能卡 k202），施法写 Shot.casts（rule 45 · 053）" % s.key)
        elif h["with"] == "投":
            what = "%s扔出去的东西砸在%s%s" % (h["who"], h["target"], ("的" + h["part"] + "上") if h.get("part") else "身上")
        else:
            what = "%s的%s%s在%s%s" % (h["who"], h["with"], "撞" if h["with"] == "盾" else "咬" if h["with"] == "咬" else "顶" if h["with"] == "叉" else "打",
                                          h["target"], ("的" + h["part"] + "上") if h.get("part") else "身上")
        seen = {re.split(r"[（(#·]", lb)[0] for lb in shot_overhead.screen_view(ov, float(h["t"]))}
        if h["who"] not in seen and h["target"] not in seen:     # 059 S21：那一下落在别人的近景之外——只听见，别让模型把它搬进近景
            what = "画外（不在画里，只听见）" + what
        res = h.get("result", "")
        if h.get("hurt"):          # 051 G12：疼多久、怎么疼一处定义在平面图，prompt 照抄
            res = "%s（疼 %g 秒：%s）" % (res, float(h["hurt"][0]), h["hurt"][1]) if res else "疼 %g 秒：%s" % (float(h["hurt"][0]), h["hurt"][1])
        groups.setdefault((what, res), []).append(float(h["t"]))
    return "；".join("%s %s%s" % ("、".join("%gs" % t for t in ts), what, ("——" + r) if r else "") for (what, r), ts in groups.items())


def _friend_safe(ep: str, s: Shot) -> str:
    """G19：并肩打斗的镜，命中行末尾写死「家伙只落在敌人身上」。"""
    ov = shot_overhead.load(_shot_dir(ep, s))
    fr = {a["label"] for a in shot_overhead.friend_actors(ov)}
    if len(fr) > 1 and any(h["who"] in fr and h["target"] not in fr and not h.get("miss") and h.get("with") not in ("光", "投") for h in ov.get("hit", [])):
        return "；锤只落在敌人身上，不碰同伴及其盾"
    return ""


def screen_clause(ep: str, s: Shot, secs: float, lines: list[Line] = ()) -> str:
    """overhead → `走位:` 里一句画面相对的话：每段机位下每个人在画左 / 中 / 右、脸对不对着镜头、朝画面哪边。
    罗盘方向（面朝东）模型不知道在画面里是哪边，会照场景参考图的构图把人摆成背影（follow-up 036 shot04）。"""
    f = _shot_dir(ep, s) / "planning" / "overhead.toml"
    if not f.is_file():
        return ""
    ov = shot_overhead.load(_shot_dir(ep, s))
    cuts = [0.0] + sorted(float(c["t"]) for c in ov.get("camera", []) if c.get("cut")) + [secs]
    segs = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 0.5:
            continue
        order, seen = [], {}
        talk = {}                  # 8f 站位 2：说话人按他自己的台词窗（与本段的交叠）取样
        for l in lines:
            card = SPEAKERS.get(l.who, (None, ""))[0]
            if l.kind == "正常台词" and card and l.win and min(b, l.win[1]) - max(a, l.win[0]) > 0.05:
                talk.setdefault(card, []).append((max(a, l.win[0]) + min(b, l.win[1])) / 2)
        base_t = [a + min(0.1, (b - a) / 4), (a + b) / 2, b - min(0.1, (b - a) / 4)]     # 8f 运镜4：只量段中会漏掉摇走之前在画的人
        for t in sorted(set(base_t + [x for xs in talk.values() for x in xs])):
            for lb, v in shot_overhead.screen_view(ov, t).items():
                if not v["key"].startswith("c"):
                    continue
                look = "" if not v["face"] else (v["turn"] if v["face"] in ("正脸", "背影") else v["face"] + v["turn"])
                if lb not in seen:
                    order.append(lb)
                    seen[lb] = [v["side"], []]
                if look and (not seen[lb][1] or (seen[lb][1][-1] == "背对镜头") != (look == "背对镜头")):   # 只记背对 ↔ 露脸的转变
                    seen[lb][1].append(look)
        who = ["%s在%s%s" % (lb, seen[lb][0], ("、" + seen[lb][1][0]) if len(seen[lb][1]) == 1 else
                              ("、先" + "、再".join(seen[lb][1][:-1]) + "、后" + seen[lb][1][-1]) if seen[lb][1] else "")   # 8f 站位 2：段内转了脸（转回去也照写）
               for lb in order]
        who += shot_overhead.gaze_notes(ov, a, b)        # follow-up 047 G4：被看的东西在画里哪一侧、还是在画外哪一侧
        if who:
            segs.append("%g–%gs %s" % (a, b, "，".join(who)))
    return ("；画面里（按机位换算）：" + "｜".join(segs)) if segs else ""


ENTITY_USAGE = "角色 entity 锁长相、服装与音色，不锁姿势与机位；挂了 entity 的人都在画面里，没挂的人不出现"


def headcount(ep: str, s: "Shot", lines: list[Line]) -> str:
    """人数锁（follow-up 046）：画里的具名人物点名、点数；画外出声的人不入画、不让画里的人替他开口。"""
    people = [c for c in s.chars if c.startswith("c")]
    if not people:
        return ""
    sd = _shot_dir(ep, s)
    lab: dict[str, str] = {}
    if (sd / "planning" / "overhead.toml").is_file():
        lab = {a["key"]: a.get("label", a["key"]) for a in shot_overhead.load(sd).get("actor", [])}
    names = [lab.get(c, c) for c in people]
    off = any(l.kind == "画外" for l in lines)
    return ("画里的具名人物只有%s，共 %d 人，任何时刻不多出第 %d 个具名人物，也不把谁换成别人的长相%s"
            % ("、".join(names), len(names), len(names) + 1, "；画外那句出声的那一刻，出声的人不在画里，也不让画里的人替他开口" if off else ""))
# 052：previz 白模人偶的僵硬被照搬进成片——设计稿与上传的精简稿同一句（一处定义）
PREVIZ_POSE_NOTE = "也不照搬白模人偶的姿势——人走路要有重心起伏、摆臂和脚下的分量，打斗要有预备、发力和收势的惯性，按真人自然表演"
USAGE_PREVIZ = ("previz 只锁站位、走位路线、机位与动作时刻，不取长相，" + PREVIZ_POSE_NOTE + "（052）；previz 分成几段时按段号首尾相接就是本镜完整的时间线；" + ENTITY_USAGE + "；"
                "场景参考只锁材质与形制，光线与时辰只按本镜 `光线:`，几何以 previz 为准；物件与装备参考只锁形制。保持角色服装、场景与光线一致，只生成本镜的运动")
USAGE_OVERHEAD = ("镜头平面图是本镜的俯视示意图，不是画面：上方为北，红色机身与扇形＝机位的位置、拍摄方向与视野（旁注离地高度与秒数），"
                  "彩色圆点＝人（尖角＝面朝，箭头＝移动路线，旁边的秒数＝到达时刻），灰色方块＝房屋与地物；"
                  "只按它摆机位、站位、朝向与走位的先后，图里的颜色、线条、箭头与文字都是标记，绝不出现在画面里，人物颜色也不是服装颜色；"
                  + ENTITY_USAGE + "；场景参考只锁材质与形制，光线与时辰只按本镜 `光线:`，空间关系以平面图为准；物件与装备参考只锁形制。"
                  "保持角色服装、场景与光线一致，只生成本镜的运动")


GS_NOTE = "；白模是绿幕前纯色小人偶，只给人物位置、朝向与大概动作（长相、服装、场景、光线、特效和细节动作按文字与参考自己演）"
KF_COMPACT = "人物长相、服装、场景、光线与特效一律按文字和角色 / 场景 / 装备参考；动作要有生命力：抬头盯着对手、肩腰发力、脚下有重心，不僵硬；打中的是敌人、不是自己人的盾"
USAGE_KF = ("状态图是绿幕前的简化小人偶示意图，只给本镜动作的先后、姿势与位置的大概意思（颜色只是标记、不是服装颜色，人偶没有长相）；人物长相、服装、场景、光线、特效与细节"
            "一律按文字与角色 / 场景 / 装备参考，动作要有生命力：抬头盯着对手、肩腰发力、脚下有重心，不僵硬站桩，打中的是敌人、不是自己人的盾；" + ENTITY_USAGE + "；保持服装与场景一致，只生成本镜的运动")


def video_prompt(ep: str, s: Shot, lines: list[Line], secs: float,
                 scenery: list[tuple[float, float, str]] | None = None, need_pv: bool = True) -> str:
    def one(c: str) -> str:
        worn = worn_clause(ep, c, s.key)
        return "%s＝%s%s%s" % (c, char_lock(c), ("；本镜状态：" + s.state[c]) if c in s.state else "",
                              ("；" + worn) if worn else "")
    chars = "；".join(one(c) for c in s.chars) or "画面里没有人"
    gear = "；".join("%s＝%s" % (asset_label(p), asset_lock(p)) for p in s.props if is_equip(p))
    things = "；".join("%s＝%s" % (p, prop_lock(p)) for p in s.props if not is_equip(p))
    props = "；".join(x for x in (("装备：" + gear) if gear else "", ("物件：" + things) if things else "") if x)
    usage = (USAGE_KF if s.kf else (USAGE_PREVIZ + (GS_NOTE if s.gs else "")) if need_pv else USAGE_OVERHEAD) + (SKILL_USAGE if skill_refs(ep, s, need_pv, secs)[0] else "")
    count = headcount(ep, s, lines)
    parts = [
        "参考: " + "、".join(_handles(ep, s, lines, need_pv, secs)),
        "参考用法: " + usage + "。",
        "角色: " + chars + ("；" + props if props else ""),
    ] + (["人数: " + count] if count else []) + [
        "情节: " + s.plot,
        "场景: " + "、".join(dict.fromkeys(scene_lock(p) for p in s.plates)),   # 同一锁定串只写一遍
        "镜头: " + s.camera + "".join("；%g–%gs 场景展示——%s" % sc for sc in (scenery or [])),
    ]
    if s.cut and "【切】" in s.cut:
        jumps = []
        if (_shot_dir(ep, s) / "planning" / "overhead.toml").is_file():
            jumps = shot_overhead.jump_cuts(shot_overhead.load(_shot_dir(ep, s)))
        if jumps:   # 切点处人换了位置 ＝ 跳过了一段时间：照实说，免得模型硬补一段走路（follow-up 034）
            parts.append("分镜: " + s.cut + "。镜内硬切不加任何转场效果；%s 的切跳过了一段时间（人已在新位置），"
                         "其余照常不打断本镜的环境声与光；同一时刻画面里每个人只有一个，切之前谁都不许先在新位置出现" % "、".join("%gs" % j for j in jumps))
        else:
            parts.append("分镜: " + s.cut + "。镜内硬切不加任何转场效果，不打断本镜同一条时间线、环境声与光")
    if s.ledger:
        parts.append("镜内状态: " + s.ledger)
    parts += [
        "走位: " + s.blocking + guard_clause(ep, s) + screen_clause(ep, s, secs, lines),
        "动作: " + composed_action(ep, s, secs),
    ]
    hits = hit_clause(ep, s)
    if hits:
        parts.append("命中: " + hits + "。打中的那一下武器与身体真的接触、看得见受力，不是挥空" + _friend_safe(ep, s))
    parts += [
        "台词: " + _lines_field(lines),
        "光线: " + s.light + "；" + SELF_LIGHT + (("；" + s.holy) if s.holy else
                                                    "；施法的光只在动作里写的那几秒出现，其余时间人物与武器都不发光" if s.casts else
                                                    "；本镜除上述之外没有任何圣光特效，武器不发光"),
        "节奏: " + s.rhythm,
        "音乐: " + music_line(secs),
        "渲染样式: " + style_base() + ("，" + s.style_extra if s.style_extra else ""),
        "比例: " + RATIO,
        "时长: %gs" % secs,
        "负面词: " + _negatives(s) + "，" + NEG_MUSIC + ("，" + NEG_SPEAKER if any(l.kind == "正常台词" for l in lines) else "")
        + (("，" + NEG_GHOST) if s.cut and "跳过了一段时间" in "".join(parts) else ""),
    ]
    return "\n".join(parts)


def seedance_prompt(ep: str, s: Shot, design: str, secs: float, need_pv: bool) -> str:
    """rule 12.4-P：设计稿 → 上传即梦的精简稿。人物＝entity 从 overhead 的 actor 读，白模颜色从本镜 previz_config 读（只在要 previz 时）。"""
    sd = _shot_dir(ep, s)
    colors: dict[str, str] = {}
    pv = sd / "previz" / "previz_config.toml"
    if need_pv and pv.is_file():
        colors = {a["名"]: a.get("色", "") for a in tomllib.loads(_read(pv)).get("角色", [])}
    actors = shot_overhead.load(sd).get("actor", []) if (sd / "planning" / "overhead.toml").is_file() else []
    if s.kf:
        colors = {a.get("label", a["key"]): DOLL_COLOR.get(a["key"], "") + "色" for a in actors if a["key"] in DOLL_COLOR}
    said: dict[str, list[str]] = {}
    for who, (card, _n) in SPEAKERS.items():
        if card:
            said.setdefault(card, []).append(who)
    cast = [prompt_compact.Cast(a["key"], a.get("label", a["key"]), colors.get(a.get("label", a["key"]), ""), "|".join(said.get(a["key"], [])))
            for a in actors]
    cfg = seedance_kit.config(DRAMA)
    swaps = ({a: b for a, b in zip(cast_chunks(ep, s, secs), cast_chunks(ep, s, secs, short=True)) if a != b}
             if s.casts else {})                                        # 8f #17：精简稿里的施法分句用卡的短串
    seed = prompt_compact.compact(design, cast, secs, cfg["audio_mode"], "，".join(x for x in (cfg.get("negatives", ""), NEG_STIFF) if x),
                                  (PREVIZ_POSE_NOTE + (GS_NOTE if s.gs else "")) if need_pv else "", swaps, binding_text(ep, s), KF_COMPACT if s.kf else "")
    leak = sorted({m.group(0) for m in _PROVENANCE.finditer(seed)})
    if leak:
        raise SystemExit("%s shot%02d：Seedance 精简稿里有审稿 / 流程来历注记（%s）——来历写进生成器的注释，不写进状态 / 情节 / 动作（061 收尾）"
                         % (ep, s.n, "、".join(leak)))
    if len(seed) > prompt_compact.COMPACT_MAX:
        msg = "%s shot%02d：Seedance 精简稿 %d 字 > %d（rule 12.4-P：拆镜，或把动作写概括）" % (ep, s.n, len(seed), prompt_compact.COMPACT_MAX)
        if ep not in cfg.get("legacy_eps", []):
            raise SystemExit(msg)
        print("  ⚠ " + msg + "——legacy_eps，只警告")
    return seed


# 上传稿里的审稿 / 流程来历注记：模型会把「旧片把锤画成了镐」当画面描述读（061 收尾，S09）；来历写生成器注释
_PROVENANCE = re.compile(r"follow-up|整集观感|对白通读|冷眼观众|审稿|审片|旧片|出片回读|rule \d|（\d{3}）|(?<![A-Za-z])r\d+：")


def seedance_block(md: str) -> str | None:
    m = re.search(r"^## Seedance prompt[^\n]*\n+" + FENCE + r"text\n(.*?)\n" + FENCE, md, re.S | re.M)
    return m.group(1) if m else None


def _shot_dir(ep: str, s: Shot) -> Path:
    return DRAMA / "5_6_分镜与prompt" / "episodes" / ep / "shots" / ("shot%02d" % s.n)


def previz_prompt(ep: str, s: Shot, secs: float) -> str:
    """第 ③ 层（shot blend）的生成指令——从 overhead.toml（位置）与本镜 `动作:`（时间轴）拼出来，不手写。

    分层（ai_video.md rule 4j）：overhead 定「谁在哪、几秒到」，本块在它上面加动作、形状与镜头远近，
    产物是 previz_config.toml 与 previz MP4；色彩、表情、特效一律留给 Seedance。"""
    sd = _shot_dir(ep, s)
    ov = shot_overhead.load(sd)
    bg = ov["meta"]["scene"]
    bg_dir = shot_overhead._bg_dir(SCENES, bg)
    xy = _plan_xform(ov)
    W, H = -2 * xy(0, 0)[0], 2 * xy(0, 0)[1]
    colors, poses = _previz_vocab()

    def B(x: float, y: float) -> str:
        return "(%.1f, %.1f)" % xy(x, y)

    cams = ov["camera"]
    segs: list[list[dict]] = [[]]
    for i, c in enumerate(cams):
        if i and c.get("cut"):
            segs.append([])
        segs[-1].append(c)
    seg_rows = []
    for k, seg in enumerate(segs):
        t1 = float(segs[k + 1][0]["t"]) if k + 1 < len(segs) else secs
        c0, c1 = seg[0], seg[-1]
        move = "定机位" if len(seg) == 1 or (c0["xy"] == c1["xy"] and c0.get("look") == c1.get("look")) else \
            "运镜 → %gs 到 %s 离地%gm 瞄%s %gmm" % (float(c1["t"]), B(*c1["xy"]), float(c1.get("h", 1.6)),
                                            B(*c1.get("look", c1["xy"])), float(c1.get("lens", 35)))
        seg_rows.append("段%d %g–%gs（%s）：位置 %s 离地%gm 瞄%s %gmm，%s" % (
            k + 1, float(c0["t"]), t1, c0.get("tag", "—"), B(*c0["xy"]), float(c0.get("h", 1.6)),
            B(*c0.get("look", c0["xy"])), float(c0.get("lens", 35)), move))
    prox = _proxy_of(ov)
    actors, props = [], []
    for a in ov.get("actor", []):
        col, h = prox[a["key"] + "|" + a.get("label", "")]
        if col not in colors:
            raise SystemExit("PROXY 色「%s」不在 build_previz.COLORS 里：%s" % (col, sorted(colors)))

        def kf(p: list) -> str:
            face = "，面朝%s" % B(float(p[3]), float(p[4])) if len(p) >= 5 else ""
            return "%gs %s%s" % (float(p[0]), B(float(p[1]), float(p[2])), face)
        n = int(a.get("count", 1))
        row = "%s（%s）：%s" % (a.get("label", a["key"]), a["key"], "；".join(kf(p) for p in a["path"]))
        if re.match(r"^[pe]\d", a["key"]):        # 会动的物件 / 装备（不是人）
            props.append(row + (" · 共 %d 件" % n if n > 1 else ""))
        else:
            actors.append("%s ＝ 色 %s、身高 %gm%s" % (row, col, h, " · 共 %d 个（同色、各自错开 ≥0.8m）" % n if n > 1 else ""))
    props += ["%s：位置 %s，尺寸 %s m%s" % (o["label"], B(*o["xy"]), "×".join("%g" % v for v in o.get("size", [0.6, 0.6])),
                                        "，转 %g°" % float(o["rot"]) if o.get("rot") else "")
              for o in ov.get("object", [])]
    lines = [
        "%02d集%02d镜 · previz 生成指令（shot blend 层）" % (int(ep[2:]), s.n),
        "上游: planning/overhead.toml（位置与时刻）＋ 本镜动作时间轴（姿态）；本块由生成器拼出，改它 ＝ 改上游重跑，"
        "坐标不在 previz_config.toml 里另起一套",
        "产物: `python tools/gen_shots_szzl_%s.py --previz-config %d` 从 overhead 写 previz/previz_config.toml，"
        "再跑 blender -b --factory-startup --python tools/previz/build_previz.py -- previz/previz_config.toml "
        "→ previz/shot%02d_previz.mp4" % (ep, s.n, s.n),
        "[全局]: shot=\"shot%02d\"，项目=\"shengji_zhilu\"，场景=\"%s\"（场景主档 %s.blend 只复制不修改），"
        "fps=%d，total_sec=%g，分辨率=[%d, %d]" % (
            s.n, bg_dir.relative_to(SCENES).as_posix(), bg, PREVIZ_FPS, secs, PREVIZ_RES[0], PREVIZ_RES[1]),
        "坐标: 下列坐标已换成 Blender 世界坐标（平面图 (x 东, y 南) → X = x − %g, Y = %g − y；原点在场地中心），Z 贴地面" % (W / 2, H / 2),
        "[机位]: 路点机位，按 overhead 分 %d 段%s；" % (len(segs), "，段与段之间是硬切（路点 切＝true，一条渲完）" if len(segs) > 1 else "")
        + "；".join(seg_rows),
        "景别档: 起幅 %s（人占画高 %g）→ 落幅 %s（%g），机位标签 %s → %s；用 焦距 + 位置 对出，不够就微调距离、不改机位方位" % (
            s.jb[1], s.jb[0], s.jb[3], s.jb[2], s.jbcam[0], s.jbcam[1]),
        "[[角色]]（色块人偶，关键帧 t / 位置 / 朝向 / 姿态）: " + ("；".join(actors) or "无"),
        "[[道具]]（box / plane / cyl / sphere；有白模的用 形=\"模型\"）: " + ("；".join(props) or "无"),
        "姿态: 按下面的动作时间轴逐拍补 姿态 关键帧，只用引擎姿态表 %s，可叠加写「跌坐+抬头」；"
        "生成器已在移动段起点打「行走」、到站打「站」，本镜额外姿态写在 Shot.previz 的 poses" % "/".join(poses),
        "动作时间轴: " + s.action,
    ]
    hits = hit_clause(ep, s)
    if hits:
        lines.append("命中（previz 机检：那一刻锤头 / 盾真的贴到目标身上）: " + hits)
    choreo = _shot_dir(ep, s) / "cascadeur" / "choreo.toml"
    if choreo.is_file() and not s.gs:      # 攻防镜：人体由 Cascadeur 出（follow-up 032），色块人偶只剩怪
        lines.append("人体动作（Cascadeur）: cascadeur/choreo.toml 逐拍写姿态、位置与朝向读 overhead；"
                     "`python tools/cascadeur/choreo.py <shot 目录> --build` 驱动在跑的 Cascadeur 出 shot%02d_body{N}.fbx，"
                     "previz 引擎按 [[角色]].模型 导入、逐帧贴地；上面「姿态」一行只管剩下的色块人偶与四足" % s.n)
    if s.previz.get("hook"):
        lines.append("本镜后处理: previz/%s（手持物件与怪的扑咬；盾面法线取前臂手背方向，挡向哪、盾就朝哪）" % s.previz["hook"])
    lines += [
        "镜头意图: " + s.camera,
        "验收: ① 每段首尾的人占画高落在景别档 ② 姿态关键帧 t 与动作时间轴逐拍对齐 ③ 人与道具不穿墙、机位不进实心体块 "
        "④ 渲完先看一眼再交给 Seedance",
        "不管: 长相、服装、色彩、光影、表情、特效——归 Seedance 那一层",
    ]
    return "\n".join(lines)


def _plan_xform(ov: dict):
    """场地平面图坐标 (x 东, y 南，米) → Blender 世界坐标（原点在场地中心）。prompt 与 previz_config 共用这一处。"""
    owner, _ = shot_overhead.planschema.resolve(str(shot_overhead._bg_dir(SCENES, ov["meta"]["scene"])))
    W, H = shot_overhead.planschema.load(owner)["meta"]["size_m"]
    return lambda x, y: (float(x) - W / 2, H / 2 - float(y))


PREVIZ_AIM_Z = 1.4        # overhead 的 look 只有平面坐标；瞄点取成人胸口高
PREVIZ_PROP_H = 1.0       # overhead [[object]] 没写 h 时的缺省高；旧镜的 Shot.previz["heights"] 按 label 覆盖
PREVIZ_GROUND = ("地形", "地面", "道路")   # build_scene 的地形 / 内景地面 / 道路集合（含桥面）；previz 按它们逐点贴地（overhead 的 h 是离地高度）


def _toml(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return "%g" % round(float(v), 3)
    if isinstance(v, str):
        return '"%s"' % v.replace('"', "'")
    return "[" + ", ".join(_toml(x) for x in v) + "]"


def _yaw(dx: float, dy: float) -> float:
    """面朝方向（Blender XY）→ build_previz 的「朝向」度数：人偶 0° 面朝 -Y（鼻锥在 -Y）。"""
    return round(math.degrees(math.atan2(dx, -dy)), 1)


def _moved(a: tuple, b: tuple) -> bool:
    return abs(a[1] - b[1]) > 0.05 or abs(a[2] - b[2]) > 0.05


def previz_config(ep: str, s: Shot, secs: float) -> str:
    """shot blend 层配置：位置与时刻逐字取自 overhead.toml（经 _plan_xform），姿态与物件高度取自 Shot.previz。
    改走位 ＝ 改 overhead 重跑本函数，previz_config.toml 不手改（rule 4j：位置只写一次）。"""
    ov = shot_overhead.load(_shot_dir(ep, s))
    xy = _plan_xform(ov)
    colors, poses = _previz_vocab()
    extra = tuple(s.previz.get("poses", ())) + cast_poses(ep, s)       # rule 45：施法手势按技能卡的姿势键自动打
    for _, _, p in extra:
        if any(q not in poses for q in p.split("+")):
            raise SystemExit("shot%02d previz 姿态「%s」不在引擎姿态表：%s" % (s.n, p, poses))
    cams = ov["camera"]
    subj = next((a for a in ov.get("actor", []) if a["key"] == cams[0].get("subject")), None)
    L = ["# 由 tools/gen_shots_szzl_%s.py --previz-config %d 从 planning/overhead.toml 生成；不手改。" % (ep, s.n), "",
         '["全局"]', "shot = %s" % _toml("shot%02d" % s.n), "\"项目\" = %s" % _toml(DRAMA.name),
         *(["\"绿幕\" = true"] if s.gs else ["\"场景\" = %s" % _toml(shot_overhead._bg_dir(SCENES, ov["meta"]["scene"]).relative_to(SCENES).as_posix())]),
         "fps = %d" % PREVIZ_FPS, "total_sec = %s" % _toml(secs), "\"分辨率\" = %s" % _toml(list(PREVIZ_RES)), *(["\"参考截止\" = %s" % _toml(s.pv_end)] if s.pv_end else []),
         *([] if s.gs else ["\"地形\" = %s" % _toml(list(PREVIZ_GROUND))])]
    if s.previz.get("hook") and not s.gs:
        L.append("\"后处理\" = %s" % _toml(s.previz["hook"]))
    names = _labels(ep, s)
    for c in sorted(s.casts, key=lambda c: c.t):      # follow-up 065：钩子的光代理按技能卡的阶段窗走，不手抄时刻
        card = skills_lib.find(skill_cards(), c.key)
        L += ["", '[["施法"]]', "\"技能\" = %s" % _toml(c.key), "\"谁\" = %s" % _toml(names.get(c.who, c.who)),
              "\"目标\" = %s" % _toml(names.get(c.target, c.target)),
              "\"阶段\" = %s" % _toml([[ph, a, b] for ph, a, b in skills_lib.phases(card, c)])]
    # 攻防镜的人体动作由 Cascadeur 出（follow-up 032）：cascadeur/choreo.toml 里列了的人，previz 挂它的烘焙 FBX
    bodies, body_o, body_fps = {}, None, 30
    choreo = _shot_dir(ep, s) / "cascadeur" / "choreo.toml"
    if choreo.is_file() and not s.gs:
        import tomllib
        ch = tomllib.loads(choreo.read_text(encoding="utf-8"))
        bodies = {lb: "../cascadeur/shot%02d_body%d.fbx" % (s.n, i + 1) for i, lb in enumerate(ch["actor"])}
        body_o, body_fps = xy(*ch["meta"]["origin"]), int(ch["meta"].get("fps", 30))
    L += ["",
         '["机位"]', "\"焦距\" = %s" % _toml(cams[0].get("lens", 35)), "\"占画高\" = %s" % _toml(s.jb[0])]
    if subj:
        L.append("\"基准主体\" = %s" % _toml(subj.get("label", subj["key"])))
    for c in cams:
        cx, cy = xy(*c["xy"])
        lx, ly = xy(*c.get("look", c["xy"]))
        L += ["", '[["机位"."路点"]]', "t = %s" % _toml(c["t"]), "\"位置\" = %s" % _toml([cx, cy, c.get("h", 1.6)]),
              "\"瞄\" = %s" % _toml([lx, ly, c.get("aim_h", PREVIZ_AIM_Z)]), "\"焦距\" = %s" % _toml(c.get("lens", 35))]
        if c.get("cut"):
            L.append("\"切\" = true")
    prox = _proxy_of(ov)
    for a0 in ov.get("actor", []):
        if re.match(r"^[pe]\d", a0["key"]):
            continue
        col, h = prox[a0["key"] + "|" + a0.get("label", "")]
        if col not in colors:
            raise SystemExit("PROXY 色「%s」不在 build_previz.COLORS 里" % col)
        for a in _crowd(a0):
            L += _previz_actor(s, a, a0, col, h, xy, extra, bodies, body_o, body_fps)
    for o in ov.get("object", []):
        ox, oy = xy(*o["xy"])
        w, d = o.get("size", [0.6, 0.6])
        L += ["", '[["道具"]]', "\"名\" = %s" % _toml(o["label"]),
              "\"尺寸\" = %s" % _toml([w, d, _obj_h(s, o)]),
              "\"位置\" = %s" % _toml([ox, oy, 0.0])]
        if o.get("rot"):
            L.append("\"朝向\" = %s" % _toml(-float(o["rot"])))
    for pr in ov.get("prop", []):        # 会动的道具（049 G9）：路点逐个打帧；出场前、gone 之后缩成一点
        w, d = pr.get("size", [0.4, 0.4])
        ph = float(pr.get("h", 0.3))
        pts = [(float(q[0]),) + tuple(xy(float(q[1]), float(q[2]))) for q in pr["path"]]
        keys = [(0.0, pts[0][1], pts[0][2], 1e-3), (max(0.0, pts[0][0] - 0.05), pts[0][1], pts[0][2], 1e-3)] if pts[0][0] > 0.05 else []
        keys += [(t, x, y, 1.0) for t, x, y in pts]
        if pr.get("gone") is not None:
            gx, gy = xy(*shot_overhead.prop_pos(dict(pr, gone=None), float(pr["gone"])))
            keys += [(float(pr["gone"]), gx, gy, 1.0), (float(pr["gone"]) + 0.05, gx, gy, 1e-3)]
        L += ["", '[["道具"]]', "\"名\" = %s" % _toml(pr["label"]), "\"尺寸\" = %s" % _toml([w, d, ph]),
              "\"位置\" = %s" % _toml([pts[0][1], pts[0][2], 0.0])]
        for t, x, y, sc in sorted(keys):
            L += ["", '[["道具"."关键帧"]]', "t = %s" % _toml(round(t, 3)), "\"位置\" = %s" % _toml([x, y, 0.0]),
                  "\"尺寸\" = %s" % _toml([w * sc, d * sc, ph * sc])]
    for h in ov.get("hit", []):          # 命中贴身：previz 自检（follow-up 042）
        if h.get("miss"):
            continue
        L += ["", '[["命中"]]', "t = %s" % _toml(float(h["t"])), "\"谁\" = %s" % _toml(h["who"]), "\"目标\" = %s" % _toml(h["target"]),
              "\"物件\" = %s" % _toml(h.get("obj") or "%s_%s" % (h["who"], HIT_OBJ.get(h["with"], h["with"])))]
        fr = [x for x in shot_overhead.friend_actors(ov) if x["label"] not in (h["who"], h["target"])]
        if h["who"] in {x["label"] for x in shot_overhead.friend_actors(ov)} and h["target"] not in {x["label"] for x in shot_overhead.friend_actors(ov)} and h["with"] not in ("光", "投"):
            L.append("\"友方\" = %s" % _toml([x["label"] for x in fr]))      # G19 回读：挥击窗口里家伙离自己人身上 / 盾的最近距离
        if h["with"] in ("光", "投"):
            L.append("\"远程\" = true")
        elif hit_part_obj(str(h.get("part", ""))):     # 049 G7：打在身上的哪件道具就量哪件（背上的木盾）
            L.append("\"部位\" = %s" % _toml(hit_part_obj(str(h["part"]))))
    return "\n".join(L) + "\n"


def _obj_h(s: "Shot", o: dict) -> float:
    """静态 [[object]] 在 previz 里的高：平面图写的 h ＞ Shot.previz['heights'] ＞ PREVIZ_PROP_H。"""
    return o.get("h", s.previz.get("heights", {}).get(o["label"], PREVIZ_PROP_H))


SEAT_MIN_H = 0.3      # 物件高过它，人在它占地里 previz 就嵌进它（049 S20 劈柴墩）


def _seat_errors(tag: str, s: "Shot", ov: dict, got: dict, secs: float) -> list[str]:
    """049 G5：人在一件 ≥ SEAT_MIN_H 的 [[object]] 占地里、previz 底姿态却不是 build_previz.ON_TOP（坐墩 / 站高）——
    色块人偶只贴地形，会嵌进它里面（S20 加瑞克「坐在劈柴墩上磨斧」previz 里腿埋在墩子里、看着像立在墩顶；
    S06 一群矿工逃跑时穿过帐篷）。底姿态按 build_previz 的 BASE_POSES 逐关键帧推。"""
    import ast
    tree = ast.parse((REPO / "tools" / "previz" / "build_previz.py").read_text(encoding="utf-8"))
    tbl = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
           and getattr(n.targets[0], "id", None) in ("BASE_POSES", "ON_TOP")}
    base_set, on_top = tbl["BASE_POSES"], tbl["ON_TOP"]
    objs = [o for o in ov.get("object", []) if float(_obj_h(s, o)) >= SEAT_MIN_H]
    rows = {r["名"]: r for r in got.get("角色", [])}
    out: list[str] = []
    for a in ov.get("actor", []):
        r = rows.get(a.get("label", a["key"]))
        if r is None or r.get("四足") or not objs:
            continue
        steps = []
        for k in sorted(r.get("关键帧", []), key=lambda k: float(k["t"])):
            bs = [p for p in str(k.get("姿态", "")).split("+") if p in base_set]
            if bs:
                steps.append((float(k["t"]), bs[-1]))
        t0, t1 = float(a.get("enter", 0.0)), min(secs, float(a.get("gone", secs)))
        for o in objs:
            box = {"xy": o["xy"], "size": o.get("size", [0.6, 0.6]), "rot": o.get("rot", 0)}
            bad = [t / 4 for t in range(int(t0 * 4), int(t1 * 4) + 1)
                   if shot_overhead._inside(box, *shot_overhead._pos_at(a["path"], t / 4))
                   and next((b for tk, b in reversed(steps) if tk <= t / 4 + 1e-6), "站") not in on_top]
            if bad:
                out.append("%s: 「%s」%g–%gs 在「%s」(h %g m) 的占地里、previz 底姿态不是 %s——色块人偶会嵌进它里面"
                           "（矮的看着像立在顶上）；坐 / 站在上面就在 Shot.previz['poses'] 写对应姿态，都不是就把 path 绕开它（049 G5）"
                           % (tag, r["名"], bad[0], bad[-1], o["label"], float(_obj_h(s, o)), " / ".join(sorted(on_top))))
    return out


CROWD_GAP = 0.7      # 同卡多只（count = N）在 previz 里排成一列：前后间距（m），左右错开 CROWD_GAP 的一半


def _crowd(a: dict) -> list[dict]:
    """overhead 里 count = N 的一群（follow-up 047 G5：shot11 的六七只矿工 previz 里只做了一只）：第一只沿用原 label，
    其余 label 加序号、沿同一条路线跟在后面一列（窄巷里横排会嵌进墙），命中与 [[guard]] 仍按原 label 找第一只。"""
    n = int(a.get("count", 1))
    if n <= 1:
        return [a]
    p0, p1 = a["path"][0], next((q for q in a["path"][1:] if math.dist(q[1:3], a["path"][0][1:3]) > 0.05), None)
    if p1 is not None:
        hx, hy = p1[1] - p0[1], p1[2] - p0[2]
    elif len(p0) >= 5:
        hx, hy = p0[3] - p0[1], p0[4] - p0[2]
    else:
        hx, hy = 0.0, -1.0
    nrm = math.hypot(hx, hy) or 1.0
    hx, hy = hx / nrm, hy / nrm
    out = [a]
    for i in range(1, n):
        back, lat = CROWD_GAP * ((i + 1) // 2), CROWD_GAP / 2 * (1 if i % 2 else -1)
        dx, dy = -hx * back - hy * lat, -hy * back + hx * lat
        path = [[q[0], q[1] + dx, q[2] + dy] + ([q[3] + dx, q[4] + dy] if len(q) >= 5 else []) for q in a["path"]]
        out.append(dict(a, label="%s%d" % (a.get("label", a["key"]), i + 1), path=path))
    return out


def _previz_actor(s: "Shot", a: dict, base: dict, col: str, h: float, xy, extra, bodies: dict, body_o, body_fps: int) -> list[str]:
    """一个 [[角色]] 块：关键帧由路点换算，持物按 base（原 label）从 Shot.previz['carry'] 取——一群人每只都拿着同样的家伙。"""
    path = [(float(p[0]), *xy(p[1], p[2]), p) for p in a["path"]]
    keys: dict[float, dict] = {}
    yaw = 0.0
    for i, (t, x, y, p) in enumerate(path):
        nxt = path[i + 1] if i + 1 < len(path) else None
        moving = nxt is not None and _moved(nxt, path[i])
        if len(p) >= 5:
            fx, fy = xy(p[3], p[4])
            yaw = _yaw(fx - x, fy - y)
        elif moving:
            yaw = _yaw(nxt[1] - x, nxt[2] - y)
        k = {"t": t, "位置": [x, y, 0.0], "朝向": yaw}
        if moving:
            k["姿态"] = "行走"
        elif i == 0 or _moved(path[i - 1], path[i]):
            k["姿态"] = "站"
        keys[t] = k
    for who, t, pose in extra:
        if who in (a["key"], a.get("label")):      # 同卡多只（两名卫兵、两只狼）按 label 区分
            keys.setdefault(float(t), {"t": float(t)})["姿态"] = pose
    L = ["", '[["角色"]]', "\"名\" = %s" % _toml(a.get("label", a["key"])), "\"色\" = %s" % _toml(col), "\"身高\" = %s" % _toml(h)]
    if a["key"] in QUADRUPED:
        L.append("\"四足\" = true")
    if a.get("gone") is not None:          # 049：钻进洞里 / 跑出画外不回来——previz 从这一刻起藏起来
        L.append("\"离场\" = %s" % _toml(float(a["gone"])))
    if a.get("enter") is not None:         # 049：从洞里钻出来之前藏着
        L.append("\"入场\" = %s" % _toml(float(a["enter"])))
    if a.get("label") in bodies:
        L += ["\"模型\" = %s" % _toml(bodies[a["label"]]), "\"模型原点\" = %s" % _toml(list(body_o)),
              "\"模型帧率\" = %d" % body_fps]
    for t in sorted(keys):
        L += ['[["角色"."关键帧"]]'] + ["\"%s\" = %s" % (k, _toml(v)) for k, v in keys[t].items()]
    lb = base.get("label", base["key"])
    if a.get("label") not in bodies:
        for c in s.previz.get("carry", {}).get(lb) or s.previz.get("carry", {}).get(base["key"], ()):
            c = c if isinstance(c, dict) else dict(zip(("件", "姿", "起", "止"), c))    # (件, 姿[, 起, 止]) 或 {件, 姿, 起, 止, 形}
            L += ['[["角色"."持物"]]'] + ["\"%s\" = %s" % (k, _toml(float(v) if k in ("起", "止") else v)) for k, v in c.items()]
    return L



def _previz_vocab() -> tuple[set[str], list[str]]:
    """build_previz.py 的 COLORS / POSES 表（它 import bpy，只能按 AST 读）；名字只在那一处定义。"""
    import ast
    tree = ast.parse((REPO / "tools" / "previz" / "build_previz.py").read_text(encoding="utf-8"))
    got = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
           if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in ("COLORS", "POSES")}
    return set(got["COLORS"]), list(got["POSES"])


def _previz_rgb() -> dict[str, tuple[float, float, float]]:
    """build_previz.py 的 COLORS（名 → RGB），按 AST 读（它 import bpy）。"""
    import ast
    tree = ast.parse((REPO / "tools" / "previz" / "build_previz.py").read_text(encoding="utf-8"))
    return next(ast.literal_eval(n.value) for n in tree.body
                if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "COLORS")


def doll_hue_errors(tag: str, s: "Shot", cfg_text: str) -> list[str]:
    """057 E3（w28 §3 ③）：previz 人偶的 ID 色不许落进同镜施法的色相带——白模是参考视频，同色的人偶会被画成那道光。"""
    if not s.casts:
        return []
    import colorsys
    rgb = _previz_rgb()
    bands = {c.key: skills_lib.card_hue(DRAMA, skills_lib.find(skill_cards(), c.key)) for c in s.casts}
    out: list[str] = []
    for r in tomllib.loads(cfg_text).get("角色", []):
        if r.get("模型") or r.get("色") not in rgb:
            continue
        h, sat, val = colorsys.rgb_to_hsv(*rgb[r["色"]])
        h *= 360
        for key, (lo, hi, smin, vmin) in bands.items():
            if (lo <= h <= hi if lo <= hi else h >= lo or h <= hi) and sat >= smin and val >= vmin:
                out.append("%s: previz 人偶「%s」的%s（色相 %.0f°）落在本镜 %s 的光的色相带里——换一种人偶色（057 E3）"
                           % (tag, r["名"], r["色"], h, skills_lib.find(skill_cards(), key).name))
                break
    return out


def plate_png(pl: str) -> Path:
    """场景主体 / plate 的出图：锚点在 bg 目录下，plate 在 bg 目录的同名子目录里。"""
    stem, d = plate_stem(pl), _bg_dir(pl.split("-")[0])
    return (d / stem / (stem + ".png")) if "-" in pl else (d / (stem + ".png"))


def upload_files(ep: str, s: Shot, lines: list[Line], need_pv: bool, secs: float) -> list[tuple[str, Path | None]]:
    """参考行每一项 → 该上传的那个文件（生成器只指路，不复制——rule 4i ①）；角色 entity 在 Seedance 里 @，没有文件（None）。"""
    sd = _shot_dir(ep, s)
    out: list[tuple[str, Path | None]] = list(_geo_handles(ep, s, need_pv, secs))
    out += [("`%s=>@`" % name, f) for name, f in skill_refs(ep, s, need_pv, secs)[0]]
    out += [(plate_stem(pl), plate_png(pl)) for pl in s.plates]
    out += [(_char_handle(c), None) for c in s.chars]
    out += [(asset_label(pp), (_equip_dir(pp) / (pp + "-1_正面.png")) if is_equip(pp)       # 装备正面（gen_equipment.py）
             else PROPS / pp / (pp.split("_", 1)[0] + "-1_正面.png")) for pp in s.props]           # 物件正面（gen_props_szzl.py）
    return out


@functools.lru_cache(maxsize=None)
def _slow_voices(ep: str) -> frozenset[str]:
    return script_tools.slow_voices(str(DRAMA / "4_剧本" / "episodes" / ep / "script.md"))


def dub_wps(ep: str, l: "Line") -> float:
    """配音按几词 / 秒念：casting 语速栏写慢 / 很慢 / 极慢的角色按 script_tools.SLOW_WPS_MAX，行尾写了 SLOW_EXEMPT 的那句与其余人按 DUB_WPS（8f 对白通读第四轮）。"""
    return script_tools.SLOW_WPS_MAX if l.who in _slow_voices(ep) and script_tools.SLOW_EXEMPT not in l.tail else DUB_WPS


def dub_blocks(ep: str, s: Shot, lines: list[Line]) -> str:
    if not lines:
        return "## 台词配音 prompt\n\n本镜无台词，不配音。只保留环境声。\n"
    out = ["## 台词配音 prompt", ""]
    for i, l in enumerate(lines, 1):
        words = len(script_tools._EN_WORD.findall(l.text))
        out += [FENCE + "text",
                "%02d集%02d镜 · 台词配音 %d" % (int(ep[2:]), s.n, i),
                "角色: %s" % l.who,
                "音色(锁定·全剧复用 · %s): 见 casting.md 同名行" % voice_id(l.who),
                "情绪: %s" % s.moods.get(i, s.emotion),
                "语速: 自然口语，约 %.1f 词/秒" % dub_wps(ep, l),
                "类型: %s" % l.kind,
                "台词: %s" % l.text,
                "中文意思: %s" % l.gloss,
                "时间窗: %s" % ("%g–%gs" % l.win if l.win else "—"),
                "时长目标: %.1fs" % max(0.6, words / dub_wps(ep, l)),
                FENCE, ""]
    out.append("> voice_id 全剧锁定（`casting.md`）；画外与内心独白也配音入片，只是画面里无人对口型——"
               "画外台词 Seedance 那一侧不生成人声、不挂 entity，只靠这里配（follow-up 046）。"
               + ("\n>\n> **配音注**：%s" % s.dub_note if s.dub_note else ""))
    return "\n".join(out) + "\n"


def cast_context(ep: str, s: Shot, secs: float, need_pv: bool) -> str:
    """Shot context 里一行人看的施放清单 + 一段机读的施放数据（后期按它贴技能音效与口令录音，tools/post/finish_ep.py）。"""
    if not s.casts:
        return ""
    import json
    names = _labels(ep, s)
    rows = []
    for c in s.casts:
        card = skills_lib.find(skill_cards(), c.key)
        rows.append("%s %s %s→%s %g–%gs（%s·%s%s）" % (card.key, card.name, names.get(c.who, c.who), names.get(c.target, c.target) or "—",
                                                   c.t, skills_lib.end_time(card, c), c.tier, c.outcome, "·" + c.variant if c.variant else ""))
    note = skill_refs(ep, s, need_pv, secs)[1]
    return ("- **施放（技能卡，rule 45）**: " + "；".join(rows) + ("\n- **技能参考**: " + note if note else "")
            + "\n" + skills_lib.casts_record(s.casts) + "\n")


def render(ep: str, s: Shot, lines: list[Line], secs: float, seam_ctx: str,
           scenery: list[tuple[float, float, str]] | None = None) -> str:
    need_pv, why = previz_needed(ep, s, secs)
    prompt = video_prompt(ep, s, lines, secs, scenery, need_pv)
    seed = seedance_prompt(ep, s, prompt, secs, need_pv)
    sd = _shot_dir(ep, s)
    ups = "\n".join(("  - %s → [`%s`](%s)" % (h.strip("`").replace("=>@", ""), f.name,
                                               os.path.relpath(f, sd).replace(os.sep, "/"))) if f else
                     "  - %s → 在 Seedance 里 @ 该角色的资产包 entity（不上传文件）" % h.strip("`").replace("=>@", "")
                     for h, f in upload_files(ep, s, lines, need_pv, secs))
    if need_pv:
        geo = (f"- **previz：要**（{why}）——分层出片（ai_video.md rule 4j）：`planning/overhead.toml` → 镜头平面图过目 → "
               f"shot blend（`previz/previz_config.toml` 从 overhead 读位置，加动作与形状；`tools/previz/build_previz.py` 渲）→ "
               f"`previz/shot{s.n:02d}_previz.mp4`（≥1280×720）")
        tail = f"""
## previz prompt（生成上面参考行里的 `shot{s.n:02d}_previz.mp4`）

> 分层出片的 shot blend 层：在镜头平面图的位置上加真实动作、物件形状与镜头远近，渲一条灰模 previz，
> 作为上面 Seedance prompt 里「运动与几何」的参考。放在文件末尾，是因为各闸门把第一个 text 块当 Seedance prompt。

{FENCE}text
{previz_prompt(ep, s, secs)}
{FENCE}
"""
    elif s.kf:
        geo = (f"- **previz：免**（{why}）——参考行挂本镜 {len(s.kf)} 张状态图（`状态图/*.png`，`python tools/shot_keyframes.py {ep} {s.key}` 出）")
        tail = ""
    else:
        geo = (f"- **previz：免**（{why}）——不做 shot blend；Seedance 版镜头平面图 `planning/shot{s.n:02d}_overhead_ref.png` "
               f"直接当运动与几何参考上传")
        tail = ""
    return f"""---
episode: {ep}
shot: {s.n:02d}
script: {s.key}
title: {s.title}
duration_s: {secs:g}
seam: 硬切
---

# {ep} · shot{s.n:02d}《{s.title}》

## Shot context

- **衔接**: 硬切（独立首帧）
- **景别档**: {s.jb[1]}{s.jb[0]:g} → {s.jb[3]}{s.jb[2]:g}（机位 `{s.jbcam[0]}` → `{s.jbcam[1]}`）
- **与前一镜的切口**: {seam_ctx}
- **情绪目的**: {s.emotion}
{cast_context(ep, s, secs, need_pv)}- **场景**: {"、".join(plate_stem(p) for p in s.plates)}
- **剧本**: `../../../../../4_剧本/episodes/{ep}/script.md` § 镜 {s.key}；台词逐句同源（生成器从剧本读，不另抄）
- **镜头平面图（overhead）**: `planning/shot{s.n:02d}_overhead.png`（审阅）· `planning/shot{s.n:02d}_overhead_ref.png`（Seedance）——本镜机位与人物走位的唯一出处（`planning/overhead.toml`）
{geo}
- **Reference uploads**（按参考行顺序；缺哪份跑 `python tools/gen_shots_szzl_{ep}.py --materials {s.n}`）:
{ups}

## 视频 prompt（设计稿：给人和闸门读，不上传）

{FENCE}text
{prompt}
{FENCE}

字数: {len(prompt)} / {PROMPT_MAX}

## Seedance prompt（上传即梦：由上面的设计稿压成，rule 12.4-P）

{FENCE}text
{seed}
{FENCE}

字数: {len(seed)} / {prompt_compact.COMPACT_MAX}

{dub_blocks(ep, s, lines)}{tail}"""


# ─────────────────────────── 闸门 ───────────────────────────

def _field_line(prompt: str, name: str) -> str:
    for ln in prompt.split("\n"):
        if ln.startswith(name + ":"):
            return ln
    return ""


CLOSE_LENS = 50.0     # ≥ 这个焦距（或机位标签带「特写 / 近景」）才算近景插入
_CHANGE = re.compile(r"亮起|亮了一下|浮出|淡了|淡下去|暗下去|暗到|稳住|熄了|熄灭|起光|一闪|聚起")
_SUBT = re.compile(r"(?<![\d.–-])\d+(?:\.\d+)?s(?!\s*[–-]\s*\d)")
_WEAPON = re.compile(r"锤|斧|剑|盾|镐|棒|草叉")
_EQUIP_WEAPON = re.compile(r"锤|斧|剑|盾|镐|棒")   # G3 ① 逐字引 [carry] 只查装备类兵器：物件兵器（草叉 p472）没有 [carry] 可引（8f ep02 S29–S43 误报 13 镜）
_HOLD = re.compile(r"握|拿|提|拎|扛|背|挂|靠|拄|放|插|抱|举|挎|套|挽|别|掂|攥|横|夹|托|接过|手里|手上|手中|臂")
_WOUND = re.compile(r"口子|伤|划开|啄开|红肿|裂开|劈开|裂成|碎成|白痕|凹痕")   # 伤与物件的损坏状态（「镐尖划开的口子」「木盾从中间裂开」），不是拿法


def demo_errors(ep: str, s: "Shot") -> list[str]:
    """学会一样本事的那一刻（goals.toml [[skill]].learned）要有 ≥ 1.5 s 的近景 / 特写段，变化（亮起 / 变暗 / 稳住）写到秒——
    shot07 教「脚下那圈光」埋在 18 s 固定全景里，出片光一直亮着、低头变暗根本没出来（follow-up 043）。"""
    sc = DRAMA / "4_剧本" / "episodes" / ep / "script.md"
    import tomllib
    gl = sc.parent / goal_ledger.FILE
    if not gl.is_file() or not (_shot_dir(ep, s) / "planning" / "overhead.toml").is_file():
        return []
    skills = [k for k in tomllib.loads(gl.read_text(encoding="utf-8")).get("skill", []) if k.get("learned", [None])[0] == s.key]
    if not skills:
        return []
    sshot = next(x for x in script_tools.parse(str(sc))[0] if x.key == s.key)
    ov = shot_overhead.load(_shot_dir(ep, s))
    cams = sorted(ov["camera"], key=lambda c: float(c["t"]))
    cuts = [0.0] + [float(c["t"]) for c in cams if c.get("cut")] + [sshot.dur]
    close = []
    for a, b in zip(cuts, cuts[1:]):
        tag = next((c.get("tag", "") for c in reversed(cams) if float(c["t"]) <= a + 1e-6 and c.get("tag")), "")
        if b - a >= 1.5 and (shot_overhead.cam_at(cams, a + 0.01)["lens"] >= CLOSE_LENS or re.search(r"特写|近景", tag)):
            close.append((a, b))
    out = []
    for k in skills:
        w = script_tools.snippet_window(sshot, k["learned"][1])
        if w is None:
            continue
        if not any(min(b, w[1]) - max(a, w[0]) >= 1.0 for a, b in close):
            out.append("学会「%s」的 %g–%gs 没有 ≥ 1.5 s 的近景 / 特写段（焦距 ≥ %g 或机位标签带特写 / 近景）——演示拍埋在全景里出片看不见（follow-up 043）"
                       % (k["what"], w[0], w[1], CLOSE_LENS))
    for m in re.finditer(r"(\d+(?:\.\d+)?)–(\d+(?:\.\d+)?)s([^；]*(?:；(?!\d)[^；]*)*)", s.action):
        a, b, seg = float(m.group(1)), float(m.group(2)), m.group(3)
        if any(min(b, w[1]) - max(a, w[0]) > 0 for w in (script_tools.snippet_window(sshot, k["learned"][1]) for k in skills) if w) \
                and _CHANGE.search(seg) and not _SUBT.search(seg):
            out.append("%g–%gs 演示拍里的变化（%s）没写到秒——几秒亮起、几秒变暗、几秒稳住（follow-up 043）" % (a, b, _CHANGE.search(seg).group(0)))
    return out


def hold_errors(s: "Shot") -> list[str]:
    """`本镜状态` 里提到兵器（锤 / 斧 / 剑 / 盾…），同一句得写清怎么拿（握 / 扛 / 挎 / 靠…）——
    只写「父亲的旧双手锤」，出片就随手给一把短锤（follow-up 043 shot07）。"""
    out = []
    for c, st in s.state.items():
        for cl in re.split(r"[；。]", st):
            if _WEAPON.search(cl) and not _HOLD.search(cl) and not _WOUND.search(cl):
                out.append("%s 的本镜状态「%s」提到兵器却没写怎么拿（引用装备卡 [carry]）" % (c, cl.strip()[:30]))
    return out


_LAND = re.compile(r"砸在|砸中|砸得|劈在|劈中|劈得|砍在|砍中|打在|打中|拍倒|磕中|撞翻|撞倒|扫开|扫得|踢在|踢中|踢跑|咬在|啄在|顶退|一顶|推得翻")


def hit_coverage(ep: str, s: Shot) -> list[str]:
    """有敌意的镜（overhead [meta] hostile）：`动作:` 每一段里写了打中（砸在 / 劈中 / 撞翻…），这一段就得有 [[hit]]——
    只写「一锤砸下去」不写落在哪、几秒，出片里锤子挥在空气里（follow-up 042 shot05）。"""
    d = _shot_dir(ep, s)
    if not (d / "planning" / "overhead.toml").is_file():
        return []
    ov = shot_overhead.load(d)
    calm = set(ov["meta"].get("calm", []))
    if not ov["meta"].get("hostile") and not any(a["key"].startswith("m") and a.get("label") not in calm and a["key"] not in calm
                                                 for a in ov.get("actor", [])):
        return []
    ts = [float(h["t"]) for h in ov.get("hit", [])]
    ms = list(_SPAN.finditer(s.action))
    out = []
    for i, m in enumerate(ms):
        seg = s.action[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(s.action)]
        a, b = float(m.group(1)), float(m.group(2))
        w = _LAND.search(seg)
        if w and not any(a - 1e-6 <= t <= b + 1e-6 for t in ts):
            out.append("%g–%gs 写了「%s」却没有 [[hit]]——几秒、谁的什么、落在谁的哪（follow-up 042）" % (a, b, w.group(0)))
    return out


AXIS_SIDE, AXIS_GAP = 0.25, 0.10     # 离画面中线多远才算「在左 / 在右」；两人横向相距多少才算分得出先后


_ACT_SEG = re.compile(r"(\d+(?:\.\d+)?)–(\d+(?:\.\d+)?)s ")


def _act_segs(act: str) -> list[tuple[str, str, str]]:
    """`动作:` 按机位段切：(起, 止, 这一段的全文)。一段里可以有好几个「；」——052：原先的正则只取到段里第一个「；」，
    S11 12–25s 起光那半句落在分号后面，施法呼应闸门说「缺 手放哪、光怎么走」；看点 / 空窗闸门同样只看了半段。"""
    ms = list(_ACT_SEG.finditer(act))
    return [(m.group(1), m.group(2), act[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(act)].rstrip("；"))
            for i, m in enumerate(ms)]


def cast_errors(ep: str, shots: tuple["Shot", ...], prompts: dict[str, str]) -> list[str]:
    """施法呼应 S07（follow-up 046）：剧本里的每一次施法（goal_ledger.casts），prompt `动作:` 里与它时间窗重叠的那几段
    也得写到起手、手、光的走向——词表只在 goals.toml `[[casting]]` 一处；有敌人的镜还得在平面图写 [[cast]]。"""
    sc = DRAMA / "4_剧本" / "episodes" / ep / "script.md"
    cfg = tomllib.loads((sc.parent / goal_ledger.FILE).read_text(encoding="utf-8"))
    by = {s.key: s for s in shots}
    out: list[str] = []
    for key, who, what, win in goal_ledger.casts(sc):
        c = goal_ledger.casting_for(cfg, who, what)       # 圣光术与审判各按各的施法（follow-up 047）
        if key not in by or c is None or win is None:
            continue
        s = by[key]
        taught = c["taught"][0]
        if int(re.sub(r"\D", "", key) or 0) < int(re.sub(r"\D", "", taught) or 0):     # 按镜号比：教的那一镜可以不在 --only 子集里（8f）
            continue
        tag = "shot%02d" % s.n
        act = _field_line(prompts[key], "动作")
        segs = [txt for a, b, txt in _act_segs(act) if float(a) < win[1] - 1e-6 and float(b) > win[0] + 1e-6]
        text = "；".join(segs)
        miss = [nm for nm, fld in (("起手", "stance"), ("手放哪", "hand"), ("光怎么走", "flow"))
                if not any(re.search(w, text) for w in goal_ledger.patterns(sc, c, fld))]
        if miss:
            out.append("%s: %s·%s（%g–%gs）prompt `动作:` 没呼应 %s 教的施法——缺 %s" % (tag, who, what, win[0], win[1], taught, "、".join(miss)))
        ov_p = _shot_dir(ep, s) / "planning" / "overhead.toml"
        if not ov_p.is_file():
            continue
        ov = shot_overhead.load(_shot_dir(ep, s))
        calm = set(ov.get("meta", {}).get("calm", []))
        foes = [x for x in ov.get("actor", []) if (x["key"].startswith("m") or x["key"] in ov["meta"].get("hostile", [])
                or x.get("label") in ov["meta"].get("hostile", [])) and x["key"] not in calm and x.get("label") not in calm]
        if foes and not any(float(k["t0"]) < win[1] and float(k["t1"]) > win[0] for k in ov.get("cast", [])):
            out.append("%s: %s·%s（%g–%gs）在有敌人的镜里施法，平面图没有 [[cast]]——写清他站在谁的盾后面（follow-up 046）"
                       % (tag, who, what, win[0], win[1]))
    return out


# axis_ok 的理由要写明换了什么（8f：ep02 打斗段 9 个接缝 7 个靠 axis_ok 放行，理由多是「重新交代」）
_AXIS_WHY = re.compile(r"换地点|换场|换时间|换天|跳过|过了一会|换侧|越轴|反打|推近|推到|拉开|拉回|景别|换了位置|自己换|走到|转身")
AXIS_OK_WIN, AXIS_OK_MAX = 8, 5     # 连续这么多个接缝里靠 axis_ok 放行的超过它就报警告


def axis_why_errors(where: str, why: str) -> list[str]:
    if _AXIS_WHY.search(why):
        return []
    return ["%s 的 axis_ok 没写换了什么——写明换地点 / 跳过时间 / 换侧 / 反打 / 推拉景别 / 人物换位，「重新交代」不算理由（8f 运镜）：%s"
            % (where, why[:30])]


def axis_errors(ep: str, shots: tuple[Shot, ...], src: dict) -> list[str]:
    """跨镜不左右互换（180° 轴，follow-up 044：S03→S04 两人进门，出片里亚伦和杜克左右对调）：
    切点两边都在画里的同一个人，不许从画左跳到画右；两个人的左右先后不许对调。有意跨轴在下一镜写 axis_ok（理由）。"""
    out = []
    oks = [bool(B.axis_ok) for B in shots[1:]]
    for i in range(max(0, len(oks) - AXIS_OK_WIN + 1)):
        if sum(oks[i:i + AXIS_OK_WIN]) > AXIS_OK_MAX:
            print("  ⚠ %s %s–%s：连续 %d 个接缝里 %d 个靠 axis_ok 放行——这一段的机位是不是该重排（8f 运镜）"
                  % (ep, shots[i].key, shots[i + AXIS_OK_WIN].key, AXIS_OK_WIN, sum(oks[i:i + AXIS_OK_WIN])))
            break
    for A, B in zip(shots, shots[1:]):
        if B.axis_ok:
            out += axis_why_errors("shot%02d" % B.n, B.axis_ok)
        if A.key not in src or B.key not in src or B.axis_ok:
            continue
        fa, fb = _shot_dir(ep, A) / "planning" / "overhead.toml", _shot_dir(ep, B) / "planning" / "overhead.toml"
        if not (fa.is_file() and fb.is_file()):
            continue
        ova, ovb = shot_overhead.load(_shot_dir(ep, A)), shot_overhead.load(_shot_dir(ep, B))
        xa = shot_overhead.screen_x(ova, src[A.key][0] - 0.05)
        xb = shot_overhead.screen_x(ovb, 0.05)
        named = {a.get("label", a["key"]) for a in ova.get("actor", []) + ovb.get("actor", []) if a["key"].startswith("c")}
        both = [k for k in xa if k in xb and k in named]
        why = ["%s 画%s→画%s" % (k, "左" if xa[k] < 0 else "右", "左" if xb[k] < 0 else "右")
               for k in both if xa[k] * xb[k] < 0 and min(abs(xa[k]), abs(xb[k])) >= AXIS_SIDE]
        why += ["%s 与 %s 左右对调" % (p, q) for i, p in enumerate(both) for q in both[i + 1:]
                if (xa[p] - xa[q]) * (xb[p] - xb[q]) < 0 and min(abs(xa[p] - xa[q]), abs(xb[p] - xb[q])) >= AXIS_GAP]
        if why:
            out.append("shot%02d→shot%02d 跨轴：%s——镜像下一镜的机位或站位；有意跨轴就在下一镜写 axis_ok（follow-up 044）"
                       % (A.n, B.n, "；".join(why)))
    return out


JUMP_RATIO, JUMP_AZ_DEG = 1.5, 45.0     # 镜内切：同一人的占画高比 < 它、机位方位差 < 它 ＝ 跳切（8f 运镜 1，与跨镜接缝同一把尺）
SPEAK_EDGE_X, SPEAK_EDGE_X_CLOSE = 0.8, 0.7   # 说话人离画边的余量（|x| 上限；近景更严，8f 站位 1）


def intra_cut_errors(tag: str, ov: dict, axis: bool = True) -> list[str]:
    """8f 运镜 1 / 2：镜内【切】也不许跨轴、不许跳切——跨镜接缝的两道闸门原先只查镜与镜之间。
    有意为之在那个 [[camera]] 写 axis_ok / jump_ok ＝ 理由；切点前后人挪了位（跳过了时间）的不算跳切。"""
    out: list[str] = []
    cams = ov.get("camera", [])
    skips = set(shot_overhead.jump_cuts(ov))
    named = {a.get("label", a["key"]): a for a in ov.get("actor", []) if a["key"].startswith("c")}
    for c in cams:
        t = float(c["t"])
        if not c.get("cut") or t <= 0:
            continue
        xa, xb = shot_overhead.screen_x(ov, t - 0.05), shot_overhead.screen_x(ov, t + 0.05)
        both = [k for k in xa if k in xb and k in named]
        if c.get("axis_ok"):
            out += axis_why_errors("%s 镜内 %gs" % (tag, t), str(c["axis_ok"]))
        if axis and not c.get("axis_ok"):
            why = ["%s 画%s→画%s" % (k, "左" if xa[k] < 0 else "右", "左" if xb[k] < 0 else "右")
                   for k in both if xa[k] * xb[k] < 0 and min(abs(xa[k]), abs(xb[k])) >= AXIS_SIDE]
            why += ["%s 与 %s 左右对调" % (p, q) for i, p in enumerate(both) for q in both[i + 1:]
                    if (xa[p] - xa[q]) * (xb[p] - xb[q]) < 0 and min(abs(xa[p] - xa[q]), abs(xb[p] - xb[q])) >= AXIS_GAP]
            if why:
                out.append("%s: 镜内 %gs 的切跨轴：%s——改机位，或在这个 [[camera]] 写 axis_ok（8f 运镜 2）" % (tag, t, "；".join(why)))
        if c.get("jump_ok") or t in skips or not both:
            continue
        cb, ca = shot_overhead.cam_at(cams, t - 0.05), shot_overhead.cam_at(cams, t + 0.05)
        az = lambda k: math.atan2(k["look"][1] - k["xy"][1], k["look"][0] - k["xy"][0])
        daz = abs((math.degrees(az(ca) - az(cb)) + 180) % 360 - 180)
        ratios = []
        for k in both:
            pb = shot_overhead._pos_at(named[k]["path"], t - 0.05)
            pa = shot_overhead._pos_at(named[k]["path"], t + 0.05)
            fb, fa = shot_overhead.subj_frac(cb, pb), shot_overhead.subj_frac(ca, pa)
            ratios.append(max(fb, fa) / max(min(fb, fa), 1e-6))
        if daz < JUMP_AZ_DEG and statistics.median(ratios) < JUMP_RATIO:    # 8f：只一人放大过 1.5、其余几乎不变，照样读成跳帧
            out.append("%s: 镜内 %gs 的切前后景别比中位数 %.2f（%s）、机位方位只差 %.0f°——同景别同角度就是跳切：换景别（多数人比值 ≥ %g）或换角度（≥ %g°），"
                       "有意的写 jump_ok（8f 运镜 1）" % (tag, t, statistics.median(ratios), " / ".join("%.2f" % r for r in ratios), daz, JUMP_RATIO, JUMP_AZ_DEG))
    return out


def speaker_edge_errors(tag: str, ov: dict, lines: list["Line"]) -> list[str]:
    """8f 站位 1：说话的人在台词窗里每个取样点都离画边有余量（|x| ≤ 0.8，近景 ≤ 0.7）——原先只查 0.22 m 立柱余量，半个人出画拦不住。"""
    out: list[str] = []
    cams = ov.get("camera", [])
    for l in lines:
        card = SPEAKERS.get(l.who, (None, ""))[0]
        if l.kind != "正常台词" or not card or not l.win:
            continue
        act = next((a for a in ov.get("actor", []) if a["key"] == card), None)
        if act is None:
            continue
        lb = act.get("label", act["key"])
        for k in range(SPEAK_SAMPLES):
            t = l.win[0] + (l.win[1] - l.win[0]) * (k + 0.5) / SPEAK_SAMPLES
            x = shot_overhead.screen_x(ov, t).get(lb)
            if x is None:
                continue
            c = shot_overhead.cam_at(cams, t)
            lim = SPEAK_EDGE_X_CLOSE if shot_overhead.subj_frac(c, shot_overhead._pos_at(act["path"], t)) >= 1.0 else SPEAK_EDGE_X
            if abs(x) > lim:
                out.append("%s: %s 在 %.1fs 说「%s」时贴着画%s边（x=%+.2f，上限 %g）——机位往他那边带一点（8f 站位 1）"
                           % (tag, l.who, t, l.text[:16], "右" if x > 0 else "左", x, lim))
                break
    return out


FLIGHT_CLEAR_M = 0.5        # 8f 站位 6：飞行物的弹道离施法者自己一方的人至少这么远


def cast_flight_errors(tag: str, s: "Shot", ov: dict) -> list[str]:
    """8f 站位 6（ep02 S37 苏伦娜的火球从强盗乙身上穿过去）：卡上 flight 那个阶段，施法者（阶段起点）→ 目标（阶段终点）的直线，
    离施法者自己一方的人（[meta] hostile 与 m 类算敌方，其余具名人物算我方）≥ FLIGHT_CLEAR_M；平面图 [[cast]] 的 over 点名的放行。"""
    out: list[str] = []
    acts = ov.get("actor", [])
    hostile = set(ov.get("meta", {}).get("hostile", []))
    side = lambda a: a["key"].startswith("m") or a["key"] in hostile or a.get("label") in hostile
    for cst in s.casts:
        card = skills_lib.find(skill_cards(), cst.key)
        span = next(((a0, b0) for ph, a0, b0 in skills_lib.phases(card, cst) if ph in card.flight), None)
        who = next((a for a in acts if a["key"] == cst.who), None)
        tgt = next((a for a in acts if a["key"] == cst.target), None)
        if span is None or who is None or tgt is None:
            continue
        a0, b0 = span
        overs = [str(x) for c in ov.get("cast", []) if _labels_match(c.get("who", ""), who) and float(c["t0"]) <= a0 + 1e-6
                 for x in (c.get("over") if isinstance(c.get("over"), list) else [c.get("over")] if c.get("over") else [])]
        P, T = shot_overhead._pos_at(who["path"], a0), shot_overhead._pos_at(tgt["path"], b0)
        for a in acts:
            if a is who or a is tgt or side(a) != side(who) or int(a.get("count", 1)) > 1 or a.get("label") in overs or a["key"] in overs:
                continue
            dd = min(shot_overhead._seg_dist(shot_overhead._pos_at(a["path"], a0 + (b0 - a0) * k / 4), P, T) for k in range(5))
            if dd < FLIGHT_CLEAR_M:
                out.append("%s: %s 的%s %g–%gs 飞向%s，弹道从自己人%s身上穿过去（离弹道 %.2f m < %g m）——挪开他，或在平面图 [[cast]] 写 over 让它从他头上飞过（8f 站位 6）"
                           % (tag, who.get("label", who["key"]), card.name, a0, b0, tgt.get("label", tgt["key"]), a.get("label", a["key"]), dd, FLIGHT_CLEAR_M))
    return out


def _labels_match(name: str, a: dict) -> bool:
    return name in (a["key"], a.get("label", ""))


FACE_TO_DEG = 45.0          # 8f 站位 3：「对 X」说话时面朝与「说话人→X」的夹角上限
_TO_WHOM = re.compile(r"(?:^|[（(；，\s】])对([^，；。、）)\s]{1,6})")
_NOT_WHOM = ("画外", "隔壁", "口型", "镜头", "着", "方", "面", "准")


def face_to_errors(tag: str, ov: dict, lines: list["Line"]) -> list[str]:
    """8f 站位 3：剧本行尾写「对 X」的台词，说话人要面朝 X（夹角 ≤ 45°），而且在画里所有人当中他最正对的是 X。"""
    out: list[str] = []
    acts = ov.get("actor", [])
    base = lambda a: re.split(r"[（(#·]", a.get("label", a["key"]))[0]
    for l in lines:
        card = SPEAKERS.get(l.who, (None, ""))[0]
        m = _TO_WHOM.search(l.tail)
        if l.kind != "正常台词" or not card or not l.win or not m or m.group(1).startswith(_NOT_WHOM):
            continue
        who_a = next((a for a in acts if a["key"] == card), None)
        tgt = next((a for a in acts if a is not who_a and base(a) and (m.group(1).startswith(base(a)) or base(a).startswith(m.group(1)))), None)
        if who_a is None or tgt is None:
            continue
        for k in range(3):
            t = l.win[0] + (l.win[1] - l.win[0]) * (k + 0.5) / 3
            u = shot_overhead.face_vec(who_a["path"], t)
            if u is None:
                continue
            p = shot_overhead._pos_at(who_a["path"], t)

            def ang(a: dict) -> float:
                q = shot_overhead._pos_at(a["path"], t)
                v = (q[0] - p[0], q[1] - p[1])
                n = math.hypot(*v) * math.hypot(*u)
                return math.degrees(math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / n)))) if n > 1e-9 else 0.0
            a_t = ang(tgt)
            if any(a["key"].startswith("m") and shot_overhead._here(a, t) and ang(a) <= FACE_TO_DEG
                   and math.dist(p, shot_overhead._pos_at(a["path"], t)) <= 4.0 for a in acts):
                continue                    # 正对着扑上来的怪喊给身后的人（S02「Behind me!」）：迎敌不回头，不算没对着 X
            rivals = [a for a in acts if a is not who_a and a is not tgt and a["key"].startswith("c") and shot_overhead._here(a, t)     # 面朝着怪喊给身后的人（S02「躲我后面」）不算
                      and ang(a) < a_t - 5.0]
            if a_t > FACE_TO_DEG or rivals:
                out.append("%s: %s 在 %.1fs「对%s」说「%s」，面朝与%s夹 %.0f°%s——改朝向或站位（8f 站位 3）"
                           % (tag, l.who, t, m.group(1), l.text[:14], base(tgt), a_t,
                              "；他更正对的是%s" % "、".join(base(a) for a in rivals[:2]) if rivals else ""))
                break
    return out


def offscreen_window_errors(ep: str, tag: str, lines: list["Line"]) -> list[str]:
    """8f B①：画外 / 内心独白由后期配音，按自然语速念；时间窗短于「词数 ÷ DUB_WPS」就只能加速硬塞（S13 杜克那句 1.41×）。"""
    out = []
    for l in lines:
        if l.kind not in ("画外", "内心独白") or not l.win:
            continue
        need = len(script_tools._EN_WORD.findall(l.text)) / dub_wps(ep, l)
        if l.win[1] - l.win[0] < need - 1e-6:
            out.append("%s: %s「%s」%s窗 %g–%gs 只有 %.1f s，按自然语速要 %.1f s——放宽时间窗（8f B①）"
                       % (tag, l.who, l.text[:16], l.kind, l.win[0], l.win[1], l.win[1] - l.win[0], need))
    return out


def gate(ep: str, shots: tuple[Shot, ...], vis_legacy: frozenset[str] = frozenset()) -> tuple[list[str], dict]:
    bad: list[str] = []
    src = script_lines(ep)
    scen = script_scenery(ep)
    keys = [s.key for s in shots]
    if keys != list(src):
        bad.append("镜号与剧本不一致：生成器 %s / 剧本 %s" % (keys, list(src)))
    for s in shots:
        if s.key not in src:
            continue
        secs, lines = src[s.key]
        tag = "shot%02d" % s.n
        bad += skill_errors(ep, s, secs, lines)
        bad += reaction_errors(ep, s)
        bad += kf_errors(ep, s, secs)
        try:
            need_pv, _ = previz_needed(ep, s, secs)
        except shot_overhead.Bad as e:
            bad.append("%s: 每镜都必须先有镜头平面图（planning/overhead.toml）：%s" % (tag, e))
            continue
        p = video_prompt(ep, s, lines, secs, scen.get(s.key), need_pv)
        if os.environ.get("DUMP_P") == s.key:
            print(*("%d %s" % (len(l), l[:(900 if l[:2] in ("台词","负面") else 40)]) for l in p.splitlines()), sep=chr(10))
        if len(p) > PROMPT_MAX:
            bad.append("%s: prompt %d 字 > %d" % (tag, len(p), PROMPT_MAX))
        if _HEX.search(p):
            bad.append("%s: prompt 内出现 hex 色值" % tag)
        if re.search(r"=>@\s*[0-9图第]", p):
            bad.append("%s: `参考:` 代填了槽位号，必须裸 `=>@`" % tag)
        ref = _field_line(p, "参考")
        for c in re.findall(r"`([cm]\d+_[^(`]+)\(Seedance 角色 entity", ref):
            if c not in s.chars:
                bad.append("%s: `参考:` 挂了不入画的 %s 的 entity——Seedance 会把他画进来（follow-up 046）" % (tag, c))
        if "只用声音" in ref:
            bad.append("%s: `参考:` 里出现「只用声音」的 entity——画外的人不挂 entity，后期配音（follow-up 046）" % tag)
        for w in IP_RED:
            if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w), p):
                bad.append("%s: 红级 IP 名「%s」进了 prompt" % (tag, w))
        for fld in NARRATIVE:
            ln = _field_line(p, fld)
            for w in IP_YELLOW:
                if w in ln:
                    bad.append("%s: 叙事字段 `%s:` 出现黄级专名「%s」（concept C3，未实测前用描述代替）" % (tag, fld, w))
        if need_pv:
            try:
                previz_prompt(ep, s, secs)
            except (shot_overhead.Bad, SystemExit, KeyError) as e:
                bad.append("%s: 生成 previz prompt 失败：%s" % (tag, e))
        spans = [(float(a), float(b)) for a, b in _SPAN.findall(s.action)]
        if not spans or abs(max(b for _, b in spans) - secs) > 0.01:
            bad.append("%s: `动作:` 时间轴没有铺满 %gs" % (tag, secs))
        bad += ["%s: %s" % (tag, e) for e in hit_coverage(ep, s)]
        bad += ["%s: %s" % (tag, e) for e in demo_errors(ep, s) + hold_errors(s)]
        _last = max((l.win[1] for l in lines if l.win), default=0.0)       # 最后一个时间窗里的台词要给配乐留 0.8 s 收尾
        if _last > secs - TAIL_QUIET + 1e-6:
            _w = [l for l in lines if l.win and l.win[1] == _last]
            _need = sum(script_tools.Shot.need_of(l.text) for l in _w)
            _a = min(l.win[0] for l in _w)
            if _need > (_last - _a) - TAIL_QUIET + 1e-6:
                bad.append("%s: 最后一个时间窗【%g–%gs】的台词要念 %.1fs，给镜尾留不出 %gs 让配乐收住（follow-up 044）"
                           % (tag, _a, _last, _need, TAIL_QUIET))
        if (_shot_dir(ep, s) / "planning" / "overhead.toml").is_file():   # 平面图闸门在生成器里也跑一遍（命中、跳切防分身…）
            _ov = shot_overhead.load(_shot_dir(ep, s))
            _b, _ = shot_overhead.gate(_ov, _overhead_site(_ov), secs, set(s.chars),
                                       "%s%g → %s%g" % (s.jb[1], s.jb[0], s.jb[3], s.jb[2]))
            bad += ["%s: 平面图 %s" % (tag, e) for e in _b]
        in_frame = set(s.chars)
        for l in lines:
            card = SPEAKERS.get(l.who, (None, ""))[0] if l.who in SPEAKERS else "?"
            if l.who not in SPEAKERS:
                bad.append("%s: 说话人 %s 不在 SPEAKERS 表" % (tag, l.who))
            elif l.kind == "正常台词" and card and card not in in_frame:
                bad.append("%s: %s 对口型说话，却没有入画（chars 缺 %s）" % (tag, l.who, card))
            elif l.kind == "正常台词" and not (in_frame - {card}) and not _TO_OFFSCREEN.search(l.tail):
                bad.append("%s: %s 说「%s」时画里没有别人——对谁说？加一个听的人，或注明「对画外 X」，"
                           "自言自语改内心独白（follow-up 032）" % (tag, l.who, l.text[:24]))
        if lines and (_shot_dir(ep, s) / "planning" / "overhead.toml").is_file():
            ov = shot_overhead.load(_shot_dir(ep, s))
            site = _overhead_site(ov)
            for l in lines:
                card = SPEAKERS.get(l.who, (None, ""))[0]
                if l.kind != "正常台词" or not card or not l.win or card not in in_frame:
                    continue
                # 049 对白通读：本剧台词由 Seedance 在窗内任意一刻念出——只量窗中点，宽窗就把背影 / 被挡藏过去了（S21 杜克）。
                #   窗内取 SPEAK_SAMPLES 个点逐点量，取最差的那一刻
                samples = ([(l.win[0] + l.win[1]) / 2] if s.key in SPEAK_WINDOW_LEGACY else
                           [l.win[0] + (l.win[1] - l.win[0]) * (k + 0.5) / SPEAK_SAMPLES for k in range(SPEAK_SAMPLES)])
                blocked = None
                for t_s in samples:
                    vis = shot_overhead.visibility(ov, site, t_s)
                    mine = {a.get("label", a["key"]): vis.get(a.get("label", a["key"]), "ok")
                            for a in ov.get("actor", []) if a["key"] == card}
                    if mine and "ok" not in mine.values():
                        blocked = (t_s, mine)
                        break
                if blocked:
                    t_mid, mine = blocked
                    (print if s.key in vis_legacy else bad.append)("%s: %s 在 %gs 说「%s」，画面里看不见说话的人（%s）——口型对说话人，说的人得在画里、没被挡；"
                               "台词窗【%g–%gs】里每一刻都要看得见，看不见的那段把窗收窄"
                               % (tag, l.who, round(t_mid, 2), l.text[:20], "；".join("%s %s" % kv for kv in mine.items()), l.win[0], l.win[1]))
                    continue
                # 说话人的脸要对着镜头（follow-up 036：shot04 两人全程背对镜头说话）
                back = bool(_BACK_OK.search(l.tail))
                sw = _BACK_SWITCH.search(l.tail) if back else None
                t_sw = float(sw.group(1)) if sw else None
                if t_sw is not None and not l.win[0] < t_sw < l.win[1]:
                    bad.append("%s: %s「%s」注明 %gs 起近景对口型，可台词窗是 %g–%gs（059）" % (tag, l.who, l.text[:20], t_sw, l.win[0], l.win[1]))
                    continue
                views = []
                for t_s in samples:
                    d_s = [v["deg"] for v in shot_overhead.screen_view(ov, t_s).values() if v["key"] == card and v["deg"] is not None]
                    if d_s:
                        views.append((t_s, min(d_s)))
                pre = [(t_s, d) for t_s, d in views if back and (t_sw is None or t_s < t_sw)]
                lip = [(t_s, d) for t_s, d in views if not back or (t_sw is not None and t_s >= t_sw)]
                # 059 对白通读 S21：背影台词 prompt 写着「不对口型」，窗里却切到了他的脸——转脸之前每一刻都不许脸对镜头
                shown = [(t_s, d) for t_s, d in pre if d <= shot_overhead.SPEAKER_PROFILE_DEG]
                if shown:
                    bad.append("%s: %s 说「%s」标了背影（不对口型），可 %gs 说话人的脸对着镜头（%.0f°）——近景挪出台词窗，"
                               "或在行尾注明「Ns 起近景对口型」（059）" % (tag, l.who, l.text[:20], round(shown[0][0], 2), shown[0][1]))
                    continue
                worst = max(lip, key=lambda x: x[1]) if lip else None
                if worst and worst[1] > shot_overhead.SPEAKER_BACK_DEG:
                    bad.append("%s: %s 在 %gs 说「%s」时背对镜头（面朝与机位夹 %.0f°，> %g°）——说话的人要看得见脸和嘴："
                               "改机位或朝向，对话镜以 3/4 侧脸为准（follow-up 036）"
                               % (tag, l.who, round(worst[0], 2), l.text[:20], worst[1], shot_overhead.SPEAKER_BACK_DEG))
                elif pre and max(d for _t, d in pre) > shot_overhead.SPEAKER_BACK_DEG:
                    t_b, d_b = max(pre, key=lambda x: x[1])
                    print("  ⚠ %s: %s 在 %gs 说「%s」背对镜头（%.0f°），剧本已注明背影理由" % (tag, l.who, round(t_b, 2), l.text[:20], d_b))
                elif worst and worst[1] > shot_overhead.SPEAKER_PROFILE_DEG:
                    print("  ⚠ %s: %s 在 %gs 说「%s」是纯侧脸（%.0f°），对话镜最好 3/4" % (tag, l.who, round(worst[0], 2), l.text[:20], worst[1]))
        # 049 对白通读：画外的人声后期从窗的第一秒起配，念的那一段不许与画内台词的窗重叠（S13 杜克的喊声压在亚伦那句上）
        for l in lines:
            if l.kind != "画外" or not l.win:
                continue
            a0 = l.win[0]
            a1 = a0 + max(0.6, len(script_tools._EN_WORD.findall(l.text)) / dub_wps(ep, l))
            card_l = SPEAKERS.get(l.who, (None, ""))[0]
            if card_l and s.key not in SPEAK_WINDOW_LEGACY and (_shot_dir(ep, s) / "planning" / "overhead.toml").is_file():
                ov_l = shot_overhead.load(_shot_dir(ep, s))
                site_l = _overhead_site(ov_l)
                for k in range(SPEAK_SAMPLES):
                    t_s = a0 + (a1 - a0) * (k + 0.5) / SPEAK_SAMPLES
                    vis = shot_overhead.visibility(ov_l, site_l, t_s)
                    sv = shot_overhead.screen_view(ov_l, t_s)
                    shown = [a for a in ov_l.get("actor", []) if a["key"] == card_l and vis.get(a.get("label", a["key"])) == "ok"]
                    faced = [v["deg"] for v in sv.values() if v["key"] == card_l and v["deg"] is not None
                             and v["deg"] <= shot_overhead.SPEAKER_BACK_DEG]
                    cam = shot_overhead.cam_at(ov_l["camera"], t_s)
                    frac = max((shot_overhead.subj_frac(cam, shot_overhead._pos_at(a["path"], t_s)) for a in shown), default=0.0)
                    if shown and faced and frac >= TINY_FRAC:      # 远景里只有一点大的人，看不清嘴，不算
                        bad.append("%s: 画外「%s」配音念到 %.1fs，%.1fs 时 %s 的脸已经在画里（%.0f°）——嘴不动却有声；把那句挪早，或那一段拍他的背（049）"
                                   % (tag, l.text[:20], a1, t_s, l.who, min(faced)))
                        break
            for o in lines:
                if o is not l and o.kind != "画外" and o.win and o.win[0] < a1 - 1e-6 and a0 < o.win[1] - 1e-6:
                    bad.append("%s: 画外「%s」从 %gs 起配音、念到 %.1fs，与画内 %s「%s」的窗【%g–%gs】重叠——两句会撞在一起，把窗错开（049）"
                               % (tag, l.text[:20], a0, a1, o.who, o.text[:20], o.win[0], o.win[1]))
        for card, pat in CREATURES.items():
            hit = next((f for f, v in (("情节", s.plot), ("动作", s.action), ("走位", s.blocking)) if pat.search(v)), None)
            if hit and card not in in_frame:
                bad.append("%s: `%s:` 里有「%s」却没挂 %s 卡——生物的长相只能由卡与它的 entity 锁（follow-up 032）"
                           % (tag, hit, pat.search(getattr(s, {"情节": "plot", "动作": "action", "走位": "blocking"}[hit])).group(0), card))
        if "画面里没有人" in s.blocking and s.chars:
            bad.append("%s: `走位:` 写着画面里没有人，却挂了人物参考（rule 23 ②）" % tag)
        if not s.plates:
            bad.append("%s: 没有挂任何场景主体（rule 23）" % tag)
        bad.extend("%s: 场景图 %s" % (tag, e) for e in scene_review.gate([plate_png(pl) for pl in s.plates]))
    # 看上下文的逐拍逻辑（follow-up 034）：速度词 ↔ 平面图、结果要有原因、跨镜状态账本、伤要登记
    states = beat_logic.load_states(DRAMA / "4_剧本" / "episodes" / ep)
    order = list(src)              # 整集剧本镜序（8f：--only 子集里状态的 to 镜不在子集 → 崩）
    bad.extend(beat_logic.check_states(states, order))
    prev = ""
    for s in shots:
        sd = _shot_dir(ep, s)
        ov = shot_overhead.load(sd) if (sd / "planning" / "overhead.toml").is_file() else None
        act = composed_action(ep, s, src[s.key][0]) if s.casts and s.key in src else s.action   # 053：从拼好施法分句的动作回读
        text_all = " ".join([act, s.blocking, s.plot] + list(s.state.values()))
        bad.extend(beat_logic.check_shot(s.key, act, text_all, ov, prev, states, order))
        bs = beat_logic.beats(act)
        prev = bs[-1][2] if bs else ""
    # 对白通读的指纹章（follow-up 037）：台词、画面动作、情节任何一处改过，就得再通读一遍
    bad.extend(dialogue_review.gate(*_dialogue_fp(ep, shots)[:2]))
    # 目标账本（follow-up 038）：观众要跟的每件事屏幕上说出、接下、提醒、了结
    bad.extend(goal_ledger.check(DRAMA / "4_剧本" / "episodes" / ep / "script.md"))
    bad.extend(cast_errors(ep, shots, {s.key: video_prompt(ep, s, src[s.key][1], src[s.key][0], scen.get(s.key),
                                                          previz_needed(ep, s, src[s.key][0])[0])
                                       for s in shots if s.key in src}))
    try:
        seams = shot_seam.audit([{"n": s.n, "jb": s.jb, "jbcam": s.jbcam, "jbnote": s.jbnote} for s in shots])
    except SystemExit as e:
        bad.append(str(e))
        seams = []
    bad += axis_errors(ep, shots, src)
    return bad, {"src": src, "seams": seams, "scen": scen}


_CARRY = re.compile(r"横挎|扛在|扛着(?![，；。、])|扛上|搭在.{0,3}肩|挎在.{0,3}肩|斜挎|背在.{0,2}背|甩到背上")
_HELD = re.compile(r"锤|斧|盾|棒|剑|镐|草叉|筐|弓")
_SUPPORT = re.compile(r"握|扶|攥|提着|抓着|拿着|托着|按着|背带|皮带|挎带|带子|绳|挂环|系|绑|插|活结")   # 不收单个「手」：「双手锤」不是手扶着


def carry_gate(mds: dict[str, str]) -> None:
    """扛 / 挎 / 背在身上的东西，同一句里得写清是手握着还是带子挂着——「锤横挎肩上」出片就是锤悬在肩上没人扶（follow-up 042）。
    从最终 shot md 的视频 prompt 回读（rule：闸门读产物，不读生成它的中间变量）。"""
    bad = []
    for tag, md in mds.items():
        m = re.search(FENCE + r"text\n(.*?)\n" + FENCE, md, re.S)
        for cl in re.split(r"[；。\n]", m.group(1) if m else ""):     # 按句不按逗号：「右手握住柄，锤头搭在肩后」是一句
            if _CARRY.search(cl) and _HELD.search(cl) and not _SUPPORT.search(cl) and not re.search(r"从.{0,3}肩上", cl):
                bad.append("%s: 「%s」扛 / 挎 / 背着东西却没写手或带子" % (tag, cl.strip()[:40]))
    if bad:
        raise SystemExit("持物支撑不合格 %d 处（follow-up 042 · item.toml [carry] 一处定义）：\n  " % len(bad) + "\n  ".join(bad))


# ───────────── follow-up 047：六道闸门里读产物的那几道（G1 空窗 · G3 装备拿法 · G4 视线登记 · G5 previz 保真 · G6 视觉出处）─────────────

_SUBJ_TAIL = ("脚下", "身边", "身后", "面前", "眼前", "头顶", "那圈", "脚边", "背后", "肩后", "旁边", "周围")
_SUBJ_OWN = re.compile(r"^的(锤|手|拳|脚|盾|斧|剑|头|眼|嘴|肩|腿|膝|背|胳膊|指)")
_PEOPLE_V = re.compile(r"^(?:\d+(?:\.\d+)?s\s*)?(把|解|穿|掂|叹|系|拍|说|走|跑|转|蹲|站|撬|递|拍|抬|举|抡|砸|盯|看|扛|接|叹|喊|笑|点头|摇头|坐|爬|数|推|掀|捡|揣|挡|顶|冲|退|跳|握|按|抱|扶|伸|低头|回头|跨|钻|扔|拖|放|拿|提|拽|甩|系|套|卸|付|买|卖|吃|喝|写|念|叫|问|答|应|撞|扑|咬|劈|砍|踢|抓|捂|跪|躺|靠|搭|攥|松|收|打|挥)")
_IDLE_OK = re.compile(r"特写|插入|空镜")
_PRONOUNS = ("他们", "她们", "两人", "三人", "众人", "他", "她", "它们", "它", "两只", "三只", "几只", "那只", "这只", "一只", "狼", "矿工", "暴徒")
_GAZE_V = re.compile(r"盯着|盯住|望着|看着|看向|数着|小声数|打量|低头看|抬头看|回头看")
_SELF = re.compile(r"看[看着]?自己|自己的|脚下|手里|手上")
FACT_OK = ("human", "ai_read")       # 视觉串挂的事实只认看过原件的（ai_draft 不算）


def _names(ov: dict | None) -> list[str]:
    out = []
    for a in (ov or {}).get("actor", []):
        lb = re.split(r"[（(#·]", a.get("label", ""))[0]
        if lb:
            out += [lb, lb[-2:]] if len(lb) > 2 else [lb]
    return out + list(_PRONOUNS)


def _has_subject(clause: str, names: list[str]) -> bool:
    c = re.sub(r"^\d+(?:\.\d+)?s\s*", "", clause.strip())
    if _PEOPLE_V.match(c):
        return True
    for n in names:
        i = c.find(n)
        while i >= 0:
            tail = c[i + len(n):]
            if not tail.startswith(_SUBJ_TAIL) and (not tail.startswith("的") or _SUBJ_OWN.match(tail)):
                return True
            i = c.find(n, i + 1)
    return False


def idle_errors(tag: str, prompt: str, ov: dict | None) -> list[str]:
    """G1 空窗（shot10：前 8 秒只写景，亚伦就蹲在箱子前摆了七秒）：有人在画的时间窗，至少一句得有人在做事。
    景可以边走边给；真要纯景就标「空镜」让画里没人；特写 / 插入镜不算。"""
    out: list[str] = []
    names = _names(ov)
    for a, b, txt in _act_segs(_field_line(prompt, "动作")):
        a, b = float(a), float(b)
        if _IDLE_OK.search(txt) or (ov and not shot_overhead.screen_view(ov, (a + b) / 2)):
            continue
        if not any(_has_subject(cl, names) for cl in re.split(r"[，。]", txt)):
            out.append("%s: `动作:` %g–%gs 画里有人却没人在做事（%s…）——景边走边给，人得推进本镜的事；"
                       "真要纯景写「空镜」、让人出画（follow-up 047 G1）" % (tag, a, b, txt[:24]))
    return out


_ARM_MOUNT = re.compile(r"(?:挽|绑|套|穿|挂)在?[^，。；]{0,4}(?:左|右)?前?臂|臂上")


def equip_errors(s: "Shot", prompt: str, script_block: str) -> list[str]:
    """G3（shot10：「左臂挎着木盾」出片盾吊在胸前；旧盾在用、新盾背着不用）：
    ① 本镜状态里拿着 / 背着装备的那一句，必须逐字含该件 item.toml [carry] 的一种拿法；盾不许写「挎」；
    ② 同一槽位两件时，拿在手上用的必须是品质高的那件——剧本 `备注:` 写「旧件在用：理由」才放行。"""
    out: list[str] = []
    tag = "shot%02d" % s.n
    eq = [k for k in s.props if is_equip(k)]
    modes = {k: equipment_lib.item(EQUIP, k).get("carry", {}) for k in eq}
    texts = _carry_texts()
    roles = re.sub(r"^角色:\s*", "", _field_line(prompt, "角色"))       # 整集观感 r2：带着字段名，排第一的人从没查过
    act = _field_line(prompt, "动作")
    for chunk in re.split(r"；(?=[cm]\d+_|装备：|物件：)", roles):
        if not chunk.startswith("c"):          # 怪的家伙什是物件卡，不是装备
            continue
        st = chunk.split("本镜状态：", 1)[1] if "本镜状态：" in chunk else ""
        for cl in re.split(r"[；。]", st):
            cl = re.sub(r"没有[^、，；]{0,10}", "", cl)        # 空槽反向声明（「左臂上没有盾」）不是拿着
            if not _EQUIP_WEAPON.search(cl) or not _HOLD.search(cl) or _WOUND.search(cl):
                continue
            if "盾" in cl and "挎" in cl:
                out.append("%s: 「%s」盾不许写「挎」——出片会吊在胸前；引用装备卡 [carry] 的「在用 / 背后」" % (tag, cl.strip()[:30]))
            elif texts and not any(t in cl for t in texts):
                out.append("%s: 「%s」拿法没逐字引用装备卡 [carry]（follow-up 047 G3）" % (tag, cl.strip()[:30]))
        for sent, owners in _carry_owners().items():      # 整集观感 r2：拿在手上的那件不在 props，锁定串与参考图就没上传
            held = [(k, m) for k, m in owners if m not in CARRY_NOT_HELD]
            if sent in st and held and not any(k in s.props for k, _m in held):
                out.append("%s: 本镜状态里「%s」是 %s 的拿法（%s），props 没挂它——装备锁定串与参考图不会上传（整集观感 r2 / 043）"
                           % (tag, sent[:20], "、".join(k for k, _m in held), "、".join(m for _k, m in held)))
        used = {k: m for k in eq for m, t in modes[k].items() if t in st}
        by_slot: dict[str, list[str]] = {}
        for k in used:
            by_slot.setdefault(equipment_lib.row(EQUIP, k).slot, []).append(k)
        cfg = equipment_lib.config(EQUIP)
        for slot, ks in by_slot.items():
            live = [k for k in ks if used[k] != "背后"]
            back = [k for k in ks if used[k] == "背后"]
            if live and back and "旧件在用：" not in script_block:
                rk = lambda k: cfg.tier(equipment_lib.row(EQUIP, k).tier).rank
                if max(rk(k) for k in back) > min(rk(k) for k in live):
                    out.append("%s: %s 槽拿在手上的 %s 比背着的 %s 品质低——新的上手、旧的收起；真要念旧，剧本 `备注:` 写「旧件在用：理由」"
                               "且理由屏幕上看得见（follow-up 047 G3）" % (tag, slot, "、".join(live), "、".join(back)))
        # 049 G9：`动作` 把背在背后的那件写成挽在 / 绑在臂上（S20 旧稿「斧刃卡进还绑在左前臂上的左半块里」）
        cores = {k: equipment_lib.item(EQUIP, k)["noun"][-2:] for k in used}
        only_back = [k for k in used if {m for m, t in modes[k].items() if t in st} == {"背后"}]   # 镜内换过拿法的按时段，归 G2 管
        for k in only_back:
            for seg in (x for x in act.split("；") if cores[k] in x):
                for cl in re.split(r"[，。]", seg):
                    if _ARM_MOUNT.search(cl) and (cores[k] in cl or re.search(r"[左右]?半[块面边]", cl)) \
                            and not any(c2 in cl for q, c2 in cores.items() if q != k):
                        out.append("%s: `动作`「%s」把%s写在臂上，本镜状态里它在背后——两处说法打架（049 G9）" % (tag, cl.strip()[:30], cores[k]))
    return out


_CARRY_ALL: list[str] = []


def _carry_texts() -> list[str]:
    """全装备库的每一种拿法原文（一件不在本镜 props 里也认——练习锤挂腰这种跨镜沿用的状态）。"""
    if not _CARRY_ALL:
        for d in _equip_all_dirs():
            spec = equipment_lib._load(d / equipment_lib.ITEM)
            _CARRY_ALL.extend(spec.get("carry", {}).values())
    return _CARRY_ALL


def _carry_owners() -> dict[str, list[tuple[str, str]]]:
    """拿法原文 → [(装备键, 拿法)]（全库；同一句几件共用时都列上）。"""
    if not _CARRY_OWN:
        for d in _equip_all_dirs():
            spec = equipment_lib._load(d / equipment_lib.ITEM)
            for mode, sent in spec.get("carry", {}).items():
                _CARRY_OWN.setdefault(sent, []).append((d.name.split("_", 1)[0], mode))
    return _CARRY_OWN


_CARRY_OWN: dict[str, list[tuple[str, str]]] = {}


def _equip_all_dirs() -> list[Path]:
    return [p.parent for p in EQUIP.rglob(equipment_lib.ITEM)]


def gaze_errors(tag: str, prompt: str, ov: dict | None) -> list[str]:
    """G4（shot09：亚伦对着镜头数烛光，烛光在镜头身后，画里看不见，看着像朝外）：`动作:` 里有人看 / 盯 / 数，
    而他正脸朝着镜头（夹角 < GAZE_CAM_DEG）——他看的东西多半在镜头身后，得在平面图登记 [[gaze]]，生成器才写得出它在哪。"""
    if not ov:
        return []
    out: list[str] = []
    acts = {a.get("label", a["key"]): a for a in ov.get("actor", [])}
    for a, b, txt in _act_segs(_field_line(prompt, "动作")):
        a, b = float(a), float(b)
        for m in _GAZE_V.finditer(txt):
            if _SELF.search(txt[m.start():m.start() + 12]):
                continue
            head = re.split(r"[，。；]", txt[:m.start()])[-1]      # 053：拼进来的施法分句用「；」隔开，主语只认本分句
            who = next((lb for lb in acts if re.split(r"[（(]", lb)[0] in head), None)
            if who is None:
                continue
            sv = shot_overhead.screen_view(ov, (a + b) / 2).get(who)
            if not sv or sv["deg"] is None or sv["deg"] >= shot_overhead.GAZE_CAM_DEG:
                continue
            key = acts[who]["key"]
            if not any(g["who"] in (key, who) and float(g["t0"]) < b and float(g["t1"]) > a for g in ov.get("gaze", [])):
                out.append("%s: %g–%gs %s「%s」时正脸朝镜头（%.0f°）——他看的东西在哪？平面图登记 [[gaze]]（follow-up 047 G4）"
                           % (tag, a, b, who, txt[m.start():m.start() + 10], sv["deg"]))
    return out


# 装备卡 [carry] 里不在手上、也不挎在身上的拿法：放下了 / 挂在别处 / 收着，previz 不用有
CARRY_NOT_HELD = frozenset({"靠放", "平放", "靠墙", "挂在墙上", "挂腰", "插腰", "入鞘"})


def _carry_kind(noun: str, mode: str) -> str:
    """装备的 previz 件名：盾 / 背盾（背后）/ 锤 / 斧 / 剑 / 镐——按装备卡的 noun 末字判。"""
    if "盾" in noun:
        return "背盾" if mode == "背后" else "盾"
    return next((k for k in ("锤", "斧", "剑", "镐") if k in noun), noun[-1:])


def carry_previz_errors(tag: str, s: "Shot", md: str, cfg_text: str, names: dict[str, str]) -> list[str]:
    """整集观感 r2（S04 故事板里杜克没盾）：`角色:` 本镜状态里拿在手上 / 挎在身上的装备，previz 人偶手上得有
    （Cascadeur 体的道具由钩子挂，不查）。从产物回读：设计稿 `角色:` × 装备卡 [carry] 拿法句 × previz 配置。"""
    line = _field_line(md, "角色")
    rows = {r["名"]: r for r in tomllib.loads(cfg_text).get("角色", [])}
    heads = list(re.finditer(r"(?:^角色: |；)([cm]\d+_[A-Za-z_]+)＝", line))
    out: list[str] = []
    for i, m in enumerate(heads):
        part = line[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(line)]
        row = rows.get(names.get(m.group(1), m.group(1)))
        if row is None or row.get("模型"):
            continue
        held = [h["件"] for h in row.get("持物", [])]
        for sent, owners in _carry_owners().items():
            if sent not in part:
                continue
            for k, mode in owners:
                if mode in CARRY_NOT_HELD or k not in s.props:
                    continue
                it = equipment_lib.item(EQUIP, k)
                kind = _carry_kind(it.get("noun", ""), mode)
                if not any(h == kind or (kind == "盾" and h == "盾") for h in held):
                    out.append("%s: %s本镜状态里「%s」%s，previz 人偶手上没有（[[角色.持物]] 件＝%s）——Shot.previz['carry'] 补上"
                               % (tag, row["名"], it.get("noun", k), mode, kind))
    return out


def previz_fidelity(ep: str, s: "Shot", secs: float, want: str | None = None) -> list[str]:
    """G5（shot11：previz 里杜克没盾、矿工 6 只只做了 1 只，命中检查找不到盾就悄悄改量身体）：
    平面图 N 只 → previz N 个；每个命中用的兵器件 previz 里得有；盘上的 previz_config 与平面图重算的一致。"""
    tag = "shot%02d" % s.n
    cfg_p = _shot_dir(ep, s) / "previz" / "previz_config.toml"
    want = want if want is not None else previz_config(ep, s, secs)
    out: list[str] = []
    got = tomllib.loads(want)
    names = [r["名"] for r in got.get("角色", [])]
    ov = shot_overhead.load(_shot_dir(ep, s))
    for a in ov.get("actor", []):
        n = int(a.get("count", 1))
        lb = a.get("label", a["key"])
        have = sum(1 for q in names if q == lb or re.fullmatch(re.escape(lb) + r"\d+", q))
        if n > 1 and have < n:
            out.append("%s: 平面图「%s」%d 只，previz 只有 %d 个" % (tag, lb, n, have))
    holds = {r["名"]: [h["件"] for h in r.get("持物", [])] for r in got.get("角色", [])}
    bodies = {r["名"] for r in got.get("角色", []) if r.get("模型")}
    for h in got.get("命中", []):
        who, _, item = h["物件"].partition("_")
        if h.get("远程") or item in BODY_HITS or who in bodies or s.previz.get("hook"):
            continue
        if not any(item.startswith(k) or k.startswith(item) or item == k + "头" for k in holds.get(who, [])):
            out.append("%s: 命中 %gs 用「%s」，previz 里%s手上没有这件——Shot.previz['carry'] 补上（follow-up 047 G5）"
                       % (tag, float(h["t"]), h["物件"], who))
    out += _seat_errors(tag, s, ov, got, secs)
    if s.key not in CASCADEUR_LEGACY and not s.gs:     # 052 G13：攻防镜的人体动作用 Cascadeur（follow-up 032 落成机检）
        bodies = {r["名"] for r in got.get("角色", []) if r.get("模型")}
        people = {a.get("label", a["key"]) for a in ov.get("actor", []) if a["key"].startswith("c")}
        for lb in sorted(people - bodies):
            if any(lb in (h["who"], h["target"]) for h in ov.get("hit", [])):
                out.append("%s: 「%s」在攻防里出手或挨打，previz 里却是色块人偶——攻防镜的人体动作用 Cascadeur "
                           "（cascadeur/choreo.toml 写他的逐拍姿势、--build 烘焙；052 G13）" % (tag, lb))
    if cfg_p.is_file() and cfg_p.read_text(encoding="utf-8") != want:
        out.append("%s: previz_config.toml 与平面图重算的不一致——跑 --previz-config %d 并重渲 previz" % (tag, s.n))
    elif cfg_p.is_file():        # 049 G10：mp4 / 静帧是拿哪一版输入渲的——对不上就是旧片
        cur = render_inputs(cfg_p)
        pv = cfg_p.parent
        stamp = pv / ("%s%s" % (tag, PREVIZ_STAMP))
        if not stamp.is_file():
            if s.key not in PREVIZ_UNSTAMPED:
                out.append("%s: previz 没有渲染戳——重渲整条（049 G10）" % tag)
        elif _stamp_of(stamp, s) != _stamp_cmp(cur, s):
            out.append("%s: previz mp4 比配置 / 钩子 / 编排旧——重渲整条（049 G10）" % tag)
        sheet, st = pv / "frames" / ("%s_stills.png" % tag), pv / "frames" / ("%s%s" % (tag, STILLS_STAMP))
        if sheet.is_file() and (not st.is_file() or _stamp_of(st, s) != _stamp_cmp(cur, s)):
            out.append("%s: 静帧拼图不是当前输入出的——重跑 review.py，或删掉 previz/frames/（049 G10）" % tag)
    return out


# 049 G10 之前渲的、之后没再动过的镜：没有渲染戳，显式列名放行（只减不增——重渲一次就从这里删掉）
PREVIZ_UNSTAMPED: frozenset[str] = frozenset()
# 052：引擎版本进了渲染戳（人偶走路加步态）；已经拿旧 previz 出过片的镜不重渲，戳里不比引擎版本（只减不增）
def kf_errors(ep: str, s: "Shot", secs: float) -> list[str]:
    """状态图：每张要有 name / at / prompt，秒数在镜内（图没出时资料包自动报「暂不可用」，不在这里拦）。"""
    out: list[str] = []
    seen: set[str] = set()
    for i, k in enumerate(s.kf, 1):
        if not all(k.get(x) for x in ("name", "at", "prompt")):
            out.append("shot%02d: 状态图第 %d 张要写 name / at / prompt" % (s.n, i))
            continue
        if k["name"] in seen:
            out.append("shot%02d: 状态图重名「%s」" % (s.n, k["name"]))
        seen.add(k["name"])
        if not 0 <= float(k["at"]) <= secs:
            out.append("shot%02d: 状态图「%s」的秒数 %g 不在 0–%gs" % (s.n, k["name"], k["at"], secs))
    return out


REACT_MIN_S = 3.5       # 人物第一次察觉敌人（听见 / 看见，actor.alert_t，缺省＝路径起点）到第一次碰到，至少这么久（用户 2026-10-01：S02 狼出现得离亚伦太近、来不及拿锤）
REACT_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset({"S15"})}      # 只减不增


def reaction_errors(ep: str, s: "Shot") -> list[str]:
    """平面图里每个敌人（m 开头）：从路径起点（第一次出画）到它参与的第一次命中，不短于 REACT_MIN_S。"""
    if s.key in REACT_LEGACY.get(ep, frozenset()):
        return []
    try:
        ov = shot_overhead.load(_shot_dir(ep, s))
    except shot_overhead.Bad:
        return []
    hits = ov.get("hit", [])
    out: list[str] = []
    for a in ov.get("actor", []):
        if not str(a.get("key", "")).startswith("m") or not a.get("path"):
            continue
        t0 = float(a.get("alert_t", a["path"][0][0]))
        ts = [float(h["t"]) for h in hits if a["label"] in (h.get("who"), h.get("target"))]
        if ts and min(ts) - t0 < REACT_MIN_S:
            out.append("shot%02d: 「%s」从被察觉到第一次交手只有 %.1fs < %gs——来不及反应；把它放远、早点出画或晚点交手（用户 2026-10-01，S02 狼）"
                       % (s.n, a["label"], min(ts) - t0, REACT_MIN_S))
    return out


PREVIZ_ENGINE_LEGACY: frozenset[str] = frozenset({"S01", "S02", "S04", "S05", "S06", "S07", "S08", "S09"})
# 052 G13：已经出过片的攻防镜，人体仍是色块人偶（只减不增）
CASCADEUR_LEGACY: frozenset[str] = frozenset({"S06", "S09"})


def _stamp_cmp(cur: dict, s: "Shot") -> dict:
    return {k: v for k, v in cur.items() if k != "engine"} if s.key in PREVIZ_ENGINE_LEGACY else cur


def _stamp_of(p: Path, s: "Shot") -> dict:
    return _stamp_cmp(json.loads(p.read_text(encoding="utf-8")), s)


DENSITY_MIN_S = 1.5       # 052 G14：一个机位段里标了时刻的节拍平均间隔不得短于它——逐拍写死，模型只能赶着做、动作发僵
# 已经出过片的镜不回溯（只减不增）
DENSITY_LEGACY: frozenset[str] = frozenset({"S05", "S06", "S09", "S10"})   # S07 / S08（053）、S01–S04（059）重写重出，退出
_SEG_T = re.compile(r"(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s\s")
_PT_T = re.compile(r"(?<![\d.–-])(\d+(?:\.\d+)?)s(?![\d–])")


def density_errors(tag: str, s: "Shot", prompt: str) -> list[str]:
    """052 G14 动作写概括（S11：17–25s 一段写了 8 个时刻，12–17s 九拍挤在五秒里）：`动作:` 每个机位段里段首之外标了时刻的
    节拍，平均间隔 < DENSITY_MIN_S 即 raise——只留起因、转折和结果的时刻，其余交给 previz 与 `命中:` 行。"""
    if s.key in DENSITY_LEGACY:
        return []
    act = _field_line(prompt, "动作")
    ms = list(_SEG_T.finditer(act))
    out = []
    for i, m in enumerate(ms):
        a, b = float(m.group(1)), float(m.group(2))
        txt = act[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(act)]
        n = len(_PT_T.findall(txt))
        if n and (b - a) / n < DENSITY_MIN_S:
            out.append("%s: `动作:` %g–%gs 一段标了 %d 个时刻（平均 %.1f 秒一拍 < %g）——动作写概括：只留起因、转折、结果的时刻，"
                       "每一下打在哪交给 `命中:` 行与 previz（052 G14）" % (tag, a, b, n, (b - a) / n, DENSITY_MIN_S))
    return out


# 8f 运镜 1 / 2、站位 1 之前就出过片、这次不改的镜（只减不增）
CUT_GATES_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset({"S03", "S05", "S06", "S09", "S10"})}
# 镜内跨轴闸门（8f 运镜 2，2026-09-30 夜）落地前已定稿过审的 ep01 镜：多为有意的反打，逐镜判改不改留给用户（pending_user §10 g；只减不增）
INTRA_AXIS_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset({"S04", "S08", "S11", "S12", "S13", "S14", "S17", "S19", "S20", "S24"})}
# 8f 站位 3（「对 X」面朝）落地前已定稿过审的 ep01 镜：见 pending_user §10（只减不增）
FACE_TO_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset()}
# 059 seg_errors 之前就出过片、这次不改的镜（只减不增）
SEG_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset({"S10"})}


def seg_errors(tag: str, prompt: str, ov: dict | None) -> list[str]:
    """059 对白通读 r4（S21）：近景挪到 16.2s，`动作:` 前一段还标着 10–16.6s——两段重叠、这一刀落在段中间。
    `动作:` 的分段不许重叠；平面图上每一刀都落在分段边界上。"""
    act = _field_line(prompt, "动作")
    segs = [(float(m.group(1)), float(m.group(2))) for m in _SEG_T.finditer(act)]
    out = ["%s: `动作:` %g–%gs 与下一段 %g–%gs 重叠（059）" % (tag, a0, b0, a1, b1)
           for (a0, b0), (a1, b1) in zip(segs, segs[1:]) if a1 < b0 - 1e-6]
    for t in sorted(float(c["t"]) for c in (ov or {}).get("camera", []) if c.get("cut")):
        for a, b in segs:
            if a + 1e-6 < t < b - 1e-6:
                out.append("%s: 机位 %gs 切，`动作:` %g–%gs 一段跨过了这一刀——分段在切点断开（059）" % (tag, t, a, b))
    return out


def _bands_meet(a: tuple, b: tuple) -> bool:
    def rng(h: tuple) -> list[tuple[float, float]]:
        return [(h[0], h[1])] if h[0] <= h[1] else [(h[0], 360.0), (0.0, h[1])]
    return any(x0 < y1 and y0 < x1 for x0, x1 in rng(a) for y0, y1 in rng(b))


RELEASE_GAP_S = 1.0      # w28 ④：不同人的放段至少错开这么久（Seedance 只认整秒）
MIDLINE_X = 0.15         # w28 ⑤：画面横向 |x| 超过它才算站在一边（-1 左 … +1 右）


def cast_schedule_errors(tag: str, md: str, ov: dict | None, names: dict[str, str]) -> list[str]:
    """057 E1（w28 §3 ①）：从写出的 shot md 回读施放记录与【切】。raise：②异色施法同在一个硬切段 ④两人放段相距 < 1 s
    ⑤施法者一镜内跨中线换边 ⑥同一人换技能时上一个还没散 ⑦跨切还在的阶段新段开头没重述；warning：③同段两人的光同时亮（等 MC-A）。"""
    casts = skills_lib.casts_in(md)
    if not casts:
        return []
    m = re.search(r"^时长:\s*(\d+(?:\.\d+)?)s", md, re.M)
    secs = float(m.group(1)) if m else 0.0
    cuts = hard_cuts(_field_line(md, "分镜"))
    segs = list(zip([0.0] + cuts, cuts + [secs]))
    act = _field_line(md, "动作")

    def seg_ids(w: tuple[float, float]) -> set[int]:
        return {i for i, (a, b) in enumerate(segs) if w[0] < b - 1e-6 and a < w[1] - 1e-6}
    info = []
    for c in casts:
        card = skills_lib.find(skill_cards(), c.key)
        ph = skills_lib.phases(card, c)
        if ph:
            rel = next((a for p, a, _ in ph if p == "release"), ph[0][1])
            live = [x for x in ph if not (card.state and x[0] == "linger")] or ph      # 光壳 / 光环的余晖是护身状态，不算「还在散」
            info.append((c, card, ph, (live[0][1], max(b for _, _, b in live)), skills_lib.card_hue(DRAMA, card), rel))
    out: list[str] = []
    for i, (c1, k1, p1, w1, h1, r1) in enumerate(info):
        for c2, k2, p2, w2, h2, r2 in info[i + 1:]:
            pair = "%s（%s %gs）与%s（%s %gs）" % (k1.name, names.get(c1.who, c1.who), c1.t, k2.name, names.get(c2.who, c2.who), c2.t)
            if c1.who != c2.who:
                same = seg_ids(w1) & seg_ids(w2)
                if same and not _bands_meet(h1, h2):
                    out.append("%s: %s 颜色不同却在同一个硬切段里——异色施法之间要有 previz 定好的硬切（w28 ②，057 E1）" % (tag, pair))
                elif same and w1[0] < w2[1] and w2[0] < w1[1]:
                    print("  ⚠ %s: %s 同段同时亮 %g–%gs（w28 ③：等 MC-A 定 raise 还是 warning）"
                          % (tag, pair, max(w1[0], w2[0]), min(w1[1], w2[1])))
                if abs(r1 - r2) < RELEASE_GAP_S - 1e-6:
                    out.append("%s: %s 放段相距 %.2f s < %g s（w28 ④）" % (tag, pair, abs(r1 - r2), RELEASE_GAP_S))
            elif c1.key != c2.key:
                a, b = (w1, w2) if c1.t <= c2.t else (w2, w1)
                if a[1] > b[0] + 1e-6:
                    out.append("%s: %s 同一人换技能时上一个还没散（%g s 散、下一个 %g s 起手）——下一个往后挪，或把上一个的余晖改短（w28 ⑥）"
                               % (tag, pair, a[1], b[0]))
    for c, card, ph, w, h, r in info:
        for cut, text in skills_lib.restates(card, c, names, cuts):
            seg = next((x for x in re.split(r"；(?=\d+(?:\.\d+)?[–-]\d+(?:\.\d+)?s\s)", act) if re.search(r"(?:^|\s)%s[–-]" % re.escape("%g" % cut), x[:16])), "")
            if text not in seg:
                out.append("%s: %s（%s）跨过 %g s 的切点还在，新段开头没有重述「%s」（w28 ⑦）" % (tag, card.name, names.get(c.who, c.who), cut, text[:24]))
    seed = seedance_block(md) or ""
    sk = next((ln for ln in seed.split("\n") if ln.startswith("【技能】")), "")
    for c, card, *_ in info:
        cl = skills_lib.binding_clause(card, c, names)
        if cl and cl.rsplit("，只在", 1)[0] not in sk:
            out.append("%s: 精简稿【技能】没有绑定「%s」（057 E2）" % (tag, cl))
    if info and sk and skills_lib.BINDING_TAIL not in sk:
        out.append("%s: 精简稿【技能】缺末句「%s」（057 E2）" % (tag, skills_lib.BINDING_TAIL))
    if ov:
        lab = {a["key"]: a.get("label", a["key"]) for a in ov.get("actor", [])}
        for who in dict.fromkeys(c.who for c, *_ in info):
            xs = [(round((a + b) / 2, 2), x) for c, _k, ph, *_ in info if c.who == who for p, a, b in ph if p in skills_lib.SELF_PHASES
                  for x in [shot_overhead.screen_x(ov, (a + b) / 2).get(lab.get(who, who))] if x is not None]
            if any(x > MIDLINE_X for _, x in xs) and any(x < -MIDLINE_X for _, x in xs):
                out.append("%s: 施法者%s一镜内跨中线换边（%s）——同一镜里施法的人留在画面同一边（w28 ⑤）"
                           % (tag, lab.get(who, who), "、".join("%gs %+.2f" % tx for tx in xs)))
    return out


def prop_seam_errors(ep: str, shots: tuple["Shot", ...]) -> list[str]:
    """G9 跨切点（049：S21 末帧斧与两半木盾躺在一处，S22 开场挪了 4 m）：同一场景接连两镜，
    上一镜同 key 的 [[prop]] 末位置（没 gone）＝下一镜同 key 的 [[prop]] 首位置 / [[object]] 位置（≤ 0.3 m）；画外被挪过写 moved。"""
    out: list[str] = []
    prev = None
    for s in shots:
        sd = _shot_dir(ep, s)
        ov = shot_overhead.load(sd) if (sd / "planning" / "overhead.toml").is_file() else None
        if prev is not None and ov is not None and prev[1]["meta"]["scene"] == ov["meta"]["scene"]:
            ends = {pr["key"]: (float(pr["path"][-1][1]), float(pr["path"][-1][2]))
                    for pr in prev[1].get("prop", []) if pr.get("key") and pr.get("gone") is None}
            nxt = [(pr["key"], (float(pr["path"][0][1]), float(pr["path"][0][2])), pr.get("moved"), pr["label"])
                   for pr in ov.get("prop", []) if pr.get("key")]
            nxt += [(o["key"], (float(o["xy"][0]), float(o["xy"][1])), None, o["label"]) for o in ov.get("object", []) if o.get("key")]
            for k, st, moved, lb in nxt:
                if k in ends and not moved and math.dist(st, ends[k]) > 0.3:
                    out.append("shot%02d: 「%s」开场在 %s，上一镜 shot%02d 结尾它在 %s（差 %.1f m）——东西不会自己挪；画外被人挪过写 moved = 理由（049 G9）"
                               % (s.n, lb, st, prev[0].n, ends[k], math.dist(st, ends[k])))
        prev = (s, ov) if ov is not None else None
    return out


ACTOR_SEAM_M = 2.0          # 8f 站位 4 / 8：同一机位点硬切接着演，同一人上一镜末与下一镜首的世界坐标最多差这么多（原 3 m，8f 第二轮收到 2 m）


def actor_seam_errors(ep: str, shots: tuple["Shot", ...]) -> list[str]:
    """8f 站位 4（ep02 S26→S27 切过去人全挪了 4 m）：同一场景、同一 plate 接连两镜，下一镜平面图没写 [meta] skip，
    就是同一条时间线接着演——上一镜结尾在场的具名人物，下一镜开场站在原处（≤ 3 m）；画外走过去了在他的 [[actor]] 写 moved。"""
    out: list[str] = []
    prev = None
    for s in shots:
        sd = _shot_dir(ep, s)
        ov = shot_overhead.load(sd) if (sd / "planning" / "overhead.toml").is_file() else None
        if (prev is not None and ov is not None and prev[1]["meta"]["scene"] == ov["meta"]["scene"]
                and prev[0].plates[-1] == s.plates[0] and not ov["meta"].get("skip")):
            ends = {a["key"]: shot_overhead._pos_at(a["path"], float("inf")) for a in prev[1].get("actor", [])
                    if a["key"].startswith("c") and a.get("gone") is None}
            for a in ov.get("actor", []):
                if a["key"] not in ends or a.get("enter") is not None or a.get("moved"):
                    continue
                st = shot_overhead._pos_at(a["path"], float("-inf"))
                if math.dist(st, ends[a["key"]]) > ACTOR_SEAM_M:
                    out.append("shot%02d: 「%s」开场在 (%.1f, %.1f)，上一镜 shot%02d 结尾他在 (%.1f, %.1f)（差 %.1f m）——硬切接着演，人不会瞬移（> %g m）："
                               "按上一镜结尾摆开场站位；跳过了时间在本镜 [meta] 写 skip ＝ 理由，画外走过去了在他的 [[actor]] 写 moved ＝ 理由（8f 站位 4）"
                               % (s.n, a.get("label", a["key"]), st[0], st[1], prev[0].n, ends[a["key"]][0], ends[a["key"]][1],
                                  math.dist(st, ends[a["key"]]), ACTOR_SEAM_M))
        prev = (s, ov) if ov is not None else None
    return out


def _rect_dist(a: dict, b: dict) -> float:
    """两个体块（矩形，含 rot）之间的最小距离；相交为 0。"""
    from tools.previz import planschema
    ca, cb = planschema.corners(a), planschema.corners(b)
    if any(shot_overhead._inside(b, x, y) for x, y in ca) or any(shot_overhead._inside(a, x, y) for x, y in cb):
        return 0.0
    edges = lambda cs: [(cs[i], cs[(i + 1) % 4]) for i in range(4)]
    return min([shot_overhead._seg_dist(p, u, v) for p in ca for u, v in edges(cb)]
               + [shot_overhead._seg_dist(p, u, v) for p in cb for u, v in edges(ca)])


def scene_gap_errors(ep: str, shots: tuple["Shot", ...]) -> list[str]:
    """8f 站位 9：本集用到的每个场景查一次它平面图里的 [[gap]]（between ＝ 两个块 id，min_m ＝ 至少留多宽，why ＝ 出处）。"""
    out: list[str] = []
    done: set[str] = set()
    for s in shots:
        sd = _shot_dir(ep, s)
        if not (sd / "planning" / "overhead.toml").is_file():
            continue
        ov = shot_overhead.load(sd)
        if ov["meta"]["scene"] in done:
            continue
        done.add(ov["meta"]["scene"])
        site = _overhead_site(ov)
        blocks = {b.get("id"): b for b in site.get("block", [])}
        for g in site.get("gap", []):
            pair = [blocks.get(k) for k in g["between"]]
            if None in pair:
                out.append("%s 平面图 [[gap]] %s：块 id 不存在" % (ov["meta"]["scene"], g["between"]))
                continue
            dd = _rect_dist(*pair)
            if dd < float(g["min_m"]) - 0.05:
                out.append("%s：「%s」与「%s」之间只剩 %.2f m，[[gap]] 要 %g m（%s）——挪块，别让窄口在图上合拢（8f 站位 9）"
                           % (ov["meta"]["scene"], pair[0]["name"], pair[1]["name"], dd, float(g["min_m"]), g.get("why", "")))
    return out


FIGHT_SAME_DIR_DEG = 45.0   # 8f 站位 8：一场打戏里机位朝向相差这么多以内的两镜，左右不许翻


def fight_side_errors(ep: str, shots: tuple["Shot", ...], src: dict) -> list[str]:
    """8f 站位 8（ep02 S34→S35 杜克与沃尔特左右翻了）：同场景、没写 [meta] skip、镜里有敌人（[meta] hostile 或 m 类）的连续几镜＝一场打戏；
    其中任意两镜，前一镜末与后一镜首的机位朝向相差 ≤ FIGHT_SAME_DIR_DEG，主角（非敌方具名人物）与敌人、[[guard]] 的护人者与被护者
    在画面上的左右先后不许翻；后一镜给那人写了 moved 的放行。"""
    az = lambda c: math.degrees(math.atan2(c["look"][1] - c["xy"][1], c["look"][0] - c["xy"][0]))
    runs, cur = [], []
    for s in shots:
        sd = _shot_dir(ep, s)
        ov = shot_overhead.load(sd) if (sd / "planning" / "overhead.toml").is_file() else None
        fight = ov is not None and s.key in src and bool(ov["meta"].get("hostile") or any(a["key"].startswith("m") for a in ov.get("actor", [])))
        if cur and fight and ov["meta"]["scene"] == cur[-1][1]["meta"]["scene"] and not ov["meta"].get("skip"):
            cur.append((s, ov))
            continue
        if len(cur) > 1:
            runs.append(cur)
        cur = [(s, ov)] if fight else []
    if len(cur) > 1:
        runs.append(cur)
    out: list[str] = []
    for run in runs:
        for i, (sa, oa) in enumerate(run):
            for sb, ob in run[i + 1:]:
                ta, tb = src[sa.key][0] - 0.05, 0.05
                daz = abs((az(shot_overhead.cam_at(oa["camera"], ta)) - az(shot_overhead.cam_at(ob["camera"], tb)) + 180) % 360 - 180)
                if daz > FIGHT_SAME_DIR_DEG:
                    continue
                xa, xb = shot_overhead.screen_x(oa, ta), shot_overhead.screen_x(ob, tb)
                hostile = set(oa["meta"].get("hostile", [])) | set(ob["meta"].get("hostile", []))
                acts = {a.get("label", a["key"]): a for a in oa.get("actor", []) + ob.get("actor", [])}
                moved = {a.get("label", a["key"]) for a in ob.get("actor", []) if a.get("moved")}
                seen = [k for k in acts if k in xa and k in xb]
                foe = lambda k: acts[k]["key"].startswith("m") or k in hostile
                pairs = [(p, q) for p in seen if acts[p]["key"].startswith("c") and not foe(p) for q in seen if foe(q)]
                pairs += [(g["who"], g["protects"]) for g in oa.get("guard", []) + ob.get("guard", [])
                          if g.get("who") in seen and g.get("protects") in seen]
                for p, q in dict.fromkeys(pairs):
                    if p in moved or q in moved:
                        continue
                    if (xa[p] - xa[q]) * (xb[p] - xb[q]) < 0 and min(abs(xa[p] - xa[q]), abs(xb[p] - xb[q])) >= AXIS_GAP:
                        out.append("shot%02d→shot%02d：同一场打戏、机位朝向只差 %.0f°，%s 与 %s 左右翻了（%s 画%s → 画%s）——"
                                   "按前一镜的左右摆站位或机位；真是人自己换了位置，在后一镜给他写 moved（8f 站位 8）"
                                   % (sa.n, sb.n, daz, p, q, p, "左" if xa[p] < xa[q] else "右", "左" if xb[p] < xb[q] else "右"))
    return out


def look(text: str, facts: tuple[str, ...], liberty: str = "") -> str:
    """G6 视觉出处（脚下光环：一条「待人眼核」的草稿事实一路进了 13 镜）：写游戏机制外观的共用串 / 施法串一律经这里，
    挂的每条事实须在 0_research 注册、且 verified 是看过原件的（human / ai_read）。
    liberty：本剧有意偏离原典的地方（锤头一闪、光团脱锤飞出…）写明偏在哪——声明出来，不许悄悄混进「原典如此」。"""
    if not facts:
        raise SystemExit("视觉串没挂事实出处：「%s…」（follow-up 047 G6）" % text[:24])
    reg = _facts()
    for fid in facts:
        f = reg.get(fid)
        if f is None:
            raise SystemExit("视觉串「%s…」挂的事实 %s 没在 0_research/parts 注册（follow-up 047 G6）" % (text[:24], fid))
        if f.get("verified_by") not in FACT_OK:
            raise SystemExit("视觉串「%s…」挂的事实 %s 是 %s，没人核过原件——先核（follow-up 047 G6）" % (text[:24], fid, f.get("verified_by")))
    return text


_FACTS: dict[str, dict] = {}


def _facts() -> dict[str, dict]:
    if not _FACTS:
        _FACTS.update(facts_registry.load(str(DRAMA))[0])
    return _FACTS


_NEGATED = re.compile(r"[不没无未别]")


def refuted_errors(tag: str, prompt: str) -> list[str]:
    """G6 反面（S13「脚下有光环」、S22「脚下光环低亮」：共用串换掉了，手写的那一句没跟着换）：
    核错（tag ❌）的事实在 0_research 里用 `banned` 列出它的写法，正文（负面词行除外）再出现即 raise；带否定的不算。"""
    body = "\n".join(ln for ln in prompt.split("\n") if not ln.startswith("负面词:"))
    out: list[str] = []
    for fid, f in _facts().items():
        if f.get("tag") != "❌":
            continue
        for pat in f.get("banned") or []:
            for m in re.finditer(pat, body):
                if not _NEGATED.search(body[max(0, m.start() - 3):m.end()]):
                    out.append("%s: 「%s」是已核错的 %s 的写法（见该条 note）——删掉或按核正后的写（follow-up 047 G6）" % (tag, m.group(0), fid))
    return out


# ───────────── follow-up 059：节奏闸门（整集观感 animatic 审：开场 3 秒没钩子、走路 19 秒、站桩交代 40 秒、高潮只有远景）─────────────
PACE_IDLE_MAX = float(script_tools.scenery_cfg(str(DRAMA)).get("idle_max_s", 4))   # G15：一处定义在 script.toml [scenery]
PACE_HOOK_S = 3.0          # G16：每集第一镜，前几秒内要有台词或事件
_STATIC_CAM = re.compile(r"固定|定机位|定点|镜头不动|机位不动")     # G17 认「不动的机位」的各种写法（8f：定机位漏检）
PACE_STATIC_MAX = 15.0     # G17：固定机位只在交代（有台词、没动作）最长秒数
PACE_HERO_FRAC = 0.75      # G18：高潮那一刻主角占画高至少（近景 0.9 那一档）
# 已出片、这次不改的镜（只减不增；按集分开，新集默认全查）
PACE_LEGACY: dict[str, frozenset[str]] = {"ep01": frozenset({"S05", "S06", "S09", "S10"})}
_WALK = re.compile(r"走进|走在|走过|走到|走向|走下|走上|走出|往里走|越走越|慢慢走|沿[^，。；]{0,8}走|跟在[^，。；]{0,6}后|拐进|穿过"
                   r"|摇过|横摇|推近|推进|纵深|揭示|展示")
_EVENT = re.compile(r"扑|砍|撞|摔|喊|吼|嚷|叫|笑|哭|抢|打|挡|劈|咬|踢|推开|拽|抓|递|扔|掏|数|问|说|开口|接过|放下|拿起|举起|跳"
                    r"|停下|站住|转身|回头|抬头|愣|冲|逃|跑|倒|滚|砸|拖|抱")   # G16 开场钩子用；G15 只认台词与带时刻的节拍
_MOVING_CAM = re.compile(r"连续运镜|推|拉|摇|跟|手持|环绕|升|降|移")


def _talk(lines: list["Line"], a: float, b: float) -> bool:
    return any(l.win and l.win[0] < b - 1e-6 and l.win[1] > a + 1e-6 for l in lines)


def pace_errors(ep: str, s: "Shot", first: bool, lines: list["Line"], prompt: str, ov: dict | None, scen: list) -> list[str]:
    """059 节奏四闸：从成品 prompt 的 `动作:` / `分镜:`、剧本台词窗与场景展示、平面图机位回读。"""
    if s.key in PACE_LEGACY.get(ep, frozenset()):
        return []
    tag, out = "shot%02d" % s.n, []
    segs = [(float(a), float(b), txt) for a, b, txt in _act_segs(_field_line(prompt, "动作"))]
    def beat(a: float, b: float, txt: str = "") -> bool:                        # 「有事」＝台词或带时刻的节拍（060：景和事一起给）
        return _talk(lines, a, b) or any(a + 1e-6 < float(t) < b - 1e-6 for t in _PT_T.findall(txt or " ".join(
            x for p, q, x in segs if p < b - 1e-6 and q > a + 1e-6)))
    for a, b, txt in segs:                                                        # G15 空走
        if b - a > PACE_IDLE_MAX + 1e-6 and _WALK.search(txt) and not beat(a, b, txt):
            out.append("%s: %g–%gs 只有走路 / 写景、没台词没事件，%.1f 秒 > %g（059 G15）——压到 %g 秒内，或在里面放一句台词 / 一个事件"
                       % (tag, a, b, b - a, PACE_IDLE_MAX, PACE_IDLE_MAX))
    for a, b, txt in scen:                                                         # G15 场景展示
        if b - a > PACE_IDLE_MAX + 1e-6 and not beat(a, b):
            out.append("%s: 场景展示 %g–%gs 没台词没事件，%.1f 秒 > %g（059 G15）——边展示边让人做事或开口，或压短" % (tag, a, b, b - a, PACE_IDLE_MAX))
    if first:                                                                      # G16 开场钩子
        hook = _talk(lines, 0.0, PACE_HOOK_S) or any(a < PACE_HOOK_S and _EVENT.search(txt.split("，")[0] + txt[:40])
                                                      and not _WALK.search(txt[:20]) for a, b, txt in segs)
        if not hook:
            out.append("%s: 每集第一镜前 %g 秒没有台词也没有事件（059 G16）——开场先给一句话或一个动静" % (tag, PACE_HOOK_S))
    secs_m = re.search(r"^时长:\s*(\d+(?:\.\d+)?)s", prompt, re.M)
    parts = s.cut.split("｜") if s.cut else (["0–%gs %s" % (float(secs_m.group(1)), s.camera)] if secs_m else [])   # 8f：整镜不切也查
    for part in parts:                                                              # G17 站桩交代
        m = re.match(r"\s*(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s", part)
        if not m:
            continue
        a, b = float(m.group(1)), float(m.group(2))
        desc = part[m.end():]
        inside = " ".join(t for x, y, t in segs if x < b - 1e-6 and y > a + 1e-6)
        if (b - a > PACE_STATIC_MAX + 1e-6 and _STATIC_CAM.search(desc) and not _MOVING_CAM.search(_STATIC_CAM.sub("", desc))
                and sum(1 for l in lines if l.win and a <= l.win[0] < b) >= 2 and not re.search(r"扑|砍|撞|摔|抢|打|挡|劈|冲|逃|跑", inside)):
            out.append("%s: %g–%gs 固定机位只在交代，%.1f 秒 > %g（059 G17）——切机位、加动作，或把交代压短" % (tag, a, b, b - a, PACE_STATIC_MAX))
    if "高潮" in s.emotion and not s.hero:                                         # G18 高潮近景
        out.append("%s: 标了高潮却没写 hero=(谁, 秒)——高潮那一刻要有主角脸部近景（059 G18）" % tag)
    elif s.hero and ov:
        who, t = s.hero
        c = shot_overhead.cam_at(ov.get("camera", []), float(t))
        act = next((x for x in ov.get("actor", []) if x["key"] == who), None)
        if act is None:
            out.append("%s: hero 的 %s 不在平面图里（059 G18）" % (tag, who))
        else:
            beats_t = [float(m.group(1)) for m in _PT_T.finditer(_field_line(prompt, "动作"))]
            rel_t = [a0 for cst in s.casts for ph, a0, _b in skills_lib.phases(skills_lib.find(skill_cards(), cst.key), cst) if ph == "release"]
            if not (any(l.win and l.win[0] - 1e-6 <= float(t) <= l.win[1] + 1e-6 for l in lines)
                    or any(abs(float(t) - x) <= 0.5 for x in beats_t + rel_t)):
                out.append("%s: hero 钉在 %gs，那一刻既不在台词窗里、也不在带时刻的动作拍或放光上——钉到高潮那句台词或那一下（8f B④）"
                           % (tag, float(t)))
            frac = shot_overhead.subj_frac(c, shot_overhead._pos_at(act["path"], float(t)))
            sv = shot_overhead.screen_view(ov, float(t)).get(act.get("label", act["key"]))
            if frac < PACE_HERO_FRAC or not sv or sv.get("face") == "背影":
                out.append("%s: 高潮 %gs %s 占画高 %.2f%s——那一刻要他的脸部近景（≥ %.2f，059 G18）"
                           % (tag, float(t), act.get("label", who), frac, "、背对 / 不在画里" if not sv or sv.get("face") == "背影" else "",
                              PACE_HERO_FRAC))
    return out


def product_gates(ep: str, shots: tuple["Shot", ...], mds: dict[str, str], src: dict) -> None:
    bad: list[str] = []
    blocks = script_blocks(ep)
    scen_all = script_scenery(ep)
    for s in shots:
        tag = "shot%02d" % s.n
        p = prompt_light.positive(mds[tag]) or ""
        sd = _shot_dir(ep, s)
        ov = shot_overhead.load(sd) if (sd / "planning" / "overhead.toml").is_file() else None
        bad += ["%s: [L3] %s" % (tag, i.detail) for i in shot_logic.check(tag, mds[tag]) if i.code == "L3"]   # G2 镜内状态对时
        bad += idle_errors(tag, p, ov) + equip_errors(s, p, blocks.get(s.key, "")) + gaze_errors(tag, p, ov) + refuted_errors(tag, p)
        bad += density_errors(tag, s, p) + ([] if s.key in SEG_LEGACY.get(ep, frozenset()) else seg_errors(tag, p, ov))
        bad += pace_errors(ep, s, s.key == next(iter(src)), src[s.key][1], p, ov, scen_all.get(s.key, []))
        bad += skill_forbid_errors(tag, s, mds[tag]) + cast_plan_errors(ep, tag, s)
        bad += cast_schedule_errors(tag, mds[tag], ov, _labels(ep, s))
        bad += offscreen_window_errors(ep, tag, src[s.key][1])
        if ov and s.key not in CUT_GATES_LEGACY.get(ep, frozenset()):
            bad += intra_cut_errors(tag, ov, s.key not in INTRA_AXIS_LEGACY.get(ep, frozenset())) + speaker_edge_errors(tag, ov, src[s.key][1])
            if s.key not in FACE_TO_LEGACY.get(ep, frozenset()):
                bad += face_to_errors(tag, ov, src[s.key][1])
        if ov:
            bad += cast_flight_errors(tag, s, ov)
        if ov:                     # 051 G11 / G12：只由本剧引擎调用，旧剧的生成器不调、不回溯
            bad += ["%s: %s" % (tag, e) for e in shot_overhead.ally_idle_errors(ov) + shot_overhead.hurt_errors(ov) + shot_overhead.path_cross_errors(ov)
                                                         + shot_overhead.low_block_errors(ov, _overhead_site(ov))]
            act = next((ln for ln in p.split("\n") if ln.startswith("动作:")), "")
            bad += ["%s: 「%s」%g–%gs 的 idle 理由「%s」在 `动作:` 里看不见——观众得看得出他为什么等（051 G11）"
                    % (tag, a.get("label", a["key"]), float(i[0]), float(i[1]), i[2])
                    for a in ov.get("actor", []) for i in a.get("idle", []) if str(i[2]) not in act]
        if ov and previz_needed(ep, s, src[s.key][0])[0]:
            pv = previz_config(ep, s, src[s.key][0])          # 三道闸门共用一份（重算一次要几十秒）
            bad += previz_fidelity(ep, s, src[s.key][0], pv)
            bad += carry_previz_errors(tag, s, p, pv, _labels(ep, s))
            bad += doll_hue_errors(tag, s, pv)
    bad += prop_seam_errors(ep, shots) + actor_seam_errors(ep, shots) + fight_side_errors(ep, shots, src) + scene_gap_errors(ep, shots)
    if bad:
        raise SystemExit("产物闸门不合格 %d 处（rule 41 · G1 空窗 / G2 状态对时 / G3 装备拿法 / G4 视线 / G5 previz 保真 / G6 核错残留 / "
                         "G7 打击几何 / G8 施法因果 / G9 道具与连续 / G10 previz 回读 / G11 友方干站 / G12 伤要疼 / G13 攻防用 Cascadeur / G14 动作写概括 / G15–G18 节奏（059）；"
                         "G7 / G8 在平面图闸门里报）：\n  " % len(bad)
                         + "\n  ".join(bad))


def _md_by_shot(ep: str, shots: tuple[Shot, ...], src: dict, seams: list, scen: dict) -> dict[str, str]:
    ctx = {sm.next_n: sm.context() for sm in seams}
    first = next(iter(src))        # 8f：--only 子集写盘时点名的第一镜不是集首镜，别写成「集首镜」
    return {"shot%02d" % s.n: render(ep, s, src[s.key][1], src[s.key][0],
                                     ctx.get(s.n, "集首镜，硬切（独立首帧）。" if s.key == first else "（子集写盘：与上一镜的切口待整集构建时补）"),
                                     scen.get(s.key))
            for s in shots}


def verify(ep_dir: Path, shots: tuple[Shot, ...], src: dict) -> list[str]:
    bad: list[str] = []
    need = ("参考:", "参考用法:", "角色:", "情节:", "场景:", "镜头:", "走位:", "动作:", "台词:",
            "光线:", "节奏:", "渲染样式:", "比例:", "时长:", "负面词:")
    for s in shots:
        f = ep_dir / "shots" / ("shot%02d" % s.n) / ("shot%02d.md" % s.n)
        if not f.is_file():
            bad.append("产物不存在 %s" % f)
            continue
        text = _read(f)
        body = prompt_light.positive(text) or ""
        for fld in need:
            if ("\n" + fld) not in ("\n" + body):
                bad.append("shot%02d: 产物缺字段 `%s`" % (s.n, fld))
        if len(body) > PROMPT_MAX:
            bad.append("shot%02d: 产物 prompt %d 字 > %d" % (s.n, len(body), PROMPT_MAX))
        if ("比例: " + RATIO) not in body:
            bad.append("shot%02d: 产物比例不是 %s" % (s.n, RATIO))
        if ("时长: %gs" % src[s.key][0]) not in body:
            bad.append("shot%02d: 产物时长与剧本不一致" % s.n)
        for l in src[s.key][1]:
            if l.text not in body:
                bad.append("shot%02d: 台词没进 prompt「%s」" % (s.n, l.text[:20]))
        need_pv, _ = previz_needed(ep_dir.name, s, src[s.key][0])
        if need_pv and ("## previz prompt" not in text
                        or not all(h in body for h, _f in _geo_handles(ep_dir.name, s, True, src[s.key][0]))):
            bad.append("shot%02d: 要 previz 的镜，产物缺 previz prompt 块或参考行没挂 previz" % s.n)
        if not need_pv and not s.kf and ("## previz prompt" in text or ("shot%02d_overhead_ref.png" % s.n) not in body):
            bad.append("shot%02d: 免 previz 的镜，参考行必须挂 Seedance 版镜头平面图、且不带 previz 块" % s.n)
        if not shot_overhead.ref_path(f.parent).is_file():
            bad.append("shot%02d: 没有 planning/shot%02d_overhead_ref.png——先跑 tools/shot_overhead.py" % (s.n, s.n))
        seed = seedance_block(text)
        if seed is None:
            bad.append("shot%02d: 产物缺 `## Seedance prompt` 块（rule 12.4-P）" % s.n)
        elif len(seed) > prompt_compact.COMPACT_MAX and ep_dir.name not in seedance_kit.config(DRAMA).get("legacy_eps", []):
            bad.append("shot%02d: Seedance 精简稿 %d 字 > %d" % (s.n, len(seed), prompt_compact.COMPACT_MAX))
        if src[s.key][1] and "## 台词配音 prompt" not in text:
            bad.append("shot%02d: 有台词却无配音块" % s.n)
    if not (ep_dir / "all_shot_prompts.md").is_file():
        bad.append("all_shot_prompts.md 不存在")
    if not (ep_dir / "shotlist.md").is_file():
        bad.append("shotlist.md 不存在")
    return bad


def shotlist(ep: str, shots: tuple[Shot, ...], src: dict, seams: list, generator: str) -> str:
    rows = ["# %s 镜头清单" % ep, "",
            "> 生成物（`%s`），勿手改。镜号 ＝ 剧本镜号；台词、锁定串、voice_id 都在构建时从源头读。" % generator,
            "> 画幅 %s（concept G9 ⑤）；全部硬切 + 景别跳档（CLAUDE.md【TOP PRIORITY】），不做首帧承接。" % RATIO, "",
            "| 镜号 | 剧本 | 内容（情绪目的） | 出场 | 景别档 | 时长 |", "|---|---|---|---|---|---|"]
    for s in shots:
        rows.append("| shot%02d | %s | %s（%s） | %s | %s%g → %s%g | %gs |" % (
            s.n, s.key, s.title, s.emotion, "、".join(c.split("_", 1)[1] for c in s.chars) or "—",
            s.jb[1], s.jb[0], s.jb[3], s.jb[2], src[s.key][0]))
    total = sum(src[s.key][0] for s in shots)
    rows += ["", "时长合计：**%gs**（%d 分 %02d 秒）" % (total, int(total) // 60, int(total) % 60)]
    return "\n".join(rows + shot_seam.table(seams, generator)) + "\n"


def materials(ep: str, shots: tuple[Shot, ...], nums: list[int]) -> int:
    """出片前的素材核对：参考行每一项要上传的文件在不在盘上（缺的列出来，退出码 1）。"""
    src = script_lines(ep)
    missing = 0
    for s in shots:
        if s.n not in nums:
            continue
        secs, lines = src[s.key]
        need_pv, why = previz_needed(ep, s, secs)
        print("shot%02d《%s》 %gs · previz %s（%s）" % (s.n, s.title, secs, "要" if need_pv else "免", why))
        for h, f in upload_files(ep, s, lines, need_pv, secs):
            label = h.strip("`").replace("=>@", "")
            if f is None:
                print("  ◇ %s → Seedance 资产包里 @" % label)
                continue
            ok = f.is_file()
            missing += not ok
            print("  %s %s → %s" % ("✓" if ok else "✗", label.split("(")[0], f.relative_to(REPO)))
        print("  prompt：%s § 视频 prompt" % (_shot_dir(ep, s) / ("shot%02d.md" % s.n)).relative_to(REPO))
    print("缺 %d 份" % missing if missing else "素材齐")
    return 1 if missing else 0


def _dialogue_fp(ep: str, shots) -> tuple[Path, str, int]:
    """(剧本集目录, 指纹, 台词句数)：指纹覆盖剧本每镜正文与生成器里进 prompt 的情节 / 动作。"""
    d = DRAMA / "4_剧本" / "episodes" / ep
    fp, n = dialogue_review.fingerprint(d / "script.md", {s.key: [s.plot, s.action] for s in shots})
    return d, fp, n


# follow-up 065 技能时长锁死之前写好、镜里覆盖了锁死时长、还没重排的镜（只减不增）：dur 照旧生效，跑闸门时打印提醒
CAST_TIME_LEGACY: dict[str, frozenset[str]] = {"ep02": frozenset({"S21", "S33"})}


def _cast_time_legacy(ep: str, shots: tuple[Shot, ...]) -> tuple[Shot, ...]:
    keep = CAST_TIME_LEGACY.get(ep, frozenset())
    for k in sorted(keep):
        print("  ⚠ %s %s：施法时长还按锁死之前的 dur 写（技能卡已按原典锁死，follow-up 065）——重排后从 CAST_TIME_LEGACY 删掉" % (ep, k))
    return tuple(dataclasses.replace(s, casts=tuple(dataclasses.replace(c, legacy=True) for c in s.casts)) if s.key in keep else s
                 for s in shots)


def run(ep: str, shots: tuple[Shot, ...], generator: str, argv: list[str] | None = None,
        vis_legacy: frozenset[str] = frozenset()) -> int:
    """vis_legacy：「说话的人看不见」闸门之前就写好、还没改的镜（显式清单，只减不增）——对它们只打印不拦。"""
    sys.stdout.reconfigure(encoding="utf-8")
    shots = _cast_time_legacy(ep, shots)
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只跑闸门，不写盘")
    ap.add_argument("--verify", action="store_true", help="回读已写出的产物")
    ap.add_argument("--materials", default="", help="逗号分隔的镜号（如 1,2,3）：逐项核对要上传的文件在不在盘上")
    ap.add_argument("--previz-config", default="", help="逗号分隔的镜号：从 overhead.toml 写 previz/previz_config.toml")
    ap.add_argument("--dialogue-stamp", default="", help="对白通读通过后盖章：把本集台词 / 动作 / 情节的指纹记进剧本集目录")
    ap.add_argument("--viewer-stamp", default="", help="冷眼观众通读通过后盖章（与对白通读同一个指纹）")
    args = ap.parse_args(argv)
    if args.dialogue_stamp or args.viewer_stamp:
        d, fp, n = _dialogue_fp(ep, shots)
        for kind, note in (("dialogue", args.dialogue_stamp), ("viewer", args.viewer_stamp)):
            if note:
                dialogue_review.stamp(d, fp, n, note, kind)
                print("%s盖章：%s · %d 句 → %s" % (dialogue_review.KINDS[kind][1], fp, n, (d / dialogue_review.STAMP).relative_to(REPO)))
        return 0
    ep_dir = DRAMA / "5_6_分镜与prompt" / "episodes" / ep
    if args.materials:
        return materials(ep, shots, [int(x) for x in args.materials.split(",") if x])
    if args.previz_config:
        src = script_lines(ep)
        want = [int(x) for x in args.previz_config.split(",") if x]
        for s in shots:
            if s.n in want:
                out = _shot_dir(ep, s) / "previz" / "previz_config.toml"
                out.parent.mkdir(exist_ok=True)
                out.write_text(previz_config(ep, s, src[s.key][0]), encoding="utf-8", newline="\n")
                print("wrote %s" % out.relative_to(REPO))
        return 0

    bad, ctx = gate(ep, shots, vis_legacy)
    if bad and args.check:           # 059：--check 不因第一层（通读章等）没过就停——产物闸门也跑完、一起列出
        for b in bad:
            print("  ✗ " + b)
        late = []
        try:
            mds = _md_by_shot(ep, shots, ctx["src"], ctx["seams"], ctx["scen"])
            for g in (prompt_light.gate, carry_gate, shot_logic.gate,
                      lambda m: product_gates(ep, shots, m, ctx["src"]), wow_version_gate.gate):
                try:
                    g(mds)
                except SystemExit as e:
                    late.append(str(e))
        except SystemExit as e:
            late.append(str(e))
        for x in late:
            print("  ✗ " + x)
        print("闸门未过（第一层 %d 条%s）" % (len(bad), "；产物闸门 %d 组" % len(late) if late else "；产物闸门全过"))
        return 1
    if bad:
        for b in bad:
            print("  ✗ " + b)
        print("闸门未过（%d 条），不生成" % len(bad))
        return 1
    src, seams = ctx["src"], ctx["seams"]
    mds = _md_by_shot(ep, shots, src, seams, ctx["scen"])
    prompt_light.gate(mds)
    carry_gate(mds)
    shot_logic.gate(mds)
    product_gates(ep, shots, mds, src)
    wow_version_gate.gate(mds)

    if args.verify:
        problems = verify(ep_dir, shots, src)
        for b in problems:
            print("  ✗ " + b)
        print("%s 产物回读：%s" % (ep, "不通过" if problems else "通过（%d 镜）" % len(shots)))
        return 1 if problems else 0

    total = sum(src[s.key][0] for s in shots)
    print("%s 闸门全过：%d 镜，%gs" % (ep, len(shots), total))
    for s in shots:
        body = prompt_light.positive(mds["shot%02d" % s.n]) or ""
        print("  shot%02d %-10s %4gs  prompt %4d 字  %s%g→%s%g" % (
            s.n, s.title, src[s.key][0], len(body), s.jb[1], s.jb[0], s.jb[3], s.jb[2]))
    if args.check:
        return 0

    paths = [ep_dir / "shots" / ("shot%02d" % s.n) / ("shot%02d.md" % s.n) for s in shots]
    before = {p: (p.read_bytes() if p.is_file() else None) for p in paths}
    for s in shots:
        d = ep_dir / "shots" / ("shot%02d" % s.n)
        d.mkdir(parents=True, exist_ok=True)
        io.open(d / ("shot%02d.md" % s.n), "w", encoding="utf-8", newline="\n").write(mds["shot%02d" % s.n])
    io.open(ep_dir / "shotlist.md", "w", encoding="utf-8", newline="\n").write(
        shotlist(ep, shots, src, seams, generator))
    combined = "\n\n---\n\n".join(
        "# shot%02d《%s》 %gs\n\n%stext\n%s\n%s" % (
            s.n, s.title, src[s.key][0], FENCE, seedance_block(mds["shot%02d" % s.n]), FENCE)
        for s in shots)
    io.open(ep_dir / "all_shot_prompts.md", "w", encoding="utf-8", newline="\n").write(
        "# %s 全部 Seedance prompt（精简稿，生成物，勿手改——改 `%s` 重跑）\n\n%s\n" % (ep, generator, combined))
    problems = verify(ep_dir, shots, src)
    for b in problems:
        print("  ✗ " + b)
    if problems:
        print("产物回读不通过")
        return 1
    print("已写出 %d 个 shot + shotlist.md + all_shot_prompts.md → %s（回读通过）" % (
        len(shots), ep_dir.relative_to(REPO)))
    seedance_kit.after_write(before)
    return 0
