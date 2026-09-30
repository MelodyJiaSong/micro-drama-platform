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
- speech：ok / low_conf 句的对齐词（收过首尾），间隙 < SPEECH_GAP 并成一段。
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
from pathlib import Path
from typing import Any, Callable, TypeVar

import post_common as pc
import prompt_compact    # tools/ 下的，post_common 已把 tools/ 加进 sys.path
import shot_logic

VERSION = 3
ALIGN_SUB = "align"                 # {ep}/post/align/{shot}.{sha12}.json
MODEL = "medium.en"
LANG = "en"
SR = 16000
ALIGN_MIN_CONF = 0.5
# 概率拦不住错位：强制对齐的词概率是「给定这段文字」的解码概率，挤成零时长的词照样 0.9+
# （shot05 模型把「Dad's boots are fine.」挪到前一句之前说，按剧本顺序对齐时它被挤在 40 ms 里：4 词 3 个零时长、概率均值 0.86）
MISSING_FRAC = 0.5
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
OK, LOW, MISSING, OFFSCREEN = "ok", "low_conf", "missing", "offscreen"

Word = tuple[str, float, float, float]      # 对齐词：（文字, 起, 止, 概率）
Heard = tuple[str, float, float]            # ASR 自由转写的词：（文字, 起, 止）
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
    spoken = [w for w in words if WORD_RE.search(w[0])]
    conf = round(sum(w[3] for w in spoken) / len(spoken), 3) if spoken else 0.0
    timed = [w for w in spoken if w[2] > w[1]]
    if len(spoken) - len(timed) > MISSING_FRAC * len(spoken) or not timed:
        return rec | {"start": ln.t0, "end": ln.t1, "conf": conf, "words": [], "status": MISSING}
    return rec | {"start": round(min(w[1] for w in timed), 3), "end": round(max(w[2] for w in timed), 3), "conf": conf,
                  "words": [{"w": w[0].strip(), "s": round(w[1], 3), "e": round(w[2], 3), "p": round(w[3], 3)}
                            for w in spoken],
                  "status": OK if conf >= ALIGN_MIN_CONF else LOW}


def speech_spans(lines: list[dict]) -> list[list[float]]:
    ws = sorted((w["s"], w["e"]) for ln in lines if ln["status"] in (OK, LOW) for w in ln["words"] if w["e"] > w["s"])
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
    if (h := _same_heard(first, heard)) is not None:
        first["s"] = round(max(first["s"], h[1]), 3)
    if (h := _same_heard(last, heard)) is not None:
        last["e"] = round(min(last["e"], h[2]), 3)
    return out


def _same_heard(w: dict, heard: list[Heard]) -> Heard | None:
    """ASR 里与对齐词 w 同词（norm_words 相同）、有时长、且与 w 时间上交叠的词；多个取交叠最长的。"""
    key = norm_words(w["w"])
    if not key:
        return None
    hits = [h for h in heard if h[2] > h[1] and h[1] < w["e"] and h[2] > w["s"] and norm_words(h[0]) == key]
    return max(hits, key=lambda h: min(w["e"], h[2]) - max(w["s"], h[1]), default=None)


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


def measure(d: Path, take: Path, sha: str, m: pc.Media, lines: list[pc.Line], planned: list[float],
            model: str, engine: Callable[[], Engine]) -> tuple[dict, str]:
    pc.check_fps(take)
    if not m.has_audio:
        raise SystemExit(f"{pc.rel(take)} 没有音轨，对不了台词")
    inframe = [ln for ln in lines if pc.onscreen(ln.kind)]
    audio = audio_16k(take)

    def work(mdl: Any) -> tuple[list[list[Word]], str, list[Heard], list[str]]:
        # stable-ts 的 Adjustment 进度条不看 verbose、总往 stderr 打；Triton 回退等提示也不是本镜的事，只留对齐告警
        with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stderr(io.StringIO()):
            warnings.simplefilter("always")
            res = (mdl.align(audio, "\n".join(" ".join(ln.text.split()) for ln in inframe), language=LANG,
                             original_split=True, verbose=None) if inframe else None)
            asr = mdl.transcribe(audio, language=LANG, verbose=None)
        per_line: list[list[Word]] = [[] for _ in inframe]
        if res is not None:
            if len(res.segments) != len(inframe):
                raise SystemExit(f"{d.name}：对齐结果 {len(res.segments)} 段 ≠ 画内台词 {len(inframe)} 句，按句切不回去")
            per_line = [[(w.word, w.start, w.end, w.probability) for w in seg.words] for seg in res.segments]
        heard = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for seg in asr.segments for w in seg.words]
        return per_line, asr.text.strip(), heard, [str(c.message) for c in caught if "align" in str(c.message)]

    (per_line, text, heard, notes), device = engine().run(d.name, work)
    for n in dict.fromkeys(notes):
        pc.warn(f"{d.name}：stable-ts：{n}")
    it = iter(per_line)
    recs = [settle(line_record(i, ln, next(it) if pc.onscreen(ln.kind) else None), heard) for i, ln in enumerate(lines, 1)]
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


def report(rec: dict, device: str, secs: float, why: str | None) -> list[str]:
    """打印一镜；返回要进人听清单的条目。"""
    n = {k: sum(x["status"] == k for x in rec["lines"]) for k in (OK, LOW, MISSING, OFFSCREEN)}
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
        span = f"{x['start']:.2f}–{x['end']:.2f}" if x["status"] in (OK, LOW) else "   （计划窗）  "
        print(f"    #{x['idx']:<2} {x['status']:<9} {conf} 覆盖 {cover}  {span}（计划 {x['planned'][0]:g}–{x['planned'][1]:g}）"
              f"  {x['speaker']}：{x['text']}")
        if x["status"] in (LOW, MISSING):
            todo.append(f"{rec['shot']} #{x['idx']} {x['status']} {conf} · 覆盖 {cover}"
                        f" · 计划 {x['planned'][0]:g}–{x['planned'][1]:g}s"
                        + (f" · 实测 {x['start']:.2f}–{x['end']:.2f}s" if x["status"] == LOW else "")
                        + f" · {x['speaker']}：{x['text']}")
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
