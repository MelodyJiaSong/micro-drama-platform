"""Generate storyboard and optional audio-preview manifests from panels.json + beats.md."""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
TOPIC = ROOT / "edu_videos/tansuo/t11_inside_an_artery"
SB = TOPIC / "storyboard"
rel = lambda p: p.relative_to(ROOT).as_posix()
spec = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
NOTE = re.compile(r"[（(][^）)]*[）)]")

beats = {}
for row in (TOPIC / "beats.md").read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    match = re.match(r"^(\d+)\s+(.+)$", cells[0]) if len(cells) >= 6 else None
    if match:
        beats[int(match.group(1))] = {"title": match.group(2), "scale": cells[1], "question": cells[2], "point": cells[3]}


def lines_of(panel):
    out = []
    for raw in panel["lines"]:
        text = NOTE.sub("", raw).strip()
        match = re.match(r"^(阿凯|林)\s*[：:]\s*(.+)$", text)
        if match:
            out.append({"speaker": match.group(1), "text": match.group(2).strip()})
    return out


tl_path = TOPIC / "audio/preview/timeline.json"
timeline = {s["id"]: s for s in json.loads(tl_path.read_text(encoding="utf-8"))["shots"]} if tl_path.exists() else {}
scenes = []
for panel in spec["panels"]:
    beat = panel["beat"]
    if not scenes or scenes[-1]["beat"] != beat:
        bt = beats.get(beat, {"title": f"拍 {beat}", "scale": "", "question": "", "point": ""})
        scenes.append({"beat": beat, "id": f"b{beat}", "location": bt["title"], "time": f"比例尺 {bt['scale']}",
                       "purpose": bt["point"], "question": bt["question"], "shots": []})
    image = SB / f"{panel['id']}.png"
    tl = timeline.get(panel["id"])
    scenes[-1]["shots"].append({
        "id": panel["id"], "key": panel["id"], "title": panel["title"], "duration": tl["duration"] if tl else 0,
        "cast": ["林", "凯"], "dialogue": [{"speaker": line["speaker"], "direction": "", "text": line["text"]} for line in lines_of(panel)],
        "action": f"{panel['title']}。特效：{panel.get('vfx') or '—'}", "blocking": "—",
        "beats": f"比例尺 {panel['scale']}" + (f"；台词起点 " + "、".join(f"{x['start']:.1f}s" for x in tl["lines"]) if tl and tl["lines"] else ""),
        "camera": f"画面来源：{panel['source']}",
        "image": {"path": rel(image), "mtime": int(image.stat().st_mtime)} if image.exists() else None,
        "framePrompt": rel(SB / "prompts" / f"{panel['id']}.txt"), "packPrompt": "", "shotDir": rel(SB), "note": "",
    })
for scene in scenes:
    scene["total"] = sum(shot["duration"] for shot in scene["shots"])
    del scene["beat"]

board = {
    "title": "探索 · 血脂 t11：血管里的小船", "eyebrow": "教学视频 · 探索 · t11 故事板",
    "lang": "zh", "version": spec["version"], "updated": spec["date"],
    "notes": [
        f"故事板 {spec['version']}：15 拍各一格，只定构图、走位、情绪和特效方向；台词是草稿，讲稿阶段按「先说后写」重说。",
        "全片只有林和凯；父亲不露面，只通过台词和出院单道具出现。",
        "全季不做任何药物推荐；本期加入他汀机制、血脂关系、降 LDL 结局证据与「治本 / 治标」解释，但不给剂量、停药方案或数字目标值（follow-up 050 / 051）。",
        "分子颜色均为编码色，比例尺、医学名词、数字与真实性角标后期叠加；结构镜头最终以 Blender 按研究档案建模。",
    ],
    "links": [{"label": "节拍", "path": rel(TOPIC / "beats.md")},
              {"label": "研究档案", "path": rel(TOPIC / "research/dossier.md")},
              {"label": "事实核查 r1", "path": rel(TOPIC / "research/factcheck_r1.md")},
              {"label": "作者自检 r1", "path": rel(SB / "reviews/self_r1.md")},
              {"label": "作者自检 r2", "path": rel(SB / "reviews/self_r2.md")},
              {"label": "panels.json", "path": rel(SB / "panels.json")}],
    "scenes": scenes,
}
(SB / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")

voice = lambda c: json.loads((ROOT / f"edu_videos/tansuo/_shared/cast/{c}/voice.json").read_text(encoding="utf-8"))["voices"]["zh"]
manifest = {
    "title": "探索 · 血脂 t11", "path": rel(TOPIC), "lang": "zh",
    "voices": {"林": {k: voice("lin")[k] for k in ("reference", "reference_text")},
               "阿凯": {k: voice("kai")[k] for k in ("reference", "reference_text")}},
    "scenes": [{"id": s["id"], "title": f"{s['id'][1:]} {s['location']}", "subtitle": s["time"],
                "shots": [{"id": x["id"], "title": x["title"], "image": x["image"]["path"] if x["image"] else None,
                           "lines": [{"speaker": d["speaker"], "text": d["text"]} for d in x["dialogue"]]} for x in s["shots"]]} for s in scenes],
    "links": [{"label": "故事板", "path": rel(SB / "storyboard.json")}, {"label": "节拍", "path": rel(TOPIC / "beats.md")}],
    "notes": [{"title": "这一版", "items": ["台词是故事板草稿，不是讲稿；用户确认故事板并走完讲稿审查后才生成整集音频预览。"]}],
}
(TOPIC / "audio").mkdir(exist_ok=True)
(TOPIC / "audio/preview_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "场", sum(len(s["shots"]) for s in scenes), "镜；timeline", "有" if timeline else "无")
