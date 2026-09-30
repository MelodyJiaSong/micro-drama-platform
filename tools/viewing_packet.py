# -*- coding: utf-8 -*-
"""整集观感的观片包（skill ai_videos__整集观感）。

    python tools/viewing_packet.py <剧> <ep> [--video PATH]    # 出包
    python tools/viewing_packet.py <剧> <ep> --check           # viewing/review.md 还作不作数（视频变了即作废，exit 1）

<剧>：剧目录名、seedance.toml 的 alias，或剧目录路径。产物落 {集目录}/viewing/（animatic 落 viewing_animatic/，出片闸门读它；
post/proxy/ 下的代理片落 viewing_proxy/{代理片名}/，剪辑回路逐版比，不碰成片的审稿）：
sheets/shotNN.jpg（每段一张联系表，每 1–2 s 一帧，印成片时间码与此刻的台词；同一镜进片几次的按段序加 _NN）、transcript.md
（成片时间码上的台词 + 每镜意图 / 情绪标签 + 静音段）、packet.json（视频路径 + sha256 + 文件清单）。
视频默认 {ep}_final.mp4 → {ep}.mp4 → {ep}_animatic.mp4；镜边界读 {视频名}.segments.json（再退 {ep}.segments.json），
都没有或总长对不上就按各镜 mp4（没有就 md 的 duration_s）顺排，标为近似。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tomllib
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO / "tools", REPO / "tools" / "post", REPO / "tools" / "previz", REPO / "projects" / "ai_video_management"):
    sys.path.insert(0, str(_p))
import post_common as pc  # noqa: E402
import render_review  # noqa: E402
import segments  # noqa: E402
import subs  # noqa: E402
from libs.common import drama_ref  # noqa: E402
from planstyle import HALO_BG, INK, PAPER, font, halo  # noqa: E402

ANIMATIC = "animatic"
PROXY = "代理片"
VIDEOS: tuple[tuple[str, str], ...] = (("{ep}_final", "成片"), ("{ep}", "拼接版"), ("{ep}_animatic", ANIMATIC))
SEGMENTS_SUFFIX = ".segments.json"
VIEW_SUB = "viewing"
VIEW_SUB_ANIMATIC = "viewing_animatic"   # animatic 的观感审单独放：出片后成片的审稿不许覆盖它（tools/animatic.py 的出片闸门读它）
VIEW_SUB_PROXY = "viewing_proxy"         # 代理片（finish_ep --proxy）的观片包：每条代理片一个子目录，不覆盖成片与 animatic 的
SHEETS_SUB = "sheets"
REVIEW_NAME = "review.md"
PACKET_NAME = "packet.json"
SHA_TAG = "视频 sha256:"
SHOT_DIR = re.compile(r"shot\d+")
SEG_TOL_S = 0.2          # segments 总长与视频差超过这么多就不信它（实测 ep01：每镜短 0.13 s，累积到末镜错 0.9 s）
COLS = 5
CELL_W = 320
ANIMATIC_GRID = (2, 640)   # animatic 每格印着分镜段与动作摘要，320 宽读不清（ep01 审稿实测）
SILENCE_DB = -45
SILENCE_MIN_S = 1.5
FENCE = "`" * 3
MEASURED, PLANNED = "实测", "计划"
TAGS: dict[str, tuple[str, ...]] = {
    "好笑": ("好笑", "笑点", "喜剧", "幽默", "滑稽", "闹哄哄"),
    "好哭/暖": ("好哭", "哭", "暖", "失落", "心软", "心事"),
    "紧张/燃": ("紧张", "狠", "急", "高潮", "带劲", "最响", "发凉"),
    "安静": ("安静", "疲惫", "喘口气"),
}


@dataclass(frozen=True)
class Seg:
    shot: str
    start_s: float
    end_s: float

    @property
    def dur(self) -> float:
        return self.end_s - self.start_s


@dataclass(frozen=True)
class Line:
    who: str
    kind: str
    text: str
    meaning: str
    t0: float
    t1: float
    mark: str = PLANNED


@dataclass(frozen=True)
class ShotInfo:
    title: str
    intent: str
    tags: tuple[str, ...]
    rhythm: str


# ─────────────────────────── 定位 ───────────────────────────

def ep_name(arg: str) -> str:
    digits = re.sub(r"\D", "", arg)
    if not digits:
        raise SystemExit(f"集号认不出：{arg}")
    return "ep%02d" % int(digits)


def _aliases(d: Path) -> list[str]:
    cfg = d / "seedance.toml"
    return tomllib.loads(cfg.read_text(encoding="utf-8")).get("alias", []) if cfg.is_file() else []


def drama_dir(arg: str) -> Path:
    if Path(arg).is_dir():
        return Path(arg).resolve()
    hits = [d for d in drama_ref.drama_dirs(REPO) if d.name == arg or arg in _aliases(d)]
    if len(hits) != 1:
        raise SystemExit(f"剧「{arg}」对不上（剧目录名 / seedance.toml 的 alias / 路径）：{[rel(d) for d in hits] or '无'}")
    return hits[0]


def episode_dir(drama: Path, ep: str) -> Path:
    for sub in ("5_6_分镜与prompt/episodes", "episodes"):
        if (drama / sub / ep / "shots").is_dir():
            return drama / sub / ep
    hits = [d for d in drama.rglob(ep) if (d / "shots").is_dir()]
    if len(hits) != 1:
        raise SystemExit(f"{drama.name} 里带 shots/ 的 {ep} 目录有 {len(hits)} 个")
    return hits[0]


def resolve(drama_arg: str, ep_arg: str) -> tuple[Path, str, Path]:
    drama, ep = drama_dir(drama_arg), ep_name(ep_arg)
    return drama, ep, episode_dir(drama, ep)


rel = pc.rel          # tools/audience.py 用 vp.rel


def shot_dirs(ep_dir: Path) -> list[Path]:
    return sorted(d for d in (ep_dir / "shots").iterdir() if d.is_dir() and SHOT_DIR.fullmatch(d.name))


def find_video(ep_dir: Path, ep: str) -> tuple[Path, str]:
    for stem, kind in VIDEOS:
        p = ep_dir / (stem.format(ep=ep) + ".mp4")
        if p.is_file():
            return p, kind
    raise SystemExit(f"{rel(ep_dir)} 里没有 %s，用 --video 指定" % " / ".join(s.format(ep=ep) + ".mp4" for s, _ in VIDEOS))


def video_kind(video: Path, ep: str) -> str:
    if video.parent.name == pc.PROXY_SUB and video.parent.parent.name == pc.POST_DIR:
        return PROXY
    return next((k for s, k in VIDEOS if video.stem == s.format(ep=ep)), "指定视频")


def sha256(p: Path) -> str:
    with open(p, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def probe(p: Path, entries: str) -> str:
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "csv=p=0", str(p)],
                          capture_output=True, text=True, check=True).stdout.strip()


def duration(p: Path) -> float:
    return float(probe(p, "format=duration"))


# ─────────────────────────── 镜边界 ───────────────────────────

def segments_files(video: Path, ep_dir: Path, ep: str) -> list[Path]:
    """先找与视频同名的，再按 VIDEOS 的顺序找集目录里的。"""
    cands = [video.with_name(video.stem + SEGMENTS_SUFFIX)] + [ep_dir / (s.format(ep=ep) + SEGMENTS_SUFFIX) for s, _ in VIDEOS]
    return list(dict.fromkeys(c for c in cands if c.is_file()))


def read_segments(path: Path) -> tuple[list[Seg], float, bool]:
    return parse_segments(path.read_text(encoding="utf-8"))


def parse_segments(text: str) -> tuple[list[Seg], float, bool]:
    data = json.loads(text)
    segs = [Seg(s["shot"], float(s["start_s"]), float(s["end_s"])) for s in data["segments"]]
    return segs, float(data.get("total_s", segs[-1].end_s)), bool(data.get("approx", False))


def _md_duration(md: Path) -> float:
    m = re.search(r"^duration_s:\s*([\d.]+)", md.read_text(encoding="utf-8"), re.M) if md.is_file() else None
    if m is None:
        raise SystemExit(f"{rel(md)}：没有 mp4 也没有 duration_s，排不出镜边界")
    return float(m[1])


def load_segments(video: Path, secs: float, ep_dir: Path, ep: str) -> tuple[list[Seg], str, bool]:
    for f in segments_files(video, ep_dir, ep):
        segs, total, approx = read_segments(f)
        if abs(total - secs) <= SEG_TOL_S:
            return segs, f.name, approx
        print(f"不用 {f.name}：总长 {total:.2f}s，视频 {secs:.2f}s，差 > {SEG_TOL_S:g}s（镜边界会逐镜漂），改按各镜时长顺排")
    segs, t = [], 0.0
    for d in shot_dirs(ep_dir):
        if t >= secs - 0.5:
            break
        mp4 = d / f"{d.name}.mp4"
        dur = duration(mp4) if mp4.is_file() else _md_duration(d / f"{d.name}.md")
        segs.append(Seg(d.name, round(t, 3), round(min(t + dur, secs), 3)))
        t += dur
    return segs, "各镜时长顺排", True


# ─────────────────────────── 读 shot md / shotlist ───────────────────────────

def dub_lines(md: Path) -> list[Line]:
    """shot md 的台词与计划窗（pc.dialogue 读，与字幕、对齐同一个解析）。"""
    return [Line(ln.speaker or "?", ln.kind, ln.text, ln.zh, ln.t0, ln.t1) for ln in pc.dialogue(md)] if md.is_file() else []


def line_times(video: Path, ep_dir: Path, ep: str, segs: list[Seg]) -> dict[Seg, list[Line]]:
    """每段的台词与它在本段里的时刻（本段起点起算）。镜边界读自 v2 segments（带 take 与源片入 / 出点）时，对得上的句子取实测
    起止（subs.measured：对齐缓存；画外 / 独白取 TTS 实际摆位）标「实测」，其余取字幕同一套计划时间（subs.planned）标「计划」，
    起点不在本段保留区间的不列；
    v1 或按各镜时长顺排的，照旧全是 shot md 的计划窗。"""
    src = next((f for f in segments_files(video, ep_dir, ep) if read_segments(f)[0] == segs), None)
    parts = segments.read_parts(src) if src else None
    out: dict[Seg, list[Line]] = {}
    for k, s in enumerate(segs):
        md = ep_dir / "shots" / s.shot / f"{s.shot}.md"
        if parts is None:
            out[s] = dub_lines(md)
            continue
        p = parts[k]
        lines = pc.dialogue(md) if md.is_file() else []
        plan = {i: (a, a + d) for i, a, d, _cap in subs.planned(lines)}
        rows = []
        for i, (ln, span) in enumerate(zip(lines, subs.measured(ep_dir, p, lines))):
            a, b = span or plan[i]
            if subs.kept(p, a):
                rows.append(Line(ln.speaker, ln.kind, ln.text, ln.zh, round(a - p.src_in, 2), round(b - p.src_in, 2),
                                 MEASURED if span else PLANNED))
        out[s] = rows
    return out


def _shotlist_content(ep_dir: Path) -> dict[str, str]:
    sl = ep_dir / "shotlist.md"
    if not sl.is_file():
        return {}
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in sl.read_text(encoding="utf-8").splitlines() if r.startswith("|")]
    head = next((r for r in rows if r and r[0] == "镜号"), None)
    ci = next((i for i, c in enumerate(head or []) if "内容" in c or "情绪" in c), None)
    if ci is None:
        return {}
    return {r[0]: r[ci] for r in rows if SHOT_DIR.fullmatch(r[0]) and len(r) > ci}


def shot_infos(ep_dir: Path) -> dict[str, ShotInfo]:
    table = _shotlist_content(ep_dir)
    out: dict[str, ShotInfo] = {}
    for d in shot_dirs(ep_dir):
        md = d / f"{d.name}.md"
        text = md.read_text(encoding="utf-8") if md.is_file() else ""
        title, _, rest = table.get(d.name, "").partition("（")
        intent = rest[:-1] if rest.endswith("）") else rest
        title = title or (re.search(r"^title:\s*(.*)$", text, re.M) or [None, ""])[1]
        intent = intent or (re.search(r"\*\*情绪目的\*\*: (.*)", text) or [None, ""])[1]
        body = (re.search(FENCE + r"text\n(.*?)\n" + FENCE, text, re.S) or [None, ""])[1]
        rhythm = (re.search(r"^节奏: (.*)$", body, re.M) or [None, ""])[1]
        tags = tuple(t for t, words in TAGS.items() if any(w in intent for w in words))
        out[d.name] = ShotInfo(title.strip(), intent.strip(), tags, rhythm.strip())
    return out


# ─────────────────────────── 声音 ───────────────────────────

def has_audio(video: Path) -> bool:
    return "audio" in probe(video, "stream=codec_type")


def silences(video: Path, secs: float) -> list[tuple[float, float]]:
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(video), "-vn", "-af", f"silencedetect=noise={SILENCE_DB}dB:d={SILENCE_MIN_S}",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return pc.silences(r.stderr, secs)


# ─────────────────────────── 联系表 ───────────────────────────

def tc(t: float) -> str:
    return "%02d:%04.1f" % (int(t // 60), t % 60)


def step_for(dur: float) -> float:
    return 1.0 if dur <= 20 else 1.5 if dur <= 32 else 2.0


def _fit(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> str:
    if d.textlength(text, font=f) <= width:
        return text
    while text and d.textlength(text + "…", font=f) > width:
        text = text[:-1]
    return text + "…"


def _wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > width:
            lines.append(cur)
            cur = ""
        cur += ch
    return lines + [cur] if cur else lines


def sheet(video: Path, seg: Seg, info: ShotInfo, lines: list[Line], out: Path, grid_spec: tuple[int, int] = (COLS, CELL_W)) -> None:
    cols, cell_w = grid_spec
    step = step_for(seg.dur)
    local = sorted({round(max(0.05, min(k * step, seg.dur - 0.15)), 2) for k in range(math.ceil(seg.dur / step) + 1)})
    tile = out.with_name(out.stem + "_tile.png")
    render_review.frames(video, [seg.start_s + t for t in local], tile, cols, cell_w)
    grid = Image.open(tile).convert("RGB")
    ch = grid.height // -(-len(local) // cols)
    f_head, f_body, f_cell = font(22, bold=True), font(16), font(15)
    head = f"{seg.shot}《{info.title}》  {tc(seg.start_s)}–{tc(seg.end_s)}（{seg.dur:.1f} s，每 {step:g} s 一帧）"
    body = _wrap(ImageDraw.Draw(grid), "意图：" + (info.intent or "—") + ("　标签：" + " / ".join(info.tags) if info.tags else ""), f_body, grid.width - 24)
    top = 16 + 30 + 22 * len(body)
    canvas = Image.new("RGB", (grid.width, top + grid.height), PAPER)
    canvas.paste(grid, (0, top))
    d = ImageDraw.Draw(canvas)
    d.text((12, 10), head, font=f_head, fill=INK)
    for i, ln in enumerate(body):
        d.text((12, 42 + 22 * i), ln, font=f_body, fill=INK)
    for i, t in enumerate(local):
        x, y = (i % cols) * cell_w, top + (i // cols) * ch
        halo(d, (x + 6, y + 5), f"{tc(seg.start_s + t)}  +{t:.1f}s", f_cell, anchor="la")
        spoken = next((ln for ln in lines if ln.t0 <= t <= ln.t1), None)
        if spoken is not None:
            halo(d, (x + 6, y + ch - 6), _fit(d, f"{spoken.who}: {spoken.text}", f_cell, cell_w - 12), f_cell, anchor="ld")
    d.rectangle((0, top - 1, canvas.width, top), fill=HALO_BG)
    canvas.save(out, quality=85)
    tile.unlink()


# ─────────────────────────── transcript ───────────────────────────

def _cell(s: str) -> str:
    return s.replace("|", "\\|")


def transcript(ep: str, video: Path, kind: str, secs: float, sha: str, segs: list[Seg], src: str, approx: bool,
               infos: dict[str, ShotInfo], lines: dict[Seg, list[Line]], sil: list[tuple[float, float]] | None) -> str:
    n = len(infos)
    part = "，**这条视频只是本集的一段**" if len(segs) < n else ""
    L = [f"# {ep} 观片包 · 台词与意图（tools/viewing_packet.py 生成，勿手改）", "",
         f"- 视频：`{rel(video)}`（{kind}）· {secs:.1f} s · sha256 `{sha[:16]}…`",
         f"- 镜边界：{src}{'（近似）' if approx else ''}；覆盖 {segs[0].shot}–{segs[-1].shot}（{len(segs)} 镜），本集共 {n} 镜{part}",
         f"- 时间码＝成片时间 mm:ss.s；「镜内」＝本镜起点起算。台词时间末列标「{MEASURED}」＝强制对齐的实测起止（画外 / 独白＝TTS "
         f"实际摆位），标「{PLANNED}」＝shot md `## 台词配音 prompt` 的计划窗。",
         "- 标签由意图文字按关键词归类：" + " / ".join(TAGS) + "。",
         "- 声音：" + ("无音轨" if sil is None else f"静音段＝低于 {SILENCE_DB} dB 且 ≥ {SILENCE_MIN_S:g} s，列在各镜下"), "",
         "## 总表", "", "| 镜 | 成片时间 | 标题 | 标签 | 台词句数 |", "|---|---|---|---|---|"]
    for s in segs:
        i = infos.get(s.shot, ShotInfo("", "", (), ""))
        L.append(f"| {s.shot} | {tc(s.start_s)}–{tc(s.end_s)} | {_cell(i.title)} | {' / '.join(i.tags) or '—'} | {len(lines.get(s, []))} |")
    for s in segs:
        i = infos.get(s.shot, ShotInfo("", "", (), ""))
        L += ["", f"## {s.shot}《{i.title}》 {tc(s.start_s)}–{tc(s.end_s)}（{s.dur:.1f} s）", "",
              f"- 意图：{i.intent or '—'}", f"- 标签：{' / '.join(i.tags) or '—'}", f"- 节奏（镜内秒）：{i.rhythm or '—'}"]
        if sil is not None:
            mine = [(max(a, s.start_s), min(b, s.end_s)) for a, b in sil if a < s.end_s and b > s.start_s]
            L.append("- 静音：" + ("、".join(f"{tc(a)}–{tc(b)}" for a, b in mine) or "无"))
        L.append("")
        if lines.get(s):
            L += ["| 成片时间 | 镜内 | 角色 | 类型 | 台词 | 中文意思 | 时间 |", "|---|---|---|---|---|---|---|"]
            L += [f"| {tc(s.start_s + ln.t0)}–{tc(s.start_s + ln.t1)} | {ln.t0:g}–{ln.t1:g}s | {_cell(ln.who)} | {_cell(ln.kind)} | "
                  f"{_cell(ln.text)} | {_cell(ln.meaning)} | {ln.mark} |" for ln in lines[s]]
        else:
            L.append("（本镜无台词）")
    return "\n".join(L) + "\n"


# ─────────────────────────── review.md 作不作数 ───────────────────────────

def view_sub(kind: str, video: Path) -> str:
    return VIEW_SUB_ANIMATIC if kind == ANIMATIC else f"{VIEW_SUB_PROXY}/{video.stem}" if kind == PROXY else VIEW_SUB


def review_state(ep_dir: Path, sub: str = VIEW_SUB) -> tuple[bool, str]:
    view = ep_dir / sub
    if not (view / PACKET_NAME).is_file():
        return False, "还没出观片包"
    video = json.loads((view / PACKET_NAME).read_text(encoding="utf-8"))["video"]
    path = Path(video["path"]) if Path(video["path"]).is_absolute() else REPO / video["path"]
    if not path.is_file():
        return False, f"观片包里的视频不见了：{video['path']}"
    cur = sha256(path)
    if cur != video["sha256"]:
        return False, "视频在出包之后变了：重出观片包、重审"
    if not (view / REVIEW_NAME).is_file():
        return False, "还没有 review.md"
    m = re.search(re.escape(SHA_TAG) + r"\s*`?([0-9a-f]{64})", (view / REVIEW_NAME).read_text(encoding="utf-8"))
    if m is None:
        return False, f"review.md 头部缺「{SHA_TAG} …」"
    if m[1] != cur:
        return False, "review.md 审的是另一条视频，作废：重审"
    return True, f"review.md 有效（{video['path']}）"


def review_scores(ep_dir: Path) -> dict[str, float]:
    """review.md 注意力曲线表里每镜的分（第三列）。"""
    p = ep_dir / VIEW_SUB / REVIEW_NAME
    rows = re.findall(r"^\|\s*(shot\d+)\s*\|[^|\n]*\|\s*(\d+(?:\.\d+)?)\s*\|", p.read_text(encoding="utf-8"), re.M) if p.is_file() else []
    return {s: float(v) for s, v in rows}


# ─────────────────────────── 出包 ───────────────────────────

def build(drama_arg: str, ep_arg: str, video_arg: str | None) -> Path:
    drama, ep, ep_dir = resolve(drama_arg, ep_arg)
    if video_arg:
        video = Path(video_arg).resolve()
        kind = video_kind(video, ep)
        if not video.is_file():
            raise SystemExit(f"没有这个视频：{video_arg}")
    else:
        video, kind = find_video(ep_dir, ep)
    secs, sha = duration(video), sha256(video)
    segs, src, approx = load_segments(video, secs, ep_dir, ep)
    infos = shot_infos(ep_dir)
    lines = line_times(video, ep_dir, ep, segs)
    sil = silences(video, secs) if has_audio(video) else None
    view = ep_dir / view_sub(kind, video)
    shutil.rmtree(view / SHEETS_SUB, ignore_errors=True)
    (view / SHEETS_SUB).mkdir(parents=True)
    files = []
    times = Counter(s.shot for s in segs)
    for k, s in enumerate(segs, 1):
        out = view / SHEETS_SUB / (f"{s.shot}.jpg" if times[s.shot] == 1 else f"{s.shot}_{k:02d}.jpg")
        sheet(video, s, infos.get(s.shot, ShotInfo("", "", (), "")), lines[s], out,
              ANIMATIC_GRID if kind == ANIMATIC else (COLS, CELL_W))
        files.append(out.relative_to(view).as_posix())
    (view / "transcript.md").write_text(transcript(ep, video, kind, secs, sha, segs, src, approx, infos, lines, sil), encoding="utf-8")
    files.insert(0, "transcript.md")
    packet = {"version": 1, "drama": rel(drama), "ep": ep,
              "video": {"path": rel(video), "kind": kind, "sha256": sha, "duration_s": round(secs, 3), "audio": sil is not None},
              "segments": {"source": src, "approx": approx, "shots": [asdict(s) for s in segs]},
              "shots_in_episode": len(infos), "review": REVIEW_NAME, "files": files}
    (view / PACKET_NAME).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ok, why = review_state(ep_dir, view.relative_to(ep_dir).as_posix())
    if (view / REVIEW_NAME).is_file() and not ok:
        print("注意：" + why)
    return view


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="整集观感的观片包（ai_videos__整集观感）")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--video")
    ap.add_argument("--check", action="store_true", help="只查 viewing/review.md 还作不作数")
    ap.add_argument("--animatic", action="store_true", help="配 --check：查 viewing_animatic/review.md")
    a = ap.parse_args()
    if a.check:
        ok, why = review_state(resolve(a.drama, a.ep)[2], VIEW_SUB_ANIMATIC if a.animatic else VIEW_SUB)
        print(("有效：" if ok else "无效：") + why)
        return 0 if ok else 1
    view = build(a.drama, a.ep, a.video)
    print(f"观片包 → {rel(view)}（{PACKET_NAME}、transcript.md、{SHEETS_SUB}/*.jpg）")
    print(f"下一步：按 ai_videos__整集观感 派没写过这集的子代理只看这个目录判读，结论写 {rel(view / REVIEW_NAME)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
