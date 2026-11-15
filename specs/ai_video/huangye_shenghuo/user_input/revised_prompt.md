# 《荒野生活》系列 · 原始请求

> 本系列的 spec 目录在第一次请求**之后**才建立，所以原始请求登记在
> `follow_ups/202609.md` 的 `## 001` 一节（不在此处复制，避免两份出处）。
> 本文件只记录系列级任务的口径。

**task_type**：`ai_video` · **范围**：系列级（跨片），非单片
**系列**：`ai_videos/huangye_shenghuo/`（`series.json` 是「这是系列」的判据）
**已完成**：`hy1` 雨林第一夜 · `hy2` 红杉第一夜
**本任务**：把系列排产到 20 部以上 —— 定场景/锚点、元素系统、拍摄骨架与逐部概念卡。

单片级意图仍落各自的 `specs/ai_video/hy{N}/`；本目录只装系列级的。

# 《荒野生活》系列 · 后续指令日志 · 2026-09

> 本目录是**系列级**（跨片）意图的落点。单片意图仍落 `specs/ai_video/hy{N}/`。

---

## 001 — 2026-09-12 — 二十部片单与元素系统

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/_series/slate.md
>   - ai_videos/huangye_shenghuo/_series/slate_research.md
>   - ai_videos/huangye_shenghuo/_series/series_bible.md
> severity: medium

### 指令

系列要拍到 **20 部以上**。在开新片之前先定三件事：

1. **场景清单** —— 20 部各自的地点与位置锚点。
2. **元素的系统化引入** —— 观众可能喜欢的元素要有一套可复用的引入规则，
   用户举的例子是「每次增加一个新的小动物」；要求给出还有哪些元素轴。
3. **同类视频的吸引力调研** —— 先做实测调研（现有类似视频靠什么吸引人），
   再据此给 **top 20 推荐**。

### 一行摘要

把系列从「一部一部想」升级为「一张 20 部的片单 + 一套元素预算表」，并要求片单由实测调研支撑。

---

## 002 — 2026-09-12 — 房子要有特点 / 安全感 / 野外做饭 / 按环境引钩子

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/_series/slate.md
>   - ai_videos/huangye_shenghuo/_series/slate_cards.md
>   - ai_videos/huangye_shenghuo/_series/slate_research.md
> severity: medium

### 指令

对 20 部片单提四条要求：

1. **每部的房子要有特点** —— 不能各部长得一样。
2. **要有点安全感，不要太简陋** —— 房子要像能住人的，不是临时躲一夜的窝。
3. **引入野外做饭元素** —— 煮汤、烤肉等。
4. **不能太单一**；并且**要根据不同环境引入各自吸引人的地方**，据此继续调研、给更详细的 plan。

### 一行摘要

把片单从「20 个锚点」细化为「20 栋各有特点、有完成度的房子 + 20 条环境专属钩子 + 20 顿饭」，
并把骨架从 12 镜扩到 14 镜以容纳取食与做饭两段戏。

---

## 003 — 2026-09-12 — 房子要结实：抵御大风与野兽 · 提案合并成单一文档

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
>   - ai_videos/huangye_shenghuo/_series/series_bible.md
> severity: medium

### 指令

1. **房子要结实，要有安全感** —— 标准可以定成「**抵御得了大风，还有野兽**」。
2. **把提案全部放在《荒野生活》主目录下的一个 md 文件里**，便于在 webapp UI 里细看。

### 一行摘要

新增结构强度标准（L1 抗风 / L2 抗兽 / L3 被验证，全系列只 3 次兽夜、兽本体不进画），
并把原先分散的三份文档合并为 `ai_videos/huangye_shenghuo/proposal.md` 单一提案。

---

## 004 — 2026-09-12 — 澄清：「野兽」是形容档位，不要真的野兽

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
> severity: low

### 指令

澄清 003 的措辞：「抵御得了大风还有野兽」**只是形容**，用来说明**想要的房子是什么 level**。
**片里不需要真的出现野兽。**

### 一行摘要

强度标准从「抗风 + 抗兽」改写为「档位量尺（八行）+ 抗风六条」——质量口径而非剧情要求；
删除全部兽夜/爪痕/响声预警物设计，兽类调研数据降级保留为否决依据。

---

## 005 — 2026-09-12 — 直接用 hy 编号；已拍的锁定不动，未拍的继续讨论

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
> severity: low

