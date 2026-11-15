---
worker_id: researcher-06-benchmark-myths
stage: 3
role: researcher
angle: benchmark-myths
status: partial
blockers:
  - "YouTube 只拿到 yt-dlp 扁平检索的播放量和时长；没有逐条看视频内容，「讲法与画面」只根据标题、频道惯例和简介写，凡是没看过的都标了「未逐帧核实」。点赞和评论没取（meta 层上季已被要求登录，本次没试）"
  - "B 站搜索：x/web-interface/search/type（可按播放排序）返回 412，只有 search/all/v2（按相关度排序，每词 20 条）可用，所以 B 站榜单不是「按播放排的头部」，只是相关结果里播放最高的"
  - "B 站 view 接口返回里没有 official 认证字段（WebFetch 摘要如此），所以没能确认各 UP 主是否有医疗资质认证"
  - "知乎问题页 WebFetch 返回 403，只拿到搜索结果里的问题标题，看不到关注数和回答正文；Reddit 没尝试（上季已确认 403、WebSearch 不收该域名）"
  - "B 站热评抓了 3 支（大物是也、泽桥医生、小哥哥不心急），热评里没有一条是提问；其余视频热评没抓"
  - "纳豆激酶：没找到卫健委、科普中国或监管机构的辟谣原文，也没查 RCT；只记了检索结论，见第 3 节"
  - "SAMSON（NEJM 2020 N-of-1 他汀试验）是 Correspondence，PubMed 没有摘要，具体数字未查到"
  - "Ofcom/BHF/Mayo Clinic 各自的健康内容规范没查；抖音《社区医疗健康公约》原文没查到，只有报道"
  - "WebSearch 本角度共用 13 次（上限 20，协调者要求本轮收尾）"
confidence: medium
---

# 血脂季 · 对标、观众真问题、流行误解与平台规则（t11 角度文件）

> 查于 2026-11-14。YouTube 数据来自 `tools/yt_research.py search`（yt-dlp 扁平检索，只有播放量和时长，原始 JSONL 在会话草稿目录，未入库）。B 站数据来自公开接口 `x/web-interface/search/all/v2`、`x/web-interface/view` 和 `x/v2/reply`（热评第 1 页）。论文摘要来自 NCBI E-utilities（efetch）。频道通用对标在 `edu_videos/_shared/research/explainer_benchmark.md`，本文不重复。

## 1. 对标：讲血脂、LDL、他汀和动脉粥样硬化的高影响力内容

### 1a. YouTube（播放量查于 2026-11-14）

