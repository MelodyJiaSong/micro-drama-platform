"""Generate locked-voice 台词配音 for AI-video shots via a local IndexTTS-2 (ai_video.md rule 12.4-H2).

Every ```text block under a shot's `## 台词配音 prompt` is one line (角色 / 音色(… · voice_id) / 情绪 / 语速 / 类型 /
台词 / 时间窗 / 时长目标; old shots without 时间窗 play their lines back to back from 0 s). Each line is synthesized with
the voice_id's locked reference sample (情绪 steers the emotion; 语速 is not fed to it), then conditioned: head/tail
silence below SILENCE_DB cut, peak-normalized to PEAK_DB, loudness-normalized to pc.DX_TARGET. It is time-fitted
(pitch-preserving) only if it overruns its 时间窗, and placed at the window start on a shot-length track:

  <shot>_tts_lip.wav   正常台词 (in frame, lips move)  — tts_first: uploaded to Seedance as @音频 to drive the lips,
                                                          then the same file goes into the final mix
  <shot>_tts_post.wav  内心独白 / 画外 / 系统提示音 (no lips) — both modes: voiced only in post (tools/post/finish_ep.py)
(file names: pc.tts_file; which lines move lips: pc.onscreen — the one definition align / subs / finish_ep also read)

Next to each track: <shot>_tts_{lip,post}.json = [{idx, speaker, text, start, end, factor}] — where every line really
sits (shot-local seconds; end = start + conditioned length / factor), for subtitles. The track is read back before it
lands (length = shot ±1 frame; every line sounds within ONSET_MAX after its start and not EARLY_MAX before it) and
the run stops on a mismatch. A track whose lines, voice samples and settings are unchanged is skipped (stamp in
<ep>/post/tts/; --force re-synthesizes).

In audio_mode=native (the drama's seedance.toml) the in-frame lines are Seedance's own voice, so only the post
track is needed: pass --only post. A track with no lines is not written.

MUST be run with the IndexTTS-2 venv python (it imports the `indextts` package):
  index-tts/.venv/Scripts/python.exe tools/indextts_dub.py --repo index-tts --shot .../shot07/shot07.md [--only post]

Voice consistency: one voice_id → one reference sample, the same one the character's Seedance entity is bound to:
casting.md maps the voice_id to its card → `2_世界观人设/characters/{cN}_*/views/views.mp3` (the establishing video's
voice line). Only a voice without that sample (e.g. a 无卡 off-screen voice) falls back to `<voices-dir>/<voice_id>/`;
--voices-dir defaults to `<剧根>/2_世界观人设/voices`.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import re
import subprocess
import sys
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

sys.path.insert(0, str(Path(__file__).resolve().parent / "post"))
import post_common as pc  # noqa: E402
import mux_av  # noqa: E402      # 响度只用 mux_av.measure_loudness 量（finish_ep 整集归一同一个量法）

if TYPE_CHECKING:
    import numpy as np

_VOICE_ID = re.compile(r"([A-Za-z]{2,4}(?:-[A-Za-z0-9]+){1,4}-\d{2})")
_CAST_ROW = re.compile(r"^\|([^|\n]*)\|\s*`([^`\n]+)`\s*\|", re.M)   # casting.md「| 角色 | `voice_id` |」
_CARD_NO = re.compile(r"[（·]\s*([cm]\d+)\s*[·）]")                   # 角色格里的卡号：「（杜克 · c2）」「（c3 · …）」「· m8 ·」
FENCE = "`" * 3
TRACKS = (pc.TTS_LIP, pc.TTS_POST)
TTS_SUB = "tts"          # 戳放 <集>/post/tts/，镜目录只留轨与 sidecar
SILENCE_DB = -45.0       # 原始合成首尾低于它的切掉
PEAK_DB = -3.0           # 量响度前先把峰值归到这里：太轻的合成会被 BS.1770 的 −70 LUFS 绝对门限整段门掉
SOUND_DB = -60.0         # 回读判「有声」：比 SILENCE_DB 低——切首尾在原始电平上，归一压低后句首几毫秒会落到 −45 以下；句外是数字零
SILENCE_MIN = 0.02       # silencedetect 的最短静音（秒）
ONSET_MAX = 0.15         # 回读：每句 schedule 起点之后这么久内要有声
EARLY_MAX = 0.05         # 回读：声音早于起点 / 晚于止点不许超过这么久


@dataclass(frozen=True)
class DubLine:
    idx: int             # 本镜第几句（台词配音块序；每块都有时间窗时与 pc.dialogue / align 的 idx 一致）
    speaker: str
    voice_id: str
    kind: str
    text: str
    emo_text: str        # 只给「情绪」：拼上语速会把 IndexTTS 的情绪识别带偏
    t0: float
    t1: float


@dataclass(frozen=True)
class Clip:
    """一句处理好的合成（切首尾、峰值归一、响度归一）。"""
    wav: Path
    line: DubLine
    dur: float


@dataclass(frozen=True)
class Placed:
    clip: Clip
    start: float
    factor: float

    @property
    def end(self) -> float:
        return self.start + self.clip.dur / self.factor


def _ffmpeg() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def _field(block: str, label: str) -> str:
    m = re.search(rf"^{label}[^:：\n]*[:：]\s*(.+)$", block, re.MULTILINE)
    return m.group(1).strip() if m else ""


def parse_shot(md_path: Path) -> tuple[float, list[DubLine]]:
    text = md_path.read_text(encoding="utf-8")
    dur = re.search(r"^duration_s:\s*([\d.]+)", text, re.MULTILINE) or re.search(r"^时长[:：]\s*(\d+(?:\.\d+)?)", text, re.MULTILINE)
    if not dur:
        raise ValueError(f"{md_path.name}: 既没有 front matter duration_s，也没有「时长:」行")
    i = text.find("## 台词配音")
    if i < 0:
        return float(dur.group(1)), []   # 无台词镜
    sec = text[i:]
    j = sec.find("\n## ", 4)
    secs = float(dur.group(1))
    lines = []
    cursor = 0.0
    for block in re.findall(FENCE + r"text\n(.*?)\n" + FENCE, sec[:j] if j > 0 else sec, re.DOTALL):
        say, win = _field(block, "台词"), pc.WINDOW_RE.search(_field(block, "时间窗"))
        if not say:
            continue
        tgt = pc.NUM_RE.search(_field(block, "时长目标"))
        if win:
            t0, t1 = float(win.group(1)), float(win.group(2))
        else:
            t0, t1 = cursor, min(secs, cursor + (float(tgt.group(0)) if tgt else secs))
            cursor = t1
        vm = _VOICE_ID.search((re.search(r"^音色.*$", block, re.MULTILINE) or re.match("", "")).group(0))
        if not vm:
            raise ValueError(f"{md_path.name}: 「{say[:20]}」的音色行没有 voice_id")
        lines.append(DubLine(len(lines) + 1, _field(block, "角色"), vm.group(1), _field(block, "类型") or pc.LIP_KINDS[0], say,
                             _field(block, "情绪"), t0, t1))
    return secs, lines


def drama_root(md_path: Path) -> Path:
    for q in md_path.resolve().parents:
        if (q / "2_世界观人设").is_dir():
            return q
    raise ValueError(f"{md_path} 不在一部剧的目录里")


def find_ref(voices_dir: Path, voice_id: str, setting: Path) -> Path:
    """声样只认一处：casting.md 把 voice_id 映到人物卡 → 卡上 views/views.mp3（建立视频的统一声样句，即梦 entity 绑的同一段）；
    卡上没有、或是无卡角色，才退回 voices_dir/{voice_id}/。一个 voice_id 映到多张卡即报错。setting＝剧根/2_世界观人设。"""
    rows = [who for who, vid in _CAST_ROW.findall((setting / "casting.md").read_text(encoding="utf-8")) if vid == voice_id]
    cards = sorted({c for who in rows for c in _CARD_NO.findall(who)})
    dirs = [d for c in cards for d in sorted((setting / "characters").glob(f"{c}_*")) if d.is_dir()]
    if len(cards) > 1 or len(dirs) > 1:
        raise ValueError(f"casting.md 里 {voice_id} 映到多张人物卡：{[d.name for d in dirs] or cards}")
    sample = dirs[0] / "views" / "views.mp3" if dirs else None
    if sample is not None and sample.is_file():
        return sample
    why = (f"{sample} 不在" if sample else f"characters/ 下没有 {cards[0]}_* 卡目录" if cards
           else "casting.md 那一行没有卡号" if rows else "casting.md 里没有这个 voice_id")
    d = voices_dir / voice_id
    for ext in ("wav", "mp3", "flac", "m4a"):
        hits = sorted(d.glob(f"*.{ext}"))
        if hits:
            pc.warn(f"{voice_id}：{why}，退回 {hits[0]}")
            return hits[0]
    raise FileNotFoundError(f"{voice_id} 没有声样：{why}；{d} 也没有"
                            "（有卡的角色用建立视频抽的 views.mp3；无卡的放一段 5–10 s 干声 ref.wav，与其 Seedance entity 绑的同一段）")


# ─────────────────────────── 一句：切首尾、归一 ───────────────────────────

def _amp(db: float) -> float:
    return 10 ** (db / 20)


def _write_wav(path: Path, x: np.ndarray) -> None:
    """float（±1.0 满度）→ pc.AR 单声道 16 位 wav。"""
    import numpy as np
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(pc.AR)
        w.writeframes(np.clip(np.round(x * 32767.0), -32768, 32767).astype("<i2").tobytes())


def _lufs(ffmpeg: str, x: np.ndarray, scratch: Path) -> float:
    """x 的积分响度。不到一个 400 ms 门控块的短句量出 -inf：首尾相接铺到 1 s 以上再量（均方功率不变）。"""
    import numpy as np
    for reps in (1, -(-pc.AR // len(x))):
        _write_wav(scratch, np.tile(x, reps))
        lufs = float(mux_av.measure_loudness(ffmpeg, scratch)["input_i"])
        if lufs > float("-inf"):
            return lufs
    raise SystemExit(f"{scratch.name}：量不出响度（整句都在 −70 LUFS 绝对门限以下，合成几乎是静音）——听一下镜目录里这句的"
                     " *.raw.wav，换情绪或重跑本镜 --force")


def condition(ffmpeg: str, raw: Path, out: Path) -> float:
    """一句原始合成 → 切掉首尾低于 SILENCE_DB 的静音 → 峰值归到 PEAK_DB → 响度归到 pc.DX_TARGET，写 out；返回切后秒数。
    先切首尾：空白也算进时长，会把本来放得下的句子压快。"""
    import numpy as np
    r = subprocess.run([ffmpeg, "-v", "error", "-i", str(raw), "-ac", "1", "-ar", str(pc.AR), "-f", "f32le", "-"],
                       capture_output=True)
    if r.returncode:
        raise SystemExit(f"读不了 {raw}：{r.stderr.decode('utf-8', 'replace')[-300:]}")
    x = np.frombuffer(r.stdout, np.float32)
    loud = np.flatnonzero(np.abs(x) >= _amp(SILENCE_DB))
    if not loud.size:
        raise SystemExit(f"{raw.name}：整段低于 {SILENCE_DB:g} dBFS，合成是空的")
    x = x[loud[0]:loud[-1] + 1]
    x = x * (_amp(PEAK_DB) / np.abs(x).max())
    x = x * _amp(pc.DX_TARGET - _lufs(ffmpeg, x, out))
    peak = float(np.abs(x).max())
    if peak > 1.0:
        raise SystemExit(f"{raw.name}：响度归到 {pc.DX_TARGET:g} LUFS 后峰值 {20 * np.log10(peak):+.1f} dBFS，会削波"
                         "（峰均比过大，多半是爆音 / 咔哒声）——听一下这条原始合成，重跑本镜")
    _write_wav(out, x)
    return len(x) / pc.AR


# ─────────────────────────── 一条轨：排、摆、回读 ───────────────────────────

def _atempo_chain(factor: float) -> str:
    """ffmpeg atempo accepts 0.5-2.0; chain for larger factors."""
    steps: list[float] = []
    f = factor
    while f > 2.0:
        steps.append(2.0)
        f /= 2.0
    while f < 0.5:
        steps.append(0.5)
        f /= 0.5
    steps.append(f)
    return ",".join(f"atempo={s:.6f}" for s in steps)


def schedule(clips: list[Clip]) -> list[Placed]:
    """同一时间窗的几句按先后排开、平分余下的空；整组超窗就一起保音高压到窗长。"""
    groups: dict[tuple[float, float], list[Clip]] = {}
    for c in clips:
        groups.setdefault((c.line.t0, c.line.t1), []).append(c)
    out: list[Placed] = []
    for (t0, t1), group in groups.items():
        win, total = t1 - t0, sum(c.dur for c in group)
        k = total / win if total > win + 0.05 else 1.0
        gap = max(0.0, win - total / k) / len(group)
        t = t0
        for c in group:
            out.append(Placed(c, t, k))
            t += c.dur / k + gap
    return out


def place(ffmpeg: str, placed: list[Placed], secs: float, out: Path) -> None:
    """每句摆到一条镜长的轨上（schedule 定起点与压缩倍数），写完回读（readback），不对即停。"""
    cmd: list[str] = [ffmpeg, "-y"]
    parts = []
    for k, p in enumerate(placed):
        cmd += ["-i", str(p.clip.wav)]
        fit = _atempo_chain(p.factor) + "," if p.factor > 1.0 else ""
        # atempo 攒够一窗才出帧，adelay 先吐的静音垫帧就没有 pts，单句轨的 atrim 会丢掉它们、整句提前；按样本数重打 pts
        parts.append(f"[{k}:a]{fit}aresample={pc.AR},aformat=channel_layouts=mono,adelay={round(p.start * 1000)}:all=1,"
                     f"asetpts=N/SR/TB[v{k}]")
    labels = "".join(f"[v{k}]" for k in range(len(parts)))
    mix = f"amix=inputs={len(parts)}:normalize=0:duration=longest," if len(parts) > 1 else ""
    n = round(secs * pc.AR)          # 按样本数补齐：imageio 带的 ffmpeg 7.1 上 amix 后接 apad=whole_dur 偶尔不补（实测 30 次短 5 次）
    parts.append(f"{labels}{mix}apad=whole_len={n},atrim=end_sample={n}[out]")
    r = subprocess.run(cmd + ["-filter_complex", ";".join(parts), "-map", "[out]", "-c:a", "pcm_s16le", "-f", "wav", str(out)],
                       capture_output=True)
    if r.returncode:
        raise SystemExit(f"摆轨失败：{out}\n{r.stderr.decode('utf-8', 'replace')[-800:]}")
    readback(ffmpeg, out, placed, secs)


def sound_spans(ffmpeg: str, wav: Path, dur: float) -> list[tuple[float, float]]:
    """silencedetect（SOUND_DB、最短 SILENCE_MIN 秒）量出的静音取补 → 有声区间（秒）。"""
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostats", "-i", str(wav), "-af",
                        f"silencedetect=noise={SOUND_DB:g}dB:d={SILENCE_MIN:g}", "-f", "null", "-"], capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode:
        raise SystemExit(f"silencedetect 读不了 {wav}：{err[-300:]}")
    edges = [0.0, *(t for q in pc.silences(err, dur) for t in q), dur]
    return [(a, b) for a, b in zip(edges[::2], edges[1::2]) if b > a]


def timing_faults(dur: float, sound: list[tuple[float, float]], placed: list[Placed], secs: float) -> list[str]:
    """回读判据：轨长与镜长差 ≤ 1 帧；每句起点之后 ONSET_MAX 内有声；每句的声音只落在 [起点 − EARLY_MAX, 止点 + EARLY_MAX]
    里——两句之间的空档、最后一句之后都得无声。"""
    bad: list[str] = []
    if abs(dur - secs) > 1 / pc.FPS:
        bad.append(f"轨长 {dur:.3f}s ≠ 镜长 {secs:.3f}s（差过 1 帧）")
    quiet_from = 0.0
    for p in sorted(placed, key=lambda p: p.start):
        ln = p.clip.line
        if not any(a <= p.start + ONSET_MAX and b >= p.start for a, b in sound):
            bad.append(f"第 {ln.idx} 句「{ln.text}」：起点 {p.start:.3f}s 之后 {ONSET_MAX:g}s 内没有声音")
        early = [(max(a, quiet_from), min(b, p.start - EARLY_MAX)) for a, b in sound
                 if max(a, quiet_from) < min(b, p.start - EARLY_MAX)]
        if early:
            bad.append(f"第 {ln.idx} 句「{ln.text}」起点 {p.start:.3f}s 之前 {early[0][0]:.3f}–{early[0][1]:.3f}s 有声"
                       f"（声音只许早 {EARLY_MAX:g}s，上一句的尾巴只许拖 {EARLY_MAX:g}s）")
        quiet_from = max(quiet_from, p.end + EARLY_MAX)
    late = [(max(a, quiet_from), b) for a, b in sound if b > quiet_from]
    if late:
        bad.append(f"最后一句之后 {late[0][0]:.3f}–{late[0][1]:.3f}s 还有声（尾巴只许拖 {EARLY_MAX:g}s）")
    return bad


def readback(ffmpeg: str, track: Path, placed: list[Placed], secs: float) -> None:
    """从写出的轨本身量（wav 头的样本数、silencedetect），按 timing_faults 判，不对即停。"""
    with wave.open(str(track), "rb") as w:
        dur = w.getnframes() / w.getframerate()
    bad = timing_faults(dur, sound_spans(ffmpeg, track, dur), placed, secs)
    if bad:
        raise SystemExit(f"{track.name} 回读不过：\n  " + "\n  ".join(bad)
                         + "\n——重跑本镜 --force；还不过先听镜目录里留下的 *.raw.wav（原始合成）是不是本身就带长静音 / 杂音")


def sidecar(placed: list[Placed]) -> list[dict]:
    """每句实际摆在哪（镜内秒）：end = start + 切后时长 / factor。"""
    return [{"idx": p.clip.line.idx, "speaker": p.clip.line.speaker, "text": p.clip.line.text,
             "start": round(p.start, 3), "end": round(p.end, 3), "factor": round(p.factor, 4)}
            for p in sorted(placed, key=lambda p: p.clip.line.idx)]


def main(argv: list[str] | None = None) -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="IndexTTS-2 台词配音：逐句合成、切首尾、归一，按时间窗摆成 lip / post 两条镜长轨。")
    ap.add_argument("--repo", required=True, help="index-tts repo dir (holds checkpoints/).")
    ap.add_argument("--shot", action="append", required=True, help="shotNN.md path (repeatable).")
    ap.add_argument("--voices-dir", default=None,
                   help="没有人物卡声样的声音（如无卡的画外音）退回这里的 <voice_id>/ref.*（默认 <剧根>/2_世界观人设/voices）。")
    ap.add_argument("--only", choices=TRACKS, default=None, help="native 模式只要 post 轨。")
    ap.add_argument("--emo-alpha", type=float, default=0.8)
    ap.add_argument("--no-emo", action="store_true", help="Pure timbre clone, ignore 情绪 (A/B).")
    ap.add_argument("--force", action="store_true", help="台词、声样、参数都没变也重新合成。")
    args = ap.parse_args(argv)

    ffmpeg = _ffmpeg()
    ckpt = Path(args.repo) / "checkpoints"
    if not ckpt.is_dir():
        raise SystemExit(f"--repo {args.repo} 下没有 checkpoints/：给 IndexTTS-2 的仓库目录（index-tts）")
    model = sorted(f for f in ckpt.iterdir() if f.is_file())     # 权重与配置进戳：换了模型要重合成
    loaded: list[Any] = []

    def tts() -> Any:
        if not loaded:
            from indextts.infer_v2 import IndexTTS2
            loaded.append(IndexTTS2(cfg_path=str(ckpt / "config.yaml"), model_dir=str(ckpt), use_fp16=True))
        return loaded[0]

    for shot_s in args.shot:
        shot = Path(shot_s)
        secs, lines = parse_shot(shot)
        setting = drama_root(shot) / "2_世界观人设"
        voices = Path(args.voices_dir) if args.voices_dir else setting / "voices"
        stamps = shot.resolve().parents[2] / pc.POST_DIR / TTS_SUB      # shots/shotNN/shotNN.md → 集目录
        for track in TRACKS:
            if args.only and track != args.only:
                continue
            chosen = [ln for ln in lines if pc.onscreen(ln.kind) == (track == pc.TTS_LIP)]
            if not chosen:
                continue
            out = pc.tts_file(shot.parent, track)
            side = pc.tts_file(shot.parent, track, ".json")
            refs = {v: find_ref(voices, v, setting) for v in dict.fromkeys(ln.voice_id for ln in chosen)}
            sig = pc.signature([*refs.values(), *model], secs=secs, lines=[dataclasses.astuple(ln) for ln in chosen],
                               emo_alpha=args.emo_alpha, no_emo=args.no_emo,
                               silence_db=SILENCE_DB, peak_db=PEAK_DB, dx_target=pc.DX_TARGET)
            if not args.force and side.is_file() and pc.fresh(out, sig, stamps):
                print(f"[{shot.stem}] {track}: 台词、声样、参数都没变，跳过（--force 重新合成）")
                continue
            clips: list[Clip] = []
            temps: list[Path] = []
            for ln in chosen:
                raw = out.with_name(f"{out.stem}_{ln.idx}.raw.wav")
                fit = out.with_name(f"{out.stem}_{ln.idx}.fit.wav")
                temps += [raw, fit]
                kw = {} if args.no_emo or not ln.emo_text else \
                    {"use_emo_text": True, "emo_text": ln.emo_text, "emo_alpha": args.emo_alpha}
                tts().infer(spk_audio_prompt=str(refs[ln.voice_id]), text=ln.text, output_path=str(raw), verbose=False, **kw)
                clips.append(Clip(fit, ln, condition(ffmpeg, raw, fit)))
            placed = schedule(clips)
            part, side_part = out.with_name(out.name + ".part"), side.with_name(side.name + ".part")
            place(ffmpeg, placed, secs, part)
            side_part.write_text(json.dumps(sidecar(placed), ensure_ascii=False, indent=1), encoding="utf-8")
            part.replace(out)
            side_part.replace(side)
            stamps.mkdir(parents=True, exist_ok=True)
            pc.stamp(out, sig, stamps)
            for f in temps:
                f.unlink(missing_ok=True)
            print(f"[{shot.stem}] {track}: {len(clips)} 句 → {out.name} + {side.name}")
            for pl in sorted(placed, key=lambda x: x.clip.line.idx):
                ln = pl.clip.line
                print(f"    #{ln.idx:<2} {pl.start:6.3f}–{pl.end:6.3f}s ×{pl.factor:.3f}  {ln.speaker}：{ln.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
