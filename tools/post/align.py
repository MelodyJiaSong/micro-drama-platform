# -*- coding: utf-8 -*-
"""台词实测层：take（默认 shotNN.mp4）的原生人声对齐到 shot md 的台词，加自由转写 WER 与镜内切点，
逐镜落盘 {ep}/post/align/{shot}.{sha12}.json，给 edl.py（锚点 / 合法切点）、subs.py（字幕时间）、qc.py（接缝对白）读。

    .venv-post/Scripts/python.exe tools/post/align.py <剧> <ep> [--shots 5,6] [--take PATH] [--model medium.en] [--force]

要 torch + stable-ts：在 pc.ALIGN_PYTHON 下跑，别的工具 subprocess.run([pc.ALIGN_PYTHON, 本文件, …]) 调；
顶层只依赖标准库，默认 Python 也能 import（读缓存的工具用 cache_path）。
- 台词：pc.dialogue(md)。pc.onscreen 判为不动嘴的（内心独白 / 画外 / 系统提示音）不在原生音轨里：offscreen，start/end＝计划窗，无 words。
- 对齐：画内台词按序一句一行拼成一段，stable-ts align 一次对齐、按行切回；conf＝该句词概率均值（纯标点不算词）；
  ok / low_conf（conf < ALIGN_MIN_CONF）/ missing（过半的词被挤成零时长：这句不在按剧本顺序该在的地方——
  没说、或被模型调了语序；start/end 退回计划窗、无 words）。
- ASR：同一模型 transcribe 自由转写（词与时刻存进 asr.words），与画内台词拼接文本比 WER；WER > WER_MAX 整镜进人听清单。
  归一口径 norm_words：whisper 的 EnglishTextNormalizer 逐词过（twelve＝12、didn't＝did not 不算错）。
- 对照 ASR（ok / low_conf 句）：句首、句尾的词，ASR 在交叠的时间里听到同一个词，就把句首收到 ASR 的起、句尾收到
  ASR 的止（只缩不扩）；再算覆盖率 cover＝这句的词 ASR 在实测起止 ±COVER_WIN 内听到几成，< COVER_MIN 降为 low_conf。
- 找回（relocate）：missing 句在 asr.words 里按序找一段（错听 / 漏词 / 段内多词各记一次错；别的句子的词只许原词对上，
  不许顶替、不许夹在段内），原词对上 ≥ MOVE_MIN、对上的 ASR 词不过半已归别的句子（ok / low_conf 句的同词）。几句一起找，
  对上的原词多的先定。起止不取 ASR 词的（whisper 常把 take 的第一个词拖回 0 s）：在那段音频上用同一模型重新强制对齐这句、
  照 ok 句 settle → moved，moved 记计划窗、找到处与对上几成；重对时过半的词挤成零时长就不算，仍 missing。
  与它重叠的 ok / low_conf 句让位：每个词夹出找回句的起止，夹出来的边对上 ASR 才收（只缩不扩），覆盖率不够降 low_conf。
  moved 句进人听清单，注明抢到了哪几句之前 / 落到了哪几句之后。
- speech：ok / low_conf / moved 句的词（收过首尾），间隙 < SPEECH_GAP 并成一段。
- 切点：planned＝设计稿「分镜:」行（prompt_compact.segments，与上传 Seedance 的整秒一致）里带【切】的段起点；
  detected＝ffmpeg scdet：每个计划切点 ±CUT_WIN 内分 ≥ SC_NEAR 的取最强一下，另加全片分 ≥ SC_ANY 的（模型自己加的硬切）。
- frames：按 pc.FPS 转成恒定帧率后的帧数（pc.cfr_frames）——edl 的 end 与整镜出点就是它，不拿容器时长乘帧率。
- 缓存键＝take 文件 sha256；version、模型、台词、计划切点都没变就跳过（--force 重算）。逐镜写 .part 再 replace，可续跑。
  模型一个进程只加载一次（全命中缓存就不加载）；某镜显存不够就那一镜改用 CPU，报表里标出来。
"""
from __future__ import annotations

import argparse
import contextlib
import functools
import io
import json
import re
import subprocess
import tempfile
import time
import warnings
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TypeVar

import post_common as pc
import prompt_compact    # tools/ 下的，post_common 已把 tools/ 加进 sys.path
import shot_logic