### 指令

提案直接用 `hy1` / `hy2` 这套编号，不要另立概念编号。
**已经拍摄好的（hy1、hy2）直接放上去、保持不变**；
未拍的（hy3 起）可以继续讨论怎么拍、还要加什么元素。

### 一行摘要

废除 s01–s20 概念编号层，全文改用 hy 编号（编号即排产顺序）；
hy1 / hy2 进表但标「已锁定 · 不回溯」；新增讨论入口与元素候选池。

---

## 006 — 2026-09-12 — 人物 / 服装 / 工具变不变，由 Claude 提案；还能加什么元素

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
>   - ai_videos/huangye_shenghuo/_series/series_bible.md
> severity: medium

### 指令

1. **人物要不要变换、穿着打扮要不要变换、工具要不要变——由 Claude 直接 propose**，不要反问。
2. 除了「每部一只小动物」，**还有什么有意思的元素可以加**，一并提案。

### 一行摘要

提案：主角不换（要换人另开支线）；服装改三层制度（锁定层不变 + 按地带加气候外层 + 脏污层）；
工具分三类（原生永不变 / 自制累积上限 6 件 / 地方工具用完留在原地，后者即痕迹线机制）；
另提 6 条建议立即采用的新元素常量 + 3 条可选 + 2 条不建议。

---

## 007 — 2026-09-12 — 再提一批元素：反差（例：女汉子劈柴）

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
> severity: medium

### 指令

还有很多其他元素可以考虑，**比如「女汉子劈柴」——就是比较有对比/反差的元素**，再 propose 一些。

### 一行摘要

把「反差」立成轴 L（七类，每部至少三处、类型不重复）；女性主角查实数据（非泳池派 6–32M，
多条频道可复制）；另提第二批 6 条非反差类元素。

---

## 008 — 2026-09-12 — 更正：人物、工具都是每集可以换的

> target_stage: 1
> target_artifacts:
>   - ai_videos/huangye_shenghuo/proposal.md
>   - ai_videos/huangye_shenghuo/_series/series_bible.md
> severity: **high**（推翻了 006 里 Claude 的「主角不换」提案，并连带改动多处结构）

### 指令

**人物、工具都是每集可以换的。**

### 一行摘要

推翻 006 的「二十部同一个人」提案。人物每部换、服装随人换、工具改为「工具即人设」；
恒定符号转移到五样（签名定帧 / 片名格式 / 无人声 / 14 镜骨架 / 火）+ 统一色域；
长线伏笔升级为「痕迹人链」（每部的人留下的东西是另一部的人看见的痕迹）；
连带改写 hy11 / hy16 / hy18 三部，其余十七部不受影响。

---

## 009 — 2026-11-08 18:21:24 — migrate-to-three-module-v1

> target_artifacts:
>   - ai_videos/huangye_shenghuo/README.md
>   - ai_videos/huangye_shenghuo/workflow.json
>   - ai_videos/huangye_shenghuo/bible.md
> severity: high

### 指令

荒野生活这部系列剧已经过期了，用最新的标准更新一下，就用 Portal Travel（chuanyue_yiri）的标准

### 摘要

系列改为 three-module-v1 连续剧片种（照 Portal Travel 结构）：旧 hy1–hy4 与提案移入 _legacy/ 只作历史；新建 README（Vision 草稿待用户认可）、workflow.json（含出片前审查闸门）、bible.md 模板库 v0、topics.md、2_世界观人设/series.md

---

## 010 — 2026-11-08 18:36:11 — protagonist-look-candidates

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters
> severity: medium

### 指令

可以（认可 Vision 草稿与第一集雨林重做的建议）；先弄个好点的主人公：中美混血的男子，要有东亚儒雅的长相

### 摘要

Vision 草稿与 ep01 雨林获用户认可；新建主角 c1（中美混血男子、东亚儒雅长相），Codex 出长相候选供用户选

---

## 012 — 2026-11-08 18:50:19 — ten-protagonist-candidates-sheets

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_主角/candidates/v2
> severity: medium

### 指令

生成10个人让我选，分别是正面、侧面、背面、各种表情的照片，做好了给我 url 我打开看

### 摘要

