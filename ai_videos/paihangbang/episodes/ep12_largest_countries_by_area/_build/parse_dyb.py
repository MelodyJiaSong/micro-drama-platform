# 解析 UN DYB 2024 Table 3 的 Surface area 列 -> raw/dyb2024_area.json
import json, re, pymupdf
from pathlib import Path
R = Path(__file__).parent / "raw"
doc = pymupdf.open(R / "dyb2024_table03.pdf")
rows = []
for pno, p in enumerate(doc):
    words = p.get_text("words")
    lines = {}
    for w in words:
        x0, y0, x1, y1, t = w[:5]
        key = round(y0 / 3)
        lines.setdefault(key, []).append((x0, t))
    names = []
    for key in sorted(lines):
        ws = sorted(lines[key])
        left = [t for x, t in ws if x < 165 and not re.match(r"^[\d.*]", t) and t not in ("DF", "DJ")]
        area = [t for x, t in ws if 485 <= x < 548]
        if left and not re.match(r"^\d", ws[0][1]) and ws[0][0] < 60:
            names.append(" ".join(left))
        if area:
            s = "".join(area)
            rows.append({"page": pno + 1, "name": " | ".join(names), "area_raw": " ".join(area)})
            names = []
json.dump(rows, open(R / "dyb2024_area_rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows))
for r in rows[:40]: print(r)
