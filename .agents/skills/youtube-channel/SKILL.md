---
name: youtube-channel
description: YouTube 频道：经官方 API 把成片传成私享（公开人点）、发评论；拉自有频道增长报告（播放、观看时长、订阅、流量来源、留存、YPP 进度）并给出改进建议；用 yt-dlp 对比同类频道公开数据。Claude Code/Codex 共用。
metadata:
  claude:
    argument-hint: "upload <剧> <期> | report [天数] | retention <video_id> | compare <频道>"
---

# YouTube 频道：上传与增长分析

三件事共用一套本机 OAuth 授权，凭据在仓库外 `%USERPROFILE%\.micro_drama\youtube\`（`client_secret.json` + `token.json`），不读取、不打印其内容。

| 要做什么 | 入口 |
|---|---|
| 授权 / 核对频道 | `python tools/youtube_upload.py auth`、`whoami` |
| 上传 | 剧级适配器，如 `python ai_videos/paihangbang/_tools/upload.py youtube <期>`；通用库 `tools/youtube_upload.py` |
| 自有频道增长 | `python tools/youtube_analytics.py report [--days 28]`、`retention <video_id>` |
| 同类频道对比 | `python tools/yt_research.py channel <handle>` / `meta <id>`（公开数据，见 `ai_videos/_research/README.md`） |

## 授权

- 首次：Google Cloud 项目启用 **YouTube Data API v3** 与 **YouTube Analytics API**，建「桌面应用」OAuth 客户端，JSON 存为上面的 `client_secret.json`，再跑 `auth`（会开浏览器，需用户本人登录点同意）。
- 报「缺权限」「授权已失效」就重跑 `auth`；OAuth 应用停在「测试」状态时 refresh token 7 天过期，建议用户发布为正式版。
- `auth` 后先 `whoami`，把频道名和链接告诉用户确认。

## 上传

- **一律传成私享，公开由用户在 YouTube Studio 亲手点**；`--publish-at` 定时公开也只在用户给出时间时用。
- 先 `--dry-run`，剧级闸门（如排行榜的配图闸门、AI 声明核对）不过就不传，报告原因，不绕过。
- 上传记录写各期 `uploads.json`；「结果未知」先让用户在 Studio 查有没有这条，确认没有才 `--retry-unknown`，不自动重传。
- API 项目未通过 Google 审核（YouTube API Services Audit）时，传上去的视频被锁私享、无法公开；遇到就如实告诉用户。
- 配额默认每天 10,000 单位：传片约 1,600，封面、每条评论各 50。批量前先算。
- 新剧要上传：照 `ai_videos/paihangbang/_tools/upload.py` 写剧级适配器，组装 `VideoJob` 调 `upload()`，标题、描述、标签、合成内容声明从该剧发布稿读，不在代码里手写。

## 增长分析

1. 跑 `report`（默认近 28 天，结束日为 3 天前，因数据滞后）。输出：
   ```
   ai_videos/_research/youtube_channel/<频道 id>/<结束日>_<天数>d/report.md
   ai_videos/_research/youtube_channel/<频道 id>/<结束日>_<天数>d/report.json
   ```
2. 读 `report.md`，给用户结论，不复述整张表：
   - 增长：播放、观看时长、净增订阅对上一期的变化，和哪几条视频贡献了大头。
   - 留存：均看比例、热门视频 25/50/75% 处留存，开头 10% 掉得多说明开场钩子弱。
   - 来源：搜索 / 推荐 / Shorts 信息流 / 外部的占比，决定该优化标题与关键词还是封面与开场。
   - 观众：地区、设备、订阅者占比（订阅者少 = 靠推荐拉新）。
   - YPP 进度：离 1,000 订阅 + 4,000 小时（或 Shorts 1,000 万播放）还差多少，按当前速度约多久。
   - 2–3 条可执行建议，每条写依据的数字；同类频道对比时数据来自 `yt_research.py` 实测，不估算。
3. 曝光次数、点击率（CTR）、收入 API 拿不到（收入需另授权，暂不做）：需要时请用户从 Studio「数据分析 → 覆盖面」截图或导出。
4. 数据为零或很少（新频道、全是私享）时直说样本不够，不硬下结论。

## 边界

- 只读分析不改频道任何设置；上传、评论属于对外发布，按上节规则执行。
- YouTube API 不是收费服务，不走 `request_log.md`；但上传记录必须落剧级 `uploads.json`。
- 平台规则（YPP 门槛、审核、配额）以 Google 官方当前文档为准，变化时更新本文件。
