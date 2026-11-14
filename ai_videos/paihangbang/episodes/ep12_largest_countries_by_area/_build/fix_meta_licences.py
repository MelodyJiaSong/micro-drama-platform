# image_reselect download 会重写 meta.json；apply 前重新写入已核实的许可（来源页原文的规范写法）
import json
from pathlib import Path
C = Path(__file__).parent / "reselect" / "cand"
FIX = {("10_11_dr_congo", "c0"): "CC BY 3.0",                 # imaggeo.egu.eu：Creative Commons Attribution 3.0 Unported
       ("27_28_mauritania", "c0"): "Public domain (NASA)",     # NASA Earth Observatory / ISS crew photo
       ("27_28_mauritania", "c1"): "Public domain (NASA)"}
for (key, cid), lic in FIX.items():
    p = C / key / "meta.json"
    m = json.load(open(p, encoding="utf-8"))
    for x in m:
        if x["id"] == cid:
            x["licence"] = lic
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    print(key, cid, lic)
