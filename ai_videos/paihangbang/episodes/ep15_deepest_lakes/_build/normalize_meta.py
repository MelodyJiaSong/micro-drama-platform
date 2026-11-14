# -*- coding: utf-8 -*-
"""把候选 meta.json 里写法不规范的许可名归一成渲染器白名单认得的形式（只改写法，不改许可本身；NC/ND 保持原样被拒）。"""
import glob
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EP = Path(__file__).resolve().parents[1]


def norm(lic: str) -> str:
    low = lic.lower()
    if re.search(r"non-?commercial|noderiv|no deriv|\bnc\b|\bnd\b", low):
        return lic
    ver = re.search(r"(\d\.\d)", lic)
    v = f" {ver.group(1)}" if ver else ""
    if "unsplash" in low and not low.startswith("unsplash license"):
        return "Unsplash License"
    if "pexels" in low and not low.startswith("pexels license"):
        return "Pexels License"
    if re.search(r"attribution[- ]?share ?alike|by-sa", low) and ("creative commons" in low or "attribution" in low):
        return f"CC BY-SA{v}"
    if re.search(r"creative commons attribution|^attribution\b", low):
        return f"CC BY{v}"
    return lic


changed = 0
for f in glob.glob(str(EP / "_build" / "reselect" / "cand" / "*" / "meta.json")):
    ms = json.loads(Path(f).read_text(encoding="utf-8"))
    for m in ms:
        n = norm(m.get("licence", ""))
        if n != m.get("licence"):
            print(Path(f).parent.name, m["id"], repr(m["licence"]), "->", n)
            m.setdefault("licence_as_stated", m["licence"])
            m["licence"] = n
            changed += 1
    Path(f).write_text(json.dumps(ms, ensure_ascii=False, indent=1), encoding="utf-8")
print("changed", changed)
