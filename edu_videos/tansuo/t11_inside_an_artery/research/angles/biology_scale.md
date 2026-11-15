---
worker_id: researcher-01-biology-scale
stage: 3
role: researcher
angle: biology-scale
status: partial
blockers:
  - "NCBI Bookshelf（Endotext 网页版、StatPearls）、PubMed、Europe PMC、nobelprize.org、ahajournals.org 返回浏览器验证或 403；Endotext 改读 endotext.org 的 PDF 版成功，其余未能直读。"
  - "后期 PMC 也开始返回 reCAPTCHA，Virmani 斑块分类原表（Heart 2003, PMC1767898）、apoB100 冷冻电镜 Nature 2025 正式版（PMC11839476）未读到全文，只用了检索摘要与 bioRxiv 预印本。"
  - "Brown & Goldstein 1985 诺贝尔演讲原文未读到（LDL 22 nm、约 1500 个胆固醇酯、约 3×10^6 Da 仅来自检索摘要）。"
  - "Dodge 1992 冠脉内径、冠脉血流速度、内皮细胞尺寸、斑块黄色成因（β-胡萝卜素）只读到检索摘要，未读原文。"
  - "未查到：人体内肝脏合成占全身合成的比例；正常冠脉内膜厚度；胆固醇分子长度的直接测量值；泡沫细胞直径；病理切片常用染色（H&E、油红 O）的颜色描述原文；HDL 致病因果争议的原始研究（留给其他研究员）。"
  - "WebSearch 20 次额度已用完。"
confidence: medium
---

# 血脂的生物学原理与尺度（「缩小进血管」画面的结构依据）

> 写法说明：每条事实标出处与可靠度。「直读」= 本次实际打开原文 / PDF 读到；「检索摘要」= 只在搜索结果摘要里看到，未能打开原文，可靠度相应下调。数字换算（胆固醇 mg/dL ÷ 38.67 = mmol/L）为标准换算系数，本次未另查来源；甘油三酯 1.7 mmol/L = 150 mg/dL 见 Borén 2020 原文。

## 主要来源清单

| 代号 | 来源 | 读取方式 |
|---|---|---|
| [Feingold] | Feingold KR. *Introduction to Lipids and Lipoproteins*. Endotext, Updated January 12, 2024. https://www.endotext.org/wp-content/uploads/pdfs/introduction-to-lipids-and-lipoproteins.pdf | 直读 PDF 第 1–16 页 |
| [Borén2020] | Borén J, Chapman MJ, … Ginsberg HN. Low-density lipoproteins cause atherosclerotic cardiovascular disease: pathophysiological, genetic, and therapeutic insights. A consensus statement from the EAS Consensus Panel. *Eur Heart J* 2020;41(24):2313–2330. https://pmc.ncbi.nlm.nih.gov/articles/PMC7308544/ | 直读（前 100k 字符；全文 398k 未读完） |
| [Ference2017] | Ference BA, et al. Low-density lipoproteins cause ASCVD. 1. Evidence from genetic, epidemiologic, and clinical studies. EAS consensus. *Eur Heart J* 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5837225/ | 直读（前 100k 字符） |
| [Williams1995] | Williams KJ, Tabas I. The Response-to-Retention Hypothesis of Early Atherogenesis. *Arterioscler Thromb Vasc Biol* 1995;15(5):551–561. https://pmc.ncbi.nlm.nih.gov/articles/PMC2924812/ | 直读（前 100k 字符） |
| [Berndsen2024] | Berndsen ZT, Cassidy CK. The Structure of ApoB100 from Human Low-density Lipoprotein. bioRxiv 2024.02.28.582555（预印本，2025 年正式发表于 *Nature* 638, 检索摘要可见） https://www.biorxiv.org/content/10.1101/2024.02.28.582555.full.pdf | 直读 PDF 第 1–4 页 |
| [Stellaard2017] | Stellaard F, Lütjohann D. The Interpretation of Cholesterol Balance Derived Synthesis Data… *Cholesterol* 2017:5046294. https://pmc.ncbi.nlm.nih.gov/articles/PMC5340945/ | 直读 |
| [LipidWeb] | Christie WW. Cholesterol and Cholesterol Esters. The LipidWeb (LIPID MAPS). https://lipidmaps.org/resources/lipidweb/lipidweb_html/lipids/simple/cholest/index.htm | 直读 |
| [Morris2014] | Morris P, et al. Relationship between plasma apolipoprotein B concentrations and LDL particle number. *Res Rep Clin Cardiol* 2014;5:237–242. https://www.dovepress.com/relationship-between-plasma-apolipoprotein-b-concentrations-and-ldl-pa-peer-reviewed-fulltext-article-RRCC | 直读 |
| [PDAY1998] | Wissler RW, Strong JP, PDAY Research Group. Risk Factors and Progression of Atherosclerosis in Youth. *Am J Pathol* 1998;153(4):1023–1033. https://pmc.ncbi.nlm.nih.gov/articles/PMC1853040/ | 直读 |
| [AAFP-Bogalusa] | Kirchner (AFP 1998, Tips from Other Journals) 对 Berenson GS et al. *NEJM* 1998;338:1650–6（Bogalusa）的摘要 https://www.aafp.org/pubs/afp/issues/1998/1101/p1657.html | 直读二手摘要（原文 NEJM 未读） |
| [HistoGuide] | HistologyGuide 血涂片切片说明 https://histologyguide.com/slideview/MH-033hr-blood-smear/07-slide-1.html | 直读（教学网站） |
| [Mizuno2017] | Mizuno K, Takano M. What Does the Yellow Color of Angioscopy Mean? Why Yellow Plaque Is Always Vulnerable? *Angioscopy* 2017;3(1):9–18. https://www.jstage.jst.go.jp/article/angioscopy/3/1/3_9/_article/-char/en | 直读摘要页 |

