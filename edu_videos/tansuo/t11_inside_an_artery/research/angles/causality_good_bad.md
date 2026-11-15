---
worker_id: researcher-02-causality
stage: 3
role: researcher
angle: causality-good-bad
status: partial
blockers:
  - "PubMed 网页（pubmed.ncbi.nlm.nih.gov）对抓取返回 cookie 页，NEJM 返回 403；NEJM 论文摘要改用 Europe PMC / 学术机构库 / 搜索摘要核对，部分数字只到二手摘要层（已逐条标可靠度）"
  - "HDL 升高药物试验（ILLUMINATE、dal-OUTCOMES、ACCELERATE、REVEAL、AIM-HIGH、HPS2-THRIVE）未读到各自原文摘要，只读到 2022 综述（Biomedicines）的转述；HR、CI 等精确数字未查到"
  - "Domanski 2020 JACC（胆固醇累积暴露）Europe PMC 抓取超时，只读到搜索摘要转述的摘要数字"
  - "ESC/EAS、ACC/AHA 指南原文中关于 ApoB / 非 HDL-C 的推荐措辞未读（且属其他研究员的指南角度）"
  - "Lp(a) 中国人群分布只查到 UK Biobank 华人中位数，未查中国本土队列；Lp(a) 每颗粒致动脉粥样硬化性约为 LDL 的若干倍——未查到出处数字"
  - "KETO-CTA 撤稿通知原文未读，撤稿原因只来自作者本人 Substack；主流对 LMHR 的批评只查到博客类，未查到同行评审社论"
  - "饮食胆固醇的证据本角度未展开（属饮食角度研究员）"
confidence: medium
---

# LDL 到底「坏」在哪、HDL 是不是「好」——因果证据链与争议

> 写作范围：因果证据、指标区别、HDL 争议、TG / 残粒 / Lp(a)、怀疑派。**不含**他汀副作用、饮食细节、指南目标值。
> 单位换算：LDL-C / HDL-C 的 mg/dL ÷ 38.67 = mmol/L。原文只给一种单位时，另一种是本研究员换算的，标「≈」。Lp(a) 的 mg/dL 与 nmol/L **不能**简单换算（见 §4）。
> 资料获取说明：PubMed 网页与 NEJM 抓取被拦，多数摘要改从 Europe PMC REST 接口读取（同一 PubMed 记录）。

## 0. 一句话结论（给编剧）

| 问题 | 现状 | 证据等级 |
|---|---|---|
| LDL 会导致动脉粥样硬化性心血管病（ASCVD）吗？ | **已证实**：基因、队列、孟德尔随机化、RCT 四条证据链一致 | 高 |
| 越低越好？ | 在已有心血管病人群中，降到约 0.5 mmol/L（≈19 mg/dL）以下仍见获益，2.2 年内未见安全信号 | 高（RCT 预设二次分析），长期仍在积累 |
| 「LDL × 年数」重要吗？ | **已证实方向**：暴露越久风险越高；年轻时的累积暴露权重更大（单队列） | 中-高 |
| HDL 是「好胆固醇」吗？ | 观察性相关存在，但升 HDL 药物与基因研究都没证明「升 HDL 本身保护心脏」；极高 HDL 反而与死亡率升高相关。**HDL-C 更像风险标记，不是治疗靶点** | 高（否定性证据） |
| ApoB 比 LDL-C 更准？ | 多数人两者一致；在高甘油三酯、糖尿病、代谢综合征时可能不一致，此时颗粒数（ApoB）更能反映风险 | 中-高（有争议的是临床是否要常规替换） |
| Lp(a) 是因果吗？降它有用吗？ | 基因证据强烈支持因果；但**首个大型降 Lp(a) 结局试验（Lp(a)HORIZON，pelacarsen）2026 年 11 月公布：未减少心血管事件** | 因果：高；「降 Lp(a) 有益」：**尚不清楚 / 首个试验阴性** |
| 「瘦体型高反应者（LMHR）不怕高 LDL」？ | 证据薄弱：小样本、无对照；2025 年纵向论文已于 2026 年**撤稿** | 低 |

---

## 1. LDL 致病的因果证据链

