# -*- coding: utf-8 -*-
"""第二轮 Codex 找图（follow-up 018：每张卡多候选）。首轮每项只回 2–3 张；本轮每包 2 项、每项要 8 张，
补充 iNaturalist（CC BY / CC0 研究级观测）与 Flickr CC 作为稀有物种来源。结果写 reselect/codex_b2_NN.json，
image_reselect.py download 会一并读取（glob codex_b*.json）。
用法：python <本文件> [--only idx,idx] [--workers 6]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
import image_reselect as R  # noqa: E402

R.PROMPT = R.PROMPT.replace("For EACH subject return up to {n} candidates.",
    "For EACH subject return {n} candidates (at least 6; search several sites, do not stop at the first good one). "
    "Every candidate MUST show the exact species named (check the source page caption / species ID) — a wrong species or a "
    "domestic / captive look-alike is worse than no candidate.") \
    .replace("Look anywhere else: Pexels, Unsplash, Pixabay, Flickr,",
    "Look anywhere else: Pexels, Unsplash, Pixabay, iNaturalist research-grade observations (CC BY / CC0 photos; use the "
    "inaturalist-open-data 'original' or 'large' URL), Flickr (prefer CC-licensed; use the _b / _h / _k / _o size), "
    "national park / conservation NGO sites,")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--tag", default="b2")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    items = list(enumerate(data["items"]))
    if a.only:
        keep = {int(x) for x in a.only.split(",")}
        items = [x for x in items if x[0] in keep]
    batches = [items[k:k + 2] for k in range(0, len(items), 2)]
    prefer = data["layout"]["image_prefer"]
    with ThreadPoolExecutor(a.workers) as ex:
        for msg in ex.map(lambda kb: R.run_search(EP, kb[1], f"{a.tag}_{kb[0]:02d}", "near-square (9:10)", prefer, a.n),
                          enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
