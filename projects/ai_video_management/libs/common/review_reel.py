"""整集审片串联的固定参数（follow-up 260）：每镜重编码成同一规格再拼，产物放集目录 review_reel/（不进 git）。"""
from __future__ import annotations

REEL_DIR = "review_reel"
SEGMENTS_DIR = "segments"
WIDTH, HEIGHT, FPS = 1280, 720, 30
AUDIO_RATE = 48000
# 改了编码参数就改这个版本号：旧的串联与中间件按指纹自动失效
REEL_FORMAT = f"v2-{WIDTH}x{HEIGHT}-{FPS}fps-aac{AUDIO_RATE}-stereo"
