# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（5.0s / pause 0.4s）：Last time, we scored the model's mistakes: the lower the score, the better.  [On screen: 「Lower is better」, a chart]
- l02（6.9s / pause 0.4s）：We mapped every setting of two knobs into a landscape, and the lowest point is the best setting.  [On screen: 「Lowest = best」, 「Lowest point」, a chart]
- l03（5.4s / pause 0.3s）：With two knobs, you can work out every setting and draw that whole map.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l04（6.5s / pause 0.4s）：But a real model has hundreds of billions of knobs, so there's no drawing the whole map.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l05（5.8s / pause 0.4s）：So the model is on a mountain blindfolded, with no idea where the valley is.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l06（2.3s / pause 0.3s）：How does it find the bottom?  [On screen: 「How to find the bottom?」, a chart]
- l07（3.8s）：It uses something called gradient descent, and that's today's topic.  [On screen: 「Gradient descent」, a chart]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “Downhill, blindfolded”]

## Downhill, blindfolded
- l08（4.2s / pause 0.3s）：Picture yourself blindfolded on a hillside, trying to reach the valley.  [On screen: 「Reach the valley」]
- l09（5.8s / pause 0.4s）：You can't see, but your feet feel which way the ground tilts, and how steeply.  [On screen: 「Can’t see」, 「Feet feel the slope」]
- l10（5.0s / pause 0.3s）：So you feel for the steepest way down, and take one small step.  [On screen: 「Steepest way down」, 「One small step」]
- l11（3.1s / pause 0.4s）：Feel again, step again, and you get there.  [On screen: 「Feel, step, repeat」]
- l12（7.3s / pause 0.3s）：For the model, the slope underfoot is how much the score changes when you nudge each knob a little.  [On screen: 「$5.00」, 「$2.00」]
- l13（6.2s / pause 0.4s）：Which way each knob should turn to drop the score fastest, all together, is the gradient.  [On screen: 「↻」, 「↻」]
- l14（6.2s / pause 0.3s）：Gradient descent turns all the knobs one small step that way, then checks the slope again.  [On screen: 「↻」, 「↻」]
- l15（5.8s）：How big each step is, that's the learning rate, set by a person before training.  [On screen: 「How big each step」, 「$5.40」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l16（4.2s / pause 0.3s）：Here's last episode's map: base fare across, price per kilometer up.  [On screen: 「Lowest point」, a chart]
- l17（4.2s / pause 0.3s）：Darker means a higher score, and the taxi data is illustrative.  [On screen: 「Darker = higher score」, 「Lowest point」, a chart]
- l18（7.7s / pause 0.3s）：We start at a five dollar base fare and two dollars a kilometer: a score of seventy-eight, way up high.  [On screen: 「78」, 「0」, a chart]
- l19（3.8s / pause 0.4s）：First, feel the slope: nudge each knob up ten cents.  [On screen: 「78」, 「0」, a chart]
- l20（6.2s / pause 0.4s）：The base fare drops the score one point seven, and per kilometer drops it eleven point two.  [On screen: 「78」, 「0」, a chart]
- l21（3.8s / pause 0.4s）：Both should go up, but per kilometer is much steeper.  [On screen: 「78」, 「0」, a chart]
- l22（3.1s / pause 0.4s）：So the first step mostly turns that one.  [On screen: 「25」, 「1」, a chart]
- l23（6.5s / pause 0.4s）：In three steps, the score falls from seventy-eight to twenty-five, twelve, nine, and we're in the valley.  [On screen: 「9.2」, 「3」, a chart]
- l24（2.7s / pause 0.4s）：The floor is a long, gentle trench.  [On screen: 「9.2」, 「3」, a chart]
- l25（5.4s / pause 0.4s）：The base fare creeps up, per kilometer eases back, and we inch along it.  [On screen: 「4.2」, 「216」, a chart]
- l26（3.1s / pause 0.4s）：The gentler the slope, the shorter each step.  [On screen: 「2.2」, 「679」, a chart]
- l27（6.5s / pause 0.3s）：After a thousand-odd steps, the score's about two. The true minimum is one point nine seven.  [On screen: 「2.0」, 「1200」, a chart]
- l28（4.2s / pause 0.4s）：The knobs sit around ten dollars base and two fifty a kilometer.  [On screen: 「2.0」, 「1200」, a chart]
- l29（4.6s）：It never saw the whole map. It only felt the ground underfoot.  [On screen: 「2.0」, 「1200」, a chart]

