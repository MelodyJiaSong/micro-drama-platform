# 问题清单：ep01 · 全集 · 出片前 第 1 轮 · 11-14 11:16

由双审评分（最终分 ≤1 的维度）与问题表推出。严重＝某维 0 分、任一「重出」、或关键维度 ≤1；主要＝其余 1 分维度与「可剪」；待核实＝「存疑」；记录＝「记录」。每条用 `review_run.py fix <审查单> <I编号> --solution "…" --status planned|implemented|wontfix` 记方案；严重与主要都 implemented（或 wontfix 写理由）后才能开下一轮。

| 级别 | 条数 | 未处理 |
|---|---|---|
| 严重（critical） | 42 | 0 |
| 主要（major） | 24 | 0 |
| 待核实（verify） | 9 | 9 |
| 记录（minor） | 68 | 68 |

| 问题 | 级别 | 类别·维度 | 镜头 | 问题 | 来源 | 建议改动 | 成本 | 状态 | 方案 |
|---|---|---|---|---|---|---|---|---|---|
| I1 | 严重 | 世界物理·P2 道具来源与去向 | s1_st2、s1_st1 → s1_st2、s1_st4 | P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；规格要求「靠指根一排 = 大币 + 小铜币，下面 4 + 3 枚 as」；同镜挂的 p6 参考图是 3/3/3 排、大币在靠手腕那排，两边打架。as 直 | claude-opus-5-5/physics_A__a | 便宜：规格改成和 p6 一致的 3/3/3 排法；把「攥拳 → 摊开即成排」改成拳头举到镜头前时已经是虚握的平掌，或者先摊开再停半拍（镜头切到已摊平的状态）。；便宜：写明是插在沙里的轻便自拍杆 / 三脚架，st1 结尾她连杆一起拔起来；st2 开头写「刚从左裤袋把钱攥在拳里」。；便宜：改 overhead.toml 的注释和 note，重生成 overhead 图。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I2 | 严重 | 世界物理·P4 重力与支撑 | s2_st5、s2_st8、s2_st4（规则源 bg2 场景卡）、s2_st1 ↔ s2_st3、s1_st2 | P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s2_st1、st3、st2 写满街 3–4cm 浑水；st5、st8、st4 的规格和 prompt 只写「被流水打湿发亮」「路面的流水反光」。bg | claude-opus-5-5/physics_A__a | 便宜：bg2 场景卡改成「满街浑水 3–4cm、绕过垫脚石」；st5、st8、st4 的画面 / 光线行补上满街流动的浑水；三张首帧重出（st4 右下垫脚石周围要有水绕流）。；便宜：统一成由北（上坡）往南流（庞贝北高南低）；st3 改成「从画左往画右流」，接点表 st3 结尾跟着改。；便宜：规格改成和 p6 一致的 3/3/3 排法；把「攥拳 → 摊开即成排」改成拳头举到镜头前时已经是虚握的平掌，或者先摊开再停半拍（镜头切到已摊平的状态）。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s2_report.md |
| I3 | 严重 | 世界物理·P5 身体可行 | s4_st1、s3_st7 | P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；俯视图里 Tertius 在 Riley 左前方（面朝院子时），她转身面朝机位后 Tertius 到了她右后方约 156°；文字写「上 | claude-opus-5-5/physics_B__a | 便宜：改成「上身往右一拧、从右肩回头瞥一眼 Tertius」；顺带核对 prompt.txt 和 overhead.toml 里的同一句；便宜：动作简化成「把两个布角在腰带上打一个活结」，或把 11–13s 的拍拍布包压短，挪出 1–1.5s | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md、fixes/s4_report.md |
| I4 | 严重 | 世界物理·P2 道具来源与去向 | s5_st3、s5_st2→st12→st3→st14、s5_st6→st7、s5_st7、s5_st3→st14、s5_st8→st9 | P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/phys | claude-opus-5-5/physics_C__a | 便宜：重出首帧，右手握拳伸在台面上方、看不到钱；或者把第一拍改成「已摊开、6 枚」并删掉握拳一拍；便宜：st2 改成把勺搁到后排靠灶罐口（或 st14 开头仍在前排、删掉「探半步取勺」）；st12/st3 清单和首帧补上勺；便宜：st7 改成两人仍站在东头台沿前；或者 st6 改成店里坐着吃；便宜：加一句「把勺横搁回中间罐口，右手拿起抹布」；酒渍改成「擦一擦杯底下」，或交代 Riley 举杯时洒出几滴；便宜：st2/st12/st3 清单补「碗旁叠着抹布」，首帧补画；便宜：st9 重出首帧，改成一只筐、画右半边街在阴影里 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md |
| I5 | 严重 | 世界物理·P8 首帧 = 第 0 秒 | s5_st3、s8_st2、s5_st2 | P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/ph | claude-opus-5-5/physics_C__a | 便宜：重出首帧，右手握拳伸在台面上方、看不到钱；或者把第一拍改成「已摊开、6 枚」并删掉握拳一拍；便宜：首帧改成迈步中（一只脚抬起），或把第一拍改成「已站定」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s8_report.md |
| I6 | 严重 | 世界物理·P9 效果有来源 | s5_st1、s5_st8→st9、s8_st7 | P9 效果有来源 最终 1 分：水花、溅泥、扬尘、影子、反光、湿脚印只出现在有来源的地方（踩在干的石头顶面不溅水，没风不扬尘）；俯视图镜头在她东边、朝西拍，prompt「光线」写太阳在她身后（西）、头发镶边、画左（街南）半边街在阴影里；首帧 | claude-opus-5-5/physics_C__a | 便宜：按「逆光、发丝镶边、画左半边街在阴影里」重出首帧；便宜：st9 重出首帧，改成一只筐、画右半边街在阴影里；便宜：看点改成「出了一身汗、神清气爽」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s8_report.md |
| I7 | 严重 | 世界物理·P6 穿模与距离 | s6_st6 | P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；镜头在大堂里朝南看，画右是西边；但 s6_st4、s6_st5 都写楼梯在“院子西侧”，俯视图里楼梯在 x≈1.5–2.5，在门（x 4.0–5.6）的西边 | claude-opus-5-5/physics_D__a | 便宜：把这一镜门洞里的院子改成楼梯在画右、马厩在画左，Riley 改成从门洞右边出画（转向她的左手边），首帧重出图；俯视图里 Riley 9.4 秒后的路线改成往西南 (2,3.7) 方向走，避开货车 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I8 | 严重 | 世界物理·P9 效果有来源 | s7_st3、s7_st7 | P9 效果有来源 最终 1 分：水花、溅泥、扬尘、影子、反光、湿脚印只出现在有来源的地方（踩在干的石头顶面不溅水，没风不扬尘）；光线段写“0–9.5 秒有灯光……9.5 秒吹灭后：灯嘴一片黑”；节拍是 9.1–10.5 秒还在说 goodn | claude-opus-5-5/physics_D__a | 便宜：光线段改成“0–12.3 秒……12.3 秒吹灭后”，和节拍、道具行统一；便宜：改成“13.8 秒前在她手里……15.8 秒后在小凳上” | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s7_report.md |
| I9 | 严重 | 人物逻辑·C9 像真人 | s3_st4 → s3_st8 → s3_st6、s2_st5 → s2_st8 → s2_st4 | C9 像真人 最终 1 分：把声音关掉看：每个人像活人还是摆件——反应及时（不超过 1.5 秒）、幅度合身份、不僵不夸张；一个梗是否拖成好几拍、同一个梗是否重复用；Felix 摇头笑 3 次（st4、st8、st6），推正或拨正面包 2 次 | claude-sonnet-5-5/character_A__a | 便宜：全集只留一次摇头，放在 s3_st8 末（她走反那一下）；st4 只留「嘴角一动」；st6 删除；便宜：st5 只留「目光落到腿上愣一下、挑一边眉」，不撇嘴摇头；st8 保留回头瞄的半秒；st4 去掉「嘴角撇着」。梗的笑点只落在 st8 台词那一下 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md、fixes/s3_report.md |
| I10 | 严重 | 人物逻辑·C10 动机来自人物 | s3_st4、s3_st6（整镜）/ s3_st8 6–9 | C10 动机来自人物 最终 1 分：每个不寻常的举动（避而不看、不回答、不指方向、突然停住）抛开剧情问「他为什么这么做」：答案只有「情节需要」就 ✗；分镜替他写的心理理由不算数，要看画面上观众能不能读出这个理由；Felix「头一直低着、眼睛 | claude-sonnet-5-5/character_A__a | 便宜：由用户在 story_beats 15/15b 挑改法。改的方向：让 Felix 抬头看她、用手一指街，Riley 带手势问路；让他不看她的理由出自人物（例如手里端着滚烫的托板腾不出手，且观众看得到），而不是「为了让她猜不出」；便宜：删 s3_st6 整镜，或并进 s3_st8 末尾一个小动作（目光追着她、嘴角动一下）。不要吸气前探、不要笑出声；便宜：核实首帧/出片里这些动作是否读得出（在检查面包有没有烤透）；写成「检查面包底」一个动作，去掉「动作要大」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I11 | 严重 | 人物逻辑·C11 反应合比例 | s3_st6（整镜）/ s3_st8 6–9、s3_st4、s2_st5 → s2_st8 → s2_st4 | C11 反应合比例 最终 1 分：配角的反应是不是过演：大表情（张大嘴、张嘴吸气、瞪大眼、鼓腮、笑出声）、单独一整镜的反应、比事情本身还大的情绪一律 ✗；宁可少一个反应，不要一张傻脸；张嘴吸一口气、身子前探、笑出声，单独一镜只拍这个反应；他 | claude-sonnet-5-5/character_A__a | 便宜：删 s3_st6 整镜，或并进 s3_st8 末尾一个小动作（目光追着她、嘴角动一下）。不要吸气前探、不要笑出声；便宜：改成嘴角一动、低头继续摆面包，并入 16.8 秒后的收尾，不单独占拍；便宜：st5 只留「目光落到腿上愣一下、挑一边眉」，不撇嘴摇头；st8 保留回头瞄的半秒；st4 去掉「嘴角撇着」。梗的笑点只落在 st8 台词那一下 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md、fixes/s3_report.md |
| I12 | 严重 | 人物逻辑·C11 反应合比例 | s8_st10、s8_st3 / s8_st8 | C11 反应合比例 最终 1 分：配角的反应是不是过演：大表情（张大嘴、张嘴吸气、瞪大眼、鼓腮、笑出声）、单独一整镜的反应、比事情本身还大的情绪一律 ✗；宁可少一个反应，不要一张傻脸；门房「摇头笑出了声」；规则 C11 把「笑出声」列为 ✗ | claude-sonnet-5-5/character_B__a | 便宜：改成「门房抬一下眉、右手朝画左一挥，嘴角一撇」，去掉笑出声。；便宜：st3 只留 1 位笑，其余用「瞥一眼」「继续梳头」；st8 把 9–10 秒那次改成「画左妇女回头接着聊天」；让反应不都是笑。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s8_report.md |
| I13 | 严重 | 人物逻辑·C10 | s6_st3 | C10：「被画面左边、镜头身后的什么动静吸引」；画面上没有任何东西可看，观众读不出她为什么突然转身走；而她听不懂拉丁语，下一镜 s6_st1 才是 Fortunata 的吆喝 | claude-sonnet-5-5/character_B__a | 便宜：写明动静 = 画外传来 Fortunata 低沉的招揽声（Hospitium hic locatur!）和暖灯光，她听到声音、看到门口灯光才转身；或把她往左走的理由写成「看见画外的油灯光」。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I14 | 严重 | 连续性·K2 钱账 | s5_st3 | K2 钱账 最终 1 分：每次付钱前后的枚数和种类，全集账平；首帧放大（z2.jpg 左）摊开的掌心里是 4 枚红铜＋1 枚黄铜＝5 枚；spec 要求 0 s 攥拳，1.5 s 摊开时「正好 6 枚：5 红铜＋1 黄铜」。按这张首帧出片， | claude-opus-5-5/continuity__a | 便宜：首帧重出，第 0 秒画右拳攥着、看不见钱；或者画摊开的手、正好 5 红＋1 黄 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md |
| I15 | 严重 | 连续性·K5 站位接续 | s6_st6、s3_st1 → s3_st2 | K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧（z1.jpg 右）也 | claude-opus-5-5/continuity__a | 便宜：spec 和 prompt 改成「院子右边（西侧）的石楼梯／马厩木栏在画左」「从门洞右边走出画」，overhead 走位改成朝西，首帧重出；可以不改（Felix 在画外）；要严谨的话，st2 开头加「Felix 转身去炉口」的声音提示 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md、fixes/s6_report.md |
| I16 | 严重 | 连续性·K6 环境接续 | s6_st6、s2_st1 ↔ s2_st3、s5_st6 ↔ s5_st7 | K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧 | claude-opus-5-5/continuity__a | 便宜：spec 和 prompt 改成「院子右边（西侧）的石楼梯／马厩木栏在画左」「从门洞右边走出画」，overhead 走位改成朝西，首帧重出；便宜：定一个方向，按北高南低算，s2_st3 改成「从画左往画右流」；s2_st2/st5/st4 里提到流向的地方一起核一遍；便宜：st7 改成「柜台东段外侧台沿边站着那两个男人（同 st6）」，首帧重出 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md、fixes/s5_report.md、fixes/s6_report.md |
| I17 | 严重 | 台词（时长与逻辑）·D1 说得完 | s8_st9、s1_st1、s6_st3、s4_st1 | D1 说得完 最终 1 分：时间够念：按正常语速（约 2.5 词/秒；语速要正常，不能靠说快塞进镜头）算出每句需要的时间与留白（开口前 ≥1 秒、说完后 ≥1.5 秒），给数字；不够时写「镜头要延长到 X 秒 / 节拍怎么重排 / 要加的镜 | claude-sonnet-5-5/dialogue__a | 不改句子；镜头延长到约 23 秒，把 “Gross.” 后的皱鼻子停半拍后，“Kind of love it, though.” 窗口放到 16.4–18.9 秒，递刮板的动作整体后移 1 秒。便宜（改节拍文字，出片前）；不改句子；把走近镜头那一段拉长 1 秒（16.5–20.5 秒），镜头延到 23 秒或把 19.5–21 秒的停留压短。便宜；把 6.3–11.7 拉到 6.3–12.2 秒，“That’s — not ideal.” 给 1.8 秒（17.0–18.8 秒），后面的转头出画顺延 0.6 秒，镜头 23→24 秒。便宜；Apage 窗口放到 6.4–7.1 秒，Riley 台词窗口放到 8.8–11.0 秒（镜头 13 秒内够用）。便宜 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s4_report.md、fixes/s6_report.md、fixes/s8_report.md |
| I18 | 严重 | 台词（时长与逻辑）·D8 跨语言说清 | s3_st4 | D8 跨语言说清 最终 1 分：Riley 对听不懂英语的人说话时：她的意图有完整说法加手势，对方的回答配了观众看得懂的动作；只有一个词、没有手势的问句 ✗；Riley 只问 “Garum?”，Felix “头一直低着、眼睛只看托板”、无手 | claude-sonnet-5-5/dialogue__a | 已知问题，不展开：按 story_beats 里用户挑的改法重写（Riley 用完整说法 + 手势问路，Felix 抬头、手指方向、慢一点说）。便宜（改文字）；若已出视频则要积分；Riley 说 “left” 的同时抬手往左一指，Felix 看到手势才憋笑。便宜 | 要积分 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I19 | 严重 | 母语听感·N8 修辞痕迹 | s7_st1、s4_st5、s3_st2、s8_st4、s4_st2、s3_st4、s6_st3、s5_st7、s4_st3、s5_st1 | N8 修辞痕迹 最终 1 分：自问自答、三连排比、停顿抖包袱、工整对仗、字幕 / 广告文案腔的句子数；每处都列出，像「写出来的台词」就扣分；「So I found a bed, I tried the garum… and I have z | claude-sonnet-5-5/native_ear__a | 便宜（只改台词文字）。改成：「Okay, so — I've got a bed. I ate the fish sauce. And I'm, like, completely broke. …Yeah, no. Honestly, still worth it.」或更散的：「So I have a bed, I had the garum, and I have, like, no money. Which — fine. Worth it.」；便宜。改成：「…No. It just smells like, you know, metal. Okay, honestly? He kind of has a point.」去掉「smells like money」的整齐双关，或保留但把它放在笑完之后的自言自语里；便宜。改成：「Oh it's pre-cut — look, it just snaps right off. That's so smart. Okay, Romans, one point.」；便宜。改成：「Oh my god, it is so hot in here. Why am I still wearing all my clothes? I'm such an idiot.」；便宜。拆成两三句带自我打断的：「So — they wash clothes in pee here. Like, actual pee. And the emperor — okay, apparently the emperor taxed it. His son was like, ew, and he goes — he holds up a coin, like, 'Does this smell?'」；便宜。改成：「Okay… I definitely heard 'dextram.' No idea what that means. I mean, he said 'straight,' I think? So maybe it's, like, a direction? Left or right… I don't know. I'm gonna go left.」（先说出她为什么猜方向）；便宜。改成：「Okay, the sun is going down, I have nowhere to sleep, and — this is what I have left. Uh. Not great.」；便宜。改成：「Okay. Garum, done. That was so good. Okay — now I really need to find a bed.」；便宜。改成：「Okay, going left. I'm pretty sure. Ish. Probably.」；便宜。改成：「Okay, I'm clean. Ish. And I'm starving — and, weirdly, that's fine, because people here eat dinner at, like, three-thirty. So it's basically dinner time.」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md、fixes/s4_report.md、fixes/s5_report.md、fixes/s6_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I20 | 严重 | 时代与世界观·E5 文字 | s7_st1、s7_st2 | E5 文字 最终 1 分：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）；首帧墙面灯上方（约 x360–520,y360–560）有五行像字母的刻痕，放大后第一行像「ACNAP」，第二至四行是连续的伪拉丁字母（裁切图 s7st1_g | claude-opus-5-5/era__a | 便宜：重出首帧，把这片墙改成乱刮的交叉短线、计数划痕，或把这片墙放到灯影外；负面词加「像字母的刻痕、成行的伪文字」；便宜：分镜改成「一小片刻得较深、交错杂乱的划痕，没有行、没有字形」，或让 Riley 只朝墙一摆手、不给墙特写；首帧重出 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s7_report.md |
| I21 | 严重 | 时代与世界观·E7 规则源 | s7_st2、s1_st1、s1_st2、s1_st4、p4 刮板（s8_st5、s8_st9、s8_st6） | E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；首帧左上（约 x120–340,y460–660）有四行整齐的伪字母刻痕（裁切图 s7st2_graffiti.png）；spec 第 11 行要求的「几行排得整 | claude-opus-5-5/era__a | 便宜：分镜改成「一小片刻得较深、交错杂乱的划痕，没有行、没有字形」，或让 Riley 只朝墙一摆手、不给墙特写；首帧重出；便宜：bible §9 改成与 dossier 一致；bg1 场景行改用 dossier 第 78 行的写法，去掉「葡萄藤」，再压小压淡；或按 bible 审查建议让山不入画；便宜：查 MANN 或大英博物馆的 strigil 图录后改卡，写成「整件青铜，弯勺和扁平把手连成一体」 | 便宜 | implemented | 刻痕改为交错杂乱、看不出字形（s7 st1/st2 文字与首帧重出）；山入不入画、怎么写待用户定（bible §9 与故事点 1B/4A/41A），s1 三张首帧的山暂不动 |
| I22 | 严重 | 镜头规格·F1 景别与人物大小 | s8_st7、s5_st3 / st14 / st13 / st7、s7_st6、s7_st3、s5_st12、s6_st5、s8_st10、s8_st9 / st6 / st3 | F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；老汉（prop 路径起点 (8.2,8.7)）距机位 (5,8) 3.28 m、35 mm、机位高 0.9 m，应占画高约 0.91；首帧 | claude-opus-5-5/framing_B__a | 重出首帧，老汉画到约 0.85–0.9 画高（便宜）；站位图机位拉近到约 1.9 m，与首帧一致；或按 2.3–2.6 m 重出首帧。st3 文字「中景、两米多」与「中近景」二选一（便宜）；按首帧反推改 overhead（机位往前约 0.9 m，或 Riley 往左）（便宜）；机位改到约 (1.3,1.6)，或景别改「中近景」，二者择一对齐（便宜）；重出首帧时按 st2 的大小（便宜）；文字改「中景」，或重出首帧（便宜）；overhead 机位前移约 0.4 m 并右偏（便宜）；三处文字按几何改（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s6_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I23 | 严重 | 镜头规格·F3 画面位置 | s5_st8、s7_st6、s7_st3、s8_st10、s5_st8 / st9、s6_st6、s8_st4、s5_st2、s6_st2、s8_st9 / st6 / st3、s6_st4 | F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；按 overhead，横街口和近角墙 (11.5,14) 应在 u0.59–0.67；首帧里店主铺子西边的南侧铺面连成一片，看不到横街口和墙角。看点「驴车拐进右边横 | claude-opus-5-5/framing_B__a | 重出首帧，在 u≈0.6–0.67 画出横街口和挡车的墙角（便宜）；按首帧反推改 overhead（机位往前约 0.9 m，或 Riley 往左）（便宜）；机位改到约 (1.3,1.6)，或景别改「中近景」，二者择一对齐（便宜）；overhead 机位前移约 0.4 m 并右偏（便宜）；look 改为接近正东，或机位往北挪，重出 overhead_ref（便宜）；改 overhead：终点不压货车，楼梯标到画左，并注明这里有意镜像（便宜）；overhead note 与首帧二选一对齐（便宜）；首帧让她只在画右边缘露半身，或改文字（便宜）；机位西移约 0.3 m（便宜）；三处文字按几何改（便宜）；确认后改图或改 overhead（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s6_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I24 | 严重 | 镜头规格·F4 节拍秒数 | s7_st7、s7_st3、s5_st3、s6_st3、s6_st4、s7_st6、s8_st10、s5_st14、s6_st1 | F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；资料包/prompt.txt 第 16 行「光线」写「8 秒前在她手里…10 秒后灯在床头小凳上」；动作行和 overhead [[beat]] 写 13.8– | claude-opus-5-5/framing_B__a | 光线行的秒数改成 13.8 / 15.8 秒（便宜）；光线行改成 0–12.3 秒 / 12.3 秒熄灭（便宜）；重出攥拳的首帧，或改第 0 拍文字；镜头栏改成付后手心数得清（便宜）；镜头段改成 11.8–16.2 秒（便宜）；改成 8 秒到顶，或镜长加到 10–11 秒（便宜）；统一时刻，或删去这段下摇（便宜）；这一拍拉到 2 秒（便宜）；把喝水后的空闲时间匀一些过来（便宜）；路径终点延到 x=8.5（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s6_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I25 | 严重 | 镜头规格·F8 看点画得出来 | s5_st8、s8_st7、s5_st3、s7_st4、s7_st5 | F8 看点画得出来 最终 1 分：每镜的 point（这一镜要观众看懂什么）靠哪些画面元素传达；这些元素在 prompt 里写成看得见的具体样子、首帧里就看得到（例：满街流动的水、只有石头顶面是干的）；没写 point 的镜头判 ✗；按 o | claude-opus-5-5/framing_B__a | 重出首帧，在 u≈0.6–0.67 画出横街口和挡车的墙角（便宜）；统一成「衬衫干爽、抖一抖前襟透气」（便宜）；重出攥拳的首帧，或改第 0 拍文字；镜头栏改成付后手心数得清（便宜）；看点改为「草垫床」，或写成床沿露出绳网（便宜）；首帧补出明显的街槽（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I26 | 严重 | Prompt 文本·T1 自相矛盾 | s1_st1、s3_st5；s8_st3/4/5/6/8/9 | T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；正文要「自己的相机架在沙滩上录着」「她把这台相机拿了起来」，负面词写「相机，手机，自拍杆」。bible.md:30 已给这一镜开例外，编译器仍套了剧 | claude-sonnet-5-5/prompt_text__a | 便宜：本镜负面词删「相机」，保留「手机，自拍杆」；最好在编译器里做按镜例外。；便宜：把「白烟，浓烟」改成「烟柱，升上天空的白烟」；s8 各镜正文加「室内雾气」。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s3_report.md |
| I27 | 严重 | Prompt 文本·T4 图文一致 | s5_st3 | T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；首帧是摊开手心托钱，文字写第 0 秒攥拳，1.5 秒才摊开。首帧「视频从这张图开始」，模型会按图不按字。 | claude-sonnet-5-5/prompt_text__a | 便宜：重出首帧成攥拳，或把动作行第 0 秒改成「手心朝上摊开，钱在手心里」，去掉攥拳那一拍。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md |
| I28 | 严重 | 角色立场·Riley·V1 语言 | s3_st4、s4_st1、s3_st1、s3_st7、s5_st4/st13、s6_st5、s8_st5/st9、s8_st2、s5_st2、s6_st1、s5_st11、s2_st8 | V1 语言 最终 1 分：我说的话（措辞、长短、语种、音量）面对此刻这个人合不合适；对方听不懂我的语言时，他能不能明白我要什么；只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人 | claude-opus-5-5/role_c1__a | 已知，等用户在 story_beats.md 选改法。站在我的立场：此刻的我会边说「Garum? Uh… where?」边做倒酱的手势，摊手四下看。听到 dextram 后，左右各指一下问「This way? That way?」，等他用手指路（便宜）；此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字）；此刻的我：s3_st7 布包递过来时说「Oh — thank you!」，手按胸口点一下头；s8_st9 递回刮板时小声说「Thank you.」。其余镜头用手按胸口加点头代替，不必每镜都开口（便宜，加半句台词或一个动作）；此刻的我：走到门房面前先开口「Salve!」，这次读对一点，带点得意；门房因为这声才抬头（不是因为脚步声）。s5_st2 或 s6_st1 也可以再用一次，是全集唯一学到手的词（便宜）；此刻的我：说「one…」时竖一根手指、朝前排那只罐子一点；说「two…」时竖两根手指、朝她扬下巴示意的那只带木盖的罐子一点，配一个「好喝？」的表情；最后才比 OK（便宜）；此刻的我：压低声音、凑近镜头说「Yeah… I don't think she's a fan of the pants.」（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md、fixes/s3_report.md、fixes/s4_report.md、fixes/s5_report.md、fixes/s8_report.md |
| I29 | 严重 | 角色立场·Riley·V2 肢体 | s4_st1、s8_st2、s5_st2、s6_st1、s5_st12 | V2 肢体 最终 1 分：我的手势、姿态、和对方的距离，合不合我的身份、对方的身份和这个场合；s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9  | claude-opus-5-5/role_c1__a | 此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字）；此刻的我：走到门房面前先开口「Salve!」，这次读对一点，带点得意；门房因为这声才抬头（不是因为脚步声）。s5_st2 或 s6_st1 也可以再用一次，是全集唯一学到手的词（便宜）；此刻的我：手比着 OK 往前伸到柜台上方、朝向她，身子微微前探，挑眉等回答（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s4_report.md、fixes/s5_report.md、fixes/s8_report.md |
| I30 | 严重 | 角色立场·Riley·V6 动机 | s3_st4、s4_st1、s8_st2→s8_st10、s6_st3、s8_st3、s8_st8、s7_st4–s7_st3、s5_st13、s7_st2、s3_st1 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人 | claude-opus-5-5/role_c1__a | 已知，等用户在 story_beats.md 选改法。站在我的立场：此刻的我会边说「Garum? Uh… where?」边做倒酱的手势，摊手四下看。听到 dextram 后，左右各指一下问「This way? That way?」，等他用手指路（便宜）；此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字）；此刻的我：把一手钱摊给门房看，挑起眉等她拿；或者先试探着递出最小那枚，手停在半空等她反应，见她收下才松手，所以下一镜才惊喜（便宜）；此刻的我：19.4 秒画外传来一个女人低沉的吆喝和骡子的响鼻、车轮声，我转头一看，眼睛一亮，因为大车进出的大门就是旅店。在 s6_st3 的音效里写明这声吆喝（便宜）；此刻的我：s8_st8 被盯着时，眼睛扫一下壁龛里叠好的衣服，手摸到衬衫最上面那颗扣子犹豫一下，又松开，脸一红，干脆快步往里走。这样「Rookie mistake」才是我自己选的（便宜）；此刻的我：s7_st4 推上门后顺手摸一下门边，发现没有闩，愣一下；s7_st6 讲完空调和厕所，补一句「…and no lock. Cool cool cool.」，或者拿凳子顶住门。这也接上「Cool cool cool」的笑点（便宜，属故事层要用户定）；此刻的我：问完「Garum?」，手往裤袋那边一摸、挑眉看她；她摆摆手，拿罐就倒。这样她的大方也看得见（便宜）；此刻的我：端起灯凑近墙，眯眼用手指描着字母，念出「Vi-bi-us… Re-sti-tu-tus」，认出人名才说「I swear this was in my history textbook」。剧级规定不出现可读文字，要核实凑近照明会不会让字显形（便宜）；此刻的我：放下 2 枚后抬眼看 Felix、挑眉，意思是「够吗？」；他点头，我才松口气笑（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md、fixes/s4_report.md、fixes/s5_report.md、fixes/s6_report.md、fixes/s7_report.md、fixes/s8_report.md |
| I31 | 严重 | 角色立场·Felix·V1 语言 | s3_st4、s3_st8、s3_st7 | V1 语言 最终 1 分：我说的话（措辞、长短、语种、音量）面对此刻这个人合不合适；对方听不懂我的语言时，他能不能明白我要什么；已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没 | claude-opus-5-5/role_c2__a | 便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路；便宜：改文字。此刻的我会下巴一扬、喊 "Vale!"（洪亮带笑）；便宜：打包前下巴朝面包一努问 "Hmm?"，递布包时说 "Tene!" | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I32 | 严重 | 角色立场·Felix·V2 肢体 | s3_st4→st8→st6、s3_st4 | V2 肢体 最终 1 分：我的手势、姿态、和对方的距离，合不合我的身份、对方的身份和这个场合；托板约 34 秒不离手；st4 17–18.5s「两手把托板重新端起来」，搁下了又端起，只为了让我腾不出手；st6 5.5s 才放下 | claude-opus-5-5/role_c2__a | 便宜：改文字。st7 结尾端来托板后，st4 一开场就放在石台上（或者搁上就不再端起），我手是空的；配合 story_beats 15 的 B 方案（腾手朝他自己的右边一指，形成镜像误会）最自然；便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I33 | 严重 | 角色立场·Felix·V3 表情 | s3_st8→st6、s3_st1 | V3 表情 最终 1 分：我的表情和强度合不合此刻的处境；不过演、不面无表情；st8 6–9s 我已经摇头认了、拨正了面包，st6 0–2.5s 目光又追过去、吸气想喊，冲动排在放弃之后，顺序反了；st6 表情过演（已知 15b） | claude-opus-5-5/role_c2__a | 便宜：按 15b 的 A 方案删 st6，或者把「想喊又停」挪进 st8 后景，st6 只留低头放托板；便宜：首帧改成专心干活的平常脸 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I34 | 严重 | 角色立场·Felix·V4 视线 | s3_st4、s3_st1 | V4 视线 最终 1 分：我看谁、什么时候看；被人问话、递东西时我会看着对方；已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就 | claude-opus-5-5/role_c2__a | 便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路；便宜：抬头时目光先往下扫一眼她的裤子和靴子、挑一下眉，再喊 Salve | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I35 | 严重 | 角色立场·Felix·V5 回应 | s3_st4、s3_st8→st6、s3_st8 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同样写 | claude-opus-5-5/role_c2__a | 便宜：改文字。此刻的我会在她 7–8s 转身对空街说话时停手，看她、顺着她的视线看一眼空街，皱眉憋笑轻摇头（觉得这外地人怪），然后接着干活，反应不对齐 left；只保留听到 dextram 时抬眼；便宜：按 15b 的 A 方案删 st6，或者把「想喊又停」挪进 st8 后景，st6 只留低头放托板；便宜：改文字。此刻的我会下巴一扬、喊 "Vale!"（洪亮带笑） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I36 | 严重 | 角色立场·Felix·V6 动机 | s3_st4、s3_st4→st8→st6、s3_st8、s3_st1 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同 | claude-opus-5-5/role_c2__a | 便宜：改文字。此刻的我会在她 7–8s 转身对空街说话时停手，看她、顺着她的视线看一眼空街，皱眉憋笑轻摇头（觉得这外地人怪），然后接着干活，反应不对齐 left；只保留听到 dextram 时抬眼；便宜：改文字。st7 结尾端来托板后，st4 一开场就放在石台上（或者搁上就不再端起），我手是空的；配合 story_beats 15 的 B 方案（腾手朝他自己的右边一指，形成镜像误会）最自然；便宜：加一个看得见的理由，比如喊一声 "Heus! Dextram!" 被经过的驴车 / 母子盖住，或者她已经拐出去，我再耸肩笑；便宜：抬头时目光先往下扫一眼她的裤子和靴子、挑一下眉，再喊 Salve | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I37 | 严重 | 角色立场·Tertius·V5 回应 | s4_st1 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；节拍写 2.5–5 秒她大声嚷 "Oh — oh no. That's pee!"（2.6–4.9 秒），我在 5–5.7 秒才「扭头看 | claude-opus-5-5/role_c3__a | 此刻的我会：她 "Oh —" 一出口就扭头；利用她 "oh no" 前的那一顿（约 3.0–3.4 秒）作为我的单独一拍——「Tertius 停下脚，转过上身看向她，皱紧眉」，之后一直看着她直到她出门；5–5.7 秒那拍改成「Tertius 盯着她，下巴一抬」。**便宜**（改分镜文字＋首帧不变）；已保留的旧片（20261108-223157，Tertius 约 6.5 秒才扭头）要改则**要积分**；此刻的我会：7.2–8 秒余光瞥一眼笑的工友、嘴角一撇；8–8.8 秒她回头瞥我，我瞪着她、下巴朝门口一扬；8.8–10.8 秒手放下、哼一声、仍看着她；10.8 秒起低头接着踩。写进节拍并加「Tertius 全程留在他的单人小石槽里」。**便宜** | 要积分 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s4_report.md |
| I38 | 严重 | 角色立场·Fortunata·V2（站位）· prompt | s6_st1/st2/st5 | V2（站位）· prompt：三镜 prompt.txt 第 8–9 行：Riley＝「overhead 里的蓝色圆点」、女店主＝「黄色圆点」；三张 overhead 图例与图上都是 Fortunata 蓝、Riley 黄。颜色标反，模型可 | claude-opus-5-5/role_c5__a | 便宜：修 prompt 编译里的颜色映射（或 overhead 配色），重编三镜 prompt | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I39 | 严重 | 角色立场·Vibia·V3 表情 | s2_st5、s2_st4 | V3 表情 最终 1 分：我的表情和强度合不合此刻的处境；不过演、不面无表情；`st5_overhead.png` 时间轴「3.4–5s 表情愣住、困惑、嘴抿着；5–7s 她就那样盯着看……两手扶着满水罐，一动不动」，与 spec「全程手上 | claude-opus-5-5/role_c6__a | 便宜：按现行 spec 重生成俯视图（`python tools/shot_pack.py sync episodes/ep01 s2_st5` 一类），核对时间轴文字；便宜：改为「目光落到腿上停住半拍，眉毛挑起、嘴角往下一压，干脆扭回身」，删当面摇头；摇头挪到 st4 她走过之后（她看不见时）；便宜：删「嘴角还撇着」，改「她擦身过去时肩膀往墙边一收、左手护一下罐耳，眼睛仍不抬」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md |
| I40 | 严重 | 角色立场·Vibia·V5 回应 | s2_st5、s2_st8 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」；上一 | claude-opus-5-5/role_c6__a | 便宜：st5 给 Riley 加一段画外声（如 2.0–2.6 秒一句含糊的 "Okay…" 或一声笑，标「画外、听不清」），声音行改成「画外有人说话」；或把 s2_st2 的尾句延到 st5 开头做音频前搭（剪辑处理）。我的动作改为「手上一顿 → 直腰 → 扭头找声音」；便宜：按现行 spec 重生成俯视图（`python tools/shot_pack.py sync episodes/ep01 s2_st5` 一类），核对时间轴文字；便宜：按现行 spec 重生成 st8 俯视图并核对时间轴；便宜：统一为「1–2 秒抬眼半秒、挑眉、不摇头；约 6 秒她笑出声时我眼珠斜上扫一下不抬头、手上擦得更重；8–11 秒她回头时我已低头不接眼神」，删配角段的「轻轻摇头」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md |
| I41 | 严重 | 角色立场·Vibia·V6 动机 | s2_st5、s2_st8、s2_st4 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」； | claude-opus-5-5/role_c6__a | 便宜：st5 给 Riley 加一段画外声（如 2.0–2.6 秒一句含糊的 "Okay…" 或一声笑，标「画外、听不清」），声音行改成「画外有人说话」；或把 s2_st2 的尾句延到 st5 开头做音频前搭（剪辑处理）。我的动作改为「手上一顿 → 直腰 → 扭头找声音」；便宜：按现行 spec 重生成 st8 俯视图并核对时间轴；便宜：加我的收尾：「2–4 秒 抬眼目送她背影，鼻子里轻哼、摇一下头；4–6 秒 把布塞回腰带，两手抱罐挎上左髋；6–8 秒 转身往北（镜头方向）走出画左 / 进身后门」；同步俯视图走位与首帧不变；便宜：改为「一个女人穿着蛮族人的裤腿」或直接删心理说明，只留可见动作 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md |
| I42 | 严重 | 角色立场·Helvia·V5 回应 | s8_st6、s8_st5、s8_st9 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；spec 节拍与 prompt 第 72 行 9–19 秒只写 Riley；她 10.1–13.4 秒朝我偏头、17–19 秒拍膝坐直， | claude-opus-5-5/role_c7__a | 便宜：节拍补「9–19 秒 Helvia 一直含笑看着她，她偏头时 Helvia 挑一下眉、轻轻笑出鼻音（闭着嘴）；她拍膝坐直时 Helvia 点点头，自己往后靠回墙上，嘴始终闭着」；便宜：改为「拿起油瓶朝她晃一晃、眉毛一挑，再朝她的胳膊努努嘴」，Riley 才伸小臂；拿瓶动作可与 5–6.5 秒合并；便宜：补「Gross 时 Helvia 嗤地笑、摇摇头」；「接过刮板时用它朝她还油亮的胳膊比一下、摇头笑，再放回凳上」；「她冲 Helvia 笑，Helvia 回笑、点一下头」，全程闭嘴 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s8_report.md |
| I43 | 主要 | 世界物理·P1 手数 | s2_st5 | P1 手数 最终 1 分：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手；道具行写「出场时在槽沿上，满的，她两手扶着」，节拍 5.2–7 秒又写她从腰带抽布、低头擦罐，手不够。prompt.txt 里原样都有。 | claude-opus-5-5/physics_A__a | 便宜：道具行改成「出场时罐在槽沿上，左手扶罐耳，右手拿布擦罐身」，和 st8、st4 对齐。；便宜：二选一。规格改成「左手托底、右手扶罐口」，或首帧重出。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md |
| I44 | 主要 | 世界物理·P2 道具来源与去向 | s3_st3 / st7 / st4、s3_st7 | P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；放大后碗里分别有 4 枚黄铜色、约 4–5 枚浅色、约 5 枚；s3_st1 首帧碗是空的，s3_st6 首帧正好 2 枚红铜。四镜连着看，钱数一路跳变 | claude-opus-5-5/physics_B__a | 便宜：局部重绘这三张首帧，碗里改成 2 枚红铜小钱，或者碗口角度不露底；三镜 spec 补一句「碗里正好 2 枚红铜小钱」；便宜：首帧补画 Felix 身后齐腰高的工作台和托板，或者末拍改成只转身、不伸手；便宜：局部重绘成缺一瓣的整只面包 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I45 | 主要 | 世界物理·P8 首帧 = 第 0 秒 | s3_st8 | P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；首帧 Riley 占画高约七成，在车道上，离石台约 3.5–4 m；spec 和俯视图要她紧贴石台外侧挥手。接着她还要「朝街上走两步」，会走到离机位 | claude-opus-5-5/physics_B__a | 便宜：重出首帧，让 Riley 站在石台外沿（全身约占画高五成五），或者把 spec 改成「七成」对应的机位前移；三者统一 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md |
| I46 | 主要 | 世界物理·P7 服装与动作相容 | s8_st5 | P7 服装与动作相容 最终 1 分：衣服允许这个动作（短袖不能卷袖、塞进腰里的下摆不会自己跑出来）；文字写刮到左臂「肘弯上方」，人物卡写半袖垂到肘部，刮的位置应该在袖子里；首帧干脆把 Helvia 左臂画成整条光着，st9/st6 首帧半袖 | claude-opus-5-5/physics_C__a | 便宜：改成「刮到左小臂靠肘处」，或加一句「左边半袖撩到肩头」，三镜一致 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s8_report.md |
| I47 | 主要 | 人物逻辑·C9 像真人 | s8_st9 / s8_st10 / s8_st6 / s5_st12 / s5_st7 / s6_st6、s8_st8 | C9 像真人 最终 1 分：把声音关掉看：每个人像活人还是摆件——反应及时（不超过 1.5 秒）、幅度合身份、不僵不夸张；一个梗是否拖成好几拍、同一个梗是否重复用；「Riley 对空气说话，旁人憋笑 / 摇头笑 / 看一眼」在 s8_st1 | claude-sonnet-5-5/character_B__a | 便宜：只留 2–3 处（建议 s8_st10 门房、s5_st7 Asellina），其余改成当地人手上的活不停、根本没注意她，不加表情。；便宜：删掉 9–10 秒那次，只留 2.5–4 秒的反应拍。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s8_report.md |
| I48 | 主要 | 连续性·K4 光与时间 | s7_st3、s7_st7、s1_st5 | K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；光线段写「0–9.5 秒有灯…9.5 秒吹灭后只剩窗洞微光」，节拍和道具段写的却是 10.8–12.3 s 吹、12.3 s 灭，台词 9.1–10.5 s 才说完 g | claude-opus-5-5/continuity__a | 便宜：光线段改成 0–12.3 秒、12.3 秒吹灭后；便宜：光线段改成「13.8 秒前在她手里…15.8 秒后在凳上」；便宜：首帧重出时按 spec 的受光侧来 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s7_report.md |
| I49 | 主要 | 连续性·K8 镜间接点 | s6_st5 → s6_st6、s3_st8 → s3_st6 | K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西、情绪和音量，和下一镜第 0 秒接得上；接不上时要有切的理由（跳过时间、换地点、 | claude-opus-5-5/continuity__a | 便宜：st6 第 0 秒直接写勾环加护火，删掉换手这一拍；已知问题，等用户在 story_beats 里挑改法 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s3_report.md、fixes/s6_report.md |
| I50 | 主要 | 母语听感·N9 / N7 | s1_st2 | N9 / N7：「Good morning from Pompeii! It's May, 75 AD — which is so weird to say out loud. Okay, so, two goals today: …」是对 | claude-sonnet-5-5/native_ear__a | 便宜。改成：「Hi — okay, good morning, from Pompeii. It's, uh, May, 75 AD. Which is so weird to say. Okay, two things today: I need somewhere to sleep, and I need to try garum — it's this fish sauce everyone here is obsessed with. And that's it. That's the plan. Oh, and my budget is… this.」（钱放最后随口带过，不做停顿亮相；若要保留亮钱，摊手时说「this」即可） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I51 | 主要 | 镜头规格·F1 景别与人物大小 | s2_st4 | F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；按 overhead.toml 第 11 行机位 (14.0,17.2)、第 14 行 28mm，Riley 在 5.42 m 应占画高约 | claude-opus-5-5/framing_A__a | 便宜：把 overhead 机位往南挪到约 y≈19.5（仍在垫脚石东北边、最近一块石头在右下角前景），或按 45mm 等效重算；改完重跑 sync | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s2_report.md |
| I52 | 主要 | 镜头规格·F2 机位与朝向 | s2_st3、s1_st4 | F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead.toml 是 11-08 的旧版：第 6 行 note 写「升镜头…镜头在西人行道边贴地」，第 11/21 行 h=0.3，第 31 行 | claude-opus-5-5/framing_A__a | 便宜：按现行文字改 overhead.toml（h=1.6、三个路点 look 统一、改 note），重跑 shot_pack sync，重出俯视图；便宜：清理 toml 注释和节拍文字；把 Riley 的朝向点改成 (36.8,56.5) 一带，让 overhead 显示侧身 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s2_report.md |
| I53 | 主要 | Prompt 文本·T2 否定句 | s1_st4、s3_st6、s5_st3、s2_st3、s7_st4、s7_st1、s5_st8 | T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；「没有耳钉、没有耳环」「没有第三枚」「没有银色或金色的钱」「不放在深色的木盖上」「墙上没有阳光」「没有月光、没有光束」「没有任何音乐声」，每句都点出了 | claude-sonnet-5-5/prompt_text__a | 便宜：改成正向描述，例如「耳垂光着，被头发盖住」「陶碗里两枚红铜钱」「钱都是红铜色和金黄色」「钱放在浅色大理石台面上」「整面墙在阴影里」。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I54 | 主要 | Prompt 文本·T5 混入别镜 | s1_st1、s5_st10、s7_st1、s8_st2 | T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；正文夹着「下一镜她举着它自拍」「（接上一镜）」「上一镜她刚坐下」「交给 st10 的台词」，指代的是 prompt 之外的镜头。 | claude-sonnet-5-5/prompt_text__a | 便宜：删掉这些括号；接点信息放在首帧和 junctions，不进 prompt。 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I55 | 主要 | Prompt 文本·T7 长度与重点 | s1_st2（4903 字）、s8_st9（4882 字）、s6_st3（4782 字）、s1_st4 | T7 长度与重点 最终 1 分：prompt 不超长，关键动作写在前面、写得清楚；离 5000 字上限不到 120 字；「画面」「走位」「动作」「镜头」重复叙述同一串动作；s1_st4 的 23 秒节拍过满（拉船、丢绳、抬筐、对视、说台词） | claude-sonnet-5-5/prompt_text__a | 便宜：编译时让「画面」只写静态构图与道具，动作只留「动作」一行；s1_st4 考虑拆成两镜（要积分）。 | 要积分 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I56 | 主要 | 角色立场·Riley·V5 回应 | s3_st1、s3_st7、s5_st4/st13、s6_st5、s8_st5/st9、s1_st5、s2_st4、s4_st3、s8_st6→s8_st7、s5_st7→s6_st3 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；整集别人给我面包、替我打包、倒鱼露、递灯、滴油递刮板，我从来不说一句 thank you，只「笑笑 / 点头」。一个爱说话的美国女孩，被 | claude-opus-5-5/role_c1__a | 此刻的我：s3_st7 布包递过来时说「Oh — thank you!」，手按胸口点一下头；s8_st9 递回刮板时小声说「Thank you.」。其余镜头用手按胸口加点头代替，不必每镜都开口（便宜，加半句台词或一个动作）；此刻的我：s1_st5 笑着点头回礼；s2_st4 擦肩时冲女孩笑一下、轻轻摆一下手指（背影也能看出偏头）；s4_st3 让开半步，小声说「oh — sorry」（便宜）；此刻的我：s8_st6 拍完膝盖站起来，冲 Helvia 笑着挥手、手按胸口点头；s5_st7 喝完放下杯子，冲 Asellina 挥一下手，再走（便宜） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s3_report.md、fixes/s8_report.md |
| I57 | 主要 | 角色立场·Felix·V7 跨集一致 | c2_Felix.md | V7 跨集一致 最终 1 分：跨集一致：和行为档案（人物目录 behavior.md）、前几集的我对照——说话方式、口头禅、对陌生人的态度、肢体习惯、表情分寸、不会做的事，这一集有没有变；变了要有这一集里看得见的原因，没有原因判 ✗。审完在 | claude-opus-5-5/role_c2__a | 便宜：卡里注明 turntable「只取音色，动作和台词都不取」；人物卡个性行与本集指路写法二者择一，统一 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md |
| I58 | 主要 | 角色立场·Tertius·V2 肢体 | s4_st1 | V2 肢体 最终 1 分：我的手势、姿态、和对方的距离，合不合我的身份、对方的身份和这个场合；「朝她挥手赶人」没写手型和方向，「挥手」在模型里常画成打招呼 | claude-opus-5-5/role_c3__a | 此刻的我会：右手手背朝她、往门口方向用力甩两下，同时喊 "Apage!"；时间够可再朝门口一指加 "Foras!"。**便宜**；此刻的我会：脚踩在槽里不动，**转过上身**侧过来看她（不是只拧脖子）。文字改「转过上身看她」。**便宜** | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s4_report.md |
| I59 | 主要 | 角色立场·Asellina·V5 回应 | s5_st14 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；节拍 7–8 秒「Riley 看着，抬起右手指着杯子」，8–10.8 秒 Asellina 只「往杯里慢慢点了一小股冷水，把水罐放回原处 | claude-opus-5-5/role_c4__a | 便宜：8–10.8 秒改为「她兑着水，抬眼看 Riley 指着杯子的手，扬一下眉，下巴朝杯子一点（当然要兑），把水罐放回原处」；不加台词 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md |
| I60 | 主要 | 角色立场·Asellina·V6 动机 | s5_st14、s5_st7、s5_st13 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；st2 节拍 3–4 秒「把勺子横搁回那只罐口上」（前排中间），st14 开场勺却在「后排靠灶那只的罐口上」（首帧可见），之间无镜挪 | claude-opus-5-5/role_c4__a | 便宜：酒罐旁加一把专舀酒的小青铜勺（或陶舀），st14 直接取用，删「侧身探半步」；或至少让长柄勺从 st2 起一直在前排罐口，st14 开场写在原处、伸手即取；便宜：改成「把她摊在台面上的面包布角往里拢一拢」，或「拿抹布擦一擦手里的长柄勺」，再抬眼冲她笑；便宜（可选，交用户定）：倒鱼露前朝她那杯酒扬下巴、笑一下（「看在你买了好酒」）；核实：问用户是否需要这层生意人的交代 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md |
| I61 | 主要 | 角色立场·Fortunata·V1 语言 | s6_st1、s6_st5 | V1 语言 最终 1 分：我说的话（措辞、长短、语种、音量）面对此刻这个人合不合适；对方听不懂我的语言时，他能不能明白我要什么；我只伸手、不开价；人物卡写「先打量人再开价」；st2 的「三枚不够、手不收回」因此没有依据 | claude-opus-5-5/role_c5__a | 便宜：9.5s 伸手同时竖四指说 "Quattuor."，三枚小钱不够、她只好搭上大币，我照收不找零；拉丁文请核实；便宜：加 "Illic. Sursum."（6.2–7.0s），声音提示改成有对白；便宜：可保留；或请 Latin 考据确认街头叫法是否更口语（如 "Hospitium! Hic!"） | 便宜 | wontfix | Fortunata 要不要开价、开多少会改钱账，交用户定（见交付说明）（理由：Fortunata 要不要开价、开多少会改钱账，交用户定（见交付说明）） |
| I62 | 主要 | 角色立场·Fortunata·V3 表情 | s6_st1 | V3 表情 最终 1 分：我的表情和强度合不合此刻的处境；不过演、不面无表情；st1_first_frame 我侧头怒视左侧两名路人，眉压低、嘴紧抿，凶相；视频从首帧开始，这个表情会被带进招客的动作 | claude-opus-5-5/role_c5__a | 便宜：重出首帧，表情改成「眼睛扫街、脸平、带点招呼人的精神头」，或在 prompt 里写明「招客时脸是松的，不瞪人」 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I63 | 主要 | 角色立场·Fortunata·V5 回应 | s6_st2、s6_st1 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；节拍只写 Riley 摊手苦笑，没写我的回应，模型会让我定住或乱动 | claude-opus-5-5/role_c5__a | 便宜：加「Fortunata 瞥一眼她的空手，嘴角动一下、肩膀轻耸，侧头看向墙龛里的灯」，接 st5 0s；便宜：她比「睡」时我下巴一抬，她竖一指时我也竖一指，低声 "Una nox?"；便宜：加「低头瞄一眼大币、拇指拨一下」再攥（不占额外秒数） | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I64 | 主要 | 角色立场·Fortunata·V6 动机 | s6_st5、s6_st1 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；刚把门口唯一的灯给了客人，又转回天已黑的街上招客，这只是为下一场让道 | claude-opus-5-5/role_c5__a | 便宜：改成掂钱袋、点头，朝黑街扫最后一眼后转身进车门（或去拉门板），收工；便宜：改成目光从脸扫过衬衫、长裤、靴子，往她身后看一眼，最后停在攥着的拳头上，眉毛一挑 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s6_report.md |
| I65 | 主要 | 角色立场·路人与群众·V5 回应 | s4_st1、s1_st4、s8_st8 | V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；我是后面槽里的踩布工：门口一个外地女人张大嘴「清清楚楚地大声嚷」（spec 2.6–4.9 秒），院子是封闭的、只有踩水声，我不可能埋头 | claude-opus-5-5/role_extras__a | 便宜：3–3.5 秒两个工人被嚷声惊得**抬一下头**、脚不停；7.2–8 秒原来的反应拍改成「看见她捏着鼻子，互相看一眼咧嘴笑」，保持单独一拍；便宜：她偏头指鱼筐那一下（约 13 秒）之后，年轻渔夫抬眼看她一下、跟年长的对视一眼、耸一下肩又低头拢鱼（不说话、不看镜头、单独一拍放在 13–14 秒）；便宜：5–6 秒加年长妇女抬下巴指一下墙上的壁龛、摇头（不说话），Riley 会错意点头笑笑照样走进蒸汽；9–10 秒两人捂嘴笑保留。存疑：若故事有意让她穿衣进热水室作笑点，这一下比划正好把笑点交给观众 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s1_report.md、fixes/s4_report.md、fixes/s8_report.md |
| I66 | 主要 | 角色立场·路人与群众·V6 动机 | s5_st8、s8_st8 | V6 动机 最终 1 分：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数；我是那个店主：一辆不相干的驴车好好地直走，我凭什么扯嗓子喊它往右？车夫凭什么听我的？spec 第 10–11 行和 story.md | claude-opus-5-5/role_extras__a | 便宜：给车夫一个看得见的「问路/犹豫」——1–1.5 秒车夫在路口前放慢、左右张望（或回头冲店主扬一下下巴问），**此刻的我（店主）**才抬臂朝横街一指喊 "Dextram, dextram!"；车夫「抬手应一下」保留，变成道谢。或者让路口正前方堆着修路的石料/脚手架（呼应 s1_st3 地震补墙），店主喊是提醒「前面走不通」；便宜：5–6 秒加年长妇女抬下巴指一下墙上的壁龛、摇头（不说话），Riley 会错意点头笑笑照样走进蒸汽；9–10 秒两人捂嘴笑保留。存疑：若故事有意让她穿衣进热水室作笑点，这一下比划正好把笑点交给观众 | 便宜 | implemented | 按 r1 问题清单修复（follow-up 066，Claude 修复代理按场改、主会话合并）：分镜文字、overhead、首帧（_r8_before→_r8_candidate），逐条处理见 fixes/s5_report.md、fixes/s8_report.md |
| I67 | 待核实 | 人物逻辑·C1 | s7_st2 | C1：刻痕「看不出字形」，Riley 在 s3_st4、s8_st6 都表现完全不会拉丁语，却能指着其中一小片说「says Vibius Restitutus slept here alone」；观众会问她怎么读的 | claude-sonnet-5-5/character_B__a | 便宜：台词加一句交代，例如「there's a famous one — I swear this was in my textbook」，不暗示她在读这面墙；或改为她凭记忆「大概就是这种」。核实：看 story.md 里这句的来源。 | 便宜 | open |  |
| I68 | 待核实 | 人物逻辑·C1 · C2 | s8_st2 | C1 · C2：Riley 不知道票价，却「挑出最小的那枚」给门房；画面没有任何犹豫或试探，观众读不出她为什么挑最小的；s8_st10 的「one tiny coin」靠观众自己倒推 | claude-sonnet-5-5/character_B__a | 便宜：在 4–6 秒补一个 Riley 的小动作（先捏起最小的，看门房一眼，等她反应），让「试探」可读。 | 便宜 | open |  |
| I69 | 待核实 | 连续性·K1 拿灯的手 | s7_st6 | K1 拿灯的手：spec 写右手掌心托灯；首帧（z1.jpg 中）她背对镜头，举灯那条胳膊看起来是左臂。核实办法：出片前请 physics/角色审稿人放大核一下手和肩的对应关系 | claude-opus-5-5/continuity__a | 便宜：首帧重出时强调右手托灯 | 便宜 | open |  |
| I70 | 待核实 | 台词（时长与逻辑）·D3 | s8_st6 / s3_st4 | D3：“Dies nihil est. Dum versas te, nox fit.” 语法通（dum + 直陈式、nox fit），但属于编写句，没有可查出处；s3_st4 的 “ito”、“platea” 偏书面 | claude-sonnet-5-5/dialogue__a | 用拉丁语模型另核转写和发音（出片后）；若要更口语可改 “i” / “via”，但这是改拉丁语，不是为语速改句子，请用户定。存疑 | — | open |  |
| I71 | 待核实 | 时代与世界观·E6 史实 | s7_st2 | E6 史实：「Vibius Restitutus slept here alone…」出自 CIL IV 2146，r02 第 194 行记在 Eumachia 巷客栈（VII.12.35，市中心），片里在斯塔比亚门边的大车店。台词说的是「 | claude-opus-5-5/era__a | 便宜：台词改成「there's a famous one, in an inn just like this」之类，不说就在这面墙上；或在 story 里注明这是艺术处理 | 便宜 | open |  |
| I72 | 待核实 | 时代与世界观·E6 史实 | s8_st10 | E6 史实：「one tiny coin to get in」：r03 第 169、250 行写明 quadrans 是罗马城的价，庞贝实价和女区价没查到 | claude-opus-5-5/era__a | 便宜：维持现状，交付前复核来源；不行就改成「basically pocket change」 | 便宜 | open |  |
| I73 | 待核实 | 镜头规格·F4 节拍秒数 | s2_st1 | F4 节拍秒数：overhead path 0.5–1.5 s 走 2.4 m（2.4 m/s），1.5–2 s 走 1.61 m（3.2 m/s）。按每步 0.5 秒算，每步约 1.2–1.6 m，接近小跑或跳步；文字写的是「像平常人过马 | claude-opus-5-5/framing_A__a | 便宜：把 2 s 时的 path 点改到 (13.2,20.1)，2–3.5 s 再走出画；或把垫脚石间距标清楚 | 便宜 | open |  |
| I74 | 待核实 | 镜头规格·F6·F5 | s8_st3 → st8 | F6·F5：st3 画左妇女在 (0.7,7.4)、同伴在 (0.7,8.3)；st8 年长那位在 (0.75,8.2)、同伴在 (0.9,7.6)，座位前后对调；st3 靠里的第三位在 st8 里没了。核实方法：对两镜 overhead  | claude-opus-5-5/framing_B__a | 核对座位，统一（便宜） | 便宜 | open |  |
| I75 | 待核实 | 角色立场·路人与群众·V1 语言 | s5_st8 | V1 语言：我是店主，冲车夫喊方向时口语更像 "Ad dextram!" 或 "Dextrorsum!"；单说 "Dextram"（宾格、省略了 viam/partem）不太像随口喊的话。story.md 第 73 行 Felix 说的是  | claude-opus-5-5/role_extras__a | 便宜：请拉丁语审稿位核实；可改 "Ad dextram, ad dextram!"，dextram 照样听得清、Riley 的回收台词不用改 | 便宜 | open |  |
| I76 | 记录 | 世界物理·P6 距离 | s2_st4 | P6 距离：overhead 里 Riley x=13.45–13.55、Vibia x=14.3，两人身体之间只剩约 0.35 m，规格却写「一臂宽」「留着一人宽的空地」。首帧里 Riley 走在人行道中间，没贴路缘。 | claude-opus-5-5/physics_A__a | 便宜：Riley 路径 x 改到 13.3 上下，或把规格改成「侧身擦肩」；首帧可不重出。 | 便宜 | open |  |
| I77 | 记录 | 世界物理·P8 | s2_st1 | P8：规格写「右脚抬起、悬在第一块垫脚石上方」，首帧里前脚靴底已经贴着石头顶面。0–0.5 秒的第一步等于提前做完了，可能会被重复一遍。 | claude-opus-5-5/physics_A__a | 便宜：首帧可以照用，规格第 0 秒改成「右脚刚落上第一块石头」；或重出首帧，把脚抬高。 | 便宜 | open |  |
| I78 | 记录 | 世界物理·P10 | s1_st1 | P10：「快步走过来」，按 overhead 是 (38.18,51.9) 到 (38.05,56)，4.1 m 用 4.5 秒≈0.9 m/s，是慢走的速度。时长里加了台词，不算拉慢，但「快步」和实际时长对不上。 | claude-opus-5-5/physics_A__a | 便宜：把「快步」改成「边说边朝镜头走」，或把走近的时间压到约 3 秒。 | 便宜 | open |  |
| I79 | 记录 | 世界物理·P9 光影 | s1_st5 | P9 光影：规格写「画右这一侧的墙面和整个街面在柔和的阴影里」；首帧画右一排店面和路面都被照成暖金色。 | claude-opus-5-5/physics_A__a | 便宜：首帧调光或重出（不急）。 | 便宜 | open |  |
| I80 | 记录 | 世界物理·P3 交接（打结方式） | s3_st7 | P3 交接（打结方式）：「拎起布的四角在顶上打成一个结，留着两个长布角」说不通，四角同结会留四个角头；后面 8.5–11s 只用「两个长布角」系腰带 | claude-opus-5-5/physics_B__a | 便宜：改成「两对角先打一个结，另两个对角留长」 | 便宜 | open |  |
| I81 | 记录 | 世界物理·P10 速度（过快） | s3_st1 | P10 速度（过快）：两枚钱各走一个来回（约 0.65 m）共 1.3s；挪步、探身、拿面包、回身放下 1.4s。真人约各要 2s | claude-opus-5-5/physics_B__a | 便宜：拈钱改成「一把拢起两枚放进碗」，或者 11.7–13s 对视压到 0.6s，补给拿面包 | 便宜 | open |  |
| I82 | 记录 | 世界物理·P1 / P3 手 | s3_st1 | P1 / P3 手：只写了左手捏出、摊掌，没写由哪只手逐枚放下；单手从掌心逐枚放钱很别扭，模型可能多画一只手或让钱黏在掌心 | claude-opus-5-5/physics_B__a | 便宜：写明「右手从左掌心拈起，一枚一枚放下」 | 便宜 | open |  |
| I83 | 记录 | 世界物理·P4 支撑 | s3_st4 | P4 支撑：托板一头搁台沿、左手扶着呈斜面，右手把下层三个面包「一个个翻过来看底」，上层两个叠在上面，会滚落或变形 | claude-opus-5-5/physics_B__a | 便宜：改成「只拿起上层的面包翻看底、放回原处，拍掉面粉」 | 便宜 | open |  |
| I84 | 记录 | 世界物理·P9 效果来源（光） | s3_st2 | P9 效果来源（光）：炉口距 Riley 约 6.7 m，又在店里深处，清晨直射阳光下她脸上不会有可见的炉火橙光 | claude-opus-5-5/physics_B__a | 便宜：删掉「火光映到她脸上」，只留「面包表面微暖」或干脆不写 | 便宜 | open |  |
| I85 | 记录 | 世界物理·P9 影子 | s4_st4 | P9 影子：正午太阳高度约 69°，6 m 高房屋在东西向街上投影约 2.3 m，不是「一窄条」；南北向街才接近零 | claude-opus-5-5/physics_B__a | 便宜：写成「南北向的北街两侧几乎没有影子，横街里有一道短影」 | 便宜 | open |  |
| I86 | 记录 | 世界物理·P6 距离 | s8_st6 | P6 距离：st5 写「两人相隔不到一米」，st6 首帧 Riley 和 Helvia 中间隔着布包、油瓶、刮板，目测约 1.5m；镜头相接时 Helvia 像往外挪了 | claude-opus-5-5/physics_C__a | 便宜：首帧把 Helvia 往画左挪近，或接受 | 便宜 | open |  |
| I87 | 记录 | 世界物理·P2 道具状态（钱袋口） | s6_st2→s6_st5 | P2 道具状态（钱袋口）：s6_st2 F 用左手拉开袋颈绳结、撑开袋口，把钱放进去后抽出空手，没写扎回去；s6_st5 首帧钱袋是扎紧鼓着的，10–12 秒还要“掂一掂”。观众不一定注意，模型可能让钱袋一直敞着口，或者在镜头切换后突然扎好 | claude-opus-5-5/physics_D__a | 便宜：s6_st2 10–12.5 秒加一句“把绳一拉扎上”，或把节拍延到 13 秒 | 便宜 | open |  |
| I88 | 记录 | 世界物理·P10 真实速度／俯视图和 spec 对不上 | s6_st1 | P10 真实速度／俯视图和 spec 对不上：首帧按 32mm 估算，F 离镜头约 4.8 米，画右边缘离 F 约 3.4 米；R 3.8 秒从画右入画、5 秒停在 F 右边 1 米，1.2 秒要走约 2.4 米（每秒约 2 米，对一个“有 | claude-opus-5-5/physics_D__a | 便宜：入画时间改成约 3.0 秒（或者停下改到 5.5 秒）；俯视图里行人的终点改到 x≥8.6 | 便宜 | open |  |
| I89 | 记录 | 人物逻辑·C7 / C5 | s2_st4 | C7 / C5：s2_st8 她刚憋着笑回头瞟 Vibia，st4 却从 Vibia 一臂宽处走过，两人没有任何眼神或笑 | claude-sonnet-5-5/character_A__a | 便宜：加一个 Riley 抿嘴笑、对 Vibia 点一下头的小动作，Vibia 仍低头擦罐；仍从背影拍，不重出 | 便宜 | open |  |
| I90 | 记录 | 人物逻辑·C8 | s3_st4 | C8：「Garum?」后 Felix 没有反应，0.6 秒后直接开口，反应没钉在这个词上 | claude-sonnet-5-5/character_A__a | 便宜：Felix 听到 garum 眼皮一抬或手停半拍，再答；与问题 1 一起改 | 便宜 | open |  |
| I91 | 记录 | 人物逻辑·C6 | s4_st3 | C6：扛柴男人从举臂自拍、穿裤装的外国女人身边擦过，只「侧身让路」，不看她 | claude-sonnet-5-5/character_A__a | 便宜：加一个余光扫一眼再赶路，保持轻微（不要停步、不要回头） | 便宜 | open |  |
| I92 | 记录 | 人物逻辑·C7 · C2 | s5_st8 → s5_st9 | C7 · C2：st8 末 Riley 已「自己也朝画右指了一下」，st9 第 0 秒又「愣着、Wait」才恍然大悟，两处的领悟时点打架；st9 末「我一天都走错了」之后，st2 她直接走进熟食铺，没有任何往右看或转身的意思，观众不知道她为 | claude-sonnet-5-5/character_B__a | 便宜：st8 末改成「皱眉看着横街口，没动手」，指的动作留到 st9 恍然后；st9 末加一个往右看一眼再摇头的动作，交代「先吃饭」。 | 便宜 | open |  |
| I93 | 记录 | 人物逻辑·C8 | s5_st12 | C8：Asellina「放下手，抱起胳膊看着她对着空气说话，嘴角一扬」，约 4 秒没有手上的活，是个站桩 | claude-sonnet-5-5/character_B__a | 便宜：让她一边擦台面或数碗里的钱一边抬眼瞥一下，不要抱胳膊定住。 | 便宜 | open |  |
| I94 | 记录 | 人物逻辑·C1 | s8_st9 | C1：Helvia 听不懂英语，spec 却写「听到 rub oil all over yourself 时抬眼瞟她」；反应钉在她听不懂的词上 | claude-sonnet-5-5/character_B__a | 便宜：改成「看到她把油亮的小臂抬起来给镜头看时抬眼瞟她」，钉在手势上。 | 便宜 | open |  |
| I95 | 记录 | 连续性·K9 视角来源 | s5_st8 → s5_st9 | K9 视角来源：st8（他拍）最后一拍她右手指向画右、不说话；st9 第 0 秒已经是右臂伸直持镜的自拍，嘴还张着，处在同一个连续时刻，中间没有举起相机的动作，也没有时间跳跃 | claude-opus-5-5/continuity__a | 便宜：st9 0–0.5 s 加「她举起相机，画面晃上来」，或者 st8 结尾加一拍她抬手举相机 | 便宜 | open |  |
| I96 | 记录 | 连续性·K1 道具去向 | s5_st7 → s6 | K1 道具去向：s5_st7 写「面包布和剩下的面包留在台面上」，s6/s7 再没出现，等于把面包丢在了熟食铺；画面上不冲突，但故事里没交代 | claude-opus-5-5/continuity__a | 可选：s5_st7 结尾加一拍她把面包推给 Asellina 或包起来带走；不改也不会穿帮 | — | open |  |
| I97 | 记录 | 台词（时长与逻辑）·D7 | s5_st7→s6_st3 | D7：s5_st7 “Now I just have to find a bed.” 之后隔一场（傍晚），s6_st3 又说 “I still don’t have anywhere to sleep” ，信息重复 | claude-sonnet-5-5/dialogue__a | 不删台词；让 s6_st3 开头多一个她看天色、摸肚子的动作表示时间过了几小时，或把 s6_st3 说成 “…I still haven’t found anywhere to sleep” 以承接 “find a bed”。便宜，可存疑 | 便宜 | open |  |
| I98 | 记录 | 台词（时长与逻辑）·D7 | s1_st2→s1_st4 | D7：st2 末尾 “Yeah. This is it.” 是大声自嘲，st4 开口 “Okay, see those little guys?” 变成小声分享秘密，中间换景、换机位没有一句话或动作交代 | claude-sonnet-5-5/dialogue__a | 在 st4 的 12.5 秒开口前加一拍：Riley 压低身子、朝渔夫那边偏头再转向镜头，让音量变化有来由（节拍里已有 “微微探身”，加半句说明即可）。便宜 | 便宜 | open |  |
| I99 | 记录 | 台词（时长与逻辑）·D5（材料） | materials/junctions.md（工具） | D5（材料）：接点表把多人对话按 “/” 拆开后，Helvia、Felix、Asellina 的拉丁语被记在 Riley 名下（如 s8_st6→st7 写成 “Riley：Dum versas te, nox fit.”），会误导审稿人 | claude-sonnet-5-5/dialogue__a | 修 tools/shot_junctions.py 的台词拆分，按说话人切。便宜（改工具） | 便宜 | open |  |
| I100 | 记录 | 母语听感·N1 / N2 | s1_st1 | N1 / N2：「Like, real, two-thousand-years-ago Pompeii.」连字符堆叠，像小标题；还有「it worked. It actually worked.」前面已说过 Okay… | claude-sonnet-5-5/native_ear__a | 便宜。改成：「Oh my god. Okay — okay, it worked. It actually worked. That's Pompeii. That's, like, actual Pompeii. It's — it's actually there.」 | 便宜 | open |  |
| I101 | 记录 | 母语听感·N2 | s2_st2 | N2：「That's why they've got these big stepping stones, so you don't have to walk through… whatever's in there.」讲解腔，「you d | claude-sonnet-5-5/native_ear__a | 便宜。改成：「Okay, made it. So there's no sewer here — the street is the drain. That's what the stones are for. Yeah. I'm not walking through that.」 | 便宜 | open |  |
| I102 | 记录 | 母语听感·N2 | s1_st3 | N2：「See all these cracks? There was this huge earthquake here, like, twelve years ago — and they're still patching it up | claude-sonnet-5-5/native_ear__a | 便宜。改成：「Oh — look at these cracks. They're all patched. I think there was a huge earthquake here, like, a decade ago? And they're still fixing it.」 | 便宜 | open |  |
| I103 | 记录 | 母语听感·N2 | s5_st14 | N2：「everyone here waters their wine down」语序不顺（真人说 waters down their wine / waters it down）；「apparently」又出现一次 | claude-sonnet-5-5/native_ear__a | 便宜。改成：「Oh — she's putting water in it. Yeah, apparently everyone waters down their wine here. Drinking it straight is, like, a barbarian thing.」 | 便宜 | open |  |
| I104 | 记录 | 母语听感·N4 | s7_st3 / s7_st1 / s4_st5 | N4：Honestly 出现 3 次（s4_st5、s7_st1、s7_st3），basically 4 次，literally 4 次，「Yeah.」当收尾 4 次（s1_st2、s2_st8、s5_st14、s6_st3） | claude-sonnet-5-5/native_ear__a | 便宜。口头禅要分散：三处 Honestly 留一处，其余换成 Actually / I mean / Okay but；basically 留两处 | 便宜 | open |  |
| I105 | 记录 | 母语听感·— | s3_st4（已知） | —：面包房问路一段用户已指出，不展开 | claude-sonnet-5-5/native_ear__a | 待用户挑 | — | open |  |
| I106 | 记录 | 时代与世界观·E2 建筑 | s5_st9 | E2 建筑：画右屋檐下（约 x1240–1300,y190–240）有一截金属落水管加弯头（裁切图 s5st9_gutter.png），在背景虚化里看着像现代建筑配件 | claude-opus-5-5/era__a | 便宜：首帧修掉；负面词加「金属落水管、檐沟」 | 便宜 | open |  |
| I107 | 记录 | 时代与世界观·E3 服饰 | s8_st3、s8_st8 | E3 服饰：prompt 写「米白粗亚麻裹身长衣」，负面词也已有「翻领浴袍、毛巾布浴袍」，但首帧 s8_st3 两侧多位妇女是带翻领的厚毛巾布袍子，s8_st8 画左两位也像浴袍 | claude-opus-5-5/era__a | 便宜：重出首帧，把衣服写成「一整块薄亚麻布从腋下裹身、无领无袖口」 | 便宜 | open |  |
| I108 | 记录 | 时代与世界观·E3 发型胡须 | s5_st6、s5_st8、s5_st7 | E3 发型胡须：r05 第 35、193 行：75 年男人刮净胡子。s5_st6 画右喝酒的男人是一圈短须（prompt 写「短胡茬」）；s5_st8 门口店主留胡子；s5_st7 后景两名食客也有胡子，而 s5_st7 的 prompt  | claude-opus-5-5/era__a | 便宜：路人模板统一写「脸刮得干净」，s5_st6 把「短胡茬」改成「刮得干净、下巴青」；首帧修掉胡须 | 便宜 | open |  |
| I109 | 记录 | 时代与世界观·E1 器物 | s6_st4 | E1 器物：p1 卡写「嘴上燃着一小朵黄色火苗」，首帧（裁切图 s6st4_lamp.png）火苗却从灯身尾部冒出，前端的灯嘴空着，看着像碟形烛台 | claude-opus-5-5/era__a | 便宜：首帧重出，火苗放在灯嘴 | 便宜 | open |  |
| I110 | 记录 | 时代与世界观·E1 器物 | s4_st5 | E1 器物：放大看，Riley 举起的铜币人像是长发、编辫、戴月桂冠的少年侧像，不像 75 年 as 币上的维斯帕先（秃顶、宽脸）；没有可读字母 | claude-opus-5-5/era__a | 便宜：首帧重出，人像写成「秃顶、宽下巴的老年男人侧像，浮雕模糊」 | 便宜 | open |  |
| I111 | 记录 | 时代与世界观·E2 建筑 | s3_st2、s4_st4 | E2 建筑：s3_st2 背景门框带线脚和檐口，像后世的意大利或殖民地小镇；s4_st4 路口四角是独立的坡顶小屋，庞贝街区应是连续临街墙面 | claude-opus-5-5/era__a | 便宜：要重出这两张首帧时，顺带把门框改成素面凝灰岩框，路口两侧改成连续店面墙 | 便宜 | open |  |
| I112 | 记录 | 时代与世界观·— | s3（面包房问路一段） | —：已知问题（BRIEF 已列，用户已指出），这一类没有新增 | claude-opus-5-5/era__a | — | — | open |  |
| I113 | 记录 | 镜头规格·F6 轴线（水流方向） | s2_st3 / s2_st1 | F6 轴线（水流方向）：s2_st1 的 prompt 第 10 行写水「从画面深处的上坡往镜头这边流」，机位朝北，等于水往南流；s2_st3 机位朝东、画左是北，文字却写水「从画右往画左顺着街流」，等于往北流（上坡）。这两镜在播放时相邻， | claude-opus-5-5/framing_A__a | 便宜：把 s2_st3 改成「从画左往画右（往南、下坡）流」，或统一改 st1；驴车方向可以不动 | 便宜 | open |  |
| I114 | 记录 | 镜头规格·F6 左右关系 | s2_st8→s2_st4 | F6 左右关系：两镜都朝南拍。st8 里 Riley 在 x=15、Vibia 在 x=14.3，Vibia 在画右，首帧也是 Riley 居中偏左、Vibia 在画右；st4 第 0 秒 Riley 已经到了 x=13.55（路缘），Vi | claude-opus-5-5/framing_A__a | 便宜：st4 开头加半拍「Riley 从 Vibia 身后绕到路缘一侧」，或接受为剪接省略，在剪辑时确认 | 便宜 | open |  |
| I115 | 记录 | 镜头规格·F3 画面位置 | s2_st8 | F3 画面位置：文字和 overhead（出水口 x@0=-0.08）写的是「牛头出水口和石槽在她正后方，大半被她的头和肩挡住」；首帧里牛头出水口在画面 0.24 处、Riley 右肩后完整露出，水柱看得清 | claude-opus-5-5/framing_A__a | 便宜：把文字改成「出水口在她右肩后（画左）露出」，和首帧一致 | 便宜 | open |  |
| I116 | 记录 | 镜头规格·F3 画面位置（后景） | s3_st1 / s3_st6（及 st4/st7） | F3 画面位置（后景）：按 bg3 平面图：东磨约 (7.0,1.8)，砖炉约 (11.0,1.5)。s3_st1 机位下砖炉应在约 0.37 处、东磨贴画左缘；首帧里炉在 0.6、东磨在 0.44。s3_st6 用 50mm，砖炉偏离镜轴 | claude-opus-5-5/framing_A__a | 便宜：接受首帧布局，就改 bg3 平面图与 s3_st5 的摇角说明；或把 s3_st6 文字改成只有石磨、炉火只映出红光 | 便宜 | open |  |
| I117 | 记录 | 镜头规格·F4 节拍秒数 / F3 | s1_st3 | F4 节拍秒数 / F3：镜头 0–6.5 s 以 1.11 m/s 前移，工人固定在 (32.6,19.25)，偏轴角到约 4.75 s 就超过半视角 32.7°。文字写的 4.8–5.6 s「点头回礼、转身」会发生在画右边缘外，3–4  | claude-opus-5-5/framing_A__a | 便宜：把打招呼和回礼提前约 0.8 s（3.2–4.8 s），或把工人位置写近镜轴 0.5 m | 便宜 | open |  |
| I118 | 记录 | 镜头规格·F4 节拍秒数 | s1_st1 | F4 节拍秒数：文字写「快步走过来」，path 是 3 s 走 2.7 m（0.9 m/s），比普通步速还慢；对白 2.1 s，节拍并不挤 | claude-opus-5-5/framing_A__a | 便宜：把「快步」改成「笑着走过来」，或把 path 压到 2 s 走完 | 便宜 | open |  |
| I119 | 记录 | 镜头规格·F2 | s5_st2 / st12 / st4 | F2：站位图上 Riley 面朝与看镜头方向夹角 88°（st2/st12）、76°（st4），是侧脸；文字写「四分之三侧脸」；st2/st12 首帧是侧脸，st4 首帧画面放大 27%、头顶被裁 | claude-opus-5-5/framing_B__a | 文字改成「侧脸」，或把朝向往镜头转约 30°（便宜） | 便宜 | open |  |
| I120 | 记录 | 镜头规格·F5 | s5_st6 → st5 → st7 | F5：st6 站在柜台东头外侧 (8.8,5.4) 的两个食客，到 st5（u≈0.79）、st7（u≈0.91）都不在；st7 另有两个男人坐在店里，overhead 却放在短边外 (10.1,3.2) | claude-opus-5-5/framing_B__a | 统一成同一对人：st7 的 overhead 把两人挪进店里，或交代 st6 那两人已离开（便宜） | 便宜 | open |  |
| I121 | 记录 | 镜头规格·F5 | s8_st3 | F5：overhead 只放了 7 个妇女里的 3 个，文字和首帧是 7 个 | claude-opus-5-5/framing_B__a | 补齐 7 个点位（便宜） | 便宜 | open |  |
| I122 | 记录 | Prompt 文本·T6 参考清单 | s4_st2、s4_st5、s5_st1/9/11、s8_st4、s6_st3、s7_st5、s3_st6 | T6 参考清单：正文写了布包、陶油灯、收钱碗，参考里没挂 p3/p1/p2。布包在画框下缘外，影响小；s6_st3 的壁龛小油灯和 s7_st5 路人的小陶灯只是远景。 | claude-sonnet-5-5/prompt_text__a | 便宜：布包出现在下缘外时可以不挂，但正文别写「从布包后面伸手」。要在画内露出的道具，补挂对应 p 参考。 | 便宜 | open |  |
| I123 | 记录 | 角色立场·Riley·V3 | s8_st4 | V3：首帧放大看：眼睛半闭、嘴唇微张、头微仰，表情慵懒、近乎性感，不是「又热又尴尬」 | claude-opus-5-5/role_c1__a | 此刻的我：热得眯眼皱眉、鼓腮吐气，额头冒汗，有点狼狈。重出首帧（便宜） | 便宜 | open |  |
| I124 | 记录 | 角色立场·Tertius·V3 表情 | s4_st1 | V3 表情：人物卡外观「眉头总是皱着，神情不耐烦」，再写「皱眉」无增量；我在画左约 1/4 处、中全景，脸小 | claude-opus-5-5/role_c3__a | 此刻的我会：停下脚、眉头拧紧、嘴角往下一撇、下巴一抬——靠停脚和转身这些大动作让观众读出「被惹毛了」，不要求脸部特写式表演。**便宜** | 便宜 | open |  |
| I125 | 记录 | 角色立场·Asellina·V3 表情／V7 | s5_st14 | V3 表情／V7：「只抬眼瞥了她一下，不笑」；人物卡「嘴角常带着做生意的笑」，前后镜都在笑 | claude-opus-5-5/role_c4__a | 便宜：改「低头擦台面，嘴角还挂着一点笑，抬眼瞥她一下，摇摇头接着擦」 | 便宜 | open |  |
| I126 | 记录 | 角色立场·Asellina·V4 视线 | s5_st12 | V4 视线：「抱起胳膊看着她对空气说话……不看镜头」：她第一次对空街说话，我没有顺她目光找人这一下 | claude-opus-5-5/role_c4__a | 便宜：加「她转脸那一下，Asellina 顺着她的方向朝她身后的街面（画右深处，不朝镜头）瞟一眼，没人，再看回她，嘴角一扬」；prompt 里保留「不看镜头」 | 便宜 | open |  |
| I127 | 记录 | 角色立场·Asellina·V3 表情 | s5_st2 / s5_st10 | V3 表情：17 秒内三次「挑眉」 | claude-opus-5-5/role_c4__a | 便宜：删 st10 第 5.5–8 秒的「又挑眉」，改「看回画右，笑着等她」 | 便宜 | open |  |
| I128 | 记录 | 角色立场·Asellina·V1 语言 | s5_st2 | V1 语言：「响亮利落」，两人「相距一米多」（走位）；她盯的是冒热气的罐，我报的是酒价 | claude-opus-5-5/role_c4__a | 便宜：音量改「利落带笑、招呼客人的嗓门」；3–4 秒放勺时「用勺柄点一下两人中间的空陶杯」再竖手指 | 便宜 | open |  |
| I129 | 记录 | 角色立场·Asellina·V1 语言 | s5_st13 | V1 语言：「只喊一声 Euge!」，对一米外的人 | claude-opus-5-5/role_c4__a | 便宜：「喊」改「笑着脱口一声」 | 便宜 | open |  |
| I130 | 记录 | 角色立场·Asellina·V4 视线 | s5_st3 | V4 视线：Asellina 在这 4 秒无视线描写，0 秒只写「看着她」 | claude-opus-5-5/role_c4__a | 便宜：加「Asellina 的眼睛跟着她的手：看一眼她手心，再看两枚钱落到台面」 | 便宜 | open |  |
| I131 | 记录 | 角色立场·Asellina·V3 表情 | s5_st12 | V3 表情：st12_first_frame.png 画左 Asellina 眉头紧皱、像怀疑不悦，规格是「愣着」 | claude-opus-5-5/role_c4__a | 便宜：首帧重出或 prompt 写「微微一怔，眉头略抬，不皱眉」 | 便宜 | open |  |
| I132 | 记录 | 角色立场·Fortunata·V7 | s6_st5 | V7：人物卡依据写「先收钱再领路」，分镜只指路不领路 | claude-opus-5-5/role_c5__a | 便宜：二选一，统一人物卡或分镜；只指不领也说得通，改卡更省 | 便宜 | open |  |
| I133 | 记录 | 角色立场·Vibia·V4 视线（第一眼看什么） | s2_st5 | V4 视线（第一眼看什么）：对 75 年的庞贝主妇，成年女人散着长发、露着胳膊上街和裤子一样扎眼（同场 st4 的女孩就盯着她的长发）；spec 只写脸→腿；story.md 第 53 行原写「裤子和靴子」，spec 只剩腿 | claude-opus-5-5/role_c6__a | 便宜（可选）：「先看脸，目光在散着的长发上停一下，再落到腿和靴子上」 | 便宜 | open |  |
| I134 | 记录 | 角色立场·Helvia·V1 语言 | s8_st5 | V1 语言：人物卡个性「热心、爱拿老话劝人」，st5 14 秒全程无声 | claude-opus-5-5/role_c7__a | 便宜：5–10 秒倒油时加一声非词语的「嗯——」并朝她点头示意抹开；若要出词须由考据给短词（bible 第 14 行），存疑待考据 | 便宜 | open |  |
| I135 | 记录 | 角色立场·Helvia·V4/V6 视线·动机 | s8_st9 | V4/V6 视线·动机：「听到 rub oil all over yourself 时抬眼瞟她一下」——我听不懂英语 | claude-opus-5-5/role_c7__a | 便宜：改「看到她把油亮的小臂举向空处时，抬眼瞟她一下、顺着她的目光往她面前空处瞟一眼，再看回她憋着笑」（不看镜头） | 便宜 | open |  |
| I136 | 记录 | 角色立场·Helvia·V3 表情 | s8_st5 | V3 表情：`st5_first_frame.png` 画右我第 0 秒已咧嘴笑，与「专心刮自己的胳膊」及 2.5 秒「嘴角一抽笑一下」冲突 | claude-opus-5-5/role_c7__a | 便宜：首帧改为专注平常脸、视线落在自己左臂，或 spec 写明 0–2.5 秒神情平静 | 便宜 | open |  |
| I137 | 记录 | 角色立场·Helvia·V3 表情 | s8_st6 | V3 表情：4.4–5.1 秒已「耸耸肩」，台词括注又写「笑着耸肩」，可能 5.1–9 秒再耸一次 | claude-opus-5-5/role_c7__a | 便宜：台词括注删「耸肩」，只留「带笑」；说话时手上只有 versas 一翻 | 便宜 | open |  |
| I138 | 记录 | 角色立场·路人与群众·V3 表情 | s8_st10 | V3 表情：我是门房：天天坐门口收钱，一个外地女人站在我面前对空气小声嘀咕两句，我会好笑，但「摇头笑出了声」偏大；9.5–11 秒又「嘴角一撇」，从笑到撇嘴中间没有任何事发生 | claude-opus-5-5/role_extras__a | 便宜：6.5–8 秒改成「鼻子里哼一声笑、摇摇头」，右手往厅里一挥；9.5–11 秒改成「还带着笑摇摇头，转回去看门外」，去掉撇嘴 | 便宜 | open |  |
| I139 | 记录 | 角色立场·路人与群众·V7 集内一致 | s5_st6→s5_st7 | V7 集内一致：st6 两个干完活的男人「站在柜台外侧、东头拐角前的台沿边」吃（首帧也是站在柜台外）；中间隔 st4、st5，st7 变成「灶台那头的店里，远远坐着两个低头吃喝的男人」（首帧坐在灶后店里）。同样的粗布 tunica、同样两人 | claude-opus-5-5/role_extras__a | 便宜：st7 背景改成 st6 那两人仍站在柜台东头台沿边吃（虚化），或在 st7 写明是另外两人、换衣色 | 便宜 | open |  |
| I140 | 记录 | 角色立场·路人与群众·V7 / 规则源 | s8_st2 / s8_st10 / s5_st8 | V7 / 规则源：bible.md 第 40 行「在两个以上镜头里出现、或要开口说话、或要和 Riley 有互动的人立人物卡」；浴场门房出现两镜并收钱互动、喊路店主开口说话，spec 却写「不立卡的配角」，于是没有 behavior.md  | claude-opus-5-5/role_extras__a | 便宜：给门房、喊路店主补最小人物卡（外观＋一两条行为：门房「话少、收钱利落、对怪人好笑不刁难」），或在 bible 写明「无名配角」例外 | 便宜 | open |  |
| I141 | 记录 | 角色立场·路人与群众·V4 视线 | s4_st3 | V4 视线：我是扛柴的：迎面走来一个高个外地女人，右臂伸得笔直、对着手大声说话，我侧身挪柴给她让路——让路时一定先看她一眼（看她伸着的胳膊别碰着我的柴）。spec 只写让路，没写看 | claude-opus-5-5/role_extras__a | 便宜：「侧身让路时斜眼看一下她伸着的右臂和她的脸，接着走」 | 便宜 | open |  |
| I142 | 记录 | 角色立场·路人与群众·V4 视线 / V2 肢体 | s3_st8 | V4 视线 / V2 肢体：我是那位母亲：儿子拽我袖子、拿手指着一个陌生女人的脚，我会顺着看一眼，然后按下他的手（指着人不礼貌）拉他走；spec 写「眼睛看着前面的路」，对儿子的拽和指毫无察觉 | claude-opus-5-5/role_extras__a | 便宜：「母亲顺着看一眼她的短靴，按下孩子指人的手，拉着他走」 | 便宜 | open |  |
| I143 | 记录 | 角色立场·路人与群众·V4 视线 | s8_st2 | V4 视线：我是门房：外地女人当着我的面摊开一手心钱慢慢挑，我的眼睛会落在钱上（还会多看一眼那枚大黄铜币），spec 这两拍没写我看哪里，模型可能让我盯镜头或发呆 | claude-opus-5-5/role_extras__a | 便宜：4–6 秒补「门房低头看她手心里的钱」 | 便宜 | open |  |

