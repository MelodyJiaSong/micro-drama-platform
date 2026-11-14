# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. Title and chapter cards are silent; they are noted only to mark scene changes.

## Cold open (before the title card)
- l01（6.7s / pause 0.3s）：A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.
- l02（4.5s）：It may not be a bug. It may be a problem called overfitting.

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l03（1.1s / pause 0.4s）：In this episode:
- l04（1.2s / pause 0.4s）：What the problem is.
- l05（2.0s / pause 0.3s）：Why memorizing answers fails.
- l06（1.9s / pause 0.4s）：A different way to think about learning.
- l07（3.2s / pause 0.3s）：Then, real-world failures, and how to avoid them.
- l08（4.5s）：No background needed. We'll explain models and training data as we go.

> [On screen: chapter card “What problem is this?”]

## What a model learns
- l09（9.7s / pause 0.3s）：First, the idea. Overfitting is when a model fits its practice data so closely that it learns the flukes, too, and does worse on new data.
- l10（6.2s / pause 0.3s）：Think of it as memorizing the practice problems without learning the pattern. Let's see it in a small experiment.
- l11（6.9s / pause 0.3s）：These ten points are the data we collected. This is called the training data. Think of it as practice problems.
- l12（5.7s / pause 0.4s）：They follow a pattern, but each point is slightly off. Those random wobbles are called noise.
- l13（6.0s）：The model's job is to find the pattern in these points, so it can predict new data it has never seen.

## Three ways to learn
- l14（9.3s / pause 0.3s）：Model one is too simple. It only draws a straight line. How far each point sits above or below the line, squared and averaged, is the error.
- l15（5.1s / pause 0.3s）：The line can't even get the error down on the practice problems. That's underfitting.
- l16（5.7s / pause 0.4s）：Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- l17（8.0s / pause 0.3s）：Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.
- l18（3.2s）：Quick guess: on new questions, which one does best?

## The exam
- l19（6.7s / pause 0.3s）：Here are six new points the models have never seen. This is the test data. Think of it as the exam.
- l20（3.7s / pause 0.3s）：Model two stays close to the new points. It does best.
- l21（7.8s / pause 0.4s）：Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.
- l22（6.9s / pause 0.4s）：It memorized the noise, too. But noise is random, so it won't repeat on new questions. That's overfitting.
- l23（11.6s）：Underfitting is easy to spot: it's bad on both practice and exam. Overfitting is harder to catch: the practice score can look great. Here, practice error is zero.

> [On screen: chapter card “An analogy”]

## An analogy
- l24（7.9s / pause 0.4s）：Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.
- l25（4.1s / pause 0.3s）：But on the exam, when a question changes even slightly, he's lost.
- l26（10.1s / pause 0.4s）：In our experiment, the workbook is the training data, the typos are noise, and the exam is new data. Forcing the curve through every point is like memorizing.
- l27（8.4s / pause 0.4s）：The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.
- l28（8.9s / pause 0.4s）：Now a related, but different, problem. Say you're teaching a child to recognize cats, and in every photo the cat is lying on a sofa.
- l29（9.9s / pause 0.4s）：What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- l30（11.2s）：Both kids treated the examples in front of them as the rule. The student remembered too much. The child saw too narrow a slice. That second kind is called shortcut learning, and we'll meet it again.

> [On screen: chapter card “Let's run an experiment”]

## One chart
- l31（8.9s / pause 0.3s）：Back to the experiment. We draw three hundred random sets of points, fit models from simple to complex on each, and look at the typical errors.
- l32（6.1s / pause 0.3s）：Practice error keeps falling. The more complex the model, the better it does on the practice problems.
- l33（6.0s / pause 0.4s）：But exam error falls, then rises. Moderately complex models do best on new data.
- l34（4.9s / pause 0.4s）：So low practice error with high exam error is the telltale sign of overfitting.
- l35（10.2s）：So is simpler always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the range where both errors are low.

> [On screen: chapter card “A different lens”]

## Learning is compression
- l36（4.2s / pause 0.4s）：Here's another way to see it. Learning can be seen as a kind of compression.
- l37（3.8s / pause 0.3s）：To remember these ten points exactly, you have to store ten heights.
- l38（6.6s / pause 0.3s）：Model two is set by just four adjustable numbers. It roughly describes the points, and it stays close on new ones.
- l39（9.1s / pause 0.4s）：Model three uses ten numbers, enough for its curve to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise, too.
- l40（6.6s）：Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern, too.

> [On screen: chapter card “The real-world cost”]

## The real-world cost
- l41（2.7s / pause 0.4s）：Problems like this have caused real trouble.
- l42（5.4s / pause 0.3s）：Google once used people's searches to estimate the share of doctor visits for flu-like illness.
- l43（6.4s / pause 0.3s）：Researchers pointed out that its first version tested fifty million search terms for the best fit to about eleven hundred data points.
- l44（10.4s / pause 0.4s）：With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.
- l45（8.7s / pause 0.4s）：Later versions still had problems. From twenty eleven to twenty thirteen, it overestimated flu in one hundred out of one hundred and eight weeks.
- l46（6.5s / pause 0.3s）：Medical imaging has examples too. A model that detected pneumonia in chest X-rays did worse at a new hospital.
- l47（10.6s / pause 0.4s）：Researchers found the X-rays carried a hospital fingerprint: a separate model could identify which hospital scans from two of the hospitals came from, with over ninety-nine point nine percent accuracy.
- l48（9.8s / pause 0.4s）：And the share of scans labeled pneumonia differed widely between hospitals. So part of the pneumonia model's success likely came from recognizing hospitals, not disease.
- l49（13.9s / pause 0.3s）：And a melanoma detector, an AI that spots skin cancer: doctors often draw ink marks around suspicious moles, and it likely learned the marks as a clue. In one study, it flagged over half of the marked harmless moles as cancer.
- l50（11.9s）：Those last two models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They may score well on similar new data, and still fail when the setting changes.

> [On screen: chapter card “How to spot and prevent it”]

## How to prevent it
- l51（4.0s / pause 0.4s）：So how do you spot and prevent overfitting? Three common ways.
- l52（10.3s / pause 0.3s）：One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- l53（6.2s / pause 0.3s）：A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't.
- l54（7.6s / pause 0.3s）：Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- l55（8.6s）：Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.

## Outro (on screen: end card)
- l56（1.5s / pause 0.4s）：Remember this one sentence.
- l57（3.1s / pause 0.3s）：Overfitting is like memorizing even the typos
- l58（1.8s / pause 0.4s）：and trusting them as the rule.
- l59（6.1s）：Next time you're sure you've got it, try a question you've never seen. Next episode: reinforcement learning.

