---
worker_id: researcher-05-scenarios
stage: 3
role: researcher
angle: guidelines-scenarios
status: partial
blockers:
  - "中国 2023 指南的「超高危」具体条目（哪些算严重 ASCVD 事件、哪些算高风险因素）在英文全文里是流程图图片，中文原文全文没取到，所以本文没有核实这些条目"
  - "中国 2023 指南 CKD 直接列为高危的分期两处说法不一：Frontiers 英文版写 3–5 期，中文解读写 3~4 期；未读到中文原文核对"
  - "中国 2023 指南余生风险评估的年龄条件英文版自相矛盾（Key Points 写 <55 岁，正文写 >55 岁）；未读到中文原文核对"
  - "中国 FH 诊断标准（2018 中国专家共识）原文未读到；只读到二手综述里的筛查入选条件"
  - "ESC/EAS 2019 的风险分层定义表（Table 4）和监测表（Table 13）在网页版是图片；ESC 2025 重点更新的推荐表也是图片，部分推荐等级来自 ESC 官方 CardioPractice 解读和 PACE-CME，不是原表"
  - "ACC/AHA 2026 期刊站（jacc.org）返回 403；全文是从第三方（Randox 新闻站）托管的 PDF 抽文本读的，引用仍写官方 DOI；Figure 1（目标值总表）是图片，目标值取自各条推荐正文"
  - "WebSearch 用了 13 次（配额 20 次）；剩下的缺口靠搜索补不上，需要中文原文 PDF"
confidence: medium
---

# 不同情景怎么处理：指南怎么说（中国 2023 / ESC-EAS 2019+2025 / ACC-AHA 2026）

> 写作规则：每一条都标出处（指南、节号或推荐表、推荐等级/证据级别）。「未证实」= 本次没读到原文，只是记忆或二手资料。mg/dL 换算：胆固醇类 ×38.67，TG ×88.57（四舍五入；指南自己给的 mg/dL 数字和换算结果有 ±1 的差异属正常）。

## 0. 来源与可靠度总表

| 代号 | 文献 | 版本状态（截至 2026-11） | 本次怎么读的 | 可靠度 |
|---|---|---|---|---|
| **CN2023** | 中国血脂管理指南修订联合专家委员会. *2023 Chinese guideline for lipid management*. Front Pharmacol 2023;14:1190934. https://pmc.ncbi.nlm.nih.gov/articles/PMC10498001/ （中文原版：《中国血脂管理指南（2023年）》，2023-03 发布；另有英文版 J Geriatr Cardiol 2023;20(9):621–663，DOI 10.26599/1671-5411.2023.09.008） | 中国目前最新的完整版指南 | PMC 全文抽读（约 38 万字符，读了正文部分；表格、流程图部分没抽到） | 高（官方指南英文版），个别条目和中文解读有出入，见 blockers |
| **CN2024基层** | 中国血脂管理指南修订联合专家委员会. 中国血脂管理指南（基层版2024年）. 中国全科医学 2024;27(20):2429–2436. DOI 10.12114/j.issn.1007-9572.2024.0005 | 2023 版的基层落地版 | 只读到摘要（https://search.napstic.cn/literature/periodical/010zgqkyx202420002） | 中（只有摘要） |
| **ESC2019** | Mach F, et al. *2019 ESC/EAS Guidelines for the management of dyslipidaemias*. Eur Heart J 2020;41:111–188. https://academic.oup.com/eurheartj/article/41/1/111/5556353 | 仍是欧洲主指南，2025 年有重点更新 | 网页全文抽读（推荐表多为图片） | 高（正文）；表格内容未读 |
| **ESC2025** | Mach F, et al. *2025 Focused Update of the 2019 ESC/EAS Guidelines for the management of dyslipidaemias*. Eur Heart J 2025;46(42):4359. DOI 10.1093/eurheartj/ehaf190. https://academic.oup.com/eurheartj/article/46/42/4359/8234482 | 2025-08-29 发布 | 正文抽读 + ESC 官方解读（Guasti 等，ESC CardioPractice，2025-12-02）+ PACE-CME 报道（2025-09-25） | 正文高；推荐等级来自解读，中 |
| **ACC2026** | Blumenthal RS, Morris PB, et al. *2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia*. J Am Coll Cardiol 2026，同时刊于 Circulation。DOI 10.1016/j.jacc.2025.11.016（2026-03-13 在线发布） | **取代** 2018 AHA/ACC 胆固醇指南（原文：“this guideline retires and replaces the previously published 2018 … Guideline on the Management of Blood Cholesterol”，§1.5） | 全文 PDF 抽文本（第三方托管副本：news.randox.com/wp-content/uploads/2026/04/2026-Guideline-on-the-Management_compressed.pdf），另读 ACC 新闻稿 https://www.acc.org/About-ACC/Press-Releases/2026/03/13/18/01/ACCAHA-Issue-Updated-Guideline-for-Managing-Lipids-Cholesterol | 高（原文推荐表逐字读到） |

**版本结论**
- 中国：2023 版是最新完整版，2024 年出了基层版（摘要说“以 LDL-C 作为首要靶点…以中等强度他汀起始…必要时联用胆固醇吸收抑制剂和（或）PCSK9 抑制剂”）。2016 版《中国成人血脂异常防治指南》已被 2023 版替代（CN2023 摘要：“update the 2016 Chinese dyslipidemia guideline”）。指南名字从“血脂异常防治”改成了“血脂管理”，因为同一个 LDL-C 数值放在不同风险的人身上意义不同（CN2023 摘要；cn-healthcare 解读 2023-03-26）。
- 欧洲：2019 主指南加 2025 重点更新。ESC 官方解读原话：“LDL-C treatment goals in each CV risk category have not changed from the 2019 Guidelines”。
- 美国：**2026 ACC/AHA 血脂异常指南已经取代 2018 版**。主要变化（ACC2026 Top Take-Home Messages）：①改用 PREVENT 方程（30–79 岁，算 10 年和 30 年风险），不再用 PCE；②**重新给出 LDL-C / 非 HDL-C 目标值**（2018 版没有目标值）；③所有成人一生至少测一次 Lp(a)；④CAC 用于重新分层；⑤糖尿病、CKD 3–4 期、HIV 患者 40–75 岁不看 LDL-C 数值都推荐降脂；⑥二级预防极高危目标 <55 mg/dL；⑦更早治疗（年轻人、LDL-C ≥160 mg/dL）。
- 未查：NLA、NICE、日本 JAS 的最新版（本角度没搜）。

---

## 1. 化验单怎么看

### 1.1 中国 2023 指南的血脂分层切点（CN2023 Table 2）

原文适用范围：“Reference standard for ASCVD, primary prevention low-risk population only”（只用于**没有心血管病、风险低**的一级预防人群），且基于空腹 12 小时的测量。英文版用的是 Ideal / Reasonable / Slight elevation / Elevation / Reduction，对应中文的「理想 / 合适 / 边缘升高 / 升高 / 降低」。

