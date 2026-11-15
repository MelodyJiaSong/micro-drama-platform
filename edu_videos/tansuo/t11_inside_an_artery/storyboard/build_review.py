import json
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
SB = ROOT / "edu_videos/tansuo/t11_inside_an_artery/storyboard"
spec = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
rel = lambda p: p.relative_to(ROOT).as_posix()

items = []
for panel in spec["panels"]:
    image = SB / f"{panel['id']}.png"
    if not image.exists():
        continue
    desc = f"拍 {panel['beat']} · 比例尺 {panel['scale']} · {panel['source']}\n特效：{panel.get('vfx', '—')}\n" + "\n".join(panel["lines"])
    items.append({"id": panel["id"], "label": panel["title"], "path": rel(image), "kind": "image", "desc": desc})

review = {
    "title": f"血脂之旅 t11 · 故事板 {spec['version']}（电影写实 · 林与凯）",
    "character": "edu_videos/tansuo t11_inside_an_artery",
    "updated": spec["date"],
    "notes": [
        "说编号提意见，例如「P05 腰带再清楚一点」「P09 纤维帽太厚」。",
        "画面里的文字、比例尺读数、医学名词、数字和真实性角标都在后期叠加，AI 图里一律不画字。",
        "台词是草稿，讲稿阶段按 edu「先说后写」重说；未核实数字不进最终讲稿。",
        "分子颜色是编码色，不是真实颜色；结构画面最终用 Blender 按研究档案建模，故事板只定构图、走位和情绪。",
        "家人不露面，全片只有林和凯；本期加入他汀机制、血脂关系、降 LDL 结局证据与「治本 / 治标」解释，但不推荐药物，不给剂量、停药方案或数字目标值（follow-up 050 / 051）。",
        "作者自检 r1 / r2：P06 与 P12A 的受体、酶和分子外形只作构图示意，出片前必须用正式结构模型替换；P12B 方阵数字由网页场景按证据生成。未做独立审稿。",
        "这一版只定故事板。确认后再写讲稿、过台词审并生成整集音频预览；扣积分的视频仍由用户点击生成。",
    ],
    "sections": [
        {"id": "storyboard", "title": f"故事板（{len(spec['panels'])} 格，目标约 5 分钟）", "layout": "wide",
         "hint": "每格下方：节拍、比例尺、计划的画面来源、台词草稿", "items": items},
        {"id": "characters", "title": "人物设定", "items": [
            {"id": "C1", "label": "林 / Lin（向导）", "path": rel(ROOT / "edu_videos/tansuo/_shared/cast/lin/turnaround.png"), "kind": "image",
             "desc": "低发髻、不戴眼镜；左腕探索表，琥珀色袖口条"},
            {"id": "C2", "label": "凯 / Kai（新手）", "path": rel(ROOT / "edu_videos/tansuo/_shared/cast/kai/turnaround.png"), "kind": "image",
             "desc": "中欧混血年轻成年人，替观众提问；父亲等家人不露面"},
        ]},
    ],
}
(SB / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(items), "panels in review")
