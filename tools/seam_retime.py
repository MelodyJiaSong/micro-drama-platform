"""Velocity-ramp ease retiming for 承接 seams — the 剪映/CapCut「光流变速」approach.

A Seedance first/last-frame chained pair decelerates into the shared seam frame
and accelerates back out of it. `seam_concat`'s trim methods BITE that ease off
and (optionally) bridge the hole; this module instead RETIMES it: the ease
window on both sides of the junction is resampled so the apparent motion speed
stays constant — no content deleted, no synthetic morph between two stills, the
freeze collapses because near-duplicate frames contribute ~zero motion and are
skipped by construction.

Algorithm (Hyperlapse-style equal-motion resampling):
  1. extract clip A's last `window_s` and clip B's first `window_s` at native
     fps (full resolution — these become output frames), drop B's first frame
     (the structural duplicate of A's last);
  2. dense-optical-flow magnitude v[i] between consecutive frames (Farneback on
     downscaled grayscale — same measure seam_metrics scores with);
  3. reference speed v* = median speed of the OUTER quarter of each window (the
     un-eased, natural-speed frames at the window boundaries);
  4. cumulative motion C[i] = Σv; resample at equal ΔC = v* steps → output frame
     count n_out ≈ C_total / v*, i.e. every output step carries the same motion;
  5. each sample lands at a fractional source index j+t: snap to the real frame
     when t is near 0/1, otherwise synthesise it with RIFE `-s t` between the
     two REAL neighbouring frames (never across distant frames);
  6. encode the ramp as a normalised segment; audio = the window's own ambient
     (A-tail + B-head crossfaded) atempo-fit to the ramp's shorter duration.

The ramp is REFUSED (returns False → the caller butt-joins, window acting as a
plain trim) when the junction step's motion is far above the natural speed —
those seam frames genuinely don't match and retiming would spread a content
jump across several morph frames.

Loaded lazily by `tools/seam_concat.py` for plan entries carrying
`retime_window`; importable standalone. Needs cv2 + numpy (already project
deps via seam_metrics).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

_ANALYSIS_W = 360          # downscale width for flow measurement (speed)
_EDGE_FRAC = 0.25          # outer fraction of each window = natural-speed reference
_SPEEDUP_CLAMP = 4.0       # max local time compression (NLE practice: ≤3–4×)
_JUNCTION_GATE = 4.0       # junction step ≤ this × v* else the frames don't match
_FRAC_SNAP = 0.08          # |t| within this of a real frame → use the real frame
_MIN_V = 0.05              # px/frame floor so a static stretch can't zero the curve
_AR = 44100
_XFADE_S = 0.05
_TIME_RE = re.compile(r"time=\s*(\d+):(\d+):(\d+(?:\.\d+)?)")


def _run(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(cmd, capture_output=True, check=False)
    except (FileNotFoundError, OSError) as exc:
        return subprocess.CompletedProcess(cmd, 1, b"", str(exc).encode())


def _norm(w: int, h: int, fps: int) -> str:
    """seam_concat's normalisation tail (duplicated: seam_concat lazy-loads THIS
    module, so importing back would be circular)."""
    return (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={fps}"
    )


def _has_audio(ffmpeg: str, src: Path) -> bool:
    info = _run([ffmpeg, "-i", str(src), "-hide_banner"]).stderr.decode("utf-8", "replace")
    return "Audio:" in info


def _extract_frames(ffmpeg: str, src: Path, start: float, end: float,
                    sd: Path, tag: str) -> list[Path]:
    """Decode [start,end] of `src` to full-resolution PNGs at native cadence."""
    pat = str(sd / f"{tag}_%04d.png")
    _run([ffmpeg, "-ss", f"{max(0.0, start):.3f}", "-to", f"{end:.3f}",
          "-i", str(src), "-vsync", "0", "-q:v", "2", pat])
    return sorted(sd.glob(f"{tag}_*.png"))


def _gray(path: Path) -> np.ndarray | None:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    h, w = img.shape
    if w > _ANALYSIS_W:
        img = cv2.resize(img, (_ANALYSIS_W, int(h * _ANALYSIS_W / w)))
    return img


def _flow_mag(a: np.ndarray, b: np.ndarray) -> float:
    f = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    return float(np.mean(np.sqrt(f[..., 0] ** 2 + f[..., 1] ** 2)))


def _rife_frac(rife: str, model: str | None, a: Path, b: Path, t: float,
               dst: Path) -> bool:
    cmd = [rife, "-0", str(a), "-1", str(b), "-s", f"{t:.4f}", "-o", str(dst)]
    if model:
        cmd += ["-m", model]
    return _run(cmd).returncode == 0 and dst.is_file()


def _atempo_chain(ratio: float) -> str:
    """An atempo filter chain speeding audio by `ratio` (>1 = faster), staying
    within each atempo stage's high-quality 0.5–2.0 band."""
    parts: list[str] = []
    r = max(0.5, min(8.0, ratio))
    while r > 2.0:
        parts.append("atempo=2.0")
        r /= 2.0
    parts.append(f"atempo={r:.4f}")
    return ",".join(parts)


