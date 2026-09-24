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
  ⑦ 参考行（rule 23）：每镜有 previz 与至少一个场景主体；入画的人都有锁定串、不入画的人不挂；路由键在盘上有目录
  ⑧ `动作:` 时间轴铺满镜长；有 `分镜:` 的镜，段数与时间轴自洽
写盘后 `verify()` 再从产物回读一遍（CLAUDE.md：闸门从最终产物回读，不校验中间变量）。
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import check_stage2  # noqa: E402
import prompt_light  # noqa: E402
import script_tools  # noqa: E402
import shot_logic  # noqa: E402
import shot_seam  # noqa: E402
import wow_version_gate  # noqa: E402

DRAMA = REPO / "ai_videos" / "shengji_zhilu"
A = DRAMA / "2_世界观人设"
CHARS, PROPS, SCENES = A / "characters", A / "props", A / "scenes"
STYLE_GUIDE, CASTING = A / "style_guide.md", A / "casting.md"
FENCE = "`" * 3

PROMPT_MAX = 5000
DUB_WPS = 2.5               # 配音时长目标按自然语速估；念不念得完由 script_tools 的 ≤3 词/秒闸门管
RATIO = "16:9"              # concept G9 ⑤

# 剧本说话人 → (人物卡目录 | None, casting.md 里的名字)
SPEAKERS: dict[str, tuple[str | None, str]] = {
    "Aaron": ("c1_小满", "Aaron"),
    "Duke": ("c2_不灭战魂", "Duke"),
    "McBride": ("c7_麦克布莱德中士", "Marshal McBride"),
    "Willem": ("c13_维里副队长", "Deputy Willem"),
    "Sammuel": ("c14_萨缪尔修士", "Brother Sammuel"),
    "Eagan": ("c15_伊根", "Eagan Peltskinner"),
    "Milly": ("c16_米莉", "Milly Osworth"),
    "Neals": ("c17_尼尔斯修士", "Brother Neals"),
    "Garrick": ("c18_加瑞克", "Garrick Padfoot"),
    "Kobold Worker": ("m1_狗头人", "Kobold"),
    "Kobold Laborer": ("m1_狗头人", "Kobold"),
    "Llane Beshere": (None, "Llane Beshere"),
}
# 红级（concept C3）：游戏名 / 公司名，任何地方都不许出现
IP_RED: tuple[str, ...] = ("魔兽世界", "魔兽", "暴雪", "Warcraft", "Blizzard", "WoW", "World of Warcraft")
# 黄级：世界内专名，text-only 实测前不进叙事字段（台词 / 角色键 / 参考行除外）
IP_YELLOW: tuple[str, ...] = ("暴风城", "北郡", "艾尔文", "圣骑士", "迪菲亚", "狗头人", "闪金镇", "联盟")
# `场景:` 是场景卡一句话锁定的逐字粘贴（卡里自带地名），不在此列；原词实测见 pending_user #3
NARRATIVE = ("情节", "镜头", "分镜", "镜内状态", "走位", "动作", "光线", "节奏")

_SPAN = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s")
_HEX = re.compile(r"#[0-9a-fA-F]{6}")


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


def _bg_dir(bg: str) -> Path:
    for dirpath, dirs, files in os.walk(SCENES):
        for d in dirs:
            if d.startswith(bg + "_") and (Path(dirpath) / d / (d + ".md")).is_file():
                return Path(dirpath) / d
    raise SystemExit("场景主体 %s 在 %s 下找不到" % (bg, SCENES))