| # | 频道 · 视频 | 链接 | 播放 | 时长 | 讲法与画面 | 讲得好 | 缺了什么 |
|---|---|---|---|---|---|---|---|
| 1 | Nucleus Medical Media · LDL and HDL Cholesterol \| Good and Bad Cholesterol | https://www.youtube.com/watch?v=0U7YHRW5dyc | **373 万** | 3:01 | 医学 3D 动画加旁白，Nucleus 的惯常风格（未逐帧核实） | 3 分钟讲一个概念，播放量在本题材的「科学派」里最高 | 无人物、无提问；仍沿用「好 / 坏胆固醇」的说法，见第 3 节误解 11 |
| 2 | Nucleus Medical Media · Atherosclerosis (2009) / (2008) | https://www.youtube.com/watch?v=OHE1ig4k64M ；https://www.youtube.com/watch?v=EQVEdFSlUGU | 132 万 / 114 万 | 3:26 / 2:52 | 3D 血管剖面，斑块形成（未逐帧核实） | **「进到动脉里看斑块」画面的老牌先例**，十几年了还有长尾 | 2008–09 年的画质；纯旁白 |
| 3 | TED-Ed · What actually causes high cholesterol? – Hei Man Chan | https://www.youtube.com/watch?v=EixIyh1gshM | 184 万 | 6:48 | 2D 动画（TED-Ed 惯例，未逐帧核实） | 问题式标题，以「为什么」开头 | 未看内容，是否讲到他汀和风险分层不清楚 |
| 4 | TED-Ed · What happens during a heart attack? – Krishna Sudhir | https://www.youtube.com/watch?v=3_PYnWVoUzM | **920 万** | 4:54 | 2D 动画 | 证明「血管里出了什么事」是大众爆款，5 分钟以内 | 讲的是结果（心梗），不讲血脂怎么来 |
| 5 | Alila Medical Media · Cholesterol Metabolism, LDL, HDL and other Lipoproteins, Animation | https://www.youtube.com/watch?v=9dghtf7Z7fw | 156 万 | 3:46 | 医学动画，脂蛋白分类 | 脂蛋白「小船」的形象化 | 偏教科书，无观众问题线（未逐帧核实） |
| 6 | Ninja Nerd · Lipoprotein Metabolism（Chylomicrons, VLDL, IDL, LDL & HDL） | https://www.youtube.com/watch?v=wQY0xpwqPfQ | 165 万 | 1:03:35 | 白板手绘讲课 | 医学生口碑，机制完整 | 63 分钟，面向医学生；同频道 Hyperlipidemia 22.5 万（28:39）、降脂药 25.8 万（1:43:45） |
| 7 | Armando Hasudungan · Atherosclerosis – Pathophysiology | https://www.youtube.com/watch?v=R6QTiBfzULE | 109 万 | 14:37 | 手绘 | 病理过程完整 | 面向医学生 |
| 8 | Osmosis from Elsevier · Fats – biochemistry；Acute coronary syndrome | https://www.youtube.com/watch?v=BVxeeiR7JB0 ；https://www.youtube.com/watch?v=PChi3kqLK5k | 102 万；44 万 | 12:20；12:11 | 2D 医学插画 | 准确、系统 | 搜索「osmosis hyperlipidemia」只出 82 秒预告片（5.8 万），**Osmosis 没有一支面向大众的血脂爆款** |
| 9 | JJ Medicine · Statin Side Effects | https://www.youtube.com/watch?v=l2r0bF7LN0U | **454 万** | 9:36 | 讲解加示意图（未逐帧核实） | 「副作用」这个搜索意图的流量极大 | 未看内容，是否给出绝对风险不清楚 |
| 10 | British Heart Foundation · Are eggs good or bad for cholesterol? / Statins, side effects and what they're used for / Foods to reduce high cholesterol naturally | https://www.youtube.com/watch?v=yAuSs-4hXa4 ；https://www.youtube.com/watch?v=d3_h9gtDsqc ；https://www.youtube.com/watch?v=RnF3j-IvhQc | 2.9 万 / 2.4 万 / 2.2 万 | 1:08 / 1:50 / 2:00 | 权威机构短片 | **选题正好就是观众真问题**（鸡蛋、他汀副作用、食物降脂） | 播放只有几万：**权威来源的选题对，但没人看** |
| 11 | Mayo Clinic · Cardiovascular Diet Myths | https://www.youtube.com/watch?v=VkRLMQ6RF60 | 0.14 万 | 9:39 | 播客式 | 权威 | 搜索「Mayo Clinic cholesterol」没有一支血脂视频进前 8；Mayo 频道血脂内容几乎没有播放 |
| 12 | Peter Attia MD · #407 Preventing cardiovascular and Alzheimer's disease: lowering LDL early, APOE4 | https://www.youtube.com/watch?v=EuPcbF9YVTo | 7.1 万 | 2:19:16 | 长访谈播客 | 「LDL 越早降越好」「apoB」的深度论证 | 2 小时，大众看不完 |
| 13 | Physionic · Doctors were Wrong about Cholesterol and Heart Disease；'They Lied about High LDL!'；Dr. Fung: 'Cholesterol is barely relevant…' | https://www.youtube.com/watch?v=mJLKTyKy-14 ；https://www.youtube.com/watch?v=JdTist3NtZ4 ；https://www.youtube.com/watch?v=R3FtYEk7nc8 | 10.5 万 / 13.4 万 / 13.0 万 | 10:03 / 28:46 / 17:31 | 未看内容；**只看标题，倾向质疑 LDL 致病**（未核实其论证） | — | 血管外科医生 Lily Johnston 专门做了回应片「The Cholesterol Myth That Won't Die – A Vascular Surgeon Reacts to @Physionic」（24.7 万）https://www.youtube.com/watch?v=dQBAUylIS9k 。说明 **反驳片本身也能拿流量** |
| 14 | Dr Brad Stanfield · We Are Witnessing The End of Heart Attacks | https://www.youtube.com/watch?v=SOWqgZDdo6A | 188 万 | 20:50 | 医生出镜（未看内容） | 讲新药 / 新疗法的「希望叙事」 | 未核实内容 |
| 15 | Doctor Mike · 搜索「Doctor Mike statins / cholesterol」**没出现他本人的血脂专题**；出现的是 Mel Robbins 访谈「The Health Lies That Are Keeping You Sick」 | https://www.youtube.com/watch?v=hNWa7zJIsko | 83 万 | 1:24:06 | 访谈 | — | 未找到 Dr. Mike 血脂单片 |
| 16 | Kurzgesagt · 搜索「kurzgesagt cholesterol / heart」**没有血脂或动脉粥样硬化片**；最接近的是 How The Immune System ACTUALLY Works（2624 万） | https://www.youtube.com/watch?v=lXfEK8G8CUI | — | 10:48 | — | — | **Kurzgesagt 级别的画面 × 血脂题材：空位** |

**「反主流」内容占据流量头部**（搜索「cholesterol explained / statins」按播放排序的前列）：

| 频道 · 标题 | 链接 | 播放 | 时长 |
|---|---|---|---|
| PowerfulJRE · Cardiologist on the Over-Prescribing of Statins for Heart Disease | https://www.youtube.com/watch?v=x3BzgZqFuZc | 498 万 | 14:55 |
| Dr. Sten Ekberg · Your Doctor Is Wrong About Cholesterol | https://www.youtube.com/watch?v=sY48qLl9ZzE | 356 万 | 28:07 |
| NBC News · Study Confirms What Many Patients Taking Statins Have Said for Years | https://www.youtube.com/watch?v=6sWmgtqROKU | 305 万 | 2:14 |
| Dr. Boz · Why I Don't Prescribe Statins For High LDL Cholesterol | https://www.youtube.com/watch?v=rymCw1ED5tk | 228 万 | 8:30 |
| KenDBerryMD · 10 Ways Statins Wreck Your Body (Hidden Side Effects) | https://www.youtube.com/watch?v=HgEv-tOAY8M | 181 万 | 5:45 |
| Low Carb Down Under · Maryanne Demasi 'Statin Wars' | https://www.youtube.com/watch?v=BzTjPuikhQE | 188 万 | 24:10 |
| Leonid Kim MD · #1 Best Meal to UNCLOG Your Arteries | https://www.youtube.com/watch?v=WQIE86q08mk | **713 万** | 11:30 |

以上只记标题与数字，未看内容，不对其论证下结论。**结论**：英文区「质疑他汀 / 吃东西就能疏通动脉」的标题，播放量是 BHF、Mayo 这类权威机构的 100 倍以上。

### 1b. B 站（公开接口，2026-11-14；按相关度检索，不是全站播放排行）

