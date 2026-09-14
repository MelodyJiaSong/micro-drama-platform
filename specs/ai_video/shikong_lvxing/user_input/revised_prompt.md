# 《时空旅行》系列 · 合并后的完整意图（raw_prompt + 全部 follow-ups）

> 派生文件，由 `raw_prompt.md` + `follow_ups/*.md` 按时序拼成。改动请改源文件后重生成。

# 《时空旅行》系列 · 原始请求

> **task_type**：`ai_video` · **范围**：系列级（跨片），新系列立项前调研
> **系列目录（暂定 slug）**：`ai_videos/shikong_lvxing/`（`series.json` 是「这是系列」的判据；2026-09-13 用户定名，原临时 slug `shikong_jizhe` 已改）
> **上游经验**：《荒野生活》系列（`ai_videos/huangye_shenghuo/`，16:9 · 约 4.5 分钟 · 无人声 · 四站发布）
> 单片级意图日后落各自的 `specs/ai_video/{prefix}{N}/`；本目录只装系列级的。

## 用户原始意图（2026-09-13，抽象化）

拍完《荒野生活》后开一个新系列：**记者穿越回古代有名的历史场景 / 城市 / 事件进行拍摄**，
用更活灵活现的方式展现和讲述历史——记者逛城市、边逛边解说、采访当地的人，
给观众一个立体的历史场景与人物；再加一些有趣、吸引人的元素。

硬要求：
1. **目标 = 观众爱看 + 从中学到历史知识**。
2. **每一集都要做大量 research**——当时的城市什么样、人们穿什么、吃什么、习俗是什么——用调研支撑每一集。
3. 立项前先**调研同类系列剧是怎么拍的**，把结论与建议一并给出。

## 本任务产物

- `ai_videos/shikong_lvxing/proposal.md` —— 系列总提案（系列公式 / 记者人设 / 单集骨架 / 片单 / 每集调研 SOP / 合规 / 调研证据 / 待拍板决定）。
- 调研原始报告与 yt-dlp 实测 JSONL 留在会话 scratchpad，不入库（`_research/` 只收系统化的选题调研数据集）。

---

# 《时空旅行》系列 · 后续指令日志 · 2026-09

> 本目录是**系列级**（跨片）意图的落点。单片意图日后落 `specs/ai_video/{prefix}{N}/`。
> 原始请求见 `../raw_prompt.md`；本文件从 001 起只记原始请求之后的追加意图。

---

## 001 — 2026-09-13 14:41:00 — 调研提速：跳过卡住的角度、不等全量核实

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
> severity: low

### 指令

立项前调研跑得慢时，**跳过仍在长时间抓取的角度直接继续**，不因个别角度未完成而卡住整份提案。

### 一行摘要

提案以已完成的 11 份调研报告为准；F7（受众机制 / 变现）与 D1（Horrible Histories 栏目深读）标为「未完成」，缺口在提案附录列明，日后可单独补跑。

---

## 002 — 2026-09-13 19:25:00 — 四个立项决定：系列名 / 旅行者名册 / 双语首发 / 片长

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/series.json
> severity: medium

### 指令

1. **系列名《时空旅行》**，片目录前缀 `sk`（`sk1 / sk2 / …`）；目录 slug 随之定为 `shikong_lvxing`。
2. **旅行者不是一个人，是一本名册**：外国城市 / 历史用欧美 vlogger 面孔，中国题材用中国面孔；男女都建，每站按需要选一位。
3. **语言**：同一画面配中英两条 TTS 轨；抖音 / 小红书先发汴京，YouTube / TikTok 先发罗马。
4. **只做 16:9，约 10 分钟**，长点短点都不要紧。

### 一行摘要

提案 §0 决定 1–4 落定；A §3 从「一个记者」改写为「旅行者名册 + 共用人设骨架 + 五样恒定符号承担识别度」；目录由 shikong_jizhe 改名为 shikong_lvxing，片前缀 zg → sk。

---

## 003 — 2026-09-13 19:32:00 — 镜长约 20 秒 / 首尾易拼接 / 逛城市一镜到底 / 体验衣食住行

> target_stage: 5
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
> severity: medium

### 指令

1. **每个 shot 最好 20 秒左右**——不要生成很多琐碎的小视频，拼接方便。
2. **每个 shot 的起始与末尾要考虑拼接的容易性**——镜头自然切换，省掉剪切的 effort。
3. **逛城市时增加「一镜到底」**，可以吸引人。
4. **旅行者要体验当地衣食住行的各个方面**——看看吃的什么、居住环境什么样。

### 一行摘要

