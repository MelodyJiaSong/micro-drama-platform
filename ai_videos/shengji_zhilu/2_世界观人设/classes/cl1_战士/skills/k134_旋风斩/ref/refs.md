# k134 旋风斩 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_52788.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/52788.jpg（Wowhead Classic 法术 1680 页的玩家截图，2007-09-09 上传，745×452） | 60ff40173a6e | 背景是外域纳格兰（紫天、浮岛），属 2.x 时期老模型截图，非 1.12 原版场景；右侧红甲牛头人战士压低身子、右手剑平伸向左（旋转中的一帧），脚下一团橙红火焰状光（whirlwind_state_base）；左侧牛头人目标胸口向四周放射出十几道橙红色长刺状光线（命中光，像炸开的针），长度超过一个身长 |
| `wowhead_74694.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/74694.jpg（Wowhead Classic 法术 1680 页的玩家截图，2008-03-10 上传，622×343） | beac841168eb | 夜间俯拍。黄红套装的牛头人手持长柄武器平扫，脚下地面一个很大的暗红色圆环（旋风斩地面光），周围三名目标（绿皮兽人、紫色巨魔等）胸口各炸出一簇橙红色放射长刺（命中光）；武器刃上带蓝白附魔光 |
| 动作库：`0_research/refs/职业技能/动作/Whirlwind_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 Whirlwind 行 | efd0054e47d3 | Whirlwind：旋风斩释放；脚下地面光。循环一圈 0.267 秒：屈膝半蹲，持武器右臂平伸到肩高、盾收胸前，原地高速旋转约 3.7 圈/秒，播若干圈后收回 |
| 动作库：`0_research/refs/职业技能/动作/CombatWound_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 CombatWound 行 | 7e6000305ec2 | CombatWound：命中反应（多目标）。命中反应（目标）：0–0.1 秒头后仰、胸口被顶起、双臂甩开，约 0.3 秒明显反应后收回 Ready |
| `sound_whirlwindshort.ogg` | https://wago.tools/api/casc/568519?download（客户端音效 `sound/spells/whirlwindshort.ogg`，文件 ID 568519；2026-10-19 下载） | d1ef08f63c71 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_decisivestrike.ogg` | https://wago.tools/api/casc/569098?download（客户端音效 `sound/spells/decisivestrike.ogg`，文件 ID 569098；2026-10-19 下载） | a817bc2f4c3b | 原版音效：命中时在施法者身上播放（客户端视觉链） |
