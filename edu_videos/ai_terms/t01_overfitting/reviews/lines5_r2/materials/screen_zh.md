# 屏幕文字（逐屏）

每句口播说完前一刻，屏幕上看得见的文字块：`[层级 字号px]` 文字（字数）。层级：eyebrow 小标签、display 大数字、h1 标题、h2 小标题、body 正文、caption 注释、chart 图表文字。截图是 1920×1080 的那一刻（字幕在成片里另外压在底部，截图里没有）。

## s0 开场（片头之前）
### l01（6.7s）
- 口播：有个模型，拿它学过的数据来考，几乎满分，可一换成新数据，就错得一塌糊涂。
- [div 16px] 学过的数据 / 几乎满分（9 字）
- [div 16px] 换到新数据 / 一塌糊涂（9 字）
- 合计（不含小标签、图表）：2 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s0_l01.png`
### l02（4.7s）
- 口播：这多半不是程序写错了，是模型犯了个毛病，叫过拟合。
- [eyebrow 22px] 这种毛病叫（5 字）
- [h1 76px] 过拟合（3 字）
- 合计（不含小标签、图表）：1 块，3 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s0_l02.png`

## c_problem（章节卡）
- 过拟合是什么
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_c_problem.png`

## s2 过拟合是什么
### l03（11.1s）
- 口播：过拟合说白了，就是模型把练习的数据学得太死了，连碰巧出现的细节都学了进去，结果一遇到新数据，反而变差了。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [eyebrow 22px] 定义（2 字）
- [display 132px] 过拟合（3 字）
- [h2 54px] 学进了碰巧的细节（8 字）
- [h2 54px] 新数据上反而变差（8 字）
- 合计（不含小标签、图表）：3 块，19 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s2_l03.png`
### l04（9.0s）
- 口播：打个比方，有个学生把练习册的答案全背了下来，连印错的那几处也照着背，所以练习册他回回满分。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [eyebrow 22px] 练习册（3 字）
- [display 132px] 100（1 字）
- [body 38px] 连印错的也照背（7 字）
- 合计（不含小标签、图表）：2 块，8 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s2_l04.png`
### l05（3.5s）
- 口播：可一到考试，题目稍微变一下，他就不会了。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [eyebrow 22px] 考试（2 字）
- [h1 76px] 题一变， / 就不会了（7 字）
- 合计（不含小标签、图表）：1 块，7 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s2_l05.png`
### l06（6.2s）
- 口播：这里的练习册，就是模型手里的数据，那几处印错的地方，就是数据里的噪声。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [div 16px] 练习册 / → / 训练数据（7 字）
- [div 16px] 印错的地方 / → / 噪声（7 字）
- 合计（不含小标签、图表）：2 块，14 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s2_l06.png`
### l07（4.5s）
- 口播：模型把噪声也当成规律记住了，这就是过拟合。
- [eyebrow 22px] 01 · 过拟合是什么（7 字）
- [div 16px] 练习册 / → / 训练数据（7 字）
- [div 16px] 印错的地方 / → / 噪声（7 字）
- [div 16px] 把噪声当规律记住 / → / 过拟合（11 字）
- 合计（不含小标签、图表）：3 块，25 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s2_l07.png`

