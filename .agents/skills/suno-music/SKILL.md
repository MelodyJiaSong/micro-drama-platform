---
name: suno-music
description: 所有新音频生成的默认入口：通过本机 Suno API/MCP 制作环境音、音效、背景音乐、主题曲和歌曲，上传参考、预检、查询与下载。Claude Code/Codex 共用；不支持的配音或克隆需求明确报能力缺口，不自动换引擎。
metadata:
  claude:
    argument-hint: "音乐需求或 Suno job ID"
---

# Suno 音乐与声音

本 skill 是制作流程所有新音频生成的默认路由，详见 [声音与音乐](../ai-videos-pipeline/modules/sound.md)。已有音频可复用；混音、剪辑、响度处理不必经过生成 API。用户未指定其他引擎时，不因 Suno 暂停或缺能力自动改用其他服务/本地模型。

共用 API、命令行和 MCP 的说明在 [服务 README](../../../projects/suno_browser_service/README.md)。先读根 AGENTS.md 与 [收费服务审计](../../references/project/paid_services.md) 的 Suno 一节。当前用户对本服务的自动 Create/下载授权持续有效；普通用户提出生成任务也属于本次生成授权，不重复确认。

优先使用已连接的 `suno_*` MCP 工具；未连接时在仓库根使用：

```powershell
./.venv/Scripts/python.exe projects/suno_browser_service/apps/cli/main.py capabilities
./.venv/Scripts/python.exe projects/suno_browser_service/apps/cli/main.py plan --file request.json
./.venv/Scripts/python.exe projects/suno_browser_service/apps/cli/main.py create --file request.json --key stable-task-cue-v1
./.venv/Scripts/python.exe projects/suno_browser_service/apps/cli/main.py wait --job JOB_ID
./.venv/Scripts/python.exe projects/suno_browser_service/apps/cli/main.py download --job JOB_ID --output OUTPUT_DIRECTORY
```

令牌由入口读取私有本机配置，不要求用户粘贴，不读取或打印 cookies。先查 `GET http://127.0.0.1:8770/health`；连不上就是服务没启动，代理自己运行 `projects/suno_browser_service/start.ps1` 再查，不用问用户。默认是常驻窗口模式：`start.ps1` 会顺带打开服务专用的普通 Chrome 窗口（也可单独运行 `open-window.ps1`），用户一直开着，服务在里面单独的标签页操作；health 的 `browser_window=closed` 时任务保持排队，服务有排队任务时每分钟自己重开窗口（卡死的服务专用 Chrome 先结束），代理也可运行 `open-window.ps1`。窗口本身出错（TimeoutError、window_not_open 等）而还没提交的任务服务会自动重排最多 3 次；仍报 needs_attention 且没进过 submitting 的，确认是窗口问题后对原 job `resume` 即可，不算重复生成。要登录时请用户直接在这个窗口登录，不用停服务；`next_action=complete_suno_login_in_open_window` 同样马上转告用户。Create 后歌曲 3–5 分钟才出现、出现后还要等生成完才能下载，按 45 秒一次继续查同一 job，不提前判失败。一次 wait 最长 45 秒，未完成就对同一 job 继续查询。`next_action=complete_suno_verification_in_open_window` 表示 Suno 弹了验证码、服务开着可见窗口在等人：马上告诉用户去那个 Chrome 窗口完成验证，代理不碰验证码，继续查同一任务。Sounds 没有时长控件，请求不要带 `duration_seconds`，prompt 不超过 500 字符。已提交但结果不明（uncertain / 超时 / 认错）先用 `resume` 加 `recollect: true` 到库里按标题或 prompt 重新认领，不重新生成；确认没生成才另建新键重提。
人工入口为 `http://127.0.0.1:8770/ui/`，API 文档为 `/docs`，机器描述为 `/openapi.json`；完整工具参数、返回值和错误恢复见服务 README。MCP 在配置里不等于本会话已经加载，未发现工具使用上述 CLI。

先查 capabilities/schema 的当前能力、验证状态和参数范围。`plan` 不创建任务、不操作网页、不收费。Advanced 用风格 prompt 与明确 lyrics；纯音乐不填歌词。Simple 用自然语言说明，可请求自动写词并附参考。Sounds 用 sound_type=one_shot/loop 与可选 bpm。options 不填的字段遵循页面默认值；型号同理：2026-11-03 实测 v6 纯音乐长度不稳定（有的只有 1 分钟）、v6-mini 约 3–3.5 分钟但同晚点 Create 后一直不出歌，下载后用 ffprobe 核对时长，需要长背景乐时在 `options.model` 写明，页面默认可能变；要求某值时明确写入，缺少控件/状态无法读回会停在 Create 前。界面可见不等于本账号已完成验收。

参考媒体用 `suno_upload_reference` 或 CLI `upload --file` 取得 asset_id，放在 `references:[{"asset_id":"..."}]`；这一步只存本机，正式任务才上传 Suno。有明确使用权时可设 rights_confirmed；不能替用户推断第三方素材的权利。已有 Suno 歌曲/歌单可用 `references:[{"url":"https://suno.com/song/UUID"}]`。Voice/Inspo 只选择用户已有项目，不创建声音、训练模型或发布作品。

制作任务的 target 指向实际 `ai_videos/` 剧/集/资产目录或 `edu_videos/<系列>/<知识点>/`，独立任务省略。正式浏览器操作由服务先写 RequestLog，不另写脚本绕过入口。请求 JSON 保存在任务审计目录，业务意图按 follow-up 落 specs。

同一次生成的幂等键固定，网络超时重用原键。`uncertain` 不换键重建：在账号确认实际歌曲后，用原 job 的 resume 和 song_urls 仅补收。`automation_paused=true` 表示验证码/访问问题，保持暂停并交代具体阻塞；不删除暂停文件、不代解。已下载文件可以继续取回。文件下载验证 SHA256，保留同名不同内容的本地文件。

批量生成前先看 suno.com/account 的「Downloads remaining」：Pro 有月度下载上限，每个任务下两首，不够就先问用户（2026-11-04 一晚用到只剩 1）。

交付注明文件路径、实际来源、完成范围和待试听项。只有 completed 且真实音频下载/检查成功才称生成完成；离线 fixture 测试不算 Suno 实测。
