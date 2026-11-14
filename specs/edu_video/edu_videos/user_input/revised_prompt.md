# 教学视频（edu_videos）— 原始意图

2026-11-08 用户：

- 方向：仿照「代理操控 Python、three.js、Blender 等程序渲染，再拼成视频」的做法，做教学类视频——教用户使用工具、网站、服务；给学生讲微积分、线性代数等，需要 3D 可视化辅助；以及 PPT 级的动画。
- 资源：Codex 出图、Suno 配乐视为免费随便用；Blender 本地免费。工具只用免费且可商用的。
- 结构：单独建一个大系列 `edu_videos/`，下分小系列（如线性代数、机器学习），小系列下再按知识点 / topic 分。

---

## 001 — 2026-11-08 10:25:43 — create-edu-videos

### 指令

建立教学视频大系列 edu_videos/：下分小系列（线性代数、机器学习等），小系列下按知识点 tNN_slug 一支视频；工具只用免费可商用的（Manim、MiKTeX、HyperFrames、KaTeX、Playwright、Blender、本地 TTS）；Codex 出图与 Suno 配乐照常记请求日志。

### 摘要

新建 edu_videos 结构、线性代数知识点地图，请求日志支持 edu_videos 归属

---

## 002 — 2026-11-08 12:04:51 — t03-pilot

### 指令

按 edu_videos 试行流程 best effort 做线性代数 t03「矩阵即线性变换」试点：先调研观众喜欢、易懂的讲法，再写讲稿、配音、动画、配乐、合成，独立审稿后交付。

### 摘要

t03 试点成片与配音/时间轴/字幕/合成工具链

---

## 003 — 2026-11-08 13:12:06 — ai-terms-t01-overfitting

### 指令

先做 AI 高频词系列（每支解释一个简单概念，如过拟合、强化学习、卷积神经网络），挑一个先做；线性代数系列暂停。three.js / Blender 用于需要立体感的概念（如 CNN）。

### 摘要

新建 ai_terms 系列，t01 过拟合成片；频道级共用风格与音色

---

## 004 — 2026-11-08 13:37:32 — series-package-bilingual

### 指令

AI 系列升级：统一片头（Apple 发布会式简约大气，介绍本期内容与建议先修知识）、统一转场与片尾，全系列共用；每期内容须覆盖：要解决的问题及其影响、现实世界的影响案例、看待它的视角（认知层面）、生活类比与比喻；配音要更好听（评估 ElevenLabs 等）；中英文两个版本同时出；整体风格简约高级，可用更强的 3D 工具；欢迎补充建议。

### 摘要

系列片包装、内容框架、中英双版本与配音升级

---

## 005 — 2026-11-08 14:08:44 — local-tts-trial

### 指令

配音先实验本地开源模型（ElevenLabs 额度用完、11-17 重置）：评估 Qwen3-TTS、VoxCPM2 等可商用模型，要求同一音色能说中英文、比现在的 MOSS 更好听；出对比样音给用户挑。

### 摘要

本地 TTS 选型实验：Qwen3-TTS、VoxCPM2 与现用 MOSS 对比

---

## 007 — 2026-11-08 17:59:47 — quant-mft-series

### 指令

新开教学视频系列：讲解系统化中频交易（systematic medium-frequency trading），覆盖中国、美国、欧洲、亚太市场；用全机器学习交易；不同数据（行情 bar 数据、外部另类数据等）在中频交易中的角色、类型、特点、难点与影响力。

### 摘要

新建 quant_mft 系列：Vision、受众、模板与知识点地图

---

## 006 — 2026-11-08 16:41:10 — voxcpm-channel-voice

> severity: medium

### 指令

用户试听本地配音选型样音后选定「用 VoxCPM2 · 男声」。

### 摘要

频道配音定为 VoxCPM2 男声，接入 edu_video.py tts

---

## 009 — 2026-11-08 19:14:55 — review-design-benchmark

> severity: high

### 指令

用户：加入审查机制（native speaker、好懂不废话、例子贴切、认知提升与启发；中英重语义不逐字）；不照搬 portal travel，要最适合本系列的审查与验证；成片色彩风格要精修、不要垃圾动画与配图，用好设计师的方法，需要工具说；需要用户选择的给多个选项对比；看网上同类视频、文章、论文与受欢迎程度、评论，吸取精华。

### 摘要

教学视频审查机制（程序检验已落地）、设计选型对比样张、同类对标调研

---

## 008 — 2026-11-08 18:00:07 — ai-terms-t00-what-is-ai

> severity: medium

### 指令

