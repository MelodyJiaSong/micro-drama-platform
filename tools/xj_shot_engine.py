# -*- coding: utf-8 -*-
"""Shared shot engine for the 仙剑奇侠传一 episodes.

One episode is a thin data file (`gen_shots_xjN.py`) holding its `SHOTS` tuple and calling
`run()`. The prompt layout, the gates and the product-readback verifier live here once.
With 81 episodes planned, copying a 250-line engine per episode is exactly how a rule ends
up enforced in episode 3 and quietly missing in episode 40.

Gates run before anything is written (ai_video.md「审计要左移进生成器」), and `verify()`
re-reads the files that were written, because a gate over a recomputed value cannot see a
broken template, a truncated write, or a later hand edit (CLAUDE.md 2026-09-20).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRAMA = REPO / "ai_videos" / "xianjian_yi"

PROMPT_MAX = 5000
SPEECH_MAX = 5.0            # 字 / 秒
SHOT_MIN, SHOT_MAX = 3, 30  # 秒

LOCK_C1 = "高马尾靛蓝发带青年，素白交领赭褐披巾靛蓝短打，笑意飞扬青涩"
LOCK_C8 = "五十许花白散发歪道髻，青灰粗布道袍洗白带陈年酒渍下摆撕口，腰系麻绳挂磨亮深褐酒葫芦，赤脚破草鞋，眼半耷拉"
LOCK_C10 = "五十许圆脸妇人，花白圆髻素木簪，靛蓝粗布交领挽袖，土黄褐围裙带油渍，手掌厚茧指节粗"
LOCK_C21 = "四十许精瘦男子，深靛青布帕缠头，深靛青对襟衣镶几何折线织带，深褐粗麻短褂，宽腰带挂素银环扣与鼓皮囊"
LOCK_C22 = "佝偻老妪深灰破麻斗篷压低兜帽面隐阴影，拄未去皮歪曲木杖，强逆光压成剪影仅边缘冷白轮廓光"
LOCK_BG1 = "深栗褐色老木穿斗构架挑空大堂，白灰粉墙地脚泛潮，青灰方砖墁地磨出暗光，二层木回廊细棂栏杆，屋架露明檩椽举折内凹"
LOCK_BG2 = "深栗褐色木板墙小客房，深色木楼板积细灰，简陋木床被褥未叠，东侧步步锦木格窗切出平行晨光带"
LOCK_BG3 = "深栗褐色临空回廊，左侧方望柱圆棱寻杖细棂栏杆，右侧四扇同款板门带铁环，深色木楼板中央一条磨痕通向尽头楼梯"
LOCK_BG4 = "无源平光灰白乱石坡，棱角碎石铺至地平线零彩度，贴地薄灰雾顺坡流动，坡脊线外浓雾吞没一切"
LOCK_P1 = "浅色杂木自削木剑，通体柴刀削面棱线未刨光，钝圆剑尖不开刃，麻绳缠扁木条护手，握位手汗浸深"
LOCK_P2 = "旧熟铁锅铲，铲面灶火熏黑带麻点锈斑，前缘磨出银白亮边，木柄油润近铲头焦黑"
LOCK_P3 = "粗陶提梁酒壶，暗黄褐釉只施至腹下露粗陶胎成釉线，细开片，短直流嘴，竹提梁握处磨出竹肉，壶肩旧磕缺"

KNOWN_CHARS = frozenset({"c1_江湖游侠", "c8_醉道人", "c10_市井大娘",
                         "c21_南疆行商头领", "c22_梦中老妪", "c23_南疆行商随从"})
IP_NAMES = ("李逍遥", "李大娘", "婶婶", "罗刹鬼婆", "苗人", "仙剑", "酒剑仙")

STYLE_BASE = "电影级实拍质感，35mm 胶片颗粒，浅景深，自然肤质，无字幕无水印无logo，无动漫卡通质感，16:9"
NEG_BASE = ("人脸变形、五官漂移、多余发光特效、画面文字、畸形肢体、夸张金光、现代服饰、字幕、水印、logo、"
            "动漫卡通质感、塑料感皮肤、眼睛发光、瞳孔发光、多余手指、断肢、现代建筑、西式服装、"
            "同一角色出现两次、两个相同人物")

_FENCE_RE = re.compile(r"^```text\n(.*?)\n^```", re.M | re.S)
_SPAN_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)s")
_REQUIRED_FIELDS = ("参考:", "参考用法:", "角色:", "情节:", "场景:", "镜头:", "走位:",
                    "动作:", "台词:", "光线:", "节奏:", "渲染样式:", "比例:", "时长:", "负面词:")


@dataclass(frozen=True)
class Line:
    who: str
    kind: str               # 正常台词 / 内心独白 / 画外
    text: str
    voice: str
    mood: str
    secs: float


@dataclass(frozen=True)
class Shot:
    n: int
    title: str
    secs: int
    seam: str
    scene_key: str
    scene_lock: str
    jingbie: str
    seam_note: str
    refs: tuple[str, ...]
    chars: tuple[tuple[str, str], ...]
    plot: str
    camera: str
    blocking: str
    action: str
    light: str
    rhythm: str
    style_extra: str
    neg_extra: str
    lines: tuple[Line, ...] = ()
    inner_cut: str = ""
    inner_state: str = ""
    source: str = ""
    dub_note: str = ""      # 配音导演注：mood 放不下的整镜级叮嘱
    last_shot: bool = False

    @property
    def carries_lastframe(self) -> bool:
        return not self.last_shot

    @property
    def speech_chars(self) -> int:
        return sum(len(l.text) for l in self.lines)


def video_prompt(s: Shot) -> str:
    refs = "、".join(f"`{r}=>@`" for r in s.refs)
    chars = "；".join(f"{k}＝{v}" for k, v in s.chars)
    lines = "；".join(f"{l.who}（{l.kind}）「{l.text}」" for l in s.lines) or "本镜无台词"
    lip = ("内心独白（OS）口不动、不出口型，其余台词正常口型。"
           if any(l.kind == "内心独白" for l in s.lines) else "台词正常口型。")
    usage = ("角色参考图只锁长相与服装，不锁姿势与机位；场景参考图只锁材质与光的性格，"
             "几何以本条 走位/镜头 为准")
    if s.seam.startswith("承接"):
        usage += "；本镜首帧＝上一镜末帧，构图与光必须从该帧无缝接起"
    parts = [
        f"参考: {refs}",
        f"参考用法: {usage}。",
        f"角色: {chars}",
        f"情节: {s.plot}",
        f"场景: {s.scene_lock}",
        f"镜头: {s.camera}",
    ]
    if s.inner_cut:
        parts.append(s.inner_cut)
    if s.inner_state:
        parts.append(s.inner_state)
    parts += [
        f"走位: {s.blocking}",
        f"动作: {s.action}",
        f"台词: {lines}。{lip}",
        f"光线: {s.light}",
        f"节奏: {s.rhythm}",
        f"渲染样式: {STYLE_BASE}，{s.style_extra}",
        "比例: 16:9",
        f"时长: {s.secs}s",
        f"负面词: {NEG_BASE}、{s.neg_extra}",
    ]
    return "\n".join(parts)


def dub_block(s: Shot) -> str:
    if not s.lines:
        return "## 台词配音 prompt\n\n本镜无台词，不配音。只保留环境声。\n"
    rows = "\n".join(
        f"| {i} | {l.who} | `{l.voice}` | {l.kind} | {l.mood} | 「{l.text}」 | {l.secs}s |"
        for i, l in enumerate(s.lines, 1))
    return ("## 台词配音 prompt\n\n"
            "| # | 角色 | voice_id | 类型 | 情绪／语速 | 台词 | 时长目标 |\n|---|---|---|---|---|---|---|\n"
            f"{rows}\n\n"
            "> voice_id 全片锁定不换（登记处：`_series/casting.md`）；"
            "**内心独白也必须配音入片**，只是口不动。\n"
            + (f">\n> **配音注**：{s.dub_note}\n" if s.dub_note else ""))


def render(ep: str, s: Shot) -> str:
    prompt = video_prompt(s)
    tail = (f"shot{s.n:02d}_lastframe.png（下游 shot{s.n + 1:02d} 承接本镜末帧；重生时用本文件钉住末帧）"
            if s.carries_lastframe else "无（本集末镜，无下游承接镜）")
    return f"""---
