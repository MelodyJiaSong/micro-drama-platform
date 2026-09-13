# Interview — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603

Shape A (parent-direct, no category workers).

## Categories probed
- 接口与集成 — 谁来调用、以什么形态、与 `shotNN.md` 流水线集成到多深
- 功能范围 — MVP 覆盖的生成模式、批量模型、花积分前的确认
- 浏览器与会话 — 登录态怎么持有、页面怎么驱动
- 异常与运行 — 验证码 / 审核 / 积分不足时的处理、通知、运行位置
- 记录与命名 — 生成记录落点、即梦人物主体命名

## Round 1

### 接口与集成
**Q:** 这个 service 对外主要以什么形态提供？
- A: HTTP API + MCP — 常驻本地进程持有浏览器；HTTP API 给脚本 / automation / 人用，MCP server 薄包一层给 Claude 直接调用，两者共用同一套 Command/Query。

**Q:** 和 AI 短剧流水线（shotNN.md）集成到什么程度？
- A: 通用接口 + shot 适配层 — 核心接口只收 prompt / 参考文件 / 参数；另加一层读 `shotNN.md`：把 `参考:` 行每个 `=>@` 解析成盘上文件、按顺序上传并对上 @，读 `比例:` / `时长:`，结果直接落到该 shot 目录。

**Q:** 给 Claude / 脚本暴露的操作粒度？
- A: 一步到位 + 分步可选 — 主操作 `generate(prompt, refs, params)` / `generate_shot(shot_path)` 一步走完；同时暴露 上传 / 填写 / 截图预览 / 提交 / 查状态 / 下载 分步操作，便于排错和人工介入。

### 功能范围
**Q:** MVP 要覆盖即梦网页上的哪些生成模式？（多选）
- A: 视频·全能参考；图片生成（Seedream）；人物主体（entity）管理。
- 未选：视频·首尾帧（承接镜的「本镜首帧(上一镜末帧)」在 shot `参考:` 行里本就是全能参考的一个上传项）。

**Q:** 批量与任务模型？
- A: 任务队列 + 并发上限 — 可一次提交整集 N 镜；service 排队、按账号允许的并发数提交，可暂停 / 取消；服务重启后能恢复未完成任务。

**Q:** 真正点「生成」（花积分）之前要不要确认？
- A: 默认先预演，确认后提交 — 先把参考、prompt、参数全部填好并截图返回（不点生成），调用方确认后才提交；automation 可显式 `auto_confirm` 跳过。

### 浏览器与会话
**Q:** 浏览器和登录态怎么持有？
- A: 专用 profile，首次手动登录 — service 启动独立的有界面 Chrome（专用用户目录），用户在里面扫码登录一次，之后一直复用；和日常 Chrome 互不干扰。

**Q:** 页面驱动方式？
- A: UI 操作 + 读页面网络响应 — 上传 / 填写 / 点击都走真实 UI；任务状态和结果视频地址从页面自己发出的请求的响应里读取（只读，不伪造请求）。

### 异常与运行
**Q:** 遇到验证码 / 风控弹窗、审核不通过、积分不足时怎么办？
- A: 暂停并通知，人工处理 — 截图 + 原因返回调用方，队列暂停；用户在浏览器窗口里手动处理后恢复。验证码始终由人来过。

**Q:** service 跑在哪台机器上？
- A: 本机 Windows 常驻进程 — 与仓库同机，只监听 localhost；需要电脑开着、浏览器窗口开着。

## Round 2

### 功能范围
**Q:** 人物主体（entity）管理做到哪一步？
- Other: 「{剧名字的字幕缩写}_{人物名字}，比如 hy3_主角」 — 用户给出的是即梦侧主体的**命名规则**，范围未选 → 转 Round 3 澄清。

**Q:** 图片生成（Seedream）怎么接入？
- A: 资产卡适配层 — 与 shot 适配层对称：读 characters / props / scenes 卡里以路由键开头的 prompt 块（`c1-1` / `p3-2` / `bg11-1`），出图后按路由键直接落进该主体目录，不再经 Downloads 中转。

