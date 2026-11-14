# On-screen text (screen by screen)

For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here).

## s0 Cold open (before the title card)
### l01（6.7s）
- narration：A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.
- [div 110px] Nearly perfect（2 words）
- [div 54px] On your data（3 words）
- [div 110px] Falls apart（2 words）
- [div 54px] On new data（3 words）
- total（excl. eyebrow & chart）：4 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s0_l01.png`
### l02（4.5s）
- narration：It may not be a bug. It may be a problem called overfitting.
- [div 110px] Nearly perfect（2 words）
- [div 54px] On your data（3 words）
- [div 110px] Falls apart（2 words）
- [div 54px] On new data（3 words）
- [eyebrow 22px] THE PROBLEM IS CALLED（4 words）
- [h1 76px] Overfitting（1 words）
- total（excl. eyebrow & chart）：5 blocks，11 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s0_l02.png`

## s1 What's coming (on screen: agenda card)
### agenda（package card, whole segment 17.1s）
- narration l03: In this episode:
- narration l04: What the problem is.
- narration l05: Why memorizing answers fails.
- narration l06: A different way to think about learning.
- narration l07: Then, real-world failures, and how to avoid them.
- narration l08: No background needed. We'll explain models and training data as we go.
- screen：Problem · What the problem is（5 words）
- screen：Analogy · Why memorizing answers fails（5 words）
- screen：Lens · A different way to think about learning（8 words）
- screen：Real world · Real failures, and how to avoid them（9 words）
- screen：Prereqs: What a “model” is / Training vs. test data / How error is measured（13 words）
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_s1.png`

## c_problem（chapter card）
- What problem is this?
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_problem.png`

## s2 What a model learns
### l09（9.7s）
- narration：First, the idea. Overfitting is when a model fits its practice data so closely that it learns the flukes, too, and does worse on new data.
- [eyebrow 22px] IN ONE SENTENCE（3 words）
- [h1 76px] Overfitting: a model fits its practice data so closely that it learns the accidents too, and does worse on new data.（21 words）
- total（excl. eyebrow & chart）：1 blocks，21 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s2_l09.png`
### l10（6.2s）
- narration：Think of it as memorizing the practice problems without learning the pattern. Let's see it in a small experiment.
- [eyebrow 22px] IN ONE SENTENCE（3 words）
- [h1 76px] Overfitting: a model fits its practice data so closely that it learns the accidents too, and does worse on new data.（21 words）
- [h2 54px] memorizing the practice problems without learning the pattern（8 words）
- [caption 28px] Think of it as（4 words）
- total（excl. eyebrow & chart）：3 blocks，33 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s2_l10.png`
### l11（6.9s）
- narration：These ten points are the data we collected. This is called the training data. Think of it as practice problems.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] What a model learns（4 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s2_l11.png`
### l12（5.7s）
- narration：They follow a pattern, but each point is slightly off. Those random wobbles are called noise.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] What a model learns（4 words）
- [caption 28px] Noise: random wobble（3 words）
- [caption 28px] The hidden pattern（3 words）
- total（excl. eyebrow & chart）：3 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s2_l12.png`
### l13（6.0s）
- narration：The model's job is to find the pattern in these points, so it can predict new data it has never seen.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] What a model learns（4 words）
- [eyebrow 22px] THE MODEL'S JOB（3 words）
- [h2 54px] Find the pattern in these points, / to predict data it has never seen（13 words）
- total（excl. eyebrow & chart）：2 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s2_l13.png`

## s3 Three ways to learn
### l14（9.3s）
- narration：Model one is too simple. It only draws a straight line. How far each point sits above or below the line, squared and averaged, is the error.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] One set of practice problems, three models（7 words）
- [caption 28px] Error（1 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s3_l14.png`
### l15（5.1s）
- narration：The line can't even get the error down on the practice problems. That's underfitting.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] One set of practice problems, three models（7 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 64px] 0.53（1 words）
- [span 22px] practice error（2 words）
- [caption 28px] Error（1 words）
- total（excl. eyebrow & chart）：6 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s3_l15.png`
### l16（5.7s）
- narration：Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] One set of practice problems, three models（7 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 64px] 0.53（1 words）
- [span 22px] practice error（2 words）
- [div 28px] ② Gentle curve（2 words）
- [b 64px] 0.05（1 words）
- [span 22px] practice error（2 words）
- total（excl. eyebrow & chart）：8 blocks，18 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s3_l16.png`
### l17（8.0s）
- narration：Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] One set of practice problems, three models（7 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 64px] 0.53（1 words）
- [span 22px] practice error（2 words）
- [div 28px] ② Gentle curve（2 words）
- [b 64px] 0.05（1 words）
- [span 22px] practice error（2 words）
- [div 28px] ③ Wiggly curve（2 words）
- [b 64px] 0.00（1 words）
- [span 22px] practice error（2 words）
- total（excl. eyebrow & chart）：11 blocks，23 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s3_l17.png`
### l18（3.2s）
- narration：Quick guess: on new questions, which one does best?
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] Quick guess: on new questions, which does best?（8 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 64px] 0.53（1 words）
- [span 22px] practice error（2 words）
- [div 28px] ② Gentle curve（2 words）
- [b 64px] 0.05（1 words）
- [span 22px] practice error（2 words）
- [div 28px] ③ Wiggly curve（2 words）
- [b 64px] 0.00（1 words）
- [span 22px] practice error（2 words）
- total（excl. eyebrow & chart）：11 blocks，24 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s3_l18.png`

