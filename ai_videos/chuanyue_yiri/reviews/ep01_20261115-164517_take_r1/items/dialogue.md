# 审稿项 dialogue（台词（时长与逻辑） · 出片）

范围：s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · kimi · kimi
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-164517_take_r1\items\dialogue__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-164517_take_r1\reports\dialogue__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-164517_take_r1" dialogue --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-164517_take_r1\reports\dialogue__a.md" --by "kimi/dialogue__a"`

## 评分维度
- **D1** 说得完：时间够念：按正常语速（约 2.5 词/秒；语速要正常，不能靠说快塞进镜头）算出每句需要的时间与留白（开口前 ≥1 秒、说完后 ≥1.5 秒），给数字；不够时写「镜头要延长到 X 秒 / 节拍怎么重排 / 要加的镜头或场」，不建议删词或改短句子
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清
- **D7** 跨镜接续：同一个人跨镜头接着说话时，把上一镜最后一句和下一镜第一句连起来出声读：像不像同一个人在同一刻接着说——不重新打招呼、不重复刚说过的地点和名字、情绪和音量的转变有一句话或一个动作交代；有意的重开要在台词里说出来
- **D8** 跨语言说清：Riley 对听不懂英语的人说话时：她的意图有完整说法加手势，对方的回答配了观众看得懂的动作；只有一个词、没有手势的问句 ✗