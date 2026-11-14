# k306 渐隐术 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_3592.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3592.jpg（Wowhead Classic 法术 10942 页的玩家截图，2006-12-08 上传，263×387） | 0febf3acf6fa | 旧版模型。矮人（绿袍）背影站在草地上，整个人发暗、半透明，能透过身体看到后面的草，肩背上散着几颗白色小星点——渐隐生效后的半透明持续状态，没有亮光。 |
| `wowhead_44035.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/44035.jpg（Wowhead Classic 法术 586 页的玩家截图，2007-08-31 上传，246×355） | 4cb2d2486252 | 旧版模型。暗夜精灵女牧师（紫袍）在红土地上一手上举，胸口炸开一团白→粉紫强光、向四周放射紫色光芒，头顶几颗青白星点——渐隐生效瞬间胸口的白紫闪光。 |
| `wowhead_48079.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/48079.jpg（Wowhead Classic 法术 586 页的玩家截图，2007-09-02 上传，596×730） | 71858c14bd7c | 旧版模型。白袍施法者在暗夜精灵风格建筑里，双手交叉举过头顶、掌间一圈青蓝圆形光阵，胸口一大团白光爆开、向四个斜角射出粉紫光芒，周围散白紫小星点——渐隐生效瞬间。与 48084 同一张图。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 本技能瞬发、没有读条时间，这段读条动作实际一般不出现，只播出手。全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastmagelow.ogg` | https://wago.tools/api/casc/568938?download（客户端音效 `sound/spells/precastmagelow.ogg`，文件 ID 568938；2026-10-19 下载） | 00dd8da88cc3 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_stealth.ogg` | https://wago.tools/api/casc/569423?download（客户端音效 `sound/spells/stealth.ogg`，文件 ID 569423；2026-10-19 下载） | 15f43cf9a83e | 原版音效：命中时在施法者身上播放（客户端视觉链） |
