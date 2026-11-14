"""Build a synthetic episode directory (generated images, real flags) for tests and previews."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import skia

COUNTRIES = [("us", "United States", "North America"), ("cn", "China", "Asia"), ("ae", "United Arab Emirates", "Asia"),
             ("jp", "Japan", "Asia"), ("fr", "France", "Europe"), ("br", "Brazil", "South America"),
             ("ke", "Kenya", "Africa"), ("au", "Australia", "Oceania")]


def make_episode(root: Path, n: int = 14, tally_by: str = "country", theme: str = "skyline") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    img_dir = root / "assets" / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    items, ledger = [], []
    for rank in range(1, n + 1):
        iso, cname, cont = COUNTRIES[rank % len(COUNTRIES)]
        rel = f"assets/img/{rank:02d}_item.jpg"
        surf = skia.Surface(800, 600)
        c = surf.getCanvas()
        hue = (rank * 37) % 360
        c.drawPaint(skia.Paint(Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(800, 600)],
            [skia.Color4f.FromColor(skia.ColorSetARGB(255, 40, 80 + rank * 5 % 150, 160)).toColor(),
             skia.ColorSetARGB(255, 230, (hue * 2) % 255, 90)])))
        c.drawCircle(400, 300, 120, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        surf.makeImageSnapshot().save(str(root / rel), skia.kJPEG)
        sha = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        ledger.append({"file": rel, "author": "Synthetic", "licence": "CC0", "sha256": sha})
        value = 900 - rank * 23.4
        items.append({
            "rank": rank, "name": f"Test Tower Number {rank}" if rank != 3 else "An Extremely Long Building Name That Must Shrink",
            "subtitle": "Somewhere City", "country_iso2": iso.upper(), "country_name": cname, "continent": cont,
            "value": value, "value_display": f"{value:,.0f} m", "secondary_display": f"{value * 3.28084:,.0f} ft",
            "badge": "NEW 2026" if rank % 5 == 0 else "", "tags": [{"icon": "stairs", "text": f"{100 + rank} floors"},
                                                                {"icon": "calendar", "text": "Completed 2019"}],
            "image": rel, "image_credit": "Synthetic / CC0",
        })
    data = {"episode": "fixture", "title": "World's Tallest Test Towers", "kicker": f"TOP {n}", "metric_label": "Height",
            "unit": "m", "period_label": "Data as of Nov 2026", "source_line": "Source: synthetic fixture",
            "theme": theme, "tally": {"by": tally_by, "title": "Towers by country" if tally_by == "country" else "By continent"},
            "items": items, "insights": [{"after_rank": 11, "text": "This is a synthetic insight card used to test wrapping across several lines."},
                                          {"after_rank": 4, "text": "Second insight."}]}
    (root / "data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (root / "assets.json").write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return root


if __name__ == "__main__":
    import sys
    print(make_episode(Path(sys.argv[1])))
