# 外部服务：调用与请求留痕

核对日期：2026-10-03。本文维护本仓库实际入口；Dreamina含用户授权的单镜实测，其余服务的核查不表示已付费验证。参数按目标模型、官方文档及服务返回值核对，旧CLI帮助不能覆盖较新模型。`Dreamina` 为即梦 CLI，用户所写 dreaming 指此服务。

## 必须执行的调用契约

全局适用范围由根目录 `AGENTS.md` / `CONVENTIONS.md` § 外部服务请求审计（全局必经）规定：Claude、Codex 与其子任务共用；所有新旧剧、季、集、共享资产、续跑、局部修复、独立 skill 和手工调用均适用；后续接入收费服务也先接同一记录入口。本文只维护服务细节、日志字段与分组。

1. 每次调用前读本页，确定服务、操作、剧/集/资产归属、完整请求、参考文件及输出位置。
2. 所有仓库调用经 `tools/service_request.py` 的 `RequestLog`：先追加 request 事件并落盘，再调用服务；日志不能写就停止。结果或异常另追加同 request_id 的事件，不覆盖历史。
3. 正文保留完整 prompt / 台词 / 脚本 / JSON 参数、CLI argv、模型、比例、分辨率、时长、参考顺序、时间、目标路径、PID、超时及请求指纹。文件记录路径、大小、SHA256；base64 记录解码后的大小和 SHA256，不复制媒体本体。
4. API key、Bearer、cookie、secret、签名 URL 的鉴权参数脱敏。不要把凭据写进 prompt / 脚本 / CLI 参数。结果保留服务任务 ID、状态及原样返回的费用字段；没有费用字段即未知，不能把估算当实扣。
5. 提交超时不代表没提交，不自动重复收费请求；先用任务 ID 查询/补收。仅明确上传失败且尚未提交时允许自动重试；结果未知时停止重提。每次由仓库发起的查询、下载和重试也留痕。Dreamina CLI 的内部上传/轮询不可观测，只能记录该次 CLI 调用与参数，不能冒充逐 HTTP 请求日志。
6. UI 左侧「请求日志」按归属选文件、分页查看完整事件；原始 request_log.md 可在目录树查看。UI 提供查看/审查，不额外引入审批流程；既有「生成视频永远人点」及剪辑批准规则继续有效；图片在修一致性问题时代理可直接生成（follow-up 229，见 CONVENTIONS.md），仍先写请求日志。
7. 外部 MCP/另一份安装插件/用户直接终端命令不能被本仓库自动拦截。代理必须走下面的记录入口；未接入的第三方入口需先接入，不能直接调用后声称已记录。历史请求不补造。

## 商业用途（全局必经）

本仓库的影片用于商业发行。条款不允许商业用途的工具、功能或套餐档，一律不用；条款写得不明确的，取得书面确认或核实原文之前不用于成片，由用户决定。新接入任何 AI 工具，先核条款再登记。**本地模型只用完全开源的**（用户 2026-10-19）：代码与权重都是 OSI 认可的开源许可证（如 MIT、Apache-2.0），商用没有收入门槛、不用登记、不另附使用限制；带收入门槛、须登记或另有使用政策的「社区许可」一律不用。核查日 2026-10-09，依据官方条款原文；不是法律意见，正式发行前建议书面确认或律师审阅。证据见 `.audit/adhoc_agents/2026-10-09/commercial-use-terms/README.md`。