def build_ramp(
    ffmpeg: str, rife: str | None, model: str | None,
    src_a: Path, src_b: Path, dur_a: float, window_s: float,
    fps: int, w: int, h: int, tmp: Path, idx: int, out: Path,
) -> bool:
    """Build the constant-velocity ramp segment replacing [A: dur−window → end]
    + [B: start → window]. Returns False on refusal/failure (caller butt-joins;
    the window then acts as a plain trim on both sides)."""
    sd = tmp / f"retime_{idx:03d}"
    sd.mkdir(parents=True, exist_ok=True)
    window_s = max(0.15, min(1.0, float(window_s)))
    a_frames = _extract_frames(ffmpeg, src_a, dur_a - window_s, dur_a, sd, "a")
    b_frames = _extract_frames(ffmpeg, src_b, 0.0, window_s, sd, "b")
    if len(a_frames) < 2 or len(b_frames) < 2:
        return False
    seq_src = a_frames + b_frames[1:]  # drop B's structural duplicate first frame
    grays = [_gray(p) for p in seq_src]
    if any(g is None for g in grays):
        return False
    v = [_flow_mag(grays[i], grays[i + 1]) for i in range(len(grays) - 1)]
    if not v:
        return False
    # natural-speed reference: the outer quarter of each window (un-eased ends)
    k = max(1, int(round(len(v) * _EDGE_FRAC)))
    v_ref = max(_MIN_V, float(np.median(np.asarray(v[:k] + v[-k:]))))
    # refuse when the junction step is a content jump, not continuous motion
    j_idx = len(a_frames) - 1
    if j_idx < len(v) and v[j_idx] > _JUNCTION_GATE * max(v_ref, 0.5):
        print(f"  seam {idx}->{idx+1}: retime refused — junction motion "
              f"{v[j_idx]:.1f} px/f ≫ natural {v_ref:.1f} (frames don't match)",
              file=sys.stderr)
        return False
    c = np.concatenate([[0.0], np.cumsum(np.maximum(v, 1e-3))])
    total = float(c[-1])
    n_src = len(seq_src)
    n_out = int(round(total / v_ref))
    n_out = max(n_out, int(np.ceil((n_src - 1) / _SPEEDUP_CLAMP)))
    n_out = min(max(2, n_out), n_src - 1)
    # interior sampling (k/(n+1)-style) so the ramp's first/last frames never
    # duplicate the bodies' boundary frames
    targets = np.linspace(0.0, total, n_out + 2)[1:-1]
    idxs = np.interp(targets, c, np.arange(n_src, dtype=float))
    seq = sd / "seq"
    seq.mkdir(exist_ok=True)
    for m, f_idx in enumerate(idxs):
        j = int(np.floor(f_idx))
        t = float(f_idx - j)
        if j >= n_src - 1:
            j, t = n_src - 2, 1.0
        dst = seq / f"{m:03d}.png"
        if t < _FRAC_SNAP:
            dst.write_bytes(seq_src[j].read_bytes())
        elif t > 1.0 - _FRAC_SNAP:
            dst.write_bytes(seq_src[j + 1].read_bytes())
        elif rife and _rife_frac(rife, model, seq_src[j], seq_src[j + 1], t, dst):
            pass
        else:
            # no interpolator (or call failed): nearest real frame — still
            # velocity-flattened, just quantised to source frames
            dst.write_bytes(seq_src[j if t < 0.5 else j + 1].read_bytes())
    ramp_dur = max(0.04, n_out / float(fps))
    return _encode_ramp(ffmpeg, seq, src_a, src_b, dur_a, window_s,
                        ramp_dur, fps, w, h, out)


def _encode_ramp(
    ffmpeg: str, seq: Path, src_a: Path, src_b: Path, dur_a: float,
    window_s: float, ramp_dur: float, fps: int, w: int, h: int, out: Path,
) -> bool:
    """Encode the ramp frames; audio = the retimed window's own ambient
    (A-tail + B-head crossfaded) tempo-fit to the ramp duration."""
    cmd: list[str] = [ffmpeg, "-y", "-framerate", str(fps),
                      "-i", str(seq / "%03d.png")]
    fc: list[str] = [f"[0:v]{_norm(w, h, fps)}[v]"]
    fmt = f"aresample={_AR},aformat=sample_fmts=fltp:channel_layouts=stereo"
    pads: list[str] = []
    ai = 1
    if _has_audio(ffmpeg, src_a):
        cmd += ["-i", str(src_a)]
        fc.append(f"[{ai}:a]atrim=start={max(0.0, dur_a - window_s):.3f},"
                  f"asetpts=N/SR/TB,{fmt}[ap]")
        pads.append("[ap]"); ai += 1
    if _has_audio(ffmpeg, src_b):
        cmd += ["-i", str(src_b)]
        fc.append(f"[{ai}:a]atrim=start=0:end={window_s:.3f},"
                  f"asetpts=N/SR/TB,{fmt}[an]")
        pads.append("[an]"); ai += 1
    if len(pads) == 2:
        ambient = max(0.05, 2.0 * window_s - _XFADE_S)
        tempo = _atempo_chain(ambient / ramp_dur)
        fc.append(f"{pads[0]}{pads[1]}acrossfade=d={_XFADE_S:.3f}:c1=tri:c2=tri,"
                  f"{tempo},apad,atrim=0:{ramp_dur:.3f},asetpts=N/SR/TB[a]")
    elif len(pads) == 1:
        tempo = _atempo_chain(window_s / ramp_dur)
        fc.append(f"{pads[0]}{tempo},apad,atrim=0:{ramp_dur:.3f},"
                  f"asetpts=N/SR/TB[a]")
    else:
        cmd += ["-f", "lavfi", "-i", f"anullsrc=r={_AR}:cl=stereo"]
        fc.append(f"[{ai}:a]atrim=0:{ramp_dur:.3f}[a]")
    cmd += [
        "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-shortest",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", str(_AR), "-ac", "2",
        "-loglevel", "error", str(out),
    ]
    return _run(cmd).returncode == 0 and out.is_file()
