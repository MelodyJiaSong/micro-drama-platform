# -*- coding: utf-8 -*-
"""把本剧 props/ 里的物件「归类」到每个引用它的 bg 目录下——**只放链接，不复制**（rule 4b-B / 4i ①）。

一件物件（`props/p{N}_{名}/`，follow-up 013）常被很多块引用（艾尔文的橡树 17 处），复制会漂；
所以每个 bg 目录下建 `assets/`，每个引用资产的编号块一个子目录，里面是指向资产库文件的
`*.link.json`（`libs/common/asset_link.py` 的格式：`{target, note}`），webapp 树把它渲成可预览的叶子：

    bg4_闪金镇/assets/b01_两层旅店（正门朝西）/
        p15-1_正面.png.link.json   p15-2_侧面.png.link.json   p15-3_背面.png.link.json
        p15.glb.link.json          p15_两层石木旅店.md.link.json

链接只指向**已经存在**的文件（还没出图 / 出模的就不建那一条），重跑即补；块改了资产或删了，旧链接目录一并清掉。

用法（仓库根目录）：
    python tools/link_bg_assets.py [scenes 根 | 区目录 | bg 目录]      # 默认 shengji_zhilu 全部 scenes
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tomllib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import props_lib  # noqa: E402
DEFAULT = REPO / "ai_videos" / "shengji_zhilu" / "2_世界观人设" / "scenes"
LINKS_DIR = "assets"
BAD = re.compile(r'[\\/:*?"<>|_\s]+')


def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def asset_files(bg: Path, key: str) -> list[Path]:
    d = props_lib.find(bg, key)
    if d is None:
        return []
    out = [d / f"{d.name}.md"] + sorted(d.glob(f"{key}-[123]_*.png")) + [d / "mesh" / f"{key}.glb"]
    return [p for p in out if p.is_file()]


def link_bg(bg: Path) -> tuple[int, int]:
    toml_p = bg / "planning" / "blocks.toml"
    if not toml_p.is_file():
        return 0, 0
    cfg = tomllib.loads(toml_p.read_text(encoding="utf-8"))
    want: dict[str, list[Path]] = {}
    for b in cfg.get("block", []):
        keys = [p["asset"] for p in b.get("parts", [])] or ([b["asset"]] if b.get("asset") else [])
        if b.get("kind") != "asset" or not keys:
            continue
        files = [f for k in dict.fromkeys(keys) for f in asset_files(bg, k)]   # parts：块里每样东西各自的文件
        if files:
            want[f"{b['id']}_{BAD.sub('', b['name'])[:40]}"] = files
    root = bg / LINKS_DIR
    if root.is_dir():                                  # 块改了资产 / 删了：旧链接目录清掉
        for d in root.iterdir():
            if d.is_dir() and d.name not in want:
                shutil.rmtree(d)
    n = 0
    for sub, files in want.items():
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        keep = set()
        for f in files:
            lp = d / f"{f.name}.link.json"
            keep.add(lp.name)
            body = json.dumps({"target": rel(f), "note": "本剧 props · 本块引用的物件（不复制，rule 4b-B）"},
                              ensure_ascii=False, indent=2) + "\n"
            if not lp.is_file() or lp.read_text(encoding="utf-8") != body:
                lp.write_text(body, encoding="utf-8", newline="\n")
            n += 1
        for old in d.glob("*.link.json"):
            if old.name not in keep:
                old.unlink()
    if root.is_dir() and not any(root.iterdir()):
        root.rmdir()
    return len(want), n


def main() -> int:
    scope = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT
    bgs = [scope] if (scope / "planning" / "blocks.toml").is_file() else sorted(
        p.parent.parent for p in scope.rglob("planning/blocks.toml")
        if re.match(r"^bg\d+_[^_]+$", p.parent.parent.name))
    nb = nl = nbg = 0
    for bg in bgs:
        b, l = link_bg(bg)
        if b:
            nbg += 1
        nb += b
        nl += l
    print(f"bg {nbg} 个有资产块 · 块 {nb} 个 · 链接 {nl} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
