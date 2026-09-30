# -*- coding: utf-8 -*-
"""整集字幕：成片时间线（segments.json）+ shot md「## 台词配音 prompt」→ SRT，可用 ASS 烧录。

    python tools/post/subs.py <剧> <ep> [--lang src|zh|both] [--segments X.segments.json] [--out-stem PATH]
    python tools/post/subs.py <剧> <ep> --burn in.mp4 out.mp4 [--lang src|zh|both] [--font 字体名] [--segments X.segments.json]

时间线：默认读集目录的 `{ep}.segments.json`（拼接时写的）；没有就按各镜 shotNN.mp4 的时长顺排。
- v1（一段＝一整镜）：一句的起点＝镜起点＋时间窗起点，时长＝时长目标（缺就用时间窗）；同一时间窗里的几句按块序依次排开。
- v2（一段＝一个剪辑事件，带 take 与源片入 / 出点，segments.py）：画内句取对齐缓存（post/align/）的实测起止，画外 / 内心独白
  取 TTS 的实际摆位（pc.tts_file 的 post sidecar），按「成片秒＝段起点＋(源秒 − src_in)」映射；起点不在本段保留区间里的句子不出。
  拿不到实测的（没有缓存、没对上 missing、缓存与 md 句子不符、没有 sidecar）退回 v1 的计划窗并警告。
  每条显示到读得完为止（字符数 ÷ CPS 上限，两种语言取长的），不越过下一句与段尾；还是读不完的由 dense / too_dense 报出来
  （finish_ep 出成片前据此报错停下，qc Q7 用同一套 CPS 口径回读）。
每条至少显示 MIN_CUE_S（不越过下一句、时间窗与段尾）。超长台词按标点折成 ≤2 行，两行放不下就按标点拆成先后几条。
输出 `{stem}.srt`（台词原文）/ `{stem}.zh.srt`（中文意思），stem 默认跟时间线走（`ep01.segments.json` → `ep01`）。
烧录按视频宽高选样式：9:16 字幕底边抬到画高 15% 以上、左右各让 10%（避开平台 UI），16:9 用常规下方位置。
"""
from __future__ import annotations

import argparse
import json
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import post_common as pc
import edl            # 对齐缓存的位置与读法只在 edl.py 定义
import segments

MIN_CUE_S = 1.0
CPS_EN = 17.0         # 字幕阅读速度上限（字符 / 秒，不计换行）：不含 CJK 的一条
CPS_ZH = 9.0          # 含 CJK 的一条
MS_PAD_S = 0.001      # SRT 起止各按毫秒取整，显示时长最多少 1 ms：排读完时间时先垫上
PUNCT = "，。！？；：、,.!?;:…—"
SENT = "。！？.!?…"
FONT = "Microsoft YaHei"
SRT_SUFFIXES = {"src": ".srt", "zh": ".zh.srt"}
BURN_VENC = ("-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p")
_warned: set[str] = set()


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    src: str
    zh: str
    where: str = ""          # 哪一镜哪一句（报读不完时用）


@dataclass(frozen=True)
class Style:
    font_size: int
    outline: int
    margin_lr: int
    margin_v: int
    max_units: int          # 一行最多几个半角宽（全角字算 2）


def style_for(w: int, h: int) -> Style:
    portrait = h > w
    fs = round(w * 0.06) if portrait else round(h * 0.05)
    mlr = round(w * 0.10)
    mv = round(h * 0.15) + round(fs * 0.4) if portrait else round(h * 0.06)
    units = min(42, int((w - 2 * mlr) / (0.52 * fs)))
    return Style(fs, max(2, round(fs * 0.08)), mlr, mv, units)


# ─────────────────────────── 阅读速度 ───────────────────────────

def cps_cap(text: str) -> float:
    return CPS_ZH if has_cjk(text) else CPS_EN


def cps(text: str, secs: float) -> float:
    """一条字幕的阅读速度：字符数（不计换行）÷ 显示秒数。"""
    return len(text.replace("\n", "")) / secs


def read_s(*texts: str) -> float:
    """这几种语言的字幕都读得完要显示多久（空的不算）。"""
    return max((len(" ".join(t.split())) / cps_cap(t) + MS_PAD_S for t in texts if t), default=0.0)


# ─────────────────────────── 排时间 ───────────────────────────

def _warn_once(msg: str) -> None:
    """同一进程里 SRT 与烧录各排一遍时间，同一条警告只打一次。"""
    if msg not in _warned:
        _warned.add(msg)
        pc.warn(msg)


def _zh(ln: pc.Line) -> str:
    return ln.zh or (ln.text if has_cjk(ln.text) else "")


