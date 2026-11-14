# k324 神圣之火 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_44097.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/44097.jpg（Wowhead Classic 法术 14914 页的玩家截图，2007-08-31 上传，462×591） | 27d2373ef266 | 旧版模型。暗夜精灵女牧师（紫袍）在红土荒地伸手指向一只背长骨刺的四足兽，兽身上竖起一根极高的橙红火焰柱，从地面直冲画面顶端、扭成螺旋火带；兽身前横一道橙色水平光线，命中处金色光芒四射。印证「目标脚下火焰柱＋胸口金白爆」。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 3.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 3.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastfirelow.ogg` | https://wago.tools/api/casc/569045?download（客户端音效 `sound/spells/precastfirelow.ogg`，文件 ID 569045；2026-10-19 下载） | 84ed3ee83866 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_firecast.ogg` | https://wago.tools/api/casc/569764?download（客户端音效 `sound/spells/cast/firecast.ogg`，文件 ID 569764；2026-10-19 下载） | 193a6f29e62d | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_holyimpactdduber.ogg` | https://wago.tools/api/casc/569770?download（客户端音效 `sound/spells/directdamage/holyimpactdduber.ogg`，文件 ID 569770；2026-10-19 下载） | 8a45ed7ff817 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
