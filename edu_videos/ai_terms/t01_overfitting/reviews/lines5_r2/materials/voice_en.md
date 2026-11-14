# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（4.5s / pause 0.4s）：A model aces the data it learned from, then fails badly on new data.  [On screen: 「Training data / Nearly p」, 「New data / Falls apart」]
- l02（4.1s）：Usually that's not a bug in the code. It's a problem called overfitting.  [On screen: 「Overfitting」]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What overfitting is”]

## What overfitting is
- l03（5.7s / pause 0.4s）：Overfitting is when a model learns its practice data too literally, flukes and all, so it does worse on new data.  [On screen: 「Overfitting」, 「Model learns flukes in p」]
- l04（6.6s / pause 0.3s）：Picture a student who memorizes every answer in the workbook, misprints included, and scores a hundred every time.  [On screen: 「100」, 「Even the misprints, memo」]
- l05（4.1s / pause 0.4s）：But on the exam, the questions change just a little, and he's lost.  [On screen: 「A small change, / and he」]
- l06（4.5s / pause 0.3s）：The workbook is the model's data, and the misprints are what we call noise.  [On screen: 「The workbook / → / Train」, 「The misprints / → / Nois」]
- l07（4.8s）：When a model memorizes the noise as if it were a real pattern, that's overfitting.  [On screen: 「The workbook / → / Train」, 「The misprints / → / Nois」]

> [On screen: chapter card “A small experiment”]

## Three ways to learn
- l08（5.0s / pause 0.3s）：Here are ten points we collected. This is the training data, our practice questions.  [On screen: 「Ten points: training dat」]
- l09（6.4s / pause 0.3s）：They roughly follow a pattern, but each one is nudged off by a bit of random wobble. That wobble is the noise.  [On screen: 「Ten points: training dat」, 「Noise: random wobble」]
- l10（3.8s / pause 0.4s）：The model's job is to find that pattern and predict new points.  [On screen: 「Ten points: training dat」, 「Find the pattern / → pre」]
- l11（4.1s / pause 0.3s）：The first model is too simple. It can only draw a straight line.  [On screen: 「Same data, three models」]
- l12（6.2s / pause 0.4s）：The farther a point is from the line, the bigger the mistake. The average mistake is the error.  [On screen: 「Same data, three models」, 「Error」]
- l13（4.7s / pause 0.4s）：The line can't even get the practice questions right. That's called underfitting.  [On screen: 「Same data, three models」, 「Error」]
- l14（5.7s / pause 0.4s）：The second model is a gentle curve. It misses some points, but it catches the overall trend.  [On screen: 「Same data, three models」, 「① Straight line / 0.53 /」]
- l15（6.1s / pause 0.4s）：The third is really complicated, twisting and turning through every single point, so its practice error is zero.  [On screen: 「Same data, three models」, 「① Straight line / 0.53 /」]
- l16（3.2s）：So which one do you think will do best on new questions?  [On screen: 「Which does best on new d」, 「① Straight line / 0.53 /」]

## The exam
- l17（5.0s / pause 0.3s）：Now we test them on six points they've never seen. That's the test data, our exam.  [On screen: 「New questions: the exam」, 「① Line · underfit / 0.53」]
- l18（3.7s / pause 0.3s）：The second model stays close to all of them, so it does best.  [On screen: 「New questions: the exam」, 「① Line · underfit / 0.53」]
- l19（4.7s / pause 0.3s）：The third zigzags between the practice points and misses some new points by a lot.  [On screen: 「New questions: the exam」, 「① Line · underfit / 0.53」]
- l20（3.4s / pause 0.4s）：Its exam error is more than twenty times the second model's.  [On screen: 「Wiggly curve's exam erro」, 「① Line · underfit / 0.53」]
- l21（6.7s / pause 0.3s）：That's because it memorized the noise, and noise is random, so it doesn't repeat on new questions. That's overfitting.  [On screen: 「Noise: memorized, but wo」, 「① Line · underfit / 0.53」]
- l22（5.2s / pause 0.4s）：Underfitting is easy to spot, because it does badly on practice and exam alike.  [On screen: 「Underfit: bad everywhere」]
- l23（6.5s）：Overfitting is sneakier, because its practice score can look amazing. Here, its practice error was zero.  [On screen: 「Underfit: bad everywhere」, 「Overfit: aces practice, 」]

