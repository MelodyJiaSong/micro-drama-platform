# Revised prompt — jimeng_web_bridge

## 目标

构建一个**独立 service**，通过驱动浏览器模拟用户在即梦网页版（`https://jimeng.jianying.com/ai-tool/generate?type=video`）上的手动操作，把「上传参考素材 → 填入 prompt → 设参数 → 提交生成 → 等待完成 → 取回结果」这条完整链路封装成一个可编程 interface，供**人、AI（Claude）和 automation** 三类调用方使用。

## 背景与动机

- 即梦网页版（会员 / 积分）的价格远低于官方 API，用户不打算购买 API，希望复用网页版的额度。
- 用户能自己在网页上手动登录；service 复用该登录态，不代替人完成登录。
- 本仓库的 AI 短剧流水线已产出标准化 shot prompt（`ai_videos/**/shotNN.md` 的 `## 视频 prompt` 块）。其 `参考:` 行用裸 `=>@` 占位列出本镜要上传的参考项（场景图 `bg{N}-{M}`、Seedance 人物 entity、道具锚点 `p{N}-{M}`、上一镜末帧等），另有 `比例:` / `时长:` 字段。当前这些都靠手工：逐个上传、手工对上 `@`、复制 prompt、设参数、下载，再用 `projects/ai_video_management` 的 DownloadsImporter 按 prompt 首行路由键把文件归位。
- 仓库已有同类先例 `tools/kling_autopilot/`：Playwright 持久化登录目录 + 填 prompt + `@` 下拉选元素 + 设画幅时长 + 生成 + 下载。其 selector 仍是占位，未真正跑通。

## 期望结果

1. 一个可程序化调用的 interface（形态待定：HTTP API / MCP / CLI 或组合），Claude 在对话里就能直接完成一镜的端到端生成。
2. 覆盖完整链路：上传 reference、填 prompt、生成视频、取回结果文件。
3. 同一 interface 人和 automation 也能用。

## 从请求与仓库上下文浮现的约束（不是新增需求）

- **依赖网页 DOM**：页面改版会让自动化失效，失败必须可诊断，页面交互细节需要集中、可维护。
- **服务条款与账号风险**：自动操作网页版可能不符合即梦用户协议，存在风控 / 封号风险。前提是用户自有账号、个人自用；service 不做绕过验证码或风控检测的对抗手段。
- **每次提交都花积分**：误提交、重复提交、失败重试都有真实成本。
- **平台上限**（CLAUDE.md，2026-09-06）：单条 prompt ≤ 5000 字，单段视频 ≤ 30 s。
- **项目布局**：落在 `projects/{name}/`，遵循 `.claude/agent_refs/project/development.md` 的 apps/+libs/ DDD+CQRS 规则。

## 留给 stage 2 澄清

interface 形态；MVP 覆盖哪些生成模式；与 `shotNN.md` / DownloadsImporter 集成到什么程度；浏览器与登录态策略；提交前确认与节奏控制；在哪台机器上运行。
