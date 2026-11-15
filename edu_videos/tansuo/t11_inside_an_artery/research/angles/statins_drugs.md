---
worker_id: researcher-03-statins
stage: 3
role: researcher
angle: statins-drugs
status: partial
blockers:
  - "pubmed.ncbi.nlm.nih.gov 网页要求 cookie，WebFetch 读不到；改用 NCBI E-utilities 读摘要。NEJM / Lancet 全文均未读，下文数字均来自摘要、药品标签或二手报道（已逐条标注）"
  - "中国他汀集采官方中选价和降幅：只查到二手转引（阿托伐他汀 20mg×7 片 6.6 元），未核对国家医保局原始文件"
  - "英克司兰（乐可为）是否已进 2025 / 2026 年国家医保目录：未查到；只查到 2024 年未进"
  - "停药后 LDL 多快回升：只在搜索摘要中见到 4 天停药研究和韩国队列，没有读到原文"
  - "《中国血脂管理指南（2023）》原文未读到（中等强度他汀起始的说法只见于 2024 基层版条目的二手描述）"
  - "CTT 关于出血性卒中的每 mmol/L 率比、FDA 2012 年认知副作用标签修改：本次未查到原文"
  - "血脂康（国产红曲提取物）及其 CCSPS 试验：未查"
  - "日本小林制药红曲事件的官方死亡 / 住院人数：只有新闻报道，数字前后不一，未读到厚生劳动省原文"
  - "ORION-4 与 VICTORION-2 PREVENT 结局：截至 2026-11-14 未查到发表的结果"
  - "WebSearch 用了 16 次（上限 20）"
confidence: medium
---

# 他汀该不该吃，以及其他降脂药（研究稿）

> 单位换算：LDL-C 1 mmol/L ≈ 38.67 mg/dL。原文只给一种单位的，另一种由本稿换算（标「换算」）。
> 可靠度：高 = 大型 RCT / 个体数据荟萃 / 监管标签原文；中 = 观察性研究、摘要转述或可信二手报道；低 = 二手转引、新闻、未核原文。

## 0. 本次实际读到的主要一手来源（速查）

| 简称 | 出处 | URL / DOI |
|---|---|---|
| Endo 2010 | Endo A. A historical perspective on the discovery of statins. Proc Jpn Acad Ser B 2010;86:484-93 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3108295/ |
| CTT 2010 | Lancet 2010;376 (26 项试验 17 万人) | doi:10.1016/S0140-6736(10)61350-5（PMID 21067804） |
| CTT 2012 | Lancet 2012;380 低风险人群 | doi:10.1016/S0140-6736(12)60367-5（PMID 22607822） |
| CTT 2019 | Lancet 2019;393 老年人 | doi:10.1016/S0140-6736(18)31942-1（PMID 30712900） |
| Collins 2016 | Lancet 2016;388:2532-61 他汀疗效与安全性证据解读 | doi:10.1016/S0140-6736(16)31357-5（PMID 27616593） |
| CTT 2022 | Lancet 2022;400 肌肉症状个体数据荟萃 | doi:10.1016/S0140-6736(22)01545-8（PMID 36049498） |
| CTT 2024 | Lancet Diabetes Endocrinol 2024;12:306-19 新发糖尿病 | doi:10.1016/S2213-8587(24)00040-8（PMID 38554713） |
| CTT 2026 | Lancet 2026;407:689-703 说明书所列副作用 | doi:10.1016/S0140-6736(25)01578-8（PMID 41655587） |
| SAMSON | Wood FA et al. NEJM 2020;383:2182-4（通信） | doi:10.1056/NEJMc2031173（PMID 33196154）；结果数字来自 https://www.eurekalert.org/news-releases/763001 及搜索摘要 |
| StatinWISE | Herrett E et al. BMJ 2021;372:n135 | doi:10.1136/bmj.n135（PMID 33627334） |
| Graham 2004 | JAMA 2004;292:2585-90 住院横纹肌溶解发生率 | doi:10.1001/jama.292.21.2585（PMID 15572716） |
| HPS2-THRIVE 2013 | Eur Heart J 2013;34:1279-91 肌肉 / 肝结局 | doi:10.1093/eurheartj/eht055（PMID 23444397） |
| SEARCH 2010 | Lancet 2010;376:1658-69 辛伐 80 vs 20 mg | doi:10.1016/S0140-6736(10)60310-8（PMID 21067805） |
| SLCO1B1 2008 | NEJM 2008;359:789-99 | doi:10.1056/NEJMoa0801936（PMID 18650507） |
| CRESTOR 标签 | FDA 瑞舒伐他汀说明书（2026 版，s047） | https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/021366s047lbl.pdf |
| SPARCL | NEJM 2006;355:549-59 | doi:10.1056/NEJMoa061894（PMID 16899775） |
| 丹麦停药 | Thompson W et al. JAMA Netw Open 2021;4:e2136802 | doi:10.1001/jamanetworkopen.2021.36802（PMID 34854906） |
| 法国停药 | Giral P et al. Eur Heart J 2019;40:3516-25 | doi:10.1093/eurheartj/ehz458（PMID 31362307） |
| SITE | Bonnet F et al. Lancet Healthy Longev 2026（经 Healio 报道读取） | doi:10.1016/j.lanhl.2026.100884；https://www.healio.com/news/cardiology/20260824/stopping-statins-did-not-raise-mortality-in-older-lowrisk-adults |
| STAREE | Zoungas S et al. NEJM 2026;395:1259-72 | doi:10.1056/NEJMoa2607314（PMID 42670961）；补充数字 https://www.tctmd.com/news/staree-statins-cut-mace-risk-30-older-adults-no-cvd-history |
| PREVENTABLE | ClinicalTrials.gov NCT04262206 | https://clinicaltrials.gov/study/NCT04262206 |
| IMPROVE-IT | NEJM 2015;372:2387-97 | doi:10.1056/NEJMoa1410489 |
| FOURIER | NEJM 2017;376:1713-22 | doi:10.1056/NEJMoa1615664 |
| ODYSSEY OUTCOMES | NEJM 2018;379:2097-107 | doi:10.1056/NEJMoa1801174 |
| VESALIUS-CV | ACC 试验摘要页（NEJM 2025 发表） | https://www.acc.org/Latest-in-Cardiology/Clinical-Trials/2025/11/20/21/09/VESALIUS-CV |
| ORION-10/11 | NEJM 2020;382:1507-19 | doi:10.1056/NEJMoa1912387 |
| ORION-4 | ClinicalTrials.gov NCT03705234 | https://clinicaltrials.gov/study/NCT03705234 |
| CLEAR Outcomes | NEJM 2023;388:1353-64 | doi:10.1056/NEJMoa2215024 |
| 恩利西肽（enlicitide） | TCTMD 2026-07 FDA 批准报道 | https://www.tctmd.com/news/fda-approves-enlicitide-oral-pcsk9-inhibitor-ldl-lowering |
| EAS 2017 | Ference BA et al. Eur Heart J 2017;38:2459-72 | doi:10.1093/eurheartj/ehx144（PMID 28444290） |
| EFSA 2018 | Scientific opinion on the safety of monacolins in red yeast rice | https://pmc.ncbi.nlm.nih.gov/articles/PMC7009499/ ；https://efsa.europa.eu/en/efsajournal/pub/5368 |
| 红曲肾损伤队列 | Doi Y et al. Kidney Int Rep 2026;11:107107 | doi:10.1016/j.ekir.2026.107107（PMID 42985088） |
| 红曲污染来源 | Tanaka S et al. J Nat Med 2025;79:1413-8 | doi:10.1007/s11418-025-01946-y（PMID 40897999） |