## s4 The exam
### l19（6.7s）
- narration：Here are six new points the models have never seen. This is the test data. Think of it as the exam.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] New questions: the exam（4 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 52px] 0.53（1 words）
- [b 52px] 0.54（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ② Gentle curve（2 words）
- [b 52px] 0.05（1 words）
- [b 52px] 0.00（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [caption 28px] Exam points（2 words）
- [div 28px] ③ Wiggly curve（2 words）
- [b 52px] 0.00（1 words）
- [b 52px] 0.00（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- total（excl. eyebrow & chart）：18 blocks，25 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s4_l19.png`
### l20（3.7s）
- narration：Model two stays close to the new points. It does best.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] New questions: the exam（4 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 52px] 0.53（1 words）
- [b 52px] 0.54（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ② Gentle curve（2 words）
- [div 22px] JUST RIGHT（2 words）
- [b 52px] 0.05（1 words）
- [b 52px] 0.07（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ③ Wiggly curve（2 words）
- [b 52px] 0.00（1 words）
- [b 52px] 0.00（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- total（excl. eyebrow & chart）：18 blocks，25 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s4_l20.png`
### l21（7.8s）
- narration：Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] New questions: the exam（4 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 52px] 0.53（1 words）
- [b 52px] 0.54（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ② Gentle curve（2 words）
- [div 22px] JUST RIGHT（2 words）
- [b 52px] 0.05（1 words）
- [b 52px] 0.07（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ③ Wiggly curve（2 words）
- [b 52px] 0.00（1 words）
- [b 52px] 1.80（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [body 38px] 25× model ②（2 words）
- total（excl. eyebrow & chart）：19 blocks，27 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s4_l21.png`
### l22（6.9s）
- narration：It memorized the noise, too. But noise is random, so it won't repeat on new questions. That's overfitting.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h1 76px] New questions: the exam（4 words）
- [caption 28px] Noise won't repeat on new questions（6 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [b 52px] 0.53（1 words）
- [b 52px] 0.54（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ② Gentle curve（2 words）
- [div 22px] JUST RIGHT（2 words）
- [b 52px] 0.05（1 words）
- [b 52px] 0.07（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ③ Wiggly curve（2 words）
- [div 22px] OVERFIT（1 words）
- [b 52px] 0.00（1 words）
- [b 52px] 1.80（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [body 38px] 25× model ②（2 words）
- total（excl. eyebrow & chart）：21 blocks，34 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s4_l22.png`
### l23（11.6s）
- narration：Underfitting is easy to spot: it's bad on both practice and exam. Overfitting is harder to catch: the practice score can look great. Here, practice error is zero.
- [eyebrow 22px] 01 · THE PROBLEM（3 words）
- [h2 54px] Underfit: bad on both — easy to spot（7 words）
- [div 28px] ① Straight line（2 words）
- [div 22px] UNDERFIT（1 words）
- [h2 54px] Overfit: zero practice error — looks great（6 words）
- [b 52px] 0.53（1 words）
- [b 52px] 0.54（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ② Gentle curve（2 words）
- [div 22px] JUST RIGHT（2 words）
- [b 52px] 0.05（1 words）
- [b 52px] 0.07（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [div 28px] ③ Wiggly curve（2 words）
- [div 22px] OVERFIT（1 words）
- [b 52px] 0.00（1 words）
- [b 52px] 1.80（1 words）
- [span 22px] practice（1 words）
- [span 22px] exam（1 words）
- [body 38px] 25× model ②（2 words）
- total（excl. eyebrow & chart）：21 blocks，37 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s4_l23.png`

## c_analogy（chapter card）
- An analogy
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_analogy.png`

