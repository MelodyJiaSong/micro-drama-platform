# t11 损失函数 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。原文均在 2026-11-09 取回原页面逐字核对（Llama 2、Kaplan 从 ar5iv HTML 全文检索；Google MLCC 从课程页面）。

## 1. 损失与均方误差（概念）
- 来源：Google Machine Learning Crash Course，Linear regression → Loss
  https://developers.google.com/machine-learning/crash-course/linear-regression/loss
- 原文：
  - "Loss is a numerical metric that describes how wrong a model's predictions are."
  - "The goal of training a model is to minimize the loss, reducing it to its lowest possible value."
  - 表格 Mean squared error (MSE)："The average of L2 losses across a set of N examples."
  - "Loss focuses on the distance between the values, not the direction." / "Thus, all methods for calculating loss remove the sign."
  - "When the difference between the prediction and label is large, squaring makes the loss even larger."
- 片中说法：「把一大堆误差汇成一个数，就是损失」「分越低越好」「训练就是把这个分压下去」「平方以后全是正数，谁也抵消不了谁；差得越多罚得越狠」「均方误差是最常见的一种损失函数」。
  - 「零分最好、一点不差」是对均方误差而言（所有误差为零时损失为零）；紧接着实验里讲清「最低点也不是零」，避免「目标是零分」的误解。
  - 不说「均方误差是唯一的损失函数」；说「最常见的一种」。

## 2. 大语言模型的损失 = 给「猜下一个词」打分（交叉熵）
- 来源：Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, Amodei. *Scaling Laws for Neural Language Models*. arXiv:2001.08361（OpenAI，2020）§2 Background and Methods。
  https://arxiv.org/abs/2001.08361
- 原文："We optimize the autoregressive log-likelihood (i.e. cross-entropy loss) averaged over a 1024-token context, which is also our principal performance metric."
- 片中说法：「它的任务是猜下一个词」「打分看的是，真正的下一个词它给了多大把握，把握越小罚得越多」「这种打分叫交叉熵」——只点名字，不讲公式（按 s1_bible）。
- 「九成把握几乎不罚、一成罚得多得多」：单个词的交叉熵罚分 = −ln(把握)，0.9 → 0.11，0.1 → 2.30（`scenes/data.py` 算出并断言），画面标注数字，口播不念。
- 例句「床前明月 __」（中文）/ "Twinkle, twinkle, little __"（英文）是我们举的例子，不是论文里的。

## 3. Llama 2 的训练损失曲线（AI 里的真实例子）
- 来源：Touvron et al. *Llama 2: Open Foundation and Fine-Tuned Chat Models*. arXiv:2307.09288（Meta，2023-07）。
  https://arxiv.org/abs/2307.09288
- 原文：
  - 图 5 图注："Figure 5: Training Loss for Llama 2 models. We compare the training loss of the Llama 2 family of models. We observe that after pretraining on 2T Tokens, the models still did not show any sign of saturation."
  - §2.1："We trained on 2 trillion tokens of data as this provides a good performance–cost trade-off, ..."
  - §1："We are releasing variants of Llama 2 with 7B, 13B, and 70B parameters."
- 片中说法：「二零二三年，Meta 训练大模型 Llama 2 时，把这个分画成了一条曲线，一路往下压」「模型读完了两万亿个词元」「分还在往下降，还没有到头的意思」（= did not show any sign of saturation）；「几百亿个旋钮」= 最大 700 亿参数。
  - 画面曲线是**示意形状**（`data.py` 的 curve，一路下降、越来越缓），标「示意」与出处，不冒充论文图 5 的数据，也不报具体损失数值。
  - 「词元大致就是字或词的碎片」：词元（token）第 2 季 2-2 才细讲，这里一句话带过。

## 4. 实验（程序算出，`scenes/data.py`）
- 数据：第 1 季共用十二趟打车（`_shared/s1_data.py`，真值起步 10、每公里 2.5，加正态波动 σ=1.6，**示意数据**）。
- 模型：车费 = 起步价 + 每公里 × 距离（两个旋钮）。损失 = 每趟（猜的 − 实际）平方后取平均（均方误差）。
- 三组拧法：
  - 第一组 起步 5、每公里 2：每趟都猜少；5 公里那趟 实际 23、猜 15、差 8、平方 64；得分 77.96（口播「七十八」）。
  - 第二组 起步 4、每公里 3.5：短途猜少（1.2 公里差 −6.1）、长途猜多（12.6 公里差 +8.3）；直接平均误差 −0.33（口播「负零点三」）；平方再平均 13.39（「十三点四」）。
  - 第三组 起步 10、每公里 2.5：得分 2.19。
- 地形图：起步价 0–20 × 每公里 1–4，161×121 格逐格算分；网格最低点与最小二乘解一致：起步 10.20、每公里 2.54、分数 1.97（= `s1_data.json` 的 best，t04 下山终点同一点）。
- 平方让大错更吃亏：同样一共差 8 元，四趟各差 2 → 罚 16，一趟差 8 → 罚 64。
- 最低点不是零：数据带随机波动，best_loss = 1.97 > 0。

## 5. 地形图画法（给 t04 梯度下降接着用）
- 横轴 = 起步价（元，0–20），纵轴 = 每公里（元，1–4）；颜色 = 分数，越高越深（琥珀 `--accent`），等高线取 2.5、5、10、20、40、80、160、320（大致每圈翻倍）。
- 最低点：绿色（`--d-good`）实心点白边；三组拧法：墨黑圆点＋编号①②③与分数。
- 网格数据在 `scenes/data.json` 的 `land`（`z` 按行 = 每公里、列 = 起步价展开），画法在 `scenes/web/_lib.js` 的 `makeLand()`。
