import sys
from pathlib import Path

for _anc in Path(__file__).resolve().parents:
    if (_anc / "tools" / "previz_sk1.py").is_file():
        sys.path.insert(0, str(_anc / "tools"))
        break
import previz_sk1  # noqa: E402

SCENE_MASTER = "ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend"
previz_sk1.run(__file__)
