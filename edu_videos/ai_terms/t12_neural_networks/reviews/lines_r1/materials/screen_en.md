# On-screen text (screen by screen)

For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here).

## s0 Cold open (before the title card)
### l01（5.4s）
- narration：Remember our two-knob taxi-fare machine? It learned distance and fare just fine.
- [chart 28px] Fare ($)（1 words）
- [div 22px] Base fare（2 words）
- [div 22px] Per km（2 words）
- [chart 24px] 40（1 words）
- [div 37px] 10.2（1 words）
- [div 37px] 2.54（1 words）
- [chart 24px] 20（1 words）
- [h2 54px] Learns it fine（3 words）
- [chart 24px] 0（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 4（1 words）
- [chart 24px] 8（1 words）
- [chart 24px] 12（1 words）
- [chart 28px] Distance (km)（2 words）
- total（excl. eyebrow & chart）：5 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s0_l01.png`
### l02（6.9s）
- narration：But fares also depend on the time: rush hour costs more, and late night a little more too.
- [chart 28px] Fare ($)（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：3 blocks，6 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s0_l02.png`
### l03（5.0s）
- narration：That, it can't learn, because all it can draw is a straight line.
- [chart 28px] Fare ($)（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [h2 54px] Only straight lines（3 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s0_l03.png`
### l04（5.4s）
- narration：So how does a machine learn a pattern that bends? With a neural network.
- [eyebrow 22px] Learning a bend（3 words）
- [h1 78px] Neural networks（2 words）
- total（excl. eyebrow & chart）：1 blocks，2 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s0_l04.png`

## s1 What's coming (on screen: agenda card)
### agenda（package card, whole segment 14.2s）
- narration l05: Last time, we turned the knobs by walking downhill blindfolded, toward wherever the score drops fastest.
- narration l06: Today we'll build a tiny network that learns the bend, and see why going deeper helps.
- screen：01 · Lines can't bend（4 words）
- screen：02 · Build a small network（5 words）
- screen：03 · Why go deep?（4 words）
- screen：04 · AlexNet, 2012（3 words）
- screen：Prereqs: Gradient descent（3 words）
- screenshot：``

## c_problem（chapter card）
- Lines can't bend
- screenshot：``