### 1.1 EAS 共识声明（2017、2020）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 证据规模 | >200 项前瞻性队列，>200 万人，>2000 万人年随访，>15 万次心血管事件 | Ference BA 等, *Low-density lipoproteins cause atherosclerotic cardiovascular disease. 1. Evidence from genetic, epidemiologic, and clinical studies.* Eur Heart J 2017;38(32):2459-2472. doi:10.1093/eurheartj/ehx144（PMC5837225） | "including more than 2 million participants with over 20 million person-years of follow-up" | 高（多来源证据综合的共识） |
| 结论 | LDL 是 ASCVD 的原因 | 同上 | "unequivocally establishes that LDL causes ASCVD" | 高 |
| 剂量关系 | LDL 与风险呈对数线性、剂量依赖 | 同上 | "a remarkably consistent dose-dependent log-linear association" | 高 |
| 时间与剂量都要紧 | 风险随暴露量和**暴露时长**增加 | 同上 | "this effect appears to increase with increasing duration of exposure to LDL-C" | 高 |
| 他汀试验：每降 1 mmol/L（≈38.7 mg/dL） | 主要心血管事件相对降低 22%（中位约 5 年） | 同上，RCT 证据节 | "a log-linear 22% proportional reduction in the risk of major cardiovascular events" | 高（RCT 荟萃） |
| 终生低 LDL（孟德尔随机化）：每低 1 mmol/L | 40 年暴露估计事件降低约 50–55%（表 2 脚注用 54%） | 同上，孟德尔随机化节 | "~50–55% per millimole per litre lower LDL-C" | 中-高（MR 推算） |
| 早降、久降效果更大 | 长期低 LDL 相比晚年开始的短期他汀，相对获益最多可达 3 倍 | 同上 | "up to a three-fold greater proportional reduction" | 中-高 |
| 核心概念 | 「累积 LDL 动脉负担」是决定因素 | 同上，Box 1 | "Cumulative LDL arterial burden is a central determinant" | 高（共识表述） |
| 进入血管壁的颗粒大小 | 直径 <70 nm 的含 ApoB 脂蛋白（LDL、VLDL 残粒、IDL、Lp(a)）可自由进出动脉内膜 | 同上，病理生理节 | "<70 nm in diameter" | 高（机制） |
| 发病起点 | 富含胆固醇的含 ApoB 脂蛋白在动脉内膜**滞留并累积** | 同上 | "the retention and accumulation of cholesterol-rich apoB-containing lipoproteins within the arterial intima" | 高 |
| 风险很低的水平 | 约 0.5–1.0 mmol/L（20–40 mg/dL）时风险低；不是一个硬阈值，滞留随 LDL 升高而剂量依赖地增加 | 同上 | "in a dose-dependent manner" | 中-高 |
| 前提条件 | 降 LDL 的获益需没有「脱靶有害作用」；举例：CETP 抑制剂 evacetrapib 降了 LDL-C 却没减少事件 | 同上 | "provided that there are no competing deleterious off-target effects" | 高 |

2020 年第二份 EAS 共识（Borén J 等, *…pathophysiological, genetic, and therapeutic insights*, Eur Heart J 2020;41(24):2313-2330, doi:10.1093/eurheartj/ehz962, PMC7308544）补充了机制（可直接用于画面）：

| 机制步骤 | 原文短引 | 可靠度 |
|---|---|---|
| 穿越内皮：最大约 70 nm 的含 ApoB 脂蛋白经「胞吞转运」通过内皮细胞 | "LDL transcytosis occurs through a vesicular pathway, involving caveolae" | 高（机制） |
| 被「粘住」：ApoB100 与动脉壁蛋白聚糖结合，是致动脉粥样硬化的关键 | "the atherogenicity of LDL is linked to the ability of its apoB100 moiety to interact with arterial wall proteoglycans" | 高 |
| 选择性滞留 | "mainly due to selective retention of LDL in the intima" | 高 |
| 单核细胞变巨噬细胞、进一步氧化 LDL、变成泡沫细胞 | "Newly recruited monocytes differentiate into macrophages that can further promote the oxidation of LDL particles" / "giving rise to cholesterol-laden foam cells" | 高 |
| 降 LDL 可使斑块稳定、部分消退；LDL-C <1.3 mmol/L（50 mg/dL）者更多为纤维斑块、纤维帽更厚 | "those with LDL-C levels <1.3 mmol/L (50 mg/dL) were more likely to have fibrous plaque and thick fibrous caps" | 中-高（影像研究） |
| 降 LDL 对「斑块侵蚀」机制作用较弱 | "indicating that LDL lowering is less efficient in counteracting erosion mechanisms" | 中 |
| LDL 的正常功能：主要的胆固醇运输者，也运维生素 E、类胡萝卜素、泛醇 | "LDL is also the major carrier of vitamin E, carotenoids, and ubiquinol" | 高 |

### 1.2 天然的「终生低 LDL」实验：PCSK9 功能缺失突变（Cohen 2006）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 人群 | ARIC 研究 3363 名黑人、9524 名白人，随访 15 年 | Cohen JC 等, *Sequence variations in PCSK9, low LDL, and protection against coronary heart disease.* N Engl J Med 2006;354(12):1264-1272. doi:10.1056/NEJMoa054013 | "over a 15-year interval in the Atherosclerosis Risk in Communities study" | 高（前瞻队列中的遗传自然实验） |
| 黑人携带无义突变 | 2.6%；LDL-C 低 28%；冠心病风险低 88%（HR 0.11，95%CI 0.02–0.81） | 同上 | "an 88 percent reduction in the risk of CHD" | 高（但事件少、CI 宽） |
| 白人携带另一序列变异（3.2%） | LDL-C 低 15%；冠心病风险低 47%（HR 0.50，95%CI 0.32–0.79） | 同上 | "a 47 percent reduction in the risk of CHD" | 高 |
| 摘要未给 mg/dL 绝对值；白人变异名（R46L）摘要中未出现 | — | — | 未查到（记忆中：R46L，未证实） | — |

**要点**：LDL 只低 15–28%，冠心病风险却低 47–88%——比他汀几年试验的效果大得多。合理解释是「从出生就低」，即累积暴露（§1.4）。这正是 PCSK9 抑制剂药物研发的起点（EAS 2017 也引用 PCSK9 功能缺失→LDL 低→终生风险显著低；功能获得→LDL 显著升高）。

