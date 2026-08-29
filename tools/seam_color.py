"""Seam color alignment for 承接 splice points (follow-up 156).

Two i2v generations of the same scene drift in color temperature / exposure, so
even a motion-continuous 承接 seam can read as a cut — the second seam signal
the 首尾帧 community identifies, invisible to the motion-only M1–M4 metrics.

This module does two things:

  * MEASURE: `seam_color_delta` — the LAB-space distance between clip A's tail
    window and clip B's head window (mean-channel ΔL/Δa/Δb + euclidean dist,
    0–255 scale). Above `AUTO_THRESHOLD` the step is clearly visible and the
    pipeline auto-suggests correction.
  * CORRECT: `build_color_head` — a RAMPED Reinhard mean-std color transfer on
    clip B's head window only: full strength at B's first kept frame (so the
    junction matches A exactly), cosine-decaying to zero over `_COLOR_RAMP_S`,
    after which B's own grade continues untouched. This fixes the seam step
    WITHOUT regrading the whole clip (a global grade would fight B's own look
    and its next seam). The corrected head is encoded as an independent
    segment; `seam_concat` inserts it right after the seam's bridge and bites
    its span off body B — duration is preserved exactly (no retiming), and any
    RIFE/blend bridge is built against the CORRECTED first frame, so the bridge
    endpoints are color-consistent too.

Downstream matches upstream (B is corrected toward A) — the already-rendered /
already-reviewed predecessor is never touched. 硬切 seams are never corrected
(a color change across an intended cut is normal). Loaded lazily by
`tools/seam_concat.py` for plan entries carrying `color: true`; needs cv2 +
numpy (already project deps via seam_metrics).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

AUTO_THRESHOLD = 5.0     # LAB mean distance above which the step is clearly visible
_COLOR_RAMP_S = 0.6      # correction window on B's head (full → zero strength)
_STATS_S = 0.3           # sampling window for the reference statistics
_AR = 44100


def _run(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(cmd, capture_output=True, check=False)
    except (FileNotFoundError, OSError) as exc:
        return subprocess.CompletedProcess(cmd, 1, b"", str(exc).encode())


def _norm(w: int, h: int, fps: int) -> str:
    """seam_concat's normalisation tail (duplicated — seam_concat lazy-loads
    THIS module, importing back would be circular)."""
    return (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={fps}"
    )


def _has_audio(ffmpeg: str, src: Path) -> bool:
    info = _run([ffmpeg, "-i", str(src), "-hide_banner"]).stderr.decode("utf-8", "replace")
    return "Audio:" in info


def _extract_frames(ffmpeg: str, src: Path, start: float, end: float,
                    sd: Path, tag: str) -> list[Path]:
    pat = str(sd / f"{tag}_%04d.png")
    _run([ffmpeg, "-ss", f"{max(0.0, start):.3f}", "-to", f"{end:.3f}",
          "-i", str(src), "-vsync", "0", "-q:v", "2", pat])
    return sorted(sd.glob(f"{tag}_*.png"))


def _lab_stats(frames: list[Path]) -> tuple[np.ndarray, np.ndarray] | None:
    """Per-channel LAB mean and std pooled over the sampled frames (downscaled
    for speed — statistics are scale-free)."""
    means, stds = [], []
    for p in frames:
        img = cv2.imread(str(p), cv2.IMREAD_COLOR)
        if img is None:
            continue
        h, w = img.shape[:2]
        if w > 360:
            img = cv2.resize(img, (360, int(h * 360 / w)))
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float64)
        means.append(lab.reshape(-1, 3).mean(axis=0))
        stds.append(lab.reshape(-1, 3).std(axis=0))
    if not means:
        return None
    return np.mean(means, axis=0), np.maximum(np.mean(stds, axis=0), 1e-3)


def seam_color_delta(ffmpeg: str, src_a: Path, src_b: Path, dur_a: float,
                     tail_off_a: float, head_off_b: float,
                     tmp: Path) -> dict | None:
    """LAB color step across the seam: A's kept tail window vs B's kept head
    window (offsets = the seam bites, so the compared frames are the ones that
    actually meet in the output). Returns {dist, dL, da, db} or None."""
    sd = tmp / "colordelta"
    sd.mkdir(parents=True, exist_ok=True)
    a_end = max(0.1, dur_a - tail_off_a)
    a_frames = _extract_frames(ffmpeg, src_a, a_end - _STATS_S, a_end, sd, "ca")
    b_frames = _extract_frames(ffmpeg, src_b, head_off_b,
                               head_off_b + _STATS_S, sd, "cb")
    sa, sb = _lab_stats(a_frames), _lab_stats(b_frames)
    if sa is None or sb is None:
        return None
    d = sa[0] - sb[0]
    return {"dist": round(float(np.linalg.norm(d)), 2),
            "dL": round(float(d[0]), 2), "da": round(float(d[1]), 2),
            "db": round(float(d[2]), 2)}


def _transfer(img: np.ndarray, mu_b: np.ndarray, sd_b: np.ndarray,
              mu_a: np.ndarray, sd_a: np.ndarray, s: float) -> np.ndarray:
    """Reinhard mean-std transfer in LAB at strength `s` (1 = fully matched to
    A's statistics, 0 = untouched — short-circuited so the ramp's tail frame is
    byte-identical to the source, no LAB round-trip drift)."""
    if s <= 1e-3:
        return img.copy()
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float64)
    gain = 1.0 + s * (sd_a / sd_b - 1.0)
    out = (lab - mu_b) * gain + mu_b + s * (mu_a - mu_b)
    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def build_color_head(
    ffmpeg: str, src_a: Path, src_b: Path, dur_a: float,
    tail_off_a: float, head_off_b: float,
    fps: int, w: int, h: int, tmp: Path, idx: int, out: Path,
) -> bool:
    """Encode B's head window [head_off_b, head_off_b + _COLOR_RAMP_S] with the
    ramped color transfer toward A. Duration-preserving (audio = B's own slice,
    untouched). Returns False on any failure (caller keeps the uncorrected
    body — never a silent half-graded seam)."""
    sd = tmp / f"color_{idx:03d}"
    sd.mkdir(parents=True, exist_ok=True)
    a_end = max(0.1, dur_a - tail_off_a)
    ref_a = _lab_stats(_extract_frames(ffmpeg, src_a, a_end - _STATS_S, a_end, sd, "ra"))
    ref_b = _lab_stats(_extract_frames(ffmpeg, src_b, head_off_b,
                                       head_off_b + _STATS_S, sd, "rb"))
    if ref_a is None or ref_b is None:
        return False
    frames = _extract_frames(ffmpeg, src_b, head_off_b,
                             head_off_b + _COLOR_RAMP_S, sd, "f")
    if len(frames) < 2:
        return False
    seq = sd / "seq"
    seq.mkdir(exist_ok=True)
    n = len(frames)
    for k, p in enumerate(frames):
        img = cv2.imread(str(p), cv2.IMREAD_COLOR)
        if img is None:
            return False
        s = 0.5 * (1.0 + np.cos(np.pi * k / (n - 1)))  # cosine ease 1 → 0
        cv2.imwrite(str(seq / f"{k:03d}.png"), _transfer(img, ref_b[0], ref_b[1],
                                                         ref_a[0], ref_a[1], s))
    seg_dur = n / float(fps)
    cmd: list[str] = [ffmpeg, "-y", "-framerate", str(fps),
                      "-i", str(seq / "%03d.png")]
    fc = [f"[0:v]{_norm(w, h, fps)}[v]"]
    if _has_audio(ffmpeg, src_b):
        cmd += ["-i", str(src_b)]
        fc.append(f"[1:a]atrim=start={head_off_b:.3f}:end={head_off_b + seg_dur:.3f},"
                  f"asetpts=N/SR/TB,aresample={_AR},"
                  f"aformat=sample_fmts=fltp:channel_layouts=stereo,"
                  f"apad,atrim=0:{seg_dur:.3f}[a]")
    else:
        cmd += ["-f", "lavfi", "-i", f"anullsrc=r={_AR}:cl=stereo"]
        fc.append(f"[1:a]atrim=0:{seg_dur:.3f}[a]")
    cmd += [
        "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-shortest",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", str(_AR), "-ac", "2",
        "-loglevel", "error", str(out),
    ]
    if _run(cmd).returncode != 0 or not out.is_file():
        return False
    return True


def ramp_seconds() -> float:
    """The correction window a color head bites off body B (exported so
    seam_concat's body-bite math and this module can never drift)."""
    return _COLOR_RAMP_S


if __name__ == "__main__":
    print("importable module — driven by tools/seam_concat.py plan entries "
          "(color: true) and tools/seam_tune.py", file=sys.stderr)
