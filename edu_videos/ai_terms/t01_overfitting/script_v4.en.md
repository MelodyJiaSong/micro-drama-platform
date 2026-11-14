# t01 Overfitting — Script

> In one sentence: Overfitting is memorizing even the typos, and then treating them as rules.

English version of `script.md` (v4.1, 2026-11-09: line review round 2 — l45 numbers, l10/l26 repetition, l14/l30/l37/l48 clarity; v4, 2026-11-08, revised after the line review `reviews/lines_r1/issues.md`: natural spoken agenda, untangled l14/l47/l49, Google Flu Trends named, complete sentences in the outro). Segment ids, line ids and tags match the Chinese script one to one; the wording is rewritten for spoken English, not translated literally. Revised after script review round 1 (`reviews/script_r1/issues.md`). v2 is kept as `script_v2.en.md`.
Each `- lNN: text` is one narration line, subtitle and animation cue; `{display|spoken}` shows the first part in subtitles and has the voice say the second; `[pause N]` adds N seconds after the line.

## s0 Cold open [cold open]
- l01: A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart.
- l02: It may not be a bug. It may be a problem called overfitting.

## s1 In this episode [package:agenda]
- l03: We'll start with a small experiment, so you can watch overfitting happen.
- l04: Then we'll look at real cases where it caused trouble, and how to prevent it.
- l05: No background needed. I'll explain every term as we go.

## s2 What a model learns [chapter:problem]
- l09: Overfitting is when a model fits its practice data so closely that it learns the flukes as well, and then does worse on new data.
- l10: It's like memorizing the practice problems without learning the pattern. Let's see how that happens.
- l11: These ten points are the data we collected. This is called the training data. Think of it as practice problems.
- l12: They follow a pattern, but each point is slightly off. Those random wobbles are called noise.
- l13: The model's job is to find the pattern in these points, so it can predict new data it has never seen.

## s3 Three ways to learn
- l14: Model one is too simple: just a straight line. To score it, we square how far each point misses the line, then average.
- l15: It misses even the practice points by a lot. That's underfitting.
- l16: Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- l17: Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero.
- l18: Quick guess: on new questions, which one does best? [pause 1.5]

## s4 The exam
- l19: Here are six new points the models have never seen. This is the test data. Think of it as the exam.
- l20: Model two stays close to the new points. It does best.
- l21: Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's.
- l22: It memorized the noise as well. But noise is random, so it won't repeat on new questions. That's overfitting.
- l23: Underfitting is easy to spot: it does badly on practice and exam alike. Overfitting is sneakier: it can ace the practice and still fail the exam.

## s5 An analogy [chapter:analogy]
- l24: Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time.
- l25: But on the exam, when a question changes even slightly, he's lost.
- l26: In our experiment, the workbook is the training data, the typos are the noise, and the exam is the test data. The memorizing student is the wiggly curve.
- l27: The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point.
- l28: There's a related problem. Say you're teaching a child to recognize cats, and in every photo, the cat is lying on a sofa.
- l29: What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- l30: Both learned the wrong lesson from their examples. The student memorized every detail; the child latched onto the sofa. The child's mistake is called shortcut learning. We'll come back to it.

## s6 One chart [chapter:experiment]
- l31: Back to the experiment. We repeat it with {300|three hundred} random sets of points, try models from simple to complex on each, and track both errors.
- l32: The more complex the model, the lower its practice error.
- l33: But exam error falls, then rises. Moderately complex models do best on new data.
- l34: Low practice error with high exam error: that's the telltale sign of overfitting.
- l35: Does that mean simpler is always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the middle, where both are low.

## s7 Learning is compression [chapter:lens]
- l36: Here's another way to look at it: learning is a kind of compression.
- l37: To remember these ten points exactly, you have to store ten numbers: how high each point sits.
- l38: Model two's curve is set by just four numbers. That's enough to follow the pattern, and to land close to new points.
- l39: Model three needs ten numbers to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise as well.
- l40: Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern.

## s8 The real-world cost [chapter:real]
- l41: Problems like this have caused real trouble.
- l42: Google Flu Trends used people's searches to estimate what share of doctor visits were for flu-like illness.
- l43: Researchers pointed out that its first version sifted through {50 million|fifty million} search terms to fit about {1,100|eleven hundred} data points.
- l44: With far more terms than data points, some were bound to rise every winter just by coincidence. The researchers called it overfitting: it was part flu detector, part winter detector.
- l45: Later versions still struggled. From {2011|twenty eleven} to {2013|twenty thirteen}, they overestimated flu in {100 out of 108|a hundred out of a hundred and eight} weeks.
- l46: Medical imaging has examples of its own. A model that detected pneumonia in chest X-rays did worse at a new hospital.
- l47: The X-rays carried a hospital fingerprint. A separate model could tell which of two hospitals a scan came from, with over {99.9|ninety-nine point nine} percent accuracy.
- l48: Hospitals also differed widely in how many scans were labeled pneumonia, so knowing the hospital was a clue to the label. Part of the model's success likely came from recognizing the hospital, not the disease.
- l49: Then there's a skin-cancer detector. Doctors often mark suspicious moles with ink, and the model likely learned the ink as a clue. In one study, it flagged over half of the inked harmless moles as cancer.
- l50: The X-ray and mole models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They can do well in familiar settings, and still fail somewhere new.

## s9 How to prevent it [chapter:fix]
- l51: So how do you spot and prevent overfitting? Three common ways.
- l52: One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- l53: A confession: in our experiment, we picked the model by its exam score. In a real project, you shouldn't.
- l54: Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- l55: Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization.

## s10 Outro [package:outro]
- l56: If you remember one thing:
- l57: Overfitting is memorizing even the typos.
- l58: And then treating them as rules.
- l59: Next time you're sure you've got it, try a question you've never seen. Up next: reinforcement learning.
