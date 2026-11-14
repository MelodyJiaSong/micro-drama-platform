# VesselFinder 抓取（只读公开页面，缓存到 vf/）：search <name> / detail <imo>
import re, sys, json, time, urllib.request, urllib.parse, html
from pathlib import Path
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
D=Path(__file__).parent/"vf"; D.mkdir(exist_ok=True)
def get(url, cache):
    p=D/cache
    if p.exists(): return p.read_text(encoding="utf-8")
    for k in range(4):
        try:
            t=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40).read().decode("utf-8","replace"); break
        except Exception as e:
            print("retry",url,e,file=sys.stderr); time.sleep(5*(k+1))
    else: return ""
    p.write_text(t,encoding="utf-8"); time.sleep(1.0); return t
def clean(s): return html.unescape(re.sub(r"<[^>]+>","",s)).strip()
def search(name):
    t=get("https://www.vesselfinder.com/vessels?name="+urllib.parse.quote(name), "s_"+re.sub(r"\W+","_",name)+".html")
    rows=[]
    for tr in re.findall(r"<tr>(.*?)</tr>",t,re.S):
        m=re.search(r'href="/vessels/details/(\d+)"',tr)
        if not m: continue
        tds=[clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>",tr,re.S)]
        rows.append([m.group(1)]+tds)
    return rows
def detail(imo):
    t=get(f"https://www.vesselfinder.com/vessels/details/{imo}", f"d_{imo}.html")
    d={}
    for m in re.finditer(r'<td class="(?:n3|tpc1)"[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',t,re.S):
        d[clean(m.group(1))]=clean(m.group(2))
    return d
if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1]=="search":
        for n in sys.argv[2:]:
            for r in search(n): print(n,"|"," | ".join(r))
    else:
        keys=["Vessel Name","Ship Type","Flag","Year of Build","Gross Tonnage","Deadweight (t)","TEU","Length / Beam","Navigation Status","Position Received"]
        for imo in sys.argv[2:]:
            d=detail(imo); print(imo," | ".join(f"{d.get(k,'')}" for k in keys))
