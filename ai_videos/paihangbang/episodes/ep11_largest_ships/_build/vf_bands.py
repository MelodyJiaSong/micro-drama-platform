# 按 GT 区间自适应切分抓 VesselFinder 高级搜索（每段 ≤ 1 页），避免翻页漂移漏船
import sys, re, json
sys.path.insert(0, '.')
import vf
out = {}
def band(lo, hi):
    t = vf.get(f"https://www.vesselfinder.com/vessels?minGT={lo}&maxGT={hi}", f"band_{lo}_{hi}.html")
    m = re.search(r'pagination-totals">([\d,]+) ships', t)
    n = int(m.group(1).replace(',', '')) if m else 0
    if n > 20 and hi - lo > 1:
        mid = (lo + hi) // 2
        band(lo, mid); band(mid + 1, hi); return
    for tr in re.findall(r"<tr>(.*?)</tr>", t, re.S):
        mm = re.search(r'href="/vessels/details/(\d+)"', tr)
        if not mm: continue
        tds = [vf.clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        nt = re.sub(r'\s{2,}', '|', tds[0]).split('|')
        out[mm.group(1)] = {"imo": mm.group(1), "name": nt[0], "type": nt[-1] if len(nt) > 1 else "", "year": tds[1], "gt": tds[2], "dwt": tds[3], "size": tds[4]}
    if n > 20: print("WARN band still >20", lo, hi, n)
band(160000, 600000)
rows = sorted(out.values(), key=lambda r: -int(r["gt"]) if r["gt"].isdigit() else 0)
json.dump(rows, open('vf_fleet_gt160_bands.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(rows))
