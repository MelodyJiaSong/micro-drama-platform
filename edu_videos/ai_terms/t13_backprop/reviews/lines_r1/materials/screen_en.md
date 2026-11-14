# On-screen text (screen by screen)

For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here).

## s0 Cold open (before the title card)
### l01（4.6s）
- narration：Today's big AI models have billions of knobs, some hundreds of billions.
- [h1 76px] Billions of knobs（3 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s0_l01.png`
### l02（6.5s）
- narration：Every step of training, you need to know which way each knob should turn, and how far.
- [h1 76px] Every step: which way, how far（6 words）
- total（excl. eyebrow & chart）：1 blocks，6 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s0_l02.png`
### l03（3.5s）
- narration：Testing them one at a time would never finish.
- [h1 76px] One by one? Never ends（5 words）
- [div 54px] Tried 9（2 words）
- total（excl. eyebrow & chart）：2 blocks，7 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s0_l03.png`
### l04（5.0s）
- narration：The real trick gets them all in one trip backward. It's called backpropagation.
- [eyebrow 22px] One trip backward, all of them（6 words）
- [display 132px] Backpropagation（1 words）
- total（excl. eyebrow & chart）：1 blocks，1 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s0_l04.png`

## s1 What's coming (on screen: agenda card)
### agenda（package card, whole segment 17.3s）
- narration l05: Last time we saw that a neural network is layers of small units, each with its own knobs.
- narration l06: This time, we'll see why testing knobs one by one breaks down, then watch the error flow backward through a tiny network.
- screen：01 · Too many knobs to try（6 words）
- screen：02 · Working backward（3 words）
- screen：03 · A small experiment（4 words）
- screen：04 · From 1986 to today（5 words）
- screen：Prereqs: Neural networks & deep learning（5 words）
- screenshot：``

## c_problem（chapter card）
- Too many knobs to try
- screenshot：``

## s2 Too many knobs to try
### l07（6.9s）
- narration：Here's training: the model guesses, we compare it with the right answer, and the gap is the error.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The gap = error（3 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s2_l07.png`
### l08（7.7s）
- narration：The loss is a score for how wrong it is. Training is turning the knobs to push that score down.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] Training: lower the loss（4 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s2_l08.png`
### l09（7.7s）
- narration：So each step, you want the gradient: which way each knob should turn to drop the error fastest. The slope.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] Gradient: which way to turn（5 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [div 64px] ↻（0 words）
- [div 64px] ↺（0 words）
- [div 64px] ↻（0 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：4 blocks，5 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s2_l09.png`
### l10（6.5s）
- narration：The obvious way? Nudge one knob, rerun everything, and see if the error went up or down.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The slow way（3 words）
- [eyebrow 22px] Model（1 words）
- [span 150px] 3（1 words）
- [h2 54px] runs（1 words）
- [div 54px] Rerun, see if the error moved（6 words）
- total（excl. eyebrow & chart）：4 blocks，11 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s2_l10.png`
### l11（5.8s）
- narration：One full rerun per knob. Billions of knobs, billions of reruns. For a single step.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The slow way（3 words）
- [eyebrow 22px] Model（1 words）
- [div 150px] Billions（1 words）
- [div 54px] for one step（3 words）
- total（excl. eyebrow & chart）：3 blocks，7 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s2_l11.png`

## c_analogy（chapter card）
- Working backward
- screenshot：``

