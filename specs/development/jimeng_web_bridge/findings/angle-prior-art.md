---
worker_id: researcher-01-prior-art
stage: 3
role: researcher
angle: prior-art
status: complete
blockers: []
confidence: medium
---

# Angle: prior-art — 即梦 / Dreamina 及同类网页生成器的自动化先例

## 1. What this angle covers

盘点社区已有做法的三条路线及其耐久性与账号风险：
- **A. 重放内部 API**：拿 sessionid cookie 直接调用网页的内部接口。
- **B. MCP 包装**：这一类几乎都是 A 或 D 的薄壳。
- **C. 网页 UI 自动化**：Playwright、浏览器扩展、油猴脚本。

检索中还发现第四条路线，而且与本任务的前提直接相关：
- **D. 即梦官方 CLI**。

另外对照了 Kling / Hailuo 的同类工具，并整理了可复用代码的 license。所有信息只来自公开网页（2026-09-13 检索），没有登录或请求即梦站点。

## 2. Key findings

### A. 重放内部 API（sessionid cookie）——反复失效、归档、被风控

| 项目 | 方式 / 能力 | 状态 | License |
|---|---|---|---|
| LLM-Red-Team/jimeng-free-api | sessionid 当 Bearer token，兼容 OpenAI 接口，以图片为主 | 2025-11-27 归档；2026-09-13 仓库页返回 404，组织主页只剩 4 个无关仓库 | —（无法取得） |
| iptag/jimeng-api（1k star） | sessionid；支持视频、Seedance 2.0 Omni Reference、国际站 | **2026-07-17 归档**。issue #166「Couldn't generate due to unusual activity in your account」，#162 omni_reference 上传报 CheckAuthenticationError，#163 sessionId 不存在 | GPL-3.0 |
| hedashuaiii/jimeng-api | sessionid；Seedance 2.0 多图，用 @1/@2 占位 | README 记载：视频生成接口加了 a_bogus 校验，直接请求返回 `ret=1019 shark not pass`。项目随后改为在后台开无头浏览器生成签名（v0.8.4），国际站改走纯算法签名（v0.8.9，2026-04-01）。也就是说，它靠逆向签名活下来 | MIT |
| zhizinan1997/jimeng-free-api-all | sessionid；Seedance 2.0、最多 10 张参考图、首尾帧 | 仍在更新（v1.2.6，2026-09-02）。自称「不保证永久可用」 | GPL-3.0 |
| deluxebear/jimeng-cli | 抓取已登录浏览器的流量，本地 msToken/a_bogus 签名 | README：「页面或接口变更后可能需要重新捕获」「不要盲目重试」 | 未声明 |

