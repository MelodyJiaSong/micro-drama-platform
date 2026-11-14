# 讲稿（中英对照）

### s0 冷开场（冷开场）
| 句号 | 中文 | English |
|---|---|---|
| l01 | 一个模型，在手里的数据上几乎满分；可一换到新数据，就错得一塌糊涂。 | A model scores almost perfectly on the data you have. Then it meets new data, and it falls apart. |
| l02 | 很多时候，不是程序写错了，而是它犯了一种毛病，叫过拟合。 | Often the code isn't broken at all. The model has a problem called overfitting. |

### s1 本期内容（包装卡 agenda）
| 句号 | 中文 | English |
|---|---|---|
| l03 | 这一期，讲四件事： | In this episode: |
| l04 | 它是个什么问题； | What the problem is. |
| l05 | 为什么只背练习册不行； | Why memorizing answers fails. |
| l06 | 换个角度看学习； | A different way to think about learning. |
| l07 | 它在现实里闯的祸，和怎么防。 | Then, real-world failures, and how to avoid them. |
| l08 | 不懂模型和训练数据也没关系，片中都会用一句话讲清。 | No background needed. We'll explain models and training data as we go. |

### s2 模型在学什么（章节 problem）
| 句号 | 中文 | English |
|---|---|---|
| l09 | 先说清楚：过拟合，就是模型连练习题里偶然的细节也学了进去，做新题反而变差。 | First, the idea. Overfitting is when a model fits its practice data so closely that it learns the flukes, too, and does worse on new data. |
| l10 | 打个比方：把练习题背下来了，却没学会规律。下面用一个小实验看清楚。 | Think of it as memorizing the practice problems without learning the pattern. Let's see it in a small experiment. |
| l11 | 这十个点，是收集到的数据，叫训练数据，相当于练习题。 | These ten points are the data we collected. This is called the training data. Think of it as practice problems. |
| l12 | 它们大致沿着某个规律分布，但每个点都有一点随机的偏差，这叫噪声。 | They follow a pattern, but each point is slightly off. Those random wobbles are called noise. |
| l13 | 模型的任务，是从这些点里找出规律，好去预测没见过的新数据。 | The model's job is to find the pattern in these points, so it can predict new data it has never seen. |

### s3 三种学法
| 句号 | 中文 | English |
|---|---|---|
| l14 | 第一种模型太简单，只会画直线。每个点和线上下差多远，汇总起来，就是误差。 | Model one is too simple. It only draws a straight line. How far each point sits above or below the line, added up, is the error. |
| l15 | 直线连练习题的误差都压不下来，这叫欠拟合。 | The line can't even get the error down on the practice problems. That's underfitting. |
| l16 | 第二种，一条平缓的曲线。它没有穿过每一个点，但抓住了大的走势。 | Model two draws a gentle curve. It doesn't pass through every point, but it captures the overall trend. |
| l17 | 第三种，模型非常复杂，曲线拐来拐去，硬是穿过了每一个点。练习题上，它的误差是零。 | Model three is very complex. Its curve twists and turns to hit every single point. On the practice problems, its error is zero. |
| l18 | 先猜一下：换成新题，哪一种考得最好？ | Quick guess: on new questions, which one does best? |

### s4 考试
| 句号 | 中文 | English |
|---|---|---|
| l19 | 再拿六个新点，模型都没见过。这叫测试数据，相当于考试。 | Here are six new points the models have never seen. This is the test data. Think of it as the exam. |
| l20 | 第二种曲线，离新点都不远，考得最好。 | Model two stays close to the new points. It does best. |
| l21 | 第三种曲线，在点和点之间乱拐，离有些新点很远。它的考试误差，是第二种的二十多倍。 | Model three swings wildly between the points and misses some new ones badly. Its exam error is over twenty times model two's. |
| l22 | 它连噪声也一起背了下来，可噪声是随机的，到了新题不会重演。这就是过拟合。 | It memorized the noise, too. But noise is random, so it won't repeat on new questions. That's overfitting. |
| l23 | 欠拟合，练习和考试都差，很容易发现；过拟合更难察觉：练习成绩可能好极了，比如这里，练习误差是零。 | Underfitting is easy to spot: it's bad on both practice and exam. Overfitting is harder to catch: the practice score can look great. Here, practice error is zero. |

