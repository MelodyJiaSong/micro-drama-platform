---
worker_id: researcher-04-lifestyle
stage: 3
role: researcher
angle: lifestyle-diet
status: partial
blockers:
  - "中国血脂管理指南 2023 中文原文（中国循环杂志 / 中华心血管病杂志 yiigle）无法抓取；只读到英文版（Front Pharmacol 2023, PMC10498001）的 9.3–9.5 节。饱和脂肪供能比、碳水供能比、膳食纤维克数、BMI 目标、运动时长、限酒克数在已读部分没找到；英文版 'Total fat intake should be limited to 20–25 g per day' 疑为烹调油而非总脂肪，需查中文原表"
  - "中国居民膳食指南 2022 官网 dg.cnsoc.org 证书错误无法打开；鸡蛋、限酒 15 g 等数字只来自媒体转述"
  - "AHA 2017 主席建议、AHA 2019 膳食胆固醇科学建议全文付费（403）；只读到摘要；「每天 1 个蛋 / 老年人 2 个」只见于媒体与检索摘要"
  - "ESC/EAS 2019 只读到 2019-02 外审稿（External Review Round 3），非终稿；终稿表号可能不同（外审稿表 7＝终稿表 8），数字需对终稿核对"
  - "PubMed 页面要求 cookie 无法读取，改用 Europe PMC REST API 读摘要；多数只读到摘要"
  - "未查到：睡眠与血脂、卵磷脂、苹果醋、「洗血 / 血液净化」、「通血管」保健品监管口径、FDA 燕麦 β-葡聚糖健康声明原文（eCFR / Cornell 被拦）、反式脂肪定量（Mozaffarian 2006 摘要未读到）、椰子油、猪油 / 内脏的专门证据、含糖饮料对 TG 的荟萃数字、Kodama 2007 HDL 荟萃、Dattilo 1992 每公斤 LDL 数字"
  - "后半段多次网络中断（Connection lost / 403），生酮与间歇性断食只拿到少量资料"
confidence: medium
---

# 生活方式与饮食能把血脂改多少（lifestyle-diet）

单位换算（本文统一使用）：胆固醇 1 mmol/L = 38.67 mg/dL；甘油三酯（TG）1 mmol/L = 88.57 mg/dL。原文只给一种单位的，另一种由本文换算，标「换算」。

主要资料清单（后文用编号引用）：

