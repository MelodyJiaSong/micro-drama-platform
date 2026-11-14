# Flickr 搜索页抓取（只取可商用许可：CC BY / BY-SA / CC0 / PDM，含 4.0 版），解析页内 photo-lite-models
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
D = Path(__file__).parent / "flickr"; D.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {4: "CC BY 2.0", 5: "CC BY-SA 2.0", 9: "CC0 1.0", 10: "Public Domain Mark 1.0", 11: "CC BY 4.0", 12: "CC BY-SA 4.0"}
def get(url, cache):
    p = D / cache
    if p.exists() and p.stat().st_size > 1000: return p.read_text(encoding="utf-8")
    for k in range(3):
        try:
            import subprocess                                # urllib 请求常被 Flickr 后端判 apiFailed，curl 正常
            t = subprocess.run(["curl", "-s", "-m", "40", "-A", UA["User-Agent"], url], capture_output=True).stdout.decode("utf-8", "replace")
            if '"apiFailed":true' in t:                    # Flickr 后端限流（零结果页不带此标记）：不缓存，退避重试
                print("apiFailed, backoff", url, file=sys.stderr); time.sleep(30); continue
            p.write_text(t, encoding="utf-8"); time.sleep(2.5); return t
        except Exception as e:
            print("retry", url, e, file=sys.stderr); time.sleep(5 * (k + 1))
    return ""
def search(text, licenses="4,5,9,10,11,12", page=1):
    params = {"text": text, "license": licenses}
    if page > 1: params["page"] = page
    q = urllib.parse.urlencode(params)
    t = get("https://www.flickr.com/search/?" + q, "s_" + re.sub(r"\W+", "_", text)[:80] + (f"_p{page}" if page > 1 else "") + ".html")
    dec = json.JSONDecoder(); out = []
    for m in re.finditer(r'\{"_flickrModelRegistry":"photo-lite-models"', t):
        try: o, _ = dec.raw_decode(t, m.start())
        except Exception: continue
        sizes = (o.get("sizes") or {}).get("data") or {}
        best = None
        for key in ("o", "6k", "5k", "4k", "3k", "k", "h", "l", "c", "z"):
            s = (sizes.get(key) or {}).get("data")
            if s and s.get("url"):
                best = s; break
        if not best: continue
        url = best["url"]; url = "https:" + url if url.startswith("//") else url
        pid = re.search(r"/(\d+)_", url)
        out.append({"id": pid.group(1) if pid else "", "title": o.get("title", ""), "description": (o.get("description") or "")[:400],
                    "author": o.get("realname") or o.get("username") or "", "owner": o.get("ownerNsid", ""), "license": o.get("license"),
                    "licence": LIC.get(o.get("license"), f"flickr-license-{o.get('license')}"), "image_url": url,
                    "w": best.get("width"), "h": best.get("height"),
                    "page_url": f"https://www.flickr.com/photos/{o.get('pathAlias') or o.get('ownerNsid')}/{pid.group(1) if pid else ''}"})
    return out
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for q in sys.argv[1:]:
        r = search(q)
        print(f"== {q}: {len(r)}")
        for x in r[:25]: print("  ", x["licence"], x["w"], x["h"], x["author"][:20], "|", x["title"][:70])
