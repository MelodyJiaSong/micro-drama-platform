# voice_en__a, round 2 (claude-sonnet-5-5, blind, ear only)

## 评分表
- V1 2 证据：Most lines pass the friend test, e.g. l07 "Say a parent allows one hour of video games a day, and the kid keeps sneaking in more." and l35 "When harm goes over the line, lambda goes up, and safety counts for more." Small dents: l04 "is called constrained optimization" (textbook definition), l34 "take the helpfulness score, and subtract lambda times the harm score" (formula read aloud), l38/l39 "sets how many / how much".
- V2 3 证据：The thread holds from the cold open (l01 "don't let harm cross a line", l02 "never cross this line") through l31 "Back to where we started", l36 "Just like the dot on our mountain", l37 "Prices on rules show up all over AI" and the outro l41 "you don't need a wall". There is no table-of-contents line anywhere, and no "Point one" templates.
- V3 2 证据：Mostly clear. Weak spots: l15 "That's this dot" (the dot was never introduced to an ear-only listener), l31 "a way to train language models called Safe RLHF" (the acronym is never unpacked), l22 "walking along the fence only takes you downhill" (two geometry ideas in 9.6s), and l25 "one point five" reuses the number from l18's price.
- V4 2 证据：Tight overall. l30 "So lambda tells you which rules are really pinning you down." mostly restates l24-l29 and could go. l38 and l39 end the same way ("a price like this sets how many / how much"), which is mild repetition.
- V5 2 证据：One warm, plain narrator with varied length (l12 3.1s, l19 3.5s against l22 9.6s). Slightly heavy: l22 and l38 (9.6s each, with a clause stack). The "Noun phrase: sentence" opener appears at l05, l40 and in the l04-l06 run, but it is kept to a few spots.
- V6 2 证据：Rewrites are in the issue table. Top 5 most awkward: l26, l22, l15, l38/l39, l31. No clearly-off line was found.
- R 2 证据：I71 l01 resolved (keeps "line"). I74 l06 resolved ("a few points"). I75/I76 l08 resolved ("every minute under earns one"). I80/I81 l16/l21 resolved (no "circle"). I83 l18 resolved ("At a price of one point five"), though the number collides with l25's radius, so only partly. I85 l22 resolved. I86/I87 l23 resolved. I88/I89 l26 changed to digits and is still four numbers in 9.6s, so it is not fully solved. I92/I93 l33 resolved. I94/I95 l34 resolved but still formula-like. I97/I98 l37 resolved. I99-I102 l38/l39 resolved, but "model they started as" is slightly off (new minor issue). I104/I105 l43 resolved ("Up next: gradient descent."). Author "不采纳" on l04 (I72), l17 (I82), l20 (I84), l30 (I91): all four reasons hold. l04 is the only definition line, l17 is plain narration, l20 states a conclusion, and l30 closes the chapter. I keep l04 and l30 only as 记录.

