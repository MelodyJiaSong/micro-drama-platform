# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（5.0s / pause 0.4s）：Last time, we scored the model's mistakes: the lower the score, the better.  [On screen: 「Lower = better」, a chart]
- l02（8.5s / pause 0.3s）：We gave every setting of two knobs a score and drew it as a landscape. The lowest point is the best setting.  [On screen: 「Lowest = best」, 「Lowest point」, a chart]
- l03（1.9s / pause 0.4s）：With two knobs, that's easy.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l04（6.2s / pause 0.4s）：But a big model can have hundreds of billions of knobs, way too many to map.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l05（6.2s / pause 0.4s）：So the model's like someone blindfolded on a mountain, with no idea where the valley is.  [On screen: 「Lowest = best」, 「2 knobs: easy to map」, a chart]
- l06（2.3s / pause 0.4s）：How does it find the bottom?  [On screen: 「Which way down?」, a chart]
- l07（4.2s）：It uses something called gradient descent. Let's see how it works.  [On screen: 「Gradient descent」, a chart]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “Downhill, blindfolded”]

## Downhill, blindfolded
- l08（3.8s / pause 0.4s）：So picture yourself up there, trying to reach the valley.  [On screen: 「Reach the valley」]
- l09（5.8s / pause 0.3s）：You can't see, but your feet feel which way the ground tilts, and how steeply.  [On screen: 「Can’t see」, 「Feet feel the slope」]
- l10（5.0s / pause 0.4s）：So you feel for the steepest way down, and take one small step.  [On screen: 「Steepest way down」, 「One small step」]
- l11（3.1s / pause 0.4s）：Feel again, step again, and you get there.  [On screen: 「Feel, step, repeat」]
- l12（7.3s / pause 0.4s）：For the model, the slope underfoot is how much the score changes when you nudge each knob a little.  [On screen: 「$5.00」, 「$2.00」]
- l13（6.5s / pause 0.4s）：The gradient tells all the knobs which way to turn at once to drop the score fastest.  [On screen: 「↻」, 「↻」]
- l14（6.2s / pause 0.3s）：Gradient descent turns all the knobs one small step that way, then checks the slope again.  [On screen: 「↻」, 「↻」]
- l15（5.4s）：The learning rate sets the step size, and a person picks it before training.  [On screen: 「Learning rate」, 「Step size」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l16（4.2s / pause 0.3s）：Here's last episode's map: base fare across, price per kilometer up.  [On screen: 「Lowest point」, a chart]
- l17（4.2s / pause 0.3s）：Darker means a higher score. The taxi fares are made up.  [On screen: 「Darker = higher score」, 「Lowest point」, a chart]
- l18（7.7s / pause 0.3s）：We start at a five dollar base fare and two dollars a kilometer: a score of seventy-eight, way up high.  [On screen: 「78」, 「0」, a chart]
- l19（3.8s / pause 0.4s）：First, feel the slope: nudge each knob up ten cents.  [On screen: 「78」, 「0」, a chart]
- l20（8.5s / pause 0.4s）：Raise the base fare, and the score drops one point seven. Raise the per-kilometer rate, and it drops eleven point two.  [On screen: 「78」, 「0」, a chart]
- l21（4.6s / pause 0.4s）：So turn both up, but the per-kilometer slope is much steeper.  [On screen: 「78」, 「0」, a chart]
- l22（3.1s / pause 0.4s）：That's the one the first step mostly turns.  [On screen: 「25」, 「1」, a chart]
- l23（6.5s / pause 0.4s）：In three steps, the score falls from seventy-eight to twenty-five, twelve, nine, and we're in the valley.  [On screen: 「9.2」, 「3」, a chart]
- l24（2.7s / pause 0.4s）：The floor is a long, gentle trench.  [On screen: 「9.2」, 「3」, a chart]
- l25（5.8s / pause 0.3s）：The base fare creeps up, the per-kilometer rate eases back, and we inch along.  [On screen: 「4.1」, 「221」, a chart]
- l26（3.5s / pause 0.3s）：Steps scale with the slope, so these get short.  [On screen: 「2.2」, 「682」, a chart]
- l27（6.5s / pause 0.3s）：After a thousand-odd steps, the score's about two. The true minimum is one point nine seven.  [On screen: 「2.0」, 「1200」, a chart]
- l28（5.4s / pause 0.4s）：The knobs end up near a ten-dollar base fare and two fifty a kilometer.  [On screen: 「2.0」, 「1200」, a chart]
- l29（4.6s）：It never saw the whole map. It only felt the ground underfoot.  [On screen: 「2.0」, 「1200」, a chart]

> [On screen: chapter card “How big a step?”]

## How big a step?
- l30（6.5s / pause 0.4s）：That run used a learning rate of zero point zero zero five. What if we'd picked wrong?  [On screen: 「Wrong learning rate?」, 「2.0」]
- l31（4.6s / pause 0.4s）：Here are three paths from the same start, same number of steps.  [On screen: 「Same start, same steps」, 「2.0」]
- l32（5.0s / pause 0.3s）：Make it ten times smaller, and it heads the right way but crawls.  [On screen: 「Same start, same steps」, 「5.6」]
- l33（5.4s / pause 0.4s）：It ends at a score of five point five, still far from the bottom.  [On screen: 「Same start, same steps」, 「5.5」]
- l34（7.3s / pause 0.4s）：Make it about four times the original, and it overshoots across the valley, ending higher than where it started.  [On screen: 「5.5」, 「2.0」, a chart]
- l35（3.1s / pause 0.3s）：Then it climbs higher and higher, past a hundred.  [On screen: 「5.5」, 「2.0」, a chart]
- l36（2.7s / pause 0.4s）：Five steps in, it's off the map.  [On screen: 「5.5」, 「2.0」, a chart]
- l37（3.1s / pause 0.4s）：Our original rate walks steadily to the bottom.  [On screen: 「5.5」, 「2.0」, a chart]
- l38（5.4s / pause 0.4s）：That's why the learning rate is often the single most important setting in training.  [On screen: 「Key setting」, 「5.5」, a chart]
- l39（5.8s）：Too big, and it bounces right off the map. Too small, and you waste time.  [On screen: 「Key setting」, 「5.5」, a chart]

> [On screen: chapter card “Training giant models”]

## How big models train
- l40（3.5s / pause 0.3s）：Big models use gradient descent too, with two upgrades.  [On screen: 「Small batches」, 「Smarter steps」]
- l41（4.2s / pause 0.4s）：First, there's too much data to read it all every step.  [On screen: 「Small batches」]
- l42（6.9s / pause 0.4s）：So each step grabs a small random batch, roughly estimates the slope, and goes. That's stochastic gradient descent.  [On screen: 「Stochastic gradient desc」, 「Small batch」, a chart]
- l43（6.2s / pause 0.3s）：The path wobbles, but it saves loads of computing and still ends up near the bottom.  [On screen: 「Stochastic gradient desc」, 「Wobbly, but gets close」, a chart]
- l44（6.5s / pause 0.4s）：GPT-3, for example, saw only about one part in a hundred thousand of its training data per step.  [On screen: 「≈ 1/100,000」, 「of the training data」]
- l45（8.1s / pause 0.4s）：Second, the steps get smarter. A method called Adam gives each knob its own step size, based on its past slopes.  [On screen: 「Adam」, 「A step size per knob」]
- l46（5.0s / pause 0.4s）：GPT-3 was trained with Adam, and Meta's Llama uses a tweaked version.  [On screen: 「Brown et al. 2020, Appen」, 「GPT-3Adam」]
- l47（6.5s）：That's how GPT-3's hundred and seventy-five billion knobs got turned, one small step at a time.  [On screen: 「175 billion knobs」, 「One small step at a time」]

## Outro (on screen: end card)
- l48（6.5s / pause 0.4s）：Gradient descent is walking downhill blindfolded: feel for the steepest way down, and take a small step.
- l49（3.8s / pause 0.3s）：And the learning rate sets the size of each step.
- l50（4.6s / pause 0.3s）：But a model with just two knobs can only learn so much.
- l51（7.3s / pause 0.4s）：Next time, we'll stack lots of little units in layers, each with its own knobs, and see what happens.
- l52（1.9s）：That's called a neural network.

