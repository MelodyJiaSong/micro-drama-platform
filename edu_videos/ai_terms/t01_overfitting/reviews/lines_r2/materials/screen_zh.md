# 屏幕文字（逐屏）

每句口播说完前一刻，屏幕上看得见的文字块：`[层级 字号px]` 文字（字数）。层级：eyebrow 小标签、display 大数字、h1 标题、h2 小标题、body 正文、caption 注释、chart 图表文字。截图是 1920×1080 的那一刻（字幕在成片里另外压在底部，截图里没有）。

## s0 开场（片头之前）
### l01（6.2s）
- 口播：一个模型，在手里的数据上几乎满分；可一换到新数据，就错得一塌糊涂。
- [div 16px] 手里的数据 / 几乎满分（9 字）
- [div 16px] 换到新数据 / 一塌糊涂（9 字）
- 合计（不含小标签、图表）：2 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s0_l01.png`
### l02（4.7s）
- 口播：这可能不是程序写错了，而是它犯了一种毛病，叫过拟合。
- [eyebrow 22px] 这种毛病叫（5 字）
- [h1 76px] 过拟合（3 字）
- 合计（不含小标签、图表）：1 块，3 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s0_l02.png`

## s1 本期内容（画面：目录卡）
### agenda（包装卡，整段 13.6s）
- 口播 l03：这期，我们先用一个小实验，亲眼看看过拟合长什么样。
- 口播 l04：再聊聊它在现实里闯过的祸，和怎么防。
- 口播 l05：不懂模型也没关系，用到的词，我都会先讲明白。
- 屏幕：01 · 过拟合是什么（7 字）
- 屏幕：02 · 打个比方（5 字）
- 屏幕：03 · 两条误差线（6 字）
- 屏幕：04 · 换个角度（5 字）
- 屏幕：05 · 现实里的祸（6 字）
- 屏幕：06 · 怎么发现，怎么防（8 字）
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_s1.png`

## c_problem（章节卡）
- 过拟合是什么
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_problem.png`

## s2 模型在学什么
### l09（7.9s）
- 口播：过拟合，就是模型把练习题贴得太紧，连碰巧的细节也学了进去，一做新题反而变差。
- [eyebrow 22px] 一句话定义（5 字）
- [display 132px] 过拟合（3 字）
- [h2 54px] 连碰巧的细节也学了进去（11 字）
- [h2 54px] 做新题反而变差（7 字）
- 合计（不含小标签、图表）：3 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s2_l09.png`
### l10（5.2s）
- 口播：就像把练习题背下来了，却没学会规律。我们用一个小实验来看看。
- [eyebrow 22px] 一句话定义（5 字）
- [display 132px] 过拟合（3 字）
- [h2 54px] 连碰巧的细节也学了进去（11 字）
- [h2 54px] 做新题反而变差（7 字）
- [h2 54px] ≈ 背下答案，没学会规律（9 字）
- 合计（不含小标签、图表）：4 块，30 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s2_l10.png`
### l11（5.0s）
- 口播：这十个点，是我们收集到的数据，叫训练数据，相当于练习题。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 模型在学什么（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s2_l11.png`
### l12（6.1s）
- 口播：它们大致沿着某个规律分布，但每个点都有一点随机的偏差，这叫噪声。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 模型在学什么（6 字）
- [caption 28px] 噪声：随机的偏差（7 字）
- [caption 28px] 背后的规律（5 字）
- 合计（不含小标签、图表）：3 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s2_l12.png`
### l13（5.5s）
- 口播：模型的任务，是从这些点里找出规律，好去预测没见过的新数据。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 模型在学什么（6 字）
- [eyebrow 22px] 模型的任务（5 字）
- [h2 54px] 找出规律 / → 预测新数据（9 字）
- 合计（不含小标签、图表）：2 块，15 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s2_l13.png`

## s3 三种学法
### l14（7.9s）
- 口播：第一种模型太简单，只会画直线。点离线越远，扣分越多；把扣分平均一下，就是误差。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [caption 28px] 误差（2 字）
- 合计（不含小标签、图表）：2 块，12 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s3_l14.png`
### l15（4.1s）
- 口播：直线连练习题的误差都压不下来，这叫欠拟合。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差 · 偏离² 的平均（9 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [caption 28px] 误差（2 字）
- 合计（不含小标签、图表）：3 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s3_l15.png`
### l16（5.6s）
- 口播：第二种，一条平缓的曲线。它没有穿过每一个点，但抓住了大的走势。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差 · 偏离² 的平均（9 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- 合计（不含小标签、图表）：3 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s3_l16.png`
### l17（7.8s）
- 口播：第三种，模型非常复杂，曲线拐来拐去，硬是穿过了每一个点。练习题上，它的误差是零。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差 · 偏离² 的平均（9 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- [div 16px] ③ 弯曲线 / 0.00（4 字）
- 合计（不含小标签、图表）：4 块，25 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s3_l17.png`
### l18（3.5s）
- 口播：先猜一下：换成新题，哪一种考得最好？
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 换成新题，谁考得最好？（9 字）
- [eyebrow 22px] 练习误差 · 偏离² 的平均（9 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- [div 16px] ③ 弯曲线 / 0.00（4 字）
- 合计（不含小标签、图表）：4 块，24 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s3_l18.png`

