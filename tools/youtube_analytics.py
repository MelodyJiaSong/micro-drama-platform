"""自有 YouTube 频道增长报告（YouTube Analytics API v2 + Data API v3，只读）。

    python tools/youtube_analytics.py report [--days 28] [--end 2026-11-04] [--retention 5] [--out DIR]
    python tools/youtube_analytics.py retention <video_id> [--days 365]

report 写 report.json（原始行）与 report.md（中文表格）到
ai_videos/_research/youtube_channel/<频道 id>/<结束日>_<天数>d/，同一窗口重跑覆盖。
内容：频道累计、本期对上一期、按天、热门视频（含留存）、内容类型、流量来源、地区、设备、订阅与否、YPP 进度（近似）。
Analytics 数据一般滞后 2–3 天，默认结束日为 3 天前。曝光次数与点击率 API 不提供，到 Studio「覆盖面」看。
授权与凭据同 tools/youtube_upload.py（auth 一次即可）；同类频道公开数据用 tools/yt_research.py。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.youtube_upload import credentials  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO / "ai_videos" / "_research" / "youtube_channel"
LAG_DAYS = 3
SHORTS = "shorts"   # creatorContentType 实测返回小写驼峰：shorts / videoOnDemand
YPP_SUBS = 1000
YPP_WATCH_HOURS = 4000
YPP_SHORTS_VIEWS = 10_000_000
CORE = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost"
ENGAGE = "likes,comments,shares"
RETENTION_MARKS = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
TRAFFIC_ZH = {
    "SHORTS": "Shorts 信息流", "YT_SEARCH": "YouTube 搜索", "SUBSCRIBER": "浏览功能（首页、订阅等）",
    "RELATED_VIDEO": "推荐视频", "EXT_URL": "外部链接", "NO_LINK_OTHER": "直接/未知", "PLAYLIST": "播放列表",
    "YT_CHANNEL": "频道页", "NOTIFICATION": "通知", "YT_OTHER_PAGE": "其他 YouTube 页", "END_SCREEN": "片尾画面",
    "ANNOTATION": "卡片/注释", "HASHTAGS": "话题标签", "SOUND_PAGE": "音频页",
}


@dataclass(frozen=True)
class Window:
    start: date
    end: date

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1

    def previous(self) -> Window:
        return Window(self.start - timedelta(days=self.days), self.start - timedelta(days=1))


@dataclass
class Table:
    columns: list[str]
    rows: list[list[Any]]
    error: str | None = None

    def records(self) -> list[dict[str, Any]]:
        return [dict(zip(self.columns, r)) for r in self.rows]

    def total(self, col: str) -> float:
        i = self.columns.index(col)
        return float(sum(r[i] or 0 for r in self.rows))


@dataclass
class Client:
    analytics: Any = field(init=False)
    data: Any = field(init=False)

    def __post_init__(self) -> None:
        creds = credentials()
        self.analytics = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
        self.data = build("youtube", "v3", credentials=creds, cache_discovery=False)

    def query(self, w: Window, metrics: str, dimensions: str | None = None, sort: str | None = None,
              max_results: int | None = None, filters: str | None = None) -> Table:
        kw: dict[str, Any] = {"ids": "channel==MINE", "startDate": w.start.isoformat(), "endDate": w.end.isoformat(),
                              "metrics": metrics}
        for k, v in (("dimensions", dimensions), ("sort", sort), ("maxResults", max_results), ("filters", filters)):
            if v is not None:
                kw[k] = v
        try:
            resp = self.analytics.reports().query(**kw).execute()
        except HttpError as e:
            if e.resp.status == 403 and b"accessNotConfigured" in e.content:
                raise SystemExit("YouTube Analytics API 未在 Google Cloud 项目里启用："
                                 "https://console.cloud.google.com/apis/library/youtubeanalytics.googleapis.com") from e
            return Table([], [], error=f"HTTP {e.resp.status}: {e.reason}")
        return Table([h["name"] for h in resp.get("columnHeaders", [])], resp.get("rows", []))

    def channel(self) -> dict[str, Any]:
        items = self.data.channels().list(part="snippet,statistics,contentDetails", mine=True).execute().get("items", [])
        if not items:
            raise SystemExit("授权账号下没有 YouTube 频道")
        c = items[0]
        s = c["statistics"]
        return {"id": c["id"], "title": c["snippet"]["title"], "created": c["snippet"]["publishedAt"][:10],
                "subscribers": int(s.get("subscriberCount", 0)), "hidden_subscribers": s.get("hiddenSubscriberCount"),
                "views": int(s.get("viewCount", 0)), "videos": int(s.get("videoCount", 0)),
                "uploads": c["contentDetails"]["relatedPlaylists"]["uploads"]}

    def videos(self, uploads: str, limit: int = 500) -> dict[str, dict[str, Any]]:
        ids: list[str] = []
        token: str | None = None
        while len(ids) < limit:
            resp = self.data.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50,
                                                  pageToken=token).execute()
            ids += [i["contentDetails"]["videoId"] for i in resp.get("items", [])]
            token = resp.get("nextPageToken")
            if not token:
                break
        out: dict[str, dict[str, Any]] = {}
        for k in range(0, len(ids), 50):
            resp = self.data.videos().list(part="snippet,statistics,contentDetails,status", id=",".join(ids[k:k + 50])).execute()
            for v in resp.get("items", []):
                out[v["id"]] = {"title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"][:10],
                                "duration": v["contentDetails"]["duration"], "privacy": v["status"]["privacyStatus"],
                                "views": int(v["statistics"].get("viewCount", 0)),
                                "likes": int(v["statistics"].get("likeCount", 0))}
        return out

    def retention(self, video_id: str, w: Window) -> Table:
        return self.query(w, "audienceWatchRatio,relativeRetentionPerformance", "elapsedVideoTimeRatio",
                          filters=f"video=={video_id}")


def pct(new: float, old: float) -> str:
    return "—" if not old else f"{(new - old) / old:+.0%}"


def num(x: float) -> str:
    return f"{x:,.0f}" if abs(x) >= 10 or float(x).is_integer() else f"{x:,.1f}"


def md_table(t: Table, cols: list[str], heads: list[str], fmt: dict[str, Any] | None = None) -> str:
    if t.error:
        return f"（未取到：{t.error}）\n"
    if not t.rows:
        return "（本期无数据）\n"
    fmt = fmt or {}
    lines = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(heads)]
    for r in t.records():
        lines.append("| " + " | ".join(str(fmt[c](r[c]) if c in fmt else (num(r[c]) if isinstance(r[c], (int, float)) else r[c]))
                                       for c in cols) + " |")
    return "\n".join(lines) + "\n"


def retention_marks(t: Table) -> dict[str, float]:
    if t.error or not t.rows:
        return {}
    pts = [(float(r[0]), float(r[1])) for r in t.rows]
    return {f"{m:.0%}": min(pts, key=lambda p: abs(p[0] - m))[1] for m in RETENTION_MARKS}


def report(days: int, end: date | None, n_retention: int, out: Path | None) -> Path:
    cl = Client()
    ch = cl.channel()
    end = end or date.today() - timedelta(days=LAG_DAYS)
    w = Window(end - timedelta(days=days - 1), end)
    prev = w.previous()
    year = Window(end - timedelta(days=364), end)
    quarter = Window(end - timedelta(days=89), end)
    metrics = f"{CORE},{ENGAGE}"
    t: dict[str, Table] = {
        "totals": cl.query(w, metrics),
        "totals_prev": cl.query(prev, metrics),
        "daily": cl.query(w, metrics, "day", "day"),
        "top_videos": cl.query(w, CORE, "video", "-views", 25),
        "content_type": cl.query(w, "views,estimatedMinutesWatched,averageViewDuration", "creatorContentType", "-views"),
        "traffic": cl.query(w, "views,estimatedMinutesWatched", "insightTrafficSourceType", "-views"),
        "country": cl.query(w, "views,estimatedMinutesWatched", "country", "-views", 15),
        "device": cl.query(w, "views,estimatedMinutesWatched", "deviceType", "-views"),
        "subscribed": cl.query(w, "views,estimatedMinutesWatched,averageViewDuration", "subscribedStatus"),
        "ypp_year": cl.query(year, "views,estimatedMinutesWatched", "creatorContentType"),
        "ypp_quarter": cl.query(quarter, "views", "creatorContentType"),
    }
    vids = cl.videos(ch["uploads"])
    top_ids = [r["video"] for r in t["top_videos"].records()]
    retention = {v: cl.retention(v, year) for v in top_ids[:n_retention]}

    dest = out or OUT_ROOT / ch["id"] / f"{end.isoformat()}_{days}d"
    dest.mkdir(parents=True, exist_ok=True)
    raw = {"channel": ch, "window": [w.start.isoformat(), w.end.isoformat()],
           "previous": [prev.start.isoformat(), prev.end.isoformat()],
           "tables": {k: {"columns": v.columns, "rows": v.rows, "error": v.error} for k, v in t.items()},
           "retention": {k: {"columns": v.columns, "rows": v.rows, "error": v.error} for k, v in retention.items()},
           "videos": vids}
    (dest / "report.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (dest / "report.md").write_text(render(ch, w, prev, t, vids, retention), encoding="utf-8")
    return dest


def render(ch: dict[str, Any], w: Window, prev: Window, t: dict[str, Table], vids: dict[str, dict[str, Any]],
           retention: dict[str, Table]) -> str:
    title = lambda v: (vids.get(v, {}).get("title") or v)[:60]  # noqa: E731
    out = [f"# {ch['title']} 增长报告 · {w.start} → {w.end}（{w.days} 天）\n",
           f"频道 https://www.youtube.com/channel/{ch['id']} · 创建 {ch['created']} · "
           f"累计订阅 {ch['subscribers']:,} · 累计播放 {ch['views']:,} · 视频 {ch['videos']}\n",
           f"对比上一期 {prev.start} → {prev.end}。Analytics 数据滞后 2–3 天；曝光与点击率 API 不提供，见 Studio。\n",
           "## 本期对上一期\n"]
    cur, old = t["totals"], t["totals_prev"]
    if cur.error or old.error:
        out.append(f"（未取到：{cur.error or old.error}）\n")
    else:
        rows = [("播放", "views", 1), ("观看时长（小时）", "estimatedMinutesWatched", 1 / 60),
                ("新增订阅", "subscribersGained", 1), ("流失订阅", "subscribersLost", 1),
                ("点赞", "likes", 1), ("评论", "comments", 1), ("分享", "shares", 1)]
        out += ["| 指标 | 本期 | 上期 | 变化 |", "|---|---|---|---|"]
        for name, col, k in rows:
            a, b = cur.total(col) * k, old.total(col) * k
            out.append(f"| {name} | {num(a)} | {num(b)} | {pct(a, b)} |")
        net, net_old = (cur.total("subscribersGained") - cur.total("subscribersLost"),
                        old.total("subscribersGained") - old.total("subscribersLost"))
        out.append(f"| 净增订阅 | {num(net)} | {num(net_old)} | {pct(net, net_old)} |")
        for name, col in (("平均观看时长（秒）", "averageViewDuration"), ("平均观看比例（%）", "averageViewPercentage")):
            a, b = cur.total(col), old.total(col)
            out.append(f"| {name} | {num(a)} | {num(b)} | {pct(a, b)} |")
        out.append("")

    out.append("## YPP 进度（近似，以 Studio 为准）\n")
    subs_line = f"- 订阅 {ch['subscribers']:,} / {YPP_SUBS:,}"
    yr, qt = t["ypp_year"], t["ypp_quarter"]
    if yr.error or qt.error:
        out += [subs_line, f"- 观看时长 / Shorts 播放未取到：{yr.error or qt.error}", ""]
    else:
        long_hours = sum(r["estimatedMinutesWatched"] for r in yr.records() if r["creatorContentType"].lower() != SHORTS) / 60
        shorts_views = sum(r["views"] for r in qt.records() if r["creatorContentType"].lower() == SHORTS)
        out += [subs_line,
                f"- 近 365 天非 Shorts 观看时长 {long_hours:,.0f} / {YPP_WATCH_HOURS:,} 小时（含私享/已删视频，Studio 只算公开）",
                f"- 或：近 90 天 Shorts 播放 {shorts_views:,.0f} / {YPP_SHORTS_VIEWS:,}", ""]

    out += ["## 热门视频（本期按播放）\n"]
    tv = t["top_videos"]
    if tv.error or not tv.rows:
        out.append(f"（{'未取到：' + tv.error if tv.error else '本期无数据'}）\n")
    else:
        out += ["| 视频 | 发布 | 播放 | 均看秒 | 均看% | 新增订阅 | 留存 25/50/75% |", "|---|---|---|---|---|---|---|"]
        for r in tv.records():
            v = r["video"]
            marks = retention_marks(retention[v]) if v in retention else {}
            ret = " / ".join(f"{marks[k]:.0%}" for k in ("25%", "50%", "75%")) if marks else ""
            out.append(f"| [{title(v)}](https://youtu.be/{v}) | {vids.get(v, {}).get('published', '')} | {num(r['views'])} | "
                       f"{num(r['averageViewDuration'])} | {num(r['averageViewPercentage'])} | {num(r['subscribersGained'])} | {ret} |")
        out.append("\n留存 = 观众在片长该位置仍在看的比例（近 365 天，>100% 表示有回看）。\n")

    sections = [
        ("内容类型", "content_type", ["creatorContentType", "views", "estimatedMinutesWatched", "averageViewDuration"],
         ["类型", "播放", "观看分钟", "均看秒"], {}),
        ("流量来源", "traffic", ["insightTrafficSourceType", "views", "estimatedMinutesWatched"], ["来源", "播放", "观看分钟"],
         {"insightTrafficSourceType": lambda x: TRAFFIC_ZH.get(x, x)}),
        ("地区（前 15）", "country", ["country", "views", "estimatedMinutesWatched"], ["国家", "播放", "观看分钟"], {}),
        ("设备", "device", ["deviceType", "views", "estimatedMinutesWatched"], ["设备", "播放", "观看分钟"], {}),
        ("订阅者与非订阅者", "subscribed", ["subscribedStatus", "views", "estimatedMinutesWatched", "averageViewDuration"],
         ["状态", "播放", "观看分钟", "均看秒"], {}),
    ]
    for name, key, cols, heads, fmt in sections:
        out += [f"## {name}\n", md_table(t[key], cols, heads, fmt)]

    out += ["## 按天\n", md_table(t["daily"], ["day", "views", "estimatedMinutesWatched", "subscribersGained", "subscribersLost"],
                                 ["日期", "播放", "观看分钟", "新增订阅", "流失订阅"])]
    return "\n".join(out)


def cmd_retention(video_id: str, days: int) -> None:
    end = date.today() - timedelta(days=LAG_DAYS)
    t = Client().retention(video_id, Window(end - timedelta(days=days - 1), end))
    if t.error:
        raise SystemExit(t.error)
    print("| 片长位置 | 仍在看 | 相对同类 |\n|---|---|---|")
    for r in t.rows[::5]:
        print(f"| {float(r[0]):.0%} | {float(r[1]):.0%} | {float(r[2]):.2f} |")
    print("\n相对同类：0.5 为同长度 YouTube 视频的中位，越高越好。")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report")
    r.add_argument("--days", type=int, default=28)
    r.add_argument("--end", type=date.fromisoformat)
    r.add_argument("--retention", type=int, default=5, help="给前 N 个热门视频取留存曲线")
    r.add_argument("--out", type=Path)
    v = sub.add_parser("retention")
    v.add_argument("video_id")
    v.add_argument("--days", type=int, default=365)
    a = ap.parse_args()
    if a.cmd == "report":
        dest = report(a.days, a.end, a.retention, a.out)
        print(f"报告：{dest / 'report.md'}\n原始数据：{dest / 'report.json'}")
    else:
        cmd_retention(a.video_id, a.days)


if __name__ == "__main__":
    sys.exit(main())
