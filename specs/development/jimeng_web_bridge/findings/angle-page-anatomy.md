---
worker_id: researcher-00-page-anatomy
stage: 3
role: researcher
angle: page-anatomy
status: complete
blockers: []
confidence: high
---

# Angle: page-anatomy — 即梦网页实际长什么样（parent-direct 实地勘察）

## 1. What this angle covers

**由 parent 直接执行，没有派 worker。** 原因有二：
- Claude in Chrome 工具与用户的登录态只在 parent 会话里可用；
- 并行 worker 共用同一个浏览器会互相踩。

勘察时间与对象：
- 2026-09-13 约 17:50–18:10（北京时间）。
- 用户已登录的即梦网页，`web_version=7.5.0`。
- 页面：`https://jimeng.jianying.com/ai-tool/generate?workspace=21635005479692&type=video` 与 `/ai-tool/elements`。
- 另在本机检查了官方 `dreamina` CLI 的安装与 help 输出。

**全程只读，做过的操作：**
- 打开下拉菜单后按 Escape 关闭；
- 读 DOM 结构；
- 读网络请求的 URL（未读 body）；
- 打开已有主体的「设置主体」弹窗，未保存直接关闭；
- CLI 只跑 `--help` / `version` / `user_credit`。

**明确没做：** 点「生成」、上传文件、新建或修改主体、调用任何花积分的 CLI 命令。勘察时用户正在另一处生成 shot09，未受影响。

事实来源一律是「现场观察」。标【推断】的是由观察推出、尚未证实的结论。

## 2. Key findings

### A. 视频生成输入区（composer）

- **创作类型下拉**：Agent 模式 / 图片生成 / 视频生成 / 音乐生成 / 音频生成 / 数字人 / 动作模仿。页面刚加载时会先渲染一帧「Agent 模式」骨架，随后恢复上次用的类型。
- **工具栏从左到右**：`[创作类型] [模型] [参考模式] [比例 · 分辨率 · 数量] [时长] [@] …… [预计积分] [发送 ↑]`。
- **模型**（下拉可见部分）：

  | 模型 | 下拉里的说明 |
  |---|---|
  | 即梦 Seedance 2.5 | 最强模型，支持 50 个参考，新增视频编辑、超长生成 |
  | Seedance 2.0 mini | 极致性价比 |
  | Seedance 2.0 Fast VIP | 会员专属通道；暂不支持真人人脸 |
  | Seedance 2.0 VIP | 会员专属通道 |
  | Seedance 2.0 Fast | 暂不支持真人人脸 |

  列表可继续向下滚动。网络请求里的图标名还出现了 1.5 pro、1.0、1.0 fast、minimax、happy_horse、wan、actor_m15-pro / m20 / m20_quick。
- **参考模式**：全能参考 / 首尾帧 / 智能多帧 / 智能编辑（Beta）/ 超长视频（Beta）。
- **比例 · 分辨率 · 数量 弹层**：
  - 比例：21:9、16:9、4:3、1:1、3:4、9:16。
  - 分辨率：480P / 720P / 1080P。各模型的可选范围本次没有逐一核对。
  - 生成数量：1 / 2 / 3 / 4。
- **时长**：滑杆刻度 0–30，另有数字输入框（单位 s）。当前为 Seedance 2.5 · 26 s。
- **输入框占位文字**：「上传最多50个参考素材、输入文字或 @ 参考内容，自由组合图、文、音、视频多元素……例如：@图片1 模仿 @视频1 的动作，音色参考 @音频1。」
- **提交前页面自己显示预计积分**：`520`，旁边是划线原价 `676`（Seedance 2.5 · 26 s · 720P · ×1）。
  - 折算：原价 26 积分/秒，会员价 20 积分/秒。
  - → 预检可以直接读页面的预计积分，不必维护价格表。
- **编辑器是 TipTap / ProseMirror**：`div.tiptap.ProseMirror[contenteditable=true][role=textbox]`。
  - 占位文字是一个 ProseMirror widget。
  - DOM 里有两个编辑器实例【推断：一个是隐藏的布局副本】。
  - 页面上**没有常驻的 `<input type=file>`**。上传入口是「+ 参考内容」卡片，hover 提示「上传参考内容」；为避免弹出系统文件对话框，没有点击。【推断：file input 在点击时动态生成 → 需要用 Playwright `expect_file_chooser`】
- **@ 选择器**（点工具栏的 @ 按钮）：
  - 标题「可能@的内容」；
  - 第一行「+ 创建主体」；
  - 下面是带缩略图的主体列表：`hy3_主角`、`hy1_主角`、`f80_f80`、`xj_酒剑仙`、`xj_阿奴`、`xj_拜月教主`、`xj_刘晋元`……，每行有「…」菜单。
  - 【推断：上传后的参考素材也会出现在这个列表里——见 B 的历史渲染】

