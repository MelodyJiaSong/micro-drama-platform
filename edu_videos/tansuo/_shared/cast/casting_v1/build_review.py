"""生成选角审阅页 review.json（/character-review?path=edu_videos/tansuo/_shared/cast/casting_v1）。"""
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
                items.append({"id": f"{c['id']}{'a' if kind == 'turnaround' else 'b'}", "label": f"{c['label']} — {label}",
                              "path": rel(img), "kind": "image",
                              "desc": "表情顺序（左上起）：" + role["expressions"] if kind == "expressions" else c["person"]})
    sections.append({"id": role_id, "title": role["name"], "layout": "wide", "items": items})

review = {
    "title": "探索系列 · 主角选角 v1",
    "character": "edu_videos/tansuo 主角",
    "updated": spec["date"],
    "notes": [
        "向导 3 位（G1 是故事板 v2 里的林工）、新手 4 位（K4 是女生选项）。每位一张四视图、一张六格表情。",
        "说编号就行：例如「向导选 G2」「新手 K1，但头发再短一点」「G3 和 K2 放一起看看」。",
        "同一角色的服装先统一，方便只比人；选定后再按主题设计换装。",
        "都是虚构人物；出图时要求不像任何真实名人。",
        "自查：K1–K3 看上去偏欧洲面孔、混血感不强；想要更明显的华人特征就说「K2 更像中欧混血」之类，我再调。",
    ],
    "sections": sections,
}
(HERE / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(len(s["items"]) for s in sections), "items")