## s4 考试
### l19（5.0s）
- 口播：再拿六个新点，模型都没见过。这叫测试数据，相当于考试。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 换成新题：考试（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 / 0.53 / 0.54（4 字）
- [div 16px] ② 平缓曲线 / 0.05 / —（5 字）
- [div 16px] ③ 弯曲线 / 0.00 / —（4 字）
- [caption 28px] 考题（2 字）
- 合计（不含小标签、图表）：5 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s4_l19.png`
### l20（3.5s）
- 口播：第二种曲线，离新点都不远，考得最好。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 换成新题：考试（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 / 0.53 / 0.54（4 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 0.00 / —（4 字）
- 合计（不含小标签、图表）：4 块，20 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s4_l20.png`
### l21（7.6s）
- 口播：第三种曲线，在点和点之间乱拐，离有些新点很远。它的考试误差，是第二种的二十多倍。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] ③ 的考试误差：② 的 25 倍（8 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 / 0.53 / 0.54（4 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 0.00 / 1.80（5 字）
- 合计（不含小标签、图表）：4 块，23 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s4_l21.png`
### l22（7.5s）
- 口播：它连噪声也一起背了下来，可噪声是随机的，到了新题不会重演。这就是过拟合。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] ③ 的考试误差：② 的 25 倍（8 字）
- [caption 28px] 噪声不会重演（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 / 0.53 / 0.54（4 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 0.00 / 1.80（5 字）
- 合计（不含小标签、图表）：5 块，29 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s4_l22.png`
### l23（8.8s）
- 口播：欠拟合好发现：练习和考试都差。过拟合难察觉：练习成绩可能好极了，像这里，练习误差是零。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [h1 76px] 欠拟合：两项都差，好发现（10 字）
- [h1 76px] 过拟合：练习好看，难察觉（10 字）
- 合计（不含小标签、图表）：2 块，20 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s4_l23.png`

## c_analogy（章节卡）
- 打个比方
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_analogy.png`

