---
worker_id: factcheck-r1
stage: 3
role: validator
level: factcheck
status: partial
blockers:
  - "F30 肝功能异常是「每年」约多 0.13%，不是笼统「约多 0.1%」；需改后才能进讲稿"
  - "F31 横纹肌溶解 0.44/万人年出处是 Graham 2004 真实世界队列，不是 CTT；且漏了出血性卒中 5–10/万人·5 年"
  - "F34 SITE 是开放标签、非劣效界值 5 个百分点、只看全因死亡，不能讲成「停药证明安全」；STAREE 的肝胆与糖尿病不良事件也要并列"
  - "F42 Cochrane RR 0.83 是「减少饱和脂肪」的总体结果，不是「换成植物油」专属"
  - "F46 饮酒 RR 0.93（P=0.07）是全因死亡，不是「护心」"
confidence: medium
---

# 事实核查 r1：探索第二季「血脂」档案 §2（F01–F58）

- 核查日期：2026-11-14。核查人与档案作者无共享上下文。
- 方法：只依据本次实际读到的文本。一手来源主要靠 Europe PMC REST 接口读摘要 / 开放全文（PMC），FDA 说明书 PDF 与 ACC/AHA 2026 指南 PDF 本地抽文本后检索原句，网信办通知读原页。WebSearch 共 7 次，只用来找线索或补读不到的一手来源；凡只读到新闻稿或检索摘要的，判定里写明。
- 本轮没覆盖的条目判「未能核」，意思是**这次没读到原文**，不等于有错。
- 角度文件只拿来找 URL，判断都是独立做的。

## 1. 逐条判定

