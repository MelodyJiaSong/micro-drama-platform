# 选题调研 · _research

为**单人创作者**挑「值得翻拍的 AIGC 内容格式」而做的调研数据，供 webapp 的
**📊 调研** 模块（`/research`）读取。

## 数据集

| 文件 | 内容 |
|---|---|
| `youtube_series.json` | 近半年（2026-03-06 → 2026-09-06）YouTube AIGC 系列排行：10 个系列 × 10 条实测样本 |

## 两条硬筛选标准

1. **回报好** —— 点赞率（like/view）**与**播放量都要高。只满足一项的一律降档。
2. **一个人能翻拍** —— 工具可以买，人不能加。凡需要真人出镜、摄制组、配音演员、
   剪辑团队，或需要「另一个人过审」才能开工的格式，直接淘汰或压到末位。

## 指标怎么来的（不接受估算）

播放量 / 点赞数 / 发布日期全部由 `tools/yt_research.py`（封装 `yt-dlp`）实测抓取。
`tools/yt_series_build.py` 在落盘前会把每条引用的视频**再抓一次**：解析不了的、
或发布日期在窗口外的，直接丢弃而不是带病发布；`stats` 里的中位数/总量由脚本计算，
不采信任何文字描述里的数字。本期 100/100 条通过复核。

## 复跑

```bash
python tools/yt_research.py search "<query>" --sp views_month --limit 25   # 发现
python tools/yt_research.py meta <id> <id> --jobs 3                        # 取 like/日期
python tools/yt_series_build.py draft.json -o ai_videos/_research/youtube_series.json
```

## 局限

`caveats` 字段里写了完整版。最要紧的三条：样本窗口只有半年、每系列 10 条，中位数只能
当量级判断；样本里的高播放多来自存量大号或工作室，**新号第一年的真实起点更接近各系列的
地板样本**；RPM 与收入全部是按语言/受众地理推断的估算，无一实测。
