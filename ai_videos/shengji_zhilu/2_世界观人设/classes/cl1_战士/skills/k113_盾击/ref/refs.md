# k113 盾击 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_52767.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/52767.jpg（Wowhead Classic 法术 72 页的玩家截图，2007-09-09 上传，671×615） | 46e5064b504f | 背景是外域纳格兰（紫天、浮岛），属 2.x 时期老模型截图，非 1.12 原版场景；右侧牛头人战士左臂把蓝面大盾猛推到头部高度、身子前压（ShieldBash 最高点），右手红刃斧下垂；左侧牛头人目标周身炸开一圈黄金色放射细线（像火花四溅），从胸口向外放射约一个身长。即盾击命中光。k138 盾牌猛击页的 `wowhead_52768.jpg`、`wowhead_53920.jpg` 与本图是同一张 |
| 动作库：`0_research/refs/职业技能/动作/ShieldBash_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 ShieldBash 行 | 3d64be0d4379 | ShieldBash：盾击释放。1.0 秒：盾收到胸前、剑向外后 → 0.2–0.35 秒左臂把盾向前上方猛推到头高、身体前压 → 盾保持外推后收回、剑同时上扬 |
| 动作库：`0_research/refs/职业技能/动作/CombatCritical_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 CombatCritical 行 | 5e4baa757546 | CombatCritical：命中时目标（数据里施法者也挂）做重击受击；胸口盾击命中光。命中反应（目标）：0–0.15 秒上身猛后仰并扭转、屈膝下坐，持盾手甩到侧上方，0.15–0.5 秒侧拧、武器乱晃，幅度约为普通受击的两倍 |
| `sound_m1hswordhitmetalshieldcrit.ogg` | https://wago.tools/api/casc/567879?download（客户端音效 `sound/item/weapons/sword1h/m1hswordhitmetalshieldcrit.ogg`，文件 ID 567879；2026-10-19 下载） | 6b09dc1c31b6 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