**Q:** 队列里一批多条时，预演确认按什么粒度？
- A: 整批预检一次确认 — 先对每条做静态校验（参考文件都在盘上、prompt ≤ 5000 字、时长 ≤ 30 s、主体存在）并列出预计积分，整批确认一次后逐条提交；每条提交前的填表截图存档备查。

**Q:** 模型档位 / 分辨率等生成参数的默认值？
- A: 质量优先，可逐次覆盖 — 配置文件默认最高质量模型 + 最高分辨率；比例 / 时长从 shot md 读；任何一次调用都可覆盖。

### 记录与命名
**Q:** 每次生成的记录（prompt、参数、即梦任务 id、积分、耗时）存在哪？
- A: 服务本地库 + 产物旁 sidecar — 队列 / 任务状态存在 service 自己的本地数据目录（gitignored）；每个成功产物旁再写一个小 json（进 git），以后能查「这条渲染是哪版 prompt 出的」。

### 异常与运行
**Q:** 队列暂停（验证码 / 审核不过 / 积分不足）时怎么通知？
- A: 接口状态 + Windows 桌面通知 — 任务状态里带暂停原因和截图；同时弹 Windows 通知。

## Round 3

### 记录与命名（人物主体）
**Q:** 人物主体按 `{剧缩写}_{人物名}` 命名。service 对主体做到哪一步？
- A: 创建 + 选用 — service 用角色卡的立绘 + turntable 在即梦里按该命名创建主体；同名已存在就直接复用、不重复建；生成时按同名 @ 选中。

**Q:** 命名里的「人物名」取什么？
- A: 角色卡目录的中文名 — `c1_砌炉的老人` → `hy3_砌炉的老人`；与 shot `参考:` 行里写的主体名一致，适配层直接机检映射，不加额外字段。

**Q:** 命名里的「剧缩写」取什么？
- A: 集目录名，独立剧在 README 配缩写 — 系列剧直接用 `hy3`；独立剧在其 README 里声明一个短缩写，没声明就预检报错。跨集复用的人物（`.link.json`）沿用来源集的名字（hy2 复用 hy1 的人 → `hy1_…`）。

## 未提问、由仓库现状直接定下的点
- **视频产物落点**：`shots/shotNN/renders/`。这是现有约定——webapp「🎯 定版」取该目录下最新的 mp4 复制为 `shotNN.mp4`（`projects/ai_video_management/README.md`），service 写进同一目录即可接上后续 定版 → 拼接 → 字幕 流程。
- **图片产物命名**：按路由键落盘（`c1-1.png` / `p3-2.png` / `bg11-1.png`），与 `libs/common/asset_key.py` 的「文件名即路由键」契约一致。

## Post-research decisions（stage 4 前置，research 暴露的开放问题）

### 后端策略
**Q:** 本机已装好并登录官方 CLI（dreamina 1.4.5，官方渠道、扣账号积分；覆盖 Seedream 出图 + Seedance 2.0 全能参考 ≤9 图 / ≤15 s，不支持 2.5 / 16–30 s / @主体）。生成后端怎么定？
- A: 网页为主 + 官方 CLI 补位 — 视频（2.5 / >15 s / @主体 / 多参考）走网页自动化；Seedream 出图走官方 CLI。两者共用队列 / 预检 / 确认 / 落盘；CLI 以后支持 2.5 时，视频也可以切过去。

### 默认视频档位
**Q:** 「质量优先 + 最高分辨率」对 16–30 s 的镜自相矛盾（2.0 最长 15 s 可 1080P；2.5 最长 30 s、资料称最高 720P）。默认取什么？
- A: 默认 Seedance 2.5 · 720P — 与现有实拍一致；时长从 shot md 读、≤ 30 s；任何一次可覆盖。