在 AI 高频词系列开做「什么是 AI」一期（概念依赖图的起点，L0 无前置）：按节目模板 v2，中英双版本，讲稿→配音→动画→合成→独立审稿。

### 摘要

ai_terms 新增 t00 什么是 AI（系列开篇），按模板 v2 制作

---

## 010 — 2026-11-08 20:13:03 — ai-terms-duration-quality-first

> severity: low

### 指令

AI 高频词系列：时长不是约束，不为控制时长删减内容；视频质量最重要。

### 摘要

ai_terms 取消 3–5 分钟时长限制，质量优先

---

## 012 — 2026-11-08 22:37:35 — line-review-v2

> target_artifacts:
>   - tools/edu_review.py
> severity: high

### 指令

用户 2026-11-08：「本期内容」台词很突兀，不是正常人会讲的话；视频 PPT 只该列纲要、相对简练，但 PPT 和台词都差很远。要求借鉴 Portal Travel 引入台词 review 机制，review 整个视频的 PPT 与台词（两者标准不同），中文、英文分别 review，确保两种母语观众都觉得通顺易懂；搭好流程后重新 review、修正、重新制作。

### 摘要

新增台词审 v2（edu_review new/check/issues + line_review.json）：口播与屏幕文字 × 中英四项，每项 Claude/Codex 双审 0–3 评分带证据，分歧与抽查交裁决，最多 3 轮；edu_web screen_dump 逐句导出可见文字与截图；t01 全片按此复审、修正、重做。

---

## 011 — 2026-11-08 20:40:16 — design-v1-t01-v3

> severity: high

### 指令

用户从对比样张选定 S3 浅色舞台、P3 暖琥珀、F3 MiSans、I1 哑光陶土 3D；要求按新设计与审查机制重做，并持续汇报进度。

### 摘要

频道设计规范 v1 落地（网页场景渲染、包装换肤、陶土插图）与《过拟合》v3 讲稿三轮审查、中英重做

---

## 013 — 2026-11-09 08:19:47 — spoken-first-shorter

> target_artifacts:
>   - tools/edu_review.py
> severity: high

### 指令

用户 2026-11-09：口播还有一听就出戏的句子（如「现实里的祸，怎么防」），问流程上怎么预防；视频太长，概念应该用更简练的语言讲清，举例一个就行；「学习 ≈ 压缩」保留，能提升认知。

### 摘要

流程：先说后写（讲解员模型按意思口述成稿）；台词审 v3 加逐句「跟朋友复述」（报告缺了不合格）、串场句与章节标题从严、口语黑名单 lint、审查链 --chain；t01 改成 v5 约 4 分钟：5 章（定义＋学生比方、小实验、学习≈压缩、谷歌流感趋势、怎么防），去掉本期内容卡、认猫、300 次实验、胸片、皮肤癌。

---

## 015 — 2026-11-09 12:28:23 — ai-terms-t09-lagrange

> severity: medium

### 指令

在 AI 里要理解拉格朗日，再做一期视频讲解拉格朗日以及和 AI 的关系与应用

### 摘要

AI 高频词新增 t09 拉格朗日乘子：按 v5 流程（先说后写、台词审 v3、3–5 分钟一个例子）制作中英两版；实验为围栏内找最高点（程序算出），AI 例子为 Safe RLHF 自动调 λ，另带正则化、KL 系数一句

---

## 014 — 2026-11-09 12:19:59 — t00-native-review

> target_artifacts:
>   - edu_videos/ai_terms/t00_what_is_ai
> severity: medium

### 指令

成片交付前再做一轮自审与自修，重点是中英母语听感审查；修完后给出管理应用 episode-preview 预览地址

### 摘要

t00 成片追加母语听感审稿轮（cut_r4），按结论修讲稿/画面并重渲染，提供预览 URL

---

## 016 — 2026-11-09 19:38:44 — ai_terms_wordlist_v2

> target_artifacts:
>   - edu_videos/ai_terms/词表提案_v2.md

### 指令

这个list 太少了，你做点reserach，看其他课程是怎么做的，给我一个新的proposal

### 摘要

调研 8 门同类课程/词表，出 AI 高频词词表提案 v2：6 季 39 期、播放顺序、前置、快线，待用户定

---

## 017 — 2026-11-09 19:51:24 — ai_terms_wordlist_v21

> target_artifacts:
>   - edu_videos/ai_terms/词表提案_v2.md

### 指令

可以，但是过拟合真的是放在第二个位置最好吗？你不用被现有的框架限制住，我重出视频又不要钱

### 摘要

