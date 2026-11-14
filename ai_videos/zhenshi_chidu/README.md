# 真实尺度（zhenshi_chidu）· True Scale · 3D 真实尺度对比系列

## Vision（观众体验）

> **让你站在它们脚下：把世界上最大的东西按真实比例放进同一个画面，一眼看出谁比谁大多少，看到最后才见到冠军。**

核心：比例是机器核对过的真比例，每个尺寸都有出处；全流程素材与工具都可商用。

（Vision 由代理起草，**待用户确认**。）

| 体验 | 怎么做到 | 规范位置 |
|---|---|---|
| 站在它们脚下 | 每个对象旁站一个 1.75 m 人体参照，地面有刻度 | `bible.md` §1 D3 |
| 一眼看出大小 | 并排横移，从小到大登场，取景随对象长高 | `bible.md` §2.3 |
| 真比例、有出处 | 比例机检闸门（误差 ≤ 2%）；`sources.md` 逐条出处 | `bible.md` §3、§7 |
| 看到最后 | 冠军最后登场；前 5 名放慢；大合影收尾 | `bible.md` §2.2 |
| 可商用 | 许可白名单 + `licenses.csv` 登记 + 渲染前闸门；不出风险版 | `bible.md` §0 |

## 这是什么，不是什么

- 是 MetaBallStudios 一类 3D 尺度对比视频的**数据可信、全自动、全可商用版**。
- **不是短剧**：不走 three-module-v1 六模块，没有 `workflow.json`，不用 Seedance。
- 与排行榜（`ai_videos/paihangbang/`）是兄弟系列：复用其数据规范、字体、国旗、配乐与发布流程；本目录规则只在本系列生效（剧级）。

## 文件

| 文件 | 内容 |
|---|---|
| [bible.md](bible.md) | 制作圣经：商用规则、定位、格式、镜头、数据、3D 素材、流程、闸门、技术路线 |
| [topics.md](topics.md) | 第一季选题候选与 `topic.md` 模板 |
| [0_research/genre.md](0_research/genre.md) | 赛道、同类频道、样例链接、风险 |
| [0_research/toolchain_licenses.md](0_research/toolchain_licenses.md) | 每个工具与素材来源的商用许可核对（含原文证据链接）与本机现状 |
| `0_research/model_sources.md` | 第一期 30 种动物 + 人体参照的可商用模型候选（调研中） |
| `0_research/ep01_animal_dimensions.*` | 第一期 30 种动物的肩高、体长及出处、分歧取舍与用户决定 |
| `episodes/epNN_<slug>/` | 每期产物（结构见 `bible.md` §6） |
| `_tools/` | 剧级原型工具：`make_ep01_data.py`（排名与数据）→ `calibrate_ai.py`（AI 模型标定）→ `build_ep.py`（Blender 场景、相机、timeline）→ `render_ep.py`（分段渲染）→ `cards.py`（中文版叠加 `cards_zh.py`，再 `compose.py --cards _build/cards_zh`）/ `music.py` / `compose.py`（叠加、配乐、合成）→ `thumbnail.py`（各平台封面：先 `render_ep.py --still` 渲高清静帧）→ `make_preview.py`（审片页数据 preview.json 与逐段缩略图，打开 `/episode-preview?path=ai_videos/zhenshi_chidu/episodes/<集目录>`）；`cutouts.py`（2.5D：抠像与肩线标定）→ `build_cutout.py`（2.5D 场景，替代 `build_ep.py` 与 `calibrate_ai.py`）+ `scene_env.py`（精细环境：远景板、中景树、3D 草）；`gate.py` 渲染前闸门；`upload.py` 英文版经 YouTube API 传私享与发出处评论；`make_ep01_meta.py` 出 licenses.csv、sources.md、置顶评论；`scene_lineup.py` 公共函数（其 `build_lineup` 是早期试排原型，正片用 `build_ep.py`） |

需求记录：`specs/ai_video/zhenshi_chidu/user_input/`。收费服务（Suno、Codex 出图）的请求日志归属本目录 `request_log.md`，经 `tools/service_request.py` 写入（首次调用时创建）。

## 状态（2026-11-07）