---

## 1. 机制与发现

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 远藤章团队 1971 年 4 月开始在数千种真菌培养液里筛选降胆固醇物质 | 先筛约 3,800 株才找到第一个有效培养液（得到橘霉素，因肾毒性放弃） | Endo 2010 | "we began our project using culture broths of thousands of fungi in April 1971." | 高（发现者本人回顾，史实） |
| 第二个有效培养液来自蓝绿色霉菌桔青霉 *Penicillium citrinum* Pen-51，1973 年 7 月分离出 ML-236B（compactin，美伐他汀） | 1973 年 7 月 | Endo 2010 | "We found a second active culture broth of blue-green mold, Penicillium citrinum Pen-51." | 高。注：文章正文用 compactin，「美伐他汀 = compactin」这一名称对应本次未在该文中读到（记忆中如此，未证实） |
| compactin 是 HMG-CoA 还原酶（胆固醇合成限速酶）的强效竞争性抑制剂 | — | Endo 2010 | "Compactin was an extremely potent inhibitor of HMG-CoA reductase." | 高（机制） |
| 降血 LDL 的关键一步：肝细胞上调 LDL 受体，把血里的 LDL 抓回肝里 | 1981 年 Brown 与 Goldstein 在狗身上证实 | Endo 2010 | "lovastatin could raise liver LDL receptors in dogs, and this led to a profound fall in plasma LDL levels." | 高（机制，动物实验 + 后续人体验证） |
| 洛伐他汀的两个独立发现：默沙东从土曲霉 *Aspergillus terreus* 分离 mevinolin；远藤团队同月从红色红曲霉 *Monascus ruber* 分离 monacolin K；两者是同一化合物 | 均为 1979 年 2 月 | Endo 2010 | 摘要转述："Merck isolated mevinolin from Aspergillus terreus … Endo's group isolated monacolin K from Monascus ruber in the same month" | 高 |

机制链（本稿综合上表）：他汀抑制 HMG-CoA 还原酶 → 肝细胞自己合成的胆固醇减少 → 肝细胞表面 LDL 受体增多 → 从血液中清除更多 LDL 颗粒 → 血 LDL-C 下降。他汀不直接「溶解」斑块；它作用于「肝脏供给 / 清除」这一环。

---

## 2. 疗效

### 2.1 相对获益：每降 1 mmol/L LDL-C

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 21 项他汀 vs 对照试验（129,526 人）：每降 1.0 mmol/L（≈38.7 mg/dL，换算），主要血管事件相对下降约 22% | RR 0.78（95% CI 0.76–0.80）；全因死亡 RR 0.90；癌症发生 RR 1.00 | CTT 2010 | 强化 vs 常规："produced a highly significant 15% (95% CI 11-18; p<0·0001) further reduction in major vascular events"（多降 0.51 mmol/L ≈ 19.7 mg/dL，换算） | 高（26 项 RCT 个体数据荟萃） |
| 没看到下限阈值：降 2–3 mmol/L（≈77–116 mg/dL，换算）可望降低风险约 40–50% | — | CTT 2010（摘要转述） | 转述："No threshold was apparent" | 高（荟萃）；外推部分为作者推断 |
| 低风险人群（5 年风险 <10%）获益比例与高风险人群相同或更大 | 最低风险组 RR 0.62，最高风险组 0.79；<10% 组每降 1 mmol/L 5 年内每 1,000 人少约 11 次主要血管事件 | CTT 2012 | "an absolute reduction in major vascular events of about 11 per 1000 over 5 years" | 高 |
| 老年人：整体每降 1 mmol/L 主要血管事件降 21% | RR 0.79（0.77–0.81）；14,483 人 >75 岁；年龄越大获益有减小趋势（p=0.06）；>75 岁且无血管病者的证据「不够直接」 | CTT 2019 | "produced a 21% (RR 0·79, 95% CI 0·77-0·81) proportional reduction in major vascular events" | 高 |

### 2.2 绝对获益与 NNT 示例

| 场景 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 二级预防（已得过心梗 / 卒中等）：阿托伐他汀 40 mg，LDL 降 2 mmol/L（≈77 mg/dL），治疗 5 年 | 每 10,000 人防止约 1,000 人发生主要血管事件（绝对获益 10%，**NNT ≈ 10**，本稿换算） | Collins 2016 | "would typically prevent major vascular events from occurring in about 1000 patients" | 高（基于 CTT 荟萃的估算） |
| 一级预防（风险升高但未发病），同上条件 | 每 10,000 人防止约 500 人（绝对获益 5%，**NNT ≈ 20**，本稿换算） | Collins 2016 | "and in 500 patients (ie, 5% absolute benefit) who are at increased risk but have not yet had a vascular event" | 高（估算） |
| 低风险（5 年风险 <10%），每降 1 mmol/L | 每 1,000 人 5 年少约 11 次事件（NNT ≈ 91，本稿换算） | CTT 2012 | 见 2.1 | 高 |
| ≥70 岁、无心血管病、无糖尿病（STAREE） | 阿托伐他汀 40 mg：10.9 vs 15.5 次 / 1,000 人年；中位 5.9 年 6.0% vs 8.3%（TCTMD 报道）→ 绝对差约 2.3 个百分点，NNT ≈ 44（TCTMD 推算） | STAREE；TCTMD | 见第 5 节 | 高（RCT）/ NNT 为二手推算 |

