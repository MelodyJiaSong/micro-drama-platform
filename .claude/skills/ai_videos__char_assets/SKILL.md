---
name: ai_videos__char_assets
description: 例：/ai_videos__char_assets 魔兽世界 ——AI 短剧人物资产一条龙：给剧名（目录名或 seedance.toml 的 alias，如「魔兽世界」），把缺的人物立绘 → 4 秒建立视频（即梦 CLI · Seedance 2.5 会员通道 · 720p · 立绘作参考 · 画幅读卡）→ 三视图（正/侧/背 + 声样 + 前 2 秒）补齐，已有的跳过，每步之间看图验收。用户说「生成人物图/立绘」「出建立视频 / turntable」「抽三视图」「把某剧的人物资产补齐」或 /ai_videos__char_assets <剧名> 时触发。
argument-hint: "<剧名> 例: 魔兽世界 | shengji_zhilu | shikong_lvxing/sk2"
---

# 人物资产一条龙（/ai_videos__char_assets）

名字用纯 ASCII：中文名的 skill 在 `/` 补全里不出现（2026-09-30 用户实测 `/ai_videos` 补不出 `ai_videos__人物资产`）。

参数 ＝ 剧名（`$ARGUMENTS`）：`ai_videos/` 下的目录名、带季的相对路径（`shikong_lvxing/sk2`），或该剧 `seedance.toml` 的 `alias`。
底层是 `tools/char_assets.py`（status / run / sheet），它调 `gen_char_images.py`（立绘）、`gen_turntable_videos.py`（建立视频）、网页端 `apps.cli.extract_views`（三视图）。**已有的一律跳过**，中断后重跑同一条命令即续。

## 流程

| 步 | 命令 | 做什么 |
|---|---|---|
| 0 | `python tools/char_assets.py status <剧名>` | 报规模：缺立绘 / 缺视频（×80 分）/ 缺三视图；⚠ 列出缺立绘块、缺 turntable 块的卡 |
| 1 | `… run <剧名> --steps portrait` | 出缺的立绘 |
| 1b | `… sheet <剧名> --what portrait --only <本轮新出的>` → Read | 按各卡「验收」行看图 |
| 2 | `… run <剧名> --steps video,views`（`run_in_background`） | 逐条出建立视频、落盘即抽三视图 |
| 2b | `… sheet <剧名> --what views --only <本轮>` → Read | 逐行对立绘验收 |
| 3 | 报告 + 记 `specs/ai_video/{剧}/changelog.md` | |

- **剧名对不上**：查 `ai_videos/*/README.md` 的中文剧名，在该剧 `seedance.toml` 的 `alias` 里补一条再跑。多季的剧给相对路径。
- **缺块的卡**：写卡是 stage2 的活——按 stage2 playbook 模板把块补进卡里（turntable 块：```text 首行 `{卡目录}_turntable`、`参考: \`{卡目录}(立绘·脸的唯一标准)=>@\``、末尾「比例：画幅 X:Y，时长 4 秒。」+ `负面词:`），读透人物卡再写，不编人设。本 skill 只跳过并在报告里点名。
- **立绘没过不进第 2 步**：视频照立绘出，坏脸会被锁进资产。不过的删 png、改卡里立绘 prompt 重出。
- **第一条提交时看 `priority` / `排第`**：priority 7、排第 0 ＝ 会员通道。排得很深就停下告诉用户——慢到不如网页手点就没有意义。
- **2b 验收**：同一张脸；装束与随身物一致、没多东西；正→侧→背转到位；无字幕文字；有 `## 叫声设计` 的卡平均响度 ≥ −50 dB（工具已判）。不过的报给用户，不擅自重出（80 分一条）。

## 纪律

- **一部剧同时只一个进程**（`characters/.char_assets.lock`）。被拒 ＝ 别的会话在跑，等它，不删锁硬上（锁主进程死了会自动接管）。
- **已有建立视频的卡不补立绘**：长相已由视频定，再出一张只会多一张不一样的脸。
- **画幅读卡，不在命令行覆盖**：立绘读立绘块「比例:」，视频读 turntable 块「比例：画幅…」；人物 9:16、四足兽 16:9。要改就改卡或卡的生成器。
- **超时 ≠ 没生成**：`python tools/gen_turntable_videos.py --drama <相对路径> --harvest` 收回。账里同卡还有在途任务时工具会等它、不重提。
- 串行出片（即梦并发上限）；只停自己的 PID，不按进程名杀。
- Seedance 2.5 在 CLI 帮助里没列，服务端收 `seedance2.5`（2026-09-30 实测：4–30 s、priority 7、80 分 / 条）。
