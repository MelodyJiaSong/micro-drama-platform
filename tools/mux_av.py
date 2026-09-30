"""Mux a finished video cut: video stream + 台词 (dialogue) MP3 + one BGM track.

v1 = SINGLE BGM (one video, one dialogue track, one bgm track). Multi-cue
`bgm.md` orchestration is a later concern.

The video stream is copied (`-c:v copy`, no re-encode). The BGM is ducked
UNDER the dialogue via `sidechaincompress` (dialogue is the sidechain key, so
music dips while someone speaks) and mixed with `amix=normalize=0` so the
dialogue is never silently halved. BGM can be looped, volume-scaled, delayed,
and faded.

The video's OWN audio track is REPLACED by default. `--keep-source-audio`
keeps it and mixes the BGM in alongside; add `--duck-source` to make the BGM
dip under it (use that when the source carries speech). Asking to keep an
audio track a silent video doesn't have warns and continues.

`--source-stem no_vocals.wav` is the replace-the-voice case: the source's
voice goes, its ambience and SFX stay — the stem (e.g. demucs no_vocals, see
tools/post/stems.py) is mixed under the dialogue in the source's slot
(`--source-volume` / `--duck-source` apply to it). Exclusive with
`--keep-source-audio`.

`--loudnorm` finishes with two-pass EBU R128 loudness normalisation of the
whole mix (I=-14 LUFS, TP<=-1 dBTP, LRA=11 — the streaming-platform target):
pass 1 measures, pass 2 applies the measured values (linear when the peaks allow,
else loudnorm's dynamic mode); the result is AAC at LOUD_BITRATE. Alone
(no dialogue / bgm / stem) it normalises the video's own audio.

Behavior matrix:
  video + dialogue + bgm  → duck bgm under dialogue, mix, copy video.
  video + bgm (no dialogue) → bgm bed only (no duck), copy video.
  video + dialogue (no bgm) → dialogue audio only, copy video.
  video only (neither)     → error (nothing to mux), unless --loudnorm.
  … + --keep-source-audio  → the source track joins the mix in every row above.
  … + --source-stem        → the stem joins the mix in the source's place.

Usage:
  python tools/mux_av.py --video in.mp4 --dialogue lines.mp3 --bgm bgm_0001.mp3 \
      --out final.mp4 [--bgm-volume 0.6] [--duck-threshold 0.03] [--duck-ratio 8] \
      [--duck-attack 40] [--duck-release 400] [--bgm-start 0] \
      [--fade-in 1.0] [--fade-out 2.0] [--audio-bitrate 192k] [--no-loop] \n      [--keep-source-audio | --source-stem no_vocals.wav] [--source-volume 1.0] \
      [--duck-source] [--loudnorm]

Duration mismatch is always resolved against the VIDEO, which is never cut:
a longer BGM is trimmed to the video length; a shorter one loops to fill it,
or with `--no-loop` plays once and leaves the tail silent.

`--bgm-volume` is a 0-1 linear gain (matches the cue `vol=` unit). ffmpeg is
located via the bundled imageio_ffmpeg when present, else `ffmpeg` on PATH.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LOUD_I: float = -14.0     # integrated loudness target (LUFS)
LOUD_TP: float = -1.0     # true-peak ceiling of the DELIVERED file (dBTP)
LOUD_LRA: float = 11.0    # loudness range target (LU)
# AAC re-encoding lifts true peak above what loudnorm wrote (measured on a
# 3-min episode: +2.3 dB at 192k, +0.2 dB at 256k), so the normalised audio is
# encoded at 256k and loudnorm aims this much under LOUD_TP.
LOUD_CODEC_HEADROOM: float = 0.5
LOUD_BITRATE: str = "256k"
LOUD_TOL_I: float = 0.3   # LU off target before loudnorm_file runs its one corrective pass


def _ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Mux video + dialogue + one BGM into a finished cut.")
    p.add_argument("--video", required=True, help="Source video (stream-copied).")
    p.add_argument("--dialogue", default=None, help="台词 MP3 (optional).")
    p.add_argument("--bgm", default=None, help="One BGM track (optional).")
    p.add_argument("--out", required=True, help="Destination mp4.")
    p.add_argument("--bgm-volume", type=float, default=0.6, help="BGM linear gain 0-1 (cue vol=).")
    p.add_argument("--duck-threshold", type=float, default=0.03)
    p.add_argument("--duck-ratio", type=float, default=8.0)
    p.add_argument("--duck-attack", type=float, default=40.0)
    p.add_argument("--duck-release", type=float, default=400.0)
    p.add_argument("--bgm-start", type=float, default=0.0, help="Seconds before BGM enters.")
    p.add_argument(
        "--keep-source-audio",
        action="store_true",
        help="Keep the video's OWN audio track and mix the BGM under it, instead "
             "of replacing it (the default).",
    )
    p.add_argument(
        "--source-volume", type=float, default=1.0,
        help="Linear gain 0-1 on the kept source audio.",
    )
    p.add_argument(
        "--duck-source",
        action="store_true",
        help="With --keep-source-audio, duck the BGM under the source audio using "
             "the --duck-* params (use when the source carries speech).",
    )
    p.add_argument(
        "--source-stem", default=None,
        help="A voice-free stem of the source (demucs no_vocals) mixed under the "
             "dialogue in place of the replaced source track. Exclusive with "
             "--keep-source-audio.",
    )
    p.add_argument(
        "--loudnorm", action="store_true",
        help="Two-pass EBU R128 normalise the final mix to I=-14 LUFS, TP=-1 dBTP, LRA=11.",
    )
    p.add_argument(
        "--no-loop",
        action="store_true",
        help="Play the BGM once instead of looping it to fill the video; a track "
             "shorter than the video leaves the tail silent.",
    )
    p.add_argument("--fade-in", type=float, default=0.0)
    p.add_argument("--fade-out", type=float, default=0.0)
    p.add_argument("--audio-bitrate", default="192k")
    return p.parse_args(argv)


def _probe_duration(ffmpeg: str, path: Path) -> float | None:
    """Read a media file's duration (seconds) by parsing ffmpeg's stderr."""
    proc = subprocess.run([ffmpeg, "-i", str(path)], capture_output=True)
    err = proc.stderr.decode("utf-8", errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err)
    if not m:
        return None
    h, mm, ss = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mm * 60 + ss


def _build_bgm_chain(dur: float | None, args: argparse.Namespace, bgm_index: int) -> str:
    """Filter chain that prepares the BGM input stream → [bgm]."""
    if args.no_loop:
        # Play once. `apad` to the video length is what keeps the VIDEO intact:
        # without it the output's `-shortest` would cut the picture down to a
        # BGM track shorter than the cut.
        steps = [f"[{bgm_index}:a]anull"]
    else:
        steps = [f"[{bgm_index}:a]aloop=loop=-1:size=2147483647"]
    if args.bgm_start and args.bgm_start > 0:
        steps.append(f"adelay={int(args.bgm_start * 1000)}:all=1")
    if dur is not None:
        if args.no_loop:
            steps.append(f"apad=whole_dur={dur:.3f}")
        steps.append(f"atrim=0:{dur:.3f}")
    steps.append(f"volume={args.bgm_volume}")
    if args.fade_in and args.fade_in > 0:
        steps.append(f"afade=t=in:st={args.bgm_start:.3f}:d={args.fade_in:.3f}")
    if args.fade_out and args.fade_out > 0 and dur is not None:
        steps.append(f"afade=t=out:st={max(dur - args.fade_out, 0):.3f}:d={args.fade_out:.3f}")
    return ",".join(steps) + "[bgm]"


def _run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", errors="replace")[-800:])
    return proc.returncode


def _has_audio_stream(ffmpeg: str, path: Path) -> bool:
    proc = subprocess.run([ffmpeg, "-i", str(path)], capture_output=True)
    err = proc.stderr.decode("utf-8", errors="replace")
    return re.search(r"Stream #\d+:\d+.*: Audio:", err) is not None


def _source_chain(args: argparse.Namespace) -> str:
    """The video's own audio track → [src]."""
    return f"[0:a]volume={args.source_volume}[src]"


