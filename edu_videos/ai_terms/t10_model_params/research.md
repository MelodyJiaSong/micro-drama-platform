# t10 模型与参数 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。

## 1. GPT-3 的参数量（AI 里的主例子）
- 论文：Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, … Dario Amodei（OpenAI）. *Language Models are Few-Shot Learners*. arXiv:2005.14165，首次提交 2020-05-28；NeurIPS 2020。
  - https://arxiv.org/abs/2005.14165（2026-11-09 用 curl 取 export.arxiv.org 摘要页逐字核对；`citation_date` = 2020/05/28）
- 原文（摘要，逐字）："Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting."
- 片中说法：「{2020|二零二零}年，OpenAI 发布的 GPT-3，就有一千七百五十亿个参数」「也就是一千七百五十亿个旋钮」；画面写 175,000,000,000，出处「Brown 等 · 2020」。
  - 不说「最大的模型」（原文只说比之前任何非稀疏语言模型大 10 倍，且今天早已不是最大），不说训练数据量的具体数字（本期不需要）。
  - 「拿海量文字训练出来的」：原文称其为 autoregressive language model（语言模型，在大量文本上训练），口播只说「海量文字」，不给数字。
- 冷开场与 l39 的「上千亿参数」：中文新闻常用说法，以 GPT-3 的 1750 亿作为例子撑住；英文说 "over a hundred billion"。

## 2. 「一秒念一个，要念五千五百多年」
- 算式：175,000,000,000 秒 ÷（365.25 × 24 × 3600 秒/年）≈ 5545.4 年。`scenes/data.py` 断言 5500 < years < 5600。
- 片中说法：「五千五百多年」/ "over five and a half thousand years"；画面「≈ 5545 年」。

## 3. 模型文件主要存的是参数读数
- PyTorch 官方教程《Saving and Loading Models》（pytorch/tutorials 仓库 `beginner_source/saving_loading_models.py`，2026-11-09 取 raw 文件逐字核对）：
  "In PyTorch, the learnable parameters (i.e. weights and biases) of an torch.nn.Module model are contained in the model’s parameters (accessed with model.parameters()). A state_dict is simply a Python dictionary object that maps each layer to its parameter tensor."
  同段还说 state_dict 也会存 registered buffers（如 batchnorm 的 running_mean），所以口播说「主要存的就是这一大串旋钮读数」，不说「只有」。
- 片中说法：「训练完存下来的模型文件，里面主要存的就是这一大串旋钮读数」。

## 4. 实验（程序算出，示意数据）
- 数据：第 1 季共用 `edu_videos/ai_terms/_shared/s1_data.py` 的十二趟打车（距离 1.2–12.6 公里，车费 14.1–39.8 元；真值起步价 10、每公里 2.5 加随机波动），示意数据，画面标「示意」。本期不改共用文件，只在 `scenes/data.py` 读取。
- 模型：车费 = 起步价 + 每公里 × 公里数（两个参数）。
- 断言（`scenes/data.py`）：
  - 演示：起步价 10、每公里 2、5 公里 → 20。
  - 起步价 0、每公里 1：十二趟全部猜少（最大差 28.2 元）。
  - 起步价 10、每公里 1：十二趟全部猜少，最远一趟差得是最近一趟的三倍以上（近的差得少、远的差得多）。
  - 起步价 10、每公里 3.5：最远四趟全部猜多（最远一趟多 14.3 元）。
  - 最小二乘最佳：起步价 10.199 → 10.2、每公里 2.541 → 2.54；最长竖线 3.2 元，平均差 < 1.2 元，比前三种拧法的平均差都小一半以上。
  - 八公里（不在十二趟里）：10.2 + 2.54 × 8 = 30.52 → 30.5 元。
- 口播「十块二左右、两块五左右」「三十块五左右」都带「左右」；画面读数 10.2、2.54。
- 本期不讲怎么给「差多少」打总分（t11 损失函数），也不讲旋钮往哪边拧、怎么自动拧（t04 梯度下降）；演示里拧旋钮的路线（0,1 → 10,1 → 10,3.5 → 10.2,2.54）是为了讲清「拧到合适」手工挑的。

## 5. 与上一期的衔接
- t00 什么是 AI（`t00_what_is_ai/script.md` l11）：「它学出来的那套认法叫模型，来一张新图，模型就给出答案。」本期 l03 用一句话带过：「今天的 AI 是从例子里自己学出规律的，学出来的那套本事，就叫模型。」
