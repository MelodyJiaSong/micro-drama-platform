# -*- coding: utf-8 -*-
"""剪辑决定 `{集}/cut/edl.toml`（唯一剪辑出处，git 跟踪）：起草、候选切点、校验、解析成事件表。

    python tools/post/edl.py init <剧> <ep> [--shots 1-6,9] [--force]   # v1 草稿：整镜顺接，钉当前 take 的 sha 前 12 位
    python tools/post/edl.py candidates <剧> <ep>             # → post/cut/candidates.json + 终端表（切点只许从这里挑）
    python tools/post/edl.py verify <剧> <ep> [--proxy-ok]    # V1–V10 全部报完；有一处不过即 exit 1
    python tools/post/edl.py plan <剧> <ep>                   # → post/cut/plan.json（秒，取整到 1/FPS），给 finish_ep / subs / qc
命令也可以放在最后：`edl.py <剧> <ep> verify`。

锚点 in / out：start | end | 秒数 | "line:N.start" / "line:N.end"（第 N 句实测起止，可带 ±秒）| "cut:K"（第 K 个镜内切点，
没有实测就用计划）。按该事件 take 的对齐缓存（align.cache_path）解析；当前出片缺缓存就用 ALIGN_PYTHON 跑 align.py 补。
end＝take 按 FPS 转恒定帧率后的末帧之后（缓存的 frames），不是容器时长 × FPS。
line: / cut: 按编号取句子与切点：md 改了台词或切点、align.py 重算后编号会挪、句子起止会变，所以用了它们的事件要写 basis
（candidates 给出的这条 take 的编号与起止指纹），对不上即报错——按旧编号切新缓存，切点会悄悄挪到别的句子上或别的时刻。
键写错、fps ≠ pc.FPS、锚点解析不到、basis 对不上、in ≥ out：报错停下，写明哪个事件、哪个锚点。
钉的 take 不是当前出片：plan / candidates 报错停下；verify 记 V1 不过（旧 take 的缓存还在就照它把别的项查完）。
- take 自己的首尾不是剪出来的切点，V2 不查；新接缝要豁免时 match_ok 写在接缝后面那个事件上。
- 承接缝（后一镜 seam: 承接）整镜顺接时两侧各剪一小段（共用的接缝帧与缓动）；edl 还表达不了，整镜相接的承接缝 V4 记不过。
- 剧本里的窗（场景展示、画面动作的带时刻节拍、目标账本的画面锚点）只在剧本这一镜与 take 时长差 ≤ SYNC_TOL 时套用：
  剧本改过、还没重出片的镜按查不了处理（场景展示退回镜首连续无词区间近似并注明），不悄悄放过。
- 批准过的版本号记在 cut/approved.json（任何命令读到 status = approved / locked 就记上）：V10 的乐观锁拿它比 base_version。
- 还没有 edl.toml 时，candidates 按 init 会写的整镜事件列（不落 edl）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import tomllib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import post_common as pc
import align          # 对齐缓存的位置、格式版本与句子状态只在 align.py 定义
import goal_ledger    # tools/ 下的，post_common 已把 tools/ 加进 sys.path
import script_tools
import shot_seam

EDL_NAME = "edl.toml"
APPROVED_NAME = "approved.json"
PLAN_NAME = "plan.json"
CANDIDATES_NAME = "candidates.json"
ALIGN_PY = Path(align.__file__)
SCRIPT_DIR = ("4_剧本", "episodes")                # 剧本在剧目录里的位置（szzl 引擎、render_review 同一约定）
GAP_MIN = 0.15
WORD_MARGIN = 0.08
MIN_EVENT = 1.0
MIN_FLASH = 0.6
FLASH_MAX = 4.0
FLASH_MAX_N = 2
LAUGH_GAP = 0.8
SYNC_TOL = 0.5          # 剧本这一镜与 take 的时长差（秒）在这以内，剧本窗才套得上（出片是整秒 + 容器零头）
LAUGH_TAG = "好笑"                                 # viewing_packet.TAGS 的键
TOP3_HEAD = "## 最该改的 3 处"                      # 整集观感 review.md 的固定小节（ai_videos__整集观感）
CMDS = ("init", "candidates", "verify", "plan")
STATUSES = ("draft", "approved", "locked")
KINDS = ("shot", "flash")
NOTE_STATUSES = ("open", "patched", "ticket", "waived")
LINE_STATUSES = align.STATUSES
WORDED = align.TIMED
TOP_KEYS = frozenset({"version", "base_version", "status", "approved_by", "fps", "event", "note"})
EVENT_KEYS = frozenset({"id", "shot", "take", "in", "out", "kind", "why", "match_ok", "quiet_ok", "basis"})
NOTE_KEYS = frozenset({"ref", "status", "detail"})
ALIGN_KEYS = frozenset({"version", "shot", "take_sha256", "duration", "frames", "lines", "speech", "cuts"})
LINE_KEYS = frozenset({"idx", "text", "status", "planned", "start", "end", "words"})
ANCHOR_FIELDS: dict[str, tuple[str, ...]] = {        # goals.toml 里「镜号 + 原文片段」的字段（goal_ledger.check 查的同一批）
    "goal": ("stated", "accepted", "resolved"),
    "skill": ("idea", "trigger", *goal_ledger.CORE_NEED, "learned", "used", "rule", "casts"),
    "casting": ("taught", "cost"),
}
ANCHOR_RE = re.compile(r"(?:line:(\d+)\.(start|end)|cut:(\d+))(?:([+-])(\d+(?:\.\d+)?))?")
TAKE_RE = re.compile(r"[0-9a-f]{%d}" % pc.TAKE_ID_LEN)
BASIS_LEN = 12
BASIS_RE = re.compile(r"[0-9a-f]{%d}" % BASIS_LEN)
JB_NAME = r"(远景|全景|中景|近景|特写)"
# shot md 的「景别档」行（各镜生成器写的 `远景0.12 → 特写1.2（机位 `甲` → `乙`）`；有的带 起幅 / 落幅 字样与粗体）
JB_RE = re.compile(r"\**景别档\**[:：]\s*(?:起幅\s*)?\**\s*" + JB_NAME + r"\s*([\d.]+)\**\s*→\s*(?:落幅\s*)?\**\s*" + JB_NAME
                   + r"\s*([\d.]+)\**[^`\n]*`([^`]+)`\s*→\s*`([^`]+)`")
TOP3_ITEM_RE = re.compile(r"^(\d+)\.\s", re.M)
EPS = 1e-6
HALF_FRAME = 0.5 / pc.FPS
FAIL, WARN = "FAIL", "WARN"


# ─────────────────────────── 数据 ───────────────────────────

@dataclass(frozen=True)
class Event:
    id: str
    shot: str
    take: str
    a_in: str | float
    a_out: str | float
    kind: str
    why: str
    match_ok: str
    quiet_ok: str
    basis: str

    @property
    def numbered(self) -> bool:
        """用了按编号取的锚点（line: / cut:）——start / end / 秒数不看编号。"""
        return any(isinstance(a, str) and a not in ("start", "end") for a in (self.a_in, self.a_out))


@dataclass(frozen=True)
class Note:
    ref: str
    status: str
    detail: str


@dataclass(frozen=True)
class Edl:
    path: Path
    version: int
    base_version: int
    status: str
    approved_by: str
    events: tuple[Event, ...]
    notes: tuple[Note, ...]


@dataclass(frozen=True)
class ALine:
    """对齐缓存里的一句。span：ok / low_conf / moved ＝实测起止（moved＝没按剧本顺序说、从 ASR 找回的，时间上可以排在
    编号更小的句子前面）；offscreen ＝计划窗（TTS 按它摆）；missing ＝计划窗（没对上）。"""
    idx: int
    text: str
    status: str
    span: tuple[float, float]
    blocks: tuple[tuple[float, float, str], ...]    # 切点要躲开的：每个词；没有词的句子整窗算一块


@dataclass(frozen=True)
class Align:
    shot: str
    sha: str
    duration: float                    # 容器时长（VFR 片比 frames / FPS 短一截）
    frames: int                        # 按 FPS 转恒定帧率后的帧数（pc.cfr_frames）
    lines: tuple[ALine, ...]
    speech: tuple[tuple[float, float], ...]
    cuts: tuple[float, ...]            # 镜内切点：detected，没有就 planned

    @property
    def end_frame(self) -> int:
        return self.frames

    @property
    def end_s(self) -> float:
        return self.frames / pc.FPS


@dataclass(frozen=True)
class Cut:
    """解析后的事件：源片里的入 / 出点（帧号）。"""
    id: str
    shot: str
    take: str
    fin: int
    fout: int
    kind: str

    @property
    def src_in(self) -> float:
        return self.fin / pc.FPS

    @property
    def src_out(self) -> float:
        return self.fout / pc.FPS

    @property
    def dur(self) -> float:
        return (self.fout - self.fin) / pc.FPS


@dataclass(frozen=True)
class Placed:
    ev: Event
    cut: Cut
    al: Align
    t0: float                          # 成片里的起点


@dataclass(frozen=True)
class Ctx:
    drama: Path
    epd: Path
    edl: Edl
    placed: tuple[Placed, ...]
    script_md: Path
    script: dict[str, script_tools.Shot]   # 剧本镜号 → 镜
    key_of: dict[str, str]                 # shotNN → 剧本镜号（shot md front matter `script:`）
    rendered: frozenset[str]               # 有 shotNN.mp4 的镜

    @property
    def total(self) -> float:
        return sum(p.cut.dur for p in self.placed)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    msg: str


class Report:
    def __init__(self) -> None:
        self.items: list[Finding] = []

    def fail(self, code: str, msg: str) -> None:
        self.items.append(Finding(FAIL, code, msg))

    def warn(self, code: str, msg: str) -> None:
        self.items.append(Finding(WARN, code, msg))


class Unresolved(Exception):
    pass


# ─────────────────────────── 路径与小工具 ───────────────────────────

def edl_path(epd: Path) -> Path:
    return epd / pc.CUT_DIR / EDL_NAME


def approved_path(epd: Path) -> Path:
    return epd / pc.CUT_DIR / APPROVED_NAME


def out_dir(epd: Path) -> Path:
    return epd / pc.POST_DIR / pc.CUT_DIR


def align_path(epd: Path, shot: str, take: str) -> Path:
    return align.cache_path(epd, shot, take)


def script_md(drama: Path, ep: str) -> Path:
    return drama.joinpath(*SCRIPT_DIR, ep, "script.md")


def frame(t: float) -> int:
    """秒 → 帧号（按 1/FPS 四舍五入）。"""
    return math.floor(t * pc.FPS + 0.5)


def _short(s: str, n: int = 24) -> str:
    return s if len(s) <= n else s[:n] + "…"


def _show(a: str | float) -> str:
    return json.dumps(a, ensure_ascii=False) if isinstance(a, str) else f"{a:g}"


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    part = p.with_name(p.stem + ".part" + p.suffix)
    part.write_text(text, encoding="utf-8")
    part.replace(p)


def _is_int(v: object) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def current_takes(epd: Path, shots: Iterable[str]) -> dict[str, str | None]:
    """各镜当前出片 shotNN.mp4 的 sha256（take 的身份；没有出片 → None）。每条命令现算一次，不落盘。"""
    out: dict[str, str | None] = {}
    for s in dict.fromkeys(shots):
        mp4 = pc.shot_mp4(epd / "shots" / s)
        out[s] = pc.sha256(mp4) if mp4.is_file() else None
    return out


def stale_pins(events: tuple[Event, ...], cur: dict[str, str | None]) -> list[str]:
    """钉的 take 不是当前出片的事件（括号里是当前 take 的 sha 前 pc.TAKE_ID_LEN 位，照抄进 edl 的 take）。"""
    return [f"{e.id} {e.shot}（钉的 {e.take}，当前 {pc.take_id(cur[e.shot] or '没有出片')}）"
            for e in events if pc.take_id(cur[e.shot] or "") != e.take]


def script_key(md: Path) -> str | None:
    """shot md front matter 的 `script:`（剧本镜号，如 S05）。"""
    parts = md.read_text(encoding="utf-8").split("---", 2)
    return pc._fields(parts[1]).get("script") if len(parts) == 3 and not parts[0].strip() else None


def _merge(iv: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1] + EPS:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _gaps(busy: list[tuple[float, float]], lo: float, hi: float) -> list[tuple[float, float]]:
    out, t = [], lo
    for a, b in busy:
        if a > t:
            out.append((t, min(a, hi)))
        t = max(t, b)
        if t >= hi:
            break
    if t < hi:
        out.append((t, hi))
    return [(a, b) for a, b in out if b > a + EPS]


def _within(spans: list[tuple[float, float]], a: float, b: float) -> bool:
    return any(lo - EPS <= a and b <= hi + EPS for lo, hi in spans)


def _covered(spans: list[tuple[float, float]], a: float, b: float) -> bool:
    """a–b 整段都在保留区间里（帧取整差半帧以内算在）。"""
    return any(lo <= a + HALF_FRAME and b - HALF_FRAME <= hi for lo, hi in spans)


def _voiced(al: Align) -> list[tuple[float, float]]:
    """有人声的区间：实测对白 + 画外 / 独白的计划窗（成片里 TTS 按计划窗摆）。"""
    return list(al.speech) + [ln.span for ln in al.lines if ln.status == align.OFFSCREEN]


# ─────────────────────────── 读 edl.toml ───────────────────────────

def _anchor(v: object) -> str | float | None:
    """合法锚点原样返回（数字转 float），不合法 → None。"""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) if v >= 0 else None
    if isinstance(v, str) and (v in ("start", "end") or ANCHOR_RE.fullmatch(v)):
        return v
    return None


def approved_versions(epd: Path) -> set[int]:
    p = approved_path(epd)
    if not p.is_file():
        return set()
    try:
        vs = json.loads(p.read_text(encoding="utf-8")).get("versions")
    except (ValueError, AttributeError):
        vs = None
    if not (isinstance(vs, list) and all(_is_int(v) and v >= 1 for v in vs)):
        raise SystemExit(f"{pc.rel(p)} 要是 {{\"versions\": [≥ 1 的整数, …]}}，读到的不是")
    return set(vs)


def load(epd: Path) -> Edl:
    """读 edl.toml 并逐项校验（schema 外的键、不合法的值全部列出后报错）；读到已批准的版本就记进 approved.json。"""
    p = edl_path(epd)
    if not p.is_file():
        raise SystemExit(f"没有 {pc.rel(p)}：先跑 edl.py init")
    try:
        cfg = tomllib.loads(p.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        raise SystemExit(f"{pc.rel(p)} 不是合法 TOML：{e}") from e
    bad = [f"未知键 {k}（schema 外的键不静默忽略）" for k in sorted(set(cfg) - TOP_KEYS)]
    ver, base, status, by = cfg.get("version"), cfg.get("base_version"), cfg.get("status"), cfg.get("approved_by", "")
    if not (_is_int(ver) and ver >= 1):
        bad.append(f"version = {ver!r}：要 ≥ 1 的整数")
    if not (_is_int(base) and _is_int(ver) and 0 <= base < ver):
        bad.append(f"base_version = {base!r}：要是比 version 小的非负整数")
    if cfg.get("fps") != pc.FPS:
        bad.append(f"fps = {cfg.get('fps')!r} ≠ pc.FPS {pc.FPS}")
    if status not in STATUSES:
        bad.append(f"status = {status!r}：只能是 {' / '.join(STATUSES)}")
    if not isinstance(by, str):
        bad.append(f"approved_by = {by!r} 要写成字符串")
    elif status in STATUSES[1:] and not by:
        bad.append(f"status = {status!r} 要写 approved_by（谁批的）")
    shots = {d.name for d in pc.shot_dirs(epd)}
    events: list[Event] = []
    for i, e in enumerate(cfg.get("event", []), 1):
        tag = f"[[event]] 第 {i} 条（{e.get('id', '没有 id')}）"
        bad += [f"{tag}：未知键 {k}" for k in sorted(set(e) - EVENT_KEYS)]
        eid, shot, take, kind = e.get("id"), e.get("shot"), e.get("take"), e.get("kind")
        if not isinstance(eid, str) or not eid or eid in {x.id for x in events}:
            bad.append(f"{tag}：id 要写、且不重复")
        if shot not in shots:
            bad.append(f"{tag}：shot = {shot!r} 不是本集 shots/ 下的镜")
        if not (isinstance(take, str) and TAKE_RE.fullmatch(take)):
            bad.append(f"{tag}：take = {take!r} 要写 sha256 前 {pc.TAKE_ID_LEN} 位（小写十六进制）")
        ends = {side: _anchor(e.get(side)) for side in ("in", "out")}
        bad += [f"{tag}：{side} = {e.get(side)!r} 不是锚点（start | end | 秒数 | line:N.start / line:N.end ±秒 | cut:K）"
                for side, a in ends.items() if a is None]
        if kind not in KINDS:
            bad.append(f"{tag}：kind = {kind!r}：只能是 {' / '.join(KINDS)}")
        text = {k: e.get(k, "") for k in ("why", "match_ok", "quiet_ok", "basis")}
        bad += [f"{tag}：{k} 要写成字符串" for k, v in text.items() if not isinstance(v, str)]
        if not (ends["in"] == "start" and ends["out"] == "end" and kind == "shot") and not text["why"]:
            bad.append(f"{tag}：不是整镜，要写 why（审稿条目或闸门号）")
        ev = Event(str(eid), str(shot), str(take), ends["in"] or 0.0, ends["out"] or 0.0, str(kind),
                   str(text["why"]), str(text["match_ok"]), str(text["quiet_ok"]), str(text["basis"]))
        if ev.numbered and not BASIS_RE.fullmatch(ev.basis):
            bad.append(f"{tag}：用了 line: / cut: 锚点，要写 basis（edl.py candidates 里这条 take 的 basis，{BASIS_LEN} 位十六进制）")
        elif ev.basis and not ev.numbered:
            bad.append(f"{tag}：basis 只配 line: / cut: 锚点（start / end / 秒数不看编号），删掉")
        events.append(ev)
    if not events:
        bad.append("一个 [[event]] 都没有")
    notes: list[Note] = []
    for i, n in enumerate(cfg.get("note", []), 1):
        tag = f"[[note]] 第 {i} 条（{n.get('ref', '没有 ref')}）"
        bad += [f"{tag}：未知键 {k}" for k in sorted(set(n) - NOTE_KEYS)]
        ref, st, detail = n.get("ref"), n.get("status"), n.get("detail", "")
        if not isinstance(ref, str) or not ref or ref in {x.ref for x in notes}:
            bad.append(f"{tag}：ref 要写、且不重复")
        if st not in NOTE_STATUSES:
            bad.append(f"{tag}：status = {st!r}：只能是 {' / '.join(NOTE_STATUSES)}")
        if not isinstance(detail, str):
            bad.append(f"{tag}：detail 要写成字符串")
        notes.append(Note(str(ref), str(st), str(detail)))
    if bad:
        raise SystemExit(f"{pc.rel(p)} 不合格 {len(bad)} 处：\n  " + "\n  ".join(bad))
    edl = Edl(p, ver, base, status, by, tuple(events), tuple(notes))
    have = approved_versions(epd)
    if status != "draft" and ver not in have:
        _write(approved_path(epd), json.dumps({"versions": sorted(have | {ver})}) + "\n")
    return edl


def default_events(epd: Path, shots: str | None) -> tuple[Event, ...]:
    """init 写的 v1：pc.cut_shots 的镜整镜顺接，钉当前 take。"""
    return tuple(Event("e%02d" % i, d.name, pc.take_id(pc.sha256(pc.shot_mp4(d))), "start", "end", "shot", "", "", "", "")
                 for i, d in enumerate(pc.cut_shots(epd, shots), 1))


def _tv(v: str | float) -> str:
    """TOML 值：字符串走 JSON 转义（与 TOML 基本字符串兼容），数字原样。"""
    return json.dumps(v, ensure_ascii=False) if isinstance(v, str) else f"{v:g}"


def edl_text(version: int, base: int, events: tuple[Event, ...]) -> str:
    out = ["# 剪辑决定（唯一出处）：锚点只从 edl.py candidates 里挑，改完跑 edl.py verify；status 只在用户批准后改",
           f"version = {version}", f"base_version = {base}", 'status = "draft"', 'approved_by = ""', f"fps = {pc.FPS}"]
    for e in events:
        out += ["", "[[event]]"] + [f"{k} = {_tv(v)}" for k, v in (
            ("id", e.id), ("shot", e.shot), ("take", e.take), ("in", e.a_in), ("out", e.a_out), ("kind", e.kind), ("why", e.why))]
    return "\n".join(out) + "\n"


# ─────────────────────────── 对齐缓存 ───────────────────────────

def read_align(p: Path, shot: str, take: str) -> Align:
    """align.py 写的对齐缓存 → Align；键、版本、镜、take、句子状态对不上就报错（重跑 align.py --force）。"""
    j = json.loads(p.read_text(encoding="utf-8"))
    bad = [f"缺 {k}" for k in sorted(ALIGN_KEYS - set(j))]
    if not bad:
        bad += [f"version {j['version']} ≠ {align.VERSION}"] if j["version"] != align.VERSION else []
        bad += [f"shot {j['shot']} ≠ {shot}"] if j["shot"] != shot else []
        bad += [f"take {pc.take_id(str(j['take_sha256']))} ≠ {take}"] if not str(j["take_sha256"]).startswith(take) else []
        bad += [f"frames {j['frames']!r} 不是正整数"] if not (_is_int(j["frames"]) and j["frames"] > 0) else []
        for x in j["lines"]:
            miss = sorted(LINE_KEYS - set(x))
            bad += [f"第 {x.get('idx')} 句缺 {miss}"] if miss else \
                [f"第 {x['idx']} 句 status {x['status']!r}"] if x["status"] not in LINE_STATUSES else []
    if bad:
        raise SystemExit(f"{pc.rel(p)} 对不上（{'；'.join(bad)}）——重跑 align.py --force")
    lines = []
    for x in j["lines"]:
        span = (float(x["planned"][0]), float(x["planned"][1])) if x["status"] == align.MISSING \
            else (float(x["start"]), float(x["end"]))
        words = tuple((float(w["s"]), float(w["e"]), str(w["w"])) for w in x["words"])
        blocks = words if words and x["status"] in WORDED else ((*span, f"「{_short(x['text'])}」整窗（{x['status']}）"),)
        lines.append(ALine(int(x["idx"]), str(x["text"]), x["status"], span, blocks))
    cuts = j["cuts"].get("detected") or j["cuts"].get("planned") or []
    return Align(shot, str(j["take_sha256"]), float(j["duration"]), int(j["frames"]), tuple(lines),
                 tuple((float(a), float(b)) for a, b in j["speech"]), tuple(sorted(float(t) for t in cuts)))


def aligns_for(drama: Path, epd: Path, events: tuple[Event, ...], cur: dict[str, str | None]) -> dict[tuple[str, str], Align]:
    """每个 (镜, take) 的对齐缓存。当前出片缺缓存 → 用 ALIGN_PYTHON 跑 align.py 补；钉的是旧 take 又没有缓存的不在返回里。"""
    need = sorted({(e.shot, e.take) for e in events})
    live = [(s, t) for s, t in need if pc.take_id(cur[s] or "") == t]
    todo = [s for s, t in live if not align_path(epd, s, t).is_file()]
    if todo:
        if not ALIGN_PY.is_file():
            raise SystemExit(f"缺对齐缓存（{'、'.join(todo)}），而 {pc.rel(ALIGN_PY)} 不在")
        shots = ",".join(str(pc.shot_no(epd / "shots" / s)) for s in todo)
        print(f"缺对齐缓存（{'、'.join(todo)} 的当前 take）：用 {pc.ALIGN_PYTHON} 跑 align.py --shots {shots}")
        if subprocess.run([str(pc.ALIGN_PYTHON), str(ALIGN_PY), str(drama), epd.name, "--shots", shots]).returncode != 0:
            raise SystemExit("align.py 没跑完（上面是它的报错）")
        still = [align_path(epd, s, t).name for s, t in live if not align_path(epd, s, t).is_file()]
        if still:
            raise SystemExit(f"align.py 跑完了还缺 {still}")
    return {(s, t): read_align(p, s, t) for s, t in need if (p := align_path(epd, s, t)).is_file()}


# ─────────────────────────── 解析锚点 ───────────────────────────

def anchor_t(a: str | float, al: Align) -> float:
    if isinstance(a, float):
        t = a
    elif a in ("start", "end"):
        t = 0.0 if a == "start" else al.end_s
    else:
        m = ANCHOR_RE.fullmatch(a)
        if m.group(1):
            n = int(m.group(1))
            ln = next((x for x in al.lines if x.idx == n), None)
            if ln is None:
                raise Unresolved(f"没有第 {n} 句（{al.shot} 这条 take 共 {len(al.lines)} 句）")
            if ln.status == align.MISSING:
                raise Unresolved(f"第 {n} 句没对上（missing），不能当锚点——人听后改用别的句子或秒数")
            t = ln.span[0] if m.group(2) == "start" else ln.span[1]
        else:
            k = int(m.group(3))
            if not 1 <= k <= len(al.cuts):
                raise Unresolved(f"没有第 {k} 个镜内切点（{al.shot} 有 {len(al.cuts)} 个）")
            t = al.cuts[k - 1]
        if m.group(4):
            t += float(m.group(5)) if m.group(4) == "+" else -float(m.group(5))
    if not -EPS <= t <= al.end_s + EPS:
        raise Unresolved(f"落在 {t:.3f}s，出了 take 的 0–{al.end_s:.3f}s")
    return t


def basis(al: Align) -> str:
    """line: / cut: 锚点的指纹：各句（序号, 原文, 状态, 起止帧号）与镜内切点（帧号）。md 改了台词或切点、align.py 重算后
    编号挪了或句子起止变了（改了算法、找回句让位），同一个 line:N 会指到别的地方——事件记下写锚点时的指纹，resolve 对不上即报错。"""
    raw = json.dumps([[[x.idx, x.text, x.status, frame(x.span[0]), frame(x.span[1])] for x in al.lines],
                      [frame(t) for t in al.cuts]], ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:BASIS_LEN]


def resolve(edl: Edl, aligns: dict[tuple[str, str], Align]) -> list[Cut]:
    """锚点 → 帧（1/FPS 取整）；解析不到、in ≥ out 的全部列出后报错。"""
    out: list[Cut] = []
    bad: list[str] = []
    for ev in edl.events:
        al = aligns[(ev.shot, ev.take)]
        if ev.numbered and ev.basis != basis(al):
            bad.append(f"{ev.id} {ev.shot}：line: / cut: 锚点是按另一版编号 / 起止写的（basis {ev.basis} ≠ 当前 {basis(al)}："
                       "md 改了台词或切点、align.py 重算后句子起止变了）——按 edl.py candidates 重挑锚点，basis 抄新的")
            continue
        fr: dict[str, int] = {}
        for side, a in (("in", ev.a_in), ("out", ev.a_out)):
            try:
                fr[side] = min(frame(anchor_t(a, al)), al.end_frame)
            except Unresolved as u:
                bad.append(f"{ev.id} {side} = {_show(a)}：{u}")
        if len(fr) < 2:
            continue
        if fr["in"] >= fr["out"]:
            bad.append(f"{ev.id}：in {_show(ev.a_in)} → {fr['in'] / pc.FPS:.3f}s，out {_show(ev.a_out)} → "
                       f"{fr['out'] / pc.FPS:.3f}s（in ≥ out）")
            continue
        out.append(Cut(ev.id, ev.shot, ev.take, fr["in"], fr["out"], ev.kind))
    if bad:
        raise SystemExit(f"{pc.rel(edl.path)} 锚点解析不了 {len(bad)} 处：\n  " + "\n  ".join(bad))
    return out


def context(drama: Path, epd: Path, edl: Edl, aligns: dict[tuple[str, str], Align]) -> Ctx:
    placed, t = [], 0.0
    for ev, c in zip(edl.events, resolve(edl, aligns)):
        placed.append(Placed(ev, c, aligns[(ev.shot, ev.take)], t))
        t += c.dur
    smd = script_md(drama, epd.name)
    dirs = pc.shot_dirs(epd)
    return Ctx(drama, epd, edl, tuple(placed), smd,
               {s.key: s for s in script_tools.parse(str(smd))[0]} if smd.is_file() else {},
               {d.name: k for d in dirs if pc.shot_md(d).is_file() and (k := script_key(pc.shot_md(d)))},
               frozenset(d.name for d in dirs if pc.shot_mp4(d).is_file()))


def _script_shot(ctx: Ctx, shot: str) -> tuple[script_tools.Shot | None, str]:
    """（这一镜的剧本段, 拿不到的原因）。剧本段按 shot md front matter `script:` 找；剧本这一镜与 take 时长差 > SYNC_TOL
    （剧本改过、还没重出片）也不给——那时剧本里的【a–bs】窗套不到这条 take 上。"""
    key = ctx.key_of.get(shot)
    s = ctx.script.get(key or "")
    if s is None:
        return None, f"{shot} 在剧本里找不到（script: {key or '没写'}）"
    dur = next(p.al.duration for p in ctx.placed if p.ev.shot == shot)
    if abs(s.dur - dur) > SYNC_TOL:
        return None, f"剧本 {key} {s.dur:g}s 与 {shot} 的 take {dur:.2f}s 对不上（剧本改过、还没重出片）"
    return s, ""


def _beat(ctx: Ctx, shot: str, a: float, b: float) -> bool | None:
    """源片 a–b 秒里有没有计划节拍（script_tools 的 G10 判据：台词窗压进来，或画面动作里有落在窗内的带时刻节拍）；查不了 → None。"""
    s, _why = _script_shot(ctx, shot)
    return None if s is None else script_tools._has_beat(s, a, b)


def _kept(ctx: Ctx, shot: str) -> list[tuple[float, float]]:
    return _merge([(p.cut.src_in, p.cut.src_out) for p in ctx.placed if p.ev.shot == shot])


def _joined(a: Placed, b: Placed) -> bool:
    """同一条 take 前后接着放（a 的出点就是 b 的入点）：中间没有接缝。"""
    return a.ev.shot == b.ev.shot and a.ev.take == b.ev.take and a.cut.fout == b.cut.fin


def _runs(ctx: Ctx) -> list[tuple[str, float, float]]:
    """成片里不断开的一段段源片：(镜, 源起, 源止)。"""
    out: list[tuple[str, float, float]] = []
    for i, p in enumerate(ctx.placed):
        if i and _joined(ctx.placed[i - 1], p):
            out[-1] = (out[-1][0], out[-1][1], p.cut.src_out)
        else:
            out.append((p.ev.shot, p.cut.src_in, p.cut.src_out))
    return out


# ─────────────────────────── V1–V10 ───────────────────────────

def v1_takes(epd: Path, edl: Edl, cur: dict[str, str | None], rep: Report) -> None:
    for ev in edl.events:
        now = cur[ev.shot]
        if now is None:
            rep.fail("V1", f"{ev.id} {ev.shot}：没有 {ev.shot}.mp4")
        elif pc.take_id(now) != ev.take:
            rep.fail("V1", f"{ev.id} {ev.shot}：钉的 take {ev.take} ≠ 当前 {ev.shot}.mp4 的 {pc.take_id(now)}——出片换过，"
                           "按当前 take 重跑 candidates 改这条")
    for why in stale_shots(epd, edl.events, cur):
        rep.fail("V1", why)


def stale_shots(epd: Path, events: tuple[Event, ...], cur: dict[str, str | None]) -> list[str]:
    """当前出片是旧片的镜（md 改了时长、片没重出；pc.stale_take）→ 原因列表。"""
    dirs = [epd / "shots" / s for s in dict.fromkeys(e.shot for e in events) if cur[s]]
    return [why for d in dirs if (why := pc.stale_take(pc.shot_md(d), pc.shot_mp4(d)))]


def _verdict(shot_dir: Path) -> str:
    """审片结论：空串＝这条 take 有「通过」且 sha 相符的 verdict.md；否则是为什么不算（查不了也算不过，不悄悄放行）。"""
    try:
        import render_review
    except ImportError as e:
        return f"render_review 导入失败（{e}），审片结论查不了"
    ok = getattr(render_review, "verdict_ok", None)
    if ok is None:
        return "render_review 没有 verdict_ok，审片结论查不了"
    return "" if ok(shot_dir, pc.shot_mp4(shot_dir)) else "没有「通过」且 sha 相符的 verdict.md（按 ai_videos__出片审片 审这条 take）"


def v1_verdicts(ctx: Ctx, rep: Report, proxy_ok: bool, cur: dict[str, str | None]) -> None:
    live = {p.ev.shot: p.ev.take for p in ctx.placed if pc.take_id(cur[p.ev.shot] or "") == p.ev.take}
    for shot, take in live.items():
        why = _verdict(ctx.epd / "shots" / shot)
        if why and proxy_ok:
            rep.warn("V1", f"{shot}（take {take}）：{why}——--proxy-ok，只出代理片")
        elif why:
            rep.fail("V1", f"{shot}（take {take}）：{why}")


def v2(ctx: Ctx, rep: Report) -> None:
    for p in ctx.placed:
        c, al = p.cut, p.al
        for side, t, native in (("in", c.src_in, c.fin == 0), ("out", c.src_out, c.fout == al.end_frame)):
            hit = None if native else next(((ln, s, e, w) for ln in al.lines for s, e, w in ln.blocks
                                             if s - WORD_MARGIN < t < e + WORD_MARGIN), None)
            if hit:
                ln, s, e, w = hit
                rep.fail("V2", f"{p.ev.id} {p.ev.shot} {side} {t:.3f}s 离第 {ln.idx} 句的 {w}（{s:.2f}–{e:.2f}s）"
                               f"不到 {WORD_MARGIN}s——切在词上")
    for key in dict.fromkeys((p.ev.shot, p.ev.take) for p in ctx.placed):
        mine = [p for p in ctx.placed if (p.ev.shot, p.ev.take) == key]
        kept = _merge([(p.cut.src_in, p.cut.src_out) for p in mine])
        for ln in mine[0].al.lines:
            inside = [_within(kept, s, e) for s, e, _w in ln.blocks]
            if any(inside) and not all(inside):
                rep.fail("V2", f"{'、'.join(p.ev.id for p in mine)} {key[0]} 删了半句：第 {ln.idx} 句「{_short(ln.text)}」只留 "
                               f"{sum(inside)}/{len(inside)} 个词——删句只能整句")


def _anchor_gone(ctx: Ctx, shot: str, snip: str) -> str:
    """空串＝锚点剪后全在；否则是怎么不在。台词按对齐缓存的实测起止，画面动作按剧本【a–bs】窗。"""
    mine = [p for p in ctx.placed if p.ev.shot == shot]
    if not mine:
        return "所在的镜已出片，却整镜没进剪辑"
    al, spans = mine[0].al, _kept(ctx, shot)
    end = al.end_s
    ln = next((x for x in al.lines if snip in x.text), None)
    if ln is not None:
        win: tuple[float, float] | None = ln.span
    else:
        s, why = _script_shot(ctx, shot)
        win = script_tools.snippet_window(s, snip) if s else None
        if win is None:
            return "" if _covered(spans, 0.0, end) else \
                f"找不到它在 take 里的时间窗（{why or '对齐缓存里没有这句、剧本画面动作也没带【a–bs】'}），这一镜剪过就确认不了"
    a, b = max(0.0, win[0]), min(end, win[1])
    return "" if _covered(spans, a, b) else \
        f"剪后不全在（{a:.2f}–{b:.2f}s；这一镜保留 " + "、".join(f"{lo:.2f}–{hi:.2f}s" for lo, hi in spans) + "）"


def v3(ctx: Ctx, rep: Report) -> None:
    f = ctx.script_md.parent / goal_ledger.FILE
    if not f.is_file():
        return
    cfg = tomllib.loads(f.read_text(encoding="utf-8"))
    shot_of = {k: s for s, k in ctx.key_of.items() if s in ctx.rendered}
    for sec, fields in ANCHOR_FIELDS.items():
        for item in cfg.get(sec, []):
            for fld in fields:
                for r in goal_ledger._pairs(item.get(fld)):
                    shot = shot_of.get(r[0])
                    gone = _anchor_gone(ctx, shot, r[1]) if shot else ""
                    if gone:
                        rep.fail("V3", f"{goal_ledger.FILE} {sec}.{fld}「{r[1]}」（{r[0]} ＝ {shot}）{gone}")


def _framing(epd: Path, p: Placed, side: str) -> tuple[float, str, str] | None:
    """接缝一端露出来的那一帧的（人占画高, 景别名, 机位标签）：取它所在分镜段最近的「景别档」——首段＝起幅、末段＝落幅
    （段界用镜内切点）。落在中段、单段镜的中间（运镜在两档之间走）、或 shot md 没有景别档：推不出，返回 None。"""
    md = pc.shot_md(epd / "shots" / p.ev.shot)
    m = JB_RE.search(md.read_text(encoding="utf-8")) if md.is_file() else None
    if m is None:
        return None
    f = p.cut.fout - 1 if side == "out" else p.cut.fin
    x = (f + 0.5) / pc.FPS
    cuts = p.al.cuts
    if f == 0 or cuts and x < cuts[0]:
        return float(m.group(2)), m.group(1), m.group(5)
    if f == p.al.end_frame - 1 or cuts and x > cuts[-1]:
        return float(m.group(4)), m.group(3), m.group(6)
    return None


def v4(ctx: Ctx, rep: Report) -> None:
    order = {d.name: i for i, d in enumerate(pc.shot_dirs(ctx.epd))}
    for a, b in zip(ctx.placed, ctx.placed[1:]):
        if _joined(a, b):
            continue
        if a.cut.fout == a.al.end_frame and b.cut.fin == 0 and order[b.ev.shot] == order[a.ev.shot] + 1:
            if pc.is_chengjie(pc.shot_md(ctx.epd / "shots" / b.ev.shot)):
                rep.fail("V4", f"{a.ev.id}→{b.ev.id}（{a.ev.shot}→{b.ev.shot}）是承接缝：整镜顺接两侧各剪一小段（共用的接缝帧与缓动），"
                               "edl 整镜相接会把它们放回来——edl 还表达不了承接缝，这集先不建 edl（finish_ep 走整镜顺接）")
            continue                                   # 原镜间接缝：沿用生成时 shot_seam 的判定
        fa, fb = _framing(ctx.epd, a, "out"), _framing(ctx.epd, b, "in")
        where = f"{a.ev.id}（{a.ev.shot} 出 {a.cut.src_out:.2f}s）→ {b.ev.id}（{b.ev.shot} 入 {b.cut.src_in:.2f}s）"
        fix = f"换切点，或在 {b.ev.id} 写 match_ok = \"理由\""
        if fa is None or fb is None:
            if not b.ev.match_ok:
                which = "、".join(n for n, x in (("出点", fa), ("入点", fb)) if x is None)
                rep.fail("V4", f"新接缝 {where}：{which}落在分镜中段（或 shot md 没有景别档），取景推不出——{fix}")
            continue
        seam = shot_seam.verdict({"n": pc.shot_no(Path(a.ev.shot)), "jb": (fa[0], fa[1], fa[0], fa[1]), "jbcam": (fa[2], fa[2])},
                                 {"n": pc.shot_no(Path(b.ev.shot)), "jb": (fb[0], fb[1], fb[0], fb[1]), "jbcam": (fb[2], fb[2])})
        if not seam.ok and not b.ev.match_ok:
            rep.fail("V4", f"新接缝 {where}：{fa[1]}{fa[0]:g} `{fa[2]}` → {fb[1]}{fb[0]:g} `{fb[2]}`，比值 {seam.ratio:.2f} "
                           f"{seam.verdict}——{fix}")


def v5(ctx: Ctx, rep: Report) -> None:
    flashes = [p.ev.id for p in ctx.placed if p.ev.kind == "flash"]
    for p in ctx.placed:
        flash = p.ev.kind == "flash"
        lo = MIN_FLASH if flash else MIN_EVENT
        if p.cut.dur < lo - EPS:
            rep.fail("V5", f"{p.ev.id} {p.ev.shot} 只有 {p.cut.dur:.2f}s < {lo:g}s（{'闪前' if flash else '事件'}下限）")
        if flash and p.cut.dur > FLASH_MAX + EPS:
            rep.fail("V5", f"{p.ev.id} 闪前 {p.cut.dur:.2f}s > FLASH_MAX {FLASH_MAX:g}s")
    if len(flashes) > FLASH_MAX_N:
        rep.fail("V5", f"闪前 {len(flashes)} 个（{'、'.join(flashes)}）> 每集 {FLASH_MAX_N} 个")
    lo, hi = script_tools.ep_range(str(ctx.script_md))
    if not lo <= ctx.total <= hi:
        rep.warn("V5", f"集长 {ctx.total:.1f}s 不在 {lo:g}–{hi:g}s（script.toml [episode]）")


def _first_seen(ctx: Ctx, zone_s: float, bg_s: float) -> dict[str, tuple[str, float]]:
    """本集首次出现的场景主体所在的剧本镜 →（新地区 / 新地点, 剪后下限）。判定照 script_tools.scenery_errors（G10）：
    `场景:` 行第一个 bgN、带「闪前」的镜不算抵达、按集序跨集数第一次。script_tools 没有返回这张表的函数，只好照走一遍。"""
    zones = script_tools._zones(str(ctx.drama / "2_世界观人设" / "scenes"))
    seen_bg: set[str] = set()
    seen_zone: set[str] = set()
    out: dict[str, tuple[str, float]] = {}
    for path in script_tools.episodes(str(ctx.drama.joinpath(*SCRIPT_DIR))):
        mine = Path(path).parent.name == ctx.epd.name
        for s in script_tools.parse(path)[0]:
            m = script_tools._BG_KEY.search(s.scene)
            if not m or "闪前" in s.scene or m.group(1) not in zones:
                continue
            bg, zone = m.group(1), zones[m.group(1)]
            if mine and bg not in seen_bg:
                out[s.key] = ("新地区", zone_s) if zone not in seen_zone else ("新地点", bg_s)
            seen_bg.add(bg)
            seen_zone.add(zone)
        if mine:
            break
    return out


def v6(ctx: Ctx, rep: Report) -> None:
    sc = script_tools.scenery_cfg(str(ctx.drama))
    if not sc:
        rep.warn("V6", "剧没有 script.toml [scenery]（G10 没开）：场景展示窗与空档（V6 / V7）不查")
        return
    miss = [k for k in ("post_trim_zone_s", "post_trim_bg_s") if k not in sc]
    if miss:
        rep.fail("V6", f"script.toml [scenery] 缺 {' / '.join(miss)}——剪后下限没定义（不拿字面量兜底）")
        return
    if not ctx.script:
        rep.fail("V6", f"没有 {pc.rel(ctx.script_md)}：场景展示窗查不了")
        return
    shot_of = {k: s for s, k in ctx.key_of.items() if s in ctx.rendered}
    runs = _runs(ctx)
    for key, (what, need) in _first_seen(ctx, float(sc["post_trim_zone_s"]), float(sc["post_trim_bg_s"])).items():
        wins = [(float(a), float(b)) for a, b, _t in script_tools._SCENERY.findall(ctx.script[key].body)]
        shot = shot_of.get(key)
        if shot is None or not wins:
            continue                                   # 还没出片；或剧本没写场景展示（剧本阶段 G10 管）
        spans = [(lo, hi) for sh, lo, hi in runs if sh == shot]
        if not spans:
            rep.fail("V6", f"{shot}（{key}）{what}的场景展示整镜没进剪辑（要 ≥ {need:g}s）")
            continue
        s, why = _script_shot(ctx, shot)
        note = ""
        if s is None:
            al = next(p.al for p in ctx.placed if p.ev.shot == shot)
            head = min((a for a, _b in _voiced(al)), default=al.duration)
            wins, note = [(0.0, head)], f"（{why}：按镜首连续无词区间 0–{head:.2f}s 近似）"
        best = max(max(0.0, min(b, hi) - max(a, lo)) for a, b in wins for lo, hi in spans)
        if best < need - HALF_FRAME:
            rep.fail("V6", f"{shot}（{key}）{what}的场景展示剪后只剩 {best:.2f}s < {need:g}s（script.toml [scenery]）{note}")


def v7(ctx: Ctx, rep: Report) -> None:
    sc = script_tools.scenery_cfg(str(ctx.drama))
    if not sc:
        return                                         # V6 已经报过没开 G10
    if "idle_max_s" not in sc:
        rep.warn("V7", "script.toml [scenery] 没有 idle_max_s：空档只由 candidates 列出，不判")
        return
    idle = float(sc["idle_max_s"])
    busy = _merge([(p.t0 + max(a, p.cut.src_in) - p.cut.src_in, p.t0 + min(b, p.cut.src_out) - p.cut.src_in)
                   for p in ctx.placed for a, b in _voiced(p.al) if a < p.cut.src_out and b > p.cut.src_in])
    for qa, qb in _gaps(busy, 0.0, ctx.total):
        if qb - qa <= idle + EPS:
            continue
        pieces = [(p, p.cut.src_in + max(qa, p.t0) - p.t0, p.cut.src_in + min(qb, p.t0 + p.cut.dur) - p.t0)
                  for p in ctx.placed if p.t0 < qb - EPS and p.t0 + p.cut.dur > qa + EPS]
        beats = [_beat(ctx, p.ev.shot, a, b) for p, a, b in pieces]
        if any(beats):
            continue
        owner = max(pieces, key=lambda x: x[2] - x[1])[0]
        if owner.ev.quiet_ok:
            continue
        where = "、".join(f"{p.ev.id} {p.ev.shot} {a:.2f}–{b:.2f}s" for p, a, b in pieces)
        unknown = "；".join(dict.fromkeys(_script_shot(ctx, p.ev.shot)[1] for (p, _a, _b), x in zip(pieces, beats) if x is None))
        rep.fail("V7", f"成片 {qa:.2f}–{qb:.2f}s 共 {qb - qa:.1f}s 没台词、没计划节拍 > idle_max_s {idle:g}s（{where}）"
                       + (f"（节拍查不了：{unknown}）" if unknown else "") + f"——剪掉，或在 {owner.ev.id} 写 quiet_ok = \"理由\"")


def _viewing_packet(rep: Report, code: str) -> ModuleType | None:
    try:
        import viewing_packet
    except ImportError as e:
        rep.fail(code, f"viewing_packet 导入失败（{e}），查不了")
        return None
    return viewing_packet


def v8(ctx: Ctx, rep: Report) -> None:
    """标了好笑的镜里，每句保留下来的台词：剪辑新加的出点（早于源片里它之后的下一句 / 镜内切 / 镜尾）离句尾 ≥ LAUGH_GAP。
    源片本来就挤的地方不是剪出来的，edl 也补不出气口，不报。"""
    vp = _viewing_packet(rep, "V8")
    if vp is None:
        return
    if LAUGH_TAG not in vp.TAGS:
        rep.fail("V8", f"viewing_packet.TAGS 里没有「{LAUGH_TAG}」——意图标签改了名，edl.LAUGH_TAG 跟着改")
        return
    infos = vp.shot_infos(ctx.epd)
    for p in ctx.placed:
        if p.ev.shot not in infos or LAUGH_TAG not in infos[p.ev.shot].tags:
            continue
        c, al = p.cut, p.al
        for ln in al.lines:
            s, e = ln.span
            if not (c.src_in <= s and e <= c.src_out):
                continue
            nxt = min([x.span[0] for x in al.lines if x is not ln and x.span[0] >= e - EPS]
                      + [t for t in al.cuts if t > e + EPS] + [al.duration])
            if c.src_out < nxt - HALF_FRAME and c.src_out - e < LAUGH_GAP - EPS:
                rep.fail("V8", f"{p.ev.id} {p.ev.shot}（标了{LAUGH_TAG}）第 {ln.idx} 句「{_short(ln.text)}」句尾 {e:.2f}s 到出点 "
                               f"{c.src_out:.2f}s 只有 {c.src_out - e:.2f}s < {LAUGH_GAP:g}s——笑点后面留气口")


def top3(review: Path) -> list[int]:
    """review.md「最该改的 3 处」小节里的条目编号。"""
    parts = review.read_text(encoding="utf-8").split(TOP3_HEAD, 1)
    body = re.split(r"^## ", parts[1], maxsplit=1, flags=re.M)[0] if len(parts) == 2 else ""
    return [int(n) for n in TOP3_ITEM_RE.findall(body)]


def v9(epd: Path, edl: Edl, rep: Report) -> None:
    """当前作数的成片与 animatic 整集观感审稿（viewing/、viewing_animatic/），「最该改的 3 处」每条都要有非 open 的 [[note]]，
    ref ＝「{目录} {视频 sha 前 8 位} #{编号}」。审的视频已经变了的 review.md 作废（viewing_packet 同一判据），只提示重审。
    代理片的审稿（viewing_proxy/{代理片名}/）是剪辑回路自己逐版比的，不在这里查。"""
    vp = _viewing_packet(rep, "V9")
    if vp is None:
        return
    notes = {n.ref: n for n in edl.notes}
    for sub in (vp.VIEW_SUB, vp.VIEW_SUB_ANIMATIC):
        review = epd / sub / vp.REVIEW_NAME
        if not review.is_file():
            continue
        ok, why = vp.review_state(epd, sub)
        if not ok:
            rep.warn("V9", f"{sub}/{vp.REVIEW_NAME} 不作数（{why}），不查")
            continue
        sha = json.loads((epd / sub / vp.PACKET_NAME).read_text(encoding="utf-8"))["video"]["sha256"]
        items = top3(review)
        if not items:
            rep.fail("V9", f"{sub}/{vp.REVIEW_NAME} 的「{TOP3_HEAD[3:]}」里没有编号条目")
        for n in items:
            ref = f"{sub} {sha[:8]} #{n}"
            if ref not in notes:
                rep.fail("V9", f"审稿 {ref} 没有 [[note]]（ref = \"{ref}\"，status 写 {' / '.join(NOTE_STATUSES[1:])}）")
            elif notes[ref].status == "open":
                rep.fail("V9", f"审稿 {ref} 的 [[note]] 还是 open")


def v10(epd: Path, edl: Edl, rep: Report) -> None:
    have = approved_versions(epd)
    prev = max(have, default=0) if edl.status == "draft" else max((v for v in have if v < edl.version), default=0)
    if edl.base_version != prev:
        rep.fail("V10", f"base_version = {edl.base_version}，上一个已批准的是 v{prev}（{pc.rel(approved_path(epd))}）——"
                        f"这份改动不是基于它，可能盖掉了别的会话批准过的剪辑：先把 v{prev} 合进来，再写 base_version = {prev}")


def verify(drama: Path, epd: Path, proxy_ok: bool = False) -> list[Finding]:
    """V1–V10 逐条查完再返回。edl 本身不合格（键 / 值 / fps）、锚点解析不了、in ≥ out：在这之前报错停下。"""
    edl = load(epd)
    cur = current_takes(epd, (e.shot for e in edl.events))
    rep = Report()
    v1_takes(epd, edl, cur, rep)
    aligns = aligns_for(drama, epd, edl.events, cur)
    lost = [e.id for e in edl.events if (e.shot, e.take) not in aligns]
    if lost:
        rep.fail("V1", f"{'、'.join(lost)} 钉的旧 take 没有对齐缓存，时间线排不出来——V2–V8 没查；按当前 take 改好再 verify")
    else:
        ctx = context(drama, epd, edl, aligns)
        v1_verdicts(ctx, rep, proxy_ok, cur)
        for check in (v2, v3, v4, v5, v6, v7, v8):
            check(ctx, rep)
    v9(epd, edl, rep)
    v10(epd, edl, rep)
    return rep.items


# ─────────────────────────── init / candidates / plan ───────────────────────────

def init(epd: Path, shots: str | None, force: bool) -> Path:
    """v1 草稿：cut_shots 的镜整镜顺接，钉当前 take。approved.json 里有批准过的版本时，接着它往上编号。"""
    p = edl_path(epd)
    if p.is_file() and not force:
        raise SystemExit(f"{pc.rel(p)} 已经有了：要从头起草加 --force（覆盖现有的剪辑决定）")
    base = max(approved_versions(epd), default=0)
    events = default_events(epd, shots)
    _write(p, edl_text(base + 1, base, events))
    print(f"edl v{base + 1} 草稿：{len(events)} 个整镜事件（{events[0].shot}–{events[-1].shot}）→ {pc.rel(p)}")
    return p


def _candidates_of(ctx: Ctx, p: Placed, idle: float | None) -> dict:
    c, al = p.cut, p.al
    blocks = sorted((s, e, ln.idx) for ln in al.lines for s, e, _w in ln.blocks)
    cuts = [{"t": round(t, 3), "legal": not any(s - WORD_MARGIN < t < e + WORD_MARGIN for s, e, _i in blocks)}
            for t in al.cuts if c.src_in < t < c.src_out]
    gaps, busy_to, last = [], 0.0, None
    for s, e, idx in blocks + [(al.duration, al.duration, None)]:
        if s - busy_to >= GAP_MIN:
            kind = "镜首" if last is None else "镜尾" if idx is None else "句内" if idx == last else "句间"
            lo = max(c.src_in, busy_to + (0.0 if last is None else WORD_MARGIN))
            hi = min(c.src_out, s - (0.0 if idx is None else WORD_MARGIN))
            lo, hi = math.ceil(lo * pc.FPS - EPS) / pc.FPS, math.floor(hi * pc.FPS + EPS) / pc.FPS
            if lo <= hi:
                gaps.append({"lo": round(lo, 3), "hi": round(hi, 3), "kind": kind})
        if e > busy_to:
            busy_to, last = e, idx
    quiet = []
    for a, b in _gaps(_merge(_voiced(al)), c.src_in, c.src_out):
        if b - a < GAP_MIN or idle is not None and b - a <= idle + EPS:
            continue
        beat = _beat(ctx, p.ev.shot, a, b)
        quiet.append({"a": round(a, 3), "b": round(b, 3), "dur": round(b - a, 3), "beat": beat,
                      "dead": None if idle is None or beat is None else not beat})
    return {"id": p.ev.id, "shot": p.ev.shot, "take": p.ev.take, "basis": basis(al), "src_in": round(c.src_in, 3),
            "src_out": round(c.src_out, 3), "cuts": cuts, "gaps": gaps, "quiet": quiet}


def candidates(drama: Path, epd: Path) -> Path:
    """每个事件的合法切点（镜内切点优先，其次词间隙 ≥ GAP_MIN、离词 ≥ WORD_MARGIN 的区间）与死区（> idle_max_s 没人声、
    没计划节拍；没有 idle_max_s 时只列不判）。剪辑只许从这里挑时间码。"""
    have = edl_path(epd).is_file()
    edl = load(epd) if have else Edl(edl_path(epd), 0, 0, "draft", "", default_events(epd, None), ())
    cur = current_takes(epd, (e.shot for e in edl.events))
    stale = stale_pins(edl.events, cur)
    if stale:
        raise SystemExit("edl 钉的 take 不是当前出片，切点得按当前 take 挑：先把这些事件的 take 改成括号里的当前值再重跑——"
                         + "、".join(stale))
    ctx = context(drama, epd, edl, aligns_for(drama, epd, edl.events, cur))
    idle_cfg = script_tools.scenery_cfg(str(drama)).get("idle_max_s")
    idle = None if idle_cfg is None else float(idle_cfg)
    rows = [_candidates_of(ctx, p, idle) for p in ctx.placed]
    out = out_dir(epd) / CANDIDATES_NAME
    _write(out, json.dumps({"edl_version": edl.version if have else None, "fps": pc.FPS, "gap_min": GAP_MIN,
                            "word_margin": WORD_MARGIN, "idle_max_s": idle, "events": rows}, ensure_ascii=False, indent=1) + "\n")
    if not have:
        print(f"还没有 {pc.rel(edl_path(epd))}：按 init 会写的整镜事件列")
    for r in rows:
        print(f"{r['id']} {r['shot']} {r['src_in']:.2f}–{r['src_out']:.2f}s（take {r['take']}，basis {r['basis']}）")
        print("  镜内切点：" + ("、".join(f"{x['t']:.2f}s" + ("" if x["legal"] else "（离词太近）") for x in r["cuts"]) or "无"))
        print("  可切区间：" + ("、".join(f"{g['lo']:.2f}–{g['hi']:.2f}s {g['kind']}" for g in r["gaps"]) or "无"))
        if idle is None:
            print(f"  空档：没有 idle_max_s，只列不判（{len(r['quiet'])} 段，见 {CANDIDATES_NAME}）")
        else:
            dead = [q for q in r["quiet"] if q["dead"] is not False]
            print("  死区：" + ("、".join(f"{q['a']:.2f}–{q['b']:.2f}s（{q['dur']:.1f}s" + ("，节拍查不了" if q["dead"] is None else "")
                                         + "）" for q in dead) or "无"))
    print(f"→ {pc.rel(out)}")
    return out


def plan(drama: Path, epd: Path) -> list[Cut]:
    """解析后的事件表 → post/cut/plan.json：[{id, shot, take, src_in, src_out, dur, kind}]（秒，取整到帧）。
    钉的 take 与当前 shotNN.mp4 不符即报错——按旧 take 的时间码去切新出片，切点全错。"""
    edl = load(epd)
    cur = current_takes(epd, (e.shot for e in edl.events))
    stale = stale_pins(edl.events, cur)
    if stale:
        raise SystemExit("edl 钉的 take 与当前出片不符（V1），先按新 take 改 edl：" + "、".join(stale))
    old = stale_shots(epd, edl.events, cur)
    if old:
        raise SystemExit("出片是旧片（V1）：\n  " + "\n  ".join(old))
    cuts = resolve(edl, aligns_for(drama, epd, edl.events, cur))
    rows = [{"id": c.id, "shot": c.shot, "take": c.take, "src_in": round(c.src_in, 6), "src_out": round(c.src_out, 6),
             "dur": round(c.dur, 6), "kind": c.kind} for c in cuts]
    _write(out_dir(epd) / PLAN_NAME, json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    return cuts


def main() -> int:
    pc.utf8_console()
    argv = sys.argv[1:]
    if len(argv) >= 3 and argv[0] not in CMDS and argv[2] in CMDS:     # 也认 <剧> <ep> <命令>
        argv = [argv[2], *argv[:2], *argv[3:]]
    ap = argparse.ArgumentParser(description="剪辑决定 cut/edl.toml：init / candidates / verify / plan")
    ap.add_argument("cmd", choices=CMDS)
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--shots", default=None, help="init：如 1-6,9；默认从第一镜起连续有出片的镜")
    ap.add_argument("--force", action="store_true", help="init：覆盖已有的 edl.toml")
    ap.add_argument("--proxy-ok", action="store_true", help="verify：审片结论不齐只警告（出代理片用）")
    a = ap.parse_args(argv)
    drama = pc.drama_root(a.drama)
    epd = pc.ep_dir(drama, a.ep)
    if a.cmd == "init":
        init(epd, a.shots, a.force)
    elif a.cmd == "candidates":
        candidates(drama, epd)
    elif a.cmd == "plan":
        cuts = plan(drama, epd)
        print(f"plan：{len(cuts)} 个事件，{sum(c.dur for c in cuts):.2f}s → {pc.rel(out_dir(epd) / PLAN_NAME)}")
    else:
        items = verify(drama, epd, a.proxy_ok)
        for f in items:
            print(f"{'✗' if f.level == FAIL else '⚠'} {f.code} {f.msg}")
        n = sum(1 for f in items if f.level == FAIL)
        print(f"verify：{n} 处不过、{len(items) - n} 条警告" if items else "verify：V1–V10 全过")
        return 1 if n else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
