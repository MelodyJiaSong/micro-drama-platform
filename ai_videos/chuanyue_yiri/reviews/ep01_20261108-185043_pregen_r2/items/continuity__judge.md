你是裁决人 **continuity__judge**（claude · claude-opus-5-5），裁「连续性」审稿项 continuity 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\continuity.md`。

## 两份报告
- a 位（claude-opus-5-5/continuity__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\continuity__a.md`
- b 位（gpt-6.1-sol/continuity__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\continuity__b.md`

## 要裁的维度
- **K3**（分歧）服装与发型：a 2 分（五镜 prompt 第 8 行人物块逐字相同，都写「自然披散在肩后和肩头」（I29 已去掉「松松拢起」）；首帧衬衫、裤子和靴子都一致（st1_riley.png 挽袖短袖、橄榄色腰带；st2、st4 是同一件亚麻衬衫）；小瑕疵是 st5 首帧腰带偏棕、带大号金扣（st5_riley.png），与 st1、st4 的橄榄色帆布腰带配银扣不一样，因为人很小，记作「记录」）；b 1 分（五镜首帧与各 prompt:8 的米白短袖、塞入裤腰、卡其裤、橄榄腰带、披散干发一致，I29 已改；但 story.md:33 仍是“秃头老汉”，st5 spec:10／快照 prompt:11 却是“满头花白短发”，I32、I33 未改好，见 C02。）
- **K4**（分歧）光与时间：a 2 分（st1、st2、st4 首帧里太阳都在画面左上屋脊处（st1 x≈260、st2 x≈165、st4 x≈245），城门在太阳右边，同一时段；st3 城墙朝海的一面在阴影里、城里那头的出口亮，接 st5 光从镜头身后来、城墙朝城里这一面上半截被照成暖金。小瑕疵 1：st5 光线一行写她出门洞时是「暗轮廓」，首帧里她却被正面照亮、脸和衣服都清楚（st5_riley.png），文字和首帧对不上。小瑕疵 2：I30 的方位问题还在（见 R 和问题表））；b 1 分（st1／st2／st4 首帧太阳均在画左上，城墙海面侧冷、发肩暖边的画面关系相合；st3 入洞变暗、st5 入街变亮也有交代。但五份快照 prompt:6 仍写“上方为北”，st3 与 st5 两张俯视图却把相反的进出城方向都画成向北，I30 未解决，无法形成同一清晨的统一方位与光向，见 C01。）
- **K2**（抽查）钱账：a 3 分（只有 st2 出现钱。spec 第 24 行与 story.md 第 24 行都写 9 枚＝7 as＋1 quadrans＋1 大黄铜币；进场 9、出场 9，最后揣回左侧裤袋；st1 写在左侧裤袋，st4、st3、st5 都写「钱一直揣在裤袋里」。本场没有付钱，账平）；b 3 分（s1 五镜均无交易，7 as＋1 quadrans＋1 sestertius＝9 枚，入场与离场均为九枚；st2 spec:10、12 的 13–19 秒只展示不支付。另以故事稿核账，9→7→7→6→4→0 枚，种类逐次扣除正确，计算表见下；此项不声称 s1 外视频已核验。）
- **K7**（抽查）跨场引用：a 3 分（st4「Future garum」接的是 st2 的「Mission two: try garum」，st2 在前、st4 在后，顺序对；st3「twelve years ago」与 st2 的「75 AD」、bg1 卡第 15 行「地震后 12 年」一致；st2「this whole town」指的是身后画右的城（首帧右半是城墙和屋顶）；st5 没有台词）；b 3 分（st2 spec:15 先提出找床与尝 garum，st4 spec:12、15 在鱼筐落地后 12.5–15.5 秒说“See those tiny fish? Future garum.”，指代有画面前件；st3 spec:12 先看补缝再说仍在修。补读故事稿:23、57、63、125、133、143、157，九枚预算、早上剩面包和两个目标均有前件及后续；s1 没有引用未曾发生的付钱或指路。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\continuity__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\continuity__judge.md" --by "<你的模型名>/continuity__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）