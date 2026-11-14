"""排行榜各期上传：YouTube 自动传成私享，抖音、TikTok 自动填表；公开与「发布」都由用户亲手点（follow-up 053 / 066）。

    python ai_videos/paihangbang/_tools/upload.py status                 # 各期上传状态
    python ai_videos/paihangbang/_tools/upload.py youtube ep12 [--dry-run] [--publish-at 2026-11-08T12:00:00Z]
    python ai_videos/paihangbang/_tools/upload.py comments ep12          # 在 Studio 公开后：发 Comment 1，其余回复在它下面
    python ai_videos/paihangbang/_tools/upload.py douyin ep12 [--cover 2] [--dry-run]
    python ai_videos/paihangbang/_tools/upload.py tiktok ep12 [--dry-run] [--no-cover] [--rehearse]   # 英文版
    python ai_videos/paihangbang/_tools/upload.py tiktok-all [--rehearse]   # 所有已收录、未发布的期逐期填，每期等你点 Post

- 文件取 `release/<期>/`（先跑 release.py 收录），文案取各期 `publish.md`（英文）/ `publish.zh.md` 的「抖音 / 快手」节。
- 合成内容声明按 publish.md 清单里「Altered or synthetic content … 选 Yes/No」，抖音 AI 声明按 publish.zh.md「AI 生成内容标识」。
- 记录写 `episodes/<期>/uploads.json`（片子 sha256、video id、评论 id）。上传中途断掉的期标为「结果未知」，
  不自动重传：先去 YouTube Studio 看有没有这条私享视频，确认没有再加 --retry-unknown。
- TikTok 说明：publish.md 有「## TikTok」节就照用其代码块（末行 #话题 拆成话题）；没有就由 Description 首行 + 固定引导语 + 话题自动拼。
- 首次使用：`python tools/youtube_upload.py auth`、`python tools/douyin_upload.py login`、`python tools/tiktok_upload.py login`。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SERIES = Path(__file__).resolve().parents[1]
REPO = SERIES.parents[1]
EPS = SERIES / "episodes"
RELEASE = SERIES / "release"
RECORD = "uploads.json"
sys.path.insert(0, str(REPO))

from tools.douyin_upload import DouyinJob  # noqa: E402
from tools.tiktok_upload import TikTokJob  # noqa: E402
from tools.youtube_upload import VideoJob  # noqa: E402

CODE_BLOCK = re.compile(r"```[a-z]*\n(.*?)\n```", re.S)
SYNTHETIC = re.compile(r"(?:选|勾选)\s*\**\s*(Yes|No)\b")


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def episode(arg: str) -> Path:
    hits = [d for d in sorted(EPS.iterdir()) if d.is_dir() and (d.name == arg or d.name.startswith(arg + "_"))]
    if len(hits) != 1:
        raise SystemExit(f"找不到唯一的期：{arg}（匹配 {[d.name for d in hits]}）")
    return hits[0]


def sections(md: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        out[head.strip()] = body
    return out


def section(secs: dict[str, str], prefix: str, optional: bool = False) -> str:
    hits = [v for k, v in secs.items() if k.startswith(prefix)]
    if optional and not hits:
        return ""
    if len(hits) != 1:
        raise SystemExit(f"publish 稿里「## {prefix}」节有 {len(hits)} 个")
    return hits[0]


def first_line(body: str) -> str:
    return next(line.strip() for line in body.splitlines() if line.strip())


def code_blocks(body: str) -> list[str]:
    return CODE_BLOCK.findall(body)


def tags(body: str) -> list[str]:
    text = (code_blocks(body) or [body.strip()])[0]
    line = text.strip().splitlines()[0] if text.strip() else ""
    return [t.strip() for t in line.split(",") if t.strip()]


def release_has_ai(ep: Path) -> bool:
    """按 release_choices.json 选定的版本（默认稳妥版）实际出现在片子里的图，判断有没有 AI 生成图。"""
    sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
    from rank_scroll.contract import load_episode
    from release import CHOICES
    from zh_publish import credits
    choices = json.loads(CHOICES.read_text(encoding="utf-8")) if CHOICES.is_file() else {}
    shown, _ = load_episode(ep, allow_risk_images=choices.get(ep.name) == "risk")
    return credits(shown, ep)[1] > 0


def image_gate(ep: Path) -> list[str]:
    """配图硬闸门（follow-up 054，bible §4）：要发的版本每张卡都有通过独立审图的高质量图，否则不传。"""
    from tile_gate import gate
    r = gate(ep)
    if r["ok"]:
        return []
    return [f"配图闸门未过（{r['variant']}）：{len({f[0] for f in r['fails']})} 个名次缺图或不合格、{len(r['pending'])} 张待独立审图、"
            f"合同错误 {len(r['errors'])} 条；详情 python ai_videos/paihangbang/_tools/tile_gate.py check {ep.name}"]


def check_declaration(ep: Path, declared: bool, where: str) -> bool:
    truth = release_has_ai(ep)
    if declared != truth:
        raise SystemExit(f"{where}写的 AI 声明是「{'有' if declared else '无'}」，但要发的版本实际{'有' if truth else '没有'} AI 图；"
                         "先改发布稿（英文 python -m rank_scroll publish，中文 zh_publish.py）再上传")
    return truth


def synthetic_flag(md: str) -> bool:
    answers = {m for line in md.splitlines() if "synthetic content" in line for m in SYNTHETIC.findall(line)}
    if len(answers) != 1:
        raise SystemExit(f"publish.md 里合成内容声明不唯一或缺失：{answers or '无'}；先补清单再上传")
    return answers == {"Yes"}


def youtube_job(ep: Path, publish_at: str | None) -> VideoJob:
    md = (ep / "publish.md").read_text(encoding="utf-8")
    secs = sections(md)
    numbered = {int(m.group(1)): v for k, v in secs.items() if (m := re.match(r"Comment (\d+)", k))}
    comments = [code_blocks(numbered[n])[0] for n in sorted(numbered)]
    return VideoJob(
        video=RELEASE / ep.name / f"{ep.name}_en.mp4",
        title=first_line(section(secs, "Title")),
        description=code_blocks(section(secs, "Description"))[0],
        tags=tags(section(secs, "Tags", optional=True)),
        synthetic=check_declaration(ep, synthetic_flag(md), "publish.md"),
        thumbnail=RELEASE / ep.name / "thumbnail_en.png",
        publish_at=publish_at,
        comments=comments,
    )


def douyin_job(ep: Path, cover: int) -> DouyinJob:
    md = (ep / "publish.zh.md").read_text(encoding="utf-8")
    secs = sections(md)
    blocks = code_blocks(section(secs, "抖音"))
    if len(blocks) < 2:
        raise SystemExit("publish.zh.md「抖音 / 快手」节缺标题或作品描述代码块")
    lines = blocks[1].rstrip().splitlines()
    topics: list[str] = []
    while lines and re.fullmatch(r"(#\S+\s*)+", lines[-1].strip()):
        topics = [t.lstrip("#") for t in lines.pop().split()] + topics
    ai_lines = [line for line in md.splitlines() if "AI 生成内容标识" in line]
    if len(ai_lines) != 1 or not re.search(r"本片(含|无)", ai_lines[0]):
        raise SystemExit("publish.zh.md 的「AI 生成内容标识」一行缺失或写法不明")
    covers = RELEASE / ep.name / "covers_zh"
    return DouyinJob(
        video=RELEASE / ep.name / f"{ep.name}_zh.mp4",
        title=blocks[0].strip(),
        description="\n".join(lines).rstrip(),
        topics=topics,
        ai_generated=check_declaration(ep, "本片含" in ai_lines[0], "publish.zh.md"),
        cover_vertical=covers / f"cover_zh_{cover}_3x4.png",
        cover_horizontal=covers / f"cover_zh_{cover}_4x3.png",
    )


TIKTOK_TAGS = ["datavisualization", "facts", "learnontiktok"]   # 排名类另加 ranking
TIKTOK_TOPIC_TAGS = 3   # 从 Tags 节取前几个做话题


def split_hashtags(text: str) -> tuple[str, list[str]]:
    lines = text.rstrip().splitlines()
    tagz: list[str] = []
    while lines and re.fullmatch(r"(#\S+\s*)+", lines[-1].strip()):
        tagz = [t.lstrip("#") for t in lines.pop().split()] + tagz
    return "\n".join(lines).rstrip(), tagz


def tiktok_job(ep: Path, cover: bool) -> TikTokJob:
    md = (ep / "publish.md").read_text(encoding="utf-8")
    secs = sections(md)
    own = section(secs, "TikTok", optional=True)
    ai = check_declaration(ep, synthetic_flag(md), "publish.md")
    if own:
        caption, hashtags = split_hashtags(code_blocks(own)[0])
    else:
        lead = first_line(code_blocks(section(secs, "Description"))[0])
        lines = [lead, "Every number on screen is sourced; photo credits are on each card."]
        if ai:
            lines.append("Some images are AI-generated illustrations, labelled on their cards.")
        lines += ["", "Which one surprised you? Tell us in the comments!"]
        caption = "\n".join(lines)
        title = first_line(section(secs, "Title"))
        topic = [re.sub(r"\W", "", t.lower()) for t in tags(section(secs, "Tags", optional=True))]
        if not topic:   # 没有 Tags 节：取标题主体，如「Deepest Lakes in the World | …」→ deepestlakes
            head = re.sub(r"\b(top \d+|in the world)\b", "", re.split(r"[|(]", title)[0], flags=re.I)
            topic = [re.sub(r"\W", "", head.lower())]
        ranked = bool(re.search(r"\b(top \d+|ranked)\b", title, re.I))
        hashtags = list(dict.fromkeys([t for t in topic if t][:TIKTOK_TOPIC_TAGS]
                                      + (["ranking"] if ranked else []) + TIKTOK_TAGS))
    thumb = RELEASE / ep.name / "thumbnail_en.png"
    return TikTokJob(
        video=RELEASE / ep.name / f"{ep.name}_en.mp4",
        caption=caption,
        hashtags=hashtags,
        ai_generated=ai,
        cover=tiktok_cover(ep, thumb) if cover and thumb.is_file() else None,
    )


def tiktok_cover(ep: Path, thumb: Path) -> Path:
    """TikTok 封面按竖版 3:4 显示，直接传 16:9 缩略图会被居中裁掉标题两端（2026-11-07 实测）。
    改为 3:4 画布：缩略图完整居中，上下用同图放大、模糊、压暗铺满。只做几何变换，不加新内容。"""
    from PIL import Image, ImageEnhance, ImageFilter
    out = ep / "_build" / "tiktok" / "cover_3x4.png"
    if out.is_file() and out.stat().st_mtime >= thumb.stat().st_mtime:
        return out
    W, H = 1080, 1440
    src = Image.open(thumb).convert("RGB")
    k = max(W / src.width, H / src.height)
    bg = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
    left, top = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    fg = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
    bg.paste(fg, (0, (H - fg.height) // 2))
    out.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out)
    return out


def load(ep: Path) -> dict[str, Any]:
    p = ep / RECORD
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def save(ep: Path, rec: dict[str, Any]) -> None:
    (ep / RECORD).write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def show(job: VideoJob | DouyinJob | TikTokJob) -> None:
    for k, v in vars(job).items():
        if k == "comments":
            v = [f"Comment {i}：{len(c)} 字符" for i, c in enumerate(v, 1)]
        print(f"[{k}]\n{v}\n")


def cmd_youtube(ep: Path, dry: bool, publish_at: str | None, retry_unknown: bool) -> None:
    import tools.youtube_upload as yu
    job = youtube_job(ep, publish_at)
    problems = job.problems() + image_gate(ep)
    if dry or problems:
        show(job)
        if problems:
            raise SystemExit("不能上传：\n" + "\n".join(problems))
        print("dry-run：校验通过，未上传")
        return
    rec = load(ep)
    yt = rec.get("youtube", {})
    if yt.get("state") == "uploaded":
        raise SystemExit(f"已上传过：{yt['url']}；要换片请先在 Studio 删掉旧的，再删 {ep / RECORD} 里的 youtube 记录")
    if yt.get("state") == "uploading" and not retry_unknown:
        raise SystemExit(f"上次上传 {yt['started']} 中断，结果未知。先到 YouTube Studio 查有没有这条私享视频；"
                         "确认没有再加 --retry-unknown")
    digest = sha256(job.video)
    rec["youtube"] = {"state": "uploading", "started": now(), "video": job.video.name, "sha256": digest,
                      "title": job.title, "synthetic": job.synthetic, "publish_at": publish_at}
    save(ep, rec)
    print(f"上传 {job.video.name}（私享）…")
    vid = yu.upload(job)
    rec["youtube"].update(state="uploaded", video_id=vid, url=f"https://youtu.be/{vid}", uploaded=now(),
                          studio=f"https://studio.youtube.com/video/{vid}/edit", comments=[])
    save(ep, rec)
    print(f"已上传：{rec['youtube']['url']}")
    if job.thumbnail:
        try:
            yu.set_thumbnail(vid, job.thumbnail)
            rec["youtube"]["thumbnail"] = job.thumbnail.name
        except yu.HttpError as e:
            rec["youtube"]["thumbnail"] = f"失败：{e.reason}"
            print(f"  封面没传上（{e.reason}；频道未验证手机号时 YouTube 不许自定义封面），请在 Studio 手动传 {job.thumbnail}")
        save(ep, rec)
    print(f"下一步：在 Studio 检查后亲手公开 {rec['youtube']['studio']}；公开后运行 comments {ep.name.split('_')[0]}")


def cmd_comments(ep: Path) -> None:
    import tools.youtube_upload as yu
    rec = load(ep)
    yt = rec.get("youtube", {})
    if yt.get("state") != "uploaded":
        raise SystemExit("这一期还没上传到 YouTube")
    state = yu.privacy(yt["video_id"])
    if state not in ("public", "unlisted"):
        raise SystemExit(f"视频现在是 {state}，先在 Studio 公开再发评论")
    job = youtube_job(ep, None)
    done: list[str] = yt.setdefault("comments", [])

    def posted(_: str) -> None:
        save(ep, rec)

    yu.post_comments(yt["video_id"], job.comments, done, posted)
    print(f"评论已发齐。请在 Studio 把 Comment 1 置顶：{yt['url']}")


def cmd_douyin(ep: Path, dry: bool, cover: int, again: bool) -> None:
    job = douyin_job(ep, cover)
    problems = job.problems() + image_gate(ep)
    if dry or problems:
        show(job)
        if problems:
            raise SystemExit("不能填表：\n" + "\n".join(problems))
        print("dry-run：校验通过，未打开浏览器")
        return
    rec = load(ep)
    if rec.get("douyin", {}).get("state") == "published" and not again:
        raise SystemExit("抖音已发布过这一期；确要再发加 --again")
    print(f"作品描述（自动填写失败时手动粘贴）：\n{job.description}\n{' '.join('#' + t for t in job.topics)}\n")
    from tools.douyin_upload import fill
    rec["douyin"] = {"state": "filling", "started": now(), "video": job.video.name, "sha256": sha256(job.video),
                     "title": job.title, "cover": cover, "ai_generated": job.ai_generated}
    save(ep, rec)
    published = fill(job)
    rec["douyin"].update(state="published" if published else "filled", ended=now())
    save(ep, rec)
    print("已记为已发布" if published else "未检测到发布（若你其实发了，到作品管理页确认后可手动改 uploads.json）")


TIKTOK_DONE = ("published",)   # 已发布的默认不再重复填


def cmd_tiktok(ep: Path, dry: bool, cover: bool, again: bool, rehearse: bool = False) -> str:
    """rehearse=True：演练，填完核对后关窗、不发布，只用来验证工具；记录写进 tiktok_rehearsals，不动 tiktok 状态。"""
    job = tiktok_job(ep, cover)
    problems = job.problems() + image_gate(ep)
    if dry or problems:
        show(job)
        if problems:
            raise SystemExit("不能填表：\n" + "\n".join(problems))
        print("dry-run：校验通过，未打开浏览器")
        return "dry-run"
    rec = load(ep)
    old = rec.get("tiktok", {})
    if old.get("state") in TIKTOK_DONE and not again:
        stale = "（但片子已变，旧的要先在 TikTok Studio 删掉）" if old.get("sha256") != sha256(job.video) else ""
        raise SystemExit(f"TikTok 这一期已是「{old['state']}」{stale}；确要再填加 --again")
    print(f"说明（自动填写失败时手动粘贴）：\n{job.caption}\n{' '.join('#' + t for t in job.hashtags)}\n")
    from tools.tiktok_upload import fill
    if rehearse:
        state = fill(job, mode="rehearse")
        rec = load(ep)
        rec.setdefault("tiktok_rehearsals", []).append({"at": now(), "video": job.video.name, "sha256": sha256(job.video),
                                                        "result": state})
        save(ep, rec)
        return state
    if old:
        rec.setdefault("tiktok_history", []).append(old)
    rec["tiktok"] = {"state": "filling", "started": now(), "video": job.video.name, "sha256": sha256(job.video),
                     "caption": job.caption, "hashtags": job.hashtags, "ai_generated": job.ai_generated,
                     "cover": job.cover.name if job.cover else None}
    save(ep, rec)
    state = fill(job)
    rec["tiktok"].update(state=state, ended=now())
    save(ep, rec)
    print({"published": "已记为已发布",
           }.get(state, "未检测到发布（若你其实发了，到 TikTok Studio 作品页确认后可手动改 uploads.json）"))
    return state


def cmd_tiktok_all(rehearse: bool, cover: bool) -> None:
    """把 release/ 里有英文成片、还没发布的期逐期填一遍（每期等你点 Post 或关窗再到下一期）；一期失败不影响下一期。"""
    eps = [d for d in sorted(EPS.iterdir()) if (RELEASE / d.name / f"{d.name}_en.mp4").is_file()]
    results: dict[str, str] = {}
    for ep in eps:
        print(f"\n===== {ep.name}")
        try:
            results[ep.name] = cmd_tiktok(ep, False, cover, False, rehearse)
        except SystemExit as e:
            results[ep.name] = f"跳过：{e}"
            print(results[ep.name])
        except Exception as e:  # noqa: BLE001  一期出错不拖累后面的期
            results[ep.name] = f"出错：{type(e).__name__}: {str(e).splitlines()[0][:160]}"
            print(results[ep.name])
    print("\n===== 汇总")
    for k, v in results.items():
        print(f"{k:40} {v}")


def cmd_status() -> None:
    for ep in sorted(d for d in EPS.iterdir() if d.is_dir()):
        if not (ep / "publish.md").is_file():
            continue
        rec = load(ep)
        yt, dy, tt = rec.get("youtube", {}), rec.get("douyin", {}), rec.get("tiktok", {})
        cur = RELEASE / ep.name / f"{ep.name}_en.mp4"
        stale = " ⚠片子已变" if yt.get("sha256") and cur.is_file() and sha256(cur) != yt["sha256"] else ""
        yts = f"{yt.get('state', '—')} {yt.get('url', '')}{stale}".strip()
        print(f"{ep.name:40} YouTube: {yts:45} 抖音: {dy.get('state', '—'):10} TikTok: {tt.get('state', '—')}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    y = sub.add_parser("youtube")
    y.add_argument("ep")
    y.add_argument("--dry-run", action="store_true")
    y.add_argument("--publish-at", help="RFC 3339 UTC，如 2026-11-08T12:00:00Z；到点自动公开")
    y.add_argument("--retry-unknown", action="store_true")
    c = sub.add_parser("comments")
    c.add_argument("ep")
    d = sub.add_parser("douyin")
    d.add_argument("ep")
    d.add_argument("--dry-run", action="store_true")
    d.add_argument("--cover", type=int, choices=(1, 2, 3), default=1, help="封面款式：1 冠军大图 2 柱状对比 3 悬念大字")
    d.add_argument("--again", action="store_true")
    t = sub.add_parser("tiktok")
    t.add_argument("ep")
    t.add_argument("--dry-run", action="store_true")
    t.add_argument("--no-cover", action="store_true", help="不传自定义封面（用 TikTok 默认帧）")
    t.add_argument("--again", action="store_true")
    t.add_argument("--rehearse", action="store_true", help="演练：填完核对后关窗，不发布")
    ta = sub.add_parser("tiktok-all", help="release/ 里所有未发布的英文成片逐期填，每期等你点 Post")
    ta.add_argument("--no-cover", action="store_true")
    ta.add_argument("--rehearse", action="store_true", help="演练：每期填完核对后关窗，不发布")
    a = ap.parse_args()
    if a.cmd == "status":
        cmd_status()
    elif a.cmd == "youtube":
        cmd_youtube(episode(a.ep), a.dry_run, a.publish_at, a.retry_unknown)
    elif a.cmd == "comments":
        cmd_comments(episode(a.ep))
    elif a.cmd == "tiktok":
        cmd_tiktok(episode(a.ep), a.dry_run, not a.no_cover, a.again, a.rehearse)
    elif a.cmd == "tiktok-all":
        cmd_tiktok_all(a.rehearse, not a.no_cover)
    else:
        cmd_douyin(episode(a.ep), a.dry_run, a.cover, a.again)


if __name__ == "__main__":
    main()
