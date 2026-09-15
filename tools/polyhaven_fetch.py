# -*- coding: utf-8 -*-
"""Download CC0 PBR texture maps from Poly Haven (diffuse / GL normal / roughness) into a folder.

Usage:  python tools/polyhaven_fetch.py <dest_dir> <asset_id> [<asset_id> ...] [--res 2k]
Files land at <dest_dir>/<asset_id>/<asset_id>_{diff,nor_gl,rough}_<res>.jpg; existing files are skipped.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

API = "https://api.polyhaven.com/files/{}"
MAPS = ("Diffuse", "nor_gl", "Rough")
UA = {"User-Agent": "micro-drama-platform/polyhaven_fetch"}


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def fetch(dest: Path, asset: str, res: str) -> list[Path]:
    files = json.loads(get(API.format(asset)))
    out: list[Path] = []
    for m in MAPS:
        entry = files.get(m, {}).get(res, {}).get("jpg")
        if entry is None:
            raise SystemExit(f"{asset}: no {m} {res} jpg")
        path = dest / asset / Path(entry["url"]).name
        if not path.is_file():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(get(entry["url"]))
        out.append(path)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dest")
    ap.add_argument("assets", nargs="+")
    ap.add_argument("--res", default="2k")
    a = ap.parse_args()
    for asset in a.assets:
        for p in fetch(Path(a.dest), asset, a.res):
            print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