## s5 打个比方
### l24（7.6s）
- 口播：有个学生，把练习册的答案全背了下来，连印错的几处也照背。练习册上，他次次满分。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [eyebrow 22px] 练习册（3 字）
- [display 132px] 100（1 字）
- [body 38px] 连印错的也照背（7 字）
- 合计（不含小标签、图表）：2 块，8 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l24.png`
### l25（3.6s）
- 口播：可一到考试，题目稍微换个样子，他就不会了。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [eyebrow 22px] 考试（2 字）
- [h1 76px] 题一变， / 就不会了（7 字）
- 合计（不含小标签、图表）：1 块，7 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l25.png`
### l26（11.0s）
- 口播：放回实验里看：练习册是训练数据，印错的答案是噪声，考试是测试数据。死记硬背的学生，就是那条穿过每个点的曲线。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [div 16px] 练习册 / → / 训练数据（7 字）
- [div 16px] 印错的答案 / → / 噪声（7 字）
- [div 16px] 考试 / → / 测试数据（6 字）
- [div 16px] 死记硬背 / → / 穿过每个点的曲线（12 字）
- 合计（不含小标签、图表）：4 块，32 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l26.png`
### l27（7.7s）
- 口播：这个比方也有局限：学生知道自己在背，模型不知道。它只是足够复杂，连每个点都能记住。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [eyebrow 22px] 类比的局限（5 字）
- [h1 76px] 学生知道自己在背（8 字）
- [h1 76px] 模型不知道（5 字）
- 合计（不含小标签、图表）：2 块，13 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l27.png`
### l28（7.1s）
- 口播：还有一个相近、但不一样的毛病。教小朋友认猫，给他看的照片里，猫全都趴在沙发上。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [eyebrow 22px] 相近，但不一样的毛病（9 字）
- [h1 76px] 猫，都在沙发上（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l28.png`
### l29（9.0s）
- 口播：他学会的，可能是：沙发上的，就是猫。换成沙发上的小狗，他说是猫；草地上的猫，他反倒不认了。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [h1 76px] 他可能学到：沙发 = 猫（8 字）
- [caption 28px] 见过的：全对（5 字）
- [h2 54px] “是猫！”（2 字）
- [h2 54px] “不是猫。”（3 字）
- 合计（不含小标签、图表）：4 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l29.png`
### l30（10.7s）
- 口播：学生死背了答案，小朋友只见过沙发上的猫，两人都把眼前的例子当成了规律。小朋友这种毛病，叫捷径学习，后面还会说到。
- [eyebrow 22px] 02 · 打个比方（5 字）
- [eyebrow 22px] 学生（2 字）
- [eyebrow 22px] 小朋友（3 字）
- [h1 76px] 死背答案（4 字）
- [h1 76px] 只见过沙发上的猫（8 字）
- [caption 28px] 过拟合（3 字）
- [caption 28px] 捷径学习（4 字）
- 合计（不含小标签、图表）：4 块，19 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s5_l30.png`

## c_experiment（章节卡）
- 两条误差线
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_experiment.png`

