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

# Follow-ups（按时间顺序合并）

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

---

## 012 — 2026-09-15 21:21:22 — 旅行者改为阳光健身型 vlogger、出 6 位候选 / 视频里旅行者要出声 / 系列人物只放 `_series`

> target_stage: 2
> target_artifacts:
>   - ai_videos/shikong_lvxing/_series/characters/
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/characters/
>   - tools/gen_shots_sk1.py
>   - specs/ai_video/sk1/divergence.md
> severity: high

### 指令

1. **sk1 主角林问的长相太普通**：需要的是 vlogger 形象——阳光开朗，身体一看就是有锻炼的独立女性。
2. **出多个 vlogger 给用户挑**：先来 3 个中国人、3 个外国人（参照 *Chloe vs History* 的主持人那样的形象）。
3. **这次视频里的人要有声音**：人物（character）prompt 要带声音，用于对台词的部分。
4. **「系列人物」的概念保留**，但每个 sk1、sk2 目录里不要再各放一份——否则下载导入会冲突、不工作。

### 一行摘要

判断：「三个国人」按上下文与 Chloe 的参照理解为「三个外国人」；6 位候选先都做成符合第 1 条气质的女性旅行者（男旅行者以后按需加）。旅行者的台词由视频模型直接出声（锁定声线 + 声样台词，出镜对口型），当地人仍不开口。系列人物卡只住 `_series/characters/`，单站目录不再建同键人物卡；单站服装等只属于这一站的视图挂在系列卡下、路由键全系列唯一。

---

## 013 — 2026-09-18 13:02:01 — 系列扩边：开虚拟城支线，第 2 站 sk2 ＝ 魔兽世界暴风城

> target_stage: 0
> target_artifacts:
>   - ai_videos/shikong_lvxing/series.json
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/_series/sources.md
>   - specs/ai_video/sk2/divergence.md
> severity: high

### 指令

1. **与 sk1 同步开启第 2 站 sk2**，形态、工具链、系列不变量沿用 sk1。
2. **这一站去的是「虚拟的城」**——魔兽世界的暴风城（Stormwind）。系列自此不再限于历史上的城。
3. **照 sk1 的做法把资料做全**：research 全部暴风城资料，据此构建 scene / character / props 与 shots。
4. 用户提供一条 YouTube 暴风城素材链接作形制对照。

### 一行摘要

系列分出**虚拟城支线**：阶段 0 由「史料调研」平移为「设定考据」（方法论同构，只换来源类型——T0 ＝ 作品本体，T4 ＝ 玩家推测与模型默认），「纪年」由年号换成**作品版本锚点**，❌ 新增第二种来源「版本错置」，参考图因权利人版权**只作形制依据不入画**，合规新增 **IP 维度**。十五条不变量只改两条（I-2 签名开场去掉「距今 N 年」、I-10 字卡改「虚构世界情景再现 + 非商业同人」），其余 13 条原样成立；**I-4 签名收尾逐字不变，含「历史不退款」，不许优化**。规则落 `proposal.md` § H + `sources.md` §8 + `sk2/divergence.md` #101–110。

### 用户两轮多选题拍板（sk2 开工参数）

版本锚点＝**经典旧世 Vanilla** · 画风＝**半写实（形制配色忠于游戏、材质光线写实）** · 旅行者＝**c4 艾拉 Ella Hart**（英语原声）· 考据严格度＝**沿用 sk1 口径** · 当天大事＝**工程日 · 矿道地铁通车** · 片长＝**15 分钟版** · 机构 4 处＝**王座厅 / 大教堂 / 矿道地铁 / 巫师圣殿** · 整城建模＝**要 · 走廊制**。

### 已知限制（据实记录）

- YouTube 链接 `roMWEeV2P4U`：页面为 SPA，WebFetch 只返回页脚导航，取不到标题 / 描述 / 字幕；**Claude 无法观看视频内容**。已登记进 `_series/sources.md` §8.2 备查，需要具体画面时由用户截图提供。
- 待用户拍板：**IP 定性与发布策略**（阶段 6 `publish.md` 之前）、**虚构站签名开场句**的最终措辞（阶段 1 立项时确认）。

---

