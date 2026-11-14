# 原始需求 · 排行榜滚动系列（paihangbang）

> 采集时间：2026-11-02 ｜ task_type: ai_video（非短剧：数据排行视频系列，不走 three-module-v1 六模块）｜ 系列 slug: paihangbang

接下来我们要做一个系列的视频，类似于这个： https://www.youtube.com/watch?v=YzRCcFx3XME
我们先找一个 topic，然后找出相应的前 X 名排名，下载图片，配上最新的 stats，配上国家，
然后再整点小的 icon，然后从左到右滚动，然后配上音乐，一个系列就出来了，
帮我 research，然后制定这个系列的 foundation。

---

## 001 — 2026-11-03 08:36:25 — pilot-decisions

> target_stage: 1

### 指令

用户定系列基础决定：试播两期为世界最高建筑 Top 50 与世界最高山峰（替换原建议的市值公司）；画面语言英文、面向全球；音乐用 Suno（本机服务）；试播先不加旁白；滚动方向确认为卡片向左平移、读序从左到右、冠军最后出场；渲染器用 Python + skia + ffmpeg 自建开发项目；发布到已有频道。

### 摘要

试播选题（建筑+山峰）、英文、Suno、无旁白、滚动方向、渲染器路线、已有频道

---

## 002 — 2026-11-03 08:38:35 — mountains-by-country

> target_stage: 1

### 指令

最高山峰试播期口径定为「各国最高峰 Top 50」：每个国家取其最高点，按海拔排序（50 国 50 面国旗，覆盖各大洲），不做纯海拔世界前 50（只有 7 个亚洲国家、多座在克什米尔争议区）。频道名与近期上传分析推迟到上线前。

### 摘要

ep02 口径=各国最高峰 Top 50；频道分析推迟到上线前

---

## 003 — 2026-11-03 09:14:55 — overnight-autonomous-build

> target_stage: 2

### 指令

用户睡前授权（2026-11-03）：尽可能多地完成后续步骤，不提问；不确定时自主做 best-effort 决定（含删除等高风险决定），判断记录在文件里。代理据此：定每期数据契约、建 ep01/ep02 数据与图片包、建渲染器 projects/rank_scroll（agent_team AUTONOMOUS）、尝试 Suno 配乐、渲染两期并独立审片、生成发布草稿。

### 摘要

AUTONOMOUS 夜间推进：数据契约、两期数据包、渲染器、渲染、审片、发布草稿

---

## 004 — 2026-11-03 12:03:36 — card-layout-photo-first

> severity: medium

### 指令

出来的视频有一个问题，就是图片占比太少，已更改把图片放大一点，其他信息放到别的位置展示，我觉得这个视频要突出的，第一是图片，第二是国旗，第三是关键的stats，你可以再仔细研究下排版，然后重出视频

### 摘要

卡片改为满版照片海报式：照片铺满整卡，大国旗（按原比例）压左上，关键数值在底部渐变区；地名/标签并成一行小字；每期可设卡宽，加 image_focus 裁切焦点；两期重渲

---

## 005 — 2026-11-03 14:23:18 — multi-source-image-candidates

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
> severity: medium

### 指令

用户：「每个图片，你都应该从 google 上多下载几个，选取色彩、角度最好的，而且图片可以从 google 多信息源取，不是非要 wikipedia，肯定能找到效果好的图片，比如 Burj Khalifa，我问 chatgpt 他就给了我一堆图片。」
执行边界（代理判断）：
- 每张主图先从多个来源各取候选（全网图片搜索 Bing〔Google 图片需登录态与反爬，无 key 不可脚本化〕、Unsplash、Openverse〔Flickr 等 CC 聚合〕、Wikimedia Commons），每张至少 8 张候选，按色彩、角度（能看清全貌的标志性视角、适合竖版满版卡的构图）、清晰度与分辨率挑最好的；候选拼图交人看。
- 版权不放松为默认：每张候选记来源与许可分级（可商用 / CC 需署名 / 许可不明），许可不明的照样参与比较但标红，进成片须用户发布前签字（与 FoP 风险图同一套签字机制）。已向用户说明 Google 结果多为版权图、频道发布有版权警告风险。
- 先拿 #1 Burj Khalifa 做示范；另一个会话正在推进本系列，规则写进 bible.md §4 后两边按同一份执行，全量重选图待用户看过示范再推。

### 摘要

排行榜：主图改为多来源（全网搜索 / Unsplash / Openverse / Commons）每张多候选择优，许可分级标注；先以 Burj Khalifa 示范

---

## 006 — 2026-11-03 14:30:53 — ask-codex-for-image-sources

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
> severity: low

### 指令

用户：「还有你直接问 codex 和 gpt 他都能给你不少图片」。
执行边界（代理判断）：把 Codex CLI（ChatGPT 订阅，--search 联网）作为找图候选的又一来源：让它联网搜目标主体的高质量照片，返回直接图片链接、来源页与已知许可（JSON），下载后并入同一张候选拼图按同一标准择优；只用它找链接，不用它生成图片。调用经 tools/service_call.py 记请求日志（ChatGPT 订阅额度，费用未知）。先在 Burj Khalifa 上试，写进 bible.md §4 的候选来源清单。

### 摘要

排行榜找图来源加上 Codex 联网搜索（返回图片链接），先以 Burj Khalifa 试

---

## 008 — 2026-11-03 15:30:23 — waving-flags

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
> severity: low

### 指令

用户：「还有国旗能一直有飘飘的简单动画感吗」。执行边界（代理判断）：卡片上的国旗（左上角国旗与无图占位卡的大国旗）改为每帧单独绘制、持续轻轻飘动：竖条按正弦波错位（旗杆侧固定、越往外摆幅越大）、波峰亮波谷暗，各卡相位错开；角落计分板与封面上的小国旗保持静态（小尺寸飘动反而干扰阅读）。实现落在 rank_scroll（见其 follow-up 002），本系列 bible §2.4 记一句。

### 摘要

排行榜卡片国旗改为持续轻轻飘动

---

## 009 — 2026-11-03 19:16:50 — wiki-for-text-codex-for-images

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/_tools/image_reselect.py
> severity: high

### 指令

用户（重挑进行中，代理报告 Codex 在『只收可商用许可』条件下给的候选 95% 以上是维基共享资源、且维基下载被 429 限流后）：「流程应该改为 维基百科只出内容和文字，其余都是 codex search 出」。
执行边界（代理判断）：
- 维基百科 / Wikidata 只作数据与文字来源；主图一律由 Codex 联网搜索取得，排除维基共享资源，现用的维基图不再作候选（某项 Codex 一张也没找到时才临时沿用并在报告里列出）。
- Codex 不再限许可，但须照实写出来源页标注的许可：可商用许可（PD / CC0 / CC BY / CC BY-SA / Pexels / Unsplash / Pixabay）照常进成片；许可未知或不允许的标 image_risk = licence unknown，并入现有风险图机制——默认母版扣下，_with-risk-images 版放进去，由用户发布前签字（渲染器相应放宽：签字版不卡许可，见 rank_scroll follow-up 003）。
- 两期都按新流程重新搜、重挑、重渲；两期都出默认版与带风险图版，交付以带风险图版为主（体现找图效果），默认版并列。

### 摘要

排行榜：维基只出数据文字，图片全部 Codex 联网搜（排除维基），许可未知并入风险图签字机制；两期按新流程重做

---

## 007 — 2026-11-03 15:25:35 — reselect-all-images-rerender

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep01_tallest_buildings/data.json
>   - ai_videos/paihangbang/episodes/ep02_highest_peak_by_country/data.json
> severity: high

### 指令