## s5 An analogy
### l24（7.9s）
- narration：Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE WORKBOOK（2 words）
- [display 132px] 100（1 words）
- [body 38px] Every answer memorized, typos included（5 words）
- total（excl. eyebrow & chart）：2 blocks，6 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l24.png`
### l25（4.1s）
- narration：But on the exam, when a question changes even slightly, he's lost.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE EXAM（2 words）
- [h1 76px] Change a question slightly, / and he's lost（7 words）
- total（excl. eyebrow & chart）：1 blocks，7 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l25.png`
### l26（10.1s）
- narration：In our experiment, the workbook is the training data, the typos are noise, and the exam is new data. Forcing the curve through every point is like memorizing.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [div 54px] →（0 words）
- [span 54px] Training data（2 words）
- [h2 54px] The workbook（2 words）
- [div 54px] →（0 words）
- [h2 54px] The typos（2 words）
- [h2 54px] Noise（1 words）
- [div 54px] →（0 words）
- [h2 54px] The exam（2 words）
- [h2 54px] New data（2 words）
- [div 54px] →（0 words）
- [h2 54px] Memorizing（1 words）
- [h2 54px] A curve forced through every point（6 words）
- total（excl. eyebrow & chart）：12 blocks，18 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l26.png`
### l27（8.4s）
- narration：The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [div 54px] →（0 words）
- [span 54px] Training data（2 words）
- [h2 54px] The workbook（2 words）
- [div 54px] →（0 words）
- [h2 54px] The typos（2 words）
- [h2 54px] Noise（1 words）
- [div 54px] →（0 words）
- [h2 54px] The exam（2 words）
- [h2 54px] New data（2 words）
- [div 54px] →（0 words）
- [h2 54px] Memorizing（1 words）
- [h2 54px] A curve forced through every point（6 words）
- [caption 28px] Where the analogy breaks: the student knows he's memorizing. The model doesn't — it's simply powerful enough to remember every point.（20 words）
- total（excl. eyebrow & chart）：13 blocks，38 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l27.png`
### l28（8.9s）
- narration：Now a related, but different, problem. Say you're teaching a child to recognize cats, and in every photo the cat is lying on a sofa.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] A RELATED, BUT DIFFERENT, PROBLEM（5 words）
- [h1 76px] Every cat in the photos is on a sofa（9 words）
- total（excl. eyebrow & chart）：1 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l28.png`
### l29（9.9s）
- narration：What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [h1 76px] The rule the child learns: sofa = cat（7 words）
- [caption 28px] Photos he has seen: all right（6 words）
- [h2 54px] “Cat!”（1 words）
- [h2 54px] “Not a cat.”（3 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l29.png`
### l30（11.2s）
- narration：Both kids treated the examples in front of them as the rule. The student remembered too much. The child saw too narrow a slice. That second kind is called shortcut learning, and we'll meet it again.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE STUDENT（2 words）
- [eyebrow 22px] THE CHILD（2 words）
- [h1 76px] Remembered too much（3 words）
- [h1 76px] Saw too narrow a slice（5 words）
- [caption 28px] Overfitting（1 words）
- [caption 28px] Shortcut learning (we'll meet it again)（6 words）
- total（excl. eyebrow & chart）：4 blocks，15 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s5_l30.png`

## c_experiment（chapter card）
- Let's run an experiment
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_experiment.png`

## s6 One chart
### l31（8.9s）
- narration：Back to the experiment. We draw 300 random sets of points, fit models from simple to complex on each, and look at the typical errors.
- [eyebrow 22px] 03 · THE EXPERIMENT（3 words）
- [h1 76px] As models get more complex, what happens to the errors（10 words）
- [eyebrow 22px] RANDOM REDRAWS（2 words）
- [span 120px] 300（1 words）
- [caption 28px] sets of points, each fit from degree 1 to 9; we take the median（14 words）
- [chart 28px] 1（1 words）
- [chart 28px] 2（1 words）
- [chart 28px] 3（1 words）
- [chart 28px] 4（1 words）
- [chart 28px] 5（1 words）
- [chart 28px] 6（1 words）
- [chart 28px] 7（1 words）
- [chart 28px] 8（1 words）
- [chart 28px] 9（1 words）
- [chart 28px] Model complexity (polynomial degree)（4 words）
- total（excl. eyebrow & chart）：3 blocks，25 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s6_l31.png`
### l32（6.1s）
- narration：Practice error keeps falling. The more complex the model, the better it does on the practice problems.
- [eyebrow 22px] 03 · THE EXPERIMENT（3 words）
- [h1 76px] As models get more complex, what happens to the errors（10 words）
- [eyebrow 22px] RANDOM REDRAWS（2 words）
- [span 120px] 300（1 words）
- [caption 28px] sets of points, each fit from degree 1 to 9; we take the median（14 words）
- [chart 28px] Practice error（2 words）
- [chart 28px] 1（1 words）
- [chart 28px] 2（1 words）
- [chart 28px] 3（1 words）
- [chart 28px] 4（1 words）
- [chart 28px] 5（1 words）
- [chart 28px] 6（1 words）
- [chart 28px] 7（1 words）
- [chart 28px] 8（1 words）
- [chart 28px] 9（1 words）
- [chart 28px] Model complexity (polynomial degree)（4 words）
- total（excl. eyebrow & chart）：3 blocks，25 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s6_l32.png`
### l33（6.0s）
- narration：But exam error falls, then rises. Moderately complex models do best on new data.
- [eyebrow 22px] 03 · THE EXPERIMENT（3 words）
- [h1 76px] As models get more complex, what happens to the errors（10 words）
- [eyebrow 22px] RANDOM REDRAWS（2 words）
- [chart 28px] Just right（2 words）
- [span 120px] 300（1 words）
- [caption 28px] sets of points, each fit from degree 1 to 9; we take the median（14 words）
- [chart 28px] Exam error（2 words）
- [chart 28px] Practice error（2 words）
- [chart 28px] 1（1 words）
- [chart 28px] 2（1 words）
- [chart 28px] 3（1 words）
- [chart 28px] 4（1 words）
- [chart 28px] 5（1 words）
- [chart 28px] 6（1 words）
- [chart 28px] 7（1 words）
- [chart 28px] 8（1 words）
- [chart 28px] 9（1 words）
- [chart 28px] Model complexity (polynomial degree)（4 words）
- total（excl. eyebrow & chart）：3 blocks，25 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s6_l33.png`
### l34（4.9s）
- narration：So low practice error with high exam error is the telltale sign of overfitting.
- [eyebrow 22px] 03 · THE EXPERIMENT（3 words）
- [h1 76px] As models get more complex, what happens to the errors（10 words）
- [chart 28px] Just right（2 words）
- [chart 28px] Overfit（1 words）
- [eyebrow 22px] THE TELLTALE SIGN（3 words）
- [chart 28px] Exam error（2 words）
- [h2 54px] Practice error low, / exam error high（6 words）
- [chart 28px] Practice error（2 words）
- [chart 28px] 1（1 words）
- [chart 28px] 2（1 words）
- [chart 28px] 3（1 words）
- [chart 28px] 4（1 words）
- [chart 28px] 5（1 words）
- [chart 28px] 6（1 words）
- [chart 28px] 7（1 words）
- [chart 28px] 8（1 words）
- [chart 28px] 9（1 words）
- [chart 28px] Model complexity (polynomial degree)（4 words）
- total（excl. eyebrow & chart）：2 blocks，16 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s6_l34.png`
### l35（10.2s）
- narration：So is simpler always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the range where both errors are low.
- [eyebrow 22px] 03 · THE EXPERIMENT（3 words）
- [h1 76px] As models get more complex, what happens to the errors（10 words）
- [eyebrow 22px] A COMMON MYTH（3 words）
- [chart 28px] Underfit（1 words）
- [chart 28px] Just right（2 words）
- [chart 28px] Overfit（1 words）
- [h2 54px] Simpler is always better?（4 words）
- [body 38px] No. Too simple, and both errors are high: underfitting. / Look for the sweet spot in the middle.（17 words）
- [chart 28px] Exam error（2 words）
- [chart 28px] Practice error（2 words）
- [chart 28px] 1（1 words）
- [chart 28px] 2（1 words）
- [chart 28px] 3（1 words）
- [chart 28px] 4（1 words）
- [chart 28px] 5（1 words）
- [chart 28px] 6（1 words）
- [chart 28px] 7（1 words）
- [chart 28px] 8（1 words）
- [chart 28px] 9（1 words）
- [chart 28px] Model complexity (polynomial degree)（4 words）
- total（excl. eyebrow & chart）：3 blocks，31 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s6_l35.png`

## c_lens（chapter card）
- A different lens
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_lens.png`

## s7 Learning is compression
### l36（4.2s）
- narration：Here's another way to see it. Learning can be seen as a kind of compression.
- [eyebrow 22px] 04 · A DIFFERENT LENS（4 words）
- [display 132px] Learning ≈ compression（2 words）
- total（excl. eyebrow & chart）：1 blocks，2 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s7_l36.png`
### l37（3.8s）
- narration：To remember these ten points exactly, you have to store ten heights.
- [eyebrow 22px] 04 · A DIFFERENT LENS（4 words）
- [h1 76px] How many numbers to remember ten points?（7 words）
- [div 28px] Store exactly: 10 heights（4 words）
- [span 24px] +0.11（1 words）
- [span 24px] -0.49（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -0.39（1 words）
- [span 24px] +0.90（1 words）
- [span 24px] +1.01（1 words）
- [span 24px] +1.45（1 words）
- [span 24px] +1.05（1 words）
- [span 24px] -0.06（1 words）
- total（excl. eyebrow & chart）：12 blocks，21 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s7_l37.png`
### l38（6.6s）
- narration：Model two is set by just four adjustable numbers. It roughly describes the points, and it stays close on new ones.
- [eyebrow 22px] 04 · A DIFFERENT LENS（4 words）
- [h1 76px] How many numbers to remember ten points?（7 words）
- [div 28px] Store exactly: 10 heights（4 words）
- [span 24px] +0.11（1 words）
- [span 24px] -0.49（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -0.39（1 words）
- [span 24px] +0.90（1 words）
- [span 24px] +1.01（1 words）
- [span 24px] +1.45（1 words）
- [span 24px] +1.05（1 words）
- [span 24px] -0.06（1 words）
- [div 28px] ② Gentle curve: 4 numbers（4 words）
- [span 24px] -0.16（1 words）
- [span 24px] +0.004（1 words）
- [span 24px] +1.23（1 words）
- [span 24px] +0.11（1 words）
- [div 22px] Compressed: stays close on new points（6 words）
- total（excl. eyebrow & chart）：18 blocks，35 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s7_l38.png`
### l39（9.1s）
- narration：Model three uses ten numbers, enough for its curve to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise, too.
- [eyebrow 22px] 04 · A DIFFERENT LENS（4 words）
- [h1 76px] How many numbers to remember ten points?（7 words）
- [div 28px] Store exactly: 10 heights（4 words）
- [span 24px] +0.11（1 words）
- [span 24px] -0.49（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -1.16（1 words）
- [span 24px] -0.39（1 words）
- [span 24px] +0.90（1 words）
- [span 24px] +1.01（1 words）
- [span 24px] +1.45（1 words）
- [span 24px] +1.05（1 words）
- [span 24px] -0.06（1 words）
- [div 28px] ② Gentle curve: 4 numbers（4 words）
- [span 24px] -0.16（1 words）
- [span 24px] +0.004（1 words）
- [span 24px] +1.23（1 words）
- [span 24px] +0.11（1 words）
- [div 22px] Compressed: stays close on new points（6 words）
- [div 28px] ③ Wiggly curve: 10 numbers（4 words）
- [span 24px] +0.01（1 words）
- [span 24px] +0.01（1 words）
- [span 24px] -0.20（1 words）
- [span 24px] -0.11（1 words）
- [span 24px] +1.01（1 words）
- [span 24px] +0.56（1 words）
- [span 24px] -2.08（1 words）
- [span 24px] -0.87（1 words）
- [span 24px] +2.34（1 words）
- [span 24px] +0.30（1 words）
- [div 22px] 10 → 10: no compression, the noise is stored too（9 words）
- total（excl. eyebrow & chart）：30 blocks，58 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s7_l39.png`
### l40（6.6s）
- narration：Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern, too.
- total（excl. eyebrow & chart）：0 blocks，0 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s7_l40.png`

## c_real（chapter card）
- The real-world cost
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_real.png`

## s8 The real-world cost
### l41（2.7s）
- narration：Problems like this have caused real trouble.
- [h1 76px] Problems like this have caused real trouble（7 words）
- total（excl. eyebrow & chart）：1 blocks，7 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l41.png`
### l42（5.4s）
- narration：Google once used people's searches to estimate the share of doctor visits for flu-like illness.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- total（excl. eyebrow & chart）：3 blocks，8 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l42.png`
### l43（6.4s）
- narration：Researchers pointed out that its first version tested 50 million search terms for the best fit to about 1,100 data points.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [eyebrow 22px] ESTIMATING FLU-LIKE DOCTOR VISITS FROM SEARCHES（6 words）
- [n 120px] 50M（1 words）
- [n 120px] 1152（1 words）
- [div 80px] →（0 words）
- [u 54px] search terms（2 words）
- [u 54px] data points（2 words）
- [caption 28px] (the first version)（3 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：10 blocks，22 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l43.png`
### l44（10.4s）
- narration：With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [quote 72px] “Part flu detector, / part winter detector”（6 words）
- [body 38px] The researchers called it overfitting（5 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：6 blocks，24 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l44.png`
### l45（8.7s）
- narration：Later versions still had problems. From 2011 to 2013, it overestimated flu in 100 out of 108 weeks.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [span 160px] 100（1 words）
- [span 160px] / 108（1 words）
- [h2 54px] weeks of flu overestimates (2011–2013, later versions)（7 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：7 blocks，22 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l45.png`
### l46（6.5s）
- narration：Medical imaging has examples too. A model that detected pneumonia in chest X-rays did worse at a new hospital.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [eyebrow 22px] DETECTING PNEUMONIA IN CHEST X-RAYS（5 words）
- [h1 76px] At a new hospital, performance dropped（6 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：5 blocks，20 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l46.png`
### l47（10.6s）
- narration：Researchers found the X-rays carried a hospital fingerprint: a separate model could identify which hospital scans from two of the hospitals came from, with over 99.9 percent accuracy.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [display 160px] 99.9%+（1 words）
- [span 96px] +（0 words）
- [h2 54px] A separate model identified the hospital for scans from two hospitals — a hospital fingerprint（14 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：7 blocks，29 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l47.png`
### l48（9.8s）
- narration：And the share of scans labeled pneumonia differed widely between hospitals. So part of the pneumonia model's success likely came from recognizing hospitals, not disease.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [display 160px] 99.9%+（1 words）
- [span 96px] +（0 words）
- [h2 54px] A separate model identified the hospital for scans from two hospitals — a hospital fingerprint（14 words）
- [body 38px] Scans labeled pneumonia, by hospital: 34% vs 1% / Part of the pneumonia model's success likely came from recognizing hospitals, not disease（21 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：8 blocks，50 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l48.png`
### l49（13.9s）
- narration：And a melanoma detector, an AI that spots skin cancer: doctors often draw ink marks around suspicious moles, and it likely learned the marks as a clue. In one study, it flagged over half of the marked harmless moles as cancer.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [eyebrow 22px] DOCTORS OFTEN MARK SUSPICIOUS MOLES（5 words）
- [span 160px] →（0 words）
- [display 160px] 16% → 54%（2 words）
- [h2 54px] of marked harmless moles flagged as cancer, in one study（10 words）
- [div 22px] Winkler et al. · JAMA Dermatology · 2019（6 words）
- total（excl. eyebrow & chart）：7 blocks，26 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l49.png`
### l50（11.9s）
- narration：Those last two models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They may score well on similar new data, and still fail when the setting changes.
- [tab 28px] Google Flu Trends（3 words）
- [tab 28px] Pneumonia X-ray model（3 words）
- [tab 28px] Melanoma detector（2 words）
- [eyebrow 22px] THE LAST TWO: SHORTCUT LEARNING, A COUSIN OF OVERFITTING（9 words）
- [h1 76px] They may score well on similar new data, and still fail when the setting changes（15 words）
- [body 38px] Like the child and the cats: they learned a clue that only holds in the data at hand（18 words）
- total（excl. eyebrow & chart）：5 blocks，41 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s8_l50.png`

## c_fix（chapter card）
- How to spot and prevent it
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_c_fix.png`

## s9 How to prevent it
### l51（4.0s）
- narration：So how do you spot and prevent overfitting? Three common ways.
- [eyebrow 22px] 05 · HOW TO PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s9_l51.png`
### l52（10.3s）
- narration：One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- [eyebrow 22px] 05 · HOW TO PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [h2 46px] Keep a mock exam（4 words）
- [div 22px] Train（1 words）
- [div 22px] Valid.（1 words）
- [div 22px] Test（1 words）
- [caption 28px] Choose models and catch overfitting on the validation set; save the test set for one final check（17 words）
- total（excl. eyebrow & chart）：6 blocks，27 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s9_l52.png`
### l53（6.2s）
- narration：A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't.
- [eyebrow 22px] 05 · HOW TO PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [h2 46px] Keep a mock exam（4 words）
- [div 22px] Train（1 words）
- [div 22px] Valid.（1 words）
- [div 22px] Test（1 words）
- [caption 28px] Choose models and catch overfitting on the validation set; save the test set for one final check（17 words）
- [caption 28px] A confession: in the demo we picked the model by its exam score — in a real project, you shouldn’t.（19 words）
- total（excl. eyebrow & chart）：7 blocks，46 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s9_l53.png`
### l54（7.6s）
- narration：Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- [eyebrow 22px] 05 · HOW TO PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [eyebrow 22px] ② MORE DATA（2 words）
- [h2 46px] Keep a mock exam（4 words）
- [h2 46px] More, and more varied, data（5 words）
- [div 22px] Train（1 words）
- [div 22px] Valid.（1 words）
- [div 22px] Test（1 words）
- [caption 28px] Choose models and catch overfitting on the validation set; save the test set for one final check（17 words）
- [caption 28px] Same complex model: wild with 10 points, close to the pattern with 40（13 words）
- total（excl. eyebrow & chart）：8 blocks，45 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s9_l54.png`
### l55（8.6s）
- narration：Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.
- [eyebrow 22px] 05 · HOW TO PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [eyebrow 22px] ② MORE DATA（2 words）
- [eyebrow 22px] ③ REGULARIZATION（1 words）
- [h2 46px] Keep a mock exam（4 words）
- [h2 46px] More, and more varied, data（5 words）
- [h2 46px] Put limits on complexity（4 words）
- [div 22px] Train（1 words）
- [div 22px] Valid.（1 words）
- [div 22px] Test（1 words）
- [caption 28px] Choose models and catch overfitting on the validation set; save the test set for one final check（17 words）
- [caption 28px] Same complex model: wild with 10 points, close to the pattern with 40（13 words）
- [caption 28px] Same 10 points: penalize overly complex curves, and it stops chasing the noise（13 words）
- total（excl. eyebrow & chart）：10 blocks，62 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/s9_l55.png`

## s10 Outro (on screen: end card)
### outro（package card, whole segment 15.2s）
- narration l56: Remember this one sentence.
- narration l57: Overfitting is like memorizing even the typos
- narration l58: and trusting them as the rule.
- narration l59: Next time you're sure you've got it, try a question you've never seen. Next episode: reinforcement learning.
- screen：Overfitting is like memorizing even the typos and trusting them as the rule.（13 words）
- screen：Reinforcement Learning / 强化学习（2 words）
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r1/materials/screen/en/card_s10.png`

