# 审稿项 audience（观众 · 场剪辑）

范围：s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · kimi · kimi
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-175225_cut_r1\items\audience__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-175225_cut_r1\reports\audience__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-175225_cut_r1" audience --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-175225_cut_r1\reports\audience__a.md" --by "kimi/audience__a"`

## 评分维度
- **A1** 看懂：每段看懂了什么、哪里糊涂
- **A2** 笑点：笑点落没落地
- **A3** 节奏：哪里拖、哪里急
- **A4** 出戏：出戏的画面或台词
- **A5** 记住与期待：看完记住了什么、想不想看下一集、为什么
- **A6** 情绪：哪里让人会心一笑、哪里感到温暖或惊奇
- **A7** 接口与连看：连着看成片：镜与镜、场与场的接口顺不顺（前一场最后 3 秒接后一场头 3 秒）；有没有人像摆件、梗拖沓；搁置镜或有瑕疵的条不放在场头、场尾这类显眼位置
- **A8** 看点落地：关掉声音看每一镜，先写一句「这镜在讲什么」，审查结束后再对照分镜 point：哪几镜对不上
- **A9** 故事点抓人：逐个故事点（集目录 story_beats.md，每点一行、按时间顺序）判抓不抓人：强 / 中 / 弱和一句理由；连续两个以上弱点的段落、整集漏掉的情绪钩子（观众比人物知道得多的事）单独列出，并给备选