用户看过 Burj Khalifa 的 Codex 候选后：「全部重挑，两个 video 都是，然后给我重新生成的成片」。
执行边界（代理判断）：
- 两期全部主图（含现为占位卡的）按 bible §4 新流程重挑：Codex 联网搜候选（每 5 项一包、每项 6 个，4 包并行）为主，旧图也参与比较；只收可商用许可（Public domain / CC0 / CC BY / CC BY-SA / Pexels / Unsplash / Pixabay），许可不明的不进；自动打分（分辨率、与卡片比例的契合、色彩、清晰度）选优，再新旧对照拼图人工过一遍。
- 被替换的旧图移到 _build/old_img/ 保留；换图的项清掉旧 image_focus 回到本期默认焦点；assets.json、image_credit、publish.md 署名同步。
- FoP 风险标记（image_risk）按国家原样保留，默认母版仍不放；ep01 另渲 _with-risk-images 版供对照。
- 配乐仍缺（Suno 卡在验证码），本次成片仍为静音。

### 摘要

排行榜两期 100 张主图按多来源流程全部重挑并重渲两期成片

---

## 019 — 2026-11-03 21:24:22 — ep06-manga-two-step-images

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep06_best_selling_manga
> severity: medium

### 指令

用户（ep06 漫画期进行中）：「请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
执行边界（代理判断）：
- 第一步只做内容：30 部作品的发行量、作者、出版社、连载年份、日文名等先定稿进 data.json / sources.md；第二步再按每部的内容（日文名、作者、出版社）让 Codex 联网搜图，每部多张候选（≥6），全部下载后按清晰度、分辨率、色彩、与卡片比例择优。
- 每张卡都必须有高质量主图：第一轮择优后长边不足或候选为零的作品，单独再让 Codex 补搜一轮（换来源：出版社官网、官方 X、英文版出版社、电商大图）；仍不达标才考虑 Codex 生成，且只生成不含原作角色与 logo 的主题插图（避免冒充官方封面与侵权），生成前在报告里列出。
- 封面均为版权作品，按 follow-up 014 标 image_risk；交付以带图版（_with-risk-images）为主片。
- 本期编号由 ep04 改为 ep06（与动物 ep04、病毒 ep05 按 follow-up 顺序协调）。

### 摘要

排行榜 ep06 漫画：先定内容再让 Codex 按内容多图搜索下载择优，两步走，确保每张卡都有高质量主图

---

## 026 — 2026-11-03 22:19:30 — claude-replaces-codex

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/ep06_best_selling_manga
> severity: medium

### 指令

用户（ep06 漫画期找图进行中）：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断）：
- 本系列（剧级，未经用户同意不升仓库级）里原来交给 Codex CLI 的工作——联网搜图返回直接图片链接、来源页与许可（bible §4、follow-up 006/009）——改由 Claude 自己做：主会话或子代理用 WebSearch / WebFetch 找图、核对来源页许可，下载、打分、拼图沿用 _tools/image_reselect.py 的 download / score / apply。不再调用 codex --search exec。
- 已由 Codex 返回、已下载的候选链接保留为普通候选参与择优（不是新的 Codex 调用）。
- Codex 内置出图也不再作为本系列的兜底；Claude 不能直接出图，某张卡确实找不到高质量真图时报给用户，不自动换其他收费出图服务。
- bible §4 同步改写；ep06 漫画期 Sazae-san 等补搜由 Claude 完成。

### 摘要

排行榜：原由 Codex 做的联网找图改由 Claude（WebSearch/WebFetch/子代理）自己做，bible §4 同步

---

## 013 — 2026-11-03 21:13:31 — ep04-deadliest-viruses

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_deadliest_viruses
>   - projects/rank_scroll
> severity: medium

### 指令

用户：「我们继续做我们的排名系列剧，这回我们做历史上杀死人类做多的前30病毒」，随后「开始你的research 和制作吧」。
执行边界（代理判断）：
- 新开 ep04（ep03 AI 公司由另一会话在做）；排名模式 Top 30，倒数到第 1 名。
- 只收病毒（鼠疫、结核、疟疾等细菌 / 寄生虫不收）；指标 = 有出处的历史累计死亡估计，口径与统计窗口写进 topic.md 与卡片，估算值标 est.，区间与争议写 sources.md。
- 病毒没有天然国家：默认不挂「首次发现国」国旗（易被读成甩锅、来源也有争议），计分板改按传播途径累计；需要的渲染器小改动按 rank_scroll follow-up 流程记录，且等另一会话的列表模式改完再动。
- 主图按 follow-up 009：Codex 联网搜（排除维基），优先 CDC PHIL / NIAID 等公有领域或 CC BY 电镜图；许可不明走 image_risk。
- 配乐仍按系列规则走 Suno，本次先出静音母版；独立审片另起上下文。

### 摘要

排行榜 ep04：历史上致死人数最多的 30 种病毒 Top 30（研究、数据、电镜主图、渲染、审片、发布稿）

---

## 016 — 2026-11-03 21:24:05 — ep05-virus-images-two-step

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep05_deadliest_viruses
> severity: medium

### 指令

用户（ep05 病毒期进行中）：「请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
执行边界（代理判断）：
- 第一步先把内容定稿（调研 → Top 30 名单、数值、出处写进 data.json / sources.md），第二步才按每张卡的内容（病毒名、科、形态、电镜类型）交给 Codex 联网搜并下载多张候选。
- 每张卡至少 3 张可用候选，出候选拼图择优；Codex 搜不到高质量可商用图的卡，用 Codex image_gen 生成科学插画式病毒结构图（不涉真人、品牌），账本标 AI 生成并在发布时勾合成内容声明。
- 目标：30 张卡全部有高质量主图，不留占位卡；许可不明的搜索图走 image_risk，但同时备好可商用或生成的替代图，保证默认母版也每张有图。

### 摘要

ep05 病毒期主图分两步：先定内容，再按内容让 Codex 搜索下载 / 生成多张候选，30 张卡都要有高质量图

---

## 024 — 2026-11-03 22:18:30 — claude-replaces-codex

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep05_deadliest_viruses
>   - ai_videos/paihangbang/bible.md
> severity: medium

### 指令

用户（ep05 第二步找图进行中）：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断）：
- 范围先按剧级（本排行榜系列）理解：联网搜图、取来源与许可、下载候选，都由 Claude 自己做（WebSearch / WebFetch / 子代理），不再调用 codex exec。升为仓库级（其他剧、codex-imagegen 出图入口）须用户明确同意，已在回复里问。
- 已在跑的 Codex 第二轮当场停掉（29 包里 23 包已返回、已计入 request_log，结果照用，不补跑剩下 6 包），剩下的由 Claude 搜。
- Claude 不能直接出位图：原来要 Codex image_gen 生成的插画，改为 Claude 自己用代码做科学插画（Blender 建模渲染或程序化绘制），账本记 Claude 制作；做不到的情况再报给用户。

### 摘要

排行榜系列：原 Codex 承担的联网搜图 / 下载 / 生成全部改由 Claude 自己做（剧级；仓库级待用户确认）

---

## 034 — 2026-11-03 23:18:53 — images-web-first-codex-final-music-preview

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep05_deadliest_viruses
> severity: medium

### 指令

用户（ep05 收尾中）：「图片请先尝试google或者互联网下载，看能不能找到合适的high quality 图片，如果实在不行，就把最后出图的一步交给codex，其余都是claude来做」；随后：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐，最后给我一个类似于dota preview的页面link给我，我好review」。
执行边界（代理判断）：
- 修正 follow-up 024：搜图、下载、挑图、写 prompt 都由 Claude 做；只有「生成图片」这一步交给 Codex（tools/codex_image.py，先记 request_log）。
- ep05 现有 7 张 Claude 依 PDB 坐标的结构渲染图：先逐张再上网找高清可商用实拍或插画；找不到的改由 Codex image_gen 出图，以 PDB 渲染图为科学参考，账本标 AI-generated。
- 收尾：独立审片意见逐条处理并复审；Suno 按系列规则配乐（先记 request_log，验证码 / 需人点时停下请用户点）；做一个与 dota 预览页同类的 review 页面，给出链接。

### 摘要

ep05：图片先上网找高清图，找不到才让 Codex 出图（其余 Claude 做）；收尾自审、Suno 配乐、给 dota 式预览页链接