VERSION = 5
ALIGN_SUB = "align"                 # {ep}/post/align/{shot}.{sha12}.json
MODEL = "medium.en"
LANG = "en"
SR = 16000
ALIGN_MIN_CONF = 0.5
# 概率拦不住错位：强制对齐的词概率是「给定这段文字」的解码概率，挤成零时长的词照样 0.9+
# （shot05 模型把「Dad's boots are fine.」挪到前一句之前说，按剧本顺序对齐时它被挤在 40 ms 里：4 词 3 个零时长、概率均值 0.86）
MISSING_FRAC = 0.5
MOVE_MIN = 0.7      # missing 句：ASR 里按序对上这么多成的原词才算找回（moved）
MOVE_TAKEN = 0.5    # 对上的 ASR 词 > 这么多成已归别的句子：那是别人的句子（重复的短语），不算
MOVE_PAD = 0.3      # 找回句重对齐：那段 ASR 词前后各放宽这么多秒（不越过段外相邻的 ASR 词）——ASR 的词边可能切短了
WER_MAX = 0.25
COVER_MIN = 0.6
COVER_WIN = 1.0
SPEECH_GAP = 0.15
CUT_MARK = "【切】"
CUT_WIN = 0.5
# scdet 分（0–100；8 位视频 = select 的 scene × 39.0625）。ep01 八条 take 实测：真切 6.96–22.3（含模型自加的硬切
# shot05 27.22s 9.8、shot06 21.25s 11.9），切后次帧余波 ≤ 6.2，非切的打斗 ≤ 5.6。
# 规格原值 select 0.30 / 0.45（= 11.7 / 17.6）漏 6 处真切：计划切 4 处、模型自加的 2 处。
SC_NEAR = 6.0     # 计划切点 ±CUT_WIN 内：取最强、不取最近——余波可能离计划更近（shot06 5.833s 6.2 紧跟 5.800s 11.5 的真切）
SC_ANY = 8.0      # 没有计划切点佐证也算切
EPS = 1e-6
SCD_RE = re.compile(r"lavfi\.scd\.score: ([\d.]+), lavfi\.scd\.time: ([\d.]+)")
WORD_RE = re.compile(r"[^\W_]+")
OK, LOW, MOVED, MISSING, OFFSCREEN = "ok", "low_conf", "moved", "missing", "offscreen"
STATUSES = (OK, LOW, MOVED, MISSING, OFFSCREEN)
TIMED = (OK, LOW, MOVED)            # start / end / words 是实测的：edl 锚点与切词、subs 字幕时间、speech 都只认这几种

Word = tuple[str, float, float, float]      # 对齐词：（文字, 起, 止, 概率）
Heard = tuple[str, float, float]            # ASR 自由转写的词：（文字, 起, 止）
Realign = Callable[[str, float, float], list[Word]]     # （句子, 起, 止）→ 这句强制对齐在 take 的这段音频上的词（秒是整条 take 的）
T = TypeVar("T")


def cache_path(epd: Path, shot: str, sha: str) -> Path:
    return epd / pc.POST_DIR / ALIGN_SUB / f"{shot}.{pc.take_id(sha)}.json"


# ─────────────────────────── 读源 ───────────────────────────

def planned_cuts(md_text: str, secs: float) -> list[float]:
    """设计稿「分镜:」行里带【切】的段起点（秒）。"""
    design = shot_logic.positive(md_text) or ""
    return [float(s.a) for s in prompt_compact.segments(prompt_compact.fields(design), secs) if s.head.startswith(CUT_MARK)]


