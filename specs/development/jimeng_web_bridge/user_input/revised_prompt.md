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

## 后续指令（follow-ups）

---

## 001 — 2026-09-20 09:30:00 — seedance2.5-cli-backend

> target_stage: 6
> target_artifacts:
>   - projects/jimeng_web_bridge/config/global.toml
> severity: low

### 指令

`model_limits.models."seedance2.5"` 的 `backends` 从 `["web"]` 改为 `["web", "cli"]`。

### 依据（实测，2026-09-20）

本机 `dreamina` CLI（build `46b5b0e-dirty`，2026-06-03）虽然 `--help` 只列 Seedance 2.0 系列、
`--duration` 标注 4–15s，但 **`model_version` 与 `duration` 是透传给服务端的，不做客户端校验**。
实测命令与结果：

```
dreamina text2video --prompt="..." --model_version=seedance2.5 \
                    --video_resolution=720p --duration=30
→ gen_status: success
→ duration 30.042s / 1280x720 / 24fps / mp4
→ commerce_info.triplets[0].benefit_type = "seedance_25_720p_no_input_video_output"
→ credit_count 600（= 20 credits/s，与 config 里 credits_per_second = 20 吻合）
→ 队列 dreamina_fusion_video45_pro / DreaminaFusion:Video45_base
```

即服务端确实按 Seedance 2.5 720p 受理并计费，CLI 后端可用。

### 附带发现

走 2.5 时 **`--video_resolution` 必须显式传**，否则服务端报
`api error: ret=10001, message=invalid param:video_resolution_type` 而失败（失败不扣费）。
原因是旧 build 按 2.0 的能力表推默认分辨率，推不出 2.5 的——报错信息与真实原因对不上。

### 验证边界

本次只验证了 **无参考图的 text2video**。CLI 侧 `multimodal2video` 能否在 2.5 下吃满
30 图 / 10 视频 / 10 音频，以及 1080p、`--ratio=9:16` 是否被接受，**均未验证**。

### 一句话总结

实测证明 dreamina CLI 可用 Seedance 2.5 直出 30s 视频，修正 `global.toml` 中
`seedance2.5.backends` 漏掉 `cli` 的错误（该错误会让 CLI 后端静默降级到 2.0 的 15s 上限而不报错）。
