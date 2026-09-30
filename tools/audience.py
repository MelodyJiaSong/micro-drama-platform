# -*- coding: utf-8 -*-
"""观众回路（轻量；skill ai_videos__整集观感 §6）：记发布、收留存曲线与评论、映射到镜，出 audience_report.md。

    python tools/audience.py log <剧> <ep> --platform youtube --url URL [--date YYYY-MM-DD]
    python tools/audience.py ingest <剧> <ep> --platform P --retention FILE.csv [--comments FILE.txt] [--views N] [--avg-view-s S] [--segments PATH]
    python tools/audience.py report <剧> <ep>

记录落 {集目录}/audience.toml（[[release]] / [[ingest]]）；留存 CSV、评论与当时的 segments.json 原件拷进 {集目录}/audience/，
报告每次都从它们重算到 {集目录}/audience_report.md。镜边界：--segments ＞ viewing/packet.json（非 animatic；它对过视频总长）
＞ 集目录 {ep}_final / {ep} / {ep}_animatic 的 .segments.json。报告末尾「候选 follow-up」只是草稿，不自动落 follow-up。

留存 CSV：两列（位置, 留存），表头可省。首选 YouTube Analytics API audienceRetention 报表的列 elapsedVideoTimeRatio
（0.01–1.0，每视频 100 个点）与 audienceWatchRatio（观看比例，重看可 > 1）；YouTube Studio 网页导出的列名没能核实，
按表头关键字与数值范围兼容：位置＝0–1 比例 / 百分比 / 秒 / mm:ss，留存＝百分比 / 0–1 比例。认不出就 raise。
"""
from __future__ import annotations

import argparse
import bisect
import csv
import datetime
import io
import json
import re
import shutil
import statistics
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewing_packet as vp  # noqa: E402

PLATFORMS = ("youtube", "tiktok", "douyin", "xiaohongshu", "bilibili")
LEDGER = "audience.toml"
RAW_SUB = "audience"
REPORT = "audience_report.md"
RET_KEYS = ("audiencewatchratio", "retention", "留存", "watch", "观看")
POS_KEYS = ("elapsedvideotimeratio", "position", "elapsed", "位置", "进度", "time", "时间", "second", "秒")
NOT_RET = ("relative", "相对")
CLOCK = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2}(?:\.\d+)?)")
COMMENT_TS = re.compile(r"(?<![\d:])(?:(\d+):)?(\d{1,2}):([0-5]\d)(?![\d:])")
EXPECTED = ("期望两列（位置, 留存），逗号 / 制表符 / 分号分隔，表头可省：① YouTube Analytics API audienceRetention："
            "elapsedVideoTimeRatio（0.01–1.0）, audienceWatchRatio（比例）；② 通用：位置＝0–1 比例、百分比（带 % 或表头写 %）、"
            "秒或 mm:ss，留存＝百分比或 0–1 比例")
TOP_N = 3
SAMPLE_S = 0.25
MAX_COMMENTS = 30


@dataclass(frozen=True)
class Curve:
    t: tuple[float, ...]
    pct: tuple[float, ...]

    def at(self, x: float) -> float:
        if x <= self.t[0]:
            return self.pct[0]
        if x >= self.t[-1]:
            return self.pct[-1]
        i = bisect.bisect_right(self.t, x)
        t0, t1, p0, p1 = self.t[i - 1], self.t[i], self.pct[i - 1], self.pct[i]
        return p0 + (p1 - p0) * (x - t0) / (t1 - t0)


@dataclass(frozen=True)
class ShotStat:
    seg: vp.Seg
    avg: float
    first: float
    last: float
    steep_t: float
    steep_pp: float

    @property
    def drop(self) -> float:
        return self.first - self.last


# ─────────────────────────── 留存 CSV ───────────────────────────

def _num(cell: str) -> tuple[float, str] | None:
    c = cell.strip()
    m = CLOCK.fullmatch(c)
    if m:
        return int(m[1] or 0) * 3600 + int(m[2]) * 60 + float(m[3]), "clock"
    try:
        return (float(c[:-1]), "pct") if c.endswith("%") else (float(c), "")
    except ValueError:
        return None