| # | UP 主 · 视频 | 链接 | 播放 | 时长 | 赞/播 | 藏/播 | 讲法与画面 | 好 / 缺 |
|---|---|---|---|---|---|---|---|---|
| 1 | **大物是也 · 瘦子竟会高血脂？「老年病」开始盯上年轻人【医生体检报告大公开】**（2023-05-31） | https://www.bilibili.com/video/BV1UM4y1i7pK | **105.9 万** | 15:58 | 3.95% | 0.59% | 医生出镜，公开自己的体检报告（据标题；未看内容） | 好：**「瘦人也高」+ 真人真报告**，是检索到的唯一百万播放。缺：热评 3 条最高（3887 / 2795 / 2043 赞）全是玩梗，**没有一条是提问** |
| 2 | 自学倪师医学 · 血脂高、血液太浓，倪师教你一招 | https://www.bilibili.com/video/BV1AC4y1f7z3 | 34.4 万 | 2:59 | — | — | 中医偏方类 | **「血液太浓」是中文区流行概念**；同类倪海厦搬运号在「胆固醇」「他汀」结果里反复出现（「西医说的胆固醇是个天大的谎言…别再吃他汀了」BV1Sbs1z4Eqm；「高血脂根本不用吃他汀…副作用为零」BV1cuckz3EXY） |
| 3 | 聊医点 · 搞清源头，再降血脂｜最后一招可太强了！ | https://www.bilibili.com/video/BV1wj41187Wf | 24.1 万 | 15:38 | — | — | 未看内容 | — |
| 4 | A地球科普 · 每天吃 3 个鸡蛋会怎样？骗你 60 年的胆固醇谣言该破了！ | https://www.bilibili.com/video/BV1MGtQ6PEWX | 26.3 万 | 5:33 | — | — | 未看内容 | **鸡蛋是中文区最热的血脂入口话题**（「胆固醇」前 20 条里有 4 条讲鸡蛋） |
| 5 | **泽桥医生 · 从出生就开始的动脉粥样硬化，血管里的「粥」到底是啥？**（2021-03） | https://www.bilibili.com/video/BV1fh411Q77c | 19.7 万 | 2:06 | 2.03% | 1.03% | 简介：「是冠心病、脑血管病等缺血性疾病的主要病理基础」 | 好：**从「粥」字切入，2 分钟**。热评（165 赞）「它大名还有一个是粥瘤」；另一条（67 赞）在争「西医霸权主义」 |
| 6 | 心血管王医生 · 血脂高究竟怎么吃？哪些食物会升血脂？ | https://www.bilibili.com/video/BV13NC9YHEYJ | 11.4 万 | 5:37 | — | — | 医生口播（未看） | — |
| 7 | **小哥哥不心急 · 【3D 演示】动脉粥样硬化（原版+字幕版）**（2017-05，转载） | https://www.bilibili.com/video/BV1Wx411v7WF | 10.5 万 | 5:34 | 1.47% | **3.72%** | 搬运 YouTube 医学 3D 动画，简介附 YouTube 源链接 | 好：**收藏率在本表最高**，3D 进血管画面在中文区有需求。热评（58 赞）「太可怕了血管就这么被堵死了啊啊啊」，**3D 画面自带恐惧感** |
| 8 | 鱼呆立和古猫宁 · 【病生三分钟】高脂血症：血脂指标咋看？LDL、HDL 有什么区别？ | https://www.bilibili.com/video/BV1sr4y117ua | 10.2 万 | 4:43 | 2.89% | 2.65% | 简介注明素材来自两支外部动画 | 好：「血脂指标咋看」直接对应体检场景；4–5 分钟 |
| 9 | 北京睿影东方 · 医学 3D 动画演示，动脉粥样硬化与心肌梗死 | https://www.bilibili.com/video/BV1C5411P7xb | 10.0 万 | 0:54 | — | — | 商业医学动画公司的样片 | 中文区 3D 进血管的本土先例 |
| 10 | 乐丰-乐真 · 为什么叫动脉粥样硬化斑块？颈动脉斑块，大小固然重要，但稳不稳定才是关键！ | https://www.bilibili.com/video/BV17CGs6PEAm | 7.7 万 | 1:44 | — | — | 未看 | **「斑块稳不稳定」是体检颈动脉超声后的真实焦虑点** |
| 11 | 鹤立烟雨 · 血脂多高需要吃药？怎样判断血脂危险程度？ | https://www.bilibili.com/video/BV1hN4y1F7V1 | 3.6 万 | 3:07 | — | — | 未看 | 标题本身就是真问题 |
| 12 | 亮曰代谢健康 · LDL 从来就不是坏胆固醇；他汀也治不好高血脂！（2026-11-12） | https://www.bilibili.com/video/BV1MMWR6fE5n | 0.29 万 | 17:24 | — | — | 未看 | 中文区也有 LDL 怀疑论，但播放远低于英文区 |

**中文区小结**：
- 检索到的血脂内容只有一支过百万（大物是也），**中文区没有「画面精良的 3D + 3–5 分钟 + 讲清他汀」的头部作品**。3D 进血管画面主要来自搬运（小哥哥不心急）和医学动画公司样片（北京睿影东方），收藏率高。
- 中医偏方与「别吃他汀」类搬运号在「他汀」「胆固醇」检索结果里密度很高，评论区出现「西医霸权」争论。**我们一旦讲他汀，评论区会有这一派**。
- 热评几乎不提问（与上季芯片的发现一致）。真问题要从问答站和视频标题里找（第 2 节）。

### 1c. 「缩小进血管 / 动脉」的画面先例