来源：
- [iptag/jimeng-api](https://github.com/iptag/jimeng-api)、[iptag issues](https://github.com/iptag/jimeng-api/issues)
- [hedashuaiii/jimeng-api](https://github.com/hedashuaiii/jimeng-api)
- [zhizinan1997/jimeng-free-api-all](https://github.com/zhizinan1997/jimeng-free-api-all)
- [deluxebear/jimeng-cli](https://github.com/deluxebear/jimeng-cli)
- [LLM-Red-Team org](https://github.com/LLM-Red-Team)。该组织自述「收到相关方联系即下架」，见 [free-api about](https://llm-red-team.github.io/free-api/about/index)。

结论：
- 这条线的典型寿命是「上游改一次签名或风控 → 一波 fork 修复 → 归档或删库」。
- 视频生成接口正是字节加签名闸门的地方。
- 能长期存活的 fork 都靠逆向签名或伪装浏览器。这类手段本项目明确不做，所以没有继承价值。
- 另有 doubao-2api 一类项目依赖 stealth 与指纹伪装（[lza6/doubao-2api](https://github.com/lza6/doubao-2api)），此处只记录这一点。

条款风险有明文依据。[即梦AI用户服务协议](https://lf9-cdn-tos.draftstatic.com/obj/ies-hotsoon-draft/vco/17620dba-f821-4a18-85f9-b8b11f73304a.html)：
- 5.1 禁止「使用任何自动化程序、软件或类似工具接入即梦AI」。
- 5.3 禁止「爬虫抓取、模拟下载」。
- 5.2 禁止反向工程。
- 7.1 处罚可到「永久关闭账号、禁止重新注册」。
- Dreamina 国际站社区准则也写明「Do not use automated scripts to collect information」（[guidelines](https://dreamina.capcut.com/clause/dreamina-community-guidelines)）。

**需要注意：条款对 UI 自动化（路线 C）同样适用。** 路线 C 的风险低于 A，但不是零。

### B. MCP 服务器——大多是 A 的壳；接口形态已形成共识

- **走 cookie 重放**：
  - [wwwzhouhui/jimeng-mcp-server](https://github.com/wwwzhouhui/jimeng-mcp-server)（MIT）：后端依赖 jimeng-free-api-all，4 个工具，异步轮询。README 自己写了「逆向接口可能随官方更新失效」。
  - [c-rick/jimeng-mcp](https://github.com/c-rick/jimeng-mcp/)（MIT）：generateImage / generateVideo，支持首尾帧。
  - [LupinLin1/jimeng-web-mcp](https://github.com/LupinLin1/jimeng-web-mcp)（MIT）：10 个工具，其中 `query` / `query_batch` 用于轮询，视频工具默认异步。
- **走第三方或官方 API**：[Ceeon/jimeng-mcp-apicore](https://github.com/Ceeon/jimeng-mcp-apicore)，经 APICore 调 doubao-seedream-4.0。
- **驱动网页 UI，与本项目最接近**：[DanikVR/dreamina-seedance-mcp](https://github.com/DanikVR/dreamina-seedance-mcp)（MIT，见 [Glama](https://glama.ai/mcp/servers/DanikVR/dreamina-seedance-mcp)）。
  - 架构：MCP 只做「pure transport」，经本地 HTTP bridge（127.0.0.1:8788）交给付费的 SeedFlow Chrome 扩展，在 Dreamina 标签页里真实点按。
  - 工具只有 5 个：`dream_status`（预检加队列）、`dream_generate`（立即返回 jobId）、`dream_edit`、`dream_wait`（每 5 秒轮询，默认超时 600s）、`dream_cancel`（只能取消未开始的任务）。
  - 参考图最多 7 张，并分配角色；支持首尾帧。
  - 自我约束：「no captcha bypass, no private API, no multi-accounting, no watermark removal」。

### C. 网页 UI 自动化：扩展与脚本——商业扩展活得最久，但只做「批量填 prompt」

- **[Seedance Automation](https://chromewebstore.google.com/detail/seedance-automation-auto/cniciedfdaehibebgdeeiobndignobnb)**
  - 同时支持即梦和 Dreamina，7,000 用户，4.9 分（88 条评分），v1.2.4，2026-08-08 更新。
  - 并发最多 6 个，**自动重试最多 20 次**。
- **autojourney.ai 系列**：[AutoDreamina](https://chrome-stats.com/d/kpfhaohjonmabolhmdaoacnkmdonblfc) 宣称「无水印自动下载」；[AutoHailuo](https://chromewebstore.google.com/detail/autohailuo-auto-send-hail/akhjgnghknikbpimcmambmpklhegbjeo?hl=en) 为 v0.0.12，147 用户。同一开发者还做 Veo / Flow 等同类扩展，走的是「一个平台一个扩展」的持续维护商业模式。
- **Kling / Hailuo 侧**：
  - 同样是扩展形态：Hailuobot、KlingGen、AutoFlow，见 [搜索结果](https://chromewebstore.google.com/detail/hailuobot-hailuoai-minima/bcoafbkjfnenfmbkfdocdpmligdndgbi)。
  - cookie 逆向形态：[yihong0618/klingCreator](https://github.com/yihong0618/klingCreator)（GPL-3.0，219 star）。
- **[leigegehaha/jimeng-cli-free](https://github.com/leigegehaha/jimeng-cli-free)**（Apache-2.0）
  - 结构：CLI 加一个本地 unpacked 扩展做桥接，复用浏览器里已登录的即梦。
  - 参考图可来自本地路径、URL 或剪贴板；每次自动下载 4 张图。
  - **只做图片**，视频「大概率单独做成新插件」。只在 macOS 验证过，作者自述代码未经完整人工审核。
- **油猴脚本**（[CSDN 2026-07-27](https://blog.csdn.net/easylife206/article/details/148351088)）：
  - 无水印下载靠「拦截并替换前端数据流中的图片URL」。
  - 另有「自动抽卡」脚本。文中完全没有讨论风险。
- **空白**：没有找到任何公开项目记录如何用 RPA 驱动即梦的 **@ 提及编辑器**、**人物主体创建与选择**，或 **全能参考的逐项绑定**。这部分 DOM 映射是本项目必须自己承担的维护成本；仓库里 `tools/kling_autopilot/` 的 selector 至今还是占位，也印证了这一点。

### D. 即梦官方 CLI——一条能用网页积分、又不依赖 DOM 的官方通道

- **发布**：约 2026-03-31 至 04-02 发布，一行 curl 安装，登录时自动拉起浏览器或扫码。
- **命令**：
  - 图片：`text2image` / `image2image` / `image_upscale`
  - 视频：`text2video` / `image2video` / `frames2video` / `multiframe2video` / `multimodal2video`（Seedance 2.0 旗舰多模态）
  - 账户与任务：`user_credit` / `list_task` / `query_result`（异步，可加 `--poll`）
  - 来源：[53AI](https://www.53ai.com/news/MultimodalLargeModel/2026040187324.html)、[simonjiang99/dreamina-cli](https://github.com/simonjiang99/dreamina-cli)、[chooseai](https://www.chooseai.net/news/3138/)
- **积分**：扣的是**账户的即梦积分**。53AI 原文：「CLI 出了之后，Agent 可以直接调用这些积分批量生成视频」，截图为「VIP · 剩余积分 10903」。3/31 到 5/1 是限时体验，之后需要会员（[apiyi](https://help.apiyi.com/en/jimeng-ai-cli-agent-image-video-generation-terminal-guide-en.html)）。
- **平台**：官方只支持 macOS / Linux，Windows 需 WSL 或 .bat 方案。
- **基于 CLI 的衍生项目**：
  - [xiaozhichao2025/JimengCli_api](https://github.com/xiaozhichao2025/JimengCli_api)（MIT）：v2.0.0（2026-04-24）要求 CLI ≥ v1.4.2，用账号池消耗会员积分。
  - [seannnnnnnnnnnnnn/jimeng-ai-video-cli-workflow](https://github.com/seannnnnnnnnnnnnn/jimeng-ai-video-cli-workflow)（MIT）：自带 Windows .exe、多账号积分路由、@素材 语法，已支持 Seedance 2.5。说明 5 月之后 CLI 仍在被使用（这是推断）。

## 3. Implications for the spec

1. **不采用路线 A（伪造或重放请求）。**
   - 视频接口有签名闸门（1019 shark），想活下去就得逆向签名，这超出本项目的边界。
   - 主力 fork 在 12 个月内相继归档或删库。
   - 已有「unusual activity」账号级风控报告。
   - 被动读取页面自己的网络响应（interview 已定）不属于伪造请求，可以保留。
2. **stage 4 应引入 `GenerationBackend` 端口**，至少两个 adapter：`WebUiBackend`（本需求的 Playwright headful 方案）和 `DreaminaCliBackend`（官方 CLI）。队列、预检确认、shot/资产卡 adapter、sidecar 全放在 application 层共用。
   - *（意见）* 在写 DOM selector 之前，先做一个 **CLI 覆盖度 spike**：多参考 + @ 绑定、人物主体、Windows 可用性、单次积分是否与网页相同。
   - 能用 CLI 的模式走 CLI，只有 CLI 缺失的能力（例如主体创建和选择，如果确实缺）才走 UI。
   - 这会改变用户原先「只能靠网页」的前提，**需要回到用户确认**。
3. **MCP / HTTP 工具面沿用 DanikVR 与 LupinLin1 的共识**：
   - `status/preflight` → `submit` 立即返回 `job_id` → `wait` / `query` → `cancel`（只能取消尚未花积分的阶段）。
   - MCP 只做传输层，所有逻辑在 application 层。这与 interview 定下的「HTTP + MCP 共用 application 层」一致。
4. **反面教材是「高并发 + 自动重试」**（Seedance Automation 并发 6、重试 20 次）。spec 应规定：
   - 默认并发 1；
   - 提交这一步**零自动重试**，只有不花积分的步骤（上传、填表、下载）可以重试；
   - 遇到风控、登录、积分类错误立即暂停队列（jimeng-cli：「不要盲目重试」）。
5. **不做去水印**（DanikVR 明确拒绝；油猴脚本靠拦截替换 URL）。只取页面按会员权益给出的下载按钮或结果 URL。
6. **selector 与流程步骤集中在一个 page-map 模块里，并做版本标注**；每一步失败都截图并记下是哪一步。@ 提及和主体选择没有任何公开先例，工作量和维护量都应按「自研」估算。
7. **License**：GPL-3.0 的项目（iptag、zhizinan1997、klingCreator）不拷代码；MIT / Apache-2.0 的项目（DanikVR MCP、LupinLin1、JimengCli_api、jimeng-cli-free）可以参考结构并注明出处；官方 CLI 当作外部二进制调用，不随仓库分发。

## 4. Open questions surfaced

- 2026-05-01 之后，官方 CLI 对会员账号是否仍然可用？每次生成扣的积分是否与网页一致？（公开来源只说「之后需会员 / 可能要付更多」，没有找到 9 月的一手信息。）
- CLI 的 `multimodal2video` 能不能完整表达 Seedance 2.0 全能参考（参考项上限、按 @ 绑定到具体素材）？支不支持人物主体的创建和选择？Windows 原生能不能用？
- 会员档位的网页下载本身是否无水印？这决定下载是否需要任何特殊处理。
- 没有找到「即梦账号因 UI 自动化被封」的公开一手报告。这只是没有证据，不能当作安全的证明。LLM-Red-Team 删库的具体原因也没有找到公开说明。
- 部分事实来自 WebFetch 的摘要，个别页面返回 403/404，所以置信度记为 medium。关键结论（归档状态、1019 签名闸门、条款原文、CLI 扣积分）至少有两个来源，或有原文引述。
