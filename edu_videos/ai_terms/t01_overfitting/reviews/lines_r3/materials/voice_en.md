# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（6.7s / pause 0.3s）：A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.  [On screen: 「Your data / Nearly perfe」, 「New data / Falls apart」]
- l02（4.5s）：It may not be a bug. It may be a problem called overfitting.  [On screen: 「Overfitting」]

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l03（3.9s / pause 0.3s）：We'll start with a small experiment, so you can watch overfitting happen.
- l04（3.9s / pause 0.3s）：Then we'll look at real cases where it caused trouble, and how to prevent it.
- l05（4.0s）：No background needed. I'll explain every term as we go.

> [On screen: chapter card “What overfitting is”]

## What a model learns
- l09（7.7s / pause 0.3s）：Overfitting is when a model fits its practice data so closely that it learns the flukes as well, and then does worse on new data.  [On screen: 「Overfitting」, 「Learns the flukes in its」]
- l10（5.2s / pause 0.3s）：It's like memorizing the practice problems without learning the pattern. Let's see how that happens.  [On screen: 「Overfitting」, 「Learns the flukes in its」]
- l11（6.8s / pause 0.4s）：These ten points are the data we collected. This is called the training data. Think of it as practice problems.  [On screen: 「What a model learns」]
- l12（5.7s / pause 0.4s）：They follow a pattern, but each point is slightly off. Those random wobbles are called noise.  [On screen: 「What a model learns」, 「Noise: random wobble」]
- l13（6.0s）：The model's job is to find the pattern in these points, so it can predict new data it has never seen.  [On screen: 「What a model learns」, 「Find the pattern / → pre」]

## Three ways to learn
- l14（8.2s / pause 0.3s）：Model one is too simple: just a straight line. To score it, we square how far each point misses the line, then average.  [On screen: 「Same data, three models」, 「Error」]
- l15（4.2s / pause 0.3s）：It misses even the practice points by a lot. That's underfitting.  [On screen: 「Same data, three models」, 「Error」]
- l16（5.7s / pause 0.4s）：Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.  [On screen: 「Same data, three models」, 「① Straight line / 0.53 /」]
- l17（8.0s / pause 0.4s）：Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.  [On screen: 「Same data, three models」, 「① Straight line / 0.53 /」]
- l18（3.2s）：Quick guess: on new questions, which one does best?  [On screen: 「Which does best on new d」, 「① Straight line / 0.53 /」]