### 1.3 反方向的天然实验：家族性高胆固醇血症（FH）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 杂合子 FH 患病率 | 1/200–1/300（EAS）；CDC 写约 1/311（各来源估计不同，另见 1/250、1/220） | EAS 2017（同上）；CDC *About Familial Hypercholesterolemia*，https://www.cdc.gov/heart-disease-family-history/about/about-familial-hypercholesterolemia.html | "between 1:200 and 1:300 people worldwide" / "affects about 1 in 311 people" | 高（患病率估计因人群不同） |
| 未治疗杂合子 LDL-C | 4.5–12 mmol/L（≈174–464 mg/dL） | EAS 2017 | — | 高 |
| 纯合子 FH | 常从出生起 >13 mmol/L（≈>500 mg/dL），几乎都在儿童或青少年早期发生 ASCVD | EAS 2017 | "almost universal development of ASCVD in childhood or early adolescence" | 高 |
| 未治疗的心梗发生 | 男性 50 岁前 50%，女性 60 岁前 30% | CDC 同上 | "heart attacks happen in 30% of women with FH by age 60 and 50% of men with FH by age 50" | 中-高（权威机构科普，引自队列） |
| 早发现早治疗 | 冠心病风险降低约 80% | CDC 同上 | "can reduce your risk of coronary artery disease by about 80%" | 中（机构科普，未回溯原研究） |
| 提示信号 | 成人 LDL-C >190 mg/dL（≈4.9 mmol/L），儿童 >160 mg/dL（≈4.1 mmol/L） | CDC 同上 | — | 中-高 |

### 1.4 累积暴露（「LDL × 年数」/ 胆固醇年）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| CARDIA 队列：18–30 岁入组的 4958 名无症状成人，40 岁后中位随访 16 年，275 例心血管事件 | 18–40 岁 LDL-C 曲线下面积平均 2520.6 ± 577.7 mg/dL×年（≈65.2 mmol/L×年）；每 100 mg/dL×年 HR 1.053 | Domanski MJ 等, *Time Course of LDL Cholesterol Exposure and Cardiovascular Disease Event Risk.* J Am Coll Cardiol 2020;76(13):1507-1516. doi:10.1016/j.jacc.2020.07.059（PMID 32972526） | 本次未读到原文（抓取超时），数字来自搜索摘要转述 | 中（单队列观察性；数字二手） |
| 时间点 | 同样的累积量，**年轻时攒的**风险增幅更大；18–30 岁累积暴露 HR 1.279（95%CI 1.104–1.483） | 同上 | 同上 | 中 |

与 EAS「累积 LDL 动脉负担」概念一致。适合讲成「血管记账本」，但注意：这是观察性研究，「早降获益更大」主要靠孟德尔随机化推算，尚无从 20 岁开始的长期 RCT。

### 1.5 越低越好？及安全下限

| 试验 | 人群 / 设计 | LDL-C | 结果 | 出处 | 可靠度 |
|---|---|---|---|---|---|
| IMPROVE-IT（依折麦布＋辛伐他汀 vs 辛伐他汀） | 18,144 例急性冠脉综合征后患者 | 时间加权中位 53.7 mg/dL（1.4 mmol/L）vs 69.5 mg/dL（1.8 mmol/L） | 7 年主要终点 32.7% vs 34.7%；HR 0.936（95%CI 0.887–0.988，p=0.016），相对降低约 6%、绝对约 2 个百分点 | Cannon CP 等, *Ezetimibe Added to Statin Therapy after Acute Coronary Syndromes.* N Engl J Med 2015. doi:10.1056/NEJMoa1410489（PMID 26039521）；原文抓取被拦，数字经搜索摘要核对 | 高（RCT），数字层面中-高 |
| FOURIER（evolocumab，PCSK9 抑制剂） | 27,564 例已有 ASCVD、他汀治疗中、LDL-C ≥70 mg/dL | 中位 92 mg/dL（2.4 mmol/L）→ 30 mg/dL（0.78 mmol/L），降 59% | 主要终点 9.8% vs 11.3%，HR 0.85（95%CI 0.79–0.92）；关键次要终点 HR 0.80（0.73–0.88）；中位随访 2.2 年；不良事件除注射部位反应（2.1% vs 1.6%）外无显著差异 | Sabatine MS 等, *Evolocumab and Clinical Outcomes in Patients with Cardiovascular Disease.* N Engl J Med 2017;376(18):1713-1722. doi:10.1056/NEJMoa1615664；经 Duke Scholars 摘要记录核对 https://scholars.duke.edu/individual/pub1353329 | 高（RCT） |
| FOURIER 极低 LDL 预设二次分析 | 4 周时 2669 人（10%）LDL-C <0.5 mmol/L（≈<19 mg/dL） | 分层：<0.5 / 0.5–<1.3 / 1.3–<1.8 / 1.8–<2.6 / ≥2.6 mmol/L | LDL 越低事件越少，单调关系一直延伸到 <0.2 mmol/L（≈<8 mg/dL）；达到的 LDL-C 与严重不良事件及其他 9 项预设安全事件无显著关联（中位 2.2 年） | Giugliano RP 等, *Clinical efficacy and safety of achieving very low LDL-cholesterol concentrations with the PCSK9 inhibitor evolocumab…* Lancet 2017;390(10106):1962-1971. doi:10.1016/S0140-6736(17)32290-0 | 高（但为非随机分层的二次分析；随访短） |

原文短引：FOURIER "from a median baseline value of 92 mg per deciliter (2.4 mmol per liter) to 30 mg per deciliter (0.78 mmol per liter)"；Giugliano "no safety concerns with very low LDL-cholesterol concentrations over a median of 2·2 years"。

**限定条件（必须讲）**：
- 「越低越好」的 RCT 证据主要在**已有心血管病或很高风险**人群；对低风险人群并不意味着都要降到极低（目标值见其他研究员）。
- 极低 LDL 的安全性数据随访只有 2.2 年（FOURIER 开放标签延伸研究本次未查）。
- 新生儿与狩猎采集人群 LDL-C 约 50–70 mg/dL（≈1.3–1.8 mmol/L）：O'Keefe JH 等, *Optimal low-density lipoprotein is 50 to 70 mg/dl: lower is better and physiologically normal.* J Am Coll Cardiol 2004. doi:10.1016/j.jacc.2004.03.046（PMID 15172426），原话 "50 to 70 mg/dl for native hunter-gatherers, healthy human neonates"。可靠度：中（综述 / 专家观点，作者立场明确）。

