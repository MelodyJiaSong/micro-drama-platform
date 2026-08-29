from __future__ import annotations

from dataclasses import dataclass

from libs.common.constants import EPISODE_DURATION_PRIOR_S

_CORROBORATION_TOL_S = 2.0


@dataclass(frozen=True)
class EpisodeSpan:
    start_s: float
    end_s: float
    confidence: str  # high | medium | low


def fuse_episode_boundaries(
    total_s: float,
    black_ranges: list[tuple[float, float]],
    prior: tuple[float, float] = EPISODE_DURATION_PRIOR_S,
    fingerprint_cuts: list[float] | None = None,
) -> list[EpisodeSpan]:
    """FR-1.3 signal fusion. Implements 2 of the 3 spec signals (blackdetect +
    duration prior); the Chromaprint intro-fingerprint signal is a seam — pass
    `fingerprint_cuts` when a backend lands. Confidence tiers: a cut corroborated
    by fingerprint = high; blackdetect-only = medium (无片头降级, U-14); the
    even-split fallback = low. Human boundary review (FR-1.4) is the backstop."""
    lo, hi = prior
    if total_s <= hi:
        return [EpisodeSpan(0.0, total_s, "high")]

    fingerprints = sorted(fingerprint_cuts or [])
    def _tier(cut: float) -> str:
        return "high" if any(abs(cut - f) <= _CORROBORATION_TOL_S for f in fingerprints) else "medium"

    candidates = sorted((a + b) / 2 for a, b in black_ranges if 0.0 < (a + b) / 2 < total_s)
    spans: list[EpisodeSpan] = []
    cursor = 0.0
    for cut in candidates:
        seg = cut - cursor
        if lo <= seg <= hi:
            spans.append(EpisodeSpan(cursor, cut, _tier(cut)))
            cursor = cut

    remainder = total_s - cursor
    if remainder <= hi:
        if remainder < lo and spans:
            last = spans.pop()
            merged = EpisodeSpan(last.start_s, total_s,
                                 "low" if total_s - last.start_s > hi else last.confidence)
            spans.append(merged)
        else:
            spans.append(EpisodeSpan(cursor, total_s, "low" if remainder < lo else _tier(total_s)))
        return spans

    mean = (lo + hi) / 2
    n = max(2, round(remainder / mean))
    step = remainder / n
    for i in range(n):
        spans.append(EpisodeSpan(cursor + i * step, cursor + (i + 1) * step, "low"))
    return spans
