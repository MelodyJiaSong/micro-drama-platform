# 讲稿（中英对照）

### s0 冷开场（冷开场）
| 句号 | 中文 | English |
|---|---|---|
| l01 | 一个模型，在手里的数据上几乎满分；可一换到新数据，就错得一塌糊涂。 | A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart. |
| l02 | 程序没写错。它犯的毛病，有个名字，叫过拟合。 | The code isn't broken. The problem has a name: overfitting. |

### s1 本期内容（包装卡 agenda）
| 句号 | 中文 | English |
|---|---|---|
| l03 | 这一期，讲四件事。 | Here's what we'll cover. |
| l04 | 它是个什么问题； | What the problem is. |
| l05 | 一个只背练习册的学生； | A student who memorized the workbook. |
| l06 | 换个角度看学习； | A different way to think about learning. |
| l07 | 还有，它在现实里闯过的祸，以及怎么防。 | And the trouble it has caused in the real world, and how to prevent it. |
| l08 | 不懂模型、训练数据也没关系，片中都会一句话讲清。 | No background needed. We'll explain models and training data as we go. |

### s2 模型在学什么（章节 problem）
| 句号 | 中文 | English |
|---|---|---|
| l09 | 先给一句话：过拟合，就是把练习题背下来了，却没学会规律。下面用一个小实验看清楚。 | Here it is in one sentence: overfitting is memorizing the practice problems without learning the pattern. Let's see it in a small experiment. |
| l10 | 这十个点，是收集到的数据，叫训练数据，相当于练习题。 | These ten points are the data we collected. This is called the training data. Think of it as practice problems. |
| l11 | 它们大致沿着某个规律分布，但每个点都带着一点随机的偏差，也就是噪声。 | They roughly follow some pattern, but every point is a little off, at random. That's noise. |
| l12 | 模型的任务，是从这些点里找出规律，好去预测没见过的新数据。 | The model's job is to find the pattern in these points, so it can predict new data it has never seen. |

### s3 三种学法
| 句号 | 中文 | English |
|---|---|---|
| l13 | 先说误差：就是点和曲线差得有多远，越小越好。第一种模型太简单，只会画直线，连练习题都对不上，这叫欠拟合。 | First, error: how far the points are from the curve. Smaller is better. Model one is too simple. It only draws a straight line, and it can't even match the practice problems. That's underfitting. |
| l14 | 第二种，一条平缓的曲线。它没有穿过每一个点，但抓住了大的走势。 | Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend. |
| l15 | 第三种，模型非常复杂，曲线拐来拐去，硬是穿过了每一个点。练习题上，它的误差是零。 | Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero. |
| l16 | 先猜一下：换成新题，哪一种考得最好？ | Quick guess: on new questions, which one does best? |

### s4 考试
| 句号 | 中文 | English |
|---|---|---|
| l17 | 拿出六个模型从没见过的新点，这叫测试数据，相当于考试。 | Here are six new points the models have never seen. This is the test data. Think of it as the exam. |
| l18 | 第二种曲线，离新点都不远，考得不错。 | Model two stays close to the new points. It does well. |
| l19 | 第三种曲线，在点和点之间乱拐，有的新点一下就差出去很远。它的考试误差，是第二种的二十多倍。 | Model three swings wildly between the points, and some new points land far from its curve. Its exam error is more than twenty times higher than model two's. |
| l20 | 它把练习题里的噪声，也一起背了下来。这就是过拟合。 | It memorized the noise in the practice problems, along with everything else. That's overfitting. |
| l21 | 欠拟合的模型，一眼就能看出不行；过拟合更危险：在你手里的数据上，它看起来好极了。 | An underfit model is obviously bad. An overfit model is more dangerous, because on the data you have, it looks great. |

### s5 打个比方（章节 analogy）
| 句号 | 中文 | English |
|---|---|---|
| l22 | 有个学生，把练习册的答案一字不落，全背了下来。练习册上的题，他次次满分。 | Picture a student who memorizes every answer in the workbook. On workbook problems, he scores a hundred every time. |
| l23 | 可一到考试，题目稍微换个样子，他就不会了。 | But on the exam, when a question changes even slightly, he's lost. |
| l24 | 对上刚才的实验：练习册就是训练数据，考试就是新数据，背下来的答案，就是那条硬穿过每个点的曲线。 | Map it back to our experiment: the workbook is the training data, the exam is new data, and the memorized answers are that curve forced through every point. |
| l25 | 再比如，教小朋友认猫。给他看的照片里，猫全都趴在沙发上。 | Or say you're teaching a child to recognize cats. In every photo you show him, the cat is lying on a sofa. |
| l26 | 他学会的，可能是：沙发上的，就是猫。换成沙发上的小狗，他说是猫；草地上的猫，他反倒不认了。 | What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no. |
| l27 | 两个例子是同一件事：记住了只在手头数据里成立的东西。不过类比也有不像的地方：模型不会偷懒，它只是被允许记得太多。 | Both are the same mistake: learning something that's only true of the data at hand. The analogy has a limit, though. A model isn't lazy. It's simply allowed to remember too much. |