---

## 2. LDL-C、非 HDL-C、ApoB、LDL 颗粒数的区别

| 指标 | 测的是什么 | 比喻（建议） |
|---|---|---|
| LDL-C | LDL 颗粒里**装的胆固醇总量** | 货车里装的货有多少 |
| 非 HDL-C | 总胆固醇 − HDL-C = 所有致动脉粥样硬化颗粒（LDL、VLDL、残粒、IDL、Lp(a)）装的胆固醇 | 所有「危险车队」装的货 |
| ApoB | 每个致动脉粥样硬化颗粒**恰好一个** ApoB 分子 → ApoB = 颗粒数 | 车的数量（每辆车一个车牌） |
| LDL-P（颗粒数，核磁法） | 直接数 LDL 颗粒 | 数车 |

| 事实 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|
| 每个 LDL 颗粒一个 ApoB100 | Borén 2020（同上） | "the proteome is dominated by apoB100 (one molecule per LDL particle)" | 高 |
| 多数情况下 LDL-C 与颗粒数高度相关；代谢综合征、糖尿病、高甘油三酯时可能不一致，此时直接测 ApoB 或颗粒数更能反映致病作用 | EAS 2017 | "LDL-C concentration and LDL particle number are highly correlated" / "plasma LDL-C and LDL particle concentration can become discordant" | 高 |
| 他汀试验中，按每 mmol/L 计，LDL-C 与 ApoB 对事件的效应非常相似 → 多数情况下 LDL-C 是合格替代指标 | EAS 2017 | "LDL-C and apoB concentrations had very similar effects" | 高 |
| 小而密 LDL 多时，ApoB 升得比 LDL-C 多 | Borén 2020 图 2 注 | "Note that when small dense LDL is abundant, apoB is elevated more than LDL-C." | 高（机制） |
| 小而密 LDL（而非大 LDL）独立于 LDL-C 预测冠心病 | Borén 2020 | "concentrations of small dense LDL but not large LDL predicted incident CHD independent of LDL-C" | 中 |
| 沉积到动脉壁的胆固醇量由 ApoB 颗粒数决定；ApoB 比 LDL-C、非 HDL-C 更准确 | Sniderman AD 等, *Apolipoprotein B Particles and Cardiovascular Disease: A Narrative Review.* JAMA Cardiol 2019;4(12):1287-1295. doi:10.1001/jamacardio.2019.3780（PMC7369156） | "apoB more accurately measures the atherogenic risk" | 中（叙述性综述，作者是 ApoB 的长期倡导者） |
| 不一致人群比例：约 20%–60% | 同上（全文） | "discordant groups that range from about 20% to about 60% of the total population" | 中 |
| 甘油三酯 >1.5 mmol/L（≈133 mg/dL）后 LDL-C 会低估 LDL 颗粒数 | 同上 | "LDL-C will underestimate the number of LDL particles" | 中 |
| 正常 TG 时约每 1 个 VLDL 对应 9 个 LDL 颗粒 | 同上 | "for every VLDL particle, there are approximately 9 LDL particles" | 中 |
| LDL-C 已 <70 mg/dL 的患者中约三分之一 ApoB 明显偏高 | 同上 | "in approximately one third of patients who achieved a level of LDL C <70mg/dl, apoB was substantially higher" | 中 |
| 证据有分歧：8 个他汀试验荟萃中非 HDL-C 略优；7 个试验荟萃中获益更贴近 ApoB 下降 | 同上 | "non-HDL-C was a marginally more accurate marker of residual risk than apoB or LDL-C" | 中（**有争议**） |
| 孟德尔随机化：LPL 与 LDLR 基因评分按相同 ApoB 降幅标准化后，风险降低「非常相似」→ 真正驱动风险的是颗粒数 | 同上，引 Ference 2019 JAMA | "normalized for the same decrease in apoB" | 中-高（二手转述，原文未读） |

**状态**：「ApoB 更准」在机制和不一致人群中有较强支持；「是否应取代 LDL-C 作为常规首要指标」属指南间分歧（本次未读指南原文，见 blockers）。

---

## 3. HDL：「好胆固醇」名不副实？

### 3.1 为什么叫「好」
观察性研究中 HDL-C 低的人心血管病多（本次未单独查 Framingham 等原始数据；记忆中：Framingham 等早期队列，未证实）。HDL 参与把外周胆固醇运回肝脏（「逆向转运」）。但「相关」不等于「升高它就能保护」。

### 3.2 升 HDL 的药物试验——一个接一个失败

| 药物（试验，年） | HDL-C 变化 | 结局 | 可靠度 |
|---|---|---|---|
| Torcetrapib（ILLUMINATE，2007） | +72% | 提前终止，治疗组死亡增加约 50%；伴血压升高 | 中（综述转述） |
| Dalcetrapib（dal-OUTCOMES，2012） | +36% | 因无效提前终止 | 中 |
| Evacetrapib（ACCELERATE，2017） | 综述未给 | 因无效提前终止 | 中 |
| Anacetrapib（REVEAL，2017） | >+100%；非 HDL-C −17% | 心梗、冠心病死亡、血运重建约降 10%（显著）；综述认为可能来自非 HDL / ApoB 的下降；药物在脂肪组织蓄积，未上市 | 中 |
| 烟酸（AIM-HIGH，2011） | 治疗组 +25%，安慰剂组 +13% | 无额外获益，缺血性卒中小幅、原因不明地增加 | 中 |
| 烟酸/laropiprant（HPS2-THRIVE，2013–14） | 约 +16%；LDL-C 与 TG 约 −20% | 冠心病事件无明显减少；严重非致死不良事件增多 | 中（综述据会议报告） |