## 证据

### I1 严重 · 世界物理 · P2 道具来源与去向
- a（1 分）：s1_st2 规格写摊开后「靠指根一排 = 大黄铜币 + 浅色小铜币，下面两排 = 4 + 3 枚 as」；同一镜挂的 p6_掌心九枚钱 参考图却是 3/3/3 排、大币和小铜币在靠手腕那排。两边打架，而且从攥着的拳头直接摊开、9 枚就整齐排成三排，也做不到。另外 s1_st1 相机「架在沙滩上」，架子是什么、后来去哪了都没写。
- 规格要求「靠指根一排 = 大币 + 小铜币，下面 4 + 3 枚 as」；同镜挂的 p6 参考图是 3/3/3 排、大币在靠手腕那排，两边打架。as 直径约 25mm，4 枚一排约 100mm，比手掌宽（约 80mm），放不下就会叠起来或伸出掌外。从攥紧的拳头直接摊开、9 枚就规整排好，物理上做不到，模型多半会生出、吞掉或变形几枚（p6 卡里记着「手心只有 6 枚」已经出过两次）。
- 相机「架在沙滩上」，overhead 机高 1.5 m，说明有个架子。st1 结尾她单手「把这台相机拿了起来」，架子是什么、怎么取下、后来放哪，全集都没交代。st2 开头 0 秒左拳里已经攥着 9 枚钱，st1 结尾她左手还空着、钱在裤袋里，掏钱这一下在镜头外。
- overhead.toml 的注释和 meta.note（渲染在 st4_overhead.png 顶部）还写着「首帧船头系着两根绳」「两个渔夫各攥一根」「两人各抓一只提耳」；规格和 prompt 写的是「只系一根绳、四只手在一根绳上」「各用双手抓提耳」。送模型的 overhead_ref 不带这段字，所以只是给人看的旧文字，但审稿人和续跑的人会被带偏。
- 分数：a 1 / b None → 最终 1
  | s1_st2 | 20.5–28.5 秒 | P2 道具 / P4 | 重出 | ② 分镜文字 + ③ 参考图 | 规格要求「靠指根一排 = 大币 + 小铜币，下面 4 + 3 枚 as」；同镜挂的 p6 参考图是 3/3/3 排、大币在靠手腕那排，两边打架。as 直径约 25mm，4 枚一排约 100mm，比手掌宽（约 80mm），放不下就会叠起来或伸出掌外。从攥紧的拳头直接摊开、9 枚就规整排好，物理上做不到，模型多半会生出、吞掉或变形几枚（p6 卡里记着「手心只有 6 枚」已经出过两次）。 | 便宜：规格改成和 p6 一致的 3/3/3 排法；把「攥拳 → 摊开即成排」改成拳头举到镜头前时已经是虚握的平掌，或者先摊开再停半拍（镜头切到已摊平的状态）。 |
  | s1_st1 → s1_st2 | st1 0–22 秒 | P2 道具来源与去向 | 记录 | ② 分镜文字 | 相机「架在沙滩上」，overhead 机高 1.5 m，说明有个架子。st1 结尾她单手「把这台相机拿了起来」，架子是什么、怎么取下、后来放哪，全集都没交代。st2 开头 0 秒左拳里已经攥着 9 枚钱，st1 结尾她左手还空着、钱在裤袋里，掏钱这一下在镜头外。 | 便宜：写明是插在沙里的轻便自拍杆 / 三脚架，st1 结尾她连杆一起拔起来；st2 开头写「刚从左裤袋把钱攥在拳里」。 |
  | s1_st4 | 0–8 秒（overhead.toml） | P2 / P3（文档） | 记录 | ② 分镜文字 | overhead.toml 的注释和 meta.note（渲染在 st4_overhead.png 顶部）还写着「首帧船头系着两根绳」「两个渔夫各攥一根」「两人各抓一只提耳」；规格和 prompt 写的是「只系一根绳、四只手在一根绳上」「各用双手抓提耳」。送模型的 overhead_ref 不带这段字，所以只是给人看的旧文字，但审稿人和续跑的人会被带偏。 | 便宜：改 overhead.toml 的注释和 note，重生成 overhead 图。 |