> [On screen: chapter card “Learning as compression”]

## Learning is compression
- l24（3.8s / pause 0.3s）：Here's another way to see it: think of learning as compression.  [On screen: 「Learning ≈ compression」]
- l25（5.8s / pause 0.3s）：To remember these ten points exactly, you'd need to store ten numbers, one height per point.  [On screen: 「How many numbers for 10 」, 「Store as is: 10 numbers」]
- l26（7.1s / pause 0.4s）：The second curve takes just four numbers. It stays close to the points and guesses new ones well, and that's compression.  [On screen: 「How many numbers for 10 」, 「Store as is: 10 numbers」]
- l27（3.5s / pause 0.3s）：The third curve needs ten numbers to go through ten points.  [On screen: 「How many numbers for 10 」, 「Store as is: 10 numbers」]
- l28（4.7s / pause 0.3s）：Ten numbers for ten points is no compression at all, so the noise got saved too.  [On screen: 「How many numbers for 10 」, 「Store as is: 10 numbers」]
- l29（7.0s）：Good compression keeps the pattern and throws out the noise. Squeeze too hard, like that straight line, and you lose the pattern too.  [On screen: 「Keep the pattern, drop t」, 「Squeeze too hard: lose t」]

> [On screen: chapter card “A real example”]

## One real example
- l30（7.6s / pause 0.3s）：Take Google Flu Trends. Google once used people's searches to estimate what share of doctor visits involved flu-like symptoms.  [On screen: 「Google Flu Trends」, 「Estimating flu from sear」]
- l31（5.3s / pause 0.3s）：At first, it sifted fifty million search terms to match about eleven hundred flu data points.  [On screen: 「far more than」, 「Lazer et al. · Science ·」]
- l32（5.5s / pause 0.4s）：With far more terms than data points, it was bound to pick up some that just happened to spike in winter.  [On screen: 「Some terms just peak in 」, 「Lazer et al. · Science ·」]
- l33（5.6s / pause 0.4s）：Researchers said this was overfitting. It was part flu detector, part winter detector.  [On screen: 「“Part flu detector, / pa」, 「The researchers: overfit」]
- l34（5.4s）：Later versions missed too. Out of a hundred and eight weeks, they guessed too high in a hundred.  [On screen: 「100 / 108」, 「weeks too high」]

> [On screen: chapter card “How to prevent overfitting”]

## How to prevent it
- l35（4.3s / pause 0.3s）：So how do you spot it and stop it? Here are three common ways.  [On screen: 「Three common ways」]
- l36（4.9s / pause 0.4s）：First, set aside some data as a mock exam, called a validation set.  [On screen: 「Three common ways」, 「① Validation: mock exam」, a chart]
- l37（5.1s / pause 0.3s）：Use it to pick your model and catch overfitting early. Save the real exam for the very end.  [On screen: 「Three common ways」, 「① Validation: mock exam」, a chart]
- l38（6.7s / pause 0.3s）：To be honest, in our experiment we picked the model by its exam score. On a real project, you shouldn't.  [On screen: 「Three common ways」, 「① Validation: mock exam」, a chart]
- l39（7.7s / pause 0.4s）：Second, collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns.  [On screen: 「Three common ways」, 「① Validation: mock exam」, a chart]
- l40（8.3s）：Third, give the model a rule: overly complicated curves get penalized, so it won't chase the noise. That's called regularization.  [On screen: 「Three common ways」, 「① Validation: mock exam」, a chart]

## Outro (on screen: end card)
- l41（4.5s / pause 0.4s）：Overfitting is memorizing the misprints and mistaking them for real patterns.
- l42（4.5s / pause 0.3s）：So whenever you feel like you totally get something, try a question you've never seen.
- l43（3.3s）：And in the next episode, we'll get into reinforcement learning.

