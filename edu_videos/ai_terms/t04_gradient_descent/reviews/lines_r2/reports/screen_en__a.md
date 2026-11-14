# screen_en__a (a · claude-sonnet-5-5), round 2

## 评分表

- P1 1 证据：three hard-limit breaches remain. l20/l21 hold about 23 words (charts 6 + knobs 6 + 78/0 2 + "Nudge +$0.10, score" 3 + "Score"/"Steps" 2 + "Base fare −1.7"/"Per km −11.2" 6 = 25; 23 even if Score/Steps are exempt) against a limit of 22. l38/l39 hold 24 words (title 3 + panel names 6 + settings 3 + scores 3 + outcomes "Still far off / Made it / Off the map" 8 + "Score" 1), and l39 holds the screen for 5.8s. l15 has 5 text blocks (h1 "Learning rate", h2 "Step size", h2 "Set before training", knob row, loop row) against a limit of 4. Everything else is genuinely an outline: l09, l10, l24, l33 and l45 are all keyword-sized.
- P2 2 证据：the screen is almost always a label or number, not a narration sentence: l44 "≈ 1/100,000 of the training data", l46 "GPT-3 / Adam; Llama / Adam, tweaked". Minor blemishes: l47 "One small step at a time" is verbatim from narration (l47); l42/l43 eyebrow "Illustration · 3 rides a step" brings in "rides", a unit narration never explains; l14 narration defines "Gradient descent" but the screen still reads "The gradient"; l30 and l31 show "2.0" with no "Score" label, because narration at l30/l31 never says score either.
- P3 2 证据：chapter eyebrows match the cards ("01 · Downhill, blindfolded", "02 · A small experiment", "03 · How big a step?", "04 · Training giant models"), Score/Steps/Lowest point are used the same way l18–l29, and "Learning rate" now leads at l15 (the term first, in h1). Remaining flaws: l12 still puts the term "The slope underfoot" in the smallest eyebrow with the paraphrase "Nudge → score change" as headline (the r1 l13/l15 problem, unfixed here); the four chapter titles use four different forms (noun phrase, noun phrase, question, gerund phrase).
- P4 2 证据：sentence case throughout; the cold open pair "Lower = better" / "Lowest = best", "Which way down?" and "Billions of knobs: no map" are all natural spoken English. Flaws: "Nudge +$0.10, score" (l19/l20) is a dangling-comma header; "Wobbly, but gets near" (l43) ends on a bare "near"; "of the training data" (l44) begins with a preposition. The chapter titles all read aloud fine.
- P5 2 证据：the screenshots s2_l14, s3_l20 and s4_l38 are legible at 1080p and the hierarchy is clear. The tight spots are l03 (new h2 "2 knobs: easy to map", 5 words in 1.9s, about 2.6 words/s while also reading subtitles) and l38 (24 words, new title plus outcome captions; the screen then stays 5.8s into l39). l20 is 8.5s so its 23 words are readable in time. Nothing is clipped; the cold-open axis title now survives the fade (s0_l04).
- P6 2 证据：every breach below has a drop-in rewrite, and the l20 and l38 rewrites bring them to 21 and 22 words. The outro rewrite cannot be checked against a screenshot (none supplied), so it is stated conditionally.
- R 2 证据：most round-1 screen_en issues are resolved, but the l20 word-count breach (I13/I14) and the l38 word-count breach (I26/I27) are not. Details are in the R table below.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l20 / l21 | P1 | 必改 | Chart "Per km / Base fare / Lowest point"; knobs "Base fare / Per km / $5.00 / $2.00"; "Score 78 / Steps 0"; header "Nudge +$0.10, score"; rows "Base fare −1.7" / "Per km −11.2" | About 23 words by the round-2 rules (the Nudge header counts with the table; 25 if Score/Steps count), over the 22 limit. "Base fare" and "Per km" are printed three times (axis, knob, result row), and l21 holds the screen 4.6s more | Drop the knob captions while the result rows are on screen (they label the same two knobs): the screen then reads about 19 words. Header: "Nudge +$0.10 → score" |
| l38 / l39 | P1 | 必改 | "The key setting" + 3 panel names + 3 settings + scores + "Still far off / Made it / Off the map" + "Score" | 24 words, over 22, and l39 holds this screen for 5.8s. Down from 26 in round 1 but not fixed | "Far off / Made it / Off the map" (-1) and drop the lone "Score" label (-1) = 22; better, also drop "Just right" repetition by moving the green outline to carry it |
| l15 | P1 | 必改 | h1 "Learning rate" / h2 "Step size" / h2 "Set before training" + knob row + loop row | 5 text blocks (limit 4); knob row and loop row are leftovers from l14 while the point is the term | Remove the knob row at l15, or merge: "Learning rate" / "Step size, set before training" (2 h-blocks + loop row) |
| l14 | P2 / P3 | 建议 | h1 "The gradient" / "Fastest way down" | Narration at l14 is "Gradient descent turns all the knobs one small step that way"; the term being named is not on screen. The screen is the l13 screen plus the loop pills | h1 "Gradient descent", sub "Turn, check, repeat" (keep the loop pills) |
| l12 | P3 | 建议 | eyebrow "The slope underfoot" over h2 "Nudge → score change" | The metaphor-to-model term sits in the smallest text and the explanation reads first. This is the r1 I11 hierarchy fault, fixed at l13/l15 but not here | h1 "The slope", sub "Nudge → score change" (the r1 judge's collision warning concerned "Slope underfoot" as a replacement for l09, not this) |
| l19 / l20 | P4 | 建议 | "Nudge +$0.10, score" | Dangling-comma header that ends on "score"; reads as a cut-off sentence | "Nudge +$0.10 → score" |
| l42 / l43 | P2 | 建议 | eyebrow "Illustration · 3 rides a step" | "rides" and "3 per step" never appear in narration; the viewer cannot decode it, and it adds a claim narration does not make | "Illustration" (or "Illustration · 3 rides per batch" if the number must stay) |
| l43 | P4 | 建议 | "Wobbly, but gets near" | "Gets near" hangs without an object; narration says "near the bottom" | "Wobbly, but near the bottom" (5) |
| l43 | P5 | 存疑 | legend "All data" (grey) | The legend names a grey path but none is visible in s5_l43 (only the purple path is drawn); it looks like a legend for something missing | Draw the grey full-data path faintly, or drop the legend |
| l30 / l31 | P3 | 建议 | "2.0" under the "Just right 0.005" panel | A bare number with no label; the "Score" label does not appear until l32 | Add a small "Score" label at l30 where "2.0" first appears (move the l32 label forward) |
| l03 | P5 | 建议 | "2 knobs: easy to map" (1.9s) | 5 new words in 1.9s next to burned-in subtitles; about 2.6 words/s | Keep as is if the previous h1 stays still; or "2 knobs: easy" (3) |
| l47 | P2 | 记录 | "One small step at a time" | Verbatim from narration ("one small step at a time"); acceptable as the close, but it is a repeat | Keep, or "Small steps" |
| outro | P4 | 存疑 | "Steepest way down" / "Step size = learning rate" / "Neural networks" | Strict item. No screenshot, so I cannot confirm layout or that the "Next" label exists; "Neural networks" alone reads like a third recap point. The recap also omits the term "gradient descent" | "Gradient descent: steepest way down" / "Step size = learning rate" / "Next: neural networks" (7 + 3 words) |

### R: recheck of round-1 screen_en issues (author's handling)

| 编号 | 复核 |
|---|---|
| I1 outro | 已解决 (now 7 words, no longer narration copy); the "Next" label is unverified, see outro row above |
| I2, I4 chapter 04 | 已解决 ("Training giant models"; no more "How big" triple) |
| I3 "Downhill, blindfolded" | 不采纳 reason holds: reads naturally aloud |
| I5, I6 l01 | 已解决 ("Lower = better") |
| I7 l04 | 已解决 ("Billions of knobs: no map") |
| I8 axis title | 已解决 (s0_l04 shows "Per km ($)" clearly) |
| I9 l06 | 已解决 ("Which way down?") |
| I10 l09 | 不采纳 reason holds; "Feet feel the slope" is a valid outline |
| I11, I12 l13/l15 | 已解决 (term now in h1); l12 still has the problem, listed above as a new row |
| I13, I14 l20/l21 | 未解决: moved the nudge value into a header but the screen is still about 23 words (25 counting every label) |
| I15 l22 | 不采纳 reason holds |
| I16, I17 l23 | 已解决 ("Valley in 3 steps") |
| I18, I19 l24 | 已解决 / 不采纳 reason holds |
| I20 l27 | 不采纳 holds |
| I21, I22 l30 | 已解决 ("Wrong learning rate?") |
| I23 l33 | 已解决 ("Still far off") |
| I24 | 已解决 (single "Score"), but it exposed the unlabeled "2.0" at l30/l31 (new) |
| I25 l36 | 已解决 (↑ on step 5) |
| I26, I27 l38 | 未解决: 24 words (was 26), still over 22 |
| I28, I29 l40 | 已解决 (s5_l40 balanced cards) |
| I30 l42 | 改出新问题: "3 rides a step" moved to the eyebrow but is still undefined |
| I31, I32 l43 | 已解决, with a small new nit ("gets near") |
| I33, I34 l45 | 已解决 |
| I35 l45 | 已解决 |
| I36, I37 l47 | 已解决 (now a verbatim echo, 记录 level) |
| I38 outro | see I1 |

## 整体观察

- Biggest remaining defects are word-count breaches on dense accumulated screens (l20/l21, l38/l39) plus one block-count breach (l15), all caused by leftovers carried forward from earlier lines.
- Chapter titles and cold open are in good shape; no strict-item wince except the unverifiable outro (no screenshot).
- Terms follow narration, except l14 ("gradient descent" not on screen) and the l12 hierarchy.
- Works, keep: (1) the l31–l39 three-panel "Too small / Just right / Too big" structure with numbers instead of sentences; (2) the cold-open pair "Lower = better" / "Lowest = best" and "2 knobs: easy to map" / "Billions of knobs: no map"; (3) l44 "≈ 1/100,000" and l47 "175 billion knobs" as big-number slides.
