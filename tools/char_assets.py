# -*- coding: utf-8 -*-
"""人物资产一条龙（任一部剧）：立绘 → 4 秒建立视频 → 三视图；已有的跳过，可中断可续跑。

    python tools/char_assets.py status 魔兽世界
    python tools/char_assets.py run    魔兽世界 [--only c1,m3] [--steps portrait,video,views] [--dry-run]
    python tools/char_assets.py sheet  魔兽世界 [--only …] [--what portrait|views]   # 拼审图用的联系表，打印 png 路径

剧名 ＝ `ai_videos/` 下的目录名、相对路径（`shikong_lvxing/sk2`），或该剧 `seedance.toml` 的 alias（`seedance_kit.find_drama`）。
每一步只做缺的：
  portrait  卡里有立绘块、还没有 `{卡目录}.png`        → `tools/gen_char_images.py run`（引擎按 rule 4l，画幅读卡）
  video     有 `{卡目录}_turntable` 块、有立绘、还没有原始建立视频 → `tools/gen_turntable_videos.py`（Seedance 2.5 · 720p · 画幅读卡）
  views     有建立视频、`views/` 里还没有正面帧       → 网页端 `python -m apps.cli.extract_views`（与 🎞 一键提取同一个命令）
整轮持有本剧的 `.char_assets.lock`：同一部剧两个会话同时跑会互相覆盖（szzl 2026-09-30），第二个直接拒绝。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_char_images as gci  # noqa: E402
from tools import gen_turntable_videos as gtv  # noqa: E402
from tools import seedance_kit as kit  # noqa: E402

AI = REPO / "ai_videos"
WEBAPP = REPO / "projects" / "ai_video_management"
WEBAPP_PY = WEBAPP / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
CREDIT_PER_VIDEO = 80                  # seedance2.5 · 4 s · 720p（2026-09-30 实测）
SHEET_ROWS = 8
TILE = (240, 427)


def drama_rel(name: str) -> str:
    """剧名 / 别名 / 相对路径 → 相对 ai_videos/ 的剧目录（characters 所在那一层）。"""
    top = AI / name if (AI / name).is_dir() else kit.find_drama(name.split("/")[0])
    if "/" in name and not (AI / name).is_dir():
        top = top / name.split("/", 1)[1]
    hits = sorted(c.parent.parent for c in [top / "2_世界观人设" / "characters", *top.glob("*/2_世界观人设/characters")]
                  if c.is_dir())
    if len(hits) != 1:
        raise SystemExit(f"{top.relative_to(AI)} 下找到 {len(hits)} 个 2_世界观人设/characters："
                         f"{[h.relative_to(AI).as_posix() for h in hits]}——用相对路径指定一季，如 shikong_lvxing/sk2")
    return hits[0].relative_to(AI).as_posix()


@dataclass(frozen=True)
class Row:
    dir: Path
    portrait_block: bool
    portrait: bool
    turntable_block: bool
    video: bool
    views: bool

    @property
    def key(self) -> str:
        return self.dir.name.split("_")[0]

    @property
    def needs_portrait(self) -> bool:
        """已有建立视频的卡，长相已由视频定下；再出一张立绘只会多一张不一样的脸（szzl c1–c18 就没有 png）。"""
        return self.portrait_block and not self.portrait and not self.video


def rows(chars: Path, only: list[str]) -> list[Row]:
    head = gci.KINDS["characters"][0]
    out = []
    for d in sorted(chars.iterdir(), key=lambda p: (p.name[0], int("".join(filter(str.isdigit, p.name.split("_")[0])) or 0))):
        md = d / f"{d.name}.md"
        if not (d.is_dir() and md.is_file()) or (only and d.name.split("_")[0] not in only):
            continue
        out.append(Row(d, head.search(md.read_text(encoding="utf-8")) is not None, (d / f"{d.name}.png").is_file(),
                       gtv.has_block(d), bool(gtv.originals(d)), gci.anchor_frame(d, "front").is_file()))
    return out


def status(rs: list[Row]) -> None:
    mark = {True: "✓", False: "·"}
    print(f"  {'卡':<28}立绘块 立绘 视频块 视频 三视图（有视频的卡不补立绘）")
    for r in rs:
        print(f"  {r.dir.name:<28}{mark[r.portrait_block]:^5}{mark[r.portrait]:^4}{mark[r.turntable_block]:^6}"
              f"{mark[r.video]:^4}{mark[r.views]:^6}")
    need_p = [r for r in rs if r.needs_portrait]
    need_v = [r for r in rs if r.turntable_block and not r.video]
    need_w = [r for r in rs if not r.views and (r.video or r.turntable_block)]
    print(f"\n  共 {len(rs)} 张卡 · 缺立绘 {len(need_p)} · 缺建立视频 {len(need_v)}（约 {len(need_v) * CREDIT_PER_VIDEO} 分）"
          f" · 缺三视图 {len(need_w)}")
    for label, bad in (("没有立绘块", [r for r in rs if not r.portrait_block]),
                       ("没有 turntable 块（按 stage2 模板补进卡里才能出视频）", [r for r in rs if not r.turntable_block])):
        if bad:
            print(f"  ⚠ {label}：{', '.join(r.dir.name for r in bad)}")


def portraits(rel: str, rs: list[Row], dry: bool) -> bool:
    keys = [r.key for r in rs if r.needs_portrait]
    if not keys:
        print("  立绘：都有了")
        return True
    print(f"  立绘：要出 {len(keys)} 张 {keys}", flush=True)
    if dry:
        return True
    p = subprocess.run([sys.executable, str(REPO / "tools" / "gen_char_images.py"), "run", "--drama", rel,
                        "--only", ",".join(keys)], cwd=REPO)
    return p.returncode == 0


def extract_views(dirs: list[Path]) -> int:
    if not dirs:
        return 0
    if not WEBAPP_PY.is_file():
        raise SystemExit(f"没有网页端的虚拟环境 {WEBAPP_PY}（在 {WEBAPP.relative_to(REPO)} 里 `uv sync`）")
    rels = [gtv.originals(d)[0].relative_to(REPO).as_posix() for d in dirs]
    p = subprocess.run([str(WEBAPP_PY), "-m", "apps.cli.extract_views", *rels], cwd=WEBAPP,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    bad = 0
    for line in p.stdout.splitlines():
        r = json.loads(line)
        name = Path(r["src"]).parent.name
        if r.get("error") or r.get("failures"):
            bad += 1
            print(f"  ✗ {name} 三视图：{r.get('error') or r.get('failures')}", flush=True)
        else:
            print(f"  ✓ {name} 三视图 {len(r['views'])}/3", flush=True)
    if p.returncode and not p.stdout:
        raise SystemExit(f"extract_views 起不来：{p.stderr[-600:]}")
    return bad


def run(rel: str, only: list[str], steps: set[str], model: str, dry: bool) -> int:
    chars = AI / rel / "2_世界观人设" / "characters"
    bad = 0
    with gtv.DramaLock(chars):
        if "portrait" in steps and not portraits(rel, rows(chars, only), dry):
            bad += 1
        if "video" in steps:
            dirs = [d for d in gtv.todo(chars, only) if (d / f"{d.name}.png").is_file() or gci.anchor_frame(d, "front").is_file()]
            print(f"  建立视频：要出 {len(dirs)} 条（约 {len(dirs) * CREDIT_PER_VIDEO} 分）{[d.name for d in dirs]}", flush=True)
            for d in [] if dry else dirs:
                res = gtv.one(d, False, model)
                print(f"  {d.name}: {res}", flush=True)
                if not res.startswith("OK"):
                    bad += 1
                elif "views" in steps:
                    bad += extract_views([d])
        if "views" in steps:
            left = [r.dir for r in rows(chars, only) if r.video and not r.views]
            print(f"  三视图：要补 {len(left)} 个", flush=True)
            if not dry:
                bad += extract_views(left)
    print(f"\n完成，失败 {bad}" if bad else "\n完成")
    return 1 if bad else 0


def sheet(rel: str, only: list[str], what: str) -> None:
    """审图联系表：portrait ＝ 立绘一格一张、每行 8 张；views ＝ 每行一张卡「立绘 | 正 | 侧 | 背」。每页 8 行。"""
    rs = [r for r in rows(AI / rel / "2_世界观人设" / "characters", only) if r.portrait and (what == "portrait" or r.views)]
    if not rs:
        raise SystemExit("范围里没有可拼的图")
    cells = [[(r.dir.name, r.dir / f"{r.dir.name}.png")] + ([] if what == "portrait" else
             [(role, gci.anchor_frame(r.dir, role)) for role in ("front", "side", "back")]) for r in rs]
    if what == "portrait":
        cells = [sum(cells[k:k + 8], []) for k in range(0, len(cells), 8)]
    out_dir = Path(tempfile.gettempdir()) / "char_assets"
    out_dir.mkdir(exist_ok=True)
    w, h = TILE
    for page, start in enumerate(range(0, len(cells), SHEET_ROWS)):
        grid = cells[start:start + SHEET_ROWS]
        img = Image.new("RGB", (w * max(map(len, grid)), h * len(grid)), "gray")
        draw = ImageDraw.Draw(img)
        for y, row in enumerate(grid):
            for x, (label, path) in enumerate(row):
                tile = Image.open(path).convert("RGB")
                tile.thumbnail(TILE)
                img.paste(tile, (x * w + (w - tile.width) // 2, y * h + (h - tile.height) // 2))
                draw.text((x * w + 4, y * h + 4), label, fill="white", stroke_width=2, stroke_fill="black")
        out = out_dir / f"{rel.replace('/', '_')}_{what}_{page + 1}.png"
        img.save(out)
        print(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("status", "run", "sheet"))
    ap.add_argument("drama", help="目录名、相对路径或 seedance.toml alias，如 魔兽世界 / shengji_zhilu / shikong_lvxing/sk2")
    ap.add_argument("--only", default="", help="逗号分隔的卡号，如 c1,m3")
    ap.add_argument("--steps", default="portrait,video,views")
    ap.add_argument("--model", default="seedance2.5", choices=gtv.MODELS)
    ap.add_argument("--what", default="views", choices=("portrait", "views"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    rel = drama_rel(args.drama)
    only = [s for s in args.only.split(",") if s]
    print(f"剧：ai_videos/{rel}")
    if args.step == "status":
        status(rows(AI / rel / "2_世界观人设" / "characters", only))
        return 0
    if args.step == "sheet":
        sheet(rel, only, args.what)
        return 0
    steps = {s.strip() for s in args.steps.split(",") if s.strip()}
    if steps - {"portrait", "video", "views"}:
        raise SystemExit(f"--steps 只认 portrait / video / views：{steps}")
    return run(rel, only, steps, args.model, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
