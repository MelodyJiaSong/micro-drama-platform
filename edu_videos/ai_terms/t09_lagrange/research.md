# t09 拉格朗日乘子 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。

## 1. 方法的出处与年代
- 来源：J.-L. Lagrange,《Mécanique analytique》（分析力学），Paris, 1788（Legendre 监印）。现代形式的乘子规则在本书中首次清楚写出；「乘子法」（Méthode des multiplicateurs）这个名称见于 1811 年版（Wanner, Woudschoten 2015 讲稿；Fraser《J. L. Lagrange's Early Contributions to the Principles and Methods of Mechanics》）。
  - https://en.wikipedia.org/wiki/Joseph-Louis_Lagrange
  - https://wsc.project.cwi.nl/woudschoten-conferences/2015-woudschoten-conference/Wanner1.pdf
- 片中说法：「两百多年前，数学家拉格朗日给过一个办法」。画面标 1788《分析力学》。不说「发明于某年」，不说他的国籍（生于都灵，后在柏林、巴黎）。

## 2. Safe RLHF（AI 里的主例子）
- 论文：Dai, Pan, Sun, Ji, Xu, Liu, Wang, Yang. *Safe RLHF: Safe Reinforcement Learning from Human Feedback*. arXiv:2310.12773（2023-10-19）；ICLR 2024 spotlight（https://iclr.cc/virtual/2024/poster/18540 ；代码 PKU-Alignment/safe-rlhf，北京大学）。
- 原文要点（摘要）：把有用（helpfulness）与无害（harmlessness）的人类偏好分开，分别训练奖励模型与代价模型；"maximizing the reward function while satisfying specified cost constraints"；"Leveraging the Lagrangian method to solve this constrained problem, Safe RLHF dynamically adjusts the balance between the two objectives during fine-tuning."
- λ 的更新（正文式 31）：ln λ_{k+1} = ln λ_k + α·λ_k·J_C(θ_k)，约束是 J_C(θ) ≤ 0。代价估计为正（超标）时 λ 变大，为负（守住）时 λ 变小；4.2.3 节说模型满足安全约束时用更小的拉格朗日乘子。被微调的是 Alpaca-7B（复现），三轮迭代得到 Beaver-v1～v3。
- 片中说法：「二零二三年，北京大学的一个团队提出 Safe RLHF」「一个打分模型管有用，一个管有害」「有用分减去 λ 乘有害分」「有害超标 λ 涨，守住了 λ 降」。画面上的 λ 曲线是**示意**，标注「示意」，不冒充论文 Figure 6(c) 的数据。
  - 严格说目标是「奖励 − λ × 代价」，代价已含底线（J_C ≤ 0 的形式），口播说「有害分」可以。

## 3. 正则化与约束（同一思路）
- Goodfellow, Bengio, Courville《Deep Learning》(2016) §7.2.2 *Norm Penalties as Constrained Optimization*：带系数 α 的范数惩罚，对应一个范数约束的广义拉格朗日函数，α 相当于 KKT 乘子。
- 片中说法：「正则化里『太复杂就扣分』扣多重，就是这样一个系数」——说「这样一个系数」，不说「正则化系数就是拉格朗日乘子本身」（固定的 α 只对应某个约束半径）。

## 4. 「别离原模型太远」
- Ouyang et al. 2022《Training language models to follow instructions with human feedback》（InstructGPT）：在 PPO 目标里对 SFT 模型加逐 token 的 KL 惩罚，系数 β，用来缓解奖励模型被过度优化。
- 片中说法：「训练聊天模型时，常常还要求它别跟原来的模型差太远，扣分的力度也是这样一个系数」——同样只说「这样一个系数」。

## 5. 实验（程序算出）
- `scenes/data.py`：山 f = 10 − |p − (2.4, 1.8)|²，围栏 |p| ≤ 1.5；在网格上数值求「高度 − λ × 离中心距离」的最高点。
- 断言：λ=0 → 山顶（离中心 3）；λ=1.5 → 圈外；λ=3 → 正好在围栏上，与有围栏时的最高点同一点，高度 7.75；λ=4 → 圈内。
- 自动调价 λ ← λ + (离中心距离 − 1.5)：0 → 1.5 → 2.25 → 2.63 → 2.81 → 2.91 → … → 3。
- 相切：最优点上坡度方向与围栏外法线夹角余弦 > 0.9999，坡度大小 = 3 = λ。
- 影子价格：半径 1.5 → 1.6，最高点 7.75 → 8.04，多 0.29 ≈ 3 × 0.1。
- 山顶在圈内（0.6, 0.45）时，调价收在 λ = 0。
