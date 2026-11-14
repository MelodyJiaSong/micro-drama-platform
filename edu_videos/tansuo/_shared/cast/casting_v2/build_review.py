"""生成向导重新选角审阅页 review.json（/character-review?path=edu_videos/tansuo/_shared/cast/casting_v2）。"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
spec = json.loads((HERE / "candidates.json").read_text(encoding="utf-8"))
rel = lambda p: p.relative_to(ROOT).as_posix()

sections = []
for role_id, role in spec["roles"].items():
    items = []
    for c in spec["candidates"]:
        if c["role"] != role_id:
            continue
        for kind, label in (("turnaround", "正面 · 四分之三 · 侧面 · 背面"), ("expressions", "表情")):
            img = HERE / f"{c['id']}_{kind}.png"
            if img.exists():
                desc = "表情顺序（左上起）：" + role["expressions"] if kind == "expressions" else c["person"]
                items.append({"id": f"{c['id']}{'a' if kind == 'turnaround' else 'b'}", "label": f"{c['label']} — {label}",
                              "path": rel(img), "kind": "image", "desc": desc})
    sections.append({"id": role_id, "title": "向导 林 / Lin 候选", "layout": "wide", "items": items})

review = {
    "title": "探索系列 · 向导重新选角 v2（知性美）",
    "character": "edu_videos/tansuo 向导",
    "updated": spec["date"],
    "notes": [
        "G4–G8 是新出的五组（漂亮、知性、有书卷气），G1 是原来选的、放在最前面对照。每位一张四视图、一张六格表情。",
        "说编号就行：例如「选 G5」「G4 但不要眼镜」「G6 和凯放一起看看」。",
        "都是虚构人物；出图时要求不像任何真实演员或名人。",
    ],
    "sections": sections,
}
(HERE / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(len(s["items"]) for s in sections), "items")
