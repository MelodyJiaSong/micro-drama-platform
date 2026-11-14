# screen_en__a (reviewer a, claude-sonnet-5-5) — English on-screen text, round 1

Method: read screen_en.md in full; opened screenshots s0_l04, s4_l33, s5_l40. Word counts below are my own recount under the round-2 ruling. The materials double-count some spans on l32-l34 ("years, for one step" counted twice), so I deduplicated.

## 评分表
- P1 1 证据：Hard limits are broken on the network and bar screens. l25 28, l26 32, l27 33, l28 31, l30 27 words (limit 22). l33 about 23 and l34 about 25 words after deduplication. l36 and l38 have 5 text blocks (limit 4). The outro title is 9 words (limit 6). The agenda has 23 words (limit 22).
- P2 2 证据：Most slides carry structure and numbers, not narration, e.g. l14 "2 × 3 = 6", l31 "1,000,000,001 runs". But l09 "Gradient: which way to turn" and l10 "Rerun, see if the error moved" restate the narration. The outro "Pass the blame back, every knob in one trip" repeats l41–l42. l40 uses "Autograd" while the narration says "automatic differentiation", and "=" claims more than "underneath, it's…".
- P3 2 证据：Eyebrow, chapter title and agenda items match exactly ("01 · Too many knobs to try"), and the formulas are parallel ("Blame = error × input" / "Passed back = error × knob"). But on l29/l30 the column heads "Nudge one by one" and "Backpropagation" sit at eyebrow size (22px), and on l40 the h1 "Autograd = Backpropagation" (76px) sits below an h2 (54px).
- P4 2 证据：Sentence case, no trailing periods, en dash in "533–536". Weak spots: l04 eyebrow "One trip backward, all of them" (dangling), l03 "One by one? Never ends" (clipped), "Tried 9" (unexplained), l17 "Error ← flows back" (arrow plus verb), outro "Pass the blame back, every knob in one trip" (run-on).
- P5 2 证据：Most screens build incrementally, so new text per line is small (l33 adds one row in 3.8s, l34 changes only the title in 3.1s). l33 is readable in the screenshot. But l26 adds four numbers in 5.4s over a 25-block diagram, and l40 holds four items including a 9-word caption in 5.0s.
- P6 2 证据：Every flagged word-wise breach has a drop-in rewrite below. The l25–l28 diagram screens cannot be fixed by wording alone: node and arrow numbers push them over 22 words, so a decision is needed on whether node values count (see issue 1).

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| outro | P1/P2/P4 | 必改 | "Pass the blame back, every knob in one trip" + "Overfitting" | Strict item. 9-word title (limit 6). It is a comma-spliced sentence repeating l41–l42 almost verbatim. "Overfitting" alone does not say it is the next topic. | "Blame flows back, one trip" (5 words) / "Next: Overfitting" |
| l04 | P4 | 必改 | eyebrow "One trip backward, all of them" | Strict (cold open). The eyebrow carries the real message but "all of them" dangles and repeats the narration. | "All knobs, one trip back" |
| l03 | P4/P2 | 必改 | "One by one? Never ends" + "Tried 9" | Strict (cold open). "Never ends" is clipped. "Tried 9" is unexplained and the narration never mentions 9 (a new claim, or an unlabelled counter). | "One at a time? Never finishes" / drop "Tried 9", or label it "Tried: 9 knobs" |
| agenda | P1/P2 | 必改 | 4 items + "Prereqs: Neural networks & deep learning" | Strict (linking). 23 words (limit 22). "Prereqs" is jargon. Item 04 "From 1986 to today" is not previewed in the narration (l06 covers items 01–03 only). | "Last time: Neural networks" and shorten items: "Too many knobs", "Working backward", "A small experiment", "1986 to today". Or add item 04 to l06 |
| l25–l28 | P1 | 必改 | network diagram, 28 / 32 / 33 / 31 words | Over 22 words per screen once in-chart numbers are counted (chart counts as one block, so blocks are fine). Node values (60, 12, 30, 6…) are real content, but the rule exempts only axis ticks. | Ask the ruling owner whether node values count. If yes, hide unused weights or fade earlier nodes, e.g. on l26 keep only the new numbers at full strength and drop "×2 ×1 +1" labels already shown |
| l30 | P1/P3 | 必改 | h1 + two column heads + 14 numbers + "1 forward + 1 back" + "✓ Same seven numbers" (27 words) | Over 22 words. The column heads "Nudge one by one" and "Backpropagation" sit at eyebrow size (22px), so they are a content row dressed as a label and would count. | Keep one copy of the seven numbers shown side by side and drop the duplicate, or shorten "1 forward + 1 back" to "2 passes" |
| l33, l34 | P1 | 必改 | "A billion knobs / Nudge one by one / 1,000,000,001 runs / At 1 second a run / ≈ 31.7 years, for one step / Backpropagation / ≈ 3 runs' worth" | About 23 words on l33, 25 on l34 (limit 22). l34's title "Without it: no big models" also uses an ambiguous "it" and echoes the narration. | Shorten row 2 to "1 s per run: ≈ 31.7 years"; title l34 "No backprop, no big models" |
| l36 | P1 | 必改 | 1986, paper title, authors, "Forward pass →", "← Backward pass" | 5 text blocks (limit 4). | Merge year, title and authors into one "paper card" block |
| l38 | P1 | 必改 | 1986, title, authors, "Middle units: learn features", "Similar methods came earlier" | 5 text blocks (limit 4). | Merge the paper card into one block as above, or drop the caption |
| l17 | P4 | 建议 | "Error ← flows back" | Arrow and verb say the same thing. | "Error flows back" or "← Error" |
| l40 | P2/P3 | 建议 | "Autograd = Backpropagation" and 9-word caption | "Autograd" is not the narration's term (automatic differentiation). "=" overclaims; the narration says "underneath, it's backpropagation". The h1 sits below an h2. The caption repeats the narration, with "gradients" for "slopes". | "Autograd runs backpropagation" and caption "PyTorch docs: traverse back from the output" |
| l09 | P2 | 建议 | "Gradient: which way to turn" | Almost verbatim from the narration. | "Gradient = slope" |
| l10 | P2 | 建议 | "Rerun, see if the error moved" | Restates the narration. | "Nudge → rerun → compare" |
| l11 | P4 | 建议 | "Billions / for one step" | The big word has no noun; "Billions" of what? | "Billions of reruns / per step" |
| l29 | P3/P5 | 建议 | column head "Nudge one by one" and "Backpropagation" at 22px | Column heads are too small against 44px numbers and the 110px "8". | Raise to h2 size |
| l07/l08 | P2 | 记录 | chart label "Error" while title says "lower the loss" | Two terms for one score. The narration introduces "loss" on l08 but the chart label stays "Error". | Keep, or label the chart "Loss" from l08 on |
| l37 | P2 | 记录 | "Middle units: learn features" | Matches the narration's "units in the middle", but the standard term is "hidden units". | "Hidden units learn features" (if the narration changes too) |

## 整体观察
- Core content is mostly short keywords and numbers; the earlier prose-on-screen problem is mostly gone. The remaining breaches are about screen totals and block counts, not sentences.
- Biggest risk: the strict items (cold open l03/l04, agenda, outro) each have a small defect, and all count as must-fix.
- Rows with numbers do work: the l31–l34 "1,000,000,001 runs / ≈ 31.7 years / ≈ 3 runs' worth" build is readable in the screenshot and the narration doesn't need to repeat the digits.
- Worth keeping 1: the chapter eyebrow ("01 · Too many knobs to try") matches the chapter cards and agenda exactly.
- Worth keeping 2: the parallel formulas "Blame = error × input" / "Passed back = error × knob".
- Worth keeping 3: l31–l34 bar build with the red figures as focal points.
- Decision needed: do node values in network diagrams count toward the 22-word limit? This decides whether l25–l28 are breaches at all.
