"""Pick a concat output canvas from the SOURCE clips instead of hardcoding one.

Both concat paths (episode/成片 concat and the character-views reel) used to
carry their own `_CONCAT_TARGET_W = 720 / _CONCAT_TARGET_H = 1280` pair with the
same "9:16 reel" comment. That hardcode letterboxed every **16:9** drama into a
vertical frame with thick black bars — and `ai_video.md` rule 7 explicitly allows
a per-project aspect override, which half the library uses. Two copies of the
rule meant fixing one would have left the other broken, so the rule lives here.

Same reasoning as matching the output framerate to the source cadence: the
pipeline should follow what was actually rendered, not impose a house format.
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

# WxH on the `Stream ... Video:` line. Anchored on a separator so the SAR/DAR
# ratios later on the same line ("[SAR 1:1 DAR 16:9]") can never match.
_DIMS_RE = re.compile(r"[,\s](\d{2,5})x(\d{2,5})(?=[\s,\]]|$)")

_PROBE_TIMEOUT_S: int = 15
LONG_EDGE: int = 1280
"""Cap on the canvas's long edge — keeps encode cost exactly where the old
720x1280 put it, whichever way the frame is oriented."""

FALLBACK_CANVAS: tuple[int, int] = (720, 1280)
"""Used only when no clip's dimensions can be read (e.g. synthetic test clips).
Keeps the historical 9:16 reel so existing behaviour is unchanged in that case."""


def probe_dims(ffmpeg: str, src: Path) -> tuple[int, int] | None:
    """The clip's pixel dimensions from `ffmpeg -i` stderr, or None."""
    try:
        result = subprocess.run(
            [ffmpeg, "-i", str(src), "-hide_banner"],
            capture_output=True, timeout=_PROBE_TIMEOUT_S, check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    for line in result.stderr.decode("utf-8", errors="replace").splitlines():
        if "Video:" not in line:
            continue
        match = _DIMS_RE.search(line)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None


def fit_canvas(width: int, height: int) -> tuple[int, int]:
    """Scale to `LONG_EDGE` preserving aspect; both dims even (h.264 with
    yuv420p rejects odd dimensions)."""
    long_edge = max(width, height)
    if long_edge > LONG_EDGE:
        k = LONG_EDGE / long_edge
        width, height = round(width * k), round(height * k)
    return max(2, width - width % 2), max(2, height - height % 2)


def target_canvas(ffmpeg: str, inputs: list[Path]) -> tuple[int, int]:
    """The output canvas for concatenating `inputs`: their modal probed size,
    long edge capped.

    Modal (not max) so one stray off-size clip gets padded into the majority
    shape rather than dragging every other clip into a letterboxed frame; ties
    break toward the larger area. Falls back to `FALLBACK_CANVAS` when nothing
    can be probed.
    """
    probed = [d for d in (probe_dims(ffmpeg, src) for src in inputs) if d]
    if not probed:
        return FALLBACK_CANVAS
    counts = Counter(probed)
    top = max(counts.values())
    best = max(
        (dims for dims, count in counts.items() if count == top),
        key=lambda d: d[0] * d[1],
    )
    return fit_canvas(best[0], best[1])