| 指标 | 理想 | 合适 | 边缘升高 | 升高 | 降低 |
|---|---|---|---|---|---|
| TC | – | <5.2 mmol/L（<201 mg/dL） | 5.2–<6.2（201–<240） | ≥6.2（≥240） | – |
| LDL-C | <2.6（<101，即约 100） | <3.4（<131） | 3.4–<4.1（131–<159） | ≥4.1（≥159，即约 160） | – |
| HDL-C | – | – | – | – | <1.0（<39，即约 40） |
| TG | – | <1.7（<151，即约 150） | 1.7–<2.3（150–<204） | ≥2.3（≥204，即约 200） | – |
| 非 HDL-C | <3.4（<131） | <4.1（<159） | 4.1–<4.9（159–<189） | ≥4.9（≥189，即约 190） | – |
| Lp(a) | – | <300 mg/L（=<30 mg/dL） | – | ≥300 mg/L（≥30 mg/dL） | – |

- 可靠度：高（指南原表）。mg/dL 为本文换算。
- **单位提醒**：中国指南 Lp(a) 用 **mg/L**，300 mg/L = 30 mg/dL；欧美用 mg/dL 或 nmol/L。mg/dL 和 nmol/L **没有固定换算系数**（ACC2026 Table 4 注：“Equivalence of levels between nmol/L and mg/dL is approximate”）；ACC 写 50 mg/dL≈125 nmol/L，ESC 写 50 mg/dL≈105 nmol/L——两份指南的近似换算本身就不同。
- ApoB：中国把 **ApoB ≥1.3 g/L** 列为风险增强因素（CN2023 Table 1）；ACC2026 把 **apoB ≥120 mg/dL** 列为风险增强因素（Table 13），把 apoB >140 mg/dL 归入“重度高胆固醇血症”定义（§4.2.4.3 注）。

### 1.2 化验单「正常范围」≠ 你的目标

| 要点 | 出处与原话 | 可靠度 |
|---|---|---|
| 上表只适用于低危、没得过心血管病的人 | CN2023 Table 2 标题：“primary prevention low-risk population only” | 高 |
| 一般人「正常」的 LDL-C，对超高危/极高危病人就是「明显升高」 | CN2023（JGC 版摘要）：“an LDL-C level that is normal in the general population may be considered significantly ‘elevated’ in patients with ultra (very) high risk of ASCVD” | 高 |
| 年轻人在「中年人看来正常」的数值就该开始干预生活方式 | ACC2026 §4.2.8.2：“counseling around health behaviors … should begin even at lipid levels that would be considered normal for middle-aged adults” | 高 |
| 年轻时 LDL 随年龄上升是「常见」不是「理想」 | ACC2026 §4.2.8.2：LDL-C/非 HDL-C 平均每年升 1–2 mg/dL，“this normative increase should not be perceived as optimal” | 高 |

### 1.3 要不要空腹

| 指南 | 说法 | 等级 |
|---|---|---|
| CN2023 §检测 | TC 空腹、非空腹都行（“no significant difference”）；**非空腹 TG ≥4.5 mmol/L（≥399 mg/dL，约 400）要改抽空腹血**；TG ≥4.5 时 Friedewald 公式不能用，改直接测 LDL-C | 未标等级 |
| ESC2019 §5.4.3 | “For general risk screening, non-fasting samples seem to have at least the same prognostic value as fasting samples”；TG >4.5 mmol/L（>400 mg/dL）Friedewald 公式不能用 | 正文 |
| ACC2026 §3.2 | 成人和儿童用空腹或非空腹血脂都可以（1, B-NR）；有早发 ASCVD 家族史、已知/可疑 TG 代谢异常、或非空腹 TG ≥400 mg/dL（4.5 mmol/L）的人**要空腹复查**（1, B-NR）；LDL-C 推荐用 Martin/Hopkins 或 Sampson/NIH 公式算，不用 Friedewald（1, B-NR）；**报告单应给出非 HDL-C**（1, B-NR）；不推荐常规做 LDL 颗粒大小等高级脂蛋白检测（3: No Benefit, B-NR） | 见括号 |
| ACC2026 §3.4 | Lp(a) 不需要空腹（“Fasting is not required for Lp(a) testing”）；ApoB 不受空腹影响（§3.3） | 正文 |

### 1.4 多久查一次血脂（未用药的人）

| 指南 | 推荐 |
|---|---|
| CN2023 §8 | <40 岁成人每 2–5 年一次；≥40 岁每年至少一次；高危人群按个体化需要；**高危人群至少查一次 Lp(a)**；有 ASCVD 史、多个危险因素、早发 ASCVD 家族史、黄色瘤的人尤其要查（未标等级） |
| ACC2026 §3.1 | 成人 **19 岁开始**，至少每 5 年一次（1, B-NR）；儿童 **9–11 岁**普查一次（1, B-NR）；一、二级亲属有早发 ASCVD / 重度高胆固醇 / FH 的，**2 岁起**可做一次血脂（级联筛查）（2a, B-NR） |
| ESC2019 Box 5 | 男性 >40 岁、女性 >50 岁或绝经后应考虑查血脂 |

---

## 2. 风险分层与目标值

### 2.1 中国 2023 的分层流程（CN2023 §5）

| 层级 | 怎么判定（已核实部分） | LDL-C 目标（CN2023 Table 6） | 等级 |
|---|---|---|---|
| **超高危** | 已有 ASCVD，且「≥2 次严重 ASCVD 事件」或「1 次严重 ASCVD 事件 + ≥2 个高风险因素」（原文：“those who have had ≥2 severe ASCVD events or 1 severe ASCVD event combined with ≥2 high-risk factors are classified as ultra-high-risk population”） | **<1.4 mmol/L（<54 mg/dL，约 55）且较基线降 >50%** | I, A |
| **极高危** | 其余 ASCVD 患者（“Other ASCVD patients are classified as very high-risk”） | **<1.8 mmol/L（<70 mg/dL）且较基线降 >50%** | I, A |
| **高危（直接判定，不用算分）** | ① LDL-C ≥4.9 mmol/L（≥190 mg/dL）或 TC ≥7.2 mmol/L（≥278 mg/dL）；② 糖尿病且 ≥40 岁；③ CKD 3–4 期（中文解读）/3–5 期（英文版）——见 blockers | <2.6 mmol/L（<100 mg/dL） | I, A |
| **中危 / 高危（按 10 年风险算）** | 10 年 ASCVD 风险：低危 <5%，中危 5%–9%，高危 ≥10% | 中危、高危都是 <2.6 mmol/L | I, A |
| **低危** | 同上 <5% | <3.4 mmol/L（<131 mg/dL） | IIa, B |

- 非 HDL-C 目标 = LDL-C 目标 + 0.8 mmol/L（Table 6 注）。
- **余生风险**：10 年风险为中危的人再看余生风险；有以下 ≥2 项算余生高危：收缩压 ≥160 或舒张压 ≥100 mmHg、非 HDL-C ≥5.2 mmol/L（≥201 mg/dL）、HDL-C <1.0 mmol/L、BMI ≥28 kg/m²、吸烟。年龄条件英文版自相矛盾（见 blockers）。**未证实**（记忆中中文原文是「年龄 <55 岁」的中危人群）。
- **风险增强因素**（CN2023 Table 1，多个增强因素时“更倾向按高危处理”——cn-healthcare 解读）：CAC ≥100 AU；颈动脉 IMT ≥0.9 mm 或斑块；ABI <0.9；左室肥厚；非 HDL-C ≥4.9 mmol/L；ApoB ≥1.3 g/L；Lp(a) ≥500 mg/L（50 mg/dL）；TG ≥2.3 mmol/L；hs-CRP ≥2.0 mg/L；肥胖或腹型肥胖；早发心血管病家族史（男 <55 岁、女 <65 岁发病）。
- 超高危的「严重 ASCVD 事件」「高风险因素」具体条目：**未查到原文**（记忆中：严重事件 = 近 1 年内 ACS、既往心梗、缺血性卒中、有症状的外周动脉疾病；高风险因素 = 多血管床病变、早发冠心病、FH 或基线 LDL-C ≥4.9、既往 CABG/PCI、糖尿病、高血压、CKD 3–4 期、吸烟、最大耐受他汀后 LDL-C ≥2.6 等）。注意：下面 ACC2026 的「极高危」定义已核实，和这个记忆版本几乎一样，可作旁证但不能代替中国原文。
- **用药起点**：中等强度他汀作为起始治疗（Table 7，I, A）；超高危且基线 LDL-C 高（服他汀时 ≥2.6 mmol/L 或未服他汀时 ≥4.9 mmol/L）的人可以**一开始就他汀 + PCSK9 抑制剂**（Table 7，IIa, A）。
- 可靠度：高（已核实部分）。