主角候选扩到 10 人（A–D 沿用 + E–J 新出）：每人定妆照、正侧背三视图、4 张表情（专注 / 满足的笑 / 疲惫 / 警觉），Codex 出图，做成可打开的对比页给用户选

---

## 011 — 2026-11-08 18:37:29 — genre-research-flow-and-hooks

> target_artifacts:
>   - ai_videos/huangye_shenghuo/0_research/parts
> severity: low

### 指令

同时 research 一下其他荒野求生的视频都是怎么个流程做的，有哪些吸引人的元素我们可以加入进来

### 摘要

同类荒野建造/求生视频调研（流程结构、吸引元素、观众吐槽与 AI 穿帮），写 0_research/parts/h01，结论再提给用户决定哪些进 bible

---

## 014 — 2026-11-08 19:38:57 — adopt-h01-recommendations

> target_artifacts:
>   - ai_videos/huangye_shenghuo/bible.md
>   - ai_videos/huangye_shenghuo/README.md
> severity: medium

### 指令

就按照你的建议来（同类视频调研 h01 的建议写进 bible：可直接加的全加；四条冲突由代理定）

### 摘要

h01 §5 建议落 bible/README：开场 15 秒亮钟、随身物清单、做饭小段 20–40 秒、合段 20–25% 屋内小仪式与窗光外景、秘密感、手部与内景布局审查、身体跟天气走、只取倒木落石、默认不配乐、睡前节奏；冲突四条代理定：成品一闪采用、跨日不采用（改雨中一滴不漏）、温柔挪开小动物采用、默认关闭 CC 字幕采用

---

## 013 — 2026-11-08 19:15:13 — protagonist-round3-from-BDI

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_主角/candidates/v3
> severity: medium

### 指令

以 B、D、I 作为 baseline，再出 10 版给我看看，表情有微笑、沮丧、悲伤、愤怒、劳累、兴奋

### 摘要

以候选 B/D/I 为参考混出 10 个变体 K–T：每人定妆照、正侧背三视图、六种表情（微笑/沮丧/悲伤/愤怒/劳累/兴奋），做成对比页

---

## 015 — 2026-11-08 19:52:59 — pick-protagonist-O

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_主角
> severity: medium

### 指令

我们选 O

### 摘要

主角定为候选 O（D+I：四十岁左右、低发髻、两鬓花白、灰黑短络腮胡）：O 定妆升为立绘，Codex 出高清正侧背三视图并合图，人物卡写外观与锁定描述符；名字与建立视频待用户定

---

## 016 — 2026-11-08 20:09:09 — julian-all-episodes

> target_artifacts:
>   - ai_videos/huangye_shenghuo/bible.md
> severity: medium

### 指令

先全部用 Julian，需要换人我会告诉你

### 摘要

主角 Julian 跨集固定：每集都用 Julian，换人只在用户明确要求时；bible §2、README、series.md、人物卡同步

---

## 017 — 2026-11-08 20:26:12 — julian-turntable-and-ep01-story

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_Julian
>   - ai_videos/huangye_shenghuo/episodes/ep01
> severity: medium

### 指令

可以出视频。然后开始故事创作

### 摘要

提交 Julian 4 秒建立视频（Seedance，用户同意）；开 ep01 雨林：先按 bible §7 做考据 dossier，再走共用故事创作模块出故事稿与集级决策记录

---

## 018 — 2026-11-08 21:06:37 — ep01-storyboard-autonomous

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01
> severity: medium

### 指令

等你整个故事板做好了，再通知我

### 摘要

EP01 由代理连续推进到故事板完成再通知用户：冷读修订故事 → 影视改编（分镜、场级决策）→ 资产（背景、道具、换装）→ 每镜 overhead、镜组板与首帧图（场故事板）；不出视频

---

## 019 — 2026-11-08 22:37:08 — storyboard-self-review-then-url

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/scenes
> severity: low

### 指令

你做好了并且 self review 完了给我 url，我来 review

### 摘要

故事板完成后先自审（代理逐张看图 + 独立审稿代理对照分镜与故事稿逐镜审），改完再给用户故事板 / 分镜 / 故事的管理站链接

---

## 020 — 2026-11-09 00:06:33 — autonomous-overnight

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01
> severity: medium

### 指令

我要睡觉了，尽可能多地完成之后能想到的步骤，不要问问题，不确定的自己 best effort 决定，包括删除文件这类高风险决定

