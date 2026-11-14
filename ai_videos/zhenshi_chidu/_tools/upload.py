"""真实尺度 · YouTube 上传（剧级适配器，照 ai_videos/paihangbang/_tools/upload.py）：英文版传成私享，公开由用户在 Studio 亲手点。

    python ai_videos/zhenshi_chidu/_tools/upload.py youtube <集目录> [--dry-run] [--cover A|B] [--retry-unknown]
    python ai_videos/zhenshi_chidu/_tools/upload.py comments <集目录>   # 用户公开后：发 Comment 1，回复挂在它下面；置顶在 Studio 手点

- 文案取 `<集>/publish.md` 英文部分：「## Title」首行、「## Description」「## Tags」代码块或首行、「## Comment 1…」两个代码块。
- 合成内容声明：publish.md 清单里「Altered or synthetic content」那行写「勾选」→ Yes；且必须与 licenses.csv 是否有 AI 生成素材一致。
- 上传前跑 `gate.py`（许可白名单、比例机检），不过不传。
- 记录写 `<集>/uploads.json`；中途断掉标「结果未知」，不自动重传，先去 Studio 查，确认没有再加 --retry-unknown。
- 中文版不传 YouTube（与排行榜频道一致，中文版发国内平台，见 publish.md 中文部分与 render/covers/）。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from tools.youtube_upload import VideoJob  # noqa: E402

CODE = re.compile(r"```[a-z]*\n(.*?)\n```", re.S)
RECORD = "uploads.json"


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sections(md: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        out[head.strip()] = body.split("\n# ")[0]          # 一级标题（如「# 中文版」）处截断
    return out


def one(secs: dict[str, str], prefix: str) -> str:
    hits = [v for k, v in secs.items() if k.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"publish.md 里「## {prefix}」节有 {len(hits)} 个")
    return hits[0]


def first_line(body: str) -> str:
    return next(ln.strip() for ln in body.splitlines() if ln.strip())


def youtube_job(ep: Path, cover: str) -> VideoJob:
    md = (ep / "publish.md").read_text(encoding="utf-8")
    secs = sections(md)
    syn = [ln for ln in md.splitlines() if "synthetic content" in ln]
    if len(syn) != 1 or "勾选" not in syn[0]:
        raise SystemExit(f"publish.md 的合成内容声明行缺失或不唯一：{syn}")
    lic = list(csv.DictReader((ep / "licenses.csv").open(encoding="utf-8")))
    has_ai = any("AI-generated" in r["source"] for r in lic)
    synthetic = "不勾选" not in syn[0]
    if synthetic != has_ai:
        raise SystemExit(f"publish.md 写合成内容「{'勾选' if synthetic else '不勾选'}」，但 licenses.csv {'有' if has_ai else '没有'} AI 生成素材")
    comments = [CODE.findall(one(secs, "Comment 1（置顶）"))[0], CODE.findall(one(secs, "Comment 1 的回复"))[0]]
    return VideoJob(
        video=ep / "render" / "ep_master.mp4",
        title=first_line(one(secs, "Title")),
        description=CODE.findall(one(secs, "Description"))[0],
        tags=[t.strip() for t in first_line(one(secs, "Tags")).split(",") if t.strip()],
        synthetic=synthetic,
        thumbnail=ep / "render" / f"thumb_{cover}.jpg",
        comments=comments,
    )


def load(ep: Path) -> dict:
    p = ep / RECORD
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def save(ep: Path, rec: dict) -> None:
    (ep / RECORD).write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def gate(ep: Path) -> list[str]:
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("gate.py")), str(ep)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return [] if r.returncode == 0 else [f"gate.py 未通过：\n{r.stdout}{r.stderr}"]


def cmd_youtube(ep: Path, dry: bool, cover: str, retry_unknown: bool) -> None:
    import tools.youtube_upload as yu
    job = youtube_job(ep, cover)
    problems = job.problems() + gate(ep)
    if dry or problems:
        for k, v in vars(job).items():
            print(f"[{k}] {[len(c) for c in v] if k == 'comments' else (v if k != 'description' else f'{len(v.encode())} 字节')}")
        if problems:
            raise SystemExit("不能上传：\n" + "\n".join(problems))
        print("dry-run：校验通过，未上传")
        return
    rec = load(ep)
    yt = rec.get("youtube", {})
    if yt.get("state") == "uploaded":
        raise SystemExit(f"已上传过：{yt['url']}；要换片先在 Studio 删旧的，再删 {ep / RECORD} 的 youtube 记录")
    if yt.get("state") == "uploading" and not retry_unknown:
        raise SystemExit(f"上次上传 {yt['started']} 中断，结果未知。先到 YouTube Studio 查有没有这条私享视频；确认没有再加 --retry-unknown")
    rec["youtube"] = {"state": "uploading", "started": now(), "video": job.video.name, "sha256": sha256(job.video),
                      "title": job.title, "synthetic": job.synthetic}
    save(ep, rec)
    print(f"上传 {job.video.name}（私享）…", flush=True)
    vid = yu.upload(job)
    rec["youtube"].update(state="uploaded", video_id=vid, url=f"https://youtu.be/{vid}", uploaded=now(),
                          studio=f"https://studio.youtube.com/video/{vid}/edit", comments=[])
    save(ep, rec)
    print(f"已上传：{rec['youtube']['url']}", flush=True)
    try:
        yu.set_thumbnail(vid, job.thumbnail)
        rec["youtube"]["thumbnail"] = job.thumbnail.name
    except yu.HttpError as e:
        rec["youtube"]["thumbnail"] = f"失败：{e.reason}"
        print(f"  封面没传上（{e.reason}），请在 Studio 手动传 {job.thumbnail}")
    save(ep, rec)
    print(f"下一步：在 Studio 检查后亲手公开 {rec['youtube']['studio']}；公开后运行 comments")


def cmd_comments(ep: Path) -> None:
    import tools.youtube_upload as yu
    rec = load(ep)
    yt = rec.get("youtube", {})
    if yt.get("state") != "uploaded":
        raise SystemExit("还没上传到 YouTube")
    state = yu.privacy(yt["video_id"])
    if state not in ("public", "unlisted"):
        raise SystemExit(f"视频现在是 {state}，先在 Studio 公开再发评论")
    job = youtube_job(ep, "A")
    done: list[str] = yt.setdefault("comments", [])
    yu.post_comments(yt["video_id"], job.comments, done, lambda _: save(ep, rec))
    print(f"评论已发齐。请在 Studio 把 Comment 1 置顶：{yt['url']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["youtube", "comments"])
    ap.add_argument("ep", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cover", choices=["A", "B"], default="A")
    ap.add_argument("--retry-unknown", action="store_true")
    a = ap.parse_args()
    ep = a.ep.resolve()
    if a.cmd == "youtube":
        cmd_youtube(ep, a.dry_run, a.cover, a.retry_unknown)
    else:
        cmd_comments(ep)


if __name__ == "__main__":
    main()