| 工具 / 功能 | 结论 | 条件或原因 |
|---|---|---|
| Dreamina 国际版：视频（Seedance）；图片（Seedream）2026-10-17 起不用（follow-up 270） | **保留（用户决定，2026-10-09）** | 条款不明确：美国版（2026-01-22）写产出归用户，但也写不得把服务「或其中内容」用于商业，且没有条款写付费档即可商用；用户知情后决定继续使用 |
| 即梦（国内版） | **保留（用户决定，2026-10-09）** | 协议原文未能取得；同上 |
| ElevenLabs 配音 / 声音克隆 | 允许（付费档） | 免费档仅限非商业；Beta 功能的产出不得商用；克隆的人声须有授权 |
| ElevenLabs 音效 | 允许（付费档） | 不得单独转售或授权音效本身 |
| ElevenLabs 图像（第三方模型） | 有条件 | 另受所选底层模型条款约束；ElevenLabs 对图像与视频产出不提供侵权赔偿 |
| ElevenLabs 声音设计（Voice Design / text-to-voice） | 不明确 | 官方帮助页标为 experimental；Beta 服务产出不得商用，是否适用于声音设计未确认（核查 2026-10-18）。产出先作试验，进成片由用户决定；只用文字描述设计，不上传第三方原声作参考 |
| **Eleven Music** | **不用（已删入口）** | 自助各档（含 Enterprise Music Lite）明确排除 film、TV；只有 Enterprise Music 合同不排除 |
| OpenAI 图像（API 与内置工具，含 Codex CLI 内置出图） | 有条件 | 产出归使用者，可商用；未经明确同意不得生成真人肖像；个人版无侵权赔偿，API 的赔偿对修改、合成后的产出可能不适用 |
| IndexTTS 本地配音（仓库入口已随旧流程删除；本地 `index-tts/` 检出与权重也已删除，重新启用需重新克隆并登记入口，2026-10-11） | 有条件 | bilibili 模型协议：免费可商用，年收入超过 1 亿元人民币（中文版为准）须另获授权；克隆声音须有声主书面商用授权；README 写「商用请联系」，正式发行前邮件确认 |
| Suno | 有条件（Pro / Premier） | 须在配额内经官方下载后使用；Remix 不得商用；不得去水印或元数据；免费档不可；版权不保证，平台收益可能被权利人认领 |
| Stable Audio 3 本地（Medium、Small-SFX；2026-10-19 试用当天删除：权重、推理环境、代码检出与 `tools/local_audio.py` 都已删） | **不用** | Stability AI Community License：年收入低于 100 万美元可商用但须登记，不是完全开源（用户 2026-10-19 决定只用完全开源的本地模型）。Stable Audio Open 1.0 同一许可，同样不用 |
| MOSS-SoundEffect-v2.0 本地（音效、生物叫声、环境声，48 kHz、每条 ≤30 秒；`tools/local_sfx.py`，权重 `.cache/models/moss-soundeffect-v2/`，代码 `.cache/src/MOSS-TTS`，2026-10-20） | 允许 | 代码与权重 Apache-2.0（模型卡 huggingface.co/OpenMOSS-Team/MOSS-SoundEffect-v2.0、github.com/OpenMOSS/MOSS-TTS LICENSE）；文本编码器 Qwen3-1.7B 为 Apache-2.0。训练数据与 DAC VAE 来源未披露 ⚠️。本地运行不收费，不走请求日志，生成记录写在产物旁的 `.json`；调研见 `.audit/adhoc_agents/2026-10-19/open-audio-models/` |
| MOSS-VoiceGenerator 本地（按文字描述设计音色并念台词，中英文，不收参考音频；`tools/local_voice.py`，权重 `.cache/models/moss-voicegenerator/` + 编解码器 `.cache/models/moss-audio-tokenizer/`，独立环境 `.cache/venvs/moss-voice/`（transformers 5.0），2026-10-21） | 允许 | 代码与权重 Apache-2.0（huggingface.co/OpenMOSS-Team/MOSS-VoiceGenerator、MOSS-Audio-Tokenizer）。训练数据来源未披露 ⚠️。本地运行不收费、不走请求日志，生成记录写在产物旁的 `.json`；第三方原版语音不得作输入 |
| MOSS-TTS-Local-Transformer-v1.5 本地（给参考录音、按其音色念台词的声音克隆，48 kHz；`tools/local_voice_clone.py`，权重 `.cache/models/moss-tts-local-v1.5/` + 编解码器 `.cache/models/moss-audio-tokenizer-v2/`，环境 `.cache/venvs/moss-voice/`，2026-10-21） | 允许（模型本身） | 代码与权重 Apache-2.0。训练数据来源未披露 ⚠️。**参考录音的权利另算**：克隆第三方原版语音须有用户书面决定并记进该卡 refs.md（目前只有 dota_yingxiong `m4`，follow-up 044，用户自担风险）；人声克隆另须声主授权。本地运行不收费、不走请求日志 |
| Qwen3-TTS 1.7B 本地（VoiceDesign 文字设计音色 + Base 克隆，中英等 10 种语言；权重 `.cache/models/qwen3-tts-{voicedesign,base,tokenizer}/`，环境 `.cache/venvs/qwen3-tts/`（torch 2.11 cu128）；选型实验 `edu_videos/_shared/voice_lab/lab_qwen.py`，2026-11-08） | 允许（选型试用） | 代码与权重 Apache-2.0（huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign 模型卡）；未见附加使用政策。训练数据来源未披露 ⚠️。本地运行不收费、不走请求日志（edu_videos follow-up 005） |
| VoxCPM2 本地（括号描述设计音色 + 参考音克隆，30 种语言，48 kHz；权重 `.cache/models/voxcpm2/`，环境 `.cache/venvs/voxcpm/`；选型实验 `edu_videos/_shared/voice_lab/lab_voxcpm.py`，2026-11-08） | 允许（edu_videos 频道配音，2026-11-08 用户选定；入口 `tools/edu_voxcpm.py`） | Apache-2.0，模型卡写明可商用；模型卡另写「严禁冒充、欺诈、虚假信息，AI 生成内容须明确标注」——本仓库只用自设计音色、成片标注 AI 配音，符合 ⚠️。训练数据未披露 ⚠️。本地运行不收费、不走请求日志（edu_videos follow-up 005） |
| VibeVoice 1.5B / Large（本机 `C:\models\vibevoice\` 已有） | **不用** | 权重 MIT，但模型卡写明仅供研究、不建议商用部署，且每条生成音频嵌入可听见的 AI 声明与水印，不能作成片旁白（2026-11-08 核查，edu_videos follow-up 005）；用户要用须另行决定 |
| ACE-Step 1.5 本地（歌曲、主题曲；权重在 `.cache/models/acestep/`，2026-10-19） | 允许 | 代码与权重 MIT；产出可商用。克隆或模仿真人歌手声音另需授权 |
| TripoSR 本地（单图转 3D，带顶点色网格；`tools/local_3d.py`，代码 `.cache/src/TripoSR`，权重 `.cache/models/triposr/` + DINO 只取 config `.cache/models/dino-vitb16/`，环境 `.cache/venvs/triposr/`，2026-11-06，zhenshi_chidu follow-up 002） | 允许 | 代码与权重 MIT（github.com/VAST-AI-Research/TripoSR README、HF stabilityai/TripoSR license tag）；DINO config Apache-2.0；依赖 rembg 代码 MIT（**去背景模型锁定 `isnet-general-use`，Apache-2.0，放 `.cache/models/rembg/` 校验 sha256；rembg 2.0.87 起默认模型 bria-rmbg = BRIA RMBG 2.0，HF 许可标 other：开放权重仅限非商用、商用须与 BRIA 另签协议，禁用**，2026-11-07 实测发现）、xatlas MIT、trimesh MIT、transformers Apache-2.0；原依赖 torchmcubes（MPL-2.0）本机编译不了，换 scikit-image（BSD-3）。训练数据来源（Objaverse 子集）各条许可不一 ⚠️。本地运行不收费、不走请求日志，生成记录写在产物旁的 `.json`；参考图若由收费服务生成，照常在其归属记请求日志。**TRELLIS / TRELLIS.2 不用**：依赖 diffoctreerast、nvdiffrast、nvdiffrec，均为非商用许可（证据见 `ai_videos/zhenshi_chidu/0_research/toolchain_licenses.md`） |
| Hyper3D / Rodin | 有条件（Creator 档及以上） | 免费档不可 |
| Cascadeur（仓库入口已随旧流程删除，2026-10-11） | Pro / Teams 允许；Indie 有条件；Free **不用** | Indie 要求个人或公司过去 12 个月收入或融资低于 10 万美元 |
| Udio | **不用** | 已不能导出 |
| CapCut / 剪映（官方 ChatGPT·Codex 插件与 MCP、编辑器内素材，及 VectCutAPI 等社区草稿工具） | **不用**（2026-11-08，follow-up 351、352） | 条款：公司内容（模板、字体、音效、特效、滤镜、贴纸、文字模板、动画等）能否商用「因产品而异」，只有 Pippit 明确允许；Commercial sounds 只许发到 CapCut、TikTok；商用与非商用素材混用即整片只限非商用；AI 产出未写明可商用；禁止自动化脚本与逆向工程。国际版条款没有把剪辑服务本身限于非商用（韩国条款与 iOS 安装许可写「个人使用」除外），**只用自备素材、只让它剪**在条款上不被禁止，但上传的素材要授予 CapCut 永久、可再授权的许可，并视为非机密；字幕默认字体也是公司内容。插件调用须在 Codex 里先写请求日志，入口 `tools/mcp_request_log.py`（MCP 宿主调用的两段式日志，follow-up 354）。**唯一例外**：chuanyue_yiri EP01 s3 剪辑盲测，只上传三条自备素材、禁用全部公司内容，成片经 `tools/edit_blind_test.py check` 机检（chuanyue_yiri follow-up 039，测试目录 `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/`）。证据见 `.audit/adhoc_agents/2026-11-08/capcut-mcp/` |
| 可灵 Kling | **不用（演员库直连出图功能已删除）** | 未经书面许可不得商用，并要求在产出上标注其品牌；手动用可灵出图同样不行 |

有条件的工具：调用前确认账户确实在允许的套餐档。所有工具都不保证产出可获版权，且多数要求使用者自负侵权责任。

## 日志归属

`request_log.md` 在首个请求时创建，目录本身是唯一分组依据。没有归属就禁止调用。

| 请求目标 | 唯一日志位置 |
|---|---|
| `…/episodes/epNN/scenes/sN/shots/stN/…`（旧布局亦兼容）、该集配音/后期 | `…/episodes/epNN/request_log.md` |
| 本剧所有人物、服装变体、建立视频、人物声样 | `…/characters/request_log.md` |
| 本剧所有环境资产、plate、环境三维资产 | `…/background/request_log.md`；未迁移旧剧仍为`…/scenes/request_log.md` |
| 道具、装备、声音、音乐、技能 | 各自 `props/`、`equipment/`、`voices/`、`music/`、`skills/` 根的 `request_log.md` |
| 系列共用资产 | `_series/{characters,background,props,…}/request_log.md`（旧scenes兼容），不复制到成员剧 |
| 音乐库或无资产分类的账户查询 | 对应库/所属剧根的 `request_log.md` |
| 独立软件服务（不伪造剧归属） | 仓库 `.audit/service_requests/<服务名>/request_log.md`；`RequestLog` 接受该专用根，现有制作 UI 的剧日志列表不展示此位置 |

例：`ai_videos/shengji_zhilu/2_世界观人设/characters/request_log.md` 与 `ai_videos/shengji_zhilu/episodes/ep01/request_log.md`。

## Suno 浏览器服务（2026-10-22）

- **音频默认路由（2026-10-22 用户确认）**：环境音、背景音、音效、背景音乐、主题曲、片头/片尾曲等所有新音频生成统一默认走本服务 API/MCP/UI，制作步骤见 [声音与音乐](../../skills/ai-videos-pipeline/modules/sound.md)。对白配音、克隆等需求先查 capabilities，未支持则记录能力缺口；不静默回退其他提供方或本机模型。只有用户明确选用替代引擎时才切换；既有音频继续复用，混音/剪辑/响度处理不属于生成。
- 入口与说明：`projects/suno_browser_service/README.md`；本机独立 Chrome profile，FastAPI 任务接口，兼容 Browserless 原生 Playwright endpoint（远程未实测）。用户明确授权本服务自动点击 Create 与官方下载，例外不扩展到其他视频生成。
- 默认 Advanced 纯音乐，唯一任务标题关联两首结果；Advanced 人声须提供歌词。v0.2 增加 Simple/Sounds、严格选项、参考上传、JSON CLI、stdio MCP 与共用 `suno-music` skill；新增功能只有离线验证，真实账号待解除验证码后逐项校准。Simple 可描述自动写词/编辑意图，引用/Remix 的商用限制仍按上表，不因接口可用而豁免。登录失效、验证码、访问拒绝、配额不足或控件不唯一时暂停。未知提交不重提，只恢复已确认歌曲的下载。
- 浏览器连接、导航、准备、提交、轮询及官方下载先经 `tools/service_request.py::RequestLog`；独立调用归 `.audit/service_requests/suno_browser_service/`，制作调用显式指定 `ai_videos` 内 target。网页自己的内部 HTTP 不宣称逐条拦截；费用未知不估报实扣。
- [当前条款](https://suno.com/terms) 明确限制 robots / scraping，未查到付费账号自动化例外；本仓库授权不等于平台许可。只走官方 Download 菜单，不取播放器流替代，不绕过验证码、封禁、生成或下载额度。[官方导出](https://help.suno.com/en/articles/2409921)、[下载额度](https://help.suno.com/en/articles/13876865)。
- 2026-10-22 已完成普通 Chrome 人工登录，实测为 Pro（首次生成前 2470 credits / 27 downloads）。v6 Advanced 表单已适配；EP1 M01/M02 各点击 Create 一次但无确认歌曲，M02 随后出现验证码。自动化队列持久暂停，不绕过、不重复 Create；费用未确认，实际下载仍未验收。
- Google 人工登录曾遇自动化浏览器拒绝（2026-10-22）：`login.ps1` 改为普通 Chrome 手动登录，专用窗口关闭后才由服务验证并保存会话；登录期间无 Playwright/调试端口。不修改安全设置、不绕过验证。该入口已完成首次登录；当前阻塞为上文的生成验证码，不能把登录成功当生成/下载验收。
- 2026-11-03 常驻窗口模式（suno_browser_service follow-up 008）：`open-window.ps1` 以专用 profile 开普通 Chrome，调试端口仅 `127.0.0.1:9333`，服务经 CDP 在独立标签页操作，登录 / 验证码由人在同一窗口完成，不隐藏自动化特征、不代解验证码。同日实测 Advanced 纯音乐首次完成生成→认领→官方下载：任务 `fa07658f…`、`ea35c3d5…`、`75c2aee8…` 各 2 首 MP3（约 3–4 分钟/首），费用未读回；`b29b0693…`（hCaptcha 未完成）与 `aabefc6d…`（Create 后过早刷新）在库中未见歌曲，保持 uncertain 不重提。Create 后歌曲行 3–5 分钟才出现；下载前须等 Download 可用。
- 2026-11-03/04 排行榜配乐（suno_browser_service follow-up 009）：服务窗口连续出问题（工作标签页卡死、退出卡死的 Chrome 占着 9333、cookie 提示挡住 Create、新出的「Clear entire form?」确认框藏起表单）均已修，排行榜 14 期配乐任务重跑。完成并下载：ep05、ep06、ep12、ep15、ep16（只有 72 s / 60 s）、ep17、ep18、ep19，各 2 首；ep03 一个任务下载中。ep11、ep13、ep14、ep20 及各自 v2 点了 Create 但库里没有歌（服务确认后才另建新键，未生成不扣点）。账号页读回：Song credits 剩 2370 / 2500；**Downloads remaining 只剩 1**（Pro 月度下载上限），已写 `automation-paused.json` 暂停新任务，等用户决定。页面默认型号曾从 v6-mini 变成 v6：v6-mini 当晚点 Create 后一直不出歌，v6 长度不稳定（60 s–220 s）。

## Dreamina CLI

- 本机入口 `~/bin/dreamina.exe`（只此一个版本，不留旧版备份，用户 2026-10-21）；2026-10-20 Windows Defender 病毒库 1.461.107.0 把 1.4.20 误判为 `Trojan:Script/Wacatac.C!ml` 隔离，用户以管理员还原；再被隔离时请用户还原并把 `C:\Users\light\bin\` 加进排除项，代理没有管理员权限；OAuth 登录复用本机 CLI 状态，`login` / `login --headless`，查询 `user_credit`、`list_task`、`query_result --submit_id=…`。
- 图片：`text2image`、`image2image --images=<按顺序的路径列表>`；图片帮助当前列 model_version 3.0/3.1/4.0/4.1/4.5/4.6/4.7/5.0。图片模型上限、resolution_type 与 ratio 以 `-h` 为准。
- 视频：`text2video`、`image2video`、`frames2video`、`multiframe2video`、`multimodal2video`。全能参考重复传 `--image` / `--video` / `--audio`。当前帮助的9图/3视频/3音频、4–15秒生成是Seedance2.0系列口径；参考音频2–15秒也是该帮助声明，不扩充成2.5已实测范围。
- **Seedance2.5**：使用 `--model_version=seedance2.5`。官方单次上限为30图、10视频、10音频、30秒生成；共用数值唯一维护在 `tools/previz/seedance_ref.py` 的 `MODEL_LIMITS`。六模块剧在剧 `workflow.json` 的 `prompt.model` 声明模型（《魔兽世界》为 `seedance2.5`），资料包 `tools/shot_pack.py` 按该模型读取上限，不照抄旧帮助数值。2.0系列仍读取旧上限，未知模型不借用2.5规格。
- 2026-10-03本机/当前账号实测：魔兽世界EP1 shot1完整14PNG+2MP3，10秒、720p、16:9，任务 `ef09984b-3878-48f9-919c-ddbffd184266` 返回success与 `credit_count=200`；下载实测1280×720/10.08秒/H.264+AAC。证据为该集request_log.md及 `.audit/adhoc_agents/2026-10-03/shot01-dreamina-25/state.json`。这证明本入口接受2.5和该组合；30图/10视频/10音频/30秒的满额组合、1080p、更多CLI flag与其他账号仍未付费实测，不杜撰支持参数或额外收费探测。30秒是**输出镜长**上限，不等于每条参考视频也能30秒；参考媒体时长、像素、帧率及文件规格另按参考规则检查。
- 使用 `--poll=0` 提交并保存 submit_id，随后独立 query_result；积分在提交阶段扣减，超时任务只补收。
- 2026-10-16 两步出片（ai_video_management follow-up 265）：草稿 `--video_resolution=480p`。CLI 帮助以 `dreamina multimodal2video -h` 为准，旧版帮助不认 2.5 时先查 `https://lf3-static.bytednsdoc.com/obj/eden-cn/psj_hupthlyk/ljhwZthlaukjlkulzlp/version.json` 有没有新版。**2026-10-16 实测：本入口 Seedance 2.5 不收 480p**——EP1 s1 st1 上传完成后服务端回 `video_resolution must be one of 720p, 1080p`，没有 submit_id、不扣费（request_id `9e4433b733c24e9ebba4deb7be722e68`，见该集 request_log.md）；同一回执说明 2.5 在本入口接受 1080p（未付费实测）。原因是本机 CLI 太旧（1.4.5，2026-06-04）：同日升级到官方 1.4.20（2026-10-16，`jimeng.jianying.com/cli` 安装脚本的同一下载地址，旧二进制备份 `~/bin/dreamina_1.4.5_backup` 已于 2026-10-21 按用户要求删除，本机只保留一个版本）后，帮助写明 seedance2.5 收 480p / 720p / 1080p（VIP），每条及合计参考视频 / 音频 2–30 秒，`--video_resolution` 必填；s1 st1 7 秒 480p 草稿提交成功，84 积分（submit af624a10…）。正式条把用户通过的草稿作参考视频追加，参考视频规格按 `tools/previz/seedance_ref.py`。
- **Seedance 2.5 样片模式（Draft）**：即梦网页「Seedance 2.5（样片模式）」与火山 API `draft=true` 有，480p 样片之后出 1080p 成片会关联样片 ID、沿用 seed。2026-10-17 核对：本机 CLI 1.4.20（`version.json` 所示最新）帮助与二进制里都没有样片开关或样片模型值，草稿照旧是普通 `--video_resolution=480p`。用户定：只走 CLI，不接火山 API；CLI 支持样片模式后，草稿一律改用样片模式 480p（shengji follow-up 065）。升级 CLI 时先查 `multimodal2video -h` 有没有这个开关。
- 2026-10-10 本机实测上传（ep1_s1_st1，follow-up 229）：① `--image/--audio` 要传**绝对路径**，相对路径 0 个上传成功；② 上传在 ByteDance ImageX SDK 内部有固定超时，CLI 没有参数可调；③ 开着 Astrill（OpenWeb）时，CLI 随机把文件分到 `tos-d-x-*` 与 `tos-d-{lq,hl,lf}.bytedancevod.com`，后者全部超时、前者全部成功——在 hosts 里把 `tos-d-lq/hl/lf.bytedancevod.com` 指向 `tos-d-x-hl` 的 IP（证书是 `*.bytedancevod.com`，握手通过）后 6 个文件 1–6 秒传完，提交成功（submit `f31decd5…`，8 秒 720p，160 积分）；hosts 里的 IP 是负载均衡节点，会变，失败时先重新解析 `tos-d-x-hl`。上传阶段失败均不扣费。资料包的 `upload/` 副本（ASCII 文件名、长边 ≤1536、JPEG）就是给 CLI 上传用的。
- 2026-10-11 本机实测下载（follow-up 231）：① 视频结果从 `v*-artist.vlabvod.com` 下，Astrill 下偶发超时，生成已扣费、只重下不重提（`tools/shot_take.py` 下载失败重试 3 次，`poll <submit_id>` 补收）；② **图片**结果在 `p*-dreamina-sign.byteimg.com`（国内 CDN cdnhwc2），开着 Astrill 时 TLS 握手全部超时，Python 与 CLI 下载都拿不回来，生成已扣费——图片任务在这种网络下改走 Codex 或 ElevenLabs（2026-10-11 起各出图器 auto 已是 Codex → ElevenLabs → 即梦），不要反复重提即梦；③ 上传 `ApplyImageUpload` 阶段失败也不扣费，与 upload phase 一样可重试。
- 2026-10-22 实测（dota_yingxiong follow-up 066）：① 生成后回 `fail` + `code=2053; OutputVideoCopyright`（「生成的视频里包含受版权保护元素」）是明确失败，同一 prompt 原样重提一次即成功（k651），是否扣费以回执与账户为准；② 建立视频下载频繁 SSL EOF 断开、进程退出时任务已成功——不重提，用 `python tools/gen_turntable_videos.py --drama <剧> --only <卡> --force --harvest` 按最新 submit_id 补收（`--force` 时旧片还占着文件名也照收，收回后旧片挪进 `_deleted/`）。
- 首尾构图必须选专门 `frames2video --first … --last …`，不能假定multimodal普通两张参考自动成为端点。[官方FAQ](https://dreamina.capcut.com/ai-video/ai-video-reference-inputs-faq)明确区分两种模式；2026-10-03本机frames2video帮助仍只列2.0及3.x，2.5/18秒在此入口尚未实测，不把multimodal2video已成功推及所有子命令。multiframe2video无model/resolution覆盖，不能冒称其默认型号是2.5。
- CLI退出0或返回submit_id不等于提交成功；先用 `tools/dreamina_receipt.py` 检查回执gen_status/fail_reason。2026-10-03 shot01 round02在upload phase明确失败，却带ID且后续query一直querying；这种回执停止轮询，保留失败及未知费用，确认上传阶段失败后才允许新请求重试。无明确失败的超时/未知提交仍不能重提。
- **2026-11-08 用户定：以后出图全部用 Codex（`tools/codex_image.py` / 各出图器 `--engine auto` 现在只用 Codex）；没有用户明确允许不用 ElevenLabs，ElevenLabs 失败也不再是自动回退的一环。** 下面关于 ElevenLabs 的说明只在用户允许时适用。
- 图片：**2026-10-17 起即梦不出图**（follow-up 270），各资产出图器只用 Codex 内置出图（2026-11-08 起；ElevenLabs 出图须用户明确允许，credit 留给配音，follow-up 341；`tools/image_engine.py`）；`RequestLog` 拒绝即梦的 `text2image` / `image2image` 与图片接口，不论归属。`tools/dreamina_image.py` 只剩字数常量与旧任务的查询 / 取回辅助。视频入口：镜头出片由 `tools/shot_pack.py cmd <集目录> <镜头key>` 打印提交命令，`tools/shot_take.py submit|poll` 提交、查询、下载并建条目录（经 `tools/service_call.py` 先记日志）；人物建立视频 `tools/gen_turntable_videos.py`（一般经 `tools/char_assets.py` 调用）；技能视频（dota_yingxiong 技能卡）`tools/skill_pack.py sync|submit|poll`（同一 `service_call.py` 入口，日志随技能目录落 `characters/request_log.md`）。手工命令也经日志封装：

```powershell
python tools/service_call.py --target ai_videos/shengji_zhilu/2_世界观人设/characters -- dreamina user_credit
python tools/service_call.py --target ai_videos/shengji_zhilu/episodes/ep01 -- dreamina query_result --submit_id=<任务ID>
# 即梦出图（text2image / image2image）已禁用（follow-up 270），会被 RequestLog 拒绝；视频走 shot_take.py
```

来源：[官方 CLI](https://dreamina.capcut.com/tools/dreamina-cli)、[Seedance2.5官方发布说明](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)；本机 `dreamina text2image -h` / `multimodal2video -h`；本集请求日志与下载媒体；仓库对应生成器。

## ElevenLabs API

- 基址 `https://api.elevenlabs.io/v1`，header `xi-api-key`；从环境或 gitignored `.env` 的 `ELEVENLABS_API_KEY` 读，不写入日志。
- 图像：`POST /flows/image`，JSON 包含 model_id、完整 prompt、aspect_ratio、resolution、images；gpt-image 家族可带 quality，其余模型不能盲目传此字段。参考支持 inline_base64、generation_id 和资产引用，具体模型 schema 以文档为准。
- 响应 id/status；`GET /flows/image/{generation_id}` 到 completed，使用 content_url 下载；failed 即失败，保留任务 ID。套餐权限、key 操作权限与模型准入分别判断，不能由网页可用推断 API 可用。
- 视频：`POST /flows/video` 同样异步，经模型专属 schema；现有仓库未实现该入口，新增前接同一个 RequestLog。
- 音乐（Eleven Music）：不用。自助套餐排除影视用途，仓库入口 `gen_bgm_sk2.py`、`gen_music_szzl.py` 与魔兽世界两首草稿已于 2026-10-09 删除（follow-up 221；回执与哈希存 `.audit/adhoc_agents/2026-10-09/commercial-use-terms/removed_eleven_music/`）。
- TTS、音效、音频分离另有官方 API；现有网页登录提示词不等于 API 调用。新增入口也必须记录全文 text、voice_id、model_id、voice_settings 和参考文件。
- 声音设计与台词合成入口 `tools/voice_design.py`（2026-10-18）：`design`（`POST /v1/text-to-voice/design`，只发文字描述，不支持 `reference_audio_base64`）→ `save`（`POST /v1/text-to-voice`）→ `tts`（`POST /v1/text-to-speech/{voice_id}`）；每步经 `RequestLog`，音频写盘、日志只记时长 / 字节 / sha256。归属用 `--target` 指到人物卡 `voice/` 下。
- 图像统一入口 `tools/image_fetch.py`：`create(..., target=<目标文件>)` → `wait_download(..., out=<目标文件>)`。不能省 target。

来源：[图片创建](https://elevenlabs.io/docs/api-reference/flows/image/create)、[异步图像/视频流程](https://elevenlabs.io/docs/eleven-api/guides/cookbooks/image-and-video)、[音乐](https://elevenlabs.io/docs/api-reference/music/compose)。

## Hyper3D / Rodin API

- 当前官方 v2 基址 `https://api.hyper3d.com/api/v2`；仓库已有适配器使用历史 `https://hyperhuman.deemos.com/api/v2` 与 Sketch/Regular tier。两套参数不可混用，此次保留已接入账户的旧调用，不擅自迁移模型/计费档位。
- `Authorization: Bearer …`；仓库变量 `HYPER3D_API_KEY`，官方示例使用 `RODIN_API_KEY`。先看实际入口，不把变量名当不同服务。
- `POST /rodin` 用 multipart/form-data：完整 prompt、最多5张 images、tier、mesh_mode、geometry_file_format、texture_mode、bbox_condition 等，支持组合以具体版本文档为准。
- `jobs.subscription_key` 供 `POST /status`；顶层 uuid 供 `POST /download` 的 task_uuid。两个 ID 不可混淆。所有 jobs Done 才下载，有 Failed 即停止；429 尊重 Retry-After，查询退避。
- bbox_condition 是归一化比例，不是场景中的米数；生成网格仍需 `whitemodel_normalize.py` 的尺度/朝向验收。
- 入口 `tools/hyper3d_fetch.py --out <ai_videos下目标文件>`；调用前日志含实际 multipart 文本字段和全部图像元信息，结果含 uuid/consumed。付费创建取消自动网络重提；没有明确任务 ID 时先检查服务端记录。
- `addon.py` 的 Rodin main_site / fal.ai 路径均接入日志；必须重载更新的插件，将工程保存在本仓库 ai_videos 下，或设置 `REQUEST_LOG_TARGET` 指向归属目录；找不到日志入口就停止。当前软件流程优先直接适配器。

来源：[官方 Quick Start](https://docs.hyper3d.ai/en/get-started/quick-start)、[v2 概述](https://docs.hyper3d.ai/en)；仓库 `hyper3d_fetch.py`。

## Cascadeur（已删除，2026-10-11）

仓库的 Cascadeur 脚本桥、动作编排工具、skill 与 MCP 声明已随旧流程删除（ai_video_management follow-up 233）；新流程 previz 用绿幕色块人偶，不调用 Cascadeur。重新接入前先按本页调用契约接入 `RequestLog` 并核对商业用途表，未接入就不调用。

## 图片服务限制（2026-10-03 scene/bg；2026-10-17 扩到所有图片，follow-up 270）

- 所有剧未来生成/重生的任何图片（scene/bg 锚点、plate、变体、shot 专用背景，以及人物、道具、物件、装备）一律用 Codex 内置出图；ElevenLabs（GPT 最新图像模型）只在用户明确允许时用（2026-11-08，follow-up 341）；禁止 Dreamina/Seedream、自动回退与绕过共用入口。即梦只用于视频。
- 2026-10-03 已查 OpenAI 官方图像指南与 ElevenLabs 在线 OpenAPI：最新 GPT 图像型号为 `gpt-image-2.5-sunburst` / `gpt-image-2.5-flare`，ElevenLabs `/v1/flows/image` 实际接受这两个 `model_id`。高质量场景当前默认 Sunburst；2.5 支持 `quality=low/medium/high/xhigh/max`、`resolution=1K/2K/4K`、`aspect_ratio=16:9`。此记录为当日能力证据，后续指定“最新”仍要重新核对，不把固定型号永远当最新。
- BG2 本次通过现有 ElevenLabs Flows 适配器指定 `gpt-image-2.5-sunburst`，不是 OpenAI 直连，也不冒称内置 image_gen 的不可观测型号。实际提交/查询/下载全部使用 `RequestLog`；模型/质量/分辨率、参考 SHA、生成 ID 和返回费用均按实记录，未返回费用记未知。
- 官方来源：[OpenAI 图像指南](https://developers.openai.com/api/docs/guides/image-generation)、[Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)、[ElevenLabs 创建图像](https://elevenlabs.io/docs/api-reference/flows/image/create)；在线 schema：`https://api.elevenlabs.io/openapi.json`。本次能力审计：`.audit/adhoc_agents/2026-10-03/bg2-gpt-refresh/capabilities.json`。

## OpenAI 内置图像生成工具

- 当前会话暴露 `image_gen.imagegen`，直接调用 OpenAI 图像生成能力；无需本地 `OPENAI_API_KEY`。这不是 ElevenLabs 或 Dreamina 的转发入口。
- 本环境参数只有 prompt、transparent_background 与可选参考图；不暴露 model、quality、API endpoint 或实时费用。不能把文档中的最新型号当成本次工具实际使用型号。
- 2026-10-03 官方 API 文档推荐 GPT Image 2.5 Sunburst / Flare；`chatgpt-image-latest` 已标弃用，名称中的 latest 不代表当前最新。
- 每次工具调用先用同一 `RequestLog.append` 落 request 事件（完整工具参数、授权、实际可观测的模型信息和归属），成功落盘后才调用；返回或抛错再追加相同 request_id 的结果/错误。工具内部 HTTP 不可逐条观察，结果未返回型号、费用时记未知，不自动再生成。
- 无所属剧的能力测试归 `ai_videos/_research/service_tests/`，日志共用 `_research/request_log.md`；不新建短剧或改动现有剧。参考图和项目资产继续按所属集/资产分类归档。

来源：[OpenAI 图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)、[chatgpt-image-latest 状态](https://developers.openai.com/api/docs/models/chatgpt-image-latest)；当前工具 schema。

## Codex 内置出图（Claude 等代理经 Codex CLI 调用）

- 入口 `tools/codex_image.py`（skill `codex-imagegen`）：先写 `RequestLog`（provider `codex_imagegen`），再在临时空目录、`--sandbox read-only` 下跑 `codex exec --json`，指令经 stdin 传入，要求 Codex 原样用 prompt 只调一次内置 `image_gen`、不跑命令不写文件；参考图用 `--image` 按顺序附带。图片由脚本从 `$CODEX_HOME/generated_images/<thread_id>/` 拷到 `--out`（目标须在 `ai_videos/` 或 `edu_videos/<系列>/<知识点>/` 下，决定日志归属；已存在不覆盖，除非 `--overwrite`）。
- 用本机 `codex login` 的 ChatGPT 订阅额度，不要 `OPENAI_API_KEY`；不能只把 Codex 的 imagegen SKILL.md 复制给 Claude，那不带出图工具本身。
- 内置工具不暴露图像型号、quality、尺寸与费用：日志记「未知」；结果记 thread_id、Codex 用量（tokens）、会话记录里的 `revisedPrompt`、`failure`、`savedPath` 与图片 SHA256。`revisedPrompt` 与原 prompt 不同时脚本提示。
- 没拿到图就报错并留痕，**不自动重提**；先查 `generated_images/<thread_id>/` 与 `~/.codex/sessions/**/rollout-*-<thread_id>.jsonl`，可能已生成（超时也会扫一次）。
- `--model` 只换 Codex 代理模型，不是图像模型。比例写在 prompt 里，不能保证精确像素。
- **2026-11-08 起（用户定，follow-up 341）：`--engine auto` 只用本入口；ElevenLabs 出图须用户明确允许，credit 留给配音。** 下面是此前的 ElevenLabs 优先规则，只在用户允许用 ElevenLabs 出图时适用——默认顺序（2026-10-17 用户定，follow-up 275，取代 270 的 Codex 优先）：各资产出图器 `--engine auto` 先走 ElevenLabs（`gpt-image-2.5-sunburst`），**ElevenLabs 有任何失败**（额度 / 套餐、审核拦截、参数错、网络、超时，`image_engine.fallback_ok`）就走本入口（`codex_image.render`，画幅比例写进 prompt 末行），不问用户（2026-10-22 用户定，dota_yingxiong follow-up 066，取代 275 的只看额度）；ElevenLabs 那条结果未知的请求照样记未知、不向 ElevenLabs 重提。也可直接点名 `--engine codex`（ElevenLabs 已知没额度时省一次失败调用）。图片不用即梦。
- 2026-10-17（shengji follow-up 062）：网络不稳时 Codex 出完图还会断线重连到超时；`run_codex` 看到会话记录里的图已落盘，等 15 秒就结束进程（结果记 `early_exit`）。并发 8–10 路时偶发 429（请求过多，未出图，属明确失败），6 路基本没有。
- 2026-10-11 实测（follow-up 237）：codex-cli 0.160.0，文字出图一张，约 140 秒，返回 941×1672 PNG（prompt 写 9:16），归 `ai_videos/_research/request_log.md`；带参考图、透明背景尚未实测。
