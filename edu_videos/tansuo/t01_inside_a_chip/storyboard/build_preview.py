"""探索 t01：由 panels.json ＋ beats.md 生成两份预览数据（edu_videos follow-up 040）。
- storyboard/storyboard.json：管理站故事板页（/storyboard-preview，与短剧「影视改编」故事板同样式），按拍分场、每格一张卡；
- audio/preview_manifest.json：整集音频预览清单，接着跑 `python tools/audio_preview.py build <清单>`。
每镜时长以音频预览的 timeline.json 为准（出视频的目标时长）；有了就写进 storyboard.json 的卡片。
"""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
TOPIC = ROOT / "edu_videos/tansuo/t01_inside_a_chip"
SB = TOPIC / "storyboard"
rel = lambda p: p.relative_to(ROOT).as_posix()
spec = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
NOTE = re.compile(r"[（(][^）)]*[）)]")

# 拍 → 场：beats.md 表格「| 拍 | 比例尺 | 阿凯的问题 | 要讲清楚的意思 | 事实 | 故事板格 |」
beats = {}
for row in (TOPIC / "beats.md").read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    m = re.match(r"^(\d+)\s+(.+)$", cells[0]) if len(cells) >= 6 else None
    if m:
        beats[int(m.group(1))] = {"title": m.group(2), "scale": cells[1], "question": cells[2], "point": cells[3]}

# 转场、特效镜头留时间给画面（秒）；台词镜头用工具缺省（起势 0.6、收尾 0.8）
PACING = {"P01": {"lead": 1.2, "tail": 1.5}, "P02": {"tail": 3.0}, "P04": {"lead": 1.5}, "P05": {"tail": 1.5},
          "P06": {"lead": 1.5, "tail": 2.0}, "P09": {"lead": 1.0}, "P11": {"lead": 1.0, "tail": 1.2}, "P13": {"min": 6, "lead": 1.5},
          "P14": {"tail": 1.5}}
EXTRA_LINES = {"P13": [{"speaker": "阿凯", "text": "呜呼——！"}]}     # 「无对白或阿凯一声欢呼」：预览里先放一声欢呼


def lines_of(p):
    out = []
    for raw in p["lines"]:
        text = NOTE.sub("", raw).strip()
        m = re.match(r"^(阿凯|林工)\s*[：:]\s*(.+)$", text)
        if m:
            out.append({"speaker": m.group(1), "text": m.group(2).strip()})
    return out or EXTRA_LINES.get(p["id"], [])


tl_path = TOPIC / "audio/preview/timeline.json"
timeline = {s["id"]: s for s in json.loads(tl_path.read_text(encoding="utf-8"))["shots"]} if tl_path.exists() else {}

scenes = []
for p in spec["panels"]:
    b = p["beat"]
    if not scenes or scenes[-1]["beat"] != b:
        bt = beats.get(b, {"title": f"拍 {b}", "scale": "", "question": "", "point": ""})
        scenes.append({"beat": b, "id": f"b{b}", "location": bt["title"], "time": f"比例尺 {bt['scale']}", "purpose": bt["point"],
                       "question": bt["question"], "shots": []})
    img = SB / f"{p['id']}.png"
    tl = timeline.get(p["id"])
    scenes[-1]["shots"].append({
        "id": p["id"], "key": p["id"], "title": p["title"], "duration": tl["duration"] if tl else 0,
        "cast": ["林", "凯"], "dialogue": [{"speaker": l["speaker"], "direction": "", "text": l["text"]} for l in lines_of(p)],
        "action": f"{p['title']}。特效：{p.get('vfx') or '—'}", "blocking": "—",
        "beats": f"比例尺 {p['scale']}" + (f"；台词起点 " + "、".join(f"{x['start']:.1f}s" for x in tl["lines"]) if tl and tl["lines"] else ""),
        "camera": f"画面来源：{p['source']}",
        "image": {"path": rel(img), "mtime": int(img.stat().st_mtime)} if img.exists() else None,
        "framePrompt": rel(SB / "prompts" / f"{p['id']}.txt"), "packPrompt": "", "shotDir": rel(SB),
        "note": "；".join(x for x in p["lines"] if x.startswith("（")) or "",
    })
for s in scenes:
    s["total"] = sum(x["duration"] for x in s["shots"])
    del s["beat"]

board = {
    "title": "探索 · 芯片 t01：芯片里面到底有什么", "eyebrow": "教学视频 · 探索 · t01 故事板",
    "lang": "zh", "version": spec["version"], "updated": spec["date"],
    "notes": [
        "故事板 v4：定稿主角林 G9、凯 K1；每格经作者自检＋独立审稿 r1–r3（storyboard/reviews/）。台词是草稿，讲稿阶段按「先说后写」重说。",
        "每镜时长取自整集音频预览（本地配音按人物声样排出的时间轴），之后出视频照这个时长。",
        "待你定：P11 林的探索表画在右腕（两次重出机会已用完）；P12 叠层约为人高六成，台词倍数讲稿时按画面重算或重出。",
    ],
    "links": [{"label": "音频预览", "href": f"/episode-preview?path={rel(TOPIC)}&audio=1"},
              {"label": "审稿 r1", "path": rel(SB / "reviews/r1.md")}, {"label": "审稿 r2", "path": rel(SB / "reviews/r2.md")},
              {"label": "审稿 r3", "path": rel(SB / "reviews/r3.md")}, {"label": "节拍", "path": rel(TOPIC / "beats.md")},
              {"label": "panels.json", "path": rel(SB / "panels.json")}],
    "scenes": scenes,
}
(SB / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")

voice = lambda c: json.loads((ROOT / f"edu_videos/tansuo/_shared/cast/{c}/voice.json").read_text(encoding="utf-8"))["voices"]["zh"]
manifest = {
    "title": "探索 · 芯片 t01", "path": rel(TOPIC), "lang": "zh",
    "voices": {"林工": {k: voice("lin")[k] for k in ("reference", "reference_text")},
               "阿凯": {k: voice("kai")[k] for k in ("reference", "reference_text")}},
    "scenes": [{"id": s["id"], "title": f"{s['id'][1:]} {s['location']}", "subtitle": s["time"],
                "shots": [{"id": x["id"], "title": x["title"], "image": x["image"]["path"] if x["image"] else None,
                           "lines": [{"speaker": d["speaker"], "text": d["text"]} for d in x["dialogue"]],
                           **PACING.get(x["id"], {})} for x in s["shots"]]} for s in scenes],
    "links": [{"label": "故事板", "path": rel(SB / "storyboard.json")}, {"label": "节拍", "path": rel(TOPIC / "beats.md")}],
    "notes": [{"title": "这一版", "items": ["台词是故事板草稿，不是讲稿；讲稿定稿后按新稿重出。",
                                          "P13 原写「无对白或阿凯一声欢呼」，预览里先放一声欢呼。",
                                          "P12 的「三千多万倍」与画面比例不符（审稿 r3），讲稿时重算。"]}],
}
(TOPIC / "audio").mkdir(exist_ok=True)
(TOPIC / "audio/preview_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "场", sum(len(s["shots"]) for s in scenes), "镜；timeline", "有" if timeline else "无")