| # | 判定 | 依据（来源、URL、原文短引） | 建议的改法（片中怎么说才准） |
|---|---|---|---|
| F01 | 未能核 | 本轮没有读 Feingold Endotext 表 1。 | 数值来源单一，进片前要读原表。片中只需讲相对大小（HDL 最小、LDL 约 20 多纳米、乳糜微粒最大），不用列全部区间。 |
| F02 | 需改 | Berndsen 等 *Nature* 2025;638:836（PMID 39662503）摘要：apoB100 是 "an approximately 61-nm-long continuous amphipathic β-sheet that wraps around the LDL particle like a belt"。预印本（bioRxiv PPR813166）写的是 "∼58 nm long x 4 nm wide"。正式版摘要里没有宽度。17×20 nm 与均值 19.3 nm 本轮没有读到。 | 改用正式版数字：「ApoB 像一条约 60 纳米长的腰带绕颗粒一圈」。宽度 4 nm 只出现在预印本，要么注明出自预印本，要么不说。颗粒尺寸要读正式版正文后再用。 |
| F03 | 属实 | Borén 2020 EAS 共识（PMC7308544）："apoB100 (one molecule per LDL particle)"。 | 片中可以说「每个颗粒正好一个 ApoB，所以数 ApoB 就是在数颗粒」。VLDL / IDL / Lp(a) 也各一个，这部分本轮没逐字读到，属教科书共识，建议审稿医生确认。 |
| F04 | 属实 | Borén 2020："2000–2700 molecules per particle, of which ∼1700 are in esterified form"。 | 可直接用：「一个 LDL 里装着两千多个胆固醇分子」。 |
| F05 | 属实（只核了算术） | 复算：1100–1600 nmol/L × 6.02×10²³ ÷ 10⁶ µL/L ≈ 6.6×10¹¹–9.6×10¹¹ 个/µL。输入值（Morris 2014 的 LDL-P 范围）本轮未核。 | 说「一微升血里大约有几千亿个 LDL 颗粒」，标「估算」，比精确区间更稳。 |
| F06 | 属实 | Borén 2020："Apolipoprotein B-containing lipoproteins of up to ∼70 nm in diameter" 能穿过内皮。原文列了乳糜微粒残粒，但没有明说「大乳糜微粒进不去」。 | 「直径小于约 70 纳米的颗粒才进得去」可以说。「乳糜微粒太大进不去」是按尺寸推出来的，片中可以讲成推论，不要说成文献原话。 |
| F07 | 属实 | Borén 2020："LDL transcytosis occurs through a vesicular pathway, involving caveolae"，并质疑「通过受损、高通透内皮被动滤过」的旧说法；滞留靠 apoB100 上带正电的精氨酸、赖氨酸与蛋白聚糖结合；"95% of ruptured plaques have cap thickness <65 μm"。 | 帽厚改成「破裂的斑块里，95% 的纤维帽薄于 65 微米」，不要说成「易损斑块的定义就是 <65 µm」。原文没有出现「完整内皮」这个词，可以说「不需要血管先破」。 |
| F08 | 属实（只有二手来源） | Berenson 1998 NEJM 摘要（Europe PMC）：尸检 204 名 2–39 岁年轻人，"The extent of fatty streaks and fibrous plaques … increased with age"。50% / 85% 只在 AAFP 1998 摘要中出现（经检索摘要读到，原页 403）；同一摘要给出隆起斑块 8% / 69%，其中年长组写的是 26–39 岁。PDAY 本轮未核。 | 「在一项美国小镇的尸检研究里，2–15 岁的孩子约一半冠脉已有脂纹，20 多到 30 多岁约八成五」。要加三条限定：①样本 204 人，多数死于意外；②脂纹不等于会堵的斑块；③这是美国人群。 |
| F09 | 未能核 | 本轮没有读 Mizuno 2017。 | 画面可以先用「血管镜下斑块偏黄」，进片前补读原文。 |
| F10 | 属实（只核了算术）；LAD 内径未能核 | 7–8 µm ÷ 20–25 nm ≈ 280–400 倍。档案 §3 的标尺也复算过：放大 4.5×10⁵ 倍时，红细胞约 3.4 m，帽厚约 29 m，LAD 3.7 mm 约 1.7 km，血流 20 cm/s 相当于每秒约 900 万个颗粒直径，全部吻合。Dodge 1992 没有读到。 | 可以用。LAD 内径因人而异，说「约 3–4 毫米」。 |
| F11 | 属实 | Ference 2017 EAS 共识（PMID 28444290）摘要："unequivocally establishes that LDL causes ASCVD"。 | 可以说「多条独立证据一致证明 LDL 是病因」。 |
| F12 | 属实 | Cohen 2006 NEJM 摘要：黑人携带无义突变者 "28 percent reduction in mean LDL cholesterol"，"88 percent reduction in the risk of CHD"；白人中某变异 "15 percent reduction in LDL"，"47 percent reduction in the risk of CHD"。 | 要分清两个人群和两种变异，不要合成一句「LDL 低 15–28%，风险低 47–88%」。可以说「天生 LDL 低一些的人，一辈子冠心病风险低一半以上」。 |
| F13 | 属实（部分） | Ference 2017："this effect appears to increase with increasing duration of exposure to LDL-C"。Domanski 2020 未读。 | 「累积暴露」可以说。「量 × 时间」要讲成比喻，不要当公式。 |
| F14 | 属实 | FOURIER 极低 LDL 分析（Giugliano 2017 Lancet，PMID 28859947）："over a median of 2·2 years"；"no safety concerns with very low LDL-cholesterol concentrations"；10% 的人 LDL <0.5 mmol/L。 | 照写，并保留「随访只有两年多」这一限定。 |
| F15 | 属实（部分） | Voight 2012（PMID 22607825）：LIPG 396Ser 升 HDL，但 "not associated with risk of myocardial infarction (OR 0.99, 95% CI 0.88-1.11"。Madsen 2017：男性 HDL 2.5–2.99 mmol/L HR 1.36（1.09–1.70），≥3.0 HR 2.06；女性 3.0–3.49 HR 1.10（不显著），≥3.5 HR 1.68。CETP 抑制剂、烟酸的试验本轮没读原文。 | 「HDL 极高反而死亡率更高」是观察性关联，不能说成「HDL 高有害」。可以说：「HDL 不是越高越好；靠药把它升上去，也没减少心脏病」。 |
| F16 | 未能核 | 本轮没有读 Sniderman 2019。 | 片中只说「有些情况下（如甘油三酯高、糖尿病）医生会加查 ApoB」，不展开。 |
| F17 | 属实（去掉「待核」） | Lp(a)HORIZON NEJM 摘要（Cho 等，PMID 43001734，2026-11-07 在线）：8,350 名已有心血管病、Lp(a) ≥70 mg/dL 的患者；12 个月 Lp(a) 中位数 64.4 vs 233.4 nmol/L；中位随访 4.7 年；MACE 12.3% vs 12.1%，"HR 1.02, 95% CI 0.90 to 1.15"。TCTMD 2026-11-07 报道相对安慰剂降 77.7%（摘要本身没写百分比，按中位数算约 72%）；Novartis "has decided to discontinue the pelacarsen … ASCVD development program"。Nissen 说 "A single trial does not provide definitive evidence of a lack of benefit of lowering lipoprotein(a)"。 | 「第一个大型降 Lp(a) 药物试验里，这种药把 Lp(a) 降了约四分之三，但五年里心脏事件没有减少。」必须加两条限定：①受试者都已得过心血管病，LDL 本来就已控制得很低；②失败的是这一种药、这一个试验，Lp(a) 是不是病因、其他药会不会有效，仍是未解问题。 |
| F18 | 属实（去掉「待核」） | Europe PMC：PMID 40192608（JACC Adv 2025;4(7):101686，"Longitudinal Data From the KETO-CTA Study: Plaque Predicts Plaque, ApoB Does Not"），pubType 为 "Retracted Publication"；关注声明 PMID 41906601（2026-01-23 在线）；撤稿声明 PMID 42206798（JACC Adv 2026;5(5):102824）："retracted at the request of the authors and the Editors … the identified errors are too great to be corrected with a corrigendum"。 | 「这篇论文 2026 年被作者和期刊编辑一起撤回，原因是错误太大、无法更正。」撤稿的是 2025 年的纵向论文，不要牵连 2024 年的 KETO 横断面研究（Budoff 2024，未撤稿）。不要推测作者动机。 |
| F19 | 属实 | Twin Res Hum Genet 2007（PMID 17903110）：男性老年双生子 LDL-C 遗传度 "from 0.49 to 0.64"；Diabetologia 2007（PMID 17694296）东佛兰德双生子研究中 LDL-C 为 78%。 | 说「双胞胎研究估计，LDL 高低大约一半到四分之三由遗传解释」。要补一句：遗传度是人群统计量，不等于「你的 LDL 有 X% 是天生的」，更不等于「改生活方式没用」。 |
| F20 | 属实（患病率部分） | ACC/AHA 2026 指南正文："The HeFH phenotype affects 1 in 250 to 300"。「多数未诊断」「未治疗者多早发冠心病」本轮没有逐字核。 | 用「约每 250–300 人里有 1 个」。 |
| F21 | 属实 | Khera 2016 JACC 摘要："1,386 (6.7%) had LDL cholesterol ≥190 mg/dl; of these, only 24 (1.7%) carried an FH mutation"；没有突变者 CAD "odds ratio: 6.0"，有突变者 "22.3"。 | 一定要带上后半句：「没查到基因突变，LDL 这么高照样让冠心病风险高好几倍」。否则观众会理解成「不是 FH 就不要紧」。 |
| F22 | 未能核 | 本轮没有读 Goldstein & Brown 2009。 | 这是教科书机制，片中可以用，建议审稿医生过目。 |
| F23 | 属实（孕期、年轻成人）；绝经未能核 | Endotext（Wild & Feingold）："total cholesterol levels increase by approximately 50%, LDL-C by 30-40%"。ACC 2026 §4.2.8.2 原文："average rate of increase=1-2 mg/dL per year for LDL-C … although this normative increase should not be perceived as optimal"。 | 可以用。「孕期 LDL 升高是正常生理变化」要说清，避免孕妇自行处理。 |
| F24 | 未能核 | 本轮没有读 ACC 2018 继发原因表。ACC 2026 正文提到要先排查继发原因，但本轮没有逐项读。 | 片中只说「医生会先排查甲状腺、肾、肝、用药等原因」。 |
| F25 | 未能核（「blue-green mold」这一描述） | 机制是教科书内容，本轮没有读一手来源。Endo 2010 的摘要里没有出现霉菌描述。 | 只说「远藤章从一种青霉菌里找到」，不说颜色。注意不要和 F39 小林制药事件里污染的「青霉」放在同一画面里混淆。 |
| F26 | 属实 | CTT 2010 Lancet（PMC2988224）：每降 1.0 mmol/L，主要血管事件 RR 0.78（0.76–0.80）；全因死亡 RR 0.90；癌症 RR 1.00。 | 照写。按 §5 规则配绝对数。 |
| F27 | 属实 | Collins 2016 Lancet 摘要：LDL 降 2 mmol/L、5 年、每 1 万人，二级预防 "prevent major vascular events from occurring in about 1000 patients"，一级预防（风险升高者）"in 500 patients (ie, 5% absolute benefit)"；害处："about 5 cases of myopathy"，"50-100 new cases of diabetes"，"5-10 haemorrhagic strokes"。 | 「100 个已经得过心脏病的人，吃 5 年、LDL 降够 2 个单位，大约 10 个人免于一次心梗或中风；没得过病但风险较高的人约 5 个」。获益和害处（肌病约 0.05 人、糖尿病 0.5–1 人、出血性卒中 0.05–0.1 人）用同一张图。要说明这是模型估算，而且降 2 mmol/L 对多数一级预防的人已经是降得很多。 |
| F28 | 未能核 | 本轮没有读 ESC 2019 与 STELLAR。另读到 CN2023："Moderate-intensity statins are the preferred strategy for lipid-lowering therapy in the Chinese population"。 | 中文版要提中国指南首选中等强度（见整体意见）。「剂量翻倍多降约 6%」要核原文后再用。 |
| F29 | 属实 | CTT 2022 Lancet 摘要："Most (>90%) of all reports of muscle symptoms by participants allocated statin therapy were not due to the statin"；第一年绝对超额 "11 (6-16) events per 1000 person-years"。SAMSON（JACC 2021）："nocebo ratio was 0.90"。StatinWISE 本轮未核。 | 两句一起说：「吃他汀后觉得肌肉痛，九成以上不是药引起的；但第一年里大约每 100 人有 1 人真的是药引起的」。不要否定观众的症状，结尾要落到「告诉医生，可以换药或调量」。 |
| F30 | 需改 | CTT 2026 Lancet（PMID 41655587；PMC7619005）摘要："four of 66 further undesirable outcomes that had been attributed to statins were FDR significant"；转氨酶异常 "0·30% per annum … vs … 0·22% per annum"（RR 1.41）；"absolute annual excess of 0·13% for combined liver function test abnormality"；正文："no evidence that statins increased the risk of clinical hepatobiliary outcomes"，包括肝衰竭、肝炎。另有：①STAREE（TCTMD 报道）肝胆不良事件 3.3% vs 0.9%；②FDA 瑞舒伐他汀说明书 5.3 节："Rare reports of fatal and non-fatal hepatic failure have occurred"。 | 「双盲试验汇总：说明书上列的 66 种副作用，只有 4 种确实比安慰剂多。肝功能化验异常每年大约每 1000 人多 1 个，但肝炎、肝衰竭没有增加。」不要说「他汀不伤肝」，要说「严重肝损伤极少见，医生会按需查肝功能」。原文已读到，可以去掉「待核」。 |
| F31 | 需改 | 糖尿病：CTT 2024 Lancet Diabetes Endocrinol 摘要，高强度 RR "1·36, 1·25-1·48"，低 / 中强度 RR 1.10；"approximately 62% of new-onset diabetes cases were among participants who were already in the top quarter" 的基线血糖。50–100 例 / 万人·5 年出自 Collins 2016（阿托伐他汀 40 mg）。横纹肌溶解：0.44 / 万人年出自 Graham 2004 JAMA（美国住院病例队列，阿托 / 普伐 / 辛伐单药；合用贝特类时 5.98），不出自 CTT 或 Collins。CTT 2026 引言给的是 "approximately 2–3 cases per 100 000 person-years"（约 0.2–0.3 / 万人年）。档案漏了出血性卒中 5–10 / 万人·5 年（Collins 2016，"probably" caused）。 | 横纹肌溶解改为「极少见，每 10 万人每年约 2–3 例（随机试验汇总）；合用某些药时风险会升高」，出处写 CTT。补上出血性卒中。糖尿病写成「多发生在血糖本来就接近糖尿病线的人身上」。 |
| F32 | 属实 | FDA CRESTOR 说明书（2026，s047）8.8 节："approximate 2-fold increase in median exposure to rosuvastatin in Asian subjects when compared with White controls"；2.4 节："Initiate CRESTOR at 5 mg"。HPS2-THRIVE 2013 EHJ 摘要：任何肌病中国 "0.66%/year vs. 0.13%/year"，欧洲 "0.07%/year vs. 0.04%/year"；对照臂（辛伐他汀 40 mg ± 依折麦布）中国约为欧洲 3 倍。 | 可以说「同样剂量，亚洲人血药浓度约为白人 2 倍；一项大试验里中国人肌病比欧洲人多约 3 倍，但绝对数仍低，每年约千分之一」。不给具体药名加剂量（合规），只说「医生给亚洲人起始剂量通常更低」。 |
| F33 | 属实（需加限定） | Diabetes Metab J 2014（PMID 24627830）：99 名已达标的 2 型糖尿病患者（瑞舒伐他汀），按 2:1 随机，10 周时复发率 79% vs 3%。SITE（Healio 2026-08-24 报道）：停药组 LDL "increased from 114.6 mg/dL to 170.6 mg/dL"。「没有反跳超过基线」本轮没能核，只能说没看到证据。 | 「停药后 LDL 会回升，基本回到吃药前的水平；他汀不会让人上瘾。」「不会反跳」改成「目前没有证据显示会升得比原来更高」。小试验要注明对象（糖尿病患者，只看了 10 周）。 |
| F34 | 需改 | STAREE：NEJM 摘要本轮没读到（Europe PMC 无摘要）；ESC 新闻稿、ACC 与 TCTMD 一致报道 ≥70 岁无心血管病者 9,971 人，中位随访 5.9 年，MACE 6.0% vs 8.3%，HR 0.70（0.61–0.82），无失能生存 HR 0.94（0.84–1.05，不显著）；剂量为 20 mg 起，耐受者 1 个月后加到 40 mg（TCTMD）；肌骨事件 32.0% vs 29.4%，肝胆 3.3% vs 0.9%，糖尿病相关 4.0% vs 2.7%。SITE：Lancet Healthy Longev 2026（PMID 42580354）摘要：≥75 岁一级预防，1,180 人，**开放标签**，非劣效界值为 **5 个百分点**的绝对差，3 年全因死亡 7.9% vs 7.2%，"non-inferior to continuation for 3-year all-cause mortality"；Healio 报道中位年龄 80 岁，排除 FH 与痴呆。「观察性研究停药事件约 +30%」本轮没找到原文（Giral 2019 检索未命中），未能核。 | STAREE 用绝对数：「70 岁以上、没得过心脏病的人，吃 6 年左右，100 人里大约少 2 个人出心脏事件，但不能让人更长时间地健康、不失能地活着」，并列不良事件。SITE 要说「一项开放标签小试验：80 岁左右、低风险的老人停药 3 年，死亡人数没有明显增加；但试验没设计来看心梗、中风」。不要说「停药被证明安全」。观察性 +30% 找到原文前不要用数字。 |
| F35 | 需改（小） | FDA 新闻稿落款 "For Immediate Release: July 17, 2026"：Lipfendra（enlicitide），"first oral inhibitor of … PCSK9"，第 24 周 LDL-C 较安慰剂平均降 56%；新闻稿没有心血管结局数据。2026-07-16 是 Merck 公告日期（Pharmacy Times 报道，经检索摘要读到）。英克司兰：ACC 2026 原文 "Cardiovascular outcomes trials are pending for inclisiran"；ORION-4 在 ClinicalTrials.gov 上的主要完成日期预计为 2026-10，检索未发现已公布结果。IMPROVE-IT、ODYSSEY、CLEAR Outcomes 本轮未核。 | 日期写「2026 年 7 月获 FDA 批准」。说法：「第一种口服 PCSK9 抑制剂在美国获批，目前只证明能降 LDL，能不能减少心梗还要等结局试验」。中国是否获批本轮没查，不要暗示国内可用。 |
| F36 | 未能核 | 本轮没有读 ASTEROID、SATURN、GLAGOV、HUYGENS、PACMAN-AMI。 | 用「斑块能缩小一点、变稳定，但回不到原样」这种定性说法，具体百分点核过原文再用。 |
| F37 | 属实（去掉「待核」） | VERVE-102 NEJM 2026;395:648-659（PMID 42187087，2026-05-25 在线）：35 人，0.3–1.0 mg/kg 单次静脉输注，PCSK9 降 51%–88%，LDL-C "9% at 0.3 mg/kg to 62% at 1.0 mg/kg"，无剂量限制性毒性；至少随访 1 年的有 15 人。VERVE-101 于 2024-04-02 暂停入组：第 6 例出现 3 级 ALT 升高和血小板减少（经检索摘要读到 HCPLive 与公司新闻稿）。礼来：PR Newswire 2025-07-25 "announced the successful completion of its acquisition of Verve Therapeutics"，新闻稿里没有金额。 | 「一针改写肝脏里的 PCSK9 基因，早期小试验里 LDL 最多降了六成；还在 1 期，长期安全未知，没有上市。」不要说「治本」「根治」：它仍是通过降 LDL 起效，没有改变饮食、其他基因等原因。 |
| F38 | 未能核 | 本轮没有读 CANTOS、LoDoCo2、CLEAR SYNERGY。 | 「片中不推荐秋水仙碱」这个立场合适，因为不给药物建议。 |
| F39 | 属实 | EFSA 2018 摘要（Europe PMC）："monacolin K in lactone form is identical to lovastatin"，"unable to identify a dietary intake of monacolins from RYR that does not give rise to concerns about harmful effects to health"，"as low as 3 mg/day" 也有严重不良反应个案；EFSA 2025 重申。小林制药：日本厚生劳动省认定致病物是 puberulic acid，来自红曲培养过程中混入的青霉（检索摘要转述 Japan Times、nippon.com 与 MHLW 资料）。 | 「红曲里的有效成分就是洛伐他汀，作为保健品剂量不受控；欧洲食品安全局找不到一个能确定安全的摄入量」。小林事件说成「生产中被霉菌污染，产生了伤肾的物质」。中国语境的注意事项见整体意见。 |
| F40 | 未能核 | 本轮没有读各项荟萃。 | 片中给数量级即可：「每一项单独都只降几个百分点」。具体数字核过原文再用。 |
| F41 | 属实 | Chiavaroli 2018 摘要：Portfolio "reduced the primary outcome LDL-C by ~17% (MD, -0.73 mmol/L"，对照是 NCEP Step 2 饮食，GRADE 高确定性。 | 要说明对照本身已经是降脂饮食；「组合饮食约降 17%，常用他汀约降 30–50%」这个对比可以用。 |
| F42 | 需改 | Hooper 2020 Cochrane 摘要："reducing dietary saturated fat reduced the risk of combined cardiovascular events by 17%"，RR 0.83（0.70–0.98），中等质量；全因死亡 RR 0.96、心血管死亡 RR 0.95，均不显著；"Replacing the energy from saturated fat with polyunsaturated fat or carbohydrate appear to be useful strategies"，换成单不饱和脂肪的效果不清楚。ESC 的 "greatest impact" 原句本轮没读到。 | RR 0.83 对应的是「少吃饱和脂肪」的总体结果，不是「换成植物油」专属。改为：「少吃饱和脂肪、换成多不饱和脂肪，心血管事件约少六分之一，但没看到总死亡减少」。不要说「橄榄油（单不饱和）最好」。 |
| F43 | 未能核 | 本轮没有读 ESC 2019 相关段落。 | 定性说法（「甘油三酯对酒和糖更敏感」）可以用。具体百分比核过再用。 |
| F44 | 属实 | CN2023（PMC10498001）Table 7："Lifestyle interventions are the foundation of lipid-lowering treatment"。Gylling 2014 EAS（PMID 24468148）：2 g/天植物甾醇 "lower LDL-C levels by between 8 and 10%"，"equivalent to doubling the dose of statin"。 | 要限定「在降 LDL 幅度上相当于他汀剂量翻倍」，这不是事件获益上的等价。不能说成「吃甾醇可以代替加药」。 |
| F45 | 属实（部分） | Abdelhamid 2020 Cochrane：全因死亡 RR 0.97（0.93–1.01）、心血管事件 RR 0.96（0.92–1.01），高确定性。Gencer 2021 Circulation：房颤 HR 1.25（1.07–1.46），>1 g/天 HR 1.49（1.04–2.15），≤1 g/天 HR 1.12。REDUCE-IT 与 STRENGTH 本轮未核。 | 「普通鱼油基本不能预防心脏病，而且剂量越大，房颤风险越高」。REDUCE-IT 是处方药，片中最好不展开，免得观众去买保健品鱼油。 |
| F46 | 需改 | Zhao 2023 JAMA Netw Open（PMID 37000449）：低量饮酒（1.3–24 g/天）对比终生不饮酒者，**全因死亡** RR 0.93，P=.07。纳豆激酶（Hodis 2021，PMID 33843667）："annualized rate of change in CIMT and CAS did not significantly differ"。大蒜本轮未核。 | 改为：「校正研究设计偏差后，少量饮酒的人总死亡风险并不比滴酒不沾的人低」。不要写成「护心」不显著，原研究的结局是全因死亡。纳豆激酶可以说「随机试验里没能延缓颈动脉增厚」。 |
| F47 | 需改 | CN2023 §9.3："reducing dietary cholesterol intake to less than 300 mg per day for those at high risk of ASCVD and patients with hypercholesterolemia"（适用人群是高危者**和**高胆固醇血症患者）。CN2023 这一节没有提鸡蛋。「每天 1 个」只有媒体来源。 | 不说具体几个鸡蛋。「中国指南建议：高危或胆固醇高的人，每天饮食胆固醇少于 300 毫克；鸡蛋对每个人影响不一样，问医生」。适用人群要写全。 |
| F48 | 属实 | CN2023 Table 2 标题："Reference standards for major lipid indicators in low-risk groups for primary prevention of ASCVD in China"；LDL-C 分级：Ideal <2.6、Reasonable <3.4、Slight elevation 3.4–4.1、Elevation ≥4.1 mmol/L。 | 这是全片最关键的一句，可以用：「化验单上的参考范围，是给没病、低风险的人用的」。 |
| F49 | 属实 | CN2023 Table 6：低危 <3.4；中危与高危 <2.6；极高危 "<1.8 and >50% reduction from baseline"；超高危 "<1.4 and >50% reduction from baseline"。超高危定义："≥2 severe ASCVD events or 1 severe ASCVD event combined with ≥2 high-risk factors"；严重事件与高风险因素的具体条目本轮未读到（原文是流程图）。 | 「风险越高，目标越低」的梯子可以用，数字可以上屏。超高危的具体条目不要凭记忆列。 |
| F50 | 未能核（ESC 部分） | 中国高危 <2.6 已核（F49）；ACC 2026 高危 <70 mg/dL（≈1.8）已核（ACC 新闻稿）。ESC 数值和三份指南的胰腺炎 TG 阈值本轮未读。 | 片中只讲「不同国家的指南数字不一样」，不逐一对表。 |
| F51 | 属实（去掉「待核」） | ACC/AHA 2026 指南 PDF 摘要原句："retires and replaces the '2018 … Guideline on the Management of Blood Cholesterol'"；推荐表："COR 1: In all adults, measurement of Lp(a) concentration is recommended at least once"。ACC 新闻稿（acc.org，2026-03-13）：PREVENT 用于 "adults ages 30-79 years"，算 10 年和 30 年风险；目标 "<100 mg/dL"（临界 / 中危）、"<70"（高危）、"<55"（极高危 ASCVD）。PDF 是第三方托管，但与 ACC 官方新闻稿一致。 | 可以用。PREVENT 还限定 LDL-C 在 70–189 mg/dL 之间、没有已知 ASCVD。 |
| F52 | 需改（小） | ACC 2026 推荐原文：COR 2a，"In adults at intermediate risk or select adults at borderline risk … if the CAC score is 0 AU and there is preference to avoid LLT and focus on lifestyle management and no higher risk conditions (FH or severe hypercholesterolemia ≥190 mg/dL, diabetes and age >40 years, current cigarette smoking, strong family history of premature ASCVD) … reasonable to defer therapy and reassess with repeat CAC testing in 3 to 7 years"。另一处："a CAC of 0 may not be used to 'de-risk' patients with FH"。 | 补上「本人倾向不吃药」这个条件，以及推荐等级（2a，「合理」而非「应该」）。「CAC=0 可以暂缓，3–7 年复查」中的「暂缓」不等于「不用管」。 |
| F53 | 属实（ACC 与中国部分；ESC 未能核） | ACC 2026 药物表："pregnancy is not a contraindication, but statins should be avoided while lactating"；§4.2.8.4 有「试孕前 1–2 个月停药」的表述（片段读到）。CN2023 §12.6："Statins are not usually recommended"，高危孕妇 "may choose statins with caution based on a multidisciplinary consultation"。 | 用档案 guidelines 角度已写好的统一说法：「普通人备孕前停药，有家族性高胆固醇或心脏病史的孕妇由医生个体化决定」。 |
| F54 | 属实（ACC 部分） | ACC 2026 推荐（COR 1）："a standard nonfasting or fasting lipid profile is recommended"。 | 可以说「多数情况下不用空腹」，并加「甘油三酯很高时医生可能让你空腹复查」。 |
| F55 | 属实 | 网信办原页（cac.gov.cn 2025-08-01）：2025-07-28，四部门联合；第五条 "严禁无资质账号生产发布专业医疗科普内容"；第三条要求对「结合医疗领域素材摆拍剧情、借助人工智能技术生成合成医疗科普信息」严格标注；第七条禁止借科普推广医疗、药品、保健食品，以及在同一页面出现商品经营者的地址、联系方式、购物链接。 | 合规清单照执行。「专业医疗科普内容」的边界没有明文，持证医生审稿署名应升为发布前的硬条件，不只是「建议」（需用户决定）。 |
| F56 | 需改（小） | YouTube 帮助中心 13813322：治疗类错误信息示例中没有他汀或胆固醇；例外条款："We may allow content … if that content includes additional context in the video, audio, title, or description"，"We may also make exceptions if the purpose of the content is to condemn, dispute, or satirize misinformation"，"This is not a pass to promote misinformation"。政策没有要求列来源。健康来源标签本轮未核。 | 改为「YouTube **可能**放行为了驳斥而引用的谣言，前提是视频、音频、标题或简介里有补充背景」。同片给来源是我们自己的标准，不是平台要求，两者要分开写。 |
| F57 | 属实 | Akl 2011 Cochrane 摘要：自然频数比概率更易懂 "SMD 0.69 (95% CI 0.45 to 0.93)"；相对风险降低 "was perceived to be larger"，而且 "more persuasive"（SMD 0.66）。Gigerenzer 2007 未读。 | 照用。Akl 的发现还反过来支持 §5「不单给相对风险」的规则。 |
| F58 | 未能核 | 本轮没有读 Shen 2015、Xu 2023。 | 只影响形式设计，不上屏，不阻塞。 |