## c_experiment（章节卡）
- 做个小实验
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_c_experiment.png`

## s3 三种学法
### l08（5.9s）
- 口播：你看，这里有十个点，是收集来的数据，叫训练数据，相当于练习题。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 十个点：训练数据（7 字）
- 合计（不含小标签、图表）：1 块，7 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l08.png`
### l09（6.8s）
- 口播：它们大致沿着一条规律走，但每个点都有点随机的偏差，这些偏差就是噪声。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 十个点：训练数据（7 字）
- [caption 28px] 噪声：随机的偏差（7 字）
- [caption 28px] 背后的规律（5 字）
- 合计（不含小标签、图表）：3 块，19 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l09.png`
### l10（5.0s）
- 口播：模型要做的，就是从这些点里找出规律，去预测没见过的新点。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 十个点：训练数据（7 字）
- [eyebrow 22px] 模型的任务（5 字）
- [h2 54px] 找出规律 / → 预测新点（8 字）
- 合计（不含小标签、图表）：2 块，15 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l10.png`
### l11（4.1s）
- 口播：我们试三种模型。第一种太简单，只会画直线。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- 合计（不含小标签、图表）：1 块，10 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l11.png`
### l12（4.2s）
- 口播：点离线越远，扣分越多，平均扣多少，就是误差。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [caption 28px] 误差（2 字）
- 合计（不含小标签、图表）：2 块，12 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l12.png`
### l13（4.8s）
- 口播：结果这条直线连练习题都做不好，这就叫欠拟合。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差（4 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [caption 28px] 误差（2 字）
- 合计（不含小标签、图表）：3 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l13.png`
### l14（4.7s）
- 口播：第二种是条平缓的曲线，没穿过每个点，但抓住了大走势。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差（4 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- 合计（不含小标签、图表）：3 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l14.png`
### l15（7.3s）
- 口播：第三种就复杂多了，曲线拐来拐去，硬是穿过了每一个点，所以它的练习误差是零。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 同一组练习题，三种模型（10 字）
- [eyebrow 22px] 练习误差（4 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- [div 16px] ③ 弯曲线 / 0.00（4 字）
- 合计（不含小标签、图表）：4 块，25 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l15.png`
### l16（4.5s）
- 口播：你先猜一下，换成新题，这三种里哪一种考得最好？
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 换成新题，谁考得最好？（9 字）
- [eyebrow 22px] 练习误差（4 字）
- [div 16px] ① 直线 / 0.53 / 欠拟合（6 字）
- [div 16px] ② 平缓曲线 / 0.05（5 字）
- [div 16px] ③ 弯曲线 / 0.00（4 字）
- 合计（不含小标签、图表）：4 块，24 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s3_l16.png`

## s4 考试
### l17（5.7s）
- 口播：我们再拿六个没见过的新点考考它们，这叫测试数据，就相当于考试。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 换成新题：考试（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 · 欠拟合 / 0.53 / 0.54（7 字）
- [div 16px] ② 平缓曲线 / 0.05 / —（5 字）
- [div 16px] ③ 弯曲线 / 过拟合 / 0.00 / —（7 字）
- 合计（不含小标签、图表）：4 块，25 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l17.png`
### l18（3.1s）
- 口播：第二种离这些新点都不远，考得最好。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 换成新题：考试（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 · 欠拟合 / 0.53 / 0.54（7 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 过拟合 / 0.00 / —（7 字）
- 合计（不含小标签、图表）：4 块，26 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l18.png`
### l19（4.7s）
- 口播：第三种呢，在点和点之间乱拐，离有些新点差得很远。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 换成新题：考试（6 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 · 欠拟合 / 0.53 / 0.54（7 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 过拟合 / 0.00 / 1.80（8 字）
- 合计（不含小标签、图表）：4 块，27 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l19.png`
### l20（3.0s）
- 口播：它的考试误差，是第二种的二十多倍。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] ③ 的考试误差：② 的 25 倍（8 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 · 欠拟合 / 0.53 / 0.54（7 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 过拟合 / 0.00 / 1.80（8 字）
- 合计（不含小标签、图表）：4 块，29 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l20.png`
### l21（8.8s）
- 口播：为什么会这样？因为它把噪声也背下来了。可噪声是随机的，到了新题里不会再来一遍，这就是过拟合。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 背下了噪声，可噪声不会重演（12 字）
- [eyebrow 22px] 练习 / 考试（4 字）
- [div 16px] ① 直线 · 欠拟合 / 0.53 / 0.54（7 字）
- [div 16px] ② 平缓曲线 / 0.05 / 0.07（6 字）
- [div 16px] ③ 弯曲线 / 过拟合 / 0.00 / 1.80（8 字）
- 合计（不含小标签、图表）：4 块，33 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l21.png`
### l22（4.1s）
- 口播：欠拟合其实挺好发现的，它练习和考试都差。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 欠拟合：两项都差，好发现（10 字）
- 合计（不含小标签、图表）：1 块，10 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l22.png`
### l23（6.6s）
- 口播：过拟合就难发现了，练习成绩可能好得出奇，像这里练习误差是零。
- [eyebrow 22px] 02 · 做个小实验（6 字）
- [h1 76px] 欠拟合：两项都差，好发现（10 字）
- [h1 76px] 过拟合：练习成绩好，难发现（11 字）
- 合计（不含小标签、图表）：2 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s4_l23.png`

## c_lens（章节卡）
- 把学习看成压缩
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_c_lens.png`

