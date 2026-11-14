你是裁决人 **continuity__judge**（claude · claude-opus-5-5），裁「连续性」审稿项 continuity 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reconcile\continuity.md`。

## 两份报告
- a 位（claude-opus-5-5/continuity__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\continuity__a.md`
- b 位（gpt-6.1-sol/continuity__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\continuity__b.md`

## 要裁的维度
- **K1**（抽查）道具状态表：a 3 分（道具台账（见下）逐镜接得上：钱 st1 左裤袋→st2 左拳摊开→收回左裤袋→st4/st3/st5「钱在她裤袋里」不拿出；两条小木船＋一卷麻绳 st1 overhead (40.6,50.1) 与 st4 overhead「st1 里那两条」(40.6,50.1) 同一坐标，st1/st4 首帧都在画右、船身原木深色；st4 渔船、鱼筐、st3 灰浆筐、st5 陶罐驴都只在本镜出现、有进有出。）；b 3 分（s1_st1 两手空、钱在左裤袋；st2 的 13–18 秒仅摊开原有九枚，18–19 秒收回；st4 的鱼筐由船舱经双人搬运到沙上，船头绳始终系船；st3 灰浆筐由地上到工人右肩，st5 双耳罐始终由灰驴驮着。逐镜进出状态见台账，未发现文字规定的道具增殖或丢失。）
- **K7**（抽查）跨场引用：a 3 分（st4「That's garum. …Eventually.」回指 st2 第 8.5–13 秒「Mission two: try garum」，播放顺序 st2 在 st4 之前；st2「It's May, 75 AD」与场头「公元 75 年 5 月 20 日」一致；st3「still fixing the damage」对上 st3 门洞补缝与 st1/st2/st4 首帧神庙脚手架；「my budget… is this」与摊开的 9 枚钱同镜对应。）；b 3 分（st2 的“Mission two: try garum”先提出鱼露目标，st4 的“See those tiny fish? …Eventually”有同镜鱼筐支撑；st3 的“still fixing”有先前 st1 的神庙脚手架及本镜灰浆、补缝支撑。s1 是首场，无需依赖尚未发生的买面包、问路或付钱；后续故事中的目标回收也与这里的两个目标一致。）

## 全部评分维度
- **K1** 道具状态表：逐镜列出每件道具进、出场状态，前后接得上
- **K2** 钱账：每次付钱前后的枚数和种类，全集账平
- **K3** 服装与发型：衣服、腰带、布包、头发干湿与发型，镜与镜一致
- **K4** 光与时间：光向、时段、天色随时间推进合理，同场一致
- **K5** 站位接续：上一镜结束的位置、朝向接下一镜开始
- **K6** 环境接续：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现
- **K7** 跨场引用：台词或画面提到前面的事（面包、方向、钱），前面确实发生过

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\continuity__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\continuity__judge.md" --by "<你的模型名>/continuity__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）