### 判定计数

每条只计一个主判定；单元格里注明的「部分」「只核了算术」等限定，以表内文字为准。

| 判定 | 条数 | 编号 |
|---|---|---|
| 属实 | 35 | F03 F04 F05 F06 F07 F08 F10 F11 F12 F13 F14 F15 F17 F18 F19 F20 F21 F23 F26 F27 F29 F32 F33 F37 F39 F41 F44 F45 F48 F49 F51 F53 F54 F55 F57 |
| 需改 | 10 | F02 F30 F31 F34 F35 F42 F46 F47 F52 F56 |
| 不实 | 0 | — |
| 未能核 | 13 | F01 F09 F16 F22 F24 F25 F28 F36 F38 F40 F43 F50 F58 |

其中「属实」里有一部分只核了一部分，用之前要看表内限定：

- F05、F10：只复核了算术，输入值（LDL-P 范围、LAD 内径）没读到原文。
- F08：只有二手摘要。
- F13、F15、F20、F23、F45：部分子项没核。
- F53、F54：只读到 ACC 与中国指南，ESC 部分没读到。
- F33：「不会反跳」那一句没能核。

## 2. 整体意见

### 2.1 论点（档案 §1）是否成立

**基本成立。** 支撑论点的三块都读到了原文：①LDL 是病因：EAS 2017 写 "unequivocally establishes"，危害随暴露时间增加；②致病起点是「颗粒穿过内皮后被滞留」：EAS 2020，颗粒靠转胞吞进入，被蛋白聚糖粘住；③化验单参考范围只适用于低危一级预防：CN2023 Table 2 标题。「量 × 时间 × 本来的风险」作为叙事框架站得住，但它是比喻，不能讲成公式。

