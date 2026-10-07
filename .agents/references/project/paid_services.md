# 外部服务：调用与请求留痕

核对日期：2026-10-03。本文维护本仓库实际入口；Dreamina含用户授权的单镜实测，其余服务的核查不表示已付费验证。参数按目标模型、官方文档及服务返回值核对，旧CLI帮助不能覆盖较新模型。`Dreamina` 为即梦 CLI，用户所写 dreaming 指此服务。

## 必须执行的调用契约

全局适用范围由根目录 `AGENTS.md` / `CONVENTIONS.md` § 外部服务请求审计（全局必经）规定：Claude、Codex 与其子任务共用；所有新旧剧、季、集、共享资产、续跑、局部修复、独立 skill 和手工调用均适用。旧剧的产物遗留规则不豁免今后的请求审计；后续接入收费服务也先接同一记录入口。本文只维护服务细节、日志字段与分组。

1. 每次调用前读本页，确定服务、操作、剧/集/资产归属、完整请求、参考文件及输出位置。
2. 所有仓库调用经 `tools/service_request.py` 的 `RequestLog`：先追加 request 事件并落盘，再调用服务；日志不能写就停止。结果或异常另追加同 request_id 的事件，不覆盖历史。
3. 正文保留完整 prompt / 台词 / 脚本 / JSON 参数、CLI argv、模型、比例、分辨率、时长、参考顺序、时间、目标路径、PID、超时及请求指纹。文件记录路径、大小、SHA256；base64 记录解码后的大小和 SHA256，不复制媒体本体。
4. API key、Bearer、cookie、secret、签名 URL 的鉴权参数脱敏。不要把凭据写进 prompt / 脚本 / CLI 参数。结果保留服务任务 ID、状态及原样返回的费用字段；没有费用字段即未知，不能把估算当实扣。
5. 提交超时不代表没提交，不自动重复收费请求；先用任务 ID 查询/补收。仅明确上传失败且尚未提交时允许自动重试；结果未知时停止重提。每次由仓库发起的查询、下载和重试也留痕。Dreamina CLI 的内部上传/轮询不可观测，只能记录该次 CLI 调用与参数，不能冒充逐 HTTP 请求日志。
6. UI 左侧「请求日志」按归属选文件、分页查看完整事件；原始 request_log.md 可在目录树查看。UI 提供查看/审查，不额外引入审批流程；既有「生成永远人点」及剪辑批准规则继续有效。
7. 外部 MCP/另一份安装插件/用户直接终端命令不能被本仓库自动拦截。代理必须走下面的记录入口；未接入的第三方入口需先接入，不能直接调用后声称已记录。历史请求不补造。

## 日志归属

`request_log.md` 在首个请求时创建，目录本身是唯一分组依据。没有归属就禁止调用。

| 请求目标 | 唯一日志位置 |
|---|---|
| `…/episodes/epNN/scenes/sN/shots/stN/…`（旧布局亦兼容）、该集配音/后期 | `…/episodes/epNN/request_log.md` |
| 本剧所有人物、服装变体、建立视频、人物声样 | `…/characters/request_log.md` |
| 本剧所有环境资产、plate、环境三维资产 | `…/background/request_log.md`；未迁移旧剧仍为`…/scenes/request_log.md` |
| 道具、装备、声音、音乐、技能 | 各自 `props/`、`equipment/`、`voices/`、`music/`、`bgm/`、`skills/` 根的 `request_log.md` |
| 系列共用资产 | `_series/{characters,background,props,…}/request_log.md`（旧scenes兼容），不复制到成员剧 |
| 公共演员库/音乐库或无资产分类的账户查询 | 对应库/所属剧根的 `request_log.md` |

例：`ai_videos/shengji_zhilu/2_世界观人设/characters/request_log.md` 与 `ai_videos/shengji_zhilu/5_6_分镜与prompt/episodes/ep01/request_log.md`。

