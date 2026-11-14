# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（9.6s / pause 0.3s）：When we train an AI, we often ask for something like this: be as helpful as you can, but keep harm below a certain line.  [On screen: 「Most helpful」, 「Harm ≤ the line」]
- l02（6.5s / pause 0.4s）："Do your best" and "never cross this line" are different requests. How does a model follow both?  [On screen: 「“Do your best”Most helpf」, 「“Never cross it”Harm ≤ t」]
- l03（6.5s）：Over two hundred years ago, the mathematician Lagrange came up with a way. It's called the Lagrange multiplier.  [On screen: 「The Lagrange multiplier」]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What is a Lagrange multiplier?”]

## What a Lagrange multiplier is
- l04（5.8s / pause 0.4s）：Making one thing as good as possible without crossing a line is called constrained optimization.  [On screen: 「Constrained optimization」, 「Make it the best」]
- l05（4.6s / pause 0.3s）：Lagrange's idea: don't build a wall. Put a price on crossing it.  [On screen: 「→」, 「No wall」, a chart]
- l06（7.3s / pause 0.3s）：Go a little over, and you lose a few points. That price is the Lagrange multiplier, usually written lambda.  [On screen: 「λ」, 「λ: the Lagrange multipli」]
- l07（6.9s / pause 0.3s）：Say a parent allows one hour of video games a day, and the kid keeps sneaking in more.  [On screen: 「1 hour a day at most」]
- l08（8.1s / pause 0.4s）：So the parent tries a new deal: every extra minute costs a dollar of allowance, and every minute under earns one.  [On screen: 「1 minute over−$1」, 「1 minute under+$1」]
- l09（6.9s / pause 0.3s）：Set the price too low, and the kid goes over anyway. Too high, and he stops playing altogether.  [On screen: 「Too lowGoes over」, 「Too highQuits」]
- l10（8.1s）：Get it just right, and he stops around the one-hour mark on his own. That just-right price is lambda.  [On screen: 「λ」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l11（9.2s / pause 0.3s）：Let's try a small experiment. Here's a map of a mountain. Each ring is a contour line, the same height all the way round.  [On screen: 「Summit」, 「Contour line」]
- l12（3.1s / pause 0.4s）：Our job is to find the highest spot.  [On screen: 「Goal: the highest spot」, 「Summit」]
- l13（6.2s / pause 0.4s）：But there's a rule: stay inside the fence around camp. And the summit is outside it.  [On screen: 「Rule: stay in the fence」, 「Summit」]
- l14（8.8s / pause 0.4s）：So we do it Lagrange's way: take the fence down, and charge lambda points for every step away from the center of camp.  [On screen: 「No fence, just a charge」, 「Each step out: −λ」]
- l15（6.2s / pause 0.4s）：Then find the spot with the most height left after the charge. This dot marks it.  [On screen: 「No fence, just a charge」, 「Each step out: −λ」]
- l16（8.1s / pause 0.4s）：Start with a price of zero. No charge, so the dot runs straight to the summit, right out past the fence.  [On screen: 「λ」, 「0」]
- l17（6.5s / pause 0.4s）：So we raise the price, and the farther outside the dot is, the more we raise it.  [On screen: 「λ」, 「0」]
- l18（9.2s / pause 0.4s）：At a price of one point five, the dot backs up a bit, but it's still outside. Raise it again, it backs up again.  [On screen: 「λ」, 「2.63」]
- l19（3.5s / pause 0.4s）：At three, the dot stops right on the fence.  [On screen: 「λ」, 「3」]
- l20（6.5s / pause 0.3s）：That's exactly the highest you can reach with the fence up: a height of seven point seven five.  [On screen: 「λ」, 「3」]
- l21（6.9s / pause 0.3s）：Push the price to four, and the dot hides back inside the fence, giving up height for nothing.  [On screen: 「λ」, 「4」]
- l22（9.6s / pause 0.3s）：Now look at that just-right point. The contour line through it just touches the fence, so walking along the fence only takes you downhill.  [On screen: 「λ」, 「3」]
- l23（6.9s）：That's the Lagrange condition: at the best spot, the steepest way uphill goes straight out through the fence.  [On screen: 「The Lagrange condition」, 「Uphill → straight throug」]

> [On screen: chapter card “Lambda as a price”]

## Lambda as a price
- l24（7.7s / pause 0.3s）：You might think lambda is just a knob we turned. But it also tells you how expensive the rule is.  [On screen: 「λ」, 「λ = 3」]
- l25（6.9s / pause 0.3s）：Make the fence a tiny bit bigger, from a radius of one point five to one point six.  [On screen: 「Fence radius1.5 → 1.6」]
- l26（9.6s / pause 0.4s）：The highest you can reach goes from seven point seven five to eight point oh four. That's a gain of about three times the extra radius.  [On screen: 「+0.29 ≈ 3λ × 0.1」, 「+0.29」]
- l27（7.3s / pause 0.3s）：So a lambda of three means: loosen the fence a little, and you climb about three times that much.  [On screen: 「+0.29 ≈ 3λ × 0.1」, 「+0.29」]
- l28（2.3s / pause 0.4s）：Economists call this a shadow price.  [On screen: 「Shadow price」, 「+0.29 ≈ 3λ × 0.1」]
- l29（8.1s / pause 0.3s）：And if the summit were already inside the fence, lambda would be zero, because the rule wouldn't be holding you back.  [On screen: 「λ」, 「λ = 0」]
- l30（4.2s）：So lambda tells you which rules are really pinning you down.  [On screen: 「What λ tells you」, 「High λ→Costly constraint」]

> [On screen: chapter card “How AI uses it”]

## An example from AI
- l31（9.2s / pause 0.3s）：Back to where we started. In twenty twenty-three, a team at Peking University proposed a way to train language models. They called it Safe RLHF.  [On screen: 「Safe RLHF」, 「Safe reinforcement learn」]
- l32（4.6s / pause 0.4s）：One scoring model rates how helpful an answer is, another how harmful.  [On screen: 「How helpful」, 「How harmful」]
- l33（6.2s / pause 0.3s）：We want harm to stay under the line, and as much help as we can get.  [On screen: 「How helpful」, 「How harmful」]
- l34（6.2s / pause 0.4s）：They used a Lagrange multiplier: take the helpfulness score, and subtract lambda times the harm score.  [On screen: 「Help score − λ × Harm sc」, 「How helpful」]
- l35（7.7s / pause 0.4s）：And lambda adjusts itself during training. When harm goes over the line, lambda goes up, and safety counts for more.  [On screen: 「λ tunes itself」, a chart]
- l36（8.8s / pause 0.4s）：When harm stays under, lambda comes back down, and the model is free to help more. Just like the dot on our mountain.  [On screen: 「λ tunes itself」, a chart]
- l37（3.1s / pause 0.4s）：Prices on rules show up all over AI.  [On screen: 「Prices on rules」, 「① Safety lineHarm costs」]
- l38（9.6s / pause 0.3s）：Take regularization, which keeps a model from memorizing. It docks points when a model gets too complex, and a price like this sets how many.  [On screen: 「Prices on rules」, 「① Safety lineHarm costs」]
- l39（8.5s）：And chatbots often lose points for drifting too far from the model they started as. A price like this sets how much.  [On screen: 「Prices on rules」, 「① Safety lineHarm costs」]

## Outro (on screen: end card)
- l40（5.4s / pause 0.3s）：So, to sum it up: a Lagrange multiplier is a price on a constraint.
- l41（6.5s / pause 0.4s）：Get the price just right, and you don't need a wall. You'll stop right at the line.
- l42（8.5s / pause 0.4s）：Next time you want it all, but there's a line you can't cross, ask yourself: what is that line really costing me?
- l43（1.5s）：Up next: gradient descent.