### I2 严重 · 世界物理 · P4 重力与支撑
- a（1 分）：同一条街的水前后对不上。s2_st1、st3、st2 写满街 3–4 厘米深的浑水；s2_st5、st8、st4 的规格和 prompt 只有「被流水打湿发亮」「路面的流水反光」，三张首帧（st5 右半、st8 右半、st4 右下垫脚石周围）也都只是湿石板。流向也矛盾：s2_st1 写由北往南流（镜头 (8.9,22.4) 朝北），s2_st3 写「从画右往画左」，即由南往北。另外 s1_st2 一排放 4 枚 as：4×25mm=100mm，比手掌宽（约 80mm）。
- s2_st1、st3、st2 写满街 3–4cm 浑水；st5、st8、st4 的规格和 prompt 只写「被流水打湿发亮」「路面的流水反光」。bg2 场景卡第 19、30 行写的还是「一道浅浅的清水沿着路面低处流下来」。三张首帧都只有湿石板，st4 右下那块垫脚石周围也没有水。照这样出片，就是 058 里用户说的「只有湿路面」在同一场后半段又出现一次。
- st1 镜头在 (8.9,22.4) 朝北偏东，水「从画面深处的上坡往镜头这边流」，即由北往南；st3 镜头在 (8.8,16) 朝东，画右是南，水「从画右往画左」流，即由南往北。剪在一起水往两个方向流，st3 结尾「浑水照常往画左流」又写死了。
- 规格要求「靠指根一排 = 大币 + 小铜币，下面 4 + 3 枚 as」；同镜挂的 p6 参考图是 3/3/3 排、大币在靠手腕那排，两边打架。as 直径约 25mm，4 枚一排约 100mm，比手掌宽（约 80mm），放不下就会叠起来或伸出掌外。从攥紧的拳头直接摊开、9 枚就规整排好，物理上做不到，模型多半会生出、吞掉或变形几枚（p6 卡里记着「手心只有 6 枚」已经出过两次）。
- 分数：a 1 / b None → 最终 1
  | s2_st5、s2_st8、s2_st4（规则源 bg2 场景卡） | 全镜 | P4 液体 / P9 | 重出 | 规则源 + ② 分镜文字 + ③ 首帧 | s2_st1、st3、st2 写满街 3–4cm 浑水；st5、st8、st4 的规格和 prompt 只写「被流水打湿发亮」「路面的流水反光」。bg2 场景卡第 19、30 行写的还是「一道浅浅的清水沿着路面低处流下来」。三张首帧都只有湿石板，st4 右下那块垫脚石周围也没有水。照这样出片，就是 058 里用户说的「只有湿路面」在同一场后半段又出现一次。 | 便宜：bg2 场景卡改成「满街浑水 3–4cm、绕过垫脚石」；st5、st8、st4 的画面 / 光线行补上满街流动的浑水；三张首帧重出（st4 右下垫脚石周围要有水绕流）。 |
  | s2_st1 ↔ s2_st3 | st1 全镜 / st3 0–8 秒 | P4 液体方向 | 重出 | ② 分镜文字 | st1 镜头在 (8.9,22.4) 朝北偏东，水「从画面深处的上坡往镜头这边流」，即由北往南；st3 镜头在 (8.8,16) 朝东，画右是南，水「从画右往画左」流，即由南往北。剪在一起水往两个方向流，st3 结尾「浑水照常往画左流」又写死了。 | 便宜：统一成由北（上坡）往南流（庞贝北高南低）；st3 改成「从画左往画右流」，接点表 st3 结尾跟着改。 |
  | s1_st2 | 20.5–28.5 秒 | P2 道具 / P4 | 重出 | ② 分镜文字 + ③ 参考图 | 规格要求「靠指根一排 = 大币 + 小铜币，下面 4 + 3 枚 as」；同镜挂的 p6 参考图是 3/3/3 排、大币在靠手腕那排，两边打架。as 直径约 25mm，4 枚一排约 100mm，比手掌宽（约 80mm），放不下就会叠起来或伸出掌外。从攥紧的拳头直接摊开、9 枚就规整排好，物理上做不到，模型多半会生出、吞掉或变形几枚（p6 卡里记着「手心只有 6 枚」已经出过两次）。 | 便宜：规格改成和 p6 一致的 3/3/3 排法；把「攥拳 → 摊开即成排」改成拳头举到镜头前时已经是虚握的平掌，或者先摊开再停半拍（镜头切到已摊平的状态）。 |

### I3 严重 · 世界物理 · P5 身体可行
- a（1 分）：s4_st1 8–8.8s「上身往左一拧、从左肩回头瞥一眼 Tertius」。按俯视图，Riley 在 (7.6,7.2)、Tertius 在 (5,6.2)，她转过来面朝机位 (9,8.7) 后，Tertius 在她右后方约 156°，从左肩回头要转约 204°，真人做不到。其余动作如 s4_st4 原地转小半圈、s3_st8 转身迈步都可行
- 俯视图里 Tertius 在 Riley 左前方（面朝院子时），她转身面朝机位后 Tertius 到了她右后方约 156°；文字写「上身往左一拧、从左肩回头」，要转约 204°，模型只会做成扭曲转头，或者看向后排工人（画右）
- 左前臂压着包，两手把两个布角绕过已经系在身上的腰带、打结、拉紧，只给 2.5s，真人要 4–5s，模型容易让手和布融在一起
- 分数：a 1 / b None → 最终 1
  | s4_st1 | 8–8.8s | P5 身体可行（回头方向） | 重出 | ② 分镜文字 | 俯视图里 Tertius 在 Riley 左前方（面朝院子时），她转身面朝机位后 Tertius 到了她右后方约 156°；文字写「上身往左一拧、从左肩回头」，要转约 204°，模型只会做成扭曲转头，或者看向后排工人（画右） | 便宜：改成「上身往右一拧、从右肩回头瞥一眼 Tertius」；顺带核对 prompt.txt 和 overhead.toml 里的同一句 |
  | s3_st7 | 8.5–11s | P5 时长 / P10 | 记录 | ② 分镜文字 | 左前臂压着包，两手把两个布角绕过已经系在身上的腰带、打结、拉紧，只给 2.5s，真人要 4–5s，模型容易让手和布融在一起 | 便宜：动作简化成「把两个布角在腰带上打一个活结」，或把 11–13s 的拍拍布包压短，挪出 1–1.5s |

### I4 严重 · 世界物理 · P2 道具来源与去向
- a（1 分）：s5 长柄勺 st2 结尾横搁前排中间罐口 → st12/st3 首帧台面上没有勺 → st14 第 0 秒在「后排靠灶」罐口；s5_st3 首帧手心只有 5 枚（4 红铜+1 黄铜，裁切图 s5_st3_coins.jpg），文字要 6 枚；s5_st6 两个男人站在柜台东头外吃饭，s5_st7 变成坐在灶台那头店里（见问题表）
- spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/physics_C__a/s5_st3_coins.jpg）。模型要么跳过「摊开」这一拍，要么让钱从拳里凭空变出来；之后拿走 2 枚剩 3 枚，和「塞回 4 枚」对不上
- st2 勺「横搁回」前排中间罐口；st12、st3 台面清单都不写勺，首帧前排罐口上也空着；st14 第 0 秒勺在「后排靠灶」罐口，这只后排罐也是 st14 才第一次写进清单。勺在两镜之间消失又换了位置
- st6 两个男人站在柜台东头外侧、台沿前吃饭，旁边有小孩和妇女；st7 变成「灶台那头的店里，远远坐着两个男人」（首帧也是坐在店里）。紧挨着的 st13/st14 首帧柜台东头和店里都没人，st6 却是正吃到一半
- Asellina 右手刚从罐口拿起勺回敬（3–4s），又用勺搅罐（5–10.9s），10.9–14s「拿起碗旁抹布擦酒渍」，没写勺放回哪里，模型容易让她一手握勺一手擦，或者勺凭空消失；酒渍是哪来的也没交代
- 灰白抹布 st14 第 0 秒「叠在小陶碗旁」，紧挨着的上一镜 st3 台面清单和首帧都没有抹布（st3 首帧碗旁空着）
- 大蒜铺门口 st8 写一只藤筐（首帧一只），st9 首帧画了两只；st9 光线写画右（街南）在阴影里，首帧画右那排铺面和人行道亮着，阴影落在街中间偏左
- 分数：a 1 / b None → 最终 1
  | s5_st3 | 0–3.5s | P8 首帧=第0秒 / P2 数量 | 重出 | ③ 首帧 | spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/physics_C__a/s5_st3_coins.jpg）。模型要么跳过「摊开」这一拍，要么让钱从拳里凭空变出来；之后拿走 2 枚剩 3 枚，和「塞回 4 枚」对不上 | 便宜：重出首帧，右手握拳伸在台面上方、看不到钱；或者把第一拍改成「已摊开、6 枚」并删掉握拳一拍 |
  | s5_st2→st12→st3→st14 | st2 3–4s；st14 0s | P2 道具来源与去向 | 记录 | ② 分镜文字 / ③ 首帧 | st2 勺「横搁回」前排中间罐口；st12、st3 台面清单都不写勺，首帧前排罐口上也空着；st14 第 0 秒勺在「后排靠灶」罐口，这只后排罐也是 st14 才第一次写进清单。勺在两镜之间消失又换了位置 | 便宜：st2 改成把勺搁到后排靠灶罐口（或 st14 开头仍在前排、删掉「探半步取勺」）；st12/st3 清单和首帧补上勺 |
  | s5_st6→st7 | st6 0–8s；st7 0s | P2 / P5 人物凭空出现、瞬移 | 记录 | ② 分镜文字 | st6 两个男人站在柜台东头外侧、台沿前吃饭，旁边有小孩和妇女；st7 变成「灶台那头的店里，远远坐着两个男人」（首帧也是坐在店里）。紧挨着的 st13/st14 首帧柜台东头和店里都没人，st6 却是正吃到一半 | 便宜：st7 改成两人仍站在东头台沿前；或者 st6 改成店里坐着吃 |
  | s5_st7 | 3–14s | P1 手数 / P2 去向 | 记录 | ② 分镜文字 | Asellina 右手刚从罐口拿起勺回敬（3–4s），又用勺搅罐（5–10.9s），10.9–14s「拿起碗旁抹布擦酒渍」，没写勺放回哪里，模型容易让她一手握勺一手擦，或者勺凭空消失；酒渍是哪来的也没交代 | 便宜：加一句「把勺横搁回中间罐口，右手拿起抹布」；酒渍改成「擦一擦杯底下」，或交代 Riley 举杯时洒出几滴 |
  | s5_st3→st14 | st14 0s | P2 道具凭空出现 | 记录 | ② 分镜文字 | 灰白抹布 st14 第 0 秒「叠在小陶碗旁」，紧挨着的上一镜 st3 台面清单和首帧都没有抹布（st3 首帧碗旁空着） | 便宜：st2/st12/st3 清单补「碗旁叠着抹布」，首帧补画 |
  | s5_st8→st9 | st9 0s | P2 数量 / P9 光影 | 记录 | ③ 首帧 | 大蒜铺门口 st8 写一只藤筐（首帧一只），st9 首帧画了两只；st9 光线写画右（街南）在阴影里，首帧画右那排铺面和人行道亮着，阴影落在街中间偏左 | 便宜：st9 重出首帧，改成一只筐、画右半边街在阴影里 |

### I5 严重 · 世界物理 · P8 首帧 = 第 0 秒
- a（1 分）：s5_st3 第 0 秒写右手「攥成拳」、钱在拳头里，首帧已经摊开手心、钱露着，等于把 1.5–3.5s 的状态当成了首帧（见问题表）；s8_st2、s5_st2 首帧把「正迈步」画成站定（小瑕疵，见问题表）；其余镜头首帧和第一拍对得上，比如 s8_st5 刮板在左上臂、s5_st14 勺在后排罐口、抹布叠在碗旁、s5_st13 两手搭台面低头看布包
- spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/physics_C__a/s5_st3_coins.jpg）。模型要么跳过「摊开」这一拍，要么让钱从拳里凭空变出来；之后拿走 2 枚剩 3 枚，和「塞回 4 枚」对不上
- 两镜第 0 秒都写「正迈步走向」门房或柜台，首帧都是站定不动；s5_st2 首帧里 Riley 已经站在柜台边，0–2s 走的那一两步没有起点
- 分数：a 1 / b None → 最终 1
  | s5_st3 | 0–3.5s | P8 首帧=第0秒 / P2 数量 | 重出 | ③ 首帧 | spec 第 0 秒右手握拳、钱在拳里，1.5–3.5s 才摊开 6 枚；首帧已经摊开手心，放大后只有 4 红铜+1 黄铜共 5 枚（work/physics_C__a/s5_st3_coins.jpg）。模型要么跳过「摊开」这一拍，要么让钱从拳里凭空变出来；之后拿走 2 枚剩 3 枚，和「塞回 4 枚」对不上 | 便宜：重出首帧，右手握拳伸在台面上方、看不到钱；或者把第一拍改成「已摊开、6 枚」并删掉握拳一拍 |
  | s8_st2、s5_st2 | 0s | P8 首帧=第0秒 | 记录 | ③ 首帧 | 两镜第 0 秒都写「正迈步走向」门房或柜台，首帧都是站定不动；s5_st2 首帧里 Riley 已经站在柜台边，0–2s 走的那一两步没有起点 | 便宜：首帧改成迈步中（一只脚抬起），或把第一拍改成「已站定」 |

### I6 严重 · 世界物理 · P9 效果有来源
- a（1 分）：s5_st1 光线写太阳在她身后（西）、头发镶边、画左半边街在阴影里，首帧却是脸部正面受光、画左街面和房子被照亮，光向反了（见问题表）；s8_st1 首帧白墙临街面在阴影里、墙根一条阴影，和下午两点太阳在西南对得上；s5_st8 首帧 Riley 影子朝前左（东北），对
- 俯视图镜头在她东边、朝西拍，prompt「光线」写太阳在她身后（西）、头发镶边、画左（街南）半边街在阴影里；首帧脸被正面直射光照亮，没有镶边，画左房子和街面都在阳光里。首帧决定开场，会出一段光向和 s5_st8/st9 矛盾的镜头
- 大蒜铺门口 st8 写一只藤筐（首帧一只），st9 首帧画了两只；st9 光线写画右（街南）在阴影里，首帧画右那排铺面和人行道亮着，阴影落在街中间偏左
- 看点写「衬衫干爽了」，动作和 prompt 写「衬衫被汗贴在背上」；prompt 用的是后者，和热水室靠湿墙（s8_st6）对得上，只是看点写错
- 分数：a 1 / b None → 最终 1
  | s5_st1 | 0–17s | P9 光影来源 | 重出 | ③ prompt 或首帧 | 俯视图镜头在她东边、朝西拍，prompt「光线」写太阳在她身后（西）、头发镶边、画左（街南）半边街在阴影里；首帧脸被正面直射光照亮，没有镶边，画左房子和街面都在阳光里。首帧决定开场，会出一段光向和 s5_st8/st9 矛盾的镜头 | 便宜：按「逆光、发丝镶边、画左半边街在阴影里」重出首帧 |
  | s5_st8→st9 | st9 0s | P2 数量 / P9 光影 | 记录 | ③ 首帧 | 大蒜铺门口 st8 写一只藤筐（首帧一只），st9 首帧画了两只；st9 光线写画右（街南）在阴影里，首帧画右那排铺面和人行道亮着，阴影落在街中间偏左 | 便宜：st9 重出首帧，改成一只筐、画右半边街在阴影里 |
  | s8_st7 | 看点 vs 动作 | P9 效果来源（文字自相矛盾） | 记录 | ② 分镜文字 | 看点写「衬衫干爽了」，动作和 prompt 写「衬衫被汗贴在背上」；prompt 用的是后者，和热水室靠湿墙（s8_st6）对得上，只是看点写错 | 便宜：看点改成「出了一身汗、神清气爽」 |

### I7 严重 · 世界物理 · P6 穿模与距离
- a（1 分）：s6_st6 Riley 退出门槛后走的方向和院子布局相反（俯视图 9.4 秒到 12 秒从 (4.8,0.3) 走到 (6.8,0.9)，往东走，到了货车边上；楼梯却在 x≈1.5–2.5，在西边），首帧也把院子左右画反了，见问题表；其余镜头量过：s7_st4 门轴到她 1.07 米，门板长 0.8 米，扫过时离她身体最近约 0.27 米；s6_st5 她进车门时离门垛 0.9 米。
- 镜头在大堂里朝南看，画右是西边；但 s6_st4、s6_st5 都写楼梯在“院子西侧”，俯视图里楼梯在 x≈1.5–2.5，在门（x 4.0–5.6）的西边，所以从大堂往外看楼梯应该在画右，马厩在画左。spec 和 prompt.txt 第 13–15 行却写“院子左边的石楼梯”“从门洞左边走出画”，首帧门洞里楼梯也画在左边。俯视图里她走到 (6.8,0.9)，往东走，离货车 (x 6.1–7.9，y≥1.0) 只差约 0.1 米，离楼梯越走越远。和下一镜 s6_st4（从车门口看，楼梯在画左）放在一起，观众会看到两个方向的楼梯
- 分数：a 1 / b None → 最终 1
  | s6_st6 | 0–12 秒（首帧门洞里的院子；9.4–12 秒的走位） | P6 走位路线／空间（院子左右画反了） | 重出 | ② 分镜文字＋③ 首帧 | 镜头在大堂里朝南看，画右是西边；但 s6_st4、s6_st5 都写楼梯在“院子西侧”，俯视图里楼梯在 x≈1.5–2.5，在门（x 4.0–5.6）的西边，所以从大堂往外看楼梯应该在画右，马厩在画左。spec 和 prompt.txt 第 13–15 行却写“院子左边的石楼梯”“从门洞左边走出画”，首帧门洞里楼梯也画在左边。俯视图里她走到 (6.8,0.9)，往东走，离货车 (x 6.1–7.9，y≥1.0) 只差约 0.1 米，离楼梯越走越远。和下一镜 s6_st4（从车门口看，楼梯在画左）放在一起，观众会看到两个方向的楼梯 | 便宜：把这一镜门洞里的院子改成楼梯在画右、马厩在画左，Riley 改成从门洞右边出画（转向她的左手边），首帧重出图；俯视图里 Riley 9.4 秒后的路线改成往西南 (2,3.7) 方向走，避开货车 |

### I8 严重 · 世界物理 · P9 效果有来源
- a（1 分）：s7_st3 光线段写“9.5 秒吹灭”，节拍写 10.8–12.3 秒才吹、12.3 秒才灭；s7_st7 光线段写“10 秒后灯在凳上”，节拍是 13.8–15.8 秒才放；两处都已写进 prompt.txt（第 16 行），见问题表。
- 光线段写“0–9.5 秒有灯光……9.5 秒吹灭后：灯嘴一片黑”；节拍是 9.1–10.5 秒还在说 goodnight from Pompeii，10.8–12.3 秒才撑起来吹，12.3 秒才灭。模型照光线段生成的话，她说晚安时灯就自己灭了，后面对着熄了的灯吹气
- 光线段写“8 秒前在她手里……10 秒后灯在床头小凳上”；节拍和道具行是 13.8–15.8 秒才放上凳子。10–13.8 秒光照会按“灯在凳上”来画，但灯其实还在她手里，可能画成同时有两盏灯，或者灯提前跑到凳子上
- 分数：a 1 / b None → 最终 1
  | s7_st3 | 9.5 秒（光线段）↔ 10.8–12.3 秒（节拍） | P9 效果没有来源（灯在吹之前就灭了） | 重出 | ② 分镜文字（prompt.txt 第 16 行已写进去） | 光线段写“0–9.5 秒有灯光……9.5 秒吹灭后：灯嘴一片黑”；节拍是 9.1–10.5 秒还在说 goodnight from Pompeii，10.8–12.3 秒才撑起来吹，12.3 秒才灭。模型照光线段生成的话，她说晚安时灯就自己灭了，后面对着熄了的灯吹气 | 便宜：光线段改成“0–12.3 秒……12.3 秒吹灭后”，和节拍、道具行统一 |
  | s7_st7 | 8 秒、10 秒（光线段）↔ 13.8–15.8 秒（节拍） | P9 光源位置不对／P2 | 可剪 | ② 分镜文字（prompt.txt 第 16 行） | 光线段写“8 秒前在她手里……10 秒后灯在床头小凳上”；节拍和道具行是 13.8–15.8 秒才放上凳子。10–13.8 秒光照会按“灯在凳上”来画，但灯其实还在她手里，可能画成同时有两盏灯，或者灯提前跑到凳子上 | 便宜：改成“13.8 秒前在她手里……15.8 秒后在小凳上” |

### I9 严重 · 人物逻辑 · C9 像真人
- a（1 分）：同一个梗拖成多拍、多镜头重复——Felix 摇头笑 s3_st4 17–18.5、s3_st8 6–9、s3_st6 3.5–5.5 共三次，推正面包 s3_st8 末与 s3_st6 5.5–8 两次；Vibia 的裤子梗 s2_st5 1.2–5.2 → s2_st8 → s2_st4「嘴角还撇着」三镜（问题 4、5）。
- Felix 摇头笑 3 次（st4、st8、st6），推正或拨正面包 2 次（st8 末、st6 5.5–8）
- 同一个梗三镜：st5 看脸、看腿、再看一眼、挑眉、撇嘴、摇头（4 秒内 6 个动作），st8 又挑眉摇头，st4 又「嘴角还撇着」。用户 2026-11-10 已说 s2 裤子梗僵硬
- 分数：a 1 / b None → 最终 1
  | s3_st4 → s3_st8 → s3_st6 | 17–18.5 / 6–9 / 3.5–5.5 | C9 / C7 | 重出 | ② 分镜文字 | Felix 摇头笑 3 次（st4、st8、st6），推正或拨正面包 2 次（st8 末、st6 5.5–8） | 便宜：全集只留一次摇头，放在 s3_st8 末（她走反那一下）；st4 只留「嘴角一动」；st6 删除 |
  | s2_st5 → s2_st8 → s2_st4 | st5 1.2–5.2；st8 0–1；st4 0–1.5 | C9 / C11 | 可剪 | ② 分镜文字 | 同一个梗三镜：st5 看脸、看腿、再看一眼、挑眉、撇嘴、摇头（4 秒内 6 个动作），st8 又挑眉摇头，st4 又「嘴角还撇着」。用户 2026-11-10 已说 s2 裤子梗僵硬 | 便宜：st5 只留「目光落到腿上愣一下、挑一边眉」，不撇嘴摇头；st8 保留回头瞄的半秒；st4 去掉「嘴角撇着」。梗的笑点只落在 st8 台词那一下 |