def scene_lock(bg: str) -> str:
    d = _bg_dir(bg)
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
    aura: str                         # none | low | first | out | back | high —— 主角脚下光环
    holy: str = ""                    # 本镜圣光表现的条件分句（空 ＝ 无圣光镜）
    cut: str = ""                     # `分镜:` 行（无镜内切镜留空）
    ledger: str = ""                  # `镜内状态:` 行
    style_extra: str = ""             # 本镜条件渲染分句（时段 / 光源 / 室内外）
    neg: tuple[str, ...] = ()         # 本镜追加负向（条件组名用 `@组名`）
    jbnote: str | None = None
    moods: dict[int, str] = field(default_factory=dict)   # 台词序号(1 起) → 配音情绪 / 语速
    dub_note: str = ""

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
            off = "画外" in tail or "隔壁" in tail or "信 ·" in tail
            kind = "画外" if off else ("内心独白" if k == "OS" else "正常台词")
            lines.append(Line(who, kind, txt, gloss,
                              (float(w.group(1)), float(w.group(2))) if w else None))
        out[s.key] = (s.dur, lines)
    return out


# ─────────────────────────── 渲染 ───────────────────────────

AURA = {
    "none": "主角脚下没有光环，人物不自发光",
    "low": "主角脚下一圈低亮度贴地柔光（不发散、不照亮周围、边缘柔和），人物本身不自发光",
    "first": "主角脚下的贴地柔光在本镜中段第一次亮起（此前没有），低亮度、不发散",
    "out": "主角脚下的贴地柔光在本镜最后几秒熄灭",
    "back": "主角脚下的贴地柔光在本镜中段闪了闪、重新亮起，低亮度",
    "high": "主角脚下的贴地光圈明显扩大、罩住并肩两人的脚",
}


def _handles(s: Shot, lines: list[Line]) -> list[str]:
    h = ["`shot%02d_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`" % s.n]
    h += ["`%s(场景主体)=>@`" % plate_stem(p) for p in s.plates]
    h += ["`%s(人物·脸与造型)=>@`" % c for c in s.chars]
    h += ["`%s(物件锚点)=>@`" % p for p in s.props]
    seen: list[str] = []
    for l in lines:
        if l.who not in seen:
            seen.append(l.who)
    h += ["`%s声音(voice_id %s)=>@`" % (w, voice_id(w)) for w in seen]
    return h


def _lines_field(lines: list[Line]) -> str:
    if not lines:
        return "本镜无台词。"
    parts = []
    for l in lines:
        lip = {"正常台词": "口型对说话人", "内心独白": "嘴唇不动", "画外": "画外声，画面里无人对口型"}[l.kind]
        at = "%g–%gs" % l.win if l.win else ""
        parts.append("%s %s（%s·%s）：%s" % (at, l.who, l.kind, lip, l.text))
    return "；".join(parts) + "。台词只供口型与配音参考，画面不出现任何文字。"


def _negatives(s: Shot) -> str:
    out = [neg_base()]
    for n in s.neg:
        out.append(neg_group(n[1:]) if n.startswith("@") else n)
    return "，".join(out)


def video_prompt(s: Shot, lines: list[Line], secs: float) -> str:
    chars = "；".join("%s＝%s%s" % (c, char_lock(c), ("；本镜状态：" + s.state[c]) if c in s.state else "")
                      for c in s.chars) or "画面里没有人"
    props = "；".join("%s＝%s" % (p, prop_lock(p)) for p in s.props)
    usage = ("previz 只锁运动、几何关系与动作时刻，不取长相；人物参考只锁长相与服装，不锁姿势与机位；"
             "场景参考只锁材质与光的性格，几何以 previz 为准；声音参考只锁音色。保持角色服装、场景与光线一致，只生成本镜的运动")
    parts = [
        "参考: " + "、".join(_handles(s, lines)),
        "参考用法: " + usage + "。",
        "角色: " + chars + ("；物件：" + props if props else ""),
        "情节: " + s.plot,
        "场景: " + "、".join(scene_lock(p.split("-")[0]) for p in dict.fromkeys(s.plates)),
        "镜头: " + s.camera,
    ]
    if s.cut:
        parts.append("分镜: " + s.cut + "。镜内硬切不加任何转场效果，不打断本镜同一条时间线、环境声与光")
    if s.ledger:
        parts.append("镜内状态: " + s.ledger)
    parts += [
        "走位: " + s.blocking,
        "动作: " + s.action,
        "台词: " + _lines_field(lines),
        "光线: " + s.light + "；" + AURA[s.aura] + (("；" + s.holy) if s.holy else
                                                    "；本镜除上述之外没有任何圣光特效，武器不发光"),
        "节奏: " + s.rhythm,
        "渲染样式: " + style_base() + ("，" + s.style_extra if s.style_extra else ""),
        "比例: " + RATIO,
        "时长: %gs" % secs,
        "负面词: " + _negatives(s),
    ]
    return "\n".join(parts)