### 2.2 欧洲 ESC/EAS

| 层级 | 定义（已核实） | LDL-C 目标（ESC2019 Table 7 / §6，2025 未改） |
|---|---|---|
| 极高危 | 一级预防：SCORE2 / SCORE2-OP ≥20%（ESC2025，据 ESC 官方解读）；已有 ASCVD 等（2019 Table 4 是图片，未读） | **<1.4 mmol/L（<55 mg/dL）且降幅 ≥50%** |
| 高危 | SCORE2 / SCORE2-OP 10%–<20% | **<1.8 mmol/L（<70 mg/dL）且降幅 ≥50%**（2019 原文：“an LDL-C goal of <1.8 mmol/L (<70 mg/dL)”，降幅要求为本文据 2019 表述整理，**未证实**原表） |
| 中危 | SCORE2 / SCORE2-OP 2%–<10% | <2.6 mmol/L（<100 mg/dL） |
| 低危 | <2% | **<3.0 mmol/L（<116 mg/dL）**——比中国低危的 3.4 更严 |
| 2 年内再发 | 最大耐受他汀下 2 年内第二次血管事件 | 可考虑 <1.0 mmol/L（<40 mg/dL）（2019 原话：“may be considered”） |

- ESC2025：SCORE2 用于 40–69 岁、SCORE2-OP 用于 ≥70 岁（官方解读与 PACE-CME：I, B；EHJ 正文写的是 40–89 岁无已知心血管病的人）。
- 直接判为高危/极高危、不用算分的人（ESC2019 §4.1）：已确诊心血管病、病程长的老年糖尿病、FH、CKD。具体切点（如 2019 版“LDL-C >4.9 mmol/L 为高危”）在 Table 4 图片里，**未证实**。
- 风险修正因素：Lp(a) >50 mg/dL（105 nmol/L）（IIa, B）；影像发现亚临床动脉粥样硬化或 CAC 升高，用于中危人群重新分层（IIa, B）（ESC2025，据 ESC 官方解读）。

### 2.3 美国 ACC/AHA 2026：PREVENT 方程与「CPR」流程

- **PREVENT**（AHA 2023 年发布的方程）：适用 30–79 岁、没有 ASCVD 或亚临床动脉粥样硬化、LDL-C 70–189 mg/dL（1.8–4.9 mmol/L）的人（§4.2.3.2，1, B-NR）。输入：年龄、性别、血压、TC 和 HDL-C、糖尿病、吸烟、eGFR、是否在服他汀、是否在服降压药；**不含种族**；可选输入白蛋白尿、HbA1c、邮编（社会决定因素）（Table 11）。从约 330 万美国成人数据推导。**注意：PREVENT 不含 LDL-C**（Table 13 注）。
- 「CPR」：Calculate 10 年风险 → Personalize（看风险增强因素）→ Reclassify（选择性做 CAC）并 Reassess（Take-Home #2）。

| 10 年 PREVENT-ASCVD 风险 | 推荐（ACC2026 §4.2.3.7） | 等级 |
|---|---|---|
| 低 <3%，30–59 岁，LDL-C <160 mg/dL（4.1）且 30 年风险 <10% | 只做生活方式指导 | 1, A |
| 低 <3%，30–59 岁，但 LDL-C 160–189 mg/dL（4.1–4.9）**或** 30 年风险 ≥10% | **中等强度他汀是合理的**（减少累积暴露） | 2a, C-LD |
| 临界 3%–<5% | 决定用药的话，中等强度他汀，LDL-C 降 30%–49% | 2a, A |
| 临界或中等，已开始他汀 | 目标 LDL-C <100 mg/dL（2.6）、非 HDL-C <130 mg/dL（3.4） | 2a, B-NR |
| 中等 5%–<10% | 至少中等强度他汀（降 30%–49%）；区间高端可用高强度（降 ≥50%） | 1, A |
| 高 ≥10% | 高强度他汀，降 ≥50% | 1, A |
| 高 ≥10%，已开始他汀 | 目标 LDL-C <70 mg/dL（1.8）、非 HDL-C <100 mg/dL（2.6） | 2a, B-R |
| 高 ≥10%，最大耐受他汀仍未达标 | 加依折麦布合理（2a, B-R）；再加 PCSK9 单抗或贝派地酸可能合理（2b, B-NR） | 见左 |
| 未治疗 LDL-C <70 mg/dL 且非 HDL-C <100 mg/dL、无其他危险因素 | 开始降脂药不太可能降低风险 | 3: No Benefit, B-NR |

- 新闻稿与 Take-Home #3 的说法：临界风险“can be considered”，中等风险“should be considered … after a clinician–patient discussion”——**医患共同决定**是硬性环节。
- **风险增强因素**（ACC2026 Table 13）：父母或兄弟姐妹早发 ASCVD（男 <55、女 <65 岁）；高风险祖源（如南亚、菲律宾）；高多基因风险；慢性炎症病（红斑狼疮、类风湿、严重银屑病）；Lp(a) ≥125 nmol/L 或 ≥50 mg/dL；hs-CRP ≥2 mg/L 超过 1 次；TG 持续 ≥175 mg/dL（2.0 mmol/L，非空腹）或 ≥150 mg/dL（1.7，空腹）；CKM 综合征；LDL-C 持续 160–189 mg/dL、非 HDL-C 190–219 mg/dL 或 apoB ≥120 mg/dL；生殖相关风险标志（过早绝经、子痫前期、妊娠糖尿病、妊娠高血压、早产）。临界风险的人考虑增强因素是合理的（2a, B-NR）；临界风险且 hs-CRP 两次 ≥2 mg/L、无其他原因，用高强度他汀有用（2a, B-R）。

### 2.4 三份指南目标值对照（最容易讲错的地方）

| 人群 | 中国 2023 | ESC 2019/2025 | ACC/AHA 2026 |
|---|---|---|---|
| 低危一级预防 | <3.4 mmol/L（131 mg/dL）（IIa, B） | <3.0 mmol/L（116 mg/dL） | 一般不用药；30–59 岁 LDL <160 且 30 年风险 <10% 只做生活方式 |
| 中危 | <2.6（100） | <2.6（100） | 临界/中等：<100 mg/dL（2.6）（2a, B-NR） |
| 高危 | **<2.6（100）** | **<1.8（70）** | 10 年 ≥10%：<70 mg/dL（1.8）（2a, B-R） |
| 有 ASCVD、非最高危 | 「极高危」<1.8（70）且降 >50% | （ESC 把 ASCVD 都归极高危）<1.4（55）且降 ≥50% | 「非极高危」：<70 mg/dL，且可以加药到 <55（2a, B-R） |
| ASCVD 最高危 | 「超高危」<1.4（55）且降 >50% | 2 年内再发可考虑 <1.0（40） | 「极高危」<55 mg/dL、非 HDL-C <85 mg/dL（2.2）（1, A） |