### I10 严重 · 人物逻辑 · C10 动机来自人物
- a（1 分）：s3_st4 2.3–5.2 秒 Felix「头一直低着、眼睛只看托板」是为了让她听不懂，画面上读不出他为什么不看人、不比划（首帧图 Felix 低头微笑看托板）；s3_st6 1.5–3.5 秒他「想喊又咽回去」，画面读不出理由，而同一个情形 s5_st8 的店主是又喊又指（问题 1、2）。
- Felix「头一直低着、眼睛只看托板」说一句飞快的拉丁语，没有手势，Riley 只问一个词「Garum?」；他在 s3_st1 已知她是外地人；s5_st8 同样的指路情形店主是大喊加整臂指方向
- 张嘴吸一口气、身子前探、笑出声，单独一镜只拍这个反应；他没喊的理由画面读不出来；st8 末他已经摇头并推正面包
- Felix 搁托板翻面包、拍粉、擦汗，写着「动作要大、看得清」，是给他补的活；翻看刚出炉面包的底部有合理性，但「擦汗」和「动作要大」像是表演指令
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 1.1–5.2 | C10 / C2 / C3 / C1 | 重出（已知，只列不展开） | ② 分镜文字 | Felix「头一直低着、眼睛只看托板」说一句飞快的拉丁语，没有手势，Riley 只问一个词「Garum?」；他在 s3_st1 已知她是外地人；s5_st8 同样的指路情形店主是大喊加整臂指方向 | 便宜：由用户在 story_beats 15/15b 挑改法。改的方向：让 Felix 抬头看她、用手一指街，Riley 带手势问路；让他不看她的理由出自人物（例如手里端着滚烫的托板腾不出手，且观众看得到），而不是「为了让她猜不出」 |
  | s3_st6（整镜）/ s3_st8 6–9 | st6 1.5–5.5；st8 6–9 | C11 / C10 | 重出（已知，只列不展开） | ① 故事 / ② 分镜 | 张嘴吸一口气、身子前探、笑出声，单独一镜只拍这个反应；他没喊的理由画面读不出来；st8 末他已经摇头并推正面包 | 便宜：删 s3_st6 整镜，或并进 s3_st8 末尾一个小动作（目光追着她、嘴角动一下）。不要吸气前探、不要笑出声 |
  | s3_st4 | 8–17 | C10（存疑） | 存疑 | ② 分镜文字 | Felix 搁托板翻面包、拍粉、擦汗，写着「动作要大、看得清」，是给他补的活；翻看刚出炉面包的底部有合理性，但「擦汗」和「动作要大」像是表演指令 | 便宜：核实首帧/出片里这些动作是否读得出（在检查面包有没有烤透）；写成「检查面包底」一个动作，去掉「动作要大」 |

### I11 严重 · 人物逻辑 · C11 反应合比例
- a（1 分）：s3_st6 1.5–2.5 秒「张嘴吸一口气、身子前探」，且单独一整镜（8 秒）只拍他的反应；s3_st4 17–18.5 秒「鼓起腮帮憋笑」单独一拍；s3_st6 3.5–5.5 秒「笑出声」，事情本身只是她选了左（问题 2、3）。
- 张嘴吸一口气、身子前探、笑出声，单独一镜只拍这个反应；他没喊的理由画面读不出来；st8 末他已经摇头并推正面包
- 「鼓起腮帮憋住笑、轻轻摇头」单独一拍，比她赌了个左本身的事大；鼓腮属于必须去掉的大表情
- 同一个梗三镜：st5 看脸、看腿、再看一眼、挑眉、撇嘴、摇头（4 秒内 6 个动作），st8 又挑眉摇头，st4 又「嘴角还撇着」。用户 2026-11-10 已说 s2 裤子梗僵硬
- 分数：a 1 / b None → 最终 1
  | s3_st6（整镜）/ s3_st8 6–9 | st6 1.5–5.5；st8 6–9 | C11 / C10 | 重出（已知，只列不展开） | ① 故事 / ② 分镜 | 张嘴吸一口气、身子前探、笑出声，单独一镜只拍这个反应；他没喊的理由画面读不出来；st8 末他已经摇头并推正面包 | 便宜：删 s3_st6 整镜，或并进 s3_st8 末尾一个小动作（目光追着她、嘴角动一下）。不要吸气前探、不要笑出声 |
  | s3_st4 | 17–18.5 | C11 | 重出 | ② 分镜文字 | 「鼓起腮帮憋住笑、轻轻摇头」单独一拍，比她赌了个左本身的事大；鼓腮属于必须去掉的大表情 | 便宜：改成嘴角一动、低头继续摆面包，并入 16.8 秒后的收尾，不单独占拍 |
  | s2_st5 → s2_st8 → s2_st4 | st5 1.2–5.2；st8 0–1；st4 0–1.5 | C9 / C11 | 可剪 | ② 分镜文字 | 同一个梗三镜：st5 看脸、看腿、再看一眼、挑眉、撇嘴、摇头（4 秒内 6 个动作），st8 又挑眉摇头，st4 又「嘴角还撇着」。用户 2026-11-10 已说 s2 裤子梗僵硬 | 便宜：st5 只留「目光落到腿上愣一下、挑一边眉」，不撇嘴摇头；st8 保留回头瞄的半秒；st4 去掉「嘴角撇着」。梗的笑点只落在 st8 台词那一下 |

### I12 严重 · 人物逻辑 · C11 反应合比例
- a（1 分）：s8_st10 6.5–8 秒门房「摇头笑出了声」，规则里「笑出声」就是 ✗；s8_st8 两位妇女「捂嘴笑」两次、s8_st3 里侧两位 0 秒起就「笑着」，共同堆成一屋子笑，比「穿衣服来洗澡」这件事本身更大（问题表 2、4）。
- 门房「摇头笑出了声」；规则 C11 把「笑出声」列为 ✗；0 秒起她已「嘴角带着一点笑意」，再笑出声就是叠加；对一个不说话的门房，只摆手放行已够读
- 厅里的反应全是「笑」：st3 里侧两位 0 秒起就「笑着朝走道看」，st8 同伴「对看一眼，捂嘴笑」2.5–4 秒与 9–10 秒各一次；首帧图 st3 右侧两位也已在笑
- 分数：a 1 / b None → 最终 1
  | s8_st10 | 6.5–8 秒 | C11 | 重出 | ② 分镜文字 | 门房「摇头笑出了声」；规则 C11 把「笑出声」列为 ✗；0 秒起她已「嘴角带着一点笑意」，再笑出声就是叠加；对一个不说话的门房，只摆手放行已够读 | 便宜：改成「门房抬一下眉、右手朝画左一挥，嘴角一撇」，去掉笑出声。 |
  | s8_st3 / s8_st8 | st3 0 秒、7–9 秒；st8 2.5–4、9–10 秒 | C11 · C6 | 重出 | ② 分镜文字 | 厅里的反应全是「笑」：st3 里侧两位 0 秒起就「笑着朝走道看」，st8 同伴「对看一眼，捂嘴笑」2.5–4 秒与 9–10 秒各一次；首帧图 st3 右侧两位也已在笑 | 便宜：st3 只留 1 位笑，其余用「瞥一眼」「继续梳头」；st8 把 9–10 秒那次改成「画左妇女回头接着聊天」；让反应不都是笑。 |

### I13 严重 · 人物逻辑 · C10
- 「被画面左边、镜头身后的什么动静吸引」；画面上没有任何东西可看，观众读不出她为什么突然转身走；而她听不懂拉丁语，下一镜 s6_st1 才是 Fortunata 的吆喝
  | s6_st3 | 19.6–20.6 秒 | C10 | 重出 | ② 分镜文字 | 「被画面左边、镜头身后的什么动静吸引」；画面上没有任何东西可看，观众读不出她为什么突然转身走；而她听不懂拉丁语，下一镜 s6_st1 才是 Fortunata 的吆喝 | 便宜：写明动静 = 画外传来 Fortunata 低沉的招揽声（Hospitium hic locatur!）和暖灯光，她听到声音、看到门口灯光才转身；或把她往左走的理由写成「看见画外的油灯光」。 |

### I14 严重 · 连续性 · K2 钱账
- a（1 分）：spec 账本身是平的，9＝2（s3_st1 面包）＋1 小铜币（s8_st2 浴场）＋2（s5_st3 酒）＋4（s6_st2 住宿），各镜「付后」枚数都对；但 s5_st3 首帧放大（z2.jpg 左）手心是 4 枚红铜＋1 枚黄铜＝5 枚，spec 要 6 枚，而且第 0 秒应该还攥着拳（见问题表）
- 首帧放大（z2.jpg 左）摊开的掌心里是 4 枚红铜＋1 枚黄铜＝5 枚；spec 要求 0 s 攥拳，1.5 s 摊开时「正好 6 枚：5 红铜＋1 黄铜」。按这张首帧出片，付 2 枚后手里只剩 3 枚，和 s6_st3 的「3 红＋1 黄」对不上
- 分数：a 1 / b None → 最终 1
  | s5_st3 | 0s 首帧 | K2 钱账 / K1 | 重出（首帧） | ③ 首帧 | 首帧放大（z2.jpg 左）摊开的掌心里是 4 枚红铜＋1 枚黄铜＝5 枚；spec 要求 0 s 攥拳，1.5 s 摊开时「正好 6 枚：5 红铜＋1 黄铜」。按这张首帧出片，付 2 枚后手里只剩 3 枚，和 s6_st3 的「3 红＋1 黄」对不上 | 便宜：首帧重出，第 0 秒画右拳攥着、看不见钱；或者画摊开的手、正好 5 红＋1 黄 |

### I15 严重 · 连续性 · K5 站位接续
- a（1 分）：s6_st6 Riley 出大堂后走向东边（overhead z3.jpg 里蓝线 10.8–12 s 朝东南去），但石楼梯在院子西侧（s6_st4 overhead z4.jpg、s6_st1/st5 首帧都是这样）；另外 s3_st1→st2 Felix 一瞬间从石台到了炉口（见问题表）
- 镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧（z1.jpg 右）也把楼梯画在左边。可是 s6_st1/st5 首帧、s6_st4 的 spec 和 overhead（z4.jpg）、本镜自己的 overhead（z3.jpg，楼梯在左下角＝西）都把楼梯放在院子西侧；本镜 overhead 里 Riley 的走位线 9.4–12 s 却朝东南、朝货车走
- st1 结尾 Felix 在石台里侧对她点头；st2 第 0 秒镜头就架在 Felix 原来的位置（石台里侧偏西），spec 说「Felix 这时在镜头身后的炉口那边取面包」，0 秒内换了位置
- 分数：a 1 / b None → 最终 1
  | s6_st6 | 0–12s | K6/K5 场景镜像 | 重出 | ② 分镜文字（首帧③跟着错了） | 镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧（z1.jpg 右）也把楼梯画在左边。可是 s6_st1/st5 首帧、s6_st4 的 spec 和 overhead（z4.jpg）、本镜自己的 overhead（z3.jpg，楼梯在左下角＝西）都把楼梯放在院子西侧；本镜 overhead 里 Riley 的走位线 9.4–12 s 却朝东南、朝货车走 | 便宜：spec 和 prompt 改成「院子右边（西侧）的石楼梯／马厩木栏在画左」「从门洞右边走出画」，overhead 走位改成朝西，首帧重出 |
  | s3_st1 → s3_st2 | 接点 | K5 站位 | 记录 | ② 分镜文字 | st1 结尾 Felix 在石台里侧对她点头；st2 第 0 秒镜头就架在 Felix 原来的位置（石台里侧偏西），spec 说「Felix 这时在镜头身后的炉口那边取面包」，0 秒内换了位置 | 可以不改（Felix 在画外）；要严谨的话，st2 开头加「Felix 转身去炉口」的声音提示 |

### I16 严重 · 连续性 · K6 环境接续
- a（1 分）：s2_st3 和 s2_st1 的水流方向相反；s6_st6 大堂门外楼梯和马厩左右镜像；s5_st6 两个吃饭的男人站在柜台东段外面，到 s5_st7 变成坐在灶台那头的店里（见问题表）
- 镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧（z1.jpg 右）也把楼梯画在左边。可是 s6_st1/st5 首帧、s6_st4 的 spec 和 overhead（z4.jpg）、本镜自己的 overhead（z3.jpg，楼梯在左下角＝西）都把楼梯放在院子西侧；本镜 overhead 里 Riley 的走位线 9.4–12 s 却朝东南、朝货车走
- s2_st3 镜头朝东，画右是南：「从画右往画左顺着街流」＝水从南往北流；s2_st1 镜头朝北，「从画面深处的上坡往镜头这边流」＝水从北往南流。两个 prompt 原文都带着这两句（已 grep 核对）。这两镜在 s2 开场连着播
- st6 写两个干完活的男人「站在柜台外侧、东头拐角前的台沿边」，一个蘸豆子一个喝酒；st7 写「灶台那头的店里，远远坐着两个低头吃喝的男人」（prompt 原文就是这样），首帧（s5 联系表 st7）也是坐在店里灶边。到底是同一对还是另一对，前后没交代，位置和姿态都对不上
- 分数：a 1 / b None → 最终 1
  | s6_st6 | 0–12s | K6/K5 场景镜像 | 重出 | ② 分镜文字（首帧③跟着错了） | 镜头在大堂北墙朝南拍，画面左边是东；spec 和 prompt 却写「门洞里看得见院子左边一道石楼梯」「朝院子左边的石楼梯走去，从门洞左边走出画」，首帧（z1.jpg 右）也把楼梯画在左边。可是 s6_st1/st5 首帧、s6_st4 的 spec 和 overhead（z4.jpg）、本镜自己的 overhead（z3.jpg，楼梯在左下角＝西）都把楼梯放在院子西侧；本镜 overhead 里 Riley 的走位线 9.4–12 s 却朝东南、朝货车走 | 便宜：spec 和 prompt 改成「院子右边（西侧）的石楼梯／马厩木栏在画左」「从门洞右边走出画」，overhead 走位改成朝西，首帧重出 |
  | s2_st1 ↔ s2_st3 | 全镜 | K6 环境（水流方向） | 重出 | ② 分镜文字 | s2_st3 镜头朝东，画右是南：「从画右往画左顺着街流」＝水从南往北流；s2_st1 镜头朝北，「从画面深处的上坡往镜头这边流」＝水从北往南流。两个 prompt 原文都带着这两句（已 grep 核对）。这两镜在 s2 开场连着播 | 便宜：定一个方向，按北高南低算，s2_st3 改成「从画左往画右流」；s2_st2/st5/st4 里提到流向的地方一起核一遍 |
  | s5_st6 ↔ s5_st7 | st6 0–8s / st7 0s | K6 环境（路人位置） | 可剪 | ② 分镜文字 | st6 写两个干完活的男人「站在柜台外侧、东头拐角前的台沿边」，一个蘸豆子一个喝酒；st7 写「灶台那头的店里，远远坐着两个低头吃喝的男人」（prompt 原文就是这样），首帧（s5 联系表 st7）也是坐在店里灶边。到底是同一对还是另一对，前后没交代，位置和姿态都对不上 | 便宜：st7 改成「柜台东段外侧台沿边站着那两个男人（同 st6）」，首帧重出 |

### I17 严重 · 台词（时长与逻辑） · D1 说得完
- a（1 分）：多数镜头语速正常（s1_st2 共 53 词 / 1.5–28.5 秒 ≈2.0 词/秒；s4_st2 49 词 / 1.2–23 秒 ≈2.2；s2_st2 32 词 / 15 秒 ≈2.1；s5_st5 33 词 / 16.8 秒 ≈2.0；s8_st1 26 词 / 12.7 秒 ≈2.0），开口前 ≥1.1 秒（最紧是 s3_st4 的 Garum? 在 1.1 秒）、说完后 ≥1.5 秒（最紧是 s2_st2 和 s1_st2 各 1.5 秒）。但有三处明显偏快：s8_st9 15.4–18.0 秒 “Gross. Kind of love it, though.” 共 7 词窗口只有 2.6 秒，其中后半 6 词只给 1.6 秒（3.75 词/秒，正常需 2.4 秒）；s1_st1 16.7–18.8 秒 “Wait, wait — I gotta do this right.” 7 词 / 2.1 秒 = 3.3 词/秒；s6_st3 6.4–11.6 秒 14 词 / 5.2 秒 = 2.7 词/秒，且 17.0–18.2 秒 “That’s — not ideal.” 4 词 / 1.2 秒。见问题表。
- 15.4–16.0 秒 “Gross.” + 16.4–18.0 秒 “Kind of love it, though.” 6 词只给 1.6 秒 = 3.75 词/秒，按 2.5 词/秒要 2.4 秒；前面 1.6–10.0 秒是 2.5 词/秒也是上限
- “Wait, wait — I gotta do this right.” 7 词窗口 16.7–18.8 秒 = 3.3 词/秒，且是边快步走边说
- 6.4–11.6 秒 14 词 = 2.7 词/秒（正常 5.6 秒）；17.0–18.2 秒 “That’s — not ideal.” 4 词 1.2 秒 = 3.3 词/秒
- Apage 只给 0.5 秒（3 音节）；“Okay, okay — I’m going!” 5 词 / 1.8 秒 = 2.8 词/秒
- 分数：a 1 / b None → 最终 1
  | s8_st9 | 15.2–18.2 | D1 | 重出 | ② 分镜文字 | 15.4–16.0 秒 “Gross.” + 16.4–18.0 秒 “Kind of love it, though.” 6 词只给 1.6 秒 = 3.75 词/秒，按 2.5 词/秒要 2.4 秒；前面 1.6–10.0 秒是 2.5 词/秒也是上限 | 不改句子；镜头延长到约 23 秒，把 “Gross.” 后的皱鼻子停半拍后，“Kind of love it, though.” 窗口放到 16.4–18.9 秒，递刮板的动作整体后移 1 秒。便宜（改节拍文字，出片前） |
  | s1_st1 | 16.5–19.5 | D1 | 记录 | ② 分镜文字 | “Wait, wait — I gotta do this right.” 7 词窗口 16.7–18.8 秒 = 3.3 词/秒，且是边快步走边说 | 不改句子；把走近镜头那一段拉长 1 秒（16.5–20.5 秒），镜头延到 23 秒或把 19.5–21 秒的停留压短。便宜 |
  | s6_st3 | 6.4–18.2 | D1 | 记录 | ② 分镜文字 | 6.4–11.6 秒 14 词 = 2.7 词/秒（正常 5.6 秒）；17.0–18.2 秒 “That’s — not ideal.” 4 词 1.2 秒 = 3.3 词/秒 | 把 6.3–11.7 拉到 6.3–12.2 秒，“That’s — not ideal.” 给 1.8 秒（17.0–18.8 秒），后面的转头出画顺延 0.6 秒，镜头 23→24 秒。便宜 |
  | s4_st1 | 6.4–7.0；8.8–10.8 | D2/D1 | 记录 | ② 分镜文字 | Apage 只给 0.5 秒（3 音节）；“Okay, okay — I’m going!” 5 词 / 1.8 秒 = 2.8 词/秒 | Apage 窗口放到 6.4–7.1 秒，Riley 台词窗口放到 8.8–11.0 秒（镜头 13 秒内够用）。便宜 |

### I18 严重 · 台词（时长与逻辑） · D8 跨语言说清
- a（1 分）：s3_st4 Riley 只问一个词 “Garum?”（1.1–1.7 秒），Felix 全程低头不看她、没有手势（2.3–5.2 秒），观众和 Riley 都不知道他说了什么，属于任务书点名的 ✗，属已知问题（story_beats 节点 15/15b）。同一维度其他镜头是好的：s5_st11 Riley 说完整一句 + OK 手势、s5_st12 Asellina 回 OK 手势；s6_st1 5–8 秒 Riley 指自己、睡觉手势、一根手指；s8_st2 门房伸手 → Riley 付一枚最小的钱；s5_st13 举着面包问 Garum? 并配 Asellina 的鱼露罐。
- Riley 只问 “Garum?”，Felix “头一直低着、眼睛只看托板”、无手势，说一句快速拉丁语；观众不知道她要什么、他答了什么
- Felix 不懂英语，却在 Riley 说英文 “left” 时憋笑摇头；她说 left 时没有手势指方向
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 1.1–5.2 | D8 | 重出（已知，待用户选） | ② 分镜文字 | Riley 只问 “Garum?”，Felix “头一直低着、眼睛只看托板”、无手势，说一句快速拉丁语；观众不知道她要什么、他答了什么 | 已知问题，不展开：按 story_beats 里用户挑的改法重写（Riley 用完整说法 + 手势问路，Felix 抬头、手指方向、慢一点说）。便宜（改文字）；若已出视频则要积分 |
  | s3_st4 | 17–18.5 | D2/D8 | 记录 | ② 分镜文字 | Felix 不懂英语，却在 Riley 说英文 “left” 时憋笑摇头；她说 left 时没有手势指方向 | Riley 说 “left” 的同时抬手往左一指，Felix 看到手势才憋笑。便宜 |

### I19 严重 · 母语听感 · N8 修辞痕迹
- a（1 分）：修辞痕迹 12 处，全部列在下面「修辞痕迹清单」，其中 s7_st1 就是用户 2026-11-08 点名的那一类：三项并列、最后一项停顿抖包袱、再自问自答「Honestly? Worth it.」。同一套「停顿 + 包袱」在 s1_st2、s4_st4、s4_st5、s6_st3、s3_st4 反复出现，见问题表。
- 「So I found a bed, I tried the garum… and I have zero money left. Honestly? Worth it.」三项并列 + 省略号抖包袱 + 自问自答，与「Okay, so garum — check」（s5_st7）一起把「清单回收」写得太整齐
- 「…Nope. Just smells like money.」双关包袱 + 「Honestly? He's got a point.」自问自答
- 「So the Romans basically had sliced bread first. Love that.」是现成俗语「best thing since sliced bread」的反用，一听就是写的
- 「Why did I keep my clothes on? Rookie mistake.」自问自答 + 收尾按钮
- 一个人走在窄街上，一口气讲完「they wash clothes in pee… the emperor puts a tax on the pee… his son thought that was disgusting… 'Does this smell?'」，连 like 都放在整齐的位置（「Like, actual pee」「like, the current emperor」）
- 「Left or right? Fifty-fifty. I'm gonna say… left.」自问自答 + 停顿；而且 Felix 双手端托板没有手势，她凭什么先猜这是「左 / 右」？
- 「…and this… is all the money I have left. Yeah. That's — not ideal.」是 s1_st2「my budget is… this. Yeah. This is it.」的镜像；三项并列加停顿亮钱，第二次用就更像设计
- 「Okay, so garum — check. Now I just have to find a bed.」清单勾选，手势和台词一起做成 to-do
- 「I'm, like, ninety percent sure. Left.」收尾单词「Left.」像一锤定音的字幕；且前一镜已说「I'm gonna say… left」，这里又重新宣布一次
- 「Okay, I'm clean. Ish.」「So it's basically dinner time. Which is wild.」两个收尾包袱；「Which is wild.」像字幕
- 分数：a 1 / b None → 最终 1
  | s7_st1 | 全镜 | N8 / N7 | 重出 | ① 故事 / ② 分镜文字 | 「So I found a bed, I tried the garum… and I have zero money left. Honestly? Worth it.」三项并列 + 省略号抖包袱 + 自问自答，与「Okay, so garum — check」（s5_st7）一起把「清单回收」写得太整齐 | 便宜（只改台词文字）。改成：「Okay, so — I've got a bed. I ate the fish sauce. And I'm, like, completely broke. …Yeah, no. Honestly, still worth it.」或更散的：「So I have a bed, I had the garum, and I have, like, no money. Which — fine. Worth it.」 |
  | s4_st5 | 全镜 | N8 | 可剪 | ② | 「…Nope. Just smells like money.」双关包袱 + 「Honestly? He's got a point.」自问自答 | 便宜。改成：「…No. It just smells like, you know, metal. Okay, honestly? He kind of has a point.」去掉「smells like money」的整齐双关，或保留但把它放在笑完之后的自言自语里 |
  | s3_st2 | 全镜 | N8 | 可剪 | ② | 「So the Romans basically had sliced bread first. Love that.」是现成俗语「best thing since sliced bread」的反用，一听就是写的 | 便宜。改成：「Oh it's pre-cut — look, it just snaps right off. That's so smart. Okay, Romans, one point.」 |
  | s8_st4 | 全镜 | N8 / N7 | 可剪 | ② | 「Why did I keep my clothes on? Rookie mistake.」自问自答 + 收尾按钮 | 便宜。改成：「Oh my god, it is so hot in here. Why am I still wearing all my clothes? I'm such an idiot.」 |
  | s4_st2 | 全镜（25 秒） | N9 / N8 | 可剪 | ② | 一个人走在窄街上，一口气讲完「they wash clothes in pee… the emperor puts a tax on the pee… his son thought that was disgusting… 'Does this smell?'」，连 like 都放在整齐的位置（「Like, actual pee」「like, the current emperor」） | 便宜。拆成两三句带自我打断的：「So — they wash clothes in pee here. Like, actual pee. And the emperor — okay, apparently the emperor taxed it. His son was like, ew, and he goes — he holds up a coin, like, 'Does this smell?'」 |
  | s3_st4 | 全镜 | N8 / N10 | 可剪 | ② | 「Left or right? Fifty-fifty. I'm gonna say… left.」自问自答 + 停顿；而且 Felix 双手端托板没有手势，她凭什么先猜这是「左 / 右」？ | 便宜。改成：「Okay… I definitely heard 'dextram.' No idea what that means. I mean, he said 'straight,' I think? So maybe it's, like, a direction? Left or right… I don't know. I'm gonna go left.」（先说出她为什么猜方向） |
  | s6_st3 | 全镜 | N8 / N10 | 记录 | ② | 「…and this… is all the money I have left. Yeah. That's — not ideal.」是 s1_st2「my budget is… this. Yeah. This is it.」的镜像；三项并列加停顿亮钱，第二次用就更像设计 | 便宜。改成：「Okay, the sun is going down, I have nowhere to sleep, and — this is what I have left. Uh. Not great.」 |
  | s5_st7 | 全镜 | N8 | 记录 | ② | 「Okay, so garum — check. Now I just have to find a bed.」清单勾选，手势和台词一起做成 to-do | 便宜。改成：「Okay. Garum, done. That was so good. Okay — now I really need to find a bed.」 |
  | s4_st3 | 全镜 | N8 / N10 | 记录 | ② | 「I'm, like, ninety percent sure. Left.」收尾单词「Left.」像一锤定音的字幕；且前一镜已说「I'm gonna say… left」，这里又重新宣布一次 | 便宜。改成：「Okay, going left. I'm pretty sure. Ish. Probably.」 |
  | s5_st1 | 全镜 | N8 | 记录 | ② | 「Okay, I'm clean. Ish.」「So it's basically dinner time. Which is wild.」两个收尾包袱；「Which is wild.」像字幕 | 便宜。改成：「Okay, I'm clean. Ish. And I'm starving — and, weirdly, that's fine, because people here eat dinner at, like, three-thirty. So it's basically dinner time.」 |

### I20 严重 · 时代与世界观 · E5 文字
- a（1 分）：s7_st1 首帧墙面（约 x360–520,y360–560）和 s7_st2 首帧墙面（约 x120–340,y460–660）各有四到五行排得整整齐齐、像拉丁字母的伪文字刻痕，s7_st1 第一行放大后像「ACNAP」（见问题表）。其余镜头的钱币（s4_st5、s5_st3、s6_st2 放大后看）和 s1 的船身都没有可读字母
- 首帧墙面灯上方（约 x360–520,y360–560）有五行像字母的刻痕，放大后第一行像「ACNAP」，第二至四行是连续的伪拉丁字母（裁切图 s7st1_graffiti.png）；spec 第 11 行本来要求的是「看不出字形的划痕」。首帧会被视频沿用整整 13 秒
- 首帧左上（约 x120–340,y460–660）有四行整齐的伪字母刻痕（裁切图 s7st2_graffiti.png）；spec 第 11 行要求的「几行排得整整齐齐、刻得比别处深的细线」在 Riley 念涂鸦的语境里，模型一定会画成字
- 分数：a 1 / b None → 最终 1
  | s7_st1 | 0 秒首帧 | E5 文字 | 重出 | ③ prompt 或首帧 | 首帧墙面灯上方（约 x360–520,y360–560）有五行像字母的刻痕，放大后第一行像「ACNAP」，第二至四行是连续的伪拉丁字母（裁切图 s7st1_graffiti.png）；spec 第 11 行本来要求的是「看不出字形的划痕」。首帧会被视频沿用整整 13 秒 | 便宜：重出首帧，把这片墙改成乱刮的交叉短线、计数划痕，或把这片墙放到灯影外；负面词加「像字母的刻痕、成行的伪文字」 |
  | s7_st2 | 0 秒首帧，0–10.7 秒重点看墙 | E5 文字 / E7 分镜写法 | 重出 | ② 分镜文字 | 首帧左上（约 x120–340,y460–660）有四行整齐的伪字母刻痕（裁切图 s7st2_graffiti.png）；spec 第 11 行要求的「几行排得整整齐齐、刻得比别处深的细线」在 Riley 念涂鸦的语境里，模型一定会画成字 | 便宜：分镜改成「一小片刻得较深、交错杂乱的划痕，没有行、没有字形」，或让 Riley 只朝墙一摆手、不给墙特写；首帧重出 |

### I21 严重 · 时代与世界观 · E7 规则源
- a（1 分）：规则源之间有矛盾。bible §9 写「维苏威只在画面里、全片不提，入画时只能是远处绿山」；dossier 第 16 行却写「片中入画的那座绿山按南面 Monti Lattari 写……维苏威在画外」，第 78 行规定山只写成「单峰绿山，山顶平缓圆润、长满灌木和草」；而 bg1 卡里送进 prompt 的场景行（s1_st1 prompt 第 9 行）写的是「长满葡萄藤……山坡上是整齐的葡萄藤」，这正是维苏威的视觉锁定。另外 s7_st2 分镜本身要求「几行排得整整齐齐、刻得比别处深的细线」，这种写法必然诱发伪文字。见问题表
- 首帧左上（约 x120–340,y460–660）有四行整齐的伪字母刻痕（裁切图 s7st2_graffiti.png）；spec 第 11 行要求的「几行排得整整齐齐、刻得比别处深的细线」在 Riley 念涂鸦的语境里，模型一定会画成字
- 三张首帧画右都是一座满坡整齐葡萄藤的锥形大山（s1_st1 约占右上三分之一），长相就是维苏威的考据画像。bible §9（维苏威可入画）、dossier 第 16 行（山是 Lattari，维苏威在画外）、dossier 第 78 行（只写「灌木和草」）、bg1 场景行（写「整齐的葡萄藤」）四处说法不一
- p4 卡写「直的木柄＋青铜弯勺」，s8_st5 首帧就像一把木柄镰刀；出土的 strigil 多是整件青铜或铁打的，弯勺加同材质把手，r03 第 173 行注明刮板外观没查到引文
- 分数：a 1 / b None → 最终 1
  | s7_st2 | 0 秒首帧，0–10.7 秒重点看墙 | E5 文字 / E7 分镜写法 | 重出 | ② 分镜文字 | 首帧左上（约 x120–340,y460–660）有四行整齐的伪字母刻痕（裁切图 s7st2_graffiti.png）；spec 第 11 行要求的「几行排得整整齐齐、刻得比别处深的细线」在 Riley 念涂鸦的语境里，模型一定会画成字 | 便宜：分镜改成「一小片刻得较深、交错杂乱的划痕，没有行、没有字形」，或让 Riley 只朝墙一摆手、不给墙特写；首帧重出 |
  | s1_st1、s1_st2、s1_st4 | 全条 | E4 禁区 / E7 规则源 | 记录 | 规则源 | 三张首帧画右都是一座满坡整齐葡萄藤的锥形大山（s1_st1 约占右上三分之一），长相就是维苏威的考据画像。bible §9（维苏威可入画）、dossier 第 16 行（山是 Lattari，维苏威在画外）、dossier 第 78 行（只写「灌木和草」）、bg1 场景行（写「整齐的葡萄藤」）四处说法不一 | 便宜：bible §9 改成与 dossier 一致；bg1 场景行改用 dossier 第 78 行的写法，去掉「葡萄藤」，再压小压淡；或按 bible 审查建议让山不入画 |
  | p4 刮板（s8_st5、s8_st9、s8_st6） | 0 秒首帧 | E7 道具卡 / E1 | 存疑 | 规则源 | p4 卡写「直的木柄＋青铜弯勺」，s8_st5 首帧就像一把木柄镰刀；出土的 strigil 多是整件青铜或铁打的，弯勺加同材质把手，r03 第 173 行注明刮板外观没查到引文 | 便宜：查 MANN 或大英博物馆的 strigil 图录后改卡，写成「整件青铜，弯勺和扁平把手连成一体」 |

### I22 严重 · 镜头规格 · F1 景别与人物大小
- a（1 分）：s8_st7 老汉站位图距镜头 3.28 m、35 mm，应占画高约 0.91，首帧实测 0.56（头 v0.37、脚 v0.93），小了约 38%。s7_st6 大了约 60%，s7_st3 脸宽大了约 97%。s5 柜台四镜（st3 st14 st13 st7）大了 22–41%，s5_st12 大了 25–30%。达标的例子：s8_st1 0.41→0.46（+12%）、s6_st3 +8%、s7_st4 0.77=0.77（见问题表）。
- 老汉（prop 路径起点 (8.2,8.7)）距机位 (5,8) 3.28 m、35 mm、机位高 0.9 m，应占画高约 0.91；首帧实测 0.56（头 v0.37、脚 v0.93），小了约 38%，看起来约在 5.3 m 外。横向 u≈0.08 是对的。人画小了，模型容易让他从 Riley 身后走过，而不是「从她和镜头之间走过」
- 首帧比站位图紧（每米占画高，几何值 → 实测）：st3 Riley +27%、Asellina +38%；st14 +34% / +23%；st13 +22% / +33%；st7 +41% / +40%，st7 Riley 头顶实测 v0.06，算出来应在 0.28
- 按头顶到腰带折算，Riley 距镜头约 1.6 m，overhead 写 2.54 m，画面里大了约 60%；u 实测 0.69，算出 0.85。窗洞尺寸和几何对得上，说明是人站位画错，不是焦距问题
- 脸宽占画宽 0.126，按 1.57 m、24 mm 应为 0.064，大了约 97%，折算距离只有约 0.8 m；灯到头 overhead 写 0.65 m，首帧约 0.3 m。文字写「中景、离床沿一米多」
- Asellina 实测 1.29 对几何 0.99（+30%），Riley 1.46 对 1.17（+25%）；和 st2 同机位，景别却紧约 13%，同机位相接会跳景
- 32 mm、2.62 m 应是中全景，画面高约 1.66 m；首帧 Fortunata 只到大腿，画面高约 1.06 m，人大约 57%；Riley 约 37%，实为中景
- 1.63 m、40 mm 取景高 0.83 m，首帧约 0.64 m（+29%）；文字写近景、偏右，首帧 u0.58，overhead 算出 0.46
- st9 Helvia 实测 u0.83、整个上半身入画，文字写「画右边缘只入画半身」；st6 文字写腰以上，2.19 m、35 mm 取景高 1.27 m，首帧露到脚（几何与首帧一致）；st3 文字写「背影在画面下部」，几何头顶 v0.32，首帧 0.25
- 分数：a 1 / b None → 最终 1
  | s8_st7 | 0–5s | F1 | 重出 | ③ prompt 或首帧 | 老汉（prop 路径起点 (8.2,8.7)）距机位 (5,8) 3.28 m、35 mm、机位高 0.9 m，应占画高约 0.91；首帧实测 0.56（头 v0.37、脚 v0.93），小了约 38%，看起来约在 5.3 m 外。横向 u≈0.08 是对的。人画小了，模型容易让他从 Riley 身后走过，而不是「从她和镜头之间走过」 | 重出首帧，老汉画到约 0.85–0.9 画高（便宜） |
  | s5_st3 / st14 / st13 / st7 | 0s 全镜 | F1 | 记录 | ③ prompt 或首帧 | 首帧比站位图紧（每米占画高，几何值 → 实测）：st3 Riley +27%、Asellina +38%；st14 +34% / +23%；st13 +22% / +33%；st7 +41% / +40%，st7 Riley 头顶实测 v0.06，算出来应在 0.28 | 站位图机位拉近到约 1.9 m，与首帧一致；或按 2.3–2.6 m 重出首帧。st3 文字「中景、两米多」与「中近景」二选一（便宜） |
  | s7_st6 | 0s | F1·F3 | 记录 | ③ prompt 或首帧 | 按头顶到腰带折算，Riley 距镜头约 1.6 m，overhead 写 2.54 m，画面里大了约 60%；u 实测 0.69，算出 0.85。窗洞尺寸和几何对得上，说明是人站位画错，不是焦距问题 | 按首帧反推改 overhead（机位往前约 0.9 m，或 Riley 往左）（便宜） |
  | s7_st3 | 0s | F1·F3 | 记录 | ③ prompt 或首帧 | 脸宽占画宽 0.126，按 1.57 m、24 mm 应为 0.064，大了约 97%，折算距离只有约 0.8 m；灯到头 overhead 写 0.65 m，首帧约 0.3 m。文字写「中景、离床沿一米多」 | 机位改到约 (1.3,1.6)，或景别改「中近景」，二者择一对齐（便宜） |
  | s5_st12 | 0s | F1 | 记录 | ③ prompt 或首帧 | Asellina 实测 1.29 对几何 0.99（+30%），Riley 1.46 对 1.17（+25%）；和 st2 同机位，景别却紧约 13%，同机位相接会跳景 | 重出首帧时按 st2 的大小（便宜） |
  | s6_st5 | 0s | F1 | 记录 | ③ prompt 或首帧 | 32 mm、2.62 m 应是中全景，画面高约 1.66 m；首帧 Fortunata 只到大腿，画面高约 1.06 m，人大约 57%；Riley 约 37%，实为中景 | 文字改「中景」，或重出首帧（便宜） |
  | s8_st10 | 0s | F1·F3 | 记录 | ② 分镜文字 | 1.63 m、40 mm 取景高 0.83 m，首帧约 0.64 m（+29%）；文字写近景、偏右，首帧 u0.58，overhead 算出 0.46 | overhead 机位前移约 0.4 m 并右偏（便宜） |
  | s8_st9 / st6 / st3 | 0s | F3·F1 | 记录 | ② 分镜文字 | st9 Helvia 实测 u0.83、整个上半身入画，文字写「画右边缘只入画半身」；st6 文字写腰以上，2.19 m、35 mm 取景高 1.27 m，首帧露到脚（几何与首帧一致）；st3 文字写「背影在画面下部」，几何头顶 v0.32，首帧 0.25 | 三处文字按几何改（便宜） |