| 先例 | 手法 | 证据 | 对我们 |
|---|---|---|---|
| Nucleus Medical Media（YouTube，2008–09 起） | 3D 剖开动脉，镜头在管腔里，看 LDL 进入管壁、斑块长大 | 两支 Atherosclerosis 合计约 246 万；LDL/HDL 片 373 万 | 「镜头在管腔里」已经是标准做法，**新的是人物在里面问问题** |
| YouTube 2025–26 年大批「3D Medical Animation」小号（Dr. How、MedWise、Medical Documentaries 等） | 同类 3D，疑似大量 AI 或模板生成 | 播放多为几千（如 Medical Documentaries「How Cholesterol Tablets Work Explained in 3D」2923） | **3D 血管画面本身已经泛滥，不再稀缺**；差异化只能靠准确性、人物与问题 |
| 北京睿影东方（B 站） | 商业 3D 动画 | 10 万（54 秒） | 中文区本土供给少 |
| 工作细胞 / 人体大冒险 | 拟人化细胞 | 上季已记（见 t01 benchmark_format.md） | 比喻会被当真，要标示意 |

「Fantastic Voyage」式「真人缩小进血管」的科普短片，本次没有检索到高播放先例（只搜了 1 个词，覆盖不全）。

## 2. 观众真问题（凯的提问来源）

只收有出处的原话（问题标题）。热评提问没有收集到（B 站 3 支热评无提问；YouTube 评论未取）。

| # | 问题原话 | 出处 | 平台 |
|---|---|---|---|
| 1 | 「降脂药对肝有损伤吗？」 | https://www.zhihu.com/question/445438810 | 知乎问题 |
| 2 | 「胆固醇高还能吃鸡蛋吗？」 | https://www.zhihu.com/question/624493850 | 知乎问题 |
| 3 | 「血脂正常他汀能停药吗？」（专栏标题，医生回答体） | https://zhuanlan.zhihu.com/p/168721070 | 知乎专栏 |
| 4 | 「吃他汀类药物，可以每年停服一段时间吗？」 | https://zhuanlan.zhihu.com/p/695942077 | 知乎专栏 |
| 5 | 「他汀副作用大吗？能不能长期吃？如何复查？」 | https://zhuanlan.zhihu.com/p/3905637999 | 知乎专栏 |
| 6 | 「血脂多高需要吃药？怎样判断血脂危险程度？」 | https://www.bilibili.com/video/BV1hN4y1F7V1 | B 站标题 |
| 7 | 「瘦子竟会高血脂？」 | https://www.bilibili.com/video/BV1UM4y1i7pK （105.9 万播放） | B 站标题 |
| 8 | 「血脂高≠肉吃多！真正元凶是它！」（反映「不吃肉为什么也高」） | https://www.bilibili.com/video/BV1wKc6zvEEf （心血管崔松主任，2.8 万） | B 站标题 |
| 9 | 「血脂高、血液太浓」（「血稠」概念） | https://www.bilibili.com/video/BV1AC4y1f7z3 （34.4 万） | B 站标题 |
| 10 | 「颈动脉斑块，大小固然重要，但稳不稳定才是关键！」 | https://www.bilibili.com/video/BV17CGs6PEAm | B 站标题 |
| 11 | 「降压药、他汀类药物不能和柚子一起吃，是不是真的？」 | https://www.bilibili.com/video/BV12G411L7qL | B 站标题 |
| 12 | 「听说吃红曲米可以降低胆固醇？他汀类药物可以不吃了，是真的吗」 | https://www.bilibili.com/video/BV1AP4y1i7TH | B 站标题 |
| 13 | "Can people who have high cholesterol levels stop taking statin medication when their cholesterol levels come down naturally?" | https://www.quora.com/Can-people-who-have-high-cholesterol-levels-stop-taking-statin-medication-when-their-cholesterol-levels-come-down-naturally | Quora |
| 14 | "My doctor said I have high cholesterol and prescribed me a drug. Should I just avoid the drug and eat better and exercise more?" | https://www.quora.com/My-doctor-said-I-have-high-cholesterol-and-prescribed-me-a-drug-Should-I-just-avoid-the-drug-and-eat-better-and-exercise-more | Quora |
| 15 | "Can I avoid taking a statin if my cholesterol is borderline with my HDL at 59? My cholesterol level is 232." | https://www.quora.com/Can-I-avoid-taking-a-statin-if-my-cholesterol-is-borderline-with-my-HDL-at-59-My-cholesterol-level-is-232 | Quora |
| 16 | "How long does it take for high cholesterol to cause damage?" | https://www.quora.com/How-long-does-it-take-for-high-cholesterol-to-cause-damage | Quora |
| 17 | "How fast can cholesterol levels change?" | https://www.quora.com/How-fast-can-cholesterol-levels-change | Quora |
| 18 | "My doctor didn't offer me an alternative to lowering my cholesterol, besides pills. As a result, I ripped off the prescription. Was that a bad decision?" | https://www.quora.com/My-doctor-didnt-offer-me-an-alternative-to-lowering-my-cholesterol-besides-pills-As-a-result-I-ripped-off-the-prescription-Was-that-a-bad-decision | Quora |
| 19 | "Are eggs good or bad for cholesterol?" | https://www.youtube.com/watch?v=yAuSs-4hXa4 （BHF） | YouTube 标题 |
| 20 | "Is High LDL Cholesterol Actually Dangerous?" | https://www.youtube.com/watch?v=AhxiWLkOtP0 （Doctor Alex，19.6 万） | YouTube 标题 |
| 21 | "Normal Cholesterol But Still Getting Heart Disease? Here's Why" | https://www.youtube.com/watch?v=F7n4duUjplQ （Mark Hyman，36 万） | YouTube 标题 |

