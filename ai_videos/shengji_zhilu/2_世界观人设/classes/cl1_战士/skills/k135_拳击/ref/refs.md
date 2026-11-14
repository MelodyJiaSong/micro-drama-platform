# k135 拳击 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_52667.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/52667.jpg（Wowhead Classic 法术 6552 页的玩家截图，2007-09-09 上传，464×829） | e0734a019e93 | 背景是外域纳格兰（紫天、浮岛），属 2.x 时期老模型截图，非 1.12 原版场景；牛头人战士深蹲马步，双臂高举过头，右手斧和左手盾一起举在头顶（像要砸下或欢呼）；看不到目标，没有命中光。与 SpecialUnarmed（单手上勾拳）原典动作不一致，可能只是举武器的瞬间，单图看不出拳击。与 `wowhead_52668.jpg` 同一张 |
| 动作库：`0_research/refs/职业技能/动作/SpecialUnarmed_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 SpecialUnarmed 行 | 4c07d17acfcc | SpecialUnarmed：拳击释放（上勾拳，持武器时也是这个动作）。1.0 秒：下蹲拧身蓄力 → 0.35–0.55 秒跳起上勾拳，一条手臂笔直打向头顶上方、身体离地 → 落地回护架 |
| 动作库：`0_research/refs/职业技能/动作/SpecialUnarmed_TQKH5U-cI-A_132.mp4`（引用，不复制） | YouTube TQKH5U-cI-A 老模型人类男录屏 https://www.youtube.com/watch?v=TQKH5U-cI-A&t=132s 的截段 | a1b96f9f6ab5 | SpecialUnarmed：交叉验证：老模型同名动作 |
| 动作库：`0_research/refs/职业技能/动作/CombatCritical_whcHM_0.mp4`（引用，不复制） | wowhead Classic 模型查看器逐帧渲染（人类男，Classic Era SD 老模型，三联屏正面/四分之三/侧面，无特效无声）；说明见 `0_research/refs/职业技能/动作/README.md` 总表 CombatCritical 行 | 5e4baa757546 | CombatCritical：命中反应（目标）：0–0.15 秒上身猛后仰并扭转、屈膝下坐，持盾手甩到侧上方，0.15–0.5 秒侧拧、武器乱晃，幅度约为普通受击的两倍 |
| `sound_mwooshmediumcrit.ogg` | https://wago.tools/api/casc/567944?download（客户端音效 `sound/item/weapons/weaponswings/mwooshmediumcrit.ogg`，文件 ID 567944；2026-10-19 下载） | fafcea6abbc0 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_challengingshout.ogg` | https://wago.tools/api/casc/569236?download（客户端音效 `sound/spells/challengingshout.ogg`，文件 ID 569236；2026-10-19 下载） | df766bb62098 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