def audio_16k(take: Path) -> Any:
    import numpy as np
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        pc.run([pc.FFMPEG, "-y", "-v", "error", "-i", take, "-map", "0:a:0", "-ac", "1", "-ar", str(SR),
                "-c:a", "pcm_s16le", wav])
        with wave.open(str(wav), "rb") as w:
            raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def scene_hits(take: Path) -> list[tuple[float, float]]:
    """scdet 检出的（秒, 分），只列分 ≥ SC_NEAR 的帧。"""
    r = subprocess.run([pc.FFMPEG, "-hide_banner", "-nostats", "-i", str(take), "-map", "0:v:0",
                        "-vf", f"scdet=threshold={SC_NEAR}", "-f", "null", "-"], capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit(f"scdet 读不了 {pc.rel(take)}：{err[-500:]}")
    return [(float(t), float(s)) for s, t in SCD_RE.findall(err)]


# ─────────────────────────── 判读 ───────────────────────────

def pick_cuts(hits: list[tuple[float, float]], planned: list[float]) -> list[float]:
    near = []
    for p in planned:
        win = [h for h in hits if abs(h[0] - p) <= CUT_WIN + EPS and h[1] >= SC_NEAR]
        if win:
            near.append(max(win, key=lambda h: (h[1], -abs(h[0] - p))))
    return sorted({round(t, 3) for t, _ in near + [h for h in hits if h[1] >= SC_ANY]})


def line_record(idx: int, ln: pc.Line, words: list[Word] | None) -> dict:
    """一句的实测结果；words=None 表示不在原生音轨里（画外 / 内心独白）。"""
    rec: dict = {"idx": idx, "speaker": ln.speaker, "kind": ln.kind, "text": ln.text, "planned": [ln.t0, ln.t1]}
    if words is None:
        return rec | {"start": ln.t0, "end": ln.t1, "conf": None, "words": [], "status": OFFSCREEN}
    return judge(rec, words)


def judge(rec: dict, words: list[Word]) -> dict:
    """一句强制对齐出来的词 → conf、ok / low_conf / missing、起止与 words；missing 退回计划窗、无 words。"""
    spoken = [w for w in words if WORD_RE.search(w[0])]
    conf = round(sum(w[3] for w in spoken) / len(spoken), 3) if spoken else 0.0
    timed = [w for w in spoken if w[2] > w[1]]
    if len(spoken) - len(timed) > MISSING_FRAC * len(spoken) or not timed:
        return rec | {"start": rec["planned"][0], "end": rec["planned"][1], "conf": conf, "words": [], "status": MISSING}
    return rec | {"start": round(min(w[1] for w in timed), 3), "end": round(max(w[2] for w in timed), 3), "conf": conf,
                  "words": [{"w": w[0].strip(), "s": round(w[1], 3), "e": round(w[2], 3), "p": round(w[3], 3)}
                            for w in spoken],
                  "status": OK if conf >= ALIGN_MIN_CONF else LOW}


def speech_spans(lines: list[dict]) -> list[list[float]]:
    ws = sorted((w["s"], w["e"]) for ln in lines if ln["status"] in TIMED for w in ln["words"] if w["e"] > w["s"])
    out: list[list[float]] = []
    for s, e in ws:
        if out and s - out[-1][1] < SPEECH_GAP:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


@functools.cache
def _normalizer() -> Callable[[str], str]:
    from whisper.normalizers import EnglishTextNormalizer
    return EnglishTextNormalizer()


def norm_words(text: str) -> list[str]:
    """WER / 覆盖率 / 同词判定的口径：whisper 的 EnglishTextNormalizer 逐词过（twelve → 12、didn't → did not、first → 1st），
    只留含字母数字的词。逐词不整句：整句会把连着的数词并成一个数（One, two, three → 123，报号码的规则），数数的台词整句算错。"""
    norm = _normalizer()
    return [t for w in text.split() for t in norm(w).split() if WORD_RE.search(t)]


def wer(ref: list[str], hyp: list[str]) -> float:
    """词级编辑距离 ÷ 参考词数；参考为空按 1 算（没有画内台词的镜转出了话，每个词记一个错）。"""
    row = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        diag, row[0] = row[0], i
        for j, h in enumerate(hyp, 1):
            diag, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, diag + (r != h))
    return row[-1] / max(1, len(ref))


def trim_edges(words: list[dict], heard: list[Heard]) -> list[dict]:
    """句首、句尾那个词：ASR 在交叠的时间里听到同一个词 → 句首收到 ASR 的起、句尾收到 ASR 的止（只缩不扩）。
    强制对齐会把句尾词拖进后面的静音或音效里（shot01「one.」对成 15.28–17.82）；只动句子外沿，不在句中切出空档。
    首尾词被挤成零时长就不动，也不改收它旁边的词：那会把被挤扁的词切掉（shot05「Thank」实际在 27.26–27.40）。"""
    out = [dict(w) for w in words]
    if not out:
        return out
    first, last = out[0], out[-1]
    if (k := _same_heard(first, heard)) is not None:
        first["s"] = round(max(first["s"], heard[k][1]), 3)
    if (k := _same_heard(last, heard)) is not None:
        last["e"] = round(min(last["e"], heard[k][2]), 3)
    return out


def _same_heard(w: dict, heard: list[Heard]) -> int | None:
    """ASR 里与对齐词 w 同词（norm_words 相同）、有时长、且与 w 时间上交叠的词的序号；多个取交叠最长的。"""
    key = norm_words(w["w"])
    if not key:
        return None
    hits = [k for k, h in enumerate(heard) if h[2] > h[1] and h[1] < w["e"] and h[2] > w["s"] and norm_words(h[0]) == key]
    return max(hits, key=lambda k: min(w["e"], heard[k][2]) - max(w["s"], heard[k][1]), default=None)


def coverage(text: str, start: float, end: float, heard: list[Heard]) -> float | None:
    """这句归一后的词里，ASR 在 start − COVER_WIN … end + COVER_WIN 内听到了几成（听到的每个词只抵一次）；归一后没有词 → None。"""
    want = norm_words(text)
    if not want:
        return None
    pool = [t for w, s, e in heard if s <= end + COVER_WIN and e >= start - COVER_WIN for t in norm_words(w)]
    hit = 0
    for t in want:
        if t in pool:
            pool.remove(t)
            hit += 1
    return round(hit / len(want), 3)


