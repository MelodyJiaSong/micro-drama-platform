# t01 Overfitting — Script

> In one sentence: Overfitting is memorizing the answers without learning the pattern.

English version of `script.md` (v2, 2026-11-08). Segment ids, line ids and tags match the Chinese script one to one; the wording is rewritten for spoken English, not translated literally.
Each `- lNN: text` is one narration line, subtitle and animation cue; `[pause N]` adds N seconds after the line and is not read.
Spell numbers so the voice reads them correctly when it matters (years, ratios).

## s0 In this episode [package:agenda]
- l01: A model scores almost perfectly on the data you have, then falls apart on new data. That's overfitting. This episode covers four things.
- l02: What the problem is, and what it costs.
- l03: A student who memorized the workbook.
- l04: A different lens: learning patterns, or memorizing data.
- l05: And the trouble it has caused in the real world, and how to prevent it.
- l06: It helps to know what a model is, and what training and test data are. If you don't, that's fine. We'll cover each in a sentence.

## s1 What a model learns [chapter:problem]
- l07: Why would a model ace the data it has, and fail on new data?
- l08: First, what is a model doing? These ten points are the data we collected. This is called the training data.
- l09: They roughly follow some pattern, but every point is a little off, at random. That's noise.
- l10: The model's job is to find the pattern in these points, so it can predict new data it has never seen.

## s2 Three ways to learn
- l11: First, error: how far the points are from the curve. Smaller is better. Model one is too simple. It can only draw a straight line, and it can't even match the training data. That's underfitting.
- l12: Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend.
- l13: Model three is very complex. Its curve twists and turns to hit every single point. On the training data, its error is zero.
- l14: Judged by the workbook alone, model three wins. But does it? [pause 1]

## s3 The exam
- l15: Here are six new points the models have never seen. That's test data. Think of it as the exam.
- l16: Model two stays close to the new points. It does well.
- l17: Model three swings wildly between points, and some new points land far from its curve. Its test error is more than twenty times higher than model two's.
- l18: It memorized the noise in the training data, along with everything else. That's overfitting.
- l19: An underfit model is obviously bad. An overfit model is more dangerous, because on the data you have, it looks great.

## s4 An analogy [chapter:analogy]
- l20: Picture a student who memorizes every answer in the workbook. On workbook problems, he scores a hundred every time.
- l21: But on the exam, when a question changes even slightly, he's lost.
- l22: Or say you're teaching a child to recognize cats. In every photo you show him, the cat is lying on a sofa.
- l23: What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no.
- l24: Memorized answers and memorized coincidences both work on the original questions. Change the setting, and they fail.

## s5 One chart [chapter:experiment]
- l25: Back to our experiment. We repeat it {300|three hundred} times, making the model more and more complex, and watch both errors.
- l26: Training error keeps falling. The more complex the model, the better it does on the practice problems.
- l27: But test error falls, then rises. Only the middle stretch has actually learned the pattern.
- l28: So low training error with high test error is the telltale sign of overfitting.

## s6 Learning is compression [chapter:lens]
- l29: Here's another way to see it. Learning is a kind of compression.
- l30: To remember these ten points exactly, you have to store ten heights.
- l31: Model two describes them, roughly, with just four numbers. And it comes close on points it has never seen.
- l32: Model three has ten numbers, exactly enough to store all ten points as they are. It never needed to find the pattern, so it didn't.
- l33: Real understanding means explaining more with less.

## s7 The real-world cost [chapter:real]
- l34: This isn't just theory. It has caused real trouble.
- l35: Google once estimated flu levels from people's searches. Researchers pointed out that it searched {50 million|fifty million} terms for the best fit to about {1,100|eleven hundred} data points. That's overfitting. It was part flu detector, part winter detector.
- l36: Later versions didn't do much better. From {2011|twenty eleven} to {2013|twenty thirteen}, it overestimated flu in {100|one hundred} out of {108|one hundred and eight} weeks.
- l37: Medical imaging has examples too. Chest X-rays turned out to carry a hospital fingerprint: a separate model could tell, almost perfectly, which hospital each one came from. Part of the pneumonia model's success likely came from recognizing hospitals, not disease. At a new hospital, its performance dropped.
- l38: And a melanoma detector was thrown off by the ink marks doctors draw on skin. With the marks, it called more than half of the harmless moles cancer.
- l39: Those last two are called shortcut learning, a close cousin of overfitting. They look brilliant on the data they were built with, but what they learned was coincidence, not the pattern.

## s8 How to prevent it [chapter:fix]
- l40: So how do you spot and prevent overfitting? Three common ways.
- l41: Earlier, for the demo, we picked the model using the exam itself. In practice, here's what you do. One: set aside another slice of data as a practice exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end.
- l42: Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- l43: Three: limit the model's complexity, so it simply can't memorize every point. These methods are called regularization.

## s9 Outro [package:outro]
- l44: Remember this one sentence.
- l45: Overfitting is memorizing the answers
- l46: without learning the pattern.
- l47: Next time: reinforcement learning.