---

## 012 — 2026-11-03 21:13:17 — ep04-largest-land-animals

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: medium

### 指令

用户：「我们继续做我们的排名系列，世界上最大的前30陆地动物。」随后：「开始你的reserach 和制作吧」。
执行边界（代理判断，写进 topic.md 待用户点头）：
- 新开 ep04（排名期，Top 30）；按物种（IUCN 分类）排，只收现存野生物种，不收家畜家禽；不收海兽与鳄类（主要在水中捕食），河马、北极熊照常收，口径在片头与描述框写明。
- 主值 = 成年雄性典型体重（kg，副显示 lb），出处为 IUCN、同行评审文献、ADW/Mammalian Species 等，维基百科只作交叉核对；最大记录体重、野外数量作小字标签，受威胁等级作徽章。
- 国旗 = 该物种野外数量最多的国家（有出处），计分板按大洲。
- 图片按 bible §4 由 Codex 联网搜野生个体照片，逐张核对物种不认错；配乐按系列走 Suno、生成由用户点，本次先出静音母版。

### 摘要

排行榜 ep04：世界最大陆地动物 Top 30（雄性典型体重，国旗=野外数量最多的国家），调研、找图、渲染静音母版

---

## 018 — 2026-11-03 21:24:13 — ep04-content-first-then-images

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: medium

### 指令

用户：「请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
执行边界（代理判断，本期 ep04 执行；是否写进 bible §4 作全系列规则待用户定，其他期由各自会话负责）：
- 第一步只做内容：物种数据、出处、每张卡要表现的特征（成年雄性、野外个体、辨认要点、易混的家养型或近缘种）落盘到 data.json / sources.md，定稿后才开始找图。
- 第二步按内容找图：每张卡把第一步写好的辨认要点写进 image_hint，交 Codex 联网搜（_tools/image_reselect.py），每张卡取多张候选并下载，出候选拼图，逐张看图核对物种和画质后挑选。
- 每张卡都必须有高质量图：没有合格真实照片的卡（分辨率不足、物种认不准、只有圈养或模糊图），用 Codex image_gen（tools/codex_image.py，先记请求日志）以最好的真实照片作参考，生成写实野生动物照片，在 assets.json 标 AI 生成、发布时勾选 YouTube 合成内容声明；不留占位卡。

### 摘要

排行榜 ep04：先定内容再找图，两步走；Codex 按内容联网搜多张候选，找不到合格照片就用 Codex 生成，保证每张卡都有高质量图

---

## 022 — 2026-11-03 22:18:22 — claude-replaces-codex

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: high

### 指令

用户：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断；先按剧级 paihangbang 记录，是否升仓库级待用户明确）：
- 找图研究、候选下载、物种 / 主体核对都由 Claude 自己做（WebSearch / WebFetch，加免 key 的开放接口如 iNaturalist API、Openverse），不再调用 codex --search exec。
- Claude 不能生成图片，所以原「找不到合格照片就用 Codex 生成」改为：继续由 Claude 找可商用的真实照片（iNaturalist 野外研究级观测的 CC0 / CC BY / CC BY-SA 照片优先）；仍找不到的，报告用户另定，不调用 Codex 出图。
- ep04 已用 Codex 跑过两轮联网找图（已记请求日志），结果保留作候选；后续补图全部由 Claude 完成。bible §4 与 _tools 里 Codex 路线的改写待用户确认后再动（其他期会话可能仍在用）。

### 摘要

排行榜：原由 Codex 做的找图、下载、核对改由 Claude 自己做；Claude 不能出图，找不到可商用照片时报告用户，不再用 Codex 生成

---

## 030 — 2026-11-03 23:04:33 — ep04-commons-exception

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: low

### 指令

用户（回答代理提问）：ep04 爪哇犀（#7）与野牦牛（#11）两张卡「Allow Commons for these 2」。
执行边界：只对这两张卡破例 follow-up 009，允许维基共享资源里 PD / CC0 / CC BY / CC BY-SA 的照片；Claude 用 Commons API 检索、逐张看图核对物种（野牦牛须是 Bos mutus 野生个体，不要家牦牛），账本照记作者与许可；其余 28 张不变。

### 摘要

排行榜 ep04：仅爪哇犀、野牦牛两张卡破例允许维基共享资源可商用照片

---

## 020 — 2026-11-03 21:24:49 — two-step-image-every-tile

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes
> severity: high

### 指令

用户（ep11–ep20 并行制作刚启动时）：「请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
执行边界（代理判断）：
- 找图分两步：① 先为每个条目抓取内容落盘（是什么、在哪、长相与标志性视角、易混对象），只用网页检索；② 再把内容浓缩成每项 image_hint 交 Codex 联网研究找多张候选，下载后逐张看图挑选。
- 每张卡都要有高质量图，默认母版不再出现占位卡：可用候选 < 3 或质量不够的项单独再搜一轮；最佳图是风险图时风险版用它、默认版另找可商用替代；两轮都没有就用 Codex 生成（tools/codex_image.py，先记日志；不生成真人、logo；账本记 AI-generated，发布时勾选合成内容声明）。
- 写进 bible §4 作为本系列规则（剧级）；已在跑的 8 个代理发消息补要求，未启动的 ep19、ep20 按新说明启动。

### 摘要

排行榜找图改为先抓内容、再据内容让 Codex 找多图两步走，每张卡必须有高质量图（找不到就 Codex 生成）

---

## 023 — 2026-11-03 22:18:26 — claude-replaces-codex

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/_tools/image_reselect.py
>   - ai_videos/paihangbang/episodes
> severity: high

### 指令

用户（ep11–ep20 并行制作中）：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断）：
- 本系列不再调用 Codex：联网找图候选改由 Claude 代理用 WebSearch / WebFetch 自己做，结果写 _build/reselect/claude_*.json（与原 Codex 输出同一 schema），image_reselect.py 的 download 同时读这类文件；search 子命令停用。已拿到的 Codex 结果保留可用，不补造日志。
- 生成图（原 follow-up 020 的最后手段 Codex image_gen）：Claude 不能出图，暂停；两轮搜索仍无可用图的项由子代理列出，主代理汇总后问用户（可选 ElevenLabs 出图或接受占位）。
- 写进 bible §4；正在跑的 10 个代理发消息改流程。

### 摘要

排行榜：原由 Codex 做的找图全部改为 Claude 自己用网页检索做；生成图暂停待定

---

## 028 — 2026-11-03 22:45:40 — google-fallback-images

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes
> severity: medium

### 指令

用户（回答「自己搜两轮仍无可用图怎么办」）：「找不到可以reserach google下载」。
执行边界（代理判断）：
- 生成图不再作兜底；兜底改为放开来源的全网检索（WebSearch / WebFetch 取页面主图，或 Bing 图片结果原图链接），下载后人工看图认对对象。
- 这类图许可多为未知：照实记账本，标 image_risk = licence unknown，进 _with-risk-images 版（用户发布前签字）；默认版有可商用替代就用 image_alt，没有就占位。目标是风险版每张卡都有高质量图。
- 极少数仍找不到的，由主代理用浏览器打开 Google 图片补找。

### 摘要

排行榜找图兜底：找不到就全网（Google 思路）检索下载，许可不明的进风险版

---

## 029 — 2026-11-03 22:45:57 — codex-generate-last-resort

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes
> severity: medium

### 指令

用户（紧接 follow-up 028）：「实在找不到，只把生成图片这一步给codex好了」。
执行边界（代理判断）：找图顺序为可商用许可图（Claude 自己搜）→ 放开来源全网检索（许可不明进风险版）→ 仍无合格图才用 Codex 生成（tools/codex_image.py，先记日志）。Codex 只做出图，不做搜索调研。生成图不冒充真实照片、不生成真人和 logo，账本记 AI-generated (Codex image_gen)，上传勾选合成内容声明；生成图默认版也显示。

### 摘要

排行榜找图最终兜底：实在找不到才让 Codex 只做生成图片这一步

---