**归并后的高频问题**（中英共有）：①要不要吃药 / 多高才吃；②他汀伤不伤肝、副作用大不大；③吃了能不能停；④鸡蛋能不能吃；⑤不吃肉 / 很瘦为什么也高；⑥只靠饮食运动行不行；⑦「正常」了为什么还会得病；⑧斑块是什么、稳不稳定；⑨「血稠」是什么（中文特有）。「HDL 越高越好吗」本次没有找到原话出处，只有研究（误解 10）。

## 3. 流行误解清单

可靠度：高 = RCT / 荟萃 / 监管；中 = 大型观察性；低 = 媒体或个别医生说法。

| # | 谣言 | 真相要点 | 出处（原文短引） | 可靠度 | 状态 |
|---|---|---|---|---|---|
| 1 | 他汀伤肝、副作用一大堆 | 双盲 RCT 荟萃：说明书列出的 66 种副作用，只有 4 种有证据（另加已知的肌肉症状和糖尿病风险）。肝功能**化验**异常约多 0.1%，**没有**带来更多肝炎或肝衰竭。肌肉症状约 1% 可归因于他汀，且只在第一年 | Reith C et al. (CTT). Assessment of adverse effects attributed to statin therapy in product labels: a meta-analysis of double-blind randomised controlled trials. *Lancet* 2026. doi:10.1016/S0140-6736(25)01578-8（经 ScienceDaily 2026-02 新闻稿转述：「a small rise of about 0.1% in abnormal liver blood test results」「did not translate into higher rates of serious liver conditions such as hepatitis or liver failure」「Only about 1% of people experienced muscle symptoms attributable to statin therapy during the first year」）https://sciencedaily.com/releases/2026/02/260212025550.htm 。另有报道质疑该研究的透明度（MedShadow，未读原文） | 高（IPD 荟萃，19 项安慰剂对照 RCT，123,940 人；数字取自新闻稿，**原文未读**） | 已证实；有程度上的争议（数据透明度） |
| 1b | 副作用全是心理作用 / 完全没副作用 | 两头都不对。N-of-1 试验提示存在明显的反安慰剂（nocebo）效应，但也有少数人确有副作用；高强度他汀的肝酶异常有剂量依赖，糖尿病风险轻度增加 | Wood FA et al. N-of-1 Trial of a Statin, Placebo, or No Treatment to Assess Side Effects. *NEJM* 2020. doi:10.1056/NEJMc2031173（摘要无数字，**具体数字未查到**；记忆中：安慰剂期症状约为他汀期的 90%，未证实）。综述：*Harv Data Sci Rev* 2022, doi:10.1162/99608f92.abc57f1b：「support the existence of a significant nocebo effect」「up to half of the patients … were able to successfully restart statins」 | 中（小样本 N-of-1） | 已证实存在 nocebo；个体是否真不耐受要医生判断 |
| 1c | 他汀伤肾 | 本次未查到专门证据。CTT 2026 只提到安慰剂对照中「changes in urine」超额 <0.1%，在强化 vs 常规对照中未被证实 | 同上 ScienceDaily 转述 | 低（间接） | 尚不清楚（本次未查） |
| 2 | 「是药三分毒」，能不吃就不吃 | 不是事实陈述，是价值判断。可讲的是：益处和风险都要换成**同一张图上的绝对数字**比较（第 5 节）。CTT 2019：他汀或更强方案使主要血管事件下降 21%（RR 0.79），各年龄段都有效 | CTT. Efficacy and safety of statin therapy in older people… *Lancet* 2019. doi:10.1016/S0140-6736(18)31942-1：「statin therapy … produced a 21% (RR 0·79, 95% CI 0·77-0·81)」 | 高 | — |
| 3 | 化验单在「参考范围」内就不用管 | 化验单参考范围不等于个人目标值；目标取决于风险分层（是否有冠心病、糖尿病等）。本角度未取指南原文，**数值请以指南角度的研究员为准** | 未查到（本角度未读《中国血脂管理指南 2023》原文） | — | 需由指南角度补证 |
| 4 | 只靠饮食就能降下来，不用吃药 | 本次没读饮食干预的一手资料。知乎医生文章普遍说：轻度升高且无其他危险因素的人可先改生活方式；已有心脑血管病的人不能只靠饮食 | 知乎专栏（医生撰写，非一手）https://zhuanlan.zhihu.com/p/168721070 | 低 | 需补证（Portfolio diet 等未查） |
| 5 | 吃鸡蛋会让胆固醇高 | 本次没读一手研究。知乎文章引用「内源性胆固醇约占 70%–85%」，但另一篇文章说指南建议高血脂者每日胆固醇 <200–300 mg，两种说法并存 | 知乎 https://zhuanlan.zhihu.com/p/665090522 等（非一手） | 低 | 有争议（本次未核实一手证据） |
| 6 | 深海鱼油能「通血管」、预防心脏病 | Cochrane 2020：长链 ω-3（多数为胶囊）对全因死亡 RR 0.97（0.93–1.01）、心血管事件 RR 0.96（0.92–1.01），高确定性证据「很少或没有效果」；甘油三酯降约 15%。另一荟萃：ω-3 补充剂使**房颤风险上升** HR 1.25（1.07–1.46），>1 g/天时 HR 1.49 | Abdelhamid AS et al. Omega-3 fatty acids for the primary and secondary prevention of cardiovascular disease. *Cochrane* 2020. doi:10.1002/14651858.CD003177.pub5；Gencer B et al. *Circulation* 2021. doi:10.1161/CIRCULATIONAHA.121.055654：「marine ɷ-3 supplementation was associated with an increased risk of AF」 | 高 | 已证实（普通鱼油不「通血管」）；处方级高纯度 EPA（如 REDUCE-IT）有争议，**本次未查** |
| 7 | 纳豆激酶能溶解血栓、通血管 | 纳豆激酶在体外有溶栓活性（学术综述）；**没找到**它能在人体内消退动脉粥样硬化斑块的 RCT，也没找到官方辟谣原文 | 检索结论（WebSearch 只返回综述与商品页） | 低 | 尚不清楚（未查到人体硬终点证据） |
| 8 | 换季输液「冲血管」「疏通血管」 | 输液药物多为扩血管、改善微循环制剂，碰不到动脉壁里的斑块；输液后的「轻松感」可能来自血容量增加；有老人输液后擅自停抗血小板药或降压药，反而增加风险；过量输液加重心脏负担 | 中国新闻网 2026-02-02 https://www.chinanews.com.cn/jk/2026/02-02/10563632.shtml ；扬子晚报 2026-10-27 https://www.yzwb.net/news/jk/202610/t20261027_406871.html ；中华网 2026-08-07（均为检索摘要，正文未读） | 低–中（医生访谈；机制合理但无 RCT） | 主流共识 |
| 9 | 「洗血」（血脂净化）一次就干净，不用吃药 | 血浆置换 / 双重滤过类治疗只用于少数严重、遗传性高胆固醇患者，在饮食和多种药物无效后才考虑；效果只维持约一周到一个月；可能有低血压、心律不齐、发麻抽筋 | TVBS 健康（台湾长庚医院医生访谈）https://health.tvbs.com.tw/nutrition/351698 ；SCMP 2024 报道中国专家对「血液净化」热潮的担忧 https://scmp.com/news/people-culture/gender-diversity/article/3251230/ （均为检索摘要） | 低–中（媒体访谈，非指南） | 主流共识；需指南原文补证 |
| 10 | HDL（「好胆固醇」）越高越好 | 丹麦两个前瞻队列（男 52,268、女 64,240）：极高 HDL 反而与全因死亡升高相关，男性 HDL 2.5–2.99 mmol/L（≈97–116 mg/dL）HR 1.36（1.09–1.70） | Madsen CM et al. Extreme high high-density lipoprotein cholesterol is paradoxically associated with high mortality… *Eur Heart J* 2017. doi:10.1093/eurheartj/ehx163 | 中（观察性，不能证明因果） | 已证实「不是越高越好」这一关联；因果尚不清楚 |
| 11 | 胆固醇降得越低越容易得癌 | CTT 27 项他汀 RCT、17.5 万人：中位 5 年治疗对任何癌症的发病和死亡都无影响，癌症死亡 RR 1.00（0.93–1.08） | CTT. Lack of effect of lowering LDL cholesterol on cancer… *PLoS One* 2012. doi:10.1371/journal.pone.0029849：「no effect on the incidence of, or mortality from, any type of cancer」 | 高（RCT 荟萃；随访中位 5 年，更长期的数据本次未查） | 已证实（5 年内） |
| 12 | 老年人胆固醇高反而长寿，不用降 | **双方都有证据**。正方：19 个队列、68,094 名 ≥60 岁老人，16 个队列中 LDL 与全因死亡呈反向关联（Ravnskov 2016，观察性，可能受「生病导致胆固醇降低」的反向因果影响——此解释为本文推断，未查到来源）。反方：CTT 2019 RCT 荟萃显示他汀获益「irrespective of age」，但「less direct evidence of benefit among patients older than 75 years」无血管病者，正在由新试验补充 | Ravnskov U et al. *BMJ Open* 2016. doi:10.1136/bmjopen-2015-010401：「High LDL-C is inversely associated with mortality in most people over 60 years」；CTT *Lancet* 2019（同上） | 正方中（观察性）；反方高（RCT），但 >75 岁一级预防证据少 | **有争议**：>75 岁且无血管病者是否获益，尚不清楚 |
| 13 | 「血稠」= 血脂高，喝水 / 输液能稀释 | 「血稠」不是血脂化验指标，中文网络把血脂高、血液黏稠度混用（如「血脂高、血液太浓」34.4 万播放）。本次未查到权威定义 | 未查到权威出处 | — | 尚不清楚（需补证） |
| 14 | 红曲米可替代他汀 | 本次未查。B 站医生视频（BV1AP4y1i7TH）专门谈此问题，内容未看 | 未查到 | — | 需补证 |