---

## 1. 血脂是什么：三种主要脂质的作用；为什么要「包裹运输」

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 胆固醇和甘油三酯不溶于水，必须与蛋白质结合（脂蛋白）才能在血中运输 | — | [Feingold] | "Cholesterol and triglycerides are insoluble in water and therefore these lipids must be transported in association with proteins." | 高（权威教科书章节） |
| 脂蛋白结构：疏水核心（胆固醇酯 + 甘油三酯）外包一层亲水膜（磷脂、游离胆固醇、载脂蛋白） | — | [Feingold] | "a central hydrophobic core of non-polar lipids, primarily cholesterol esters and triglycerides… surrounded by a hydrophilic membrane consisting of phospholipids, free cholesterol, and apolipoproteins" | 高 |
| 饭里的大量脂肪酸要以甘油三酯形式运输以免毒性 | 膳食甘油三酯约 100 g/天 | [Feingold] | "Large quantities of fatty acids from meals must be transported as triglycerides to avoid toxicity." / "Dietary triglycerides (approximately 100 grams per day)" | 高 |
| 胆固醇功能 1：调节细胞膜流动性；与鞘脂共同组装膜上「脂筏」 | 质膜中游离胆固醇约占膜脂的 30–50%，占细胞内胆固醇的 60–80% | [LipidWeb] | "One of the main functions of cholesterol is to modulate the fluidity of membranes"; "roughly 30-50% of the lipid in the membrane or 60‑80% of the cholesterol in the cell" | 高（专业参考站） |
| 胆固醇功能 2：胆汁酸和类固醇激素的合成前体；维生素 D3 由 7-脱氢胆固醇经紫外线裂解生成 | — | [LipidWeb] | "It is a biosynthetic precursor of bile acids and steroid hormones"; "Ultraviolet light mediates cleavage of 7‑dehydrocholesterol" | 高 |
| 胆固醇酯是血浆运输和细胞内储存的「惰性」形式 | — | [LipidWeb] | cholesterol esters are "preferred for transport in plasma and as a biologically inert storage" form | 高 |
| 脑是含胆固醇最多的器官 | 约占全身游离胆固醇的 1/4 | [LipidWeb] | "it comprises roughly a quarter of the total free cholesterol in the human body" | 高 |
| 甘油三酯：经脂蛋白脂肪酶（LPL）水解为脂肪酸，供肌肉 / 心脏利用（能量）或脂肪组织储存 | — | [Feingold] | "free fatty acids, which can be taken up by the adjacent muscle cells and adipocytes for either energy production or storage" | 高 |
| 磷脂：构成脂蛋白表面单分子层（以及细胞膜） | — | [Feingold] 图 1 "Surface Monolayer of Phospholipids and Free Cholesterol" | 高 |

### 人体胆固醇：自己合成 vs 吃进来

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 胆固醇平衡法测得的全身合成量（杂食者、安慰剂组） | 868 ± 358 mg/天 | [Stellaard2017] 表 1 | placebo 868 ± 358 | 中高（同位素/平衡法人体研究，样本小） |
| 同组从饮食吸收进体内的胆固醇 | 162 ± 51 mg/天 | [Stellaard2017] 表 1 | placebo 162 ± 51 | 中高 |
| 由上两数推算：新进入体内的胆固醇约 84% 来自自身合成、约 16% 来自饮食吸收（868 /(868+162)） | 约 84% / 16% | 本文计算 | — | 中（单一小样本，个体差异大，SD 很宽） |
| 纯素食者：合成 595 mg/天，吸收的饮食胆固醇平均仅 14 mg/天 | — | [Stellaard2017] | "The daily amount of absorbed dietary chol was even lower in the vegans" | 中 |
| 肠腔里的胆固醇主要来自胆汁而非食物 | 胆汁 800–1200 mg/天 vs 饮食 200–500 mg/天 | [Feingold] | "approximately 800-1200mg of cholesterol from bile vs. 200-500mg from diet" | 高 |
| 人通常只吸收约一半的饮食胆固醇 | 约 50%（25–75%）；另一来源 20–80% | [Feingold]；[Stellaard2017] | "humans typically absorb only approximately 50% of dietary cholesterol with a range of 25-75%" | 高 |
| 肝脏在全身合成中所占比例（人） | **未查到人类数据**；啮齿类肝约 40–50%，食蟹猴肝仅约 10–20% | [Stellaard2017] | "the liver is the major site of chol synthesis (about 40–50%) followed by the skin (20%)"（啮齿类）；"hepatic contribution is low, maybe 10–20%"（猴） | — 尚不清楚 |
| HMG-CoA 还原酶是胆固醇合成的限速酶 | — | [Feingold]；[LipidWeb] | "HMG-CoA reductase, the rate limiting enzyme in cholesterol synthesis" | 高 |

