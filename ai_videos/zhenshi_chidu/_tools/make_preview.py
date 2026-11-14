"""审片页数据：写 `{集}/preview.json`（管理 UI 单集预览页的成片模式，follow-up ai_video_management §328）
并从成片抽每段的缩略图到 `_build/preview/`。

    python ai_videos/zhenshi_chidu/_tools/make_preview.py <集目录>
    打开 http://127.0.0.1:5174/episode-preview?path=ai_videos/zhenshi_chidu/episodes/<集目录名>

时间换算与 compose.py 同序：钩子 → 阵列（含片头卡、洞察卡叠加）→ 合影 → 来源卡。
阵列第 f 帧（1 起）在成片的 HOOK_S + (f − 1) / fps 秒。每只动物一段：从上一只的静止段结束（镜头开始移动）到本只静止段结束（洞察卡叠在静止段上）。
逐只备注写在 ITEM_NOTES（本集审片要看的点，来自 review_for_user.md 与 qc.md）。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HOOK_S = 7.0

ZH = {
    "Giraffe": "长颈鹿", "African Bush Elephant": "非洲草原象", "Asian Elephant": "亚洲象", "African Forest Elephant": "非洲森林象",
    "Moose": "驼鹿", "Wild Yak": "野牦牛", "Gaur": "印度野牛", "White Rhinoceros": "白犀", "Indian Rhinoceros": "印度犀",
    "Wild Water Buffalo": "野水牛", "American Bison": "美洲野牛", "European Bison": "欧洲野牛", "Giant Eland": "大羚羊（德氏大羚羊）",
    "African Buffalo": "非洲水牛", "Javan Rhinoceros": "爪哇犀", "Banteng": "爪哇野牛", "Common Eland": "普通大羚羊",
    "Hippopotamus": "河马", "Black Rhinoceros": "黑犀", "Elk (Wapiti)": "马鹿（北美马鹿）", "Grévy's Zebra": "细纹斑马",
    "Polar Bear": "北极熊", "Muskox": "麝牛", "Mountain Zebra": "山斑马", "Kiang": "藏野驴", "Brown Bear": "棕熊",
    "Plains Zebra": "平原斑马", "Sumatran Rhinoceros": "苏门答腊犀", "Bongo": "紫羚（邦戈羚）", "Takin": "扭角羚",
}

# 本集逐只要看的点（flag：note = 有备注，ok = 无备注）
ITEM_NOTES = {
    "ep01_largest_land_animals": {
        "Giraffe": "肩线看图定（背线转入颈部处）；头顶约 4.6 m，在 HMW 4.5–6.0 m（雌雄混合）内。",
        "Grévy's Zebra": "肩线看图定（鬃毛起点）；自动列落在颈部鬃毛上。",
        "African Bush Elephant": "剪影长含前伸象牙与尾。",
        "Asian Elephant": "剪影长含象牙与尾，长 ÷ 头体长 1.24。",
        "Gaur": "1.88 m 是 Nowak 1999 经维基百科转引；AWCSG 范围 1.5–2.2 m，描述里写明。",
        "American Bison": "第二张洞察卡（2:22）在它身下的地面区，卡上文字是「从下一只起」。",
        "Polar Bear": "图偏长（剪影长 ÷ 头体长 1.22，头前伸）；1.45 m 是雌雄混合，公熊约 1.6 m。",
        "Muskox": "估计值（≈，资料分歧）。",
        "Brown Bear": "估计值（≈，按堪察加实测公熊换算）。",
        "Elk (Wapiti)": "肩线取躯干上沿，鹿角不计。",
        "Moose": "肩线取肩峰上沿，鹿角不计。",
    },
}


def t_of(frame: int, fps: int) -> float:
    return round(HOOK_S + (frame - 1) / fps, 2)


def thumb(master: Path, t: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(master), "-frames:v", "1",
                    "-vf", "scale=480:-2", "-q:v", "4", str(out)], check=True)


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    rel = lambda p: p.resolve().relative_to(REPO).as_posix()  # noqa: E731
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    tl = json.loads((ep / "_build/timeline.json").read_text(encoding="utf-8"))
    fps = tl["fps"]
    by_name = {it["name"]: it for it in data["items"]}
    notes = ITEM_NOTES.get(ep.name, {})
    master = ep / "render/ep_master.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(master)]))
    lineup_end = t_of(tl["segments"]["lineup"][1] + 1, fps)
    group_end = lineup_end + (tl["segments"]["group"][1] - tl["segments"]["group"][0] + 1) / fps
    tdir = ep / "_build/preview"

    items = [{"t": 0, "end": HOOK_S, "title": "钩子：夕阳剪影", "subtitle": "非洲草原象与长颈鹿，各配一个 1.75 m 人",
              "chapter": "intro", "thumb_t": 4.0, "flag": "ok"}]
    prev_end = HOOK_S
    for row in tl["items"]:
        it = by_name[row["name"]]
        end = t_of(row["static"][1] + 1, fps)   # 静止段含叠在它上面的洞察卡
        mid = t_of((row["label"][0] + row["label"][1]) // 2, fps)
        rank = f"{'=' if it['tied'] else '#'}{it['rank']}"
        chapter = "top5" if it["rank"] <= 5 else "top10" if it["rank"] <= 10 else "mid" if it["rank"] <= 20 else "intro"
        items.append({
            "t": prev_end, "end": end, "title": f"{rank} {ZH.get(it['name'], it['name'])}",
            "subtitle": f"{it['name']} · 肩高 {it['value_display']}（{it['secondary_display']}）· {it['basis'].split('· ')[-1]}",
            "badge": ("AI IMAGE" if it.get("cutout") else "AI MODEL") if it["model"].get("ai_model") else "", "chapter": chapter,
            "note": notes.get(it["name"], ""), "flag": "note" if it["name"] in notes else "ok",
            "detail": f"出处：{it['source_short']}", "thumb_t": mid,
        })
        prev_end = end
    items.append({"t": lineup_end, "end": group_end, "title": "全体合影", "chapter": "end", "thumb_t": lineup_end + 6,
                  "subtitle": "五排站位（小的在前、大的在后），平视长焦，人在最左；金合欢与草原作背景",
                  "note": "长焦远机位（约 600 m），前后排透视差 ≤ 约 2%；前排挡住后排的脚。", "flag": "note"})
    items.append({"t": group_end, "end": round(dur, 2), "title": "来源与署名卡", "chapter": "end", "thumb_t": group_end + 3,
                  "subtitle": "15 s，兼片尾推荐位（End screen）", "flag": "ok"})
    for i, x in enumerate(items):
        out = tdir / f"{i:02d}.jpg"
        thumb(master, x.pop("thumb_t"), out)
        x["image"] = rel(out)

    def at(frame: int) -> float:
        return t_of(frame, fps)
    marks = [{"t": at(tl["title"][0]), "label": "片头卡"}] + [
        {"t": at(s["frames"][0]), "label": f"洞察卡 {s['index'] + 1}：{data['insights'][s['index']]['text']}"} for s in tl["insights"]]

    doc = lambda name: rel(ep / name)  # noqa: E731
    preview = {
        "title": "真实尺度 EP01 · 最大的 30 种陆地动物（按肩高）",
        "tagline": "第 3 版：30 只 AI 写实图抠像按肩线精确缩放，站在精细草原场景里（远景板 + 中景金合欢 + 3D 枯草与石块）；"
                   "每只旁边站一个 1.75 m 的人（同样是 AI 图），黄线标出量肩高的位置；最后全体合影与来源卡。比例机检 30/30。",
        "video": rel(master), "duration": round(dur, 2),
        "chapters": [
            {"id": "intro", "title": "钩子 · #30 扭角羚 – #21 细纹斑马", "t": 0},
            {"id": "mid", "title": "=19 马鹿 – #11 美洲野牛", "t": next(x["t"] for x in items if x.get("chapter") == "mid")},
            {"id": "top10", "title": "前十", "t": next(x["t"] for x in items if x.get("chapter") == "top10")},
            {"id": "top5", "title": "前五与冠军", "t": next(x["t"] for x in items if x.get("chapter") == "top5")},
            {"id": "end", "title": "全体合影与来源", "t": lineup_end},
        ],
        "items": items, "marks": marks,
        "images": [{"path": doc("render/thumb_A.jpg"), "caption": "封面 A：冠军 + 人（推荐）"},
                   {"path": doc("render/thumb_B.jpg"), "caption": "封面 B：全体合影"}]
                  + [{"path": doc(f"render/thumb_{k}_zh.jpg"), "caption": f"中文版封面 {k}"} for k in "AB"
                     if (ep / f"render/thumb_{k}_zh.jpg").exists()],
        "links": [{"label": "审核说明 review_for_user.md", "path": doc("review_for_user.md")}]
                 + ([{"label": "中文版成片 ep_master_zh.mp4（画面同英文版，卡片中文）", "path": doc("render/ep_master_zh.mp4")}]
                    if (ep / "render/ep_master_zh.mp4").exists() else []) + [
                  {"label": "发布稿 publish.md", "path": doc("publish.md")},
                  {"label": "独立审片 qc.md", "path": doc("qc.md")},
                  {"label": "出处 sources.md", "path": doc("sources.md")},
                  {"label": "许可 licenses.csv", "path": doc("licenses.csv")},
                  {"label": "比例机检 scale_check.json", "path": doc("scale_check.json")}],
        "notes": [
            {"title": "请你拍板", "items": [
                "第 3 版画面：精细草原场景 + AI 写实动物与人（卡上标 AI IMAGE），镜头只做横移和推拉。能否接受？",
                "标题：英文「The 30 Largest Land Animals Ranked by Height | True Scale Size Comparison」；中文「最大的 30 种陆地动物按肩高排名｜真实比例大小对比」。",
                "中文版发在哪（单独的中文频道或平台，还是同频道另发一条）。两版的发布稿都在 publish.md。",
                "封面选 A 还是 B（上面两张）。",
                "YouTube「合成内容」申报：建议勾选。上传由你亲手做。"]},
            {"title": "已知问题", "items": [
                "动物是平面，不投真实影子，只有蹄下柔和的接触阴影；前景草为了不挡蹄子只能矮。",
                "合影：后排大象偏灰（远距离空气透视）；钩子地面是平涂灰褐（机位贴地，铺草会挡住剪影脚底）。",
                "亚洲象背顶比黄线高约 0.1 m（背顶高于肩峰本属正常）；北极熊图偏长。",
                "钩子仍是灰白天空的日落剪影；配乐前十开头有约 2 dB 回落。"]},
            {"title": "这一版怎么做的", "items": [
                "Codex 侧面图 → rembg（isnet，Apache-2.0）抠像 → 在剪影上定肩线（2 只人工）→ 米/像素 = 肩高 ÷ 肩线像素高。",
                "135 mm 平视长焦，f/2.8 景深；人与动物在同一纵深，比例不受透视影响。",
                "环境四层：Codex 远景板（5 km 外）→ Codex 金合欢 / 灌木抠像（40–700 m，有视差）→ Poly Haven CC0 3D 草与石块（前景草按与镜头的距离限高，挡不到蹄子）→ 动物。",
                "第 6 轮独立审片后修了 4 处再全片重渲：平面投影造成的细黑线、下 1/3 像泥地、合影的人难找、标题卡和洞察卡盖住动物；第 7 轮后又修了合影前景的台阶与色调；第 8 轮复核可交付，按建议把合影取景居中到「人 + 全体」、封面 B 保留人并加标。",
                "钩子剪影用 Poly Haven「Plains Sunset」HDRI；光照仍用 Mpumalanga Veld HDRI + 左前方太阳。",
                "许可：42 条全在白名单（自产 AI 图、CC0 环境与模型、Inter OFL）。第 1 版 3D 成片备份在 _build/v1_3d/。"]},
        ],
    }
    (ep / "preview.json").write_text(json.dumps(preview, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(items), "items;", ep / "preview.json")


if __name__ == "__main__":
    main()