def settle(rec: dict, heard: list[Heard]) -> dict:
    """一句的对齐结果对照 ASR：收首尾（trim_edges）、重算起止、算覆盖率，覆盖率 < COVER_MIN 降为 low_conf。
    missing / offscreen 不动（cover 记 None）。"""
    if rec["status"] not in (OK, LOW):
        return rec | {"cover": None}
    words = trim_edges(rec["words"], heard)
    timed = [w for w in words if w["e"] > w["s"]]
    start, end = min(w["s"] for w in timed), max(w["e"] for w in timed)
    cover = coverage(rec["text"], start, end, heard)
    low = cover is not None and cover < COVER_MIN
    return rec | {"start": start, "end": end, "words": words, "cover": cover, "status": LOW if low else rec["status"]}


@dataclass(frozen=True)
class Fit:
    """一句的词按序对进 ASR 词串里的一段（_fit）。lo / hi：段首 / 段尾的 toks 下标（含两端）；
    pairs：对位的（want 下标, toks 下标），原词对上或错听顶替；hits：其中原词对上的 toks 下标。"""
    cost: int
    lo: int
    hi: int
    pairs: tuple[tuple[int, int], ...]
    hits: tuple[int, ...]


@dataclass(frozen=True)
class Found:
    """missing 句在 ASR 里找到的一段（_find）。words：段内 ASR 词序号（含段内多出的词）；claim：对位的 ASR 词序号（找回后锁住）；
    match：原词对上几成；rank：几句一起找时谁先定（对上的原词多的先、错少的先、离计划窗近的先）。"""
    idx: int
    words: tuple[int, ...]
    claim: frozenset[int]
    match: float
    rank: tuple[int, int, float]


def _fit(want: list[str], toks: list[str], free: list[bool]) -> list[Fit]:
    """want（一句归一后的词）按序对进 toks（ASR 归一后的词串）里的一段：编辑距离，错听 / 漏词 / 段内多出的词各记 1，
    段前段后不计；free[j] 为假的 toks[j]（别的句子的词）只许原词对上：不许顶替错听的词，也不许夹在段内当多出的词。
    每个段尾一个解，回溯先走对位：句首句尾错听的词（Kobolds 听成 Cobbles）算进段里。"""
    n, m = len(want), len(toks)
    inf = float("inf")
    d = [[0.0] * (m + 1)] + [[float(i)] + [inf] * m for i in range(1, n + 1)]

    def pair(i: int, j: int) -> float:
        return 0.0 if want[i - 1] == toks[j - 1] else 1.0 if free[j - 1] else inf

    def extra(j: int) -> float:
        return 1.0 if free[j - 1] else inf

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j - 1] + pair(i, j), d[i - 1][j] + 1, d[i][j - 1] + extra(j))
    out = []
    for end in range(1, m + 1):
        if d[n][end] == inf:
            continue
        i, j, took, pairs = n, end, [], []
        while i:
            if j and d[i][j] == d[i - 1][j - 1] + pair(i, j):
                took.append(j - 1)
                pairs.append((i - 1, j - 1))
                i, j = i - 1, j - 1
            elif d[i][j] == d[i - 1][j] + 1:
                i -= 1
            else:
                took.append(j - 1)
                j -= 1
        if took:
            pairs.reverse()
            out.append(Fit(int(d[n][end]), took[-1], took[0], tuple(pairs), tuple(b for a, b in pairs if want[a] == toks[b])))
    return out


def _claims(recs: list[dict], heard: list[Heard]) -> dict[int, int]:
    """ASR 词序号 → 认领它的句子 idx：ok / low_conf 句每个词在 ASR 里的同一个词（_same_heard）。"""
    out: dict[int, int] = {}
    for r in recs:
        for w in r["words"] if r["status"] in (OK, LOW) else ():
            if (k := _same_heard(w, heard)) is not None:
                out.setdefault(k, r["idx"])
    return out


def _find(rec: dict, heard: list[Heard], toks: list[str], src: list[int], owner: dict[int, int],
          taken: set[int]) -> Found | None:
    """missing 句在 ASR 里的那一段：_fit 的各段里，原词对上 ≥ MOVE_MIN、对上的 ASR 词不过 MOVE_TAKEN 归了别的句子（owner）、
    不含已找回的句子的词（taken）的，取错最少、对上最多、离计划窗最近的；没有 → None。
    toks / src：全部 ASR 词归一后的词串，与每个词出自第几个 ASR 词。别的句子的词与 taken 在 _fit 里都只许原词对上。"""
    want = norm_words(rec["text"])
    if not want:
        return None
    mid = (rec["planned"][0] + rec["planned"][1]) / 2
    free = [k not in owner and k not in taken for k in src]
    best: tuple[tuple[int, int, float], Found] | None = None
    for f in _fit(want, toks, free):
        ks = tuple(sorted(set(src[f.lo:f.hi + 1])))
        got = {src[j] for j in f.hits}
        if len(f.hits) / len(want) + EPS < MOVE_MIN or not taken.isdisjoint(ks) \
                or sum(k in owner for k in got) > MOVE_TAKEN * len(got):
            continue
        dist = abs((heard[ks[0]][1] + heard[ks[-1]][2]) / 2 - mid)
        if best is None or (f.cost, -len(f.hits), dist) < best[0]:
            best = ((f.cost, -len(f.hits), dist), Found(rec["idx"], ks, frozenset(src[j] for _i, j in f.pairs),
                                                       len(f.hits) / len(want), (-len(f.hits), f.cost, dist)))
    return None if best is None else best[1]


