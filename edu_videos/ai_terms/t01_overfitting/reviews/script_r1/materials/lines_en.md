# Script (English)

### s0 Cold open（冷开场）
| 句号 | English |
|---|---|
| l01 | A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart. |
| l02 | The code isn't broken. The problem has a name: overfitting. |

### s1 In this episode（包装卡 agenda）
| 句号 | English |
|---|---|
| l03 | Here's what we'll cover. |
| l04 | What the problem is. |
| l05 | A student who memorized the workbook. |
| l06 | A different way to think about learning. |
| l07 | And the trouble it has caused in the real world, and how to prevent it. |
| l08 | No background needed. We'll explain models and training data as we go. |

### s2 What a model learns（章节 problem）
| 句号 | English |
|---|---|
| l09 | Here it is in one sentence: overfitting is memorizing the practice problems without learning the pattern. Let's see it in a small experiment. |
| l10 | These ten points are the data we collected. This is called the training data. Think of it as practice problems. |
| l11 | They roughly follow some pattern, but every point is a little off, at random. That's noise. |
| l12 | The model's job is to find the pattern in these points, so it can predict new data it has never seen. |

### s3 Three ways to learn
| 句号 | English |
|---|---|
| l13 | First, error: how far the points are from the curve. Smaller is better. Model one is too simple. It only draws a straight line, and it can't even match the practice problems. That's underfitting. |
| l14 | Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend. |
| l15 | Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero. |
| l16 | Quick guess: on new questions, which one does best? |

### s4 The exam
| 句号 | English |
|---|---|
| l17 | Here are six new points the models have never seen. This is the test data. Think of it as the exam. |
| l18 | Model two stays close to the new points. It does well. |
| l19 | Model three swings wildly between the points, and some new points land far from its curve. Its exam error is more than twenty times higher than model two's. |
| l20 | It memorized the noise in the practice problems, along with everything else. That's overfitting. |
| l21 | An underfit model is obviously bad. An overfit model is more dangerous, because on the data you have, it looks great. |

### s5 An analogy（章节 analogy）
| 句号 | English |
|---|---|
| l22 | Picture a student who memorizes every answer in the workbook. On workbook problems, he scores a hundred every time. |
| l23 | But on the exam, when a question changes even slightly, he's lost. |
| l24 | Map it back to our experiment: the workbook is the training data, the exam is new data, and the memorized answers are that curve forced through every point. |
| l25 | Or say you're teaching a child to recognize cats. In every photo you show him, the cat is lying on a sofa. |
| l26 | What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no. |
| l27 | Both are the same mistake: learning something that's only true of the data at hand. The analogy has a limit, though. A model isn't lazy. It's simply allowed to remember too much. |

### s6 One chart（章节 experiment）
| 句号 | English |
|---|---|
| l28 | Back to the experiment. We repeat it 300 times, making the model more and more complex, and watch both errors. |
| l29 | Practice error keeps falling. The more complex the model, the better it does on the practice problems. |
| l30 | But exam error falls, then rises. Only the middle stretch has actually learned the pattern. |
| l31 | So low practice error with high exam error is the telltale sign of overfitting. |
| l32 | Does that mean simpler is always better? No. Too simple is underfitting, on the left. What you want is the sweet spot in the middle. |

### s7 Learning is compression（章节 lens）
| 句号 | English |
|---|---|
| l33 | Here's another way to see it. Learning is a kind of compression. |
| l34 | To remember these ten points exactly, you have to store ten heights. |
| l35 | Model two describes them, roughly, with just four numbers. And it comes close on points it has never seen. |
| l36 | Model three has ten numbers, exactly enough to store all ten points as they are. It never needed to find the pattern, so it didn't. |
| l37 | Real understanding means explaining more with less. |

### s8 The real-world cost（章节 real）
| 句号 | English |
|---|---|
| l38 | This isn't just theory. It has caused real trouble. |
| l39 | Google once estimated flu levels from people's searches. Researchers pointed out that it searched 50 million terms for the best fit to about 1,100 data points. That's overfitting. It was part flu detector, part winter detector. |
| l40 | Later versions didn't do much better. From 2011 to 2013, it overestimated flu in 100 out of 108 weeks. |
| l41 | Medical imaging has examples too. Chest X-rays turned out to carry a hospital fingerprint: a separate model could tell, almost perfectly, which hospital each one came from. Part of the pneumonia model's success likely came from recognizing hospitals, not disease. At a new hospital, its performance dropped. |
| l42 | And a melanoma detector was thrown off by the ink marks doctors draw on skin. With the marks, it called more than half of the harmless moles cancer. |
| l43 | Those last two are called shortcut learning, a close cousin of overfitting. They look brilliant on the data they were built with, but what they learned was coincidence, not the pattern. |

### s9 How to prevent it（章节 fix）
| 句号 | English |
|---|---|
| l44 | So how do you spot and prevent overfitting? Three common ways. |
| l45 | Earlier, for the demo, we picked the model using the exam itself. In practice, here's what you do. One: set aside another slice of data as a practice exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end. |
| l46 | Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns. |
| l47 | Three: limit the model's complexity, so it simply can't memorize every point. These methods are called regularization. |

### s10 Outro（包装卡 outro）
| 句号 | English |
|---|---|
| l48 | Remember this one sentence. |
| l49 | Overfitting is memorizing the practice problems |
| l50 | without learning the pattern. |
| l51 | Next time: reinforcement learning. |
