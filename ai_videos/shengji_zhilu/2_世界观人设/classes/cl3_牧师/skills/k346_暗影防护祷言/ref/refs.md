# k346 暗影防护祷言 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_7490.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/7490.jpg（Wowhead Classic 法术 27683 页的玩家截图，2006-12-13 上传，318×452） | ae9afbd63f67 | 旧版模型。紫发白皮施法者（同 7226 的人）一手握拳高举、拳上一团绿芯紫边光晕（暗影手光），另一手也一团暗光，胸前立着一个粉紫色细线的圆形符文环（环上带刻度尖刺），头上一团青绿光。 |
| `wowhead_73378.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/73378.jpg（Wowhead Classic 法术 27683 页的玩家截图，2008-02-29 上传，789×734） | 33cb6b9a85dd | 旧版模型。戴兜帽牧师（黑金长袍，纳格兰背景，TBC 地图）双手举到头两侧、两掌各一团黑芯、绿紫边的暗影手光，胸前立着一个粉白细线圆形符文环，四周放射许多紫粉细光线，空中几点黑色小烟团。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 本技能瞬发、没有读条时间，这段读条动作实际一般不出现，只播出手。全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastshadowmagiclow.ogg` | https://wago.tools/api/casc/569424?download（客户端音效 `sound/spells/precastshadowmagiclow.ogg`，文件 ID 569424；2026-10-19 下载） | b057d7f0fc70 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_holyprotection.ogg` | https://wago.tools/api/casc/568491?download（客户端音效 `sound/spells/holyprotection.ogg`，文件 ID 568491；2026-10-19 下载） | 49ff1b024122 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