## 4. 平台规则（决定免责声明与措辞边界）

### 4a. YouTube

| 规则 | 原文要点 | 对我们 |
|---|---|---|
| 医疗错误信息政策 https://support.google.com/youtube/answer/13813322 | 「doesn't allow content that poses a serious risk of egregious harm by spreading medical misinformation that contradicts local health authority (LHA) guidance about specific health conditions and substances」。分两类：Prevention misinformation 与 Treatment misinformation | 我们按指南讲，不冲突 |
| 治疗类示例 | 示例集中在 MMS、黑药膏、松节油、杏仁核、高浓度双氧水，以及癌症替代疗法（「Content that promotes diet and exercise instead of seeking approved treatment for cancer」）、堕胎和婴儿配方奶。**页面上没有他汀或降脂药的示例** | 「别吃他汀」类内容并不在明文列举中，这能部分解释英文区反他汀片的流量 |
| EDSA 例外 | 「We may allow content that violates the misinformation policies … if that content includes additional context in the video, audio, title, or description」；「This is not a pass to promote misinformation」；可「condemn, dispute, or satirize misinformation」 | **我们在片中让凯说出谣言再驳倒，属于 dispute；必须在同一片内给出卫生机构或专家的反驳和出处** |
| 健康来源标签 https://support.google.com/youtube/answer/12796915 | 只对美、英、德、巴西、印尼、日、法、韩、加、墨开放申请；个人须持有医生、护士、心理师、婚姻家庭治疗师、临床社工执照，须证明「oversight and review of the content」；频道 12 个月内公开观看时长 >1,500 小时（或 90 天 Shorts 播放 150 万），主要内容为健康信息，无社区准则警告；药企、保险、器械公司的频道不能申请；执照由 LegitScript 核验；审核约 1–2 个月 | **我们的频道拿不到这个标签**（除非与持照医生合作并由其审核）。不要在片中暗示自己是权威来源 |