需要处理的两个问题：

1. **开场句「LDL 不是『坏胆固醇』」跟怀疑派用的是同一句话。** 档案 benchmark 角度列的 B 站怀疑论视频标题就是「LDL 从来就不是坏胆固醇；他汀也治不好高血脂！」。如果观众只看了开头几秒（短视频平台很常见），会把这句当成「LDL 无害」。建议开场就把后半句说出来：「它不是坏东西，是运输船；但船太多、开太久，就会造成伤害。」两句之间不要隔一个镜头。英文版同理，"LDL isn't 'bad cholesterol'" 是 LMHR 圈子的常用语。
2. **「回应」段里的 3 个事实需要更新或补限定。** ①KETO-CTA 撤稿已核实，去掉「待核」，表述为「作者和编辑一同撤回，原因是错误过大」，不要推测动机。②「RCT 显示获益不分年龄」：STAREE 已经给出 ≥70 岁一级预防的 RCT 证据（MACE 少约 30%），但无失能生存没有改善，而且不良事件（肝胆、糖尿病）增加。这一段应改成「老年人吃他汀能减少心脏事件，但不能让人活得更长、更不失能，所以是取舍」，比「不分年龄」更准确。③「>90% 肌肉症状不由他汀引起」要并列「第一年每 100 人约 1 人真由药引起」（CTT 2022 / 2026），否则对已经有症状的观众显得轻慢。

