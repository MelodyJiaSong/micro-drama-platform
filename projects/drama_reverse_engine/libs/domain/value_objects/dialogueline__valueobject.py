from __future__ import annotations

import difflib
import re
from dataclasses import dataclass

_MATCH_RATIO = 0.9
_OVERLAP_MIN_S = 0.2
_NOISE = re.compile(r"[^\w一-鿿]+")


@dataclass(frozen=True)
class RawLine:
    text: str
    start_s: float
    end_s: float


@dataclass(frozen=True)
class ReconciledLine:
    """One dialogue line after OCR/ASR reconciliation (FR-2.3). OCR is the master
    text source; ASR corroborates. `flagged` drives the red-flag UI; single-source
    episodes suppress per-line flags (degradation is episode-level, per U-05)."""

    text: str
    start_s: float
    end_s: float
    status: str  # match | mismatch | ocr_only | asr_only
    flagged: bool
    ocr_text: str = ""
    asr_text: str = ""


def _normalized_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _NOISE.sub("", a), _NOISE.sub("", b)).ratio()


def _overlap(a: RawLine, b: RawLine) -> float:
    return min(a.end_s, b.end_s) - max(a.start_s, b.start_s)


def reconcile_lines(ocr: list[RawLine], asr: list[RawLine]) -> list[ReconciledLine]:
    both_present = bool(ocr) and bool(asr)
    pairs = sorted(
        (
            (-_overlap(o, a), oi, ai)
            for oi, o in enumerate(ocr)
            for ai, a in enumerate(asr)
            if _overlap(o, a) > _OVERLAP_MIN_S
        ),
    )
    ocr_partner: dict[int, int] = {}
    used_asr: set[int] = set()
    for _neg, oi, ai in pairs:
        if oi in ocr_partner or ai in used_asr:
            continue
        ocr_partner[oi] = ai
        used_asr.add(ai)

    result: list[ReconciledLine] = []
    for oi, line in enumerate(ocr):
        ai = ocr_partner.get(oi)
        if ai is None:
            result.append(ReconciledLine(line.text, line.start_s, line.end_s, "ocr_only", both_present,
                                         ocr_text=line.text))
            continue
        partner = asr[ai]
        matched = _normalized_ratio(line.text, partner.text) >= _MATCH_RATIO
        result.append(ReconciledLine(
            line.text, line.start_s, line.end_s,
            "match" if matched else "mismatch", not matched,
            ocr_text=line.text, asr_text=partner.text,
        ))
    for ai, cand in enumerate(asr):
        if ai not in used_asr:
            result.append(ReconciledLine(cand.text, cand.start_s, cand.end_s, "asr_only", both_present,
                                         asr_text=cand.text))
    return sorted(result, key=lambda r: r.start_s)
