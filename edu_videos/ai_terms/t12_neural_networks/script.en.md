# t12 Neural networks and deep learning — narration (English)

v1.3.1 (2026-11-09, trimmed for the 5-minute limit after voicing: l06, l24, l40 names left to the screen, l43; l17 "how steep it gets" because the voice kept slurring "how steeply"). v1.3 (2026-11-09, final wording from the lines_r3 judges: l05, l30 "By the way… faster trick", l22). v1.2 (2026-11-09, per lines_r2 judges: l12 split, l21 last knob shifts the total, l30 and l50 reframed around speed so they no longer repeat l25, l34, l44, l46 tense). v1.1 (2026-11-09, per lines_r1 judges: cold open l01–l03, agenda l06 names AlexNet, l12 ties loss to the score, l21, l30, l31 tense, l33, l46 first-guess accuracy, l50 split; fewer "So" openers). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` only (`drafts/v1_en.md`); the author only split or merged lines to match the Chinese line ids (l12, l16–l17, l18–l19, l28–l29, l36–l37, l39–l40) and checked facts. Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: Remember our two-knob taxi-fare machine? It learned how fares change with distance just fine.
- l02: But fares also depend on the time of day: rush hour costs more, and late night a little more too.
- l03: It can't learn that, because all it can draw is a straight line.
- l04: So how does a machine learn a pattern that bends? With a neural network.

## s1 In this episode [包装:agenda]
- l05: Last time, turning the knobs was like walking downhill blindfolded, always stepping where the score drops fastest.
- l06: Today we'll build a tiny network that learns the bend, see why more layers help, and meet AlexNet.

## s2 Beyond straight lines [章:problem]
- l07: Here's some made-up data: the same {5|five}-kilometer ride, {48|forty-eight} times, at different hours of the day.
- l08: Daytime rides cost about {$23|twenty-three dollars}, just what our two-knob machine charges.
- l09: Around {8|eight} a.m. and {6|six} p.m. it spikes, and late at night it's a bit pricier.
- l10: Same two knobs, one for height and one for slope, but now we feed it the time, not the distance.
- l11: However you turn them, the best you get is a nearly flat line through the middle.
- l12: It undercharges at rush hour and overcharges by day. Its loss, the score for how wrong it is, can't get below {11.5|eleven point five}.
- l13: The knobs aren't the problem: this machine only draws straight lines, and the pattern bends.

## s3 Build a small network [章:experiment]
- l14: The fix isn't one big machine. It's lots of simple little ones.
- l15: Each unit still has two knobs and draws a line, plus one rule: anything below zero becomes zero.
- l16: Its line stays flat, then bends upward.
- l17: The two knobs set where it bends and how steep it gets.
- l18: One bend isn't enough, so add more units that bend in different spots.
- l19: Add them up, and you can build bumps, steps, almost any curve.
- l20: Our network has {12|twelve} units side by side in the first layer, and one unit in the second.
- l21: That unit scales each bent line with a knob, adds them up, then one last knob shifts the total. That's the fare.
- l22: Thirty-seven knobs in all.
- l23: Layers of little units like this are what we call a neural network.
- l24: The name comes from neurons in the brain, but don't take that too seriously.

## s4 Training
- l25: To turn all thirty-seven, we use last episode's trick, nudging every knob whichever way drops the loss fastest.
- l26: Our curve starts as a random squiggle, and step by step it bends toward the peaks.
- l27: After {10,000|ten thousand} steps, the loss is down to {0.26|zero point two six}. The best straight line never got below {11.5|eleven point five}.
- l28: Rush hours and late nights, it catches them all.
- l29: And every corner on this curve is one little unit making its bend.
- l30: By the way, there's a much faster trick for finding which way to turn each knob. More on that next time.

## s5 Why go deep? [章:lens]
- l31: So far, we've put units side by side, each adding one bend.
- l32: Now stack them, so each layer folds the line it gets from the layer before, like folding paper.
- l33: For example, two units per layer can fold a slanted line exactly in half.
- l34: One layer makes two straight pieces, two layers make four, and in this example each new layer doubles that.
- l35: So ten units side by side give at most {11|eleven} pieces. Stacked five deep, they can give {32|thirty-two}.
- l36: Later layers reuse what earlier ones already folded.
- l37: The deeper the stack, the more complex the shapes the same units can build.
- l38: That's the "deep" in deep learning.

## s6 AlexNet, 2012 [章:real]
- l39: In {2012|twenty twelve}, three researchers at the University of Toronto trained a very deep neural network.
- l40: Their network became known as AlexNet.
- l41: It had {8|eight} layers and {60 million|sixty million} knobs. It learned {1,000|a thousand} categories from {1.2 million|one point two million} photos.
- l42: At that year's ImageNet contest, it got five guesses per picture, and only missed if all five were wrong.
- l43: The version they entered got {15.3%|fifteen point three percent} wrong. The runner-up got {26.2%|twenty-six point two}.
- l44: Nobody told it what to look for, yet its first layer learned to spot stripes at every angle, and patches of color.
- l45: Later layers combined those into more and more complex patterns.
- l46: Removing any middle layer made its first-guess accuracy drop about {2|two} percentage points.
- l47: As the paper put it, "the depth really is important."

## s7 Ending [包装:outro]
- l48: So a neural network is just simple little units with knobs, stacked layer on layer.
- l49: Stack them deep enough, and they can recognize really complicated things.
- l50: Thirty-seven knobs, we can test one by one. But sixty million? How do you find which way to turn them all?
- l51: That's backpropagation, coming up next time.
