# On-screen text (screen by screen)

For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here).

## s0 Cold open (before the title card)
### l01（4.6s）
- narration：Today's big AI models have billions of knobs, some hundreds of billions.
- [h1 76px] Billions of knobs（3 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s0_l01.png`
### l02（6.5s）
- narration：Every step of training, you need to know which way each knob should turn, and how far.
- [h1 76px] Every step: which way, how far（6 words）
- total（excl. eyebrow & chart）：1 blocks，6 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s0_l02.png`
### l03（3.5s）
- narration：You'd never finish testing them one at a time.
- [h1 76px] One at a time? Never finishes（6 words）
- [div 54px] 9 tested（2 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s0_l03.png`
### l04（5.4s）
- narration：The real trick finds every knob's direction in one trip backward. It's called backpropagation.
- [display 132px] Backpropagation（1 words）
- total（excl. eyebrow & chart）：1 blocks，1 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s0_l04.png`

## s1 What's coming (on screen: agenda card)
### agenda（package card, whole segment 19.6s）
- narration l05: Last time we saw that a neural network is layers of small units, each with its own knobs.
- narration l06: This time, we'll see why testing knobs one by one breaks down, watch the error flow backward through a tiny network, and see where the idea came from.
- screen：01 · Too many knobs to try（6 words）
- screen：02 · Working backward（3 words）
- screen：03 · A small experiment（4 words）
- screen：04 · From 1986 to today（5 words）
- screen：Prereqs: Last time: neural networks（5 words）
- screenshot：``

## c_problem（chapter card）
- Too many knobs to try
- screenshot：``

## s2 Too many knobs to try
### l07（7.7s）
- narration：In training, the model makes a guess, we compare it with the right answer, and the gap is the error.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The gap = error（3 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s2_l07.png`
### l08（7.7s）
- narration：The loss is a score for how wrong it is. Training is turning the knobs to push that score down.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] Training: lower the loss（4 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s2_l08.png`
### l09（8.8s）
- narration：Each step, you want to know which way each knob should turn to drop the error fastest. That's the gradient, or the slope.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] Gradient = slope（2 words）
- [eyebrow 22px] Model（1 words）
- [chart 40px] Guess（1 words）
- [chart 40px] Answer（1 words）
- [div 64px] ↻（0 words）
- [div 64px] ↺（0 words）
- [div 64px] ↻（0 words）
- [chart 40px] Error（1 words）
- total（excl. eyebrow & chart）：4 blocks，2 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s2_l09.png`
### l10（6.5s）
- narration：The obvious way? Nudge one knob, rerun everything, and see if the error went up or down.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The slow way（3 words）
- [eyebrow 22px] Model（1 words）
- [span 150px] 3（1 words）
- [h2 54px] reruns（1 words）
- [div 54px] Nudge → rerun → compare（3 words）
- total（excl. eyebrow & chart）：4 blocks，8 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s2_l10.png`
### l11（5.8s）
- narration：One full rerun per knob. Billions of knobs, billions of reruns. For a single step.
- [eyebrow 22px] 01 · Too many knobs to try（6 words）
- [h1 60px] The slow way（3 words）
- [eyebrow 22px] Model（1 words）
- [div 150px] Billions（1 words）
- [div 54px] of reruns, for one step（5 words）
- total（excl. eyebrow & chart）：3 blocks，9 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s2_l11.png`

## c_analogy（chapter card）
- Working backward
- screenshot：``

## s3 Working backward
### l12（6.9s）
- narration：Backpropagation starts at the answer instead. Picture a chain of gears, with a pointer on the last one.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] A chain of gears（4 words）
- [chart 30px] Pointer（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l12.png`
### l13（8.1s）
- narration：Turn the first gear one notch, and the second turns 2. Turn the second one notch, and the third turns 3.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] A chain of gears（4 words）
- [chart 30px] Pointer（1 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l13.png`
### l14（6.2s）
- narration：So how far does the pointer move? Multiply along the way: 2 × 3. 6 notches.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] How far does it go?（5 words）
- [chart 30px] Pointer（1 words）
- [div 130px] 2 × 3 = 6（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l14.png`
### l15（6.2s）
- narration：So start at the pointer and work backward, multiplying by each gear's ratio as you go.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Backward, gear by gear（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l15.png`
### l16（5.8s）
- narration：At each gear you multiply once and reuse what you already have. Nothing gets redone.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Backward, gear by gear（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [h2 54px] Reuse what’s done（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：2 blocks，7 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l16.png`
### l17（10.4s）
- narration：A neural network is a chain like this: each knob affects the answer through the layers after it. So the error can flow back the same way.
- [eyebrow 22px] 02 · Working backward（3 words）
- [h1 54px] Networks work like gears（4 words）
- [chart 64px] 6（1 words）
- [chart 64px] 3（1 words）
- [chart 64px] 1（1 words）
- [chart 30px] Pointer（1 words）
- [h2 54px] Knob → layers → answer（3 words）
- [h2 54px] Error flows back（3 words）
- [chart 52px] ×2（1 words）
- [chart 52px] ×3（1 words）
- total（excl. eyebrow & chart）：3 blocks，10 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s3_l17.png`