要点：相对获益各人群相近，**绝对获益取决于本人基线风险**——风险越高，吃同样的药，少发生的事件越多。

### 2.3 剂量与「他汀的 6 规则」

ACC/AHA 2018 指南把他汀分为高强度（LDL-C 降 ≥50%）、中强度（30%–49%）、低强度（<30%）（来源：指南执行摘要 Table 3 的转载，https://sites.duke.edu/extracvd/files/2019/09/Cholesterol-guidelines.pdf ，本次只经搜索摘要读取，可靠度：中）。高强度举例阿托伐他汀 40–80 mg、瑞舒伐他汀 20–40 mg（CCJM 综述转述，中）。

FDA 瑞舒伐他汀标签 Table 11（STELLAR 研究，2,240 人，6 周，基线 LDL-C 均值 189 mg/dL ≈ 4.9 mmol/L）LDL-C 下降百分比：

| 药物 | 10 mg | 20 mg | 40 mg | 80 mg |
|---|---|---|---|---|
| 瑞舒伐他汀 | −46% | −52% | −55% | — |
| 阿托伐他汀 | −37% | −43% | −48% | −51% |
| 辛伐他汀 | −28% | −35% | −39% | −46% |
| 普伐他汀 | −20% | −24% | −30% | — |

来源：CRESTOR 标签 2026，原文表头 "Percent Change in LDL-C by Dose of CRESTOR, Atorvastatin, Simvastatin, and Pravastatin From Baseline to Week 6"。可靠度：高（监管标签，开放标签剂量研究）。

「6 规则」核对（本稿据上表计算）：剂量翻倍多降的百分点——阿托伐 10→20→40→80：+6、+5、+3；瑞舒伐 10→20→40：+6、+3；辛伐 10→20→40→80：+7、+4、+7。**结论：翻倍通常只多降约 3–7 个百分点，「约 6%」是粗略经验值，大体成立但不精确。**「6 规则」这个说法本身的原始出处本次未查到。

---

## 3. 副作用（重点）

### 3.1 肌肉症状：大多数不是药引起的

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 19 项双盲安慰剂对照试验 123,940 人 + 4 项强化 vs 常规 30,724 人：他汀第 1 年肌肉痛 / 无力略多，以后不多 | 第 1 年 RR 1.07；1 年后 RR 0.99；全程 RR 1.03；强化方案 RR 1.08；第 1 年绝对多出 11（6–16）例 / 1,000 人年；CK 仅升约 0.02 倍正常上限 | CTT 2022 | "Most (>90%) of all reports of muscle symptoms by participants allocated statin therapy were not due to the statin." / "an absolute excess rate of 11 (6-16) events per 1000 person-years" | 高（盲法 RCT 个体数据荟萃） |
| SAMSON：曾因副作用停他汀的人，12 个月里随机轮换「他汀 / 安慰剂 / 空瓶」各 4 个月 | 约 60 人；症状 0–100 分：空瓶月 8.0，安慰剂月 15.4，他汀月 16.3（他汀 vs 安慰剂 P=0.39）；反安慰剂比 0.90（他汀时的症状约 90% 在吃安慰剂时也出现）；6 个月后约一半人重新服他汀 | SAMSON（NEJM 通信本次只读到题录；数字来自 EurekAlert 新闻稿与 mdedge 等报道） | 新闻稿转述："90% of symptoms reported on statin were also reported on placebo" | 中（RCT，n 小，单一药物剂量阿托伐 20 mg；原文未读） |
| StatinWISE：200 名因肌肉症状停药 / 想停药者，阿托伐 20 mg 与安慰剂各 2 个月交替 6 期 | 症状评分差 −0.11（−0.36 至 0.14，P=0.40）；因无法耐受退出：他汀期 18 人（9%）vs 安慰剂期 13 人（7%）；完成者 2/3 表示会重新长期服用 | StatinWISE | "No overall effect of atorvastatin 20 mg on muscle symptoms compared with placebo was found" | 高（多个 n-of-1 RCT） |

### 3.2 真正的肌病与横纹肌溶解：真实存在，但罕见

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 住院级横纹肌溶解发生率（美国 11 个医保计划理赔数据） | 阿托伐 / 普伐 / 辛伐单药：0.44 / 10,000 人年（0.20–0.84）→ 每年需治疗约 22,727 人才多出 1 例；西立伐他汀（已撤市）5.34；贝特类 2.82；他汀 + 贝特 5.98；西立伐 + 贝特 1,035 | Graham 2004 | "Rhabdomyolysis risk was similar and low for monotherapy with atorvastatin, pravastatin, and simvastatin" | 中-高（大型观察性队列） |
| 按 RCT 估算：阿托伐 40 mg 治 10,000 人 5 年 | 约 5 例肌病，其中约 1 例若不停药可能进展为横纹肌溶解 | Collins 2016 | "would cause about 5 cases of myopathy" | 高（基于 RCT 荟萃估算） |
| 高剂量风险：辛伐他汀 80 mg vs 20 mg（12,064 名心梗后患者，6.7 年） | 肌病 53 例（0.9%）vs 2 例（0.03%） | SEARCH 2010 | "Myopathy was increased with 80 mg simvastatin daily" | 高（RCT） |
| 标签列出的肌病危险因素 | ≥65 岁、未控制的甲减、肾功能不全、合用某些药物（含其他降脂药）、高剂量；瑞舒伐 40 mg 风险更高；与环孢素、吉非罗齐合用不推荐；烟酸、贝特、秋水仙碱也增加风险 | CRESTOR 标签 5.1 | "Risk factors for myopathy include age 65 years or greater, uncontrolled hypothyroidism, renal impairment, concomitant use with certain other drugs" | 高 |
| 罕见的免疫介导坏死性肌病（IMNM）：停药后仍持续，抗 HMG-CoA 还原酶抗体阳性，需免疫抑制治疗 | "rare reports" | CRESTOR 标签 5.2 | "There have been rare reports of immune-mediated necrotizing myopathy (IMNM)" | 高（标签；上市后报告） |