def dub_blocks(s: Shot, lines: list[Line]) -> str:
    if not lines:
        return "## 台词配音 prompt\n\n本镜无台词，不配音。只保留环境声。\n"
    out = ["## 台词配音 prompt", ""]
    for i, l in enumerate(lines, 1):
        words = len(script_tools._EN_WORD.findall(l.text))
        out += [FENCE + "text",
                "01集%02d镜 · 台词配音 %d" % (s.n, i),
                "角色: %s" % l.who,
                "音色(锁定·全剧复用 · %s): 见 casting.md 同名行" % voice_id(l.who),
                "情绪: %s" % s.moods.get(i, s.emotion),
                "语速: 自然口语，约 %.1f 词/秒" % DUB_WPS,
                "类型: %s" % l.kind,
                "台词: %s" % l.text,
                "中文意思: %s" % l.gloss,
                "时间窗: %s" % ("%g–%gs" % l.win if l.win else "—"),
                "时长目标: %.1fs" % max(0.6, words / DUB_WPS),
                FENCE, ""]
    out.append("> voice_id 全剧锁定（`casting.md`）；画外与内心独白也配音入片，只是画面里无人对口型。"
               + ("\n>\n> **配音注**：%s" % s.dub_note if s.dub_note else ""))
    return "\n".join(out) + "\n"


def render(ep: str, s: Shot, lines: list[Line], secs: float, seam_ctx: str) -> str:
    prompt = video_prompt(s, lines, secs)
    ups = "\n".join("  - %s" % h.strip("`").replace("=>@", "") for h in _handles(s, lines))
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
- **场景**: {"、".join(plate_stem(p) for p in s.plates)}
- **剧本**: `../../../../../4_剧本/episodes/{ep}/script.md` § 镜 {s.key}；台词逐句同源（生成器从剧本读，不另抄）
- **Reference uploads**（⚠ previz 与图尚未出，先占位）:
{ups}

## 视频 prompt

{FENCE}text
{prompt}
{FENCE}

字数: {len(prompt)} / {PROMPT_MAX}

