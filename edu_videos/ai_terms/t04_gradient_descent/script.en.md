# t04 Gradient descent — narration (English)

v1.3 (2026-11-09, per lines_r3 final judges, wording used verbatim: l02, l13, l16–l17; suggestions l15, l22, l26). v1.2 (2026-11-09, per lines_r2 judges: l13, l15/l26/l49 step size vs slope, l20–l22, l32/l34/l35, l45 strict link). v1.1 (2026-11-09, per lines_r1 judges: cold open l03–l04, l07, l13 definition, l20–l21, l30 strict link, l32/l34, l45, outro l48/l50/l51). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` (`drafts/v1_en.md`); the author only split and joined lines to match the Chinese line ids, and checked facts. Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: Last time, we scored the model's mistakes: the lower the score, the better.
- l02: We scored every setting of the two knobs and drew the scores as a landscape. The lowest point is the best setting.
- l03: With two knobs, that's easy.
- l04: But a big model can have hundreds of billions of knobs, way too many to map.
- l05: So the model's like someone blindfolded on a mountain, with no idea where the valley is.
- l06: How does it find the bottom?
- l07: It uses something called gradient descent. Let's see how it works.

## s2 Downhill, blindfolded [章:analogy]
- l08: So picture yourself up there, trying to reach the valley.
- l09: You can't see, but your feet feel which way the ground tilts, and how steeply.
- l10: So you feel for the steepest way down, and take one small step.
- l11: Feel again, step again, and you get there.
- l12: For the model, the slope underfoot is how much the score changes when you nudge each knob a little.
- l13: Put those slopes together, and that's the gradient. It shows every knob the fastest way down.
- l14: Gradient descent turns all the knobs one small step that way, then checks the slope again.
- l15: The learning rate sets the step size, and you pick it before training starts.

## s3 A small experiment [章:experiment]
- l16: Let's try it on the taxi map: base fare across, per-kilometer rate up.
- l17: Darker means a higher score. The fares are made up.
- l18: We start at a {5|five} dollar base fare and {2|two} dollars a kilometer: a score of {78|seventy-eight}, way up high.
- l19: First, feel the slope: nudge each knob up ten cents.
- l20: Raise the base fare, and the score drops {1.7|one point seven}. Raise the per-kilometer rate, and it drops {11.2|eleven point two}.
- l21: So turn both up, but the per-kilometer slope is much steeper.
- l22: Our first step turns that knob the most.
- l23: In three steps, the score falls from {78|seventy-eight} to {25|twenty-five}, {12|twelve}, {9|nine}, and we're in the valley.
- l24: The floor is a long, gentle trench.
- l25: The base fare creeps up, the per-kilometer rate eases back, and we inch along.
- l26: Gentler slopes mean smaller steps, so we slow down.
- l27: After a thousand-odd steps, the {score's|score is} about {2|two}. The true minimum is {1.97|one point nine seven}.
- l28: The knobs end up near a ten-dollar base fare and two fifty a kilometer.
- l29: It never saw the whole map. It only felt the ground underfoot.

## s4 How big a step? [章:lens]
- l30: That run used a learning rate of {0.005|zero point zero zero five}. What if we'd picked wrong?
- l31: Here are three paths from the same start, same number of steps.
- l32: Make it ten times smaller, and it heads the right way but crawls.
- l33: It ends at a score of {5.5|five point five}, still far from the bottom.
- l34: Make it about four times the original, and it overshoots across the valley, ending higher than where it started.
- l35: Then it climbs higher and higher, past a hundred.
- l36: Five steps in, it's off the map.
- l37: Our original rate walks steadily to the bottom.
- l38: That's why the learning rate is often the single most important setting in training.
- l39: Too big, and it bounces right off the map. Too small, and you waste time.

## s5 Training giant models [章:real]
- l40: Big models use gradient descent too, with two upgrades.
- l41: First, there's too much data to read it all every step.
- l42: So each step grabs a small random batch, roughly estimates the slope, and goes. That's stochastic gradient descent.
- l43: The path wobbles, but it saves loads of computing and still ends up near the bottom.
- l44: GPT-3, for example, saw only about {1/100,000|one part in a hundred thousand} of its training data per step.
- l45: Second, the steps get smarter. A method called Adam gives each knob its own step size, based on its past slopes.
- l46: {GPT-3|GPT three} was trained with Adam, and Meta's Llama uses a tweaked version.
- l47: That's how GPT-3's {175 billion|one hundred seventy-five billion} knobs got turned, one small step at a time.

## s6 Wrap-up [包装:outro]
- l48: Gradient descent is walking downhill blindfolded: feel for the steepest way down, and take a small step.
- l49: And the learning rate sets the size of each step.
- l50: But a model with just two knobs can only learn so much.
- l51: Next time, we'll stack lots of little units in layers, each with its own knobs, and see what happens.
- l52: That's called a neural network.