## 逐句复述
| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | When we train an AI, we often ask for something like this: be as helpful as you can, but don't let harm cross a line. | When we train an AI, we usually say: be as helpful as you can, but don't let it do anything harmful. | natural |
| l02 | "Do your best" and "never cross this line" are different requests. How does a model follow both? | Those are two different asks, "do your best" and "never cross the line". How does a model do both? | natural |
| l03 | Over two hundred years ago, the mathematician Lagrange came up with a way. It's called the Lagrange multiplier. | Over two hundred years ago a mathematician named Lagrange came up with a trick for exactly this. It's called the Lagrange multiplier. | a bit off ("a way" with no object) |
| l04 | Making one thing as good as possible without crossing a line is called constrained optimization. | Getting the best result without crossing a line? That's called constrained optimization. | a bit off (definition tone) |
| l05 | Lagrange's idea: don't build a wall. Put a price on crossing it. | Lagrange's idea was, don't build a wall. Just put a price on crossing it. | natural |
| l06 | Go a little over, and you lose a few points. That price is the Lagrange multiplier, usually written lambda. | Go a little over and you lose a few points. That price is the Lagrange multiplier, usually called lambda. | natural |
| l07 | Say a parent allows one hour of video games a day, and the kid keeps sneaking in more. | Say a parent lets their kid play an hour of video games a day, and the kid keeps sneaking in more. | natural |
| l08 | So the parent tries a new deal: every extra minute costs a dollar of allowance, and every minute under earns one. | So the parent tries a deal: every extra minute costs a dollar, and every minute under earns a dollar. | natural |
| l09 | Set the price too low, and the kid goes over anyway. Too high, and he stops playing altogether. | If the price is too low, the kid goes over anyway. Too high, and he just stops playing. | natural |
| l10 | Get it just right, and he stops around the one-hour mark on his own. That just-right price is lambda. | Get it just right and he'll stop around an hour by himself. That just-right price is lambda. | natural |
| l11 | Let's try a small experiment. Here's a map. The rings are contour lines, rising toward the summit in the middle. | Let's try a little experiment. Here's a map. These rings are contour lines, and the ground rises toward the peak in the middle. | natural |
| l12 | Our job is to find the highest spot. | We're trying to find the highest spot. | natural |
| l13 | But there's a rule: stay inside the fence around camp. And the summit is outside it. | But there's a rule: you have to stay inside the fence around camp. And the peak is outside it. | natural |
| l14 | So we do it Lagrange's way: take the fence down, and charge lambda points for every step away from the center of camp. | So we do it Lagrange's way. We take the fence down and charge lambda points for every step away from the middle of camp. | natural |
| l15 | Then find where height, minus that charge, comes out highest. That's this dot. | Then we look for where height minus the charge is highest. That's the dot you see. | a bit off ("this dot" not yet introduced; equation read aloud) |
| l16 | Start with a price of zero. No charge, so the dot runs straight to the summit, right out past the fence. | Start with a price of zero. No charge, so the dot runs straight to the peak, way out past the fence. | natural |
| l17 | So we raise the price, and the farther outside the dot is, the more we raise it. | So we raise the price, and the further out the dot is, the more we raise it. | natural |
| l18 | At a price of one point five, the dot backs up a bit, but it's still outside. Raise it again, it backs up again. | At a price of 1.5 the dot backs up a bit but it's still outside. Raise it again and it backs up again. | natural |
| l19 | At three, the dot stops right on the fence. | At three, the dot lands right on the fence. | natural |
| l20 | That's exactly the highest point you can reach with the fence up: a height of seven point seven five. | That's the best you can do with the fence up: a height of 7.75. | natural |
| l21 | Push the price to four, and the dot hides back inside the fence, giving up height for nothing. | Push the price up to four and the dot retreats inside the fence, giving up height for nothing. | natural |
| l22 | Now look at that just-right point. The contour line through it just touches the fence, so walking along the fence only takes you downhill. | Look at that sweet spot. The contour line there just touches the fence, so if you walk along the fence, you only go downhill. | a bit off (dense, two ideas) |
| l23 | That's the Lagrange condition: at the best spot, the steepest way uphill goes straight out through the fence. | That's the Lagrange condition: at the best spot, the steepest way up points straight out through the fence. | natural |
| l24 | You might think lambda is just a knob we turned. But it also tells you how expensive the rule is. | You might think lambda is just a knob we turned. But it also tells you how costly the rule is. | natural |
| l25 | Make the fence a tiny bit bigger: the radius goes from one point five to one point six. | Make the fence a tiny bit bigger, radius 1.5 to 1.6. | natural |
| l26 | The highest point rises from seven point seven five to eight point oh four. That's point two nine more, about three times the point one we added. | The top goes from 7.75 to 8.04, about 0.3 more, roughly three times the 0.1 we added. | a bit off (four numbers by ear) |
| l27 | So a lambda of three means: loosen the fence a little, and you climb about three times that much. | So a lambda of three means: loosen the fence a bit and you climb about three times as much. | natural |
| l28 | Economists call this a shadow price. | Economists call this a shadow price. | natural |
| l29 | And if the summit were already inside the fence, lambda would be zero: the rule isn't holding you back. | And if the peak were already inside the fence, lambda would be zero, because the rule isn't holding you back. | natural |
| l30 | So lambda tells you which rules are really pinning you down. | So lambda shows you which rules are really holding you back. | natural |
| l31 | Back to where we started. In twenty twenty-three, a team at Peking University proposed a way to train language models called Safe RLHF. | Back to where we started. In 2023 a team at Peking University came up with a way to train language models, called Safe RLHF. | a bit off (acronym unexplained) |
| l32 | One scoring model rates how helpful an answer is, another how harmful. | One model scores how helpful an answer is, and another scores how harmful it is. | natural |
| l33 | We want harm under the line, and as much help as we can get within it. | We want harm under the line, and as much help as we can get while staying under it. | natural |
| l34 | They used a Lagrange multiplier: take the helpfulness score, and subtract lambda times the harm score. | They used a Lagrange multiplier: take the helpfulness score and subtract lambda times the harm score. | natural |
| l35 | And lambda adjusts itself during training. When harm goes over the line, lambda goes up, and safety counts for more. | And lambda adjusts itself during training. If harm goes over the line, lambda goes up, so safety matters more. | natural |
| l36 | When harm stays under, lambda comes back down, and the model is free to help more. Just like the dot on our mountain. | When harm stays under, lambda comes back down and the model can help more. Same as the dot on our mountain. | natural |
| l37 | Prices on rules show up all over AI. | You see prices on rules all over AI. | natural |
| l38 | Take regularization, which keeps a model from memorizing. It docks points when a model gets too complex, and a price like this sets how many. | Take regularization, which stops a model from just memorizing. It docks points when the model gets too complex, and a price like this decides how many. | a bit off ("sets how many") |
| l39 | And chatbots often lose points for drifting too far from the model they started as. A price like this sets how much. | And chatbots often lose points for drifting too far from the model they started from. Again, a price decides how much. | a bit off ("started as", repeated tail) |
| l40 | So, in one line: a Lagrange multiplier is a price on a constraint. | So, in one line: a Lagrange multiplier is a price on a rule. | natural |
| l41 | Get the price just right, and you don't need a wall. You'll stop right at the line. | Get the price right and you don't need a wall. You'll stop right at the line. | natural |
| l42 | Next time you want it all, but there's a line you can't cross, ask yourself: what's this rule really worth? | Next time you want it all but there's a line you can't cross, ask yourself what that rule is really worth. | natural |
| l43 | Up next: gradient descent. | Up next: gradient descent. | natural |