### B. 历史记录与结果

- **每条记录的样子**：
  - 顶部是参考缩略图条。
  - prompt 里被 @ 的项渲染成**内联 chip**。原文是 `` `bg14-1(场景参考图)=> `` 加一个 chip `[缩略图] bg14-1`；人物项 `` `砌炉的老人(Seedance 人物 entity)=> `` 后面的 chip 是 `[缩略图] hy3_主角`。
  - 也就是说，**上传的参考素材按「文件名 stem」（＝路由键）被 @**，人物项 @ 的是主体名。用户现在的手工流程事实上已经在做「`=>@` → 文件 stem / 主体名」这一步绑定。
- **元信息行**：`即梦 Seedance 2.5 | 24s | 16:9 | 720P | 详细信息ⓘ`。hover 详细信息会显示「生成时间」与「消耗积分数」，生成中显示「计算中」。
- **生成中的记录**：
  - 画面上叠加「N%造梦中」，进度数字随时间递增。
  - 下方提示「超级会员 成功进入生成阶段，为您节省约 1 小时排队时间」→ 平台存在排队，会员可以跳过。
- **并发**：页面浮标显示「2/3 生成中… 回到底部」→ 这个账号同时跑多条是常态。
- **已完成记录的操作**：
  - 文字按钮：「重新编辑」「再次生成」「⋯」。「⋯」里的内容本次没打开成功，页面自动滚动导致点偏。
  - 视频上还叠着若干纯图标按钮（`span.action-button-*`，没有文字也没有 aria-label）。
  - → **下载入口在哪、是否无水印，尚未证实**。
- **结果视频地址**：video 元素的 src 是带签名、会过期的 CDN 地址 `https://v9-artist.vlabvod.com/{sig}/{expiry}/video/tos/cn/tos-cn-v-148450/{id}/`。它和下载按钮拿到的是否为同一文件，**未证实**。
- **记录流会自动滚到底部**（生成中的记录更新时）→ 按屏幕坐标点击不可靠，必须先按记录定位再在记录内找控件。

### C. 网络（只看 URL，没读 body）

- **签名**：内部接口都是 POST `/mweb/v1/*`、`/commerce/v1/*`，query 带 `aid=513695&web_version=7.5.0&da_version=3.3.27`。生成和历史相关的请求还带 `msToken` + `a_bogus` 签名。→ 自己重放请求就得伪造签名。这印证了 interview 定的「UI 操作 + 被动读响应」。
- **状态轮询**（反复出现）：
  - `/mweb/v1/get_history_queue_info`
  - `/mweb/v1/get_history_by_ids`
  - `/mweb/v1/creation_agent/v2/subscribe_session`：长轮询，先 pending 后 200。
  - → 状态可以通过 HTTP 响应被动拿到。页面是否另外还用 WebSocket，本次没有排除。
- **配置**：`/mweb/v1/video_generate/get_common_config`、`/mweb/v1/audio_generate/get_common_config`、`/mweb/v1/creation_agent/v2/get_agent_config`。【推断：各模型的参考数量、时长、分辨率上限应该就在这些响应里，机器可读】
- **主体**：`/mweb/v1/dreamina_subject/get`。**资产**：`/mweb/v1/get_asset_list`。
- **积分与会员**：`/commerce/v1/benefits/user_credit`、`/commerce/v1/benefits/user_credit_history`、`/commerce/v1/subscription/user_info`。
- **其他**：加载时出现了 `/mweb/v1/aigc_draft/generate_accelerate`，含义未知。真正的提交接口没有观察到，因为本次没有提交。
- **页内抓包试验失败**：往页面里注入 XHR/fetch 包装做被动捕获，约 6 s 窗口内一条目标响应都没抓到。→ 生产实现应在 CDP 层用 Playwright `page.on("response")` / context 级监听，不要在页面里 monkey-patch。

### D. 主体页 `/ai-tool/elements`

- **页面布局**：卡片网格。第一张是「新建主体」，后面是已有主体（`hy3_主角` · 1小时前修改、`hy1_主角`、`f80_f80`、`xj_*` ……）。顶部有 筛选 / 时间 / 排序。
- **「设置主体」弹窗**（打开的是已有的 `hy3_主角`，未保存即关闭）：
  - `参考主体*`：一张主图 + 若干附加图位 + 添加按钮；
  - `添加角色`；
  - `名称*`：带 **x/20** 计数，即**名称最多 20 字**；
  - `描述`：一段已预填的长文字描述；
  - `保存`。
- **顶部横幅**（2026-09-13）：「触底价，官方满血 Seedance2.5 720P 低至0.4元/秒｜Seedance2.0 Fast VIP 720P 低至0.2元/秒｜限时直降：会员5折」。
- **页头**：积分 `1.1万` · 超级会员 · 会员5折。