### 2.2 遗漏的重要限定

- **绝对获益取决于本来的风险。** 档案已经有这个意思，但 F27 的「每万人 1,000 / 500 例」默认 LDL 降 2 mmol/L、为期 5 年。多数一级预防观众实际降不了这么多，得到的获益更小。片中每个「100 个人里」都要注明前提：什么风险、降多少、吃几年。
- **副作用要全。** 出血性卒中（每万人 5 年 5–10 例，Collins 2016 写「probably」）在 F31 里漏了；STAREE 的肝胆不良事件 3.3% vs 0.9% 也没提。宣讲安全性时漏掉不利数字，正是怀疑派最常抓的把柄。
- **Lp(a) 结局阴性不等于「Lp(a) 无害」。** 档案 causality 角度已经提醒过，讲稿里必须保留。还要说明受试者都已得病，而且 LDL 基线很低（约 65 mg/dL）。
- **「停药」相关数据的质量。** 79% 复发率来自 99 人、10 周的小试验；SITE 是开放标签、界值很宽（5 个百分点）、只看全因死亡。两者都不能撑起「可以停」或「停了很危险」这类强结论。片中只说「停药后 LDL 会回到原来的水平，停不停要和医生一起决定」。
- **基因编辑（F37）不能称作「治本」。** follow-up 046 用户问的「治本还是治标」，最诚实的回答是：他汀和基因编辑都是在降 LDL 这一环起作用，不改变饮食、其他基因、年龄等上游原因；区别只在于基因编辑可能是一次性的，而且尚在 1 期。