### 3.3 中国人 / 东亚人：同剂量风险更高（已证实）

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| HPS2-THRIVE（25,673 人，中位 3.9 年）：所有人都服辛伐他汀 40 mg；对照组（只吃他汀 + 安慰剂）中，中国参与者肌病（确诊 + 早期）发生率是欧洲的约 3 倍 | 对照组：中国 0.13% / 年 vs 欧洲 0.04% / 年；加烟酸 / 拉罗匹仑后：中国 0.66% / 年 vs 欧洲 0.07% / 年 | HPS2-THRIVE 2013 | "particularly in Chinese patients whose myopathy rates on simvastatin were higher" | 高（RCT 预设结局） |
| 瑞舒伐他汀在亚裔体内药物暴露约为白人 2 倍；FDA 要求亚裔从 5 mg 起始 | 中位暴露（AUC、Cmax）≈ 2 倍；起始 5 mg；20 mg 仍不达标时权衡利弊 | CRESTOR 标签 2.4、8.8、12.3 | "Initiate CRESTOR at 5 mg orally once daily due to increased rosuvastatin plasma concentrations." / "an approximate 2-fold elevation in median exposure (AUC and Cmax) in Asian subjects" / "Asian patients on CRESTOR may be at higher risk for myopathy" | 高（监管标签） |
| 英国说明书：亚裔起始 5 mg，40 mg 对亚裔禁用 | — | UK SmPC（https://www.medicines.org.uk/emc/product/6779/smpc，仅经搜索摘要读到） | 摘要："The 40 mg dose is contraindicated in these patients." | 中（未直接读原文） |
| SLCO1B1 基因（编码把他汀运进肝的转运体）rs4149056 C 等位基因：辛伐 80 mg 肌病风险显著升高 | 每个 C 拷贝 OR 4.5（2.6–7.7）；CC vs TT OR 16.9（4.7–61.1）；该研究人群 C 等位基因频率 15%；>60% 的肌病归因于该变异；在 2 万人辛伐 40 mg 试验中复现 | SLCO1B1 2008（SEARCH 遗传分析） | "Genotyping these variants may help to achieve the benefits of statin therapy more safely" | 高（全基因组关联 + 复现）。注：中国人群该等位基因频率本次未查到 |

尚不清楚：中国人对高强度他汀的整体获益-风险比是否需要普遍降强度——《中国血脂管理指南（2023）》原文本次未读到，只见二手描述称其基层版（2024）建议「以中等强度他汀作为起始」（https://search.napstic.cn/literature/periodical/010lcxxgbzz202409001 条目转述，可靠度：低-中）。

### 3.4 新发糖尿病：真实、剂量相关，主要发生在本来血糖已偏高的人

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 低 / 中强度他汀 vs 安慰剂 | RR 1.10（1.04–1.16）；1.3% / 年 vs 1.2% / 年 | CTT 2024 | "Statins cause a moderate dose-dependent increase in new diagnoses of diabetes" | 高 |
| 高强度他汀 vs 安慰剂 | RR 1.36（1.25–1.48）；摘要给出 4.8% vs 3.5%（摘要转述称为年率，本稿按例数 1,221/9,935 核算，单位需读全文确认） | CTT 2024 | 同上 | 高（RR）/ 绝对率单位待核 |
| 血糖变化很小 | 无糖尿病者空腹血糖平均升 0.04 mmol/L（≈0.7 mg/dL，换算）、HbA1c 升 0.06%（低 / 中强度）或 0.08%（高强度） | CTT 2024 | — | 高 |
| 约 62% 的新诊断发生在基线血糖已处于最高 1/4 的人（接近诊断线） | 62% | CTT 2024 | "with the majority of new diagnoses of diabetes occurring in people with baseline glycaemic markers" | 高 |
| 按 RCT 估算：阿托伐 40 mg 治 10,000 人 5 年 | 新增 50–100 例糖尿病（对比：二级预防防止约 1,000 例主要血管事件） | Collins 2016 | "50-100 new cases of diabetes" | 高（估算） |

### 3.5 肝：转氨酶轻度升高常见于化验，真正肝损伤罕见

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 19 项盲法试验：转氨酶异常略多，且剂量相关 | 0.30% / 年 vs 0.22% / 年，RR 1.41（1.26–1.57）；其他肝功能异常 RR 1.26；合计绝对每年多 0.13% | CTT 2026 | "783 participants [0·30% per annum] allocated statin vs 556 [0·22% per annum] allocated placebo, RR 1·41 [95% CI 1·26-1·57]" | 高 |
| CTT 2026 摘要未报告肝炎、肝衰竭等临床肝病数据 | — | CTT 2026 | — | 尚不清楚（在这份数据里） |
| 瑞舒伐他汀：转氨酶 >3 倍正常上限 | 1.1% vs 安慰剂 0.5%；多为短暂、无症状；上市后有罕见致死 / 非致死肝衰竭报告；急性肝衰竭 / 失代偿肝硬化禁用 | CRESTOR 标签 5.3 | "There have been rare postmarketing reports of fatal and non-fatal hepatic failure in patients taking statins" | 高（标签） |
| HPS2-THRIVE：连续两次 ALT >3 倍且无肌肉损伤 | 加烟酸组 0.10% / 年 vs 对照 0.06% / 年 | HPS2-THRIVE 2013 | — | 高 |