def _retime(rec: dict, f: Found, heard: list[Heard], realign: Realign) -> dict | None:
    """找回句的起止与词：whisper 自由转写常把 take 的第一个词拖回 0 s（shot10「A」0.00–8.68s），ASR 词的起止不能直接用。
    在那段 ASR 词前后各放宽 MOVE_PAD（不越过段外相邻的 ASR 词）的音频上用同一模型强制对齐这句，再照 ok 句 settle
    （收首尾、算覆盖率）→ moved；过半的词挤成零时长（judge 判 missing）→ None：重对不上，这段不是它。"""
    first, last = f.words[0], f.words[-1]
    lo = min(heard[first][1], max([heard[first][1] - MOVE_PAD, 0.0] + [heard[k][2] for k in range(first)]))
    hi = max(heard[last][2], min([heard[last][2] + MOVE_PAD] + [heard[k][1] for k in range(last + 1, len(heard))]))
    got = settle(judge(rec, realign(rec["text"], lo, hi)), heard)
    if got["status"] == MISSING:
        return None
    return got | {"status": MOVED, "moved": {"expected": list(rec["planned"]), "found": [got["start"], got["end"]],
                                              "match": round(f.match, 3)}}


def _split(words: list[dict], a: float, b: float) -> int:
    """一句的词按序在 a–b（找回句）前后切开：words[:k] 夹到 a 之前、words[k:] 夹到 b 之后，取词的起止挪得最少的 k。"""
    def shift(k: int) -> float:
        return (sum(max(0.0, w["s"] - a) + max(0.0, w["e"] - a) for w in words[:k])
                + sum(max(0.0, b - w["s"]) + max(0.0, b - w["e"]) for w in words[k:]))
    return min(range(len(words) + 1), key=shift)


def _reclaim(rec: dict, heard: list[Heard], spans: list[tuple[float, float]], skip: set[int], rest: list[Heard]) -> dict:
    """被找回句（spans）盖住的 ok / low_conf 句让位：
    ① 每个词夹出找回句的起止，按词序在它前后切开（_split）——找回句夹在这句两个分句之间说也一样，不只收首尾；
    ② 夹出来的边（句首、句尾、找回句两侧的词）：在自己原起止内、不属于找回句与别的句子（skip）的 ASR 词里按序对这句（_fit），
       边上的词对上了（原词或错听）且时间交叠才收到那个 ASR 词（只缩不扩）；没对上的留着对齐的起止——ASR 漏听的词不当空档；
    ③ 覆盖率按去掉找回句的 ASR（rest）重算，< COVER_MIN 或一个原词都没对上降为 low_conf；词全被夹成零时长 → missing。"""
    words = [dict(w) for w in rec["words"]]
    starts, ends = {0}, {len(words) - 1}
    for a, b in sorted(spans):
        k = _split(words, a, b)
        for w in words[:k]:
            w["s"], w["e"] = min(w["s"], a), min(w["e"], a)
        for w in words[k:]:
            w["s"], w["e"] = max(w["s"], b), max(w["e"], b)
        if 0 < k < len(words):
            starts.add(k)
            ends.add(k - 1)
    ks = [k for k, h in enumerate(heard) if k not in skip and h[1] < rec["end"] and h[2] > rec["start"]]
    norm = {k: norm_words(heard[k][0]) for k in ks}
    src = [k for k in ks for _t in norm[k]]
    of = [i for i, w in enumerate(words) for _t in norm_words(w["w"])]
    fits = [f for f in _fit([t for w in words for t in norm_words(w["w"])], [t for k in ks for t in norm[k]],
                            [True] * len(src)) if f.hits]
    if fits:
        heard_of: dict[int, list[int]] = {}
        for i, j in min(fits, key=lambda f: (f.cost, -len(f.hits))).pairs:
            heard_of.setdefault(of[i], []).append(src[j])
        for i in sorted((starts | ends) & heard_of.keys()):
            w = words[i]
            s, e = min(heard[k][1] for k in heard_of[i]), max(heard[k][2] for k in heard_of[i])
            if not (w["s"] < w["e"] and s < w["e"] and e > w["s"]):
                continue
            if i in starts:
                w["s"] = max(w["s"], s)
            if i in ends:
                w["e"] = min(w["e"], e)
    timed = [w for w in words if w["e"] > w["s"]]
    if not timed:
        return rec | {"start": rec["planned"][0], "end": rec["planned"][1], "words": [], "cover": None, "status": MISSING}
    start, end = min(w["s"] for w in timed), max(w["e"] for w in timed)
    words = [w | {"s": min(max(w["s"], start), end), "e": max(min(w["e"], end), start)} for w in words]
    cover = coverage(rec["text"], start, end, rest)
    low = not fits or cover is not None and cover < COVER_MIN
    return rec | {"start": start, "end": end, "words": words, "cover": cover, "status": LOW if low else rec["status"]}