## s7 学习就是压缩
### l24（3.7s）
- 口播：咱们换个角度看，学习其实可以看成一种压缩。
- [display 132px] 学习 ≈ 压缩（4 字）
- 合计（不含小标签、图表）：1 块，4 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l24.png`
### l25（5.2s）
- 口播：想原样记住这十个点，就得存十个数字，也就是每个点的高度。
- [eyebrow 22px] 03 · 把学习看成压缩（8 字）
- [h1 76px] 记住 10 个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- 合计（不含小标签、图表）：2 块，17 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l25.png`
### l26（8.6s）
- 口播：第二种曲线呢，只要四个数字就能定下来，它大致贴着这些点走，新点也估得准，这就是把数据压缩了。
- [eyebrow 22px] 03 · 把学习看成压缩（8 字）
- [h1 76px] 记住 10 个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- [div 28px] ② 4 个数字：压缩了（7 字）
- 合计（不含小标签、图表）：3 块，24 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l26.png`
### l27（3.5s）
- 口播：第三种得用十个数字，才能穿过这十个点。
- [eyebrow 22px] 03 · 把学习看成压缩（8 字）
- [h1 76px] 记住 10 个点，要几个数字？（10 字）
- [div 28px] 原样记：10 个数字（7 字）
- [div 28px] ② 4 个数字：压缩了（7 字）
- [div 28px] ③ 10 个数字：没压缩（7 字）
- 合计（不含小标签、图表）：4 块，31 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l27.png`
### l28（5.7s）
- 口播：十个数字记十个点，等于根本没压缩，连噪声也一起存了下来。
- 屏幕同上一句
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l28.png`
### l29（8.4s）
- 口播：所以好的压缩，是把规律留下、把噪声扔掉。可要是压过了头，就像那条直线，连规律也给丢了。
- [eyebrow 22px] 03 · 把学习看成压缩（8 字）
- [eyebrow 22px] 好的压缩（4 字）
- [h1 76px] 留住规律，少记噪声（8 字）
- [h2 54px] 压过头：连规律也丢了（9 字）
- 合计（不含小标签、图表）：2 块，17 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s7_l29.png`