### 3.6 认知、出血性卒中及说明书里的其他副作用

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 说明书列出的 66 项其他副作用中，盲法数据只支持 4 项（转氨酶异常、其他肝功能异常、尿成分改变、水肿）；**不支持认知障碍、抑郁、睡眠障碍、周围神经病变** | 尿成分 RR 1.18；水肿 1.38% vs 1.31% / 年，RR 1.07；作者呼吁修改说明书 | CTT 2026 | "only four of 66 further undesirable outcomes that had been attributed to statins were FDR significant" / "Adverse event data from blinded randomised trials do not support causal relationships" | 高（盲法 RCT 个体数据）；有作者回复读者质疑的通信（Lancet 2026;407:2373），质疑内容本次未读 |
| 出血性卒中：卒中 / TIA 后阿托伐 80 mg（SPARCL，4,731 人） | 总卒中 HR 0.84（0.71–0.99）；出血性卒中 55 vs 33 例；LDL 73 vs 129 mg/dL（1.9 vs 3.3 mmol/L） | SPARCL | — | 高（RCT） |
| 按 RCT 估算：阿托伐 40 mg 治 10,000 人 5 年 | 出血性卒中 5–10 例（同期防止数百至上千次主要血管事件） | Collins 2016 | "5-10 haemorrhagic strokes" | 高（估算） |
| CTT 全体荟萃对卒中死亡无显著影响 | 卒中死亡 RR 0.96（0.84–1.09）；缺血性卒中下降 16% | CTT 2010 | "no significant effect on deaths due to stroke (RR 0·96, 95% CI 0·84-1·09; p=0·5)" | 高 |
| FDA 2012 年曾加入「可逆性记忆问题」标签说明 | — | 未查到（记忆中：FDA 2012 年安全通讯） | — | 未证实 |

**副作用一句话总表（10,000 人服阿托伐 40 mg 5 年，Collins 2016）**：肌病约 5 例、新糖尿病 50–100 例、出血性卒中 5–10 例；同期防止主要血管事件约 500（一级预防）–1,000（二级预防）例。

---

## 4. 「吃上就停不了」吗

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 停药后 LDL 会回升（RCT 直接证据） | SITE 停药组 LDL 从 114.6 升到 170.6 mg/dL（≈2.96 → 4.41 mmol/L，换算），继续组稳定 | SITE（Healio 报道） | — | 中（RCT，但本次只读到二手报道） |
| 回升速度 | 搜索摘要显示：阿托伐他汀停 4 天 LDL-C 升约 30%（EJPC 2022 摘要）；韩国队列停药 2–3 月升 44.9%、4–6 月升 54.6% | 未读原文，仅搜索摘要 | — | 低（未核原文） |
| 丹麦全国队列：≥75 岁长期服药者停药 | 67,418 人；一级预防停药 MACE sHR 1.32（1.18–1.48），每年每 112 人停药多 1 例 MACE；二级预防 sHR 1.28（1.18–1.39），每 77 人多 1 例 | 丹麦停药 | "discontinuation of statins was associated with a higher rate of MACE" | 中（观察性，存在「因病情变差才停药」等混杂） |
| 法国全国队列：75 岁一级预防者停药 | 120,173 人，14.3% 停药；心血管入院 HR 1.33（1.18–1.50）；冠脉事件 HR 1.46 | 法国停药 | "Statin discontinuation was associated with a 33% increased risk of admission for cardiovascular event" | 中（观察性） |
| **SITE 随机试验（法国，2026）**：≥75 岁、一级预防、已服他汀 ≥1 年，随机继续 vs 停药 | 1,180 人，中位 80 岁，开放标签非劣效；3 年全因死亡 7.9%（继续）vs 7.2%（停药），停药非劣效；不良事件、生活质量无差别；注意 65.8% 预测 10 年风险 ≥15%；报道中 CI 数字有误印 | SITE（Healio） | "Statin discontinuation was noninferior to continuation for 3-year all-cause death" | 中（RCT，但开放标签、样本小、主要终点是全因死亡而非心血管事件、原文未读） |

结论分层：
- **已证实**：他汀只在服用期间压低 LDL；停药 LDL 回到较高水平（机制 + SITE）。
- **有争议**：停药是否增加事件。观察性研究（丹麦、法国）显示停药者事件多约 30%；SITE 随机试验在 ≥75 岁一级预防人群 3 年未见全因死亡增加。双方最强论证——观察性：样本大、结局是心血管事件；RCT：随机消除了「病重才停药」的混杂，但只看全因死亡、3 年、1,180 人，统计效力有限。
- **尚不清楚**：是否「必须终身吃」。获益与 LDL 累计暴露有关（见第 8 节），停药即失去后续保护；但对高龄、一级预防、预期寿命有限者，停药的净损益尚无定论（SITE 与 STAREE 指向不同侧重）。「停不了」不是成瘾或依赖——没有找到他汀存在戒断综合征的证据（本次也未专门检索）。

---

## 5. 老年人（>75 岁）

| 研究 | 人群 | 结果 | 可靠度 |
|---|---|---|---|
| CTT 2019 | 28 项 RCT，186,854 人，其中 >75 岁 14,483 人 | 每降 1 mmol/L 主要血管事件 RR 0.79；年龄越大获益趋小（p=0.06）；>75 岁无血管病者证据「less direct」 | 高 |
| **STAREE（NEJM 2026-08-29，ESC 2026 发布）** | 澳大利亚全科，9,971 名 ≥70 岁（约 40% ≥75 岁），无心血管病、无糖尿病、无痴呆；阿托伐 40 mg vs 安慰剂，中位 5.9 年 | 主要心血管事件 297（10.9/1,000 人年）vs 412（15.5/1,000 人年），**HR 0.70（0.61–0.82）**；**无失能生存未改善** HR 0.94（0.84–1.05）；严重不良事件 2.7% vs 2.7%；肌肉骨骼、肝胆、糖尿病相关不良事件更常见（TCTMD：32.0% vs 29.4%、3.3% vs 0.9%、4.0% vs 2.7%）；基线 LDL 127 mg/dL（≈3.28 mmol/L），他汀组多降约 32 mg/dL | 高（双盲 RCT）；原文引语："Treatment with atorvastatin led to a lower risk of major cardiovascular events than placebo at a median of 5.9 years" / "did not result in longer disability-free survival" |
| PREVENTABLE（美国，NCT04262206） | 计划 20,000 名 ≥75 岁、无心血管病 / 痴呆 / 明显失能；阿托伐 40 mg vs 安慰剂；主要终点：死亡、痴呆、持续失能的复合 | 截至注册页 2026-09-01 更新：仍为 Recruiting，预计主要完成 2026-12-31；**尚无结果** | 高（注册信息） |
| SITE | 见第 4 节 | ≥75 岁一级预防停药 3 年全因死亡非劣效 | 中 |

已证实：≥70 岁、无心血管病者服他汀能减少心梗 / 卒中 / 血运重建（STAREE）。尚不清楚：能否让老人更长时间不失能、不痴呆（STAREE 否定了「延长无失能生存」，PREVENTABLE 未出结果）。

---

## 6. 其他降脂药

