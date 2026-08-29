# drama_reverse_engine — 短剧逆向工程服务

客户上传第三方短剧 MP4（UI 内置上传按钮），系统逆向出 **小说 / 细致剧本 / 逐镜分镜 prompt**（对齐仓库 ai_video shot 契约，含台词配音 prompt）。**到这三层文字即止**——分镜 prompt 由用户自行拿去投喂视频生成模型。

> **follow-up 001（2026-07-15）**：Seedance 重生成侧（首帧生成/i2v/拼接/新片 vs 原片 QC/AI 定妆图）已整体删除。本服务专注逆向文字产出。
>
> **follow-up 002（2026-07-18）**：**默认零 API key**——视频理解与文学合成默认走本机已登录的 Claude Code CLI（每次调用 spawn 一个 headless 新会话 `claude -p`；视频理解＝ffmpeg 抽关键帧 + Claude 读图）。Gemini/Qwen、豆包降级为 env 显式切换的可选 keyed 后端。

Spec: `specs/development/drama_reverse_engine/final_specs/spec.md`（APPROVED 2026-07-14，follow-up 001/002 amended）。

## 架构

- `apps/api/` — FastAPI（127.0.0.1），路由按 `{aggregate}__route.py` 拆分
- `apps/worker/` — 管线 worker（文件系统队列 + 原子锁 claim，多进程可横向扩）
- `apps/probe_cli/` — FR-13 PoC 探针（视频理解连通性 Gemini/Qwen；无 key 时 skip）
- `apps/ui/` — React 前端（浅色主题）
- `libs/{infrastructure,domain,application,common}/` — DDD+CQRS 四层，依赖方向 apps→application→{infrastructure,domain}→common

**状态外置（NFR-A2）**：管线真相在工作区文件树 `workspace/{drama_id}/ep{NN}/`（产物在=阶段完成）；无 DB，每集 `pipeline_state.json` 即状态机。

**模型层可替换（NFR-O1）**：视频理解与文学合成各自 client Protocol，配置选型；测试在 Protocol seam 打桩。**默认后端＝本机 Claude Code CLI（零 key）**；`DRE_UNDERSTANDING=gemini_qwen`（需 GEMINI/DASHSCOPE key）、`DRE_COMPOSER=doubao`（需 ARK key）切回 HTTP keyed 后端。

## 管线（每集一条 job，follow-up 001 后 8 阶段）

ingest → extract（切镜/OCR+ASR 台词对账/说话人归属）→ assets（人脸聚类角色卡）→ understand（整集+逐镜两 pass）→ compose（剧本→小说→逐镜 shot prompt）→ gate_a（剧本确认，可选拦停）→ gate_b（prompt 确认，可选拦停）→ done。产物 = 每集 `script.md`/`dialogue.md`/`novel.md`/`shots/shotNN/shotNN.md`（含台词配音 prompt）/`all_shot_prompts.md`。

**产物分层（follow-up 005）**：整集级＝完整剧本 + 台词 + 小说（保持原片检测镜头结构，先生成）；分镜级＝prompt 单元（由整集层派生，强制 Seedance 4–15s——原片镜头 >15s 拆承接段、<4s 并入相邻单元、每单元标注对应原镜/时间码）。

**合规（SEC-12/13）**：上传强制勾选授权声明并留存 sha256 内容绑定存根；逆向他人作品的版权责任归客户。

## 已知实现边界（v1 骨架诚实清单）

这是一个**端到端可跑的降级态骨架**：管线全链贯通、契约/合规/prompt 自检为生产级、外部模型层为 NFR-O1 可插拔 seam（默认 Null，配 key 切真实后端）。以下能力**尚未落地**，均在代码/事件里显式标注、不静默：

