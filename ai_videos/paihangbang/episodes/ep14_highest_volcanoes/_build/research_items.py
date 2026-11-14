# -*- coding: utf-8 -*-
"""follow-up 016 单项补搜：只对指定名次再跑一轮 Codex 联网搜图（照样经 image_reselect.run_search → RequestLog 先记日志）。
结果写 _build/reselect/codex_bR<round>_<k>.json（文件名排在 codex_b00..b09 之后，download 追加候选、已有候选编号不变）。

    python _build/research_items.py <round> <rank> [<rank> ...] [--hint rank="..."] [--workers 2] [--batch 3]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "ai_videos" / "paihangbang" / "_tools"))
import image_reselect as R  # noqa: E402

EP = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("round")
    ap.add_argument("ranks", nargs="+", type=int)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--batch", type=int, default=3)
    ap.add_argument("--n", type=int, default=8)
    a = ap.parse_args()
    p = R.ep_paths(EP)
    (p["build"] / "codex_schema.json").write_text(json.dumps(R.SCHEMA), encoding="utf-8")
    data, _ = R.load(EP)
    prefer = (data.get("layout") or {}).get("image_prefer")
    prefer += ("; SECOND SEARCH ROUND: the first round found almost only 'all rights reserved' photos, so this round "
               "wants COMMERCIALLY USABLE licences only (public domain, CC0, CC BY, CC BY-SA, Pexels, Unsplash, Pixabay). "
               "Search specifically: ESO / ALMA image archives (eso.org/public/images, almaobservatory.org — CC BY 4.0, "
               "many photos of Atacama volcanoes), NASA Earth Observatory and ISS astronaut photography "
               "(earthobservatory.nasa.gov, eol.jsc.nasa.gov — public domain; oblique views of Andes volcanoes are fine), "
               "USGS (public domain), Flickr photos under CC BY / CC BY-SA (give the live.staticflickr.com _b or _o URL), "
               "Pexels, Unsplash, Pixabay, Openverse. Do NOT return Smithsonian GVP gallery photos (CC BY-NC) or any NC/ND "
               "licence. Return as many valid candidates as you can find (up to the limit), each verified to show the named volcano")
    sel = [(i, it) for i, it in enumerate(data["items"]) if it["rank"] in set(a.ranks)]
    batches = [sel[k:k + a.batch] for k in range(0, len(sel), a.batch)]
    with ThreadPoolExecutor(a.workers) as ex:
        for msg in ex.map(lambda kb: R.run_search(EP, kb[1], f"bR{a.round}_{kb[0]:02d}", "near-square (9:10)", prefer, a.n),
                          enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
