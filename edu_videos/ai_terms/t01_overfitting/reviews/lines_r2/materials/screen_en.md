# On-screen text (screen by screen)

For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here).

## s0 Cold open (before the title card)
### l01（6.7s）
- narration：A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.
- [div 16px] Your data / Nearly perfect（4 words）
- [div 16px] New data / Falls apart（4 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s0_l01.png`
### l02（4.5s）
- narration：It may not be a bug. It may be a problem called overfitting.
- [eyebrow 22px] THE PROBLEM IS CALLED（4 words）
- [h1 76px] Overfitting（1 words）
- total（excl. eyebrow & chart）：1 blocks，1 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s0_l02.png`

## s1 What's coming (on screen: agenda card)
### agenda（package card, whole segment 14.0s）
- narration l03: We'll start with a small experiment, so you can watch overfitting happen.
- narration l04: Then we'll look at real cases where it caused trouble, and how to prevent it.
- narration l05: No background needed. I'll explain every term as we go.
- screen：01 · What overfitting is（4 words）
- screen：02 · An analogy（3 words）
- screen：03 · Two error curves（4 words）
- screen：04 · Another lens（3 words）
- screen：05 · Real-world failures（3 words）
- screen：06 · Spot it, prevent it（5 words）
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_s1.png`

## c_problem（chapter card）
- What overfitting is
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_problem.png`

## s2 What a model learns
### l09（7.7s）
- narration：Overfitting is when a model fits its practice data so closely that it learns the flukes as well, and then does worse on new data.
- [eyebrow 22px] IN ONE SENTENCE（3 words）
- [display 132px] Overfitting（1 words）
- [h2 54px] Learns the flukes in its practice data（7 words）
- [h2 54px] Does worse on new data（5 words）
- total（excl. eyebrow & chart）：3 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s2_l09.png`
### l10（6.4s）
- narration：It's like memorizing the practice problems without learning the pattern. Let's watch it happen in a small experiment.
- [eyebrow 22px] IN ONE SENTENCE（3 words）
- [display 132px] Overfitting（1 words）
- [h2 54px] Learns the flukes in its practice data（7 words）
- [h2 54px] Does worse on new data（5 words）
- [h2 54px] ≈ Memorizing answers, missing the pattern（5 words）
- total（excl. eyebrow & chart）：4 blocks，18 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s2_l10.png`
### l11（6.9s）
- narration：These ten points are the data we collected. This is called the training data. Think of it as practice problems.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] What a model learns（4 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s2_l11.png`
### l12（5.7s）
- narration：They follow a pattern, but each point is slightly off. Those random wobbles are called noise.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] What a model learns（4 words）
- [caption 28px] Noise: random wobble（3 words）
- [caption 28px] The hidden pattern（3 words）
- total（excl. eyebrow & chart）：3 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s2_l12.png`
### l13（6.0s）
- narration：The model's job is to find the pattern in these points, so it can predict new data it has never seen.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] What a model learns（4 words）
- [eyebrow 22px] THE MODEL'S JOB（3 words）
- [h2 54px] Find the pattern / → predict new data（6 words）
- total（excl. eyebrow & chart）：2 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s2_l13.png`

## s3 Three ways to learn
### l14（7.4s）
- narration：Model one is too simple: just a straight line. We score it by how far the points miss the line, squared and averaged.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Same data, three models（4 words）
- [caption 28px] Error（1 words）
- total（excl. eyebrow & chart）：2 blocks，5 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s3_l14.png`
### l15（4.2s）
- narration：It misses even the practice points by a lot. That's underfitting.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Same data, three models（4 words）
- [eyebrow 22px] PRACTICE ERROR · MEAN SQUARED MISS（5 words）
- [div 16px] ① Straight line / 0.53 / Underfit（4 words）
- [caption 28px] Error（1 words）
- total（excl. eyebrow & chart）：3 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s3_l15.png`
### l16（5.7s）
- narration：Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Same data, three models（4 words）
- [eyebrow 22px] PRACTICE ERROR · MEAN SQUARED MISS（5 words）
- [div 16px] ① Straight line / 0.53 / Underfit（4 words）
- [div 16px] ② Gentle curve / 0.05（3 words）
- total（excl. eyebrow & chart）：3 blocks，11 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s3_l16.png`
### l17（8.0s）
- narration：Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Same data, three models（4 words）
- [eyebrow 22px] PRACTICE ERROR · MEAN SQUARED MISS（5 words）
- [div 16px] ① Straight line / 0.53 / Underfit（4 words）
- [div 16px] ② Gentle curve / 0.05（3 words）
- [div 16px] ③ Wiggly curve / 0.00（3 words）
- total（excl. eyebrow & chart）：4 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s3_l17.png`
### l18（3.2s）
- narration：Quick guess: on new questions, which one does best?
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Which does best on new data?（6 words）
- [eyebrow 22px] PRACTICE ERROR · MEAN SQUARED MISS（5 words）
- [div 16px] ① Straight line / 0.53 / Underfit（4 words）
- [div 16px] ② Gentle curve / 0.05（3 words）
- [div 16px] ③ Wiggly curve / 0.00（3 words）
- total（excl. eyebrow & chart）：4 blocks，16 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s3_l18.png`