- ✅ 立项：系列名、全流程可商用、不用 Hyper3D、用 Blender MCP（用户定）。
- ✅ 本机环境：Blender 5.2.3 LTS + MCP 插件已对齐协议，遥测关闭，AI 生成器全关。
- ✅ Foundation v0：`bible.md`、`topics.md`、工具链许可核对。
- 🟡 ep01 最大陆地动物（按肩高排名）：**成片已出、待用户审核**（follow-up 003）。成片 `render/ep_master.mp4`（4:08），封面候选 `render/thumb_A.jpg` / `thumb_B.jpg`，交审说明 `review_for_user.md`；独立审片 3 轮，第 3 轮「可交用户审核」、无阻塞项。
  - 模型：30/30 AI MODEL（Codex 正侧面参考图 + 本地 TripoSR），标定与检查在 `episodes/ep01_largest_land_animals/assets/models_ai/models_ai.json`；长颈鹿用 v3（颈部前倾）、北极熊用 v3（头放平）。
  - 开放库 16 只改走 AI 流程（自动下载需 Sketchfab / Poly Pizza API key；代理决定，见 `topic.md`）。
  - 闸门：`_tools/gate.py` 通过（licenses.csv 31 行全在白名单；scale_check 30/30 误差 ≤ 0.5%；参照人 1.75 m）。
  - 产物：`data.json`、`sources.md`、`licenses.csv`、`scene/ep.blend`、`render/ep_master.mp4`、`publish.md`、`qc.md`（独立审片）、`review_for_user.md`。
- ⬜ 下一步：用户审核 → 按意见改 → 上传（用户亲手）。

## 已定（用户 2026-11-05 至 11-06，立项对话）

| # | 决定 | 结论 |
|---|---|---|
| 1 | 系列 | 开 3D 真实尺度对比系列「真实尺度 · True Scale」 |
| 2 | 3D 生成 | 不用 Hyper3D |
| 3 | 商用 | 全流程可商用；许可不明不用；不出风险版 |
| 4 | Blender MCP | 用（MIT；遥测关；其 AI 生成功能不用） |
| 5 | 开工默认 | 镜头先用并排横移；先作为排行榜频道子系列（播放列表区分）；ep01 用排行榜 ep04 的动物 |
| 6 | ep01 排序（2026-11-06，follow-up 001） | 按肩高排名（物种仍是 ep04 体重前 30）；冠军长颈鹿 3.31 m |
| 7 | 人体参照（follow-up 001） | 1.75 m，画面标「1.75 m man」 |
| 8 | 尺寸分歧取值（follow-up 001） | 用户授权代理定；河马体长改 3.5 m est.，其余维持，见 `0_research/ep01_animal_dimensions.md` 文末 |
| 9 | 缺口物种（2026-11-06，follow-up 002） | 开放库没有合格模型的物种用 AI 生成兜底：Codex 参考图 + 本地 TripoSR（MIT），卡上标 AI MODEL；不用近缘替代 |
| 10 | 做到成片（2026-11-07，follow-up 003） | 用户：「继续做，直到成片完成，给我审核」；代理决定 ep01 30 只全走 AI 流程 |
| 12 | 精细环境（2026-11-08，follow-up 005） | 用户：「后面的场景太粗糙了应该做一个精细的场景，可以用图片或者blender来做」；代理做远景板 + 中景树（Codex 图）+ 3D 草（Poly Haven CC0）四层环境 |
| 11 | 画面改 2.5D（2026-11-07，follow-up 004） | 用户看第 1 版：「每个动物感觉都不是3d，是不是还不如我自己codex生成一张图片来的好，还有背景也没有」；看过 A（3D + HDRI）/ B（抠像 + HDRI）样张后定「用B吧」。主体与参照人改为 AI 写实图抠像，按肩线像素缩放，真实草原环境（Poly Haven CC0）；标题去掉「3D」 |

## 待用户决定

| # | 事项 | 代理默认（可改） |
|---|---|---|
| 1 | Vision 措辞 | 见文首 |
| 2 | 材质路线：写实贴图 vs 统一中性材质 | 试制两版对比后再定 |
| 3 | 技术路线：剧级原型跑通后按 `agent_team` 立项 `projects/scale_3d/` | 是 |
| 4 | 是否设 `DISABLE_TELEMETRY=true`（停发 MCP 匿名使用记录；用户级配置） | 建议设，未改 |
| 5 | 第一季选题顺序 | 见 `topics.md` |
