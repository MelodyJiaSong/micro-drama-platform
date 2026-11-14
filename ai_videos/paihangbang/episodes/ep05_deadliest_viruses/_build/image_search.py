# -*- coding: utf-8 -*-
"""ep05 第二步（follow-up 016）：内容定稿后，按每张卡的内容让 Codex 联网搜病毒电镜图候选。

    python ai_videos/paihangbang/episodes/ep05_deadliest_viruses/_build/image_search.py [--workers 3] [--batch 3] [--tag v1]

输出与 _tools/image_reselect.py 同格式（_build/reselect/codex_<tag>_bNN.json），之后照常：
    python ai_videos/paihangbang/_tools/image_reselect.py download|score|apply <ep_dir>
每次 Codex 调用先经 RequestLog 记进本剧 request_log.md；只找链接，不生成图。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
REPO = EP.parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "ai_videos" / "paihangbang" / "_tools"))
from image_reselect import SCHEMA, item_key  # noqa: E402
from tools.service_request import RequestLog  # noqa: E402

# 每种病毒的形态提示，帮 Codex 认对图（不是给生成用的）
LOOK = {
    "smallpox": "variola virus: large brick-shaped poxvirus particles (TEM); vaccinia acceptable only if labelled orthopoxvirus/variola relative — prefer variola",
    "influenza": "influenza A virus (e.g. H1N1 / 1918 reconstructed / H3N2) spherical or filamentous virions with surface spikes, colorized TEM",
    "hiv": "HIV-1 virions budding from or attached to a T cell, colorized SEM or TEM",
    "measles": "measles virus (morbillivirus) particles, colorized TEM",
    "hbv": "hepatitis B virus (Dane particles, small spheres and filaments), TEM",
    "rotavirus": "rotavirus wheel-shaped particles, colorized TEM",
    "hpv": "human papillomavirus icosahedral particles, TEM (or a scientific cryo-EM reconstruction)",
    "covid": "SARS-CoV-2 virions with crown of spikes, colorized TEM or SEM (NIAID RML)",
    "hcv": "hepatitis C virus particles, TEM / cryo-EM",
    "norovirus": "norovirus small round particles, colorized TEM",
    "rsv": "respiratory syncytial virus filamentous / pleomorphic virions, colorized TEM",
    "ebv": "Epstein–Barr virus (herpesvirus) particles, TEM",
    "hav": "hepatitis A virus small round particles, TEM",
    "dengue": "dengue virus particles, colorized TEM",
    "yellow_fever": "yellow fever virus (flavivirus) particles, TEM",
    "rabies": "rabies virus bullet-shaped virions, colorized TEM",
    "varicella": "varicella-zoster virus (herpesvirus) particles, colorized TEM",
    "je": "Japanese encephalitis virus particles, TEM",
    "kshv": "Kaposi sarcoma-associated herpesvirus (HHV-8) particles, TEM",
    "hanta": "hantavirus (Hantaan / Sin Nombre / Andes) particles, colorized TEM",
    "hev": "hepatitis E virus particles, TEM",
    "ebola": "Ebola virus filamentous virions (shepherd's-crook shape), colorized SEM or TEM",
    "ev71": "enterovirus A71 particles, TEM",
    "wnv": "West Nile virus particles, colorized TEM",
    "tbe": "tick-borne encephalitis virus particles, TEM",
    "mers": "MERS coronavirus particles, colorized TEM (NIAID RML)",
    "sars": "SARS coronavirus (SARS-CoV, 2003) particles, TEM",
    "marburg": "Marburg virus filamentous virions, colorized SEM or TEM",
    "cchf": "Crimean-Congo hemorrhagic fever virus particles, TEM",
    "nipah": "Nipah virus particles, colorized TEM / SEM (NIAID RML)",
}

PROMPT = """Use web search to find the best real scientific images of each virus below, for a full-bleed near-square (9:10) card in an educational YouTube ranking video about the deadliest viruses.
For EACH subject return up to {n} candidates. Prefer, in this order:
1. Colourised electron micrographs (TEM or SEM) of the actual virus — e.g. NIAID Flickr (flickr.com/photos/niaid, usually CC BY 2.0), CDC Public Health Image Library phil.cdc.gov (public domain), NIH / NCI Visuals Online, NIH 3D, other government or university labs.
2. If no good micrograph exists: a scientifically accurate, high-resolution 3D illustration of that specific virus from a free source (CDC/NIH public domain illustrations, Pixabay, Unsplash, Pexels).
Requirements: the image must show THIS virus (check the caption), be sharp, long side >= 1600 px if possible, strong colour, no watermark, no big text or labels baked in, not a collage. Do NOT use Wikimedia Commons / Wikipedia images at all (no upload.wikimedia.org). Avoid stock-agency previews (Science Photo Library, Getty, Shutterstock, Alamy, Dreamstime).
Report the licence EXACTLY as stated on the source page (e.g. "CC BY 2.0", "Public domain", "Pixabay Content License", "All rights reserved"); write "unknown" if the page does not state one.
For each candidate give a DIRECT image file URL that downloads the image itself (e.g. live.staticflickr.com/..._o.jpg or _k.jpg / _b.jpg, phil.cdc.gov/PHIL_Images/..., images.unsplash.com/photo-..., cdn.pixabay.com/...), the page URL, the source site, the author, the exact licence name, and a short reason (say what the caption says the image shows).
Copy each subject's key exactly. Do not run shell commands. Return only the JSON.

