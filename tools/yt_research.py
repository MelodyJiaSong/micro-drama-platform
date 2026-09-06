"""YouTube AIGC series research probe — real metrics via yt-dlp, never estimates.

Three sub-commands, all emitting JSON Lines on stdout so callers can pipe/merge:

    search  <query>...        YouTube search, flat (cheap; view_count only)
    channel <handle|url>...   a channel's recent uploads, flat
    meta    <id|url>...       full per-video metadata (adds like_count, upload_date)

`search` / `channel` are one innertube call per target and are the discovery
tier. `meta` fetches a watch page per video and is the verification tier — it is
the only tier that yields like_count, so ranking by like-rate always requires it.

Duplicate ids are collapsed across targets within a single invocation.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Iterable, Iterator

FLAT_FIELDS = (
    "id", "title", "channel", "channel_id", "uploader_id", "view_count",
    "duration", "url", "description",
)
META_FIELDS = (
    "id", "title", "channel", "channel_id", "uploader_id", "channel_url",
    "channel_follower_count", "upload_date", "view_count", "like_count",
    "comment_count", "duration", "webpage_url", "categories", "tags",
    "description", "width", "height",
)

# YouTube `sp=` search filters (double-encoded so the shell/yt-dlp pass them through).
SP_FILTERS: dict[str, str] = {
    "none": "",
    "month": "EgQIBBAB",              # this month + video
    "year": "EgQIBRAB",               # this year + video
    "views_month": "CAMSBAgEEAE%253D",  # sort by views + this month + video
    "views_year": "CAMSBAgFEAE%253D",   # sort by views + this year + video
    "views": "CAMSAhAB",              # sort by views + video
    "recent": "CAISAhAB",             # sort by upload date + video
}


class ProbeError(RuntimeError):
    pass


@dataclass(frozen=True)
class Probe:
    timeout: int
    retries: int

    def _run(self, args: list[str]) -> str:
        last: str = ""
        for attempt in range(self.retries + 1):
            try:
                done = subprocess.run(
                    ["yt-dlp", *args],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                last = f"timeout after {self.timeout}s"
                continue
            if done.returncode == 0 or done.stdout.strip():
                return done.stdout
            last = (done.stderr or "").strip().splitlines()[-1] if done.stderr else "empty output"
        raise ProbeError(last)

    def flat(self, target: str, limit: int) -> Iterator[dict[str, object]]:
        out = self._run([
            "--flat-playlist", "--dump-json", "--no-warnings",
            "--playlist-end", str(limit), "--extractor-args",
            "youtubetab:approximate_date", target,
        ])
        for line in out.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            raw = json.loads(line)
            yield {k: raw.get(k) for k in FLAT_FIELDS}

    def meta(self, video: str) -> dict[str, object]:
        url = video if video.startswith("http") else f"https://www.youtube.com/watch?v={video}"
        out = self._run(["--skip-download", "--dump-json", "--no-warnings", url])
        raw = json.loads(out.splitlines()[0])
        row = {k: raw.get(k) for k in META_FIELDS}
        row["tags"] = (row.get("tags") or [])[:15]
        desc = row.get("description") or ""
        row["description"] = desc[:400]
        views, likes = row.get("view_count"), row.get("like_count")
        row["like_rate"] = round(likes / views, 5) if views and likes else None
        w, h = row.get("width") or 0, row.get("height") or 0
        row["vertical"] = bool(h and w and h > w)
        return row


def _search_url(query: str, sp_key: str) -> str:
    from urllib.parse import quote_plus

    sp = SP_FILTERS[sp_key]
    base = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    return f"{base}&sp={sp}" if sp else base


def _channel_url(handle: str) -> str:
    if handle.startswith("http"):
        return handle if handle.rstrip("/").endswith(("/videos", "/shorts")) else handle.rstrip("/") + "/videos"
    return f"https://www.youtube.com/{handle.lstrip('@') and '@' + handle.lstrip('@')}/videos"


def _emit(rows: Iterable[dict[str, object]], seen: set[str]) -> int:
    n = 0
    for row in rows:
        vid = str(row.get("id") or "")
        if vid and vid in seen:
            continue
        if vid:
            seen.add(vid)
        sys.stdout.write(json.dumps(row, ensure_ascii=False) + "\n")
        n += 1
    sys.stdout.flush()
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("search", "channel", "meta"))
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--limit", type=int, default=20, help="results per search/channel target")
    ap.add_argument("--sp", choices=sorted(SP_FILTERS), default="views_year", help="search filter preset")
    ap.add_argument("--jobs", type=int, default=4, help="parallel workers for meta")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--retries", type=int, default=1)
    args = ap.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    probe = Probe(timeout=args.timeout, retries=args.retries)
    seen: set[str] = set()
    failures = 0

    if args.mode == "meta":
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for target, result in zip(args.targets, pool.map(_safe(probe), args.targets)):
                if isinstance(result, ProbeError):
                    print(f"!! {target}: {result}", file=sys.stderr)
                    failures += 1
                else:
                    _emit([result], seen)
    else:
        build = _search_url if args.mode == "search" else (lambda t, _sp: _channel_url(t))
        for target in args.targets:
            try:
                _emit(probe.flat(build(target, args.sp), args.limit), seen)
            except ProbeError as exc:
                print(f"!! {target}: {exc}", file=sys.stderr)
                failures += 1

    print(f"-- emitted {len(seen)} unique, {failures} failed", file=sys.stderr)
    return 1 if failures and not seen else 0


def _safe(probe: Probe):
    def run(video: str) -> dict[str, object] | ProbeError:
        try:
            return probe.meta(video)
        except (ProbeError, json.JSONDecodeError, IndexError) as exc:
            return ProbeError(str(exc))
    return run


if __name__ == "__main__":
    raise SystemExit(main())