### I23 严重 · 镜头规格 · F3 画面位置
- a（1 分）：s5_st8 横街口应在 u0.59–0.67，首帧里那段是连成一片的铺面；s6_st6 石楼梯在站位图上镜像到画右；s7_st6 Riley 实测 u0.69，算出 0.85；s8_st4 热水池应在镜头身后，首帧画在画右（见问题表）。
- 按 overhead，横街口和近角墙 (11.5,14) 应在 u0.59–0.67；首帧里店主铺子西边的南侧铺面连成一片，看不到横街口和墙角。看点「驴车拐进右边横街」画不出来，overhead note 也记着上一条成片在画内转弯、整车横移、穿模
- 按头顶到腰带折算，Riley 距镜头约 1.6 m，overhead 写 2.54 m，画面里大了约 60%；u 实测 0.69，算出 0.85。窗洞尺寸和几何对得上，说明是人站位画错，不是焦距问题
- 脸宽占画宽 0.126，按 1.57 m、24 mm 应为 0.064，大了约 97%，折算距离只有约 0.8 m；灯到头 overhead 写 0.65 m，首帧约 0.3 m。文字写「中景、离床沿一米多」
- 1.63 m、40 mm 取景高 0.83 m，首帧约 0.64 m（+29%）；文字写近景、偏右，首帧 u0.58，overhead 算出 0.46
- look 偏南 18° / 29°（28 mm），按几何柜台东南角在 u≈0.04（st8），st9 柜台全部在画外；文字和首帧都写画左是熟食铺门脸（st8 首帧柜台占 u0.03–0.33）。st8 overhead_ref 的扇形只画了约 9 m 长，驴车、店主、横街口都在扇形外
- overhead 里石楼梯在西南（朝南看是画右），Riley 却往东走到 (6.8,0.9)，终点压在「院里的货车」块上；文字和首帧写楼梯在画左；st1/st4/st5 楼梯都在西侧 x≈2，st6 院子镜像了
- overhead note 写「热水池在镜头身后」，首帧在画右约三分之一画了池子；圆盆按几何在 u0.17–0.67（大半被她挡住），首帧在 u0–0.33
- 文字写第 0 秒在「画右边缘」（几何 u0.99），首帧已在 u≈0.85、离柜台一步，0–2 秒的入画拍被吃掉
- 油灯 (4.6,6.4) 算出 u=−0.01，在左边框外；文字写「画面左上」，首帧在 u≈0.09
- st9 Helvia 实测 u0.83、整个上半身入画，文字写「画右边缘只入画半身」；st6 文字写腰以上，2.19 m、35 mm 取景高 1.27 m，首帧露到脚（几何与首帧一致）；st3 文字写「背影在画面下部」，几何头顶 v0.32，首帧 0.25
- 大堂门算出 u=1.18，应在画外；首帧画面右中（u≈0.84）有一个透暖光的门洞，不确定是不是大堂门。核实方法：对照 bg6 平面图
- 分数：a 1 / b None → 最终 1
  | s5_st8 | 0–8s | F3·F7·F8 | 重出 | ③ prompt 或首帧 | 按 overhead，横街口和近角墙 (11.5,14) 应在 u0.59–0.67；首帧里店主铺子西边的南侧铺面连成一片，看不到横街口和墙角。看点「驴车拐进右边横街」画不出来，overhead note 也记着上一条成片在画内转弯、整车横移、穿模 | 重出首帧，在 u≈0.6–0.67 画出横街口和挡车的墙角（便宜） |
  | s7_st6 | 0s | F1·F3 | 记录 | ③ prompt 或首帧 | 按头顶到腰带折算，Riley 距镜头约 1.6 m，overhead 写 2.54 m，画面里大了约 60%；u 实测 0.69，算出 0.85。窗洞尺寸和几何对得上，说明是人站位画错，不是焦距问题 | 按首帧反推改 overhead（机位往前约 0.9 m，或 Riley 往左）（便宜） |
  | s7_st3 | 0s | F1·F3 | 记录 | ③ prompt 或首帧 | 脸宽占画宽 0.126，按 1.57 m、24 mm 应为 0.064，大了约 97%，折算距离只有约 0.8 m；灯到头 overhead 写 0.65 m，首帧约 0.3 m。文字写「中景、离床沿一米多」 | 机位改到约 (1.3,1.6)，或景别改「中近景」，二者择一对齐（便宜） |
  | s8_st10 | 0s | F1·F3 | 记录 | ② 分镜文字 | 1.63 m、40 mm 取景高 0.83 m，首帧约 0.64 m（+29%）；文字写近景、偏右，首帧 u0.58，overhead 算出 0.46 | overhead 机位前移约 0.4 m 并右偏（便宜） |
  | s5_st8 / st9 | 全镜 | F2·F3 | 记录 | ② 分镜文字 | look 偏南 18° / 29°（28 mm），按几何柜台东南角在 u≈0.04（st8），st9 柜台全部在画外；文字和首帧都写画左是熟食铺门脸（st8 首帧柜台占 u0.03–0.33）。st8 overhead_ref 的扇形只画了约 9 m 长，驴车、店主、横街口都在扇形外 | look 改为接近正东，或机位往北挪，重出 overhead_ref（便宜） |
  | s6_st6 | 9.4–12s | F3·F6 | 记录 | ③ prompt 或首帧 | overhead 里石楼梯在西南（朝南看是画右），Riley 却往东走到 (6.8,0.9)，终点压在「院里的货车」块上；文字和首帧写楼梯在画左；st1/st4/st5 楼梯都在西侧 x≈2，st6 院子镜像了 | 改 overhead：终点不压货车，楼梯标到画左，并注明这里有意镜像（便宜） |
  | s8_st4 | 0s | F2·F3 | 记录 | ③ prompt 或首帧 | overhead note 写「热水池在镜头身后」，首帧在画右约三分之一画了池子；圆盆按几何在 u0.17–0.67（大半被她挡住），首帧在 u0–0.33 | overhead note 与首帧二选一对齐（便宜） |
  | s5_st2 | 0–2s | F3 | 记录 | ③ prompt 或首帧 | 文字写第 0 秒在「画右边缘」（几何 u0.99），首帧已在 u≈0.85、离柜台一步，0–2 秒的入画拍被吃掉 | 首帧让她只在画右边缘露半身，或改文字（便宜） |
  | s6_st2 | 全程 | F3 | 记录 | ② 分镜文字 | 油灯 (4.6,6.4) 算出 u=−0.01，在左边框外；文字写「画面左上」，首帧在 u≈0.09 | 机位西移约 0.3 m（便宜） |
  | s8_st9 / st6 / st3 | 0s | F3·F1 | 记录 | ② 分镜文字 | st9 Helvia 实测 u0.83、整个上半身入画，文字写「画右边缘只入画半身」；st6 文字写腰以上，2.19 m、35 mm 取景高 1.27 m，首帧露到脚（几何与首帧一致）；st3 文字写「背影在画面下部」，几何头顶 v0.32，首帧 0.25 | 三处文字按几何改（便宜） |
  | s6_st4 | 0s | F3 | 存疑 | ③ prompt 或首帧 | 大堂门算出 u=1.18，应在画外；首帧画面右中（u≈0.84）有一个透暖光的门洞，不确定是不是大堂门。核实方法：对照 bg6 平面图 | 确认后改图或改 overhead（便宜） |

### I24 严重 · 镜头规格 · F4 节拍秒数
- a（1 分）：s7_st7 prompt 第 16 行写「8 秒前在她手里…10 秒后在凳上」，节拍里放灯是 13.8–15.8 秒；s7_st3 第 16 行写 9.5 秒吹灭，节拍是 12.3 秒；s6_st3 镜头段写 7.9–12.5 秒摊手，节拍是 11.7–16.2 秒。排得下的例子：s8_st1 0–3 秒走 4.23 m（1.41 m/s），s8_st8 1.49 m/s。
- 资料包/prompt.txt 第 16 行「光线」写「8 秒前在她手里…10 秒后灯在床头小凳上」；动作行和 overhead [[beat]] 写 13.8–15.8 秒才放灯。模型可能 8–10 秒就把灯放下，和台词、动作冲突
- prompt 第 16 行写「0–9.5 秒…9.5 秒吹灭后」，节拍是 10.8–12.3 秒吹、12.3 秒灭；台词 goodnight from Pompeii 到 10.5 秒才说完，照光线行出片，话没说完灯就灭了
- 第 0 拍应是攥拳，首帧已经是摊开的手心，等于跳过了攥拳那一拍；手心只有 4 铜 + 1 黄铜 = 5 枚，看点要求的是付后「只剩四枚」
- prompt 镜头段写「7.9–12.5 秒递到胸前的右手和钱」，节拍是 11.7–16.2 秒（说到 this… 起）。7.9 秒她还攥着拳说第一句，模型可能提前摊手
- 第 9 秒才到楼梯顶（y0.7），而镜头 9 秒结束，「拐进走廊、只剩灯光在墙上移动」没有时间演；前段 1.6 级/秒、后段 1.1 级/秒，和 note 写的「步速一致」不符
- 下摇时刻文字写 4.5–6.5 秒，overhead 写 6–8 秒；挪半步 0.35 m 压在 5.8–6.0 秒；夜壶首帧已在画内（u≈0.38、v≈0.92），下摇是多余动作
- 1.5 秒内要回头、点头、走 1.2 m 出画
- 5 秒里排了 7 个动作，探身、拿勺、退回、舀酒只有约 2 秒
- 两个行人 5.5 秒走 3 m（0.55 m/s），5.5 秒时 u0.97 还在画框边上，后面那个还在画内
- 分数：a 1 / b None → 最终 1
  | s7_st7 | 8–15.8s | F4 | 重出 | ② 分镜文字 | 资料包/prompt.txt 第 16 行「光线」写「8 秒前在她手里…10 秒后灯在床头小凳上」；动作行和 overhead [[beat]] 写 13.8–15.8 秒才放灯。模型可能 8–10 秒就把灯放下，和台词、动作冲突 | 光线行的秒数改成 13.8 / 15.8 秒（便宜） |
  | s7_st3 | 9.5–12.3s | F4 | 重出 | ② 分镜文字 | prompt 第 16 行写「0–9.5 秒…9.5 秒吹灭后」，节拍是 10.8–12.3 秒吹、12.3 秒灭；台词 goodnight from Pompeii 到 10.5 秒才说完，照光线行出片，话没说完灯就灭了 | 光线行改成 0–12.3 秒 / 12.3 秒熄灭（便宜） |
  | s5_st3 | 0–1.5s | F4·F8 | 重出 | ③ prompt 或首帧 | 第 0 拍应是攥拳，首帧已经是摊开的手心，等于跳过了攥拳那一拍；手心只有 4 铜 + 1 黄铜 = 5 枚，看点要求的是付后「只剩四枚」 | 重出攥拳的首帧，或改第 0 拍文字；镜头栏改成付后手心数得清（便宜） |
  | s6_st3 | 7.9–16.2s | F4 | 可剪 | ② 分镜文字 | prompt 镜头段写「7.9–12.5 秒递到胸前的右手和钱」，节拍是 11.7–16.2 秒（说到 this… 起）。7.9 秒她还攥着拳说第一句，模型可能提前摊手 | 镜头段改成 11.8–16.2 秒（便宜） |
  | s6_st4 | 4.5–9s | F4 | 记录 | ② 分镜文字 | 第 9 秒才到楼梯顶（y0.7），而镜头 9 秒结束，「拐进走廊、只剩灯光在墙上移动」没有时间演；前段 1.6 级/秒、后段 1.1 级/秒，和 note 写的「步速一致」不符 | 改成 8 秒到顶，或镜长加到 10–11 秒（便宜） |
  | s7_st6 | 4.5–8s | F7·F4 | 记录 | ② 分镜文字 | 下摇时刻文字写 4.5–6.5 秒，overhead 写 6–8 秒；挪半步 0.35 m 压在 5.8–6.0 秒；夜壶首帧已在画内（u≈0.38、v≈0.92），下摇是多余动作 | 统一时刻，或删去这段下摇（便宜） |
  | s8_st10 | 8–9.5s | F4 | 记录 | ② 分镜文字 | 1.5 秒内要回头、点头、走 1.2 m 出画 | 这一拍拉到 2 秒（便宜） |
  | s5_st14 | 2–7s | F4 | 记录 | ② 分镜文字 | 5 秒里排了 7 个动作，探身、拿勺、退回、舀酒只有约 2 秒 | 把喝水后的空闲时间匀一些过来（便宜） |
  | s6_st1 | 0–5.5s | F4 | 记录 | ② 分镜文字 | 两个行人 5.5 秒走 3 m（0.55 m/s），5.5 秒时 u0.97 还在画框边上，后面那个还在画内 | 路径终点延到 x=8.5（便宜） |

### I25 严重 · 镜头规格 · F8 看点画得出来
- a（1 分）：s8_st7 看点是「衬衫干爽了」，prompt 动作行写「衬衫被汗贴在背上」；s5_st8 看点「驴车拐进右边横街」，首帧里没有横街口；s5_st3 看点「只剩四枚」，镜头栏写「钱数不要求数清」，首帧手心是 5 枚；s7_st4「绳床」的绳网全镜被草垫盖住。其余如 s7_st6 夜壶、s6_st2 掌心 1 大币＋3 小钱、s8_st5 刮板和油瓶，首帧都看得见（见问题表）。
- 按 overhead，横街口和近角墙 (11.5,14) 应在 u0.59–0.67；首帧里店主铺子西边的南侧铺面连成一片，看不到横街口和墙角。看点「驴车拐进右边横街」画不出来，overhead note 也记着上一条成片在画内转弯、整车横移、穿模
- spec 第 10 行看点「衬衫干爽了，神清气爽」；prompt 动作行写「衬衫被汗贴在背上，她揪着衬衫前襟抖了抖」，两者相反
- 第 0 拍应是攥拳，首帧已经是摊开的手心，等于跳过了攥拳那一拍；手心只有 4 铜 + 1 黄铜 = 5 枚，看点要求的是付后「只剩四枚」
- 看点写「绳床」，但绳网全镜都被草垫盖住，看不到
- 首帧路人高约 45 px（按 43 m 算应约 52 px，大小大致对），但看起来像走在屋顶那一层，看不出是窄街
- 分数：a 1 / b None → 最终 1
  | s5_st8 | 0–8s | F3·F7·F8 | 重出 | ③ prompt 或首帧 | 按 overhead，横街口和近角墙 (11.5,14) 应在 u0.59–0.67；首帧里店主铺子西边的南侧铺面连成一片，看不到横街口和墙角。看点「驴车拐进右边横街」画不出来，overhead note 也记着上一条成片在画内转弯、整车横移、穿模 | 重出首帧，在 u≈0.6–0.67 画出横街口和挡车的墙角（便宜） |
  | s8_st7 | 2–3s | F8 | 重出 | ② 分镜文字 | spec 第 10 行看点「衬衫干爽了，神清气爽」；prompt 动作行写「衬衫被汗贴在背上，她揪着衬衫前襟抖了抖」，两者相反 | 统一成「衬衫干爽、抖一抖前襟透气」（便宜） |
  | s5_st3 | 0–1.5s | F4·F8 | 重出 | ③ prompt 或首帧 | 第 0 拍应是攥拳，首帧已经是摊开的手心，等于跳过了攥拳那一拍；手心只有 4 铜 + 1 黄铜 = 5 枚，看点要求的是付后「只剩四枚」 | 重出攥拳的首帧，或改第 0 拍文字；镜头栏改成付后手心数得清（便宜） |
  | s7_st4 | 4.3–6.3s | F8 | 记录 | ② 分镜文字 | 看点写「绳床」，但绳网全镜都被草垫盖住，看不到 | 看点改为「草垫床」，或写成床沿露出绳网（便宜） |
  | s7_st5 | 0–4s | F8 | 存疑 | ③ prompt 或首帧 | 首帧路人高约 45 px（按 43 m 算应约 52 px，大小大致对），但看起来像走在屋顶那一层，看不出是窄街 | 首帧补出明显的街槽（便宜） |

### I26 严重 · Prompt 文本 · T1 自相矛盾
- a（1 分）：s1_st1 的 prompt.txt 画面行、镜头行都要「她自己的相机架在沙滩上录着」「她把这台相机拿了起来」，负面词行却写了「相机，手机，自拍杆」；bible.md:30 明文给 EP1 s1 st1 开了例外，负面词没跟着改（见问题 1）。另外 s3_st5 正文要「一缕淡淡的炉烟」，负面词有「烟柱，白烟，浓烟」；s8_st3/4/5/6/8/9 正文要「白色蒸汽／浓蒸汽」，负面词有「白烟，浓烟，升上天空的蒸汽」，措辞相近（问题 6）。其余 55 镜的正文名词与负面词逐词比对没有命中。
- 正文要「自己的相机架在沙滩上录着」「她把这台相机拿了起来」，负面词写「相机，手机，自拍杆」。bible.md:30 已给这一镜开例外，编译器仍套了剧级负面词。模型可能不让 21–22 秒的拿相机动作出现，或把相机当禁区。
- 正文要「炉烟」「白色蒸汽／浓蒸汽」，负面词有「白烟，浓烟，烟柱，升上天空的蒸汽」。负面意图是室外烟柱，措辞会连带压住室内雾气。核实：出片后看 s8_st4 的热水室雾气是否还在。
- 分数：a 1 / b None → 最终 1
  | s1_st1 | 0–22 秒（全镜） | T1 自相矛盾 | 重出（出片前必改） | ③ prompt（负面词） | 正文要「自己的相机架在沙滩上录着」「她把这台相机拿了起来」，负面词写「相机，手机，自拍杆」。bible.md:30 已给这一镜开例外，编译器仍套了剧级负面词。模型可能不让 21–22 秒的拿相机动作出现，或把相机当禁区。 | 便宜：本镜负面词删「相机」，保留「手机，自拍杆」；最好在编译器里做按镜例外。 |
  | s3_st5；s8_st3/4/5/6/8/9 | s3_st5 3–6 秒炉口；s8 全镜（热水室蒸汽） | T1 自相矛盾（近义） | 存疑 | ③ prompt（负面词） | 正文要「炉烟」「白色蒸汽／浓蒸汽」，负面词有「白烟，浓烟，烟柱，升上天空的蒸汽」。负面意图是室外烟柱，措辞会连带压住室内雾气。核实：出片后看 s8_st4 的热水室雾气是否还在。 | 便宜：把「白烟，浓烟」改成「烟柱，升上天空的白烟」；s8 各镜正文加「室内雾气」。 |

### I27 严重 · Prompt 文本 · T4 图文一致
- a（1 分）：s5_st3 首帧图（upload/01_image1.jpg）里 Riley 的手已经摊开、手心朝上托着几枚钱，伸向 Asellina；prompt 动作行第 0 秒写的是「右手攥成拳伸在台面上方，钱在拳头里……1.5–3.5 秒才摊开」（问题 3）。s5_st3 首帧手心里的红铜币我数约 4 枚，文字写 5 枚红铜加 1 枚大黄铜币，存疑。其余看过的首帧：s1_st1（海在左、两条船在右、城门在左上）、s3_st5（蒙眼驴、两座石磨、台面面包）、s3_st6（托板 5 个面包下三上二、陶碗 2 枚钱）、s7_st1（坐床边、手放膝盖、油灯在左）、s2_st1（垫脚石、脏水）都与文字一致。
- 首帧是摊开手心托钱，文字写第 0 秒攥拳，1.5 秒才摊开。首帧「视频从这张图开始」，模型会按图不按字。
- 分数：a 1 / b None → 最终 1
  | s5_st3 | 0–1.5 秒（首帧） | T4 图文一致 | 重出（首帧文字二选一） | ③ 首帧或 prompt | 首帧是摊开手心托钱，文字写第 0 秒攥拳，1.5 秒才摊开。首帧「视频从这张图开始」，模型会按图不按字。 | 便宜：重出首帧成攥拳，或把动作行第 0 秒改成「手心朝上摊开，钱在手心里」，去掉攥拳那一拍。 |

### I28 严重 · 角色立场·Riley · V1 语言
- a（1 分）：s3_st4 1.1–1.7 秒对面包师只说一个词「Garum?」（已知问题）。s5_st11 1.6–11.4 秒对 Asellina 讲一整串英文，却没用手指比 1 和 2，她看不出我在问什么。整集对帮过我的人一句 thank you 都没说（s3_st1、s3_st7、s5_st4、s6_st5、s8_st5）。学会的 Salve 一次也没再用。s4_st1 2.6–4.9 秒在别人的作坊里大声嚷（见问题表）
- 只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人
- s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴
- 整集别人给我面包、替我打包、倒鱼露、递灯、滴油递刮板，我从来不说一句 thank you，只「笑笑 / 点头」。一个爱说话的美国女孩，被人帮了会脱口说谢谢，对方听不懂也会说
- 早上从 Felix 那里学会 Salve，之后进浴场、到熟食铺、到大车店，一次也没再用。s8_st2 还写着我站在低头的门房面前「两手垂在身侧，不比划」，干等她发现我
- 我对 Asellina 讲完整的英文长句「one coin gets you the cheap stuff, and two gets you the good stuff? Is that what you're saying?」，只是点头，最后比一个 OK。她听不懂英文，看不出我在问「一枚还是两枚」
- Vibia 就在我左肩后约 1 米，我当着她的面拿她开玩笑，分镜只写「忍着笑」，没写音量
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 1–17 | V1·V4·V6（已知 15/15b） | 重出 | ① 故事 | 只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人 | 已知，等用户在 story_beats.md 选改法。站在我的立场：此刻的我会边说「Garum? Uh… where?」边做倒酱的手势，摊手四下看。听到 dextram 后，左右各指一下问「This way? That way?」，等他用手指路（便宜） |
  | s4_st1 | 0–5.7 | V6·V2·V1 | 重出 | ② 分镜文字 | s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴 | 此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字） |
  | s3_st1、s3_st7、s5_st4/st13、s6_st5、s8_st5/st9 | s3_st1 11.7–13；s3_st7 11–13；s6_st5 7.5–8.5；s8_st5 13–14 | V1·V5 | 可剪 | ① 故事 | 整集别人给我面包、替我打包、倒鱼露、递灯、滴油递刮板，我从来不说一句 thank you，只「笑笑 / 点头」。一个爱说话的美国女孩，被人帮了会脱口说谢谢，对方听不懂也会说 | 此刻的我：s3_st7 布包递过来时说「Oh — thank you!」，手按胸口点一下头；s8_st9 递回刮板时小声说「Thank you.」。其余镜头用手按胸口加点头代替，不必每镜都开口（便宜，加半句台词或一个动作） |
  | s8_st2、s5_st2、s6_st1 | s8_st2 0–3；s5_st2 0–2；s6_st1 3.5–5 | V1·V2·V7 | 可剪 | ② 分镜文字 | 早上从 Felix 那里学会 Salve，之后进浴场、到熟食铺、到大车店，一次也没再用。s8_st2 还写着我站在低头的门房面前「两手垂在身侧，不比划」，干等她发现我 | 此刻的我：走到门房面前先开口「Salve!」，这次读对一点，带点得意；门房因为这声才抬头（不是因为脚步声）。s5_st2 或 s6_st1 也可以再用一次，是全集唯一学到手的词（便宜） |
  | s5_st11 | 1.6–11.4 | V1 | 可剪 | ② 分镜文字 | 我对 Asellina 讲完整的英文长句「one coin gets you the cheap stuff, and two gets you the good stuff? Is that what you're saying?」，只是点头，最后比一个 OK。她听不懂英文，看不出我在问「一枚还是两枚」 | 此刻的我：说「one…」时竖一根手指、朝前排那只罐子一点；说「two…」时竖两根手指、朝她扬下巴示意的那只带木盖的罐子一点，配一个「好喝？」的表情；最后才比 OK（便宜） |
  | s2_st8 | 3.5–8 | V1 | 记录 | ② 分镜文字 | Vibia 就在我左肩后约 1 米，我当着她的面拿她开玩笑，分镜只写「忍着笑」，没写音量 | 此刻的我：压低声音、凑近镜头说「Yeah… I don't think she's a fan of the pants.」（便宜） |

### I29 严重 · 角色立场·Riley · V2 肢体
- a（1 分）：s4_st1 2.5–5.7 秒手垂在身侧张大嘴嚷完，才去捏鼻子，反射顺序反了。s8_st2 0–3 秒站在没注意到我的门房面前不吭声，「两手垂在身侧，不比划」。s5_st12 首帧 OK 手势举在脸边朝上，没有伸向柜台（见问题表）
- s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴
- 早上从 Felix 那里学会 Salve，之后进浴场、到熟食铺、到大车店，一次也没再用。s8_st2 还写着我站在低头的门房面前「两手垂在身侧，不比划」，干等她发现我
- 首帧里 OK 手势举在脸边、朝上，像在打招呼，不是分镜写的「伸向柜台里，挑眉等着」
- 分数：a 1 / b None → 最终 1
  | s4_st1 | 0–5.7 | V6·V2·V1 | 重出 | ② 分镜文字 | s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴 | 此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字） |
  | s8_st2、s5_st2、s6_st1 | s8_st2 0–3；s5_st2 0–2；s6_st1 3.5–5 | V1·V2·V7 | 可剪 | ② 分镜文字 | 早上从 Felix 那里学会 Salve，之后进浴场、到熟食铺、到大车店，一次也没再用。s8_st2 还写着我站在低头的门房面前「两手垂在身侧，不比划」，干等她发现我 | 此刻的我：走到门房面前先开口「Salve!」，这次读对一点，带点得意；门房因为这声才抬头（不是因为脚步声）。s5_st2 或 s6_st1 也可以再用一次，是全集唯一学到手的词（便宜） |
  | s5_st12 | 首帧 0 秒 | V2 | 记录 | ③ prompt 或首帧 | 首帧里 OK 手势举在脸边、朝上，像在打招呼，不是分镜写的「伸向柜台里，挑眉等着」 | 此刻的我：手比着 OK 往前伸到柜台上方、朝向她，身子微微前探，挑眉等回答（便宜） |

### I30 严重 · 角色立场·Riley · V6 动机
- a（1 分）：s8_st2 6–8 秒我果断挑了最小那枚钱交门票，到 s8_st10 1.1–6.4 秒又惊讶「只要一枚小钱」，前后矛盾。s4_st1 1.5–2.5 秒在 s4_st3 已经被熏得皱脸之后，反而走进去深吸一口气。s6_st3 19.6 秒「什么动静」没写是什么。s8_st3、s8_st8 一直穿着衣服，看不到我自己做了这个决定。s7_st4–st3 一个人住店，从来不看门闩（见问题表）
- 只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人
- s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴
- s8_st2 我「用右手捏起那枚最小的浅色小铜币」，很果断，说明我知道票价；s8_st10 又「又惊又喜」地说「literally one tiny coin… That's it!」。知道就不会惊讶，不知道就不会这么果断
- 「像被画面左边、镜头身后的什么动静吸引」没写是什么。Fortunata 的吆喝在 s6_st1 的 1.5–3.0 秒，比我转头还晚，我转头的理由画面里不存在
- 更衣厅里人人裹着亚麻长衣，墙上壁龛放着衣服，我「有点不知所措」，然后穿着全套衣服和靴子走进热水室；到 s8_st4 才说「Why did I keep my clothes on?」。决定穿着衣服的那一刻画面里没有
- 我一个女人独自住大车店，楼下坐着陌生车夫，进屋关上门。分镜反复写「门板内侧两个空着的木闩座」，我却从来没去看门闩、没想锁门
- 我身上只剩 4 枚钱，开口要鱼露，却一点「要不要钱」的表示都没有。Asellina 拿罐就倒，我连问都没问
- 我早上连 dextram 都听不懂，晚上却瞥一眼墙上的拉丁文刻痕就认出了课本里那句，还逐字翻译出来。认出的过程画面里没有：灯在凳子上，我只是回头看一眼
- 我第一次买东西，不知道价钱，却直接捏出正好 2 枚放下，不看他的反应
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 1–17 | V1·V4·V6（已知 15/15b） | 重出 | ① 故事 | 只问一个词「Garum?」。Felix 说完后，我 7 秒就转身对镜头赌「left」，没利用眼前这个能问的人 | 已知，等用户在 story_beats.md 选改法。站在我的立场：此刻的我会边说「Garum? Uh… where?」边做倒酱的手势，摊手四下看。听到 dextram 后，左右各指一下问「This way? That way?」，等他用手指路（便宜） |
  | s4_st1 | 0–5.7 | V6·V2·V1 | 重出 | ② 分镜文字 | s4_st3 8.5–12 秒我已经被熏得「脸皱成一团」，s4_st1 却一路走进门厅最里面，1.5 秒还「深吸一口气」才被熏到。2.6–4.9 秒「手垂在身侧」张大嘴大声嚷完，5.7 秒才捏鼻子。这是为了露出嘴在倒排顺序，可捏鼻子本来就不挡嘴 | 此刻的我：被踩水声和人吸引，走到门口探头；憋着的气憋不住，换了一口，马上捏住鼻子往后一缩，用捏着鼻子的鼻音压低声音说「Oh — oh no. That's pee.」，嘴照样露着，鼻音还更好笑。不在人家作坊里大声嚷（便宜，改文字） |
  | s8_st2→s8_st10 | st2 6–8；st10 1.1–6.4 | V6 | 重出 | ② 分镜文字 | s8_st2 我「用右手捏起那枚最小的浅色小铜币」，很果断，说明我知道票价；s8_st10 又「又惊又喜」地说「literally one tiny coin… That's it!」。知道就不会惊讶，不知道就不会这么果断 | 此刻的我：把一手钱摊给门房看，挑起眉等她拿；或者先试探着递出最小那枚，手停在半空等她反应，见她收下才松手，所以下一镜才惊喜（便宜） |
  | s6_st3 | 19.6–20.6 | V6 | 可剪 | ② 分镜文字 | 「像被画面左边、镜头身后的什么动静吸引」没写是什么。Fortunata 的吆喝在 s6_st1 的 1.5–3.0 秒，比我转头还晚，我转头的理由画面里不存在 | 此刻的我：19.4 秒画外传来一个女人低沉的吆喝和骡子的响鼻、车轮声，我转头一看，眼睛一亮，因为大车进出的大门就是旅店。在 s6_st3 的音效里写明这声吆喝（便宜） |
  | s8_st3、s8_st8 | st3 2.5–4；st8 4–5 | V6 | 记录 | ① 故事 | 更衣厅里人人裹着亚麻长衣，墙上壁龛放着衣服，我「有点不知所措」，然后穿着全套衣服和靴子走进热水室；到 s8_st4 才说「Why did I keep my clothes on?」。决定穿着衣服的那一刻画面里没有 | 此刻的我：s8_st8 被盯着时，眼睛扫一下壁龛里叠好的衣服，手摸到衬衫最上面那颗扣子犹豫一下，又松开，脸一红，干脆快步往里走。这样「Rookie mistake」才是我自己选的（便宜） |
  | s7_st4–s7_st3 | st4 2.2–3.6；st6 全镜 | V6 | 记录 | ① 故事 | 我一个女人独自住大车店，楼下坐着陌生车夫，进屋关上门。分镜反复写「门板内侧两个空着的木闩座」，我却从来没去看门闩、没想锁门 | 此刻的我：s7_st4 推上门后顺手摸一下门边，发现没有闩，愣一下；s7_st6 讲完空调和厕所，补一句「…and no lock. Cool cool cool.」，或者拿凳子顶住门。这也接上「Cool cool cool」的笑点（便宜，属故事层要用户定） |
  | s5_st13 | 7.5–11.3 | V6 | 记录 | ① 故事 | 我身上只剩 4 枚钱，开口要鱼露，却一点「要不要钱」的表示都没有。Asellina 拿罐就倒，我连问都没问 | 此刻的我：问完「Garum?」，手往裤袋那边一摸、挑眉看她；她摆摆手，拿罐就倒。这样她的大方也看得见（便宜） |
  | s7_st2 | 0–18.1 | V6·V7 | 存疑 | ① 故事 | 我早上连 dextram 都听不懂，晚上却瞥一眼墙上的拉丁文刻痕就认出了课本里那句，还逐字翻译出来。认出的过程画面里没有：灯在凳子上，我只是回头看一眼 | 此刻的我：端起灯凑近墙，眯眼用手指描着字母，念出「Vi-bi-us… Re-sti-tu-tus」，认出人名才说「I swear this was in my history textbook」。剧级规定不出现可读文字，要核实凑近照明会不会让字显形（便宜） |
  | s3_st1 | 6.3–9 | V6 | 记录 | ② 分镜文字 | 我第一次买东西，不知道价钱，却直接捏出正好 2 枚放下，不看他的反应 | 此刻的我：放下 2 枚后抬眼看 Felix、挑眉，意思是「够吗？」；他点头，我才松口气笑（便宜） |

### I31 严重 · 角色立场·Felix · V1 语言
- a（1 分）：st4 2.3–5.2s 对着明知听不懂拉丁语的人飞快说整句（已知 15）；另外 "Hac recta platea" 在东西向街上不配朝向就没指出往哪头走（新）；st7、st8 交接和告别全程不出声，和人物卡「嗓门大」不符（见问题表）
- 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来
- 她挥手告别，我两手端托板，整镜只有街上的环境声，不回一句
- 整镜「两人都安静」，13 秒交接没有一句话；人物卡写的是嗓门大
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 2.3–5.2 | V1·V4·V2 | 重出 | ① 故事 | 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来 | 便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路 |
  | s3_st8 | 0–1.5 | V1·V5 | 可剪 | ② 分镜文字 | 她挥手告别，我两手端托板，整镜只有街上的环境声，不回一句 | 便宜：改文字。此刻的我会下巴一扬、喊 "Vale!"（洪亮带笑） |
  | s3_st7 | 0–13 | V1 | 记录 | ② 分镜文字 | 整镜「两人都安静」，13 秒交接没有一句话；人物卡写的是嗓门大 | 便宜：打包前下巴朝面包一努问 "Hmm?"，递布包时说 "Tene!" |

### I32 严重 · 角色立场·Felix · V2 肢体
- a（1 分）：st4 17–18.5s「两手把托板重新端起来」，托板从 st4 0s 端到 st6 5.5s 约 34 秒，只为剧情让我手占着；st4 指路零手势，和人物卡「整条胳膊比划」相反（见问题表）
- 托板约 34 秒不离手；st4 17–18.5s「两手把托板重新端起来」，搁下了又端起，只为了让我腾不出手；st6 5.5s 才放下
- 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来
- 分数：a 1 / b None → 最终 1
  | s3_st4→st8→st6 | st4 0–20 / st8 0–9 / st6 0–5.5 | V2·V6 | 重出 | ① 故事 / ② 分镜文字 | 托板约 34 秒不离手；st4 17–18.5s「两手把托板重新端起来」，搁下了又端起，只为了让我腾不出手；st6 5.5s 才放下 | 便宜：改文字。st7 结尾端来托板后，st4 一开场就放在石台上（或者搁上就不再端起），我手是空的；配合 story_beats 15 的 B 方案（腾手朝他自己的右边一指，形成镜像误会）最自然 |
  | s3_st4 | 2.3–5.2 | V1·V4·V2 | 重出 | ① 故事 | 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来 | 便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路 |

### I33 严重 · 角色立场·Felix · V3 表情
- a（1 分）：st6 1.5–3.5s 张嘴吸气、咽回、再笑出声（已知 15b，过演）；st1 首帧画左 Felix 还没看见 Riley 就对面包咧嘴笑，与节拍「说完才咧嘴笑」不符（小）；st5、st7 6–7s 的表情强度合适
- st8 6–9s 我已经摇头认了、拨正了面包，st6 0–2.5s 目光又追过去、吸气想喊，冲动排在放弃之后，顺序反了；st6 表情过演（已知 15b）
- `st1_first_frame.png` 画左 Felix 低头摞面包时已经在咧嘴笑，节拍写的是「说完才咧嘴笑」
- 分数：a 1 / b None → 最终 1
  | s3_st8→st6 | st8 6–9 / st6 0–3.5 | V5·V3 | 重出 | ② 分镜文字 | st8 6–9s 我已经摇头认了、拨正了面包，st6 0–2.5s 目光又追过去、吸气想喊，冲动排在放弃之后，顺序反了；st6 表情过演（已知 15b） | 便宜：按 15b 的 A 方案删 st6，或者把「想喊又停」挪进 st8 后景，st6 只留低头放托板 |
  | s3_st1 | 0（首帧） | V3 | 记录 | ③ 首帧 | `st1_first_frame.png` 画左 Felix 低头摞面包时已经在咧嘴笑，节拍写的是「说完才咧嘴笑」 | 便宜：首帧改成专心干活的平常脸 |

### I34 严重 · 角色立场·Felix · V4 视线
- a（1 分）：st4 2–5.5s 被问话时头不抬、眼睛只看托板（已知 15）；st1 1.5s 抬头从没看过她的裤子和靴子，「觉得穿裤子好玩」只停在作者说明里；st7 7–8.5s 递布包时看着她 ✓、st8 0–1.5s 看着她挥手 ✓
- 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来
- 「觉得这个穿裤子的外地姑娘很好玩」只写在配角说明里，画面里我从没看过她的裤子和靴子
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 2.3–5.2 | V1·V4·V2 | 重出 | ① 故事 | 已知节点 15（头不抬、不比划、飞快说）。另补一条：「Hac recta platea」在东西向街上不配朝向，没指出往哪头走，就算她懂拉丁语也走不对，这句话本身就没把路说出来 | 便宜：按 story_beats 15 挑 A/B/C；无论哪个方案，台词都要配一个看得见的朝向（下巴、手或眼神），先说 "Garum? Non hic." 再指路 |
  | s3_st1 | 1.5–2.2 | V4·V6 | 记录 | ② 分镜文字 | 「觉得这个穿裤子的外地姑娘很好玩」只写在配角说明里，画面里我从没看过她的裤子和靴子 | 便宜：抬头时目光先往下扫一眼她的裤子和靴子、挑一下眉，再喊 Salve |