**结论（已证实）**：大部分胆固醇是身体自己造的，饮食只占少数，且吸收率个体差异很大。**尚不清楚**：「肝脏合成了全身大部分胆固醇」这一常见说法——本次未找到人体数据支持；肝脏确定的角色是**调控血中 LDL 的主要器官**（见第 3 节约 70% LDL 经肝清除）。视频里建议说「身体自己造的」，不要说「肝脏造了 X%」。

---

## 2. 脂蛋白家族

### 2.1 分类总表（[Feingold] 表 1，直读）

| 脂蛋白 | 密度 g/mL | 直径 nm | 主要脂质 | 主要载脂蛋白 | 来源 |
|---|---|---|---|---|---|
| 乳糜微粒 | <0.930 | 75–1200 | 甘油三酯 | ApoB-48、C、E、A-I、A-II、A-IV | 小肠 |
| 乳糜微粒残粒 | 0.930–1.006 | 30–80 | 甘油三酯、胆固醇 | ApoB-48、E | 血中由乳糜微粒转化 |
| VLDL | 0.930–1.006 | 30–80 | 甘油三酯 | ApoB-100、E、C | 肝 |
| IDL（VLDL 残粒） | 1.006–1.019 | 25–35 | 甘油三酯、胆固醇 | ApoB-100、E、C | 血中由 VLDL 转化 |
| LDL | 1.019–1.063 | 18–25 | 胆固醇 | ApoB-100 | 血中由 IDL 转化 |
| HDL | 1.063–1.210 | 5–12 | 胆固醇、磷脂 | ApoA-I、A-II、C、E | 肝、小肠 |
| Lp(a) | 1.055–1.085 | ~30 | 胆固醇 | ApoB-100 + Apo(a) | 肝 |

- 可靠度：高（权威教科书章节；数值为范围，各来源略有差异）。
- 其他来源的 LDL 直径：[Berndsen2024] "LDL particles range in diameter from ~17-28 nm"；VLDL "large (~40-70 nm)"。检索摘要中另有来源给 VLDL 30–90 nm、LDL 20–25 nm——**引用时注明来源**。
- **致动脉粥样硬化性**：[Feingold] "Chylomicron remnants, VLDL, VLDL remnants (IDL), LDL, and Lp (a) are all pro-atherogenic while HDL is anti-atherogenic."（高；但「HDL 抗动脉粥样硬化」的因果性有争议，见第 3 节注）。
- **能进入动脉壁的尺寸门槛**：[Ference2017] "LDL and other apoB-containing lipoproteins <70 nm in diameter (including VLDL, their remnants, IDL, and Lp(a)) efficiently enter and exit the arterial intima."；[Borén2020] "Apolipoprotein B-containing lipoproteins of up to ∼70 nm in diameter"。高（两份 EAS 共识）。推论：大的乳糜微粒（75–1200 nm）太大进不去。

### 2.2 载脂蛋白（[Feingold] 表 3 与正文，直读）

| 载脂蛋白 | 分子量 Da | 产地 | 每颗粒数目 | 要点 |
|---|---|---|---|---|
| ApoB-48 | 241,000 | 小肠 | 每个乳糜微粒 1 个 | 与 ApoB-100 同一基因；小肠 apobec-1 编辑 mRNA 产生终止密码子，蛋白约为肝版一半长；**不含 LDL 受体识别区** |
| ApoB-100 | 512,000（Feingold）；~550 kDa、4563 个残基（Berndsen） | 肝 | **每个 VLDL、IDL、LDL、Lp(a) 恰好 1 个** | LDL 受体的配体 |
| ApoA-I | 28,000 | 肝、小肠 | 每个 HDL 可有多个 | 约占 HDL 蛋白 70%；激活 LCAT |
| Apo(a) | 250,000–800,000（正文写 300,000–800,000） | 肝 | 与 ApoB-100 1:1，二硫键相连 | 纤溶酶原同源物；抑制纤溶；仅灵长类有；生理功能未知 |
| ApoE | 34,000 | 肝为主 | 可交换 | 残粒清除的关键配体 |

原文要点：
- "There is a single molecule of Apo B-100 per VLDL, IDL, LDL and Lp(a) particle."（[Feingold]，高）；[Ference2017] "each LDL particle contains a single apoB molecule"；[Borén2020] "apoB100 (one molecule per LDL particle)"。
- "Lp (a) is an LDL particle that has apolipoprotein (a) attached to Apo B-100 via a disulfide bond… The size of Lp(a) particles can vary greatly based on the size of apolipoprotein (a)."（[Feingold]，高）
- "Interestingly this apolipoprotein is found in primates but not in other species."（[Feingold]，高）

