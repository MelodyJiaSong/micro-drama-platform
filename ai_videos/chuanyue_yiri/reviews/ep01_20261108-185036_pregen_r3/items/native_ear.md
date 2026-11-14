# 审稿项 native_ear（母语听感 · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s2、s3、s4、s8、s5、s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-sonnet-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\items\native_ear__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" native_ear --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__a.md" --by "claude-sonnet-5-5/native_ear__a"`

## b 位 · codex · gpt-6.1-sol
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\items\native_ear__b.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__b.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" native_ear --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__b.md" --by "gpt-6.1-sol/native_ear__b"` `--attest-log <codex exec 运行日志>`（Codex 沙箱跑不了 python，由调用方凭日志代登记）

## 评分维度
- **N1** 自然度：逐句：母语观众听着自然 / 有点怪 / 很怪
- **N2** 别扭原因：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词
- **N3** 笑点与回收：笑点母语观众接得住；开场目标与结尾、dextram 回收得上
- **N4** 人设口吻：像一个二十多岁、亲切的旅行博主在说话，前后口吻一致
- **N5** 改写：每句「有点怪 / 很怪」都给不更长的改写
- **N6** 最别扭的 5 句：列出并排序
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`