def planned(lines: list[pc.Line]) -> list[tuple[int, float, float, float]]:
    """计划窗排时间（镜内秒）：同一时间窗里的几句按块序依次排开、平分余下的空 → 按窗分组的顺序 [(句序, 起点, 时长, 显示上限)]。"""
    groups: dict[tuple[float, float], list[int]] = {}
    for i, ln in enumerate(lines):
        groups.setdefault((ln.t0, ln.t1), []).append(i)
    out = []
    for (t0, t1), idx in groups.items():
        win = t1 - t0
        durs = [lines[i].target or win / len(idx) for i in idx]
        gap = max(0.0, win - sum(durs)) / len(idx)
        starts = [t0 + sum(durs[:k]) + gap * k for k in range(len(idx))]
        for k, i in enumerate(idx):
            out.append((i, starts[k], durs[k], starts[k + 1] if k + 1 < len(idx) else max(t1, starts[k] + durs[k])))
    return out


def _align(epd: Path, part: segments.Part, tag: str) -> edl.Align | None:
    p = edl.align_path(epd, part.shot, part.take)
    if not p.is_file():
        _warn_once(f"{tag} 没有对齐缓存 {p.name}（tools/post/align.py）——画内台词按计划窗")
        return None
    try:
        return edl.read_align(p, part.shot, part.take)
    except SystemExit as e:
        _warn_once(f"{e}——画内台词按计划窗")
        return None


def _sidecar(epd: Path, shot: str) -> list[tuple[str, float, float]] | None:
    p = pc.tts_file(epd / "shots" / shot, pc.TTS_POST, ".json")
    if not p.is_file():
        return None
    try:
        rows = [(" ".join(str(r["text"]).split()), float(r["start"]), float(r["end"]))
                for r in json.loads(p.read_text(encoding="utf-8"))]
    except (ValueError, KeyError, TypeError) as e:
        raise SystemExit(f"{p.name} 不是 [{{idx, speaker, text, start, end, factor}}]：{e}——"
                         f"重跑 tools/indextts_dub.py --force --only {pc.TTS_POST} 重写") from e
    if bad := [t for t, a, b in rows if b <= a]:
        raise SystemExit(f"{p.name}：这几句 end ≤ start——{bad}；重跑 tools/indextts_dub.py --force --only {pc.TTS_POST}")
    return rows


def measured(epd: Path, part: segments.Part, lines: list[pc.Line]) -> list[tuple[float, float] | None]:
    """每句在这一段 take 里的实际起止（源秒）：画内句取对齐缓存 ok / low_conf 的实测，画外 / 内心独白取 TTS sidecar 的实际摆位。
    拿不到的 → None（调用方退回计划窗），每个原因警告一次。"""
    tag = f"{part.shot}（take {part.take}）"
    out: list[tuple[float, float] | None] = [None] * len(lines)
    on = [pc.onscreen(ln.kind) for ln in lines]
    al = _align(epd, part, tag) if any(on) else None
    side = _sidecar(epd, part.shot) if not all(on) else None
    by_idx = {x.idx: x for x in al.lines} if al else {}
    sidecar = pc.tts_file(epd / "shots" / part.shot, pc.TTS_POST, ".json").name
    for i, ln in enumerate(lines):
        what = f"{tag} 第 {i + 1} 句「{ln.text[:24]}」"
        if not on[i]:
            key = " ".join(ln.text.split())
            k = next((j for j, r in enumerate(side) if r[0] == key), None) if side is not None else None
            if k is None:
                why = f"没有 {sidecar}" if side is None else "TTS sidecar 里没有这句（TTS 比 md 旧？）"
                _warn_once(f"{what}（{ln.kind}）{why}——字幕按计划窗")
            else:
                _t, a, b = side.pop(k)
                out[i] = (a, b)
        elif al is not None:
            x = by_idx.get(i + 1)
            if x is None or x.text != ln.text:
                _warn_once(f"{what} 与对齐缓存里的句子对不上（md 改过、还没重跑 align.py）——按计划窗")
            elif x.status in edl.WORDED:
                out[i] = x.span
            else:
                _warn_once(f"{what} 没对上（{x.status}）——按计划窗")
    return out


def kept(part: segments.Part, t: float) -> bool:
    """源片 t 秒在不在这一段的保留区间里（入 / 出点按帧取整，差半帧以内算在）。"""
    return part.src_in - edl.HALF_FRAME <= t < part.src_out - edl.HALF_FRAME