def relocate(recs: list[dict], heard: list[Heard], realign: Realign) -> list[dict]:
    """settle 之后：missing 句按 ASR 找回（_find 找段、_retime 定时间）→ moved，
    moved＝{expected: 计划窗, found: 实测起止, match: 原词对上几成}；再让与找回句重叠的 ok / low_conf 句让位（_reclaim）。
    几句 missing 一起找：每轮各找各的，先定 rank 最前的一句（「Let's go.」不抢「Let's go home.」的词），锁住它对位的 ASR 词，
    剩下的重找；重对不上的那句仍 missing、不再找。没有 missing 句、或一句都没找回：原样返回。"""
    if not any(r["status"] == MISSING for r in recs):
        return recs
    owner = _claims(recs, heard)
    norm = [norm_words(h[0]) for h in heard]
    toks = [t for ts in norm for t in ts]
    src = [k for k, ts in enumerate(norm) for _t in ts]
    taken: set[int] = set()
    todo = {r["idx"]: r for r in recs if r["status"] == MISSING}
    done: dict[int, dict] = {}
    while found := [f for f in (_find(r, heard, toks, src, owner, taken) for r in todo.values()) if f is not None]:
        best = min(found, key=lambda f: f.rank)
        got = _retime(todo.pop(best.idx), best, heard, realign)
        if got is not None:
            done[best.idx] = got
            taken |= best.claim
    if not done:
        return recs
    spans = [(r["start"], r["end"]) for r in done.values()]
    rest = [h for k, h in enumerate(heard) if k not in taken]
    out = []
    for r in recs:
        r = done.get(r["idx"], r)
        mine = [(a, b) for a, b in spans if r["status"] in (OK, LOW) and r["start"] < b and a < r["end"]]
        out.append(_reclaim(r, heard, mine, taken | {k for k, i in owner.items() if i != r["idx"]}, rest) if mine else r)
    return out


def inputs(lines: list[pc.Line]) -> list[list]:
    """缓存的输入部分：每句（序号, 人, 类型, 句子, 计划窗）。"""
    return [[i, ln.speaker, ln.kind, ln.text, [ln.t0, ln.t1]] for i, ln in enumerate(lines, 1)]


def stale(cached: dict | None, model: str, want: list[list], planned: list[float]) -> str | None:
    """缓存还能用 → None；否则返回要重算的原因。"""
    if cached is None:
        return "没有缓存"
    if cached.get("version") != VERSION:
        return f"缓存 version {cached.get('version')} ≠ {VERSION}"
    if cached.get("model") != model:
        return f"缓存是 {cached.get('model')} 对的"
    if [[x["idx"], x["speaker"], x["kind"], x["text"], x["planned"]] for x in cached.get("lines", [])] != want:
        return "台词（人 / 类型 / 句子 / 时间窗）变了"
    if cached.get("cuts", {}).get("planned") != planned:
        return "计划切点变了"
    return None


# ─────────────────────────── 模型 ───────────────────────────

class Engine:
    """stable-ts 模型：一个进程只加载一次；某镜显存不够就那一镜改用 CPU（CPU 副本第一次要用时加载，之后复用）。"""

    def __init__(self, name: str) -> None:
        import torch
        self.name, self.torch = name, torch
        self.models: dict[str, Any] = {}

    def _model(self, device: str) -> Any:
        if device not in self.models:
            import stable_whisper
            self.models[device] = stable_whisper.load_model(self.name, device=device)
        return self.models[device]

    def run(self, shot: str, fn: Callable[[Any], T]) -> tuple[T, str]:
        if self.torch.cuda.is_available():
            try:
                return fn(self._model("cuda")), "cuda"
            except RuntimeError as e:                   # torch.OutOfMemoryError 也是 RuntimeError
                if "out of memory" not in str(e):
                    raise
                self.torch.cuda.empty_cache()
                pc.warn(f"{shot}：显存不够（别的会话可能在用 GPU），这一镜改用 CPU")
        return fn(self._model("cpu")), "cpu"