**命名陷阱**：中国的「极高危」（目标 1.8）≠ ESC 的「very high risk」（目标 1.4）；中国「超高危」≈ ESC「very high」≈ ACC「very high risk」。视频里只说「风险越高，目标越低」，不要逐一对应英文名。

---

## 3. 各情景

### a. 年轻、健康、体检 LDL-C 偏高（3.6–4.5 mmol/L，约 139–174 mg/dL）

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | 3.4–<4.1 是「边缘升高」，≥4.1 是「升高」（Table 2）；<4.9 不会直接判高危，按 10 年风险算，年轻人多数是低危 → 目标 <3.4（IIa, B）；中危的年轻人还要看余生风险；不用药的话 3–6 个月复查血脂（§监测） | 见左 |
| ACC2026 | 18–39 岁：饮食、运动、体重优化以减少累积暴露（§4.2.8.2，1, B-NR）。30–59 岁、10 年风险 <3%：LDL <160 mg/dL（4.1）且 30 年风险 <10% → 只做生活方式（1, A）；**LDL 160–189 mg/dL（4.1–4.9）或 30 年风险 ≥10% → 中等强度他汀合理**（2a, C-LD）。18–29 岁没有降脂终点 RCT，“a matter of clinical judgment and patient preference”（§4.2.8.2）。Take-Home #1：LDL-C ≥160 mg/dL 或早发 ASCVD 家族史强的人，在青年期就要“early consideration of pharmacotherapy” | 见左 |
| ESC | SCORE2 从 40 岁起算；低危目标 <3.0 mmol/L | – |

- 要点：①先排除继发原因（甲状腺、肾、肝、药物、饮食——ACC2026 Table 15 列有继发原因，本次没逐项读）；②测一次 Lp(a)；③问家族史（父母兄弟姐妹早发心梗）；④30 岁以上可用 PREVENT 算 30 年风险。
- 证据：这一段证据最弱——没有针对 18–39 岁的事件终点 RCT，依据是孟德尔随机化和累积暴露（ACC2026 §3.1、§4.2.8.2）。属于**有争议/证据外推**：一方主张越早降、累积暴露越少（遗传学证据）；另一方指出没有年轻人硬终点试验、要终生用药。
- 常见误区：「化验单没标箭头就没事」（3.6 在多数化验单参考上限附近）；「年轻扛得住」；「一次超标就要吃药」（指南的首选都是生活方式 + 复查）。

### b. LDL-C ≥4.9 mmol/L（190 mg/dL）或怀疑家族性高胆固醇血症（FH）

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | LDL-C ≥4.9 或 TC ≥7.2 直接列为高危，目标 <2.6；FH 推荐筛查一、二级亲属；FH 诊断可用 DLCN、Simon Broome，“China’s FH screening and diagnosis can be based on the Chinese FH expert consensus criteria”；核心是“early initiation and lifelong adherence to cholesterol-lowering therapy”；纯合子 FH 加血浆脂蛋白分离（LA） | 正文未标等级 |
| ACC2026 §4.2.4.3 | ①先排除继发原因（1, B-NR）；②**最大耐受剂量他汀**（1, B-R）；③没有其他危险因素/HeFH/CAC：加依折麦布、PCSK9 单抗和/或贝派地酸，达到 **LDL <100 mg/dL、非 HDL <130**（1, B-NR）；④有 HeFH、其他危险因素或冠脉钙化：目标 **<70 mg/dL、非 HDL <100**（1, B-R）；⑤已有 ASCVD：**<55 mg/dL、非 HDL <85**（1, B-R）；⑥最大耐受他汀 ± 依折麦布后 LDL 仍 ≥100 mg/dL：英克司兰合理（2a, B-R）。重度高胆固醇定义：LDL-C >190 mg/dL、非 HDL-C >220 mg/dL 和/或 apoB >140 mg/dL | 见左 |
| ACC2026 §4.2.4.1–2 | HeFH 不能用一般人群风险计算器算 10/30 年风险（3: Harm, C-EO）；可能/很可能/确诊 FH 做基因 panel 检测（1, B-NR）；LDL ≥190 无继发原因做基因检测有用（2a, B-NR）；LDL 160–189 可考虑（2b, B-NR） | 见左 |
| ACC2026 儿童 | 9–11 岁普查（1, B-NR）；2 岁起级联筛查（2a, B-NR）；**≥8 岁、LDL-C 持续 ≥160 mg/dL（4.1）且表现符合 FH、生活方式 3–6 个月无效 → 开始他汀**（§4.2.8.1，1, B-R）；纯合子 FH 诊断时即积极治疗，包括婴儿期 | 见左 |
| ESC2019 | DLCN 评分 >8 分「确诊」，6–8 分「很可能」（Table 12）；级联筛查高效；FH 儿童“Statin treatment should be considered at 6–10 years of age”，>10 岁目标 LDL-C <3.5 mmol/L（<135 mg/dL）（§9.1.2.3） | 正文未标等级 |

- 流行病学（ACC2026 §3.1）：HeFH 表型约 1/250–1/300；早发 ASCVD 风险高 2–4 倍；**多达 90% 未被诊断**；早发心梗的人里多达 20% 有 FH 表型。
- 中国 FH 诊断标准：**未查到原文**（记忆中 2018 中国专家共识：成人满足 ≥2 项——未治疗 LDL-C ≥4.7 mmol/L；皮肤/腱黄色瘤或 <45 岁脂性角膜弓；一级亲属 FH 或早发 ASCVD——未证实）。读到的二手综述（raredisease.cn，来源标注不清）列出的是**筛查入选条件**：早发 ASCVD；成人 LDL-C ≥3.8 mmol/L（146.7 mg/dL）；儿童 LDL-C ≥2.9 mmol/L（112.7 mg/dL）且排除继发；<45 岁皮肤/腱黄色瘤或脂性角膜弓；一级亲属有上述情况。可靠度：低（二手、出处标注混乱）。
- 常见误区：「我饮食很健康，是遗传没办法」——正因为是遗传才要更早吃药；「孩子还小不用查」——ACC 建议 9–11 岁普查；忘了查家人（级联筛查）。

### c. 糖尿病；高血压；慢性肾病

**糖尿病**

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 §12.2 | 糖尿病 ≥40 岁直接为高危；LDL-C 和非 HDL-C 都作为目标；中、低危糖尿病 LDL-C 都要 <2.6；高危糖尿病（≥40 岁且病程长、靶器官损害或 ≥3 个危险因素）以他汀为基础，不达标联用胆固醇吸收抑制剂或 PCSK9 抑制剂；LDL 达标但 TG 高或非 HDL 不达标，可考虑高纯度 IPE、ω-3 或贝特 | 正文未标等级 |
| ACC2026 §4.2.5 | 40–75 岁无 ASCVD：中等强度他汀，降 30%–49%，**LDL <100 mg/dL、非 HDL <130**（1, A）；多个危险因素：高强度他汀，**<70 mg/dL**（2a, B-R）；PREVENT ≥10%：可加依折麦布或 PCSK9 单抗到 <70（2b, C-LD）；他汀不良反应：依折麦布/贝派地酸/PCSK9 单抗（1, B-R）；>75 岁且预期寿命 ≥2.5 年：医患讨论后可启动中等强度他汀（2b, C-LD）；**20–39 岁**且病程长（2 型 ≥10 年、1 型 ≥20 年）、白蛋白尿、eGFR <60、视网膜/神经病变或 ABI <0.9：可启动中等强度他汀（2b, C-LD） | 见左 |
| ESC2019 §9.4 | LDL-C 是糖尿病降脂首要目标；高危糖尿病“Non-HDL-C <2.6 mmol/L (<100 mg/dL) and ApoB <80 mg/dL are desirable” | 正文 |

