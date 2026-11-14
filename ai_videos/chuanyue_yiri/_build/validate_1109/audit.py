# -*- coding: utf-8 -*-
"""EP01 全集只读审计（2026-11-09）：每镜/镜组的出片、审核结论、用的 prompt 与参考是不是当前版本、Riley 用的是哪一版脸、剪辑用的是哪一条。"""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
EP = os.path.join(REPO, "ai_videos/chuanyue_yiri/episodes/ep01")
CH = os.path.join(REPO, "ai_videos/chuanyue_yiri/2_世界观人设/characters")
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
# Riley 各版本三视图合图 sha
RV = {}
for lab, p in [("v2旧脸", "c1_Riley/_v2_tall/c1_Riley_views.png"), ("当前", "c1_Riley/views/c1_Riley_views.png")]:
    s = sha(os.path.join(CH, p)); RV[s] = lab
for p in glob.glob(os.path.join(CH, "c1_Riley/_v3*/**/*views*.png"), recursive=True):
    RV.setdefault(sha(p), os.path.relpath(p, os.path.join(CH, "c1_Riley")).split(os.sep)[0])
filming = json.load(open(os.path.join(EP, "filming.json"), encoding="utf-8"))["content"]["scenes"]
prompts = json.load(open(os.path.join(EP, "prompts.json"), encoding="utf-8"))["content"]
ptext = {}
for sc in prompts["scenes"]:
    for x in sc.get("shots", []) + sc.get("groups", []):
        ptext[x["id"]] = x["text"]
# 每场最新正片剪辑用到的条
used = {}
for sc in filming:
    cuts = sorted(glob.glob(os.path.join(EP, f"scenes/{sc['id']}/edit/final/cut_v*.json")), key=lambda f: int(re.search(r"v(\d+)", f).group(1)))
    if cuts:
        d = json.load(open(cuts[-1], encoding="utf-8"))
        for e in d.get("events", []):
            used.setdefault(sc["id"], {})[e.get("shot") or e.get("group")] = (e.get("take"), os.path.basename(cuts[-1]), e.get("sha256"))
rows = []
for sc in filming:
    sid = sc["id"]
    units = [("shots", s["id"]) for s in sc["shots"]] + [("groups", g["id"]) for g in sc.get("groups", [])]
    for kind, uid in units:
        rd = sorted(glob.glob(os.path.join(EP, f"scenes/{sid}/{kind}/{uid}/renders/2026*")))
        if not rd:
            continue
        u = used.get(sid, {}).get(uid)
        for r in rd:
            take = os.path.basename(r)
            g = json.load(open(os.path.join(r, "generation.json"), encoding="utf-8")) if os.path.isfile(os.path.join(r, "generation.json")) else {}
            rv = os.path.join(r, "review.md")
            st = re.search(r"状态：(.+)", open(rv, encoding="utf-8").read()).group(1).strip() if os.path.isfile(rv) else "未审"
            key = g.get("key", "")
            cur = ptext.get(key)
            prompt_ok = cur is not None and hashlib.sha256(cur.encode("utf-8")).hexdigest() == g.get("prompt_sha256")
            face = "无 Riley"
            changed = []
            for ref in g.get("refs", []):
                cur_sha = sha(os.path.join(REPO, ref["src"]))
                if ref.get("key") == "c1_Riley" or "c1_Riley" in ref["src"]:
                    face = RV.get(ref.get("sha256"), "其他版本")
                elif cur_sha != ref.get("sha256"):
                    changed.append(ref.get("role", ref.get("key")))
            vid = os.path.join(r, g.get("video", "")) if g.get("video") else None
            in_cut = bool(u and u[0] == take)
            rows.append(dict(scene=sid, unit=uid, take=take, model=g.get("model"), res=g.get("resolution"), dur=g.get("duration_s"),
                             status=st, prompt="当前" if prompt_ok else ("prompt 已改" if cur else "已不在编译结果"), face=face,
                             changed=changed, in_cut=in_cut, cut=u[1] if in_cut else "", video_ok=bool(vid and os.path.isfile(vid))))
json.dump(rows, open(os.path.join(os.path.dirname(__file__), "renders.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# 汇总
from collections import Counter
cut_rows = [r for r in rows if r["in_cut"]]
print("出片条数", len(rows), "｜被最新场剪辑采用", len(cut_rows))
print("采用条的脸：", Counter(r["face"] for r in cut_rows))
print("采用条的 prompt：", Counter(r["prompt"] for r in cut_rows))
print("采用条的审核：", Counter(r["status"][:6] for r in cut_rows))
print("采用条参考图已变：", [(r["scene"], r["unit"], r["changed"]) for r in cut_rows if r["changed"]])
print("采用条缺视频：", [(r["scene"], r["unit"]) for r in cut_rows if not r["video_ok"]])
# 分镜里每个镜头是否被剪辑覆盖
for sc in filming:
    have = set(used.get(sc["id"], {}))
    grouped = {s for g in sc.get("groups", []) for s in g["shots"]}
    miss = [s["id"] for s in sc["shots"] if s["id"] not in have and not any(g["id"] in have and s["id"] in g["shots"] for g in sc.get("groups", []))]
    print(sc["id"], "分镜", len(sc["shots"]), "镜｜剪辑用了", len(have), "个单元｜未进剪辑：", miss)
