<!-- followup-entry owner=0e57c120-a37a-4876-b865-9226435a360e month=202611 -->

## 360 — 2026-11-14 20:47:16 — audio-preview-gate-free-video

> severity: high

### 指令

音频预览写入总流程（仓库级，用户明确要求）：出视频前先做整集音频预览（本地 TTS 按人物声音模拟对白，按镜头时长排好时间轴，播放器下方显示 scene / shot 进度条），用户审过音频才出视频；音频时间轴尽量与成片一致，代理也用它自检。授权边界：只有扣积分的生成（Seedance 等收费视频）需要用户审阅并人点；不扣积分的视频（本地渲染等）代理可以直接出。

### 摘要

总流程加「出视频前审音频预览」闸门；只有扣积分的视频生成要人点，免费本地视频代理直接出

<!-- changelog -->

## Follow-up 360 — 2026-11-14 20:47:16
Source: user_input/follow_ups/202611.md - section 360
Summary: 总流程加「出视频前审音频预览」闸门；只有扣积分的视频生成要人点，免费本地视频代理直接出

Auto-updated:
- （待补：执行后用 `python tools/followup.py done` 写入）

验证: （待补）

No conflicts found in: （待补）