## 031 — 2026-11-03 23:16:38 — internet-first-quality-images

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes
> severity: medium

### 指令

用户：「图片请先尝试google或者互联网下载，看能不能找到合适的high quality 图片，如果实在不行，就把最后出图的一步交给codex，其余都是claude来做」。
执行边界（代理判断）：取代 028/029 的先后顺序——第一轮即全网（Google / 互联网）找最高质量的真实照片，不先限定免费图库；同等好时优先可商用许可。许可照实记：许可不明的标 image_risk 进风险版，尽量另配可商用 image_alt 给默认版。全网都找不到合格图才由 Codex 出图（tools/codex_image.py）；其余调研、搜索、下载、挑选、核对全部由 Claude 做。

### 摘要

排行榜找图：先全网（Google）找高质量图，实在不行才让 Codex 出图，其余全由 Claude 做

---

## 015 — 2026-11-03 21:21:25 — ten-episodes-ep11-ep20

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes
>   - projects/rank_scroll/rank_scroll/theme.py
> severity: high

### 指令

用户：「我们继续我们的排名系列据，请research 前十名你觉的观众想看的排名topic，然后分别10个并行的agent去deep research还有制作，然后我要看到10个完整的成片」。
执行边界（代理判断）：
- 选题：用 YouTube 同题实测播放（30 个候选，yt-dlp 每题前 15 条的中位数 / 最高播放，存 _build 外的 0_research/data/yt_demand_2026-11-03.json）加 bible 打分（国家维度、素材风险、数据开放、广告友好）选 10 个；避开已做或其他会话在做的选题（ep01 建筑、ep02 山峰、ep03 AI 公司、ep04 陆地动物 / 病毒 / 漫画），也避开人物肖像类。
- 编号预留 ep11–ep20（ep04 已有三个会话撞号，ep05–ep10 留给其他会话），开工前通知并行会话。
- 每期一个并行子代理，按 bible §6 ①–⑤ 全流程：topic.md、data.json + sources.md（维基只出数据文字，主值找一手来源交叉核对）、Codex 联网找图（经 RequestLog 记日志）、洞察卡、渲染默认母版与 _with-risk-images 版、封面、publish.md。N 按题材 30–50。
- 10 个新主题皮肤由主代理一次性加进 rank_scroll/theme.py，子代理不改渲染器，避免并发写冲突；渲染器缺能力就报告。
- 审片（⑥）由主代理另起独立上下文的审片代理做，不让作者自审。
- 配乐：Suno 不在 10 个子代理里并发调用；母版先出静音，配乐由主代理在母版完成后集中处理（照常先写 request_log.md）。

### 摘要

排行榜 ep11–ep20：按 YouTube 实测需求选 10 个题，10 个并行代理各自调研并做出成片

---

## 010 — 2026-11-03 20:55:24 — ep03-ai-companies-list

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep03_ai_companies
>   - projects/rank_scroll
> severity: high

### 指令

用户：「我们继续来做排名系列剧集，这次做ai公司，不管是大语言，还是视频，还是声音，还是其他，帮我所deep research，30家知名公司，下载他们的log还有公司照片以及创始人大头照做reference，然后我们做一个视频这次不用排名，只是一个一个list就好」。
用户随后选定（2026-11-03 提问）：范围 = AI 原生公司为主（Google DeepMind 作为独立实验室可算，不收 NVIDIA / 微软 / Meta 等大厂本体）；出场顺序 = 按成立年份从老到新；卡上主数字 = 最新估值（标出处与日期）+ 成立年，小字放总部、代表产品。
执行边界（代理判断）：
- 新开 ep03（系列第 3 期，不排名的列表期）；Wikipedia / Wikidata 只作数据与文字来源，估值等以公司公告 / 主流财经媒体为准并交叉核对。
- 每家下载三类参考图：logo、公司照片（办公室 / 总部 / 产品场景）、创始人头像，存 ep03 assets/ref/，账本记来源与许可；许可不明的按既有 image_risk 机制默认不进成片、由用户发布前签字。不生成真人或 logo。
- 渲染器 rank_scroll 增加「列表模式」（不显示名次、不倒数）与公司卡（照片满版 + logo + 创始人圆形头像）；改动按 rank_scroll 项目 follow-up 流程记录。
- 配乐仍按系列规则走 Suno，生成由用户点；本次先出静音母版。

### 摘要

排行榜 ep03：30 家 AI 原生公司按成立年份列表（不排名），深度调研并下载 logo / 公司照片 / 创始人头像作参考，出列表模式视频

---

## 017 — 2026-11-03 21:24:08 — ep03-content-first-images

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep03_ai_companies
>   - ai_videos/paihangbang/bible.md
> severity: high

### 指令

用户（ep03 第一轮找图与调研并行跑完后）：「请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
执行边界（代理判断）：
- 第一步：每家公司的事实内容（产品、总部、近况、创始人、估值）先调研落盘；第二步：用这些内容写进 Codex 搜图提示（代表产品、总部楼、发布会、机器人等具体画面），每张卡每类取多张候选并下载。
- 质量闸门：照片长边 ≥ 1600 px、头像 ≥ 600 px 且脸清楚、logo 为官方矢量或大图；不合格不算有图。
- 真实照片找不到合格的卡，用 Codex 生成配图（只生成场景 / 产品氛围插图，不生成真人、不生成 logo 或品牌产品外观，卡上署名标 AI-generated illustration，上传时勾选合成内容声明）。创始人头像不生成，找不到合格的用姓名首字母圆章。
- 第一轮不看内容的候选保留作对比，不删除。

### 摘要

ep03 找图改为两步：先落盘内容调研，再按内容让 Codex 搜/下多张候选（不足时生成配图），每张卡都要过高质量闸门

---

## 025 — 2026-11-03 22:18:36 — claude-replaces-codex

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/ep03_ai_companies/_build/ref_images.py
>   - ai_videos/paihangbang/_tools/image_reselect.py
> severity: high

### 指令

用户（ep03 找图、出片进行中）：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断）：
- 范围先定在本系列（剧级，AGENTS「拿不准一律先放剧级」）；是否升仓库级（codex-imagegen skill、各剧出图默认顺序、tools/qc_review.py 默认换模型）须用户明确同意，已在回复中询问。
- 联网搜图 / 找资料：由 Claude 子代理用 WebSearch / WebFetch 完成，输出与原 Codex 结果同一 JSON 结构（items[].images[]），下载、质量闸门、拼图、组装脚本不变；不再调用 codex --search。Claude 会话自带的搜索不是收费外部服务，不写 request_log；下载仍照常留在 assets/ref 的 meta.json。
- 生成配图：Claude 没有位图生成能力；以后需要配图时改用代码绘制（skia / SVG 风格化插图）或继续找真实照片，不再调 Codex image_gen。ep03 已用 Codex 生成的 Midjourney 配图（follow-up 017）是历史产物，保留并照实记录，是否替换由用户定。
- 独立审片 / 审稿：用 Claude 独立上下文的子代理，不用 Codex。
- 已经跑完的 Codex 请求不补造、不重跑；日志照旧保留。

### 摘要

排行榜系列：原交给 Codex 的搜图、找资料、审片改由 Claude 子代理完成；Claude 无位图生成能力，配图改代码绘制或真实照片

---

## 032 — 2026-11-03 23:16:40 — images-claude-search-codex-gen-only

> target_stage: 3
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/ep03_ai_companies
> severity: high

### 指令

用户（紧接 follow-up 023/025「Codex 的事全部由 Claude 做」之后的澄清）：「图片请先尝试google或者互联网下载，看能不能找到合适的high quality 图片，如果实在不行，就把最后出图的一步交给codex，其余都是claude来做」。
执行边界（代理判断）：
- 找图顺序：Claude（子代理）先用网页搜索 / 打开网页找并下载高质量真实图片，多轮补搜、看图挑选、质量闸门都由 Claude 做。
- 只有「实在找不到合适的高质量真实图」时，最后的生成配图这一步交给 Codex（tools/codex_image.py，先记 request_log；不生成真人和 logo；账本记 AI-generated，上传时勾选合成内容声明）；prompt 由 Claude 写。
- 取代 follow-up 023 里「生成图暂停」一句；023 / 025 的其余部分（Codex 不再做搜索、资料、审片）不变。
- ep03：Midjourney 卡的 Codex 生成图符合本规则（真实照片只有 2013 年 Leap Motion 时期与 ISEF 活动照），保留；其余卡继续由 Claude 找可商用替代图。