## The exam
- l19（6.7s / pause 0.3s）：Here are six new points the models have never seen. This is the test data. Think of it as the exam.  [On screen: 「New questions: the exam」, 「① Line · underfit / 0.53」]
- l20（3.7s / pause 0.3s）：Model two stays close to the new points. It does best.  [On screen: 「New questions: the exam」, 「① Line · underfit / 0.53」]
- l21（7.8s / pause 0.4s）：Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.  [On screen: 「Exam error: ③ ≈ 25× ②」, 「① Line · underfit / 0.53」]
- l22（7.0s / pause 0.3s）：It memorized the noise as well. But noise is random, so it won't repeat on new questions. That's overfitting.  [On screen: 「Memorized noise won't re」, 「① Line · underfit / 0.53」]
- l23（9.6s）：Underfitting is easy to spot: it does badly on practice and exam alike. Overfitting is sneakier: it can ace the practice and still fail the exam.  [On screen: 「Underfit: fails both, ea」, 「Overfit: aces practice, 」]

> [On screen: chapter card “An analogy”]

## An analogy
- l24（7.9s / pause 0.4s）：Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.  [On screen: 「100」, 「Even the typos, memorize」]
- l25（4.1s / pause 0.3s）：But on the exam, when a question changes even slightly, he's lost.  [On screen: 「A small change, / and he」]
- l26（9.3s / pause 0.4s）：In our experiment, the workbook is the training data, the typos are the noise, and the exam is the test data. The memorizing student is the wiggly curve.  [On screen: 「The workbook / → / Train」, 「The typos / → / Noise」]
- l27（8.4s / pause 0.3s）：The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.  [On screen: 「Student: knows it」, 「Model: doesn't」]
- l28（7.5s / pause 0.3s）：There's a related problem. Say you're teaching a child to recognize cats, and in every photo, the cat is lying on a sofa.  [On screen: 「Every cat: on a sofa」]
- l29（9.9s / pause 0.4s）：What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.  [On screen: 「Maybe his rule: sofa = c」, 「“Cat!”」]
- l30（11.6s）：Both learned the wrong lesson from their examples. The student memorized every detail; the child latched onto the sofa. The child's mistake is called shortcut learning. We'll come back to it.  [On screen: 「Memorized every detail」, 「Latched onto the sofa」]

> [On screen: chapter card “Two error curves”]

## One chart
- l31（8.5s / pause 0.3s）：Back to the experiment. We repeat it with three hundred random sets of points, try models from simple to complex on each, and track both errors.  [On screen: 「300」, 「Complexity vs. error」, a chart]
- l32（3.6s / pause 0.3s）：The more complex the model, the lower its practice error.  [On screen: 「300」, 「Complexity vs. error」, a chart]
- l33（6.0s / pause 0.4s）：But exam error falls, then rises. Moderately complex models do best on new data.  [On screen: 「Complexity vs. error」, a chart]
- l34（4.5s / pause 0.3s）：Low practice error with high exam error: that's the telltale sign of overfitting.  [On screen: 「Warning sign: low practi」, a chart]
- l35（9.5s）：Does that mean simpler is always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the middle, where both are low.  [On screen: 「Too simple: both errors 」, a chart]

> [On screen: chapter card “Learning ≈ compression”]

## Learning is compression
- l36（4.2s / pause 0.3s）：Here's another way to look at it: learning is a kind of compression.  [On screen: 「Learning ≈ compression」]
- l37（5.7s / pause 0.3s）：To remember these ten points exactly, you have to store ten numbers: how high each point sits.  [On screen: 「Numbers needed for 10 po」, 「Store as is: 10 numbers」]
- l38（6.4s / pause 0.4s）：Model two's curve is set by just four numbers. That's enough to follow the pattern, and to land close to new points.  [On screen: 「Numbers needed for 10 po」, 「Store as is: 10 numbers」]
- l39（8.1s / pause 0.3s）：Model three needs ten numbers to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise as well.  [On screen: 「Numbers needed for 10 po」, 「Store as is: 10 numbers」]
- l40（6.7s）：Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern.  [On screen: 「Keep the pattern, drop t」, 「Squeeze too hard: lose t」]

> [On screen: chapter card “Real-world failures”]

## The real-world cost
- l41（2.7s / pause 0.4s）：Problems like this have caused real trouble.  [On screen: 「Three real cases」]
- l42（5.9s / pause 0.3s）：Google Flu Trends used people's searches to estimate what share of doctor visits were for flu-like illness.  [On screen: 「Flu, estimated from sear」]
- l43（6.5s / pause 0.3s）：Researchers pointed out that its first version sifted through fifty million search terms to fit about eleven hundred data points.  [On screen: 「far more than」, 「Lazer et al. · Science ·」]
- l44（10.4s / pause 0.4s）：With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.  [On screen: 「“Part flu detector, / pa」, 「The researchers: overfit」]
- l45（8.3s / pause 0.4s）：Later versions still struggled. From twenty eleven to twenty thirteen, they overestimated flu in a hundred out of a hundred and eight weeks.  [On screen: 「100」, 「/ 108」]
- l46（7.1s / pause 0.4s）：Medical imaging has examples of its own. A model that detected pneumonia in chest X-rays did worse at a new hospital.  [On screen: 「New hospital, worse resu」, 「Zech et al. · PLOS Medic」]
- l47（8.8s / pause 0.4s）：The X-rays carried a hospital fingerprint. A separate model could tell which of two hospitals a scan came from, with over ninety-nine point nine percent accuracy.  [On screen: 「> 99.9%」, 「>」]
- l48（12.1s / pause 0.4s）：Hospitals also differed widely in how many scans were labeled pneumonia, so knowing the hospital was a clue to the label. Part of the model's success likely came from recognizing the hospital, not the disease.  [On screen: 「34%」, 「34% vs 1%」]
- l49（11.6s / pause 0.3s）：Then there's a skin-cancer detector. Doctors often mark suspicious moles with ink, and the model likely learned the ink as a clue. In one study, it flagged over half of the inked harmless moles as cancer.  [On screen: 「54%」, 「of inked harmless moles 」]
- l50（11.8s）：The X-ray and mole models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They can do well in familiar settings, and still fail somewhere new.  [On screen: 「Can fail somewhere new」, 「May do well in familiar 」]

> [On screen: chapter card “Spot it, prevent it”]

## How to prevent it
- l51（4.0s / pause 0.4s）：So how do you spot and prevent overfitting? Three common ways.  [On screen: 「Three common ways」]
- l52（10.3s / pause 0.3s）：One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.  [On screen: 「Three common ways」, 「① Validation: a mock exa」, a chart]
- l53（6.2s / pause 0.3s）：A confession: in our experiment, we picked the model by its exam score. In a real project, you shouldn't.  [On screen: 「Three common ways」, 「① Validation: a mock exa」, a chart]
- l54（7.6s / pause 0.4s）：Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.  [On screen: 「Three common ways」, 「① Validation: a mock exa」, a chart]
- l55（8.6s）：Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.  [On screen: 「Three common ways」, 「① Validation: a mock exa」, a chart]

## Outro (on screen: end card)
- l56（1.4s / pause 0.4s）：If you remember one thing:
- l57（2.7s / pause 0.3s）：Overfitting is memorizing even the typos.
- l58（2.1s / pause 0.4s）：And then treating them as rules.
- l59（5.9s）：Next time you're sure you've got it, try a question you've never seen. Up next: reinforcement learning.