### 2.3 一个 LDL 颗粒里有多少胆固醇

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 每个 LDL 含胆固醇分子数 | 2000–2700 个，其中约 1700 个为酯化形式 | [Borén2020] | "(2000–2700 molecules per particle, of which ∼1700 are in esterified form)" | 高（EAS 共识） |
| 脂质占 LDL 重量 | 约 80% | [Borén2020] | "The lipidome accounts for ∼80% by weight." | 高 |
| 经典描述：LDL 直径 22 nm、质量约 3×10^6 Da、核心约 1500 个胆固醇酯分子；外壳约 800 个磷脂、500 个游离胆固醇、1 个 apoB | — | Brown & Goldstein 诺贝尔演讲（1985）/ 诺奖新闻稿 | **仅检索摘要，原文 403 未读** | 中（与 Borén 数量级一致） |
| 交叉验算：用 [Morris2014] 人群均值 LDL-C 112.7 mg/dL（= 2.91 mmol/L）÷ LDL-P 1590 nmol/L ≈ **每颗粒约 1830 个胆固醇分子** | ~1800 | 本文计算 | — | 中（落在 Borén 2000–2700 范围下沿附近，量级一致） |

### 2.4 血液里有多少个 LDL 颗粒

| 事实 | 数字 | 出处 | 原文 | 可靠度 |
|---|---|---|---|---|
| 1,027 名门诊患者的均值 | LDL-C 112.7 ± 39.4 mg/dL（2.91 mmol/L）；LDL-P 1590 ± 554 nmol/L；apoB 97.7 ± 25.1 mg/dL | [Morris2014] | "mean LDL-P was 1,590±554 nmol/L"; "mean apoB was 97.7±25.1 mg/dL" | 中（观察性，非人群随机样本，患者人群） |
| Framingham 后代研究人群百分位：apoB 第 20 百分位 <78 mg/dL、第 80 百分位 >118 mg/dL；LDL-P 1100–1439 nmol/L 对应第 20–50 百分位 | — | [Morris2014] 引 Framingham | "apoB concentration <78 mg/dL which corresponds to the 20th Framingham Offspring Study population percentile" | 中 |

**算法（写清楚，便于复核）**：
- 1 nmol/L = 10⁻⁹ mol/L × 6.022×10²³ = 6.0×10¹⁴ 个/L = 6.0×10¹¹ 个/mL。
- LDL-P 1100–1600 nmol/L → **约 0.7×10¹⁸ – 1.0×10¹⁸ 个/L**，即**每毫升约 7×10¹⁴ – 1×10¹⁵ 个，每微升约 7000 亿 – 1 万亿个**。
- 用 apoB 推算（因每个 VLDL/IDL/LDL/Lp(a) 恰好 1 个 apoB）：97.7 mg/dL = 977 mg/L ÷ 512,000 g/mol ≈ 1.9 µmol/L ≈ 1.15×10¹⁸ 个致动脉粥样硬化颗粒/L（用 550 kDa 则约 1.07×10¹⁸）。这包含 VLDL、IDL、Lp(a)，不只是 LDL。
- 注意：[Borén2020] 原文网页显示 "At circulating particle concentrations of ∼1 mmol/L"——按上式应为约 1 µmol/L 量级，疑为网页单位符号转换问题，**不要引用该处单位**。
- 红细胞数量的对比（每微升数百万个）本次**未查到来源**（记忆中：成人约 4–6×10⁶/µL，未证实）；若要讲「LDL 比红细胞多十万倍」，需他人核实红细胞计数。

### 2.5 LDL 的真实形状（冷冻电镜，[Berndsen2024]，直读）

| 事实 | 原文 | 可靠度 |
|---|---|---|
| 纯化的较小 LDL 颗粒直径 16.2–22.4 nm，均值 19.3 nm，离心率 0.48（不是正圆） | "The particle diameters ranged from 16.2-22.4 nm (mean = 19.3 nm)… mean eccentricity was 0.48" | 中高（预印本，已在 Nature 2025 正式发表——正式版本次未读） |
| 整体形状：**半盘状、带多边形特征，约 17 × 20 nm**（属小而密 LDL） | "semi-discoidal with polygonal features and dimensions of ~17 nm x 20 nm" | 中高 |
| 约 30% 颗粒核心可见胆固醇酯的液晶态有序堆叠 | "~30% contained well-ordered stacks of high-density features in their core… liquid crystalline phase of CE" | 中高 |
| ApoB100：一个大球状 N 端结构域 + 一条**约 58 nm 长、4 nm 宽的连续 β-折叠「腰带」绕颗粒一整圈** | "a ~58 nm long x 4 nm wide continuous amphipathic β-sheet that wraps completely around the circumference of the particle, holding it together like a belt" | 中高（正式版检索摘要为 ~61 nm） |
| 腰带两侧有 9 个插入片段（约 30–700 个残基），最大两个形成跨越脂表面的螺旋串 | "9 strategically located inserts that vary in size from ~30-700 residues" | 中高 |
| N 端 β-桶以约 35° 伸出颗粒表面，是电镜图像中最突出的蛋白特征 | "The β-barrel projects away from the surface of the particle at ~35° and is the most prominent protein feature in the cryo-EM images" | 中高 |

验算：直径 19.3 nm 的圆周 ≈ π × 19.3 ≈ 61 nm，与 58–61 nm 的腰带长度吻合——「一条蛋白腰带绕一圈」在尺度上自洽。

---

## 3. 运输路线

