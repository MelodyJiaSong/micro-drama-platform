# Script (English)

### s0 Cold open（冷开场）
| 句号 | English |
|---|---|
| l01 | A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart. |
| l02 | Often the code isn't broken at all. The model has a problem called overfitting. |

### s1 In this episode（包装卡 agenda）
| 句号 | English |
|---|---|
| l03 | In this episode: |
| l04 | What the problem is. |
| l05 | Why memorizing answers fails. |
| l06 | A different way to think about learning. |
| l07 | Then, real-world failures, and how to avoid them. |
| l08 | No background needed. We'll explain models and training data as we go. |

### s2 What a model learns（章节 problem）
| 句号 | English |
|---|---|
| l09 | First, the idea. Overfitting is when a model fits its practice data so closely that it learns the accidents, too, and does worse on new data. |
| l10 | Think of it as memorizing the practice problems without learning the pattern. Let's see it in a small experiment. |
| l11 | These ten points are the data we collected. This is called the training data. Think of it as practice problems. |
| l12 | They follow a pattern, but each point is slightly off. Those random wobbles are called noise. |
| l13 | The model's job is to find the pattern in these points, so it can predict new data it has never seen. |

### s3 Three ways to learn
| 句号 | English |
|---|---|
| l14 | Model one is too simple. It only draws a straight line. The gap between each point and the line is the error. |
| l15 | The line can't even get the error down on the practice problems. That's underfitting. |
| l16 | Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend. |
| l17 | Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero. |
| l18 | Quick guess: on new questions, which one does best? |

### s4 The exam
| 句号 | English |
|---|---|
| l19 | Here are six new points the models have never seen. This is the test data. Think of it as the exam. |
| l20 | Model two stays close to the new points. It does best. |
| l21 | Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's. |
| l22 | It memorized the noise, too. But noise is random, so it won't repeat on new questions. That's overfitting. |
| l23 | Underfitting is easy to spot: it's bad on both practice and exam. Overfitting is harder to catch: zero practice error, and it looks great. |

### s5 An analogy（章节 analogy）
| 句号 | English |
|---|---|
| l24 | Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time. |
| l25 | But on the exam, when a question changes even slightly, he's lost. |
| l26 | In our experiment, the workbook is the training data, the typos are the noise, and the exam is new data. Memorizing is that curve forced through every point. |
| l27 | The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply powerful enough to remember every point. |
| l28 | Now a related, but different, problem. Say you're teaching a child to recognize cats, and in every photo the cat is lying on a sofa. |
| l29 | What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no. |
| l30 | Both kids trusted something that's only true of the data at hand. The student remembered too much. The child saw too little. That second kind is called shortcut learning, and we'll meet it again. |

### s6 One chart（章节 experiment）
| 句号 | English |
|---|---|
| l31 | Back to the experiment. We draw 300 random sets of points, fit models from simple to complex on each, and average both errors. |
| l32 | Practice error keeps falling. The more complex the model, the better it does on the practice problems. |
| l33 | But exam error falls, then rises. Models of middle complexity predict new data best. |
| l34 | So low practice error with high exam error is the telltale sign of overfitting. |
| l35 | So is simpler always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the sweet spot in the middle. |

### s7 Learning is compression（章节 lens）
| 句号 | English |
|---|---|
| l36 | Here's another way to see it. Learning can be seen as a kind of compression. |
| l37 | To remember these ten points exactly, you have to store ten heights. |
| l38 | Model two is set by just four adjustable numbers. It roughly describes the points, and it stays close on new ones. |
| l39 | Model three has ten numbers, exactly enough to pass through all ten points. It stores the noise, too, so new points come out wrong. |
| l40 | Good compression throws away exactly the noise. What's left is the pattern. |

### s8 The real-world cost（章节 real）
| 句号 | English |
|---|---|
| l41 | Overfitting has caused real trouble. |
| l42 | Google once used people's searches to estimate flu levels. |
| l43 | Researchers pointed out that its first version tested 50 million search terms for the best fit to about 1,100 data points. |
| l44 | Far more choices than data, like ten numbers for ten points. The researchers called it overfitting: it was part flu detector, part winter detector. |
| l45 | Later versions still had problems. From 2011 to 2013, it overestimated flu in 100 out of 108 weeks. |
| l46 | Medical imaging has examples too. A model that detected pneumonia in chest X-rays did worse at a new hospital. |
| l47 | Researchers found the X-rays carried a hospital fingerprint: a separate model could tell scans from two of the hospitals apart with over 99.9 percent accuracy. |
| l48 | So part of the pneumonia model's success likely came from recognizing hospitals, not disease. |
| l49 | And a melanoma detector, an AI that spots skin cancer, was fooled by the ink marks doctors draw on skin. In one study, it flagged over half of the marked harmless moles as cancer. |
| l50 | Those last two, like the child with the cats, are shortcut learning, a close cousin of overfitting. They can still score well on similar data, and only fail when the setting changes. |

### s9 How to prevent it（章节 fix）
| 句号 | English |
|---|---|
| l51 | So how do you spot and prevent overfitting? Three common ways. |
| l52 | One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end. |
| l53 | A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't. |
| l54 | Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns. |
| l55 | Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization. |

### s10 Outro（包装卡 outro）
| 句号 | English |
|---|---|
| l56 | Remember this one sentence. |
| l57 | Overfitting is memorizing the practice problems |
| l58 | without learning the pattern. |
| l59 | Next time you're sure you've got it, try a question you've never seen. Next episode: reinforcement learning. |