### 摘要

AUTONOMOUS：代理连夜推进 EP01 故事板到自审完成（重出首帧、独立审稿第二轮、修复），整理链接与待用户决定事项；确定版本与出视频仍留给用户（生成永远人点）

---

## 021 — 2026-11-09 21:32:54 — julian-black-hair-boots

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_Julian/
> severity: medium

### 指令

男主的白发太多了，去掉白发。 还有脚上，小腿不要搞白色的布料，样式不好看，颜色也不搭，重新生成

### 摘要

Julian 改黑发黑胡；雨林装米白防蚂蟥袜套+低帮胶鞋换黑色哑光橡胶中筒靴；重出立绘、两套三视图与 EP01 含 Julian 的首帧，文字设定同步

---

## 022 — 2026-11-14 11:40:22 — julian-turntable-v2

> target_artifacts:
>   - ai_videos/huangye_shenghuo/2_世界观人设/characters/c1_Julian/c1_Julian_turntable.mp4
> severity: low

### 指令

重新出turntable视频

### 摘要

用 v2 黑发立绘重出 c1_Julian_turntable.mp4（Seedance 2.5 · 16:9 · 4 秒），旧视频存 _v1/

---

## 023 — 2026-11-14 11:53:52 — spatial-consistency-cooking-cozy

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/
> severity: high

### 指令

对于这类视频，空间大小的正确性非常重要，比如外面看屋子不大，到了里面如果空间很大就显得很突兀，所以确保有组后的空间建立房子，还有空间一致性的检擦，还有就是位置和状态一致性，比如门口的小溪里房子多近？ 下雨后能变成多大？ 这些都要一致性检查，确保图片都是统一的。还有就是做饭的场景可以加一点，以及找个skill，把房子内部做的惬意一点。请重新review，然后自动更新文字和图片，只有出片前给我review，其他你都自己fix就好

### 摘要

Blender 白模定尺度；内外景独立空间审稿；修离群首帧；屋内参考按正确尺度重画并做惬意版；加三段做饭镜头；故事稿几何文字对齐锁定表

---

## 024 — 2026-11-14 14:58:35 — remove-buttress-roots

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/
> severity: high

### 指令

薄板看起来还是一眼假，哪有树干或树根长起来个薄板的，这个要去掉

### 摘要

锚点树与巨树去掉板状板根，改为普通树干与粗圆表面根；屋檐改由屋角四根带杈短柱架起的檐杆支撑，两侧半米扇叶矮墙；锁定表、故事、分镜、卡片、白模与约 38 张图同步

---

## 025 — 2026-11-14 15:52:33 — door-view-site-map

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/decisions/site_map.png
> severity: medium

### 指令

房子盖好后。打开门就是翻滚的褐色大水，这个位置和之前刚房子的时候consistent么？ 之前感觉小溪没有离得这么近啊，为什么打开们就看到了，这个审查有审查到么，还有是不是可以放一个俯视图，标记房子，小溪，树，就是主要object的相对位置和距离

### 摘要

s1 st1/s8 st5 门外洪水画成贴着门槛，与锁定（门→岩坎 6.4 米、洪水比阶地低 2 米）不符，空间审稿漏查；改图；新增场地俯视图+门口视线剖面 site_map.png

---

## 026 — 2026-11-14 16:26:01 — ep01-final-render

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/
> severity: high

### 指令

好的，如果审查没问题就开始出片子吧直接720p正片

### 摘要

确定 EP01 故事与分镜版本，Prompt 编译，跑 pregen 审查单收轮，审查无严重问题即按用户授权跳过草稿直接 720p 正片提交全集

## 027 — 2026-11-14 23:15:47 — ep01-submit-720p

> target_artifacts:
>   - ai_videos/huangye_shenghuo/episodes/ep01/
> severity: high

### 指令

出片吧

### 摘要

用户看过整集预览后同意出片：EP01 全集 67 镜按 r3 审查结论跳过草稿直接提交 720p 正片（Seedance，扣积分），提交后轮询下载并记录

## 028 — 2026-11-15 10:36:37 — resume-ep01-render-recovery

### 指令

继续完成此前已授权的 EP01 720p 出片：补收已生成镜头，处理失败和未提交镜头，核验全集并执行出片后质检。

### 摘要

接续 Claude 中断的 EP01 出片收尾