### I35 严重 · 角色立场·Felix · V5 回应
- a（1 分）：st4 8–17s 对听不懂的英语 Fifty-fifty、left 卡着点反应（嘴角动、鼓腮憋笑、摇头）；st8 0–1.5s 她挥手告别我不回 Vale；st8 6–9s 已经摇头认了，st6 0–2.5s 又想喊她，反应顺序反了
- 动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同样写了；Felix 只说拉丁语（人物卡），听不懂 left / Fifty-fifty，也不可能知道她猜反了，这是在替观众演
- st8 6–9s 我已经摇头认了、拨正了面包，st6 0–2.5s 目光又追过去、吸气想喊，冲动排在放弃之后，顺序反了；st6 表情过演（已知 15b）
- 她挥手告别，我两手端托板，整镜只有街上的环境声，不回一句
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 8–18.5 | V5·V6 | 重出 | ② 分镜文字 | 动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同样写了；Felix 只说拉丁语（人物卡），听不懂 left / Fifty-fifty，也不可能知道她猜反了，这是在替观众演 | 便宜：改文字。此刻的我会在她 7–8s 转身对空街说话时停手，看她、顺着她的视线看一眼空街，皱眉憋笑轻摇头（觉得这外地人怪），然后接着干活，反应不对齐 left；只保留听到 dextram 时抬眼 |
  | s3_st8→st6 | st8 6–9 / st6 0–3.5 | V5·V3 | 重出 | ② 分镜文字 | st8 6–9s 我已经摇头认了、拨正了面包，st6 0–2.5s 目光又追过去、吸气想喊，冲动排在放弃之后，顺序反了；st6 表情过演（已知 15b） | 便宜：按 15b 的 A 方案删 st6，或者把「想喊又停」挪进 st8 后景，st6 只留低头放托板 |
  | s3_st8 | 0–1.5 | V1·V5 | 可剪 | ② 分镜文字 | 她挥手告别，我两手端托板，整镜只有街上的环境声，不回一句 | 便宜：改文字。此刻的我会下巴一扬、喊 "Vale!"（洪亮带笑） |

### I36 严重 · 角色立场·Felix · V6 动机
- a（1 分）：st4 托板放下又端起、不比划，这两件都是为了「让她猜不出方向」的剧情需要；st4 17–18.5s 的憋笑建立在我不可能知道的信息上；st8 看出她走错却不喊，镜里没有看得见的理由；st1 收钱拿面包 9–11.7s、st7 打包的动机成立
- 动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同样写了；Felix 只说拉丁语（人物卡），听不懂 left / Fifty-fifty，也不可能知道她猜反了，这是在替观众演
- 托板约 34 秒不离手；st4 17–18.5s「两手把托板重新端起来」，搁下了又端起，只为了让我腾不出手；st6 5.5s 才放下
- 我是热心的大嗓门，看出她走错，人就在五六米外，却只是摇头。镜里没有不喊的理由
- 「觉得这个穿裤子的外地姑娘很好玩」只写在配角说明里，画面里我从没看过她的裤子和靴子
- 分数：a 1 / b None → 最终 1
  | s3_st4 | 8–18.5 | V5·V6 | 重出 | ② 分镜文字 | 动作「说到 Fifty-fifty 时他嘴角一动，她说出 left 时他鼓起腮帮憋住笑、轻轻摇头」，st4 prompt.txt 同样写了；Felix 只说拉丁语（人物卡），听不懂 left / Fifty-fifty，也不可能知道她猜反了，这是在替观众演 | 便宜：改文字。此刻的我会在她 7–8s 转身对空街说话时停手，看她、顺着她的视线看一眼空街，皱眉憋笑轻摇头（觉得这外地人怪），然后接着干活，反应不对齐 left；只保留听到 dextram 时抬眼 |
  | s3_st4→st8→st6 | st4 0–20 / st8 0–9 / st6 0–5.5 | V2·V6 | 重出 | ① 故事 / ② 分镜文字 | 托板约 34 秒不离手；st4 17–18.5s「两手把托板重新端起来」，搁下了又端起，只为了让我腾不出手；st6 5.5s 才放下 | 便宜：改文字。st7 结尾端来托板后，st4 一开场就放在石台上（或者搁上就不再端起），我手是空的；配合 story_beats 15 的 B 方案（腾手朝他自己的右边一指，形成镜像误会）最自然 |
  | s3_st8 | 6–9 | V6 | 可剪 | ① 故事 | 我是热心的大嗓门，看出她走错，人就在五六米外，却只是摇头。镜里没有不喊的理由 | 便宜：加一个看得见的理由，比如喊一声 "Heus! Dextram!" 被经过的驴车 / 母子盖住，或者她已经拐出去，我再耸肩笑 |
  | s3_st1 | 1.5–2.2 | V4·V6 | 记录 | ② 分镜文字 | 「觉得这个穿裤子的外地姑娘很好玩」只写在配角说明里，画面里我从没看过她的裤子和靴子 | 便宜：抬头时目光先往下扫一眼她的裤子和靴子、挑一下眉，再喊 Salve |

### I37 严重 · 角色立场·Tertius · V5 回应
- a（1 分）：见问题表 #1、#4——2.6 秒她在 2.79 米外大喊，我到 5.0 秒才扭头，迟 2.4 秒；7.2–13 秒（工友笑、她举手投降回头看我、她认怂退出）分镜一个字没写我怎么回应
- 节拍写 2.5–5 秒她大声嚷 "Oh — oh no. That's pee!"（2.6–4.9 秒），我在 5–5.7 秒才「扭头看见她」；俯视图我在 (5,6.2)、她在 (7.6,7.2)，相距 2.79 m。和 s3 面包师「被问路头也不抬」同类
- 7.2 秒后的节拍、走位、配角说明都没写 Tertius；10.8–13 秒「工人们接着踩布」不明确含不含他。旧片审核记录 11.1 秒起 Tertius 被挪到压布机后面，正是他「无人管」的那段
- 分数：a 1 / b None → 最终 1
  | s4_st1 | 2.6–5.0 | V5 回应 | 重出 | ② 分镜文字 | 节拍写 2.5–5 秒她大声嚷 "Oh — oh no. That's pee!"（2.6–4.9 秒），我在 5–5.7 秒才「扭头看见她」；俯视图我在 (5,6.2)、她在 (7.6,7.2)，相距 2.79 m。和 s3 面包师「被问路头也不抬」同类 | 此刻的我会：她 "Oh —" 一出口就扭头；利用她 "oh no" 前的那一顿（约 3.0–3.4 秒）作为我的单独一拍——「Tertius 停下脚，转过上身看向她，皱紧眉」，之后一直看着她直到她出门；5–5.7 秒那拍改成「Tertius 盯着她，下巴一抬」。**便宜**（改分镜文字＋首帧不变）；已保留的旧片（20261108-223157，Tertius 约 6.5 秒才扭头）要改则**要积分** |
  | s4_st1 | 7.2–13 | V5 回应 | 记录 | ② 分镜文字 | 7.2 秒后的节拍、走位、配角说明都没写 Tertius；10.8–13 秒「工人们接着踩布」不明确含不含他。旧片审核记录 11.1 秒起 Tertius 被挪到压布机后面，正是他「无人管」的那段 | 此刻的我会：7.2–8 秒余光瞥一眼笑的工友、嘴角一撇；8–8.8 秒她回头瞥我，我瞪着她、下巴朝门口一扬；8.8–10.8 秒手放下、哼一声、仍看着她；10.8 秒起低头接着踩。写进节拍并加「Tertius 全程留在他的单人小石槽里」。**便宜** |

### I38 严重 · 角色立场·Fortunata · V2（站位）· prompt
- 三镜 prompt.txt 第 8–9 行：Riley＝「overhead 里的蓝色圆点」、女店主＝「黄色圆点」；三张 overhead 图例与图上都是 Fortunata 蓝、Riley 黄。颜色标反，模型可能把我放到 Riley 的位置
  | s6_st1/st2/st5 | 全镜 | V2（站位）· prompt | 重出 | ③ prompt | 三镜 prompt.txt 第 8–9 行：Riley＝「overhead 里的蓝色圆点」、女店主＝「黄色圆点」；三张 overhead 图例与图上都是 Fortunata 蓝、Riley 黄。颜色标反，模型可能把我放到 Riley 的位置 | 便宜：修 prompt 编译里的颜色映射（或 overhead 配色），重编三镜 prompt |

### I39 严重 · 角色立场·Vibia · V3 表情
- a（1 分）：st5 4.2–5.2 秒挑眉＋撇嘴＋摇头叠在 3.2–4.2 秒愣＋再看之后，2 秒五个表情动作，过演；st4「嘴角还撇着」把同一嫌弃表情挂过 st8 整 11 秒；st5 俯视图写 5–7 秒「一动不动」盯着看（见问题表）
- `st5_overhead.png` 时间轴「3.4–5s 表情愣住、困惑、嘴抿着；5–7s 她就那样盯着看……两手扶着满水罐，一动不动」，与 spec「全程手上有活，不定住」、5.2–7 秒抽布擦罐相反；分段秒数也和 spec 不同（2.6/3.4 vs 2.4/3.2）。该图作为 `@图片2` 送模
- 「愣一下、又飞快地再看一眼」＋「挑起一边眉毛、撇撇嘴、轻轻摇一下头」，2 秒内五个评判动作，摇头是冲陌生人当面表态
- 「嘴角还撇着」延续自 st5 4.2 秒，跨过 st8 整 11 秒；陌生人一臂宽擦身而过，我身体毫无反应
- 分数：a 1 / b None → 最终 1
  | s2_st5 | 0–7（俯视图） | V3 / V5 送模参考图过期 | 重出 | ③ prompt 或首帧 | `st5_overhead.png` 时间轴「3.4–5s 表情愣住、困惑、嘴抿着；5–7s 她就那样盯着看……两手扶着满水罐，一动不动」，与 spec「全程手上有活，不定住」、5.2–7 秒抽布擦罐相反；分段秒数也和 spec 不同（2.6/3.4 vs 2.4/3.2）。该图作为 `@图片2` 送模 | 便宜：按现行 spec 重生成俯视图（`python tools/shot_pack.py sync episodes/ep01 s2_st5` 一类），核对时间轴文字 |
  | s2_st5 | 3.2–5.2 | V3 表情过演 | 可剪 | ② 分镜文字 | 「愣一下、又飞快地再看一眼」＋「挑起一边眉毛、撇撇嘴、轻轻摇一下头」，2 秒内五个评判动作，摇头是冲陌生人当面表态 | 便宜：改为「目光落到腿上停住半拍，眉毛挑起、嘴角往下一压，干脆扭回身」，删当面摇头；摇头挪到 st4 她走过之后（她看不见时） |
  | s2_st4 | 0–1.5 | V3 / V2 表情挂太久、身体无避让 | 记录 | ② 分镜文字 | 「嘴角还撇着」延续自 st5 4.2 秒，跨过 st8 整 11 秒；陌生人一臂宽擦身而过，我身体毫无反应 | 便宜：删「嘴角还撇着」，改「她擦身过去时肩膀往墙边一收、左手护一下罐耳，眼睛仍不抬」 |

### I40 严重 · 角色立场·Vibia · V5 回应
- a（1 分）：st5 2.4 秒「听见身后有人大声说外国话」但 prompt 首末行「本镜没有人说话」、台词无，触发我回头的声音不存在；st8 1–2 秒「只抬眼瞄半秒、眉毛一挑」与同一 prompt 配角段「挑眉看一眼、轻轻摇头」冲突；st8 俯视图 2.5–3.5 秒要我再从腰带抽布（见问题表）
- spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」；上一镜 s2_st2 16.5–18 秒 Riley 已闭嘴（junctions 第 66 行）。成片里我会在静默中无故回头
- `st5_overhead.png` 时间轴「3.4–5s 表情愣住、困惑、嘴抿着；5–7s 她就那样盯着看……两手扶着满水罐，一动不动」，与 spec「全程手上有活，不定住」、5.2–7 秒抽布擦罐相反；分段秒数也和 spec 不同（2.6/3.4 vs 2.4/3.2）。该图作为 `@图片2` 送模
- `st8_overhead.png` 时间轴「2.5–3.5s 女人把头扭开，从腰带里抽出一小块布，低头擦罐身」，抬头说明「直腰扶着满水罐，挑眉撇嘴」；但 st5 5.2 秒已抽布、st8 第 0 秒布在我手里（首帧画右可见）。按图演我会第二次抽布；台词时间也不同（4.4–8.7 vs 3.6–7.9 秒）
- 同一 prompt：节拍「只抬眼瞄半秒、眉毛一挑」vs 配角段「挑起眉毛看她一眼、轻轻摇头」；配角段「之后一直擦罐、偶尔瞄一眼」vs 8–11 秒「没再看她」
- 分数：a 1 / b None → 最终 1
  | s2_st5 | 2.4–3.2 | V5 / V6 回应缺触发 | 重出 | ② 分镜文字 | spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」；上一镜 s2_st2 16.5–18 秒 Riley 已闭嘴（junctions 第 66 行）。成片里我会在静默中无故回头 | 便宜：st5 给 Riley 加一段画外声（如 2.0–2.6 秒一句含糊的 "Okay…" 或一声笑，标「画外、听不清」），声音行改成「画外有人说话」；或把 s2_st2 的尾句延到 st5 开头做音频前搭（剪辑处理）。我的动作改为「手上一顿 → 直腰 → 扭头找声音」 |
  | s2_st5 | 0–7（俯视图） | V3 / V5 送模参考图过期 | 重出 | ③ prompt 或首帧 | `st5_overhead.png` 时间轴「3.4–5s 表情愣住、困惑、嘴抿着；5–7s 她就那样盯着看……两手扶着满水罐，一动不动」，与 spec「全程手上有活，不定住」、5.2–7 秒抽布擦罐相反；分段秒数也和 spec 不同（2.6/3.4 vs 2.4/3.2）。该图作为 `@图片2` 送模 | 便宜：按现行 spec 重生成俯视图（`python tools/shot_pack.py sync episodes/ep01 s2_st5` 一类），核对时间轴文字 |
  | s2_st8 | 2.5–3.5（俯视图） | V5 / V6 重复动作 | 重出 | ③ prompt 或首帧 | `st8_overhead.png` 时间轴「2.5–3.5s 女人把头扭开，从腰带里抽出一小块布，低头擦罐身」，抬头说明「直腰扶着满水罐，挑眉撇嘴」；但 st5 5.2 秒已抽布、st8 第 0 秒布在我手里（首帧画右可见）。按图演我会第二次抽布；台词时间也不同（4.4–8.7 vs 3.6–7.9 秒） | 便宜：按现行 spec 重生成 st8 俯视图并核对时间轴 |
  | s2_st8 | 1–2；3.5–11 | V4 / V5 写法自相矛盾 | 记录 | ② 分镜文字 | 同一 prompt：节拍「只抬眼瞄半秒、眉毛一挑」vs 配角段「挑起眉毛看她一眼、轻轻摇头」；配角段「之后一直擦罐、偶尔瞄一眼」vs 8–11 秒「没再看她」 | 便宜：统一为「1–2 秒抬眼半秒、挑眉、不摇头；约 6 秒她笑出声时我眼珠斜上扫一下不抬头、手上擦得更重；8–11 秒她回头时我已低头不接眼神」，删配角段的「轻轻摇头」 |

### I41 严重 · 角色立场·Vibia · V6 动机
- a（1 分）：从 st5 5.2 秒抽布到 st4 10 秒我一直在擦同一只罐，约 1.8＋11＋10≈22.8 秒，st4 1.5–10 秒对我无任何指示也不离场——留在喷泉边只为剧情（被她看见、被她擦身而过）；st5 回头缺声音动因
- spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」；上一镜 s2_st2 16.5–18 秒 Riley 已闭嘴（junctions 第 66 行）。成片里我会在静默中无故回头
- `st8_overhead.png` 时间轴「2.5–3.5s 女人把头扭开，从腰带里抽出一小块布，低头擦罐身」，抬头说明「直腰扶着满水罐，挑眉撇嘴」；但 st5 5.2 秒已抽布、st8 第 0 秒布在我手里（首帧画右可见）。按图演我会第二次抽布；台词时间也不同（4.4–8.7 vs 3.6–7.9 秒）
- spec 与 prompt 只在 0–1.5 秒写我；之后 8.5 秒对我无指示。从 st5 5.2 秒算起我已连续擦同一只罐约 22.8 秒，只为留在画面里
- prompt 写「一个女人穿着男人的裤子」，但当时罗马男人也不穿裤子，bracae 是蛮族（高卢人）的衣服；对画面影响小
- 分数：a 1 / b None → 最终 1
  | s2_st5 | 2.4–3.2 | V5 / V6 回应缺触发 | 重出 | ② 分镜文字 | spec 写「听见身后有人大声说外国话」，`st5/资料包/prompt.txt` 第 2 行与末行「本镜没有人说话」、台词「无」；上一镜 s2_st2 16.5–18 秒 Riley 已闭嘴（junctions 第 66 行）。成片里我会在静默中无故回头 | 便宜：st5 给 Riley 加一段画外声（如 2.0–2.6 秒一句含糊的 "Okay…" 或一声笑，标「画外、听不清」），声音行改成「画外有人说话」；或把 s2_st2 的尾句延到 st5 开头做音频前搭（剪辑处理）。我的动作改为「手上一顿 → 直腰 → 扭头找声音」 |
  | s2_st8 | 2.5–3.5（俯视图） | V5 / V6 重复动作 | 重出 | ③ prompt 或首帧 | `st8_overhead.png` 时间轴「2.5–3.5s 女人把头扭开，从腰带里抽出一小块布，低头擦罐身」，抬头说明「直腰扶着满水罐，挑眉撇嘴」；但 st5 5.2 秒已抽布、st8 第 0 秒布在我手里（首帧画右可见）。按图演我会第二次抽布；台词时间也不同（4.4–8.7 vs 3.6–7.9 秒） | 便宜：按现行 spec 重生成 st8 俯视图并核对时间轴 |
  | s2_st4 | 1.5–10 | V6 动机 / 无事可做 | 可剪 | ② 分镜文字 | spec 与 prompt 只在 0–1.5 秒写我；之后 8.5 秒对我无指示。从 st5 5.2 秒算起我已连续擦同一只罐约 22.8 秒，只为留在画面里 | 便宜：加我的收尾：「2–4 秒 抬眼目送她背影，鼻子里轻哼、摇一下头；4–6 秒 把布塞回腰带，两手抱罐挎上左髋；6–8 秒 转身往北（镜头方向）走出画左 / 进身后门」；同步俯视图走位与首帧不变 |
  | s2_st5 | 配角段 | V6 心理说明史实偏差 | 记录 | 规则源 | prompt 写「一个女人穿着男人的裤子」，但当时罗马男人也不穿裤子，bracae 是蛮族（高卢人）的衣服；对画面影响小 | 便宜：改为「一个女人穿着蛮族人的裤腿」或直接删心理说明，只留可见动作 |

### I42 严重 · 角色立场·Helvia · V5 回应
- a（1 分）：st6 9–19 秒（10 秒）、st9 12.7–18.2 秒与 19.8–21 秒，她朝我偏头、皱鼻子、冲我笑、拍膝，spec 与 prompt 都没写我的回应（见问题表第 1、3 条）
- spec 节拍与 prompt 第 72 行 9–19 秒只写 Riley；她 10.1–13.4 秒朝我偏头、17–19 秒拍膝坐直，我无任何身体/表情指示，只有「其他人不开口」
- 「朝她抬抬下巴」后 Riley 即伸小臂——抬下巴不是可读的「要不要油」，伸手是剧情替她读懂的
- 12.7–18.2 秒她皱鼻子说 Gross、19.8–21 秒冲我笑，spec 都没写我；18.2–19.8 秒我只接过刮板放下
- 分数：a 1 / b None → 最终 1
  | s8_st6 | 9–19 | V5 回应 | 重出 | ② 分镜文字 | spec 节拍与 prompt 第 72 行 9–19 秒只写 Riley；她 10.1–13.4 秒朝我偏头、17–19 秒拍膝坐直，我无任何身体/表情指示，只有「其他人不开口」 | 便宜：节拍补「9–19 秒 Helvia 一直含笑看着她，她偏头时 Helvia 挑一下眉、轻轻笑出鼻音（闭着嘴）；她拍膝坐直时 Helvia 点点头，自己往后靠回墙上，嘴始终闭着」 |
  | s8_st5 | 2.5–5 | V1/V5 语言·回应 | 记录 | ② 分镜文字 | 「朝她抬抬下巴」后 Riley 即伸小臂——抬下巴不是可读的「要不要油」，伸手是剧情替她读懂的 | 便宜：改为「拿起油瓶朝她晃一晃、眉毛一挑，再朝她的胳膊努努嘴」，Riley 才伸小臂；拿瓶动作可与 5–6.5 秒合并 |
  | s8_st9 | 12.7–21 | V5 回应 | 记录 | ② 分镜文字 | 12.7–18.2 秒她皱鼻子说 Gross、19.8–21 秒冲我笑，spec 都没写我；18.2–19.8 秒我只接过刮板放下 | 便宜：补「Gross 时 Helvia 嗤地笑、摇摇头」；「接过刮板时用它朝她还油亮的胳膊比一下、摇头笑，再放回凳上」；「她冲 Helvia 笑，Helvia 回笑、点一下头」，全程闭嘴 |

### I43 主要 · 世界物理 · P1 手数
- a（1 分）：s2_st5 道具行写「出场时在槽沿上，满的，她两手扶着」，同一镜 5.2–7 秒又写她「从腰带里抽出一小块布，低头擦罐身」，两只手不够用。prompt.txt 里原句照抄了这两段；首帧左右手和规格也是反的（见问题表）。自拍镜 s1_st2、s2_st2、s2_st8 都是右手持镜、只用左手做动作，没问题。
- 道具行写「出场时在槽沿上，满的，她两手扶着」，节拍 5.2–7 秒又写她从腰带抽布、低头擦罐，手不够。prompt.txt 里原样都有。
- 规格写「右手托着罐底，左手握着罐颈」。首帧里她侧背对镜头、面朝画左，靠镜头那只手（左手）在下面托底，远侧那只手（右手）扶着罐口，正好反了。
- 分数：a 1 / b None → 最终 1
  | s2_st5 | 1.2–7 秒 | P1 手数 | 可剪 | ② 分镜文字 | 道具行写「出场时在槽沿上，满的，她两手扶着」，节拍 5.2–7 秒又写她从腰带抽布、低头擦罐，手不够。prompt.txt 里原样都有。 | 便宜：道具行改成「出场时罐在槽沿上，左手扶罐耳，右手拿布擦罐身」，和 st8、st4 对齐。 |
  | s2_st5 | 0 秒 | P8 / P1 | 记录 | ③ 首帧 | 规格写「右手托着罐底，左手握着罐颈」。首帧里她侧背对镜头、面朝画左，靠镜头那只手（左手）在下面托底，远侧那只手（右手）扶着罐口，正好反了。 | 便宜：二选一。规格改成「左手托底、右手扶罐口」，或首帧重出。 |

### I44 主要 · 世界物理 · P2 道具来源与去向
- a（1 分）：s3_st3 首帧画右下的陶碗放大后有 4 枚黄铜色钱，s3_st7 的碗里约 4–5 枚浅色圆片，s3_st4 的碗里约 5 枚，s3_st6 首帧却是正好 2 枚红铜色。s3_st1 首帧碗是空的，从 st1 到 st6 碗里的数目一路跳变。另外 s3_st7 首帧 Felix 身后看不到工作台和托板（spec 11–13s 要去端它），托板可能凭空出现（见问题表）
- 放大后碗里分别有 4 枚黄铜色、约 4–5 枚浅色、约 5 枚；s3_st1 首帧碗是空的，s3_st6 首帧正好 2 枚红铜。四镜连着看，钱数一路跳变
- 俯视图里工作台在 (5.8,2.9)，Felix 身后 0.85 m；首帧 Felix 身后只有两座石磨和空地，没有工作台和放着 5 个面包的托板，末拍「双手伸向身后托板」时托板可能凭空出现
- 首帧剩下的面包看起来像切成两块（右边一大块露着切面），不是「七瓣连在一起、缺一瓣」；Felix 挪动时可能断开或多出一块。核实：放大 bowls.png 上半部分
- 分数：a 1 / b None → 最终 1
  | s3_st3 / st7 / st4 | 0s（首帧） | P2 道具守恒（钱数） | 可剪 | ③ 首帧 | 放大后碗里分别有 4 枚黄铜色、约 4–5 枚浅色、约 5 枚；s3_st1 首帧碗是空的，s3_st6 首帧正好 2 枚红铜。四镜连着看，钱数一路跳变 | 便宜：局部重绘这三张首帧，碗里改成 2 枚红铜小钱，或者碗口角度不露底；三镜 spec 补一句「碗里正好 2 枚红铜小钱」 |
  | s3_st7 | 11–13s | P2 道具来源（托板） | 可剪 | ③ 首帧 | 俯视图里工作台在 (5.8,2.9)，Felix 身后 0.85 m；首帧 Felix 身后只有两座石磨和空地，没有工作台和放着 5 个面包的托板，末拍「双手伸向身后托板」时托板可能凭空出现 | 便宜：首帧补画 Felix 身后齐腰高的工作台和托板，或者末拍改成只转身、不伸手 |
  | s3_st7 | 0s（首帧） | P2 道具形态 | 存疑 | ③ 首帧 | 首帧剩下的面包看起来像切成两块（右边一大块露着切面），不是「七瓣连在一起、缺一瓣」；Felix 挪动时可能断开或多出一块。核实：放大 bowls.png 上半部分 | 便宜：局部重绘成缺一瓣的整只面包 |

### I45 主要 · 世界物理 · P8 首帧 = 第 0 秒
- a（1 分）：s3_st8 首帧 Riley 的全身约占 680/941 像素高，石台正面约 190 像素对 0.95 m，推算 Riley 离机位约 3.4 m，石台约 7 m，她已经站到街心车道上；spec 第 0 秒和俯视图 (5.8,5.15) 要求她紧贴石台外侧。其余 12 镜首帧都和第 0 秒对得上（s3_st6 碗里 2 枚、托板 3+2；s4_st4 Riley 刚越过北街口墙角、猫在画右台阶上；s4_st1 侧背对、Tertius 在画左 1/4）
- 首帧 Riley 占画高约七成，在车道上，离石台约 3.5–4 m；spec 和俯视图要她紧贴石台外侧挥手。接着她还要「朝街上走两步」，会走到离机位 1.5 m 内，可能出画下沿；挥手的距离也不对
- 分数：a 1 / b None → 最终 1
  | s3_st8 | 0s | P8 首帧 = 第 0 秒 / P6 距离 | 可剪 | ③ 首帧 | 首帧 Riley 占画高约七成，在车道上，离石台约 3.5–4 m；spec 和俯视图要她紧贴石台外侧挥手。接着她还要「朝街上走两步」，会走到离机位 1.5 m 内，可能出画下沿；挥手的距离也不对 | 便宜：重出首帧，让 Riley 站在石台外沿（全身约占画高五成五），或者把 spec 改成「七成」对应的机位前移；三者统一 |

### I46 主要 · 世界物理 · P7 服装与动作相容
- a（1 分）：s8_st5 文字写 Helvia「正刮到肘弯上方」，人物卡 c7 第 12 行写「宽松的半袖垂到肘部」，肘上那段在袖子里；s8_st5 首帧把她左臂画成整条光着，到 st9/st6 首帧半袖又回到肘部（见问题表）。Riley 短袖、下摆塞进腰里，揪前襟（s8_st7）、扯领口（s8_st8）、露小臂抹油（s8_st5）都和衣服相容
- 文字写刮到左臂「肘弯上方」，人物卡写半袖垂到肘部，刮的位置应该在袖子里；首帧干脆把 Helvia 左臂画成整条光着，st9/st6 首帧半袖又回来。成片会出现刮板刮布或袖子忽有忽无
- 分数：a 1 / b None → 最终 1
  | s8_st5 | 0–2.5s | P7 服装与动作 | 记录 | ② 分镜文字（人物卡冲突） | 文字写刮到左臂「肘弯上方」，人物卡写半袖垂到肘部，刮的位置应该在袖子里；首帧干脆把 Helvia 左臂画成整条光着，st9/st6 首帧半袖又回来。成片会出现刮板刮布或袖子忽有忽无 | 便宜：改成「刮到左小臂靠肘处」，或加一句「左边半袖撩到肩头」，三镜一致 |

### I47 主要 · 人物逻辑 · C9 像真人
- a（1 分）：「Riley 对着空气说话，当地人摇头笑 / 憋笑」这个梗在范围内重复出现：s8_st10 6.5–8 秒、s8_st9 1.6–10 秒、s5_st12、s5_st7 的 Asellina、s6_st6 8.6–9.4 秒的远车夫，加上范围外的 s2_st8、s3_st4；s8_st8 同一拍「对看一眼，捂嘴笑」2.5–4 秒和 9–10 秒各写一次（问题表 2、4）。
- 「Riley 对空气说话，旁人憋笑 / 摇头笑 / 看一眼」在 s8_st10、s8_st9、s8_st6、s5_st12、s5_st7、s6_st6 里各用一次，范围外还有 s2_st8、s3_st4；同一个梗用了六次以上，观众会觉得全城的人都这个反应
- 10 秒镜头里同一拍「对看一眼，捂嘴笑」出现两次
- 分数：a 1 / b None → 最终 1
  | s8_st9 / s8_st10 / s8_st6 / s5_st12 / s5_st7 / s6_st6 | 见证据 | C9 | 可剪 | ② 分镜文字 | 「Riley 对空气说话，旁人憋笑 / 摇头笑 / 看一眼」在 s8_st10、s8_st9、s8_st6、s5_st12、s5_st7、s6_st6 里各用一次，范围外还有 s2_st8、s3_st4；同一个梗用了六次以上，观众会觉得全城的人都这个反应 | 便宜：只留 2–3 处（建议 s8_st10 门房、s5_st7 Asellina），其余改成当地人手上的活不停、根本没注意她，不加表情。 |
  | s8_st8 | 2.5–4、9–10 秒 | C9 | 可剪 | ② 分镜文字 | 10 秒镜头里同一拍「对看一眼，捂嘴笑」出现两次 | 便宜：删掉 9–10 秒那次，只留 2.5–4 秒的反应拍。 |

### I48 主要 · 连续性 · K4 光与时间
- a（1 分）：时段推进 清晨(s1–s3)→上午(s4_st3)→正午(s4_st4)→14 时(s8)→15:30(s5)→日落(s6_st3)→天快全黑(s6_st4)→夜(s7)是对的；但 s7_st3 和 s7_st7 光线段写的秒数和节拍/道具段对不上，而且 prompt.txt 原样带进去了；s1_st5 首帧受光的一侧和 spec 左右相反（见问题表）
- 光线段写「0–9.5 秒有灯…9.5 秒吹灭后只剩窗洞微光」，节拍和道具段写的却是 10.8–12.3 s 吹、12.3 s 灭，台词 9.1–10.5 s 才说完 goodnight from Pompeii。prompt.txt 两种秒数都在
- 光线段写「8 秒前在她手里…10 秒后灯在床头小凳上」，动作和道具段写 13.8–15.8 s 才放灯；prompt 两种都带着。按 8/10 秒出的话，她 4.5–13.4 s 说台词时灯已经离手，光源会和动作打架
- spec 和 prompt 写的是「画左那排房子墙面的上半截暖金色；画右这一侧的墙面和整个街面在柔和的阴影里」，首帧却是画右那排橙黄墙被照亮，画左偏暗
- 分数：a 1 / b None → 最终 1
  | s7_st3 | 9.5s / 12.3s | K4 光与时间 | 可剪（文字矛盾，出片多半会提前灭灯） | ② 分镜文字 | 光线段写「0–9.5 秒有灯…9.5 秒吹灭后只剩窗洞微光」，节拍和道具段写的却是 10.8–12.3 s 吹、12.3 s 灭，台词 9.1–10.5 s 才说完 goodnight from Pompeii。prompt.txt 两种秒数都在 | 便宜：光线段改成 0–12.3 秒、12.3 秒吹灭后 |
  | s7_st7 | 8s/10s vs 13.8–15.8s | K4 光与时间 | 可剪 | ② 分镜文字 | 光线段写「8 秒前在她手里…10 秒后灯在床头小凳上」，动作和道具段写 13.8–15.8 s 才放灯；prompt 两种都带着。按 8/10 秒出的话，她 4.5–13.4 s 说台词时灯已经离手，光源会和动作打架 | 便宜：光线段改成「13.8 秒前在她手里…15.8 秒后在凳上」 |
  | s1_st5 | 首帧 | K4 光向 | 记录 | ③ 首帧 | spec 和 prompt 写的是「画左那排房子墙面的上半截暖金色；画右这一侧的墙面和整个街面在柔和的阴影里」，首帧却是画右那排橙黄墙被照亮，画左偏暗 | 便宜：首帧重出时按 spec 的受光侧来 |

### I49 主要 · 连续性 · K8 镜间接点
- a（1 分）：60 个接点逐条判过（见下方接点表），56 ✓、4 ✗：s3_st8→st6（已知问题）、s5_st8→st9、s6_st5→st6，另有 s2_st1 和 s2_st3 的水流冲突落在同一组接点里（记在 K6）
- st5 在 4.5–6 s 已经换成右手食指勾环、掌心托底、左手护火，就这样走进院子；st6 第 0 秒又是「双手在胸前捧着」，1.5 s 再换回勾环，首帧（z1.jpg 右）也是双手捧
- st8 结尾 Felix 已经「嘴角一抽、摇摇头、拇指拨正面包」，st6 又从「目光慢慢移过去→吸气想喊→停住→摇头笑→推正面包」重来一遍，摇头和推面包都做了两次
- 分数：a 1 / b None → 最终 1
  | s6_st5 → s6_st6 | 接点 0–1.5s | K1/K8 道具手势回退 | 记录 | ② 分镜文字 | st5 在 4.5–6 s 已经换成右手食指勾环、掌心托底、左手护火，就这样走进院子；st6 第 0 秒又是「双手在胸前捧着」，1.5 s 再换回勾环，首帧（z1.jpg 右）也是双手捧 | 便宜：st6 第 0 秒直接写勾环加护火，删掉换手这一拍 |
  | s3_st8 → s3_st6 | 接点 | K8 表演倒退（已知，属节点 15b） | 记录 | ① 故事 / ② 分镜 | st8 结尾 Felix 已经「嘴角一抽、摇摇头、拇指拨正面包」，st6 又从「目光慢慢移过去→吸气想喊→停住→摇头笑→推正面包」重来一遍，摇头和推面包都做了两次 | 已知问题，等用户在 story_beats 里挑改法 |

### I50 主要 · 母语听感 · N9 / N7
- 「Good morning from Pompeii! It's May, 75 AD — which is so weird to say out loud. Okay, so, two goals today: …」是对镜头念的开场稿；两个目标并列 + 「And my budget for all of that is… this. Yeah. This is it.」停顿亮钱
  | s1_st2 | 0–约 20 秒（整段台词） | N9 / N7 | 可剪 | ② 分镜文字 | 「Good morning from Pompeii! It's May, 75 AD — which is so weird to say out loud. Okay, so, two goals today: …」是对镜头念的开场稿；两个目标并列 + 「And my budget for all of that is… this. Yeah. This is it.」停顿亮钱 | 便宜。改成：「Hi — okay, good morning, from Pompeii. It's, uh, May, 75 AD. Which is so weird to say. Okay, two things today: I need somewhere to sleep, and I need to try garum — it's this fish sauce everyone here is obsessed with. And that's it. That's the plan. Oh, and my budget is… this.」（钱放最后随口带过，不做停顿亮相；若要保留亮钱，摊手时说「this」即可） |

### I51 主要 · 镜头规格 · F1 景别与人物大小
- a（1 分）：s2_st4 首帧 Riley 头顶 y≈155→靴底 y≈830，占画高 72%；按 overhead.toml 第 11/14 行（机位 (14.0,17.2)、28mm）算她在 5.42 m，应占约 45%，Vibia 实测 56% 对算得 34–36%，两人都大约 +60%，超过 25%（见问题表）；其余镜都在 25% 以内，例如 s1_st1 算 46% 实测 46%，s1_st5 算 26% 实测 22%，s3_st8 算 68% 实测 74%，s4_st4 算 30% 实测 33%，s4_st1 算 102% 实测 90%
- 按 overhead.toml 第 11 行机位 (14.0,17.2)、第 14 行 28mm，Riley 在 5.42 m 应占画高约 45%，首帧实测 72%；Vibia 在 6.56 m 应占约 35%，实测 56%；石槽在 6.8 m 处，首帧看起来约 3 m。首帧相当于机位往南近了约 2–2.5 m。模型以首帧为准，影响主要在俯视图与首帧对不上，走位秒数会偏
- 分数：a 1 / b None → 最终 1
  | s2_st4 | 0s | F1 景别与人物大小 | 记录 | ③ prompt 或首帧 | 按 overhead.toml 第 11 行机位 (14.0,17.2)、第 14 行 28mm，Riley 在 5.42 m 应占画高约 45%，首帧实测 72%；Vibia 在 6.56 m 应占约 35%，实测 56%；石槽在 6.8 m 处，首帧看起来约 3 m。首帧相当于机位往南近了约 2–2.5 m。模型以首帧为准，影响主要在俯视图与首帧对不上，走位秒数会偏 | 便宜：把 overhead 机位往南挪到约 y≈19.5（仍在垫脚石东北边、最近一块石头在右下角前景），或按 45mm 等效重算；改完重跑 sync |

### I52 主要 · 镜头规格 · F2 机位与朝向
- a（1 分）：s2_st3 overhead.toml 第 6/11/21/31 行写的是「升镜头，离地 0.3→1.6 m」，look 在第 6 秒从 (15,16) 换到 (15.5,15.6)，俯视图上也标着「离地0.3→1.6m」并画了两个视野扇形；prompt 第 13 行和首帧（人眼高度）却是「固定机位、人眼高度、不升不降不推不摇」，三处对不上（见问题表）；其余镜机位朝向三处一致，例如 s1 都朝北、海在画左，s3 机位都在 Felix–Riley 连线西侧
- overhead.toml 是 11-08 的旧版：第 6 行 note 写「升镜头…镜头在西人行道边贴地」，第 11/21 行 h=0.3，第 31 行 h=1.6、look 改向；作为 @图片2 发给模型的俯视图上标着「离地0.3→1.6m」并画了两个扇形。prompt 第 13 行和首帧都是「人眼高度约一米六、固定、不升不降」。模型拿到的两份指令互相矛盾，可能出现起手升镜头或中途改构图
- overhead.toml 第 10/13 行注释和第 21 行 note、第 76 行节拍里还写着「两根绳、各攥一根」，现行 prompt 是「只系着一根」；第 0–11.7 s Riley 的朝向点 (37.8,54.0) 算出来是背影（与人→机位方向约 143°），首帧是左侧脸、身体 3/4 朝镜头。俯视图上没有绳子文字，不进模型，属于文件残留
- 分数：a 1 / b None → 最终 1
  | s2_st3 | 0–8s | F2 机位与朝向（另涉 F7） | 存疑 | ③ prompt 或首帧 | overhead.toml 是 11-08 的旧版：第 6 行 note 写「升镜头…镜头在西人行道边贴地」，第 11/21 行 h=0.3，第 31 行 h=1.6、look 改向；作为 @图片2 发给模型的俯视图上标着「离地0.3→1.6m」并画了两个扇形。prompt 第 13 行和首帧都是「人眼高度约一米六、固定、不升不降」。模型拿到的两份指令互相矛盾，可能出现起手升镜头或中途改构图 | 便宜：按现行文字改 overhead.toml（h=1.6、三个路点 look 统一、改 note），重跑 shot_pack sync，重出俯视图 |
  | s1_st4 | 0–8s | F2/F3（文件残留） | 记录 | 规则源 | overhead.toml 第 10/13 行注释和第 21 行 note、第 76 行节拍里还写着「两根绳、各攥一根」，现行 prompt 是「只系着一根」；第 0–11.7 s Riley 的朝向点 (37.8,54.0) 算出来是背影（与人→机位方向约 143°），首帧是左侧脸、身体 3/4 朝镜头。俯视图上没有绳子文字，不进模型，属于文件残留 | 便宜：清理 toml 注释和节拍文字；把 Riley 的朝向点改成 (36.8,56.5) 一带，让 overhead 显示侧身 |