| 编号 | 资料 | 类型 | URL |
|---|---|---|---|
| S1 | Hooper L, et al. Reduction in saturated fat intake for cardiovascular disease. Cochrane Database Syst Rev 2020;8:CD011737（PMID 32827219） | Cochrane 系统评价，15 项 RCT | https://doi.org/10.1002/14651858.CD011737.pub3 |
| S2 | Sacks FM, et al. Dietary Fats and Cardiovascular Disease: A Presidential Advisory From the AHA. Circulation 2017（PMID 28620111） | 专家建议（基于 RCT 综述），只读到摘要 | https://doi.org/10.1161/CIR.0000000000000510 |
| S3 | 2019 ESC/EAS Guidelines for the Management of Dyslipidaemias，External Review Round 3（2019-02 外审稿，牛津 ORA 存档 PDF） | 指南草稿 | https://ora.ox.ac.uk/objects/uuid:b66cfed8-126f-4ed3-ac5a-cc6225b0e141 |
| S4 | Li JJ, et al. 2023 Chinese guideline for lipid management. Front Pharmacol 2023;14:1190934（PMID 37711173，中国血脂管理指南 2023 英文版） | 指南 | https://doi.org/10.3389/fphar.2023.1190934 |
| S5 | Carson JAS, et al. Dietary Cholesterol and Cardiovascular Risk: A Science Advisory From the AHA. Circulation 2020;141:e39–e53（2019-12-16 在线，PMID 31838890） | 科学建议，只读到摘要 | https://doi.org/10.1161/CIR.0000000000000743 |
| S6 | Vincent MJ, et al. Meta-regression analysis of the effects of dietary cholesterol intake on LDL and HDL cholesterol. Am J Clin Nutr 2019（PMID 30596814） | 55 项干预研究的荟萃回归 | https://doi.org/10.1093/ajcn/nqy273 |
| S7 | Whitehead A, et al. Cholesterol-lowering effects of oat β-glucan: a meta-analysis of RCTs. Am J Clin Nutr 2014（PMID 25411276） | RCT 荟萃（28 项） | https://doi.org/10.3945/ajcn.114.086108 |
| S8 | Gylling H, et al. Plant sterols and plant stanols in the management of dyslipidaemia and prevention of CVD（EAS 共识小组）. Atherosclerosis 2014;232:346–360（PMID 24468148） | 专家共识 | https://doi.org/10.1016/j.atherosclerosis.2013.11.043 |
| S9 | Del Gobbo LC, et al. Effects of tree nuts on blood lipids, apolipoproteins, and blood pressure. Am J Clin Nutr 2015;102:1347–56（PMID 26561616） | 61 项对照试验剂量反应荟萃 | https://doi.org/10.3945/ajcn.115.110965 |
| S10 | Chiavaroli L, et al. Portfolio Dietary Pattern and Cardiovascular Disease: SR & MA of Controlled Trials. Prog Cardiovasc Dis 2018（PMID 29807048） | RCT 荟萃（7 组比较） | https://pubmed.ncbi.nlm.nih.gov/29807048/ |
| S11 | Estruch R, et al. Primary Prevention of CVD with a Mediterranean Diet Supplemented with EVOO or Nuts. N Engl J Med 2018;378:e34（PMID 29897866，PREDIMED 撤稿后重发版） | RCT | https://pubmed.ncbi.nlm.nih.gov/29897866/ |
| S12 | Smart NA, et al. The Effect of Exercise Training on Blood Lipids: SR & MA. Sports Med 2025;55:67–78（PMID 39331324） | RCT 荟萃（148 项） | https://doi.org/10.1007/s40279-024-02115-z |
| S13 | Dattilo AM, Kris-Etherton PM. Effects of weight reduction on blood lipids and lipoproteins: a meta-analysis. Am J Clin Nutr 1992;56:320–8（PMID 1386186） | 荟萃 | https://doi.org/10.1093/ajcn/56.2.320 |
| S14 | Zhao J, et al. Association Between Daily Alcohol Intake and Risk of All-Cause Mortality. JAMA Netw Open 2023（PMID 37000449） | 107 项队列荟萃 | https://doi.org/10.1001/jamanetworkopen.2023.6185 |
| S15 | Gepner AD, et al. Effects of smoking and smoking cessation on lipids and lipoproteins: outcomes from a RCT. Am Heart J 2011（PMID 21167347） | RCT 二次分析 | https://doi.org/10.1016/j.ahj.2010.09.023 |
| S16 | Bhatt DL, et al. Cardiovascular Risk Reduction with Icosapent Ethyl for Hypertriglyceridemia（REDUCE-IT）. N Engl J Med 2019;380:11–22（PMID 30415628） | RCT | https://doi.org/10.1056/NEJMoa1812792 |
| S17 | Ridker PM, et al. Effects of Randomized Treatment With Icosapent Ethyl and a Mineral Oil Comparator on ... Biomarkers（REDUCE-IT 子研究）. Circulation 2022（PMID 35762321） | RCT 子分析 | https://doi.org/10.1161/CIRCULATIONAHA.122.059410 |
| S18 | Nicholls SJ, et al. STRENGTH. JAMA 2020（PMID 33190147） | RCT | https://doi.org/10.1001/jama.2020.22258 |
| S19 | Manson JE, et al. VITAL: Marine n-3 Fatty Acids and Prevention of CVD and Cancer. N Engl J Med 2019（PMID 30415637）；数字取自 Bassuk & Manson, Cardiovasc Res 2023（PMID 36378553）综述 | RCT（经综述转引） | https://doi.org/10.1056/NEJMoa1811403 ；https://doi.org/10.1093/cvr/cvac172 |
| S20 | Kalstad AA, et al. OMEMI. Circulation 2021（PMID 33191772） | RCT | https://doi.org/10.1161/CIRCULATIONAHA.120.052209 |
| S21 | Gencer B, et al. Effect of Long-Term Marine ω-3 Fatty Acids Supplementation on the Risk of Atrial Fibrillation in RCTs. Circulation 2021（PMID 34612056） | RCT 荟萃（7 项，81,210 人） | https://doi.org/10.1161/CIRCULATIONAHA.121.055654 |
| S22 | Gardner CD, et al. Effect of raw garlic vs commercial garlic supplements on plasma lipid concentrations. Arch Intern Med 2007（PMID 17325296） | RCT（n=192，6 个月） | https://doi.org/10.1001/archinte.167.4.346 |
| S23 | 大蒜荟萃：Phytother Res 2025（PMID 40628369，陈蒜提取物 19 项）；Nutrients 2024（PMID 38892625） | RCT 荟萃 | https://pubmed.ncbi.nlm.nih.gov/40628369/ ；https://pubmed.ncbi.nlm.nih.gov/38892625/ |
| S24 | Hodis HN, et al. Nattokinase atherothrombotic prevention study: a randomized controlled trial. Clin Hemorheol Microcirc 2021（PMID 33843667） | RCT（n=265，中位 3 年） | https://pubmed.ncbi.nlm.nih.gov/33843667/ |
| S25 | 鸡蛋「超反应者」：Curr Dev Nutr 2019 会议摘要（PMC6818912，Egg Nutrition Center 资助） | 小样本干预，会议摘要 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6818912/ |
| S26 | 生酮相关：Budoff MJ, et al. JACC Adv 2024（PMID 39372369）；DiMattia & Petersen, J Am Heart Assoc 2026（PMID 42047192，综述）；Soto-Mota A, et al. JACC Adv 2025（PMID 40192608，Europe PMC 记录显示有关注声明 PMID 41906601 与撤稿 PMID 42206798） | 病例对照 / 综述 / 观察性 | https://doi.org/10.1016/j.jacadv.2024.101109 ；https://doi.org/10.1161/JAHA.125.048903 |
| S27 | Li H, Li T. Intermittent fasting versus continuous energy restriction in MASLD: SR & MA. Front Nutr 2026（PMID 42211106） | RCT 荟萃（9 项，n=894） | https://doi.org/10.3389/fnut.2026.1833688 |
| S28 | Erlich MN, et al. 豆奶替代牛奶对心脏代谢风险因子. BMC Med 2024（PMID 39169353） | 对照试验荟萃（17 项） | https://doi.org/10.1186/s12916-024-03524-7 |
| M1 | 澎湃新闻 2023 解读中国血脂管理指南（2023）生活方式 | 媒体（线索） | https://m.thepaper.cn/newsDetail_forward_22509214 |
| M2 | 人民日报 2022-05-20《中国居民膳食指南(2022)》发布 | 媒体（官方通稿） | https://paper.people.com.cn/rmrbwap/html/2022-05/20/nw.D110000renmrb_20220520_1-19.htm |
| M3 | 范志红，澎湃新闻 2022-05-04 解读膳食指南 2022 | 专家科普（线索） | https://www.thepaper.cn/newsDetail_forward_17919126 |

---

## 1. 总览：各项措施的典型降幅（一张表）

