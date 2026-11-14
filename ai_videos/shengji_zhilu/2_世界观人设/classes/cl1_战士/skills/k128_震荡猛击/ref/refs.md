# k128 震荡猛击 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_52681.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/52681.jpg（Wowhead Classic 法术 12809 页的玩家截图，2007-09-09 上传，876×605） | 091985ff41ce | 背景是外域纳格兰（紫天、浮岛），属 2.x 时期老模型截图，非 1.12 原版场景；右侧牛头人战士举盾、右手斧刚从上方劈过（斧刃在头顶后方），左侧牛头人目标胸口炸出几道蓝白色的细刺状光线，头顶上方悬一个青色的旋转环线（stunswirl，像两三圈水平的青色弧线）。即震荡猛击命中 + 昏迷 |
| 动作库：`0_research/refs/职业技能/动作/ReadyAbility_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 ReadyAbility 行 | 31a5f0756d4d | ReadyAbility：震荡猛击读条段。读条循环 0.267 秒：单手战斗预备站姿，屈膝、剑横身前低位、盾在左，几乎不动（蓄势站定） |
| 动作库：`0_research/refs/职业技能/动作/Special2H_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 Special2H 行 | 79d0ef51cae6 | Special2H：震荡猛击释放。1.5 秒：深蹲蓄力、武器拖到身侧后下 → 0.3–0.85 秒跃起离地、双手把武器抡到头顶后方（腾空约 0.4 秒） → 0.85–1.0 秒连人带武器砸地、深蹲 → 起身回 Ready2H |
| 动作库：`0_research/refs/职业技能/动作/Special2H_TQKH5U-cI-A_48.mp4`（引用，不复制） | YouTube TQKH5U-cI-A 老模型人类男录屏 https://www.youtube.com/watch?v=TQKH5U-cI-A&t=48s 的截段 | 7018d9279de1 | Special2H：交叉验证：老模型同名动作 |
| 动作库：`0_research/refs/职业技能/动作/CombatCritical_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 CombatCritical 行 | 5e4baa757546 | CombatCritical：命中反应（目标）：0–0.15 秒上身猛后仰并扭转、屈膝下坐，持盾手甩到侧上方，0.15–0.5 秒侧拧、武器乱晃，幅度约为普通受击的两倍 |
| 动作库：`0_research/refs/职业技能/动作/Stun_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 Stun 行 | c1d2e93fce8c | Stun：昏迷 5 秒期间目标循环 Stun，头顶青色旋转环。昏迷期间（目标）2.0 秒循环：屈膝、上身前弓驼背、双臂松垂、低头，缓慢轻晃 |
| `sound_swingweaponspecialwarriora.ogg` | https://wago.tools/api/casc/569828?download（客户端音效 `sound/spells/warriorswings/swingweaponspecialwarriora.ogg`，文件 ID 569828；2026-10-19 下载） | a8c4a8b02d51 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_swingweaponspecialwarriorb.ogg` | https://wago.tools/api/casc/569830?download（客户端音效 `sound/spells/warriorswings/swingweaponspecialwarriorb.ogg`，文件 ID 569830；2026-10-19 下载） | 316369a68697 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_swingweaponspecialwarriorc.ogg` | https://wago.tools/api/casc/569827?download（客户端音效 `sound/spells/warriorswings/swingweaponspecialwarriorc.ogg`，文件 ID 569827；2026-10-19 下载） | 5ab0f4d9f9bb | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_swingweaponspecialwarriord.ogg` | https://wago.tools/api/casc/569829?download（客户端音效 `sound/spells/warriorswings/swingweaponspecialwarriord.ogg`，文件 ID 569829；2026-10-19 下载） | aa2891af6457 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_m1hswordhitmetalshieldcrit.ogg` | https://wago.tools/api/casc/567879?download（客户端音效 `sound/item/weapons/sword1h/m1hswordhitmetalshieldcrit.ogg`，文件 ID 567879；2026-10-19 下载） | 6b09dc1c31b6 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
