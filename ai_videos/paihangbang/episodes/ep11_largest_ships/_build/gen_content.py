# 第一步（follow-up 016）：为每项落盘内容 _build/content/NN_<key>.md —— 登记数据、成员、维基摘要、外观辨认、易混对象、拍摄建议
import json, sys
from pathlib import Path
B = Path(__file__).parent; EP = B.parent
sys.path.insert(0, str(B))
from visual_notes import NOTES
from build import EXTRA
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
cs = {c["key"]: c for c in json.loads((B / "classes_computed.json").read_text(encoding="utf-8"))}
from visual_notes import VN_EXTRA
out = B / "content"; out.mkdir(exist_ok=True)
for it in data["items"]:
    k = it["key"]; c = cs[k]; e = EXTRA[k]
    vn = NOTES.get(k) or VN_EXTRA.get(k) or {}
    wp = ""
    if e.get("wiki"):
        p = B / "raw" / "wp" / f"{e['wiki']}.json"
        if p.exists():
            try: wp = json.loads(p.read_text(encoding="utf-8")).get("extract", "")
            except Exception: wp = ""
    mem = "\n".join(f"  - {m[1]} (IMO {m[0]}, {m[2]}, {int(m[3]):,} GT, {m[4]} m)" for m in c["members"][:30])
    md = f"""# {it['rank']:02d} · {it['name']}

- 类型：{it['ship_type']}；运营商：{it['operator']}（{it['country_name']}）
- 船级最大登记总吨：{it['value']:,} GT（代表船 {it['representative']['name']}，IMO {it['representative']['imo']}）
- 来源：{it['source']['name']} — {it['source']['url']}
- 交叉核对：{(it.get('cross_check') or {}).get('name','（无第二来源）')}
- 成员（VesselFinder GT≥160k 清单，{c['n']} 艘，{c['first_year']}–{c['last_year']}）：
{mem}

## 说明
{e['note']}

## 维基摘要（只作文字参考）
{wp or '（无独立维基条目或未取到）'}

## 长什么样（找图辨认）
{vn.get('look','')}

## 易混淆对象
{vn.get('confuse','')}

## 最佳拍摄视角 / 地点
{vn.get('view','')}
"""
    (out / f"{it['rank']:02d}_{k}.md").write_text(md, encoding="utf-8")
print("written", len(data["items"]))