ESC/EAS 2019 外审稿表 7「Impact of specific lifestyle changes on lipid levels」给出效应量级：`+++` >10%，`++` 5–10%，`+` <5%（S3）。下表把该分级和本次读到的具体数字合在一起。

| 措施 | 对 LDL-C | 对 TG | 对 HDL-C | 出处 | 可靠度 |
|---|---|---|---|---|---|
| 不吃反式脂肪 | ++（5–10%） | — | 避免它可让 HDL ++ | S3 表 7 | 中（指南分级，外审稿） |
| 减少饱和脂肪 | ++；每多 1% 能量来自饱和脂肪，LDL 升 0.02–0.04 mmol/L（0.8–1.6 mg/dL） | 用不饱和脂肪替代：+ | — | S3 | 高（机制与大量喂养试验，指南级） |
| 用植物油替代黄油、猪油 | −0.20 至 −0.42 mmol/L（换算 −7.7 至 −16.2 mg/dL） | — | — | S3（引文 169） | 中高 |
| 燕麦 β-葡聚糖 ≥3 g/天 | −0.25 mmol/L（95% CI 0.20–0.30；换算 −9.7 mg/dL） | 无显著作用 | 无显著作用 | S7 | 高（28 项 RCT 荟萃） |
| 可溶性纤维（不同纤维 3–10 g/天） | 3–5% | — | — | S3 | 中 |
| 植物甾醇 / 甾烷醇 2 g/天 | 8–10%（EAS 共识），7–10%（ESC 外审稿） | 高 TG 患者降 6–9% | 几乎无影响 | S8、S3 | 高（LDL 降幅）；**无硬终点 RCT** |
| 坚果每天 1 盎司（28.4 g） | −4.8 mg/dL（95% CI −5.5 至 −4.2；换算 −0.12 mmol/L） | −2.2 mg/dL（换算 −0.025 mmol/L） | 无显著作用 | S9 | 高（61 项试验） |
| 豆奶约 500 mL/天（约 22 g 大豆蛋白）替代牛奶 | −0.19 mmol/L（95% CI −0.29 至 −0.09；换算 −7.3 mg/dL） | — | — | S28 | 中 |
| Portfolio 组合饮食 | 约 −17%，−0.73 mmol/L（95% CI −0.89 至 −0.56；换算 −28 mg/dL） | 显著降（摘要无数字） | — | S10 | 高（GRADE 对 LDL 为 high），但只有 7 组、439 人 |
| 红曲（每天 5–10 mg 莫纳可林 K） | 最多约 20% | — | — | S3 | 中；**本质是天然低剂量他汀**，成分不稳定、可能有污染物 |
| 减重（肥胖者） | 每减 10 kg，LDL 约 −0.2 mmol/L（8 mg/dL） | + | 体重稳定后每减 1 kg HDL +0.01 mmol/L（0.4 mg/dL） | S3、S13 | 中高 |
| 运动训练 | −7.22 mg/dL（换算 −0.19 mmol/L） | −8.01 mg/dL（换算 −0.09 mmol/L） | +2.11 mg/dL（换算 +0.055 mmol/L）；每周快走 25–30 km 可升 0.08–0.15 mmol/L（3.1–6 mg/dL） | S12、S3 | 高（148 项 RCT），但预测区间显示只有约 1/4 的研究各项都改善 |
| 减酒 | — | +++（>10%），对 TG 影响最大的生活方式因素之一 | — | S3 | 高（指南 A 级） |
| 少吃单糖、双糖 / 果糖 | — | 果糖长期占能量 15–20% 时，TG 可升 30–40% | — | S3 | 中 |
| 戒烟 | 无显著变化 | — | 戒烟者 +2.4 mg/dL，持续吸烟者 +0.1 mg/dL（换算 +0.062 / +0.003 mmol/L） | S15 | 中高（RCT 内比较） |
| 鱼油（处方级 n-3，2–3 g/天） | 剂量更高时可能**升高** LDL | 最多降 30% | — | S3 | 高 |

**对照：他汀能降多少。** ESC/EAS 2019 外审稿：高强度他汀方案定义为平均降 LDL-C 约 50%，中等强度为 30–50%（S3 第 8.1.2.1 节）。原文："A high-intensity regimen is defined as the dose of a statin that on average reduces LDL-C by 50%"。可靠度：高（指南定义，来自大量 RCT）。他汀本身的细节由其他研究员负责。

---

## 2. 脂肪：饱和脂肪、不饱和脂肪替代、反式脂肪

### 2.1 Cochrane 2020（Hooper）——减少饱和脂肪的硬终点证据【已证实，幅度中等】

| 结局 | RR（95% CI） | 研究数 / 人数 | GRADE |
|---|---|---|---|
| 合并心血管事件 | **0.83（0.70–0.98）** | 12 项 / 53,758 | 中 |
| 全因死亡 | 0.96（0.90–1.03） | 11 项 / 55,858 | 中 |
| 心血管死亡 | 0.95（0.80–1.12） | 10 项 / 53,421 | 中 |
| 非致死性心梗 | 0.97（0.87–1.07） | — | 低 |
| 冠心病死亡 | 0.97（0.82–1.16） | — | 低 |

- NNT：一级预防约 56（约 4 年），二级预防约 53。
- 血脂：摘要只说总胆固醇、LDL「小幅下降」，HDL、TG「几乎无影响」，没有给数字。
- 替代营养素：用 PUFA 替代与用碳水替代，亚组间无显著差异；MUFA、蛋白质替代的数据很少。
- 荟萃回归：血清胆固醇降得越多，心血管事件降得越多，这一点解释了大部分异质性。
- 原话："reducing saturated fat intake for at least two years causes a potentially important reduction in combined cardiovascular events"（S1）。
- 可靠度：高（Cochrane，15 项 RCT，56,675 人）。