- **算法 seam（配 key/装重后端即启用）**：切镜默认走 ffmpeg 场景滤镜（TransNetV2/AutoShot 未接）；**硬字幕 OCR 默认＝Claude CLI 读帧转写（零 key，follow-up 002）**，PaddleOCR 仍为可装的高精后端；ASR、人脸聚类为 Null 默认，缺失时**逐阶段降级并打标**（如 `asr_backend_unavailable`、`face_backend_unavailable`）。**人脸缺失不再卡死管线**：understand 阶段为 VLM 发现的角色自动建卡（`origin: vlm_discovered`）并写锁定描述符。
- **FR-1.3 切集**：当前 blackdetect + 时长先验两路；Chromaprint 片头指纹为预留 seam（`fuse_episode_boundaries(fingerprint_cuts=...)`），未接入时切点只到 medium 置信（无片头降级）。
- **operator 工作台 UI（人在环）未完整**：FR-1.4 集边界拖动校对、FR-3.3 角色卡命名/合簇/拆簇、FR-6.1 说话人标红复核高亮——当前 UI 只做总览/单集驱动/产物预览+编辑+版本化；这些交互面是首要补齐项。
- **成本计量（FR-10.2/10.3、NFR-P3）未实现**：事件日志记阶段与耗时，但 token/费用累计与告警链未落地。
- **FR-13 视频理解 PoC 待实测**：`make probe ARGS=all` 就绪，需 GEMINI/DASHSCOPE key + 真实素材，验证 Gemini/Qwen 连通性与逐镜描述质量基线。
- **NFR-D1 Docker Compose 未提供**：当前 `make run-*` + 多 worker 进程即可跑；容器化编排待补。
- **已删除（follow-up 001）**：Seedance 重生成侧（首帧生成/i2v/拼接/新片 vs 原片 QC/AI 定妆图）——不在本服务范围，用户拿分镜 prompt 自行生成。

## 快速开始（默认零 API key）

```
make install          # pip install -r requirements.txt + npm install
make run-prod         # 构建 UI 并以静态模式起服务 http://127.0.0.1:8620
make run-worker       # 起一个管线 worker（文件系统队列 + 原子锁 claim，可多开）
make run-backend      # 仅后端（配合 make run-frontend 走 Vite 代理开发模式）
make test             # 后端测试（模型层全打桩，无需 API key）
make e2e              # Playwright 浏览器 e2e（prod-static 与 dev-vite 双 profile）
make probe ARGS=all   # FR-13 视频理解探针（仅 keyed 后端需要；默认 Claude CLI 引擎无需）
```

**使用流程（follow-up 003 上传即建主体）**：浏览器打开 http://127.0.0.1:8620 → 左侧上传面板**选 MP4、勾授权声明、点「上传并新建主体」**（逐集或整剧长文件，≤2GB）→ 自动创建 entry（ID 取自文件名、标题可改）并出现在左侧导航 → worker 自动走 ingest→extract→assets→understand→compose→gates→done → 点击 entry 看集列表，进集页预览/编辑 `novel.md` / `script.md` / `dialogue.md` / 逐镜 `shotNN.md`。同一主体追加集数用主体页「追加上传（续集）」；需要预设闸口时用「高级新建」。

**默认引擎前提**：本机安装并登录了 Claude Code CLI（`claude` 在 PATH 上）。每次模型调用 spawn 一个 headless 新会话，默认模型 `sonnet`（`DRE_CLAUDE_MODEL` 可换，置空则用 CLI 默认模型）。

**队列/状态**：无 DB——每集 `pipeline_state.json` 即状态机，worker 扫描工作区用原子锁文件 claim；断点续跑天然成立（产物在=阶段完成）。

可选重型后端（不装则用轻量降级/桩，测试不受影响）：`scenedetect`（切镜）、`paddleocr`（硬字幕）、`funasr`（ASR 校验）、`insightface`（人脸/FaceSim）。

## 环境变量

| 变量 | 用途 |
|---|---|
| `DRE_WORKSPACE` | 工作区根（默认 `./workspace`，ASCII 路径） |
| `DRE_DB` | SQLite 路径（默认 `./workspace/dre.sqlite3`） |
| `DRE_API_TOKEN` | API 鉴权 token（不入日志） |
| `DRE_UNDERSTANDING` | 视频理解后端：`claude`（默认，零 key）/ `gemini_qwen` |
| `DRE_COMPOSER` | 文学合成后端：`claude`（默认，零 key）/ `doubao` |
| `DRE_SUBTITLES` | 硬字幕提取后端：`claude`（默认，读帧转写）/ `null`（关闭） |
| `DRE_CLAUDE_BIN` | Claude CLI 可执行名/路径（默认 `claude`） |
| `DRE_CLAUDE_MODEL` | Claude CLI 模型（默认 `sonnet`；置空＝CLI 默认模型） |
| `ARK_API_KEY` | 可选：`DRE_COMPOSER=doubao` 时的豆包 chat |
| `GEMINI_API_KEY` / `DASHSCOPE_API_KEY` | 可选：`DRE_UNDERSTANDING=gemini_qwen` 时的主/备选 |
