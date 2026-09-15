"""shot35 previz（S 档航拍收束，20 s）—— 五更天亮，沿城客店屋脊上方起飞，边退边升到 W11 WP3 看整座城与外城整圈。

（协调者 2026-09-14 改序：原 shot36 的航拍收束挪到客店之后，成为 shot35。）
起点＝Place B 方块 26 第 0 栋沿城客店屋脊上方；终点＝W11 WP3。理由与 R3-26 取舍写在同目录 `previz_config.toml` 抬头。
编排只写在同目录 TOML；其余全部来自 `tools/build_bianjing.py`「previz 公用」段。

用法（仓库根目录；脚本只动副本）：
    cp ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend \
       "ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot35/shot35_previz.blend"
    blender -b ".../shots/shot35/shot35_previz.blend" --python ".../shots/shot35/shot35_previz.py"
    blender -b ".../shots/shot35/shot35_previz.blend" -a          # → shot35_previz.mp4
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