### 2.2 AHA 2017 主席建议（Sacks）【指南级观点，与 Cochrane 方向一致、幅度更大】

- 摘要：RCT 中用多不饱和植物油替代饱和脂肪，心血管病**约降 30%**，与他汀降幅相近（S2）。
- 原话："conclude strongly that lowering intake of saturated fat and replacing it with unsaturated fats, especially polyunsaturated fats, will lower the incidence of CVD"。
- 建议放进 DASH、地中海饮食等整体健康饮食模式。
- 摘要里没有提椰子油（「椰子油」部分：未查到，记忆中 AHA 2017 不建议用椰子油，**未证实**）。
- **与 Cochrane 的差异（有争议的是幅度，不是方向）**：AHA 只挑选设计较好的「核心试验」，得出约 30%；Cochrane 纳入更多试验，合并心血管事件降 17%，死亡率没有显著下降。两者都支持「用不饱和脂肪替代饱和脂肪」。视频宜说「能减少心血管事件，幅度约一到三成，不同的分析结论不同」。

### 2.3 反式脂肪【已证实有害】

- ESC 外审稿：反式脂肪升 LDL 的作用与饱和脂肪相近，但饱和脂肪会升 HDL，反式脂肪会**降** HDL；工业部分氢化油是主要来源，约占总摄入的 80%（S3）。原话："while SFAs increase HDL-C levels, trans fats decrease them"。
- 中国血脂指南 2023 英文版："Avoid trans fats (hydrogenated vegetable oils, etc.)"，Class III，证据 A（S4）。
- 定量（如能量 2% 来自反式脂肪对应的冠心病风险）：Mozaffarian 2006 NEJM（PMID 16611951）摘要未读到，**未查到**。

### 2.4 指南给出的脂肪数字

| 项目 | ESC/EAS 2019（外审稿） | 中国血脂指南 2023（英文版已读部分） |
|---|---|---|
| 饱和脂肪 | <10% 总能量；高胆固醇者 <7%（S3） | 「限制饱和脂肪和反式脂肪」，用不饱和植物油替代动物油、棕榈油，IIa / A；**供能比数字未读到**（S4） |
| 总脂肪 | 范围宽；超过 35–40% 能量时常伴随饱和脂肪和总热量过多（S3） | 原文 "Total fat intake should be limited to 20–25 g per day"（表 9）；**疑为烹调油，需核对中文原文**（S4）；M1 转述为「烹调油每天不超过 25 克」 |
| 反式脂肪 | 完全避免 | 避免，III / A |
| 膳食胆固醇 | <300 mg/天，尤其是血胆固醇高的人 | 高危和高胆固醇者 <300 mg/天；中危及以上或混合型高脂血症者可考虑减少，IIa / B |
| 碳水 | 45–55% 能量；添加糖 <10% 能量 | 未读到数字；TG 高者减少精制碳水，多吃富含纤维的低糖食物（9.4 节） |
| 纤维 | 总膳食纤维 25–40 g，其中可溶性 7–13 g | 「增加膳食纤维」，未读到克数 |
| 酒 | 饮酒者 ≤10 g/天；高 TG 者戒酒 | 「TG 升高者需严格限酒」（9.4 节） |
| 运动 | 每天至少 30 分钟中等强度 | 未读到成人数字（12.7.3 节 "No less than 1 h of moderate to vigorous exercise per day" 疑为儿童部分，未核对） |

中国指南的定位：**"Lifestyle interventions are the foundation of lipid-lowering treatment."**（第 9 节，Class I，证据 B）；饮食对血脂影响最大；起始药物治疗是「中等强度他汀 + 心脏健康生活方式」（S4 摘要）。9.5 节：通过非药物治疗达标的，继续该治疗并定期复查；低危者 LDL-C 目标 <3.4 mmol/L（130 mg/dL，换算），IIa / B。

中国指南 2023 英文版表 8（只有推荐级别，没有幅度）：

| 措施 | 目标血脂 | 推荐级别 | 证据 |
|---|---|---|---|
| 控制体重 | TC、LDL-C | I | A |
| 增加运动 | TC、LDL-C | IIa | B |
| 减酒 | TG | I | A |
| 增加运动 | TG | I | A |
| 控制体重 | TG | I | A |
| 增加运动 | HDL-C | I | A |
| 控制体重 | HDL-C | I | A |
| 戒烟 | HDL-C | IIa | B |

---

## 3. 膳食胆固醇与鸡蛋【有争议：个体差异大】

