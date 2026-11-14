你是裁决人 **framing__judge**（claude · claude-opus-5-5），裁「镜头规格」审稿项 framing 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reconcile\framing.md`。

## 两份报告
- a 位（claude-opus-5-5/framing__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\framing__a.md`
- b 位（gpt-6.1-sol/framing__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\framing__b.md`

## 要裁的维度
- **F5**（抽查）画内人数：a 3 分（st1、st2 首帧都只有 Riley 一人；st4 首帧 3 人，年轻渔夫在左、年长渔夫在右，Riley 在画右；st3 首帧 3 人 1 骡，小门洞空着；st5 0 秒首帧街上只有 Riley。文字、toml、prompt 第 9 行（「另有 1 个」）三处人数一致）；b 3 分（逐张首帧数人：st1＝1、st2＝1、st4＝3、st3＝3，均与开场文字一致；st3 另有 1 头骡子。st5 第 0 秒只有 Riley，驴和赶驴人按 3 秒后入画，不能把全镜的 2 人要求误当作开场应有 2 人。）
- **F6**（抽查）轴线：a 2 分（st3 跟拍往纵深走，st5 反打朝镜头走，是沿纵深轴的正常反打。小瑕疵：st1 到 st2 是同一站位 (38.18,51.9)，城门却从画左上（st1 实测 28%，回望越过右肩）跳到画右（st2 实测 71%，拇指越过左肩去指），两机位分在 Riley 和城门连线的两侧（st1 方位 182°，st2 方位 155°，轴线 166°/346°））；b 3 分（st4 两渔夫的路径始终年轻人在年长者左侧，船在左、Riley 在右；st3 大门居中、小门在右，挑夫在骡子左；st1→st2 是有自拍动作交代的换角度，st3→st5 是由入城背影转为城内正面反拍，没有发现同一双人关系被无解释地左右翻转。）

## 全部评分维度
- **F1** 景别与人物大小：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%
- **F2** 机位与朝向：站位图的机位方向、首帧的视角、文字的「镜头」三者一致
- **F3** 画面位置：人和关键道具在画面里的左右上下位置，三处一致
- **F4** 节拍秒数：动作节拍的秒数排得下（走多远、几秒到），没有挤压
- **F5** 画内人数：写了几个人就几个人（含 extras），首帧一致
- **F6** 轴线：同一场前后镜头的左右关系不跳轴
- **F7** 一镜到底：单镜内不需要切镜；镜头运动写清且做得到

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\framing__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" framing --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\framing__judge.md" --by "<你的模型名>/framing__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）