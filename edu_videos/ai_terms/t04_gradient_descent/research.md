# t04 梯度下降 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。原文都是本期制作时下载原文核对的（Adam 论文 PDF、GPT-3 与 LLaMA 论文的 ar5iv 版、Bengio 2012 的 ar5iv 版）。

## 1. Adam（AI 里的主例子之一）
- 论文：Diederik P. Kingma, Jimmy Lei Ba. *Adam: A Method for Stochastic Optimization*. arXiv:1412.6980（v1 2014-12-22；本次核对 v9，2017-01-30）；ICLR 2015 会议论文。
- 原文（摘要）："We introduce Adam, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments."
- 原文（§1）："The method computes individual adaptive learning rates for different parameters from estimates of first and second moments of the gradients; the name Adam is derived from adaptive moment estimation."
- 片中说法：「二零一四年提出的 Adam，会根据每个旋钮之前的坡，单独定步子大小」。「之前的坡」对应「梯度的一阶、二阶矩估计」（对过去梯度的指数滑动平均）。不说「Adam 不需要学习率」（它仍有步长超参数 α）。

## 2. 随机梯度下降
- 同一篇 Adam 论文 §1："many objective functions are composed of a sum of subfunctions evaluated at different subsamples of data; in this case optimization can be made more efficient by taking gradient steps w.r.t. individual subfunctions, i.e. stochastic gradient descent (SGD) or ascent. SGD proved itself as an efficient and effective optimization method that was central in many machine learning success stories, such as recent advances in deep learning"；§2 "The stochasticity might come from the evaluation at random subsamples (minibatches) of datapoints"。
- 片中说法：「每步只随机抽一小批数据，估个大概的坡就走，这叫随机梯度下降」。画面用同一张打车费地形图，每步从十二趟里随机抽三趟算坡度（`scenes/data.py` 的 sgd），标「示意」。

## 3. GPT-3：参数量、每步的数据量、优化方法
- 论文：Brown et al. *Language Models are Few-Shot Learners*. arXiv:2005.14165（2020，OpenAI）。
- 表 2.1 GPT-3 175B 行：n_params 175.0B、批大小 3.2M（词元）、学习率 0.6 × 10⁻⁴；表注："All models were trained for a total of 300 billion tokens."
- 附录 B："To train all versions of GPT-3, we use Adam with β1 = 0.9, β2 = 0.95, and ϵ = 10^-8"；同节还写了批大小从 32k 词元线性增加到满批（前 4–12 B 词元）。
- 片中说法：「GPT-3 每步只看大约十万分之一的训练数据」（3.2M / 300B ≈ 1.07 × 10⁻⁵，满批时；刚开始批更小，所以不会更多）；「GPT-3 训练用的就是 Adam」；「GPT-3 那一千七百五十亿个旋钮」（与 t10 的说法一致）。
  - 画面出处行写「每批 320 万词元，共 3000 亿词元」；口播不提「词元」（第 2 季才讲）。

## 4. LLaMA 用 AdamW
- Touvron et al. *LLaMA: Open and Efficient Foundation Language Models*. arXiv:2302.13971（2023，Meta），§2.3 Optimizer："Our models are trained using the AdamW optimizer (Loshchilov and Hutter, 2017)"。
- 片中说法：「Meta 的 Llama 用它的改版」。AdamW 是把权重衰减从 Adam 的更新里拆出来的版本，说「改版」不说具体改了什么。

## 5. 学习率常常是最要紧的设定
- Bengio, Y. *Practical Recommendations for Gradient-Based Training of Deep Architectures*. arXiv:1206.5533（2012），§3.1.1 Hyper-Parameters of the Approximate Optimization，讲初始学习率："This is often the single most important hyper-parameter and one should always make sure that it has been tuned"。
- 片中说法：「学习率常常是训练时最要紧的一个设定」——保留「常常」。

## 6. 实验（程序算出，`scenes/data.py`）
- 数据：`_shared/s1_data.py` 十二趟打车（示意）；模型 车费 = 起步价 + 每公里 × 距离；分数 = 均方误差（与 t11 同一种打分、同一张地形图：起步价 0–20、每公里 1–4、同一组等高线与绿环最低点，2026-11-10 对齐 t11 的 makeLand；只有第 03 章三张小图纵轴放宽到 0–5，学习率太大时的来回跳才看得见）。
- 起点 = t11 第一组拧法（5, 2），77.96 分（说「七十八」）。
- 试拧 0.1：起步价 −1.69、每公里 −11.24；梯度 (−17.0, −117.4)。
- 学习率 0.005：78.0 → 25.3 → 12.4 → 9.2；第 1075 步到 2.0；1200 步 1.985，旋钮 (9.93, 2.57)。最低点 (10.20, 2.54)，1.97。
- 学习率 0.0005：1200 步 5.49，旋钮 (6.43, 3.01)。
- 学习率 0.021：78 → 96 → 118 → 145 → 180 → 224，第 5 步每公里 5.19，出了地图（0–5）；每一步都跳到谷底另一侧，离谷底越来越远。
- 随机梯度下降（每步抽 3 趟、学习率 0.005）：末百步平均 2.27，终点 (9.98, 2.50)。
- 这张图只有一个谷底（均方误差对两个旋钮是二次碗形），片中只说「打车费这张图」，不推广。