def _duck_chain(key: str, args: argparse.Namespace) -> str:
    """Compress [bgm] against `key` (the foreground) → [bgmduck]."""
    return (
        f"[bgm][{key}]sidechaincompress="
        f"threshold={args.duck_threshold}:ratio={args.duck_ratio}:"
        f"attack={args.duck_attack}:release={args.duck_release}[bgmduck]"
    )


def _mix(labels: list[str]) -> str:
    """`normalize=0` so mixing N sources never silently divides each by N."""
    joined = "".join(f"[{l}]" for l in labels)
    return f"{joined}amix=inputs={len(labels)}:normalize=0:duration=longest[aout]"


def _loud_targets(i: float) -> str:
    return f"loudnorm=I={i}:TP={LOUD_TP - LOUD_CODEC_HEADROOM}:LRA={LOUD_LRA}"


def measure_loudness(ffmpeg: str, src: Path, i: float = LOUD_I) -> dict[str, str]:
    """EBU R128 pass 1 on `src`'s first audio track → loudnorm's JSON (input_i, input_tp, …)."""
    af = f"{_loud_targets(i)}:print_format=json"
    proc = subprocess.run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-map", "0:a:0",
                           "-af", af, "-f", "null", "-"], capture_output=True)
    err = proc.stderr.decode("utf-8", errors="replace")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err)
    if proc.returncode != 0 or not m:
        raise RuntimeError(f"loudness measure failed for {src}: {err[-500:]}")
    return json.loads(m.group(0))