| 药物（机制） | 关键试验 | LDL 效果 | 结局 | 可靠度 |
|---|---|---|---|---|
| 依折麦布（抑制肠道胆固醇吸收，口服） | IMPROVE-IT，18,144 名急性冠脉综合征后，中位 6 年 | 时间加权 LDL 53.7 vs 69.5 mg/dL（1.4 vs 1.8 mmol/L） | 主要终点 HR 0.936（0.89–0.99）；7 年 32.7% vs 34.7%（绝对差 2.0 个百分点）；"ezetimibe resulted in incremental lowering of LDL cholesterol levels and improved cardiovascular outcomes" | 高 |
| 依洛尤单抗（PCSK9 单抗，皮下注射） | FOURIER，27,564 名心血管病患者，中位 2.2 年 | 较安慰剂降 59%，从 92 mg/dL（≈2.38 mmol/L）降到中位 30 mg/dL（0.78 mmol/L） | HR 0.85（0.79–0.92）；9.8% vs 11.3% | 高 |
| 依洛尤单抗（一级预防高危，无心梗 / 卒中史） | VESALIUS-CV，12,257 人，中位 4.6 年（NEJM 2025，经 ACC 摘要页读取） | — | 3 点 MACE 6.2% vs 8.0%，HR 0.75（0.65–0.86）；AHA 2026 分析未见出血性卒中增加 HR 0.64（0.30–1.37）（AJMC 报道） | 高（RCT，经 ACC 页面）/ 出血性卒中为二手报道（中） |
| 阿利西尤单抗（PCSK9 单抗） | ODYSSEY OUTCOMES，18,924 名 ACS 后，中位 2.8 年 | 目标滴定 LDL 25–50 mg/dL（0.65–1.29 mmol/L，换算） | HR 0.85（0.78–0.93）；9.5% vs 11.1% | 高 |
| 英克司兰（siRNA，抑制肝脏合成 PCSK9；第 1 天、第 90 天，之后每 6 个月皮下注射 1 次） | ORION-10/11（1,561 + 1,617 人） | 第 510 天较安慰剂降 52.3% / 49.9%；注射部位反应 2.6% vs 0.9% / 4.7% vs 0.5%，轻微 | **心血管结局截至 2026-11-14 尚未公布**：ORION-4（16,124 人）注册页预计 2026-10 主要完成；诺华 2026 Q3 材料称 ORION-4 于 2026 Q4 读出、VICTORION-2 PREVENT 于 2027 读出（经搜索摘要读取） | 高（LDL）/ 结局：尚不清楚 |
| 贝派地酸（作用于他汀上游的 ATP 柠檬酸裂解酶，口服） | CLEAR Outcomes，13,970 名他汀不耐受者，中位 40.6 月 | 基线 139 mg/dL（≈3.59 mmol/L），6 个月较安慰剂多降 29.2 mg/dL（≈0.76 mmol/L），百分比差 21.1 个百分点 | HR 0.87（0.79–0.96）；11.7% vs 13.3% | 高 |
| 恩利西肽 enlicitide（Lipfendra，MK-0616，口服 PCSK9 抑制剂，每日 20 mg） | CORALreef Lipids / HeFH | 24 周较安慰剂降 55.8% / 59.4% | **FDA 2026-07-16 批准，首个口服 PCSK9 抑制剂**；心血管结局试验 CORALreef Outcomes 已入组 >14,500 人，尚无结果；HeFH 试验腹泻 7% vs 2%、头晕 9% vs 4%（无显著差异）；"We are still awaiting cardiovascular outcomes data" | 中（TCTMD 报道，未读标签与原文） |

共同规律（本稿综合）：非他汀药物只要降低 LDL，事件也随之下降，与 EAS 2017「按 LDL 绝对降幅成比例获益」的判断一致；但在已用他汀的基础上加药，绝对获益（约 1.5–2 个百分点 / 2–6 年）远小于对高风险人群首先使用他汀。

### 6.1 中国价格与医保

| 事实 | 数字 | 出处 | 可靠度 |
|---|---|---|---|
| 「4+7」首轮集采：阿托伐他汀 20 mg×7 片中选价 6.6 元（日均约 0.94 元）；瑞舒伐他汀 10 mg 一组 21.8 元（包装写法有歧义） | 见左 | 药融云文章转引《4+7 城市药品集中采购中选后供应品种清单》（https://www.pharnexcloud.com/zixun/sx_48768 等，仅经搜索摘要） | 低（二手转引，未核国家医保局原件） |
| 2025 年 1–8 批国采接续：阿托伐、瑞舒伐等均有多家企业拟中选，以往中选价为基准 | 具体价格未查到 | 同上（搜索摘要） | 低 |
| 依洛尤单抗：2018 年国内上市，2021 年进医保，医保价 283 元 / 支，年费用降至 1 万元以内 | 见左 | 界面新闻 2024-11-29（https://www.jiemian.com/article/12052741.html） | 中（新闻，与医保谈判公开结果对应，未核目录原件） |
| 阿利西尤单抗：2019 年上市，2022 年进医保，290.7 元 / 支 | 见左 | 同上 | 中 |
| 托莱西单抗（信达，国产 PCSK9 单抗）：2023 年 8 月获批，2024 年谈判进医保；原定价 1,388 元 / 支 | 见左 | 同上 | 中 |
| 英克司兰钠（乐可为）：2023 年 8 月在华获批；**未进入 2024 年医保目录**；2025 / 2026 年状态未查到 | 见左 | 同上；"英克司兰钠注射液并未最终出现在今年的医保目标[录]中" | 中 / 2025 后：未查到 |

---

