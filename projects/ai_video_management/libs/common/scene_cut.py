"""剪辑模块的目录约定（follow-up 269，与 tools/scene_cut.py 同一份约定）。

每场的剪辑决定放在 `{集}/scenes/{场}/edit/{阶段}/cut_v{N}.json`：
草稿剪辑（draft）只用各镜 drafts/ 的 480p 草稿条；正片剪辑（final）只用 renders/ 的 720p 正式条。
成片 mp4 放同一目录（不进 git），文件名记在决定的 output.files 里。
"""
from __future__ import annotations

EDIT_DIR = "edit"
CUT_STAGES = ("draft", "final")
CUT_FILE_PATTERN = r"cut_v(\d+)\.json"
EPISODE_CUT = "episode"   # 剪辑页 `scene=episode` ＝ 集级剪辑（follow-up 278）

# 集级剪辑（follow-up 277 / 278）：`{集}/edit/{阶段}/cut_v{N}.json` 把各场接起来，场与场之间的转场只能从下面的菜单里选。
# tools/episode_cut.py 渲染、管理界面展示都读这一份。key → (中文名, ffmpeg xfade 名；None ＝ 不重叠的切, 默认秒, 最长秒, 用来)
TRANSITIONS: dict[str, tuple[str, str | None, float, float, str]] = {
    "cut":          ("切", None, 0, 0, "最常用；场内默认，场与场之间也以切为主"),
    "smash_cut":    ("硬切", None, 0, 0, "静到吵、乱到定的强反差，惊醒观众；画面同切，靠两场的声音与画面反差成立"),
    "dissolve":     ("叠化", "fade", 1.0, 3, "表示比一刀切更长的时间流逝；进入回忆、梦境"),
    "superimpose":  ("叠印", "fade", 2.5, 4, "长叠化，中途两幅画面同框成第三个镜头，让两场、两个人互相对照"),
    "dip_to_black": ("黑场过渡", "fadeblack", 1.0, 3, "淡到黑再淡出，隔开两个时刻，像章节结束、让观众喘口气"),
    "dip_to_white": ("白场", "fadewhite", 1.0, 3, "淡到白，进入梦境或死亡，或让结局悬而不决"),
    "iris_open":    ("光圈开", "circleopen", 1.0, 2, "圆形打开，把世界向人物敞开；复古风格选择"),
    "iris_close":   ("光圈合", "circleclose", 1.0, 2, "圆形收拢，把注意力聚到一点；复古风格选择"),
    "wipe_left":    ("划像·向左", "wipeleft", 0.8, 2, "下一场从右往左把上一场推出；复古、反讽或喜剧"),
    "wipe_right":   ("划像·向右", "wiperight", 0.8, 2, "同上，从左往右"),
    "wipe_up":      ("划像·向上", "wipeup", 0.8, 2, "同上，从下往上"),
    "wipe_down":    ("划像·向下", "wipedown", 0.8, 2, "同上，从上往下"),
    "wipe_diag":    ("划像·斜角", "diagtl", 0.8, 2, "同上，斜着划过"),
    "wipe_clock":   ("划像·时钟", "radial", 1.0, 2, "像钟表指针扫过；复古（《星球大战》式）"),
    "slide_left":   ("推出·向左", "slideleft", 0.8, 2, "两场一起滑动，下一场把上一场整幅推走"),
    "whip_sim":     ("模拟甩镜", "hblur", 0.4, 1, "横向拖影近似甩镜，延续势头；真正的甩镜要两镜各自生成"),
    "zoom_in":      ("推近转场", "zoomin", 0.8, 2, "推进上一场的画面中心再出下一场，把注意力往里带"),
}
EDGES = {"cut": ("切", None), "fade_black": ("淡入 / 淡出（黑）", "black"), "fade_white": ("淡入 / 淡出（白）", "white")}
GALLERY_PATTERN = r"转场样片_(s\d+)_(s\d+)\.mp4"     # 两场交界的转场样片；同名 .txt 是时间索引（「  0.0s  切 cut」一行一条）
