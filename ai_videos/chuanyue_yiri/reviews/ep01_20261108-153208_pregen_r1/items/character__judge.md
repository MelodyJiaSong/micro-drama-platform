你是裁决人 **character__judge**（claude · claude-opus-5-5），裁「人物逻辑」审稿项 character 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reconcile\character.md`。

## 两份报告
- a 位（claude-sonnet-5-5/character__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\character__a.md`
- b 位（gpt-6.1-sol/character__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\character__b.md`

## 要裁的维度
- **C6**（分歧）路人：a 1 分（本场三个路人的反应是同一模板——st3 工人「愣住→她笑→不好意思咧嘴点头」、st4 年轻渔夫「看她脸、眉毛一挑→她笑→不好意思低头」、st5 赶驴人「打量、眉毛挑得老高→她尴尬笑→憋笑转头」；st4 与 st5 与 s2 喷泉女人（story 第 45 行「眉毛挑得老高」）用了同一个「眉毛挑得老高」。st5 的赶驴人看裤子+眉毛挑高，把 s2 喷泉段「a woman in pants is a lot」的主笑点提前用掉（见问题 1、2）。）；b 2 分（s1_st4 年长渔夫只拢鱼、年轻渔夫好奇后收回目光，st3 挑夫持续赶路，st5 老汉看裤子憋笑，已有差异且不抢台词；但 st4 10.2–11 秒与 st3 4.8–5.6 秒都用「不好意思」收束男人收到她笑容后的反应，局部重复，见问题表。）
- **C5**（抽查）主持人性格：a 3 分（st3 4–4.8 秒她咧嘴笑、左手两指在眉边一挥打招呼；st4 9.5–10.2 秒冲年轻渔夫笑、点头，再转镜头小声说话；st5 7.5–8.5 秒低头看裤子、尴尬笑、微耸肩（自嘲）；st4 7.5 秒看鱼眼睛一亮（好奇）。三镜都是「先回应当地人，再对观众说话」，主持人说话的时机在对方反应结束之后，符合人设。）；b 3 分（s1_st1 0–5.5 秒先看城、转身、半笑半喘再开口；st4 9.5–10.2 秒先回应渔夫、12 秒后才向观众说鱼露笑话；st3 4–4.8 秒友好招呼工人；st5 7.5–8.5 秒看自己裤子后尴尬笑、耸肩，符合好奇、亲切与自嘲的人设。）
- **C7**（抽查）动机连贯：a 2 分（st4 结尾她回头看鱼筐「不再转回来」→st3 她跟在挑夫后面走坡道，情绪连得上；st3 12.5–14 秒眨眼走向亮处→st5 0 秒她从门洞阴影里迈出，位置、方向接得上；st5 她这一镜已经明白「裤子引人注目」，s2 再说「apparently」仍可当作总结，但「发现」感被削弱（问题 1）。小瑕疵：st3 末尾挑夫+骡子 10 秒已走远，st5 0 秒「街上只有她一个人」，可接受。）；b 3 分（按 st1→st2→st4→st3→st5，惊讶看城→兴奋定目标→看渔获联想到鱼露→跟人进城并观察补缝→街上看驴和铺子，行动与情绪连续；st3 12.5–14 秒继续朝城里走，接 st5 从门洞出来，没有突然改目标或情绪跳变。）

## 全部评分维度
- **C1** 知道什么：每个人此刻知道什么、不知道什么，行为不越过他的认知
- **C2** 想要什么：每个人此刻的目的清楚，动作服务于目的
- **C3** 视线：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）
- **C4** 反应拍：配角的反应单独占拍，不被吞掉；反应和身份、性格相符
- **C5** 主持人性格：Riley 的反应符合人设（好奇、敢试、自嘲），对当地人有回应
- **C6** 路人：路人有合理的反应且不雷同，不抢主笑点
- **C7** 动机连贯：跨镜头的情绪与动机连得上，没有突然的转变

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\character__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" character --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\character__judge.md" --by "<你的模型名>/character__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）