def loudnorm_file(ffmpeg: str, src: Path, dst: Path) -> dict[str, str]:
    """Two-pass loudnorm `src` → `dst` (video stream-copied, audio AAC at
    LOUD_BITRATE). When the peaks rule out a linear gain loudnorm runs its
    dynamic mode, which lands under the integrated target (measured -0.9 LU on
    a 3-min episode) — so `dst` is re-measured and, if off by more than
    LOUD_TOL_I, pass 2 is re-run once with the target shifted by that error.
    Returns the measurement of the delivered `dst`."""
    target = LOUD_I
    for _ in range(2):
        m = measure_loudness(ffmpeg, src, target)
        if m["input_i"] == "-inf":
            raise RuntimeError(f"{src}: audio is silent, nothing to normalise")
        af = (
            f"{_loud_targets(target)}:measured_I={m['input_i']}:"
            f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
            f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
        )
        code = _run([
            ffmpeg, "-y", "-i", str(src), "-map", "0:v?", "-map", "0:a:0", "-c:v", "copy",
            "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", LOUD_BITRATE,
            "-loglevel", "error", str(dst),
        ])
        if code != 0:
            raise RuntimeError(f"loudnorm pass 2 failed for {src}")
        got = measure_loudness(ffmpeg, dst)
        if abs(float(got["input_i"]) - LOUD_I) <= LOUD_TOL_I:
            break
        target = round(target + LOUD_I - float(got["input_i"]), 2)
    return got


def _mux(ffmpeg: str, video: Path, out: Path, keep_source: bool, args: argparse.Namespace) -> int:
    """One filter graph for every row of the behaviour matrix. Inputs: 0=video,
    then (stem), (dialogue), (bgm) in that order, each only when given."""
    inputs = ["-i", str(video)]
    parts: list[str] = []

    def add(path: str) -> int:
        inputs.extend(["-i", path])
        return len(inputs) // 2 - 1

    src: str | None = None
    if keep_source:
        parts.append(_source_chain(args))
        src = "src"
    elif args.source_stem:
        parts.append(f"[{add(args.source_stem)}:a]volume={args.source_volume}[src]")
        src = "src"
    dlg = add(args.dialogue) if args.dialogue else None
    labels: list[str] = []
    if args.bgm:
        # The dialogue / source feeds two filters (sidechain key + the mix), so
        # split it first; an input pad can only drive one filter input otherwise.
        parts.append(_build_bgm_chain(_probe_duration(ffmpeg, video), args, bgm_index=add(args.bgm)))
        if dlg is not None and src and args.duck_source:
            # native 音频模式：画内人声在源音轨里、画外 / 独白在 dialogue 里，BGM 要在两者任一出声时都压下去
            parts += [f"[{dlg}:a]asplit=2[dkey][dmix]", "[src]asplit=2[skey][smix]",
                      "[dkey][skey]amix=inputs=2:normalize=0[key]", _duck_chain("key", args)]
            labels, src = ["bgmduck", "dmix", "smix"], None
        elif dlg is not None:
            parts += [f"[{dlg}:a]asplit=2[dkey][dmix]", _duck_chain("dkey", args)]
            labels = ["bgmduck", "dmix"]
        elif src and args.duck_source:
            parts += ["[src]asplit=2[skey][smix]", _duck_chain("skey", args)]
            labels, src = ["bgmduck", "smix"], None
        else:
            labels = ["bgm"]
    elif dlg is not None:
        parts.append(f"[{dlg}:a]anull[d]")
        labels = ["d"]
    if src:
        labels.append(src)
    parts.append(_mix(labels) if len(labels) > 1 else f"[{labels[0]}]anull[aout]")
    return _run([ffmpeg, "-y", *inputs, "-filter_complex", ";".join(parts),
                 "-map", "0:v", "-map", "[aout]",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", args.audio_bitrate,
                 "-shortest", "-loglevel", "error", str(out)])


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    ffmpeg = _ffmpeg_exe()
    video = Path(args.video)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    keep_source = bool(args.keep_source_audio)
    if keep_source and args.source_stem:
        sys.stderr.write("--keep-source-audio and --source-stem are exclusive: the stem "
                         "replaces the source track, it does not join it\n")
        return 2
    if keep_source and not _has_audio_stream(ffmpeg, video):
        # Asking to keep an audio track the video doesn't have is a no-op, not a
        # failure — say so and carry on rather than aborting a long render.
        sys.stderr.write("--keep-source-audio: video has no audio track; ignoring\n")
        keep_source = False

    if not (args.dialogue or args.bgm or args.source_stem):
        if args.loudnorm:
            loudnorm_file(ffmpeg, video, out)
            return 0
        sys.stderr.write("nothing to mux: provide --dialogue, --bgm and/or --source-stem "
                         "(or --loudnorm alone)\n")
        return 2

    target = out.with_name(out.stem + ".premix" + out.suffix) if args.loudnorm else out
    code = _mux(ffmpeg, video, target, keep_source, args)
    if code != 0 or not args.loudnorm:
        return code
    try:
        loudnorm_file(ffmpeg, target, out)
    finally:
        target.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
