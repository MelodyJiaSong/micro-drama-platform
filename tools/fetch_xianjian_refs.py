"""Build the per-scene visual reference library for 仙剑奇侠传一 from the
98 柔情版 纯剧情剪辑 playlist.

Each playlist part is fetched at low resolution, sampled to one JPEG every
`--interval` seconds, and then discarded — only the frames are kept. The frames
are a rebuildable derived cache (gitignored, skipped by assets_sync), never a
state surface: delete `refs_game98/` and re-run to get it back.

    python tools/fetch_xianjian_refs.py            # all parts, 1 frame / 5 s
    python tools/fetch_xianjian_refs.py --parts 1 2
    python tools/fetch_xianjian_refs.py --interval 10 --force
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

PLAYLIST_URL: str = (
    "https://www.youtube.com/playlist?list=PLYgfrA_ODMo_EdKuGWCThtuo8iXj0IwQ9"
)
# Part 7 of the playlist was made private by its uploader. This chapter-segmented
# longplay of the same 98 柔情版 covers the gap and doubles as a second reference set;
# its 61 chapter markers are indexed in 0_原作资料/longplay_chapters.md.
LONGPLAY_ID: str = "qdSHOKnHw00"
_SOURCE_ROOT: Path = (
    Path(__file__).resolve().parents[1]
    / "ai_videos" / "xianjian_yi" / "_series" / "0_原作资料"
)
OUT_ROOT: Path = _SOURCE_ROOT / "refs_game98"
LONGPLAY_ROOT: Path = _SOURCE_ROOT / "refs_longplay"
FRAME_WIDTH: int = 854
DOWNLOAD_FORMAT: str = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"


@dataclass(frozen=True)
class Part:
    index: int
    video_id: str
    title: str
    duration: int | None

    @property
    def slug(self) -> str:
        return f"p{self.index:02d}"

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"


def list_parts() -> list[Part]:
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--dump-json", PLAYLIST_URL],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    parts: list[Part] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if not entry.get("id"):
            continue
        parts.append(Part(
            index=int(entry.get("playlist_index") or len(parts) + 1),
            video_id=str(entry["id"]),
            title=str(entry.get("title") or ""),
            duration=int(entry["duration"]) if entry.get("duration") else None,
        ))
    return parts


def download(part: Part, work_dir: Path) -> Path | None:
    target = work_dir / f"{part.slug}.mp4"
    result = subprocess.run(
        ["yt-dlp", "-f", DOWNLOAD_FORMAT, "--merge-output-format", "mp4",
         "--no-playlist", "--retries", "10", "--fragment-retries", "10",
         "-o", str(target), part.url],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0 or not target.is_file():
        print(f"  ! download failed: {result.stderr.strip().splitlines()[-1:]}", flush=True)
        return None
    return target


def sample(source: Path, out_dir: Path, interval: int) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(source),
         "-vf", f"fps=1/{interval},scale={FRAME_WIDTH}:-2",
         "-q:v", "4", "-frame_pts", "0",
         str(out_dir / "f%05d.jpg"), "-y"],
        check=True,
    )
    frames = sorted(out_dir.glob("f*.jpg"))
    for ordinal, frame in enumerate(frames):
        stamp = ordinal * interval
        renamed = out_dir / f"t{stamp:05d}.jpg"
        if frame != renamed:
            frame.replace(renamed)
    return len(frames)


def write_index(parts: list[Part], interval: int) -> None:
    lines = [
        "# 98 柔情版 纯剧情剪辑 · 逐场景参考帧库（索引）",
        "",
        f"> 来源播放列表：{PLAYLIST_URL}",
        f"> 采样：每 {interval} 秒一帧，宽 {FRAME_WIDTH}px。文件名 `t{{累计秒数}}.jpg`。",
        "> **derived cache**：gitignored、不进 R2，删掉重跑 `python tools/fetch_xianjian_refs.py` 即可复原。",
        "> 用途：分镜取景时对照原作构图/场景长相/过场动画，**不是**剧情权威——剧情与台词以 `game98/` 为准。",
        "",
        "| 段 | 目录 | 时长 | 帧数 | 原标题 |",
        "|---|---|---|---|---|",
    ]
    for part in parts:
        folder = OUT_ROOT / part.slug
        count = len(list(folder.glob("t*.jpg"))) if folder.is_dir() else 0
        length = f"{part.duration // 60}分{part.duration % 60:02d}秒" if part.duration else "—"
        lines.append(f"| {part.index:02d} | `{part.slug}/` | {length} | {count} | {part.title} |")
    lines.append("")
    lines.append("## 定位方法")
    lines.append("")
    lines.append(
        f"全片按段顺序即游戏进度顺序。要找某一场戏：先在 `../game98/chNN_*.md` 定位章与场景序号，"
        f"再按本表的段时长折算大致落点，打开对应 `t*.jpg` 附近几帧即可。"
    )
    (OUT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def sample_longplay(interval: int, force: bool) -> int:
    part = Part(index=0, video_id=LONGPLAY_ID, title="98 柔情版 LongPlay", duration=None)
    existing = len(list(LONGPLAY_ROOT.glob("t*.jpg"))) if LONGPLAY_ROOT.is_dir() else 0
    if existing and not force:
        print(f"[longplay] {existing} frames already present — skip", flush=True)
        return 0
    print("[longplay] downloading ...", flush=True)
    with tempfile.TemporaryDirectory(prefix="xjlong_") as tmp:
        source = download(part, Path(tmp))
        if source is None:
            return 1
        count = sample(source, LONGPLAY_ROOT, interval)
    print(f"[longplay] {count} frames", flush=True)
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=5)
    parser.add_argument("--parts", type=int, nargs="*", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--longplay", action="store_true",
                        help="sample the chapter-segmented longplay instead of the playlist")
    args = parser.parse_args()

    if shutil.which("yt-dlp") is None or shutil.which("ffmpeg") is None:
        print("yt-dlp and ffmpeg are both required", file=sys.stderr)
        return 1

    if args.longplay:
        return sample_longplay(args.interval, args.force)

    parts = list_parts()
    if args.parts:
        wanted = set(args.parts)
        parts = [p for p in parts if p.index in wanted]
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"{len(parts)} part(s) to sample into {OUT_ROOT}", flush=True)

    for part in parts:
        out_dir = OUT_ROOT / part.slug
        existing = len(list(out_dir.glob("t*.jpg"))) if out_dir.is_dir() else 0
        if existing and not args.force:
            print(f"[{part.slug}] {existing} frames already present — skip", flush=True)
            continue
        print(f"[{part.slug}] downloading {part.title} ...", flush=True)
        with tempfile.TemporaryDirectory(prefix="xjrefs_") as tmp:
            source = download(part, Path(tmp))
            if source is None:
                continue
            count = sample(source, out_dir, args.interval)
        print(f"[{part.slug}] {count} frames", flush=True)

    write_index(parts, args.interval)
    total = sum(len(list(d.glob("t*.jpg"))) for d in OUT_ROOT.glob("p*") if d.is_dir())
    print(f"done — {total} frames total", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
