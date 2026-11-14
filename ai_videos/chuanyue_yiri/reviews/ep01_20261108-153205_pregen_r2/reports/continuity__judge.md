# 连续性裁决 · continuity__judge（claude-opus-5-5）· ep01 出片前 第 2 轮

本项要裁的是两个抽查维度：K3、K7（两位审稿人都打了 ≥2 分）。我读了 a、b 两份报告和对比表，回到材料逐条核：a 位的拼图 `work/continuity__a/s3/s4/s5/s8_first_frame.jpg`；s8_st4/st5/st9/st6 的原尺寸首帧 `episodes/ep01/scenes/s8/shots/st*/planning/st*_first_frame.png` 及对应首帧 prompt；`materials/lines.md` 全文；s3_st4、s3_st8、s5_st13、s8_st5 的 spec；`story.md` 第 21 行。自制裁切图在 `work/continuity__judge/`（`s8_bag_side_st5_st9_st6.jpg`、`s8_hair_st4_st5_st9_st6.jpg`）。

判左右的办法：人物大体面朝镜头时，她的右侧在画左；背对镜头时，她的左侧在画左；侧身朝画左时，她的左侧对着镜头。

## 裁决

- K3 1 理由：两位都漏了一处布包挂反。s8_st5、st9、st6 三张首帧里，Riley 坐在画左、大体面朝镜头，布包都在她身体的画左一侧，也就是她的**右胯**旁（见 s8_bag_side_st5_st9_st6.jpg：st5 布包贴着她放在右膝上的右手外侧；st9 她右手握刮板，涂了油的左小臂朝画右，布包在另一侧，也就是画左）。spec 写的是「布包挂在 Riley 左胯」，妇女又坐在她左手边（画右），所以布包本该在她和妇女之间。前一镜 s8_st8、后一镜 s8_st7 的首帧都在左胯（st8 面朝镜头，包在她身体画右；st7 走向镜头，包在她画右），所以 st6→st7 一剪，包会从右胯跳回左胯。成因：st5、st9 的首帧 prompt 根本没写布包；st6 只写了「搭在她身边的石凳上」，没写哪一侧。a 说包「像单独立在石凳上」，只说中一半，没看出挂反；b 没提。其余部分两人说得对：s3_st4/st8、s4_st1/st4、s5_st2/st12/st3/st14/st13 首帧都在左胯，s5_st7 腰上已空，衬衫、腰带、裤子全集一致。头发干湿按「存疑」保留（b 的 C07）：st6 头顶的头发也贴头、发量变少，比 st4 和 s8_st7 更像湿发。
- K7 3 理由：我按 lines.md 全文和 spec 逐条复核，两人的证据都站得住。s3_st4 第 15 行台词含「Okay. Straight… then 'dextram.' No clue. Sounds like left?」（8.2–12.8 秒）。s3_st8 她先转身朝街，再往自己的左边（街东头，画右）走。s4_st3 说「Left. Definitely left.」。s5_st8 店主喊「Dextram」，驴车右拐。s5_st9 说「went the wrong way all morning」。story.md 第 21 行「Mission one: find a bed… Mission two: try garum… my budget… is this」，分别对上 s5_st7「Mission two: done. Now… a bed」、s6_st3「what's left of the budget」和 s7_st1「Bed? Found. Garum? Tasted. Budget? …Gone」。s5_st13 spec 写「露出缺了一瓣的…面包」再掰一瓣，对上 s3_st2/st3 掰下并咬过的那一瓣；s4_st5「Nope」回收 s4_st2「Smell anything?」；s5_st1「Clean-ish」回收 s4_st4「still smell like pee」和 s8 浴场。没找到两人共同漏掉的跨场引用问题。

## 问题表（两位都漏的）

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s8_st5、s8_st9、s8_st6（接 st8 / st7） | 0 s（首帧），st6 末 → st7 0 s | K3 布包·左右 | 重出 | ③ prompt 或首帧（兼 ② 分镜文字） | 三张首帧里布包都在 Riley 画左一侧，即她的右胯旁（s8_bag_side_st5_st9_st6.jpg）；spec 写左胯，妇女坐在她左手边（画右），st8、st7 首帧也都在左胯。st5、st9 首帧 prompt 没写布包，st6 只写「搭在她身边的石凳上」。照现在的图出片，st6→st7 布包换边 | 便宜：重出三张首帧，prompt 写「布包的两个长布角系在她腰带左侧，布包挨着她左胯落在石凳上，在她和妇女之间、小油瓶旁边（画面里在她身体的右侧）」；负面词加「布包在 Riley 画左一侧、布包和腰带分开」。spec 里小油瓶和布包都放在两人之间，写清两者的前后位置，免得挤成一团 |
| s8_st6 | 0 s（首帧） | K3 头发干湿 | 存疑 | ③ prompt 或首帧 | 在 b 的 C07 上补一镜：st6 头顶的头发贴头，发量明显比 st4 和 s8_st7 少，像湿发；静帧没法确定 | 便宜：与 C07 一起，把 st4/st5/st9/st6/st7 的原尺寸首帧并排复核；确认是湿发观感就重画头发 |

## 整体观察

- 第 2 轮布包的大方向（何时系上、何时解下）已经理顺。漏的是「坐下时布包在哪一侧」：首帧 prompt 不写这件道具，模型就会随手放。凡是 spec 的道具行写了「挂在左胯」的镜头，首帧 prompt 都应把它写进去。
- 跨场引用是本项做得最扎实的一维，台词回收与故事稿目标一一对应。