| 环节 | 事实 | 出处 / 原文 | 可靠度 |
|---|---|---|---|
| 外源途径（小肠） | 吸收的脂肪酸重新合成甘油三酯，与胆固醇酯一起在内质网装进乳糜微粒，需 ApoB-48 和 MTTP | [Feingold] "The triglycerides and cholesterol esters are packaged into chylomicrons in the endoplasmic reticulum." | 高 |
| 乳糜微粒走淋巴 | 分泌入淋巴，经胸导管进入体循环，**不经门静脉直接到肝** | [Feingold] "Chylomicrons are secreted into the lymph and delivered via the thoracic duct to the circulation… not delivered directly to the liver via the portal circulation." | 高 |
| LPL 卸货 | 肌肉、脂肪组织的 LPL 锚定在毛细血管内皮腔面，经 ApoC-II 激活水解甘油三酯 → 乳糜微粒残粒 → 被肝摄取 | [Feingold] | 高 |
| 处理能力 | 正常人可处理 ≥100 g/天脂肪；一餐 75 g 脂肪只轻度升高餐后甘油三酯 | [Feingold] "a meal containing 75 grams of fat results in only a very modest increase in postprandial triglyceride levels" | 高 |
| 内源途径（肝） | 肝把甘油三酯与胆固醇酯装上新合成的 ApoB-100 → VLDL；甘油三酯供应决定 VLDL 分泌速率与大小 | [Feingold] "The availability of triglycerides is the primary determinant of the rate of VLDL synthesis." | 高 |
| VLDL → IDL → LDL | LPL 水解 → IDL；约 50% IDL 被肝清除，其余经肝脂酶进一步水解成 LDL | [Feingold] "only a fraction of IDL particles are cleared (approximately 50% but varies)… Thus, LDL is a product of VLDL metabolism." | 高 |
| LDL 清除 | **约 70% 循环 LDL 经肝细胞 LDL 受体介导的内吞清除**，其余由肝外组织摄取 | [Feingold] "approximately 70% of circulating LDL is cleared via hepatocyte LDL receptor mediated endocytosis" | 高 |
| LDL 受体机制 | 识别 ApoB-100 与 ApoE → 内吞 → 溶酶体降解 → 释放胆固醇 → 抑制 HMG-CoA 还原酶、减少受体表达（反馈） | [Feingold] 图 3（改自 Brown & Goldstein, *Annu Rev Biochem* 46:897, 1977） | 高 |
| 受体数量调控 | 细胞胆固醇低 → SREBP 从内质网转运至高尔基体被切割激活 → 入核促进 LDL 受体与 HMG-CoA 还原酶转录 | [Feingold] | 高 |
| PCSK9 | 分泌型蛋白，与 LDL 受体结合，促使受体在溶酶体中降解；功能缺失突变 → 受体增多、LDL 降低；功能获得突变 → LDL 升高 | [Feingold] "PCSK9, a secreted protein that binds to the LDL receptor and enhances LDL receptor degradation in the lysosomes." | 高 |
| HDL 逆向转运 | ApoA-I 经 ABCA1 获得胆固醇与磷脂 → 盘状 HDL → LCAT 把游离胆固醇酯化入核 → 球形 HDL → 经肝 SR-B1 直接交还，或经 CETP 转给 VLDL/LDL 再被肝摄取 | [Feingold] 图 8 与摘要 | 高（机制） |
| Brown & Goldstein 诺奖 | 1985 年诺贝尔生理学或医学奖，演讲题为 "A Receptor-Mediated Pathway for Cholesterol Homeostasis" | 仅检索摘要（nobelprize.org 403） | 中 |

注（有争议，仅点到）：[Feingold] 对 HDL 写的是 "one potential mechanism by which HDL may be anti-atherogenic"——机制上合理，但「升高 HDL 胆固醇是否降低风险」本次未查原始研究（记忆中：孟德尔随机化与 CETP 抑制剂试验对 HDL-C 因果性提出质疑，未证实），交由负责「好与坏」的研究员。

---

## 4. 动脉粥样硬化如何发生

### 4.1 步骤与证据