单镜 15–27 s（目标 20 s）、10 分钟 ≈ 28–34 镜、一个地点 + 一个状态 ＝ 一镜；相邻镜按「硬切 + 景别跳档」设计并由 `jb= / jbcam=` 逐对机检，出片端零剪辑；每站 ≥ 1 个 20–30 s 一镜到底穿街长镜；骨架显式覆盖衣 / 食 / 住 / 行（站一「住 + 穿」、站六「住 · 客栈晚饭」）。

---

## 004 — 2026-09-13 19:40:00 — 资产建立前先做大量参考图 research / 下载历史图片做 reference / 一镜到底走 Blender 建城

> target_stage: 2
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
> severity: medium

### 指令

1. **为了真实，创作时要做大量 research**：每个场景、建筑、食物、人物穿着、object 的建立，都要从网上查找大量 reference。
2. **在 scenes / props 目录下下载历史图片做 reference**，方便生成真实的图片（要求 Claude 代为下载）。
3. **一镜到底长镜头**：有些 shot 需要先在 Blender 里建造完整的城市容貌，用 Blender 渲出一镜到底的视频，上传做 reference，再让 Seedance 拍摄。

### 一行摘要

阶段 2 每个资产先建「参考图库」（≥ 8 张历史参考图 + `refs.md` 索引，图走 R2）再写锚点 prompt；新建 `tools/ref_fetch.py` 从开放馆藏 API 检索下载并登记许可；一镜到底镜走 `build_{city}.py` 建城 → previz mp4 → Seedance 视频参考（运动 / 几何），长相仍由锚点图给，与 rule 4d ① 的关系在 divergence 登记。

---

## 005 — 2026-09-13 20:05:00 — 第二轮拍板：结尾不固定 / 每站独立 / 只定 sk1 / 城市建立要俯视排版图

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
> severity: medium

### 指令

1. 同意「一个任务 + 一个障碍」主线；受访者只用虚构平民。
2. **同意阶段 0 史料调研作硬门槛 + 史实标签机检写进格式契约**（仓库级变更，批准）。
3. **结尾不固定**：「带古人到今天看一眼」看视频 feedback 再决定要不要固化。
4. 发布用已有频道；月更 2 站。
5. **不做「上一站纠错」；每一站都不需要知道其他站**。
6. **不现在定 12 站顺序：先拍一个看效果，再慢慢选下一站**。
7. 英文系列名只在 publish.md 里用得到，不反对 *Posted to the Past*。
8. 城市建立：**先下载很多历史图做 reference → 生成 AI 图片 → 导入 Blender 建城市模型；还要一张俯视全景 / 排版图**（方块 1 ＝ p1 建筑、方块 2 ＝ p2 建筑…标出整个城市或地形）。
9. **批准新建 `tools/ref_fetch.py`**。

### 一行摘要

提案 §0 决定 5–12 落定；不变量去掉固定结尾与全部跨站线索（I-6 / I-8 / I-12、元素系统「跨站轻线索」行删除、骨架无下站预告）；B 章改为「候选池、只定 sk1 汴京」、C 章 sk2/sk3 降为候选卡；G §8 加「城市建立五步」（参考图 → 单体建筑三视图 AI 出图 → image-to-3D → 俯视排版图 city_plan → build → previz），与 rule 4g ② 的差异记 divergence。

---

## 006 — 2026-09-14 00:05:00 — 自主模式：sk1 不停顿跑到出 prompt

> target_stage: 2
> severity: low

### 指令

sk1 从阶段 2 起**不停顿跑到出 prompt 与 publish.md**；有疑问时 Claude 自行做最佳判断并在产物里记「判断：」，不再向用户提问；所需权限已全部授予。

### 一行摘要

等同于 `# EXECUTION MODE: AUTONOMOUS`：每阶段 QC 照跑（blocker 清零才进下一步），人工确认关卡由「判断记录 + changelog」替代，用户醒来后复核。

---

## 007 — 2026-09-14 08:12:53 — 自主跑完 sk1 剩余全部工作 / 系列按《荒野生活》同构延续

> target_stage: 6
> target_artifacts:
>   - tools/gen_shots_sk1.py
>   - ai_videos/shikong_lvxing/sk1/
>   - ai_videos/shikong_lvxing/proposal.md
> severity: medium

### 指令

1. **不向用户提问**，疑问由 Claude 自行判断并在产物里记「判断：」，把 2026-09-14 盘点出的剩余事项全部做完：修分镜生成器的构建闸门问题、修镜内逻辑检查器的误报、补齐阶段 2（人物网 / 配音选角表 / 阶段 2 QC / README）、出全部分镜 prompt、全维度审查、四站发布页、提交 git 并把参考图同步到 R2、Blender 建城与 previz、补跑 F7 / D1 两个调研角度。
2. **系列结构对齐《荒野生活》**：`ai_videos/shikong_lvxing/` 是系列目录（`series.json`），每一站 `sk1`、`sk2`… 与 `hy1`、`hy2` 同构、各自独立成片。

### 一行摘要

