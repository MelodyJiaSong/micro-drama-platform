# t12 Neural Networks and Deep Learning — English narration v1

## s0 Cold open
- l01: Remember our two-knob taxi-fare machine? It learned distance and fare just fine.
- l02: But fares also depend on the time: rush hour costs more, and late night a bit more.
- l03: And that, it can't learn, because all it draws is a straight line.
- l04: So how does a machine learn a pattern that bends? With a neural network.

## s1 This episode
- l05: Last time, we turned knobs by walking downhill blindfolded, toward wherever the score drops fastest.
- l06: Today, we'll build a tiny network that learns the bend, and see why deeper is better.

## s2 One straight line isn't enough
- l07: Here's some made-up data: the same {5|five}-kilometer ride, {48|forty-eight} times, at different hours.
- l08: Daytime runs about {$23|twenty-three dollars}, just what our two-knob machine charges.
- l09: Around {8|eight} a.m. and {6|six} p.m. it spikes, and late nights cost a bit more.
- l10: It's the same two knobs, height and slope, but now we feed it the time, not the distance.
- l11: However you turn them, you get a nearly flat line through the middle.
- l12: It's too cheap at rush hour, too pricey by day.
- l13: The lowest loss it can reach is {11.5|eleven point five}.
- l14: This machine only draws straight lines, and the pattern bends.

## s3 Build a tiny network
- l15: The fix isn't one big machine; it's lots of simple little ones.
- l16: Each unit still has two knobs, plus one rule: anything below zero becomes zero.
- l17: So its line stays flat, then bends upward; the knobs set where, and how steeply.
- l18: Mix units bending in different spots, and you can build bumps, steps, almost any curve.
- l19: Our network has {12|twelve} units side by side.
- l20: One more unit weighs each line with its own knob, adds one more, and out comes the fare.
- l21: That's {37|thirty-seven} knobs in total.
- l22: Layers of little units like this are a neural network.
- l23: The name comes from neurons, but don't take it seriously: it's just little units with knobs.

## s4 Training
- l24: To turn all thirty-seven, we use last episode's trick: nudge every knob whichever way drops the loss fastest.
- l25: It starts as a random squiggle, then bends toward the peaks, step by step.
- l26: After {10,000|ten thousand} steps, the loss falls from {20.5|twenty point five} to {0.26|zero point two six}; the best straight line managed {11.5|eleven point five}.
- l27: Rush hours and late nights, it catches them all.
- l28: Every corner on this curve is one little unit making its bend.
- l29: How we work out each knob's direction is next episode's story.

## s5 Why go deep
- l30: So far, our units sat side by side, each adding one bend.
- l31: Now stack them, so each layer folds the line from the layer before.
- l32: In a worked example, two units per layer fold a slanted line in half.
- l33: One layer gives two pieces, two layers give four, and each new layer can double it.
- l34: So ten units side by side give at most {11|eleven} pieces; stacked five deep, they can give {32|thirty-two}.
- l35: Later layers reuse what earlier ones folded, so deeper stacks build far more complex shapes.
- l36: That's the "deep" in deep learning.

## s6 AlexNet
- l37: In {2012|twenty twelve}, Krizhevsky, Sutskever and Hinton at the University of Toronto trained a very deep network, now called AlexNet.
- l38: It had {8|eight} layers and {60 million|sixty million} knobs, and learned {1,000|a thousand} categories from {1.2 million|one point two million} photos.
- l39: At that year's ImageNet contest, it got five guesses per image, and missed only if all five were wrong.
- l40: A version of it had an error rate of {15.3%|fifteen point three percent}, versus {26.2%|twenty-six point two percent} for the runner-up.
- l41: Nobody told it what to look for, yet its first layer learned stripes at all angles, and patches of color.
- l42: Each later layer built on top of those.
- l43: Remove any middle layer, and performance dropped about {2|two} percentage points.
- l44: As the paper put it, "the depth really is important."

## s7 Ending
- l45: So a neural network is just simple little units with knobs, stacked layer on layer.
- l46: Stack them deep enough, and they can recognize complicated things.
- l47: Thirty-seven knobs is easy, but AlexNet had sixty million: how do you work out which way each one turns?
- l48: That's backpropagation, coming up next time.