## s6 一张图看懂
### l31（8.2s）
- 口播：回到实验。我们换三百组随机的点，每组都试一遍从简单到复杂的模型，看两种误差通常怎么变。
- [eyebrow 22px] 03 · 两条误差线（6 字）
- [h1 76px] 模型越复杂，误差怎么变？（10 字）
- [span 120px] 300（1 字）
- [h2 54px] 组随机的点（5 字）
- [caption 28px] 曲线取中位数（6 字）
- [chart 28px] 1（1 字）
- [chart 28px] 2（1 字）
- [chart 28px] 3（1 字）
- [chart 28px] 4（1 字）
- [chart 28px] 5（1 字）
- [chart 28px] 6（1 字）
- [chart 28px] 7（1 字）
- [chart 28px] 8（1 字）
- [chart 28px] 9（1 字）
- [chart 28px] 模型复杂度（多项式次数）（10 字）
- 合计（不含小标签、图表）：4 块，22 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s6_l31.png`
### l32（4.6s）
- 口播：练习误差一路往下走：模型越复杂，练习题做得越好。
- [eyebrow 22px] 03 · 两条误差线（6 字）
- [h1 76px] 模型越复杂，误差怎么变？（10 字）
- [span 120px] 300（1 字）
- [h2 54px] 组随机的点（5 字）
- [caption 28px] 曲线取中位数（6 字）
- [chart 28px] 练习误差（4 字）
- [chart 28px] 1（1 字）
- [chart 28px] 2（1 字）
- [chart 28px] 3（1 字）
- [chart 28px] 4（1 字）
- [chart 28px] 5（1 字）
- [chart 28px] 6（1 字）
- [chart 28px] 7（1 字）
- [chart 28px] 8（1 字）
- [chart 28px] 9（1 字）
- [chart 28px] 模型复杂度（多项式次数）（10 字）
- 合计（不含小标签、图表）：4 块，22 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s6_l32.png`
### l33（5.6s）
- 口播：考试误差却先降后升。中等复杂的模型，预测新数据最准。
- [eyebrow 22px] 03 · 两条误差线（6 字）
- [h1 76px] 模型越复杂，误差怎么变？（10 字）
- [span 120px] 300（1 字）
- [chart 28px] 刚刚好（3 字）
- [h2 54px] 组随机的点（5 字）
- [caption 28px] 曲线取中位数（6 字）
- [chart 28px] 考试误差（4 字）
- [chart 28px] 练习误差（4 字）
- [chart 28px] 1（1 字）
- [chart 28px] 2（1 字）
- [chart 28px] 3（1 字）
- [chart 28px] 4（1 字）
- [chart 28px] 5（1 字）
- [chart 28px] 6（1 字）
- [chart 28px] 7（1 字）
- [chart 28px] 8（1 字）
- [chart 28px] 9（1 字）
- [chart 28px] 模型复杂度（多项式次数）（10 字）
- 合计（不含小标签、图表）：4 块，22 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s6_l33.png`
### l34（5.2s）
- 口播：所以，练习误差很低、考试误差却很高，就是过拟合的信号。
- [eyebrow 22px] 03 · 两条误差线（6 字）
- [h1 76px] 模型越复杂，误差怎么变？（10 字）
- [chart 28px] 刚刚好（3 字）
- [chart 28px] 过拟合（3 字）
- [eyebrow 22px] 过拟合的信号（6 字）
- [h2 54px] 练习误差低 / 考试误差高（10 字）
- [chart 28px] 考试误差（4 字）
- [chart 28px] 练习误差（4 字）
- [chart 28px] 1（1 字）
- [chart 28px] 2（1 字）
- [chart 28px] 3（1 字）
- [chart 28px] 4（1 字）
- [chart 28px] 5（1 字）
- [chart 28px] 6（1 字）
- [chart 28px] 7（1 字）
- [chart 28px] 8（1 字）
- [chart 28px] 9（1 字）
- [chart 28px] 模型复杂度（多项式次数）（10 字）
- 合计（不含小标签、图表）：2 块，20 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s6_l34.png`
### l35（10.0s）
- 口播：那模型越简单越好吗？也不是。太简单，两种误差都高，就是左边的欠拟合。要找的，是两种误差都低的那一段。
- [eyebrow 22px] 03 · 两条误差线（6 字）
- [h1 76px] 模型越复杂，误差怎么变？（10 字）
- [eyebrow 22px] 常见误解（4 字）
- [chart 28px] 欠拟合（3 字）
- [chart 28px] 刚刚好（3 字）
- [chart 28px] 过拟合（3 字）
- [h2 54px] 越简单越好？（5 字）
- [body 38px] 不：太简单，两种误差都高（10 字）
- [body 38px] 要找中间刚刚好的那段（10 字）
- [chart 28px] 考试误差（4 字）
- [chart 28px] 练习误差（4 字）
- [chart 28px] 1（1 字）
- [chart 28px] 2（1 字）
- [chart 28px] 3（1 字）
- [chart 28px] 4（1 字）
- [chart 28px] 5（1 字）
- [chart 28px] 6（1 字）
- [chart 28px] 7（1 字）
- [chart 28px] 8（1 字）
- [chart 28px] 9（1 字）
- [chart 28px] 模型复杂度（多项式次数）（10 字）
- 合计（不含小标签、图表）：4 块，35 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s6_l35.png`

## c_lens（章节卡）
- 换个角度
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_lens.png`

## s7 学习就是压缩
### l36（3.4s）
- 口播：换个角度想：学习，可以看成一种压缩。
- [eyebrow 22px] 04 · 换个角度（5 字）
- [display 132px] 学习 ≈ 压缩（4 字）
- 合计（不含小标签、图表）：1 块，4 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s7_l36.png`
### l37（5.4s）
- 口播：要原样记住这十个点，就得存下十个数字，也就是每个点的高度。
- [eyebrow 22px] 04 · 换个角度（5 字）
- [h1 76px] 记住十个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- 合计（不含小标签、图表）：2 块，17 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s7_l37.png`
### l38（5.7s）
- 口播：第二种曲线，只用四个数字，就能大致画出这些点，新点也估得准。
- [eyebrow 22px] 04 · 换个角度（5 字）
- [h1 76px] 记住十个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- [div 28px] ② 4 个数字：压缩了（7 字）
- 合计（不含小标签、图表）：3 块，24 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s7_l38.png`
### l39（9.6s）
- 口播：第三种曲线要十个数字，才能穿过全部十个点。十个数字记十个点，等于没压缩，连噪声也一起存了下来。
- [eyebrow 22px] 04 · 换个角度（5 字）
- [h1 76px] 记住十个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- [div 28px] ② 4 个数字：压缩了（7 字）
- [div 28px] ③ 10 个数字：没压缩（7 字）
- 合计（不含小标签、图表）：4 块，31 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s7_l39.png`
### l40（7.1s）
- 口播：好的压缩，要留住规律、少记噪声；可压过了头，像那条直线，连规律也丢了。
- [eyebrow 22px] 好的压缩（4 字）
- [h1 76px] 留住规律，少记噪声（8 字）
- [h2 54px] 压过头：连规律也丢了（9 字）
- 合计（不含小标签、图表）：2 块，17 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s7_l40.png`

## c_real（章节卡）
- 现实里的祸
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_real.png`