### s5 打个比方（章节 analogy）
| 句号 | 中文 | English |
|---|---|---|
| l24 | 有个学生，把练习册的答案全背了下来，连印错的几处也照背。练习册上，他次次满分。 | Picture a student who memorizes every answer in the workbook, even the typos. On workbook problems, he scores a hundred every time. |
| l25 | 可一到考试，题目稍微换个样子，他就不会了。 | But on the exam, when a question changes even slightly, he's lost. |
| l26 | 对应刚才的实验：练习册是训练数据，印错的答案是噪声，考试是新数据；死记硬背，就是那条硬穿过每个点的曲线。 | In our experiment, the workbook is the training data, the typos are noise, and the exam is new data. Forcing the curve through every point is like memorizing. |
| l27 | 这个比方也有局限：学生知道自己在背，模型不知道。它只是足够复杂，连每个点都能记住。 | The analogy has a limit. The student knows he's memorizing. The model doesn't. It's simply complex enough to remember every point. |
| l28 | 再看一个相近、但不一样的毛病。教小朋友认猫，给他看的照片里，猫全都趴在沙发上。 | Now a related, but different, problem. Say you're teaching a child to recognize cats, and in every photo the cat is lying on a sofa. |
| l29 | 他学会的，可能是：沙发上的，就是猫。换成沙发上的小狗，他说是猫；草地上的猫，他反倒不认了。 | What he may learn is: if it's on the sofa, it's a cat. Show him a puppy on the sofa, and he says cat. Show him a cat on the grass, and he says no. |
| l30 | 这两个孩子，都把眼前的例子当成了规律：学生是记得太多，小朋友是见得太少。后一种叫捷径学习，后面还会碰到。 | Both kids trusted something that's only true of the data at hand. The student remembered too much. The child saw too little. That second kind is called shortcut learning, and we'll meet it again. |

### s6 一张图看懂（章节 experiment）
| 句号 | 中文 | English |
|---|---|---|
| l31 | 回到实验。换三百组随机的点，每组都把模型从简单做到复杂，看两种误差通常怎么变。 | Back to the experiment. We draw 300 random sets of points, fit models from simple to complex on each, and look at the typical errors. |
| l32 | 练习误差一路往下走：模型越复杂，练习题做得越好。 | Practice error keeps falling. The more complex the model, the better it does on the practice problems. |
| l33 | 考试误差却先降后升。复杂度在中间的模型，预测新数据最准。 | But exam error falls, then rises. Moderately complex models do best on new data. |
| l34 | 所以，练习误差很低、考试误差却很高，就是过拟合的信号。 | So low practice error with high exam error is the telltale sign of overfitting. |
| l35 | 那模型越简单越好吗？也不是。太简单，两种误差都高，就是左边的欠拟合。要找的，是两种误差都低的那一段。 | So is simpler always better? No. Too simple, and both errors are high. That's underfitting, on the left. You want the range where both errors are low. |

### s7 学习就是压缩（章节 lens）
| 句号 | 中文 | English |
|---|---|---|
| l36 | 换个角度想：学习，可以看成一种压缩。 | Here's another way to see it. Learning can be seen as a kind of compression. |
| l37 | 这十个点，要原样记住，就得存下十个高度。 | To remember these ten points exactly, you have to store ten heights. |
| l38 | 第二种曲线，只用四个可调的数字，就能大致描述这些点，新点也估得准。 | Model two is set by just four adjustable numbers. It roughly describes the points, and it stays close on new ones. |
| l39 | 第三种有十个数字，正好能穿过全部十个点。十个数字存十个点，等于没有压缩，连噪声也一起存了下来。 | Model three uses ten numbers, enough for its curve to pass through all ten points. Ten numbers for ten points is no compression at all, so it stores the noise, too. |
| l40 | 好的压缩，要留住规律、少记噪声；可压过了头，像那条直线，连规律也丢了。 | Good compression keeps the pattern and leaves out the noise. Squeeze too hard, like the straight line, and you lose the pattern, too. |

