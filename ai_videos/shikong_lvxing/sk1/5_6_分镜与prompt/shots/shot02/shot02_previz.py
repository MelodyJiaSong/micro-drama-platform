"""shot02 previz（S 档航拍，30 s，镜内 14 s 一切）—— 承接 shot01 末帧 → 起升后退到三圈城墙全景 ｜切｜ 御街上空向北低飞，停在宣德楼前。

首帧由 `previz_config.toml` 的 `["承接", "shot01"]` 逐值继承 shot01 最后一个关键帧（位置 / 看向 / 焦距），
交接状态只有 shot01 那一份出处；机位取相机审查 R3-02 方案 (A)，落幅按协调者定调。编排只写在同目录 TOML，
其余全部来自 `tools/build_bianjing.py`「previz 公用」段。

用法（仓库根目录；脚本只动副本）：
    cp ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend \
       "ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot02/shot02_previz.blend"
    blender -b ".../shots/shot02/shot02_previz.blend" --python ".../shots/shot02/shot02_previz.py"
    blender -b ".../shots/shot02/shot02_previz.blend" -a          # → shot02_previz.mp4
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