### 摘要

排行榜找图：Claude 先上网找并下载高质量图，实在不行才把最后的生成一步交给 Codex，其余全部 Claude 做

---

## 014 — 2026-11-03 21:13:47 — ep04-best-selling-manga

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_best_selling_manga
> severity: high

### 指令

用户：「我们继续我们的排名系列据，到今天为止销量最高的前30 日本动漫排名，开始你的research和制作吧」。
执行边界（代理判断，未提问，用户要求直接开工）：
- 新开 ep04（ep03 AI 公司由另一会话进行中，不动它的文件与渲染器改动）。
- 「销量」取漫画系列累计发行量（copies in circulation，出版社 / 主流媒体公布的最新数字，含海外与电子版按公布口径），Top 30 排名；动画本身无统一销量口径，不混入。Wikipedia 只作数据与文字来源和交叉核对，主值优先出版社公告。
- 全部是日本作品，国家计分板改为按出版社计（复用 continent 字段，标签写出版社），国旗统一日本。
- 主图按 bible §4（follow-up 009）由 Codex 联网搜索：首卷封面或官方主视觉。均为版权作品，统一标 image_risk = copyrighted artwork：默认母版扣下，_with-risk-images 版放入，由用户发布前决定。不生成角色图。
- 配乐按系列规则走 Suno（生成由用户点），先出静音母版；审片另起上下文。

### 摘要

排行榜 ep04：日本漫画累计发行量 Top 30（截至 2026-11），调研、找图、渲染、独立审片、发布草稿

---

## 038 — 2026-11-03 23:55:16 — ep05-overnight-autonomous

> target_stage: 1
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep05_deadliest_viruses
> severity: medium

### 指令

用户（ep05 收尾中，2026-11-03 深夜）：「接下来我要睡觉了，你需要尽可能多的完成之后你能想到的步骤，不要问我问题，遇到不确定的就自己make best effort decision，即使碰到删除文件这种high risk decision,你也自己make 就好，不要来问我，我要睡觉去了。」
执行边界（代理判断）：
- 本授权只覆盖 ep05 收尾（以及为它所需的 Suno 服务恢复）：第 2 轮独立审片与修复、Suno 配乐（服务卡住时按服务 README 自行重启 / 开窗口，验证码仍不代解、不绕过）、带配乐重渲、预览页核对、publish.md、follow-up 收尾。
- 不碰别的剧 / 别的会话的产物；删除只限 ep05 自己的中间文件。所有自主决定写进 topic.md / qc.md / 本条收尾记录，供用户醒来复核。
- 生成永远人点等仓库硬规则不因本授权放宽：上传 YouTube 仍由用户亲手做。

### 摘要

ep05 夜间自主收尾：不提问、自行决策（含删除中间文件），完成审片、配乐、重渲、预览页

---

## 035 — 2026-11-03 23:22:56 — ep04-review-music-preview

> target_stage: 7
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: medium

### 指令

用户：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐，最后给我一个类似于dota preview的页面link给我，我好review」。
执行边界（代理判断）：
- 审查：成片与数据按 bible §7 清单做独立审片（另起上下文，不由作者自审冒充），结论与问题写 ep04 qc.md；能修的当场修、重渲。
- 配乐：按系列规则走本机 Suno（先写 request_log、固定幂等键，验证码 / 需登录就停下报告，不绕过、不换引擎），每期独有纯音乐，--music 重渲默认版与带风险图版。
- 预览页：管理应用（127.0.0.1:5174）新增排行榜单期预览页（类似 Dota 英雄预览页：成片播放、逐卡图片 / 数值 / 出处 / 许可 / 风险标记、审片结论），交片只给这一个链接；管理应用改动按该项目 follow-up 流程另记。

### 摘要

排行榜 ep04：独立审片、Suno 配乐重渲，并在管理应用新增排行榜单期预览页供用户审阅

---

## 039 — 2026-11-03 23:55:45 — ep04-overnight-autonomous

> target_stage: 7
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: medium

### 指令

用户（ep04 审片修改进行中）：「接下来我要睡觉了，你需要尽可能多的完成之后你能想到的步骤，不要问我问题，遇到不确定的就自己make best effort decision，即使碰到删除文件这种high risk decision,你也自己make 就好」。
执行边界（代理判断）：AUTONOMOUS 推进 ep04 剩余步骤——按独立审片意见修数据与图片、Suno 配乐（验证码 / 需登录时不绕过，记录阻塞，先出静音母版）、重渲默认版与带风险图版、复审、发布稿、预览页链接；判断写进 ep04 qc.md / topic.md；不提问。

### 摘要

排行榜 ep04：用户授权夜间自主推进剩余步骤，不提问、自行决策（含删除）

---

## 036 — 2026-11-03 23:23:13 — ep03-review-music-preview

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep03_ai_companies
> severity: medium

### 指令

用户：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐，最后给我一个类似于dota preview的页面link给我，我好review」。
执行边界（代理判断）：
- review：另起独立上下文（Claude 子代理）按 bible §7 审片清单审 ep03 两个母版与数据，结论写 qc.md；作者自查另记，不冒充独立审片。
- 配乐：按系列规则走本机 Suno 服务（suno skill；先写 request_log；生成由用户在 Suno 网页点或服务允许时提交，遇验证码不绕过），一首 4–5 分钟纯音乐，渲染时混入。
- 预览页：管理应用新增排行榜单期预览页 /rank-preview?path=<集目录>（参照 dota 英雄预览页），交片只给这一个链接。

### 摘要

ep03 完成后独立审查、Suno 配乐，并在管理应用做单期预览页交审

---

## 037 — 2026-11-03 23:53:57 — ep03-autonomous-overnight

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep03_ai_companies
> severity: medium

### 指令

用户（2026-11-03 夜）：「接下来我要睡觉了，你需要尽可能多的完成之后你能想到的步骤，不要问我问题，遇到不确定的就自己make best effort decision，即使碰到删除文件这种high risk decision,你也自己make 就好，不要来问我，我要睡觉去了。」
执行边界（代理判断）：AUTONOMOUS——不提问，把 ep03 剩余步骤（可商用替代图、重建数据、独立审片与修复、Suno 配乐（遇页面故障 / 验证码不绕过，只重试同一任务）、母版重渲、publish.md、预览页链接、follow-up 收尾）尽量做完；每个判断写进对应 follow-up 与 topic.md / qc.md。删除只限本期 _build 中间产物与被替换的图（旧图移到 _build/old_img/ 保留），不删别的会话或用户的文件；生成仍守「不生成真人和 logo」与收费服务日志规则。

### 摘要

ep03 夜间自主推进：不提问，按最佳判断做完剩余步骤并记录依据

---

## 011 — 2026-11-03 20:55:52 — add-suno-bgm

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep01_tallest_buildings/render
>   - ai_videos/paihangbang/episodes/ep02_highest_peak_by_country/render
> severity: medium

### 指令

用户（Suno 服务修好后）：「suno好了，我们有一版新的最高楼排名，请帮我的视频加上音乐」。
执行边界（代理判断）：
- 先对三个 uncertain 旧任务（ep01 5823cd40、ep02 105977e5 / ed28881e）做 recollect 按标题回库认领，库里没有才新建；新建沿用原 prompt（ep01 skyline 电子、ep02 alpine 管弦），每期一个任务两首，按 bible 用 --music 两首交叉淡入接满全片。
- 画面用另一会话（follow-up 007/009）刚重挑图后的当前 data.json，不改数据与图片；ep02 等另一会话的渲染结束再动。默认母版与 _with-risk-images 版都加音乐。
- 加完音乐做独立音频审片（fresh context），结果记 qc.md。