## s2 Lines can't bend
### l07（6.9s）
- narration：Here's some made-up data: the same 5-kilometer ride, 48 times, at different hours of the day.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [h2 54px] Same 5 km（3 words）
- [h2 54px] 48 rides（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：2 blocks，5 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l07.png`
### l08（4.6s）
- narration：Daytime runs about $23, just what our two-knob machine charges.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [h2 54px] Same 5 km（3 words）
- [h2 54px] 48 rides（2 words）
- [h2 54px] Daytime ≈ $23（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [caption 28px] Daytime（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：4 blocks，8 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l08.png`
### l09（6.9s）
- narration：Around 8 a.m. and 6 p.m. it spikes, and late at night it's a bit pricier.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [h2 54px] Same 5 km（3 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [h2 54px] 48 rides（2 words）
- [caption 28px] Late night（2 words）
- [h2 54px] Daytime ≈ $23（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [caption 28px] Daytime（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：7 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l09.png`
### l10（7.7s）
- narration：Same two knobs, one for height and one for slope, but now we feed it the time, not the distance.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [div 25px] Height（1 words）
- [div 25px] Slope（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [div 42px] 33.0（1 words）
- [div 42px] 0.55（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：7 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l10.png`
### l11（6.2s）
- narration：However you turn them, the best you get is a nearly flat line through the middle.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [div 25px] Height（1 words）
- [div 25px] Slope（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [div 42px] 26.6（1 words）
- [div 42px] -0.07（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：7 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l11.png`
### l12（7.7s）
- narration：It's too cheap at rush hour and too pricey by day, and its loss can't get below 11.5.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [div 25px] Height（1 words）
- [div 25px] Slope（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [div 42px] 26.6（1 words）
- [div 42px] -0.07（1 words）
- [chart 24px] 20（1 words）
- [eyebrow 22px] Lowest loss（2 words）
- [div 110px] 11.5（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：8 blocks，11 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l12.png`
### l13（5.8s）
- narration：The knobs aren't the problem: this machine only draws straight lines, and the pattern bends.
- [eyebrow 22px] 01 · Lines can't bend（4 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush（2 words）
- [caption 28px] Morning rush（2 words）
- [h1 64px] Lines can’t bend（3 words）
- [caption 28px] Late night（2 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：4 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s2_l13.png`

## c_experiment（chapter card）
- Build a small network
- screenshot：``

## s3 Build a small network
### l14（4.6s）
- narration：The fix isn't one big machine. It's lots of simple little ones.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [h1 76px] Lots of simple units（4 words）
- total（excl. eyebrow & chart）：1 blocks，4 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l14.png`
### l15（6.9s）
- narration：Each unit still has two knobs and draws a line, plus one rule: anything below zero becomes zero.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [div 25px] How steep（2 words）
- [div 25px] Where it bends（3 words）
- [chart 26px] 0（1 words）
- [div 42px] 1.6（1 words）
- [div 42px] -0.4（1 words）
- [h2 54px] Below zero → zero（3 words）
- total（excl. eyebrow & chart）：5 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l15.png`
### l16（3.1s）
- narration：So its line stays flat, then bends upward.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [div 25px] How steep（2 words）
- [div 25px] Where it bends（3 words）
- [chart 26px] 0（1 words）
- [div 42px] 1.6（1 words）
- [div 42px] -0.4（1 words）
- [h2 54px] A line with one bend（5 words）
- total（excl. eyebrow & chart）：5 blocks，12 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l16.png`
### l17（3.8s）
- narration：The two knobs set where it bends and how steeply.
- screen unchanged from previous line
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l17.png`
### l18（5.0s）
- narration：One bend isn't enough, so add more units that bend in different spots.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [span 76px] +（0 words）
- [span 76px] +（0 words）
- total（excl. eyebrow & chart）：2 blocks，0 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l18.png`
### l19（4.6s）
- narration：Add them up, and you can build bumps, steps, almost any curve.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [span 76px] +（0 words）
- [span 76px] +（0 words）
- [span 76px] =（0 words）
- [h2 54px] Add bends → bumps, steps…（4 words）
- total（excl. eyebrow & chart）：4 blocks，4 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l19.png`
### l20（6.9s）
- narration：Our network has 12 units side by side in the first layer, and one unit in the second.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 30px] Time（1 words）
- [chart 30px] Fare（1 words）
- [caption 28px] Layer 1 · 12 units（4 words）
- [caption 28px] Layer 2 · 1 unit（4 words）
- total（excl. eyebrow & chart）：2 blocks，8 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l20.png`
### l21（7.3s）
- narration：That one weighs each bent line with its own knob, adds one more knob, and out comes the fare.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [h1 76px] A knob for each（4 words）
- [h2 54px] Plus one more → fare（4 words）
- [chart 30px] Time（1 words）
- [chart 30px] Fare（1 words）
- [caption 28px] Layer 1 · 12 units（4 words）
- [caption 28px] Layer 2 · 1 unit（4 words）
- total（excl. eyebrow & chart）：4 blocks，16 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l21.png`
### l22（1.9s）
- narration：That's 37 knobs in total.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [display 180px] 37（1 words）
- [h2 54px] knobs（1 words）
- [chart 30px] Time（1 words）
- [chart 30px] Fare（1 words）
- [caption 28px] 12 × 2 + 12 + 1（4 words）
- [caption 28px] Layer 1 · 12 units（4 words）
- [caption 28px] Layer 2 · 1 unit（4 words）
- total（excl. eyebrow & chart）：5 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l22.png`
### l23（5.0s）
- narration：Layers of little units like this are what we call a neural network.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [h1 76px] Neural network（2 words）
- [h2 54px] Layers of small units（4 words）
- [chart 30px] Time（1 words）
- [chart 30px] Fare（1 words）
- [caption 28px] Layer 1 · 12 units（4 words）
- [caption 28px] Layer 2 · 1 unit（4 words）
- total（excl. eyebrow & chart）：4 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l23.png`
### l24（7.7s）
- narration：The name comes from neurons in the brain, but don't take that too seriously: it's just little units with knobs.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [h1 76px] Neural network（2 words）
- [h2 54px] Layers of small units（4 words）
- [caption 28px] Named after neurons · loosely（4 words）
- [chart 30px] Time（1 words）
- [chart 30px] Fare（1 words）
- [caption 28px] Layer 1 · 12 units（4 words）
- [caption 28px] Layer 2 · 1 unit（4 words）
- total（excl. eyebrow & chart）：5 blocks，18 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s3_l24.png`

