# t01 Overfitting — Script

> In one sentence: Overfitting is like memorizing even the typos and trusting them as the rule.

English version of `script.md` (v3.1, 2026-11-08). Segment ids, line ids and tags match the Chinese script one to one; the wording is rewritten for spoken English, not translated literally. Revised after script review round 1 (`reviews/script_r1/issues.md`). v2 is kept as `script_v2.en.md`.
Each `- lNN: text` is one narration line, subtitle and animation cue; `{display|spoken}` shows the first part in subtitles and has the voice say the second; `[pause N]` adds N seconds after the line.

## s0 Cold open [cold open]
- l01: A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.
- l02: It may not be a bug. It may be a problem called overfitting.

## s1 In this episode [package:agenda]
- l03: In this episode:
- l04: What the problem is.
- l05: Why memorizing answers fails.
- l06: A different way to think about learning.
- l07: Then, real-world failures, and how to avoid them.
- l08: No background needed. We'll explain models and training data as we go.

## s2 What a model learns [chapter:problem]
- l09: First, the idea. Overfitting is when a model fits its practice data so closely that it learns the flukes, too, and does worse on new data.
- l10: Think of it as memorizing the practice problems without learning the pattern. Let's see it in a small experiment.
- l11: These ten points are the data we collected. This is called the training data. Think of it as practice problems.
- l12: They follow a pattern, but each point is slightly off. Those random wobbles are called noise.
- l13: The model's job is to find the pattern in these points, so it can predict new data it has never seen.

## s3 Three ways to learn
- l14: Model one is too simple. It only draws a straight line. How far each point sits above or below the line, squared and averaged, is the error.
- l15: The line can't even get the error down on the practice problems. That's underfitting.
- l16: Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- l17: Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.
- l18: Quick guess: on new questions, which one does best? [pause 1.5]

## s4 The exam
- l19: Here are six new points the models have never seen. This is the test data. Think of it as the exam.
- l20: Model two stays close to the new points. It does best.
- l21: Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.
- l22: It memorized the noise, too. But noise is random, so it won't repeat on new questions. That's overfitting.
- l23: Underfitting is easy to spot: it's bad on both practice and exam. Overfitting is harder to catch: the practice score can look great. Here, practice error is zero.

## s5 An analogy [chapter:analogy]
- l24: Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.
- l25: But on the exam, when a question changes even slightly, he's lost.
- l26: In our experiment, the workbook is the training data, the typos are noise, and the exam is new data. Forcing the curve through every point is like memorizing.
- l27: The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.
- l28: Now a related, but different, problem. Say you're teaching a child to recognize cats, and in every photo the cat is lying on a sofa.
- l29: What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- l30: Both kids treated the examples in front of them as the rule. The student remembered too much. The child saw too narrow a slice. That second kind is called shortcut learning, and we'll meet it again.

## s6 One chart [chapter:experiment]
- l31: Back to the experiment. We draw {300|three hundred} random sets of points, fit models from simple to complex on each, and look at the typical errors.
- l32: Practice error keeps falling. The more complex the model, the better it does on the practice problems.
- l33: But exam error falls, then rises. Moderately complex models do best on new data.
- l34: So low practice error with high exam error is the telltale sign of overfitting.
- l35: So is simpler always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the range where both errors are low.

## s7 Learning is compression [chapter:lens]
- l36: Here's another way to see it. Learning can be seen as a kind of compression.
- l37: To remember these ten points exactly, you have to store ten heights.
- l38: Model two is set by just four adjustable numbers. It roughly describes the points, and it stays close on new ones.
- l39: Model three uses ten numbers, enough for its curve to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise, too.
- l40: Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern, too.

## s8 The real-world cost [chapter:real]
- l41: Problems like this have caused real trouble.
- l42: Google once used people's searches to estimate the share of doctor visits for flu-like illness.
- l43: Researchers pointed out that its first version tested {50 million|fifty million} search terms for the best fit to about {1,100|eleven hundred} data points.
- l44: With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.
- l45: Later versions still had problems. From {2011|twenty eleven} to {2013|twenty thirteen}, it overestimated flu in {100|one hundred} out of {108|one hundred and eight} weeks.
- l46: Medical imaging has examples too. A model that detected pneumonia in chest X-rays did worse at a new hospital.
- l47: Researchers found the X-rays carried a hospital fingerprint: a separate model could identify which hospital scans from two of the hospitals came from, with over {99.9|ninety-nine point nine} percent accuracy.
- l48: And the share of scans labeled pneumonia differed widely between hospitals. So part of the pneumonia model's success likely came from recognizing hospitals, not disease.
- l49: And a melanoma detector, an AI that spots skin cancer: doctors often draw ink marks around suspicious moles, and it likely learned the marks as a clue. In one study, it flagged over half of the marked harmless moles as cancer.
- l50: Those last two models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They may score well on similar new data, and still fail when the setting changes.

## s9 How to prevent it [chapter:fix]
- l51: So how do you spot and prevent overfitting? Three common ways.
- l52: One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- l53: A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't.
- l54: Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- l55: Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.

## s10 Outro [package:outro]
- l56: Remember this one sentence.
- l57: Overfitting is like memorizing even the typos
- l58: and trusting them as the rule.
- l59: Next time you're sure you've got it, try a question you've never seen. Next episode: reinforcement learning.
