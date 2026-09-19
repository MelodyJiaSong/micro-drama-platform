# -*- coding: utf-8 -*-
"""sk2 白模流水线驱动：三视图 → Rodin GLB → 闸门 → whitemodel/{name}.blend。

用法（仓库根目录）：
    python tools/build_sk2_whitemodels.py --fetch      # 只跑网络端（Rodin），不开 Blender
    python tools/build_sk2_whitemodels.py --gate       # 只跑闸门（开 Blender）
    python tools/build_sk2_whitemodels.py --fetch --gate
    python tools/build_sk2_whitemodels.py --only p16,p19

为什么分两段
------------
`ai_video.md` rule 4h ⑥：**previz 批量任务不许重叠跑**——`TaskStop` 杀 shell 不杀已 spawn 的
`blender.exe`，重叠会报假失败。闸门也是 Blender，所以它与 previz 批次**必须错开**；
而 Rodin 那一段是纯网络，随时可跑。两段因此拆开。

fit=stretch 的理由
------------------
`object_inventory.toml` 里的尺寸是**作者按画面推的估值**（多条标 ⚠️），不是实测。
生成网格的比例与它对不上时，对 previz 有意义的是**占位体积与城市布局槽一致**，
不是让网格去迁就一个本来就不确定的数。所以批量走 `--fit stretch`；
`--aspect-tol` 仍会对「被压成饼」的极端情形报 warning。
真要追究比例，回头改 `object_inventory.toml` 的尺寸重跑，而不是改这里。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
A = REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "2_世界观人设"
PROPS = A / "props"
INV = A / "object_inventory.toml"
BLENDER = os.environ.get("BLENDER_BIN") or r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"


def objects():
    inv = tomllib.loads(INV.read_text(encoding="utf-8"))
    out = {}
    for o in inv.get("object", []):
        out[o["key"]] = o
    return out


def prop_dir(key):
    for d in sorted(PROPS.iterdir()):
        if d.is_dir() and d.name.split("_")[0] == key:
            return d
    return None


def run(cmd, timeout=1800):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="跑 Rodin 出 raw.glb（纯网络）")
    ap.add_argument("--gate", action="store_true", help="跑白模闸门（开 Blender，勿与 previz 重叠）")
    ap.add_argument("--only", default="", help="逗号分隔的 pN")
    ap.add_argument("--tier", default="Regular", choices=("Sketch", "Regular"))
    args = ap.parse_args()
    if not (args.fetch or args.gate):
        args.fetch = args.gate = True

    keep = {x.strip() for x in args.only.split(",") if x.strip()}
    objs = objects()
    out = sys.stdout.buffer
    ok_fetch = ok_gate = skipped = failed = 0

    for key, o in objs.items():
        if keep and key not in keep:
            continue
        d = prop_dir(key)
        if not d:
            continue
        imgs = sorted(d.glob(f"{key}-*.png"))
        wm = d / "whitemodel"
        wm.mkdir(exist_ok=True)
        raw = wm / "raw.glb"
        blend = wm / f"{d.name}.blend"

        if args.fetch:
            if len(imgs) < 3:
                out.write(f"· {d.name} 跳过（只有 {len(imgs)} 张图，需要三视图）\n".encode())
                skipped += 1
            elif raw.exists() and raw.stat().st_size > 100_000:
                out.write(f"· {d.name} raw.glb 已存在，跳过\n".encode())
            else:
                size = o.get("size", [1, 1, 1])
                m = max(size) or 1.0
                bbox = [round(v / m, 3) for v in size]
                cmd = [sys.executable, str(REPO / "tools" / "hyper3d_fetch.py"),
                       "--prompt", o.get("en", o.get("name", key)),
                       "--bbox", str(bbox[0]), str(bbox[1]), str(bbox[2]),
                       "--tier", args.tier, "--out", str(raw)]
                for im in imgs[:3]:
                    cmd += ["--image", str(im)]
                rc, log = run(cmd)
                if rc == 0 and raw.exists():
                    out.write(f"✓ {d.name} raw.glb {raw.stat().st_size//1024} KB\n".encode())
                    ok_fetch += 1
                else:
                    out.write(f"✗ {d.name} Rodin 失败：{log.strip().splitlines()[-1][:160] if log.strip() else rc}\n".encode())
                    failed += 1

        if args.gate:
            if not raw.exists():
                continue
            cmd = [BLENDER, "-b", "--factory-startup", "--python",
                   str(REPO / "tools" / "whitemodel_normalize.py"), "--",
                   "--src", str(raw), "--spec", str(d / "object.toml"),
                   "--out", str(blend), "--fit", "stretch"]
            rc, log = run(cmd)
            tail = [l for l in log.splitlines() if l.strip().startswith(("✓", "✗", "[whitemodel]"))]
            passed = blend.exists() and not any("验收未通过" in l for l in tail)
            out.write(f"{'✓' if passed else '△'} {d.name} 闸门：".encode())
            out.write((("通过" if passed else "有失败项（blend 仍已写出，供人眼看）") + "\n").encode())
            for l in tail:
                if l.strip().startswith("✗"):
                    out.write(("    " + l.strip() + "\n").encode())
            ok_gate += 1

    out.write(f"\n合计：Rodin 成功 {ok_fetch} · 闸门跑过 {ok_gate} · 跳过 {skipped} · 失败 {failed}\n".encode())


if __name__ == "__main__":
    main()