### 2.3 措辞上可能误导普通观众的地方

- 「他汀不伤肝」不要说，改为「严重肝损伤极少见；化验异常每年约千分之一，医生会按需复查」。中国观众最常问的就是「伤不伤肝」，说过头反而失去信任，也和说明书冲突（FDA 说明书仍写有罕见肝衰竭报告）。
- 「九成肌肉痛不是药引起的」容易被听成「你是装的」，要加「但确实有少数人是药引起的，告诉医生就能调整」。
- 「HDL 越高越危险」不能说。Madsen 是观察性研究，男性 HR 1.36 也只对应极高的那一档。
- 「少量饮酒不护心」的出处结局是全因死亡（F46），措辞要对上。
- 「CAC=0 可以不吃药」必须带上「本人倾向、无高危条件、3–7 年复查」，否则会被转述成「做个 CT 没钙化就不用管」。
- 「LDL 降 78%」这类百分比，观众容易理解成「风险也降了 78%」。Lp(a) 那一段恰好可以拿来讲「数字降了，不等于病少了」，这是好素材，要用对。
- 「化验单没箭头」这句很好，但要配 CN2023 的原话「只适用于低风险、未患病人群」，并提醒「已经得过心梗、中风的人，正常范围对你不适用」。

### 2.4 中国语境下要特别小心的说法

