## s0 Cold open
- l01: Last time, we scored the model's mistakes, lower is better, and mapped two knobs' settings into a landscape.
- l02: The lowest point is the best setting.
- l03: With two knobs, you can draw that whole map; a real model has hundreds of billions.
- l04: So it's on a mountain blindfolded, with no idea where the valley is.
- l05: How does it find the bottom?
- l06: It uses something called gradient descent, and that's today's topic.

## s2 Downhill, blindfolded
- l07: Picture yourself blindfolded on a hillside, trying to reach the valley.
- l08: You can't see, but your feet feel which way the ground tilts, and how steeply.
- l09: So you feel for the steepest way down, and take one small step.
- l10: Feel again, step again, and you get there.
- l11: For the model, the slope underfoot is how much the score changes when you nudge each knob a little.
- l12: Which way each knob should turn to drop the score fastest, all together, is the gradient.
- l13: Gradient descent turns all the knobs one small step that way, then checks the slope again.
- l14: How big each step is, that's the learning rate, set by a person before training.

## s3 A little experiment
- l15: Here's last episode's map, with illustrative taxi data: base fare across, per kilometer up, darker means a higher score.
- l16: We start at a {5|five} dollar base fare and {2|two} dollars a kilometer: a score of {78|seventy-eight}, way up high.
- l17: Nudge each knob up ten cents: the base fare drops the score {1.7|one point seven}, per kilometer drops it {11.2|eleven point two}.
- l18: Both should go up, but per kilometer is much steeper, so the first step mostly turns that.
- l19: In three steps, the score falls from {78|seventy-eight} to {25|twenty-five}, {12|twelve}, {9|nine}, and we're in the valley.
- l20: The floor is a long, gentle trench: the base fare creeps up, per kilometer eases back, and we inch along.
- l21: The gentler the slope, the shorter each step.
- l22: After a thousand-odd steps, the score's about {2|two}; the true minimum is {1.97|one point nine seven}.
- l23: The knobs sit around {10|ten} dollars base and {2.50|two fifty} a kilometer.
- l24: It never saw the whole map; it only felt the ground underfoot.

## s4 How big a step
- l25: That run used a learning rate of {0.005|zero point zero zero five}, so what if we'd picked wrong?
- l26: Here are three paths from the same start, same number of steps.
- l27: Ten times smaller, {0.0005|zero point zero zero zero five}, and it heads the right way but crawls, ending at {5.5|five point five}.
- l28: About four times bigger, {0.021|zero point zero two one}, and it overshoots across the valley, higher than where it started.
- l29: Then higher and higher: {96|ninety-six}, {118|a hundred eighteen}, {145|a hundred forty-five}, and five steps in, it's off the map.
- l30: The one in the middle walks steadily to the bottom.
- l31: That's why the learning rate is often the single most important setting in training.
- l32: Too big, and you fly off course; too small, and you waste time.

## s5 How big models are trained
- l33: Real large models use gradient descent too, with two upgrades.
- l34: First, there's too much data to read it all every step.
- l35: So each step grabs a small random batch, roughly estimates the slope, and goes; that's stochastic gradient descent.
- l36: The path wobbles, but saves loads of computing and still ends up near the bottom.
- l37: GPT-3, for example, saw only about {1/100,000|one hundred-thousandth} of its training data per step.
- l38: Second, smarter steps.
- l39: Adam, from {2014|twenty fourteen}, gives each knob its own step size, based on its past slopes.
- l40: GPT-3 was trained with Adam; Meta's Llama uses a tweaked version.
- l41: That's how GPT-3's {175 billion|a hundred seventy-five billion} knobs got turned, one small step at a time.

## s6 Wrap-up
- l42: Gradient descent is walking downhill blindfolded: each step, feel for the steepest way down and take one small step.
- l43: And how big those steps are is the learning rate.
- l44: But a straight line with two knobs can only learn so much.
- l45: Next time, we'll stack lots of little knob-filled units in layers, and see what happens.
- l46: That episode is about neural networks.