## s4 Training
### l25（6.9s）
- narration：To turn all thirty-seven, we use last episode's trick, nudging every knob whichever way drops the loss fastest.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] 37 knobs（2 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [chart 24px] 30（1 words）
- [chart 24px] 20（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：0 blocks，0 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l25.png`
### l26（5.8s）
- narration：It starts as a random squiggle, and step by step it bends toward the peaks.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] 37 knobs（2 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [chart 24px] 30（1 words）
- [eyebrow 22px] Loss（1 words）
- [chart 24px] 20（1 words）
- [div 110px] 0.87（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：1 blocks，1 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l26.png`
### l27（8.1s）
- narration：After 10,000 steps, the loss is down to 0.26, while the best straight line managed 11.5.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] 37 knobs（2 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [chart 24px] 30（1 words）
- [eyebrow 22px] Loss（1 words）
- [chart 24px] 20（1 words）
- [div 110px] 0.26（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [h2 54px] Best line: 11.5（3 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：2 blocks，4 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l27.png`
### l28（3.5s）
- narration：Rush hours and late nights, it catches them all.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] 37 knobs（2 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush ✓（2 words）
- [caption 28px] Morning rush ✓（2 words）
- [caption 28px] Late night ✓（2 words）
- [chart 24px] 30（1 words）
- [eyebrow 22px] Loss（1 words）
- [chart 24px] 20（1 words）
- [div 110px] 0.26（1 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [h2 54px] Best line: 11.5（3 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：5 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l28.png`
### l29（5.0s）
- narration：And every corner on this curve is one little unit making its bend.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] 37 knobs（2 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush ✓（2 words）
- [caption 28px] Morning rush ✓（2 words）
- [caption 28px] Late night ✓（2 words）
- [chart 24px] 30（1 words）
- [eyebrow 22px] Loss（1 words）
- [chart 24px] 20（1 words）
- [div 110px] 0.26（1 words）
- [caption 28px] Each corner = one unit（4 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [h2 54px] Best line: 11.5（3 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：6 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l29.png`
### l30（5.4s）
- narration：How we work out which way each knob should turn is next episode's story.
- [eyebrow 22px] 02 · Build a small network（5 words）
- [chart 28px] Fare ($)（1 words）
- [eyebrow 22px] Illustration（1 words）
- [chart 24px] 40（1 words）
- [caption 28px] Evening rush ✓（2 words）
- [h1 76px] Which way to turn?（4 words）
- [caption 28px] Morning rush ✓（2 words）
- [caption 28px] Late night ✓（2 words）
- [chart 24px] 30（1 words）
- [h2 54px] Next episode（2 words）
- [chart 24px] 20（1 words）
- [caption 28px] Each corner = one unit（4 words）
- [chart 24px] 0（1 words）
- [chart 24px] 6（1 words）
- [chart 24px] 12（1 words）
- [chart 24px] 18（1 words）
- [chart 24px] 24（1 words）
- [chart 28px] Time of day (h)（4 words）
- total（excl. eyebrow & chart）：6 blocks，16 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s4_l30.png`

## c_lens（chapter card）
- Why go deep?
- screenshot：``

## s5 Why go deep?
### l31（4.6s）
- narration：So far, our units sat side by side, each adding one bend.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h1 76px] Side by side: one bend each（6 words）
- total（excl. eyebrow & chart）：1 blocks，6 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l31.png`
### l32（6.2s）
- narration：Now stack them instead, so each layer folds the line it gets from the layer before.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h1 76px] Stacked: fold again（3 words）
- total（excl. eyebrow & chart）：1 blocks，3 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l32.png`
### l33（6.2s）
- narration：In a worked example, two units per layer can fold a slanted line exactly in half.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h1 76px] Stacked: fold again（3 words）
- [display 160px] 2（1 words）
- [h2 54px] pieces（1 words）
- [caption 28px] 2 units per layer · worked example（6 words）
- total（excl. eyebrow & chart）：4 blocks，11 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l33.png`
### l34（6.2s）
- narration：One layer gives two pieces, two layers give four, and each new layer can double it.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h1 76px] Stacked: fold again（3 words）
- [display 160px] 32（1 words）
- [h2 54px] pieces（1 words）
- [caption 28px] 2 units per layer · worked example（6 words）
- total（excl. eyebrow & chart）：4 blocks，11 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l34.png`
### l35（6.9s）
- narration：So ten units side by side give at most 11 pieces. Stacked five deep, they can give 32.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h2 54px] 10 side by side: ≤ 11（5 words）
- [h2 54px] 10 in 5 layers: 32（5 words）
- total（excl. eyebrow & chart）：2 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l35.png`
### l36（3.1s）
- narration：Later layers reuse what earlier ones already folded.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [h2 54px] 10 side by side: ≤ 11（5 words）
- [h2 54px] 10 in 5 layers: 32（5 words）
- [h2 54px] Later layers reuse earlier folds（5 words）
- total（excl. eyebrow & chart）：3 blocks，15 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l36.png`
### l37（5.8s）
- narration：So the deeper the stack, the more complex the shapes the same units can build.
- screen unchanged from previous line
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l37.png`
### l38（2.3s）
- narration：That's the "deep" in deep learning.
- [eyebrow 22px] 03 · Why go deep?（4 words）
- [display 150px] Deep learning（2 words）
- [h1 76px] Many layers deep（3 words）
- total（excl. eyebrow & chart）：2 blocks，5 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s5_l38.png`

