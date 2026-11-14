# screen_en__judge ruling (round 1) — English on-screen text (slides)

Judge: screen_en__judge (claude-opus-5-5). Read both reports, screen_en.md, the item brief, and the scene sources `scenes/web/s5–s9.html`. Opened screenshots: card_s1, card_s10, card_c_problem, s2_l10, s3_l18, s4_l20, s4_l23, s5_l27, s5_l29, s6_l31, s6_l34, s6_l35, s7_l37, s7_l39, s8_l43, s8_l47, s8_l48, s8_l49, s9_l53, s9_l55.

Verified from screenshots: l18 title clipped at the right edge ("which does b…"); l31–l35 title clipped ("what happens t…"); l55 third card cut off at the right edge; l37/l39 "?" touches the right edge; l20 wiggly curve exam shows `0.00` while the narration says model two does best (b's catch is real); em dashes "—" on l23, l27, l47/l48, l53 and the agenda note (b's 原文 column misquotes these as en dashes "–"); straight apostrophe on l27/l48 ("he's", "model's") vs curly on l53 ("shouldn’t").

## 裁决

- P4 1 理由：Both reviewers gave 2, but the shared blind spots go past minor flaws. l31–l35 title "As models get more complex, what happens to the errors" is a question with no question mark (s6.html data-en has none). l37–l39 "How many numbers to remember ten points?" is ungrammatical, and it spells out "ten" next to "10 heights" / "10 numbers". l54–l55 "More, and more varied, data" is a stilted spoken parenthetical, and it is not parallel with "Keep a mock exam" / "Put limits on complexity". l43 "50M search terms → 1152 data points" uses an arrow that reads as a conversion, not a mismatch. The l37–l39 tables use hyphen-minus ("-0.49") beside true plus signs. Add a's confirmed items: em dashes against the en-dash house style (l23, l27, l47, l53, agenda), mixed straight/curly apostrophes (l48 vs l53), "vs" (l48) vs "vs." (agenda), and the l29 "all right" calque of 全对. A native editor would wince at several of these, so this is a 1.
- P6 2 理由：Both reports give broad rewrites, but neither earns 3. a claims "every breach" yet has no row for l22 (34 words), l38 (35), l26 (12 blocks) or the apostrophe and "vs" inconsistencies. Some of a's rewrites are worse than the original: l50 "Right clue, wrong setting" misstates shortcut learning, and l52 "Choose models on Valid." reuses the abbreviation a itself flagged. b covers almost every screen, but l02 collapses the "Nearly perfect / Falls apart" contrast that b says to keep. b's l27 "Model: capacity without awareness" is abstract jargon. b's l48 drops "34% vs 1%", the number the screen should carry. Neither report gives a rewrite for the missed P4 items above.

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l31–l35 | P4 | 必改 | "As models get more complex, what happens to the errors" | A direct question with no "?" (also missing in s6.html data-en). The clipping hides this, but fixing the overflow will expose it. It is also a 10-word sentence. | "Complexity vs. error" (3) |
| l37–l39 | P4 | 必改 | "How many numbers to remember ten points?" | Ungrammatical ellipsis (it drops "does it take"). "ten" is spelled out while the same screen shows "10 heights", "10 numbers", "10 → 10". | "Numbers needed for 10 points?" (5) |
| l43 | P4/P2 | 必改 | "50M search terms → 1152 data points" | The arrow reads as "became / mapped to". The point is the mismatch: far more candidates than data points ("With far more terms than data points…"). | "50M search terms vs. 1,152 data points" (keep the two big numbers; replace the arrow with "vs.") |
| l54–l55 | P4 | 必改 | "More, and more varied, data" | A spoken parenthetical with commas, which reads stilted as a heading. It is a noun phrase, while card 1 "Keep a mock exam" and card 3 "Put limits on complexity" are imperatives (not parallel). | "Collect more, varied data" → better "Collect more diverse data" (4) |
| l37–l39 | P4 | 建议 | "+0.11  -0.49  -1.16 … +0.004" | Hyphen-minus "-" sits beside full-width "+" (s7.html `fmt` builds the sign from "-"). "+0.004" breaks the two-decimal column. | Use U+2212 "−0.49", "−1.16"; show "+0.00" (or round to 2 decimals) |
| l47–l48 | P4 | 建议 | "99.9%+" (grey "+" glued after "%") | Non-standard notation. The detached "+" reads like a footnote mark or plus sign. | ">99.9%" |
| c_problem | P4 | 建议 | "What problem is this?" (zh "它在解决什么问题") | Unidiomatic, and it is not parallel with the other cards ("An analogy", "A different lens", "The real-world cost"). The zh line means "What problem does it solve?", which is wrong for overfitting. | "The problem" (zh: "问题是什么") |
| l55 | P4 | 建议 | "Same 10 points: penalize overly complex curves, and it stops chasing the noise" | Switches from an imperative to "it" with no antecedent (the model is never named). | "Same 10 points, complexity penalized" (5) or drop the caption |
| l34–l35 | P5 | 必改 | "Exam error" curve label | The label is clipped at the chart's right edge ("Exam erro") in both screenshots. | Anchor the label left of degree 8 or inside the plot area |
| l34 | P5/P4 | 建议 | "Practice error low, / exam error high" | Renders as three lines with the orphan "low," on its own line, which splits the contrast. | Two balanced lines: "Practice error: low" / "Exam error: high" |

## 驳回

- a l50 改写 "Right clue, wrong setting": This misstates the concept. Shortcut learning means the clue is spurious (sofa, ink marks), not "right". Use b's "Shortcut learning" plus a short contrast, or "Wrong clue, works only here".
- a l52–l54 改写 "Choose models on Valid.": It reuses the clipped "Valid." that a itself flagged. Read as an adjective, "on Valid." is nonsense. Use "Validation: choose model" / "Test: final check".
- b l02 改写 (`Overfitting` / `Your data: nearly perfect` / `New data: falls apart`, remove eyebrow): It rewrites the l01 contrast mid-reveal and breaks the "Nearly perfect / Falls apart" layout that b itself lists under keep. a's fix is better: fade the four lines to 30% as the title lands.
- b c_problem … c_fix (remove the six-label navigation strip, 必改): The progress strip is a navigation component, comparable to ticks or an eyebrow, on a short-hold card. Removing it loses orientation. The real defect is the inconsistent numbering and names (05 vs 06, agenda vs strip), which is fixed by aligning labels, not by deleting them.
- b l48 (the "34% vs 1%" percentages are absent from narration, treated as a P2 problem): The number quantifies the narrated claim "differed widely between hospitals". Carrying numbers is exactly the screen's job under P2, so this is not a new claim. b's rewrite also drops the number and the user-endorsed term "hospital fingerprint". Keep "34% vs. 1% labeled pneumonia".
- b l27 改写 "Model: capacity without awareness": Abstract jargon, harder to parse than the original. a's "Limit: the model doesn't know it's memorizing" (7) is clearer, or shorten it to "Model: memorizes without knowing" (4).
- b l31 改写 "300 trials": This changes the narration's term ("300 random sets of points"). "Trials" is new vocabulary. Use "300 random sets".
- b 原文 for l23, l27, l47, l53 (quoted with en dash "–"): The material and the screenshots show em dashes "—". The misquote hid the dash-style breach that a correctly reported. b's rows otherwise stand.
