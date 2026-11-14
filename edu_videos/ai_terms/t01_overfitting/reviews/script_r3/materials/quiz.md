# 测验（不含答案）

**Q1** 一个识别垃圾邮件的模型，在训练用的邮件上准确率 99%，上线后对新邮件只有 70%。最可能是什么问题？  
A spam filter is 99% accurate on its training emails but only 70% on new emails after launch. What is the most likely problem?
- A 欠拟合：模型太简单 / A Underfitting: the model is too simple
- B 过拟合：记住了训练邮件的特点，没学到通用规律 / B Overfitting: it memorized quirks of the training emails
- C 新邮件太少，统计不准 / C Too few new emails to measure
- D 训练准确率越高越好，这不是问题 / D Higher training accuracy is always better, so no problem

**Q2** 为了避免过拟合，是不是应该总用最简单的模型？  
To avoid overfitting, should you always use the simplest possible model?
- A 是，越简单越安全 / A Yes, simpler is always safer
- B 不是，太简单会欠拟合，要找练习和考试都好的中间那一段 / B No. Too simple underfits; look for the middle where both errors are low
- C 是，只要数据够多 / C Yes, as long as there is enough data
- D 不是，应该用最复杂的模型再多训练 / D No, use the most complex model and train longer

**Q3** 用十个点训练两个模型：一个有 4 个可调的数字，一个有 10 个。哪个更可能过拟合？为什么？  
Two models are trained on ten points: one has 4 adjustable numbers, the other has 10. Which is more likely to overfit, and why?

**Q4** 你在调一个模型，想在不碰最终测试集的前提下尽早发现过拟合，应该怎么做？  
You are tuning a model and want to catch overfitting early without touching the final test set. What should you do?
- A 只看训练误差 / A Watch the training error only
- B 每次都用测试集挑模型 / B Use the test set to pick the model each time
- C 另留一份验证集来挑模型、观察误差 / C Hold out a validation set to choose models and watch its error
- D 把测试集也加进训练 / D Add the test set to the training data

**Q5** 一个识别牛的模型，训练照片里的牛几乎都站在草地上。它遇到海滩上的牛可能会出什么错？这和本期讲的什么有关？  
A cow-recognition model was trained on photos where cows almost always stand on grass. What might go wrong with a cow on a beach, and how does it relate to this episode?

**讲回来**：请用两三句话，给一个没学过 AI 的朋友解释什么是过拟合。 / In two or three sentences, explain overfitting to a friend who has never studied AI.
