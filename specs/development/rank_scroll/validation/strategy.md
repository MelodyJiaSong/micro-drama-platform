# Validation strategy · rank_scroll

| 层级 | 做什么 | 怎么跑 |
|---|---|---|
| 单元 | 时间线（段落顺序、总时长、冠军最后居中）、文本适配、数值格式、校验器对坏输入报错 | `python -m pytest projects/rank_scroll/tests -q` |
| 帧级 | 关键时刻单帧 PNG（片头、第 N 名入场、洞察卡、第 10 名放大、冠军、计分板、来源卡）人工 / 代理看图 | `preview` 子命令 |
| 可复现 | 同输入两次渲染同一帧，像素哈希一致 | 单元测试 |
| 系统 | 用 fixtures 渲染 10 s 草稿 MP4，ffprobe 校验分辨率、帧率、时长、音轨 | 测试 + 手动 |
| 端到端 | ep01 / ep02 全片渲染，独立审片（另起上下文）按 bible §7 清单 | 代理 + 子代理 |

AUTONOMOUS：用户不在，`validation.requires_manual_walkthrough` 留给用户醒来后看片。
