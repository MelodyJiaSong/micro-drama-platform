"""由参考图生成白模原始网格（本地 Hunyuan3D，零成本、可无限重试）。

用法（仓库根目录，用 hy3d venv 的 python）：
    C:/workspace/hy3d_venv/Scripts/python.exe tools/whitemodel_generate.py \
        --spec ai_videos/{drama}/2_世界观人设/props/{object}/object.toml \
        --out  <raw.glb>

产物是**原始网格**，不是可用白模——它朝向随机、尺度随机、自带烤死的材质。
下一步必须过闸门：

    blender -b --factory-startup --python tools/whitemodel_normalize.py -- \
        --src <raw.glb> --spec <object.toml> --out <{object}.blend>

为什么走本地而不是云端 API
--------------------------
薄结构（尾翼、扩散器叶片、器物细部）是 image-to-3D 最不稳的地方，换哪家都一样，
**所以重试次数才是质量的主要来源**。本地跑没有 per-call 成本、没有额度、没有 key，
可以一直重掷到过闸门为止。云端 vendor 仍然随时可换——闸门 vendor 无关，
`whitemodel_normalize.py --src` 吃任何来源的网格。

只生成 shape，不生成 texture
----------------------------
白模只承载几何，材质在闸门里会被无条件剥掉，生成贴图纯属浪费。
副作用是显存需求从 16GB 降到 6GB，并且能跳过 Windows 上最难装的两个 CUDA 扩展
（custom_rasterizer / differentiable_renderer 只在贴图链路里用）。

多视角优先
----------
`Hunyuan3D-2mv` 吃 front / left / back / right 多张图，比单图重建稳得多——
而这几张图 rule 4d 的五步本来就要求出（锚点 + 正/侧/背）。
视角与文件的对应写在 object.toml 的 ["参考图"] 段；缺哪个视角就不传哪个。
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# mv 模型认的视角键。object.toml 的 ["参考图"] 用同一套键。
MV_VIEWS = ("front", "left", "back", "right")


def resolve(p: str | Path, base: Path = REPO) -> Path:
    q = Path(p)
    return q if q.is_absolute() else (base / q).resolve()


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="由参考图生成白模原始网格（本地 Hunyuan3D）")
    ap.add_argument("--spec", required=True, help="object.toml")
    ap.add_argument("--out", required=True, help="输出 .glb")
    ap.add_argument("--model", default="tencent/Hunyuan3D-2mv",
                    help="多视角默认 2mv；单图退路用 tencent/Hunyuan3D-2")
    ap.add_argument("--steps", type=int, default=50)
    ap.add_argument("--guidance", type=float, default=7.5)
    ap.add_argument("--octree", type=int, default=384,
                    help="八叉树分辨率。越高越吃薄结构，也越慢；384 是薄件与显存的折中")
    ap.add_argument("--seed", type=int, default=0,
                    help="换 seed 重掷。薄结构靠重试拿，不靠调参")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    spec_path = resolve(args.spec)
    if not spec_path.is_file():
        sys.exit(f"spec 不存在：{spec_path}")
    spec = tomllib.loads(spec_path.read_text(encoding="utf-8"))
    refs = spec.get("参考图", {})
    if not refs:
        sys.exit(f"{spec_path} 缺 [\"参考图\"] 段；至少要给 front")

    from PIL import Image
    import torch
    from hy3dgen.rembg import BackgroundRemover
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

    # 棚拍图带灰底，必须先抠。留底会被当成几何的一部分，重建出一个包着车的壳。
    rembg = BackgroundRemover()
    images: dict[str, Image.Image] = {}
    for view in MV_VIEWS:
        rel = refs.get(view)
        if not rel:
            continue
        img_path = resolve(rel, spec_path.parent)
        if not img_path.is_file():
            sys.exit(f"参考图不存在：{img_path}")
        img = Image.open(img_path)
        if img.mode == "RGB":
            img = rembg(img)
        images[view] = img
        print(f"  {view:<6} {img_path.name}  {img.size}")
    if "front" not in images:
        sys.exit("至少要给 front 视角")

    print(f"\n加载 {args.model} …")
    pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(args.model)

    payload = images if len(images) > 1 and "mv" in args.model else images["front"]
    mesh = pipe(
        image=payload,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        octree_resolution=args.octree,
        generator=torch.manual_seed(args.seed),
    )[0]

    out = resolve(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(str(out))
    print(f"\n写出 {out}")
    print("下一步过闸门：")
    print(f'  blender -b --factory-startup --python tools/whitemodel_normalize.py -- \\\n'
          f'      --src "{out}" --spec "{spec_path}" --out <{spec.get("对象", {}).get("名称", "object")}.blend>')


if __name__ == "__main__":
    main()