### 4b. 中国大陆（B 站 / 抖音）

| 规则 | 原文要点 | 对我们 |
|---|---|---|
| 中央网信办秘书局、国家卫健委办公厅、市场监管总局办公厅、国家中医药局综合司《关于规范「自媒体」医疗科普行为的通知》（2025-07-28 印发，08-01 公开）https://www.cac.gov.cn/2025-08/01/c_1755764425442686.htm | 定义：「医疗科普行为是以提高公众的医学健康科学素养为目的，通过文字、图片、音视频等形式，生产传播预防或治疗疾病等相关知识的行为。」「严禁无资质账号生产发布专业医疗科普内容。」「对新注册的『自媒体』账号，不经医疗资质认证，不得生产发布专业医疗科普内容。」存量未认证账号「2 个月内完成资质认证」 | **最关键的约束**。通知**没有定义「专业医疗科普内容」的边界**，无资质账号能讲到什么程度没有明文。保守理解：没有医疗资质的账号，不应给诊断、用药、剂量、停药建议 |
| 同一通知：标注要求 | 「借助人工智能技术生成合成医疗科普信息……需严格标注信息来源或生成合成内容标识」；「结合医疗领域素材摆拍剧情」也要标注；「不得随意拼接发布不准确信息」 | **我们是 AI 视频＋剧情化**，两条都踩中：每期必须标「AI 生成合成」，片尾列信息来源 |
| 同一通知：广告 | 「不得以介绍健康、养生知识等形式，变相发布医疗、药品、医疗器械、保健食品……广告」；同页不得出现购物链接 | 不接鱼油、纳豆激酶、检测仪等商单，不挂链接 |
| 同一通知：处置 | 「取消互动功能、清理粉丝、取消营利权限、禁言、关闭等梯度措施」；资质需「通过国家卫生健康委官方信息查询渠道进行查验比对」 | 风险是封号级 |
| B 站职业资质认证 2.0（认证小助手，据检索摘要称 2026-01-20 更新）https://www.bilibili.com/opus/659053218220736529 | 个人认证；「认证领域需与稿件内容一致」；医疗领域「因缺少从业信息暂不支持资质外显」，显示为「医学学历」（检索摘要，原页未读） | 需要确认：本账号若无医学认证，在 B 站发血脂内容是否会被限流。**本次未查到 B 站针对医疗类内容的专门公告** |
| 抖音 | 2025 Q1 新版《社区医疗健康公约》，修订 12 处，治理范围从「医疗」扩展到「医疗与泛健康」；截至 2025-07 清理资质造假医生 683 名、低质同质化视频 50 万条以上（科技日报 2025-08-19 https://www.stdaily.com/web/gdxw/2025-08/19/content_387403.html ）。2026-01：认证医疗创作者 7.8 万；5–10 分钟深度视频条均播放增长近 60%（新华网 2026-02-02，平台自述）https://www.news.cn/tech/20260202/c5cbe0dc36924bd0b44b8a0cf046a8b6/c.html | 「泛健康」也纳入治理；公约原文未查到 |

**落到片子上的措辞边界**（据以上规则的推论，非法律意见）：
1. 不给具体药名＋剂量、不说「可以停药 / 不用吃药」、不替观众判断「你该不该吃」。只讲「医生会根据哪些因素决定」。
2. 每期片头或片尾固定字幕：「本片为科普，不能替代医生诊疗。用药、停药请遵医嘱」＋「画面含 AI 生成合成内容，结构为示意」＋信息来源（指南、论文）。
3. 最稳妥的路径：**与有资质的医生（心内科 / 内分泌科）合作审稿并署名**，以满足网信办通知；YouTube 的健康来源标签也只对持照者开放。这一点需用户决定，本角度只指出风险。

## 5. 形式证据

