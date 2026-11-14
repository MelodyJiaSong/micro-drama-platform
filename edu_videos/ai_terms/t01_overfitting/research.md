# t01 过拟合 — 调研与出处

讲稿 v2「⑤ 现实」段（s7，l34–l39）的案例与屏幕上的数字都来自下列原文。2026-11-08 先由独立调研整理候选，再逐条打开原文核对数字与原话（下方「核对」）。

## 用到的三个案例

### 1. Google 流感趋势（明确称过拟合）
- 出处：Lazer D, Kennedy R, King G, Vespignani A. "The Parable of Google Flu: Traps in Big Data Analysis." *Science* 343(6176):1203–1205, 2014. https://doi.org/10.1126/science.1248506
- 核对（原文 PDF）：最初的做法是「find the best matches among 50 million search terms to fit 1152 data points」（从五千万个搜索词里挑最能贴合 1152 个数据点的）；作者说这是大数据在"overfitting the small number of cases"（这里的 cases 指数据点，不是病人少）；最初版本"part flu detector, part winter detector"（一部分在测流感，一部分在测冬天；不要译成「一半…一半」）。另有一句：从 2011 年 8 月 21 日到 2013 年 9 月 1 日，GFT 在 108 周中有 100 周报得过高。
- 措辞注意：过拟合说的是**最初版本**的构造方式；2011–2013 年估高是后来的版本，作者另列了"算法动态"（搜索引擎本身在变）等原因。讲稿写「后来的版本也没好多少」，没有把 100/108 全算在过拟合头上。

### 2. 胸片肺炎模型认医院（捷径学习）
- 出处：Zech JR, Badgeley MA, Liu M, Costa AB, Titano JJ, Oermann EK. "Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study." *PLOS Medicine* 15(11): e1002683, 2018. https://doi.org/10.1371/journal.pmed.1002683
- 核对（原文摘要、方法与结果）：用 NIH 与 Mount Sinai 数据联合训练的肺炎模型，内部 AUC 0.931，换到 Indiana University 的外部数据只有 0.815。**另训的一个**专门预测医院系统的 CNN（"We trained a CNN to predict hospital systems from radiographs"）能认出片子来自哪家：NIH 99.95%（22,050/22,062），Mount Sinai 99.98%（8,386/8,388）——说明胸片里带着医院的「指纹」，不是肺炎模型本身在报医院。
- 更正（2026-11-08 独立审稿抓到，已改讲稿与画面）：初稿把 99.9% 写成肺炎模型自己认医院，错。
- 措辞注意：这是研究，不是临床事故，所以说「成绩掉了下来」，不说「害了病人」。论文的说法是混杂（confounding），通称捷径学习（Geirhos 等，*Nature Machine Intelligence* 2020，https://doi.org/10.1038/s42256-020-00257-z）。

### 3. 黑色素瘤 AI 被手术标记笔迹误导（捷径学习 / 虚假关联）
- 出处：Winkler JK, Fink C, Toberer F, et al., Haenssle HA. "Association Between Surgical Skin Markings in Dermoscopic Images and Diagnostic Performance of a Deep Learning Convolutional Neural Network for Melanoma Recognition." *JAMA Dermatology* 155(10):1135–1141, 2019. https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808
- 核对（原文摘要）：共 130 个皮损（107 个良性痣、23 个黑色素瘤）。无标记时敏感度 95.7%、特异度 84.1%；有紫色标记笔迹时敏感度 100%、特异度降到 45.8%；把笔迹裁掉后特异度 97.2%。
- 屏幕数字：良性痣被误判的比例 = 1 − 特异度，即 15.9% → 54.2%，写作「16% → 54%」；讲稿说「一半多的良性痣」。

## 备选（这一期没用）
- **Epic 败血症模型**：Wong 等，*JAMA Internal Medicine* 2021（https://doi.org/10.1001/jamainternmed.2021.2626），外部验证 AUC 0.63，漏掉 67% 的病例。论文定性为外部验证不佳，不叫过拟合；Epic 有异议。适合讲「泛化」的那一期。
- **新冠影像 AI**：Roberts 等，*Nature Machine Intelligence* 2021（https://doi.org/10.1038/s42256-021-00307-0），纳入的 62 个研究没有一个可用于临床；原因是数据偏差与方法缺陷。
- **股票因子发表后失效**：McLean & Pontiff，*Journal of Finance* 2016（https://doi.org/10.1111/jofi.12365），97 个因子样本外收益低 26%。

## 不用
- **Zillow Offers（2021）**：没有可靠原始来源把亏损归因于过拟合，属于市场急变下的预测失败。
- **"尺子"皮肤科故事**：常被引用，但出处偏轶事，没有核实。