- 中国高危糖尿病的 LDL 目标数值：**未查到**（记忆中 <1.8 mmol/L，未证实）。

**高血压**：CN2023 写“LDL-C target values for hypertensive individuals should be determined according to risk stratification”（不单设目标，按分层）。ACC2026：高血压是 PREVENT 的输入项，也是「极高危」定义里的高风险特征之一（§2.1）。

**慢性肾病**

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 §12.3 | CKD 3–5 期（英文版原文）直接列高危；他汀在轻中度肾功能不全中明显降风险；**两项透析患者他汀研究未显示获益** | 正文 |
| ACC2026 §4.2.8.8 | 40–75 岁 CKD ≥3 期、LDL 70–189 mg/dL：中等强度他汀或中等强度他汀 + 依折麦布（1, B-R）；CKD ≥3 期 + ASCVD：高强度他汀 ± 依折麦布/PCSK9 单抗，降 ≥50%，**<55 mg/dL**（1, B-R）；维持血透者**继续**他汀可能合理，个体化（2b, C-LD）；Take-Home #8：糖尿病、CKD 3–4 期、HIV 患者 40–75 岁“regardless of LDL-C level”推荐降脂 | 见左 |

- 常见误区：「我的 LDL 在正常范围，糖尿病不用管血脂」——三份指南都按「糖尿病本身就是高风险」处理；「透析了才开始吃他汀」——证据恰恰不支持透析时才开始。

### d. 心梗 / 支架 / 缺血性卒中后（二级预防）

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | 极高危 <1.8 且降 >50%；超高危 <1.4 且降 >50%（I, A）；中等强度他汀起始（I, A），不达标加依折麦布，再加 PCSK9 抑制剂；超高危且基线 LDL 高可**直接他汀 + PCSK9 抑制剂**（IIa, A）；依折麦布 + 中高强度他汀可使 LDL-C 降 >50%，三联约降 85%（药物表）。卒中：他汀每降 1 mmol/L LDL-C 卒中复发风险降 12%；脑出血问题“There is disagreement”，但“the benefits of LDL-C reduction far outweighed the harms of potential hemorrhagic stroke” | 见左 |
| ESC2019 + 2025 | 极高危 <1.4 且降 ≥50%；2 年内再发可考虑 <1.0。**2025 新增**：ACS 住院期间就要强化降脂（I, C）；未用过降脂药的 ACS 患者，住院期间就开始高强度他汀 + 依折麦布联合（IIa, B）（据 ESC 官方解读）。卒中：“Statin pre-treatment at TIA onset was associated with reduced recurrent early stroke risk”（2019 §9.6） | 见左 |
| ACC2026 §4.2.6 | **极高危定义**（§2.1 原文）：≥2 次主要 ASCVD 事件（12 个月内 ACS、既往心梗、缺血性卒中史、有症状 PAD），或 1 次主要事件 + ≥2 个高风险特征（≥65 岁、冠脉搭桥或介入、目前吸烟、糖尿病、心衰史、高血压、最大耐受他汀 + 依折麦布后 LDL-C 仍 ≥100 mg/dL）。非极高危：高强度他汀，降 ≥50%，**<70 mg/dL**（1, A），可加依折麦布/PCSK9 单抗/贝派地酸到 <70（2a, B-R）甚至 <55（2a, B-R）；极高危：高强度他汀，**<55 mg/dL、非 HDL <85**（1, A）；加依折麦布和/或 PCSK9 单抗（1, A）；加贝派地酸（2a, B-R）；不能耐受或拿不到 PCSK9 单抗、或希望少打针的，加英克司兰（2a, B-R，尚无心血管结局试验，二线）。Take-Home #9：“the majority of those with a history of ASCVD events will likely qualify for an LDL-C goal of <55 mg/dL” | 见左 |

- 「越低越好」吗：三份指南都只设**上限目标**（达到某值以下），都没有写「低于多少就要减药」的下限；ESC 允许考虑 <1.0 mmol/L。极低 LDL 的长期安全性**本角度未查**（其他研究员负责）。可以说「指南的方向是：已经得过心梗的人，目标越来越低，而且要尽早联合用药」，不要说「越低越好没有任何上限」。
- ACC2026 §1.5 写明新推荐来自 FOURIER、ODYSSEY OUTCOMES、CLEAR OUTCOMES、REDUCE-IT 等大型结局试验。
- 常见误区：「放了支架就通了，不用吃降脂药」；「LDL 正常了就停药」（停药 LDL 会回升——停药后风险升高，ACC2026 §4.2.11 让医生告知“heightened ASCVD risk associated with statin discontinuation”）；「只看 LDL 达标，不看降幅」（中国和 ESC 都要求「双达标」：数值 + 降幅 >50%）。

### e. 75 岁以上老人

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 §12.5 | “There is limited evidence for statins in elderly patients aged ≥75 years”；**有 ASCVD 的 ≥75 岁按与年轻人相同原则治疗**；“no specific recommendation is made for statin treatment targets in elderly patients”；从低剂量开始、逐步调整，监测肝肾功能和 CK；≥80 岁中基线 LDL-C <70 mg/dL 的人未见进一步获益，最佳切点需研究 | 正文 |
| ESC2019 §8.1.3.1 / §9.3.1 | “Statins are effective for the prevention of ASCVD in the elderly, including those aged >75 years”；但 “there is less direct evidence of benefit among patients aged >75 years”；正式推荐在表格图片里，**等级未读到**（记忆中：>75 岁高危以上一级预防可考虑，IIb B，未证实）。2025：≥70 岁用 SCORE2-OP | 见左 |
| ACC2026 §4.2.8.3 | 医患讨论要考虑患者意愿、功能状态、多病共存、衰弱、多重用药、预期寿命，**不能只看年龄**决定停药（1, C-EO）；>75 岁预期寿命 ≥2.5 年：医患讨论后可启动中等强度他汀（2b, B-NR）；决策不确定时可测 CAC，CAC 为 0 或很少（1–10）可不用药（2b, B-NR）；预期寿命 <1 年可停药（2b, B-R）。正在进行的老年一级预防试验：STAREE、PREVENTABLE（参考文献） | 见左 |

- 有争议：老年人一级预防的证据主要来自亚组和观察性研究，大型 RCT 尚未出结果（STAREE、PREVENTABLE 在进行中）——**尚不清楚**。二级预防（已经得过病）各指南一致支持继续。
- 常见误区：「老了就不用管胆固醇」/「老人一律停药」——指南都说个体化，已有 ASCVD 的老人继续按原则治疗。