## s3 Working backward
### l12（6.9s）
- narration：Backpropagation works from the other end. Picture a chain of gears, with a pointer on the last one.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] A chain of gears（4 words）
- [chart 30px] Pointer（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l12.png`
### l13（7.3s）
- narration：Turn the first gear one notch, the second turns 2. One notch on the second, the third turns 3.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] A chain of gears（4 words）
- [chart 30px] Pointer（1 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l13.png`
### l14（6.2s）
- narration：So how far does the pointer move? Multiply along the way: 2 × 3. 6 notches.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] How far does it go?（5 words）
- [chart 30px] Pointer（1 words）
- [div 130px] 2 × 3 = 6（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l14.png`
### l15（6.2s）
- narration：It's easiest to start at the pointer and walk back, multiplying in one ratio per gear.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Backward: one step each（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l15.png`
### l16（5.8s）
- narration：Each gear handles only its own link and reuses what's already done. Nothing is recalculated.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Backward: one step each（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [h2 54px] Reuse what’s done（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：2 blocks，7 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l16.png`
### l17（9.2s）
- narration：A neural network is a chain like this. Every knob drives the final answer through a few layers. So the error can flow back.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Networks work the same（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [h2 54px] Knob → layers → answer（3 words）
- [h2 54px] Error ← flows back（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：3 blocks，10 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s3_l17.png`

## c_experiment（chapter card）
- A small experiment
- screenshot：``

## s4 A small experiment
### l18（6.5s）
- narration：Here's a real, tiny network. Two layers, 7 knobs. The input is a taxi ride: 5 kilometers.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- total（excl. eyebrow & chart）：11 blocks，11 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l18.png`
### l19（6.5s）
- narration：In the first layer, units A and B use two knobs each to turn that into 6 and 4.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- total（excl. eyebrow & chart）：13 blocks，13 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l19.png`
### l20（5.8s）
- narration：The second layer weights each by a knob, adds one more, and guesses: 29 yuan.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [span 76px] 29（1 words）
- [span 54px] Guess（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- total（excl. eyebrow & chart）：16 blocks，16 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l20.png`
### l21（6.2s）
- narration：The real fare was 23. 6 too high. That six is the error we pass back.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [span 76px] 29（1 words）
- [span 54px] Guess（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [span 76px] 23（1 words）
- [span 54px] Actual（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [span 76px] +6（1 words）
- [span 54px] Too high（2 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- total（excl. eyebrow & chart）：21 blocks，22 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l21.png`
### l22（6.5s）
- narration：Last layer first. Each knob's blame is the error times what's fed into it: 36, 24, 6.
- [h2 54px] Blame = error × input（3 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 34px] 36（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：19 blocks，21 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l22.png`
### l23（1.9s）
- narration：Bigger number in, bigger blame.
- screen unchanged from previous line
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l23.png`
### l24（4.6s）
- narration：One layer back, the error is multiplied by the knob it crosses.
- [h2 54px] Passed back = error × knob（4 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 34px] 36（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：19 blocks，22 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l24.png`
### l25（3.8s）
- narration：Times 2 gives A 12. Times 1 gives B 6.
- [h2 54px] Passed back = error × knob（4 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 40px] 6 × 2 = 12（3 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 34px] 36（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 40px] 6 × 1 = 6（3 words）
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：21 blocks，28 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l25.png`
### l26（5.4s）
- narration：Each unit then splits its share between its own two knobs, the same way.
- [h2 54px] Passed back = error × knob（4 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 40px] 6 × 2 = 12（3 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 34px] 36（1 words）
- [div 34px] 60（1 words）
- [div 34px] 12（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 34px] 30（1 words）
- [div 34px] 6（1 words）
- [div 40px] 6 × 1 = 6（3 words）
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：25 blocks，32 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l26.png`
### l27（8.5s）
- narration：One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others.
- [h2 54px] All positive → all turn down（5 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 40px] 6 × 2 = 12（3 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 34px] 36（1 words）
- [div 34px] 60（1 words）
- [div 34px] 12（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 34px] 30（1 words）
- [div 34px] 6（1 words）
- [div 40px] 6 × 1 = 6（3 words）
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：25 blocks，33 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l27.png`
### l28（5.4s）
- narration：Turn each a small step and guess again. 29 becomes about 24. Much closer.
- [h2 54px] One small step: closer（4 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 40px] 6 × 2 = 12（3 words）
- [div 44px] 6（1 words）
- [div 32px] ×1.82（1 words）
- [div 32px] ×0.7（1 words）
- [div 32px] +0.94（1 words）
- [div 34px] 36（1 words）
- [div 34px] 60（1 words）
- [div 34px] 12（1 words）
- [div 40px] 23.88（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +12.97（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.25（1 words）
- [div 32px] +1.97（1 words）
- [div 34px] 30（1 words）
- [div 34px] 6（1 words）
- [div 40px] 6 × 1 = 6（3 words）
- [div 32px] ×0.88（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：24 blocks，31 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l28.png`
### l29（6.5s）
- narration：Now check it the slow way. That took 8 forward runs: one untouched, plus one per knob.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] Check: two ways（3 words）
- [eyebrow 22px] Nudge one by one（4 words）
- [span 110px] 8（1 words）
- [h2 54px] forward runs（2 words）
- [span 44px] 60（1 words）
- [span 44px] 12（1 words）
- [span 44px] 30（1 words）
- [span 44px] 6（1 words）
- [span 44px] 36（1 words）
- [span 44px] 24（1 words）
- [span 44px] 6（1 words）
- total（excl. eyebrow & chart）：10 blocks，13 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l29.png`
### l30（5.4s）
- narration：Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] Check: two ways（3 words）
- [eyebrow 22px] Nudge one by one（4 words）
- [eyebrow 22px] Backpropagation（1 words）
- [span 110px] 8（1 words）
- [div 110px] 1 forward + 1 back（4 words）
- [h2 54px] forward runs（2 words）
- [span 44px] 60（1 words）
- [span 44px] 12（1 words）
- [span 44px] 30（1 words）
- [span 44px] 6（1 words）
- [span 44px] 36（1 words）
- [span 44px] 24（1 words）
- [span 44px] 6（1 words）
- [span 44px] 60（1 words）
- [span 44px] 12（1 words）
- [span 44px] 30（1 words）
- [span 44px] 6（1 words）
- [span 44px] 36（1 words）
- [span 44px] 24（1 words）
- [span 44px] 6（1 words）
- [h2 54px] ✓ Same seven numbers（3 words）
- total（excl. eyebrow & chart）：19 blocks，27 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l30.png`
### l31（6.2s）
- narration：Scale up to a billion knobs, and the slow way is 1,000,000,001 runs.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l31.png`
### l32（5.0s）
- narration：Even at one second a run, that's over 30 years. For one step.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [span 92px] ≈ 31.7years, for one step（4 words）
- [h2 54px] At 1 second a run（5 words）
- [span 28px] years, for one step（4 words）
- total（excl. eyebrow & chart）：7 blocks，22 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l32.png`
### l33（3.8s）
- narration：Backpropagation stays one forward, one back. Roughly 3 runs' worth.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [span 92px] ≈ 31.7years, for one step（4 words）
- [h2 54px] At 1 second a run（5 words）
- [span 28px] years, for one step（4 words）
- [span 92px] ≈ 3runs’ worth（2 words）
- [h2 54px] Backpropagation（1 words）
- [span 28px] runs’ worth（2 words）
- total（excl. eyebrow & chart）：10 blocks，27 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l33.png`
### l34（3.1s）
- narration：Without it, billion-knob models couldn't be trained.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] Without it: no big models（5 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [span 92px] ≈ 31.7years, for one step（4 words）
- [h2 54px] At 1 second a run（5 words）
- [span 28px] years, for one step（4 words）
- [span 92px] ≈ 3runs’ worth（2 words）
- [h2 54px] Backpropagation（1 words）
- [span 28px] runs’ worth（2 words）
- total（excl. eyebrow & chart）：10 blocks，29 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s4_l34.png`