## s4 The exam
### l19（6.7s）
- narration：Here are six new points the models have never seen. This is the test data. Think of it as the exam.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] New questions: the exam（4 words）
- [eyebrow 22px] PRACTICE / EXAM（2 words）
- [div 16px] ① Straight line / 0.53 / 0.54（4 words）
- [div 16px] ② Gentle curve / 0.05 / —（3 words）
- [div 16px] ③ Wiggly curve / 0.00 / —（3 words）
- [caption 28px] Exam points（2 words）
- total（excl. eyebrow & chart）：5 blocks，16 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s4_l19.png`
### l20（3.7s）
- narration：Model two stays close to the new points. It does best.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] New questions: the exam（4 words）
- [eyebrow 22px] PRACTICE / EXAM（2 words）
- [div 16px] ① Straight line / 0.53 / 0.54（4 words）
- [div 16px] ② Gentle curve / 0.05 / 0.07（4 words）
- [div 16px] ③ Wiggly curve / 0.00 / —（3 words）
- total（excl. eyebrow & chart）：4 blocks，15 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s4_l20.png`
### l21（7.8s）
- narration：Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] ③'s exam error: 25× ②'s（5 words）
- [eyebrow 22px] PRACTICE / EXAM（2 words）
- [div 16px] ① Straight line / 0.53 / 0.54（4 words）
- [div 16px] ② Gentle curve / 0.05 / 0.07（4 words）
- [div 16px] ③ Wiggly curve / 0.00 / 1.80（4 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s4_l21.png`
### l22（7.0s）
- narration：It memorized the noise as well. But noise is random, so it won't repeat on new questions. That's overfitting.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] ③'s exam error: 25× ②'s（5 words）
- [caption 28px] Noise won't repeat（3 words）
- [eyebrow 22px] PRACTICE / EXAM（2 words）
- [div 16px] ① Straight line / 0.53 / 0.54（4 words）
- [div 16px] ② Gentle curve / 0.05 / 0.07（4 words）
- [div 16px] ③ Wiggly curve / 0.00 / 1.80（4 words）
- total（excl. eyebrow & chart）：5 blocks，20 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s4_l22.png`
### l23（9.6s）
- narration：Underfitting is easy to spot: it does badly on practice and exam alike. Overfitting is sneakier: it can ace the practice and still fail the exam.
- [eyebrow 22px] 01 · WHAT OVERFITTING IS（4 words）
- [h1 76px] Underfit: bad on both, easy to spot（7 words）
- [h1 76px] Overfit: aces practice, hard to catch（6 words）
- total（excl. eyebrow & chart）：2 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s4_l23.png`

## c_analogy（chapter card）
- An analogy
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_analogy.png`