### f. 只是甘油三酯高（尤其 ≥5.6 mmol/L）

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 Table 10 | **TG >5.6 mmol/L（≥496，约 500 mg/dL）**：可用贝特、高纯度 ω-3 或烟酸降低胰腺炎风险（I, C）；ASCVD/高危、中等剂量他汀后 TG >2.3 mmol/L：高剂量 IPE（IIa, B），ω-3 或非诺贝特（IIb, C）；生活方式和单药不行时可联用 | 见左 |
| ESC2019 §9.1.4.1 | “The risk of pancreatitis is clinically significant if TGs are >10 mmol/L (880 mg/dL)”；用非诺贝特，ω-3（2–4 g/天）辅助 | 正文 |
| ESC2025 | 高危/极高危、他汀后空腹 TG 135–499 mg/dL（1.5–5.6 mmol/L）：IPE 2×2 g/天（IIa, B）；他汀仍是降心血管风险的首选 | 据解读 |
| ACC2026 §4.2.9 | TG ≥150 mg/dL（1.7）：先查继发原因，生活方式为一线（少添加糖、少酒、少饱和脂肪、运动、超重者减重 5%–10%）（1, B-NR）；无 ASCVD/糖尿病的 40–75 岁：用 PREVENT 评估再决定他汀（1, A）；**TG 500–999 mg/dL（5.7–11.3），尤其 ≥1000 mg/dL（11.3）**：贝特或处方 ω-3 合理，降胰腺炎风险（2a, B-NR）；家族性乳糜微粒血症且 TG ≥1000：olezarsen（1, B-R）；TG ≥150 时看非 HDL-C 或 apoB 比 LDL-C 更好（2a, B-NR）；Take-Home #10：“statin therapy remains the foundation” | 见左 |

- 胰腺炎阈值三家不同：中国 5.6、ACC 500/1000 mg/dL（5.7/11.3）、ESC 10 mmol/L——都标「胰腺炎风险」，但「显著升高」的切点不同。ACC2026 §4.1.2：“The risk for acute pancreatitis is substantially increased at TG levels ≥1000 mg/dL”。
- 常见误区：「TG 高只是吃多了，不严重」（≥5.6 要尽快就医）；「TG 高就吃鱼油保健品」（ACC2026 §4.1.5 不建议非处方鱼油；ESC2025：“Dietary supplements or vitamins are not recommended for reducing ASCVD risk”）；非空腹 TG ≥4.5 时要空腹复查再判断。

### g. Lp(a) 高

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | Lp(a) ≥300 mg/L（30 mg/dL）为升高（Table 2）；≥500 mg/L（50 mg/dL）为风险增强因素（Table 1）；高危人群至少查 1 次；高 Lp(a) 作为管理高危患者的指标（IIa, C）；**没有针对 Lp(a) 的药物治疗阈值**；引用英德指南：进展性冠心病且 Lp(a) >150 nmol/L 可考虑血浆分离 | 见左 |
| ESC2019 §5.5 | “Measurement of Lp(a) should be considered at least once in each person’s lifetime, if available”；≥180 mg/dL（≥430 nmol/L）终生风险与 HeFH 相当 | 正文 |
| ESC2025 | 每个成人一生至少测一次（IIa, B）；>50 mg/dL（105 nmol/L）视为风险修正因素（IIa, B） | 据解读 |
| ACC2026 §3.4、§4.2.10 | **所有成人至少测一次**（1, B-NR）；FH、早发 ASCVD 或高 Lp(a) 者的一级亲属做级联检测（1, B-NR）；用对 apo(a) 异构体不敏感、可溯源的检测方法（1, B-NR）；**≥125 nmol/L（50 mg/dL）**为风险增强因素。风险（Table 4，UK Biobank）：中位数 20 nmol/L（7 mg/dL）为参照；125 nmol/L（50 mg/dL，约第 80 百分位）约 1.4 倍；250 nmol/L（100 mg/dL，约第 95 百分位）约 2 倍；430 nmol/L（180 mg/dL，约第 99 百分位）约 4 倍、与 HeFH 相当。处理：早期最佳控制所有可改变的危险因素（1, B-NR）；有 ASCVD、Lp(a) 高、最大耐受他汀不达标：加有心血管获益证据的 PCSK9 单抗（1, B-R） | 见左 |

- 要点：Lp(a) 主要由 LPA 基因决定，一生基本稳定，**生活方式几乎改不了**（“minimally modified by lifestyle factors”）；测一次通常够；肾、肝、甲状腺病、妊娠、绝经和某些药物会使其升高（ACC2026 §3.4）；非洲裔和南亚裔水平最高，但相对风险各族群相似。
- 尚不清楚：专门降 Lp(a) 的药（如 pelacarsen，CN2023 提到其 II 期试验）能否降低事件——本角度未查结局试验结果（其他研究员负责）。
- 常见误区：「Lp(a) 高了吃得更清淡就能降」；「Lp(a) 高但 LDL 正常就没事」（ACC：风险独立于 LDL-C，“even among individuals with low LDL-C”）；单位混用（mg/L、mg/dL、nmol/L）。

### h. 他汀不耐受

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | 定义需同时满足 4 条：有主观和/或客观异常；**不能耐受 ≥2 种他汀，其中一种为最低剂量**；与他汀有因果关系；排除其他原因。CK <4×ULN 无症状：可继续并密切监测；<4×ULN 有症状：停药，症状消失、CK 正常后可换另一种他汀重试；**CK >4×ULN：停药**；CK >10×ULN 警惕横纹肌溶解。不能耐受他汀：考虑胆固醇吸收抑制剂或 PCSK9 抑制剂（Table 7，IIa, C） | 见左 |
| ESC2019 + 2025 | 不能耐受推荐强度的，在最大耐受他汀上加非他汀药（2019 §8.1.2.1）；2025：**不能用他汀的人推荐贝派地酸**（I, B）；他汀 ± 依折麦布不达标加贝派地酸（IIa, C）（据 PACE-CME） | 见左 |
| ACC2026 §4.2.11 | 先查继发原因；严重肌痛或无力时测肌力和 CK（1, C-LD）；医患讨论要承认患者的担忧，**告知停药会升高风险**，并提供替代方案（1, B-R）；有 ASCVD：减量他汀（能耐受的话）+ 贝派地酸/依折麦布/PCSK9 单抗（1, B-R）；无 ASCVD 但高危（PREVENT ≥10%、CAC ≥300、或有糖尿病的 >65 岁女性/>60 岁男性）：加贝派地酸和/或依折麦布到 <70 mg/dL（1, B-R），仍不达标加 PCSK9 单抗（1, B-R）；临界/中等风险：可加依折麦布/贝派地酸到 <100（2b, B-NR）。安全表：正常 CK 的肌痛“common and dose-related”；肌炎/肌病、横纹肌溶解（CK >10×ULN 伴肾损伤）、转氨酶 >3×ULN 均为“rare” | 见左 |

- 常见误区：「吃一种他汀不舒服 = 他汀不耐受」（中国定义要求 ≥2 种）；「不耐受就什么都不吃了」。肌肉症状机制和反安慰剂效应由其他研究员负责。

### i. 孕期 / 备孕；儿童青少年筛查