## c_real（chapter card）
- From 1986 to today
- screenshot：``

## s5 From 1986 to today
### l35（5.4s）
- narration：In 1986, a Nature paper by Rumelhart, Hinton and Williams laid this out clearly.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature（1 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [h2 38px] Rumelhart · Hinton · Williams（3 words）
- [div 22px] Nature 323, 533–536 (1986)（4 words）
- total（excl. eyebrow & chart）：4 blocks，13 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l35.png`
### l36（7.3s）
- narration：In the paper, each connection's slope is worked out in two passes: forward, then backward from the top layer.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature（1 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [h2 38px] Rumelhart · Hinton · Williams（3 words）
- [div 22px] Nature 323, 533–536 (1986)（4 words）
- [h2 54px] Forward pass →（2 words）
- [h2 54px] ← Backward pass（2 words）
- total（excl. eyebrow & chart）：6 blocks，17 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l36.png`
### l37（5.8s）
- narration：They also found that the units in the middle learn useful features on their own.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature（1 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [h2 38px] Rumelhart · Hinton · Williams（3 words）
- [div 22px] Nature 323, 533–536 (1986)（4 words）
- [h2 54px] Middle units: learn features（4 words）
- total（excl. eyebrow & chart）：5 blocks，17 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l37.png`
### l38（6.2s）
- narration：Similar methods had been proposed earlier. This paper showed it could train networks with several layers.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature（1 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [h2 38px] Rumelhart · Hinton · Williams（3 words）
- [div 22px] Nature 323, 533–536 (1986)（4 words）
- [h2 54px] Middle units: learn features（4 words）
- [caption 28px] Similar methods came earlier（4 words）
- total（excl. eyebrow & chart）：6 blocks，21 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l38.png`
### l39（5.0s）
- narration：Today in PyTorch, one line, loss.backward(), gives every knob its slope.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [div 96px] loss.backward()（1 words）
- [span 96px] loss（1 words）
- [h2 54px] PyTorch: every knob’s slope, at once（6 words）
- total（excl. eyebrow & chart）：3 blocks，8 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l39.png`
### l40（5.0s）
- narration：That's automatic differentiation. Underneath, it's backpropagation: walking back from the output, collecting slopes.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [div 96px] loss.backward()（1 words）
- [span 96px] loss（1 words）
- [h2 54px] PyTorch: every knob’s slope, at once（6 words）
- [h1 76px] Autograd（1 words）
- [h1 76px] =（0 words）
- [h1 76px] Backpropagation（1 words）
- [caption 28px] PyTorch docs: traverse back from the output, collecting gradients（9 words）
- total（excl. eyebrow & chart）：7 blocks，19 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/en/s5_l40.png`

## s6 Outro (on screen: end card)
### outro（package card, whole segment 21.8s）
- narration l41: Backpropagation is passing the blame backward, from the output, layer by layer.
- narration l42: One trip back, and every knob knows which way to turn, and how far.
- narration l43: But lots of knobs bring trouble. A model can memorize the practice questions and flunk a new one.
- narration l44: That's overfitting, and it's up next.
- screen：Pass the blame back, every knob in one trip（9 words）
- screen：Overfitting（1 words）
- screenshot：``