def _col(header: list[str], keys: tuple[str, ...], avoid: tuple[str, ...], skip: int | None) -> int | None:
    for k in keys:
        for i, h in enumerate(header):
            hl = h.lower()
            if i != skip and k in hl and not any(a in hl for a in avoid):
                return i
    return None


def _table(path: Path) -> tuple[list[str], list[list[str]]]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        dialect: type[csv.Dialect] | csv.Dialect = csv.Sniffer().sniff(text[:4096], delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    rows = [r for r in csv.reader(io.StringIO(text), dialect) if any(c.strip() for c in r)]
    if not rows:
        raise SystemExit(f"{path.name} 是空的。{EXPECTED}")
    header = [c.strip() for c in rows.pop(0)] if any(_num(c) is None for c in rows[0] if c.strip()) else []
    return header, rows


def _seconds(vals: list[float], hints: list[str], head: str, total: float, name: str) -> list[float]:
    h = head.lower()
    if all(x == "clock" for x in hints):
        return vals
    if "clock" in hints:
        raise SystemExit(f"{name}：位置列 mm:ss 与数字混写。{EXPECTED}")
    if all(x == "pct" for x in hints) or any(k in h for k in ("%", "percent", "百分")):
        return [v / 100 * total for v in vals]
    if "ratio" in h or "比例" in h:
        return [v * total for v in vals]
    if any(k in h for k in ("sec", "秒", "(s)")):
        return vals
    top = max(vals)
    if top <= 1.0:
        return [v * total for v in vals]
    if abs(top - total) <= max(2.0, 0.05 * total) or top > 100:
        return vals
    if top >= 90:
        return [v / 100 * total for v in vals]
    raise SystemExit(f"{name}：位置列最大 {top:g}，视频 {total:.1f}s，看不出是秒还是百分比——表头写上 % 或 秒。{EXPECTED}")


def _percent(vals: list[float], hints: list[str], head: str) -> list[float]:
    h = head.lower()
    if all(x == "pct" for x in hints) or any(k in h for k in ("%", "percent", "百分")):
        return vals
    if "ratio" in h or "比例" in h or max(vals) <= 1.5:
        return [v * 100 for v in vals]
    return vals


def parse_retention(path: Path, total: float) -> Curve:
    if not path.is_file():
        raise SystemExit(f"没有这个文件：{path}")
    header, rows = _table(path)
    ri = _col(header, RET_KEYS, NOT_RET, None) if header else None
    pi = _col(header, POS_KEYS, NOT_RET, ri) if header else None
    if pi is None or ri is None:
        if header and len(header) > 2:
            raise SystemExit(f"{path.name}：表头 {header} 里找不到位置列与留存列。{EXPECTED}")
        pi, ri = 0, 1
    cells = []
    for n, r in enumerate(rows, 1):
        p, v = (_num(r[pi]), _num(r[ri])) if len(r) > max(pi, ri) else (None, None)
        if p is None or v is None:
            raise SystemExit(f"{path.name} 数据第 {n} 行认不出：{r}。{EXPECTED}")
        cells.append((p, v))
    if len(cells) < 5:
        raise SystemExit(f"{path.name} 只有 {len(cells)} 个点，太少。{EXPECTED}")
    head = (header[pi], header[ri]) if header else ("", "")
    ts = _seconds([p[0] for p, _ in cells], [p[1] for p, _ in cells], head[0], total, path.name)
    ps = _percent([v[0] for _, v in cells], [v[1] for _, v in cells], head[1])
    if max(ts) > total * 1.05 or min(ps) < 0 or max(ps) > 300:
        raise SystemExit(f"{path.name}：位置到 {max(ts):.1f}s（视频 {total:.1f}s）、留存 {min(ps):.0f}–{max(ps):.0f}%，"
                         "多半传错了视频或 segments。" + EXPECTED)
    pts = dict(sorted(zip(ts, ps)))
    return Curve(tuple(pts), tuple(pts.values()))


# ─────────────────────────── 映射到镜 ───────────────────────────

def segments_json(ep_dir: Path, ep: str, override: str | None) -> tuple[str, str]:
    """(镜边界 JSON, 出处)。发布的是成片 / 拼接版时优先用 viewing/packet.json 的镜边界——它对过视频总长。"""
    if override:
        if not Path(override).is_file():
            raise SystemExit(f"没有这个 segments：{override}")
        return Path(override).read_text(encoding="utf-8"), override
    pk = ep_dir / vp.VIEW_SUB / vp.PACKET_NAME
    if pk.is_file():
        d = json.loads(pk.read_text(encoding="utf-8"))
        if d["video"]["kind"] != vp.ANIMATIC:
            body = {"version": 1, "approx": d["segments"]["approx"], "total_s": d["video"]["duration_s"],
                    "source": f"{vp.VIEW_SUB}/{vp.PACKET_NAME}（{d['video']['path']}）", "segments": d["segments"]["shots"]}
            return json.dumps(body, ensure_ascii=False, indent=2), body["source"]
    for stem, _ in vp.VIDEOS:
        p = ep_dir / (stem.format(ep=ep) + vp.SEGMENTS_SUFFIX)
        if p.is_file():
            return p.read_text(encoding="utf-8"), p.name
    raise SystemExit(f"{vp.rel(ep_dir)} 里既没有观片包也没有 segments.json：先跑 viewing_packet.py，或用 --segments 指定发布的那条视频的镜边界")


def shot_stats(curve: Curve, segs: list[vp.Seg]) -> list[ShotStat]:
    out = []
    for s in segs:
        n = max(2, int(s.dur / SAMPLE_S) + 1)
        ts = [s.start_s + s.dur * k / (n - 1) for k in range(n)]
        vals = [curve.at(t) for t in ts]
        pp, t = max(((curve.at(t) - curve.at(min(t + 1.0, s.end_s)), t) for t in ts[:-1]), default=(0.0, s.start_s))
        out.append(ShotStat(s, statistics.fmean(vals), vals[0], vals[-1], t, pp))
    return out


def comment_time(c: str) -> float | None:
    m = COMMENT_TS.search(c)
    return int(m[1] or 0) * 3600 + int(m[2]) * 60 + int(m[3]) if m else None


def shot_at(segs: list[vp.Seg], t: float) -> str:
    return next((s.shot for s in segs if s.start_s <= t < s.end_s), "片外")


# ─────────────────────────── 记录 ───────────────────────────

def ledger(ep_dir: Path) -> dict:
    p = ep_dir / LEDGER
    return tomllib.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def append(ep_dir: Path, table: str, fields: dict[str, str | int | float | None]) -> None:
    p = ep_dir / LEDGER
    old = p.read_text(encoding="utf-8") if p.is_file() else "# 观众回路记录（tools/audience.py 维护）：[[release]] 发布，[[ingest]] 收到的数据\n"
    body = [f"[[{table}]]"] + [f"{k} = {json.dumps(v, ensure_ascii=False)}" for k, v in fields.items() if v is not None]
    new = old + "\n" + "\n".join(body) + "\n"
    tomllib.loads(new)
    p.write_text(new, encoding="utf-8")


# ─────────────────────────── 报告 ───────────────────────────

def _platform_section(ep_dir: Path, rec: dict, infos: dict[str, vp.ShotInfo], scores: dict[str, float]) -> tuple[list[str], list[str]]:
    segs, total, _ = vp.read_segments(ep_dir / rec["segments"])
    curve = parse_retention(ep_dir / rec["retention"], total)
    stats = shot_stats(curve, segs)
    med = statistics.median(s.drop for s in stats)
    tc = vp.tc
    head = f"{rec['date']} 收"
    if "views" in rec:
        head += f"；播放 {rec['views']}"
    if "avg_view_s" in rec:
        head += f"；平均观看 {rec['avg_view_s']:g} s（全长 {rec['avg_view_s'] / total:.0%}）"
    L = ["", f"## {rec['platform']}（{head}）", "",
         f"- 3 秒留存 {curve.at(3.0):.0f}%，片尾 {curve.pct[-1]:.0f}%，全片平均 {statistics.fmean(curve.at(t) for t in range(int(total) + 1)):.0f}%",
         f"- 镜边界：`{rec['segments']}`（取自 {rec.get('segments_from', '?')}）；原件：`{rec['retention']}`", "",
         "| 镜 | 成片时间 | 标题 | 标签 | 平均留存 | 镜起 → 镜尾 | 镜内跌 | 最陡 1 s | 观感预估 |", "|---|---|---|---|---|---|---|---|---|"]
    for s in stats:
        i = infos.get(s.seg.shot, vp.ShotInfo("", "", (), ""))
        sc = scores.get(s.seg.shot)
        L.append(f"| {s.seg.shot} | {tc(s.seg.start_s)}–{tc(s.seg.end_s)} | {i.title} | {' / '.join(i.tags) or '—'} | {s.avg:.0f}% | "
                 f"{s.first:.0f}% → {s.last:.0f}% | {s.drop:.1f} pp | {tc(s.steep_t)} −{s.steep_pp:.1f} pp | {'—' if sc is None else f'{sc:g}'} |")
    worst = sorted(stats, key=lambda s: s.drop, reverse=True)[:TOP_N]
    L += ["", f"### 跌得最狠的 {len(worst)} 镜", ""]
    L += [f"{k}. **{s.seg.shot}**《{infos.get(s.seg.shot, vp.ShotInfo('', '', (), '')).title}》{tc(s.seg.start_s)}–{tc(s.seg.end_s)}："
          f"跌 {s.drop:.1f} pp（各镜中位 {med:.1f} pp；每 10 s {s.drop / s.seg.dur * 10:.1f} pp），最陡在 {tc(s.steep_t)}（1 s 跌 {s.steep_pp:.1f} pp）"
          for k, s in enumerate(worst, 1)]
    comments = (ep_dir / rec["comments"]).read_text(encoding="utf-8-sig").splitlines() if rec.get("comments") else []
    comments = [c.strip() for c in comments if c.strip()]
    timed = [(comment_time(c), c) for c in comments if comment_time(c) is not None]
    L += ["", f"### 评论原文摘录（共 {len(comments)} 条；带时间码的先列）", ""]
    L += [f"- [{tc(t)} → {shot_at(segs, t)}] {c}" for t, c in sorted(timed)]
    L += [f"- {c}" for c in comments if comment_time(c) is None][:max(0, MAX_COMMENTS - len(timed))]
    if not comments:
        L.append("（没收评论）")
    drafts = []
    first, last = segs[0].shot, segs[-1].shot
    for s in worst:
        what = "开场钩子（V2）" if s.seg.shot == first else "集尾钩（V5）" if s.seg.shot == last else "拖沓 / 情绪空档（V1、V3）"
        drafts.append(f"- [{rec['platform']}] {s.seg.shot} {tc(s.seg.start_s)}–{tc(s.seg.end_s)} 镜内跌 {s.drop:.1f} pp、最陡在 {tc(s.steep_t)}："
                      f"复看这一秒前后，按 ai_videos__整集观感 的{what}给改法方向")
        sc = scores.get(s.seg.shot)
        if sc is not None and sc >= 7:
            drafts.append(f"- [{rec['platform']}] {s.seg.shot} 观感审稿给了 {sc:g} 分却在跌得最狠之列：审稿口径偏松，拿这一镜校准 ai_videos__整集观感")
        drafts += [f"- [{rec['platform']}] 评论点名 {tc(t)}（{s.seg.shot}）：「{c}」" for t, c in timed if shot_at(segs, t) == s.seg.shot]
    return L, drafts


def write_report(drama: Path, ep: str, ep_dir: Path) -> Path:
    data = ledger(ep_dir)
    latest = {r["platform"]: r for r in data.get("ingest", [])}
    infos = vp.shot_infos(ep_dir)
    scores = vp.review_scores(ep_dir)
    valid, why = vp.review_state(ep_dir)
    L = [f"# {ep} 观众数据（tools/audience.py 生成，勿手改；原件在 {RAW_SUB}/，记录在 {LEDGER}）", "",
         "- 观感预估＝`viewing/review.md` 注意力分（0–10）：" + (why if scores else "还没有 review.md"),
         "- 同一平台只用最近一次收的数据；pp＝百分点。", "", "## 发布", ""]
    rel = data.get("release", [])
    L += ["| 平台 | 日期 | 链接 |", "|---|---|---|"] + [f"| {r['platform']} | {r['date']} | {r['url']} |" for r in rel] if rel else ["（还没登记，`audience.py log`）"]
    drafts: list[str] = []
    for rec in latest.values():
        sec, d = _platform_section(ep_dir, rec, infos, scores if valid else {})
        L += sec
        drafts += d
    if not latest:
        L += ["", "（还没收数据，`audience.py ingest`）"]
    L += ["", "## 候选 follow-up（草稿）", "",
          f"> 只是建议，不会自动落档；要落请人工按 CLAUDE.md § Follow-up prompt handling 写进 `specs/ai_video/{drama.name}/user_input/follow_ups/`。", ""]
    L += drafts or ["（无）"]
    out = ep_dir / REPORT
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


# ─────────────────────────── CLI ───────────────────────────

def _date(s: str) -> str:
    try:
        return datetime.date.fromisoformat(s).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"日期要 YYYY-MM-DD：{s}")