**孕期 / 备孕 / 哺乳**

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 §12.6 | 他汀一般不推荐；ASCVD 高危的孕妇（如 FH、既往急性冠脉事件）可多学科会诊后谨慎考虑他汀；合并 ACS 的孕妇可考虑胆酸螯合剂；FH 合并 ASCVD 可考虑 LA | 正文 |
| ESC2019 §9.2.3 / §9.4.4 | “statins are not indicated in pregnancy”；“Lipid-lowering drugs should not be given when pregnancy is planned, during pregnancy”；计划怀孕的糖尿病女性应避免他汀 | 正文 |
| ACC2026 §4.2.8.4 | 非高危、计划怀孕：**试孕前 1–2 个月或一发现怀孕就停他汀**（1, C-LD）；孕期/哺乳期 HoFH：血浆分离（2a, B-NR）；孕期空腹 TG ≥500 mg/dL（5.7）：贝特（孕早期后）或高剂量 ω-3 乙酯（2a, B-NR）；孕期/哺乳期单纯高胆固醇：胆酸螯合剂（2a, C-EO）；**有 FH 或 ASCVD 史的孕妇，个体化讨论后继续他汀可能合理**（2b, C-LD），优先亲水性他汀如普伐他汀。安全表原话：“pregnancy is not a contraindication, but statins should be avoided while lactating” | 见左 |

- **指南分歧**：ESC2019 写「孕期不适用」；ACC2026 写「妊娠不是禁忌证、哺乳期应避免」，并允许 FH/ASCVD 孕妇个体化继续；中国介于两者之间（一般不推荐，高危多学科会诊）。三家一致的是：**普通人备孕就停药，高危者找医生个体化**。

**儿童青少年**

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 §12.7 | 血脂检测应纳入中小学体检常规项目；以下儿童要筛查：父母 TC ≥6.2 mmol/L 或有血脂异常史、有黄色瘤或角膜弓、糖尿病、高血压、肥胖（2–8 岁）、超重（12–16 岁）、吸烟，疑似 FH 做基因筛查；每天不少于 1 小时中高强度运动；饮食干预不影响生长发育；药物治疗参照专门共识。儿童参考值在补充表 S6（**未读到**） | 正文未标等级 |
| ACC2026 §3.1、§4.2.8.1 | 9–11 岁普查（1, B-NR）——理由：颈动脉内中膜厚度最早 8–10 岁可见；青春期中后期 TC、LDL-C 会暂时降 10%–20%，晚查不准；可用非空腹 TC 和 HDL-C 算非 HDL-C；儿童不常规查 apoB。**儿童参考值（Table 18，mg/dL）**：TC 合格 <170、临界 170–199、异常 ≥200；LDL-C 合格 <110、临界 110–129（异常一栏 PDF 抽取被截断，记忆中 ≥130，未证实）；TG 0–9 岁 <75 / 75–99 / ≥100，10–19 岁 <90 / 90–129 / ≥130；HDL-C >45 / 40–45 / <40。有血脂异常的儿童首选生活方式（1, B-R） | 见左 |

- 儿童换算：TC 170/200 mg/dL ≈ 4.4/5.2 mmol/L；LDL-C 110/130 ≈ 2.8/3.4 mmol/L。
- 常见误区：用成人参考值看孩子化验单；「只有胖孩子才会胆固醇高」（ACC：多达一半 LDL 高的孩子家族史阴性，“Family history alone is not sufficient”）。

### j. 冠脉钙化积分（CAC）——尤其 CAC = 0

| 指南 | 怎么说 | 等级 |
|---|---|---|
| CN2023 | CAC ≥100 AU 是风险增强因素（Table 1） | – |
| ESC2019 / 2025 | 2019：中危人群里 CAC >100 AU 可重新分层，“CAC had the best reclassification ability”；2025：影像发现亚临床动脉粥样硬化或 CAC 升高作为风险修正因素，用于中危或接近治疗阈值的人（IIa, B，据解读） | 见左 |
| ACC2026 §4.2.3.6、§4.2.7 | 适用：**男 ≥40 岁、女 ≥45 岁**。中等风险或部分临界风险、用药决定不确定时，应该用 CAC 帮助决定不用、推迟或开始（1, B-R）。**CAC = 0**，且本人倾向不用药、**没有更高风险情况**（FH 或 LDL >190 mg/dL、糖尿病且 >40 岁、目前吸烟、早发 ASCVD 家族史强），**推迟治疗、3–7 年后复查 CAC 是合理的**（2a, B-NR）；CAC >0 推荐开始降脂，尤其 ≥100 AU 或 ≥第 75 百分位（1, B-NR）。CAC 分级目标：1–99 且 <第 75 百分位 → 中等强度他汀、<100 mg/dL（2a, B-R）；100–299 或 ≥第 75 百分位 → <70（1, B-R）；300–999 → <70（1, B-R），可强化到 <55（2a, B-NR）；**≥1000 → <55、非 HDL <85**（1, B-NR）。非心脏 CT 偶然发现钙化也要纳入决策（1, B-NR）。>75 岁：CAC 为 0 或 1–10 可不用药（2b, B-NR）。可能有大量非钙化斑块的人（炎症病、HIV、糖尿病）可选择性做冠脉 CTA（2b, B-NR） | 见左 |

- 要点：CAC = 0 是「可以推迟」的依据，**不是「血管完全干净」的证明**——CAC 只看钙化斑块，看不到早期的软斑块（ACC 对糖尿病、炎症病、HIV 才建议 CTA 就是这个原因）；吸烟、糖尿病、FH、家族史强的人 CAC = 0 也不能推迟。CT 有辐射，中国基层可及性**未查**。
- 常见误区：「CAC 0 = 一辈子不用管」（ACC 要求 3–7 年复查）；「年轻人去做 CAC」（指南限 40/45 岁以上）。

### k. 女性绝经后；生酮饮食后 LDL 大幅升高

**绝经后女性**
- ACC2026 Table 13：**过早绝经（<40 岁）、早绝经（<45 岁）**列为风险增强因素；§3.4：绝经过渡期 Lp(a) 会变化（“remain stable except for some conditions, such as the menopause transition”）。
- ESC2019 Box 5：女性 >50 岁或绝经后应考虑查血脂。
- CN2023：≥40 岁每年查一次（不分性别）。
- 激素替代治疗对血脂/心血管的作用：**本角度未查**。

**生酮饮食后 LDL-C 大幅升高**
- ACC2026 §4.1.2（饮食）：生酮饮食短期内体重和 TG 下降明显，“LDL-C can be increased substantially in some individuals, particularly when there is high consumption of animal products”，且难以长期坚持。
- ACC2026 §4.2.4.3（重度高胆固醇）：碳水降到约 20–50 g/天的生酮饮食，碳水多被脂肪（常是饱和脂肪）替代，“some individuals, with or without lipid disorders, may manifest a severe hypercholesterolemia phenotype”；所有重度高胆固醇患者都要仔细问饮食史；因生酮导致的，要在保住减重目标的同时“counseled on ways to mitigate the LDL-C elevation”。
- 「瘦体重高反应者（lean mass hyper-responder）」等概念：指南未提，**本角度未查**。
- 可靠度：高（指南原文）。属于**有争议**的公众话题：生酮支持者认为 TG 降、HDL 升、体重降可抵消 LDL 升高；指南立场是 LDL-C/apoB 本身是致病因素，升高需要处理。
- 常见误区：「生酮让 HDL 升了，LDL 高无所谓」；「LDL 是饮食造成的，所以不是真的高」（ACC 把它当继发性重度高胆固醇处理）。

---

## 4. 开始用药后多久复查