## 问题表
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l26 | V3, V5 | 建议 | The highest point rises from seven point seven five to eight point oh four. That's point two nine more, about three times the point one we added. | Four decimals by ear, plus a subtraction and a ratio, in 9.6s. A listener is still doing the arithmetic when l27 draws the conclusion. The screen carries it, but the voice should stand alone. | The highest point rises from seven point seven five to eight point oh four, about three times the point one we added. |
| l15 | V3, V1 | 建议 | Then find where height, minus that charge, comes out highest. That's this dot. | "This dot" has no referent for an ear-only listener, and "height, minus that charge, comes out highest" is an equation read aloud. | Then we look for the spot where height minus the charge is highest. The dot marks it. |
| l22 | V3, V5 | 建议 | Now look at that just-right point. The contour line through it just touches the fence, so walking along the fence only takes you downhill. | Two geometric ideas in one 9.6s line. Hard to picture by ear, though the clause break helps. | At that point the contour line just touches the fence, so walking along the fence only takes you downhill. |
| l31 | V3 | 建议 | a way to train language models called Safe RLHF | The acronym is never unpacked; "called Safe RLHF" sounds like a label for the whole sentence. It is the one unexplained jargon item in the AI chapter. | a team at Peking University proposed a way to train language models. They called it Safe RLHF. |
| l38/l39 | V1, V4 | 建议 | a price like this sets how many. / A price like this sets how much. | Same ending twice in a row; "sets how many" is the stiffest phrase left in the film. "Started as" also sounds off. | l38: ...and a price like this decides how many. l39: ...drifting too far from the model they started from. |
| l03 | V1 | 建议 | the mathematician Lagrange came up with a way. | Cold open (strict item). I judge it natural but vague: "a way" to what? A friend would name it as a trick. | Over two hundred years ago, the mathematician Lagrange came up with a trick for this. It's called the Lagrange multiplier. |
| l25 | V3 | 记录 | the radius goes from one point five to one point six | The number "one point five" was the price at l18, now the radius. Said clearly each time, but a hurried listener may link them. | Make the fence a tiny bit bigger: the radius goes from one point five to one point six. (Keep; l18 already says "price".) |
| l04 | V1 | 记录 | is called constrained optimization | Definition tone, but the author's reason (the only definition, sets up a term) holds. | Keep. |
| l30 | V4 | 记录 | So lambda tells you which rules are really pinning you down. | Recap that could go; works as a chapter close. | Keep, or cut. |
| 章节卡 "Lambda as a price" / "How AI uses it" | V1 | 存疑 | Lambda as a price | Strict item. Noun-phrase title, but normal for YouTube chapter cards. Also, the fourth card reads "How AI uses it" while the narration heading is "An example from AI", so check they match. | Lambda is a price |

## 整体观察
- No table-of-contents opener, no "In this episode" line, and no "noun phrase + and how to..." pattern. The cold open leads straight into a question.
- The strict spots (cold open, chapter flow, outro l40-l43) pass. l03's "a way" is the only soft spot there.
- Keep 1: the parent and allowance example (l07-l10). It is the most human stretch, sets the price idea before any math, and is reused at l36 and l41.
- Keep 2: the threaded metaphor, wall vs price, with l05 "don't build a wall" paid off at l41 "you don't need a wall".
- Keep 3: l35-l36 with l36 "Just like the dot on our mountain", which ties the AI example back to the experiment.
- Weakest area: numbers and geometry in the experiment (l15, l22, l26). They read fine on screen but burden the ear.
- No 必改 found; the film passes the ear test with suggestions only.