## 7. 红曲米与保健品

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 红曲中的莫纳可林 K（内酯形式）与洛伐他汀是同一分子 | — | EFSA 2018；Endo 2010 | "monacolin K in lactone form is identical to lovastatin" | 高 |
| EFSA：红曲莫纳可林在 10 mg / 天时有显著安全担忧；低至 3 mg / 天也有个案严重不良反应；**无法确定安全摄入量** | 10 mg / 天；3 mg / 天 | EFSA 2018 | "the Panel was unable to identify a dietary intake of monacolins from RYR that does not give rise to concerns" | 高（监管机构科学意见） |
| 主要风险：肌肉骨骼（含横纹肌溶解）与肝 | — | EFSA 2018（搜索摘要转述） | — | 中-高 |
| 红曲菌某些菌株可能产生毒性代谢物橘霉素 | — | EFSA 2018 正文 2.4.2 | "a secondary toxic metabolite called citrinin" | 高 |
| 欧盟 2022 年起把红曲莫纳可林列入「Union scrutiny」，补充剂每日剂量须 <3 mg；EFSA 后续意见仍认为提交数据不能证明 <3 mg / 天安全 | <3 mg / 天 | EFSA NDA 意见（https://pmc.ncbi.nlm.nih.gov/articles/PMC11868785，经搜索摘要读取）；Regulation (EU) 2022/860 原文未读 | — | 中 |
| **日本小林制药红曲事件（2024）**：服用其含红曲的功能性标示食品后出现肾损伤；国家卫生科学研究所在原料中检出软毛青霉酸（puberulic acid）等化合物；大鼠实验显示软毛青霉酸致肾损害 | 新闻报道的死亡数前后不一（5 例、76 例「疑似」、80 例、175 例不等）；一度报道住院 492 人、其中 291 人有肾病；2024-08-08 停产 | 新闻（Wikipedia、Yahoo/Kyodo、China Daily 等，经搜索摘要）；未读厚生劳动省原文 | "it remains unclear whether this substance is directly responsible"（新闻转述厚劳省） | 低-中（数字不可直接引用） |
| 污染来源线索：生产设施可能受青霉菌 *Penicillium adametzioides* 污染；红曲霉与该青霉共培养产生非预期代谢物 | — | 红曲污染来源 J Nat Med 2025 | "the possibility contamination of FFC products by Penicillium adametzioides in a manufacturing facility" | 中（实验研究；摘要未明确证实该菌产生软毛青霉酸） |
| 日本全国队列：190 名疑似该补充剂相关肾损伤成人 | 女性 68%；就诊时中位 eGFR 29.2 mL/min/1.73m²；60 天内快速改善后停在 <60；初始 eGFR <60 者到第 540 天仅 33% 恢复到 ≥60；范可尼综合征样肾小管异常 ≥80% 在 120 天内恢复；6 人需急性透析，1 人进入永久肾替代治疗 | 红曲肾损伤队列 Kidney Int Rep 2026 | "Proximal tubular biochemical abnormalities largely resolved within 120 days" | 中-高（全国队列） |

要点：红曲保健品有两类风险——①**它本身就是不标剂量的洛伐他汀**（剂量不定、无医生监测、照样有他汀的副作用）；②**生产质控问题**（小林事件是污染物致肾损伤，与莫纳可林 K 本身无关）。注意：保健品「天然」不等于更安全。中国处方药「血脂康」（红曲提取物）及其试验本次未查。

---

## 8. 他汀治本还是治标

### 8.1 他汀作用在哪一环

| 环节 | 本次资料支持的事实 | 出处 |
|---|---|---|
| A. 为什么某人 LDL 高（原因） | 本角度未研究 LDL 升高的具体原因（遗传、饮食等由其他研究员负责）。本次读到的只有：SLCO1B1 等基因影响他汀在肝内的处置；PCSK9、LDL 受体通路是降 LDL 药物的靶点 | SLCO1B1 2008；FOURIER 等 |
| B. 肝脏如何调节血 LDL | 他汀抑制 HMG-CoA 还原酶 → 肝 LDL 受体增加 → 血 LDL 下降 | Endo 2010 |
| C. 动脉粥样硬化的致病暴露 | EAS 共识：LDL **导致** 动脉粥样硬化性心血管病；风险与 LDL-C 暴露的**绝对水平**呈剂量依赖的对数线性关系，并随**暴露时间**延长而增加 | EAS 2017："unequivocally establishes that LDL causes ASCVD" / "dose-dependent log-linear association between the absolute magnitude of exposure" / "this effect appears to increase with increasing duration of exposure to LDL-C" |
| D. 事件（心梗、卒中） | 每降 1 mmol/L LDL-C，主要血管事件相对降约 22% | CTT 2010 |

**结论**：他汀不改变「为什么你的 LDL 高」（A），停药后 LDL 回升（SITE：114.6 → 170.6 mg/dL）；从这个意义上它是「治标」——像一直按住水龙头而不是修好水管。但它直接压低的是动脉粥样硬化的**致病暴露本身**（C）——LDL 颗粒浓度及其累计暴露；从「动脉为什么会堵」看，它针对的是病因而不是症状，这一点与止痛药缓解症状、却不改变疾病进程不同。

### 8.2 这种区分在证据上意味着什么

| 推论 | 证据 | 判定 |
|---|---|---|
| 获益来自「降 LDL」本身，而不只是他汀这个分子 | 依折麦布（IMPROVE-IT）、PCSK9 单抗（FOURIER、ODYSSEY、VESALIUS-CV）、贝派地酸（CLEAR Outcomes）机制不同，都在降 LDL 后减少事件；EAS 2017：任何降 LDL 的机制应带来与 LDL "absolute reduction" 成比例的风险下降（前提是同时降低 LDL 颗粒数且无脱靶效应） | 已证实（多机制 RCT 一致） |
| 获益按 LDL 降幅计，不按「吃了药」计 | CTT 以「每降 1 mmol/L」表达，强化 vs 常规多降 0.51 mmol/L 带来额外 15% 下降；未见下限阈值 | 已证实 |
| 停药 = 失去对暴露的控制 | LDL 回升（SITE）；观察性研究停药后事件增多约 30%（丹麦、法国）；但 SITE（≥75 岁一级预防）3 年全因死亡未增加 | LDL 回升已证实；事件后果有争议 |
| 暴露是累计的，所以「越早、越久」的意义 | EAS 2017 称风险随暴露时间增加；但「年轻时开始吃他汀能否更多获益」本次没有读到 RCT 直接证据 | 机制与遗传学证据支持，干预时机：尚不清楚 |
| 降 LDL 不能消除全部风险 | 即使 LDL 降到 30 mg/dL（0.78 mmol/L），FOURIER 治疗组 2.2 年仍有 9.8% 发生主要事件 | 已证实（残余风险存在）；残余风险来源不在本角度范围 |
| 已形成的斑块能否「逆转」 | 本次未检索 | 尚不清楚（本稿未查） |

---

## 9. 已证实 / 有争议 / 尚不清楚 汇总