### 摘要

排行榜两期用 Suno 生成背景音乐并重渲带配乐成片

---

## 021 — 2026-11-03 21:25:03 — content-first-image-pipeline

> target_artifacts:
>   - ai_videos/paihangbang/_tools/image_pipeline.py
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/ep01_tallest_buildings/data.json
>   - ai_videos/paihangbang/episodes/ep02_highest_peak_by_country/data.json
> severity: high

### 指令

用户（看过配乐版后）：「图片有很多缺失和质量不好，请确保你是先下载到内容，然后根据内容让codex research和帮你下载或生成多张图片，要分两步走，确保每一个tile都有高质量图片才行」。
现状（代理盘点）：两期默认母版各 22 张卡因许可不明 / FoP 被扣成占位卡；ep01 8 张、ep02 10 张短边 < 1000 px；上一轮 Codex 只按名字搜，没核对主体对不对。
执行边界（代理判断）：
- 第一步「内容」：每张卡先下载内容资料——维基百科 / Wikidata 正文摘要、外观与位置描述、坐标，外加 1 张维基首图只作「认主体」参照（不进成片），落盘 `_build/content/<key>/`；据此写每张卡的视觉简报（长什么样、标志性视角、易混淆对象）。
- 第二步「图片」：按视觉简报让 Codex 联网研究，每卡至少 6 张候选，由 Codex 自己下载到候选目录并写来源 / 作者 / 许可；只要真实照片，核对主体与简报一致；之后按分辨率（裁成卡片后不放大）、色彩、角度打分并人工过拼图。找不到合格真实照片的卡用 Codex 出图（tools/codex_image.py）生成写实插图，标「AI illustration」并在发布时勾合成内容声明。
- 验收：100 张卡每张都有图、主体正确、裁到卡片后不需放大（短边达标），新旧对照拼图交独立审核。许可不明 / FoP 仍按 image_risk 记录，交付以全图版为主（follow-up 009 已定），默认版并列。
- 换完图重渲两期配乐版，同时按音频审片意见修渲染器配乐（衔接点 / 两遍 loudnorm，见 follow-up 011）。

### 摘要

排行榜找图改两步：先下载每张卡的内容资料，再据内容让 Codex 研究并下载多张候选（不行就生成），确保 100 张卡全部有高质量正确主体图

---

## 027 — 2026-11-03 22:19:31 — claude-replaces-codex

> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/_tools/tile_images.py
> severity: medium

### 指令

用户（ep01/ep02 两步找图进行中）：「以前需要codex做的事情，现在全部有claude 模型自己来处理」。
执行边界（代理判断，先放剧级）：
- 本系列找图的第二步（读内容 → 视觉简报 → 联网找真实照片 → 下载 → 逐张核对主体 → 写 candidates.json）改由 Claude 子代理用 WebSearch / WebFetch / curl 完成，产物格式不变，打分、拼图、应用沿用 tile_images.py。
- 已由 Codex 完成的卡（ep01 13 张、ep02 11 张）结果保留，未完成的卡清空后交 Claude；本会话的 Codex 进程已停，其他会话的不动。
- 出图兜底：Claude 不能生成位图，找不到合格真实照片的卡先如实报告，不自动改走其他出图服务，由用户决定。
- bible §4 找图来源改写；是否升为仓库级（codex-imagegen 等共用 skill）须用户明确同意，本次不动。

### 摘要

排行榜：原先交给 Codex 的找图研究与下载改由 Claude 模型（子代理）自己完成

---

## 033 — 2026-11-03 23:16:42 — internet-first-codex-only-generate

> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/_tools/tile_research_brief.md
> severity: medium

### 指令

用户（follow-up 027 之后补充）：「图片请先尝试google或者互联网下载，看能不能找到合适的high quality 图片，如果实在不行，就把最后出图的一步交给codex，其余都是claude来做」。
执行边界（代理判断，剧级）：
- 研究、下载、核对、打分、选图、换图全部由 Claude 做；来源不限图库，Google、Bing、Flickr、新闻媒体、官网、摄影师站都可以，许可照实写，许可不明的走 image_risk 签字机制（维基共享资源仍按 009 排除）。
- 只有确认没有合格真实照片（主体正确、裁成卡片后短边 ≥ 1000 px）的卡，才由 Codex 出写实图（`tools/codex_image.py`，经 tile_images.py generate，先记请求日志），卡上署名 AI illustration，上传时勾合成内容声明。
- 取代 027 中「出图交用户决定」一条。

### 摘要

排行榜找图：先由 Claude 在 Google / 全网找高质量真实照片，实在找不到才把最后的出图交给 Codex

---

## 040 — 2026-11-04 04:47:07 — qc5-fixes-tiles-music

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep01_tallest_buildings/data.json
>   - ai_videos/paihangbang/episodes/ep02_highest_peak_by_country/data.json
> severity: medium

### 指令

用户：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐，最后给我一个类似于dota preview的页面link给我，我好review」。第 5 轮 fresh-context 审片两期都判「修后可发布」，代理按发现逐条修：ep01 换 #3/#7/#8/#15/#19/#28/#29/#31/#49；ep02 换 #4/#6/#7/#17/#26、重出 #18/#50 AI 图、洞察 after_rank 41→43；AI 卡署名改 Illustration: AI-generated, not a photo；配乐重排（ep01 两首对调、ep02 改入点）。风险图签字仍由用户决定，不在本条。

### 摘要

按第 5 轮独立审片修两期：楼顶/峰顶被国旗挡住的卡换图或调焦点，重出两张 AI 图，AI 署名去掉 Photo，配乐重排对准 #1 高潮

---

## 041 — 2026-11-04 06:25:15 — ep11-20-review-music-preview

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes
>   - ai_videos/paihangbang/README.md
> severity: medium

### 指令

用户：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐，最后给我一个类似于dota preview的页面link给我，我好review」；随后「接下来我要睡觉了，你需要尽可能多的完成之后你能想到的步骤，不要问我问题……即使碰到删除文件这种high risk decision,你也自己make」。
执行边界（代理判断）：每期独立审片（fresh context）→ 制作代理返修 → 独立复核，直到 blocker 清零；过时风险版移入 render/_stale/（不删除）；Suno 因账号下载额度用完暂停，用另一会话已下载的曲子经 add_music.py 只换音轨，静音版备份 render/_silent/；审片页用管理应用 /rank-preview（ai_video_management follow-up 320）；不购买额度、不绕过暂停。

### 摘要

排行榜 ep11–ep20：独立审片与复核清零 blocker、7 期补 Suno 配乐、审片页链接

---

## 044 — 2026-11-04 08:57:11 — ep03-suno-second-track

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep03_ai_companies/render
> severity: low

### 指令

try again（重试下载 ep03 第二首 Suno 配乐）

### 摘要

ep03 第二首 Suno 配乐取回，两版母版用两首重渲

---

## 042 — 2026-11-04 08:51:37 — ep04-suno-music-final

> target_stage: 7
> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep04_largest_land_animals
> severity: medium

### 指令

用户：「suno is good now」（Suno 下载额度恢复、暂停解除）。执行边界（代理判断）：取 ep04 已完成的 v2 任务 101bce70 两首曲，用 _build/add_music.py 给默认版与风险图版补音轨（不重渲画面），加 music_credit、重出发布稿，删临时配乐审片版，独立音频复核，更新交接与预览。

### 摘要

排行榜 ep04：Suno 恢复后补正式配乐、删临时版、音频复核

---

## 043 — 2026-11-04 08:54:38 — music-retry-ep11-13-14-20

> target_artifacts:
>   - ai_videos/paihangbang/episodes
> severity: medium

### 指令

try again（重试为 ep11/ep13/ep14/ep20 配 Suno 音乐）

### 摘要