## c_real（章节卡）
- 一个真实的例子
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_c_real.png`

## s8 一个真实的例子
### l30（7.6s）
- 口播：说个真事儿：谷歌做过个项目，叫流感趋势，想靠搜索记录，估看病的人里有多少有流感症状。
- [eyebrow 22px] 04 · 一个真实的例子（8 字）
- [h1 76px] 谷歌流感趋势（6 字）
- [h2 54px] 用搜索记录估流感（8 字）
- 合计（不含小标签、图表）：2 块，14 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s8_l30.png`
### l31（5.5s）
- 口播：一开始，它拿一千多个流感数据点，去五千万个搜索词里挑走势最像的。
- [eyebrow 22px] 最初的版本（5 字）
- [div 16px] 5000万个搜索词（6 字）
- [div 54px] 远多于（3 字）
- [div 16px] 1152个数据点（5 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：4 块，18 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s8_l31.png`
### l32（6.5s）
- 口播：问题是，能挑的词比数据点多太多，难免挑中只是碰巧在冬天搜得多的词。
- [h1 76px] 碰巧在冬天搜得多的词（10 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：2 块，14 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s8_l32.png`
### l33（5.4s）
- 口播：研究者说这就是过拟合，它一部分在测流感，一部分在测冬天。
- [quote 72px] “一部分在测流感， / 一部分在测冬天”（14 字）
- [body 38px] 研究者：这是过拟合（8 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：3 块，26 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s8_l33.png`
### l34（7.6s）
- 口播：后来的版本也不准：从2011年到2013年，108周里，有100周它都估高了。
- [eyebrow 22px] 后来的版本 · 2011–2013（7 字）
- [display 160px] 100 / 108 周（3 字）
- [h2 54px] 流感估高了（5 字）
- [div 22px] Lazer 等 ·《Science》· 2014（4 字）
- 合计（不含小标签、图表）：3 块，12 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s8_l34.png`

## c_fix（章节卡）
- 怎么防过拟合
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_c_fix.png`

## s9 怎么防
### l35（4.9s）
- 口播：那过拟合怎么发现，又怎么防呢？常用的办法有三个。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l35.png`
### l36（5.2s）
- 口播：第一，再留出一份数据来当模拟考，这份数据叫验证集。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- [h2 44px] ① 验证集：模拟考（6 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- 合计（不含小标签、图表）：2 块，12 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l36.png`
### l37（5.3s）
- 口播：拿它来挑模型，也能早点发现过拟合，真正的考试留到最后再考。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- [h2 44px] ① 验证集：模拟考（6 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- [caption 28px] 用它挑模型，考试留到最后（11 字）
- 合计（不含小标签、图表）：3 块，23 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l37.png`
### l38（6.3s）
- 口播：说实话，刚才演示时，我们是直接按考试成绩挑的模型，真做项目可不能这么干。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- [h2 44px] ① 验证集：模拟考（6 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- [caption 28px] 演示时按考试成绩挑，实际别这样（14 字）
- 合计（不含小标签、图表）：3 块，26 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l38.png`
### l39（6.3s）
- 口播：第二，多收些数据，越多样越好，噪声和巧合就不容易被当成规律了。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- [h2 44px] ① 验证集：模拟考（6 字）
- [h2 44px] ② 多收数据，越多样越好（9 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- 合计（不含小标签、图表）：3 块，21 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l39.png`
### l40（7.7s）
- 口播：第三，给模型立点规矩，曲线太复杂就扣分，别让它追着噪声跑，这个办法叫正则化。
- [eyebrow 22px] 05 · 怎么防过拟合（7 字）
- [h1 76px] 三个常用办法（6 字）
- [h2 44px] ① 验证集：模拟考（6 字）
- [h2 44px] ② 多收数据，越多样越好（9 字）
- [h2 44px] ③ 正则化：太复杂就扣分（9 字）
- [chart 22px] 训练（2 字）
- [chart 22px] 验证（2 字）
- [chart 22px] 测试（2 字）
- 合计（不含小标签、图表）：4 块，30 字
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/s9_l40.png`

## s10 片尾（画面：片尾卡）
### outro（包装卡，整段 16.1s）
- 口播 l41：所以说，过拟合，就是连练习册上印错的地方都背了下来，还把它们当成了规律。
- 口播 l42：下回你觉得自己全懂了，就找道没见过的题试试。
- 口播 l43：下一期，我们来聊聊强化学习。
- 屏幕：连印错的都背下， 还当成规律（12 字）
- 屏幕：强化学习（4 字）
- 截图：`edu_videos/ai_terms/t01_overfitting/reviews/lines5_r2/materials/screen/zh/card_s10.png`

