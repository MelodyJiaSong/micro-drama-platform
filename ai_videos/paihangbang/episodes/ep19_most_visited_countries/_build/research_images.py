# -*- coding: utf-8 -*-
# 注意：follow-up 023（2026-11-03）起不再调用 Codex，本脚本停用、未运行过；保留作记录。
"""ep19 补搜（follow-up 016 第二步「单独再搜一轮」）：复用共用 image_reselect.py 的 run_search（同一 RequestLog 先记日志），
只改提示词（要求每项至少 N 张、不同机位 / 摄影师）和批次，可只搜指定条目。结果写 _build/reselect/codex_b<tag>.json，
共用 download / score / apply 会一并读入。

    python -I _build/research_images.py --round r2 --batch 3 --n 8 [--only 0 5 12] [--workers 2]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
REPO = EP.parents[3]
sys.path.insert(0, str(REPO / "ai_videos" / "paihangbang" / "_tools"))
import image_reselect as R  # noqa: E402

R.PROMPT = """Use web search to find real photographs (not AI-generated, not renders, not illustrations) of the specific landmark named for each subject below, for a full-bleed {shape} card in a YouTube ranking video about the world's most visited countries.
For EACH subject return AT LEAST 6 and ideally {n} different candidates (different photographers, angles, light). The landmark must be the one named in the note — check the photo really shows it and not a similarly named or similar-looking place listed after "NOT".
Prefer: {prefer}; sharp; long side >= 2000 px; no watermarks, no text overlays, no logos, no collage, no heavy HDR/AI look.
Do NOT use Wikimedia Commons / Wikipedia images at all (no upload.wikimedia.org). Search Pexels, Unsplash and Pixabay first (search each site for the landmark name), then Flickr (CC-licensed), official tourism boards, photographers' sites.
Report the licence EXACTLY as stated on the source page (e.g. "Pexels License", "Unsplash License", "Pixabay Content License", "CC BY 2.0", "All rights reserved"); write "unknown" if the page does not state one.
For each candidate give a DIRECT image file URL that downloads the image itself (e.g. images.pexels.com/photos/..., images.unsplash.com/photo-..., cdn.pixabay.com/photo/..., live.staticflickr.com/..._b.jpg), the page URL, the source site, the author, the exact licence name, and a short reason naming what is visible.
Copy each subject's key exactly. Do not run shell commands. Return only the JSON.

Subjects:
{subjects}"""


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--batch", type=int, default=3)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--only", type=int, nargs="*", default=None, help="data.json items 下标（0 起）")
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    p = R.ep_paths(EP)
    p["build"].mkdir(parents=True, exist_ok=True)
    (p["build"] / "codex_schema.json").write_text(json.dumps(R.SCHEMA), encoding="utf-8")
    items = [(i, it) for i, it in enumerate(data["items"]) if a.only is None or i in a.only]
    shape = "landscape-friendly near-square (9:10)"
    prefer = data["layout"]["image_prefer"]
    batches = [items[k:k + a.batch] for k in range(0, len(items), a.batch)]
    with ThreadPoolExecutor(a.workers) as ex:
        for msg in ex.map(lambda kb: R.run_search(EP, kb[1], f"{a.round}_{kb[0]:02d}", shape, prefer, a.n), enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