账号额度已恢复（Downloads 60）后按服务自带 clear_automation_pause 解除下载额度暂停并存档记录；ep14 v2 补下载，ep20 v2 排队出歌，ep11/ep13 v2 库内认领无歌后新建 v3；四期用 add_music.py 只换音轨（-16 LUFS，帧数不变，静音版备份 render/_silent/）；同时发现 ep11–ep20 各期 publish.md 漏了 Suno 配乐署名与 Content ID 清单项，已补。

---

## 045 — 2026-11-04 09:24:11 — ep06-suno-music-v3

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep06_best_selling_manga
> severity: low

### 指令

try again, suno is good now（ep06 配乐：Suno 恢复后重做）

### 摘要

ep06 配乐重做：Suno 新任务只用一首约 155 BPM 的曲子，在曲内按拍对齐跳回、中段重复 28 小节补足 3:37，替换原来两首不同 BPM 硬接的底轨；两版成片重渲，独立音频审片。

---

## 049 — 2026-11-04 21:17:05 — release-folder-preview

> target_artifacts:
>   - ai_videos/paihangbang/_tools/release.py

### 指令

所有排行榜下面的video，正式版本英文和中文promote到单独的一个folder，全部混在render下面不好找；每一个都需要一个preview page，可以preview这些video以及重要的信息

### 摘要

新增 _tools/release.py：稳妥版英中视频与封面硬链接进 release/<期>/，生成总览与单期预览页（播放器、发布稿复制、审片、待定），--check 报不同步

---

## 050 — 2026-11-04 21:56:22 — douyin-collection-cover

> target_artifacts:
>   - ai_videos/paihangbang/_tools/collection_cover.py

### 指令

帮我做几张合集封面照片，我选一张

### 摘要

抖音合集「全球之最排行榜」封面 4 款候选（3:4），免署名实拍图 + Noto Sans SC

---

## 051 — 2026-11-04 22:29:06 — zh-cover-candidates

> target_artifacts:
>   - ai_videos/paihangbang/_tools/zh_covers.py

### 指令

帮我给每一个视频做三张封面，到时候我选择一张，三张中文封面

### 摘要

新增 _tools/zh_covers.py：每期三张中文封面候选（冠军大图 / 柱状对比 / 悬念大字），接进 release 预览页与 covers_zh.html 挑选页

---

## 052 — 2026-11-04 22:55:22 — zh-cover-4x3-3x4

> target_artifacts:
>   - ai_videos/paihangbang/_tools/zh_covers.py

### 指令

帮我做三张横屏4：3 的封面和三张竖屏3：4的封面

### 摘要

zh_covers.py 增加 4:3（1440×1080）与 3:4（1080×1440）两种尺寸，每期各三款；竖屏柱状改横向照片条、悬念款改上下排版；挑选页按尺寸分 tab

---

## 053 — 2026-11-05 22:18:43 — auto-upload

> severity: medium

### 指令

YouTube 与抖音上传自动化：YouTube 走官方 Data API v3，从 release/<期> 与 publish.md 读标题、描述、标签、合成内容声明、封面，上传为私享（公开由用户在 Studio 亲手点），评论在公开后由脚本发出、置顶仍手动；抖音无可用官方接口，用本机 Chrome（Playwright 持久登录）自动打开上传页、传片、填标题描述话题、封面与 AI 声明，最后「发布」由用户亲手点。上传记录逐期落盘，结果未知不自动重传。

### 摘要

新增 YouTube API 上传（私享）与抖音自动填表（人点发布）

---

## 054 — 2026-11-05 22:50:13 — tile-image-hard-gate

> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/_tools/tile_gate.py
>   - ai_videos/paihangbang/_tools/release.py
>   - ai_videos/paihangbang/_tools/upload.py
> severity: high

### 指令

针对排行榜系列的剧，帮我加上几个硬性要求，每个tile必须有高质量的配图，不然我宁愿不出片

### 摘要

配图硬闸门：bible §4.0 六条（零空卡、高质量标准、独立逐卡审图、榜尾截短 / 整期不出、立项查配图可行性、机检硬拦）；AI 图算合格不设上限；新增 _tools/tile_gate.py（check / sheet / record），release.py 不收录、upload.py 不上传未过闸门的期

---

## 055 — 2026-11-06 13:58:12 — ep21-rice-and-tile-layouts

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties/
> severity: medium

### 指令

我们现在做一下排行榜，新的topic是大米，米饭，这里不需要排名，重点是给观众展示世界各种不同的大米。于此同时，我希望improve这个系列，其中一个点是每张tile图片的展示和layout，你应该给我多个对比的图片和视频展示

### 摘要

新一期（列表期，不排名）：世界各地的大米品种；同时改进系列的卡片（tile）图片展示与版式：在渲染器里做多种卡片版式，用同一批大米卡出对比静帧与短视频交用户选，再按选定版式出整期。

---

## 056 — 2026-11-06 19:48:58 — ep21-pure-rice-images

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

我要的是纯米饭 不要一堆其他的菜，损失focus了

### 摘要

ep21 大米期：卡片图片只拍米本身（一碗白米饭 / 生米粒特写），不用配菜、成品菜；主图=该品种煮熟的纯米饭，小图=生米粒；大字一栏不再写招牌菜，改写米本身的特征（粒长、口感等）。剧级（本期）约定。

---

## 059 — 2026-11-06 22:54:21 — ep21-suno-music

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

需要配乐，用suno

### 摘要

ep21 大米期配乐：用本机 Suno 服务生成纯音乐（先记 request_log），下载后经 add_music 只换音轨，配乐版母版发给用户。

---

## 062 — 2026-11-07 00:00:52 — ep21-youtube-upload

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

帮我把英文版上传youtube

### 摘要

ep21 英文版经 upload.py 传 YouTube（私享，公开由用户在 Studio 亲手点），记录 uploads.json；评论待公开后再发。

---

## 061 — 2026-11-07 00:00:20 — card-image-fit-mode

> severity: medium

### 指令

用户（ep18 最快量产车补图）：可商用的车型照片多为横幅、车身占满画面宽，正方形卡裁切必切车头车尾，真实品牌产品又不能 AI 生成。用户选：给这类卡加「完整放入」模式——整张照片完整缩放放进卡片，空白处用同一张照片的虚化放大填满，车身不被裁切；独立审图按新裁法再审。适用范围：按卡逐张开启（data.json 卡级字段），不改其他卡与其他期的默认裁切。

### 摘要

卡片配图新增「完整放入 + 同图虚化填充」模式，先用于 ep18 车型卡

---

## 058 — 2026-11-06 22:27:29 — upload-ep15-20

> severity: medium

### 指令

用户：「帮我看下排行榜还有哪些视频没有上传，有的就都上传了」「好的，你全都做吧」。执行边界：未传的 ep15–ep20 先过配图硬闸门（follow-up 054）——逐期 sheet，独立子代理审图并 record；ep16 三张被扣下的风险图补可商用 image_alt（不行再按 §4.1 兜底）；审图 fail 的按 §4.0 第 4 条补图；闸门过后 release.py 收录、upload.py youtube 传私享，公开与评论由用户在 Studio 检查后人点。ep21 另一会话在做（follow-up 057），不在本次范围。

### 摘要

ep15–ep20 独立审图过配图闸门后经 API 传成 YouTube 私享

---

## 064 — 2026-11-07 08:59:25 — ep18-wiki-ai-exceptions

> severity: low

### 指令

用户（ep18 最快量产车补图）：#10 Rimac Nevera R 可商用实拍只在维基共享资源上有，#14 Dauer 962 Le Mans 公路版全网可商用的只有赛车版。用户定：本期两处破例——Nevera R 用维基共享资源的 CC BY-SA 4.0 实拍（署名照写，突破 follow-up 009「不用维基图」，仅限这一张）；Dauer 先在维基共享资源找可商用公路版实拍，找不到再用 Codex 生成写实图（突破 bible §4.1「不生成真实品牌产品」，仅限这一张；卡上标 AI IMAGE，上传勾选合成内容声明，不生成车标与牌照文字）。其他卡、其他期规则不变。