def cmd_log(a: argparse.Namespace) -> int:
    _, ep, ep_dir = vp.resolve(a.drama, a.ep)
    if not re.match(r"https?://", a.url):
        raise SystemExit(f"链接要 http(s)://：{a.url}")
    append(ep_dir, "release", {"platform": a.platform, "url": a.url, "date": a.date})
    print(f"已记 {ep} {a.platform} 发布 → {vp.rel(ep_dir / LEDGER)}")
    return 0


def cmd_ingest(a: argparse.Namespace) -> int:
    drama, ep, ep_dir = vp.resolve(a.drama, a.ep)
    seg_text, seg_src = segments_json(ep_dir, ep, a.segments)
    parse_retention(Path(a.retention), vp.parse_segments(seg_text)[1])
    if a.comments and not Path(a.comments).is_file():
        raise SystemExit(f"没有这个评论文件：{a.comments}")
    raw = ep_dir / RAW_SUB
    raw.mkdir(exist_ok=True)
    base = f"{a.platform}_{datetime.datetime.now():%Y-%m-%d_%H%M%S}"
    names = {"retention": f"{base}_retention{Path(a.retention).suffix}", "segments": f"{base}{vp.SEGMENTS_SUFFIX}"}
    shutil.copy2(a.retention, raw / names["retention"])
    (raw / names["segments"]).write_text(seg_text, encoding="utf-8")
    if a.comments:
        names["comments"] = f"{base}_comments.txt"
        shutil.copy2(a.comments, raw / names["comments"])
    append(ep_dir, "ingest", {"platform": a.platform, "date": datetime.date.today().isoformat(), "views": a.views, "avg_view_s": a.avg_view_s,
                              "segments_from": seg_src, **{k: f"{RAW_SUB}/{n}" for k, n in names.items()}})
    out = write_report(drama, ep, ep_dir)
    print(f"已收 {ep} {a.platform} 数据 → {vp.rel(out)}")
    return 0


def cmd_report(a: argparse.Namespace) -> int:
    drama, ep, ep_dir = vp.resolve(a.drama, a.ep)
    print(f"→ {vp.rel(write_report(drama, ep, ep_dir))}")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="观众回路（ai_videos__整集观感 §6）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("log", "ingest", "report"):
        p = sub.add_parser(name)
        p.add_argument("drama")
        p.add_argument("ep")
        if name != "report":
            p.add_argument("--platform", required=True, choices=PLATFORMS)
    sub.choices["log"].add_argument("--url", required=True)
    sub.choices["log"].add_argument("--date", type=_date, default=datetime.date.today().isoformat())
    ing = sub.choices["ingest"]
    ing.add_argument("--retention", required=True)
    ing.add_argument("--comments")
    ing.add_argument("--views", type=int)
    ing.add_argument("--avg-view-s", type=float)
    ing.add_argument("--segments")
    a = ap.parse_args()
    return {"log": cmd_log, "ingest": cmd_ingest, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