### 主体命名冲突（及一切需确认的规则）
**Q:** 已有主体 `hy3_主角` 与规则「角色卡目录名 → `hy3_砌炉的老人`」对不上，怎么处理？
- Other: 「所有的 key、规则，你可以建一个 UI 可以看和 manage 的 config file，你可以按照默认值 propose，但我可以在 UI 上修改，每部剧都以自己的独立的 config。所有规则上你需要我 confirm 的都应该覆盖在 config 里。」
- 抽象：**每部剧一份独立 config**，装下所有路由键 / 命名 / 映射 / 默认值 / 校验阈值等规则。service 先按默认值提议，用户在 UI 上查看和修改。凡是需要用户确认的规则一律落进 config，不在代码里写死。主体名的冲突也由 config 里的映射项解决。

### 并发
**Q:** 同时在即梦渲染的条数默认是多少？（UI 动作始终串行）
- A: 默认 3，可配置 — 与手动出片时一致；页面提示并行已达上限时当作背压、等待后再提交，不报错。

### config 的 UI 与落点（由上一条 Other 引出的澄清）
**Q:** 管理每部剧 config 的 UI 放在哪？
- A: service 自带的本地网页 — jimeng_web_bridge 自己出一个轻量 React 页，由同一个 localhost 进程提供，独立于 ai_video_management。

**Q:** 每部剧的 config 文件存在哪？
- A: 放在剧目录里，进 git — 例如 `ai_videos/huangye_shenghuo/hy3/jimeng_config.toml`。账号级设置（并发、每日预算、profile 路径等）另放一份全局 config，同样可以在 UI 里改。

**Q:** 这个 UI 除了管 config 还要做哪些？（多选）
- A: 批次确认 — 看每批的预检结果、预计积分、填表截图，点确认才花积分；Claude 提交的批次也在这里由用户确认。
- A: 任务队列看板 — 看排队 / 生成中 / 暂停（原因 + 截图）/ 完成，可暂停、恢复、取消。
- A: 生成历史与积分 — 按剧 / 按镜查历史，看预估与实扣积分、每日消耗。
- A: 主体列表对账 — 列出即梦里的主体与各剧角色卡的映射，标出未建 / 未映射。

## Stage-5 decisions（validation 暴露的关键冲突，stage-5 sign-off 前由用户裁决）

### 确认权
**Q:** 谁能「确认批次」（确认即开始花积分）？安全审查发现两个问题：靠 Claude Code 的权限弹窗拦 MCP `confirm_batch`，一旦工具进了 allow 列表或开了 bypass-permissions 就等于没拦；持 token 的脚本也能自己调 confirm。
- A: 只有 UI 里的人能确认 — Claude 和脚本只能做预检、拿到确认页链接；确认按钮只在本地网页上；服务端按请求来源判定 confirmer，持 token 的客户端一律不能确认。（这一条取代了 spec 原来的 MCP `confirm_batch` 和 HTTP `auto_confirm`。）

### 旧写法
**Q:** 老剧的旧 `参考:` 写法 v1 要不要支持？（wushen_juexing 是 `名字=>` 无 @ 无括号；rexue_gaoxiao 是 `=>@1` 带槽位号；xianjian_yi_mv 有无括号项。）
- A: v1 只支持现行写法 — 只认 `` `{名}({类型})=>@` ``；旧写法在预检时报错并说明原因。老剧需要重拍哪一镜，就先把那一镜的 `参考:` 行改成现行写法（CLAUDE.md「规则变更只对改动的产物生效」）。

### turntable
**Q:** 角色卡里的 turntable 是视频 prompt（如 `c1-2_…turntable`），资产卡适配层怎么处理？
- A: 视频块走网页视频，立绘做参考 — 按 config 识别视频块，用同一张卡的立绘 `c{N}-1` 作参考走网页 Seedance，结果落进该卡的 `_candidates/`。

## Team consensus
All categories marked clear after 3 round(s); research-surfaced open questions resolved in the post-research decisions above; stage-5 conflicts resolved in the stage-5 decisions above.
