# Validation results · rank_scroll v0.1（2026-11-03，AUTONOMOUS）

| AC | 结果 | 证据 |
|---|---|---|
| AC1 校验器 | 通过 | `tests/test_rank_scroll.py`：坏图标、超长徽章、错 after_rank、乱序、缺国旗、缺图（strict）、NC 许可均报错；ep01 / ep02 `validate` 通过（缺图仅警告） |
| AC2 时间线 | 通过 | 单测：倒数顺序、洞察卡位置、第一张卡在左三分之一（x=320）、冠军（含并列组）结束时居中；ep02 并列 #1 复审确认两张完整对称 |
| AC3 整数像素 | 通过 | 单测：匀速段每帧恰 2 px；ep02 独立审片用帧互相关实测 2 px/帧 |
| AC4 输出规格 | 通过 | 单测 ffprobe（960×540 片段）；ep02 母版 1920×1080 60fps H.264 yuv420p + AAC，328 s |
| AC5 可复现 | 通过 | 单测：同输入同帧像素一致 |
| AC6 看图 | 通过（有遗留） | ep02 两轮 fresh-context 审片（`ai_videos/paihangbang/episodes/ep02_*/qc.md`）；ep01 审片见对应 qc.md |
| AC7 manifest | 通过 | `render/*.manifest.json` 记录输入 sha256、参数、ffmpeg 命令 |
| AC8 速度 | 通过 | 合成样例 1080p60 128.8 fps；真实图片 + 并行负载下 62 fps，5.5 分钟片约 5.3 分钟 |

`validation.requires_manual_walkthrough`：用户醒来后看片（ep01 / ep02 母版）。

## 运行中修订

- NVENC 不可用（驱动 596.58 < 610）：草稿改 libx264 veryfast。
- 非拉丁字符（Commons 作者名）出现方框：加 Noto Sans SC 回退字体。
- 角落计分板溢出到标题下：按宽度裁掉末位。
- 并列冠军：相机停在并列组中点，取消右侧 No. 1 标注，全部并列卡发光。
- 竖幅照片（摩天楼）被横向裁切：竖图改为「模糊铺底 + 完整显示」。
- 洞察卡数字与单位断行：单位前用不换行空格。