## s8 现实里的代价
### l41（3.0s）
- 口播：这类毛病，在现实里真的闯过祸。
- [eyebrow 22px] 05 · 现实里的祸（6 字）
- [h1 76px] 它真的闯过祸（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l41.png`
### l42（6.4s）
- 口播：谷歌流感趋势，曾用人们的搜索记录，估算去看病的人里，有多少是流感样症状。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- 合计（不含小标签、图表）：0 块，0 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l42.png`
### l43（5.9s）
- 口播：它最初从五千万个搜索词里，挑出跟一千多个历史数据点最贴合的那些。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 最初的版本（5 字）
- [div 16px] 5000 万 个搜索词（6 字）
- [div 16px] 1152 个数据点（5 字）
- [div 80px] ≫（0 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：4 块，15 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l43.png`
### l44（10.3s）
- 口播：可挑的词远比数据点多，总有一些，只是碰巧在冬天搜得多。研究者说，这是过拟合：它既在测流感，也在测冬天。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [quote 72px] “一部分在测流感， / 一部分在测冬天”（14 字）
- [body 38px] 研究者：这是过拟合（8 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：3 块，26 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l44.png`
### l45（6.8s）
- 口播：后来的版本还是不准：2011到2013年，108周里，有100周估高了。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 后来的版本 · 2011–2013（7 字）
- [span 160px] 100（1 字）
- [span 160px] / 108（1 字）
- [h2 54px] 周，流感估高了（6 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：4 块，12 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l45.png`
### l46（7.0s）
- 口播：医学影像里也有。一个看胸片诊断肺炎的模型，换到一家新医院，成绩就掉了下来。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 看胸片诊断肺炎（7 字）
- [h1 76px] 换到新医院，成绩下降（9 字）
- [div 22px] Zech 等 ·《PLOS Medicine》· 2018（5 字）
- 合计（不含小标签、图表）：2 块，14 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l46.png`
### l47（8.0s）
- 口播：研究者另训了一个模型，专门看胸片认医院：在两家医院的片子上，准确率超过百分之九十九点九。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 另训一个模型：看胸片认医院（12 字）
- [display 160px] 99.9%+（1 字）
- [span 96px] +（0 字）
- [h2 54px] 胸片里有医院的“指纹”（9 字）
- [div 22px] Zech 等 ·《PLOS Medicine》· 2018（5 字）
- 合计（不含小标签、图表）：4 块，15 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l47.png`
### l48（10.0s）
- 口播：而各家医院的片子里，标成肺炎的比例差得很远。所以肺炎模型的好成绩，很可能有一部分靠的是认医院，而不是认病。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 各医院标成肺炎的比例（10 字）
- [span 160px] 34%（1 字）
- [display 160px] 34% vs 1%（3 字）
- [span 96px] vs（1 字）
- [h2 54px] 好成绩，部分可能靠认医院（11 字）
- [div 22px] Zech 等 ·《PLOS Medicine》· 2018（5 字）
- 合计（不含小标签、图表）：5 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l48.png`
### l49（11.1s）
- 口播：还有个识别皮肤癌的系统。医生常在可疑的痣上画标记，它很可能把标记当成了线索：画了标记的良性痣，一半多被它判成了癌。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 医生常给可疑的痣画标记（11 字）
- [display 160px] 54%（1 字）
- [h2 54px] 画了标记的良性痣，被判成癌（12 字）
- [div 22px] Winkler 等 ·《JAMA Dermatology》· 2019（5 字）
- 合计（不含小标签、图表）：3 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l49.png`
### l50（11.2s）
- 口播：胸片和痣这两个例子，和认猫的小朋友一样，是捷径学习，过拟合的近亲。它们在熟悉的环境里也许考得不错，换个环境就可能失灵。
- [eyebrow 28px] 谷歌流感趋势（6 字）
- [eyebrow 28px] 胸片肺炎模型（6 字）
- [eyebrow 28px] 皮肤癌识别（5 字）
- [eyebrow 22px] 胸片和痣：捷径学习，过拟合的近亲（14 字）
- [h1 76px] 换个环境，就可能失灵（9 字）
- [body 38px] 学到的线索，只在手头数据里成立（14 字）
- 合计（不含小标签、图表）：2 块，23 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s8_l50.png`

