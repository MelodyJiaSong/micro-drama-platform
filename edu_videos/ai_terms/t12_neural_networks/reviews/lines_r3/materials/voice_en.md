# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（6.2s / pause 0.4s）：Remember our two-knob taxi-fare machine? It learned how fares change with distance just fine.  [On screen: 「Good fit」, 「10.2」, a chart]
- l02（7.7s / pause 0.4s）：But fares also depend on the time of day: rush hour costs more, and late night a little more too.  [On screen: 「Evening rush」, 「Morning rush」, a chart]
- l03（5.0s / pause 0.3s）：It can't learn that, because all it can draw is a straight line.  [On screen: 「Straight lines only」, 「Evening rush」, a chart]
- l04（5.4s）：So how does a machine learn a pattern that bends? With a neural network.  [On screen: 「Neural networks」]

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l05（6.2s / pause 0.4s）：Last time, we turned the knobs by walking downhill blindfolded, toward wherever the score drops fastest.
- l06（8.8s）：Today we'll build a tiny network that learns the bend, see why stacking more layers helps, and meet a famous one called AlexNet.

> [On screen: chapter card “Beyond straight lines”]

## Beyond straight lines
- l07（6.9s / pause 0.4s）：Here's some made-up data: the same five-kilometer ride, forty-eight times, at different hours of the day.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l08（5.0s / pause 0.4s）：Daytime rides cost about twenty-three dollars, just what our two-knob machine charges.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l09（6.9s / pause 0.3s）：Around eight a.m. and six p.m. it spikes, and late at night it's a bit pricier.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l10（7.7s / pause 0.4s）：Same two knobs, one for height and one for slope, but now we feed it the time, not the distance.  [On screen: 「33.0」, 「0.55」, a chart]
- l11（6.2s / pause 0.4s）：However you turn them, the best you get is a nearly flat line through the middle.  [On screen: 「26.6」, 「-0.07」, a chart]
- l12（9.6s / pause 0.4s）：It undercharges at rush hour and overcharges by day. Its loss, the score for how wrong it is, can't get below eleven point five.  [On screen: 「11.5」, 「26.6」, a chart]
- l13（5.8s）：The knobs aren't the problem: this machine only draws straight lines, and the pattern bends.  [On screen: 「Straight lines only」, 「Evening rush」, a chart]

> [On screen: chapter card “Build a small network”]

## Build a small network
- l14（4.6s / pause 0.4s）：The fix isn't one big machine. It's lots of simple little ones.  [On screen: 「Lots of simple units」]
- l15（6.9s / pause 0.3s）：Each unit still has two knobs and draws a line, plus one rule: anything below zero becomes zero.  [On screen: 「Below zero → zero」, 「-0.4」, a chart]
- l16（2.7s / pause 0.3s）：Its line stays flat, then bends upward.  [On screen: 「A line with one bend」, 「-0.4」, a chart]
- l17（3.8s / pause 0.4s）：The two knobs set where it bends and how steeply.  [On screen: 「A line with one bend」, 「-0.4」, a chart]
- l18（5.0s / pause 0.3s）：One bend isn't enough, so add more units that bend in different spots.  [On screen: 「+」, 「+」]
- l19（4.6s / pause 0.3s）：Add them up, and you can build bumps, steps, almost any curve.  [On screen: 「+」, 「+」]
- l20（6.9s / pause 0.4s）：Our network has twelve units side by side in the first layer, and one unit in the second.  [On screen: 「Layer 1 · 12 units」, 「Layer 2 · 1 unit」, a chart]
- l21（8.1s / pause 0.4s）：That unit scales each bent line with a knob, adds them up, then one last knob shifts the total. That's the fare.  [On screen: 「One knob per line」, 「Sum + 1 knob → fare」, a chart]
- l22（1.9s / pause 0.4s）：That's thirty-seven knobs in total.  [On screen: 「37」, 「knobs」, a chart]
- l23（5.0s / pause 0.4s）：Layers of little units like this are what we call a neural network.  [On screen: 「Neural network」, 「Layer 1 · 12 units」, a chart]
- l24（7.7s）：The name comes from neurons in the brain, but don't take that too seriously: it's just little units with knobs.  [On screen: 「Neural network」, 「Layers of small units」, a chart]

