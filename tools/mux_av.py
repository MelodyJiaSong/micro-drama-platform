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

Behavior matrix:
  video + dialogue + bgm  → duck bgm under dialogue, mix, copy video.
  video + bgm (no dialogue) → bgm bed only (no duck), copy video.
  video + dialogue (no bgm) → dialogue audio only, copy video.
  video only (neither)     → error (nothing to mux).
  … + --keep-source-audio  → the source track joins the mix in every row above.

Usage:
  python tools/mux_av.py --video in.mp4 --dialogue lines.mp3 --bgm bgm_0001.mp3 \
      --out final.mp4 [--bgm-volume 0.6] [--duck-threshold 0.03] [--duck-ratio 8] \
      [--duck-attack 40] [--duck-release 400] [--bgm-start 0] \
      [--fade-in 1.0] [--fade-out 2.0] [--audio-bitrate 192k] [--no-loop] \n      [--keep-source-audio] [--source-volume 1.0] [--duck-source]

Duration mismatch is always resolved against the VIDEO, which is never cut:
a longer BGM is trimmed to the video length; a shorter one loops to fill it,
or with `--no-loop` plays once and leaves the tail silent.

`--bgm-volume` is a 0-1 linear gain (matches the cue `vol=` unit). ffmpeg is
located via the bundled imageio_ffmpeg when present, else `ffmpeg` on PATH.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


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


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    ffmpeg = _ffmpeg_exe()
    video = Path(args.video)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    has_dialogue = bool(args.dialogue)
    has_bgm = bool(args.bgm)
    keep_source = bool(args.keep_source_audio)
    if keep_source and not _has_audio_stream(ffmpeg, video):
        # Asking to keep an audio track the video doesn't have is a no-op, not a
        # failure — say so and carry on rather than aborting a long render.
        sys.stderr.write("--keep-source-audio: video has no audio track; ignoring\n")
        keep_source = False

    if not has_dialogue and not has_bgm:
        sys.stderr.write("nothing to mux: provide --dialogue and/or --bgm\n")
        return 2

    base = [ffmpeg, "-y", "-i", str(video)]
    tail = [
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", args.audio_bitrate,
        "-shortest", "-loglevel", "error", str(out),
    ]

    # video + dialogue only
    if has_dialogue and not has_bgm:
        if not keep_source:
            cmd = base + [
                "-i", args.dialogue,
                "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", args.audio_bitrate,
                "-shortest", "-loglevel", "error", str(out),
            ]
            return _run(cmd)
        graph = f"{_source_chain(args)};[1:a]anull[d];{_mix(['src', 'd'])}"
        return _run(base + ["-i", args.dialogue, "-filter_complex", graph] + tail)

    dur = _probe_duration(ffmpeg, video)

    # video + bgm only. BGM is input index 1.
    if has_bgm and not has_dialogue:
        bgm_chain = _build_bgm_chain(dur, args, bgm_index=1)
        if not keep_source:
            # No foreground to duck against — the bgm IS the whole audio track.
            cmd = base + [
                "-i", args.bgm,
                "-filter_complex", f"{bgm_chain}",
                "-map", "0:v", "-map", "[bgm]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", args.audio_bitrate,
                "-shortest", "-loglevel", "error", str(out),
            ]
            return _run(cmd)
        if args.duck_source:
            # [src] drives two filters (sidechain key + mix), so split it first.
            graph = (
                f"{bgm_chain};{_source_chain(args)};[src]asplit=2[skey][smix];"
                f"{_duck_chain('skey', args)};{_mix(['bgmduck', 'smix'])}"
            )
        else:
            graph = f"{bgm_chain};{_source_chain(args)};{_mix(['bgm', 'src'])}"
        return _run(base + ["-i", args.bgm, "-filter_complex", graph] + tail)

    # video + dialogue + bgm — inputs: 0=video, 1=dialogue, 2=bgm.
    # Duck bgm under dialogue, then mix. The dialogue feeds two filters
    # (sidechain key + the mix), so split it; an input pad can only drive one
    # filter input otherwise.
    bgm_chain = _build_bgm_chain(dur, args, bgm_index=2)
    split = "[1:a]asplit=2[dkey][dmix]"
    duck = _duck_chain("dkey", args)
    parts = [bgm_chain, split, duck]
    labels = ["bgmduck", "dmix"]
    if keep_source:
        parts.append(_source_chain(args))
        labels.append("src")
    parts.append(_mix(labels))
    cmd = base + [
        "-i", args.dialogue,
        "-i", args.bgm,
        "-filter_complex", ";".join(parts),
    ] + tail
    return _run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