## s5 An analogy
### l24（7.9s）
- narration：Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE WORKBOOK（2 words）
- [display 132px] 100（1 words）
- [body 38px] Even the typos, memorized（4 words）
- total（excl. eyebrow & chart）：2 blocks，5 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l24.png`
### l25（4.1s）
- narration：But on the exam, when a question changes even slightly, he's lost.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE EXAM（2 words）
- [h1 76px] A small change, / and he's lost（6 words）
- total（excl. eyebrow & chart）：1 blocks，6 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l25.png`
### l26（11.1s）
- narration：Back in our experiment, the workbook is the training data, the typos are the noise, and the exam is the test data. The student who memorized everything is the curve through every point.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [div 16px] The workbook / → / Training data（4 words）
- [div 16px] The typos / → / Noise（3 words）
- [div 16px] The exam / → / Test data（4 words）
- [div 16px] Memorizing / → / A curve through every point（6 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l26.png`
### l27（8.4s）
- narration：The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] WHERE THE ANALOGY BREAKS（4 words）
- [h1 76px] The student knows he's memorizing（5 words）
- [h1 76px] The model doesn't（3 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l27.png`
### l28（7.5s）
- narration：There's a related problem. Say you're teaching a child to recognize cats, and in every photo, the cat is lying on a sofa.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] A RELATED, BUT DIFFERENT, PROBLEM（5 words）
- [h1 76px] Every cat: on a sofa（5 words）
- total（excl. eyebrow & chart）：1 blocks，5 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l28.png`
### l29（9.9s）
- narration：What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [h1 76px] His likely rule: sofa = cat（5 words）
- [caption 28px] Photos he's seen: correct（4 words）
- [h2 54px] “Cat!”（1 words）
- [h2 54px] “Not a cat.”（3 words）
- total（excl. eyebrow & chart）：4 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l29.png`
### l30（11.7s）
- narration：Both took the examples in front of them as the rule. The student memorized every detail; the child latched onto the sofa. The child's mistake is called shortcut learning. We'll come back to it.
- [eyebrow 22px] 02 · AN ANALOGY（3 words）
- [eyebrow 22px] THE STUDENT（2 words）
- [eyebrow 22px] THE CHILD（2 words）
- [h1 76px] Memorized every detail（3 words）
- [h1 76px] Latched onto the sofa（4 words）
- [caption 28px] Overfitting（1 words）
- [caption 28px] Shortcut learning（2 words）
- total（excl. eyebrow & chart）：4 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s5_l30.png`

## c_experiment（chapter card）
- Two error curves
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_experiment.png`

## s6 One chart
### l31（8.5s）
- narration：Back to the experiment. We repeat it with 300 random sets of points, try models from simple to complex on each, and track both errors.
- [eyebrow 22px] 03 · TWO ERROR CURVES（4 words）
- [h1 76px] Complexity vs. error（3 words）
- [span 120px] 300（1 words）
- [h2 54px] random point sets（3 words）
- [caption 28px] median shown（2 words）
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
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s6_l31.png`
### l32（3.6s）
- narration：The more complex the model, the lower its practice error.
- [eyebrow 22px] 03 · TWO ERROR CURVES（4 words）
- [h1 76px] Complexity vs. error（3 words）
- [span 120px] 300（1 words）
- [h2 54px] random point sets（3 words）
- [caption 28px] median shown（2 words）
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
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s6_l32.png`
### l33（6.0s）
- narration：But exam error falls, then rises. Moderately complex models do best on new data.
- [eyebrow 22px] 03 · TWO ERROR CURVES（4 words）
- [h1 76px] Complexity vs. error（3 words）
- [span 120px] 300（1 words）
- [chart 28px] Just right（2 words）
- [h2 54px] random point sets（3 words）
- [caption 28px] median shown（2 words）
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
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s6_l33.png`
### l34（4.5s）
- narration：Low practice error with high exam error: that's the telltale sign of overfitting.
- [eyebrow 22px] 03 · TWO ERROR CURVES（4 words）
- [h1 76px] Complexity vs. error（3 words）
- [chart 28px] Just right（2 words）
- [chart 28px] Overfit（1 words）
- [eyebrow 22px] THE TELLTALE SIGN（3 words）
- [h2 54px] Practice error low / Exam error high（6 words）
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
- total（excl. eyebrow & chart）：2 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s6_l34.png`
### l35（9.5s）
- narration：Does that mean simpler is always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the middle, where both are low.
- [eyebrow 22px] 03 · TWO ERROR CURVES（4 words）
- [h1 76px] Complexity vs. error（3 words）
- [eyebrow 22px] A COMMON MYTH（3 words）
- [chart 28px] Underfit（1 words）
- [chart 28px] Just right（2 words）
- [chart 28px] Overfit（1 words）
- [h2 54px] Is simpler always better?（4 words）
- [body 38px] No: too simple, both errors high（6 words）
- [body 38px] Aim for the middle（4 words）
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
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s6_l35.png`

## c_lens（chapter card）
- Another lens
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_lens.png`

