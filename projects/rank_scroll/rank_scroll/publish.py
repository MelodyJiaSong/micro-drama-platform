"""Draft YouTube publish text: chapters from the timeline, data sources, photo credits from assets.json."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .contract import Episode
from .timeline import FPS, SPEED, Timeline, build


def _ts(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def _arrive_s(tl: Timeline, center: int) -> float:
    """Seconds when a band x reaches screen centre (clamped to the scroll start)."""
    if center <= tl.cam_start:
        return tl.f_intro / FPS
    const_end = tl.cam_start + SPEED * tl.f_const
    if center <= const_end:
        return (tl.f_intro + tl.f_hold + (center - tl.cam_start) / SPEED) / FPS
    return tl.segments[1][2] / FPS


def _list_chapters(ep: Episode, tl: Timeline) -> list[tuple[float, str]]:
    """List mode (follow-up 013): one chapter per ~6 cards, labelled 'First → Last' (no ranks, no champion)."""
    cards = [e for e in tl.elements if e.kind == "card"]
    out: list[tuple[float, str]] = []
    size = 6
    for k in range(0, len(cards), size):
        grp = cards[k:k + size]
        t = 0.0 if k == 0 else _arrive_s(tl, grp[0].center)
        lab = f"{ep.items[grp[0].index].name} → {ep.items[grp[-1].index].name}"
        out.append((t, ("Intro & " if k == 0 else "") + lab))
    out.append((tl.segments[3][1] / FPS + 1.0, ep.tally_title))
    out.append((tl.segments[4][1] / FPS, "Sources & credits"))
    clean: list[tuple[float, str]] = []
    for t, lab in out:
        if clean and t - clean[-1][0] < 10:
            continue
        clean.append((t, lab))
    return clean


def chapters(ep: Episode, tl: Timeline) -> list[tuple[float, str]]:
    if ep.is_list:
        return _list_chapters(ep, tl)
    n = max(it.rank for it in ep.items)
    cards = [e for e in tl.elements if e.kind == "card"]
    out: list[tuple[float, str]] = [(0.0, "Intro")]
    groups: list[tuple[int, int]] = []          # decade groups; the first one starts at N (N=36 → #36–#31, not dropped)
    hi = n
    for lo in (41, 31, 21, 11):
        if hi >= lo:
            groups.append((hi, lo))
            hi = lo - 1
    if len(groups) > 1 and groups[0][0] - groups[0][1] < 2:   # N=41 → "#41–#31", not a lone "#41–#41" chapter
        groups[0:2] = [(groups[0][0], groups[1][1])]
    for hi, lo in groups:
        members = [e for e in cards if lo <= e.rank <= hi]
        if not members:
            continue
        first = members[0]                      # countdown order → highest rank of the group
        t = tl.f_intro / FPS if not out[1:] else _arrive_s(tl, first.center)
        out.append((t, f"#{first.rank}–#{members[-1].rank}"))   # actual ranks present (ties can skip the group floor)
    top = [e for e in cards if e.rank <= 10]
    if top:
        out.append((_arrive_s(tl, top[0].center), "Top 10"))
    out.append((tl.segments[2][1] / FPS - 4.0, "No. 1"))
    out.append((tl.segments[3][1] / FPS + 1.0, ep.tally_title))
    out.append((tl.segments[4][1] / FPS, "Sources & credits"))
    if len(out) > 1 and out[1][0] - out[0][0] < 10:   # first group starts right after the title card
        out = [(0.0, f"Intro & {out[1][1]}")] + out[2:]
    clean: list[tuple[float, str]] = []          # YouTube: increasing, ≥ 10 s apart
    for t, lab in out:
        if clean and t - clean[-1][0] < 10:
            continue
        clean.append((t, lab))
    return clean


DESC_LIMIT = 5000        # YouTube description limit (characters)
COMMENT_LIMIT = 9500    # YouTube comment limit is 10,000; keep a margin


def _split(lines: list[str], limit: int) -> list[str]:
    parts, cur = [], ""
    for ln in lines:
        if cur and len(cur) + len(ln) + 1 > limit:
            parts.append(cur.rstrip())
            cur = ""
        cur += ln + "\n"
    if cur.strip():
        parts.append(cur.rstrip())
    return parts


def _hashtags(data: dict) -> list[str]:
    tag = "#" + "".join(w.capitalize() for w in data["title"].replace("'", "").split())
    tags = [tag] if len(tag) <= 40 else []
    if data.get("mode") == "list":
        return tags + ["#DataComparison", "#Explained"]
    return tags + [f"#{data['kicker'].replace(' ', '').title()}", "#Ranking", "#DataComparison"]


def draft(ep: Episode, title: str | None = None) -> str:
    tl = build(ep)
    data = json.loads((ep.root / "data.json").read_text(encoding="utf-8"))
    ledger_path = ep.root / "assets.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.is_file() else []
    by_file = {str(x.get("file", "")).replace("\\", "/"): x for x in ledger}
    items = sorted(data["items"], key=lambda r: (r["rank"], r.get("country_name", "")))

    shown = {str(it.image.relative_to(ep.root)).replace("\\", "/") for it in ep.items if it.image}
    shown_people = {str(it.person_image.relative_to(ep.root)).replace("\\", "/") for it in ep.items if it.person_image}
    compact, full, src_lines = [], [], []
    synth = 0   # AI-generated images on screen (ledger licence / synthetic flag; rank_scroll follow-up 009)
    for raw in items:
        rel = next((r for r in ((raw.get(k) or "").replace("\\", "/") for k in ("image", "image_alt")) if r in shown), "")
        e = by_file.get(rel) if rel else None
        label = (raw["name"] if ep.is_list else f"#{raw['rank']} {raw['name']}") + (f" ({raw.get('country_name')})" if data.get("tally", {}).get("by") == "continent" and ep.show_flags else "")
        if e and (str(e.get("licence", "")).lower().startswith("ai-generated") or e.get("synthetic")):
            synth += 1
        if e:
            e = dict(e, author=str(e.get("author", "unknown")).replace("User:", "").strip())
            compact.append(f"{label}: {e.get('author', 'unknown')} ({e.get('licence', '')})")
            full.append(f"{label}: {e.get('author', 'unknown')}, {e.get('licence', '')}"
                        + (f" {e['licence_url']}" if e.get("licence_url") else "")
                        + (f" — {e.get('source_page') or e.get('commons_page') or e.get('source_url')}" if (e.get('source_page') or e.get('commons_page') or e.get('source_url')) else ""))
        prel = str((raw.get("person") or {}).get("image") or "").replace("\\", "/")
        pe = by_file.get(prel) if prel in shown_people else None
        if pe:                                  # founder portraits need credits too (CC BY / BY-SA) — follow-up 013
            pe = dict(pe, author=str(pe.get("author", "unknown")).replace("User:", "").strip())
            plabel = f"{label} (portrait of {raw['person'].get('name', '')})"
            compact.append(f"{plabel}: {pe.get('author', 'unknown')} ({pe.get('licence', '')})")
            full.append(f"{plabel}: {pe.get('author', 'unknown')}, {pe.get('licence', '')}"
                        + (f" {pe['licence_url']}" if pe.get("licence_url") else "")
                        + (f" — {pe.get('source_page') or pe.get('source_url')}" if (pe.get('source_page') or pe.get('source_url')) else ""))
        src = raw.get("source") or {}
        if src.get("url"):
            src_lines.append(f"{label}: {src.get('name', '')} {src['url']}")

    # title year = last 4-digit year in period_label ("Data as of Nov 2026"); labels without one fall back
    # to the current year (rank_scroll follow-up 008: "... · year on each card" used to yield "(card)")
    years = re.findall(r"\b(?:19|20)\d{2}\b", ep.period_label)
    yt_title = title or data.get("youtube_title") or f"{data['title']} | {data['kicker'].title()} ({years[-1] if years else date.today().year})"
    lead = (f"{data['title']}: {len(ep.items)} entries one by one, in order (not a ranking), each with its {ep.metric_label.lower()} ({ep.period_label})."
            if ep.is_list else f"{data['title']} — {data['kicker'].lower()} ranked by {ep.metric_label.lower()} ({ep.period_label}).")
    desc = [lead,
            "Every number on screen is sourced (per-item links in the pinned comment). Which one surprised you? Tell us in the comments!", "",
            "Chapters:"] + [f"{_ts(t)} {lab}" for t, lab in chapters(ep, tl)] + [
            *(["", ep.scope_note] if ep.scope_note else []),
            "", ep.source_line, "Full image credits and per-item data sources with links: see the pinned comment and the replies under it.", "",
            "Image credits (resized and cropped, no other changes"
            + (f"; {synth} images marked AI-generated are illustrations, not photos" if synth else "")
            + "):"] + compact + [
            *(["", data["music_credit"]] if data.get("music_credit") else []),
            "", ("Flags: flagcdn.com (public domain) · " if ep.show_flags else "") + "Icons: Tabler Icons (MIT) · Font: Inter (SIL OFL 1.1)", "",
            " ".join(_hashtags(data))]
    desc_text = "\n".join(desc)
    comments = (_split(["Full image credits (author, licence, licence link, source):"] + full, COMMENT_LIMIT)
                + _split(["Data sources per item:"] + src_lines, COMMENT_LIMIT))

    lines = [f"# publish draft · {ep.episode}", "", "> 由 `python -m rank_scroll publish` 生成；上传前人工检查。上传由用户亲手做。", "",
             "## Title", "", yt_title, f"（{len(yt_title)} 字符）", "",
             f"## Description（{len(desc_text)} / {DESC_LIMIT} 字符{'，⚠ 超长' if len(desc_text) > DESC_LIMIT else ''}）", "",
             "```text", desc_text, "```", ""]
    for i, cm in enumerate(comments, 1):
        lines += [f"## Comment {i}{'（置顶）' if i == 1 else ''}（{len(cm)} 字符）", "", "```text", cm, "```", ""]
    lines += ["## Upload checklist", "",
              "- [ ] 标题 ≤ 60 字符（YouTube 上限 100，搜索结果约显示 60），封面用 `render/thumbnail.png` 或人工改版",
              "- [ ] 片尾元素：最后 18 秒放 2 个视频 + 订阅",
              ("- [ ] 「Altered or synthetic content」：本片有 AI 生成的写实风格插画（卡上标 AI IMAGE，署名注明 AI-generated）→ 选 Yes（bible §4）"
               if synth else
               "- [ ] 「Altered or synthetic content」：本片无 AI 生成的逼真画面 → 选 No"),
              "- [ ] 语言 English；类别 Education",
              *(["- [ ] 配乐为自家 Suno 生成曲：不登记 Content ID；被第三方认领时用本剧 request_log.md 的生成记录申诉（bible §5）"] if data.get("music_credit") else []),
              f"- [ ] 时长 {tl.duration / 60:.1f} 分钟（< 8 分钟，不能插中插广告）",
              "- [ ] Comment 1 发布后置顶；其余 Comment 依次回复在 Comment 1 下", ""]
    return "\n".join(lines)


def write(ep: Episode, out: Path | None = None) -> Path:
    out = out or ep.root / "publish.md"
    out.write_text(draft(ep), encoding="utf-8")
    return out
