## s0 Cold open [cold open]
- l01: A model scores almost perfectly on the data it learned from, then gets new data badly wrong.
- l02: Usually that's not a bug in the code. It's a problem called overfitting.

## s2 What overfitting is [chapter:problem]
- l03: Overfitting is when a model learns its practice data too literally, flukes and all, so it does worse on new data.
- l04: Picture a student who memorizes every answer in the workbook, misprints included, and scores {100|a hundred} every time.
- l05: But on the exam, the questions change just a little, and he's lost.
- l06: The workbook is the model's data, and the misprints are what we call noise.
- l07: When a model memorizes the noise as if it were a real pattern, that's overfitting.

## s3 Three ways to learn [chapter:experiment]
- l08: Here are {10|ten} points we collected. This is the training data, our practice questions.
- l09: They roughly follow a pattern, but each one is nudged off by a bit of random wobble. That wobble is the noise.
- l10: The model's job is to find that pattern and predict new points.
- l11: The first model is too simple. It can only draw a straight line.
- l12: The farther a point is from the line, the more it costs. The average cost is the error.
- l13: The line can't even get the practice questions right. That's called underfitting.
- l14: The second model is a gentle curve. It misses some points, but it catches the overall trend.
- l15: The third is really complicated, twisting and turning through every single point, so its practice error is zero.
- l16: So which one do you think will do best on new questions? [pause 1.5]

## s4 The exam
- l17: Now we test them on {6|six} points they've never seen. That's the test data, our exam.
- l18: The second model stays close to all of them, so it does best.
- l19: The third zigzags between the points and lands far from some of the new ones.
- l20: Its exam error is more than twenty times the second model's.
- l21: That's because it memorized the noise, and noise is random, so it doesn't repeat on new questions. That's overfitting.
- l22: Underfitting is easy to spot, because it does badly on practice and exam alike.
- l23: Overfitting is sneakier, because its practice score can look amazing. Here, its practice error was zero.

## s7 Learning is compression [chapter:lens]
- l24: Here's another way to see it. Learning can be thought of as compression.
- l25: To remember these {10|ten} points exactly, you'd need to store {10|ten} numbers, one height per point.
- l26: The second curve takes just {4|four} numbers. It stays close to the points and guesses new ones well, and that's compression.
- l27: The third curve needs {10|ten} numbers to go through {10|ten} points.
- l28: Ten numbers for ten points is no compression at all, so the noise got saved too.
- l29: Good compression keeps the pattern and throws out the noise. Squeeze too hard, like that straight line, and you lose the pattern too.

## s8 One real example [chapter:real]
- l30: Take Google Flu Trends. Google once used people's searches to estimate what share of doctor visits involved flu-like symptoms.
- l31: At first, it went through {50 million|fifty million} search terms for the ones that best tracked {1,152|eleven hundred and fifty-two} flu data points.
- l32: With far more terms than data points, it was bound to pick up some that just happened to spike in winter.
- l33: Researchers said this was overfitting. It was part flu detector, part winter detector.
- l34: Later versions missed too. From {2011|twenty eleven} to {2013|twenty thirteen}, it guessed too high in {100|a hundred} of {108|a hundred and eight} weeks.

## s9 How to prevent it [chapter:fix]
- l35: So how do you catch it and prevent it? There are three common ways.
- l36: First, set aside some data as a practice exam, called a validation set.
- l37: Use it to pick your model and catch overfitting early. Save the real exam for the very end.
- l38: To be honest, in our demo we picked the model by its exam score. On a real project, you shouldn't.
- l39: Second, collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.
- l40: Third, give the model a rule: overly complicated curves get penalized, so it won't chase the noise. That's called regularization.

## s10 Outro [package:outro]
- l41: Overfitting is like memorizing even the misprints. And then you mistake them for real patterns.
- l42: So next time you feel like you totally get something, try a question you've never seen.
- l43: And in the next episode, we'll get into reinforcement learning.
