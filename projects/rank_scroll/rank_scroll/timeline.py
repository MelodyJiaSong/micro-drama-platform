"""Deterministic timeline: band layout (band px) and camera position per frame.

Band coordinates are 1080p pixels. The band holds elements (cards and insight cards) in
countdown order N..1 left→right (list mode: file order 1..N, no enlarged top 10, the final hold
centres the last card without champion styling); the camera's centre moves right, so cards slide left.
Constant segment moves exactly SPEED px per frame (integer) so text never shimmers.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .contract import Episode

FPS = 60
W, H = 1920, 1080
CARD_H = 800          # card height (1080p px); width comes from episode.card_w
GAP = 40              # gap between normal cards
GAP_TOP = 52          # gap around top-10 cards
TOP_SCALE = 1.06      # top-10 card scale (848 px tall: still clears header and progress bar)
TOP_N_BIG = 10
LEFT_MARGIN = 40      # first card's left edge at scroll start
SPEED = 3             # px per frame at 1080p60 in the constant segment (paihangbang 2026-11-07: 1.5x faster, rank_scroll follow-up 018)
EASE_DIST = 240       # px covered by the final ease-out (velocity-matched: 2*d/v frames)

INTRO = 5.0           # title card; band slides in during the last SLIDE_IN seconds
SLIDE_IN = 1.5
CHAMP_HOLD = 6.0
LAST_HOLD = 4.0       # list mode: hold on the last card (segment keeps the name "champion")
TALLY = 7.0
SOURCES = 4.0
ENDSCREEN = 18.0
XFADE = 0.4


@dataclass
class Element:
    kind: str                 # "card" | "insight"
    index: int                # index into episode.items or episode.insights
    rank: int                 # card rank; for insight = after_rank
    center: int               # band x of element centre
    slot: int
    scale: float


def _ceil4(x: float) -> int:
    return int(math.ceil(round(x, 6) / 4) * 4)


INSIGHT_FRAC = 0.72   # insight cards are narrower than photo cards (photos keep the screen)


def insight_w(card_w: int) -> int:
    return int(round(card_w * INSIGHT_FRAC / 8) * 8)


def slots(card_w: int) -> tuple[int, int, int]:
    """(normal, top-10, insight) slot widths; multiples of 4 so every centre and camera target is an even pixel."""
    return _ceil4(card_w + GAP), _ceil4(card_w * TOP_SCALE + GAP_TOP), _ceil4(insight_w(card_w) + GAP)


@dataclass
class Timeline:
    elements: list[Element]
    cam_start: int
    cam_end: int
    f_intro: int
    f_scroll: int             # frames of scroll (constant + ease)
    f_const: int
    f_ease: int
    f_champ: int
    f_tally: int
    f_sources: int
    f_end: int
    segments: list[tuple[str, int, int]] = field(default_factory=list)  # (name, start_frame, end_frame)
    f_hold: int = 0           # frames the band stands still at cam_start before scrolling (layout.intro_hold)
    ease_dist: int = EASE_DIST  # px of the final ease-out = EASE_DIST + remainder so the constant part is a whole number of SPEED steps

    @property
    def total_frames(self) -> int:
        return self.segments[-1][2]

    @property
    def duration(self) -> float:
        return self.total_frames / FPS

    def segment_at(self, f: int) -> tuple[str, int, int]:
        for seg in self.segments:
            if seg[1] <= f < seg[2]:
                return seg
        return self.segments[-1]

    def camera(self, f: int) -> float:
        """Band x at screen centre for frame f (the slide-in offset is handled by `band_offset`)."""
        s = f - self.f_intro - self.f_hold
        if s <= 0:
            return float(self.cam_start)
        if s <= self.f_const:
            return float(self.cam_start + SPEED * s)
        e = s - self.f_const
        if e >= self.f_ease:
            return float(self.cam_end)
        tau = e / self.f_ease
        return self.cam_start + SPEED * self.f_const + self.ease_dist * (1 - (1 - tau) ** 2)

    def band_offset(self, f: int) -> float:
        """Extra screen-x offset for the intro slide-in (cards enter from the right)."""
        t = f / FPS
        start = INTRO - SLIDE_IN
        if t >= INTRO:
            return 0.0
        if t <= start:
            return float(W + 200)
        u = (t - start) / SLIDE_IN
        return (W + 200) * (1 - u) ** 3


def build(ep: Episode) -> Timeline:
    items = ep.items
    after: dict[int, list[int]] = {}
    for j, ins in enumerate(ep.insights):
        after.setdefault(ins.after_rank, []).append(j)

    slot, slot_top, slot_ins = slots(ep.card_w)
    seq: list[tuple[str, int, int, int, float]] = []   # kind, index, rank, slot, scale
    # Countdown order: highest rank number first; within a tie, file order reversed so the
    # file's first item (e.g. alphabetical) ends up nearest the champion side. Deterministic.
    if ep.is_list:
        order = list(range(len(items)))                        # file order, first item enters first
    else:
        order = sorted(range(len(items)), key=lambda i: (items[i].rank, i), reverse=True)
    last_of_rank = {items[i].rank: i for i in order}          # last card of each rank in countdown
    for i in order:
        it = items[i]
        big = it.rank <= TOP_N_BIG and not ep.is_list
        seq.append(("card", i, it.rank, slot_top if big else slot, TOP_SCALE if big else 1.0))
        if last_of_rank[it.rank] == i:
            for j in after.get(it.rank, []):
                seq.append(("insight", j, it.rank, slot_ins, 1.0))

    elements: list[Element] = []
    x = 0
    for n, (kind, idx, rank, slot, scale) in enumerate(seq):
        if n:
            x += (seq[n - 1][3] + slot) // 2
        elements.append(Element(kind, idx, rank, x, slot, scale))

    first_scale = elements[0].scale
    first_sx = LEFT_MARGIN + int(ep.card_w * first_scale) // 2
    first_sx -= first_sx % 2
    cam_start = elements[0].center + (W // 2 - first_sx)   # first card fully visible at the left edge
    # champion centred; tied champions (same top rank) are centred as a group so none is cut off
    top_rank = min(it.rank for it in items)
    tied = ([elements[-1]] if ep.is_list else
            [e for e in elements if e.kind == "card" and e.rank == top_rank])
    cam_end = (tied[0].center + tied[-1].center) // 2
    dist = cam_end - cam_start
    if dist < EASE_DIST:
        raise ValueError("too few elements to scroll")
    ease_dist = EASE_DIST + (dist - EASE_DIST) % SPEED     # whole SPEED steps in the constant part, remainder eased
    f_const = (dist - ease_dist) // SPEED
    f_ease = int(round(2 * ease_dist / SPEED))
    f_intro = int(INTRO * FPS)
    f_hold = int(round(ep.intro_hold * FPS))
    f_scroll = f_hold + f_const + f_ease

    tl = Timeline(elements, cam_start, cam_end, f_intro, f_scroll, f_const, f_ease,
                  int((LAST_HOLD if ep.is_list else CHAMP_HOLD) * FPS), int(TALLY * FPS), int(SOURCES * FPS), int(ENDSCREEN * FPS),
                  f_hold=f_hold, ease_dist=ease_dist)
    a = 0
    for name, length in (("intro", f_intro), ("scroll", f_scroll), ("champion", tl.f_champ),
                         ("tally", tl.f_tally), ("sources", tl.f_sources), ("end", tl.f_end)):
        tl.segments.append((name, a, a + length))
        a += length
    return tl


def describe(tl: Timeline) -> str:
    lines = [f"total {tl.duration:.2f}s ({tl.total_frames} frames @ {FPS}fps)"]
    for name, a, b in tl.segments:
        lines.append(f"  {name:9s} {a / FPS:7.2f}s → {b / FPS:7.2f}s  ({(b - a) / FPS:.2f}s)")
    lines.append(f"  elements {len(tl.elements)}  band {tl.cam_start}→{tl.cam_end}px  speed {SPEED}px/frame")
    return "\n".join(lines)
