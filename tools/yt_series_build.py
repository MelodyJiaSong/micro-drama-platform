"""Assemble a research dataset from a draft, re-measuring every cited video.

The draft carries the judgment (which series, why it works, how a solo creator
would replicate it) and nothing but video *ids* as evidence. This script fetches
each id live and derives every published number itself, so:

  * an id that was hallucinated or mistyped fails loudly instead of shipping,
  * a video outside the research window is dropped instead of padding a series,
  * medians/totals are computed, never asserted.

    python tools/yt_series_build.py draft.json -o ai_videos/_research/youtube_series.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBE = REPO_ROOT / "tools" / "yt_research.py"


def fetch(ids: list[str], jobs: int) -> dict[str, dict[str, Any]]:
    """Live-measure every id. Returns id -> metadata for the ones that resolved."""
    out: dict[str, dict[str, Any]] = {}
    for start in range(0, len(ids), 12):
        batch = ids[start : start + 12]
        done = subprocess.run(
            [sys.executable, str(PROBE), "meta", *batch, "--jobs", str(jobs)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
        )
        for line in done.stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                row = json.loads(line)
                out[row["id"]] = row
        print(f"  measured {len(out)}/{len(ids)}", file=sys.stderr)
    return out


def video_row(meta: dict[str, Any], note: str | None) -> dict[str, Any]:
    row = {
        "video_id": meta["id"],
        "title": meta.get("title") or "",
        "channel": meta.get("channel") or "",
        "channel_url": meta.get("channel_url") or "",
        "url": meta.get("webpage_url") or f"https://www.youtube.com/watch?v={meta['id']}",
        "upload_date": meta.get("upload_date") or "",
        "view_count": meta.get("view_count") or 0,
        "like_count": meta.get("like_count") or 0,
        "like_rate": meta.get("like_rate") or 0.0,
        "duration": meta.get("duration") or 0,
        "vertical": bool(meta.get("vertical")),
    }
    if note:
        row["note"] = note
    return row


def stats_for(videos: list[dict[str, Any]]) -> dict[str, Any]:
    views = [v["view_count"] for v in videos] or [0]
    rates = [v["like_rate"] for v in videos if v["like_rate"]] or [0.0]
    return {
        "videos": len(videos),
        "total_views": sum(views),
        "median_views": int(statistics.median(views)),
        "max_views": max(views),
        "median_like_rate": round(statistics.median(rates), 5),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--window-from", default="20260306")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--min-videos", type=int, default=10)
    args = ap.parse_args(argv)
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    every_id: list[str] = []
    for s in draft["series"]:
        every_id.extend(v["video_id"] if isinstance(v, dict) else v for v in s["videos"])
    unique = list(dict.fromkeys(every_id))
    print(f"measuring {len(unique)} unique videos across {len(draft['series'])} series", file=sys.stderr)
    measured = fetch(unique, args.jobs)

    problems: list[str] = []
    series_out: list[dict[str, Any]] = []
    for s in draft["series"]:
        rows: list[dict[str, Any]] = []
        for entry in s["videos"]:
            vid = entry["video_id"] if isinstance(entry, dict) else entry
            note = entry.get("note") if isinstance(entry, dict) else None
            meta = measured.get(vid)
            if meta is None:
                problems.append(f"{s['slug']}: {vid} did not resolve — dropped")
                continue
            if (meta.get("upload_date") or "") < args.window_from:
                problems.append(
                    f"{s['slug']}: {vid} uploaded {meta.get('upload_date')} — before window, dropped"
                )
                continue
            rows.append(video_row(meta, note))
        rows.sort(key=lambda r: -r["view_count"])
        if len(rows) < args.min_videos:
            problems.append(f"{s['slug']}: only {len(rows)} verified videos (< {args.min_videos})")
        out = {k: v for k, v in s.items() if k != "videos"}
        out["stats"] = stats_for(rows)
        out["videos"] = rows
        series_out.append(out)

    dataset = {k: v for k, v in draft.items() if k != "series"}
    dataset["series"] = series_out
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(s["videos"]) for s in series_out)
    print(f"\nwrote {args.out} — {len(series_out)} series, {total} verified videos", file=sys.stderr)
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
