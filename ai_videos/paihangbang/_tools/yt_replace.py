# -*- coding: utf-8 -*-
"""删除某期在 YouTube 上**非公开**的旧上传，以便重传新版（paihangbang follow-up 068）。

    python ai_videos/paihangbang/_tools/yt_replace.py delete <期> [--dry-run]

- 只删 uploads.json 里记录的那条 video id；删前用 API 现查 privacyStatus，public 的一律拒删。
- 删除后把旧记录移到 uploads.json 的 youtube_deleted 列表（留 id、URL、删除时间、原因），清空 youtube 记录，
  之后照常 `upload.py youtube <期>` 重传。
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
from tools.youtube_upload import client  # noqa: E402
from upload import RECORD, episode, load, save  # noqa: E402


def cmd_delete(ep: Path, dry: bool, reason: str) -> None:
    rec = load(ep)
    yt_rec = rec.get("youtube") or {}
    vid = yt_rec.get("video_id") or yt_rec.get("id")
    if not vid:
        raise SystemExit(f"{ep.name}：{RECORD} 里没有 YouTube 记录，没东西可删")
    yt = client()
    items = yt.videos().list(part="status,snippet", id=vid).execute().get("items", [])
    if not items:
        raise SystemExit(f"{ep.name}：{vid} 在频道上已不存在（可能已手动删除）；核实后手动清 {RECORD} 的 youtube 记录")
    status = items[0]["status"]["privacyStatus"]
    title = items[0]["snippet"]["title"]
    if status == "public":
        raise SystemExit(f"{ep.name}：{vid}（{title}）是 public，按规则不删")
    print(f"{ep.name}：{vid}（{title}）当前 {status}")
    if dry:
        print("dry-run：未删除")
        return
    yt.videos().delete(id=vid).execute()
    rec.setdefault("youtube_deleted", []).append({**yt_rec, "deleted_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                                                  "privacy_at_delete": status, "reason": reason})
    rec.pop("youtube", None)
    save(ep, rec)
    print(f"已删除 {vid}，旧记录移到 youtube_deleted；可以重传")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("delete")
    d.add_argument("ep")
    d.add_argument("--dry-run", action="store_true")
    d.add_argument("--reason", default="follow-up 068：滚动速度 ×1.5 重出，旧私享版删除重传")
    a = ap.parse_args()
    cmd_delete(episode(a.ep), a.dry_run, a.reason)


if __name__ == "__main__":
    main()