词表提案 v2.1：不受已做三期位置限制重排，过拟合移到怎么学之后（1-7），新增模型与参数、损失函数、反向传播，40 期

---

## 018 — 2026-11-09 20:12:30 — ai_terms_syllabus

> target_artifacts:
>   - edu_videos/ai_terms/课程表.md

### 指令

单独做一期，然后把完整的6季写入md文件我要在UI上能看到。left nav 能navigate

### 摘要

ai_terms 课程表.md 定稿（6 季 40 期，损失函数单独一期），README 指向它

---

## 019 — 2026-11-09 20:16:39 — ai_terms_s1_parallel

> target_artifacts:
>   - edu_videos/ai_terms/课程表.md

### 指令

做完之后，请把1-2 ~ 1-6 并行生成

### 摘要

t10 模型与参数、t11 损失函数、t04 梯度下降、t12 神经网络、t13 反向传播 五期并行制作（各一子代理，按 t09 流程与 s1_bible）

---

## 020 — 2026-11-14 10:39:43 — redian_xiangying_series

> target_artifacts:
>   - edu_videos/redian_xiangying/README.md
>   - edu_videos/redian_xiangying/_shared/dossier_template.md
>   - edu_videos/README.md
> severity: low

### 指令

我们开启一个新的系列剧叫做热点相迎：给一个热点词，先大量搜索互联网，找到最近一段时间相关的所有材料，总结归纳，要有自己的立场，提炼认知精华，再以视频形式展现给大众；视频可含相关人或事物的图片、视频节选、Seedance 模拟视频，穿插像 edu_videos 一样的 PPT 视频，剪辑到一起，Suno 配乐。（追加）采用你的 1，2，3，5，其余不采纳。

### 摘要

新建 edu_videos/redian_xiangying 系列（系列级规则）：采纳定位（热点开场、长期认知为正片）、立场（事实/观点/推测分开、反方最强论证、claims.json 带 as_of）、素材版权分级与 media_ledger.json、研究档案模板；不采纳 Seedance 额外限制、固定片子结构、快慢两条线；平台、语言、主持人声音待定

---

## 021 — 2026-11-14 10:42:40 — redian_trend_pick_t01_t02

> target_artifacts:
>   - edu_videos/redian_xiangying/README.md
>   - edu_videos/redian_xiangying/t01_faa_ground_stop/research/
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/research/
> severity: low

### 指令

从网上 search 一些热点话题，比如 youtube、tiktok、抖音等等，然后我们选前两名制作热点视频

### 摘要

2026-11-14 跨平台热榜检索（抖音/微博/B站/知乎聚合、TikTok 标签、YouTube 全球趋势）：第一 美国 FAA 全国地面停飞（11-13），第二 黄仁勋辞任英伟达 CEO（11-12）；建 t01、t02 期目录并启动研究档案

---

## 022 — 2026-11-14 11:30:19 — redian_t01_t02_decisions

> target_artifacts:
>   - edu_videos/redian_xiangying/README.md
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/research/
> severity: medium

### 指令

t01 用论点 A（动它的时候最危险）。t02：我们要深度挖掘观众感兴趣的，之间是的背后应该是美国两党之间的斗争，老黄是牺牲的对象，还有就是中美竞争大背景，这些才是有意思的点。英伟达官方素材：直接用就行，这种热点类的剧集不用在意这些条款。平台语言：中英双语，B站＋YouTube。

### 摘要

t01 论点定 A；t02 角度改为两党政治斗争与中美竞争背景下的黄仁勋（作为待证假设补充研究，按系列立场规则检验）；本系列素材不再按网站条款分级（用户决定，素材台账只记来源）；中英双语，B站＋YouTube

---

## 023 — 2026-11-14 11:48:22 — redian_t02_thesis_faa_archive

> target_artifacts:
>   - edu_videos/redian_xiangying/README.md
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/research/dossier.md
>   - edu_videos/redian_xiangying/t01_faa_ground_stop/research/archive/
> severity: low

### 指令

t02 论点选「科技战＋两党都拿他打仗」；FAA 原文用 Chrome 存档

### 摘要

t02 主线定为「中美科技战让一个 CEO 的私事变成国家安全问题」，第二层「对华芯片上国会两党都要收紧、只有白宫在放，两党都拿他打自己的仗」（标我们的判断），「牺牲品」作中文舆论说法引用并检验；t01 FAA 公告与声明页用 Chrome 存档到 research/archive/

---

## 024 — 2026-11-14 12:10:26 — redian_t01_script_start

> target_artifacts:
>   - edu_videos/redian_xiangying/t01_faa_ground_stop/
> severity: low

### 指令

