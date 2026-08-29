from __future__ import annotations

SHOT_SIZES = ("远景", "全景", "中景", "近景", "特写")
CAMERA_ANGLES = ("平视", "俯视", "仰视", "过肩", "肩后跟随")
CAMERA_MOVES = ("固定", "推", "拉", "摇", "移", "跟", "手持")
LOW_CONFIDENCE_FLOOR = 0.6
SUBTITLE_FORBIDDEN_TOKENS = ("字幕", "字体", "字号", "硬字幕", "软字幕")
STANDARD_NEGATIVES = "负面词: 文字, 水印, logo, 多余肢体, 畸形手指, 面部扭曲, 闪烁, 抖动, 卡顿, 低清, 噪点, 过曝, 死黑, 变形, 穿模, 突兀转场, 背景人物突变, 服装突变, 发型突变, 口型错位, 画面撕裂, 色带"