### I53 主要 · Prompt 文本 · T2 否定句
- a（1 分）：s1_st4 写「没有耳钉、没有耳环，耳朵上没有任何金属亮点」；s3_st6 写「没有银色或金色的钱、没有第三枚」；s5_st3 写「没有银色或银灰色的钱」「不放在深色的木盖上」「不会凭空消失」；s2_st3 写「墙上没有阳光、没有明暗分界线」；s7_st4 写「没有月光照进屋、没有光束」；s7_st1 写「也没有任何音乐声或叮的一声」。Riley 人物行「不矮不胖不壮实」和各镜「画面里看不到驴车侧过身」（s5_st8）也是否定写法。人物卡 c1_Riley.md 自己写明「外观正文不写否定句」（见问题 2）。
- 「没有耳钉、没有耳环」「没有第三枚」「没有银色或金色的钱」「不放在深色的木盖上」「墙上没有阳光」「没有月光、没有光束」「没有任何音乐声」，每句都点出了不想要的东西。c1_Riley.md 明说正文不写否定句。
- 分数：a 1 / b None → 最终 1
  | s1_st4、s3_st6、s5_st3、s2_st3、s7_st4、s7_st1、s5_st8 | s1_st4 约 0–23 秒（人物段）；s3_st6 全镜；s5_st3 付钱段；其余整镜 | T2 否定句 | 可剪（出片前建议改） | ② 分镜文字 | 「没有耳钉、没有耳环」「没有第三枚」「没有银色或金色的钱」「不放在深色的木盖上」「墙上没有阳光」「没有月光、没有光束」「没有任何音乐声」，每句都点出了不想要的东西。c1_Riley.md 明说正文不写否定句。 | 便宜：改成正向描述，例如「耳垂光着，被头发盖住」「陶碗里两枚红铜钱」「钱都是红铜色和金黄色」「钱放在浅色大理石台面上」「整面墙在阴影里」。 |

### I54 主要 · Prompt 文本 · T5 混入别镜
- a（1 分）：s1_st1 画面行写「（下一镜她举着它自拍）」；s5_st10 画面行与动作行各写「（接上一镜）」；s7_st1 画面行写「上一镜她刚坐下、舒过气」；s8_st2 画面行写「数钱交给 st10 的台词」。这些别镜指代是 prompt 正文里的元信息，对视频模型没有意义，也可能被当成画面内容（问题 4）。其余镜头「场景」行都是该场景卡的原文，没有混入别镜的动作。
- 正文夹着「下一镜她举着它自拍」「（接上一镜）」「上一镜她刚坐下」「交给 st10 的台词」，指代的是 prompt 之外的镜头。
- 分数：a 1 / b None → 最终 1
  | s1_st1、s5_st10、s7_st1、s8_st2 | s5_st10 第 0–1.2 秒；其余全镜 | T5 混入别镜 | 记录 | ② 分镜文字 | 正文夹着「下一镜她举着它自拍」「（接上一镜）」「上一镜她刚坐下」「交给 st10 的台词」，指代的是 prompt 之外的镜头。 | 便宜：删掉这些括号；接点信息放在首帧和 junctions，不进 prompt。 |

### I55 主要 · Prompt 文本 · T7 长度与重点
- a（1 分）：63 个 prompt.txt（含索引外的 s2_st6、s2_st7 等）平均约 3560 字，最长 s1_st2 为 4903 字、s8_st9 为 4882 字，离 5000 字拒绝线只差约 100 字。prompts-seedance.md 写的本剧设计区间是 1100–2800 字，资料包目录下 63 个 prompt 里有 52 个超了区间上沿。「画面」「走位」「动作」「镜头」四行把同一串动作写了两到三遍（s1_st1 的「画面」行已经包含全部 22 秒动作，「动作」行又逐秒重写）。s1_st4 的画面行约 2400 字，23 秒里要拉船、抬筐、对视、说话，节拍过满（问题 7）。
- 离 5000 字上限不到 120 字；「画面」「走位」「动作」「镜头」重复叙述同一串动作；s1_st4 的 23 秒节拍过满（拉船、丢绳、抬筐、对视、说台词）。
- 分数：a 1 / b None → 最终 1
  | s1_st2（4903 字）、s8_st9（4882 字）、s6_st3（4782 字）、s1_st4 | 全镜 | T7 长度与重点 | 记录（s1_st4 为存疑） | ② 分镜文字 / 编译器 | 离 5000 字上限不到 120 字；「画面」「走位」「动作」「镜头」重复叙述同一串动作；s1_st4 的 23 秒节拍过满（拉船、丢绳、抬筐、对视、说台词）。 | 便宜：编译时让「画面」只写静态构图与道具，动作只留「动作」一行；s1_st4 考虑拆成两镜（要积分）。 |

### I56 主要 · 角色立场·Riley · V5 回应
- a（1 分）：s1_st5 6.5–7.5 秒赶驴人冲我点头，分镜没写我回礼，只写「目送、嘴角带笑」。s4_st3 6.5–8 秒扛柴的人侧身让我，我没反应。s8_st6 到 s8_st7 Helvia 教了我刮油，我走时没道别。s3_st7 8.5–13 秒 Felix 主动替我包面包，我只拍拍布包笑一下（见问题表）
- 整集别人给我面包、替我打包、倒鱼露、递灯、滴油递刮板，我从来不说一句 thank you，只「笑笑 / 点头」。一个爱说话的美国女孩，被人帮了会脱口说谢谢，对方听不懂也会说
- 赶驴人点头，我不回礼；小女孩盯着我的头发、摸自己的短发，我没反应；扛柴的人侧身让我，我只顾往前走
- Helvia 教我刮油，Asellina 免费给我倒鱼露，我离开时都没道别，下一镜直接到了街上
- 分数：a 1 / b None → 最终 1
  | s3_st1、s3_st7、s5_st4/st13、s6_st5、s8_st5/st9 | s3_st1 11.7–13；s3_st7 11–13；s6_st5 7.5–8.5；s8_st5 13–14 | V1·V5 | 可剪 | ① 故事 | 整集别人给我面包、替我打包、倒鱼露、递灯、滴油递刮板，我从来不说一句 thank you，只「笑笑 / 点头」。一个爱说话的美国女孩，被人帮了会脱口说谢谢，对方听不懂也会说 | 此刻的我：s3_st7 布包递过来时说「Oh — thank you!」，手按胸口点一下头；s8_st9 递回刮板时小声说「Thank you.」。其余镜头用手按胸口加点头代替，不必每镜都开口（便宜，加半句台词或一个动作） |
  | s1_st5、s2_st4、s4_st3 | s1_st5 6.5–7.5；s2_st4 4–5.5；s4_st3 6.5–8 | V5 | 记录 | ② 分镜文字 | 赶驴人点头，我不回礼；小女孩盯着我的头发、摸自己的短发，我没反应；扛柴的人侧身让我，我只顾往前走 | 此刻的我：s1_st5 笑着点头回礼；s2_st4 擦肩时冲女孩笑一下、轻轻摆一下手指（背影也能看出偏头）；s4_st3 让开半步，小声说「oh — sorry」（便宜） |
  | s8_st6→s8_st7、s5_st7→s6_st3 | s8_st6 17–19；s5_st7 10.9–14 | V5 | 记录 | ① 故事 | Helvia 教我刮油，Asellina 免费给我倒鱼露，我离开时都没道别，下一镜直接到了街上 | 此刻的我：s8_st6 拍完膝盖站起来，冲 Helvia 笑着挥手、手按胸口点头；s5_st7 喝完放下杯子，冲 Asellina 挥一下手，再走（便宜） |

### I57 主要 · 角色立场·Felix · V7 跨集一致
- a（1 分）：没有 behavior.md 和前几集可对照（bible §2.1 每集新设计），所以拿人物卡「个性」行对照：st4 不比划，与「指路整条胳膊比划」相反，镜里没有原因；人物卡声样台词是 "Ad sinistram…" 加右手指画左，和本集「说右、不比划」相反
- 叫声设计台词 "Ad sinistram hac recta platea."，加右手指画左，与本集「说右」相反；人物卡「指路整条胳膊比划」与 st4 相反
- 分数：a 1 / b None → 最终 1
  | c2_Felix.md | 声样 / turntable | V7 | 记录 | 规则源 | 叫声设计台词 "Ad sinistram hac recta platea."，加右手指画左，与本集「说右」相反；人物卡「指路整条胳膊比划」与 st4 相反 | 便宜：卡里注明 turntable「只取音色，动作和台词都不取」；人物卡个性行与本集指路写法二者择一，统一 |

### I58 主要 · 角色立场·Tertius · V2 肢体
- a（1 分）：见问题表 #2、#3——6.4–7.2 秒「朝她挥手赶人」没写手背朝外往门口甩，模型可能画成打招呼；5.0 秒「扭过头」与俯视图 0–5s 朝西、需转约 120–150° 才看得到她不符
- 「朝她挥手赶人」没写手型和方向，「挥手」在模型里常画成打招呼
- 「扭过头」；俯视图 `st1_overhead_ref.png` 我 0–5s 尖角朝西、5.6–13s 朝东南偏东，转角约 120–150°；首帧我身体朝画左前方
- 分数：a 1 / b None → 最终 1
  | s4_st1 | 6.4–7.2 | V2 肢体 | 记录 | ② 分镜文字 | 「朝她挥手赶人」没写手型和方向，「挥手」在模型里常画成打招呼 | 此刻的我会：右手手背朝她、往门口方向用力甩两下，同时喊 "Apage!"；时间够可再朝门口一指加 "Foras!"。**便宜** |
  | s4_st1 | 5.0–5.7 | V2 肢体 | 记录 | ② 分镜文字 | 「扭过头」；俯视图 `st1_overhead_ref.png` 我 0–5s 尖角朝西、5.6–13s 朝东南偏东，转角约 120–150°；首帧我身体朝画左前方 | 此刻的我会：脚踩在槽里不动，**转过上身**侧过来看她（不是只拧脖子）。文字改「转过上身看她」。**便宜** |

### I59 主要 · 角色立场·Asellina · V5 回应
- a（1 分）：st14 第 7–10.8 秒她伸手指着我正在兑水的杯子，分镜让我照常兑水、放罐、擦台面，第 10.8 秒后才只瞥一眼，对指点没有回应（见问题表第 1 条）；其余回应快慢合适：st12 愣 1 秒回手势，st13 1 秒后 Euge!，st7 第 3–4 秒举勺回敬
- 节拍 7–8 秒「Riley 看着，抬起右手指着杯子」，8–10.8 秒 Asellina 只「往杯里慢慢点了一小股冷水，把水罐放回原处」，对被指着毫无反应
- 分数：a 1 / b None → 最终 1
  | s5_st14 | 7–10.8 | V5 回应 | 记录 | ② 分镜文字 | 节拍 7–8 秒「Riley 看着，抬起右手指着杯子」，8–10.8 秒 Asellina 只「往杯里慢慢点了一小股冷水，把水罐放回原处」，对被指着毫无反应 | 便宜：8–10.8 秒改为「她兑着水，抬眼看 Riley 指着杯子的手，扬一下眉，下巴朝杯子一点（当然要兑），把水罐放回原处」；不加台词 |

### I60 主要 · 角色立场·Asellina · V6 动机
- a（1 分）：st14 第 2–4 秒侧身探半步去后排罐口拿勺，但 st2 第 3–4 秒勺子是横搁回前排中间罐口的，中间没人挪过，这个绕路只为道具摆位；st7 第 10.9–14 秒擦一块前文从没洒出的「酒渍」（见问题表）
- st2 节拍 3–4 秒「把勺子横搁回那只罐口上」（前排中间），st14 开场勺却在「后排靠灶那只的罐口上」（首帧可见），之间无镜挪动；同一把勺 st2 搅冒热气的罐、st7 第 5–10.9 秒又搅中间罐，st14 却用来舀好酒
- 「擦一擦陶杯旁台面上的酒渍」，st14 第 18.8–21 秒、st7 第 1.5–3 秒都没写洒酒，台面无渍
- 精明老板娘白给自带面包的外地客倒鱼露，无任何表示；钱账 9 枚已定，不能加价
- 分数：a 1 / b None → 最终 1
  | s5_st14 | 2–4 | V6 动机／V2 | 记录 | ② 分镜文字 | st2 节拍 3–4 秒「把勺子横搁回那只罐口上」（前排中间），st14 开场勺却在「后排靠灶那只的罐口上」（首帧可见），之间无镜挪动；同一把勺 st2 搅冒热气的罐、st7 第 5–10.9 秒又搅中间罐，st14 却用来舀好酒 | 便宜：酒罐旁加一把专舀酒的小青铜勺（或陶舀），st14 直接取用，删「侧身探半步」；或至少让长柄勺从 st2 起一直在前排罐口，st14 开场写在原处、伸手即取 |
  | s5_st7 | 10.9–14 | V6 动机 | 记录 | ② 分镜文字 | 「擦一擦陶杯旁台面上的酒渍」，st14 第 18.8–21 秒、st7 第 1.5–3 秒都没写洒酒，台面无渍 | 便宜：改成「把她摊在台面上的面包布角往里拢一拢」，或「拿抹布擦一擦手里的长柄勺」，再抬眼冲她笑 |
  | s5_st13 | 9.3–14 | V6 动机 | 存疑 | ① 故事 | 精明老板娘白给自带面包的外地客倒鱼露，无任何表示；钱账 9 枚已定，不能加价 | 便宜（可选，交用户定）：倒鱼露前朝她那杯酒扬下巴、笑一下（「看在你买了好酒」）；核实：问用户是否需要这层生意人的交代 |

### I61 主要 · 角色立场·Fortunata · V1 语言
- a（1 分）：s6_st1 9.5–11s 只伸手不开价，与人物卡「先打量人再开价」不符；s6_st5 6–7.5s 指路全程不说话（见问题表）；Hospitium hic locatur 是墙上广告原文，口语感偏弱，小瑕疵
- 我只伸手、不开价；人物卡写「先打量人再开价」；st2 的「三枚不够、手不收回」因此没有依据
- 指路全程无声，人对外地人照样会说短词
- Hospitium hic locatur 是墙上广告原文（书面腔），当街叫卖略像念招牌
- 分数：a 1 / b None → 最终 1
  | s6_st1 | 8–11s | V1 · V7 | 记录 | ② 分镜文字 | 我只伸手、不开价；人物卡写「先打量人再开价」；st2 的「三枚不够、手不收回」因此没有依据 | 便宜：9.5s 伸手同时竖四指说 "Quattuor."，三枚小钱不够、她只好搭上大币，我照收不找零；拉丁文请核实 |
  | s6_st5 | 6–7.5s | V1 | 记录 | ② 分镜文字 | 指路全程无声，人对外地人照样会说短词 | 便宜：加 "Illic. Sursum."（6.2–7.0s），声音提示改成有对白 |
  | s6_st1 | 1.5–3.0s | V1 | 存疑 | ① 故事 | Hospitium hic locatur 是墙上广告原文（书面腔），当街叫卖略像念招牌 | 便宜：可保留；或请 Latin 考据确认街头叫法是否更口语（如 "Hospitium! Hic!"） |

### I62 主要 · 角色立场·Fortunata · V3 表情
- a（1 分）：st1_first_frame 中部我侧头怒视左侧两名路人，眉头压低，与人物卡「不凶」及 0–1.5s 招客的处境相反；st2 8.5s 点头、st5 10–12s 嘴角一抿分寸合适（见问题表）
- st1_first_frame 我侧头怒视左侧两名路人，眉压低、嘴紧抿，凶相；视频从首帧开始，这个表情会被带进招客的动作
- 分数：a 1 / b None → 最终 1
  | s6_st1 | 首帧；0–3.5s | V3 | 记录 | ③ 首帧 | st1_first_frame 我侧头怒视左侧两名路人，眉压低、嘴紧抿，凶相；视频从首帧开始，这个表情会被带进招客的动作 | 便宜：重出首帧，表情改成「眼睛扫街、脸平、带点招呼人的精神头」，或在 prompt 里写明「招客时脸是松的，不瞪人」 |

### I63 主要 · 角色立场·Fortunata · V5 回应
- a（1 分）：s6_st2 12.5–14s Riley 冲我苦笑，分镜未写我的回应；s6_st1 5–8s 她比划三秒，我没有任何领会的反应（见问题表）
- 节拍只写 Riley 摊手苦笑，没写我的回应，模型会让我定住或乱动
- Riley 比划三秒，我没有任何反应
- 外地人递来大黄铜币，我一秒内直接攥拳，不看成色
- 分数：a 1 / b None → 最终 1
  | s6_st2 | 12.5–14s | V5 | 记录 | ② 分镜文字 | 节拍只写 Riley 摊手苦笑，没写我的回应，模型会让我定住或乱动 | 便宜：加「Fortunata 瞥一眼她的空手，嘴角动一下、肩膀轻耸，侧头看向墙龛里的灯」，接 st5 0s |
  | s6_st1 | 5–8s | V5 | 记录 | ② 分镜文字 | Riley 比划三秒，我没有任何反应 | 便宜：她比「睡」时我下巴一抬，她竖一指时我也竖一指，低声 "Una nox?" |
  | s6_st2 | 7.5–8.5s | V5 | 记录 | ② 分镜文字 | 外地人递来大黄铜币，我一秒内直接攥拳，不看成色 | 便宜：加「低头瞄一眼大币、拇指拨一下」再攥（不占额外秒数） |

### I64 主要 · 角色立场·Fortunata · V6 动机
- a（1 分）：s6_st5 10–12s 刚把门口唯一的灯给了客人，又转回黑街招客，动机只来自下一场需要；s6_st1 8–9.5s 直盯拳头像预知有钱（见问题表）
- 刚把门口唯一的灯给了客人，又转回天已黑的街上招客，这只是为下一场让道
- 目光从脸直落攥钱的拳头，像知道里面有钱；见多识广的店主先看怪衣服和她是不是一个人
- 分数：a 1 / b None → 最终 1
  | s6_st5 | 10–12s | V6 | 记录 | ① 故事 / ② 分镜 | 刚把门口唯一的灯给了客人，又转回天已黑的街上招客，这只是为下一场让道 | 便宜：改成掂钱袋、点头，朝黑街扫最后一眼后转身进车门（或去拉门板），收工 |
  | s6_st1 | 8–9.5s | V4 · V6 | 记录 | ② 分镜文字 | 目光从脸直落攥钱的拳头，像知道里面有钱；见多识广的店主先看怪衣服和她是不是一个人 | 便宜：改成目光从脸扫过衬衫、长裤、靴子，往她身后看一眼，最后停在攥着的拳头上，眉毛一挑 |

### I65 主要 · 角色立场·路人与群众 · V5 回应
- a（1 分）：s4_st1 踩布工在 2.6–4.9 秒院门口一声大嚷时仍「一直埋头踩布」，7.2 秒才抬头，迟了约 4.6 秒；s1_st4 两个渔夫在 12.5–20.5 秒 Riley 离他们三四米、朝鱼筐偏头对空气说话时完全没反应；s8_st8 妇女看着一个穿全套衣服、靴子的人走进热水室不吭声不比划（见问题表第 2、3、4 行）
- 我是后面槽里的踩布工：门口一个外地女人张大嘴「清清楚楚地大声嚷」（spec 2.6–4.9 秒），院子是封闭的、只有踩水声，我不可能埋头不理，等到 Tertius 喊完 Apage 后的 7.2 秒才抬头
- 我是年轻渔夫：这个外地女人刚冲我笑过点过头（10–10.7 秒），转眼就背过身对着空地小声说了 8 秒，还朝我的鱼筐偏头（"see those little guys?"）。人离我三四米，我会再瞟她一眼，八成跟老的对个眼色；spec 写「两个渔夫闷头干活，只有 Riley 开口」，等于我对一个盯着我鱼说话的人毫无知觉
- 我是画左那位年长的妇女：一个穿衬衫长裤短靴、挎着面包包的女人站在更衣厅里不脱衣，直接朝热水室走去——在我眼里这跟穿着外套进澡堂一样荒唐。只捂嘴笑可以，但更像我的是指一指墙上放衣服的壁龛、或冲她的衣服摇摇头；她听不懂照样进去，也更合 bible 第 14 行「听不懂也要沟通」
- 分数：a 1 / b None → 最终 1
  | s4_st1 | 2.6–7.2 秒 | V5 回应 | 记录 | ② 分镜文字 | 我是后面槽里的踩布工：门口一个外地女人张大嘴「清清楚楚地大声嚷」（spec 2.6–4.9 秒），院子是封闭的、只有踩水声，我不可能埋头不理，等到 Tertius 喊完 Apage 后的 7.2 秒才抬头 | 便宜：3–3.5 秒两个工人被嚷声惊得**抬一下头**、脚不停；7.2–8 秒原来的反应拍改成「看见她捏着鼻子，互相看一眼咧嘴笑」，保持单独一拍 |
  | s1_st4 | 12.5–20.5 秒 | V5 回应 / V4 视线 | 记录 | ② 分镜文字 | 我是年轻渔夫：这个外地女人刚冲我笑过点过头（10–10.7 秒），转眼就背过身对着空地小声说了 8 秒，还朝我的鱼筐偏头（"see those little guys?"）。人离我三四米，我会再瞟她一眼，八成跟老的对个眼色；spec 写「两个渔夫闷头干活，只有 Riley 开口」，等于我对一个盯着我鱼说话的人毫无知觉 | 便宜：她偏头指鱼筐那一下（约 13 秒）之后，年轻渔夫抬眼看她一下、跟年长的对视一眼、耸一下肩又低头拢鱼（不说话、不看镜头、单独一拍放在 13–14 秒） |
  | s8_st8 | 4–10 秒 | V5 回应 / V6 动机 | 记录（存疑） | ① 故事 / ② 分镜文字 | 我是画左那位年长的妇女：一个穿衬衫长裤短靴、挎着面包包的女人站在更衣厅里不脱衣，直接朝热水室走去——在我眼里这跟穿着外套进澡堂一样荒唐。只捂嘴笑可以，但更像我的是指一指墙上放衣服的壁龛、或冲她的衣服摇摇头；她听不懂照样进去，也更合 bible 第 14 行「听不懂也要沟通」 | 便宜：5–6 秒加年长妇女抬下巴指一下墙上的壁龛、摇头（不说话），Riley 会错意点头笑笑照样走进蒸汽；9–10 秒两人捂嘴笑保留。存疑：若故事有意让她穿衣进热水室作笑点，这一下比划正好把笑点交给观众 |

### I66 主要 · 角色立场·路人与群众 · V6 动机
- a（1 分）：s5_st8 店主 1.5–3 秒冲一个素不相识、正直行的车夫大喊「往右」，车夫照办——画面里看不到店主为什么管这辆车、车夫为什么听他的（story.md 第 121 行也没给理由），只因为后面要回收 dextram＝右（见问题表第 1 行）；其余路人的动作各有自己的理由：s1_st3 工人去补墙、s2_st3 店主开门、s6_st3 铺主傍晚上门板
- 我是那个店主：一辆不相干的驴车好好地直走，我凭什么扯嗓子喊它往右？车夫凭什么听我的？spec 第 10–11 行和 story.md 第 121 行都只写「喊、指、车就拐」，动机只在剧情（教 Riley dextram＝右）。首帧车夫低头直走、店主抱臂站门口，画面里没有任何让店主开口的东西
- 我是画左那位年长的妇女：一个穿衬衫长裤短靴、挎着面包包的女人站在更衣厅里不脱衣，直接朝热水室走去——在我眼里这跟穿着外套进澡堂一样荒唐。只捂嘴笑可以，但更像我的是指一指墙上放衣服的壁龛、或冲她的衣服摇摇头；她听不懂照样进去，也更合 bible 第 14 行「听不懂也要沟通」
- 分数：a 1 / b None → 最终 1
  | s5_st8 | 0–4 秒 | V6 动机 | 记录 | ① 故事 / ② 分镜文字 | 我是那个店主：一辆不相干的驴车好好地直走，我凭什么扯嗓子喊它往右？车夫凭什么听我的？spec 第 10–11 行和 story.md 第 121 行都只写「喊、指、车就拐」，动机只在剧情（教 Riley dextram＝右）。首帧车夫低头直走、店主抱臂站门口，画面里没有任何让店主开口的东西 | 便宜：给车夫一个看得见的「问路/犹豫」——1–1.5 秒车夫在路口前放慢、左右张望（或回头冲店主扬一下下巴问），**此刻的我（店主）**才抬臂朝横街一指喊 "Dextram, dextram!"；车夫「抬手应一下」保留，变成道谢。或者让路口正前方堆着修路的石料/脚手架（呼应 s1_st3 地震补墙），店主喊是提醒「前面走不通」 |
  | s8_st8 | 4–10 秒 | V5 回应 / V6 动机 | 记录（存疑） | ① 故事 / ② 分镜文字 | 我是画左那位年长的妇女：一个穿衬衫长裤短靴、挎着面包包的女人站在更衣厅里不脱衣，直接朝热水室走去——在我眼里这跟穿着外套进澡堂一样荒唐。只捂嘴笑可以，但更像我的是指一指墙上放衣服的壁龛、或冲她的衣服摇摇头；她听不懂照样进去，也更合 bible 第 14 行「听不懂也要沟通」 | 便宜：5–6 秒加年长妇女抬下巴指一下墙上的壁龛、摇头（不说话），Riley 会错意点头笑笑照样走进蒸汽；9–10 秒两人捂嘴笑保留。存疑：若故事有意让她穿衣进热水室作笑点，这一下比划正好把笑点交给观众 |

### I67 待核实 · 人物逻辑 · C1
- 刻痕「看不出字形」，Riley 在 s3_st4、s8_st6 都表现完全不会拉丁语，却能指着其中一小片说「says Vibius Restitutus slept here alone」；观众会问她怎么读的
  | s7_st2 | 全镜（说 there's one 时指刻痕） | C1 | 存疑 | ① 故事 | 刻痕「看不出字形」，Riley 在 s3_st4、s8_st6 都表现完全不会拉丁语，却能指着其中一小片说「says Vibius Restitutus slept here alone」；观众会问她怎么读的 | 便宜：台词加一句交代，例如「there's a famous one — I swear this was in my textbook」，不暗示她在读这面墙；或改为她凭记忆「大概就是这种」。核实：看 story.md 里这句的来源。 |

### I68 待核实 · 人物逻辑 · C1 · C2
- Riley 不知道票价，却「挑出最小的那枚」给门房；画面没有任何犹豫或试探，观众读不出她为什么挑最小的；s8_st10 的「one tiny coin」靠观众自己倒推
  | s8_st2 | 4–8 秒 | C1 · C2 | 存疑 | ② 分镜文字 | Riley 不知道票价，却「挑出最小的那枚」给门房；画面没有任何犹豫或试探，观众读不出她为什么挑最小的；s8_st10 的「one tiny coin」靠观众自己倒推 | 便宜：在 4–6 秒补一个 Riley 的小动作（先捏起最小的，看门房一眼，等她反应），让「试探」可读。 |

### I69 待核实 · 连续性 · K1 拿灯的手
- spec 写右手掌心托灯；首帧（z1.jpg 中）她背对镜头，举灯那条胳膊看起来是左臂。核实办法：出片前请 physics/角色审稿人放大核一下手和肩的对应关系
  | s7_st6 | 首帧 | K1 拿灯的手 | 存疑 | ③ 首帧 | spec 写右手掌心托灯；首帧（z1.jpg 中）她背对镜头，举灯那条胳膊看起来是左臂。核实办法：出片前请 physics/角色审稿人放大核一下手和肩的对应关系 | 便宜：首帧重出时强调右手托灯 |

### I70 待核实 · 台词（时长与逻辑） · D3
- “Dies nihil est. Dum versas te, nox fit.” 语法通（dum + 直陈式、nox fit），但属于编写句，没有可查出处；s3_st4 的 “ito”、“platea” 偏书面
  | s8_st6 / s3_st4 | Helvia 5.1–8.8 / Felix 2.3–5.2 | D3 | 存疑 | ① 故事 | “Dies nihil est. Dum versas te, nox fit.” 语法通（dum + 直陈式、nox fit），但属于编写句，没有可查出处；s3_st4 的 “ito”、“platea” 偏书面 | 用拉丁语模型另核转写和发音（出片后）；若要更口语可改 “i” / “via”，但这是改拉丁语，不是为语速改句子，请用户定。存疑 |

### I71 待核实 · 时代与世界观 · E6 史实
- 「Vibius Restitutus slept here alone…」出自 CIL IV 2146，r02 第 194 行记在 Eumachia 巷客栈（VII.12.35，市中心），片里在斯塔比亚门边的大车店。台词说的是「这里的墙上有一句」，等于把这条涂鸦搬了地方
  | s7_st2 | 5.7–20 秒台词 | E6 史实 | 存疑 | ① 故事 | 「Vibius Restitutus slept here alone…」出自 CIL IV 2146，r02 第 194 行记在 Eumachia 巷客栈（VII.12.35，市中心），片里在斯塔比亚门边的大车店。台词说的是「这里的墙上有一句」，等于把这条涂鸦搬了地方 | 便宜：台词改成「there's a famous one, in an inn just like this」之类，不说就在这面墙上；或在 story 里注明这是艺术处理 |

### I72 待核实 · 时代与世界观 · E6 史实
- 「one tiny coin to get in」：r03 第 169、250 行写明 quadrans 是罗马城的价，庞贝实价和女区价没查到
  | s8_st10 | 台词 | E6 史实 | 存疑 | ① 故事 | 「one tiny coin to get in」：r03 第 169、250 行写明 quadrans 是罗马城的价，庞贝实价和女区价没查到 | 便宜：维持现状，交付前复核来源；不行就改成「basically pocket change」 |

### I73 待核实 · 镜头规格 · F4 节拍秒数
- overhead path 0.5–1.5 s 走 2.4 m（2.4 m/s），1.5–2 s 走 1.61 m（3.2 m/s）。按每步 0.5 秒算，每步约 1.2–1.6 m，接近小跑或跳步；文字写的是「像平常人过马路一样轻快利落」。核实办法：按 bg2 路面 x 9–13 定下垫脚石中心距，确认每步跨距不超过约 1 m
  | s2_st1 | 0.5–2s | F4 节拍秒数 | 存疑 | ② 分镜文字 | overhead path 0.5–1.5 s 走 2.4 m（2.4 m/s），1.5–2 s 走 1.61 m（3.2 m/s）。按每步 0.5 秒算，每步约 1.2–1.6 m，接近小跑或跳步；文字写的是「像平常人过马路一样轻快利落」。核实办法：按 bg2 路面 x 9–13 定下垫脚石中心距，确认每步跨距不超过约 1 m | 便宜：把 2 s 时的 path 点改到 (13.2,20.1)，2–3.5 s 再走出画；或把垫脚石间距标清楚 |

### I74 待核实 · 镜头规格 · F6·F5
- st3 画左妇女在 (0.7,7.4)、同伴在 (0.7,8.3)；st8 年长那位在 (0.75,8.2)、同伴在 (0.9,7.6)，座位前后对调；st3 靠里的第三位在 st8 里没了。核实方法：对两镜 overhead 的 key 和首帧服色
  | s8_st3 → st8 | — | F6·F5 | 存疑 | ② 分镜文字 | st3 画左妇女在 (0.7,7.4)、同伴在 (0.7,8.3)；st8 年长那位在 (0.75,8.2)、同伴在 (0.9,7.6)，座位前后对调；st3 靠里的第三位在 st8 里没了。核实方法：对两镜 overhead 的 key 和首帧服色 | 核对座位，统一（便宜） |

### I75 待核实 · 角色立场·路人与群众 · V1 语言
- 我是店主，冲车夫喊方向时口语更像 "Ad dextram!" 或 "Dextrorsum!"；单说 "Dextram"（宾格、省略了 viam/partem）不太像随口喊的话。story.md 第 73 行 Felix 说的是 "ito ad dextram"，可回收的是同一个词
  | s5_st8 | 1.6–2.6 秒 | V1 语言 | 存疑 | ③ prompt / 规则源（考据） | 我是店主，冲车夫喊方向时口语更像 "Ad dextram!" 或 "Dextrorsum!"；单说 "Dextram"（宾格、省略了 viam/partem）不太像随口喊的话。story.md 第 73 行 Felix 说的是 "ito ad dextram"，可回收的是同一个词 | 便宜：请拉丁语审稿位核实；可改 "Ad dextram, ad dextram!"，dextram 照样听得清、Riley 的回收台词不用改 |

### I76 记录 · 世界物理 · P6 距离
- overhead 里 Riley x=13.45–13.55、Vibia x=14.3，两人身体之间只剩约 0.35 m，规格却写「一臂宽」「留着一人宽的空地」。首帧里 Riley 走在人行道中间，没贴路缘。
  | s2_st4 | 0–1.5 秒 | P6 距离 | 记录 | ② 分镜文字 / ③ 首帧 | overhead 里 Riley x=13.45–13.55、Vibia x=14.3，两人身体之间只剩约 0.35 m，规格却写「一臂宽」「留着一人宽的空地」。首帧里 Riley 走在人行道中间，没贴路缘。 | 便宜：Riley 路径 x 改到 13.3 上下，或把规格改成「侧身擦肩」；首帧可不重出。 |

### I77 记录 · 世界物理 · P8
- 规格写「右脚抬起、悬在第一块垫脚石上方」，首帧里前脚靴底已经贴着石头顶面。0–0.5 秒的第一步等于提前做完了，可能会被重复一遍。
  | s2_st1 | 0 秒 | P8 | 记录 | ③ 首帧 | 规格写「右脚抬起、悬在第一块垫脚石上方」，首帧里前脚靴底已经贴着石头顶面。0–0.5 秒的第一步等于提前做完了，可能会被重复一遍。 | 便宜：首帧可以照用，规格第 0 秒改成「右脚刚落上第一块石头」；或重出首帧，把脚抬高。 |

### I78 记录 · 世界物理 · P10
- 「快步走过来」，按 overhead 是 (38.18,51.9) 到 (38.05,56)，4.1 m 用 4.5 秒≈0.9 m/s，是慢走的速度。时长里加了台词，不算拉慢，但「快步」和实际时长对不上。
  | s1_st1 | 16.5–21 秒 | P10 | 记录 | ② 分镜文字 | 「快步走过来」，按 overhead 是 (38.18,51.9) 到 (38.05,56)，4.1 m 用 4.5 秒≈0.9 m/s，是慢走的速度。时长里加了台词，不算拉慢，但「快步」和实际时长对不上。 | 便宜：把「快步」改成「边说边朝镜头走」，或把走近的时间压到约 3 秒。 |

### I79 记录 · 世界物理 · P9 光影
- 规格写「画右这一侧的墙面和整个街面在柔和的阴影里」；首帧画右一排店面和路面都被照成暖金色。
  | s1_st5 | 0 秒首帧 | P9 光影 | 记录 | ③ 首帧 | 规格写「画右这一侧的墙面和整个街面在柔和的阴影里」；首帧画右一排店面和路面都被照成暖金色。 | 便宜：首帧调光或重出（不急）。 |

### I80 记录 · 世界物理 · P3 交接（打结方式）
- 「拎起布的四角在顶上打成一个结，留着两个长布角」说不通，四角同结会留四个角头；后面 8.5–11s 只用「两个长布角」系腰带
  | s3_st7 | 3.5–6s | P3 交接（打结方式） | 记录 | ② 分镜文字 | 「拎起布的四角在顶上打成一个结，留着两个长布角」说不通，四角同结会留四个角头；后面 8.5–11s 只用「两个长布角」系腰带 | 便宜：改成「两对角先打一个结，另两个对角留长」 |

### I81 记录 · 世界物理 · P10 速度（过快）
- 两枚钱各走一个来回（约 0.65 m）共 1.3s；挪步、探身、拿面包、回身放下 1.4s。真人约各要 2s
  | s3_st1 | 9–11.7s | P10 速度（过快） | 记录 | ② 分镜文字 | 两枚钱各走一个来回（约 0.65 m）共 1.3s；挪步、探身、拿面包、回身放下 1.4s。真人约各要 2s | 便宜：拈钱改成「一把拢起两枚放进碗」，或者 11.7–13s 对视压到 0.6s，补给拿面包 |

### I82 记录 · 世界物理 · P1 / P3 手
- 只写了左手捏出、摊掌，没写由哪只手逐枚放下；单手从掌心逐枚放钱很别扭，模型可能多画一只手或让钱黏在掌心
  | s3_st1 | 6.3–9s | P1 / P3 手 | 记录 | ② 分镜文字 | 只写了左手捏出、摊掌，没写由哪只手逐枚放下；单手从掌心逐枚放钱很别扭，模型可能多画一只手或让钱黏在掌心 | 便宜：写明「右手从左掌心拈起，一枚一枚放下」 |

### I83 记录 · 世界物理 · P4 支撑
- 托板一头搁台沿、左手扶着呈斜面，右手把下层三个面包「一个个翻过来看底」，上层两个叠在上面，会滚落或变形
  | s3_st4 | 8–17s | P4 支撑 | 记录 | ② 分镜文字 | 托板一头搁台沿、左手扶着呈斜面，右手把下层三个面包「一个个翻过来看底」，上层两个叠在上面，会滚落或变形 | 便宜：改成「只拿起上层的面包翻看底、放回原处，拍掉面粉」 |

### I84 记录 · 世界物理 · P9 效果来源（光）
- 炉口距 Riley 约 6.7 m，又在店里深处，清晨直射阳光下她脸上不会有可见的炉火橙光
  | s3_st2 | 全镜 | P9 效果来源（光） | 记录 | ② 分镜文字 | 炉口距 Riley 约 6.7 m，又在店里深处，清晨直射阳光下她脸上不会有可见的炉火橙光 | 便宜：删掉「火光映到她脸上」，只留「面包表面微暖」或干脆不写 |

### I85 记录 · 世界物理 · P9 影子
- 正午太阳高度约 69°，6 m 高房屋在东西向街上投影约 2.3 m，不是「一窄条」；南北向街才接近零
  | s4_st4 | 全镜 | P9 影子 | 记录 | ② 分镜文字 | 正午太阳高度约 69°，6 m 高房屋在东西向街上投影约 2.3 m，不是「一窄条」；南北向街才接近零 | 便宜：写成「南北向的北街两侧几乎没有影子，横街里有一道短影」 |