现在就开，不用等（t01 中英讲稿现在开写，不等 t02）

### 摘要

t01 FAA 停飞开写讲稿：按 edu「先说后写」——先写每拍意思与事实（beats），再由中英讲解员各自口述成稿，作者剪短核事实，lint 后进台词审

---

## 025 — 2026-11-14 12:31:22 — redian_t02_factcheck_applied

> target_artifacts:
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/claims.json
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/research/dossier.md
> severity: low

### 指令

（执行 follow-up 023 的延续）t02 独立事实核查 r1 意见落实

### 摘要

t02 claims.json 落实核查 r1（改 34 条、新增 C113–C126，共 126 条）；dossier 第二层论点改为「两党都借这件事追问」、新增风险句与截图禁区；coverage.md 隐私说明改正

---

## 027 — 2026-11-14 14:29:09 — chips-series-start

> target_stage: 1
> severity: medium

### 指令

新建芯片科普系列：用虚拟人物缩小到芯片上参观电路结构与纳米级晶体管、参观制造厂房；两个人物一问一答。流程：先 research 全部芯片细节，再创作 AI 视频；先出 t01 故事板图片给用户 review，再定怎么出视频。系列只讲芯片（用户未选『微观之旅』，按芯片立系列，名字可改）。画面为系列级例外：准确结构用 Blender/代码，人物与氛围镜头可用 Seedance。

### 摘要

建 chips 系列、t01 研究档案与故事板

---

## 028 — 2026-11-14 15:07:35 — chips-cinematic-real-humans

> target_stage: 1
> severity: medium

### 指令

芯片系列画风定为电影写实（故事板选项 S2）；人物改为写实真人（虚构人物，不像任何真实个人）；台词草稿认可，按 edu「先说后写」与台词审流程定稿。据此重做人物设定图与 t01 故事板。

### 摘要

chips 系列画风定 S2 电影写实、人物改真人，重做设定图与故事板

---

## 029 — 2026-11-14 15:47:40 — explore-series-cast

> target_stage: 1
> severity: medium

### 指令

芯片升为「探索系列」的第一个主题，后续还有其他主题；两位主角跨主题、跨系列重复使用，选角时要考虑以后的系列。待定：中英各一对演员（中文版两位中国人、英文版两位欧美人），还是一对混血/多元组合只出一个画面版本、中英配音。

### 摘要

探索系列：主角跨主题复用；选角方案待用户选

---

## 030 — 2026-11-14 15:54:32 — explore-casting-v1

> target_stage: 1
> severity: medium

### 指令

选角方案采纳：一套画面、中英两版配音；向导华人、新手中欧混血（作为推荐方向）；目录改为 edu_videos/tansuo（探索系列），芯片为第一个主题。先生成几组候选人物照片供选角：每人要正面、侧面、背面，以及若干表情图。人物跨主题、跨系列复用。

### 摘要

探索系列选角 v1：向导与新手各几组候选（四视图＋表情）

---

## 031 — 2026-11-14 16:08:41 — explore-cast-chosen

> target_stage: 1
> severity: medium

### 指令

探索系列主角选定：向导林 = 选角 G1（齐耳短发、圆框眼镜，即原林工），新手凯 = 选角 K1（中欧混血，深棕卷发、榛色眼睛、高瘦）。之后所有主题都以这两人为准；用他们重出 t01 故事板。

### 摘要

主角定 G1（林）与 K1（凯），重出 t01 故事板 v3

---

## 032 — 2026-11-14 16:09:59 — explore-vfx-imagination

> target_stage: 1
> severity: medium

### 指令

既然用 AI，特效要做得漂亮、发挥想象力。原则：特效华丽但服务内容——画真实存在的现象（光、电信号、电子、尺度变化、剖开结构），标「示意」；结构本身仍按研究档案、不画装饰性假电路花纹与假文字。取代 follow-up 028 画风里「不画发光电路、全息投影」的限制。

### 摘要

探索系列加想象力特效（服务内容、标示意），重设计 t01 故事板 v3 的特效

---

## 033 — 2026-11-14 16:42:00 — explore-cast-turntable

> target_stage: 1
> severity: low

### 指令

用户批准提交林与凯的 Seedance 建立视频（15 秒，中英各一句＋原地转身，seedance2.5 720p 16:9）。

### 摘要

提交林、凯建立视频

---

## 034 — 2026-11-14 16:50:17 — explore-guide-recast

> target_stage: 1
> severity: medium

### 指令

女主（向导林）要很漂亮、知性美、有学识；再出 5 组候选照片（四视图＋表情）与 G1 对比，重新选。