出处：Wang Lorkowski S, Smith JD. *HDL Is Not Dead Yet.* Biomedicines 2022;10(1):128（PMC8773442）。原文短引："Torceptrapib raised HDL-C by 72%, but it led to a significant increase in blood pressure"；"the trial was stopped early due to futility"。各试验原文本次未读（blockers）。另：Sniderman 2019 引 Ference 2017 JAMA："Only in the REVEAL trial was the decrease in apoB large enough to produce significant clinical benefit."——即 REVEAL 的那点获益用 ApoB 下降解释得通。

### 3.3 孟德尔随机化（Voight 2012）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 内皮脂酶基因 LIPG 396Ser 变异（频率 2.6%）使 HDL-C 终生升高 | +0.14 mmol/L（≈+5.4 mg/dL），p=8×10⁻¹³ | Voight BF 等, *Plasma HDL cholesterol and risk of myocardial infarction: a mendelian randomisation study.* Lancet 2012;380(9841). doi:10.1016/S0140-6736(12)60312-2 | "higher HDL cholesterol (0·14 mmol/L higher, p=8×10(-13))" | 高 |
| 但心梗风险没降 | OR 0.99（95%CI 0.88–1.11） | 同上 | "the 396Ser allele was not associated with risk of myocardial infarction" | 高 |
| HDL 基因评分（每升高 1 SD） | OR 0.93（0.68–1.26），无关联 | 同上 | — | 高 |
| 对照：LDL 基因评分 | OR 2.13（1.69–2.69），强关联 | 同上 | — | 高 |
| 作者结论 | 有些升 HDL 的遗传机制并不降低心梗风险 | 同上 | "Some genetic mechanisms that raise plasma HDL cholesterol do not seem to lower risk of myocardial infarction." | 高 |

### 3.4 HDL 太高反而不好（Madsen 2017）

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 两项哥本哈根队列，52,268 男、64,240 女 | HDL-C 与全因死亡呈 U 形 | Madsen CM 等, *Extreme high high-density lipoprotein cholesterol is paradoxically associated with high mortality in men and women: two prospective cohort studies.* Eur Heart J 2017;38(32):2478-2486. doi:10.1093/eurheartj/ehx163（PMID 28419274） | "The association between HDL cholesterol concentrations and all-cause mortality was U-shaped for both men and women." | 中-高（大型观察性） |
| 死亡率最低点 | 男 1.9 mmol/L（73 mg/dL）；女 2.4 mmol/L（93 mg/dL） | 同上 | — | 中-高 |
| 极高 HDL 的风险 | 男 ≥3.0 mmol/L（116 mg/dL）HR 2.06（1.44–2.95）；2.5–2.99 mmol/L HR 1.36（1.09–1.70）；女 ≥3.5 mmol/L（135 mg/dL）HR 1.68（1.09–2.58） | 同上 | — | 中-高 |
| 作者保留 | 需在其他研究中证实 | 同上 | "These findings need confirmation in other studies." | — |

### 3.5 现状怎么表述
- **已证实**：用药把 HDL-C 数字抬高，并不能减少心血管事件；部分遗传性 HDL 升高也不降低心梗风险。
- **有争议 / 尚不清楚**：HDL 的「功能」（如胆固醇外流能力）可能比 HDL-C 数量重要。综述原话："HDL-C may not be protective against CHD and it may be the functions of HDL"；"CEC may capture key HDL traits that are not captured simply by measuring HDL-C."（Biomedicines 2022）。同一综述也指出 CETP 活性降低的常见基因变异与 HDL 升高、风险降低相关，与药物试验结果不一致——所以作者说「HDL 还没死」。
- **建议口径**：「HDL-C 低是一个提醒你风险偏高的信号，但目前没有证据表明把它人为抬高就能保护心脏；它是标记，不是治疗靶点。HDL 很高也不代表可以忽视 LDL。」

---

## 4. 甘油三酯与残粒、Lp(a)

### 4.1 甘油三酯（TG）与富含 TG 脂蛋白残粒

| 事实 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|
| TG、富含 TG 脂蛋白（TRL）及其残粒与心血管事件有因果关联的强支持 | Ginsberg HN 等（EAS 共识）, *Triglyceride-rich lipoproteins and their remnants…* Eur Heart J 2021;42(47):4791-4806. doi:10.1093/eurheartj/ehab551（PMC8670783） | "strong support for a causal association between triglycerides (TG), TG-rich lipoproteins (TRL), and TRL remnants" | 高（共识） |
| 可能是降 LDL 后「残余风险」的重要来源 | 同上 | "may contribute significantly to residual cardiovascular risk" | 中-高 |
| 残粒同样 <70 nm、含 ApoB，可进入内膜 | EAS 2017 | 见 §1.1 | 高 |

讲法：真正「惹事」的不是甘油三酯分子本身，而是装着胆固醇、带 ApoB 的残粒颗粒（本次未读到原文直接这样说，属基于上表的推论，标「示意」）。孟德尔随机化提示按 ApoB 降幅标准化后 TG 通路与 LDL 通路效果相近（Sniderman 2019 转述 Ference 2019）。

