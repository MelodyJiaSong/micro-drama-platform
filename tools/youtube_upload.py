"""YouTube 上传（官方 Data API v3）：视频一律先传成私享，公开由人在 YouTube Studio 亲手点。

    python tools/youtube_upload.py auth      # 首次或加了权限后：浏览器里登录并授权频道，token 存本机
    python tools/youtube_upload.py whoami    # 核对授权的是哪个频道

授权同时包含 YouTube Analytics 只读权限，供 tools/youtube_analytics.py 拉增长数据；
旧 token 缺权限时报错要求重新 auth（Google Cloud 项目里还要启用 YouTube Analytics API）。

凭据放仓库外：%USERPROFILE%\\.micro_drama\\youtube\\client_secret.json（Google Cloud「桌面应用」OAuth 客户端，
可用 YOUTUBE_CLIENT_SECRET 覆盖路径）与 token.json（auth 生成）。
剧级适配器（如 ai_videos/paihangbang/_tools/upload.py）组装 VideoJob 后调用 upload() / post_comments()。
配额：默认每天 10,000 单位；传片约 1,600，封面、评论各 50。
未通过 Google 审核的 API 项目，传上去的视频会被锁成私享，要先申请 YouTube API Audit 才能公开。
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]
HOME = Path.home() / ".micro_drama" / "youtube"
TOKEN = HOME / "token.json"
CHUNK = 16 * 1024 * 1024
RETRY_STATUS = {500, 502, 503, 504}
MAX_RETRIES = 8
THUMB_MAX = 2 * 1024 * 1024
TITLE_MAX = 100
DESCRIPTION_MAX_BYTES = 5000
TAGS_MAX = 500
COMMENT_MAX = 10000

Log = Callable[[str], None]


@dataclass(frozen=True)
class VideoJob:
    video: Path
    title: str
    description: str
    tags: list[str]
    synthetic: bool
    thumbnail: Path | None = None
    category_id: str = "27"   # Education
    language: str = "en"
    made_for_kids: bool = False
    publish_at: str | None = None   # RFC 3339 UTC；给了就到点自动公开，否则一直私享
    comments: list[str] = field(default_factory=list)

    def problems(self) -> list[str]:
        out: list[str] = []
        if not self.video.is_file():
            out.append(f"视频不存在：{self.video}")
        if self.thumbnail and not self.thumbnail.is_file():
            out.append(f"封面不存在：{self.thumbnail}")
        if not 0 < len(self.title) <= TITLE_MAX:
            out.append(f"标题 {len(self.title)} 字符，须 1–{TITLE_MAX}")
        size = len(self.description.encode("utf-8"))
        if size > DESCRIPTION_MAX_BYTES:
            out.append(f"描述 {size} 字节（UTF-8），超过 {DESCRIPTION_MAX_BYTES}")
        for name, text in (("标题", self.title), ("描述", self.description)):
            if "<" in text or ">" in text:
                out.append(f"{name}含 < 或 >，YouTube 拒收")
        tag_len = sum(len(t) + (2 if " " in t else 0) for t in self.tags) + max(len(self.tags) - 1, 0)
        if tag_len > TAGS_MAX:
            out.append(f"标签合计 {tag_len} 字符，超过 {TAGS_MAX}")
        for i, c in enumerate(self.comments, 1):
            if len(c) > COMMENT_MAX:
                out.append(f"Comment {i} {len(c)} 字符，超过 {COMMENT_MAX}")
        return out


def _granted() -> set[str]:
    return set(json.loads(TOKEN.read_text(encoding="utf-8")).get("scopes") or []) if TOKEN.is_file() else set()


def credentials(interactive: bool = False) -> Credentials:
    missing = set(SCOPES) - _granted() if TOKEN.is_file() else set()
    if missing and not interactive:
        raise SystemExit(f"YouTube 授权缺权限 {sorted(missing)}：重新运行 python tools/youtube_upload.py auth")
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.is_file() and not missing else None
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save(creds)
            return creds
        except Exception as e:  # refresh token 被撤销或过期（测试状态的 OAuth 应用 7 天过期）
            if not interactive:
                raise SystemExit(f"YouTube 授权已失效（{e}）：重新运行 python tools/youtube_upload.py auth") from e
    if not interactive:
        raise SystemExit("YouTube 尚未授权：先运行 python tools/youtube_upload.py auth")
    secret = Path(os.environ.get("YOUTUBE_CLIENT_SECRET", HOME / "client_secret.json"))
    if not secret.is_file():
        raise SystemExit(
            f"找不到 OAuth 客户端文件：{secret}\n"
            "在 Google Cloud Console：新建项目 → 启用 YouTube Data API v3 → OAuth 同意屏幕（外部，把自己加为测试用户，"
            "或发布为正式版以免 refresh token 7 天过期）→ 凭据 → 创建 OAuth 客户端 ID（桌面应用）→ 下载 JSON 存到上面的路径。")
    flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", open_browser=True)
    _save(creds)
    return creds


def _save(creds: Credentials) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")


def client() -> Any:
    return build("youtube", "v3", credentials=credentials(), cache_discovery=False)


def channel(yt: Any) -> dict[str, str]:
    items = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
    if not items:
        raise SystemExit("授权账号下没有 YouTube 频道")
    return {"id": items[0]["id"], "title": items[0]["snippet"]["title"]}


def _execute(call: Callable[[], Any], log: Log) -> Any:
    for attempt in range(MAX_RETRIES + 1):
        try:
            return call()
        except HttpError as e:
            if e.resp.status not in RETRY_STATUS or attempt == MAX_RETRIES:
                raise
            reason = f"HTTP {e.resp.status}"
        except (httplib2.HttpLib2Error, OSError) as e:
            if attempt == MAX_RETRIES:
                raise
            reason = type(e).__name__
        wait = min(60, 2 ** attempt) + random.random()
        log(f"  {reason}，{wait:.0f} 秒后重试（{attempt + 1}/{MAX_RETRIES}）")
        time.sleep(wait)
    raise AssertionError("unreachable")


def upload(job: VideoJob, log: Log = print) -> str:
    """传片（私享）并返回 video id。中途进程被杀时片子可能已建好，由调用方按「结果未知」处理，不自动重传。"""
    problems = job.problems()
    if problems:
        raise ValueError("\n".join(problems))
    yt = client()
    status: dict[str, Any] = {"privacyStatus": "private", "selfDeclaredMadeForKids": job.made_for_kids,
                              "containsSyntheticMedia": job.synthetic}
    if job.publish_at:
        status["publishAt"] = job.publish_at
    body = {"snippet": {"title": job.title, "description": job.description, "tags": job.tags,
                        "categoryId": job.category_id, "defaultLanguage": job.language,
                        "defaultAudioLanguage": job.language},
            "status": status}
    media = MediaFileUpload(str(job.video), chunksize=CHUNK, resumable=True, mimetype="video/mp4")
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        progress, response = _execute(request.next_chunk, log)
        if progress:
            log(f"  已传 {progress.progress():.0%}")
    return str(response["id"])


def set_thumbnail(video_id: str, path: Path, log: Log = print) -> None:
    src = path
    if path.stat().st_size > THUMB_MAX:
        from PIL import Image
        src = Path(tempfile.gettempdir()) / f"yt_thumb_{video_id}.jpg"
        Image.open(path).convert("RGB").save(src, "JPEG", quality=90)
        log(f"  封面 {path.stat().st_size // 1024} KB 超 2 MB，转 JPEG {src.stat().st_size // 1024} KB 上传")
    mime = "image/png" if src.suffix.lower() == ".png" else "image/jpeg"
    yt = client()
    _execute(lambda: yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(src), mimetype=mime)).execute(), log)


def privacy(video_id: str) -> str | None:
    items = client().videos().list(part="status", id=video_id).execute().get("items", [])
    return items[0]["status"]["privacyStatus"] if items else None


def post_comments(video_id: str, comments: list[str], done: list[str], on_posted: Callable[[str], None],
                  log: Log = print) -> None:
    """Comment 1 为顶层评论，其余依次回复在它下面；done 是已发出的评论 id，续跑时跳过。置顶要在 Studio 手动点。"""
    yt = client()
    for i, text in enumerate(comments):
        if i < len(done):
            continue
        if i == 0:
            body = {"snippet": {"videoId": video_id, "topLevelComment": {"snippet": {"textOriginal": text}}}}
            cid = _execute(lambda: yt.commentThreads().insert(part="snippet", body=body).execute(), log)["id"]
        else:
            body = {"snippet": {"parentId": done[0], "textOriginal": text}}
            cid = _execute(lambda: yt.comments().insert(part="snippet", body=body).execute(), log)["id"]
        done.append(cid)
        on_posted(cid)
        log(f"  Comment {i + 1} 已发：{cid}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["auth", "whoami"])
    args = ap.parse_args()
    if args.cmd == "auth":
        credentials(interactive=True)
        print(f"已授权，token：{TOKEN}")
    ch = channel(client())
    print(f"频道：{ch['title']}（{ch['id']}）https://www.youtube.com/channel/{ch['id']}")


if __name__ == "__main__":
    sys.exit(main())