1. **他汀强度。** CN2023 原文："Moderate-intensity statins are the preferred strategy for lipid-lowering therapy in the Chinese population"，要求先用常规剂量或中等强度。欧美叙事常讲「高强度他汀」，中文版直接照搬会和国内指南冲突。还要结合亚洲人的药代动力学差异（FDA：瑞舒伐他汀暴露约 2 倍）和 HPS2-THRIVE 中国人肌病率更高的数据。片中不提药名和剂量，只说「中国指南多从中等强度起步，医生会按你的情况调整」。
2. **红曲。** 在国内，「红曲」既有保健品，也有经过审批的中成药处方（如血脂康）。本轮**没有**核实 CN2023 对血脂康的具体表述。说「红曲 = 不受控的洛伐他汀」之前，要分清「保健品红曲」和「处方中成药」，否则会被理解为否定一类正规药物。小林事件是日本产品被污染，不能外推到国内产品。建议审稿医生专门过这一段。
3. **单位与目标值。** 国内化验单用 mmol/L。中国「极高危」（<1.8）≠ ESC「very high」（<1.4）。中文版只用中国指南数字，英文版只用 ACC/ESC 数字，同一画面不要并列两套目标。
4. **资质与平台规则。** 网信办通知第五条（「严禁无资质账号生产发布专业医疗科普内容」）的边界没有明文。本季涉及他汀获益与风险的绝对数、停药、孕期、老人用药，按保守理解已经接近「专业医疗科普」。建议把「持证心内或内分泌医生审稿署名」升为中文平台发布的前置条件（需用户决定）。第三条对 AI 生成与剧情演绎的标注，片尾和画面都要做。
5. **「血稠」、输液「冲血管」、「洗血」。** 这三个是中国特有的谣言。档案 benchmark 角度引用的来源多为媒体访谈（可靠度低到中）。片中驳斥时以「指南没有这种做法」「斑块长在血管壁里，药液冲不掉」这类机制性说法为主，不要引用无法核实的个案。
6. **鸡蛋。** 国内观众最关心的问题之一。只引 CN2023「高危或高胆固醇者饮食胆固醇 <300 mg/天」，不给「每天几个」，因为本轮读到的唯一具体个数只来自媒体。

