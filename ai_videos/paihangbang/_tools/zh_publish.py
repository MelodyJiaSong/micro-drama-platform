# -*- coding: utf-8 -*-
"""大陆中文版发布稿（paihangbang follow-up 048）：抖音 / 快手 / B站 / 视频号 / 小红书。

    python ai_videos/paihangbang/_tools/zh_publish.py <ep_dir> ...      # 写 <ep>/publish.zh.md

只用 data.zh.json、assets.json 和 rank_scroll 的时间轴，不调用任何外部服务、不编新事实。
国内平台不放外链（YouTube、维基等），逐条来源只列名称；图片署名卡面已有，另附置顶评论版。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import load_episode  # noqa: E402
from rank_scroll.publish import _ts, chapters  # noqa: E402
from rank_scroll.timeline import build  # noqa: E402
from release import CHOICES  # noqa: E402

RISK_EPS = {"ep01", "ep02", "ep03", "ep04", "ep06", "ep11", "ep13", "ep15", "ep16", "ep20"}   # 英文版也出了带风险图版的期
TOPIC = {"ep01": ["摩天大楼", "建筑"], "ep02": ["登山", "地理"], "ep03": ["人工智能", "AI"], "ep04": ["动物", "野生动物"],
         "ep05": ["病毒", "医学科普"], "ep06": ["漫画", "动漫"], "ep11": ["船舶", "航运"], "ep12": ["地理", "世界地理"],
         "ep13": ["雕像", "旅行"], "ep14": ["火山", "地理"], "ep15": ["湖泊", "地理"], "ep16": ["体育场", "足球"],
         "ep17": ["河流", "地理"], "ep18": ["超跑", "汽车"], "ep19": ["旅游", "出境游"], "ep20": ["瀑布", "旅行"]}
BILI_ZONE = {"ep03": "知识 → 科技/科学科普", "ep05": "知识 → 科学科普", "ep06": "动画 → 综合 或 知识 → 社科人文",
             "ep16": "体育 → 综合 或 知识 → 科学科普", "ep18": "汽车 → 汽车知识科普"}


def zh_chapter(label: str, ep_list: bool) -> str:
    label = label.replace("Intro & ", "开场 · ").replace("Intro", "开场")
    label = re.sub(r"#(\d+)–#(\d+)", r"第\1–\2名", label)
    return {"Top 10": "前十名", "No. 1": "第1名揭晓", "Sources & credits": "数据来源与图片署名"}.get(label, label)


def credits(ep, root: Path) -> tuple[list[str], int, int]:
    ledger = json.loads((root / "assets.json").read_text(encoding="utf-8")) if (root / "assets.json").is_file() else []
    by_file = {str(x.get("file", "")).replace("\\", "/"): x for x in ledger}
    out, synth, risk = [], 0, 0
    for it in sorted(ep.items, key=lambda i: i.rank):
        for img, who in ((it.image, ""), (getattr(it, "person_image", None), "（人物像）")):
            if not img:
                continue
            e = by_file.get(str(img.relative_to(root)).replace("\\", "/"))
            if not e:
                continue
            lic = str(e.get("licence", ""))
            if lic.lower().startswith("ai-generated") or e.get("synthetic"):
                synth += 1
                lic = "AI生成插画，非实拍"
            author = str(e.get("author", "unknown")).replace("User:", "").strip()
            author = "作者不详" if author.lower() in ("", "unknown") else author
            lic = "授权不明" if lic.lower() in ("", "unknown") else lic
            label = it.name if ep.is_list else f"第{it.rank}名 {it.name}"
            out.append(f"{label}{who}：{author}（{lic}）")
    raw = json.loads((root / "data.zh.json").read_text(encoding="utf-8"))
    risk = sum(1 for r in raw["items"] if r.get("image_risk")) + sum(1 for r in raw["items"] if (r.get("person") or {}).get("image_risk"))
    return out, synth, risk


def draft(root: Path) -> str:
    key = root.name[:4]
    risk_ep = key in RISK_EPS
    choices = json.loads(CHOICES.read_text(encoding="utf-8")) if CHOICES.is_file() else {}
    # 署名与 AI 声明按要发的版本（release_choices.json，默认稳妥版）统计；按风险版统计会漏掉替代用的 AI 图（follow-up 053）
    ep, _ = load_episode(root, allow_risk_images=choices.get(root.name) == "risk", lang="zh")
    d = json.loads((root / "data.zh.json").read_text(encoding="utf-8"))
    ovp = root / "zh_publish.json"   # 列表期文案覆盖（不改 data.zh.json，免得渲染清单的哈希失配；follow-up 060）
    if ovp.is_file():
        d["zh_publish"] = {**json.loads(ovp.read_text(encoding="utf-8")), **(d.get("zh_publish") or {})}
    tl = build(ep)
    n = len(ep.items)
    top = min(ep.items, key=lambda i: i.rank)
    title = d["title"]
    dur = f"{int(tl.duration // 60)}:{int(tl.duration % 60):02d}"
    chaps = [f"{_ts(t)} {zh_chapter(lab, ep.is_list)}" for t, lab in chapters(ep, tl)]
    cred, synth, risk = credits(ep, root)
    topics = TOPIC.get(key, [])
    tag_title = "#" + re.sub(r"[^\w一-鿿]", "", title)

    if ep.is_list:
        lead = f"{title}：{n}家公司逐一看，每家都标了{ep.metric_label}（{ep.period_label}）。不是排名，按顺序介绍。"
        t_dy = f"{title}，估值和融资一次看完"
        t_bili = f"{title}：估值、融资、创始人一次看完（{ep.period_label}）"
        t_xhs = f"{n}家AI公司一次看完"
        hook = "你最看好哪一家？评论区说说。"
        # 列表期题材各不相同：data.zh.json 可用 zh_publish 覆盖上面按公司题材写的文案（paihangbang follow-up 060，ep21 大米）
        ov = d.get("zh_publish") or {}
        lead, t_dy, t_bili, t_xhs, hook = (ov.get("lead", lead), ov.get("t_dy", t_dy), ov.get("t_bili", t_bili),
                                           ov.get("t_xhs", t_xhs), ov.get("hook", hook))
    else:
        lead = f"{title}TOP{n}：按{ep.metric_label}排名（{ep.period_label}），从第{n}名一路数到第1名。"
        first = f"第1名{top.name}{top.value_display}"
        t_dy = f"{title}TOP{n}｜{first}"
        if len(t_dy) > 30:
            t_dy = f"{title}TOP{n}，第1名你猜对了吗"
        t_bili = f"{title}TOP{n}：{first}（{ep.period_label}）"
        t_xhs = f"{title}TOP{n}"[:20]
        hook = "第1名你猜对了吗？哪个最出乎你意料？评论区聊聊。"
    ins = [i.text for i in ep.insights if not re.match(r"(下一|接下来)", i.text)][:3]   # 「接下来是…」类过场句脱离画面没意义
    dy_tags = " ".join([tag_title, "#排行榜", "#涨知识", "#数据可视化"] + [f"#{t}" for t in topics])
    music = ("配乐：本频道用 Suno 原创生成的纯音乐。"
             if d.get("music_credit") or (d.get("zh_publish") or {}).get("music_credit") or (root / "render" / "_audio" / f"{root.name}_music.m4a").is_file() else "")
    ai_line = (f"说明：片中全部{synth}张图片都是 AI 生成的写实插画（卡面标「AI 生成图」），不是实拍。" if synth and synth >= n else
               f"说明：片中有{synth}张标注「AI 生成图」的插画由 AI 生成，用于没有可用实拍照片的条目，不是实拍；其余为实拍照片，"
               f"作者署名在每张卡片底部。" if synth else "说明：片中图片均为实拍照片，作者署名在每张卡片底部。")
    sourced = (d.get("zh_publish") or {}).get("sourced_line", "画面上每个数字都有出处。")
    if synth and synth >= n:
        cred = [f"全部{synth}张图片均为 AI 生成插画（Codex image_gen），非实拍。"]
    bili_desc = "\n".join([lead, sourced + hook, "", "章节："] + chaps
                          + ["", re.sub(r"[^。]*(列于下方|见下方|置顶评论)[^。]*。", "", d.get("scope_note", "")), "", d.get("source_line", ""), ai_line]
                          + ([music] if music else []) + ["国旗图案：flagcdn（公有领域）；图标：Tabler Icons（MIT）；字体：思源黑体（SIL OFL 1.1）。"])
    bili_tags = [re.sub(r"[^\w一-鿿]", "", title)[:20], "排行榜", "数据可视化", "涨知识", "科普", "盘点"] + topics
    if (d.get("zh_publish") or {}).get("tags"):
        bili_tags = [re.sub(r"[^\w一-鿿]", "", title)[:20]] + d["zh_publish"]["tags"]
        dy_tags = " ".join([tag_title] + [f"#{t}" for t in d["zh_publish"]["tags"][:4]])
    bili_tags = list(dict.fromkeys(bili_tags))[:10]

    L = [f"# 中文版发布稿 · {root.name}", "",
         "> 由 `python ai_videos/paihangbang/_tools/zh_publish.py` 生成（follow-up 048）；国内平台：抖音、快手、B站、视频号、小红书。上传由用户亲手做。",
         "> 各平台字数上限以上传页实际提示为准；本稿不含任何外链。", "",
         "## 上传文件", "",
         (f"- 视频（推荐，稳妥）：`render/{root.name}_master_zh.mp4`：版权不明的图片已换成占位卡"
          f"\n- 视频（带风险图版，即发给你预览的那版）：`render/{root.name}_master_with-risk-images_zh.mp4`：含 {risk} 张授权不明 / 保留所有权利的图片，被投诉有下架风险"
          if risk_ep else f"- 视频：`render/{root.name}_master_zh.mp4`"),
         "- 封面：`render/thumbnail_zh.png`（16:9，1280×720）",
         f"- 时长 {dur}，横屏 1920×1080 60fps", "",
         "## 抖音 / 快手", "",
         f"标题（{len(t_dy)} 字，抖音标题 ≤30 字）：", "", "```text", t_dy, "```", "",
         "作品描述：", "", "```text", "\n".join([lead, *ins, hook, "", dy_tags]), "```", "",
         "## B站", "",
         f"标题（{len(t_bili)} 字，≤80）：", "", "```text", t_bili, "```", "",
         f"分区建议：{BILI_ZONE.get(key, '知识 → 科学科普 / 人文地理（按题材选）')}；类型：自制", "",
         f"标签（{len(bili_tags)} 个，≤10）：{'、'.join(bili_tags)}", "",
         f"简介（{len(bili_desc)} 字，≤2000）：", "", "```text", bili_desc, "```", "",
         "置顶评论（图片署名）：", "", "```text", "\n".join(([] if synth and synth >= n else ["图片署名（作者，授权）："]) + cred), "```", "",
         "## 视频号", "",
         "```text", "\n".join([lead, ins[0] if ins else "", hook, "", (" ".join([tag_title] + [f"#{t}" for t in (d.get("zh_publish") or {})["tags"][:3]]) if (d.get("zh_publish") or {}).get("tags") else " ".join([tag_title, "#排行榜", "#涨知识"] + [f"#{t}" for t in topics[:1]]))]), "```", "",
         "## 小红书", "",
         f"标题（{len(t_xhs)} 字，≤20）：{t_xhs}", "",
         "```text", "\n".join([lead, "", *[f"· {s}" for s in ins], "", hook, "", dy_tags]), "```", "",
         "## 发布前检查", "",
         "- [x] 地区合规：台湾、香港、澳门均为中国的地区（五星红旗、「中国台湾」等写法、计入中国），`zh_edition.py gate` 已通过",
         ("- [ ] AI 生成内容标识：本片含 AI 生成插画（卡面已标「AI 生成图」）→ 抖音、快手、视频号、小红书勾选「内容由AI生成」声明，"
          "B站在「创作声明」里选「使用AI合成技术」（按《人工智能生成合成内容标识办法》）" if synth else
          "- [ ] AI 生成内容标识：本片无 AI 生成画面，不必勾选 AI 声明"),
         "- [ ] 简介、评论不放外链（YouTube、维基百科等）",
         "- [ ] 封面用 `render/thumbnail_zh.png`；抖音、视频号可另设竖版封面（3:4），需要时让我出",
         "- [ ] 本片为横屏；抖音、快手、视频号横屏可直接发，竖屏版目前没有",
         *(["- [ ] 配乐为本频道 Suno 生成曲（同英文版）；若被平台识别为他人作品，用本剧 request_log.md 的生成记录申诉"] if music else []),
         "- [ ] B站：发布后把「置顶评论（图片署名）」发在评论区并置顶", ""]
    return "\n".join(L)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    for a in sys.argv[1:]:
        root = Path(a).resolve()
        out = root / "publish.zh.md"
        out.write_text(draft(root), encoding="utf-8")
        print(out.relative_to(REPO))


if __name__ == "__main__":
    main()