### 4.2 Lp(a)：天生的、主要由基因决定

| 事实 | 数字 | 出处 | 原文短引 | 可靠度 |
|---|---|---|---|---|
| 主要由 LPA 基因决定 | >90% | Kronenberg F 等（EAS 共识）, *Lipoprotein(a) in atherosclerotic cardiovascular disease and aortic stenosis.* Eur Heart J 2022;43(39):3925-3946. doi:10.1093/eurheartj/ehac361（PMC9639807） | "predominantly (>90%) determined by genetic variability at the LPA locus" | 高 |
| 因果 | 流行病学与遗传研究强烈支持因果 | 同上 | "Epidemiologic and genetic studies involving hundreds of thousands of individuals strongly support a causal" | 高 |
| 生活方式影响很小 | 低碳水 / 高脂饮食可能降 10–15%；成年前可能上升，女性绝经后上升 | 同上 | "Lifestyle interventions have minimal impact" | 高 |
| 族群差异（UK Biobank 中位数） | 华人 16、白人 19、南亚人 31、黑人 75 nmol/L | 同上 | "16, 19, 31, and 75 nmol/L, respectively" | 中-高（UK Biobank 华人样本，非中国本土） |
| 建议一生至少测一次 | — | 同上 | "This panel recommends testing Lp(a) concentration at least once in adults" | 高（共识推荐） |
| 风险分界 | 排除 <30 mg/dL（<75 nmol/L）；确定 >50 mg/dL（>125 nmol/L）；极高 >180 mg/dL（>430 nmol/L）≈ 未治疗杂合 FH 的终生风险 | 同上 | "Very high Lp(a) levels (>180 mg/dL or >430 nmol/L)" | 高（共识，作者称为「实用工具」） |
| 单位不能简单换算 | 检测方法差异大，受 apo(a) 异构体大小影响 | 同上 | "assays vary extensively" | 高 |
| 每颗粒风险可能超过 LDL | 未查到倍数 | 同上 | "risk associated with Lp(a) on a per particle basis may exceed that of LDL" | 中 |
| 受影响人数 | 全球约 14 亿人 | 同上 | "≈1.4 billion people worldwide" | 中 |
| 临床获益所需降幅（MR 推算） | 需大幅绝对降低 >50–100 mg/dL | 同上 | "large absolute reductions in Lp(a) concentration (>50–100 mg/dL) are needed" | 中 |

### 4.3 降 Lp(a) 新药：截至 2026-11-14 的最新状态（重要更新）

| 药物 / 试验 | 状态 | 数字 | 出处 | 可靠度 |
|---|---|---|---|---|
| **Pelacarsen（反义寡核苷酸）/ Lp(a)HORIZON** | 2026-09-04 Novartis 公布未达主要终点；2026-11-07 AHA 年会公布全部结果，同期发表于 NEJM（Cho 等） | 8,350 例（42 国，797 中心）已有心血管病、Lp(a) ≥70 mg/dL（约 148 nmol/L）；基线 LDL-C 约 65 mg/dL（≈1.7 mmol/L）；12 个月 Lp(a) 降 77.7%（64.4 vs 233.4 nmol/L）；主要终点 12.3% vs 12.1%，**HR 1.02（95%CI 0.90–1.15）**；中位随访 4.7 年；Lp(a) ≥90 mg/dL 亚组 HR 1.00（0.87–1.15）；药物相关不良事件 56.8% vs 18.0%，因不良事件停药 20.6% vs 7.5%；Novartis 已终止该药 ASCVD 项目 | TCTMD, *Full Lp(a)HORIZON Results Affirm Lack of Pelacarsen Benefit in Secondary Prevention*, 2026-11-07, https://www.tctmd.com/news/full-lpahorizon-results-affirm-lack-pelacarsen-benefit-secondary-prevention ；Novartis 新闻稿 2026-09-04 https://www.novartis.com/news/media-releases/novartis-announces-lpahorizon-phase-iii-topline-results-pelacarsen-patients-elevated-lpa-and-established-cardiovascular-disease-cvd | RCT 结果本身：高；数字为专业媒体转述 NEJM 论文（原文未读）：中-高 |
| Olpasiran（siRNA，Amgen）/ OCEAN(a)-Outcomes | 进行中；主要完成时间各来源说法不一（ClinicalTrials.gov 2024 旧快照写 2026-12，较新报道写约 2028，TCTMD 称结果 2029 前不会出） | — | 搜索摘要；ClinicalTrials.gov NCT05581303 | 低-中（时间表不确定） |
| Lepodisiran（siRNA，Lilly）/ ACCLAIM-Lp(a) | 进行中；主要完成约 2029-03，目标 12,500 人 | — | 搜索摘要 | 低-中 |
| Muvalaplin（口服）/ MOVE-Lp(a)；zerlasiran | 进行中；均未获 FDA 批准 | — | TCTMD 2026-09-08、2026-11-07 | 中 |

专家解读（TCTMD 2026-11-07）：Lloyd-Jones 认为 Lp(a) 仍满足因果因素的标准，并列出可能解释——患者动脉粥样硬化已太晚期、Lp(a) 升高幅度不够大、降后残余 Lp(a) 仍够高、药物毒性抵消获益、试验太短、其他风险已控制得好；称 HORIZON 是「the first trial to give us direct evidence」。研究主席 Nissen："We have to be humble about what our trial did show, what it didn't show." 另有医生在社交媒体质疑 Lp(a) 是否为因果（TCTMD 2026-09-08 引 David Brown："So treating a non-causal marker of disease doesn't treat the disease? Shocking."）。

