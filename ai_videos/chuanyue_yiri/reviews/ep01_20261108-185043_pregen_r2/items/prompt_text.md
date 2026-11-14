# 审稿项 prompt_text（Prompt 文本 · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s1。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-sonnet-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\items\prompt_text__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\prompt_text__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" prompt_text --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\prompt_text__a.md" --by "claude-sonnet-5-5/prompt_text__a"`

## b 位 · codex · gpt-6.1-sol
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\items\prompt_text__b.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\prompt_text__b.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" prompt_text --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\prompt_text__b.md" --by "gpt-6.1-sol/prompt_text__b"` `--attest-log <codex exec 运行日志>`（Codex 沙箱跑不了 python，由调用方凭日志代登记）

## 评分维度
- **T1** 自相矛盾：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致
- **T2** 否定句：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句
- **T3** 过期描述：人物、场景、道具描述是现行版本（发色、造型、卡片）
- **T4** 图文一致：文字和挂的首帧、站位图、场景图一致
- **T5** 混入别镜：「本场」「场景」行没有把别的镜头的内容带进来
- **T6** 参考清单：参考图齐全、顺序与用法说明对得上，没有多余或缺失
- **T7** 长度与重点：prompt 不超长，关键动作写在前面、写得清楚
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`