| 事实 | 数字 | 出处 | 可靠度 |
|---|---|---|---|
| 膳食胆固醇每多吃 100 mg/天对应的 LDL 变化 | 线性模型 +1.90 mg/dL（换算 +0.049 mmol/L）；非线性 MM 模型 +4.46 mg/dL（+0.115）；Hill 模型 +4.58 mg/dL（+0.118）；非线性模型拟合最好（范围 0–1,500 mg/天） | S6 | 中高（55 项研究，2,652 人） |
| AHA 2019 科学建议 | 多数干预荟萃显示，摄入超过当前平均水平时总胆固醇或 LDL 升高；多国观察性研究一般**不显示**膳食胆固醇与心血管病显著相关；不设具体数字上限，改为强调饮食模式。原话：pattern-focused guidance is "more likely to improve diet quality" | S5 摘要 | 中（只读到摘要） |
| AHA 2019 对鸡蛋的说法 | 检索摘要转述：健康人每天 1 个蛋可以纳入健康饮食；胆固醇正常的老年人每天最多 2 个；素食者可适量多吃奶和蛋。**原文没有读到** | WebSearch 摘要（news-medical、Healio），全文 403 | 低（媒体转述） |
| 「超反应者」 | 每天 3 个蛋（约多 540 mg 胆固醇）吃 4 周，血胆固醇升 >12 mg/dL 的人算超反应者；摘要称"approximately 1/3 of the population"，本研究 36 人中 12 人；超反应者的 LDL、HDL 都升高，增加的主要是大颗粒 LDL | S25 | 低（会议摘要，n=36，**蛋业资助**） |
| 北欧营养推荐 2023 鸡蛋综述 | RCT 中多吃蛋"may increase serum total cholesterol concentration"，LDL/HDL 比值也会升，但"substantial heterogeneity in the response" | PMID 38370115（检索结果摘要片段，未读全文） | 中 |
| ESC 2019 食物表 | 蛋列在「适量食用」一栏，动物内脏列在「偶尔、限量」一栏 | S3 表 8 | 中 |
| 中国居民膳食指南 2022 | 八条准则之四是「适量吃鱼、禽、蛋、瘦肉」，鱼禽蛋瘦肉合计每天平均 120–200 克（M2，官方通稿）；媒体转述「蛋类每周 300–350 克，约每天 1 个全蛋、不弃蛋黄」（检索摘要与 M3 中「蛋每天吃1个」） | M2、M3 | 中（通稿）/ 低（转述） |
| 中国血脂指南 2023 | 对**高危和高胆固醇者**仍建议 <300 mg/天；M1 转述为「一般健康人不要求限制胆固醇」。一个蛋黄约 200 mg 胆固醇（检索摘要中的媒体说法，**未核对一手数据**） | S4、M1 | 高（指南）/ 低（蛋黄含量） |

「300 mg 上限被取消」：本次没有找到中国膳食指南取消该上限的原文（记忆中：2013 版中国 DRIs 和 2016 版膳食指南取消了 300 mg 上限，美国 2015–2020 膳食指南也取消了，**未证实**）。可以确定的是，2023 中国血脂指南对高危人群仍保留 <300 mg/天。

**两方论证。** 一方认为鸡蛋问题不大：观察性研究多数显示与心血管病无显著关联（S5），且多数人的反应较弱（S6 线性模型下每 100 mg 只升约 2 mg/dL）。另一方认为不能放开：干预试验确实显示升 LDL（S5、S6），个体差异大，约 1/3 是超反应者（S25，证据弱），而高危、高胆固醇人群仍有指南上限（S4）。结论：健康人每天约 1 个蛋多数指南可接受；高胆固醇、高危、家族性高胆固醇血症者应听医生的。

---

## 4. 纤维、植物甾醇、坚果、大豆、Portfolio、地中海饮食

- **燕麦 β-葡聚糖**：≥3 g/天（试验剂量 3.0–12.4 g/天），LDL −0.25 mmol/L，总胆固醇 −0.30 mmol/L（换算 −11.6 mg/dL），HDL、TG 无显著影响（S7）。FDA 健康声明原文（21 CFR 101.81）**未读到**（记忆中：每天 3 g 燕麦 / 大麦 β-葡聚糖或 7 g 车前子可溶性纤维，每份 ≥0.75 g / 1.7 g，并需配合低饱和脂肪、低胆固醇饮食，**未证实**）。一碗燕麦含多少 β-葡聚糖：**未查到**。
- **植物甾醇**：2 g/天，LDL 降 8–10%，与他汀叠加，"equivalent to doubling the dose of statin"（S8）；"no randomised, controlled clinical trial data with hard end-points"（S8）。适合人群（S8、S3 一致）：① 胆固醇高、总体风险中低、不需要用药的人；② 高危或极高危者用他汀不达标或不耐受时作为辅助；③ 成人及 6 岁以上的 FH 儿童。日常饮食只含约 250–500 mg/天（S3），**2 g 要靠强化食品**。
- **坚果**：见总表（S9）。ESC 食物表：坚果「所有不加盐的」都可适量吃，椰子除外（S3）。
- **大豆**：豆奶替代牛奶 LDL −0.19 mmol/L（S28）；ESC 外审稿说大豆蛋白替代动物蛋白有 modest 作用，"this was not confirmed when changes in other dietary components were taken into account"（S3）。【有争议】
- **Portfolio 饮食**（Jenkins 团队，组合植物甾醇、黏性纤维、坚果、大豆蛋白）：LDL 约 −17%（S10）。原话："~17%"，GRADE 对 LDL "high"。这是「单项食物的效果可以叠加」的最好证据。
- **地中海饮食 PREDIMED（2018 重发版）**：7,447 名 55–80 岁、高心血管风险但尚无心血管病的人，中位随访 4.8 年。主要终点（心梗、卒中、心血管死亡）：特级初榨橄榄油组 HR 0.69（0.53–0.91），坚果组 HR 0.72（0.54–0.95），对照为低脂饮食；事件率 3.8% / 3.4% / 4.4%（S11）。撤稿原因：有的家庭成员未经随机就入组，11 个中心中有 1 个未随机分配，另一中心随机表使用不一致；作者撤回 2013 版，用不完全依赖随机假设的分析重新估计（S11）。可靠度：中高（RCT，但随机化有瑕疵；绝对风险差约 1 个百分点）。
- 注意：PREDIMED 降的是**事件**，这一效果不主要靠降 LDL；对照组也是健康的低脂饮食。

---

## 5. 体重、运动、酒精、吸烟、睡眠