episode: {ep}
shot: {s.n:02d}
title: {s.title}
duration_s: {s.secs}
seam: {"承接" if s.seam.startswith("承接") else "硬切"}
effects_tier: {"T2" if "T2" in s.style_extra or "御剑" in s.action else "T0"}
source: {s.source}
---

# {ep} · shot{s.n:02d}《{s.title}》

## Shot context

- **衔接**: {s.seam}
- **尾帧锁定**: {tail}
- **接缝**: {s.seam_note.removeprefix("接缝: ")}
- **景别档**: {s.jingbie}
- **场景**: {s.scene_key}
- **原作出处**: {s.source}
- **剧本**: `../../../4_剧本/script.md` § shot{s.n:02d}；台词逐句同步 `../../../4_剧本/dialogue.md`

## 视频 prompt

```text
{prompt}
```

字数: {len(prompt)} / {PROMPT_MAX}

{dub_block(s)}"""


def dialogue_doc(ep: str, shots: tuple[Shot, ...]) -> str:
    """Emit 4_剧本/dialogue.md from the shot data.

    A hand-kept dialogue.md is a second copy of every line, and a copy drifts
    (ai_video.md rule 4i ①). The shot table is the one source; this file is its view.
    """
    out = [f"# {ep} · 台词表（生成物，勿手改——改 `tools/gen_shots_{ep}.py`）", "",
           "> 与各 shot 的 `台词:` 字段同源，不可能不一致。",
           "> 类型：`正常台词` ／ `内心独白`（OS，口不动，仍须配音）／ `画外`（人不在画内）。",
           "> voice_id 登记处：`../../_series/casting.md`。", ""]
    voices: dict[str, str] = {}
    for s in shots:
        out.append(f"## shot{s.n:02d} · {s.title}（{s.secs}s）")
        out.append("")
        if not s.lines:
            out += ["（无台词）", ""]
            continue
        out.append("| # | 角色 | 类型 | 台词 | 情绪／语速 | 时长目标 |")
        out.append("|---|---|---|---|---|---|")
        for i, l in enumerate(s.lines, 1):
            out.append(f"| {i} | {l.who} | {l.kind} | 「{l.text}」 | {l.mood} | {l.secs}s |")
            voices[l.who] = l.voice
        dub = sum(l.secs for l in s.lines)
        out += ["", f"> 配音合计 {dub:.1f}s / 镜长 {s.secs}s；"
                    f"语速 {s.speech_chars / s.secs:.2f} 字/秒（上限 {SPEECH_MAX}）。"]
        if s.dub_note:
            out.append(f">\n> **配音注**：{s.dub_note}")
        out.append("")
    out += ["## 本集用到的 voice_id", "", "| 角色 | voice_id |", "|---|---|"]
    out += [f"| {k} | `{v}` |" for k, v in sorted(voices.items())]
    out.append("")
    return "\n".join(out)


def gate(shots: tuple[Shot, ...]) -> list[str]:
    bad: list[str] = []
    for s in shots:
        p = video_prompt(s)
        if len(p) > PROMPT_MAX:
            bad.append(f"shot{s.n:02d}: 视频 prompt {len(p)} 字 > {PROMPT_MAX}")
        rate = s.speech_chars / s.secs
        if rate > SPEECH_MAX:
            bad.append(f"shot{s.n:02d}: 语速 {rate:.2f} 字/秒 > {SPEECH_MAX}")
        dub = sum(l.secs for l in s.lines)
        if dub > s.secs:
            bad.append(f"shot{s.n:02d}: 配音时长之和 {dub:.1f}s > 镜长 {s.secs}s")
        if not (SHOT_MIN <= s.secs <= SHOT_MAX):
            bad.append(f"shot{s.n:02d}: 时长 {s.secs}s 不在 {SHOT_MIN}–{SHOT_MAX}s")
        if s.n == 1 and not s.seam.startswith("硬切"):
            bad.append("shot01: 集首镜必须是独立首帧硬切")
        if s.n > 1 and not s.seam.startswith("承接"):
            bad.append(f"shot{s.n:02d}: 非首镜必须承接（本片 divergence，见 proposal §2.1）")
        if "@1" in p or "@图" in p:
            bad.append(f"shot{s.n:02d}: `参考:` 出现代填槽位号，必须裸 `=>@`")
        if re.search(r"#[0-9a-fA-F]{6}", p):
            bad.append(f"shot{s.n:02d}: prompt 内出现 hex 色值")
        if s.inner_cut and not s.inner_state:
            bad.append(f"shot{s.n:02d}: 有镜内切镜但缺 `镜内状态:`")
        spans = [(float(a), float(b)) for a, b in _SPAN_RE.findall(s.action)]
        if not spans:
            bad.append(f"shot{s.n:02d}: `动作:` 没有任何时间轴标注")
        elif abs(max(b for _, b in spans) - s.secs) > 0.01:
            bad.append(f"shot{s.n:02d}: 动作时间轴只到 {max(b for _, b in spans):.0f}s，"
                       f"镜长 {s.secs}s——末尾无动作描述")
        locked = {k for k, _ in s.chars}
        on_screen = {k for k in KNOWN_CHARS if k in s.blocking}
        on_screen |= {l.who for l in s.lines if l.kind != "画外"}
        for who in sorted(on_screen - locked):
            bad.append(f"shot{s.n:02d}: {who} 入画但 chars 缺其锁定串——承接链上会长成两个人")
        in_plot = {k for k in KNOWN_CHARS if k in s.plot}
        for who in sorted(locked - on_screen - in_plot):
            bad.append(f"shot{s.n:02d}: {who} 有锁定串却不入画——白占字数")
        narrative = " ".join((s.plot, s.camera, s.blocking, s.action, s.light, s.rhythm))
        for name in IP_NAMES:
            if name in narrative:
                bad.append(f"shot{s.n:02d}: 叙事字段出现 IP 专名「{name}」——只用锁定键或代词")
    ns = [s.n for s in shots]
    if ns != list(range(1, len(shots) + 1)):
        bad.append(f"镜号必须从 1 连续编号，实得 {ns}")
    if sum(1 for s in shots if s.last_shot) != 1 or not shots[-1].last_shot:
        bad.append("必须且只能由最后一镜标 last_shot=True")
    return bad


def verify(ep_dir: Path, shots: tuple[Shot, ...]) -> list[str]:
    bad: list[str] = []
    for s in shots:
        f = ep_dir / "shots" / f"shot{s.n:02d}" / f"shot{s.n:02d}.md"
        if not f.is_file():
            bad.append(f"shot{s.n:02d}: 产物不存在 {f}")
            continue
        text = f.read_text(encoding="utf-8")
        m = _FENCE_RE.search(text)
        if m is None:
            bad.append(f"shot{s.n:02d}: 产物里找不到 ```text 块")
            continue
        body = m.group(1)
        for fld in _REQUIRED_FIELDS:
            if ("\n" + fld) not in ("\n" + body):
                bad.append(f"shot{s.n:02d}: 产物缺字段 `{fld}`")
        if len(body) > PROMPT_MAX:
            bad.append(f"shot{s.n:02d}: 产物 prompt {len(body)} 字 > {PROMPT_MAX}")
        if re.search(r"#[0-9a-fA-F]{6}", body):
            bad.append(f"shot{s.n:02d}: 产物含 hex 色值")
        if re.search(r"=>@\s*[0-9图第]", body):
            bad.append(f"shot{s.n:02d}: 产物 `参考:` 代填了槽位号")
        if "比例: 16:9" not in body:
            bad.append(f"shot{s.n:02d}: 产物比例不是 16:9")
        if f"时长: {s.secs}s" not in body:
            bad.append(f"shot{s.n:02d}: 产物时长与表不一致（应 {s.secs}s）")
        if s.carries_lastframe and "尾帧锁定" not in text:
            bad.append(f"shot{s.n:02d}: 产物缺尾帧锁定行")
        if s.n > 1 and "承接 shot" not in text:
            bad.append(f"shot{s.n:02d}: 产物未声明承接")
        if s.lines and "## 台词配音 prompt" not in text:
            bad.append(f"shot{s.n:02d}: 有台词却无配音块")
        for l in s.lines:
            if l.text not in text:
                bad.append(f"shot{s.n:02d}: 台词未出现在产物中「{l.text[:14]}…」")
        if any(l.kind == "内心独白" for l in s.lines) and "口不动" not in body:
            bad.append(f"shot{s.n:02d}: 有内心独白但产物未写明口不动")
        for line in body.splitlines():
            if line.startswith(("台词:", "角色:", "参考:")):
                continue
            for name in IP_NAMES:
                if name in line:
                    bad.append(f"shot{s.n:02d}: 产物 `{line[:6]}` 行出现 IP 专名「{name}」")
    combined = ep_dir / "all_shot_prompts.md"
    if not combined.is_file():
        bad.append("all_shot_prompts.md 不存在")
    else:
        ct = combined.read_text(encoding="utf-8")
        for s in shots:
            if f"shot{s.n:02d}" not in ct:
                bad.append(f"all_shot_prompts.md 缺 shot{s.n:02d}")
    return bad


def run(ep: str, shots: tuple[Shot, ...], argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只跑闸门，不写文件")
    ap.add_argument("--verify", action="store_true", help="回读已写出的产物校验")
    args = ap.parse_args(argv)
    ep_dir = DRAMA / ep / "5_6_分镜与prompt"

    if args.verify:
        problems = verify(ep_dir, shots)
        for b in problems:
            print(f"  ✗ {b}")
        print(f"{ep} 产物回读校验：" + ("不通过" if problems else f"通过（{len(shots)} 个文件）"))
        return 1 if problems else 0

    problems = gate(shots)
    for b in problems:
        print(f"  ✗ {b}")
    if problems:
        print("闸门未过，不生成")
        return 1
    total = sum(s.secs for s in shots)
    print(f"{ep} 闸门全过：{len(shots)} 镜，合计 {total}s = {total // 60}分{total % 60:02d}秒")
    for s in shots:
        print(f"  shot{s.n:02d} {s.title:10} {s.secs:>3}s  prompt {len(video_prompt(s)):>4}字  "
              f"语速 {s.speech_chars / s.secs:.2f}字/秒  {s.seam[:2]}")
    if args.check:
        return 0

    for s in shots:
        d = ep_dir / "shots" / f"shot{s.n:02d}"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"shot{s.n:02d}.md").write_text(render(ep, s), encoding="utf-8")
    combined = "\n\n---\n\n".join(
        f"# shot{s.n:02d}《{s.title}》 {s.secs}s\n\n```text\n{video_prompt(s)}\n```" for s in shots)
    (ep_dir / "all_shot_prompts.md").write_text(
        f"# {ep} 全部分镜 prompt（生成物，勿手改——改 `tools/gen_shots_{ep}.py`）\n\n{combined}\n",
        encoding="utf-8")
    dlg = DRAMA / ep / "4_剧本" / "dialogue.md"
    dlg.parent.mkdir(parents=True, exist_ok=True)
    dlg.write_text(dialogue_doc(ep, shots), encoding="utf-8")
    print(f"已写出 {len(shots)} 个 shot 文件 + all_shot_prompts.md + 4_剧本/dialogue.md → {ep_dir.parent}")
    return 0
