# -*- coding: utf-8 -*-
"""经 web.archive.org 取 Britannica 河流条目（britannica.com 直连被 Cloudflare 拦），抽出含长度的句子 → raw/brit_lengths.json。可续跑。"""
import json, re, html, subprocess, sys, time
from pathlib import Path
R = Path(__file__).parent / "raw"; B = R / "brit"; B.mkdir(parents=True, exist_ok=True)
SLUGS = sys.argv[1:] or [l.strip() for l in (Path(__file__).parent / "brit_slugs.txt").read_text().split() if l.strip()]
out_p = R / "brit_lengths.json"
out = json.loads(out_p.read_text(encoding="utf-8")) if out_p.exists() else {}
for slug in SLUGS:
    f = B / (slug.replace("/", "_") + ".html")
    if not f.exists() or f.stat().st_size < 5000:
        r = subprocess.run(["curl", "-sL", "--compressed", "-m", "90", "-w", "%{http_code} %{url_effective}", "-o", str(f),
                            f"https://web.archive.org/web/2025id_/https://www.britannica.com/place/{slug}"], capture_output=True, text=True)
        print(slug, r.stdout, flush=True)
        time.sleep(3)
    t = f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    s = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", t))))
    sents = [m.group(0).strip() for m in re.finditer(r"[^.]{0,260}\b(long|length|lengths|flows for|course of)\b[^.]{0,260}\.", s) if re.search(r"\d[\d,]* (miles|km|kilometres)", m.group(0))]
    out[slug] = {"title": title.group(1).strip() if title else "", "bytes": len(t), "sentences": sents[:8],
                 "url": f"https://www.britannica.com/place/{slug}"}
    out_p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in out.items():
    if k in SLUGS:
        print("##", k, "|", v["title"][:60], v["bytes"]); [print("   -", x[:300]) for x in v["sentences"][:4]]
