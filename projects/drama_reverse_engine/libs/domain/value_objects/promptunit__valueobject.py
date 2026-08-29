from __future__ import annotations

import math
from dataclasses import dataclass

SEEDANCE_MIN_S = 4.0
SEEDANCE_MAX_S = 15.0


@dataclass(frozen=True)
class PromptUnit:
    """One 分镜级 prompt unit (follow-up 005). Episode-level deliverables (script /
    dialogue / novel) keep the original detected shot structure; prompt units re-plan
    those spans under the Seedance 4–15s hard bounds — >15s spans split into 承接
    segments, <4s spans merge into a neighbor. duration_s is always a whole number of
    seconds (follow-up 007), rounded from the real span the unit covers."""

    unit_index: int
    start_s: float
    end_s: float
    duration_s: float
    source_shot_indexes: tuple[int, ...]
    segment: tuple[int, int] | None = None  # (k, n) when a >15s span group was split
    floor_clamped: bool = False  # lone span shorter than 4s, planned duration raised


def plan_prompt_units(spans: list[dict], min_s: float = SEEDANCE_MIN_S,
                      max_s: float = SEEDANCE_MAX_S) -> list[PromptUnit]:
    """spans: ordered [{"index", "start_s", "end_s"}, ...] from shot detection."""
    groups: list[list[dict]] = []
    for span in spans:
        dur = span["end_s"] - span["start_s"]
        if groups and (dur < min_s or _group_duration(groups[-1]) < min_s):
            groups[-1].append(span)
        else:
            groups.append([span])

    units: list[PromptUnit] = []
    for group in groups:
        start = group[0]["start_s"]
        end = group[-1]["end_s"]
        total = end - start
        sources = tuple(s["index"] for s in group)
        if total <= max_s:
            clamped = total < min_s
            units.append(PromptUnit(
                unit_index=len(units) + 1, start_s=start, end_s=end,
                duration_s=float(max(int(min_s), round(total))),
                source_shot_indexes=sources, floor_clamped=clamped,
            ))
            continue
        count = math.ceil(total / max_s)
        base, rem = divmod(round(total), count)
        durations = [base + 1] * rem + [base] * (count - rem)
        seg_start = start
        for k, dur in enumerate(durations):
            seg_end = end if k == count - 1 else min(seg_start + dur, end)
            units.append(PromptUnit(
                unit_index=len(units) + 1, start_s=seg_start, end_s=seg_end,
                duration_s=float(dur),
                source_shot_indexes=sources, segment=(k + 1, count),
            ))
            seg_start = seg_end
    return units


def _group_duration(group: list[dict]) -> float:
    return group[-1]["end_s"] - group[0]["start_s"]