- **减重**：LDL 降幅小，肥胖者每减 10 kg 约降 0.2 mmol/L（8 mg/dL）（S3）。原话："the magnitude of the effect is small"。HDL 在减重进行时会小幅下降（每公斤 −0.007 mmol/L），体重稳定后回升（每公斤 +0.009 mmol/L）（S13；ESC 取整为 +0.01 mmol/L/kg）。减重 5–10% 即可改善血脂异常；对死亡与心血管结局的获益"less clear"（S3）。每天热量缺口 300–500 kcal（S3）。
- **运动**：对 LDL 作用小。"The reduction of LDL-C levels induced by regular physical exercise is even smaller"（S3）。148 项 RCT 中 LDL 约 −0.19 mmol/L，TG 约 −0.09 mmol/L，HDL 约 +0.055 mmol/L；有氧加抗阻的联合训练"optimal"（S12）。运动在减重之外还能额外降 TG（S3）。运动的主要价值在血压、血糖、体能等其他风险因素（S3）。
- **酒精**：
  - 血脂：酒精对 TG 影响很大，尤其是高 TG 者（S3）；高 TG 者应戒酒（S3 Box S1）；中国指南要求 TG 高者严格限酒（S4）。
  - 「少量饮酒有益」：107 项队列、约 484 万人，校正「戒酒者偏倚」（把因病戒酒的人算作不饮酒者）后，少量饮酒（1.3–24 g/天）对比终生不饮酒者 RR 0.93，P=0.07，不显著；45–64 g/天 RR 1.19，≥65 g/天 RR 1.35；女性风险起点更低（S14）。原话："daily low or moderate alcohol intake was not significantly associated with all-cause mortality risk"。可靠度：中高（观察性，但处理了关键偏倚）。【过去的「少量有益」说法证据已动摇；不应为了「护心」开始喝酒】
  - 中国膳食指南 2022 限酒：媒体转述「男女一致下调到 15 克酒精」（M3），**未读到原文**。
- **吸烟 / 戒烟**：戒烟一年左右，HDL +2.4 mg/dL，持续吸烟者 +0.1 mg/dL，戒烟者同时多增重 4.6 kg 对 0.7 kg；LDL 无显著变化（S15；样本量摘要中未给出）。戒烟的心血管获益远超 HDL 本身（S3："clear benefits on the overall CV risk"）。
- **睡眠**：**未查到**（ESC 外审稿只把阻塞性睡眠呼吸暂停列为风险相关情况，没有血脂幅度）。

---

## 6. 低碳 / 生酮、间歇性断食、中国常见饮食

- **生酮 / 很低碳水**【有争议，个体差异巨大】
  - ESC 外审稿："there is no justification for the recommendation of very low carbohydrate diets"；碳水占能量低于 40% 或高于 70% 都与较高死亡率相关，45–55% 时最低（观察性荟萃，S3）。
  - 减少碳水能降 TG（ESC 表 7：++，A 级），用不饱和脂肪替代碳水可升 HDL（++，A）（S3）。
  - 部分人 LDL 大幅升高：一项针对特定生酮人群的病例对照研究中，生酮组 LDL 平均 272 mg/dL（换算 7.03 mmol/L），对照 123 mg/dL（3.18 mmol/L）（S26 Budoff 2024；人群经过选择，不代表所有生酮者）。2026 JAHA 综述：BMI 正常的成人在短期试验中 LDL 平均上升 18–70 mg/dL（换算 0.47–1.81 mmol/L）（S26）。
  - 所谓「瘦体型超反应者（lean mass hyper-responder）」的 KETO-CTA 研究（Soto-Mota 2025 JACC Adv）在 Europe PMC 记录中显示有关注声明和撤稿条目，**引用前必须核实**（S26）。
  - 「BMI 越低、低碳后 LDL 升得越多」：只在上述摘要中以「先前发现的负相关」出现，**未找到原始荟萃**。
- **间歇性断食**：9 项 RCT（脂肪肝人群，n=894）对比持续限能量，LDL 只多降 0.08 mmol/L（换算约 3 mg/dL），TG、HDL 无差异（S27）。可以认为它不比普通减少热量更神奇（人群局限，可靠度中）。
- **中国常见饮食**：
  - ESC 食物表（S3 表 8）：精制面包、米饭、面条属于「适量」；糕点、含糖饮料、香肠、培根、**动物内脏**属于「偶尔、限量」；**猪油、黄油、棕榈油、椰子油**和油炸属于「偶尔、限量」；烹调方式优先烤、煮、蒸。
  - 中国指南：用不饱和植物油替代动物油、棕榈油；TG 高者少吃高脂食物和精制碳水，多吃全谷物、粗粮（S4）。
  - 含糖饮料 / 果糖：果糖 >10% 能量会升 TG；15–20% 能量时 TG 升 30–40%；TG 高或腹型肥胖者应严格限制含糖饮料（S3）。
  - 猪油、内脏、油炸对中国人血脂的专门研究：**未查到**。

---

## 7. 鱼油

| 试验 | 制剂 / 剂量 | 对照 | 人群 | 主要结果 | 房颤 / 出血 |
|---|---|---|---|---|---|
| REDUCE-IT 2019（S16） | 纯化 EPA（icosapent ethyl）2 g，每天 2 次 | 「安慰剂」，实为矿物油 | n=8,179，用他汀，TG 135–499 mg/dL（1.52–5.63 mmol/L），中位 4.9 年 | 17.2% 对 22.0%，**HR 0.75（0.68–0.83）** | 房颤 / 房扑住院 3.1% 对 2.1%（P=0.004）；严重出血 2.7% 对 2.1%（P=0.06） |
| STRENGTH 2020（S18） | EPA+DHA 羧酸 4 g/天 | 玉米油 | n=13,078 | 12.0% 对 12.2%，HR 0.99（0.90–1.09）；因 "low probability of clinical benefit" 提前终止 | 摘要未报 |
| VITAL 2019（S19） | 普通剂量鱼油 1 g/天 | 安慰剂 | n=25,871，≥50 岁一般人群，中位 5.3 年 | 主要心血管终点 HR 0.92（0.80–1.06），不显著；总心梗 HR 0.72（0.59–0.90，次要终点） | — |
| OMEMI 2021（S20） | n-3 1.8 g/天（EPA 930 mg + DHA 660 mg） | 玉米油 | n=1,027，70–82 岁心梗后，2 年 | 21.4% 对 20.0%，HR 1.08（0.82–1.41） | 房颤 7.2% 对 4.0%，HR 1.84（0.98–3.45），P=0.06 |