| 分类 | 结论 |
|---|---|
| 已证实 | 他汀降低 LDL 并按降幅成比例减少心梗、卒中（CTT）；获益比例在低风险者也存在，绝对获益随基线风险升高；>90% 的「他汀肌肉痛」不由药物引起（CTT 2022、SAMSON、StatinWISE）；横纹肌溶解真实但罕见（约 0.44 / 万人年）；高强度他汀增加新发糖尿病（RR 1.36），多见于血糖已偏高者；转氨酶轻度升高略增，剂量相关；说明书所列认知障碍等多数副作用无盲法证据支持（CTT 2026）；亚裔同剂量瑞舒伐他汀暴露约 2 倍、中国人辛伐他汀肌病率更高；≥70 岁无心血管病者服阿托伐 40 mg 心血管事件降 30%（STAREE）；依折麦布、PCSK9 单抗、贝派地酸在 RCT 中减少事件；红曲莫纳可林 K = 洛伐他汀，EFSA 无法确定安全剂量 |
| 有争议 | 老年一级预防停药是否有害（观察性：有害；SITE RCT：3 年全因死亡非劣效）；出血性卒中风险的大小与临床意义（SPARCL 增加，Collins 估 5–10 / 万人 5 年，VESALIUS 未见 PCSK9 增加） |
| 尚不清楚 | 他汀能否延长老人无失能 / 无痴呆生存（STAREE 阴性，PREVENTABLE 未出）；英克司兰、口服 PCSK9 恩利西肽能否减少心血管事件（结局试验未读出）；中国指南对中国人起始强度的原文表述（本次未读到）；红曲事件的确切致病物与最终伤亡数 |

---

## 给视频的建议

**最值得讲的 5 点**
1. **他汀怎么起作用**：一个「霉菌里找到的分子」堵住肝细胞造胆固醇的工厂（HMG-CoA 还原酶），肝细胞「缺胆固醇」后在表面多装 LDL 受体，把血里的 LDL 抓回去。这是最好画、最直观的一幕。
2. **相对获益 vs 绝对获益**：「每降 1 mmol/L 少约 1/5 的事件」对所有人差不多；但「吃 5 年，100 人里少几人出事」取决于你本来多危险（二级预防约 10 人、一级预防约 5 人，Collins 2016 的 LDL 降 2 mmol/L 情景）。
3. **反安慰剂效应**：SAMSON「空瓶 / 安慰剂 / 他汀」的设计本身就是好故事；用 CTT 2022「>90% 不是药引起的」收尾。但要同时说：真正的肌病存在，出现原因不明的肌肉痛、无力、尤其伴发热或尿色变深要立刻就医。
4. **中国人用药的特殊点**：瑞舒伐他汀在亚裔体内约 2 倍暴露、FDA 要求从 5 mg 起；HPS2-THRIVE 中中国人辛伐他汀肌病率约为欧洲 3 倍。这是对中国观众很有价值、又常被忽略的事实。
5. **「治标还是治本」**：他汀不修好「LDL 为什么高」，所以停药 LDL 会回来；但它压低的正是让动脉变堵的那个东西（LDL 暴露），所以对动脉而言它针对的是病因。

**最容易讲错的地方**
- 把「22% 相对下降」说成「你的风险降 22 个百分点」。
- 说「他汀伤肝，要定期查肝功」说得太重：标签只说「开始前考虑查，之后按临床需要」；转氨酶轻度升高多为短暂无症状，严重肝衰竭是罕见上市后报告。
- 说「他汀导致糖尿病，所以别吃」：要同时给分母（50–100 例糖尿病 vs 500–1,000 例主要血管事件 / 万人 5 年）。
- 说「吃上就停不了 = 成瘾」：停药不会戒断，只是 LDL 回升、保护消失。
- 把 STAREE 说成「老人吃他汀能长寿 / 不失能」：它**没有**改善无失能生存。
- 把「6 规则」说成精确规律：实测翻倍多降 3–7 个百分点。
- 把英克司兰、口服 PCSK9 说成「已证明减少心梗」：截至 2026-11 结局试验尚未出结果，只证明降 LDL。
- 把红曲说成「天然他汀，更安全」：它就是洛伐他汀，剂量不可控；小林事件是另一种风险（污染）。
- 本稿的价格数字可靠度低，视频中若要讲价格，先核对国家医保局原文。

**可以怎么画**
- 真实可画：肝细胞（直径约 20–30 µm，本次未查证尺寸，仅记忆）表面 LDL 受体抓取 LDL 颗粒（LDL 直径约 20–25 nm，本次未查证，仅记忆）；受体数量变化可夸张示意。HMG-CoA 还原酶在内质网膜上（记忆，未查证），他汀分子「插进」酶活性口袋——标「示意」。
- 霉菌发现史：蓝绿色青霉菌落（Endo 原文说「blue-green mold」），培养皿 / 培养液成排筛选——真实可画。
- SAMSON：12 个药瓶（4 他汀、4 安慰剂、4 空瓶），每月一个——真实的试验设计，可直接画。
- 剂量 vs 降幅：用上面的 STELLAR 表画成阶梯，展示「翻倍只多一小截」。
- 只能示意：「累计 LDL 暴露」可用沙漏 / 进度条示意，不能画成真实的斑块生长速度；「风险下降百分比」用 100 人方阵图（图标）比较好。
- 红曲：真实的红色发酵米可以画；「污染」只能示意，不要画成具体某品牌包装。

**观众最可能的误解**
- 「LDL 正常了就可以停药」——LDL 正常是药效，不是病好了。
- 「肌肉酸就是他汀的副作用，马上停」——多数不是药引起的，应与医生沟通（换药、减量、重新试用），不要自行停药；但严重症状要立即就医。
- 「保健品 / 红曲可以替代他汀」——成分就是他汀，却没有剂量与质量保障。
- 「新药（PCSK9、英克司兰）更好，他汀过时了」——新药多作为他汀之外的加法或不耐受时的替代；部分新药尚无事件终点证据，且价格与医保情况各异。
- 「老了就不用吃了」——STAREE 显示 ≥70 岁仍减少心血管事件，但不延长无失能生存；是否继续需个体化与医生决定。
- 本视频不替代医生：是否用药、用哪种、多大剂量，取决于个人风险、化验和合并用药。