**现状表述**：「Lp(a) 高与心血管病、主动脉瓣狭窄风险升高有关，基因证据提示它是原因之一；但到 2026 年 11 月，第一个大型降 Lp(a) 药物试验没有减少心血管事件，其余几种药还在试验中，目前没有获批的专门降 Lp(a) 药。」**有争议**：Lp(a) 作为治疗靶点是否成立。

---

## 5. 「好坏」的真相

| 论点 | 证据 | 状态 |
|---|---|---|
| 胆固醇本身是身体必需的（细胞膜、激素、胆汁酸等） | 本次未查 StatPearls 原文（记忆中：细胞膜成分、类固醇激素与胆汁酸前体，未证实来源但属教科书常识） | 已证实（教科书），本次未取出处 |
| LDL 是正常的运输工具：主要的胆固醇载体，也运维生素 E、类胡萝卜素、泛醇 | Borén 2020 "At circulating particle concentrations of ∼1 mmol/L, LDL is the principal carrier of cholesterol" | 已证实 |
| 「好 / 坏胆固醇」是俗称：LDL 和 HDL 里装的是同一种胆固醇分子，区别在「车」（脂蛋白）和去向 | 由 EAS 2017「LDL-C 是 LDL 颗粒里的胆固醇量」及 §2 推出 | 已证实（定义层面） |
| 问题在于「过量 × 时间」：颗粒多→更多颗粒穿入并滞留在内膜→斑块；暴露越久越多 | EAS 2017（剂量、时长、累积负担）；CARDIA；PCSK9、FH 自然实验 | 已证实 |
| 很低的 LDL 足够满足生理需要：新生儿、狩猎采集者约 50–70 mg/dL | O'Keefe 2004（专家综述）；FOURIER 极低 LDL 2.2 年无安全信号 | 中（长期极低水平的安全性仍在积累） |

---

## 6. 怀疑派：最强论点、证据质量、主流回应

| 怀疑派论点 | 最强版本与证据 | 证据质量 | 主流回应与证据 | 判断 |
|---|---|---|---|---|
| 「LDL 不导致心血管病」 | Ravnskov U 等, *LDL-C does not cause cardiovascular disease: a comprehensive review of the current literature.* Expert Rev Clin Pharmacol 2018;11(10):959-970. doi:10.1080/17512433.2018.1519391：称高 LDL 「unable to satisfy any of the Bradford Hill criteria for causality」，指主流综述「based on misleading statistics」，他汀一级预防获益「of doubtful benefit」 | 低-中（叙述性综述，选择性引用的批评来自主流；该刊另有评论 PMID 30570363，内容未读） | EAS 2017 用基因（FH、PCSK9）、200 多个队列、孟德尔随机化、RCT 逐项检验因果标准，得出一致结论；PCSK9 抑制剂、依折麦布这类**非他汀**机制降 LDL 同样减少事件（FOURIER、IMPROVE-IT），说明获益来自 LDL 下降本身 | 主流共识强；该论点不被接受 |
| 「老年人胆固醇高反而活得久」 | Ravnskov 等, BMJ Open 2016;6(6):e010401（PMID 27292972）：19 项研究 30 个队列 68,094 名老人，16 个队列 LDL-C 与全因死亡负相关（14 个显著），代表 92% 受试者；结论 "High LDL-C is inversely associated with mortality in most people over 60 years." | 低-中（观察性汇总，未处理反向因果） | ① **反向因果**：疾病、衰弱、癌症、体重下降会使胆固醇降低（多项队列提示，本次只读到二手转述，可靠度低-中）；② 结局不同：看**心血管**结局而非全因死亡——Mortensen MB 等, Lancet 2020;396(10263):1644-1652（PMID 33186534）：哥本哈根 91,131 人，每升高 1 mmol/L 心梗 HR 1.34（1.27–1.41），70–100 岁组心梗与 ASCVD 绝对风险最高、需治疗人数最低；③ ASPREE 二次分析（Zhou Z 等, J Gerontol A 2024, PMID 38038339，12,334 人，平均 75.2 岁）：全因与癌症死亡呈 U 形（最低点 3.3–3.4 mmol/L ≈128–131 mg/dL），但 LDL-C >3.3 mmol/L 后心血管死亡上升 | 「低胆固醇老人死亡多」的现象真实存在，但主要被认为是反向因果；**有争议之处**：老年人的最佳水平与是否启动治疗（属其他研究员） |
| 「瘦体型高反应者（LMHR）：生酮后 LDL 极高也不长斑块」 | ① Budoff M 等, *Carbohydrate Restriction-Induced Elevations in LDL-Cholesterol and Atherosclerosis: The KETO Trial.* JACC Adv 2024;3(8):101109（PMC11450898）：80 名生酮饮食者 LDL-C 272 ± 91 mg/dL（≈7.0 mmol/L），与 80 名 Miami Heart 对照（123 ± 38 mg/dL ≈3.2 mmol/L）配对，CAC 中位 0 vs 1（P=0.520），冠脉斑块无显著差异："is not greater than a matched cohort with 149 mg/dL lower average LDL-C"；② Soto-Mota A 等, *Longitudinal Data From the KETO-CTA Study: Plaque Predicts Plaque, ApoB Does Not.* JACC Adv 2025;4(7):101686：100 人单组，LDL-C 中位 237 mg/dL、ApoB 178 mg/dL，1 年非钙化斑块体积中位 +18.9 mm³、斑块体积百分比 +0.8%，ApoB 与进展无关联 | 低：小样本、横断面配对或单组无对照、经社交媒体招募、对照组 BMI 等不匹配、资助方与作者存在利益关联（论文自述）；**2025 纵向论文 2026 年先发关注声明（JACC Adv 2026;5(3):102607）后被撤稿（JACC Adv 2026;5(5):102824）**（PMC 页面标注） | 撤稿原因：本次只读到共同第一作者 Norwitz 的 Substack（2026-03-05）自述——提供 AI 斑块分析的公司「inappropriately unblinded」且拒绝盲法重做；作者称盲法重分析显示斑块进展「much lower」，但仍坚持「LDL/ApoB 不预测进展」（作者自述，未独立证实）。批评者（博客，低可靠度）指出：无对照组、样本量不足以做关联分析、改用次要分析、1 年进展速度并不慢。主流框架：1 年、100 人的无对照研究不足以推翻多条证据链；FH 与孟德尔随机化显示高 LDL 的伤害需要数十年显现 | 低质量证据，不能作为「高 LDL 无害」的依据；**尚不清楚**这个特殊人群的长期风险 |
| 「饮食胆固醇没关系」 | 本角度未查 | — | 属饮食角度研究员 | 未查 |

