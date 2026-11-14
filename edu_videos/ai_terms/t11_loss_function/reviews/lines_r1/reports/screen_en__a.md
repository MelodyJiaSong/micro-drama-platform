# screen_en__a (slot a, claude-sonnet-5-5), round 1

## 评分表
- P1 2 证据：Hard limits mostly hold: l29/l30 about 19 words across 4 blocks, l36 21 words (limit 22), l41 16 words, titles all ≤6 words (l37 "The loss function / = what “good” means" is exactly 6). No narration sentences on screen. Small flaws: l34 h2 "Doesn't know what a taxi is" is a clause; l19 sits at the block ceiling (chart, dials, h1, score card with a separate h2 "✗ They cancel out"); l36 at 21/22 words.
- P2 1 证据：l19 screen shows "−0.33" while narration says "about −$0.30": the numbers contradict. Also near-verbatim echoes: l07 "Lower is better" / "0 = not wrong at all" (narration: "lower is better, and zero means not wrong at all"); l34 "Doesn't know what a taxi is" (narration: "has no idea what a taxi is"); l40 "sure" on screen vs "confident" in narration.
- P3 2 证据：Eyebrow numbering "01 · What is a loss function?" … "04 · How big models are scored" matches the chapter cards. Never more than 3 levels. Weak spots: l41 the display line "Twinkle, twinkle, little star" (96px) outranks the h1 takeaway "Less sure, bigger penalty" at the bottom; chapter-card titles are not parallel (see issue table); l25 shows "Try 3" twice (h1 and table row).
- P4 1 证据：Outro "Score the mistakes / Training pushes it down" is an imperative next to a declarative (not parallel, and the imperative misdescribes the idea). Chapter card "The score is all it sees" is a full sentence among a question and noun phrases. l46 "Tens of billions" has no noun beside "2 knobs". Chinese "损失函数" sits in the English track (l04, l42). Elsewhere punctuation is clean: no trailing periods, proper minus signs, sentence case.
- P5 3 证据：Most screens carry 4–9 words and stay 4–10 s (l38 "Language models / Scored in training, too" 6 s; l21 13 words in 6.9 s, about 2 words/s). The densest, l36 (21 words, 6.2 s, mostly short chart labels) and l41 (16 words, 7.7 s), are still readable. The only worry is the l19 "Too low −" callout, which covers a data point.
- P6 3 证据：Every breach or awkward phrase below has a drop-in rewrite of the same or shorter length.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| outro | P4 | 必改 | "Score the mistakes" / "Training pushes it down" | Outro is a strict item. Lines are not parallel (imperative vs declarative); "Score the mistakes" reads as an instruction to the viewer and drops the key takeaway "lower is better" from l47. | "Loss: a score for mistakes" / "Training: push it down" |
| l19 | P2 | 必改 | "−0.33" (card "Plain average error") | Contradicts narration "about −$0.30". | Make both match: show "−$0.30" or have narration say "about −33 cents". |
| c_lens | P4 | 必改 | "The score is all it sees" | Chapter title (strict). A full sentence next to "What is a loss function?", "A small experiment", "How big models are scored"; also repeated as the eyebrow on 7 screens. | "All the model sees" (or "What the model sees") |
| s0_l04 / l42 | P4 | 必改 | "A score for mistakes" + "损失函数" (l04); "交叉熵" (l42) | Chinese gloss in the English-track slide. If the English cut is for English viewers this is stray text; l04 is the cold open (strict). Also it is not counted in the word totals. | Drop the Chinese lines on the English version. If kept on purpose, state so and treat it as a note, not a title. |
| l46 | P4 | 建议 | "Tens of billions" (beside "2 knobs") | Missing noun, not parallel with "2 knobs". | "Billions of knobs" or "Tens of billions of knobs" (4 words) |
| l37 | P4 | 建议 | "The loss function / = what “good” means" | The "=" reads awkwardly aloud; this is the chapter's closing line. | "Loss defines “good”" |
| l36/l35 | P4 | 建议 | "Score it, shape it" | Cute, vague, and the sound-alike phrasing carries no concrete claim. | "How you score shapes learning" (4) or "Score shapes learning" |
| l34 | P2 | 建议 | "Doesn't know what a taxi is" | Clause echoing the narration; not an outline fragment. | "No idea what a taxi is" or "Knows no taxis" |
| l07/l08 | P2 | 建议 | "0 = not wrong at all" | Near-verbatim narration. | "0 = no error" (l08's 4-block stack is at the limit; this also lowers the word count from 13 to 11) |
| l19 | P5 | 建议 | "Too low −" | Callout overlaps a data point in the screenshot. | Move the label above or beside the dot. |
| l40 | P2 | 记录 | "Less sure, bigger penalty" | Narration uses "confident"; screen uses "sure". Keep one term (l41 "90% sure" fits the screen). | Change narration to "sure", or screen to "Less confident, bigger penalty" (4 words) |
| l41 | P3 | 记录 | "Twinkle, twinkle, little star" (96px) over the h1 at the bottom | Quote outranks the takeaway. | Keep the quote and shrink it, or move the takeaway above the bars. |
| outro | P2 | 记录 | "Next · Gradient descent" shown for all 25.3 s | Gives away the answer before l49 poses the question "which way do you turn?" | Reveal "Next · Gradient descent" only at l50. |
| l25 | P3 | 记录 | h1 "Try 3" plus table row "Try 3 2.19" | Duplicate label. | Drop the h1 "Try 3" or highlight the row only. |

## 整体观察
- Biggest change from the previous version: slides are now mostly short fragments, and no screen repeats a full narration sentence. P1 and P5 are healthy.
- The remaining must-fixes are strict items (outro, a chapter title, the Chinese gloss in the cold open) plus the numeric mismatch on l19.
- Word counts, using the round-2 rules (charts count, tick numbers exempt), stay under 22 everywhere; the tightest is l36 at 21.
- Keep: l05 "How far off = error", l06 "Errors → one score" and l09 "Turn, then check". These are clean outlines that add structure instead of echoing the narration.
- Keep: the l41 bar pairs ("90% sure / Penalty 0.11" against "10% sure / Penalty 2.30"), a parallel look-alike list that carries the contrast.
- Keep: the l25 scoreboard (Try 1 78 / Try 2 13.4 / Try 3 2.19 in green) for a one-glance conclusion.