## Training
- l25（6.9s / pause 0.4s）：To turn all thirty-seven, we use last episode's trick, nudging every knob whichever way drops the loss fastest.  [On screen: a chart]
- l26（6.2s / pause 0.4s）：Our curve starts as a random squiggle, and step by step it bends toward the peaks.  [On screen: 「0.86」, a chart]
- l27（8.5s / pause 0.3s）：After ten thousand steps, the loss is down to zero point two six. The best straight line never got below eleven point five.  [On screen: 「0.26」, 「Straight line: 11.5」, a chart]
- l28（3.5s / pause 0.4s）：Rush hours and late nights, it catches them all.  [On screen: 「0.26」, 「Evening rush ✓」, a chart]
- l29（5.0s / pause 0.4s）：And every corner on this curve is one little unit making its bend.  [On screen: 「0.26」, 「Unit bends → corner」, a chart]
- l30（5.8s）：With this many knobs, there's a much faster way to find each one's direction. That's next time.  [On screen: 「Which way / to turn?」, 「Next episode」, a chart]

> [On screen: chapter card “Why go deep?”]

## Why go deep?
- l31（4.6s / pause 0.4s）：So far, we've put units side by side, each adding one bend.  [On screen: 「Side by side: 1 bend eac」]
- l32（6.9s / pause 0.3s）：Now stack them, so each layer folds the line it gets from the layer before, like folding paper.  [On screen: 「Stacked: folds on folds」]
- l33（5.4s / pause 0.4s）：For example, two units per layer can fold a slanted line exactly in half.  [On screen: 「2」, 「Stacked: folds on folds」]
- l34（6.2s / pause 0.4s）：One layer makes two straight pieces, two layers make four, and in this example each new layer doubles that.  [On screen: 「32」, 「Stacked: folds on folds」]
- l35（6.9s / pause 0.4s）：So ten units side by side give at most eleven pieces. Stacked five deep, they can give thirty-two.  [On screen: 「10 side by side: ≤ 11 pi」, 「10 in 5 layers: up to 32」]
- l36（3.1s / pause 0.4s）：Later layers reuse what earlier ones already folded.  [On screen: 「10 side by side: ≤ 11 pi」, 「10 in 5 layers: up to 32」]
- l37（5.4s / pause 0.4s）：The deeper the stack, the more complex the shapes the same units can build.  [On screen: 「10 side by side: ≤ 11 pi」, 「10 in 5 layers: up to 32」]
- l38（2.3s）：That's the "deep" in deep learning.  [On screen: 「Deep learning」, 「Deep = many layers」]

> [On screen: chapter card “AlexNet, 2012”]

## AlexNet, 2012
- l39（5.8s / pause 0.4s）：In twenty twelve, three researchers at the University of Toronto trained a very deep neural network.  [On screen: 「AlexNet」]
- l40（5.4s / pause 0.4s）：They were Krizhevsky, Sutskever and Hinton, and the network later became known as AlexNet.  [On screen: 「AlexNet」, 「Krizhevsky · Sutskever ·」]
- l41（7.3s / pause 0.3s）：It had eight layers and sixty million knobs. It learned a thousand categories from one point two million photos.  [On screen: 「Krizhevsky et al. · NIPS」, 「8layers」]
- l42（7.3s / pause 0.3s）：At that year's ImageNet contest, it got five guesses per picture, and only missed if all five were wrong.  [On screen: 「ImageNet contest, 2012」, 「5 guesses · all wrong = 」]
- l43（7.7s / pause 0.3s）：The version they entered got fifteen point three percent wrong, and the runner-up got twenty-six point two percent wrong.  [On screen: 「ImageNet contest, 2012」, 「5 guesses · all wrong = 」, a chart]
- l44（7.7s / pause 0.4s）：Nobody told it what to look for, yet its first layer learned to spot stripes at every angle, and patches of color.  [On screen: 「Layer 1: stripes, colors」, 「Krizhevsky et al. · NIPS」]
- l45（3.8s / pause 0.3s）：Later layers combined those into more and more complex patterns.  [On screen: 「Built up layer by layer」, 「Krizhevsky et al. · NIPS」, a chart]
- l46（5.4s / pause 0.3s）：Removing any middle layer made its first-guess accuracy drop about two percentage points.  [On screen: 「Remove a middle layer → 」, 「First-guess accuracy (to」, a chart]
- l47（3.8s）：As the paper put it, "the depth really is important."  [On screen: 「“…the depth really / is 」, 「Krizhevsky et al. 2012 ·」]

## Outro (on screen: end card)
- l48（5.8s / pause 0.4s）：So a neural network is just simple little units with knobs, stacked layer on layer.
- l49（4.2s / pause 0.4s）：Stack them deep enough, and they can recognize really complicated things.
- l50（7.7s / pause 0.3s）：Thirty-seven knobs, we can test one by one. But sixty million? How do you find which way to turn them all?
- l51（2.3s）：That's backpropagation, coming up next time.