## 014 — 2026-09-18 15:10:00 — 虚拟城站的 I-7 改为「有逐字原文才能开口」

> target_stage: 0
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - specs/ai_video/sk2/divergence.md
> severity: high

### 指令

虚拟城站放宽 I-7「当地人零台词」：**当地人可以开口，但只允许逐字引用作品内原文**（须带 `source_url` + `quote`），**一个字不得自编**；没有原文的路人仍零台词。

### 一行摘要

**这不是放宽，是把铁律还原成它本来的意思。** I-7 的原始理由是「古代方言与说法无法确定，当地人一开口就等于编造」（follow-up 008）——**约束的对象从来是编造，不是声音**。历史站里两者恰好重合（没有原文，开口即编），所以写成了「零台词」；**虚拟城站里两者分开了**：作品本体记着每一句台词的逐字原文。**历史站的 I-7 原样不动。**

**配套三条**：① 开口的 NPC 按 rule 12.4-H 建 `voice_id`（同一角色全剧复用一个）；② 每句台词进事实注册表、`tag` 只能是 ✅（**没有 ⚠️ 档，推测出来的台词不存在**）；③ **旅行者形态完全不变**——对镜 ≤ 40% + 画外 ≥ 60%，一路边走边讲，密度合同照旧，**她仍然不和当地人对话**。

### 解锁了什么

sk2 候选池里画面与结构最强的《假面舞会》——温德索尔从城门一路走到王座厅、当庭揭穿卡特拉娜·普瑞斯托即黑龙奥妮克希亚。这条路线本身就是一条贯穿全城、落点在既定机构的摄影机动线。

---

## 015 — 2026-09-18 16:10:00 — 虚拟城站允许「偶尔的 NPC 互动」；形态定调「旅游 + 解说」

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/proposal.md
>   - ai_videos/shikong_lvxing/series.json
>   - specs/ai_video/sk2/divergence.md
>   - ai_videos/shikong_lvxing/sk2/1_立项/concept.md
> severity: high

### 指令

1. 整体给人的感觉就是**旅游 + 解说**。
2. **还要有偶尔的和 NPC 互动。**

### 一行摘要

第 1 条确认既定形态（游览 vlog：路线管「旅游」、密度合同管「解说」），无需改动。
第 2 条**撤销 follow-up 008 的「她不和当地人对话」在虚拟城站的适用**——改为**三档互动制**，并借 follow-up 014 已放宽的 I-7 落地：

| 档 | 允许什么 | 依据 |
|---|---|---|
| **档 1 · 无声互动** | 手势、点头、摇头、指一指、递东西、付钱；**敬礼 → 回敬礼、挥手 → 回挥手** | 历史站已有；且**游戏里 NPC 的反应本来就是动作**（W5 查实），天然成立 |
| **档 2 · 她开口 + NPC 以逐字原文回应** | 她问路 → 卫兵 `"Light be with you, sir."`；她买面包 → 小贩 `"Rolls, buns and bread. Baked fresh!"`；她进店 → 旅店老板 `"Welcome to my Inn, weary traveler."`；她坐下 → 酒馆老板 `"Grab a drink my friend and pull up a seat"` | follow-up 014 的 I-7 虚拟城口径：**有逐字原文才能开口** |
| **档 3 · ❌ 仍然禁止** | 自编 NPC 台词 · NPC 回答她的具体问题（除非恰好有对得上的原文）· **NPC 讲解设定知识** · NPC 参与叙述 | I-7 的原始原则「**不借当地人之口说史料**」原样保留 |

**一条不变的分界**：**知识仍然只由旅行者讲。** NPC 只做他们本来会做的事、说他们本来会说的话；他们不是解说员、不是信息源。

**为什么这对虚拟城站是净收益**：NPC 的招呼语与吆喝**恰恰是一部旅游 vlog 最需要的环境真实感**，而且**一个字都不用编**——这批台词在作品里逐字存在。历史站做不到这一点（没有原文），所以历史站的「零对话」原样不动。

### 连带改动

- `series.json` 的 description 里「**她不和当地人对话**」一句需按两类站分述。
- `proposal.md` § H 的 I-7 条目补一节「互动三档」。
- sk2 登记 `divergence #113`，并回改 `1_立项/concept.md` 的形态铁律段。