{dub_blocks(s, lines)}"""


# ─────────────────────────── 闸门 ───────────────────────────

def _field_line(prompt: str, name: str) -> str:
    for ln in prompt.split("\n"):
        if ln.startswith(name + ":"):
            return ln
    return ""


def gate(ep: str, shots: tuple[Shot, ...]) -> tuple[list[str], dict]:
    bad: list[str] = []
    src = script_lines(ep)
    keys = [s.key for s in shots]
    if keys != list(src):
        bad.append("镜号与剧本不一致：生成器 %s / 剧本 %s" % (keys, list(src)))
    for s in shots:
        if s.key not in src:
            continue
        secs, lines = src[s.key]
        tag = "shot%02d" % s.n
        p = video_prompt(s, lines, secs)
        if len(p) > PROMPT_MAX:
            bad.append("%s: prompt %d 字 > %d" % (tag, len(p), PROMPT_MAX))
        if _HEX.search(p):
            bad.append("%s: prompt 内出现 hex 色值" % tag)
        if re.search(r"=>@\s*[0-9图第]", p):
            bad.append("%s: `参考:` 代填了槽位号，必须裸 `=>@`" % tag)
        for w in IP_RED:
            if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w), p):
                bad.append("%s: 红级 IP 名「%s」进了 prompt" % (tag, w))
        for fld in NARRATIVE:
            ln = _field_line(p, fld)
            for w in IP_YELLOW:
                if w in ln:
                    bad.append("%s: 叙事字段 `%s:` 出现黄级专名「%s」（concept C3，未实测前用描述代替）" % (tag, fld, w))
        spans = [(float(a), float(b)) for a, b in _SPAN.findall(s.action)]
        if not spans or abs(max(b for _, b in spans) - secs) > 0.01:
            bad.append("%s: `动作:` 时间轴没有铺满 %gs" % (tag, secs))
        in_frame = set(s.chars)
        for l in lines:
            card = SPEAKERS.get(l.who, (None, ""))[0] if l.who in SPEAKERS else "?"
            if l.who not in SPEAKERS:
                bad.append("%s: 说话人 %s 不在 SPEAKERS 表" % (tag, l.who))
            elif l.kind == "正常台词" and card and card not in in_frame:
                bad.append("%s: %s 对口型说话，却没有入画（chars 缺 %s）" % (tag, l.who, card))
        if "画面里没有人" in s.blocking and s.chars:
            bad.append("%s: `走位:` 写着画面里没有人，却挂了人物参考（rule 23 ②）" % tag)
        if not s.plates:
            bad.append("%s: 没有挂任何场景主体（rule 23）" % tag)
        if s.aura not in AURA:
            bad.append("%s: aura=%s 不在 %s" % (tag, s.aura, "/".join(AURA)))
    try:
        seams = shot_seam.audit([{"n": s.n, "jb": s.jb, "jbcam": s.jbcam, "jbnote": s.jbnote} for s in shots])
    except SystemExit as e:
        bad.append(str(e))
        seams = []
    return bad, {"src": src, "seams": seams}


def _md_by_shot(ep: str, shots: tuple[Shot, ...], src: dict, seams: list) -> dict[str, str]:
    ctx = {sm.next_n: sm.context() for sm in seams}
    return {"shot%02d" % s.n: render(ep, s, src[s.key][1], src[s.key][0],
                                     ctx.get(s.n, "集首镜，硬切（独立首帧）。"))
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


def run(ep: str, shots: tuple[Shot, ...], generator: str, argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只跑闸门，不写盘")
    ap.add_argument("--verify", action="store_true", help="回读已写出的产物")
    args = ap.parse_args(argv)
    ep_dir = DRAMA / "5_6_分镜与prompt" / "episodes" / ep

    bad, ctx = gate(ep, shots)
    if bad:
        for b in bad:
            print("  ✗ " + b)
        print("闸门未过（%d 条），不生成" % len(bad))
        return 1
    src, seams = ctx["src"], ctx["seams"]
    mds = _md_by_shot(ep, shots, src, seams)
    prompt_light.gate(mds)
    shot_logic.gate(mds)
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

    for s in shots:
        d = ep_dir / "shots" / ("shot%02d" % s.n)
        d.mkdir(parents=True, exist_ok=True)
        io.open(d / ("shot%02d.md" % s.n), "w", encoding="utf-8", newline="\n").write(mds["shot%02d" % s.n])
    io.open(ep_dir / "shotlist.md", "w", encoding="utf-8", newline="\n").write(
        shotlist(ep, shots, src, seams, generator))
    combined = "\n\n---\n\n".join(
        "# shot%02d《%s》 %gs\n\n%stext\n%s\n%s" % (
            s.n, s.title, src[s.key][0], FENCE, prompt_light.positive(mds["shot%02d" % s.n]), FENCE)
        for s in shots)
    io.open(ep_dir / "all_shot_prompts.md", "w", encoding="utf-8", newline="\n").write(
        "# %s 全部分镜 prompt（生成物，勿手改——改 `%s` 重跑）\n\n%s\n" % (ep, generator, combined))
    problems = verify(ep_dir, shots, src)
    for b in problems:
        print("  ✗ " + b)
    if problems:
        print("产物回读不通过")
        return 1
    print("已写出 %d 个 shot + shotlist.md + all_shot_prompts.md → %s（回读通过）" % (
        len(shots), ep_dir.relative_to(REPO)))
    return 0
