---
name: ai-videos-char-assets
description: 短剧人物资产补齐：立绘、4 秒建立视频、三视图与声样；给剧目录名，跳过已有资产，每步看图验收。
metadata:
  claude:
    argument-hint: '<剧目录名> 例: shengji_zhilu'
---

> Claude / Codex 共用正文。执行前按根目录 `AGENTS.md` 路由，工具、提问、委派、参数与收尾遵 `CONVENTIONS.md` § Tool scoping and team coordination。路径相对仓库根；同目录资源相对本源文件。


# 人物资产一条龙（/ai_videos__char_assets）

**调用前关卡**：独立补资产和旧剧续跑也遵 `CONVENTIONS.md` § 外部服务请求审计（全局必经）；先读 `.agents/references/project/paid_services.md`，由已接入的生成器先记录请求再调用服务，归属本剧/系列的 characters 日志。已有产物跳过不等于后续调用可免审计。

名字用纯 ASCII：中文名的 skill 在 `/` 补全里不出现（2026-09-30 用户实测 `/ai_videos` 补不出 `ai_videos__人物资产`）。

参数 ＝ 剧（`实际用户消息中的参数`）：`ai_videos/` 下的目录名，或带季的相对路径。
底层是 `tools/char_assets.py`（status / run / sheet），它调 `gen_char_images.py`（立绘）、`gen_turntable_videos.py`（建立视频）、网页端 `apps.cli.extract_views`（三视图）。**已有的一律跳过**，中断后重跑同一条命令即续。

## 按需上传的资产交接

**全剧命名规则**：所有剧（含旧剧续跑、系列共享资产）、所有character今后的新建/补齐/重生成/抽帧/导入三视图和声样，必须使用下述front/side/back/audio文件名。`{角色}`取角色目录名；历史文件只兼容读取，不作为新输出命名依据。生成器及导入器不得把新文件改回数字名或中文方向后缀。

每个已入画人物交付当前造型三张PNG与实际声样MP3，文件统一为 `views/{角色}_front.png`、`{角色}_side.png`、`{角色}_back.png`、`{角色}_audio.mp3`；换装子目录用 `{造型键}_front/side/back.png`，复用本角色声样。不因文件数或新文件名宣称方向质量通过；不从建立视频的示例句推导当前剧情。编译时每个出场人物上传三视图合图与声样，见 [参考](../ai-videos-pipeline/modules/prompts-references.md) 与 [资产](../ai-videos-pipeline/resources/assets.md)；请求留痕沿用 paid_services.md。

**三视图合图交接（2026-10-03，follow-up 102）**：所有剧、所有character今后的资产流程在三张源图齐备后，用 `python tools/character_sheet.py ai_videos/{剧}` 确定性拼接；左front、中side、右back，原像素保留，尺寸不同时等宽格内居中补边，不裁切/拉伸/重画。基础输出 `views/{角色目录名}_views.png`，换装输出 `{造型键}_views.png`；三张源图及 `_audio.mp3` 保留。合图内写源图SHA，源图改变须重建合图；每人只上传合图与声样，不同时上传三张单图；缺合图或源指纹过期即阻碍编译。合图三格代表同一角色三个角度；原图朝向质量问题仍须单独验收。

## 流程

| 步 | 命令 | 做什么 |
|---|---|---|
| 0 | `python tools/char_assets.py status <剧目录名>` | 报规模：缺立绘 / 缺视频（×80 分）/ 缺三视图；⚠ 列出缺立绘块、缺 turntable 块的卡 |
| 1 | `… run <剧名> --steps portrait` | 出缺的立绘 |
| 1b | `… sheet <剧名> --what portrait --only <本轮新出的>` → Read | 按各卡「验收」行看图 |
| 2 | `… run <剧名> --steps video,views`（`run_in_background`） | 逐条出建立视频、落盘即抽三视图 |
| 2a | `python tools/character_sheet.py ai_videos/{剧}` | 合成并排 `_views.png`，校验像素与源SHA；char_assets run抽帧后及换装生成器自动合成 |
| 2b | `… sheet <剧名> --what views --only <本轮>` → Read | 逐行对立绘验收 |
| 3 | 报告 + 记 `specs/ai_video/{剧}/changelog.md` | |

- **剧名对不上**：用 `ai_videos/` 下的目录名；多季的剧给相对路径。
- **缺块的卡**：按人物卡模板把块补进卡里（turntable 块：```text 首行 `{卡目录}_turntable`、`参考: \`{卡目录}(立绘·脸的唯一标准)=>@\``、末尾「比例：画幅 X:Y，时长 4 秒。」+ `负面词:`），读透人物卡再写，不编人设。本 skill 只跳过并在报告里点名。
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