## c_experiment（chapter card）
- A small experiment
- screenshot：``

## s4 A small experiment
### l18（7.7s）
- narration：Here's a real, tiny network: two layers, 7 knobs. We feed it the length of a taxi ride: 5 kilometers.
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l18.png`
### l19（7.3s）
- narration：In the first layer, two units, A and B, use two knobs each. A gets 6, B gets 4.
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l19.png`
### l20（5.8s）
- narration：The second layer multiplies each by a knob, adds one more, and guesses: 29 yuan.
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l20.png`
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l21.png`
### l22（8.5s）
- narration：Last layer first. Each knob's share of the blame, which is its slope, is the error times the number fed into it.
- [h2 54px] Blame = error × input（3 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 44px] 6（1 words）
- [div 32px] ×2（1 words）
- [div 32px] ×1（1 words）
- [div 32px] +1（1 words）
- [div 56px] 29（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +13（1 words）
- [div 28px] B（1 words）
- [div 34px] 6（1 words）
- [div 44px] 4（1 words）
- [div 32px] ×0.4（1 words）
- [div 32px] +2（1 words）
- [div 32px] ×1（1 words）
- total（excl. eyebrow & chart）：16 blocks，18 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l22.png`
### l23（5.8s）
- narration：The inputs are 6, 4 and 1, so the blame is 36, 24 and 6. Bigger input, bigger blame.
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l23.png`
### l24（6.5s）
- narration：One layer back, the error flows along the wires and gets multiplied by each knob it passes.
- [h2 54px] Going back: error × knob（4 words）
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l24.png`
### l25（4.6s）
- narration：A's side is times 2: 12. B's side is times 1: 6.
- [h2 54px] Going back: error × knob（4 words）
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
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l25.png`
### l26（4.2s）
- narration：Each unit then does the same for its own two knobs.
- [h2 54px] Blame = received × input（3 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
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
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：23 blocks，25 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l26.png`
### l27（8.5s）
- narration：One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others.
- [h2 54px] Guess too high → all turn down（6 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
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
- [div 32px] ×1（1 words）
- [div 34px] 24（1 words）
- total（excl. eyebrow & chart）：23 blocks，28 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l27.png`
### l28（6.9s）
- narration：We turn each knob a small step that way and guess again. 29 becomes about 24. Much closer.
- [h2 54px] One small step: closer（4 words）
- [eyebrow 22px] 03 · A small experiment（4 words）
- [div 28px] A（1 words）
- [div 32px] ×1.82（1 words）
- [div 32px] ×0.7（1 words）
- [div 32px] +0.94（1 words）
- [div 40px] 23.88（1 words）
- [n 84px] 5（1 words）
- [u 28px] km（1 words）
- [div 32px] +12.97（1 words）
- [div 28px] B（1 words）
- [div 32px] ×0.25（1 words）
- [div 32px] +1.97（1 words）
- [div 32px] ×0.88（1 words）
- total（excl. eyebrow & chart）：13 blocks，16 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l28.png`
### l29（6.9s）
- narration：We checked the slow way too: one run with nothing changed, then one per nudged knob. 8 runs.
- [eyebrow 22px] 03 · A small experiment（4 words）
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
- total（excl. eyebrow & chart）：9 blocks，10 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l29.png`
### l30（5.4s）
- narration：Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back.
- [eyebrow 22px] 03 · A small experiment（4 words）
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
- [h2 54px] ✓ Identical（1 words）
- total（excl. eyebrow & chart）：18 blocks，22 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l30.png`
### l31（6.2s）
- narration：Scale up to a billion knobs, and the slow way is 1,000,000,001 runs.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l31.png`
### l32（5.0s）
- narration：Even at one second a run, that's over 30 years. For one step.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [div 38px] At 1 second a run: ≈ 31.7 years for one step（10 words）
- total（excl. eyebrow & chart）：5 blocks，19 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l32.png`
### l33（7.3s）
- narration：Backpropagation is still one trip each way. The trip back costs about two runs, so roughly 3 in all.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] A billion knobs（3 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [span 92px] ≈ 3runs（1 words）
- [h2 54px] Backpropagation（1 words）
- [span 28px] runs（1 words）
- [div 38px] At 1 second a run: ≈ 31.7 years for one step（10 words）
- total（excl. eyebrow & chart）：8 blocks，22 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l33.png`
### l34（2.7s）
- narration：Without it, nobody could train these models.
- [eyebrow 22px] 03 · A small experiment（4 words）
- [h1 76px] No backprop, no big models（5 words）
- [span 92px] 1,000,000,001runs（1 words）
- [h2 54px] Nudge one by one（4 words）
- [span 28px] runs（1 words）
- [span 92px] ≈ 3runs（1 words）
- [h2 54px] Backpropagation（1 words）
- [span 28px] runs（1 words）
- [div 38px] At 1 second a run: ≈ 31.7 years for one step（10 words）
- total（excl. eyebrow & chart）：8 blocks，24 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s4_l34.png`

## c_real（chapter card）
- From 1986 to today
- screenshot：``

## s5 From 1986 to today
### l35（7.3s）
- narration：So where does this come from? A 1986 Nature paper by Rumelhart, Hinton and Williams laid it out clearly.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature · 1986（2 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（7 words）
- total（excl. eyebrow & chart）：3 blocks，13 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l35.png`
### l36（5.4s）
- narration：They found each knob's slope in two passes: forward, then back from the output.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature · 1986（2 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（7 words）
- [h2 54px] Forward pass →（2 words）
- [h2 54px] ← Backward pass（2 words）
- total（excl. eyebrow & chart）：5 blocks，17 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l36.png`
### l37（6.9s）
- narration：They also found that the units in the middle learn to pick up useful patterns on their own.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature · 1986（2 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（7 words）
- [h2 54px] Middle units: find patterns（4 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l37.png`
### l38（6.2s）
- narration：Others had similar ideas earlier. This paper showed the method working on networks with several layers.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [display 190px] 1986（1 words）
- [eyebrow 22px] Nature · 1986（2 words）
- [h2 54px] Learning representations by back-propagating errors（5 words）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（7 words）
- [caption 28px] Similar methods came earlier（4 words）
- total（excl. eyebrow & chart）：4 blocks，17 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l38.png`
### l39（7.3s）
- narration：Today, in PyTorch, a popular tool for building models, one line, loss.backward(), gives every knob its slope.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [div 96px] loss.backward()（1 words）
- [span 96px] loss（1 words）
- [h2 54px] PyTorch: every slope at once（5 words）
- total（excl. eyebrow & chart）：3 blocks，7 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l39.png`
### l40（5.0s）
- narration：That's automatic differentiation. Underneath, it's backpropagation: walking back from the output, collecting slopes.
- [eyebrow 22px] 04 · From 1986 to today（5 words）
- [div 96px] loss.backward()（1 words）
- [span 96px] loss（1 words）
- [h1 76px] Automatic differentiation（2 words）
- [h2 54px] Underneath: backpropagation（2 words）
- [div 22px] Source: PyTorch tutorial（3 words）
- total（excl. eyebrow & chart）：5 blocks，9 words
- screenshot：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/en/s5_l40.png`

## s6 Outro (on screen: end card)
### outro（package card, whole segment 21.4s）
- narration l41: Backpropagation is passing the blame backward, from the output, layer by layer.
- narration l42: One trip back, and every knob knows which way to turn, and how far.
- narration l43: But with so many knobs, a model can memorize the practice questions and get new ones wrong.
- narration l44: That's overfitting, and it's up next.
- screen：Blame flows back, layer by layer（6 words）
- screen：Overfitting（1 words）
- screenshot：``

