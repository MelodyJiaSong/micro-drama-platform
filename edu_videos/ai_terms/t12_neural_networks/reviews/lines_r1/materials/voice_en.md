# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（5.4s / pause 0.3s）：Remember our two-knob taxi-fare machine? It learned distance and fare just fine.  [On screen: 「Learns it fine」, 「10.2」, a chart]
- l02（6.9s / pause 0.4s）：But fares also depend on the time: rush hour costs more, and late night a little more too.  [On screen: 「Evening rush」, 「Morning rush」, a chart]
- l03（5.0s / pause 0.3s）：That, it can't learn, because all it can draw is a straight line.  [On screen: 「Only straight lines」, 「Evening rush」, a chart]
- l04（5.4s）：So how does a machine learn a pattern that bends? With a neural network.  [On screen: 「Neural networks」]

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l05（6.2s / pause 0.4s）：Last time, we turned the knobs by walking downhill blindfolded, toward wherever the score drops fastest.
- l06（6.2s）：Today we'll build a tiny network that learns the bend, and see why going deeper helps.

> [On screen: chapter card “Lines can't bend”]

## Lines can't bend
- l07（6.9s / pause 0.4s）：Here's some made-up data: the same five-kilometer ride, forty-eight times, at different hours of the day.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l08（4.6s / pause 0.3s）：Daytime runs about twenty-three dollars, just what our two-knob machine charges.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l09（6.9s / pause 0.4s）：Around eight a.m. and six p.m. it spikes, and late at night it's a bit pricier.  [On screen: 「Same 5 km」, 「48 rides」, a chart]
- l10（7.7s / pause 0.4s）：Same two knobs, one for height and one for slope, but now we feed it the time, not the distance.  [On screen: 「33.0」, 「0.55」, a chart]
- l11（6.2s / pause 0.4s）：However you turn them, the best you get is a nearly flat line through the middle.  [On screen: 「26.6」, 「-0.07」, a chart]
- l12（7.7s / pause 0.4s）：It's too cheap at rush hour and too pricey by day, and its loss can't get below eleven point five.  [On screen: 「11.5」, 「26.6」, a chart]
- l13（5.8s）：The knobs aren't the problem: this machine only draws straight lines, and the pattern bends.  [On screen: 「Lines can’t bend」, 「Evening rush」, a chart]

> [On screen: chapter card “Build a small network”]

## Build a small network
- l14（4.6s / pause 0.4s）：The fix isn't one big machine. It's lots of simple little ones.  [On screen: 「Lots of simple units」]
- l15（6.9s / pause 0.3s）：Each unit still has two knobs and draws a line, plus one rule: anything below zero becomes zero.  [On screen: 「Below zero → zero」, 「1.6」, a chart]
- l16（3.1s / pause 0.4s）：So its line stays flat, then bends upward.  [On screen: 「A line with one bend」, 「1.6」, a chart]
- l17（3.8s / pause 0.4s）：The two knobs set where it bends and how steeply.  [On screen: 「A line with one bend」, 「1.6」, a chart]
- l18（5.0s / pause 0.4s）：One bend isn't enough, so add more units that bend in different spots.  [On screen: 「+」, 「+」]
- l19（4.6s / pause 0.4s）：Add them up, and you can build bumps, steps, almost any curve.  [On screen: 「+」, 「+」]
- l20（6.9s / pause 0.3s）：Our network has twelve units side by side in the first layer, and one unit in the second.  [On screen: 「Layer 1 · 12 units」, 「Layer 2 · 1 unit」, a chart]
- l21（7.3s / pause 0.4s）：That one weighs each bent line with its own knob, adds one more knob, and out comes the fare.  [On screen: 「A knob for each」, 「Plus one more → fare」, a chart]
- l22（1.9s / pause 0.4s）：That's thirty-seven knobs in total.  [On screen: 「37」, 「knobs」, a chart]
- l23（5.0s / pause 0.4s）：Layers of little units like this are what we call a neural network.  [On screen: 「Neural network」, 「Layers of small units」, a chart]
- l24（7.7s）：The name comes from neurons in the brain, but don't take that too seriously: it's just little units with knobs.  [On screen: 「Neural network」, 「Layers of small units」, a chart]

## Training
- l25（6.9s / pause 0.4s）：To turn all thirty-seven, we use last episode's trick, nudging every knob whichever way drops the loss fastest.  [On screen: a chart]
- l26（5.8s / pause 0.4s）：It starts as a random squiggle, and step by step it bends toward the peaks.  [On screen: 「0.87」, a chart]
- l27（8.1s / pause 0.4s）：After ten thousand steps, the loss is down to zero point two six, while the best straight line managed eleven point five.  [On screen: 「0.26」, 「Best line: 11.5」, a chart]
- l28（3.5s / pause 0.4s）：Rush hours and late nights, it catches them all.  [On screen: 「0.26」, 「Best line: 11.5」, a chart]
- l29（5.0s / pause 0.3s）：And every corner on this curve is one little unit making its bend.  [On screen: 「0.26」, 「Best line: 11.5」, a chart]
- l30（5.4s）：How we work out which way each knob should turn is next episode's story.  [On screen: 「Which way to turn?」, 「Next episode」, a chart]

> [On screen: chapter card “Why go deep?”]

## Why go deep?
- l31（4.6s / pause 0.4s）：So far, our units sat side by side, each adding one bend.  [On screen: 「Side by side: one bend e」]
- l32（6.2s / pause 0.4s）：Now stack them instead, so each layer folds the line it gets from the layer before.  [On screen: 「Stacked: fold again」]
- l33（6.2s / pause 0.4s）：In a worked example, two units per layer can fold a slanted line exactly in half.  [On screen: 「2」, 「Stacked: fold again」]
- l34（6.2s / pause 0.4s）：One layer gives two pieces, two layers give four, and each new layer can double it.  [On screen: 「32」, 「Stacked: fold again」]
- l35（6.9s / pause 0.4s）：So ten units side by side give at most eleven pieces. Stacked five deep, they can give thirty-two.  [On screen: 「10 side by side: ≤ 11」, 「10 in 5 layers: 32」]
- l36（3.1s / pause 0.4s）：Later layers reuse what earlier ones already folded.  [On screen: 「10 side by side: ≤ 11」, 「10 in 5 layers: 32」]
- l37（5.8s / pause 0.4s）：So the deeper the stack, the more complex the shapes the same units can build.  [On screen: 「10 side by side: ≤ 11」, 「10 in 5 layers: 32」]
- l38（2.3s）：That's the "deep" in deep learning.  [On screen: 「Deep learning」, 「Many layers deep」]

> [On screen: chapter card “AlexNet, 2012”]

## AlexNet, 2012
- l39（5.8s / pause 0.4s）：In twenty twelve, three researchers at the University of Toronto trained a very deep neural network.  [On screen: 「AlexNet」]
- l40（5.4s / pause 0.4s）：They were Krizhevsky, Sutskever and Hinton, and the network later became known as AlexNet.  [On screen: 「AlexNet」, 「Krizhevsky · Sutskever ·」]
- l41（7.3s / pause 0.3s）：It had eight layers and sixty million knobs, and learned a thousand categories from one point two million photos.  [On screen: 「Krizhevsky et al. · NIPS」, 「8layers」]
- l42（7.3s / pause 0.3s）：At that year's ImageNet contest, it got five guesses per picture, and only missed if all five were wrong.  [On screen: 「ImageNet contest, 2012」, 「5 guesses; all wrong = a」]
- l43（8.1s / pause 0.4s）：A version of it had a fifteen point three percent error rate, against twenty-six point two percent for the runner-up.  [On screen: 「ImageNet contest, 2012」, 「5 guesses; all wrong = a」, a chart]
- l44（8.5s / pause 0.4s）：Nobody told it what to look for, yet its first layer learned to spot stripes at all angles, and patches of color.  [On screen: 「Layer 1: stripes, colors」, 「Krizhevsky et al. · NIPS」]
- l45（3.1s / pause 0.4s）：Later layers built on those, layer by layer.  [On screen: 「Built up layer by layer」, 「Krizhevsky et al. · NIPS」, a chart]
- l46（5.0s / pause 0.3s）：They also found that removing any middle layer cost about two percentage points.  [On screen: 「Remove a middle layer → 」, 「Krizhevsky et al. · NIPS」, a chart]
- l47（3.8s）：As the paper put it, "the depth really is important."  [On screen: 「“The depth really / is i」, 「Krizhevsky et al. 2012 ·」]

## Outro (on screen: end card)
- l48（5.8s / pause 0.4s）：So a neural network is just simple little units with knobs, stacked layer on layer.
- l49（4.2s / pause 0.4s）：Stack them deep enough, and they can recognize really complicated things.
- l50（7.7s / pause 0.3s）：Thirty-seven knobs is easy, but AlexNet had sixty million, so how do you work out which way each one turns?
- l51（2.3s）：That's backpropagation, coming up next time.

