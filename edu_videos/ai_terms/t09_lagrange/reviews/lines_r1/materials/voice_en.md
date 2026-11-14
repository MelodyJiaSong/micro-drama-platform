# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（9.6s / pause 0.3s）：When we train an AI, we often ask for something like this: be as helpful as you can, but keep anything harmful below a line.  [On screen: 「Be helpful」, 「Harm ≤ the line」]
- l02（6.5s / pause 0.4s）："Do your best" and "never cross this line" are different requests. How does a model follow both?  [On screen: 「Do your bestBe helpful」, 「Never crossHarm ≤ the li」]
- l03（6.5s）：Over two hundred years ago, the mathematician Lagrange came up with a way. It's called the Lagrange multiplier.  [On screen: 「The Lagrange multiplier」]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What a Lagrange multiplier is”]

## What a Lagrange multiplier is
- l04（5.8s / pause 0.4s）：Making one thing as good as possible without crossing a line is called constrained optimization.  [On screen: 「Constrained optimization」, 「Make it the best」]
- l05（4.6s / pause 0.3s）：Lagrange's idea: don't build a wall. Put a price on crossing it.  [On screen: 「→」, 「No wall」, a chart]
- l06（6.5s / pause 0.4s）：Go a little over, lose a little score. That price is the Lagrange multiplier, usually written lambda.  [On screen: 「λ」, 「→」, a chart]
- l07（6.9s / pause 0.4s）：Say a parent allows one hour of video games a day, and the kid keeps sneaking in more.  [On screen: 「1 hour a day, max」]
- l08（8.1s / pause 0.4s）：So the parent tries a new deal: every extra minute costs a dollar of allowance, and every minute less earns one.  [On screen: 「1 extra minute−$1」, 「1 minute less+$1」]
- l09（6.9s / pause 0.4s）：Set the price too low, and the kid goes over anyway. Too high, and he stops playing altogether.  [On screen: 「Too lowGoes over」, 「Too highQuits」]
- l10（8.8s）：Get it just right, and he stops around the one-hour mark on his own. That just-right price is what lambda is.  [On screen: 「λ」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l11（7.7s / pause 0.3s）：Let's try a small experiment. Here's a map. The rings are contour lines, rising toward the summit in the middle.  [On screen: 「Summit」, 「Contour line」]
- l12（2.3s / pause 0.4s）：Our job: find the highest spot.  [On screen: 「Goal: the highest spot」, 「Summit」]
- l13（6.2s / pause 0.3s）：But there's a rule: stay inside the fence around camp. And the summit is outside it.  [On screen: 「Rule: stay inside」, 「Summit」]
- l14（8.8s / pause 0.4s）：So we do it Lagrange's way: take the fence down, and charge lambda points for every step away from the center of camp.  [On screen: 「No fence. A charge.」, 「Each step out: −λ」]
- l15（5.4s / pause 0.4s）：Then find the spot where height minus that charge is biggest. That's this dot.  [On screen: 「No fence. A charge.」, 「Each step out: −λ」]
- l16（8.1s / pause 0.4s）：Start with a price of zero. No charge, so the dot runs straight to the summit, right out of the circle.  [On screen: 「λ」, 「0」]
- l17（6.5s / pause 0.3s）：So we raise the price, and the farther outside the dot is, the more we raise it.  [On screen: 「λ」, 「0」]
- l18（8.1s / pause 0.3s）：At one point five, the dot backs up a bit, but it's still outside. Raise it again, it backs up again.  [On screen: 「λ」, 「2.63」]
- l19（3.5s / pause 0.3s）：At three, the dot stops right on the fence.  [On screen: 「λ」, 「3」]
- l20（6.9s / pause 0.4s）：That's exactly the highest point you can reach with the fence up: a height of seven point seven five.  [On screen: 「λ」, 「3」]
- l21（6.5s / pause 0.4s）：Push the price to four, and the dot hides inside the circle, giving up height for nothing.  [On screen: 「λ」, 「4」]
- l22（9.6s / pause 0.4s）：Now look at that just-right point. The contour line through it just touches the fence, so moving along the fence only takes you lower.  [On screen: 「λ」, 「3」]
- l23（6.9s）：That's what the Lagrange condition looks like: at the best point, uphill points straight out through the fence.  [On screen: 「Contour meets fence」, 「Uphill points」]

> [On screen: chapter card “Lambda as a price”]

## Lambda as a price
- l24（7.7s / pause 0.3s）：You might think lambda is just a knob we turned. But it also tells you how expensive the rule is.  [On screen: 「λ」, 「λ = 3」]
- l25（6.9s / pause 0.3s）：Make the fence a tiny bit bigger: the radius goes from one point five to one point six.  [On screen: 「Fence radius1.5 → 1.6」]
- l26（8.8s / pause 0.4s）：The highest point rises from seven point seven five to eight point oh four. That's point two nine more, almost exactly three times point one.  [On screen: 「+0.29 ≈ 3 × 0.1」, 「+0.29」]
- l27（7.3s / pause 0.4s）：So lambda equals three means: loosen the fence a little, and you climb about three times that much higher.  [On screen: 「+0.29 ≈ 3 × 0.1」, 「+0.29」]
- l28（2.3s / pause 0.4s）：Economists call this a shadow price.  [On screen: 「Shadow price」, 「+0.29 ≈ 3 × 0.1」]
- l29（7.3s / pause 0.4s）：And if the summit were already inside the fence, lambda would be zero: the rule isn't holding you back.  [On screen: 「λ」, 「λ = 0」]
- l30（4.2s）：So lambda tells you which rules are really pinning you down.  [On screen: 「λ shows what holds you b」, 「Big λ→Holding you back」]

> [On screen: chapter card “An example from AI”]

## An example from AI
- l31（8.5s / pause 0.4s）：Back to where we started. In twenty twenty-three, a team at Peking University proposed a way to train language models called Safe RLHF.  [On screen: 「Safe RLHF」, 「Safe reinforcement learn」]
- l32（4.6s / pause 0.4s）：One scoring model rates how helpful an answer is, another how harmful.  [On screen: 「How helpful」, 「How harmful」]
- l33（5.8s / pause 0.3s）：The goal: keep harm below the line, and within that, be as helpful as possible.  [On screen: 「How helpful」, 「How harmful」]
- l34（5.4s / pause 0.4s）：Their tool was the Lagrange multiplier: helpfulness score, minus lambda times the harm score.  [On screen: 「Helpful − λ × Harmful」, 「How helpful」]
- l35（7.7s / pause 0.4s）：And lambda adjusts itself during training. When harm goes over the line, lambda goes up, and safety counts for more.  [On screen: 「λ tunes itself」, a chart]
- l36（7.3s / pause 0.3s）：When harm stays under, lambda comes back down, and the model is free to help. Just like our mountain.  [On screen: 「λ tunes itself」, a chart]
- l37（4.6s / pause 0.4s）：Coefficients that put a price on a rule are all over AI.  [On screen: 「Prices on rules」, 「① Safety lineλ tunes its」]
- l38（8.5s / pause 0.4s）：Regularization, which keeps a model from memorizing, docks points for being too complex. How many is set by a coefficient like this.  [On screen: 「Prices on rules」, 「① Safety lineλ tunes its」]
- l39（8.8s）：And chatbots are often kept from drifting too far from the original model. How hard that's penalized is the same kind of coefficient.  [On screen: 「Prices on rules」, 「① Safety lineλ tunes its」]

## Outro (on screen: end card)
- l40（5.0s / pause 0.4s）：So, in one line: a Lagrange multiplier is a price on a constraint.
- l41（6.5s / pause 0.3s）：Get the price just right, and you don't need a wall. You'll stop right at the line.
- l42（7.7s / pause 0.4s）：Next time you want it all, but there's a line you can't cross, ask yourself: what's this rule really worth?
- l43（2.7s）：Next time, we'll get into gradient descent.

