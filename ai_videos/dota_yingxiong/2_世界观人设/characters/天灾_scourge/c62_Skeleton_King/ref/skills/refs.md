# c62 骷髅王 · 技能原版截帧（供出片前后审稿的「原版还原」视角使用）

> follow-up 271：`tools/qc_pre.py original_refs` 只读本目录 `dota1_{技能号}_*`。只作人眼 / 审稿参考，不上传给生成服务。

| 文件 | 来源 | 说明 |
|---|---|---|
| dota1_k624_reincarnation_sequence.jpg | 复制自 `skills/k624_Reincarnation/ref/dota1_reincarnation_sequence.jpg`（YouTube `_PAqnGca7nU`，DotA 1 实机，版本号看不到） | 死后骨堆中立灰白十字墓碑约 3 s → 原地复活，脚下暗红 → 金橙光柱 |
| dota1_k624_tombstone_cross.png | 复制自同目录 `dota1_reincarnation_tombstone_cross.png` | 十字墓碑放大 |
| dota1_k624_revive_burst.jpg | 复制自同目录 `dota1_reincarnation_revive_burst.jpg` | 复活瞬间：脚下暗红炸开、金橙光柱 |
| dota1_k621_stun_swirl_wc3classic_from_k751.jpg | 复制自 `c75_Sand_King/skills/k751_Burrowstrike/ref/research_125/yt_jJDfZx-VUMI_wc3_impale_classic_460-462.3s_10fps.jpg`（魔兽 3 经典版画面，DotA 1 用同一代特效） | **不是冥火爆击本身**，只用来看眩晕标记 ThunderclapTarget 的样子：落地单位头顶一圈浅蓝白旋涡（7:41.5–41.7）；用户 follow-up 137 据此定本剧眩晕样子 |
| dota1_k621_hellfire_blast_cast_flight_impact_ExXCErH5VAY_3.07-3.57s.jpg | YouTube https://www.youtube.com/watch?v=ExXCErH5VAY （「Skeleton King - Hellfire Blast 1」，guides-dota.ru，7.5 s，魔兽 3 经典画面 DotA 1；右上版本号低清读作 v6.78c，不是 6.83d）片中 3.067–3.567 s，30 fps 逐帧，只裁骷髅王与目标 Lina 一块放大 2 倍；sha256 `f9596363db13` | 施法→飞行→命中全过程。确认是冥火爆击：骷髅王蓝量 3.10 s 由 286 扣到 146（扣 140），同一刻技能图标进冷却。**3.10 s** 火球在骷髅王手前出现：一团大红色光晕，中心白黄高光；**3.133 s** 已飞过约 2/3 路程，仍是红晕白芯的球，直径与骷髅王身体差不多大；**3.167 s** 撞上目标。从出手到命中约 0.07–0.1 s（2–3 帧），快到几乎看不见飞行。两点间距约骷髅王三个身宽，只有两帧，看不出弧线，看上去是直线。命中：目标身上炸开一团橙红火焰，带向后拖的火舌（3.17–3.30 s），随后四散橙红火星和淡粉白放射细线（3.33–3.57 s） |
| dota1_k621_projectile_closeup_ExXCErH5VAY_3.10-3.13s.jpg | 同上视频 3.100 s 与 3.133 s 两帧，局部放大 4 倍；sha256 `4ba43e13dcef` | 火球特写：外圈大片红色辉光，内芯白到淡黄，3.10 s 芯里带一点绿（可能是骷髅王手部颜色透出，不确定）；3.133 s 球后有一道细长暗绿色条（可能是导弹模型尾部，也可能是背景，不确定）。整体是**红 / 橙红火球，不是绿色** |
| dota1_k621_target_stun_swirl_burn_ExXCErH5VAY_3.5-5.8s.jpg | 同上视频 3.5–5.8 s，6 fps，只裁目标头部放大 3 倍；sha256 `6f3233851db3` | 命中后目标头顶：**浅蓝白色旋涡圈**（眩晕标记，与上行 k751 截帧同款），约 3.67–5.17 s 可见（前段被目标名牌遮住一部分）；目标原地不动，约 6.0 s 后开始走动。另有一缕**红色火焰**从目标头顶往上飘，最晚 4.33 s 起可见，持续到约 6.5 s，施法前目标头上没有；推测是冥火爆击眩晕后的持续伤害 / 减速效果，未经游戏内说明确认。目标脚下粉红圆圈和身上的火光施法前就有（Lina 自带），不是本技能 |

- k624 的减速「腿上挂暗红」是用户 follow-up 223 要求的创作加法，原版截帧里没有对应标记。
- 冥火爆击火球已有原版截帧（上面三行 `ExXCErH5VAY`，v6.78c，非 6.83d）：红色光晕白芯的火球，不是绿色。d05 记的 `LordofFlameMissile` 名称未从画面核对。另查过 `XaWmjd-gUQs`（6.83d 实战），镜头太远、团战太乱，看不清火球，没有取图。
