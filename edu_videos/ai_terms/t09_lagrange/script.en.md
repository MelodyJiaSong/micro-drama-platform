# t09 Lagrange multiplier — narration (English)

v1.3 (2026-11-09, per lines_r3 judges: l21 "pulls back", l38, l39). v1.2 (2026-11-09, per lines_r2 judges' final wording: l01, l11 defines contour lines, l15, l26, l31, l40 "to sum it up", l42). v1.1 (2026-11-09, per lines_r1 judges: l01 keeps "line", l18 says "price", l23 rewritten, fewer "X:" openers, l43 "Up next"). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` (`drafts/v1_en.md`); the author only trimmed and checked facts. Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: When we train an AI, we often ask for something like this: be as helpful as you can, but keep harm below a certain line.
- l02: "Do your best" and "never cross this line" are different requests. How does a model follow both?
- l03: Over two hundred years ago, the mathematician Lagrange came up with a way. It's called the Lagrange multiplier.

## s2 What a Lagrange multiplier is [章:problem]
- l04: Making one thing as good as possible without crossing a line is called constrained optimization.
- l05: Lagrange's idea: don't build a wall. Put a price on crossing it.
- l06: Go a little over, and you lose a few points. That price is the Lagrange multiplier, usually written {λ|lambda}.
- l07: Say a parent allows one hour of video games a day, and the kid keeps sneaking in more.
- l08: So the parent tries a new deal: every extra minute costs a dollar of allowance, and every minute under earns one.
- l09: Set the price too low, and the kid goes over anyway. Too high, and he stops playing altogether.
- l10: Get it just right, and he stops around the one-hour mark on his own. That just-right price is {λ|lambda}.

## s3 A small experiment [章:experiment]
- l11: Let's try a small experiment. Here's a map of a mountain. Each ring is a contour line, the same height all the way round.
- l12: Our job is to find the highest spot.
- l13: But there's a rule: stay inside the fence around camp. And the summit is outside it.
- l14: So we do it Lagrange's way: take the fence down, and charge {λ|lambda} points for every step away from the center of camp.
- l15: Then find the spot with the most height left after the charge. This dot marks it.
- l16: Start with a price of {0|zero}. No charge, so the dot runs straight to the summit, right out past the fence.
- l17: So we raise the price, and the farther outside the dot is, the more we raise it.
- l18: At a price of {1.5|one point five}, the dot backs up a bit, but it's still outside. Raise it again, it backs up again.
- l19: At {3|three}, the dot stops right on the fence.
- l20: That's exactly the highest you can reach with the fence up: a height of {7.75|seven point seven five}.
- l21: Push the price to {4|four}, and the dot pulls back inside the fence, giving up height for nothing.
- l22: Now look at that just-right point. The contour line through it just touches the fence, so walking along the fence only takes you downhill.
- l23: That's the Lagrange condition: at the best spot, the steepest way uphill goes straight out through the fence.

## s4 Lambda as a price [章:lens]
- l24: You might think {λ|lambda} is just a knob we turned. But it also tells you how expensive the rule is.
- l25: Make the fence a tiny bit bigger, from a radius of {1.5|one point five} to {1.6|one point six}.
- l26: The highest you can reach goes from {7.75|seven point seven five} to {8.04|eight point oh four}. That's a gain of about three times the extra radius.
- l27: So a {λ|lambda} of three means: loosen the fence a little, and you climb about three times that much.
- l28: Economists call this a shadow price.
- l29: And if the summit were already inside the fence, {λ|lambda} would be zero, because the rule wouldn't be holding you back.
- l30: So {λ|lambda} tells you which rules are really pinning you down.

## s5 An example from AI [章:real]
- l31: Back to where we started. In {2023|twenty twenty-three}, a team at Peking University proposed a way to train language models. They called it Safe RLHF.
- l32: One scoring model rates how helpful an answer is, another how harmful.
- l33: We want harm to stay under the line, and as much help as we can get.
- l34: They used a Lagrange multiplier: take the helpfulness score, and subtract {λ|lambda} times the harm score.
- l35: And {λ|lambda} adjusts itself during training. When harm goes over the line, {λ|lambda} goes up, and safety counts for more.
- l36: When harm stays under, {λ|lambda} comes back down, and the model is free to help more. Just like the dot on our mountain.
- l37: Prices on rules show up all over AI.
- l38: Take regularization. It puts a price on complexity, so the model doesn't just memorize the examples it's trained on.
- l39: And chatbots often pay a price for drifting too far from their original model.

## s6 Wrap-up [包装:outro]
- l40: So, to sum it up: a Lagrange multiplier is a price on a constraint.
- l41: Get the price just right, and you don't need a wall. You'll stop right at the line.
- l42: Next time you want it all, but there's a line you can't cross, ask yourself: what is that line really costing me?
- l43: Up next: gradient descent.