> [On screen: chapter card “How big a step?”]

## How big a step?
- l30（6.9s / pause 0.4s）：That run used a learning rate of zero point zero zero five, so what if we'd picked wrong?  [On screen: 「What if it’s wrong?」, 「2.0」]
- l31（4.6s / pause 0.3s）：Here are three paths from the same start, same number of steps.  [On screen: 「Same start, same steps」, 「2.0」]
- l32（6.5s / pause 0.4s）：Ten times smaller, zero point zero zero zero five, and it heads the right way but crawls.  [On screen: 「Same start, same steps」, 「5.6」]
- l33（5.4s / pause 0.4s）：It ends at a score of five point five, still far from the bottom.  [On screen: 「Same start, same steps」, 「5.5」]
- l34（7.7s / pause 0.3s）：About four times bigger, zero point zero two one, and it overshoots across the valley, higher than where it started.  [On screen: 「5.5」, 「2.0」, a chart]
- l35（2.7s / pause 0.4s）：Then higher and higher: ninety-six, a hundred eighteen, a hundred forty-five.  [On screen: 「5.5」, 「2.0」, a chart]
- l36（2.7s / pause 0.4s）：Five steps in, it's off the map.  [On screen: 「5.5」, 「2.0」, a chart]
- l37（3.5s / pause 0.4s）：The one in between walks steadily to the bottom.  [On screen: 「5.5」, 「2.0」, a chart]
- l38（5.4s / pause 0.4s）：That's why the learning rate is often the single most important setting in training.  [On screen: 「Often the key setting」, 「5.5」, a chart]
- l39（5.0s）：Too big, and it bounces right off the map. Too small, and you waste time.  [On screen: 「Often the key setting」, 「5.5」, a chart]

> [On screen: chapter card “How big models train”]

## How big models train
- l40（3.8s / pause 0.4s）：Real large models use gradient descent too, with two upgrades.  [On screen: 「A small batch per step」, 「Smarter steps」]
- l41（4.2s / pause 0.4s）：First, there's too much data to read it all every step.  [On screen: 「A small batch per step」]
- l42（6.9s / pause 0.3s）：So each step grabs a small random batch, roughly estimates the slope, and goes. That's stochastic gradient descent.  [On screen: 「3 rides per step」, 「Small batch」, a chart]
- l43（6.2s / pause 0.4s）：The path wobbles, but it saves loads of computing and still ends up near the bottom.  [On screen: 「3 rides per step」, 「Wobbly, still gets there」, a chart]
- l44（5.8s / pause 0.4s）：GPT-3, for example, saw only about one hundred-thousandth of its training data per step.  [On screen: 「≈ 1/100,000」, 「of the training data」]
- l45（6.9s / pause 0.4s）：Second, smarter steps: Adam, from twenty fourteen, gives each knob its own step size, based on its past slopes.  [On screen: 「Adam」, 「Each knob gets its own s」]
- l46（4.6s / pause 0.4s）：GPT-3 was trained with Adam, and Meta's Llama uses a tweaked version.  [On screen: 「Brown et al. 2020, Appen」, 「GPT-3Adam」]
- l47（5.8s）：That's how GPT-3's a hundred seventy-five billion knobs got turned, one small step at a time.  [On screen: 「175 billion knobs」, 「Turned one small step at」]

## Outro (on screen: end card)
- l48（7.3s / pause 0.3s）：Gradient descent is walking downhill blindfolded: each step, feel for the steepest way down and take one small step.
- l49（3.8s / pause 0.4s）：And how big those steps are is the learning rate.
- l50（4.6s / pause 0.4s）：But a straight line with two knobs can only learn so much.
- l51（6.2s / pause 0.3s）：Next time, we'll stack lots of little knob-filled units in layers, and see what happens.
- l52（1.9s）：That's called a neural network.