| 指南 | 血脂 | 肝酶 | CK | 原文/等级 |
|---|---|---|---|---|
| CN2023 | 不用药：3–6 个月复查；**首次用药 4–6 周内复查**血脂、肝酶、CK；达标后逐步改为每 3–6 个月复查（英文版原话：“gradually change to re-examination every 3–6 months”；记忆中中文原文后续为 6–12 个月，未证实） | ALT/AST ≥3×ULN 且总胆红素升高 → 减量或停药 | 见 §h 的 4×ULN / 10×ULN 处理 | “review their lipids, liver enzymes and creatine kinase (CK) within 4–6 weeks of taking the drug”；未标等级 |
| ESC2019 §8.1.4 | Table 13（图片）未读（记忆中：开始后 8±4 周查血脂，未证实） | “routine monitoring of ALT during statin treatment is no longer recommended” | 横纹肌溶解时 CK 常 ≥10 倍、甚至 ≥40 倍 ULN | 正文 |
| ACC2026 §3.5 | **开始或调整剂量后 4–12 周查血脂，此后每 6–12 个月**（1, A）；稳定、无变化者每 12 个月一次；非空腹一般够，已知高 TG 要空腹；评估看较基线降幅 + 绝对目标 | 他汀 + 依折麦布联用前后监测转氨酶（药物安全表）；他汀单用转氨酶 >3×ULN「罕见」 | 严重肌痛或无力时测 CK（§4.2.11，1, C-LD） | 见左 |

- 指南分歧：中国要求首次用药就查肝酶和 CK；ESC 明确不再推荐常规监测 ALT；ACC 只在联用依折麦布或有症状时查。视频里可以说「开始吃药后 1–3 个月复查血脂，肝功能和肌酶按医生要求查」，不要说「每个月都要抽血查肝」。
- 复查的意义（ACC2026 §3.5）：个体对他汀反应差异大，复查血脂“associated with improved medication adherence”，并减少“therapeutic inertia”。

---

## 5. 已证实 / 有争议 / 尚不清楚

| 分类 | 内容 |
|---|---|
| 已证实（三份指南一致） | LDL-C 是首要靶点；风险越高目标越低；已有 ASCVD 用高强度他汀、不达标加依折麦布/PCSK9；FH 要早治疗并筛查家人；TG 极高有胰腺炎风险；Lp(a) 由遗传决定；非空腹血一般可用；孕前停用他汀（非高危） |
| 指南间分歧 | 高危一级预防目标（中国 2.6 / ESC 1.8 / ACC 1.8）；低危目标（中国 3.4 / ESC 3.0）；胰腺炎切点（5.6 / 10 / 11.3 mmol/L）；Lp(a) 阈值与单位（中国 300 mg/L 升高、500 mg/L 增强因素；ESC 50 mg/dL≈105 nmol/L；ACC 50 mg/dL≈125 nmol/L）；成人开始筛查年龄（中国未定起始年龄、<40 每 2–5 年；ACC 19 岁起每 5 年；ESC 男 >40、女 >50）；孕期他汀（ESC「不适用」vs ACC「不是禁忌证」）；常规查 ALT（中国查、ESC 不查） |
| 有争议 / 证据外推 | 18–39 岁无其他危险因素者是否吃药（无硬终点 RCT）；>75 岁一级预防；生酮饮食导致的 LDL 升高要不要处理 |
| 尚不清楚 | 老年一级预防 RCT（STAREE、PREVENTABLE 进行中）；专门降 Lp(a) 药物的事件获益；英克司兰的心血管结局（ACC2026：“Cardiovascular outcomes trials are pending for inclisiran”） |

---

## 给视频的建议

**最值得讲的 5 个点**
1. **「化验单正常」不等于「你达标」**：同一个 LDL-C 3.0 mmol/L，对健康年轻人是合适，对心梗后的人是明显超标。一张化验单配三个人（健康年轻人、糖尿病人、放过支架的人），箭头一样、目标不同——这正是中国指南改名「血脂管理」的原因。
2. **风险分层是一把梯子**：低危 <3.4 → 中/高危 <2.6 → 极高危 <1.8 → 超高危 <1.4（中国）。画成动脉内一层层降低的「水位线」，标「示意」。
3. **LDL ≥4.9 / 家族史 → 想到 FH，查全家**：ACC 引用「多达 90% 未诊断」。凯可以问「那我孩子要不要查？」，林答「美国新指南建议 9–11 岁查一次，有家族史 2 岁就可以查」，同时说明中国指南建议纳入中小学体检。
4. **Lp(a) 一生测一次**：遗传决定，饮食改不了，测一次够。最适合「缩小进血管」画面：LDL 颗粒上多挂一条 apo(a) 链。
5. **CAC = 0 可以「推迟」，不等于「干净」**：限 40/45 岁以上、风险不确定的人，有糖尿病/吸烟/FH 的不适用，3–7 年复查。

**最容易讲错的地方**
- 把中国「极高危」和欧美「very high risk」当成一回事（目标差 0.4 mmol/L）。
- 说「美国指南没有目标值」——那是 2018 版；**2026 版已重新设目标**（<100 / <70 / <55 mg/dL）。
- 说「ACC/AHA 2018 胆固醇指南」是最新的——已被 2026 版取代；风险计算器已从 PCE 换成 PREVENT（30–79 岁，算 10 年和 30 年）。
- Lp(a) 单位混写：中国 mg/L、ESC/ACC mg/dL 或 nmol/L；mg/dL 和 nmol/L 不能简单互换。
- TG 胰腺炎阈值只讲一个数——中国 5.6、ACC 11.3（1000 mg/dL）为「尤其」、ESC 10 mmol/L。
- 孕期：不要说「孕期绝对禁用他汀」（ACC2026 已改口），也不要说「孕期可以吃」；统一说法：「普通人备孕前停药，有家族性高胆固醇或心脏病史的孕妇由医生个体化决定」。
- 复查：不要说「每月查肝功能」；ESC 已不推荐常规查 ALT。
- 所有涉及「该不该吃药」的台词都要带「和医生讨论」——ACC 的每条一级预防推荐都以「医患讨论」为前提。

**可以怎么画**
- 化验单特写：真实的血脂报告格式（TC、TG、HDL-C、LDL-C，单位 mmol/L，参考范围一栏），可画真实结构，但数值和医院名要虚构、标「示意」。
- 风险梯子 / 水位线：纯示意图，标「示意」。
- CAC：真实的 CT 冠脉钙化是骨白色亮斑，沿冠状动脉分布；CAC=0 画干净的 CT 截面，同时画一个看不见的软斑块（CT 看不到，用虚线标「示意」）。
- FH 家谱：三代家谱图，箭头表示级联筛查（示意）。
- 黄色瘤：真实存在于肘、膝伸侧、跟腱、手部（二手综述来源），视频里画要克制、不吓人，或只用文字。
- Lp(a)：LDL 颗粒（直径约 20–25 nm，此数字本次未查，需结构研究员核对）+ apo(a) 链——形态按结构研究员的资料画。

**观众最可能的误解**
- 「我体检单上没箭头，所以我没事。」
- 「只要吃得健康就不会胆固醇高。」（FH、Lp(a) 是遗传的）
- 「降到正常就可以停药。」
- 「年纪大了不用管 / 年轻不用管。」
- 「CAC 为 0 就永远不用担心。」
- 「生酮让我瘦了，LDL 高是好胆固醇变多了。」
- 「欧美的标准不适合中国人。」——可以说「数字有细微差别，但方向完全一致；在中国就按中国指南和你的医生」。

**免责声明位置**：每期结尾固定一句「本视频依据中国血脂管理指南（2023）等公开指南，不替代医生诊断；是否用药请与医生讨论」。