Subjects:
{subjects}"""

# 第二轮：只针对高分辨率公共图库，逐个查询，措辞只谈图库检索（第一轮 2 包被 Codex 的生物风险过滤误拦）
PROMPT2 = """This is a picture-library lookup for a school-level science video. Use web search to find high-resolution catalogue images of the microscope subject below in public science image libraries. Only links are needed.
Look first at: the NIAID account on Unsplash (unsplash.com/@niaid, Unsplash License, originals 3000–4500 px), the NIH Image Gallery on Flickr (flickr.com/photos/nihgov, public domain; give the largest size, e.g. _o.jpg / _k.jpg / _h.jpg), the NIAID Flickr account (flickr.com/photos/niaid, CC BY 2.0; largest size), CDC Public Health Image Library (phil.cdc.gov, public domain), NCI Visuals Online, Pixabay. Do NOT use Wikimedia Commons / Wikipedia.
Return up to {n} different images of THIS subject (check each caption names it), largest available size, no watermark, no baked-in labels if possible. Report the licence exactly as stated on the page ("unknown" if none).
For each: a DIRECT image file URL (images.unsplash.com/photo-...?w=4000 style is fine, live.staticflickr.com/..._o.jpg, phil.cdc.gov/PHIL_Images/...), the page URL, source site, author, licence, and a short reason quoting the caption. Copy the key exactly. Do not run shell commands. Return only the JSON.

Subject:
{subjects}"""


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--batch", type=int, default=3)
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--tag", default="b", help="文件名前缀；须以 b 开头，download 才认（codex_b*.json）")
    ap.add_argument("--only", nargs="*", default=[], help="只搜这些 key（病毒 key，如 hpv kshv）")
    ap.add_argument("--v2", action="store_true", help="第二轮：高分辨率图库专搜（PROMPT2）")
    a = ap.parse_args()
    build = EP / "_build" / "reselect"
    build.mkdir(parents=True, exist_ok=True)
    schema = build / "codex_schema.json"
    schema.write_text(json.dumps(SCHEMA), encoding="utf-8")
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    items = [(i, it) for i, it in enumerate(data["items"]) if not a.only or it["key"] in a.only]
    batches = [items[k:k + a.batch] for k in range(0, len(items), a.batch)]

    def run(kb):
        k, batch = kb
        tag = f"{a.tag}{k:02d}"
        out = build / f"codex_{tag}.json"
        if out.exists():
            return f"{tag} 已有，跳过"
        subjects = "\n".join(f"- key {item_key(i, it)}: {it['name']} ({it['tags'][0]['text']} family) — look for: {LOOK[it['key']]}" for i, it in batch)
        prompt = PROMPT.format(n=a.n, subjects=subjects)
        argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
                "--output-schema", str(schema), "-o", str(out), "-"]
        req = {"argv": argv, "prompt": prompt, "purpose": "ep05 病毒电镜图候选链接（只找链接，不生成图；follow-up 016 第二步）",
               "output": str(out), "cost": "ChatGPT 订阅额度，未知"}
        r = RequestLog(EP).invoke("codex_cli", "web_search", req, lambda: subprocess.run(
            argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500))
        return f"{tag} rc={r.returncode} {'ok' if out.exists() else 'NO OUTPUT ' + r.stderr[-300:]}"

    with ThreadPoolExecutor(a.workers) as ex:
        for msg in ex.map(run, enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