---

## 给视频的建议

### 最值得讲的点（按优先级）
1. **「天生的实验」**：PCSK9 突变的人 LDL 只低 15–28%，冠心病风险却低 47–88%；FH 的人 LDL 天生高，未治疗男性一半在 50 岁前心梗。凯可以问：「为什么一点点差别，几十年后差这么多？」→ 引出「LDL × 年数」。
2. **「车与货」**：LDL-C 是货量，ApoB 是车辆数。真正撞进血管壁的是「车」（颗粒），所以颗粒数多的人即使货量看着正常也可能有风险。
3. **「好胆固醇」的反转**：药把 HDL 抬高 30–100% 以上都没救心脏，基因让 HDL 天生高也没少心梗，太高反而死亡率升高。结论：HDL 是「体检报告上的提醒灯」，不是「拧大就好的旋钮」。
4. **Lp(a) 的最新转折（2026 年 11 月）**：天生的、基因决定、一生测一次；第一个大型降 Lp(a) 药物试验失败了——科学还在进行中。这是很好的「诚实科学」桥段，但要说清：失败的是**这一种药 / 这一个试验人群**，并不说明 Lp(a) 无害。

### 最容易讲错的地方
- 说「LDL 是坏东西」→ 错。LDL 是必需的运输车，问题是**太多、太久**。
- 说「HDL 越高越好」→ 错（极高 HDL 与死亡率升高相关；升 HDL 药无效）。
- 说「降到很低完全安全」→ 只能说「在约 2 年的试验里没看到安全问题」，且主要在已有心血管病的人群中。
- 把 FOURIER 15% 相对降低讲成「心梗少 15 个人」→ 绝对差是 1.5 个百分点（11.3% vs 9.8%）。区分相对 / 绝对风险。
- 说「Lp(a) 新药已证明有效」或「Lp(a) 已被证明无关」→ 两者都错。
- 说「老人胆固醇高反而好」→ 混淆了「生病导致胆固醇低」与「胆固醇低导致死亡」。
- 引用 KETO-CTA 而不提撤稿 → 严重错误。
- mg/dL 与 mmol/L 混用、Lp(a) 两种单位直接互换 → 错。

### 可以怎么画（真实 vs 示意）
| 画面 | 真实依据 | 注意 |
|---|---|---|
| LDL 颗粒：球形，表面一条巨大的 ApoB100 蛋白「缠绕带」，内含胆固醇酯 | 每颗粒一个 ApoB100（Borén 2020）；尺寸 <70 nm（EAS） | 颜色、质感是示意；真实 LDL 约 20–25 nm（本次未查到出处，记忆中，未证实，画面上不标数字） |
| 颗粒经内皮细胞「小泡」运送穿过血管壁（胞吞转运），被蛋白聚糖「粘住」 | Borén 2020 | 过程真实，镜头比例示意 |
| 巨噬细胞吞下修饰的 LDL 变成泡沫状细胞 | Borén 2020 | 真实过程，标「示意」 |
| 「记账本」：年龄轴上 LDL 累积成越来越厚的层 | EAS 累积负担、CARDIA | 纯示意图形 |
| HDL：比 LDL 小的颗粒 | — | 本次未查 HDL 尺寸，不标数字 |
| Lp(a)：LDL 颗粒上多挂一条 apo(a) 长链 | EAS Lp(a) 共识称其为含 ApoB 的脂蛋白 | apo(a) 结构细节本次未查，示意 |
| 「车与货」比喻：同样货量，车多（小而密 LDL）vs 车少（大 LDL） | Borén 2020 图 2、Sniderman 2019 | 比喻，标示意 |

### 观众最可能的误解
- 「我 HDL 高，所以 LDL 高也没事。」
- 「胆固醇是吃出来的，少吃蛋黄就行。」（饮食角度另讲；Lp(a) 和 FH 主要是基因决定）
- 「化验单没有箭头就是正常、没风险。」（风险取决于整体情况，不止一个数字，且 LDL 的伤害靠累积）
- 「降胆固醇药会把必需的胆固醇降没。」（细胞可自己合成；极低 LDL 试验 2.2 年未见安全信号——只能说到这一步）
- 「网上说生酮的人 LDL 很高也没斑块。」（证据弱，关键论文已撤稿）
- 每期都要提醒：个人情况请咨询医生，本片不替代诊疗。