def _cues_v2(epd: Path, part: segments.Part, lines: list[pc.Line]) -> list[Cue]:
    """起点＝实测（或计划窗）映射到成片，夹在段首之后（入点按帧取整可能比句首晚半帧）；显示到读得完，不越过段尾。"""
    real = measured(epd, part, lines)
    out = []
    for i, s, d, cap in planned(lines):
        span = real[i]
        a, b = span or (s, s + d)
        if not kept(part, a):
            al = _align(epd, part, f"{part.shot}（take {part.take}）") if a >= part.src_out - edl.HALF_FRAME else None
            if al is not None and a >= al.end_s - edl.HALF_FRAME:
                _warn_once(f"{part.shot}「{lines[i].text[:20]}」起点 {a:.2f}s 超出 take 的 {al.end_s:.2f}s（md 比出片新？），不出字幕")
            continue
        limit = part.end if span else min(part.at(cap), part.end)
        t0 = max(part.start, part.at(a))
        need = max(b - a, MIN_CUE_S, read_s(lines[i].text, _zh(lines[i])))
        out.append(Cue(t0, min(t0 + need, limit), lines[i].text, _zh(lines[i]), f"{part.shot} 第 {i + 1} 句"))
    return out


def cues_for(epd: Path, segs: Sequence[pc.Seg | segments.Part]) -> list[Cue]:
    out: list[Cue] = []
    for seg in segs:
        lines = pc.dialogue(pc.shot_md(epd / "shots" / seg.shot))
        if isinstance(seg, segments.Part):
            out += _cues_v2(epd, seg, lines)
            continue
        for i, s, d, cap in planned(lines):
            if s >= seg.dur:
                pc.warn(f"{seg.shot}「{lines[i].text[:20]}」起点 {s:.2f}s 超出成片里这一镜的 {seg.dur:.2f}s（md 比出片新？），不出字幕")
                continue
            end = min(s + max(d, MIN_CUE_S), cap, seg.dur)
            out.append(Cue(seg.start + s, seg.start + end, lines[i].text, _zh(lines[i]), f"{seg.shot} 第 {i + 1} 句"))
    out.sort(key=lambda c: c.start)
    for i in range(len(out) - 1):
        if out[i].end > out[i + 1].start:
            c = out[i]
            out[i] = Cue(c.start, max(c.start + 0.2, out[i + 1].start - 0.04), c.src, c.zh, c.where)
    return out


# ─────────────────────────── 折行 ───────────────────────────

def has_cjk(s: str) -> bool:
    return any(unicodedata.east_asian_width(c) in "WF" for c in s)


