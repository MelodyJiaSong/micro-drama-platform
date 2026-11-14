"""TripoSR 输入剪影的宽高比（bible §7 第 3a 条：模型侧视长高比与参考图剪影差 ≤ 5%）。

用 TripoSR 环境跑（要 numpy、Pillow）：
    .cache/venvs/triposr/Scripts/python -I ai_videos/zhenshi_chidu/_tools/silhouette.py <models_ai 目录>
读每个 `<stem>_input.png`（local_3d.py 去背景后合成在 0.5 灰底上的图），前景 = 与灰底差 > 6/255 的像素；
写 `<目录>/silhouette.json`：{stem: {"w_px", "h_px", "aspect_wh"}}。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

GRAY = 127
THRESH = 6


def aspect(path: Path) -> dict:
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    fg = np.abs(a - GRAY).max(axis=2) > THRESH
    ys, xs = np.where(fg)
    w, h = int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)
    return {"w_px": w, "h_px": h, "aspect_wh": round(w / h, 4)}


def main() -> None:
    d = Path(sys.argv[1])
    out = {p.name[: -len("_input.png")]: aspect(p) for p in sorted(d.glob("*_input.png"))}
    (d / "silhouette.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in out.items():
        print(k, v["aspect_wh"])


if __name__ == "__main__":
    main()