- **矿物油安慰剂争议**【有争议】：REDUCE-IT 中，矿物油组 12 个月 LDL **+10.9%**，EPA 组 −1.2%；矿物油组 hsCRP +21.9%，IL-1β +28.9%，IL-6 +16.2%，而 EPA 组变化很小（S17）。作者原话：其对总体风险下降的解读影响"uncertain"（S17）。一方观点：疗效有一部分可能来自对照组变差（STRENGTH 用玉米油对照，结果为阴性）。另一方观点：生物标志物升幅只能解释一小部分（这一观点本次**未查到**原文定量，记忆中 FDA 评审认为矿物油不能完全解释 25% 的降幅，**未证实**）。另外，REDUCE-IT 的是处方药纯化 EPA，**不能外推到普通鱼油保健品**。
- **房颤**：7 项 RCT、81,210 人，鱼油使房颤风险 HR 1.25（1.07–1.46）；>1 g/天 HR 1.49，≤1 g/天 HR 1.12（S21）。
- **降 TG**：处方剂量 2–3 g/天，TG 最多降 30%；剂量更高时可能升 LDL（S3）。保健品胶囊每粒实际含多少 EPA+DHA：**未查到**。
- 结论：普通剂量鱼油保健品（约 1 g/天）在一般人群中没有显著减少主要心血管事件（VITAL），还会小幅增加房颤风险；吃鱼（每周至少 2 次）与较低的心血管死亡相关，但对血脂影响不大（S3，观察性）。

---

## 8. 保健品与偏方

| 产品 / 说法 | 证据 | 结论 | 出处 | 可靠度 |
|---|---|---|---|---|
| 生大蒜 / 大蒜粉 / 陈蒜提取物 | 192 人 RCT，6 个月，每天约 1 瓣的剂量：三种形式 LDL 均无显著变化（+0.4、+3.2、+0.2 mg/dL；安慰剂 −3.9 mg/dL） | "None of the forms of garlic used in this study" had significant effects | S22 | 高（设计好的 RCT） |
| 大蒜荟萃 | 陈蒜提取物 LDL −4.41 mg/dL（−8.28 至 −0.54；换算 −0.11 mmol/L），I² 56%；另一荟萃 LDL −8.20 mg/dL（换算 −0.21 mmol/L） | 作用小且异质性大，作者也要求更多高质量试验 | S23 | 中低 |
| 纳豆激酶 | 265 名低危健康人，2,000 FU/天，中位 3 年：颈动脉内中膜厚度进展与安慰剂无差异，各项化验指标无显著影响 | "has a null effect on subclinical atherosclerosis progression" | S24 | 中高（RCT） |
| 纳豆激酶 + 红曲复方 | LDL −0.43 mmol/L（换算 −16.6 mg/dL） | 降脂作用来自**红曲**（天然洛伐他汀），不能算作纳豆激酶的效果 | PMID 37836525（Nutrients 2023） | 中 |
| 红曲 | 每天 5–10 mg 莫纳可林 K，LDL 最多降约 20%；部分纯化提取物在一项 ASCVD 患者 RCT 中使复发事件降 45%；含量不一、可能有污染物，有类似他汀的副作用 | 有效，正因为它就是低剂量他汀；需要监管 | S3 | 中 |
| 深海鱼油 | 见第 7 节 | 降 TG，不降 LDL；普通保健品剂量对硬终点无显著获益 | S16–S21 | 高 |
| 普利醇（policosanol） | 对 LDL、HDL、TG、apoB、Lp(a) 均无显著作用 | 无效 | S3 | 中高 |
| 小檗碱 | 降 LDL、TG 优于对照，但缺乏高质量 RCT，不同制剂生物利用度有争议 | 尚不清楚 | S3 | 低 |
| 卵磷脂 | **未查到** | — | — | — |
| 苹果醋 | **未查到** | — | — | — |
| 「洗血 / 血液净化」「通血管」 | **未查到**一手资料（记忆中：脂蛋白单采是 FH 等少数病人的医院治疗，不是保健手段，**未证实**） | — | — | — |

---

## 9. 关键结论：生活方式能降多少、对谁够、和药物什么关系

| 问题 | 结论 | 依据 | 证据状态 |
|---|---|---|---|
| 单项措施能降多少 LDL | 多数单项只降 3–10%：燕麦约 0.25 mmol/L，甾醇 8–10%，坚果约 0.12 mmol/L，减重 10 kg 约 0.2 mmol/L，运动约 0.19 mmol/L | 第 1 节总表 | 已证实 |
| 组合起来最多降多少 | Portfolio 组合饮食约 17%（−0.73 mmol/L）；饱和脂肪换成植物油可降 0.20–0.42 mmol/L | S10、S3 | 已证实（试验条件下，现实中依从性会打折扣） |
| 他汀降多少 | 中等强度 30–50%，高强度约 50% | S3 | 已证实 |
| 对谁可能够 | 总体风险中低、LDL 轻中度升高、不需要用药的人；指南把甾醇、红曲推荐给这类人（S8、S3）；中国指南：非药物治疗达标的继续并定期复查（S4 9.5 节） | S3、S4、S8 | 指南意见 |
| 对谁不够 | 杂合子 FH：患病率约 1/200–1/250，未经治疗的男性多在 55 岁前、女性多在 60 岁前得冠心病，风险至少高 10 倍；儿童 FH 也要健康饮食加他汀（6–10 岁起考虑），>10 岁目标 LDL <3.5 mmol/L（135 mg/dL）（S3 9.1.2 节）。高危、极高危人群：中国指南起始治疗即为「中等强度他汀 + 生活方式」（S4） | S3、S4 | 已证实（FH 的定性）；「生活方式对 FH 降幅不够」**没有读到直接定量数据**，依据是 17% 的上限与 FH 常见的 LDL 水平推断 |
| 是替代还是叠加 | 叠加：甾醇与他汀叠加，相当于他汀剂量翻倍（S8）；中国指南把生活方式定为 "foundation"，药物是在其基础上加（S4） | S4、S8 | 已证实（LDL 层面） |
| 硬终点 | 减饱和脂肪：合并心血管事件 −17%（S1）；地中海饮食：HR 约 0.7（S11）；减重对死亡与心血管结局的获益 "less clear"（S3）；甾醇无硬终点 RCT（S8） | S1、S3、S8、S11 | 部分证实 |

