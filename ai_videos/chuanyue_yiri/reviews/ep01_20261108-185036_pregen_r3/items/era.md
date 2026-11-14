# 审稿项 era（时代与世界观 · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s2、s3、s4、s8、s5、s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-opus-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\items\era__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" era --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__a.md" --by "claude-opus-5-5/era__a"`

## b 位 · codex · gpt-6.1-sol
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\items\era__b.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__b.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" era --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__b.md" --by "gpt-6.1-sol/era__b"` `--attest-log <codex exec 运行日志>`（Codex 沙箱跑不了 python，由调用方凭日志代登记）

## 评分维度
- **E1** 器物：器物是公元 75 年庞贝有的（陶灯、双耳罐、铜币），没有现代或中世纪器物
- **E2** 建筑与材质：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍
- **E3** 服饰与发型：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰
- **E4** 系列禁区：画面不出现烟柱、白烟、冒白气的山；prompt 不写火山词；维苏威不提
- **E5** 文字：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）
- **E6** 史实一致：台词和画面里的史实与考据一致（地震年份、浴场时间、物价、尿税）
- **E7** 规则源：场景卡、道具卡、考据负面词里没有和以上冲突的写法
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`