# k317 治疗术 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_49187.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/49187.jpg（Wowhead Classic 法术 2054 页的玩家截图，2007-09-03 上传，451×737） | 831919a8dd70 | 旧版模型。巨魔男牧师（蓝皮白发、黄绿长袍）在暗处弓步，两手向两侧张开、各一团暖金光晕（手光），从身后往上冲出几道细金竖光束越过头顶，周围大颗金色十字星——治疗命中时光从下往上冒（施法者给自己加血）。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 3 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 3 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastholymagiclow.ogg` | https://wago.tools/api/casc/568915?download（客户端音效 `sound/spells/precastholymagiclow.ogg`，文件 ID 568915；2026-10-19 下载） | 9e8b758a4fd7 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_heal_low_base.ogg` | https://wago.tools/api/casc/569570?download（客户端音效 `sound/spells/heal_low_base.ogg`，文件 ID 569570；2026-10-19 下载） | 996125bd05c3 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
| `wowhead_49601.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/49601.jpg（Wowhead Classic 法术 2055 页的玩家截图，2007-09-03 上传，378×618） | 586d11340d0a | 暗处（像洞穴），巨魔男牧师（蓝皮白发、黄绿长袍）弓步，两手张开各一团暖金光晕，从身后往上冲出几道细金竖光束越过头顶，周围大颗金色十字星——与 49187 / 49603 同一场景；看到手光与上冲金光，脚下 heal_low_base 命中光被身体挡住看不清；原版老模型 |
| `wowhead_49602.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/49602.jpg（Wowhead Classic 法术 6063 页的玩家截图，2007-09-03 上传，447×740） | 8c84aae1f105 | 巨魔男两手暖金光晕，几道细金竖光束从身后冲过头顶，金色十字星；原版老模型 |
