# -*- coding: utf-8 -*-
"""成片回读 QC（Q1–Q9）：全部从交付件本身回读；报告写 {集}/post/qc/{视频名}.qc.json（绑视频 sha256），任一 FAIL 即报错。

    python tools/post/qc.py <剧> <ep> [--video X] [--plan plan.json] [--selftest]

视频默认 {ep}_final.mp4；事件表默认读视频自己的 {视频名}.segments.json：v2（事件、take、源片入 / 出点）照读，
v1 按整镜顺排（源起点记 0、take 取当前 shotNN.mp4，承接缝剪掉的头不计——Q6 映射是近似）。
--plan 给了才用 plan.json（edl.py plan 的事件表 [{id, shot, take, src_in, src_out, dur, kind}]）——post/cut/plan.json 跟着
最新的 edl 草稿走，不一定是这条视频的。
finish_ep 收尾调 `run(...)`。
- Q1 时长：视频 = plan 总长 ±1 帧；音视频差 ≤ 1 帧。
- Q2 规格：分辨率 = 母带声明值（take 短边不足 MASTER_SHORT 就等比放大到它）；avg_frame_rate == FPS 且 r_frame_rate 同值（CFR）；
  yuv420p；AAC 48 kHz。
- Q3 切点（scdet 逐帧 mafd / 分）：每个事件边界 ±1 帧内有检出（同一 take 源里相接、原镜间承接缝不要求）；
  边界 ±0.5 s 内不许再有强切（闪帧，含紧挨边界的 1 帧夹心）。离边界远的镜内切不管。
- Q4 blackdetect ≥ 0.1 s / freezedetect ≥ 1.0 s 命中即 FAIL（落在 hold 类事件里的除外）。
- Q5 响度：I = −14 ±1 LUFS、TP ≤ −1.0 dBTP；LRA 不在 [7, 12] 先只警告。
- Q6 接缝对白响度：每个边界两侧 2 s 内的对白段（align 缓存的 speech 区间映射到成片）BS.1770 门控响度差 ≤ 2 LU；
  要用的 align 缓存缺了即 FAIL，只有 --selftest 记 SKIP。
- Q7 字幕：{视频名}.srt / .zh.srt 每条落在成片内、不越过所属事件尾；CPS（字符 / 秒，不计换行）≤ subs.cps_cap（英 17、中 9）。
- Q8 AIGC 隐式标识：aigc.readback 通过，且 ProduceID 含全部进片 take 的。
- Q9 视频码率 ≥ 4 Mbps。
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from pathlib import Path

import post_common as pc
import aigc
import edl
import mux_av        # tools/ 下的，post_common 已把 tools/ 加进 sys.path
import segments
import subs

TOL_FRAMES = 1                      # Q1 / Q3 / Q7 的「±1 帧」
FRAME_S = 1 / pc.FPS
PIX_FMT = pc.DELIVER[pc.DELIVER.index("-pix_fmt") + 1]
SC_CUT = 8.0          # scdet 分（0–100）≥ 它算切。ep01 实测：镜间硬切 13.4–20.8，镜内切 9.7–21.4，切后次帧的运动余波到过 8.1
SC_FLASH = 12.0       # 分 ≥ 它、又不是边界那一下 → 边界旁多出的强切（余波到不了它）
SPIKE_MAFD = 6.0      # mafd 局部尖峰也算切（且算强切）：≥ 它，且 ≥ SPIKE_RATIO × 前后 SPIKE_WIN 帧（隔开紧邻 1 帧）的中位数。
SPIKE_RATIO = 3.0     # scdet 的分 = min(mafd, 与上一帧 mafd 之差)，会压掉紧挨着的第二下（1 帧夹心：切进 4.3 分），尖峰压不掉；
SPIKE_WIN = 6         # ep01 实测：切的尖峰比 ≥ 4.0，不是切的（含手持打斗 mafd 9–17 连成片）≤ 1.9
FLASH_WIN_S = 0.5
BLACK_MIN_S = 0.1
FREEZE_MIN_S = 1.0
HOLD_KINDS = ("hold",)
LOUD_I = mux_av.LOUD_I
LOUD_TOL_LU = 1.0
TP_MAX = mux_av.LOUD_TP
LRA_RANGE = (7.0, 12.0)
SEAM_WIN_S = 2.0
SEAM_JUMP_LU = 2.0
GATE_BLOCK_S = 0.4    # BS.1770 门控块长；ebur128 每 0.1 s 报一块（块尾时刻）的 M
GATE_ABS_LUFS = -70.0
GATE_REL_LU = 10.0
BITRATE_MIN = 4_000_000

QC_SUB = "qc"                       # {集}/post/qc/{视频名}.qc.json
SRT_SUFFIXES = tuple(subs.SRT_SUFFIXES.values())    # subs.write_srts 的两种输出（src、zh 的顺序）
PLAN_KEYS = ("id", "shot", "take", "src_in", "src_out", "dur", "kind")    # edl.py plan 的事件表
META_RE = re.compile(r"pts_time:([\d.]+)|lavfi\.scd\.(mafd|score)=([\d.]+)")
BLACK_RE = re.compile(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)")
FREEZE_START_RE = re.compile(r"freeze_start: ([\d.]+)")
FREEZE_END_RE = re.compile(r"freeze_end: ([\d.]+)")
EBU_RE = re.compile(r"t:\s*([\d.]+)\s+TARGET:\S+\s+LUFS\s+M:\s*(-?[\d.]+)")
SRT_TIME_RE = re.compile(r"(\d+):(\d\d):(\d\d)[,.](\d{3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{3})")

PASS, FAIL, WARN, SKIP = "PASS", "FAIL", "WARN", "SKIP"


@dataclass(frozen=True)
class Event:
    id: str
    shot: str
    take: str          # take 的 sha256 前 12 位
    src_in: float
    src_out: float
    start: float       # 成片里的起点
    dur: float
    kind: str

    @property
    def end(self) -> float:
        return self.start + self.dur


@dataclass(frozen=True)
class Check:
    status: str
    detail: str
    data: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Streams:
    fps: Fraction
    r_fps: Fraction
    pix_fmt: str
    v_bitrate: int
    acodec: str | None
    ar: int | None


@dataclass(frozen=True)
class Change:
    t: float
    mafd: float
    score: float
    spike: bool

    @property
    def strong(self) -> bool:
        return self.spike or self.score >= SC_FLASH


@dataclass(frozen=True)
class Scan:
    cuts: list[Change]                   # 分 ≥ SC_CUT 或 mafd 尖峰的帧
    black: list[tuple[float, float]]
    freeze: list[tuple[float, float]]


def frames(dt: float) -> float:
    return round(abs(dt) * pc.FPS, 3)


def report_path(epd: Path, video: Path) -> Path:
    return epd / pc.POST_DIR / QC_SUB / f"{video.stem}.qc.json"


# ─────────────────────────── 事件表 ───────────────────────────

def events(plan: list[dict] | list[edl.Cut]) -> list[Event]:
    """plan.json 的行，或 edl.plan() 返回的 Cut（同名属性）→ 成片时间线上的事件。"""
    if not isinstance(plan, list) or not plan:
        raise SystemExit(f"plan 要是非空的事件列表 [{{{', '.join(PLAN_KEYS)}}}]，拿到的是 {type(plan).__name__}")
    out: list[Event] = []
    t = 0.0
    for i, x in enumerate(plan, 1):
        e = x if isinstance(x, dict) else {k: getattr(x, k) for k in PLAN_KEYS}
        miss = [k for k in PLAN_KEYS if k not in e]
        if miss:
            raise SystemExit(f"plan 第 {i} 个事件缺 {miss}（要 {list(PLAN_KEYS)}）")
        ev = Event(str(e["id"]), str(e["shot"]), str(e["take"]), float(e["src_in"]), float(e["src_out"]),
                   round(t, 6), float(e["dur"]), str(e["kind"]))
        if not (pc.SHOT_RE.fullmatch(ev.shot) and edl.TAKE_RE.fullmatch(ev.take) and 0 <= ev.src_in < ev.src_out
                and ev.dur > 0 and frames(ev.dur - (ev.src_out - ev.src_in)) <= TOL_FRAMES):
            raise SystemExit(f"plan 事件 {ev.id} 不成立（shot 名、take sha 前 12 位、0 ≤ src_in < src_out、dur ≈ src_out − src_in）：{e}")
        out.append(ev)
        t += ev.dur
    return out


def events_from_segments(video: Path, epd: Path) -> tuple[list[Event], str]:
    seg = video.with_name(video.stem + ".segments.json")
    if not seg.is_file():
        raise SystemExit(f"没有 plan，也没有 {seg.name}：用 --plan 给事件表（tools/post/edl.py plan）")
    parts = segments.read_parts(seg)
    if parts is not None:
        return ([Event(p.event, p.shot, p.take, p.src_in, p.src_out, p.start, p.dur, "shot") for p in parts],
                f"{seg.name}（v2：事件、take、源片入 / 出点照读；segments 不记 kind，一律按 shot）")
    segs = pc.read_segments(seg)
    mp4s = _present([pc.shot_mp4(epd / "shots" / s.shot) for s in segs])
    evs = [Event(segments.WHOLE_ID % i, s.shot, pc.take_id(pc.sha256(p)), 0.0, s.dur, s.start, s.dur, "shot")
           for i, (s, p) in enumerate(zip(segs, mp4s), 1)]
    return evs, f"{seg.name}（v1 整镜顺排，源起点记 0）"


def _present(takes: list[Path]) -> list[Path]:
    if missing := [pc.rel(p) for p in takes if not p.is_file()]:
        raise SystemExit(f"进片的 take 不在：{missing}")
    return takes


def takes_of(evs: list[Event], epd: Path) -> list[Path]:
    return _present(list(dict.fromkeys(pc.shot_mp4(epd / "shots" / e.shot) for e in evs)))


# ─────────────────────────── 回读 ───────────────────────────

def _log(cmd: list[str | Path]) -> str:
    r = subprocess.run([str(c) for c in cmd], capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit(f"命令失败（{r.returncode}）：{' '.join(str(c) for c in cmd[:8])} …\n{err[-1500:]}")
    return err


def _rate(s: str) -> Fraction:
    return Fraction(0) if s.endswith("/0") else Fraction(s)


def streams(video: Path) -> Streams:
    r = subprocess.run([pc.FFPROBE, "-v", "error", "-show_entries",
                        "stream=codec_type,codec_name,avg_frame_rate,r_frame_rate,pix_fmt,sample_rate,bit_rate",
                        "-of", "json", str(video)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ffprobe 读不了 {video}：{r.stderr.decode('utf-8', 'replace')[-300:]}")
    ss = json.loads(r.stdout)["streams"]
    v = next((s for s in ss if s["codec_type"] == "video"), None)
    if v is None:
        raise SystemExit(f"{video} 没有视频流")
    a = next((s for s in ss if s["codec_type"] == "audio"), None)
    return Streams(_rate(v["avg_frame_rate"]), _rate(v["r_frame_rate"]), v.get("pix_fmt", ""), int(v.get("bit_rate", 0)),
                   a["codec_name"] if a else None, int(a["sample_rate"]) if a else None)


def scan(video: Path, dur: float) -> Scan:
    """一遍解码：scdet 逐帧 mafd 与分（metadata=print）+ blackdetect + freezedetect（冻到片尾的没有 freeze_end，按片尾算）。"""
    vf = f"scdet=threshold={SC_CUT},metadata=print,blackdetect=d={BLACK_MIN_S},freezedetect=d={FREEZE_MIN_S}"
    err = _log([pc.FFMPEG, "-hide_banner", "-nostats", "-i", video, "-map", "0:v:0", "-vf", vf, "-f", "null", "-"])
    rows: list[list[float]] = []                        # [秒, mafd, 分]
    for t, key, val in META_RE.findall(err):
        if t:
            rows.append([float(t), 0.0, 0.0])
        elif rows:
            rows[-1][1 if key == "mafd" else 2] = float(val)
    mafd = [r[1] for r in rows]
    cuts = []
    for j, (t, v, s) in enumerate(rows):
        around = [mafd[k] for k in range(max(0, j - SPIKE_WIN), min(len(rows), j + SPIKE_WIN + 1)) if abs(k - j) >= 2]
        spike = v >= SPIKE_MAFD and v >= SPIKE_RATIO * statistics.median(around or [0.0])
        if spike or s >= SC_CUT:
            cuts.append(Change(t, v, s, spike))
    starts = [float(x) for x in FREEZE_START_RE.findall(err)]
    ends = [float(x) for x in FREEZE_END_RE.findall(err)]
    return Scan(cuts, [(float(a), float(b)) for a, b in BLACK_RE.findall(err)],
                [(a, ends[i] if i < len(ends) else dur) for i, a in enumerate(starts)])


def momentary(video: Path) -> list[tuple[float, float]]:
    """ebur128 每 0.1 s 一块的 M（400 ms 窗）→ [(块尾秒, LUFS)]；块尾按毫秒取整（ebur128 打印成 0.399979 这类）。"""
    err = _log([pc.FFMPEG, "-hide_banner", "-nostats", "-i", video, "-map", "0:a:0", "-af", "ebur128=framelog=info",
                "-f", "null", "-"])
    return [(round(float(t), 3), float(m)) for t, m in EBU_RE.findall(err)]


def _power_mean(lufs: list[float]) -> float:
    return 10 * math.log10(sum(10 ** (x / 10) for x in lufs) / len(lufs))


def gated_lufs(blocks: list[tuple[float, float]], spans: list[tuple[float, float]]) -> float | None:
    """BS.1770 门控响度，只取整块落在 spans 里的 400 ms 块：绝对门 −70 LUFS、相对门 −10 LU。一块都没有 → None。"""
    ms = [m for t, m in blocks if m > GATE_ABS_LUFS and any(a <= round(t - GATE_BLOCK_S, 3) and t <= b for a, b in spans)]
    if not ms:
        return None
    rel = _power_mean(ms) - GATE_REL_LU
    return _power_mean([m for m in ms if m > rel])


def srt_cues(p: Path) -> list[tuple[float, float, str]]:
    out = []
    for block in re.split(r"\n\s*\n", p.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        k = next((i for i, ln in enumerate(lines) if SRT_TIME_RE.search(ln)), None)
        if k is None:
            raise SystemExit(f"{p.name}：这一块没有时间行——{block[:80]!r}")
        g = [int(x) for x in SRT_TIME_RE.search(lines[k]).groups()]
        out.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                    "\n".join(lines[k + 1:])))
    return out


# ─────────────────────────── Q1–Q9 ───────────────────────────

def _verdict(probs: list[str], ok: str, data: dict[str, object] | None = None) -> Check:
    return Check(FAIL, "；".join(probs), data or {}) if probs else Check(PASS, ok, data or {})


def _broken(*rules: tuple[bool, str]) -> list[str]:
    return [msg for bad, msg in rules if bad]


def q1(evs: list[Event], m: pc.Media) -> Check:
    total = evs[-1].end
    dv, da = frames(m.v_dur - total), frames(m.a_dur - m.v_dur)
    probs = _broken((dv > TOL_FRAMES, f"视频 {m.v_dur:.3f}s ≠ plan {total:.3f}s（差 {dv:g} 帧）"),
                    (da > TOL_FRAMES, f"音频 {m.a_dur:.3f}s 与视频差 {da:g} 帧"))
    return _verdict(probs, f"视频 {m.v_dur:.3f}s = plan {total:.3f}s；音视频差 {abs(m.a_dur - m.v_dur):.3f}s",
                    {"video_s": m.v_dur, "audio_s": m.a_dur, "plan_s": total})


def q2(m: pc.Media, st: Streams, want: tuple[int, int]) -> Check:
    probs = _broken(((m.w, m.h) != want, f"分辨率 {m.w}×{m.h} ≠ 声明 {want[0]}×{want[1]}"),
                    (st.fps != pc.FPS, f"avg_frame_rate {st.fps} ≠ {pc.FPS}"),
                    (st.r_fps != st.fps, f"r_frame_rate {st.r_fps} ≠ avg {st.fps}（不是 CFR）"),
                    (st.pix_fmt != PIX_FMT, f"像素格式 {st.pix_fmt} ≠ {PIX_FMT}"),
                    ((st.acodec, st.ar) != (pc.ACODEC, pc.AR), f"音频 {st.acodec or '无'} {st.ar or '-'} Hz ≠ {pc.ACODEC} {pc.AR} Hz"))
    return _verdict(probs, f"{m.w}×{m.h} {st.fps} fps CFR {st.pix_fmt} · {st.acodec} {st.ar} Hz",
                    {"size": [m.w, m.h], "want": list(want), "avg_frame_rate": str(st.fps), "r_frame_rate": str(st.r_fps),
                     "pix_fmt": st.pix_fmt, "acodec": st.acodec, "ar": st.ar})


def expects_cut(prev: Event, nxt: Event, epd: Path) -> bool:
    """这个边界画面上该不该有切：同一 take 源里相接的没有；原镜间的承接缝（后一镜 seam: 承接）沿用原判定，不要求检出。"""
    if prev.take == nxt.take and frames(nxt.src_in - prev.src_out) <= TOL_FRAMES:
        return False
    return not (pc.shot_no(Path(nxt.shot)) == pc.shot_no(Path(prev.shot)) + 1
                and pc.is_chengjie(pc.shot_md(epd / "shots" / nxt.shot)))


def q3(evs: list[Event], sc: Scan, epd: Path) -> Check:
    pairs = list(zip(evs, evs[1:]))
    probs, matched, lenient = [], set(), 0
    for prev, nxt in pairs:
        near = [c for c in sc.cuts if frames(c.t - nxt.start) <= TOL_FRAMES]
        if near:
            matched.add(min(near, key=lambda c: abs(c.t - nxt.start)))
        elif expects_cut(prev, nxt, epd):
            probs.append(f"{nxt.start:.3f}s（{prev.id}→{nxt.id}）±{TOL_FRAMES} 帧内没检出切点")
        else:
            lenient += 1
    for prev, nxt in pairs:
        extra = [c for c in sc.cuts if c not in matched and c.strong and abs(c.t - nxt.start) <= FLASH_WIN_S]
        if extra:
            probs.append(f"{nxt.start:.3f}s（{prev.id}→{nxt.id}）±{FLASH_WIN_S:g}s 内多出强切 "
                         + "、".join(f"{c.t:.3f}s（mafd {c.mafd:.1f}，分 {c.score:.1f}）" for c in extra) + "——闪帧？")
    ok = f"{len(pairs)} 个事件边界都在 ±{TOL_FRAMES} 帧内检出切点、旁边无闪帧" if pairs else "只有一个事件，没有边界"
    ok += f"（其中 {lenient} 个承接 / 源内相接的边界不要求检出）" if lenient else ""
    return _verdict(probs, ok, {"boundaries": [round(n.start, 3) for _, n in pairs],
                                "cuts": [[round(c.t, 3), c.mafd, c.score, c.spike] for c in sc.cuts]})


def q4(evs: list[Event], sc: Scan) -> Check:
    holds = [e for e in evs if e.kind in HOLD_KINDS]
    hits = [(what, a, b) for what, spans in (("黑场", sc.black), ("冻帧", sc.freeze)) for a, b in spans
            if not any(e.start - FRAME_S <= a and b <= e.end + FRAME_S for e in holds)]
    return _verdict([f"{what} {a:.2f}–{b:.2f}s" for what, a, b in hits],
                    f"无黑场（≥{BLACK_MIN_S:g}s）、无冻帧（≥{FREEZE_MIN_S:g}s）",
                    {"black": sc.black, "freeze": sc.freeze})


def q5(video: Path, m: pc.Media) -> Check:
    if not m.has_audio:
        return Check(FAIL, "没有音轨")
    r = mux_av.measure_loudness(pc.FFMPEG, video)
    i, tp, lra = float(r["input_i"]), float(r["input_tp"]), float(r["input_lra"])
    line = f"I {i:.1f} LUFS · TP {tp:.1f} dBTP · LRA {lra:.1f} LU"
    data: dict[str, object] = {"i": i, "tp": tp, "lra": lra}
    probs = _broken((abs(i - LOUD_I) > LOUD_TOL_LU, f"I 不在 {LOUD_I:g} ±{LOUD_TOL_LU:g}"),
                    (tp > TP_MAX, f"TP 高于 {TP_MAX:g}"))
    if probs:
        return Check(FAIL, f"{line}：{'；'.join(probs)}", data)
    if not LRA_RANGE[0] <= lra <= LRA_RANGE[1]:
        return Check(WARN, f"{line}：LRA 不在 [{LRA_RANGE[0]:g}, {LRA_RANGE[1]:g}]（先只警告）", data)
    return Check(PASS, line, data)


def dialogue_spans(ev: Event, speech: tuple[tuple[float, float], ...], lo: float, hi: float) -> list[tuple[float, float]]:
    """take 的 speech 区间（源秒）→ 成片秒，裁到本事件与 [lo, hi]。"""
    out = []
    for a, b in speech:
        a2 = max(ev.start + a - ev.src_in, ev.start, lo)
        b2 = min(ev.start + b - ev.src_in, ev.end, hi)
        if b2 > a2:
            out.append((round(a2, 3), round(b2, 3)))
    return out


def q6(video: Path, evs: list[Event], m: pc.Media, epd: Path, align_dir: Path | None, selftest: bool) -> Check:
    pairs = list(zip(evs, evs[1:]))
    if not pairs:
        return Check(PASS, "只有一个事件，没有接缝")
    caches: dict[str, edl.Align] = {}
    missing, stale = [], []
    for e in dict.fromkeys(x for pair in pairs for x in pair):
        p = edl.align_path(epd, e.shot, e.take)
        p = align_dir / p.name if align_dir else p
        if not p.is_file():
            missing.append(p)
            continue
        try:
            caches[e.id] = edl.read_align(p, e.shot, e.take)
        except SystemExit as why:
            stale.append(str(why))
    if stale:
        return Check(FAIL, "；".join(dict.fromkeys(stale)))
    if missing:
        why = f"缺 align 缓存 {sorted({p.name for p in missing})}（{pc.rel(missing[0].parent)}；先跑 tools/post/align.py）"
        return Check(SKIP, why + "——自测模式记 SKIP") if selftest else Check(FAIL, why)
    if not m.has_audio:
        return Check(FAIL, "没有音轨")
    blocks = momentary(video)
    rows, probs = [], []
    for prev, nxt in pairs:
        b = nxt.start
        left = gated_lufs(blocks, dialogue_spans(prev, caches[prev.id].speech, b - SEAM_WIN_S, b))
        right = gated_lufs(blocks, dialogue_spans(nxt, caches[nxt.id].speech, b, b + SEAM_WIN_S))
        rows.append({"t": round(b, 3), "events": [prev.id, nxt.id], "left": left, "right": right})
        if left is not None and right is not None and abs(left - right) > SEAM_JUMP_LU:
            probs.append(f"{b:.3f}s（{prev.id}→{nxt.id}）对白 {left:.1f} → {right:.1f} LUFS，跳 {abs(left - right):.1f} LU")
    both = sum(r["left"] is not None and r["right"] is not None for r in rows)
    return _verdict([f"{p}（> {SEAM_JUMP_LU:g} LU）" for p in probs],
                    f"{both}/{len(rows)} 个接缝两侧都有对白，响度差都 ≤ {SEAM_JUMP_LU:g} LU", {"seams": rows})


def q7(video: Path, evs: list[Event], m: pc.Media) -> Check:
    files = [video.with_name(video.stem + s) for s in SRT_SUFFIXES]
    files = [p for p in files if p.is_file()]
    if not files:
        return Check(FAIL, f"没有字幕：{' / '.join(video.stem + s for s in SRT_SUFFIXES)}")
    probs, n = [], 0
    for p in files:
        for k, (a, b, text) in enumerate(srt_cues(p), 1):
            n += 1
            tag = f"{p.name} #{k}（{a:.3f}–{b:.3f}s）"
            if b <= a or a < 0 or (b > m.v_dur and frames(b - m.v_dur) > TOL_FRAMES):
                probs.append(f"{tag} 不在成片 0–{m.v_dur:.3f}s 内")
                continue
            ev = next(e for e in reversed(evs) if a >= e.start - FRAME_S / 2)     # SRT 毫秒取整可能落在边界前半帧
            if b > ev.end and frames(b - ev.end) > TOL_FRAMES:
                probs.append(f"{tag} 越过 {ev.id} 尾 {ev.end:.3f}s")
            rate, cap = subs.cps(text, b - a), subs.cps_cap(text)
            if rate > cap:
                probs.append(f"{tag} CPS {rate:.1f} > {cap:g}")
    return _verdict(probs, f"{'、'.join(p.name for p in files)} 共 {n} 条：都在成片与所属事件内，CPS 未超",
                    {"files": [p.name for p in files], "cues": n})


def q8(video: Path, takes: list[Path]) -> Check:
    want = aigc.collect(takes)
    if not want:
        return Check(WARN, "进片 take 都没有 AIGC 标签（旧剧 / 非即梦出片），成片没有可写回的隐式标识——发布时在平台手动勾 AI 标识", {})
    miss = aigc.readback(video, want)
    return _verdict([f"AIGC 标识缺 {miss}"] if miss else [], f"AIGC 标识在，ProduceID 含 {len(takes)} 条进片 take 的")


def q9(st: Streams) -> Check:
    line = f"视频码率 {st.v_bitrate / 1e6:.2f} Mbps（下限 {BITRATE_MIN / 1e6:g}）"
    return Check(PASS if st.v_bitrate >= BITRATE_MIN else FAIL, line, {"bps": st.v_bitrate})


# ─────────────────────────── 入口 ───────────────────────────

def run(video: Path, plan: list[dict] | list[edl.Cut] | None, epd: Path, *, selftest: bool = False,
        align_dir: Path | None = None) -> dict:
    """回读成片、写报告、打印摘要；任一 FAIL 即 SystemExit（报告已落盘）。
    plan：plan.json 的行或 edl.plan() 的 Cut；None 时读 {视频名}.segments.json（events_from_segments）。
    align_dir：对齐缓存目录（默认 edl.align_path 的 post/align/；自测指向合成缓存）。"""
    evs, plan_src = (events(plan), "plan") if plan is not None else events_from_segments(video, epd)
    takes = takes_of(evs, epd)
    m, st = pc.probe(video), streams(video)
    sizes = [pc.probe(p) for p in takes]
    sc = scan(video, m.v_dur)
    checks = {"Q1": q1(evs, m),
              "Q2": q2(m, st, pc.master_size(max(s.w for s in sizes), max(s.h for s in sizes))),
              "Q3": q3(evs, sc, epd),
              "Q4": q4(evs, sc),
              "Q5": q5(video, m),
              "Q6": q6(video, evs, m, epd, align_dir, selftest),
              "Q7": q7(video, evs, m),
              "Q8": q8(video, takes),
              "Q9": q9(st)}
    failed = [k for k, c in checks.items() if c.status == FAIL]
    sha = pc.sha256(video)
    rep = {"version": 1, "video": pc.rel(video), "video_sha256": sha, "plan": plan_src, "selftest": selftest,
           "result": FAIL if failed else PASS,
           "events": [{"id": e.id, "shot": e.shot, "take": e.take, "start": round(e.start, 3), "end": round(e.end, 3),
                       "kind": e.kind} for e in evs],
           "checks": {k: asdict(c) for k, c in checks.items()}}
    out = report_path(epd, video)
    out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.name + ".part")
    part.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    part.replace(out)
    print(f"QC {video.name}（sha {pc.take_id(sha)}，{len(evs)} 个事件）：{rep['result']}")
    for k, c in checks.items():
        print(f"  {k} {c.status:<4} {c.detail}")
    print(f"报告 → {pc.rel(out)}")
    if failed:
        raise SystemExit(f"QC 没过：{'、'.join(failed)}（{pc.rel(out)}）")
    return rep


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="成片回读 QC（Q1–Q9），报告绑视频 sha256")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--video", type=Path, default=None, help="默认 {ep}_final.mp4")
    ap.add_argument("--plan", type=Path, default=None, help="事件表 plan.json；不给就读视频自己的 {视频名}.segments.json")
    ap.add_argument("--selftest", action="store_true", help="缺 align 缓存时 Q6 记 SKIP 而不是 FAIL（只给自测用）")
    a = ap.parse_args()
    epd = pc.ep_dir(pc.drama_root(a.drama), a.ep)
    video = a.video or epd / f"{epd.name}_final.mp4"
    if not video.is_file():
        raise SystemExit(f"找不到 {video}")
    if a.plan and not a.plan.is_file():
        raise SystemExit(f"找不到 {a.plan}")
    run(video, json.loads(a.plan.read_text(encoding="utf-8")) if a.plan else None, epd, selftest=a.selftest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