### 摘要

向导重新选角：casting_v2 五组知性美候选

---

## 035 — 2026-11-14 17:00:41 — explore-guide-recast-v3

> target_stage: 1
> severity: medium

### 指令

向导选角以 G5（低发髻、无眼镜、清冷优雅）和 G6（侧分齐耳短发、细黑方框、干练）为基础，再漂亮一点，再出 5 组新照片对比。

### 摘要

向导选角 v3：基于 G5/G6 更漂亮的五组

---

## 036 — 2026-11-14 17:10:47 — explore-guide-g9

> target_stage: 1
> severity: medium

### 指令

向导林定为选角 v3 的 G9（基于 G5：低发髻、不戴眼镜、知性美）；出她的 Seedance 建立视频（用户已同意提交）。原 G1 的参考与建立视频归档作废。

### 摘要

林改定 G9，出立绘与建立视频

---

## 037 — 2026-11-14 17:19:47 — explore-turntable-fullbody

> target_stage: 1
> severity: low

### 指令

人物建立视频必须全身入画（头顶到鞋底完整可见）。林 G9 的建立视频只到大腿，不合格，重出。验收时取景不是全身就判不过。

### 摘要

林建立视频重出（全身）；建立视频验收加全身一条

---

## 026 — 2026-11-14 12:44:32 — redian_t01_full_production

> target_artifacts:
>   - edu_videos/redian_xiangying/t01_faa_ground_stop/
> severity: medium

### 指令

给我 preview url / 等你做完了给我 preview url；素材①②都下；等 Seedance 做完再给 preview

### 摘要

t01 做到成片再给 /episode-preview 链接：网页场景、下载 Commons 公共领域图片与白宫记者会视频（登记 media_ledger）、Seedance 镜头 prompt 交用户点生成、配音、Suno 配乐、合成

---

## 038 — 2026-11-14 17:37:43 — t01-storyboard-g9-selfcheck

> target_stage: 1
> severity: medium

### 指令

用定稿主角（林 G9、凯 K1）重出 t01 整集故事板图；出完自检＋独立审稿，不满意就改到满意（每格最多重出两次，仍不过交用户）；生成视频前先给用户预览。

### 摘要

t01 故事板 v4（G9）整集重出＋自检迭代，出片前用户预览

## 039 — 2026-11-14 20:31:55 — redian_t02_full_production

> target_artifacts:
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/
> severity: medium

### 指令

（电脑重启后接续）不是荒野生活，是热点相迎的两个 topic：黄仁勋、美国飞机事件；没做完的继续；做好了之后给我 preview url；t02 Seedance 4 条同意都提交

### 摘要

t01 已成片待审；t02 从讲稿做到成片：讲稿要点→中英讲解员口述→台词审→配音→网页场景＋Seedance 4 镜（用户已同意，约 480 积分）＋公开图片→Suno 配乐→合成→/episode-preview 链接

## 040 — 2026-11-14 20:35:09 — tansuo-preview-drama-style-audio

> target_artifacts:
>   - edu_videos/tansuo/t01_inside_a_chip/
> severity: medium

### 指令

探索 t01 的故事板预览改成和短剧「拍摄」模块页同样的样式（参照 /drama?drama=ai_videos/chuanyue_yiri&episode=ep01&module=filming）。另加一个整集「音频预览」：不出视频，用本地 TTS 按人物声音模拟出整集对白，让用户真实体验听感；播放器下方像视频一样显示 scene / shot 进度条；音频时间轴尽量和以后真实视频一致，作为出视频前更完整的审阅材料，代理也用它自检。以后每次出视频前的预览都要包括这个音频预览。

### 摘要

t01 故事板预览改为短剧拍摄页样式；新增整集音频预览（本地 TTS、scene/shot 进度条、时间对齐成片），今后出视频前必给

## 041 — 2026-11-14 20:47:54 — redian_t02_images_voice_fluency

> target_artifacts:
>   - edu_videos/redian_xiangying/t02_jensen_huang_resigns/
> severity: medium

### 指令

图片少了点，没有 public 的图片就让 codex 生成；中文配音一听就是电脑，ElevenLabs 效果会好吗、还有没有其他付费专业中文配音 API → 先试 ElevenLabs；文字不够通顺流畅

### 摘要

t02：补公开图片（国会议员官方照、总部、港口等）＋Codex 生成示意图（不出真人、标 AI 生成）；讲稿中英按通顺流畅重写一轮再进台词审；ElevenLabs 中文母语音色 5 句样音给用户盲听，定了再决定 t01/t02 是否换配音引擎