| 发现 | 出处 | 可靠度 | 对我们的含义 |
|---|---|---|---|
| 叙事（故事）类健康信息对态度、意图、行为的说服效应很小但显著：r = .063（25 项研究，N = 9,330）；**音频和视频叙事有效，印刷叙事无效**；倡导「检测、预防」行为的叙事有效，倡导「戒除」的无效 | Shen F, Sheer VC, Li R. Impact of Narratives on Persuasion in Health Communication: A Meta-Analysis. *J Advertising* 2015;44(2):105–113. doi:10.1080/00913367.2015.1018467（数字来自检索摘要，全文未读） | 中 | 视频形式是对的；「去体检、查血脂」这类检测行为正好在有效区间；但效应小，不能靠剧情代替信息 |
| 叙事证据和统计证据的说服力**没有显著差别**（50 项研究、65 对实验、N = 13,113；r = 0.016，95% CI −0.014 至 0.045），健康与非健康情境都一样 | Xu J. A Meta-Analysis Comparing the Effectiveness of Narrative vs. Statistical Evidence: Health vs. Non-Health Contexts. *Health Commun* 2023;38(14):3113–3123. doi:10.1080/10410236.2022.2137750 | 高（荟萃） | **两者都要**：凯的处境（故事）承载问题，林给出数字 |
| 健康叙事里用第一人称视角，能小幅提高感知易感性（d = 0.10）和认同（d = 0.10） | Chen M, Bell RA. *Psychol Health* 2022;37(5):545–562. doi:10.1080/08870446.2021.1894331 | 中（k = 16） | 凯说「我的体检单」而不是「有个人」 |
| 恐惧诉求总体有效：127 篇文章、248 个独立样本、N = 27,372，综合效应 d = 0.29 | Tannenbaum MB et al. Appealing to fear. *Psychol Bull* 2015. doi:10.1037/a0039729：「fear appeals are effective at positively influencing attitude, intentions, and behaviors」 | 高 | 恐惧有效，但本次摘要里**没有读到**「何时适得其反」的调节条件（记忆中：需同时给出效能信息，如可做的事；未证实）。保守做法：每个吓人的画面（斑块破裂）后紧跟「可以做什么」 |
| 统计素养：「把乳腺癌死亡风险降低 25%」实际意味着「1000 名女性中少死 1 人」；建议用绝对风险代替相对风险，用自然频数代替条件概率 | Gigerenzer G et al. Helping Doctors and Patients Make Sense of Health Statistics. *Psychol Sci Public Interest* 2007;8(2). doi:10.1111/j.1539-6053.2008.00033.x：「absolute risks instead of relative risks」「natural frequencies instead of conditional probabilities」 | 高（权威综述） | **他汀益处和副作用都必须用「每 100 / 1000 人中多少人」说**，不说「降低 21%」 |
| 自然频数比概率更容易被理解（SMD 0.69）；35 项研究、83 组比较 | Akl EA et al. Using alternative statistical formats for presenting risks and risk reductions. *Cochrane* 2011. doi:10.1002/14651858.CD006776.pub2：「Natural frequencies are probably better understood than probabilities」 | 高 | 画面用人群图（100 个小人，几个变色） |

图标阵列（icon array）对理解的专门研究本次未查（记忆中：Galesic & Garcia-Retamero 等研究支持，未证实）。

## 给视频的建议

**最值得讲的点**
1. **「他汀伤肝」**：中文区最高频的问题（知乎问题原话「降脂药对肝有损伤吗？」）。有 2026 年 CTT 双盲 RCT 荟萃可讲：肝功能化验异常约多 0.1%，但不增加肝炎和肝衰竭；肌肉症状约 1%，只在第一年。要讲成「化验单上的数会动，但肝不会因此坏掉」，并保留「高剂量更明显、个别人确实不耐受、要复查」的限定。
2. **「瘦人、不吃肉为什么也高」**：中文区唯一的百万播放（大物是也）就是这个切口。机制（肝脏自己合成、遗传）由机制角度补数字。
3. **鱼油不「通血管」**：Cochrane 2020 高确定性证据显示，对死亡和心血管事件「很少或没有效果」；补充剂还与房颤风险上升相关。这是反直觉、有硬证据、和观众钱包直接相关的点。
4. **风险怎么讲**：用 Gigerenzer 的绝对风险和自然频数（「100 个像你一样的人里……」），这本身就可以是一期的画面核心。

**最容易讲错的地方**
- 把「老年人胆固醇高更长寿」直接判为谣言：这是**有争议**的。观察性研究（Ravnskov 2016）支持反向关联；RCT 显示他汀获益不分年龄，但 >75 岁且无血管病的人直接证据少（CTT 2019 原话）。片中要并列两方，说「这个年龄段要和医生个别讨论」。
- 把「副作用都是心理作用」讲成定论。nocebo 存在，但确有少数人真有副作用。
- 用「降低 21%」这种相对风险，或者只讲获益的绝对值、不讲副作用的绝对值（或者反过来）。两者要用同一种格式、放在同一张图上。
- 「HDL 是好胆固醇，越高越好」：极高 HDL 与死亡率升高相关（观察性）。片中慎用「好 / 坏胆固醇」，或者用了马上加限定。
- 给剂量、给停药建议：网信办通知明确禁止无资质账号发「专业医疗科普内容」。

**可以怎么画**
- 3D 进动脉已经是 Nucleus 以来的标准画面，也被大量模板号复制，**不稀缺**。差异化靠：真实比例（LDL 颗粒、内皮细胞、斑块厚度，数值由机制角度提供）、人物在管腔里的视角、角标「示意」。
- 风险画面用 100 人图标阵列，变色的小人代表绝对风险。
- 谣言节拍：凯念出真实标题（如「换季输液冲血管」），林用画面说明药液顺着血流经过、碰不到管壁里的斑块（这是示意，需标注），然后给出处。符合 YouTube EDSA「dispute」例外，前提是同一片内给出反驳和来源。
- 斑块破裂、血管堵死这类画面自带恐惧（B 站热评「太可怕了血管就这么被堵死了」）。按 Tannenbaum 的结果，恐惧有效，但每个吓人镜头后要马上接「可以做什么」（检测、找医生）。

**观众最可能的误解**
- 「化验单没有箭头就没事」（参考范围不等于个人目标，需指南角度给数）。
- 「一吃他汀就终身离不开、肝会坏」。
- 「鱼油、纳豆激酶、输液、洗血能清血管」。
- 「血稠 = 血脂高」。

**合规清单（每期固定）**：AI 生成合成标识；「科普不能替代诊疗，用药停药遵医嘱」；片尾或简介列出指南与论文出处；不接健康产品商单、不挂链接；建议找持证医生审稿署名（需用户决定）。