---

## 给视频的建议

**最值得讲的 5 点**
1. **「一招降很多」不存在，但「很多招加起来」有用。** 单项通常 3–10%；Portfolio 组合约 17%；他汀 30–50%。可以画成「降脂量尺」：一格一格累加的小方块对比一根长条。
2. **饱和脂肪换成植物油，是饮食里对 LDL 最有力的一招**（ESC："the dietary factor with the greatest impact on LDL-C levels"），而且有硬终点证据（Cochrane：心血管事件 −17%）。注意说「换成」，不是「少吃油然后换成白米饭」。
3. **运动和减重对 LDL 作用小，对 TG、HDL、血压、血糖作用大。** 凯可以问「我天天跑步，LDL 怎么没怎么降？」，正好讲清这一点。
4. **TG 高时先看酒和糖。** 酒对 TG 的作用 >10%，高 TG 者应戒酒；含糖饮料和果糖要限制。
5. **生活方式是地基，药是在地基上盖楼，两者叠加，不是二选一。** 家族性高胆固醇血症是天生 LDL 受体有缺陷，光靠吃不够。

**最容易讲错的地方**
- 不要说「鸡蛋随便吃」或「鸡蛋绝对不能吃」。准确的说法：健康人每天约 1 个蛋多数指南可接受；个体差异大；高胆固醇、高危者听医生的（中国血脂指南仍建议高危者 <300 mg/天）。
- 不要说「少量饮酒护心」。最新校正偏倚后的荟萃显示没有显著获益。
- 不要把 REDUCE-IT 的结果套到超市鱼油上：那是处方纯化 EPA、4 g/天、人群是 TG 高且在用他汀的人，安慰剂（矿物油）也有争议。普通鱼油不降 LDL，>1 g/天还会增加房颤风险。
- 不要说「红曲是天然的、比他汀安全」：它的有效成分就是洛伐他汀类物质，含量不稳定，也有副作用。
- 不要说地中海饮食「降胆固醇」：PREDIMED 降的是心血管事件，绝对差约 1 个百分点，且有随机化瑕疵后重发的背景。
- 「生酮让我瘦了，所以血脂一定变好」：TG 往往下降，但部分人 LDL 会大幅上升（一项选择人群的研究平均 7 mmol/L 以上）。
- 数字单位：中国化验单用 mmol/L，英文观众习惯 mg/dL，画面两者都标。

**可以怎么画（真实的 vs 只能示意的）**
- 真实可画：
  - 燕麦 β-葡聚糖在肠道里形成黏稠凝胶、裹住胆汁酸带走（机制真实，形态为示意）；
  - 植物甾醇和胆固醇在肠道微团里「抢座位」（S3："compete with cholesterol for intestinal absorption"；分子大小相近，画面可画两种相似的分子）；
  - 反式脂肪的直链 vs 顺式不饱和脂肪的弯折（分子形状真实）；
  - 饱和脂肪在室温下是固体（猪油、黄油），植物油是液体（真实可拍）。
- 只能示意：「LDL 浓度上升」画成血管里颗粒变密，标「示意」；LDL 颗粒直径约 20–25 nm（**本文未查证**，由负责 LDL 结构的研究员核对）。
- 量化可视化：用同一把尺子并排放「燕麦 0.25、坚果 0.12、减重 10 kg 0.2、Portfolio 0.73、他汀 30–50%」，单位统一为 mmol/L 或百分比，避免混用。

**观众最可能的误解**
- 「我瘦 / 我运动，所以胆固醇不会高」：FH 和遗传因素与体重无关；运动对 LDL 作用小。
- 「吃保健品可以代替吃药」：大蒜、纳豆激酶、普利醇的高质量 RCT 多为阴性；有效的（红曲）本身就是药。
- 「生活方式改了就能停药」：中国指南写的是生活方式 + 药物；达标后是否减药由医生判断，不能自己停。
- 「植物油随便多吃」：替代是关键，总热量仍要控制；中国指南建议烹调油限量（具体克数以中文原文为准，待核）。
- 「HDL 越高越好，所以我喝酒升 HDL」：喝酒升 HDL 不等于获益；酒同时升 TG。

**本文的局限（制作前需补）**
- 中国血脂指南 2023 中文原表的全部数字（饱和脂肪供能比、BMI、运动、限酒克数）尚未核对。
- ESC 2019 数字来自外审稿，需对终稿（EHJ 2020;41:111–188）核对。
- 鸡蛋的 AHA 具体个数只有媒体来源。
- 睡眠、卵磷脂、苹果醋、「洗血」、「通血管」、FDA 燕麦声明原文均未查到。
