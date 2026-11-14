"""渲染前闸门（bible §7 第 1–3a 条）。

    python ai_videos/zhenshi_chidu/_tools/gate.py <集目录>

1 每个主体与人体参照都在 licenses.csv，许可在白名单（§0.1）；
2 scale_check.json 全部 ≤ 2%、落地；3 每个参照人 1.75 m ± 1%；
3a AI 模型 x_stretch ≤ 8%、模型长 ÷ 头体长 0.7–1.15（models_ai.json 的 check）；
   2.5D 版（data.json 每条有 cutout）改查：抠像 PNG 存在、肩线在剪影内（肩顶在底行之上）、
   剪影长 ÷ 头体长 0.7–1.6（含头颈、尾、角，只防抠错或比例离谱），参照人抠像已登记。
全部通过退出码 0，否则列出问题、退出码 1。
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

WHITELIST = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "own-generated", "public-domain"}


def main() -> None:
    ep = Path(sys.argv[1])
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    problems = []
    lic = list(csv.DictReader((ep / "licenses.csv").open(encoding="utf-8")))
    ids = {r["asset_id"] for r in lic}
    for r in lic:
        if r["license"] not in WHITELIST:
            problems.append(f"许可不在白名单：{r['item_name']} {r['license']}")
    for it in data["items"]:
        if not it.get("model") or it["model"]["key"] not in ids:
            problems.append(f"未登记模型：{it['name']}")
    if not any(r["role"] == "human" for r in lic):
        problems.append("人体参照未登记")
    sc = json.loads((ep / "scale_check.json").read_text(encoding="utf-8"))
    if len(sc["items"]) != len(data["items"]):
        problems.append(f"比例机检条数 {len(sc['items'])} ≠ {len(data['items'])}")
    for r in sc["items"]:
        if not r["pass"]:
            problems.append(f"比例机检不过：{r}")
    repo = Path(__file__).resolve().parents[3]
    if all(it.get("cutout") for it in data["items"]):
        cuts = json.loads((ep / "assets/cutouts/cutouts.json").read_text(encoding="utf-8"))
        if "human" not in cuts or not (repo / cuts["human"]["png"]).exists():
            problems.append("参照人抠像未登记")
        for it in data["items"]:
            c = it["cutout"]
            if not (repo / c["png"]).exists():
                problems.append(f"3a 抠像缺文件：{it['name']}")
                continue
            px_h = c["bottom"] - c["shoulder_top"]
            if px_h <= 0:
                problems.append(f"3a 肩线不在剪影内：{it['name']}")
                continue
            ratio = c["size"][0] * it["dims"]["height_m"] / px_h / it["dims"]["length_m"]
            if not 0.7 <= ratio <= 1.6:
                problems.append(f"3a 剪影长 ÷ 头体长 {ratio:.2f} 超出 0.7–1.6：{it['name']}")
    else:
        models = json.loads((ep / "assets/models_ai/models_ai.json").read_text(encoding="utf-8"))["models"]
        for it in data["items"]:
            c = models[it["model"]["key"]]["check"]
            if not (c.get("x_stretch_ok") and c.get("length_ok")):
                problems.append(f"3a 不过：{it['name']} {c}")
    print("GATE", "PASS" if not problems else "FAIL")
    for p in problems:
        print(" -", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
