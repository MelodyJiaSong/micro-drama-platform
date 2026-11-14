你是裁决人 **framing__judge**（claude · claude-opus-5-5），裁「镜头规格」审稿项 framing 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\framing.md`。

## 两份报告
- a 位（claude-opus-5-5/framing__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\framing__a.md`
- b 位（gpt-6.1-sol/framing__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\framing__b.md`

## 要裁的维度
- **F3**（分歧）画面位置：a 1 分（st5 首帧画左人行道实测只有约 0.9 m 宽（toml/平面图 2 m），Riley 第 5 秒停点 (8.4,8.6) 在首帧几何里正好落在铺面墙线上，3–5 秒的路线还要穿过第二块斜靠门板（见问题表 1）；其余对得上：st4 船头算 29%／实测 27%、年轻渔夫算 41.5%／实测约 40%、年长渔夫算 51.7%／实测约 54%；st3 工人算 62%／实测 64%、骡子算 51%／实测 54%、小门洞算 82%／实测 83%；st5 城门算 58.6%／实测 57.7%、Riley 0 秒算 54.6%／实测 56.5%）；b 2 分（st2 脸轴约 50%、头顶约 y=29 px、城门约 x=330 px＝19.7%，旧偏左及裁头已修；st4 船头约 28% 对照投影 29.2%，年轻／年长渔夫约 40%／52% 对照 41.5%／51.7%。背景、Riley 垂直位置和 st3 主体横向位置仍有小偏差或存疑，见 B01–B03。）
- **F1**（抽查）景别与人物大小：a 2 分（st1 算 47.3%／实测约 45%（头顶 y≈440、脚 y≈865）；st2 头顶到下巴算约 427 px／实测约 460 px（差 8%）；st3 0 秒算 516 px/m／实测约 582 px/m（差 13%，膝上背影一致）；st4 渔夫算 52.7%／实测约 55%；st5 0 秒算 27.3%／实测约 22%（差 19%）；均在 25% 内。小瑕疵：st4 Riley 比例只差 7%，但眼睛在 y≈210，按机高 1.5 m 应在 y≈350，等于首帧机位约 1.3 m（I46 仍开着，记录级））；b 3 分（五镜首帧逐张量取，st1 全身 436–870 px＝46.1% 画高，对照 28 mm、轴向深度 5.204 m 预期 47.3%，偏差约 −2.5%；st5 全身 392–601 px＝22.2%，对照 35 mm、11.315 m 预期 27.2%，偏差约 −18.3%。st2、st3、st4 为裁身构图，按同一身体段比较，估计偏差均不足约 25%，详见测量表。）
- **F5**（抽查）画内人数：a 3 分（st1 首帧只有 1 人；st2 只有 1 人；st4 一共 3 人（Riley＋两渔夫）；st3 一共 3 人＋1 骡（Riley、挑夫、弯腰工人，拱外拱内都没有多余的人）；st5 第 0 秒街上只有 Riley，驴和赶驴人 4.5 秒从画右入画，与文字及 toml 一致）；b 3 分（首帧逐人数：st1＝1、st2＝1、st4＝3、st3＝3 人＋1 骡、st5＝1 人；st5 的另 1 人＋1 驴明确在约 4.5 秒后进画，第 0 秒在镜头身后，与首帧只有 Riley 相符。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\framing__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" framing --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\framing__judge.md" --by "<你的模型名>/framing__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）