import json
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
SB = ROOT / "edu_videos/tansuo/t01_inside_a_chip/storyboard"
spec = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
rel = lambda p: p.relative_to(ROOT).as_posix()

items = []
for p in spec["panels"]:
    img = SB / f"{p['id']}.png"
    if not img.exists():
        continue
    desc = f"拍 {p['beat']} · 比例尺 {p['scale']} · {p['source']}\n特效：{p.get('vfx', '—')}\n" + "\n".join(p["lines"])
    items.append({"id": p["id"], "label": p["title"], "path": rel(img), "kind": "image", "desc": desc})

chars = ROOT / "edu_videos/tansuo/_shared/characters"
styles = ROOT / "edu_videos/tansuo/_shared/style_options"
review = {
    "title": "芯片之旅 t01 · 故事板 v4（电影写实 · 林 G9 与凯 K1）",
    "character": "edu_videos/tansuo t01_inside_a_chip",
    "updated": spec["date"],
    "notes": [
        "说编号提意见，例如「P08 光波再大一点」「C2 阿凯换件外套」「选 S3」。",
        "画面里的文字、比例尺读数、真实性角标都在后期叠加，AI 图里一律不画字。",
        "台词是草稿：讲稿阶段按 edu「先说后写」重说；带数字的句子等事实核查 r1 回来再定。",
        "结构画面最终用 Blender 按研究档案尺寸建模，故事板只定构图、走位和情绪。",
        "v4 用定稿主角（林 = G9、凯 = K1）整集重出，经作者自检＋独立审稿（storyboard/reviews/）修改；淘汰图在 storyboard/rejected/，v3（林 G1）在 storyboard/v3_G1/。",
        "生成视频前的预览：这一版只定构图、走位、情绪和特效方向；确认后再逐镜决定 Blender / Seedance 怎么出。",
        "待你定：P11 林的探索表画在了右腕（两次重出机会已用完，审稿 r3 判必改）——可以再重出一次，或故事板先放行、出片时再修；P12 叠层约为人高的六成，台词倍数讲稿时按画面重算或重出。审稿记录：storyboard/reviews/r1.md、r2.md、r3.md。",
    ],
    "sections": [
        {"id": "storyboard", "title": "故事板（14 格，约 4 分 30 秒）", "layout": "wide",
         "hint": "每格下方：节拍、比例尺、计划的画面来源、台词草稿", "items": items},
        {"id": "characters", "title": "人物设定", "items": [
            {"id": "C1", "label": "林 / Lin（向导）", "path": rel(ROOT / "edu_videos/tansuo/_shared/cast/lin/turnaround.png"), "kind": "image",
             "desc": "探索向导（选角 G9：低发髻、不戴眼镜）；左腕「探索表」，表盘比例尺就是全片比例尺"},
            {"id": "C2", "label": "凯 / Kai（新手）", "path": rel(ROOT / "edu_videos/tansuo/_shared/cast/kai/turnaround.png"), "kind": "image",
             "desc": "中欧混血年轻人（选角 K1），替观众提问；爱掏手机拍"},
        ]},
        {"id": "style", "title": "画风选项（同一场景三种画法）", "hint": "已选 S2 电影写实（2026-11-14）", "items": [
            {"id": "S1", "label": "频道陶土", "path": rel(styles / "A_clay.png"), "kind": "image",
             "desc": "沿用频道 I1 哑光陶土：最统一，但材料分不清、铜线像塑料"},
            {"id": "S2", "label": "电影感写实（已选）", "path": rel(styles / "B_cinematic.png"), "kind": "image",
             "desc": "像纪录片：震撼，但暗、重，人物与结构抢画面，AI 视频难稳定"},
            {"id": "S3", "label": "风格化 3D 动画", "path": rel(styles / "C_stylized.png"), "kind": "image",
             "desc": "材料按颜色编码（铜、硅、介质、金属），明亮好读，人物亲和"},
        ]},
    ],
}
(SB / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(items), "panels in review")
