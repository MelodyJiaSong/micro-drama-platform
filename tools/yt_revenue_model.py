"""Attach a 6-month solo-creator revenue projection to a research dataset.

Every number here is derived, and the derivation is written into the dataset so
the UI can show its own arithmetic. The two inputs are measured, not guessed:

  * `views_6mo` comes from enumerating real channels that started in the last
    ~10 months in each format and normalising to one person's sustainable output.
  * `rpm` comes from published per-niche RPM evidence, per market.

The projection's dominant term is not RPM — it is the **YouTube Partner Program
gate**. A channel earns exactly $0 of ad revenue until it clears 1,000 subs plus
4,000 watch hours, so a format whose realistic 6-month view total sits below the
gate is worth $0 in six months no matter how good its RPM is. Reporting
`views x RPM` without that gate is the single easiest way to produce a number
that is wrong by an order of magnitude.

    python tools/yt_revenue_model.py ai_videos/_research/2026-09.json inputs.json
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

# --- YPP gate, as of 2026-09 (thresholds double on 2027-02-01) ---
SUBS_REQUIRED: int = 1000
WATCH_HOURS_REQUIRED: int = 4000
REVIEW_LAG_MONTHS: float = 1.0
PAYOUT_FLOOR_USD: int = 100

# Measured across the new channels in this research: roughly one subscriber per
# 110 views (Ruby 1/119, Grace 1/108, Charles 1/120, Evelyn 1/85, Mosslight 1/23).
VIEWS_PER_SUB: int = 110
# Share of a video's runtime an average viewer actually watches.
RETENTION: float = 0.30
# Cumulative-view share by month for a channel ramping from zero — the measured
# shape is back-loaded: almost nothing lands in months 1-2.
RAMP_SHARE: list[float] = [0.02, 0.06, 0.14, 0.26, 0.50, 1.00]


def gate_month(
    total_views: float, avg_watch_hours_per_view: float, views_per_sub: float
) -> float | None:
    """First month whose cumulative views clear BOTH gate conditions, else None."""
    for i, share in enumerate(RAMP_SHARE, start=1):
        views = total_views * share
        if views / views_per_sub >= SUBS_REQUIRED and views * avg_watch_hours_per_view >= WATCH_HOURS_REQUIRED:
            return float(i)
    return None


def monetized_views(
    total_views: float, avg_watch_hours_per_view: float, views_per_sub: float
) -> tuple[float, float | None]:
    """Views that actually earn: those accruing after the gate clears + review lag."""
    gate = gate_month(total_views, avg_watch_hours_per_view, views_per_sub)
    if gate is None:
        return 0.0, None
    earning_from = gate + REVIEW_LAG_MONTHS
    if earning_from >= len(RAMP_SHARE):
        return 0.0, gate
    lo = int(earning_from) - 1
    share_at_start = RAMP_SHARE[lo] + (RAMP_SHARE[min(lo + 1, len(RAMP_SHARE) - 1)] - RAMP_SHARE[lo]) * (
        earning_from - int(earning_from)
    )
    return total_views * (1.0 - share_at_start), gate


def project(series: dict[str, Any], ramp: dict[str, Any], market: dict[str, Any]) -> dict[str, Any]:
    est = ramp["six_month_view_estimate"]
    # Subscriber conversion is a per-format property, not a constant: measured
    # 49 views/sub for US senior-benefits explainers vs 730 for Hindi nostalgia.
    # Using one global figure is the difference between "earns" and "earns $0".
    views_per_sub = float(ramp.get("views_per_sub") or VIEWS_PER_SUB)
    durations = [v["duration"] for v in series.get("videos", []) if v.get("duration")]
    median_duration = statistics.median(durations) if durations else 600
    per_view_hours = median_duration * RETENTION / 3600.0

    scenarios: dict[str, Any] = {}
    for name in ("low", "mid", "high"):
        views = float(est[name])
        earning, gate = monetized_views(views, per_view_hours, views_per_sub)
        scenarios[name] = {
            "views_6mo": int(views),
            "subs_estimate": int(views / views_per_sub),
            "watch_hours_estimate": int(views * per_view_hours),
            "ypp_cleared_month": gate,
            "monetized_views": int(earning),
            "adsense_usd_low": round(earning / 1000 * market["rpm_low"], 1),
            "adsense_usd_high": round(earning / 1000 * market["rpm_high"], 1),
            "reaches_payout_floor": earning / 1000 * market["rpm_high"] >= PAYOUT_FLOOR_USD,
        }

    return {
        "market_key": market["key"],
        "market_label": market["label_zh"],
        "rpm_low": market["rpm_low"],
        "rpm_high": market["rpm_high"],
        "sustainable_uploads_per_month": est["sustainable_uploads_per_month"],
        "median_duration_sec": int(median_duration),
        "assumptions": {
            "views_per_sub": views_per_sub,
            "retention": RETENTION,
            "ypp_subs": SUBS_REQUIRED,
            "ypp_watch_hours": WATCH_HOURS_REQUIRED,
            "review_lag_months": REVIEW_LAG_MONTHS,
            "payout_floor_usd": PAYOUT_FLOOR_USD,
            "ramp_share_by_month": RAMP_SHARE,
        },
        "scenarios": scenarios,
        "views_basis": est["basis"],
        "rpm_basis": market["basis"],
        "ad_friendliness": market["ad_friendliness"],
        "off_adsense_6mo": market["off_adsense"],
        "confidence": ramp["confidence"],
        "new_channels_measured": len(ramp.get("new_channels") or []),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dataset", type=Path)
    ap.add_argument("inputs", type=Path, help="JSON with {ramps: {slug: ...}, rpm: {markets: [...]}}")
    args = ap.parse_args(argv)
    import sys

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    data = json.loads(args.dataset.read_text(encoding="utf-8"))
    src = json.loads(args.inputs.read_text(encoding="utf-8"))
    by_slug = {s: m for m in src["rpm"]["markets"] for s in m["applies_to_slugs"]}

    for series in data["series"]:
        slug = series["slug"]
        ramp, market = src["ramps"].get(slug), by_slug.get(slug)
        if not ramp or not market:
            print(f"  ! {slug}: no ramp or market — skipped")
            continue
        series["revenue"] = project(series, ramp, market)
        sc = series["revenue"]["scenarios"]
        print(
            f"#{series['rank']:>2} {series['name_zh'][:20]:22} "
            f"views {sc['low']['views_6mo']:>8,}/{sc['mid']['views_6mo']:>9,}/{sc['high']['views_6mo']:>9,}  "
            f"YPP@{sc['mid']['ypp_cleared_month']}  "
            f"6mo ${sc['mid']['adsense_usd_low']:.0f}-{sc['mid']['adsense_usd_high']:.0f}"
        )

    data["revenue_gate"] = src["rpm"]["monetization_gate"]
    data["revenue_caveats"] = src["rpm"]["caveats"]
    args.dataset.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {args.dataset}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
