# DNV Vessel Register（船级社公开登记，含 GT69、船厂、交船日、运营状态、船东/管理人）。缓存到 dnv/
import json, sys, time, urllib.request, urllib.parse
from pathlib import Path
D=Path(__file__).parent/"dnv"; D.mkdir(exist_ok=True)
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
B="https://vesselregister.dnv.com/vesselregister"
def j(url):
    for k in range(3):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40).read())
        except Exception as e: print("retry",url,e,file=sys.stderr); time.sleep(3*(k+1))
    return None
def by_imo(imo):
    p=D/f"{imo}.json"
    if p.exists(): return json.loads(p.read_text(encoding="utf-8"))
    s=j(f"{B}/vessel/get?term={imo}")
    hits=[v for v in (s or {}).get("vessels",[]) if v.get("imoNo")==str(imo)]
    d={"search":s}
    if hits:
        d["details"]=j(f"{B}/VesselDetails?vesselId={hits[0]['id']}")
    p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8"); time.sleep(0.5)
    return d
def summary(imo):
    d=by_imo(imo); x=d.get("details") or {}
    if not x: return f"{imo} | (not in DNV register)"
    i=x.get("identification",{}); y=x.get("yard",{}); m=x.get("dimensions",{}); o=x.get("owner",{})
    return " | ".join(str(v) for v in [imo,i.get("vesselName"),i.get("classStatusString"),i.get("operationalStatusString"),i.get("flagName"),m.get("grossTon69"),m.get("lengthOverall"),y.get("contractedBuilder") or y.get("hullYardName"),(y.get("dateOfBuild") or "")[:10],o.get("ownerName"),o.get("managerName")])
if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for imo in sys.argv[1:]: print(summary(imo))
