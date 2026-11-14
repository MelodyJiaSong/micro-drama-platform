# -*- coding: utf-8 -*-
"""本地单图转 3D（TripoSR：代码与权重 MIT；paid_services.md 商业用途一节登记）。

只用完全开源的本地模型。独立环境跑（Python 3.11，torch cu128）：
    .cache/venvs/triposr/Scripts/python tools/local_3d.py --image <参考图.png> --out <模型.glb> [--mc-resolution 256]
代码检出 .cache/src/TripoSR，权重 .cache/models/triposr/（stabilityai/TripoSR），DINO 只取 config
（.cache/models/dino-vitb16/config.json，facebook/dino-vitb16，Apache-2.0）；只读本地，不连 Hugging Face。
本机无 CUDA 编译器，原依赖 torchmcubes 编译不了，等价换成 scikit-image（BSD-3）的 marching cubes。
去背景只用 rembg 的 isnet-general-use（IS-Net/DIS，Apache-2.0），模型放 .cache/models/rembg/，sha256 校验；
不许用 rembg 默认模型：2.0.87 起默认 bria-rmbg（BRIA RMBG 2.0，仅限非商用），缺文件就报错，不自动下载。

产物：<out>（.glb 或 .obj，带顶点色）与同名 .json（模型、代码提交、权重 sha256、输入 sha256、参数、
顶点与面数、输出 sha256）。输入与参数都没变且产物还在时跳过。本地运行不收费、不走请求日志；
参考图若由收费服务生成，其请求日志在参考图自己的归属目录。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / ".cache" / "src" / "TripoSR"
MODEL = REPO / ".cache" / "models" / "triposr"
DINO_CONFIG = REPO / ".cache" / "models" / "dino-vitb16" / "config.json"
PARAM_KEYS = ("mc_resolution", "foreground_ratio", "remove_bg", "chunk_size")
PIPELINE_VERSION = 2  # 2：导出前转成 glTF 的 Y 轴朝上（同官方 gradio 演示）、体积为负时翻面
REMBG_DIR = REPO / ".cache" / "models" / "rembg"
REMBG_MODEL = "isnet-general-use"  # Apache-2.0；换模型须先核许可
REMBG_SHA256 = "60920e99c45464f2ba57bee2ad08c919a52bbf852739e96947fbb4358c0d964a"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _install_shims() -> None:
    """torchmcubes → scikit-image；DINO config → 本地文件。"""
    import numpy as np
    import torch
    from skimage.measure import marching_cubes as sk_mc

    def marching_cubes(vol: "torch.Tensor", thresh: float):
        v, f, _, _ = sk_mc(vol.detach().cpu().numpy().astype(np.float32), level=thresh)
        # torchmcubes 返回顶点坐标为 (k, j, i)；TripoSR 之后会再按 [2, 1, 0] 换回 (i, j, k)
        verts = torch.from_numpy(np.ascontiguousarray(v[:, ::-1])).float()
        faces = torch.from_numpy(np.ascontiguousarray(f[:, ::-1])).long()
        return verts, faces

    sys.modules["torchmcubes"] = types.SimpleNamespace(marching_cubes=marching_cubes)
    sys.path.insert(0, str(SRC))
    import tsr.models.tokenizers.image as tok
    tok.hf_hub_download = lambda **_: str(DINO_CONFIG)


def _prepare(image_path: Path, remove_bg: bool, ratio: float):
    import numpy as np
    import rembg
    from PIL import Image
    from tsr.utils import remove_background, resize_foreground
    img = Image.open(image_path)
    if remove_bg:
        onnx = REMBG_DIR / f"{REMBG_MODEL}.onnx"
        if not onnx.exists() or sha256(onnx) != REMBG_SHA256:
            sys.exit(f"缺少或校验不符：{onnx}（下载见 .cache/models/triposr_download_list.md）")
        img = remove_background(img, rembg.new_session(REMBG_MODEL))
        img = resize_foreground(img, ratio)
        arr = np.array(img).astype(np.float32) / 255.0
        arr = arr[:, :, :3] * arr[:, :, 3:4] + (1 - arr[:, :, 3:4]) * 0.5
        img = Image.fromarray((arr * 255.0).astype(np.uint8))
    return img.convert("RGB")


def run(args: argparse.Namespace) -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["U2NET_HOME"] = str(REMBG_DIR)  # rembg 只从这里读模型
    image, out = Path(args.image).resolve(), Path(args.out).resolve()
    meta_path = out.with_suffix(".json")
    params = {"mc_resolution": args.mc_resolution, "foreground_ratio": args.foreground_ratio,
              "remove_bg": not args.no_remove_bg, "chunk_size": args.chunk_size,
              "rembg_model": REMBG_MODEL if not args.no_remove_bg else None}
    want = {"input_sha256": sha256(image), "pipeline_version": PIPELINE_VERSION} | params
    if out.exists() and meta_path.exists() and not args.force:
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if {k: old.get(k) for k in want} == want and old.get("output_sha256") == sha256(out):
            print("跳过（未变）", out)
            return
    _install_shims()
    import torch
    from tsr.system import TSR
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = TSR.from_pretrained(str(MODEL), config_name="config.yaml", weight_name="model.ckpt")
    model.renderer.set_chunk_size(args.chunk_size)
    model.to(device)
    img = _prepare(image, params["remove_bg"], args.foreground_ratio)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out.with_name(out.stem + "_input.png"))
    with torch.no_grad():
        codes = model([img], device=device)
    mesh = model.extract_mesh(codes, True, resolution=args.mc_resolution)[0]
    from tsr.utils import to_gradio_3d_orientation
    mesh = to_gradio_3d_orientation(mesh)  # 原始输出 Z 轴朝上；glTF 约定 Y 轴朝上
    flipped = bool(mesh.volume < 0)
    if flipped:
        mesh.invert()
    mesh.export(str(out))
    commit = subprocess.run(["git", "-C", str(SRC), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta_path.write_text(json.dumps(want | {
        "model": "stabilityai/TripoSR", "model_license": "MIT", "code_commit": commit,
        "rembg_license": "Apache-2.0" if params["remove_bg"] else None,
        "weights_sha256": sha256(MODEL / "model.ckpt"), "input": str(image),
        "vertices": int(len(mesh.vertices)), "faces": int(len(mesh.faces)),
        "watertight": bool(mesh.is_watertight), "volume_raw_sign": "negative→已翻面" if flipped else "positive",
        "vertex_color_space": "sRGB（glTF 按线性读；导入 Blender 时须加 sRGB→线性转换）",
        "output": str(out), "output_sha256": sha256(out), "device": device,
        "note": "marching cubes 用 scikit-image 替代 torchmcubes（tools/local_3d.py）",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已生成", out, len(mesh.vertices), "verts", len(mesh.faces), "faces")


def main() -> None:
    ap = argparse.ArgumentParser(description="TripoSR 本地单图转 3D（MIT）")
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True, help=".glb 或 .obj")
    ap.add_argument("--mc-resolution", type=int, default=256)
    ap.add_argument("--foreground-ratio", type=float, default=0.85)
    ap.add_argument("--no-remove-bg", action="store_true")
    ap.add_argument("--chunk-size", type=int, default=8192)
    ap.add_argument("--force", action="store_true")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