等同 `# EXECUTION MODE: AUTONOMOUS`，范围＝sk1 出 prompt 与发布页之前的全部剩余工作 + 系列提案补跑调研；系列嵌套结构维持现状（已与荒野生活同构）。

---

## 008 — 2026-09-14 08:26:14 — 旅行者不与当地人对话：只对镜头自述

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/sk1/1_立项/concept.md
>   - ai_videos/shikong_lvxing/sk1/3_大纲/outline.md
>   - tools/gen_shots_sk1.py
> severity: high

### 指令

1. **不要和当地人有太多语言交流**：古代的方言与说法无法确定，当地人一开口就等于编造。
2. **旅行者只对着镜头自己介绍、解说**（对镜说话 + 画外独白）。
3. 适用于全系列每一站。

### 一行摘要

当地人不出清晰台词，只靠动作、神态、手势与旅行者互动，人群只留听不清字句的环境声；「采访任务 / 街头民调 / 今天是他 / 受访者」改为「观察 / 跟拍」。

---

## 009 — 2026-09-14 08:27:55 — 节目形态定为「外来游客带逛」：全开放游览，方方面面都介绍

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/series.json
>   - ai_videos/shikong_lvxing/sk1/1_立项/concept.md
>   - ai_videos/shikong_lvxing/sk1/3_大纲/outline.md
>   - tools/gen_shots_sk1.py
> severity: high

### 指令

1. **重点是 vlogger 带观众游当地**：介绍古时候这座城的城市面貌、吃什么、住的条件（比如亲自住一晚旅馆试试）、怎么娱乐、穿什么、人们怎么活动；当天如果有重大历史事件，就去看它是什么样子。
2. **可以到处转**：医馆、官府、皇宫、文人雅客聚集的地方……方方面面都可以介绍。
3. **旅行者的身份**：一个**默认有权限到处逛的外来旅客**，带着好奇心去发现、记录、讲解所见所闻。
4. **片长**：10 分钟左右，不限死，需要时延长到 15 分钟也可以。

### 一行摘要

系列公式由「记者领采访任务、撞规矩、日落交差」改为「好奇游客全开放带逛、边看边讲」：无采访、无被拦、无与当地人对话（承 008）；每站按城市面貌 / 吃 / 住（过夜）/ 娱乐 / 穿 / 人的活动 / 当天大事 / 医馆·官府·皇宫·文人聚处等逐块覆盖；片长 10–15 分钟。

---

## 010 — 2026-09-14 08:39:28 — 开场航拍式长镜扫全城 / 整城 Blender 建模 + 白模动画作 Seedance 参考 / 自主做完

> target_stage: 2
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/sk1/1_立项/concept.md
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/city_plan.md
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/blender_build.md
>   - tools/build_bianjing.py
> severity: high

### 指令

1. **拍摄手法**：展现城市面貌是重点，所以**每站片子一开始就是一个连续长镜头扫过整座城**——像无人机飞过城市，时而低空穿行、时而高空俯瞰（只是比喻，画面里没有无人机）；长镜之后才进正片。
2. **城市与环境要求极高**：先用 Blender 建一座**完整的城市 3D 模型**。做法是先有一张城市平面排版图（floor plan），方块 1 ＝ 房屋 prop1、方块 2 ＝ 房屋 prop2……，拿到整座城的全局布局；再按需要让 Claude 在 Blender 里把城建出来。辅助工具：Hyper3D、Cascadeur。
3. **白模动画当参考**：在 Blender 里模拟一镜到底和其他需要的镜头，生成白模动画视频；Seedance 以这些白模视频为参考生成最终视频。
4. 用户需要一份「怎么帮助 Claude + Blender 建出完整城市模型」的说明。
5. **自主做完**：遇到疑问自行决定，一气把能做的都做完；有错不要紧，用户回来检查再改。

### 一行摘要

每站开场 ＝ 航拍式连续长镜扫全城（系列不变量）；城市几何由「全城平面排版图 → 方块占位 → 建筑资产替换」的 Blender 模型承载，全部需要的镜头出白模动画作 Seedance 运动 / 几何参考；说明写进 proposal G §8 与 sk1 `blender_build.md`。

---

## 011 — 2026-09-14 12:49:07 — 高风险问题也自行决定（用户离开约 8 小时）

> severity: low

### 指令

即使是有风险的问题，也由 Claude 自行做决定；用户约 8 小时后回来检查。

### 一行摘要

扩展 007 / 010 的自主授权到高风险决策。判断：本地 git commit 照做（资产 hook 同步 R2）；**不执行 `git push` 到远端**（用户从未要求、推出去无法撤回）；即梦出图仍不代点确认（桥接服务规定只能本人在本地网页确认、自动化有封号风险）。所有决定记入 `specs/ai_video/sk1/changelog.md`。