## c_fix（章节卡）
- 怎么发现，怎么防
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_c_fix.png`

## s9 怎么防
### l51（4.1s）
- 口播：那该怎么发现和避免过拟合？常用的办法有三个。
- [eyebrow 22px] 06 · 怎么发现，怎么防（8 字）
- [h1 76px] 三个常用办法（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s9_l51.png`
### l52（9.3s）
- 口播：第一，再留出一份数据当模拟考，叫验证集：用它来挑模型、及早发现过拟合，真正的考试留到最后。
- [eyebrow 22px] 06 · 怎么发现，怎么防（8 字）
- [h1 76px] 三个常用办法（6 字）
- [eyebrow 22px] ① 验证集（3 字）
- [h2 44px] 留一份模拟考（6 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- [caption 28px] 验证集挑模型，测试集留到最后（13 字）
- 合计（不含小标签、图表）：3 块，25 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s9_l52.png`
### l53（7.2s）
- 口播：坦白一句：刚才为了演示，我们直接按考试成绩挑了模型；实际做项目，可不能这样。
- [eyebrow 22px] 06 · 怎么发现，怎么防（8 字）
- [h1 76px] 三个常用办法（6 字）
- [eyebrow 22px] ① 验证集（3 字）
- [h2 44px] 留一份模拟考（6 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- [caption 28px] 演示里按考试成绩挑了，实际别这样（15 字）
- 合计（不含小标签、图表）：3 块，27 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s9_l53.png`
### l54（6.0s）
- 口播：第二，收集更多、更多样的数据，噪声和巧合，就不容易被当成规律。
- [eyebrow 22px] 06 · 怎么发现，怎么防（8 字）
- [h1 76px] 三个常用办法（6 字）
- [eyebrow 22px] ① 验证集（3 字）
- [eyebrow 22px] ② 更多数据（4 字）
- [h2 44px] 留一份模拟考（6 字）
- [h2 44px] 更多、更多样的数据（8 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- 合计（不含小标签、图表）：3 块，20 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s9_l54.png`
### l55（9.1s）
- 口播：第三，给模型立规矩：对过于复杂的曲线加惩罚，让它别去追着噪声跑。这类方法叫正则化。
- [eyebrow 22px] 06 · 怎么发现，怎么防（8 字）
- [h1 76px] 三个常用办法（6 字）
- [eyebrow 22px] ① 验证集（3 字）
- [eyebrow 22px] ② 更多数据（4 字）
- [eyebrow 22px] ③ 正则化（3 字）
- [h2 44px] 留一份模拟考（6 字）
- [h2 44px] 更多、更多样的数据（8 字）
- [h2 44px] 惩罚太复杂的曲线（8 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- 合计（不含小标签、图表）：4 块，28 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/s9_l55.png`

## s10 片尾（画面：片尾卡）
### outro（包装卡，整段 15.0s）
- 口播 l56：如果只记一句：
- 口播 l57：过拟合，就像连印错的都背了下来。
- 口播 l58：还把它们当成了规律。
- 口播 l59：下回你觉得全懂了，换一道没见过的题试试。下一期，我们讲强化学习。
- 屏幕：过拟合，就像连印错的都背了下来， 还把它们当成了规律。（23 字）
- 屏幕：强化学习（4 字）
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/zh/card_s10.png`