def width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _two_lines(text: str, max_u: int) -> str:
    """折成 ≤2 行：先找标点后的断点，再找空格，最后（CJK）任意字间；取两行最匀的。"""
    if width(text) <= max_u:
        return text

    def at(i: int) -> str:
        return text[:i].rstrip() + "\n" + text[i:].lstrip()

    def balance(j: int) -> int:
        return abs(width(text[:j]) - width(text[j:]))

    rules = (lambda i: text[i - 1] in PUNCT, lambda i: text[i] == " " or text[i - 1] == " ",
             lambda i: has_cjk(text[i - 1:i + 1]))
    cands = [[i for i in range(1, len(text)) if ok(i) and text[i] not in PUNCT] for ok in rules]   # 不在标点前断行
    for cs in cands:
        fits = [i for i in cs if width(text[:i].rstrip()) <= max_u and width(text[i:].lstrip()) <= max_u]
        if fits:
            return at(min(fits, key=balance))
    loose = cands[1] or cands[2]                       # 哪种都放不下：宁可略超宽，也不在词中间断
    return at(min(loose, key=balance)) if loose else at(len(text) // 2)


def fold(text: str, max_u: int) -> list[str]:
    """→ 若干块，每块 ≤2 行（块与块在时间上先后出现）；先在句末断，句子本身放不下再在分句 / 词间断。"""
    text = " ".join(text.split())
    limit = 2 * max_u
    if width(text) <= limit:
        return [_two_lines(text, max_u)]
    pieces: list[str] = []
    for sent in _split_after(text, SENT):
        pieces += [sent] if width(sent) <= limit else _pack(_split_after(sent, PUNCT + " "), limit)
    return [_two_lines(p.strip(), max_u) for p in _pack(pieces, limit) if p.strip()]


def _split_after(text: str, marks: str) -> list[str]:
    """在标记字符之后切开（半角标点要后跟空格或到结尾才算，免得把「...」「3.5」切碎）。"""
    toks, cur = [], ""
    for i, c in enumerate(text):
        cur += c
        nxt = text[i + 1] if i + 1 < len(text) else " "
        if c == " " and c in marks or c in marks and (nxt == " " or has_cjk(c)):
            toks.append(cur)
            cur = ""
    return toks + ([cur] if cur else [])


def _pack(tokens: list[str], limit: int) -> list[str]:
    out, cur = [], ""
    for tok in tokens:
        while width(tok) > limit:                       # 连一个分句都放不下（无标点长串）：硬切
            k = next(j for j in range(len(tok), 0, -1) if width(tok[:j]) <= limit)
            while k < len(tok) and tok[k] in PUNCT:     # 标点不落到下一块行首
                k += 1
            tok, head = tok[k:], tok[:k]
            out += [cur, head] if cur else [head]
            cur = ""
        if cur and width(cur + tok) > limit:
            out.append(cur)
            cur = ""
        cur += tok
    return out + ([cur] if cur else [])


def split_timed(c: Cue, text: str, max_u: int) -> list[tuple[float, float, str]]:
    chunks = fold(text, max_u)
    total = sum(width(x) for x in chunks) or 1
    out, t = [], c.start
    for x in chunks:
        d = (c.end - c.start) * width(x) / total
        out.append((t, t + d, x))
        t += d
    return out


# ─────────────────────────── 写出 ───────────────────────────

def _nonneg(t: float) -> float:
    if t < 0:
        raise SystemExit(f"字幕时间 {t:.3f}s < 0：排时间出了错（SRT / ASS 写不了负时间）")
    return t


def _ms(t: float) -> int:
    return round(_nonneg(t) * 1000)


def _srt_time(t: float) -> str:
    ms = _ms(t)
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def langs(lang: str) -> list[str]:
    return [lg for lg in SRT_SUFFIXES if lang in (lg, "both")]


def srt_rows(cues: list[Cue], lang: str, max_u: int) -> list[tuple[float, float, str, Cue]]:
    """一种语言的 SRT 条目（一条字幕太长就按 fold 拆成先后几条）。"""
    return [(a, b, t, c) for c in cues if (c.zh if lang == "zh" else c.src)
            for a, b, t in split_timed(c, c.zh if lang == "zh" else c.src, max_u)]


def srt_text(cues: list[Cue], lang: str, max_u: int) -> str:
    return "".join(f"{i}\n{_srt_time(a)} --> {_srt_time(b)}\n{t}\n\n"
                   for i, (a, b, t, _c) in enumerate(srt_rows(cues, lang, max_u), 1))


def dense(cues: list[Cue], lang: str, max_u: int) -> list[str]:
    """读不完的字幕：按 qc Q7 的口径（每条 SRT 的字符数 ÷ 毫秒取整后的显示时长 > CPS 上限）→ 哪一镜哪一句、显示多久、要多久。"""
    out: dict[tuple[str, str], str] = {}
    for lg in langs(lang):
        for a, b, t, c in srt_rows(cues, lg, max_u):
            text = c.zh if lg == "zh" else c.src
            if cps(t, (_ms(b) - _ms(a)) / 1000) > cps_cap(t) and (c.where, lg) not in out:
                out[(c.where, lg)] = (f"{c.where}「{' '.join(text.split())[:40]}」只能显示 {c.end - c.start:.2f}s，读完要 "
                                      f"{read_s(text):.2f}s（CPS 上限 英 {CPS_EN:g} / 中 {CPS_ZH:g}）")
    return list(out.values())


def too_dense(epd: Path, segs: Sequence[pc.Seg | segments.Part], lang: str, w: int, h: int) -> list[str]:
    return dense(cues_for(epd, segs), lang, style_for(w, h).max_units)


def write_srts(epd: Path, segs: Sequence[pc.Seg | segments.Part], stem: Path, lang: str, w: int, h: int) -> list[Path]:
    """写 {stem}.srt / .zh.srt（先写 .part 再换名：存档里的同名文件不会被原地改掉）；读不完的字幕逐条警告。"""
    cues = cues_for(epd, segs)
    max_u = style_for(w, h).max_units
    for msg in dense(cues, lang, max_u):
        _warn_once(f"字幕读不完：{msg}")
    out = []
    for lg in langs(lang):
        p = stem.with_name(stem.name + SRT_SUFFIXES[lg])
        part = p.with_name(p.name + ".part")
        part.write_text(srt_text(cues, lg, max_u), encoding="utf-8")
        part.replace(p)
        out.append(p)
    print(f"字幕 {len(cues)} 条 → " + "、".join(p.name for p in out))
    return out


def _ass_time(t: float) -> str:
    cs = round(_nonneg(t) * 100)
    return "%d:%02d:%02d.%02d" % (cs // 360000, cs // 6000 % 60, cs // 100 % 60, cs % 100)


def _ass_esc(s: str) -> str:
    return s.replace("{", "(").replace("}", ")").replace("\n", r"\N")


def ass_text(cues: list[Cue], lang: str, w: int, h: int, font: str) -> str:
    st = style_for(w, h)
    head = ("[Script Info]\nScriptType: v4.00+\n"
            f"PlayResX: {w}\nPlayResY: {h}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n"
            f"Style: Main,{font},{st.font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,"
            f"{st.outline},1,2,{st.margin_lr},{st.margin_lr},{st.margin_v},1\n\n[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    rows: list[tuple[float, float, str]] = []
    for c in cues:
        if lang == "both":
            parts = [_ass_esc("\n".join(fold(c.zh, st.max_units)))] if c.zh else []
            small = round(st.font_size * 0.8)
            parts += [f"{{\\fs{small}}}" + _ass_esc("\n".join(fold(c.src, round(st.max_units / 0.8))))]
            rows.append((c.start, c.end, r"\N".join(parts)))
        else:
            text = c.zh if lang == "zh" else c.src
            rows += [(a, b, _ass_esc(t)) for a, b, t in split_timed(c, text, st.max_units)] if text else []
    return head + "".join(f"Dialogue: 0,{_ass_time(a)},{_ass_time(b)},Main,,0,0,0,,{t}\n" for a, b, t in rows)


def burn(video: Path, out: Path, epd: Path, segs: Sequence[pc.Seg | segments.Part], lang: str, font: str,
         ass: Path | None = None, extra: Sequence[str] = (), venc: Sequence[str] = BURN_VENC) -> Path:
    """venc：视频编码参数（成片烧录版传 pc.DELIVER）；extra：拼在输出文件名前的附加输出参数（如 aigc.ffmpeg_args 的元数据）。"""
    m = pc.probe(video)
    ass = ass or out.with_suffix(".ass")
    ass.write_text(ass_text(cues_for(epd, segs), lang, m.w, m.h, font), encoding="utf-8")
    part = out.with_name(out.stem + ".part.mp4")
    pc.run([pc.FFMPEG, "-y", "-i", video.resolve(), "-vf", f"ass={ass.name}", "-map", "0:v:0", "-map", "0:a?",
            *venc, "-c:a", "copy", "-movflags", "+faststart", *extra, part.resolve()], cwd=ass.parent)   # 相对文件名：免 Windows 盘符冒号转义
    part.replace(out)
    print(f"烧录 {m.w}x{m.h}（{'9:16' if m.h > m.w else '横屏'}样式）→ {out}")
    return out


def timeline(epd: Path, seg_file: Path | None) -> tuple[list[pc.Seg] | list[segments.Part], Path]:
    """→（时间线，默认输出 stem）。v2 的 segments 给各段（带源片入 / 出点），v1 给整镜。"""
    seg_path = seg_file or epd / f"{epd.name}.segments.json"
    if seg_path.is_file():
        return (segments.read_parts(seg_path) or pc.read_segments(seg_path),
                seg_path.with_name(seg_path.name.removesuffix(".segments.json")))
    if seg_file:
        raise SystemExit(f"找不到 {seg_file}")
    pc.warn(f"没有 {seg_path.name}，按各镜 shotNN.mp4 的时长顺排")
    return pc.segments_from_mp4s(pc.cut_shots(epd, None)), epd / epd.name


def canvas(epd: Path, segs: Sequence[pc.Seg | segments.Part]) -> tuple[int, int]:
    mp4 = pc.shot_mp4(epd / "shots" / segs[0].shot)
    if mp4.is_file():
        m = pc.probe(mp4)
        return m.w, m.h
    return (720, 1280) if "比例: 9:16" in pc.shot_md(mp4.parent).read_text(encoding="utf-8") else (1280, 720)


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="整集字幕：SRT + ASS 烧录")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--lang", choices=("src", "zh", "both"), default="both")
    ap.add_argument("--segments", type=Path, default=None)
    ap.add_argument("--out-stem", type=Path, default=None, help="SRT 路径去掉 .srt（默认跟时间线同名）")
    ap.add_argument("--burn", nargs=2, type=Path, metavar=("IN", "OUT"))
    ap.add_argument("--font", default=FONT)
    a = ap.parse_args()
    epd = pc.ep_dir(pc.drama_root(a.drama), a.ep)
    segs, stem = timeline(epd, a.segments)
    if a.burn:
        burn(a.burn[0], a.burn[1], epd, segs, a.lang, a.font)
    else:
        write_srts(epd, segs, a.out_stem or stem, a.lang, *canvas(epd, segs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
