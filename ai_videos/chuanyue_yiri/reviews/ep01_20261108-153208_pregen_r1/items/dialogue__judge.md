你是裁决人 **dialogue__judge**（claude · claude-opus-5-5），裁「台词（时长与逻辑）」审稿项 dialogue 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reconcile\dialogue.md`。

## 两份报告
- a 位（claude-sonnet-5-5/dialogue__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\dialogue__a.md`
- b 位（gpt-6.1-sol/dialogue__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\dialogue__b.md`

## 要裁的维度
- **D6**（分歧）听得清：a 2 分（st1 她在画内约4.5米外「压低声音」，画左海浪拍岸，这是开场第一句；st3 全程骡蹄声在拱顶下「越来越响」又要压低声音说悄悄话（7.5–12.5s）；st4 12–16.5s 浪拍船尾、鱼在筐里蹦跳还要「小声」。三镜都是低声对环境声，prompt 的声音行没写台词要听得清、环境声压低，存在盖过台词的风险（问题4）。）；b 1 分（st1 5.5–10 秒在约 4.5 米外压低声音，st4 12–16.5 秒小声讲话时海浪仍在，st3 7.5–12.5 秒悄悄话与拱廊内骡蹄回声重叠；三份 prompt 的声音行只规定保留对白、环境声、动作声及禁配乐，没有规定对白优先、压低环境声或避免回声遮字。已确认的是声音设计指令缺口，实际听感是否受损尚未验证，见问题表。）
- **D2**（抽查）节拍对位：a 3 分（st1 spec 节拍 2.5–5.5s 转身、迈步、停顿，5.5–10s 才开口，说完10–12s 回头看城门，动作与句子对得上；st2 garum 眼睛一亮在8.5–13s 句内、this whole town 竖拇指、And my budget… 举拳、is this 摊手、16–18s 拨钱在台词之后；st4 11–12s 凑近镜头后12–16.5s 才开口、说完16.5s 回头看鱼。）；b 3 分（st2 prompt 第 15 行把 this whole town 对齐左拇指越肩指城，把 is this 对齐摊掌，16–18 秒才拨开钱币；st4 4–7.5 秒先放下鱼筐，12–16.5 秒才说 See those tiny fish，Eventually 说完后于 16.5 秒回头；st3 5.6–6.5 秒先看修补裂缝，7.5 秒才解释地震。各动作不抢占所指定的说话窗口。）
- **D4**（抽查）台词逻辑：a 3 分（st2「Mission one: find a bed」「Mission two: try garum」与 story.md 场一和场六「Mission two: done. Now… a bed.」、场七「still no bed」一致；st2 的 9 枚钱（7 红铜+1 小铜币+1 大黄铜币）与 story 场三/五/六/七逐步扣钱（5→4→3）相符；st3 twelve years ago 与 bg1.md 第15行「地震后12年」、Seneca 63 年说相符；st4「That's garum. …Eventually.」回收 st2 目标二。）；b 3 分（story.md 第 21 行目标一找床、目标二尝鱼露，第 133 行回收为 Mission two: done，第 157 行同时回收 Bed/Garum/Budget；第 23 行起始钱币为 7+1+1=9，后续先付 2 枚小钱、再付小铜币、再付 2 枚小钱、最后付余下 3 枚小钱及大黄铜币，数量闭合。st4 的 Eventually 使“鱼将变成鱼露”的玩笑成立。地震句沿本集考据采用 63 年分支，75−63=12，无内部年份矛盾。）

## 全部评分维度
- **D1** 说得完：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。

## 规则
- 分歧维度：回到材料本身核两人的证据，谁的证据站得住；抽查维度：专门找两个模型可能**共同**漏掉的问题，不因两人都给高分就放过。
- 每个要裁的维度在报告「## 裁决」写一行：`- <编号> <最终分 0–3> 理由：<引用证据：镜头·秒数·图上位置·文件行>`（理由至少 8 个字）。
- 发现两人都漏的问题，可以加问题表（同审稿报告的表头，含「严重度」列）。只读，不改被审材料。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\dialogue__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" dialogue --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\dialogue__judge.md" --by "<你的模型名>/dialogue__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）