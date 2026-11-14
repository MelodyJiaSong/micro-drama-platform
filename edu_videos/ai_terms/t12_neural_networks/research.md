# t12 神经网络与深度学习 — 出处核对（2026-11-09）

每条事实写明出处、原文与我们怎么说；台账见 `claims.json`。原文都是下载论文 PDF / arXiv 页面后逐字核对的。

## 1. AlexNet（AI 里的主例子）
- 论文：A. Krizhevsky, I. Sutskever, G. E. Hinton. *ImageNet Classification with Deep Convolutional Neural Networks*. NIPS 2012（作者单位均为 University of Toronto）。核对用的 PDF：https://www.cs.toronto.edu/~kriz/imagenet_classification_with_deep_convolutional.pdf （与 NeurIPS 论文集版同文）。
- 摘要原文：
  - "The neural network, which has 60 million parameters and 650,000 neurons, consists of five convolutional layers, some of which are followed by max-pooling layers, and three fully-connected layers with a final 1000-way softmax."
  - "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes."
  - "We also entered a variant of this model in the ILSVRC-2012 competition and achieved a winning top-5 test error rate of 15.3%, compared to 26.2% achieved by the second-best entry."
- 深度的作用（§7 Discussion）："It is notable that our network's performance degrades if a single convolutional layer is removed. For example, removing any of the middle layers results in a loss of about 2% for the top-1 performance of the network. So the depth really is important for achieving our results."
  - 引言里也有："this depth seems to be important: we found that removing any convolutional layer (each of which contains no more than 1% of the model's parameters) resulted in inferior performance."
- 第一层学到什么（§6.1）："The network has learned a variety of frequency- and orientation-selective kernels, as well as various colored blobs."
- 训练成本（§1）："Our network takes between five and six days to train on two GTX 580 3GB GPUs."（片中不用）
- 片中说法：「{2012|二零一二}年，多伦多大学三位研究者训练的很深的网络，后来叫 AlexNet」「八层、六千万个旋钮、一百二十万张照片、一千类」「每张图猜五个答案，五个都不对才算错：错误率 15.3%，第二名 26.2%」「第一层自己学会了找各种方向的条纹和色块」「拿掉中间任何一层，成绩掉大约两个百分点；原话：深度真的很重要」。
  - 限定：15.3% 是参赛的「这个模型的一个变体」（7 个 CNN 平均，表 2）；单个 CNN 在验证集上 top-5 为 18.2%。口播只说「它」「他们的网络」，画面标「ILSVRC-2012 · top-5」。
  - 「AlexNet」这个名字论文里没有，是后来通行的叫法，所以说「后来大家叫它 AlexNet」。
  - 不说「深度学习从这里诞生」「第一个深度网络」。
  - 「六千万个旋钮」= 60 million parameters（全季统一：参数就是旋钮）。「八层」= 五个卷积层 + 三个全连接层。

## 2. 为什么叠深：同样多的单元，叠起来能拼出更多段
- G. Montúfar, R. Pascanu, K. Cho, Y. Bengio. *On the Number of Linear Regions of Deep Neural Networks*. NIPS 2014, arXiv:1402.1869。摘要原文："Deep networks are able to sequentially map portions of each layer's input-space to the same output. … The compositional structure of these functions enables them to re-use pieces of computation exponentially often in terms of the network's depth."
- M. Telgarsky. *Benefits of depth in neural networks*. COLT 2016, arXiv:1602.04485。摘要原文："there exist neural networks with Θ(k³) layers, Θ(1) nodes per layer, and Θ(1) distinct parameters which can not be approximated by networks with O(k) layers unless they are exponentially large"。其构造用的就是「帐篷」函数（每层两个 ReLU 单元，把 [0,1] 对折一次）反复复合，段数 2^k。
- 片中说法：用程序算的构造例子（`scenes/data.py` 第 3 部分）：每层两个单元 max(0, 2x) − max(0, 4x − 2) 把斜线对折一次；叠 1–5 层，段数 2、4、8、16、32。同样十个单元并排一层，每个单元只有一个折点，最多 11 段。限定：「能」「最多」，是特意构造的例子，不说「叠一层一定翻倍」。

## 3. 小单元（「小于零就当零」）
- 这是 ReLU（rectified linear unit）：max(0, w·x + b)。AlexNet 用的正是它，原文 §3.1："Following Nair and Hinton, we refer to neurons with this nonlinearity as Rectified Linear Units (ReLUs)."，并说它让训练快了好几倍。
- 片中说法：「每个小单元还是两个旋钮算一条直线，只多一条规矩：算出来小于零，就当成零」；不说它是唯一的一种。

## 4. 名字
- 神经网络的「神经元」叫法来自生物神经元的类比（McCulloch & Pitts 1943 起），但现代网络只是带旋钮的数学小单元。片中只说一句「名字来自神经元，但别当真」，不说「模仿人脑」（第 1 季统一说法，`_shared/s1_bible.md`）。

## 5. 实验（程序算出，`scenes/data.py`）
- 数据（示意）：同样五公里、一天里 48 趟（每半小时一趟，时刻略有前后）。白天价 = 第 1 季共用数据 `_shared/s1_data.py` 学出的两个旋钮（起步价 + 每公里）× 5 公里 ≈ 22.9 元；早高峰（8 点前后）、晚高峰（18 点前后）加价，23 点到 5 点深夜加价，再加一点随机波动。断言：白天均价与 22.9 相差 < 0.6；高峰均价 > 白天 1.3 倍；深夜 > 1.15 倍。
- 直线（两个旋钮：车费 = a + b × 时刻）：最小二乘最优 a = 27.4、b = −0.07，几乎是平的；损失（均方误差）11.5。网格搜一大片拧法都不比它好（断言）。高峰时段平均少算 3 元以上，白天平均多算 3 元以上（断言）。
- 网络：1 个输入（出发时刻，缩放到 −1…1）→ 第一层 12 个小单元（ReLU，每个 2 个旋钮）→ 第二层 1 个单元（12 个权重 + 1 个偏置）。共 37 个旋钮。梯度下降（带动量 0.9，学习率 0.05，全批 48 趟）拧 1 万步；损失 20.5 → 9.8 → 6.9 → 4.7 → 3.1 → 1.6 → 1.1 → 0.26（第 0、30、100、250、600、1500、4000、10000 步）。断言：损失 < 0.3、比直线小 30 倍以上、高峰与深夜预测平均误差 < 1 元；曲线 = 12 条折线之和 + 常数。
  - 坡度在程序里用反向传播算；片中不讲（留给 t13）。动量是梯度下降的常见加速做法，片中只说「还是上一期的下山办法」。
  - 12 个单元里有 1 个训练后整天输出为零（没用上），一天里的拐点有 10 个；片中只说「每个拐点都是某个小单元在拐弯」，不说「十二个拐点」。
- 叠深的构造例子见第 2 节。

## 6. 深度学习的定义
- Y. LeCun, Y. Bengio, G. Hinton. *Deep learning*. Nature 521, 436–444 (2015)，摘要原文（nature.com 页面核对）："Deep learning allows computational models that are composed of multiple processing layers to learn representations of data with multiple levels of abstraction."
- 片中说法：「这就是深度学习的那个『深』」「深 = 层数多」。
