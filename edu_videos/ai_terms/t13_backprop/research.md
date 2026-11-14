# t13 反向传播 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。

## 1. 1986 年《自然》论文（AI 里的主例子）
- 论文：D. E. Rumelhart, G. E. Hinton & R. J. Williams, *Learning representations by back-propagating errors*. Nature 323, 533–536（1986 年 10 月 9 日；DOI 10.1038/323533a0）。作者单位：加州大学圣迭戈分校认知科学研究所（Rumelhart、Williams）、卡内基梅隆大学计算机系（Hinton）。
  - 原文扫描：https://papers.baulab.info/papers/Rumelhart-1986.pdf （逐字核对，2026-11-09 下载）；出版社页 https://www.nature.com/articles/323533a0
- 原文（摘要第一句）："We describe a new learning procedure, back-propagation, for networks of neurone-like units. The procedure repeatedly adjusts the weights of the connections in the network so as to minimize a measure of the difference between the actual output vector of the net and the desired output vector."
- 原文（摘要，隐藏单元）："As a result of the weight adjustments, internal 'hidden' units which are not part of the input or output come to represent important features of the task domain, and the regularities in the task are captured by the interactions of these units. The ability to create useful new features distinguishes back-propagation from earlier, simpler methods such as the perceptron-convergence procedure."
- 原文（正文，两趟）："For a given case, the partial derivatives of the error with respect to each weight are computed in two passes. We have already described the forward pass in which the units in each layer have their states determined by the input they receive from units in lower layers … The backward pass which propagates derivatives from the top layer back to the bottom one is more complicated."
- 原文（正文，链式法则）："The backward pass starts by computing ∂E/∂y for each of the output units. … We can then apply the chain rule to compute ∂E/∂x_j" —— 片中不点链式法则的名字，用齿轮讲「倍数一路相乘」。
- 原文（结尾的自我限定）："The learning procedure, in its current form, is not a plausible model of learning in brains." —— 与本季「不说模仿人脑」一致。
- 片中说法：「一九八六年，Rumelhart、Hinton、Williams 在《自然》上发表论文，把这个办法讲清楚了」「每个连接的坡度分两趟算：先正着一趟，再从最上一层倒着传回来」「中间那些单元会自己学出有用的特征」。
- **限定语**：反向传播式的求导在 1986 年之前已有人提出。Wikipedia「Backpropagation」History 节（2026-11-09 取 wikitext 核对）原文："Modern backpropagation was first published by Seppo Linnainmaa as 'reverse mode of automatic differentiation' (1970) … In 1982, Paul Werbos applied backpropagation to MLPs in the way that has become standard."；同节还说 Rumelhart 约 1982 年独立推导出这个算法，"He did not cite previous work as he was unaware of them"；引言 "Backpropagation had multiple discoveries and partial discoveries, with a tangled history and terminology"。片中只说「类似的算法更早也有人提出过」，不说他们发明或最早提出；论文自称 "a new learning procedure"，我们不照搬这一说法。

## 2. PyTorch 的自动求导
- PyTorch 官方教程 *A Gentle Introduction to torch.autograd*（https://docs.pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html ，页面标 Last Updated: Oct 01, 2025；2026-11-09 下载核对）：
  - "torch.autograd is PyTorch's automatic differentiation engine that powers neural network training."
  - "Backward Propagation: In backprop, the NN adjusts its parameters proportionate to the error in its guess. It does this by traversing backwards from the output, collecting the derivatives of the error with respect to the parameters of the functions (gradients), and optimizing the parameters using gradient descent."
  - "Backward propagation is kicked off when we call .backward() on the error tensor. Autograd then calculates and stores the gradients for each model parameter in the parameter's .grad attribute."
  - "Training a NN happens in two steps: Forward Propagation … Backward Propagation …"
- 片中说法：「用 PyTorch 这类框架训练模型，写一行 loss.backward()，所有旋钮的坡度就都算好了。这叫自动求导，底下做的就是反向传播：从输出倒着往回走，一路收集每个旋钮的坡度」「训练每一步：正着猜一遍，倒着传一趟，再把每个旋钮拧一小步」。

## 3. 倒着那一趟的工夫（约是正着的两倍）
- 程序算：`scenes/data.py` 第 6 步数乘法次数——十层、每层 1024 个单元的全连接网络，倒着一趟要算两样（旋钮的坡度、往前一层传的错误），乘法次数约为正着一遍的 1.9 倍，合计 ≈ 2.9 遍正着的工夫（断言 2.8～3.0）。
- 文献：Kaplan et al. 2020, *Scaling Laws for Neural Language Models*（arXiv:2001.08361）§2.1，原文（ar5iv 全文核对）："Accounting for the backwards pass (approximately twice the compute as the forwards pass), we then define the estimated non-embedding compute as C ≈ 6N floating point operators per training token."
- 片中说法：「正着一遍、倒着一趟，加起来差不多三遍的工夫」——说「差不多」。

## 4. 实验（程序算出，示意数据）
- 数据：第一季共用打车数据 `_shared/s1_data.py`（示意）里 5 公里、实付 23 元的那一趟。
- 网络：两层、七个旋钮。第一层单元 A = 距离 × 1 + 1 = 6，B = 距离 × 0.4 + 2 = 4（负数归零，这一趟两个都为正）；第二层：猜 = A × 2 + B × 1 + 13 = 29。多猜 6 块。
- 错误分 = ½ ×（猜 − 实际）²；½ 只为让「坡度 = 传到这儿的错误 × 放大倍数」不多出个 2，与平方误差只差常数倍，往哪拧完全一样。
- 倒着走一趟：第二层三个旋钮 36、24、6（= 6 × 送进来的 6、4、1）；传回 A：6 × 2 = 12，传回 B：6 × 1 = 6；第一层 60、12、30、6（= 收到的 × 距离 5 或 × 1）。
- 挨个试拧（每个旋钮 +0.0001，从头重算）：数到 8 遍正着算（不拧 1 遍 + 7 个旋钮各 1 遍）；七个坡度与反向传播一致（差 < 0.01）。反向传播：1 遍正着 + 1 趟倒着。
- 按七个数拧一小步（步子 0.005）：猜 29 → 23.88。
- 中号网络（1-32-32-1，1153 个旋钮，十二趟车全用）：挨个试数到 1154 遍；反向传播 1 + 1；两边坡度一致（差 < 1e-4）。
- 十亿个旋钮：挨个试 1,000,000,001 遍；假设一遍一秒，约 31.7 年（只是一步）。
- 齿轮：×2、×3 → 一路乘起来 6。

## 6. 口播里的人名念法
- 中文口播按中文译名念「鲁梅尔哈特、辛顿和威廉姆斯」（第 2 轮台词审：三个英文姓连念打断中文节奏），字幕用中文译名（原名字幕一屏超 35 字），画面论文卡显示原名 Rumelhart、Hinton、Williams。第一作者仍是 Rumelhart。