### E. 本机上的官方 `dreamina` CLI

- **安装**：
  - Windows 原生安装在 `~/bin/dreamina`。安装脚本本来就有 `windows_amd64` 分支，不需要 WSL。
  - `~/.dreamina_cli/version.json` 为 **1.4.5（2026-06-04）**，build 46b5b0e。
  - `tasks.db` 最后写入于 2026-06-21 → 用户以前用过。
- **登录与积分**：已登录。`user_credit` 返回 `total_credit: 8712`、`vip_level: ultra`。网页页头显示「1.1万」，两者对不上。【未证实：两边是否同一个积分池，页头可能把别的权益一并算进去】
- **最新版本**：官方已发布 **1.4.18（2026-09-10）**，更新说明「视频生成支持比例控制」。本机没有升级。
- **`multimodal2video`**（help 原文写明「对应网页『全能参考』」）：
  - 素材：image ≤ 9、video ≤ 3、audio ≤ 3（每段 2–15 s）；
  - `--model_version`：只有 `seedance2.0 / seedance2.0fast / seedance2.0_vip / seedance2.0fast_vip`；
  - `--duration` 4–15 s；1080p 仅 `seedance2.0_vip` 可选；
  - **没有主体相关参数**；
  - `--prompt` 是自由文本，没有文档说明怎么用 @ 绑定到具体素材；
  - 提交后异步返回 `submit_id`，用 `query_result --download_dir` 取结果。
- **图片命令**：
  - `text2image`：模型 3.0–5.0，分辨率 2k / 4k，比例 8 种；
  - `image2image`：1–10 张输入图，模型 4.0–5.0。
  - → 能覆盖 Seedream 锚点图生成，这类图本来就是「纯文字、零参考图」（`ai_video.md` rule 4d）。
- **其他**：1.4.5 没有任何主体命令。有 `session create/list/...`，对应网页的「对话」。

## 3. Implications for the spec

1. **仓库当前的出片方式只能走网页。** 实拍用的是 Seedance 2.5、16–30 s 的镜、`@主体`、单条可上传到 50 个参考，这些 CLI 1.4.5 一样都不支持。所以视频主路径必须有 web UI backend。
2. **`=>@` 的绑定规则直接照用户现在的手工做法定：**
   - 参考项 `{key}(类型)=>@`：上传 stem 等于 `key` 的文件，再 @ 这个 stem；
   - 人物项：@ 对应的主体名。
   - shot 适配层要保证上传后的文件名 stem 与路由键逐字一致。
3. **编辑器是 TipTap。** 填写方式：
   - 正文用可切换的文本插入策略填入；
   - 每个 mention 走真实交互：输入 `@` → 过滤 → 选中候选项；
   - 提交前校验编辑器 DOM 里 mention 节点的数量和名字与期望一致。
4. **预检直接读页面自己显示的预计积分。** 生成完成后再读「详细信息 → 消耗积分数」，把实际消耗写进记录。
5. **状态靠被动监听**：在 CDP 层监听 `get_history_queue_info` 和 `get_history_by_ids` 的响应，解析器带 `web_version` 版本号。
6. **主体**：
   - 名称 ≤ 20 字，要写进预检；
   - 创建所需字段是「参考图（主图 + 附加图）+ 名称 + 描述」。弹窗里**没有看到 turntable 视频的上传位**，与 interview 中「立绘 + turntable」的设想不符。
   - 已有主体叫 `hy3_主角`，与 interview 选定的规则 `hy3_砌炉的老人` 冲突，需要决定是迁移还是加别名。
7. **Seedream 图片可以走官方 CLI**（text2image / image2image），不需要做 DOM 映射，是第二个 backend 的候选。
8. **并发**：这个账号本来就常态同时跑 2–3 条，所以并发上限要做成可配置。

## 4. Open questions surfaced

- **下载**：下载入口在「⋯」还是视频上的图标按钮？会员下载是否无水印？CDN src 与下载文件是否同一份？
- **上传**：上传完成的信号是什么（缩略图出现，还是某个接口返回）？上传后的素材是不是一定出现在 @ 列表里、名字是否就是文件 stem？
- **提交**：提交接口的 URL 和响应结构（提交后如何拿到平台侧任务 id）？
- **配置**：`get_common_config` 响应里是否带各模型的上限，能否替代硬编码的规则表？
- **主体**：建主体能否上传视频？「添加角色」是做什么的？主体描述要不要由 service 生成？
- **CLI**：1.4.18 是否已经支持 Seedance 2.5、主体、30 s？CLI 的 8712 与网页的 1.1万 是否同一个积分池？