### 2.5 本轮没核、进讲稿前应补的

F01、F02 的颗粒尺寸、F09、F16、F22、F24、F25 的霉菌描述、F28、F36、F38、F40、F43、F50 中的 ESC 数值、F58；F34 的「观察性停药 +30%」；PDAY；CETP 抑制剂、烟酸试验；IMPROVE-IT、ODYSSEY、CLEAR Outcomes；REDUCE-IT 与 STRENGTH；CN2023 超高危的具体条目与血脂康表述。

## 3. 主要来源（本轮实际读到）

- Europe PMC REST（摘要 / 开放全文）：PMID 43001734（Lp(a)HORIZON）、40192608 / 41906601 / 42206798（KETO-CTA 原文、关注声明与撤稿）、42580354（SAGA/SITE）、41655587 与 PMC7619005（CTT 2026 副作用）、CTT 2022 肌肉症状、CTT 2024 糖尿病、42187087（VERVE-102）、17903110、17694296、24627830、Khera 2016、Collins 2016、Cohen 2006、Berenson 1998、HPS2-THRIVE 2013 EHJ、Graham 2004 JAMA、PMC7308544（Borén 2020）、28444290（Ference 2017）、PMC2988224（CTT 2010）、28859947（FOURIER 极低 LDL）、Hooper 2020、Abdelhamid 2020、Gencer 2021、Chiavaroli 2018、Gylling 2014、Voight 2012、Madsen 2017、Zhao 2023、Hodis 2021、Akl 2011、SAMSON 2021、EFSA 2018 / 2025、39662503（Berndsen Nature 2025）、PMC10498001（CN2023 英文版）、Wild & Feingold Endotext。接口：https://www.ebi.ac.uk/europepmc/webservices/rest/search
- FDA CRESTOR 说明书 2026（s047）：https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/021366s047lbl.pdf
- FDA 新闻稿（Lipfendra / enlicitide，2026-07-17）：https://www.fda.gov/news-events/press-announcements/fda-approves-first-oral-pcsk9-inhibitor-lower-ldl-cholesterol-adults-high-cholesterol
- ACC/AHA 2026 血脂异常指南 PDF（第三方托管，已本地抽文本检索原句）：https://news.randox.com/wp-content/uploads/2026/04/2026-Guideline-on-the-Management_compressed.pdf ；ACC 新闻稿：https://www.acc.org/About-ACC/Press-Releases/2026/03/13/18/01/ACCAHA-Issue-Updated-Guideline-for-Managing-Lipids-Cholesterol
- TCTMD：STAREE https://www.tctmd.com/news/staree-statins-cut-mace-risk-30-older-adults-no-cvd-history ；Lp(a)HORIZON https://www.tctmd.com/news/full-lpahorizon-results-affirm-lack-pelacarsen-benefit-secondary-prevention
- Healio（SITE 的 LDL 数字）：https://www.healio.com/news/cardiology/20260824/stopping-statins-did-not-raise-mortality-in-older-lowrisk-adults
- 礼来完成收购 Verve（PR Newswire，2025-07-25）：https://www.prnewswire.com/news-releases/lilly-completes-acquisition-of-verve-therapeutics-to-advance-one-time-treatments-for-people-with-high-cardiovascular-risk-302513948.html
- 网信办等四部门通知：https://www.cac.gov.cn/2025-08/01/c_1755764425442686.htm
- YouTube 医疗错误信息政策：https://support.google.com/youtube/answer/13813322
- 只经 WebSearch 检索摘要读到的（线索级）：STAREE HR 与 CI（ESC 新闻稿 https://www.escardio.org/news/press/press-releases/cholesterol-lowering-medication-reduces-major-cardiovascular-events-by-30-per-cent-in-older-people-without-known-cardiovascular-disease/ ）；Bogalusa 50% / 85%（AAFP 1998 https://www.aafp.org/pubs/afp/issues/1998/1101/p1657.html ）；VERVE-101 暂停（https://hcplive.com/view/verve-therapeutics-halts-enrollment-of-heart-1-pcsk9-gene-therapy-trial ）；小林制药 puberulic acid（https://japantimes.co.jp/news/2024/09/18/japan/science-health/beni-koji-puberulic-acid-to-blame ）；ORION-4 状态（https://clinicaltrials.gov/study/NCT03705234 ）；Merck 公告日（https://www.pharmacytimes.com/view/fda-approves-enlicitide-the-first-oral-pcsk9-inhibitor-for-high-cholesterol ）。