## s7 Learning is compression
### l36（4.2s）
- narration：Here's another way to look at it: learning is a kind of compression.
- [eyebrow 22px] 04 · ANOTHER LENS（3 words）
- [display 132px] Learning ≈ compression（2 words）
- total（excl. eyebrow & chart）：1 blocks，2 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s7_l36.png`
### l37（4.9s）
- narration：To remember these ten points exactly, you have to store ten numbers, one height for each.
- [eyebrow 22px] 04 · ANOTHER LENS（3 words）
- [h1 76px] Numbers needed for 10 points?（5 words）
- [div 28px] Store as is: 10 numbers（5 words）
- total（excl. eyebrow & chart）：2 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s7_l37.png`
### l38（6.4s）
- narration：Model two's curve is set by just four numbers. That's enough to follow the pattern, and to land close to new points.
- [eyebrow 22px] 04 · ANOTHER LENS（3 words）
- [h1 76px] Numbers needed for 10 points?（5 words）
- [div 28px] Store as is: 10 numbers（5 words）
- [div 28px] ② 4 numbers: compressed（3 words）
- total（excl. eyebrow & chart）：3 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s7_l38.png`
### l39（8.1s）
- narration：Model three needs ten numbers to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise as well.
- [eyebrow 22px] 04 · ANOTHER LENS（3 words）
- [h1 76px] Numbers needed for 10 points?（5 words）
- [div 28px] Store as is: 10 numbers（5 words）
- [div 28px] ② 4 numbers: compressed（3 words）
- [div 28px] ③ 10 numbers: no compression（4 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s7_l39.png`
### l40（6.7s）
- narration：Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern.
- [eyebrow 22px] GOOD COMPRESSION（2 words）
- [h1 76px] Keep the pattern, drop the noise（6 words）
- [h2 54px] Squeeze too hard: lose the pattern（6 words）
- total（excl. eyebrow & chart）：2 blocks，12 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s7_l40.png`

## c_real（chapter card）
- Real-world failures
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_real.png`

## s8 The real-world cost
### l41（2.7s）
- narration：Problems like this have caused real trouble.
- [eyebrow 22px] 05 · REAL-WORLD FAILURES（3 words）
- [h1 76px] It has caused real trouble（5 words）
- total（excl. eyebrow & chart）：1 blocks，5 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l41.png`
### l42（5.9s）
- narration：Google Flu Trends used people's searches to estimate what share of doctor visits were for flu-like illness.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- total（excl. eyebrow & chart）：0 blocks，0 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l42.png`
### l43（6.5s）
- narration：Researchers pointed out that its first version sifted through 50 million search terms to fit about 1,100 data points.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] THE FIRST VERSION（3 words）
- [div 16px] 50M search terms（3 words）
- [div 16px] 1,152 data points（3 words）
- [div 80px] ≫（0 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：4 blocks，11 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l43.png`
### l44（10.4s）
- narration：With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [quote 72px] “Part flu detector, / part winter detector”（6 words）
- [body 38px] The researchers: overfitting（3 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：3 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l44.png`
### l45（8.0s）
- narration：Later versions still struggled. From 2011 to 2013, it overestimated flu in 100 of 108 weeks.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] LATER VERSIONS · 2011–2013（3 words）
- [span 160px] 100（1 words）
- [span 160px] / 108（1 words）
- [h2 54px] weeks overestimated（2 words）
- [div 22px] Lazer et al. · Science · 2014（5 words）
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l45.png`
### l46（7.1s）
- narration：Medical imaging has examples of its own. A model that detected pneumonia in chest X-rays did worse at a new hospital.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] PNEUMONIA FROM CHEST X-RAYS（4 words）
- [h1 76px] New hospital, worse results（4 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：2 blocks，10 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l46.png`
### l47（8.8s）
- narration：The X-rays carried a hospital fingerprint. A separate model could tell which of two hospitals a scan came from, with over 99.9 percent accuracy.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] A SEPARATE MODEL: WHICH HOSPITAL?（5 words）
- [display 160px] 99.9%+（1 words）
- [span 96px] +（0 words）
- [h2 54px] The X-rays carry a hospital fingerprint（6 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：4 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l47.png`
### l48（9.5s）
- narration：And the share of scans labeled pneumonia varied widely between hospitals. So part of the pneumonia model's success likely came from recognizing the hospital, not the disease.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] SCANS LABELED PNEUMONIA, BY HOSPITAL（5 words）
- [span 160px] 34%（1 words）
- [display 160px] 34% vs 1%（3 words）
- [span 96px] vs（1 words）
- [h2 54px] Partly recognizing hospitals, not disease（5 words）
- [div 22px] Zech et al. · PLOS Medicine · 2018（6 words）
- total（excl. eyebrow & chart）：5 blocks，16 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l48.png`
### l49（11.6s）
- narration：Then there's a skin-cancer detector. Doctors often mark suspicious moles with ink, and the model likely learned the ink as a clue. In one study, it flagged over half of the inked harmless moles as cancer.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] DOCTORS OFTEN INK SUSPICIOUS MOLES（5 words）
- [display 160px] 54%（1 words）
- [h2 54px] of inked harmless moles flagged as cancer（7 words）
- [div 22px] Winkler et al. · JAMA Dermatology · 2019（6 words）
- total（excl. eyebrow & chart）：3 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l49.png`
### l50（11.8s）
- narration：The X-ray and mole models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They can do well in familiar settings, and still fail somewhere new.
- [eyebrow 28px] Google Flu Trends（3 words）
- [eyebrow 28px] Pneumonia X-ray model（3 words）
- [eyebrow 28px] Skin-cancer detector（2 words）
- [eyebrow 22px] X-RAY AND MOLE: SHORTCUT LEARNING（5 words）
- [h1 76px] Can fail somewhere new（4 words）
- [body 38px] The clue only holds in the data at hand（9 words）
- total（excl. eyebrow & chart）：2 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s8_l50.png`