| 步骤 | 事实 | 出处 / 原文 | 可靠度 / 状态 |
|---|---|---|---|
| ① 进入 | <70 nm 的含 apoB 颗粒可进出动脉内膜 | [Ference2017]；[Borén2020] | 高 / 已证实 |
| ① 进入方式 | 跨内皮转胞吞：依赖小窝（caveolae）的囊泡途径，涉及 SR-B1（与 DOCK4 偶联）和 ALK1；在体循环中**不依赖 LDL 受体**（PCSK9 降解 LDL 受体对其无影响） | [Borén2020] | 中高 / 较新机制研究，细节仍在发展 |
| ① 小而密 LDL 进得更快 | "small dense LDL appears to enter the arterial intima faster than larger LDL" | [Borén2020] | 中 |
| ② 滞留（核心事件） | 「滞留反应假说」：脂蛋白滞留是早期病变「既必要又充分」的关键致病事件 | [Williams1995] "there exists a key pathogenic event, namely, lipoprotein retention, that is both necessary and sufficient" | 高 / 主流共识（[Borén2020] 沿用） |
| ② 滞留机制 | ApoB100 上带正电的精氨酸、赖氨酸残基与动脉蛋白聚糖带负电基团结合 | [Borén2020] "positively charged amino acyl residues (arginine and lysine) in apoB100" | 高 |
| ② 速度（动物） | 高胆固醇血症开始后数分钟到数小时内即可检测到滞留与聚集；兔注射 LDL 后 2 小时内 | [Williams1995] "lipoprotein retention and aggregation are detectable within minutes to hours after the onset of hypercholesterolemia" | 中（动物模型） |
| ② 好发部位 | 分叉等湍流部位易发病；胆固醇很高时低剪切部位也会发病 | [Williams1995] "show a predisposition to lesion development" | 高 |
| ③ 修饰 | 滞留的 LDL 易被氧化（产生氧化磷脂等）、聚集；氧化被视为「滞留的正常预期后果」 | [Borén2020]；[Williams1995] "a normal, expected consequence of lipoprotein trapping" | 高（发生）；**有争议**（氧化是起始原因还是后果——滞留假说一方认为是后果；对方「氧化假说」的原文本次未读） |
| ④ 单核 → 巨噬 → 泡沫细胞 | 新招募的单核细胞分化为巨噬细胞，经清道夫受体摄取修饰 LDL，成为充满胆固醇酯脂滴的泡沫细胞 | [Borén2020] "giving rise to cholesterol-laden foam cells"；图 1 图注 "cholesteryl ester droplet-engorged macrophage foam cells" | 高 |
| ⑤ 坏死核心 | 凋亡细胞清除受损 → 坏死核心；含细胞与胞外碎屑及**胆固醇结晶** | [Borén2020] "Impaired clearance of apoptotic cells results in the formation of necrotic cores"；图 1 "LDL-cholesterol-derived cholesterol crystals" | 高 |
| ⑥ 破裂与血栓 | 尸检冠脉血栓多数由斑块破裂引起（73%）；侵蚀在较年轻、尤其女性患者中占比更高 | [Borén2020] "Plaque rupture accounts for the majority of coronary thrombi at autopsy (73%)" | 高（尸检病理） |
| 内皮多数时候是完整的 | 病变发展多数阶段内皮层保持完整，只有最复杂的病变才失去内皮 | [Williams1995] | 高 |
| 暴露累积 | LDL 致病「因果且累积」 | [Ference2017] "both causal and cumulative over time" | 高 |

### 4.2 稳定斑块 vs 易损斑块

| 特征 | 易损（薄帽纤维粥样瘤 TCFA） | 较稳定 | 出处 / 可靠度 |
|---|---|---|---|
| 纤维帽厚度 | <65 µm（定义）；95% 破裂斑块帽厚 <65 µm；破裂处帽厚约 23 ± 19 µm（后者仅检索摘要） | 他汀治疗、LDL-C <1.3 mmol/L（50 mg/dL）患者的斑块帽厚可达 139.9 µm | [Borén2020] "95% of ruptured plaques have cap thickness <65 μm"；"thick fibrous caps (51.7% and 139.9 μm, respectively)"——高 |
| 坏死核心 | 相对较大 | 纤维钙化斑块：富胶原、大片钙化、炎症细胞少 | Virmani 改良 AHA 分类（检索摘要，Heart 2003 表未直读）——中 |
| 炎症细胞 | 帽内巨噬细胞、T 细胞浸润 | 少 | 同上——中 |
| 肉眼 / 血管镜颜色 | 黄色（尤其「闪亮黄」）；但并非所有黄斑块都易损 | 白色 | [Mizuno2017] "Yellow plaque has been considered to be vulnerable… all yellow plaques might not be vulnerable."——中 |

### 4.3 要多少年：青少年尸检

| 研究 | 发现 | 出处 / 原文 | 可靠度 |
|---|---|---|---|
| PDAY（美国，15–34 岁意外死亡者尸检；检索摘要示 JAMA 1999 样本 2876 例） | 「大多数美国青少年动脉系统某处已有脂纹」；35 岁以下约 10% 已有进展期病变；15–34 岁每 5 年组病变范围持续增加；主动脉含脂病变早在 15–20 岁组出现 | [PDAY1998] "most teenagers in the United States have fatty streaks in some part of their arterial system"；"10% of the young people under 35 in this study"；"The extent of lesions increased steadily from 15 to 34 years" | 高（大型尸检观察研究） |
| PDAY：与血脂关系 | 进展与总胆固醇、LDL-C 升高、HDL-C 低相关；吸烟、高血压分别使进展期冠脉病变约 6 倍、近 4 倍 | [PDAY1998] | 高（观察性关联） |
| Bogalusa（Berenson NEJM 1998，204 例 2–39 岁尸检） | 冠脉脂纹患病率：2–15 岁 50%，21–39 岁 85%；冠脉隆起纤维斑块：2–15 岁 8%，26–39 岁 69% | [AAFP-Bogalusa] "The prevalence of fatty streaks in the coronary arteries was 50 percent in persons from two to 15 years of age" | 中高（读的是 AAFP 二手摘要） |
| PESA（中年人影像） | 中年男性 71%、女性 43% 有亚临床动脉粥样硬化 | [Borén2020] | 高 |

**结论（已证实）**：病变从童年 / 青少年开始，经数十年累积；心梗多发生在中老年，是几十年暴露的结果。具体「从脂纹到破裂要多少年」个体差异极大，**没有统一年数**（尚不清楚，不要给一个数字）。