R2资产路径迁移使用`tools/assets/r2.py`的现有存储能力，经`RequestLog.invoke`逐次记录查询、复制或上传；目标归属迁入的资产集合。先确认对象复制/上传成功，再更新`ai_videos/assets.json`对应路径；不提前声明远端已迁移，不自动删除旧对象，不同步其他剧的未提交媒体。SDK内部重试不可逐次观测，日志记录外层调用边界；存储操作不授权媒体生成。

## Dreamina CLI

- 本机入口 `~/bin/dreamina.exe`；OAuth 登录复用本机 CLI 状态，`login` / `login --headless`，查询 `user_credit`、`list_task`、`query_result --submit_id=…`。
- 图片：`text2image`、`image2image --images=<按顺序的路径列表>`；图片帮助当前列 model_version 3.0/3.1/4.0/4.1/4.5/4.6/4.7/5.0。图片模型上限、resolution_type 与 ratio 以 `-h` 为准。
- 视频：`text2video`、`image2video`、`frames2video`、`multiframe2video`、`multimodal2video`。全能参考重复传 `--image` / `--video` / `--audio`。当前帮助的9图/3视频/3音频、4–15秒生成是Seedance2.0系列口径；参考音频2–15秒也是该帮助声明，不扩充成2.5已实测范围。
- **Seedance2.5**：使用 `--model_version=seedance2.5`。官方单次上限为30图、10视频、10音频、30秒生成；共用数值唯一维护在 `tools/previz/seedance_ref.py` 的 `MODEL_LIMITS`。新剧与本次更新的魔兽世界在 `seedance.toml` 的 `[dreamina_cli]` 声明 `model_version = "seedance2.5"`，资料包按模型读取上限，不照抄旧帮助数值。2.0系列仍读取旧上限，未知模型不借用2.5规格；项目只有在实际入口另有明确限额时才显式覆盖对应max键。
- 2026-10-03本机/当前账号实测：魔兽世界EP1 shot1完整14PNG+2MP3，10秒、720p、16:9，任务 `ef09984b-3878-48f9-919c-ddbffd184266` 返回success与 `credit_count=200`；下载实测1280×720/10.08秒/H.264+AAC。证据为该集request_log.md及 `.audit/adhoc_agents/2026-10-03/shot01-dreamina-25/state.json`。这证明本入口接受2.5和该组合；30图/10视频/10音频/30秒的满额组合、1080p、更多CLI flag与其他账号仍未付费实测，不杜撰支持参数或额外收费探测。30秒是**输出镜长**上限，不等于每条参考视频也能30秒；参考媒体时长、像素、帧率及文件规格另按参考规则检查。
- 使用 `--poll=0` 提交并保存 submit_id，随后独立 query_result；积分在提交阶段扣减，超时任务只补收。
- 首尾构图必须选专门 `frames2video --first … --last …`，不能假定multimodal普通两张参考自动成为端点。[官方FAQ](https://dreamina.capcut.com/ai-video/ai-video-reference-inputs-faq)明确区分两种模式；2026-10-03本机frames2video帮助仍只列2.0及3.x，2.5/18秒在此入口尚未实测，不把multimodal2video已成功推及所有子命令。multiframe2video无model/resolution覆盖，不能冒称其默认型号是2.5。
- CLI退出0或返回submit_id不等于提交成功；先用 `tools/dreamina_receipt.py` 检查回执gen_status/fail_reason。2026-10-03 shot01 round02在upload phase明确失败，却带ID且后续query一直querying；这种回执停止轮询，保留失败及未知费用，确认上传阶段失败后才允许新请求重试。无明确失败的超时/未知提交仍不能重提。
- 图片入口：`gen_images_xianjian.py`、`gen_bg_assets.py`（其他人物/场景/装备生成器复用）；视频入口：`gen_turntable_videos.py`、旧 sk2 生成器。手工命令也经日志封装：

```powershell
python tools/service_call.py --target ai_videos/shengji_zhilu/2_世界观人设/characters -- dreamina user_credit
python tools/service_call.py --target ai_videos/shengji_zhilu/5_6_分镜与prompt/episodes/ep01 -- dreamina query_result --submit_id=<任务ID>
# 下面会消费积分，仅在用户请求生成后执行
python tools/service_call.py --target ai_videos/shengji_zhilu/2_世界观人设/characters -- dreamina text2image --prompt="完整画面描述" --model_version=5.0 --ratio=9:16 --resolution_type=2k --poll=0
```

来源：[官方 CLI](https://dreamina.capcut.com/tools/dreamina-cli)、[Seedance2.5官方发布说明](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)；本机 `dreamina text2image -h` / `multimodal2video -h`；本集请求日志与下载媒体；仓库对应生成器。

## ElevenLabs API

- 基址 `https://api.elevenlabs.io/v1`，header `xi-api-key`；从环境或 gitignored `.env` 的 `ELEVENLABS_API_KEY` 读，不写入日志。
- 图像：`POST /flows/image`，JSON 包含 model_id、完整 prompt、aspect_ratio、resolution、images；gpt-image 家族可带 quality，其余模型不能盲目传此字段。参考支持 inline_base64、generation_id 和资产引用，具体模型 schema 以文档为准。
- 响应 id/status；`GET /flows/image/{generation_id}` 到 completed，使用 content_url 下载；failed 即失败，保留任务 ID。套餐权限、key 操作权限与模型准入分别判断，不能由网页可用推断 API 可用。
- 视频：`POST /flows/video` 同样异步，经模型专属 schema；现有仓库未实现该入口，新增前接同一个 RequestLog。
- 音乐：`POST /music` 的 prompt、music_length_ms、force_instrumental；`POST /music/detailed` 的 composition_plan 返回音频及详情。仓库入口 `gen_bgm_sk2.py`、`gen_music_szzl.py`；请求参数全部记入日志，音频本体记大小/哈希。
- TTS、音效、音频分离另有官方 API；现有网页登录提示词不等于 API 调用。新增入口也必须记录全文 text、voice_id、model_id、voice_settings 和参考文件。
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

## Cascadeur API

- 官方 Python 模块 `csc` 在 Cascadeur 进程内运行，不是独立 pip SDK 或云端逐次计费 HTTP API。软件许可与 Motion Generation 等功能费用须按账号核实，本次不虚构单次价格。
- 仓库本地脚本桥 `http://127.0.0.1:8765/run`，POST JSON `{"code":"完整Python脚本"}`，返回 ok/value/messages/error；它是本机安装的脚本服务器，不是官方公共云端 endpoint。
- 启动方式、已验证工程：`.agents/skills/ai-videos-cascadeur/SKILL.md`、`tools/cascadeur/casc_lib.py`。`scene.modify_update` 改控制器/关键帧，`app.current_scene()` 提供导出所需 view scene；用 FBX 烘焙动作给下游。
- `call_action` 可调用菜单 action；选择范围/时间轴前置条件与 GUI 一致。没有实测的 action 不标已验证。
- 调用必须指定归属：

```powershell
python tools/cascadeur/casc_run.py --target ai_videos/shengji_zhilu/5_6_分镜与prompt/episodes/ep01 -c "print(scene.get_current_frame())"
python tools/cascadeur/choreo.py <shot目录> --build
```

`choreo.py` 自动把 shot 归属传给桥。直接 MCP 调脚本不会自动走该桥，须先以相同 RequestLog 记录，再执行；没有记录机制不得直接调用。逐帧截图、改姿态分段验证、改完重开等现有工艺继续遵守。

来源：[官方 Python API](https://cascadeur.com/help/category/215)、[CSC 参考](https://cascadeur.com/python-api/csc.html)；仓库脚本桥与技能。

## scene/bg 图片服务限制（2026-10-03 用户更新）

- 所有剧未来生成/重生的 scene/bg 锚点、plate、变体和 shot 专用背景图只允许 GPT 最新图像模型或 ElevenLabs；禁止 Dreamina/Seedream、自动回退与绕过共用入口。旧图不批量回溯；人物、道具、装备、视频沿用各自规则。
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