## c_fix（chapter card）
- Spot it, prevent it
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_c_fix.png`

## s9 How to prevent it
### l51（4.0s）
- narration：So how do you spot and prevent overfitting? Three common ways.
- [eyebrow 22px] 06 · SPOT IT, PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s9_l51.png`
### l52（10.3s）
- narration：One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- [eyebrow 22px] 06 · SPOT IT, PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [h2 44px] Keep a mock exam（4 words）
- [chart 22px] Train（1 words）
- [chart 22px] Valid.（1 words）
- [chart 22px] Test（1 words）
- [caption 28px] Pick models on validation, test last（6 words）
- total（excl. eyebrow & chart）：3 blocks，13 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s9_l52.png`
### l53（6.2s）
- narration：A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't.
- [eyebrow 22px] 06 · SPOT IT, PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [h2 44px] Keep a mock exam（4 words）
- [chart 22px] Train（1 words）
- [chart 22px] Valid.（1 words）
- [chart 22px] Test（1 words）
- [caption 28px] Our demo picked by exam score. Don't.（7 words）
- total（excl. eyebrow & chart）：3 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s9_l53.png`
### l54（7.6s）
- narration：Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- [eyebrow 22px] 06 · SPOT IT, PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [eyebrow 22px] ② MORE DATA（2 words）
- [h2 44px] Keep a mock exam（4 words）
- [h2 44px] More data, more variety（4 words）
- [chart 22px] Train（1 words）
- [chart 22px] Valid.（1 words）
- [chart 22px] Test（1 words）
- total（excl. eyebrow & chart）：3 blocks，11 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s9_l54.png`
### l55（8.6s）
- narration：Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.
- [eyebrow 22px] 06 · SPOT IT, PREVENT IT（5 words）
- [h1 76px] Three common ways（3 words）
- [eyebrow 22px] ① VALIDATION SET（2 words）
- [eyebrow 22px] ② MORE DATA（2 words）
- [eyebrow 22px] ③ REGULARIZATION（1 words）
- [h2 44px] Keep a mock exam（4 words）
- [h2 44px] More data, more variety（4 words）
- [h2 44px] Penalize complex curves（3 words）
- [chart 22px] Train（1 words）
- [chart 22px] Valid.（1 words）
- [chart 22px] Test（1 words）
- total（excl. eyebrow & chart）：4 blocks，14 words
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/s9_l55.png`

## s10 Outro (on screen: end card)
### outro（package card, whole segment 14.6s）
- narration l56: If you remember one thing:
- narration l57: Overfitting is memorizing even the typos.
- narration l58: And then treating them as rules.
- narration l59: Next time you're sure you've got it, try a question you've never seen. Up next: reinforcement learning.
- screen：Overfitting is memorizing even the typos, and then treating them as rules.（12 words）
- screen：Reinforcement learning（2 words）
- screenshot：`edu_videos/ai_terms/t01_overfitting/reviews/lines_r2/materials/screen/en/card_s10.png`