---

## 5. 尺度数据（比例尺）

| 对象 | 尺寸 | 出处 | 可靠度 |
|---|---|---|---|
| 胆固醇分子 | 未查到直接测量的长度；文献称其嵌在磷脂之间「约跨半个双层」，双层厚约 3.8–4.1 nm（模拟）→ 推算约 2 nm 量级 | 检索摘要（膜模拟研究） | 低（推算） |
| HDL | 5–12 nm | [Feingold] | 高 |
| LDL | 18–25 nm（Feingold）；17–28 nm；冷冻电镜小 LDL 16.2–22.4 nm，均值 19.3，约 17×20 nm | [Feingold]；[Berndsen2024] | 高 |
| ApoB100 腰带 | 约 58 nm 长 × 4 nm 宽 | [Berndsen2024] | 中高 |
| IDL | 25–35 nm | [Feingold] | 高 |
| Lp(a) | ~30 nm（随 apo(a) 大小变化） | [Feingold] | 高 |
| VLDL | 30–80 nm | [Feingold] | 高 |
| 能进动脉内膜的上限 | <70 nm | [Ference2017]；[Borén2020] | 高 |
| 乳糜微粒 | 75–1200 nm | [Feingold] | 高 |
| 血小板 | 1–3 µm（PubMed 收录的血涂片章节，检索摘要）；2–4 µm（HistoGuide） | 检索摘要；[HistoGuide] | 中 |
| 红细胞 | 7–8 µm（HistoGuide）；均值约 7.5 µm，双凹圆盘（血涂片章节，检索摘要）；厚 1.7–2.2 µm（检索摘要） | [HistoGuide] | 中高 |
| 单核细胞 | 12–20 µm | [HistoGuide] | 中 |
| 内皮细胞 | 约 50–70 µm 长、10–30 µm 宽、0.1–10 µm 厚（NCBI Bookshelf 章节，检索摘要）；人肝动脉内皮 SEM 测得约 21.9 × 4.9 µm，髂总动脉约 25.8 × 13.2 µm | 检索摘要 | 中低 |
| 易损斑块纤维帽 | <65 µm | [Borén2020] | 高 |
| 冠脉内径（Dodge 1992，*Circulation* 86:232） | 左主干约 4.5 ± 0.5 mm；LAD 近段约 3.7 ± 0.4 mm，远段约 1.9 ± 0.4 mm；RCA 近段约 2.8–3.9 mm（视优势型）；与年龄无关 | 检索摘要（原文 403） | 中 |
| 冠脉内膜厚度 | **未查到可靠数据**（一份泰国学位论文给出 >1 mm，明显不像正常值，未采用） | — | — |
| 冠脉血流速度 | 静息时导丝多普勒近段 LAD 平均峰值速度约 18–25 cm/s，充血时约 50–56 cm/s（小样本研究） | 检索摘要 | 中低 |

**换算成「缩小后」的直觉比例（本文计算，基于上表）**：设 LDL ≈ 22 nm 放大到 1 cm（放大约 45 万倍）：

| 对象 | 放大后 |
|---|---|
| 胆固醇分子（~2 nm，推算） | 约 1 mm |
| HDL（5–12 nm） | 2–5 mm |
| LDL | 1 cm（弹珠） |
| VLDL（30–80 nm） | 1.4–3.6 cm |
| 乳糜微粒（75–1200 nm） | 3.4–55 cm |
| 血小板（2–3 µm） | 约 1–1.4 m |
| 红细胞（7.5 µm） | 约 3.4 m（一辆小车长） |
| 内皮细胞长（20–70 µm） | 约 9–32 m |
| 易损斑块纤维帽（65 µm） | 约 30 m |
| LAD 近段内径（3.7 mm） | 约 1.7 km |
| 血流 20 cm/s | 每秒走过约 900 万个 LDL 直径——画面必须大幅放慢 |

一句话版本：**红细胞直径约是 LDL 的 300–400 倍**（7.5 µm ÷ 18–25 nm）。

---

## 6. 真实外观：哪些能「写实」，哪些只能示意

| 对象 | 真实可见到的样子 | 出处 | 画面处理 |
|---|---|---|---|
| LDL 颗粒 | 冷冻电镜灰度图：略扁的半盘状、带棱角，表面一条蛋白「腰带」，一端突出的 β-桶；部分颗粒核心有层状条纹（液晶态胆固醇酯） | [Berndsen2024] | 形状可写实；**颜色一定是示意**（电镜是灰度；纳米级颗粒远小于可见光波长，本身无「颜色」可言——后半句为物理常识，本次未另查来源） |
| 教科书脂蛋白示意图 | 橙色小球表层 + 黄色带状蛋白绕行 | [Feingold] 图 1（改自 *Biochemistry* 39:9763, 2000） | 是艺术示意，可参考但需标「示意」 |
| 血细胞 | 瑞氏染色血涂片：红细胞亮粉色、单核细胞胞质淡蓝 | [HistoGuide] | 粉色是**染料颜色**；活体血中红细胞整体呈红色（血红蛋白），但单个细胞在显微镜下颜色很淡（未查来源，常识） |
| 黄色斑块 | 冠脉血管镜下直接看到斑块颜色：白色 vs 黄色（1 浅黄 / 2 黄 / 3 深黄，检索摘要中的尸检评级）；黄色与薄纤维帽、脂质核心相关；颜色成因据检索摘要为与脂质结合的 β-胡萝卜素 | [Mizuno2017]（成因一句仅读到截断原文 "produces the yellow color of atherosclerotic plaque"） | **黄色是真实颜色**（血管镜所见），可写实；他汀等治疗可使黄色变淡 |
| 泡沫细胞 / 坏死核心 / 胆固醇结晶 | 病理切片所见；切片颜色取决于染色 | [Borén2020] 文字描述 | 病理切片颜色全是染料伪色（H&E、油红 O 等的具体颜色本次**未查到原文**：记忆中油红 O 把脂质染红、H&E 下泡沫细胞胞质呈空泡状，未证实）；动画里建议用「透明细胞里塞满黄色油滴」示意 |
| 跨内皮转运、蛋白聚糖「挂住」LDL、PCSK9 拖走受体 | 分子事件，无法直接拍到 | [Borén2020]；[Feingold] | 只能示意 |