### s8 现实里的代价（章节 real）
| 句号 | 中文 | English |
|---|---|---|
| l41 | 这类毛病，在现实里真的闯过祸。 | Problems like this have caused real trouble. |
| l42 | 谷歌曾用人们的搜索记录，估算流感样病例的就诊比例。 | Google once used people's searches to estimate the share of doctor visits for flu-like illness. |
| l43 | 研究者说，它最初从五千万个搜索词里筛选，看哪些最贴合那一千多个历史数据点。 | Researchers pointed out that its first version tested 50 million search terms for the best fit to about 1,100 data points. |
| l44 | 可挑的远比数据点多，比刚才十个数字配十个点还夸张。研究者说，这是过拟合：它既在测流感，也在测冬天。 | Far more choices than data points, even more lopsided than ten numbers for ten points. The researchers called it overfitting: it was part flu detector, part winter detector. |
| l45 | 后来的版本也有偏差：2011到2013年，108周里，有100周估得偏高。 | Later versions still had problems. From 2011 to 2013, it overestimated flu in 100 out of 108 weeks. |
| l46 | 医学影像里也有。一个看胸片诊断肺炎的模型，换到一家新医院，成绩就掉了下来。 | Medical imaging has examples too. A model that detected pneumonia in chest X-rays did worse at a new hospital. |
| l47 | 研究者发现，胸片里藏着医院的“指纹”：单独训练一个模型，在两家医院的片子上，认医院的准确率超过百分之九十九点九。 | Researchers found the X-rays carried a hospital fingerprint: a separate model could identify which hospital scans from two of the hospitals came from, with over 99.9 percent accuracy. |
| l48 | 而各家医院的肺炎病人比例差得很远。所以肺炎模型的好成绩，很可能有一部分靠的是认医院，而不是认病。 | And pneumonia rates differed widely between hospitals. So part of the pneumonia model's success likely came from recognizing hospitals, not disease. |
| l49 | 还有一个识别黑色素瘤的系统：医生常在可疑的痣上画标记，它很可能把标记当成了线索。研究中，画了标记的良性痣，一半多被它判成了癌。 | And a melanoma detector, an AI that spots skin cancer: doctors often draw ink marks around suspicious moles, and it likely learned the marks as a clue. In one study, it flagged over half of the marked harmless moles as cancer. |
| l50 | 后两个例子，和认猫的小朋友一样，叫捷径学习，是过拟合的近亲。它们在同类的新数据上也能考好，换个环境才露馅。 | Those last two models took shortcuts, like the child with the cats. That's shortcut learning, a close cousin of overfitting. They can score well on similar new data, and only fail when the setting changes. |

### s9 怎么防（章节 fix）
| 句号 | 中文 | English |
|---|---|---|
| l51 | 那该怎么发现和避免过拟合？常用的办法有三个。 | So how do you spot and prevent overfitting? Three common ways. |
| l52 | 第一，再留出一份数据当模拟考，叫验证集：用它来挑模型、及早发现过拟合，真正的考试留到最后。 | One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early. Save the real exam for the very end. |
| l53 | 坦白一句：刚才为了演示，我们直接按考试成绩挑了模型；实际做项目，可不能这样。 | A confession: for the demo, we picked the model by its exam score. In a real project, you shouldn't. |
| l54 | 第二，收集更多、更多样的数据，噪声和巧合，就不容易被当成规律。 | Two: collect more data, and more varied data, so noise and coincidences are less likely to pass for patterns. |
| l55 | 第三，给模型立规矩：对过于复杂的曲线加惩罚，让它别去追着噪声跑。这类方法叫正则化。 | Three: put limits on the model. Penalize overly complex curves, so it doesn't chase the noise. That's called regularization. |

### s10 片尾（包装卡 outro）
| 句号 | 中文 | English |
|---|---|---|
| l56 | 记住这一句： | Remember this one sentence. |
| l57 | 过拟合，就像把练习题背下来了， | Overfitting is like memorizing the practice problems |
| l58 | 却没学会规律。 | without learning the pattern. |
| l59 | 下回你觉得全懂了，换一道没见过的题试试。下一期，我们讲强化学习。 | Next time you're sure you've got it, try a question you've never seen. Next episode: reinforcement learning. |