### 摘要

ep18 两处破例：Nevera R 用维基 CC BY-SA 图；Dauer 公路版无可商用图时允许 AI 生成

---

## 057 — 2026-11-06 20:39:20 — ep21-poster-codex-images

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

我们用poster style，找不到图片就直接codex出图 帮我制作吧

### 摘要

ep21 大米期定稿用 poster 版式（layout.card_style 默认）；按本期纯米图片约定找真实照片，找不到合格照片的卡直接走 codex 出写实图（AI IMAGE 标注），然后完整制作 ep21。

---

## 060 — 2026-11-06 23:23:18 — ep21-qc-fixes-zh-en-publish

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

好的 帮我把中英文版 还有 publish.md都做好吧

### 摘要

ep21：按第 1 轮独立审片（qc.md：1 blocker / 5 major / 11 minor）修数据与卡面，英文版重渲（带 Suno 配乐），另出大陆中文版（data.zh.json、zh 渲染、中文发布稿与封面），英文 publish.md 补齐（tags、封面、置顶评论说明），再做独立复核。

---

## 063 — 2026-11-07 00:06:43 — ep21-qc-round2-fixes

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties

### 指令

（第 2 轮独立复核 qc.md：中文版 R2-B1 洞察卡截断、R2-M1 出处未核、14 条中文 minor）

### 摘要

ep21：修中文洞察卡断行后重渲中文版；中文用词与发布稿按复核修订；Paw San / Ofada 出处处理；英文 publish.md 小修。

---

## 067 — 2026-11-07 10:00:24 — ep21-zh-covers

> target_artifacts:
>   - ai_videos/paihangbang/episodes/ep21_rice_varieties/render/covers_zh

### 指令

你少了4:3和3:4的cover

### 摘要

ep21 补中文封面三种尺寸（16:9 / 4:3 横屏 / 3:4 竖屏，各 3 个候选，covers_zh/），列表期不用排名版式，按本期白紫红黑米的主题做。

---

## 068 — 2026-11-07 10:34:32 — scroll-speed-1-5x

> severity: medium

### 指令

用户：「排行榜的视频从左到右的滑动速度太慢了，要快 1.5 倍，给我重出所有视频，没有 public 的视频删除并且重新 upload」。执行边界：匀速滚动段速度 ×1.5（rank_scroll SPEED 2→3 px/帧，仍为整数像素防文字闪烁；片头、冠军停留、计分板、片尾时长不变）；配乐按各期 manifest 记录的 Suno 曲目用 --music-fit end 重新裁到新时长；发布稿章节时间与时长按新时间轴重算（保留人工标签）。重渲本会话负责的 16 期（ep01–06、ep11–20，中英文默认版）；ep21 归另一会话、正在做且已公开，不动（之后它重渲自动用新速度）。YouTube 上非 public 的（ep15–20 私享）删除后重传私享；已 public 的（ep01–06、ep11–14、ep21）不删不重传。删除前逐条用 API 复核 privacyStatus，public 的一律不删。

### 摘要

滚动速度 ×1.5，16 期重渲，私享的 ep15–20 删除重传

---

## 046 — 2026-11-04 16:49:18 — zh-mainland-edition

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/bible.md
>   - ai_videos/paihangbang/episodes/*/data.zh.json
> severity: high

### 指令

用户：「帮我把这些全部做另一套中文版出来，有一点要注意的是，中国和台湾的问题，确保台湾是一个地区，而不是另一个独立的国家，因为我们要在大陆发视频，这点尤其重要。」
执行边界（代理判断）：
- 16 期全部出中文版（data.zh.json + 渲染器 --lang zh，输出 *_zh 文件，不覆盖英文版）；版本选择与英文版一致（有带风险图版就出带风险图版）。
- 大陆合规由合并脚本确定性执行、不交给翻译：TW/HK/MO 条目的国家代码一律改 CN、名称固定「中国台湾 / 中国香港 / 中国澳门」、用五星红旗、计分板计入「中国」；全片不得出现青天白日满地红旗、「中华民国 / ROC / 台湾国」或不带「中国」前缀的「台湾」作国家名——自动闸门检查，不过不出片。
- ep02（各国最高峰，按主权国家一国一张）删去玉山（台湾）条目，名次重排，补第 51 个国家凑足 50；ep19 标题改「国家和地区」；ep12 中国面积用官方 960 万平方千米。
- 字体整套用 Noto Sans SC（OFL，可商用），不用微软雅黑（方正版权，商用需授权）。
- 中文显示惯例：单位用中文（米 / 千米 / 平方千米 / 万人次），英尺等英制副数值去掉，专名用大陆通行标准译名（Codex 联网核对）。
- 发布页（抖音 / B 站文案）本轮不做，另议。

### 摘要

排行榜 16 期出大陆中文版；台湾 / 香港 / 澳门按中国的地区处理并由闸门机检

---

## 047 — 2026-11-04 16:57:44 — en-edition-taiwan-region

> target_stage: 6
> target_artifacts:
>   - ai_videos/paihangbang/episodes/*/data.json
> severity: high

### 指令

用户（中文版进行中）：「其实英文版也注意一下这个问题，有需要重做的就重做。」
执行边界（代理判断）：英文版同样按「台湾、香港、澳门是中国的地区」处理：TW / HK / MO 条目改 CN（五星红旗、计分板计入 China），显示名「Taiwan, China / Hong Kong, China / Macao, China」；ep02 删玉山、补伊拉克 Cheekha Dar（3,611 m）；ep19 标题改 Countries and Regions、相关洞察改写；ep12 印度面积按外交部口径约 2.98M km²（注明不含与中国、巴基斯坦有争议的地区），与中文版一致。渲染器的 TW / HK / MO 拒收扩到所有语言。受影响各期（ep01 / 02 / 11 / 12 / 13 / 19）按原配乐与原版本重渲。

### 摘要

英文版同样按台湾、香港、澳门是中国的地区修正并重渲受影响各期

---

## 048 — 2026-11-04 18:51:32 — publish-en-zh-platforms

> target_artifacts:
>   - ai_videos/paihangbang/publish_index.md

### 指令

帮我做好publish.md 我准备上传到youtube， 抖音等国内外平台

### 摘要

英文 publish.md 按地区口径逐条修订（ep02/11/12/13/19）；新增 _tools/zh_publish.py 生成 16 期 publish.zh.md（抖音/快手/B站/视频号/小红书）、thumbnail_zh.png 与 publish_index.md 上传总表；补渲中文稳妥版

---

## 066 — 2026-11-07 09:43:51 — tiktok-upload

> target_stage: 6
> target_artifacts:
>   - tools/tiktok_upload.py
>   - ai_videos/paihangbang/_tools/upload.py
> severity: medium

### 指令

我做了很多排行榜的视频，你能帮我自动upload到tiktok么（用户已在网页登录 TikTok，可配合登录）

### 摘要

仿抖音自动填表新增 tools/tiktok_upload.py 与 upload.py tiktok 子命令：独立 Chrome 配置登录一次，传英文版成片、填说明与话题、传封面、打开 AI 生成内容标识；Post 由用户亲手点

## 065 — 2026-11-07 09:21:31 — ep18-wiki-whole-episode

> severity: low

### 指令

用户（ep18 补图）：follow-up 064 原只批准 #10 Nevera R 一张用维基共享资源图；代理补搜 #11 SSC Ultimate Aero TT 时误告研究员「本期可用维基图」，SSC 已用维基 CC0 实拍（Nate Hawbaker）并过独立审图。代理如实报告后，用户定：维基图破例扩到 ep18 全期所有卡（仅限可商用许可：PD / CC0 / CC BY / CC BY-SA，署名照写）；SSC 保留，#15 Speedtail、#20 Centodieci 可去维基找干净的整车照。其他期仍按 follow-up 009 不用维基图。

### 摘要

ep18 全期允许可商用许可的维基共享资源图（扩大 064 的破例）