def _quiet(fn: Callable[[], T]) -> tuple[T, list[str]]:
    """跑一次 stable-ts：它的 Adjustment 进度条不看 verbose、总往 stderr 打，Triton 回退等提示也不是本镜的事，都吞掉，只留对齐告警。"""
    with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stderr(io.StringIO()):
        warnings.simplefilter("always")
        out = fn()
    return out, [str(c.message) for c in caught if "align" in str(c.message)]


def align_slice(mdl: Any, audio: Any, text: str, a: float, b: float) -> tuple[list[Word], list[str]]:
    """一句按原文强制对齐在 audio 的 a–b 秒上（找回句重对齐）→（词，秒换回整条 take 的；对齐告警）。"""
    lo = max(0, round(a * SR))
    res, notes = _quiet(lambda: mdl.align(audio[lo:round(b * SR)], " ".join(text.split()), language=LANG,
                                          original_split=True, verbose=None))
    return [(w.word, round(float(lo / SR + w.start), 3), round(float(lo / SR + w.end), 3), float(w.probability))
            for seg in res.segments for w in seg.words], notes


def measure(d: Path, take: Path, sha: str, m: pc.Media, lines: list[pc.Line], planned: list[float],
            model: str, engine: Callable[[], Engine]) -> tuple[dict, str]:
    pc.check_fps(take)
    if not m.has_audio:
        raise SystemExit(f"{pc.rel(take)} 没有音轨，对不了台词")
    inframe = [ln for ln in lines if pc.onscreen(ln.kind)]
    audio = audio_16k(take)

    def work(mdl: Any) -> tuple[list[list[Word]], str, list[Heard], list[str]]:
        res, notes = _quiet(lambda: mdl.align(audio, "\n".join(" ".join(ln.text.split()) for ln in inframe), language=LANG,
                                              original_split=True, verbose=None)) if inframe else (None, [])
        asr, more = _quiet(lambda: mdl.transcribe(audio, language=LANG, verbose=None))
        per_line: list[list[Word]] = [[] for _ in inframe]
        if res is not None:
            if len(res.segments) != len(inframe):
                raise SystemExit(f"{d.name}：对齐结果 {len(res.segments)} 段 ≠ 画内台词 {len(inframe)} 句，按句切不回去")
            per_line = [[(w.word, w.start, w.end, w.probability) for w in seg.words] for seg in res.segments]
        heard = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for seg in asr.segments for w in seg.words]
        return per_line, asr.text.strip(), heard, notes + more

    (per_line, text, heard, notes), device = engine().run(d.name, work)
    for n in dict.fromkeys(notes):
        pc.warn(f"{d.name}：stable-ts：{n}")

    def realign(txt: str, a: float, b: float) -> list[Word]:
        (words, extra), _dev = engine().run(d.name, lambda mdl: align_slice(mdl, audio, txt, a, b))
        for n in dict.fromkeys(extra):
            pc.warn(f"{d.name}：stable-ts（找回句 {a:.2f}–{b:.2f}s 重对齐）：{n}")
        return words

    it = iter(per_line)
    recs = relocate([settle(line_record(i, ln, next(it) if pc.onscreen(ln.kind) else None), heard)
                     for i, ln in enumerate(lines, 1)], heard, realign)
    ref = [w for ln in inframe for w in norm_words(ln.text)]
    return {"version": VERSION, "shot": d.name, "take": pc.rel(take), "take_sha256": sha, "model": model,
            "duration": round(m.v_dur, 3), "frames": pc.cfr_frames(take),
            "lines": recs,
            "asr": {"text": text, "wer": round(wer(ref, norm_words(text)), 3),
                    "words": [{"w": w, "s": s, "e": e} for w, s, e in heard]},
            "speech": speech_spans(recs),
            "cuts": {"planned": planned, "detected": pick_cuts(scene_hits(take), planned)}}, device


# ─────────────────────────── 入口 ───────────────────────────

def targets(epd: Path, shots: str | None, take: Path | None) -> list[tuple[Path, Path]]:
    """（镜目录, take）：默认 pc.cut_shots 的镜配各自的 shotNN.mp4；--take 只对 --shots 指的那一镜。"""
    if take is None:
        return [(d, pc.shot_mp4(d)) for d in pc.cut_shots(epd, shots)]
    want = pc.parse_shots(shots) if shots else set()
    hit = [d for d in pc.shot_dirs(epd) if pc.shot_no(d) in want]
    if len(want) != 1 or len(hit) != 1:
        raise SystemExit(f"--take 要配 --shots 指明是哪一镜（只能一镜、且要在 {epd.name} 里）：拿到 --shots {shots}")
    if not take.is_file():
        raise SystemExit(f"找不到 take {take}")
    return [(hit[0], take)]


