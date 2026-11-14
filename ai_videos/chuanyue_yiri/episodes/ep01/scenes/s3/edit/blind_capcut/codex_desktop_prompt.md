# 给 Codex 桌面版的执行提示（CapCut 一方）

用法：在 ChatGPT / Codex **桌面版**里新开一个任务，工作目录选 `C:\workspace\micro-drama-platform`，把下面分隔线以下的全文贴进去。CapCut 插件要先按官方页面 https://www.capcut.com/tools/capcut-x-codex 装好并授权；只装插件、授权不收费。账号所在地区要和出口 IP 一致（美国 IP 用美国账号，否则用非美国账号）。

**先装插件**（2026-11-08 首次执行时 Codex 报告会话里没有 CapCut 工具、插件目录也搜不到，chuanyue_yiri follow-up 043）：CapCut 插件不在 Codex 自带的插件目录里，要用官方安装提示装。在 Codex 桌面版新开一个任务，工作目录同上，发：

> Download and read https://sf16-sg.tiktokcdn.com/obj/eden-sg/962370eh7nupenuhbo/capcut_codex_plugin/SKILL.md, then follow it exactly to install and authorize the CapCut plugin. 它做连接检查、要调用任何 CapCut 工具之前，先按 `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/codex_desktop_prompt.md` 硬规则第 2 条，用 `tools/mcp_request_log.py` 记请求日志（target 用该测试目录）。不要做任何生成、上传或草稿操作。

安装会弹出 CapCut 授权页，在 Codex 内置浏览器里登录、同意。装好后它可能自动分出一个新任务；之后**在新任务里**再发执行那一句（旧任务的工具列表不会刷新）。

---

你在执行一次剪辑盲测的 CapCut 一方。测试目录：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/`（下称 `T`）。先完整读 `T/README.md` 和 `T/brief_en.md`，再按下面步骤做。全程中文汇报。

## 硬规则（违反任何一条，这一方作废）

1. **商用**：成片只能由 `T/pool/` 的三条素材组成。禁止使用 CapCut 的任何素材或模板：音乐、音效、字体、字幕 / 自动字幕、文字、文字模板、贴纸、特效、滤镜、转场、动画、画布背景、模板、库存视频与图片。禁止调用 `capcut_image_generate`、`capcut_video_generate` 和一切生成。只许剪、排序、改入出点、变速、音量、关键帧。
2. **请求日志先写**：每一次 CapCut MCP 工具调用（上传、开始剪辑、每一次轮询、提交方案回复、读写草稿）之前，先运行
   `python tools/mcp_request_log.py request --target T --provider capcut --operation <工具名> --request @T/arms/_req/<序号>_req.json [--file <上传的本地文件>]`，
   拿到它打印的 request_id 再调用；调用后运行 `... result --request-id <id> --response @T/arms/_req/<序号>_resp.json`，失败运行 `... error --request-id <id> --error "<原样错误>"`。参数与返回先原样写成 JSON 文件再用 `@路径` 传（Windows PowerShell 直接传 JSON 字符串会吃掉双引号）。日志写不进就停止。凭据、签名 URL 不写进参数（脚本会脱敏，但不要主动贴）。
3. **不偷看对照**：不要打开 `T/arms/pipeline.mp4`、`T/check/pipeline.json`、`T/pool.json` 里的 `arms` 段、场景目录里的 `cut_v*.json`、`s3_final_*.mp4`，以及集目录的 `edit/`。只用 brief 和三条素材。
4. **不重复提交**：结果未知时用已有 session_id / event cursor 继续查询，不重开任务。
5. 不改 `T/` 以外的仓库文件；不开浏览器操作 CapCut 编辑器改草稿（只用插件工具）。

## 步骤

1. **上传**：`T/pool/clip_01.mp4`、`clip_02.mp4`、`clip_03.mp4` 按顺序用 capcut-upload 上传（每条先记日志）。每条拿到 VID 后运行 `python tools/edit_blind_test.py set-vid T clip_0N <VID>`。
2. **AI 粗剪**：用 `capcut_ailab_start_edit`，assets 按 clip_01、clip_02、clip_03 顺序，query 用下面这段英文（原样，前面接上 `T/brief_en.md` 全文）：

   > Edit these three clips into one scene following the brief above. Use ONLY the uploaded clips and their original audio. Do NOT add any music, background music, sound effects, captions, subtitles, text, titles, stickers, filters, effects, transitions, animations or templates, and do not generate any new images or video. Hard cuts only. Output 16:9, 1280x720, 24 fps, about 45–55 seconds.

3. **方案卡与配乐卡**：如果方案里出现上面禁止的任何东西，回复：`Please remove all music, sound effects, captions, text, effects, filters and transitions. Hard cuts of the uploaded clips only.` 出现 `background_music` 卡，一律不选任何配乐，回复不要配乐。对剪法本身的意见只能依据 brief，最多回复两轮；记下每一轮你回复了什么。
4. **收结果**：完成后把成片卡对应的 `stdraft` 原样存成 `T/arms/capcut_stdraft.json`，把编辑页链接、session_id、所用积分（按返回原样记，没有就写未知）写进 `T/arms/capcut_notes.md`。
5. **导出（用户来点）**：请用户在 CapCut 编辑器里打开这份草稿，**不做任何修改**，导出 1280×720（720p）、24 fps、MP4，保存为 `T/arms/capcut.mp4`。导出时如果提示 Pro 功能或会员素材，说明草稿里混进了 CapCut 素材——停下报告，不要付费解锁。
6. **合规机检**：运行 `python tools/edit_blind_test.py check T T/arms/capcut.mp4 --draft T/arms/capcut_stdraft.json --name capcut`。
   - 通过：在 `capcut_notes.md` 里写「机检通过」和输出摘要，结束。
   - 不通过：把问题原样写进 `capcut_notes.md`。只允许用插件的后期编辑**删除**违规元素（不做其他任何修改），再请用户重新导出并重跑机检；删了什么写清楚。仍不通过就停止，报告这一方作废。
7. 不要运行 `blind`、`review`、`reveal`。完成后告诉用户：「CapCut 一方已就绪，回 Claude Code 继续盲化」。
