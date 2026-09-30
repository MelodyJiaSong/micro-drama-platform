# -*- coding: utf-8 -*-
"""P2 试验：2026-09-29 前出的 take 带 Seedance 原生配乐——拆成对白 / 音乐 / 音效，出等响试听、AB 对照片与指标，
供用户听过后在 A（本地分离：原声减掉音乐估计，留原生对白、吼叫与音效）与 B（ElevenLabs Voice Isolator 只留人声 + 新铺环境声床）之间拍板。

    .venv-post/Scripts/python.exe tools/post/stems_trial.py <剧> <ep> --shots 3,5,6 [--force]

每镜落在 {ep}/post/stems_test/{shot}/（整个 post/ 不进 git、可删可重算）：
  {shot}_src.wav            源片音轨：AAC 原样解码成源采样率（Seedance 出 44.1 kHz）立体声 float32，不重采样
  {run}/                    四次分离（separate）：两个模型各跑原片，再各跑对方的一条输出（级联，目录名写明谁跑在谁的哪条轨上）
  preview/{shot}_*.wav      试听：各自线性增益到 PREVIEW_I 积分响度（float32、不压不限）；9_ 开头的按原声同一增益（原始电平）
  preview/{shot}_AB.mp4     同一画面依次配 AB_ORDER 的几条，左上角写着是哪条
  _stamps/                  续跑戳：输入与参数没变就跳过
{ep}/post/stems_test/metrics.json：每镜的耗时、各轨积分响度、能量指标（stem_metrics）、独立分类器的听感指标（stem_tags）、
ASR 词错率（align.py 同一模型同一口径）、试听清单；每跑完一镜就写一次。

去音乐一律写成「原声 − 音乐估计」（RECIPES 只换音乐估计）：分离模型没接住的残差（Bandit 三轨相加差原声 −26…−42 dB）留在成品里。
*(judgment call — 去掉上一版的「RoFormer 对白＋Bandit 音效」混合：两个模型都认领的内容（shot03 的脚步）会被加两遍，
  间隙电平反比原声高 0.1–0.5 dB；它想要的「RoFormer 的人声＋去掉音乐的其余部分」由 roformer_then_bandit 按原声减法做对了。)*
*(judgment call — 2 轨模型单独做不出「去音乐」：它只分 vocals / instrumental，音乐和音效同在 instrumental；
  所以去音乐只出 3 轨模型与两种级联，2 轨模型单独只出「只留人声」。)*
*(judgment call — 台词区间＝对齐缓存的 speech（实测对白）并上 asr.words（自由转写的词）：剧本外的话、被 Seedance 挪了位置的句子也算人声。)*
*(judgment call — 逐秒择优拿 stem_tags 当裁判来挑（代价＝剩下的音乐＋扔掉的非音乐），它自己的 music / removed_nonmusic 因此偏乐观；
  独立检验靠 ASR 与耳朵，metrics 里写明。只在 roformer_then_bandit 与 bandit_then_roformer 两条之间挑：只用 Bandit 在 shot06 把前 21 s 几乎清空，不进候选。)*
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import io
import json
import os
import shutil
import subprocess
import tempfile
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr
from scipy.ndimage import uniform_filter1d

import post_common as pc
import align               # ASR：同一模型、同一 WER 口径
import edl                 # 对齐缓存的位置与读法
import loudness            # 积分响度（loudnorm 第一遍）
import subs                # 字体
import sep_models as sm
import stem_metrics as smx
import stem_tags as st

TEST_SUB = "stems_test"
STAMPS = "_stamps"
PREVIEW_I = -23.0          # 任务单：试听一律对齐到 −23 LUFS 积分响度（EBU R128 广播参考电平），线性增益
AB_SHORT = 540
AB_CRF = "23"
GATE_DELTA = 0.10          # 逐秒择优：保人声那条的代价（cost：剩下的 Music 分＋扔掉的非音乐分）比去净那条高出这么多，这一秒改用去净那条
GATE_FADE_S = 0.25         # 换条处线性交叉淡化
LINE_PAD_S = 0.5           # 逐句转写：对齐窗前后各让这么多，句首句尾的字不被切掉

ROF, BAN = sm.ROFORMER, sm.BANDIT
BAN_ROF = f"{BAN}.music__{ROF}"            # RoFormer 跑在 Bandit 的音乐轨上：把被 Bandit 当音乐的吼叫、尖叫捞回人声
ROF_BAN = f"{ROF}.instrumental__{BAN}"     # Bandit 跑在 RoFormer 的伴奏轨上：人声先由 RoFormer 保住，只在其余部分里分音乐与音效


@dataclass(frozen=True)
class Recipe:
    key: str
    label: str                          # AB 片上的字：不许有半角 : , ; [ ] ' % \（drawtext 会当语法）
    music: tuple[str, str] | None       # (分离, 轨)＝音乐估计；None＝逐秒择优（GATE_PAIR）
    note: str


RECIPES = (
    Recipe("gated", "去音乐 · 逐秒择优", None,
           "默认减 roformer_then_bandit 的音乐估计；某个 2 s 窗里它的代价（候选剩下的 Music 分＋被扔掉那条的非音乐分，stem_tags）"
           "比 bandit_then_roformer 高出 GATE_DELTA，窗覆盖的秒改减后者，换处交叉淡化 GATE_FADE_S"),
    Recipe("roformer_then_bandit", "去音乐 · 先 RoFormer 后 Bandit", (ROF_BAN, "music"),
           "原声减「Bandit 在 RoFormer 伴奏轨里分出的音乐」：人声（含吼叫、尖叫、怪物叫）先由 RoFormer 保住"),
    Recipe("bandit_then_roformer", "去音乐 · 先 Bandit 后 RoFormer", (BAN_ROF, "instrumental"),
           "原声减「RoFormer 在 Bandit 音乐轨里分出的伴奏」：Bandit 误分进音乐的人声由 RoFormer 捞回一部分"),
    Recipe("bandit", "去音乐 · 只用 Bandit v2", (BAN, "music"),
           "原声减 Bandit 的音乐轨（≈ 对白＋音效）：上一版的做法，对照用"),
)
GATE_PAIR = ("roformer_then_bandit", "bandit_then_roformer")     # (默认：保人声，换用：去得净)
DIALOGUE = (
    (ROF, (ROF, "vocals"), "只留人声 · BS-RoFormer"),
    (BAN, (BAN, "speech"), "只留对白 · Bandit v2"),
)
NOT_POSSIBLE = {
    f"2_music_removed__{ROF}": "做不到：2 轨模型只分 vocals / instrumental，音乐与音效同在 instrumental，单独用它去音乐＝连音效一起去（就是 1_dialogue）",
}
ASR_NOTE = ("wer：align.py 同一模型（whisper medium.en，stable-ts）整镜自由转写候选，与画内台词比 WER（align.norm_words / align.wer），"
            "original 与对齐缓存里的 asr.wer 同一口径；整镜解码不稳（短的怪物台词会整句漏掉、两次跑可差一句），只当粗看。"
            "lines：每句画内台词按对齐窗 ± LINE_PAD_S 单独转写（温度 0，可复现），cover＝align.coverage 听到几成；"
            "lines_lost＝原声听得出（≥ align.COVER_MIN）、这条候选听不出的句子——去音乐把台词伤了就看这一栏")


@dataclass(frozen=True)
class Preview:
    name: str                            # 文件名 {shot}_{name}.wav
    label: str
    signal: str                          # 信号表里的键
    true_level: bool = False             # True＝用原声那条的增益（听被去掉的东西原本多响），False＝自己对齐到 PREVIEW_I


ORIGINAL = "3_original"
PREVIEWS = (      # 原声必须排第一：true_level 的几条要用它的增益
    (Preview(ORIGINAL, "原声（参考）", "original"),)
    + tuple(Preview(f"2_music_removed__{r.key}", r.label, f"cand:{r.key}") for r in RECIPES)
    + tuple(Preview(f"1_dialogue__{name}", label, f"dia:{name}") for name, _, label in DIALOGUE)
    + tuple(Preview(f"9_removed__{r.key}", f"被去掉的 · {r.label.split(' · ')[1]}（原始电平）", f"removed:{r.key}", True)
            for r in RECIPES)
)
AB_ORDER = (ORIGINAL, "2_music_removed__gated", "9_removed__gated", f"1_dialogue__{ROF}",       # 前四条就够拍板 A / B
            "2_music_removed__roformer_then_bandit", "2_music_removed__bandit_then_roformer", "2_music_removed__bandit")
# *(judgment call — AB 片把拍板要听的四条排前面：原声 → A 的最好一版 → A 扔掉了什么 → 只留人声（B 路线的起点，要在它下面重铺环境声）；
#   其余配方排后面对照，听不听都行。)*

_bad = [n for n in AB_ORDER if n not in {p.name for p in PREVIEWS}] + [k for k in GATE_PAIR if k not in {r.key for r in RECIPES}]
if _bad:
    raise SystemExit(f"stems_trial：AB_ORDER / GATE_PAIR 里有 PREVIEWS / RECIPES 没定义的名字 {_bad}")


@dataclass(frozen=True)
class Signal:
    x: np.ndarray                        # (n, ch) float32
    inputs: tuple[Path, ...]             # 算它用到的文件（续跑戳）
    params: dict                         # 算法参数（续跑戳）


def lufs(p: Path) -> tuple[float | None, float | None]:
    """积分响度 LUFS、真峰值 dBTP；整条静音 → (None, None)。"""
    try:
        s = loudness.measure(p)
    except SystemExit as e:
        if "静音" in str(e):
            return None, None
        raise
    return round(float(s["input_i"]), 2), round(float(s["input_tp"]), 2)


def read(p: Path) -> np.ndarray:
    return sf.read(p, dtype="float32", always_2d=True)[0]


def gpu_context() -> dict:
    """开跑时 GPU 上还有谁：本机常有别的会话占着显卡，耗时要带着这个读。"""
    try:
        apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name", "--format=csv,noheader"],
                              capture_output=True, text=True, check=True).stdout
        gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        return {"gpu": None, "why": f"nvidia-smi 读不了：{e}"}
    me = str(os.getpid())
    others = sorted({Path(name.strip()).name for pid, _, name in (ln.partition(",") for ln in apps.splitlines() if ln.strip())
                     if pid.strip() != me})
    name, util, used, total = [s.strip() for s in gpu.splitlines()[0].split(",")]
    return {"gpu": name, "util_pct_at_start": int(util), "mem_used_mib_at_start": int(used), "mem_total_mib": int(total),
            "other_gpu_processes_at_start": others}


def extract(take: Path, sd: Path) -> Path:
    out = sd / f"{sd.name}_src.wav"
    sig = pc.signature([take], codec="pcm_f32le", ac=2)
    if pc.fresh(out, sig, where=sd / STAMPS):
        return out
    (sd / STAMPS).mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.stem + ".part.wav")
    pc.run([pc.FFMPEG, "-y", "-v", "error", "-i", take, "-map", "0:a:0", "-vn", "-ac", "2", "-c:a", "pcm_f32le", part])
    part.replace(out)
    pc.stamp(out, sig, where=sd / STAMPS)
    return out


def separate(src: Path, sd: Path) -> dict[str, sm.Run]:
    rof = sm.roformer(src, sd / ROF)
    ban = sm.bandit(src, sd / BAN)
    return {ROF: rof, BAN: ban,
            BAN_ROF: sm.roformer(ban.stems["music"], sd / BAN_ROF),
            ROF_BAN: sm.bandit(rof.stems["instrumental"], sd / ROF_BAN)}


def align_cache(epd: Path, shot: str, tid: str) -> tuple[smx.Spans, list[str], list[dict]]:
    """（台词区间, 画内台词归一后的词＝WER 参考, 画内台词各句的缓存记录）。"""
    p = edl.align_path(epd, shot, tid)
    if not p.is_file():
        raise SystemExit(f"缺对齐缓存 {pc.rel(p)}：先跑 .venv-post/Scripts/python.exe tools/post/align.py <剧> <ep> --shots {shot}")
    al = edl.read_align(p, shot, tid)
    raw = json.loads(p.read_text(encoding="utf-8"))       # edl.Align 不带 ASR 词和句子类型，这两样直接读
    spans = smx.merge(list(al.speech) + [(float(w["s"]), float(w["e"])) for w in raw["asr"]["words"]])
    inframe = [x for x in raw["lines"] if pc.onscreen(x["kind"])]
    ref = [w for x in inframe for w in align.norm_words(x["text"])]
    return spans, ref, inframe


def cost(cand: st.Tags, removed: st.Tags) -> np.ndarray:
    """逐窗代价＝候选里还听得出的音乐（Music 分）＋被当音乐扔掉的非音乐内容（stem_tags.nonmusic）。"""
    return cand.groups["music"] + st.nonmusic(removed)


def gate(n: int, sr: int, keep: np.ndarray, clean: np.ndarray, t: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """keep / clean：两条配方的逐窗代价（cost）。某窗 keep 比 clean 贵出 GATE_DELTA → 窗覆盖的秒改用 clean 的音乐估计。
    返回逐样本权重（1＝clean）与改用的秒。"""
    use = np.zeros(int(np.ceil(n / sr)), bool)
    for t0, d in zip(t, keep - clean):
        if d > GATE_DELTA:
            use[int(t0):int(t0 + st.WIN_S)] = True
    w = np.repeat(use.astype(np.float32), sr)[:n]
    w = uniform_filter1d(w, size=max(1, int(GATE_FADE_S * sr)), mode="nearest")
    return w, [int(i) for i in np.flatnonzero(use)]


def transcribe(engine: align.Engine, shot: str, x: np.ndarray, sr: int, greedy: bool = False) -> str:
    """greedy＝温度 0、不回退：同一输入每次同一结果（逐句覆盖率要可复现）；否则与 align.py 同一解码（整镜 WER 与缓存同口径）。"""
    y = soxr.resample(np.ascontiguousarray(x.mean(axis=1)), sr, align.SR).astype(np.float32)
    kw = {"temperature": 0.0} if greedy else {}

    def work(mdl: object) -> str:
        with warnings.catch_warnings(), contextlib.redirect_stderr(io.StringIO()):     # stable-ts 的进度条总往 stderr 打
            warnings.simplefilter("ignore")
            return mdl.transcribe(y, language=align.LANG, verbose=None, **kw).text.strip()   # type: ignore[attr-defined]

    return engine.run(shot, work)[0]


def line_cover(engine: align.Engine, shot: str, x: np.ndarray, sr: int, lines: list[dict]) -> list[dict]:
    """每句画内台词单独转写（对齐窗 ± LINE_PAD_S，温度 0），按 align.coverage 算听到几成：整镜转写会因 30 s 窗的解码
    把短的怪物台词整句漏掉（shot06「Me run!」在原声整镜 ASR 里就没有，单切出来听得清）。"""
    out = []
    for ln in lines:
        a, b = max(0.0, float(ln["start"]) - LINE_PAD_S), float(ln["end"]) + LINE_PAD_S
        text = transcribe(engine, shot, x[int(a * sr):int(b * sr)], sr, greedy=True)
        out.append({"idx": ln["idx"], "status": ln["status"], "window": [round(a, 2), round(b, 2)],
                    "cover": align.coverage(ln["text"], a, b, [(text, a, b)]), "heard": text})
    return out


def previews(sd: Path, sr: int, sigs: dict[str, Signal]) -> dict[str, dict]:
    pdir, stamps = sd / "preview", sd / STAMPS
    pdir.mkdir(parents=True, exist_ok=True)
    out: dict[str, dict] = {}
    orig_gain: float | None = None
    for pv in PREVIEWS:
        s = sigs[pv.signal]
        dst = pdir / f"{sd.name}_{pv.name}.wav"
        sig = pc.signature(list(s.inputs), signal=pv.signal, params=s.params, target=PREVIEW_I, true_level=pv.true_level,
                           gain=orig_gain if pv.true_level else None)
        stp = pc.fresh(dst, sig, where=stamps)
        if stp is None:
            with tempfile.TemporaryDirectory(dir=sd) as td:
                raw = Path(td) / "raw.wav"
                sf.write(raw, s.x, sr, subtype="FLOAT")
                i_raw, _ = lufs(raw)
            gain = orig_gain if pv.true_level else (None if i_raw is None else round(PREVIEW_I - i_raw, 2))
            if gain is None:
                out[pv.name] = {"file": None, "why": "整条静音，没法对齐响度"}
                continue
            y = s.x * np.float32(10 ** (gain / 20))
            sm.write_wav(dst, y, sr)
            i_out, tp_out = lufs(dst)
            stp = {"i_raw": i_raw, "gain_db": gain, "i_out": i_out, "tp_out": tp_out,
                   "sample_peak_dbfs": round(smx.db(float(np.max(np.abs(y))) ** 2), 2)}
            pc.stamp(dst, sig, where=stamps, **stp)
        if pv.name == ORIGINAL:
            orig_gain = float(stp["gain_db"])
        out[pv.name] = {"file": pc.rel(dst), "label": pv.label,
                        "level": "原始电平（与 3_original 同一增益）" if pv.true_level else f"{PREVIEW_I:g} LUFS",
                        **{k: stp[k] for k in ("i_raw", "gain_db", "i_out", "tp_out", "sample_peak_dbfs")}}
    return out


def ab_video(take: Path, sd: Path, prev: dict[str, dict]) -> Path:
    rows = [(pc.REPO / prev[n]["file"], prev[n]["label"]) for n in AB_ORDER if prev[n].get("file")]
    dst = sd / "preview" / f"{sd.name}_AB.mp4"
    sig = pc.signature([take] + [p for p, _ in rows], labels=[t for _, t in rows], short=AB_SHORT, crf=AB_CRF, font=subs.FONT)
    if pc.fresh(dst, sig, where=sd / STAMPS):
        return dst
    m = pc.probe(take)
    w, h = pc.scale_short(m.w, m.h, AB_SHORT)
    v = f"{m.v_dur:.3f}"
    n = len(rows)
    fc = [f"[0:v]trim=0:{v},setpts=PTS-STARTPTS,fps={pc.FPS},scale={w}:{h}:flags=lanczos,setsar=1,split={n}"
          + "".join(f"[v{i}]" for i in range(n))]
    for i, (_p, label) in enumerate(rows):
        fc.append(f"[v{i}]drawtext=font='{subs.FONT}':text='{i + 1}/{n} {label}':x=16:y=16:fontsize={round(h * 0.05)}:"
                  f"fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10[w{i}]")
        fc.append(f"[{i + 1}:a]atrim=0:{v},asetpts=PTS-STARTPTS,apad=whole_dur={v},aresample={pc.AR}[a{i}]")
    fc.append("".join(f"[w{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    part = dst.with_name(dst.stem + ".part.mp4")
    pc.run([pc.FFMPEG, "-y", "-v", "error", "-i", take, *[x for p, _ in rows for x in ("-i", p)],
            "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", AB_CRF, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", part])
    part.replace(dst)
    pc.stamp(dst, sig, where=sd / STAMPS)
    return dst


def trial(epd: Path, d: Path, root: Path, force: bool, engine: align.Engine) -> dict:
    t_start = time.perf_counter()
    shot, take = d.name, pc.shot_mp4(d)
    sha = pc.sha256(take)
    sd = root / shot
    if force and sd.exists():
        shutil.rmtree(sd)
    src = extract(take, sd)
    print(f"{shot}：分离 …", flush=True)
    runs = separate(src, sd)
    files = {(r, k): p for r, run in runs.items() for k, p in run.stems.items()}
    sr = sf.info(src).samplerate
    o = read(src)
    x = {k: read(p) for k, p in files.items()}
    dur = len(o) / sr
    spans, ref, lines = align_cache(epd, shot, pc.take_id(sha))

    print(f"{shot}：听 …", flush=True)
    t_eval = time.perf_counter()
    tg = st.tagger()
    music = {r.key: x[r.music] for r in RECIPES if r.music}
    t_orig = tg.tags(o, sr)
    t_cand = {k: tg.tags(o - m, sr) for k, m in music.items()}
    t_rem = {k: tg.tags(m, sr) for k, m in music.items()}
    keep, clean = GATE_PAIR
    w, clean_secs = gate(len(o), sr, cost(t_cand[keep], t_rem[keep]), cost(t_cand[clean], t_rem[clean]), t_orig.t)
    music["gated"] = (1.0 - w)[:, None] * music[keep] + w[:, None] * music[clean]
    t_cand["gated"] = tg.tags(o - music["gated"], sr)
    t_rem["gated"] = tg.tags(music["gated"], sr)
    rec_inputs = {r.key: (files[r.music],) for r in RECIPES if r.music}
    rec_inputs["gated"] = rec_inputs[keep] + rec_inputs[clean]
    gate_params = {"pair": list(GATE_PAIR), "delta": GATE_DELTA, "fade_s": GATE_FADE_S, "tagger": st.MODEL_ID,
                   "tagger_rev": st.MODEL_REV, "clean_seconds": clean_secs}
    dia = {name: x[key] for name, key, _ in DIALOGUE}
    t_dia = {name: tg.tags(v, sr) for name, v in dia.items()}
    m_orig = st.music_score(t_orig)
    tags = {
        "original": {"music": m_orig, "nonmusic": round(float(st.nonmusic(t_orig).mean()), 3)},
        "music_removed": {k: {"music": st.music_score(t_cand[k]),
                              "music_left": round(st.music_score(t_cand[k]) / m_orig, 2) if m_orig >= st.MUSIC_MIN else None,
                              "removed_music": st.music_score(t_rem[k]),
                              "removed_nonmusic": round(float(st.nonmusic(t_rem[k]).mean()), 3),
                              "removed_lost": st.lost_events(t_rem[k])} for k in music},
        "dialogue_only": {name: {"music": st.music_score(t), "nonmusic": round(float(st.nonmusic(t).mean()), 3)}
                          for name, t in t_dia.items()},
    }
    asr = {"ref_words": len(ref), "original": {}, "music_removed": {}, "dialogue_only": {}}
    base: dict[int, float | None] = {}
    for group, key, sig_x in ([("original", None, o)] + [("music_removed", k, o - m) for k, m in music.items()]
                              + [("dialogue_only", name, v) for name, v in dia.items()]):
        text = transcribe(engine, shot, sig_x, sr)
        per = line_cover(engine, shot, sig_x, sr, lines)
        if key is None:
            base = {x["idx"]: x["cover"] for x in per}
        lost = [x["idx"] for x in per if (base.get(x["idx"]) or 0.0) >= align.COVER_MIN and (x["cover"] or 0.0) < align.COVER_MIN]
        rec = {"wer": round(align.wer(ref, align.norm_words(text)), 3), "text": text,
               "line_cover_mean": round(float(np.mean([x["cover"] or 0.0 for x in per])), 3) if per else None,
               "lines_lost": lost, "lines": per}
        if key is None:
            asr[group] = rec
        else:
            asr[group][key] = rec
    energy = smx.evaluate(sr, spans, o, music, dia, [x[(BAN, s)] for s in sm.BANDIT_STEMS])
    eval_s = round(time.perf_counter() - t_eval, 1)

    print(f"{shot}：试听 …", flush=True)
    sigs = {"original": Signal(o, (src,), {})}
    for r in RECIPES:
        params = gate_params if r.music is None else {"music": list(r.music)}
        sigs[f"cand:{r.key}"] = Signal(o - music[r.key], (src,) + rec_inputs[r.key], params)
        sigs[f"removed:{r.key}"] = Signal(music[r.key], rec_inputs[r.key], params)
    for name, key, _ in DIALOGUE:
        sigs[f"dia:{name}"] = Signal(dia[name], (files[key],), {"stem": list(key)})
    prev = previews(sd, sr, sigs)
    ab = ab_video(take, sd, prev)
    return {
        "take": pc.rel(take), "take_sha256": sha,
        "take_mtime": datetime.datetime.fromtimestamp(take.stat().st_mtime).isoformat(timespec="seconds"),
        "audio_s": round(dur, 3), "sample_rate": sr, "src_wav": pc.rel(src),
        "runs": {name: {"model": r.model, "input": pc.rel(src) if name in (ROF, BAN) else pc.rel(
                     runs[BAN].stems["music"] if name == BAN_ROF else runs[ROF].stems["instrumental"]),
                        "device": r.device, "load_s": r.load_s, "sep_s": r.sep_s,
                        "x_realtime": round(dur / r.sep_s, 2) if r.sep_s else None, "reused": r.reused,
                        "stems": {k: pc.rel(p) for k, p in r.stems.items()}} for name, r in runs.items()},
        "loudness": {"src.mix": dict(zip(("lufs", "dbtp"), lufs(src)))}
                    | {f"{r}.{k}": dict(zip(("lufs", "dbtp"), lufs(p))) for (r, k), p in files.items()},
        "speech_spans": [[round(a, 2), round(b, 2)] for a, b in spans],
        "no_music": {"flag": m_orig < st.MUSIC_MIN, "music": m_orig, "min": st.MUSIC_MIN,
                     "why": "原声的 music 分低于 MUSIC_MIN＝这条 take 本来就几乎没有配乐：任何配方减掉的都只会是人声与音效，不该分离"},
        "energy": energy,
        "tags": tags,
        "asr": asr,
        "gate": gate_params,
        "previews": prev | {k: {"file": None, "why": v} for k, v in NOT_POSSIBLE.items()},
        "ab_video": pc.rel(ab),
        "eval_s": eval_s,
        "wall_s": round(time.perf_counter() - t_start, 1),
    }


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="P2 试验：拆 Seedance 原生音轨（对白 / 音乐 / 音效），出试听、AB 片与指标")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--shots", required=True)
    ap.add_argument("--force", action="store_true", help="删掉这几镜的试验目录重算")
    a = ap.parse_args()
    epd = pc.ep_dir(pc.drama_root(a.drama), a.ep)
    want = pc.parse_shots(a.shots)
    dirs = [d for d in pc.shot_dirs(epd) if pc.shot_no(d) in want]
    missing = sorted(want - {pc.shot_no(d) for d in dirs if pc.shot_mp4(d).is_file()})
    if missing:
        raise SystemExit(f"这些镜没有出片：{missing}")
    root = epd / pc.POST_DIR / TEST_SUB
    root.mkdir(parents=True, exist_ok=True)
    report = root / "metrics.json"
    doc = json.loads(report.read_text(encoding="utf-8")) if report.is_file() else {}
    doc.setdefault("shots", {})
    doc["gpu"] = gpu_context()
    engine = align.Engine(align.MODEL)
    for d in dirs:
        doc["shots"][d.name] = trial(epd, d, root, a.force, engine)
        doc["shots"] = dict(sorted(doc["shots"].items()))
        doc["models"] = sm.CARDS | {"ast": st.CARD, "asr": {"file": align.MODEL, "licence": "MIT（openai-whisper）",
                                                          "why": "align.py 同一个，WER 与对齐缓存同口径"}}
        doc["recipes"] = {r.key: r.note for r in RECIPES}
        doc["indicators"] = {"energy": smx.INDICATORS, "tags": st.INDICATORS, "asr": ASR_NOTE}
        doc["ab_order"] = list(AB_ORDER)
        doc["preview_i_lufs"] = PREVIEW_I
        doc["updated"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        part = report.with_name(report.stem + ".part.json")
        part.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        part.replace(report)
        print(f"{d.name} → {pc.rel(report)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