## c_real（chapter card）
- AlexNet, 2012
- screenshot：``

## s6 AlexNet, 2012
### l39（5.8s）
- narration：In 2012, three researchers at the University of Toronto trained a very deep neural network.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [eyebrow 22px] 2012 · University of Toronto（4 words）
- [display 190px] AlexNet（1 words）
- total（excl. eyebrow & chart）：1 blocks，1 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l39.png`
### l40（5.4s）
- narration：They were Krizhevsky, Sutskever and Hinton, and the network later became known as AlexNet.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [eyebrow 22px] 2012 · University of Toronto（4 words）
- [display 190px] AlexNet（1 words）
- [h2 54px] Krizhevsky · Sutskever · Hinton（3 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：3 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l40.png`
### l41（7.3s）
- narration：It had 8 layers and 60 million knobs, and learned 1,000 categories from 1.2 million photos.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [div 16px] 8layers（1 words）
- [div 16px] 60Mknobs（1 words）
- [div 16px] 1.2Mphotos（1 words）
- [div 16px] 1,000categories（1 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：5 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l41.png`
### l42（7.3s）
- narration：At that year's ImageNet contest, it got five guesses per picture, and only missed if all five were wrong.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [h1 76px] ImageNet contest, 2012（3 words）
- [h2 54px] 5 guesses; all wrong = a miss（6 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：3 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l42.png`
### l43（8.1s）
- narration：A version of it had a 15.3% error rate, against 26.2% for the runner-up.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [h1 76px] ImageNet contest, 2012（3 words）
- [h2 54px] 5 guesses; all wrong = a miss（6 words）
- [chart 60px] 15.3%（1 words）
- [chart 54px] AlexNet（1 words）
- [chart 60px] 26.2%（1 words）
- [chart 54px] Runner-up（1 words）
- [chart 28px] Error rate (top-5)（3 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：3 blocks，14 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l43.png`
### l44（8.5s）
- narration：Nobody told it what to look for, yet its first layer learned to spot stripes at all angles, and patches of color.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [eyebrow 22px] Illustration（1 words）
- [eyebrow 22px] Nobody taught it（3 words）
- [h1 76px] Layer 1: stripes, colors（4 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：2 blocks，9 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l44.png`
### l45（3.1s）
- narration：Later layers built on those, layer by layer.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [chart 54px] 1（1 words）
- [chart 54px] 2（1 words）
- [chart 54px] 3（1 words）
- [chart 54px] 4（1 words）
- [chart 54px] 5（1 words）
- [chart 54px] 6（1 words）
- [chart 54px] 7（1 words）
- [chart 54px] 8（1 words）
- [h2 54px] Built up layer by layer（5 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：2 blocks，10 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l45.png`
### l46（5.0s）
- narration：They also found that removing any middle layer cost about 2 percentage points.
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [chart 54px] 1（1 words）
- [chart 54px] 2（1 words）
- [chart 54px] 3（1 words）
- [chart 54px] 4（1 words）
- [chart 54px] 5（1 words）
- [chart 54px] 6（1 words）
- [chart 54px] 7（1 words）
- [chart 54px] 8（1 words）
- [h2 54px] Remove a middle layer → about −2 points（7 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：2 blocks，12 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l46.png`
### l47（3.8s）
- narration：As the paper put it, "the depth really is important."
- [eyebrow 22px] 04 · AlexNet, 2012（3 words）
- [eyebrow 22px] From the paper（3 words）
- [display 104px] “The depth really / is important”（5 words）
- [div 22px] Krizhevsky et al. 2012 · §7（5 words）
- [div 22px] Krizhevsky et al. · NIPS 2012（5 words）
- total（excl. eyebrow & chart）：3 blocks，15 words
- screenshot：`edu_videos/ai_terms/t12_neural_networks/reviews/lines_r1/materials/screen/en/s6_l47.png`

## s7 Outro (on screen: end card)
### outro（package card, whole segment 22.6s）
- narration l48: So a neural network is just simple little units with knobs, stacked layer on layer.
- narration l49: Stack them deep enough, and they can recognize really complicated things.
- narration l50: Thirty-seven knobs is easy, but AlexNet had sixty million, so how do you work out which way each one turns?
- narration l51: That's backpropagation, coming up next time.
- screen：Simple units, stacked in layers Deep enough to see more（10 words）
- screen：Backpropagation（1 words）
- screenshot：``

