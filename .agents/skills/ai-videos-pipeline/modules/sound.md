# 声音与音乐

状态：完整后期流程待设计；音频生成默认入口与 Suno 调用步骤已接入（2026-10-22）。

| | |
|---|---|
| 输入 | 锁片版本；剧级音乐资产（主题等，待建） |
| 输出 | 对白、环境声与音效、音乐各自的轨，以及混音成品与分轨 |
| 大致步骤 | 对白整理 → 环境声、音效 → 音乐（定起止、制作或授权、cue 表）→ 混音与响度 |
| 前提 | 锁片之后开始：画面再改，声音与音乐要返工 |
| Vision | 设计与审查都对照剧 README 的全剧 Vision |

旧流程的后期声音工具已于 2026-10-11 删除，本模块的做法与工具从零设计；集级 `episodes/epNN/cue/` 是占位目录。生成视频时 prompt 已禁止背景音乐，配乐在这里独立处理。设计时参考[注意力引导](filming-attention.md)的声音手段：最响者优先、放大细节或抽掉其余、画外声、故意打散。只用条款明确允许商业用途的工具，见[外部服务](../../../references/project/paid_services.md)。

## 默认音频生成入口

**所有新音频生成统一默认使用 Suno 浏览器服务 API**，包括环境声床、背景音、动作/生物音效、背景音乐、主题曲、片头/片尾曲及其他音频需求。Kimi Code 读 [suno-music](../../suno-music/SKILL.md)，优先调用其 MCP，未加载时用同服务的 CLI 或 HTTP API（本机 `http://127.0.0.1:8770`，[接口文档](http://127.0.0.1:8770/docs)，`/health` 查运行与暂停状态）；人工使用同服务的 [本机工作台](http://127.0.0.1:8770/ui/)。用户 2026-10-24 确认：以后声音默认都用这个自建 Suno API。[API、CLI 与运行说明](../../../../projects/suno_browser_service/README.md) 是接口唯一说明源。

| 需求 | 默认模式与输入 |
|---|---|
| 环境音、背景氛围、持续声音 | `sounds` + `sound_type=loop`，prompt 描述空间、声源、远近和强弱 |
| 动作音效、生物叫声、单次声音 | `sounds` + `sound_type=one_shot` |
| 背景音乐、器乐主题 | `advanced` + `instrumental=true`，prompt 写情绪、配器和节奏；不填歌词 |
| 人声主题曲、片头/片尾歌曲 | `advanced` + `instrumental=false` + 明确 `lyrics`；需要自动写词时用 `simple` |
| 人物资产的技能 / 动作音效（技能视频、建立视频） | `sounds` + `one_shot`（施放、命中）或 `loop`（持续光环、护罩）；按该人物 / 技能的声音研究写 prompt；做好后混进视频另存带音效版本，不覆盖原片 |
| 音频/图片/视频启发的音乐 | 先上传参考，再传 `references`；图片/视频用 `simple` |
| 对白配音、声线克隆、分离人声等 | 仍先查默认 API 的 capabilities；当前无这些专用能力，记为未支持，不用歌曲模式假装 TTS 或克隆 |

Suno 遇验证码、配额、页面变化或能力缺口，保留阻塞与原任务，不自动换 ElevenLabs、MOSS、ACE-Step 或其他引擎。只有用户另行明确指定替代引擎时按对应规则调用；不因本机已有模型就切换。已有音频资产可继续复用，不为落实默认值重生成。

## 从创作需求到分轨

1. 读剧 Vision 与已确定画面；记录每条声音的用途、起止位置、强弱与是否压低对白。预览片的声音先标试做，不能当锁片后终混。
2. 先确认服务：有 `suno_*` MCP 工具（`.kimi-code/mcp.json` 里的 `suno-browser`）就用 MCP，更方便；会话没加载就用 CLI / HTTP API。`GET http://127.0.0.1:8770/health` 连不上说明服务没启动，代理**自己运行** `projects/suno_browser_service/start.ps1` 再查 health，不用问用户（用户 2026-10-24）。默认常驻窗口模式（2026-11-03）：`start.ps1` 顺带打开服务专用 Chrome 窗口，用户一直开着；需要登录或验证码时请用户直接在这个窗口处理，不用停服务（health `browser_window=closed` 时服务有排队任务会自己重开窗口，代理也可运行 `open-window.ps1`；还没提交就因窗口出错的任务服务自动重排，最多 3 次）。`automation_paused=true` 时代理不删暂停文件。然后 `suno_capabilities` → 如需参考则 `suno_upload_reference` → `suno_plan`。设置实际集/资产目录 `target`，使服务请求日志归属正确；plan 不访问 Suno。
3. `suno_create` 每条声音固定一个幂等键，保存请求、job ID 和预检结果。该服务已有自动 Create/下载授权；不改变视频出片规则。
4. `suno_get_job` / `suno_wait_job` 查询原任务。`next_action=complete_suno_verification_in_open_window` 表示 Suno 弹了验证码、服务开着可见窗口在等人：马上告诉用户去那个 Chrome 窗口完成验证，代理不碰验证码，继续查同一任务。Sounds 没有时长控件，请求不要带 `duration_seconds`，prompt 不超过 500 字符。验证码暂停或 `uncertain` 停止自动推进；确认歌曲后只恢复原任务补收，不能另建键碰运气。已提交但结果不明（uncertain / 超时 / 认错）先用 `resume` 加 `recollect: true` 到库里按标题或 prompt 重新认领，不重新生成；确认没生成才另建新键重提。
5. `suno_download` 取回并校验音频，记录实际引擎、歌曲 URL、文件 SHA 与用途；试听确认音色、时长、循环接缝、意外人声及与 Vision 的一致性。只有文件存在并核对后才能标成品。
6. 把已选环境声、音效、音乐交给后期混音，保留原始音频与分轨。对白清楚优先，环境声与配乐按场景压低；用户确认终混后才交付。

**后期处理工具**：`tools/episode_post.py` 继续负责环境声床、配乐、对白压低与混音；剪辑、响度、格式转换不是生成，仍使用本机后期工具。`tools/local_sfx.py` 与 ACE-Step 等保留为用户明确选择的替代工具，不再是流程默认生成器。完整 cue 数据格式、锁片与终混验收仍待模块设计，不恢复 legacy BGM 契约。