### I86 记录 · 世界物理 · P6 距离
- st5 写「两人相隔不到一米」，st6 首帧 Riley 和 Helvia 中间隔着布包、油瓶、刮板，目测约 1.5m；镜头相接时 Helvia 像往外挪了
  | s8_st6 | 0s | P6 距离 | 记录 | ③ 首帧 | st5 写「两人相隔不到一米」，st6 首帧 Riley 和 Helvia 中间隔着布包、油瓶、刮板，目测约 1.5m；镜头相接时 Helvia 像往外挪了 | 便宜：首帧把 Helvia 往画左挪近，或接受 |

### I87 记录 · 世界物理 · P2 道具状态（钱袋口）
- s6_st2 F 用左手拉开袋颈绳结、撑开袋口，把钱放进去后抽出空手，没写扎回去；s6_st5 首帧钱袋是扎紧鼓着的，10–12 秒还要“掂一掂”。观众不一定注意，模型可能让钱袋一直敞着口，或者在镜头切换后突然扎好
  | s6_st2→s6_st5 | s6_st2 10–12.5 秒 → s6_st5 0 秒 | P2 道具状态（钱袋口） | 记录 | ② 分镜文字 | s6_st2 F 用左手拉开袋颈绳结、撑开袋口，把钱放进去后抽出空手，没写扎回去；s6_st5 首帧钱袋是扎紧鼓着的，10–12 秒还要“掂一掂”。观众不一定注意，模型可能让钱袋一直敞着口，或者在镜头切换后突然扎好 | 便宜：s6_st2 10–12.5 秒加一句“把绳一拉扎上”，或把节拍延到 13 秒 |

### I88 记录 · 世界物理 · P10 真实速度／俯视图和 spec 对不上
- 首帧按 32mm 估算，F 离镜头约 4.8 米，画右边缘离 F 约 3.4 米；R 3.8 秒从画右入画、5 秒停在 F 右边 1 米，1.2 秒要走约 2.4 米（每秒约 2 米，对一个“有点累”的人太快）；俯视图 R 0–5 秒从 (11.4,7.4) 匀速走到 (6.4,7.4)，按这个速度约 2.3 秒就入画了。另外俯视图里行人 5.5 秒才走到 x 7.6，还在画内（画右边缘约 x 8.5），spec 却写“约 5.5 秒走出画右”
  | s6_st1 | 3.5–5 秒；两个行人 0–5.5 秒 | P10 真实速度／俯视图和 spec 对不上 | 记录 | ② 分镜文字＋俯视图 | 首帧按 32mm 估算，F 离镜头约 4.8 米，画右边缘离 F 约 3.4 米；R 3.8 秒从画右入画、5 秒停在 F 右边 1 米，1.2 秒要走约 2.4 米（每秒约 2 米，对一个“有点累”的人太快）；俯视图 R 0–5 秒从 (11.4,7.4) 匀速走到 (6.4,7.4)，按这个速度约 2.3 秒就入画了。另外俯视图里行人 5.5 秒才走到 x 7.6，还在画内（画右边缘约 x 8.5），spec 却写“约 5.5 秒走出画右” | 便宜：入画时间改成约 3.0 秒（或者停下改到 5.5 秒）；俯视图里行人的终点改到 x≥8.6 |

### I89 记录 · 人物逻辑 · C7 / C5
- s2_st8 她刚憋着笑回头瞟 Vibia，st4 却从 Vibia 一臂宽处走过，两人没有任何眼神或笑
  | s2_st4 | 0–1.5 | C7 / C5 | 记录 | ② 分镜文字 | s2_st8 她刚憋着笑回头瞟 Vibia，st4 却从 Vibia 一臂宽处走过，两人没有任何眼神或笑 | 便宜：加一个 Riley 抿嘴笑、对 Vibia 点一下头的小动作，Vibia 仍低头擦罐；仍从背影拍，不重出 |

### I90 记录 · 人物逻辑 · C8
- 「Garum?」后 Felix 没有反应，0.6 秒后直接开口，反应没钉在这个词上
  | s3_st4 | 1.1–2.3 | C8 | 记录 | ② 分镜文字 | 「Garum?」后 Felix 没有反应，0.6 秒后直接开口，反应没钉在这个词上 | 便宜：Felix 听到 garum 眼皮一抬或手停半拍，再答；与问题 1 一起改 |

### I91 记录 · 人物逻辑 · C6
- 扛柴男人从举臂自拍、穿裤装的外国女人身边擦过，只「侧身让路」，不看她
  | s4_st3 | 约 7–10 | C6 | 记录 | ② 分镜文字 | 扛柴男人从举臂自拍、穿裤装的外国女人身边擦过，只「侧身让路」，不看她 | 便宜：加一个余光扫一眼再赶路，保持轻微（不要停步、不要回头） |

### I92 记录 · 人物逻辑 · C7 · C2
- st8 末 Riley 已「自己也朝画右指了一下」，st9 第 0 秒又「愣着、Wait」才恍然大悟，两处的领悟时点打架；st9 末「我一天都走错了」之后，st2 她直接走进熟食铺，没有任何往右看或转身的意思，观众不知道她为什么不去纠正方向
  | s5_st8 → s5_st9 | st8 13 秒末；st9 全镜 | C7 · C2 | 记录 | ② 分镜文字 | st8 末 Riley 已「自己也朝画右指了一下」，st9 第 0 秒又「愣着、Wait」才恍然大悟，两处的领悟时点打架；st9 末「我一天都走错了」之后，st2 她直接走进熟食铺，没有任何往右看或转身的意思，观众不知道她为什么不去纠正方向 | 便宜：st8 末改成「皱眉看着横街口，没动手」，指的动作留到 st9 恍然后；st9 末加一个往右看一眼再摇头的动作，交代「先吃饭」。 |

### I93 记录 · 人物逻辑 · C8
- Asellina「放下手，抱起胳膊看着她对着空气说话，嘴角一扬」，约 4 秒没有手上的活，是个站桩
  | s5_st12 | 约 4–8 秒 | C8 | 记录 | ② 分镜文字 | Asellina「放下手，抱起胳膊看着她对着空气说话，嘴角一扬」，约 4 秒没有手上的活，是个站桩 | 便宜：让她一边擦台面或数碗里的钱一边抬眼瞥一下，不要抱胳膊定住。 |

### I94 记录 · 人物逻辑 · C1
- Helvia 听不懂英语，spec 却写「听到 rub oil all over yourself 时抬眼瞟她」；反应钉在她听不懂的词上
  | s8_st9 | 1.6–10 秒 | C1 | 记录 | ② 分镜文字 | Helvia 听不懂英语，spec 却写「听到 rub oil all over yourself 时抬眼瞟她」；反应钉在她听不懂的词上 | 便宜：改成「看到她把油亮的小臂抬起来给镜头看时抬眼瞟她」，钉在手势上。 |

### I95 记录 · 连续性 · K9 视角来源
- st8（他拍）最后一拍她右手指向画右、不说话；st9 第 0 秒已经是右臂伸直持镜的自拍，嘴还张着，处在同一个连续时刻，中间没有举起相机的动作，也没有时间跳跃
  | s5_st8 → s5_st9 | 接点 0s | K9 视角来源 | 记录 | ② 分镜文字 | st8（他拍）最后一拍她右手指向画右、不说话；st9 第 0 秒已经是右臂伸直持镜的自拍，嘴还张着，处在同一个连续时刻，中间没有举起相机的动作，也没有时间跳跃 | 便宜：st9 0–0.5 s 加「她举起相机，画面晃上来」，或者 st8 结尾加一拍她抬手举相机 |

### I96 记录 · 连续性 · K1 道具去向
- s5_st7 写「面包布和剩下的面包留在台面上」，s6/s7 再没出现，等于把面包丢在了熟食铺；画面上不冲突，但故事里没交代
  | s5_st7 → s6 | 场间 | K1 道具去向 | 记录 | ① 故事 | s5_st7 写「面包布和剩下的面包留在台面上」，s6/s7 再没出现，等于把面包丢在了熟食铺；画面上不冲突，但故事里没交代 | 可选：s5_st7 结尾加一拍她把面包推给 Asellina 或包起来带走；不改也不会穿帮 |

### I97 记录 · 台词（时长与逻辑） · D7
- s5_st7 “Now I just have to find a bed.” 之后隔一场（傍晚），s6_st3 又说 “I still don’t have anywhere to sleep” ，信息重复
  | s5_st7→s6_st3 | s5_st7 5.1–10.7 / s6_st3 6.4–11.6 | D7 | 记录 | ① 故事 | s5_st7 “Now I just have to find a bed.” 之后隔一场（傍晚），s6_st3 又说 “I still don’t have anywhere to sleep” ，信息重复 | 不删台词；让 s6_st3 开头多一个她看天色、摸肚子的动作表示时间过了几小时，或把 s6_st3 说成 “…I still haven’t found anywhere to sleep” 以承接 “find a bed”。便宜，可存疑 |

### I98 记录 · 台词（时长与逻辑） · D7
- st2 末尾 “Yeah. This is it.” 是大声自嘲，st4 开口 “Okay, see those little guys?” 变成小声分享秘密，中间换景、换机位没有一句话或动作交代
  | s1_st2→s1_st4 | s1_st4 第 0 秒 | D7 | 记录 | ② 分镜文字 | st2 末尾 “Yeah. This is it.” 是大声自嘲，st4 开口 “Okay, see those little guys?” 变成小声分享秘密，中间换景、换机位没有一句话或动作交代 | 在 st4 的 12.5 秒开口前加一拍：Riley 压低身子、朝渔夫那边偏头再转向镜头，让音量变化有来由（节拍里已有 “微微探身”，加半句说明即可）。便宜 |

### I99 记录 · 台词（时长与逻辑） · D5（材料）
- 接点表把多人对话按 “/” 拆开后，Helvia、Felix、Asellina 的拉丁语被记在 Riley 名下（如 s8_st6→st7 写成 “Riley：Dum versas te, nox fit.”），会误导审稿人
  | materials/junctions.md（工具） | s3_st1→st2、s4_st1→st2、s8_st6→st7、s5_st13→st6 | D5（材料） | 记录 | 规则源 | 接点表把多人对话按 “/” 拆开后，Helvia、Felix、Asellina 的拉丁语被记在 Riley 名下（如 s8_st6→st7 写成 “Riley：Dum versas te, nox fit.”），会误导审稿人 | 修 tools/shot_junctions.py 的台词拆分，按说话人切。便宜（改工具） |

### I100 记录 · 母语听感 · N1 / N2
- 「Like, real, two-thousand-years-ago Pompeii.」连字符堆叠，像小标题；还有「it worked. It actually worked.」前面已说过 Okay…
  | s1_st1 | 全镜 | N1 / N2 | 记录 | ② | 「Like, real, two-thousand-years-ago Pompeii.」连字符堆叠，像小标题；还有「it worked. It actually worked.」前面已说过 Okay… | 便宜。改成：「Oh my god. Okay — okay, it worked. It actually worked. That's Pompeii. That's, like, actual Pompeii. It's — it's actually there.」 |

### I101 记录 · 母语听感 · N2
- 「That's why they've got these big stepping stones, so you don't have to walk through… whatever's in there.」讲解腔，「you don't have to」像在写科普
  | s2_st2 | 全镜 | N2 | 记录 | ② | 「That's why they've got these big stepping stones, so you don't have to walk through… whatever's in there.」讲解腔，「you don't have to」像在写科普 | 便宜。改成：「Okay, made it. So there's no sewer here — the street is the drain. That's what the stones are for. Yeah. I'm not walking through that.」 |

### I102 记录 · 母语听感 · N2
- 「See all these cracks? There was this huge earthquake here, like, twelve years ago — and they're still patching it up.」冷知识讲解；且 s1_st4 刚用过「Okay, see those little guys?」，两镜连用「See…」
  | s1_st3 | 全镜 | N2 | 记录 | ② | 「See all these cracks? There was this huge earthquake here, like, twelve years ago — and they're still patching it up.」冷知识讲解；且 s1_st4 刚用过「Okay, see those little guys?」，两镜连用「See…」 | 便宜。改成：「Oh — look at these cracks. They're all patched. I think there was a huge earthquake here, like, a decade ago? And they're still fixing it.」 |

### I103 记录 · 母语听感 · N2
- 「everyone here waters their wine down」语序不顺（真人说 waters down their wine / waters it down）；「apparently」又出现一次
  | s5_st14 | 全镜 | N2 | 记录 | ② | 「everyone here waters their wine down」语序不顺（真人说 waters down their wine / waters it down）；「apparently」又出现一次 | 便宜。改成：「Oh — she's putting water in it. Yeah, apparently everyone waters down their wine here. Drinking it straight is, like, a barbarian thing.」 |

### I104 记录 · 母语听感 · N4
- Honestly 出现 3 次（s4_st5、s7_st1、s7_st3），basically 4 次，literally 4 次，「Yeah.」当收尾 4 次（s1_st2、s2_st8、s5_st14、s6_st3）
  | s7_st3 / s7_st1 / s4_st5 | 全集 | N4 | 记录 | 规则源 | Honestly 出现 3 次（s4_st5、s7_st1、s7_st3），basically 4 次，literally 4 次，「Yeah.」当收尾 4 次（s1_st2、s2_st8、s5_st14、s6_st3） | 便宜。口头禅要分散：三处 Honestly 留一处，其余换成 Actually / I mean / Okay but；basically 留两处 |

### I105 记录 · 母语听感 · —
- 面包房问路一段用户已指出，不展开
  | s3_st4（已知） | — | — | 记录 | — | 面包房问路一段用户已指出，不展开 | 待用户挑 |

### I106 记录 · 时代与世界观 · E2 建筑
- 画右屋檐下（约 x1240–1300,y190–240）有一截金属落水管加弯头（裁切图 s5st9_gutter.png），在背景虚化里看着像现代建筑配件
  | s5_st9 | 0 秒首帧 | E2 建筑 | 记录 | ③ prompt 或首帧 | 画右屋檐下（约 x1240–1300,y190–240）有一截金属落水管加弯头（裁切图 s5st9_gutter.png），在背景虚化里看着像现代建筑配件 | 便宜：首帧修掉；负面词加「金属落水管、檐沟」 |

### I107 记录 · 时代与世界观 · E3 服饰
- prompt 写「米白粗亚麻裹身长衣」，负面词也已有「翻领浴袍、毛巾布浴袍」，但首帧 s8_st3 两侧多位妇女是带翻领的厚毛巾布袍子，s8_st8 画左两位也像浴袍
  | s8_st3、s8_st8 | 0 秒首帧 | E3 服饰 | 记录 | ③ prompt 或首帧 | prompt 写「米白粗亚麻裹身长衣」，负面词也已有「翻领浴袍、毛巾布浴袍」，但首帧 s8_st3 两侧多位妇女是带翻领的厚毛巾布袍子，s8_st8 画左两位也像浴袍 | 便宜：重出首帧，把衣服写成「一整块薄亚麻布从腋下裹身、无领无袖口」 |

### I108 记录 · 时代与世界观 · E3 发型胡须
- r05 第 35、193 行：75 年男人刮净胡子。s5_st6 画右喝酒的男人是一圈短须（prompt 写「短胡茬」）；s5_st8 门口店主留胡子；s5_st7 后景两名食客也有胡子，而 s5_st7 的 prompt 没写刮脸
  | s5_st6、s5_st8、s5_st7 | 0 秒首帧 | E3 发型胡须 | 记录 | ③ prompt 或首帧 / ② 分镜文字 | r05 第 35、193 行：75 年男人刮净胡子。s5_st6 画右喝酒的男人是一圈短须（prompt 写「短胡茬」）；s5_st8 门口店主留胡子；s5_st7 后景两名食客也有胡子，而 s5_st7 的 prompt 没写刮脸 | 便宜：路人模板统一写「脸刮得干净」，s5_st6 把「短胡茬」改成「刮得干净、下巴青」；首帧修掉胡须 |

### I109 记录 · 时代与世界观 · E1 器物
- p1 卡写「嘴上燃着一小朵黄色火苗」，首帧（裁切图 s6st4_lamp.png）火苗却从灯身尾部冒出，前端的灯嘴空着，看着像碟形烛台
  | s6_st4 | 0 秒首帧 | E1 器物 | 记录 | ③ prompt 或首帧 | p1 卡写「嘴上燃着一小朵黄色火苗」，首帧（裁切图 s6st4_lamp.png）火苗却从灯身尾部冒出，前端的灯嘴空着，看着像碟形烛台 | 便宜：首帧重出，火苗放在灯嘴 |

### I110 记录 · 时代与世界观 · E1 器物
- 放大看，Riley 举起的铜币人像是长发、编辫、戴月桂冠的少年侧像，不像 75 年 as 币上的维斯帕先（秃顶、宽脸）；没有可读字母
  | s4_st5 | 0 秒首帧 | E1 器物 | 记录 | ③ prompt 或首帧 | 放大看，Riley 举起的铜币人像是长发、编辫、戴月桂冠的少年侧像，不像 75 年 as 币上的维斯帕先（秃顶、宽脸）；没有可读字母 | 便宜：首帧重出，人像写成「秃顶、宽下巴的老年男人侧像，浮雕模糊」 |

### I111 记录 · 时代与世界观 · E2 建筑
- s3_st2 背景门框带线脚和檐口，像后世的意大利或殖民地小镇；s4_st4 路口四角是独立的坡顶小屋，庞贝街区应是连续临街墙面
  | s3_st2、s4_st4 | 0 秒首帧 | E2 建筑 | 记录 | ③ prompt 或首帧 | s3_st2 背景门框带线脚和檐口，像后世的意大利或殖民地小镇；s4_st4 路口四角是独立的坡顶小屋，庞贝街区应是连续临街墙面 | 便宜：要重出这两张首帧时，顺带把门框改成素面凝灰岩框，路口两侧改成连续店面墙 |

### I112 记录 · 时代与世界观 · —
- 已知问题（BRIEF 已列，用户已指出），这一类没有新增
  | s3（面包房问路一段） | — | — | 记录 | ① 故事 | 已知问题（BRIEF 已列，用户已指出），这一类没有新增 | — |

### I113 记录 · 镜头规格 · F6 轴线（水流方向）
- s2_st1 的 prompt 第 10 行写水「从画面深处的上坡往镜头这边流」，机位朝北，等于水往南流；s2_st3 机位朝东、画左是北，文字却写水「从画右往画左顺着街流」，等于往北流（上坡）。这两镜在播放时相邻，同一条街的流向前后相反
  | s2_st3 / s2_st1 | st3 0–8s；st1 0–5s | F6 轴线（水流方向） | 记录 | ② 分镜文字 | s2_st1 的 prompt 第 10 行写水「从画面深处的上坡往镜头这边流」，机位朝北，等于水往南流；s2_st3 机位朝东、画左是北，文字却写水「从画右往画左顺着街流」，等于往北流（上坡）。这两镜在播放时相邻，同一条街的流向前后相反 | 便宜：把 s2_st3 改成「从画左往画右（往南、下坡）流」，或统一改 st1；驴车方向可以不动 |

### I114 记录 · 镜头规格 · F6 左右关系
- 两镜都朝南拍。st8 里 Riley 在 x=15、Vibia 在 x=14.3，Vibia 在画右，首帧也是 Riley 居中偏左、Vibia 在画右；st4 第 0 秒 Riley 已经到了 x=13.55（路缘），Vibia 在画中偏左、Riley 在画中偏右。剪接点上两人左右对调，Riley 还横跳了约 1.45 m
  | s2_st8→s2_st4 | st8 11s / st4 0s | F6 左右关系 | 记录 | ② 分镜文字 | 两镜都朝南拍。st8 里 Riley 在 x=15、Vibia 在 x=14.3，Vibia 在画右，首帧也是 Riley 居中偏左、Vibia 在画右；st4 第 0 秒 Riley 已经到了 x=13.55（路缘），Vibia 在画中偏左、Riley 在画中偏右。剪接点上两人左右对调，Riley 还横跳了约 1.45 m | 便宜：st4 开头加半拍「Riley 从 Vibia 身后绕到路缘一侧」，或接受为剪接省略，在剪辑时确认 |

### I115 记录 · 镜头规格 · F3 画面位置
- 文字和 overhead（出水口 x@0=-0.08）写的是「牛头出水口和石槽在她正后方，大半被她的头和肩挡住」；首帧里牛头出水口在画面 0.24 处、Riley 右肩后完整露出，水柱看得清
  | s2_st8 | 0–11s | F3 画面位置 | 记录 | ③ prompt 或首帧 | 文字和 overhead（出水口 x@0=-0.08）写的是「牛头出水口和石槽在她正后方，大半被她的头和肩挡住」；首帧里牛头出水口在画面 0.24 处、Riley 右肩后完整露出，水柱看得清 | 便宜：把文字改成「出水口在她右肩后（画左）露出」，和首帧一致 |

### I116 记录 · 镜头规格 · F3 画面位置（后景）
- 按 bg3 平面图：东磨约 (7.0,1.8)，砖炉约 (11.0,1.5)。s3_st1 机位下砖炉应在约 0.37 处、东磨贴画左缘；首帧里炉在 0.6、东磨在 0.44。s3_st6 用 50mm，砖炉偏离镜轴约 49°，应在画外；首帧和文字「身后是店里的石磨和炉火」都把炉放在画右。s3_st5 摇 50° 才摇到炉口，说明炉在店的东头深处，几镜之间店内布局对不上
  | s3_st1 / s3_st6（及 st4/st7） | 全镜 | F3 画面位置（后景） | 记录 | ③ prompt 或首帧 | 按 bg3 平面图：东磨约 (7.0,1.8)，砖炉约 (11.0,1.5)。s3_st1 机位下砖炉应在约 0.37 处、东磨贴画左缘；首帧里炉在 0.6、东磨在 0.44。s3_st6 用 50mm，砖炉偏离镜轴约 49°，应在画外；首帧和文字「身后是店里的石磨和炉火」都把炉放在画右。s3_st5 摇 50° 才摇到炉口，说明炉在店的东头深处，几镜之间店内布局对不上 | 便宜：接受首帧布局，就改 bg3 平面图与 s3_st5 的摇角说明；或把 s3_st6 文字改成只有石磨、炉火只映出红光 |

### I117 记录 · 镜头规格 · F4 节拍秒数 / F3
- 镜头 0–6.5 s 以 1.11 m/s 前移，工人固定在 (32.6,19.25)，偏轴角到约 4.75 s 就超过半视角 32.7°。文字写的 4.8–5.6 s「点头回礼、转身」会发生在画右边缘外，3–4 s「目光从靴子抬到脸」也已经在 0.6–0.85 的画右边缘
  | s1_st3 | 3–5.6s | F4 节拍秒数 / F3 | 记录 | ② 分镜文字 | 镜头 0–6.5 s 以 1.11 m/s 前移，工人固定在 (32.6,19.25)，偏轴角到约 4.75 s 就超过半视角 32.7°。文字写的 4.8–5.6 s「点头回礼、转身」会发生在画右边缘外，3–4 s「目光从靴子抬到脸」也已经在 0.6–0.85 的画右边缘 | 便宜：把打招呼和回礼提前约 0.8 s（3.2–4.8 s），或把工人位置写近镜轴 0.5 m |

### I118 记录 · 镜头规格 · F4 节拍秒数
- 文字写「快步走过来」，path 是 3 s 走 2.7 m（0.9 m/s），比普通步速还慢；对白 2.1 s，节拍并不挤
  | s1_st1 | 16.5–19.5s | F4 节拍秒数 | 记录 | ② 分镜文字 | 文字写「快步走过来」，path 是 3 s 走 2.7 m（0.9 m/s），比普通步速还慢；对白 2.1 s，节拍并不挤 | 便宜：把「快步」改成「笑着走过来」，或把 path 压到 2 s 走完 |

### I119 记录 · 镜头规格 · F2
- 站位图上 Riley 面朝与看镜头方向夹角 88°（st2/st12）、76°（st4），是侧脸；文字写「四分之三侧脸」；st2/st12 首帧是侧脸，st4 首帧画面放大 27%、头顶被裁
  | s5_st2 / st12 / st4 | 全镜 | F2 | 记录 | ② 分镜文字 | 站位图上 Riley 面朝与看镜头方向夹角 88°（st2/st12）、76°（st4），是侧脸；文字写「四分之三侧脸」；st2/st12 首帧是侧脸，st4 首帧画面放大 27%、头顶被裁 | 文字改成「侧脸」，或把朝向往镜头转约 30°（便宜） |

### I120 记录 · 镜头规格 · F5
- st6 站在柜台东头外侧 (8.8,5.4) 的两个食客，到 st5（u≈0.79）、st7（u≈0.91）都不在；st7 另有两个男人坐在店里，overhead 却放在短边外 (10.1,3.2)
  | s5_st6 → st5 → st7 | — | F5 | 记录 | ② 分镜文字 | st6 站在柜台东头外侧 (8.8,5.4) 的两个食客，到 st5（u≈0.79）、st7（u≈0.91）都不在；st7 另有两个男人坐在店里，overhead 却放在短边外 (10.1,3.2) | 统一成同一对人：st7 的 overhead 把两人挪进店里，或交代 st6 那两人已离开（便宜） |

### I121 记录 · 镜头规格 · F5
- overhead 只放了 7 个妇女里的 3 个，文字和首帧是 7 个
  | s8_st3 | 全镜 | F5 | 记录 | ③ prompt 或首帧 | overhead 只放了 7 个妇女里的 3 个，文字和首帧是 7 个 | 补齐 7 个点位（便宜） |

### I122 记录 · Prompt 文本 · T6 参考清单
- 正文写了布包、陶油灯、收钱碗，参考里没挂 p3/p1/p2。布包在画框下缘外，影响小；s6_st3 的壁龛小油灯和 s7_st5 路人的小陶灯只是远景。
  | s4_st2、s4_st5、s5_st1/9/11、s8_st4、s6_st3、s7_st5、s3_st6 | s4_st2 全镜、s4_st5 8.8–10.3 秒、s6_st3 壁龛、s7_st5 端灯路人 | T6 参考清单 | 记录 | ③ prompt | 正文写了布包、陶油灯、收钱碗，参考里没挂 p3/p1/p2。布包在画框下缘外，影响小；s6_st3 的壁龛小油灯和 s7_st5 路人的小陶灯只是远景。 | 便宜：布包出现在下缘外时可以不挂，但正文别写「从布包后面伸手」。要在画内露出的道具，补挂对应 p 参考。 |

### I123 记录 · 角色立场·Riley · V3
- 首帧放大看：眼睛半闭、嘴唇微张、头微仰，表情慵懒、近乎性感，不是「又热又尴尬」
  | s8_st4 | 首帧 | V3 | 记录 | ③ prompt 或首帧 | 首帧放大看：眼睛半闭、嘴唇微张、头微仰，表情慵懒、近乎性感，不是「又热又尴尬」 | 此刻的我：热得眯眼皱眉、鼓腮吐气，额头冒汗，有点狼狈。重出首帧（便宜） |

### I124 记录 · 角色立场·Tertius · V3 表情
- 人物卡外观「眉头总是皱着，神情不耐烦」，再写「皱眉」无增量；我在画左约 1/4 处、中全景，脸小
  | s4_st1 | 5.0–7.2 | V3 表情 | 记录 | ② 分镜文字 | 人物卡外观「眉头总是皱着，神情不耐烦」，再写「皱眉」无增量；我在画左约 1/4 处、中全景，脸小 | 此刻的我会：停下脚、眉头拧紧、嘴角往下一撇、下巴一抬——靠停脚和转身这些大动作让观众读出「被惹毛了」，不要求脸部特写式表演。**便宜** |

### I125 记录 · 角色立场·Asellina · V3 表情／V7
- 「只抬眼瞥了她一下，不笑」；人物卡「嘴角常带着做生意的笑」，前后镜都在笑
  | s5_st14 | 10.8–18.8 | V3 表情／V7 | 记录 | ② 分镜文字 | 「只抬眼瞥了她一下，不笑」；人物卡「嘴角常带着做生意的笑」，前后镜都在笑 | 便宜：改「低头擦台面，嘴角还挂着一点笑，抬眼瞥她一下，摇摇头接着擦」 |

### I126 记录 · 角色立场·Asellina · V4 视线
- 「抱起胳膊看着她对空气说话……不看镜头」：她第一次对空街说话，我没有顺她目光找人这一下
  | s5_st12 | 3.5–8.6 | V4 视线 | 记录 | ② 分镜文字 | 「抱起胳膊看着她对空气说话……不看镜头」：她第一次对空街说话，我没有顺她目光找人这一下 | 便宜：加「她转脸那一下，Asellina 顺着她的方向朝她身后的街面（画右深处，不朝镜头）瞟一眼，没人，再看回她，嘴角一扬」；prompt 里保留「不看镜头」 |

### I127 记录 · 角色立场·Asellina · V3 表情
- 17 秒内三次「挑眉」
  | s5_st2 / s5_st10 | st2 2–3；st10 0.3–1.2、5.5–8 | V3 表情 | 记录 | ② 分镜文字 | 17 秒内三次「挑眉」 | 便宜：删 st10 第 5.5–8 秒的「又挑眉」，改「看回画右，笑着等她」 |

### I128 记录 · 角色立场·Asellina · V1 语言
- 「响亮利落」，两人「相距一米多」（走位）；她盯的是冒热气的罐，我报的是酒价
  | s5_st2 | 4.1–6.2 | V1 语言 | 记录 | ② 分镜文字 | 「响亮利落」，两人「相距一米多」（走位）；她盯的是冒热气的罐，我报的是酒价 | 便宜：音量改「利落带笑、招呼客人的嗓门」；3–4 秒放勺时「用勺柄点一下两人中间的空陶杯」再竖手指 |

### I129 记录 · 角色立场·Asellina · V1 语言
- 「只喊一声 Euge!」，对一米外的人
  | s5_st13 | 10.4–11.0 | V1 语言 | 记录 | ② 分镜文字 | 「只喊一声 Euge!」，对一米外的人 | 便宜：「喊」改「笑着脱口一声」 |

### I130 记录 · 角色立场·Asellina · V4 视线
- Asellina 在这 4 秒无视线描写，0 秒只写「看着她」
  | s5_st3 | 1.5–5.5 | V4 视线 | 记录 | ② 分镜文字 | Asellina 在这 4 秒无视线描写，0 秒只写「看着她」 | 便宜：加「Asellina 的眼睛跟着她的手：看一眼她手心，再看两枚钱落到台面」 |

### I131 记录 · 角色立场·Asellina · V3 表情
- st12_first_frame.png 画左 Asellina 眉头紧皱、像怀疑不悦，规格是「愣着」
  | s5_st12 | 首帧 0 | V3 表情 | 记录 | ③ 首帧 | st12_first_frame.png 画左 Asellina 眉头紧皱、像怀疑不悦，规格是「愣着」 | 便宜：首帧重出或 prompt 写「微微一怔，眉头略抬，不皱眉」 |

### I132 记录 · 角色立场·Fortunata · V7
- 人物卡依据写「先收钱再领路」，分镜只指路不领路
  | s6_st5 | 8.5–12s | V7 | 记录 | ② 分镜 / 人物卡 | 人物卡依据写「先收钱再领路」，分镜只指路不领路 | 便宜：二选一，统一人物卡或分镜；只指不领也说得通，改卡更省 |

### I133 记录 · 角色立场·Vibia · V4 视线（第一眼看什么）
- 对 75 年的庞贝主妇，成年女人散着长发、露着胳膊上街和裤子一样扎眼（同场 st4 的女孩就盯着她的长发）；spec 只写脸→腿；story.md 第 53 行原写「裤子和靴子」，spec 只剩腿
  | s2_st5 | 3.2–4.2 | V4 视线（第一眼看什么） | 记录 | ① 故事 | 对 75 年的庞贝主妇，成年女人散着长发、露着胳膊上街和裤子一样扎眼（同场 st4 的女孩就盯着她的长发）；spec 只写脸→腿；story.md 第 53 行原写「裤子和靴子」，spec 只剩腿 | 便宜（可选）：「先看脸，目光在散着的长发上停一下，再落到腿和靴子上」 |

### I134 记录 · 角色立场·Helvia · V1 语言
- 人物卡个性「热心、爱拿老话劝人」，st5 14 秒全程无声
  | s8_st5 | 0–14 | V1 语言 | 记录 | ① 故事 | 人物卡个性「热心、爱拿老话劝人」，st5 14 秒全程无声 | 便宜：5–10 秒倒油时加一声非词语的「嗯——」并朝她点头示意抹开；若要出词须由考据给短词（bible 第 14 行），存疑待考据 |

### I135 记录 · 角色立场·Helvia · V4/V6 视线·动机
- 「听到 rub oil all over yourself 时抬眼瞟她一下」——我听不懂英语
  | s8_st9 | 1.5–10.2 | V4/V6 视线·动机 | 记录 | ② 分镜文字 | 「听到 rub oil all over yourself 时抬眼瞟她一下」——我听不懂英语 | 便宜：改「看到她把油亮的小臂举向空处时，抬眼瞟她一下、顺着她的目光往她面前空处瞟一眼，再看回她憋着笑」（不看镜头） |

### I136 记录 · 角色立场·Helvia · V3 表情
- `st5_first_frame.png` 画右我第 0 秒已咧嘴笑，与「专心刮自己的胳膊」及 2.5 秒「嘴角一抽笑一下」冲突
  | s8_st5 | 0 | V3 表情 | 记录 | ③ 首帧 | `st5_first_frame.png` 画右我第 0 秒已咧嘴笑，与「专心刮自己的胳膊」及 2.5 秒「嘴角一抽笑一下」冲突 | 便宜：首帧改为专注平常脸、视线落在自己左臂，或 spec 写明 0–2.5 秒神情平静 |

### I137 记录 · 角色立场·Helvia · V3 表情
- 4.4–5.1 秒已「耸耸肩」，台词括注又写「笑着耸肩」，可能 5.1–9 秒再耸一次
  | s8_st6 | 4.4–9 | V3 表情 | 记录 | ② 分镜文字 | 4.4–5.1 秒已「耸耸肩」，台词括注又写「笑着耸肩」，可能 5.1–9 秒再耸一次 | 便宜：台词括注删「耸肩」，只留「带笑」；说话时手上只有 versas 一翻 |

### I138 记录 · 角色立场·路人与群众 · V3 表情
- 我是门房：天天坐门口收钱，一个外地女人站在我面前对空气小声嘀咕两句，我会好笑，但「摇头笑出了声」偏大；9.5–11 秒又「嘴角一撇」，从笑到撇嘴中间没有任何事发生
  | s8_st10 | 6.5–11 秒 | V3 表情 | 记录 | ② 分镜文字 | 我是门房：天天坐门口收钱，一个外地女人站在我面前对空气小声嘀咕两句，我会好笑，但「摇头笑出了声」偏大；9.5–11 秒又「嘴角一撇」，从笑到撇嘴中间没有任何事发生 | 便宜：6.5–8 秒改成「鼻子里哼一声笑、摇摇头」，右手往厅里一挥；9.5–11 秒改成「还带着笑摇摇头，转回去看门外」，去掉撇嘴 |

### I139 记录 · 角色立场·路人与群众 · V7 集内一致
- st6 两个干完活的男人「站在柜台外侧、东头拐角前的台沿边」吃（首帧也是站在柜台外）；中间隔 st4、st5，st7 变成「灶台那头的店里，远远坐着两个低头吃喝的男人」（首帧坐在灶后店里）。同样的粗布 tunica、同样两人，观众会读成同一对人瞬移进店坐下
  | s5_st6→s5_st7 | st6 0–8 秒 / st7 0 秒 | V7 集内一致 | 记录 | ② 分镜文字 | st6 两个干完活的男人「站在柜台外侧、东头拐角前的台沿边」吃（首帧也是站在柜台外）；中间隔 st4、st5，st7 变成「灶台那头的店里，远远坐着两个低头吃喝的男人」（首帧坐在灶后店里）。同样的粗布 tunica、同样两人，观众会读成同一对人瞬移进店坐下 | 便宜：st7 背景改成 st6 那两人仍站在柜台东头台沿边吃（虚化），或在 st7 写明是另外两人、换衣色 |

### I140 记录 · 角色立场·路人与群众 · V7 / 规则源
- bible.md 第 40 行「在两个以上镜头里出现、或要开口说话、或要和 Riley 有互动的人立人物卡」；浴场门房出现两镜并收钱互动、喊路店主开口说话，spec 却写「不立卡的配角」，于是没有 behavior.md 可锚住她们的分寸，下一集复现时无据可查
  | s8_st2 / s8_st10 / s5_st8 | — | V7 / 规则源 | 记录 | 规则源 | bible.md 第 40 行「在两个以上镜头里出现、或要开口说话、或要和 Riley 有互动的人立人物卡」；浴场门房出现两镜并收钱互动、喊路店主开口说话，spec 却写「不立卡的配角」，于是没有 behavior.md 可锚住她们的分寸，下一集复现时无据可查 | 便宜：给门房、喊路店主补最小人物卡（外观＋一两条行为：门房「话少、收钱利落、对怪人好笑不刁难」），或在 bible 写明「无名配角」例外 |

### I141 记录 · 角色立场·路人与群众 · V4 视线
- 我是扛柴的：迎面走来一个高个外地女人，右臂伸得笔直、对着手大声说话，我侧身挪柴给她让路——让路时一定先看她一眼（看她伸着的胳膊别碰着我的柴）。spec 只写让路，没写看
  | s4_st3 | 6.5–8 秒 | V4 视线 | 记录 | ② 分镜文字 | 我是扛柴的：迎面走来一个高个外地女人，右臂伸得笔直、对着手大声说话，我侧身挪柴给她让路——让路时一定先看她一眼（看她伸着的胳膊别碰着我的柴）。spec 只写让路，没写看 | 便宜：「侧身让路时斜眼看一下她伸着的右臂和她的脸，接着走」 |

### I142 记录 · 角色立场·路人与群众 · V4 视线 / V2 肢体
- 我是那位母亲：儿子拽我袖子、拿手指着一个陌生女人的脚，我会顺着看一眼，然后按下他的手（指着人不礼貌）拉他走；spec 写「眼睛看着前面的路」，对儿子的拽和指毫无察觉
  | s3_st8 | 4.5–6 秒 | V4 视线 / V2 肢体 | 记录 | ② 分镜文字 | 我是那位母亲：儿子拽我袖子、拿手指着一个陌生女人的脚，我会顺着看一眼，然后按下他的手（指着人不礼貌）拉他走；spec 写「眼睛看着前面的路」，对儿子的拽和指毫无察觉 | 便宜：「母亲顺着看一眼她的短靴，按下孩子指人的手，拉着他走」 |

### I143 记录 · 角色立场·路人与群众 · V4 视线
- 我是门房：外地女人当着我的面摊开一手心钱慢慢挑，我的眼睛会落在钱上（还会多看一眼那枚大黄铜币），spec 这两拍没写我看哪里，模型可能让我盯镜头或发呆
  | s8_st2 | 4–8 秒 | V4 视线 | 记录 | ② 分镜文字 | 我是门房：外地女人当着我的面摊开一手心钱慢慢挑，我的眼睛会落在钱上（还会多看一眼那枚大黄铜币），spec 这两拍没写我看哪里，模型可能让我盯镜头或发呆 | 便宜：4–6 秒补「门房低头看她手心里的钱」 |