def swapped(x: dict, lines: list[dict]) -> str:
    """找回句与剧本顺序的出入：抢在剧本里排它前面的哪几句之前说、落到排它后面的哪几句之后说。"""
    timed = [y for y in lines if y["status"] in TIMED and y is not x]
    early = [f"#{y['idx']}" for y in timed if y["idx"] < x["idx"] and y["start"] > x["start"]]
    late = [f"#{y['idx']}" for y in timed if y["idx"] > x["idx"] and y["start"] < x["start"]]
    return "、".join(([f"抢在 {'、'.join(early)} 之前说"] if early else []) + ([f"落到 {'、'.join(late)} 之后说"] if late else []))


def report(rec: dict, device: str, secs: float, why: str | None) -> list[str]:
    """打印一镜；返回要进人听清单的条目。"""
    n = {k: sum(x["status"] == k for x in rec["lines"]) for k in STATUSES}
    cuts = rec["cuts"]
    extra = [t for t in cuts["detected"] if all(abs(t - p) > CUT_WIN + EPS for p in cuts["planned"])]
    lost = [p for p in cuts["planned"] if all(abs(t - p) > CUT_WIN + EPS for t in cuts["detected"])]
    wer_s = rec["asr"]["wer"]
    print(f"{rec['shot']}  sha {pc.take_id(rec['take_sha256'])} · {device} · {secs:.1f}s · WER {wer_s:.3f} · "
          + " / ".join(f"{k} {v}" for k, v in n.items()) + (f"（重算：{why}）" if why else ""))
    print(f"    切点 计划 {cuts['planned']} · 实测 {cuts['detected']}"
          + (f" · 计划外 {extra}" if extra else "") + (f" · 计划了没检出 {lost}" if lost else ""))
    todo = []
    for x in rec["lines"]:
        conf = "  -  " if x["conf"] is None else f"{x['conf']:.2f}"
        cover = " -  " if x["cover"] is None else f"{x['cover']:.2f}"
        span = f"{x['start']:.2f}–{x['end']:.2f}" if x["status"] in TIMED else "   （计划窗）  "
        print(f"    #{x['idx']:<2} {x['status']:<9} {conf} 覆盖 {cover}  {span}（计划 {x['planned'][0]:g}–{x['planned'][1]:g}）"
              f"  {x['speaker']}：{x['text']}")
        if x["status"] in (LOW, MISSING, MOVED):
            order = swapped(x, rec["lines"]) if x["status"] == MOVED else ""
            todo.append(f"{rec['shot']} #{x['idx']} {x['status']} {conf} · 覆盖 {cover}"
                        f" · 计划 {x['planned'][0]:g}–{x['planned'][1]:g}s"
                        + (f" · 实测 {x['start']:.2f}–{x['end']:.2f}s" if x["status"] in (LOW, MOVED) else "")
                        + (f"（{order}）" if order else "") + f" · {x['speaker']}：{x['text']}")
    if wer_s > WER_MAX:
        todo.append(f"{rec['shot']} 整镜 WER {wer_s:.3f} > {WER_MAX} · ASR：{rec['asr']['text']}")
    return todo


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="台词实测层：原生人声对齐台词 + WER + 镜内切点 → post/align/")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--shots", default=None, help="如 1-6,9,10；默认从第一镜起连续有出片的镜")
    ap.add_argument("--take", type=Path, default=None, help="对这条 take（配 --shots 指一镜）；默认各镜 shotNN.mp4")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--force", action="store_true", help="缓存在也重算")
    a = ap.parse_args()
    drama = pc.drama_root(a.drama)
    epd = pc.ep_dir(drama, a.ep)
    jobs = targets(epd, a.shots, a.take)
    (epd / pc.POST_DIR / ALIGN_SUB).mkdir(parents=True, exist_ok=True)
    print(f"{drama.name} {epd.name}：{len(jobs)} 镜 · 模型 {a.model}")
    engine: list[Engine] = []

    def get_engine() -> Engine:
        if not engine:
            engine.append(Engine(a.model))
        return engine[0]

    todo: list[str] = []
    for d, take in jobs:
        t0 = time.monotonic()
        md = pc.shot_md(d)
        lines = pc.dialogue(md)
        m = pc.probe(take)
        try:
            planned = planned_cuts(md.read_text(encoding="utf-8"), m.v_dur)
        except ValueError as e:
            raise SystemExit(f"{md.name}：{e}") from e
        sha = pc.sha256(take)
        out = cache_path(epd, d.name, sha)
        cached = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
        why = "--force" if a.force else stale(cached, a.model, inputs(lines), planned)
        if why is None:
            rec, device = cached, "缓存"
        else:
            rec, device = measure(d, take, sha, m, lines, planned, a.model, get_engine)
            part = out.with_name(out.name + ".part")
            part.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            part.replace(out)
        todo += report(rec, device, time.monotonic() - t0, why)
    print(f"\n人听清单（{len(todo)} 条）：" + ("".join(f"\n  {t}" for t in todo) if todo else "无"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
