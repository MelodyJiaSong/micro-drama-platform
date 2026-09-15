"""shot01 previz（S 档航拍，30 s）—— 虹桥贴水低飞 → 擦过桥面 → 沿汴河爬升 → 悬停远眺东水门（交接给 shot02）。

本镜编排只写在同目录 `previz_config.toml`（机位关键帧 + 放桅纲船，机位取相机审查 R3-01）；解析、改道后的汴河、
W11 航点、逐帧机位插值与渲染设置全部来自 `tools/build_bianjing.py` 的「previz 公用」段——本脚本不另写一份（rule 4h §C / 4i ①）。

用法（仓库根目录；脚本只动副本，绝不写回场景主档）：
    cp ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend \
       "ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot01/shot01_previz.blend"
    blender -b ".../shots/shot01/shot01_previz.blend" --python ".../shots/shot01/shot01_previz.py"
    blender -b ".../shots/shot01/shot01_previz.blend" -a          # → shot01_previz.mp4（灰模 workbench）
"""
import sys
from pathlib import Path

for _anc in Path(__file__).resolve().parents:
    if (_anc / "tools" / "build_bianjing.py").is_file():
        sys.path.insert(0, str(_anc / "tools"))
        break
import build_bianjing  # noqa: E402

# 场景主档（仓库相对路径）：webapp「出片」按钮据此自动 copy + 重建本 .blend
SCENE_MASTER = "ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend"

build_bianjing.run_aerial_previz(__file__)