### s6 一张图看懂（章节 experiment）
| 句号 | 中文 | English |
|---|---|---|
| l28 | 回到实验。把它重复三百次，让模型从简单变到复杂，看两种误差怎么变。 | Back to the experiment. We repeat it 300 times, making the model more and more complex, and watch both errors. |
| l29 | 练习误差一路往下走：模型越复杂，练习题做得越好。 | Practice error keeps falling. The more complex the model, the better it does on the practice problems. |
| l30 | 考试误差却先降后升。中间那一段，才是真正学到了规律。 | But exam error falls, then rises. Only the middle stretch has actually learned the pattern. |
| l31 | 所以，练习误差很低、考试误差却很高，就是过拟合的信号。 | So low practice error with high exam error is the telltale sign of overfitting. |
| l32 | 那模型越简单越好吗？也不是。太简单，就是左边的欠拟合。要找的，是中间刚刚好的那一段。 | Does that mean simpler is always better? No. Too simple is underfitting, on the left. What you want is the sweet spot in the middle. |

### s7 学习就是压缩（章节 lens）
| 句号 | 中文 | English |
|---|---|---|
| l33 | 换个角度想：学习，其实是一种压缩。 | Here's another way to see it. Learning is a kind of compression. |
| l34 | 这十个点，要原样记住，就得存下十个高度。 | To remember these ten points exactly, you have to store ten heights. |
| l35 | 第二种曲线，只用四个数字，就把它们大致说清了，还能说中没见过的点。 | Model two describes them, roughly, with just four numbers. And it comes close on points it has never seen. |
| l36 | 第三种模型有十个数字，正好够把十个点原样存下来。它不用找规律，所以也就没找。 | Model three has ten numbers, exactly enough to store all ten points as they are. It never needed to find the pattern, so it didn't. |
| l37 | 真正的理解，是用更少的东西，解释更多的事。 | Real understanding means explaining more with less. |

### s8 现实里的代价（章节 real）
| 句号 | 中文 | English |
|---|---|---|
| l38 | 这种毛病，在现实里真的闯过祸。 | This isn't just theory. It has caused real trouble. |
| l39 | 谷歌曾用人们的搜索记录估算流感。研究者指出，它从五千万个搜索词里，挑出最能贴合一千多个历史数据点的那些，这正是过拟合：它既在测流感，也在测冬天。 | Google once estimated flu levels from people's searches. Researchers pointed out that it searched 50 million terms for the best fit to about 1,100 data points. That's overfitting. It was part flu detector, part winter detector. |
| l40 | 后来的版本也没好多少：2011到2013年，108周里，有100周估高了。 | Later versions didn't do much better. From 2011 to 2013, it overestimated flu in 100 out of 108 weeks. |
| l41 | 医学影像里也有。研究者发现，胸片里藏着医院的“指纹”：另训一个模型，几乎能百分之百认出片子来自哪家医院。看肺炎的模型，好成绩很可能有一部分就靠认医院，而不是认病；换到一家新医院，成绩就掉了下来。 | Medical imaging has examples too. Chest X-rays turned out to carry a hospital fingerprint: a separate model could tell, almost perfectly, which hospital each one came from. Part of the pneumonia model's success likely came from recognizing hospitals, not disease. At a new hospital, its performance dropped. |
| l42 | 还有一个识别黑色素瘤的系统：医生在皮肤上画的标记笔迹，让它把一半多的良性痣，都误判成了癌。 | And a melanoma detector was thrown off by the ink marks doctors draw on skin. With the marks, it called more than half of the harmless moles cancer. |
| l43 | 后两个例子，专业上叫捷径学习，是过拟合的近亲：在手里的数据上表现亮眼，学到的却是巧合，不是规律。 | Those last two are called shortcut learning, a close cousin of overfitting. They look brilliant on the data they were built with, but what they learned was coincidence, not the pattern. |

### s9 怎么防（章节 fix）
| 句号 | 中文 | English |
|---|---|---|
| l44 | 那该怎么发现和避免过拟合？常用的办法有三个。 | So how do you spot and prevent overfitting? Three common ways. |
| l45 | 刚才为了演示，我们直接拿考试挑了模型；实际该这样做。第一，再留出一份数据当模拟考，叫验证集：用它来挑模型、及早发现过拟合，真正的考试留到最后。 | Earlier, for the demo, we picked the model using the exam itself. In practice, here's what you do. One: set aside another slice of data as a practice exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end. |
| l46 | 第二，收集更多、更多样的数据，噪声和巧合，就不容易被当成规律。 | Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns. |
| l47 | 第三，限制模型的复杂度，别让它有本事把每个点都背下来。这类方法叫正则化。 | Three: limit the model's complexity, so it simply can't memorize every point. These methods are called regularization. |

### s10 片尾（包装卡 outro）
| 句号 | 中文 | English |
|---|---|---|
| l48 | 记住这一句： | Remember this one sentence. |
| l49 | 过拟合，就是把练习题背下来了， | Overfitting is memorizing the practice problems |
| l50 | 却没学会规律。 | without learning the pattern. |
| l51 | 下一期，我们讲强化学习。 | Next time: reinforcement learning. |