---

## 给视频的建议

**最值得讲的点**
1. **油水不相溶 → 必须「装船」运输**：脂蛋白 = 外层亲水壳（磷脂 + 游离胆固醇 + 载脂蛋白）+ 内部油核（胆固醇酯 + 甘油三酯）。「LDL 不是胆固醇，是运胆固醇的船」——体检单上的 LDL-C 是「船上装的胆固醇总量」。
2. **一船一个 ApoB**：每个 LDL / VLDL / IDL / Lp(a) 恰好一个 ApoB-100，所以数 ApoB 就是数「能钻进血管壁的船」。冷冻电镜看到 ApoB 像一条腰带绕颗粒一圈——这是可以写实的超级好画面。
3. **数量感**：每微升血里约 7000 亿–1 万亿个 LDL；每个 LDL 装约 2000 个胆固醇分子；红细胞比它大 300–400 倍。
4. **病因主线是「滞留」**：<70 nm 的颗粒穿过完整内皮进入内膜 → 被蛋白聚糖「粘住」→ 氧化 / 聚集 → 巨噬细胞吞食变泡沫细胞 → 坏死核心 + 胆固醇结晶 → 薄纤维帽破裂 → 血栓。内皮多数时候是完整的，不是「血管被划破才进去」。
5. **从小就开始**：PDAY / Bogalusa 尸检里，青少年冠脉已普遍有脂纹，2–15 岁组冠脉脂纹患病率 50%。累积暴露的概念由此引出。
6. **身体自己造的多**：胆固醇平衡研究中，新进入体内的胆固醇约八成以上来自自身合成；肠道里的胆固醇大部分来自胆汁而非食物。

**最容易讲错的地方**
- 说「LDL 就是坏胆固醇分子」——错，LDL 是颗粒，胆固醇本身无好坏。
- 说「肝脏合成了 X% 的胆固醇」——人体数据本次未查到，避免给具体百分比。
- 说「血管被划伤，胆固醇粘在伤口上」——主流机制是完整内皮下的转胞吞 + 滞留。
- 把斑块画成「水管内壁的水垢」——斑块主要长在**血管壁里**（内膜内），向内鼓起，表面盖着纤维帽和内皮。
- 给出「从脂纹到心梗要 N 年」的统一数字——没有。
- 说「HDL 把坏胆固醇运走所以越高越好」——逆向转运机制存在，但 HDL 的因果作用有争议，交给负责「好与坏」的一期。
- 易损斑块不一定导致狭窄；稳定斑块也可能很窄——画面别把「堵得多」与「危险」画成同一件事（第一句为本次未直接核对的推论，以 Virmani 资料补核后再定稿）。

**可以怎么画**
- 比例尺：以「LDL = 弹珠（1 cm）」作为镜头内标尺，红细胞 ≈ 3–4 m 的软圆盘，冠脉内腔 ≈ 1.7 km 宽的隧道；镜头要分级切换尺度（血管 → 细胞 → 颗粒），并在屏上标尺度。
- LDL：略扁半盘状、表面凹凸、一条宽约 1/5 颗粒直径的蛋白带绕一圈、一端突出一块球状蛋白；不要画成光滑完美的球。颜色自定，但标「示意」。
- HDL 更小（一半或更小）、外面多条 ApoA-I；VLDL / 乳糜微粒更大、更「油」；Lp(a) = LDL 外挂一条长链蛋白。
- 斑块：内皮完整，下方黄色油核 + 白色纤维帽；易损斑块帽极薄（<65 µm，约 8–9 个红细胞直径），内含巨噬细胞；破裂后红色血栓。黄色可写实（血管镜所见）。
- 必须减速：真实血流在近段冠脉约每秒 20 cm，缩小视角下快得看不清，需标注「慢动作示意」。

**观众最可能的误解**
- 「血脂 = 血里漂着油滴」——实际是被蛋白包裹的纳米颗粒。
- 「吃进去的胆固醇直接变成血管里的斑块」——大部分胆固醇是自己造的，吸收率个体差异大（饮食话题交其他研究员）。
- 「年轻人不用管」——尸检显示病变从青少年起步。
- 「斑块是堆在血管内表面的」——实际在血管壁内。
