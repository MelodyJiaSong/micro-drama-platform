# k301 次级治疗术 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_43262.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/43262.jpg（Wowhead Classic 法术 2050 页的玩家截图，2007-08-31 上传，357×445） | 8045cd88759b | 旧版模型。暗夜精灵女牧师（白紫长袍）夜晚在暗夜精灵城镇（月光林地一带），双手合拢在胸前，掌间一大团暖金白光，四周散着金色十字星点——读条中的双手圣光（holy_precast_low_hand），看不到目标脚下的命中光。与 43264 是同一张图。 |
| `wowhead_81522.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/81522.jpg（Wowhead Classic 法术 2050 页的玩家截图，2008-05-14 上传，388×446） | da9b4918a1e6 | 旧版模型。巨魔女（蓝皮红发）站在橙红色地面上，双手张开举过肩，两掌各一团橙金光晕；身前身后从脚下竖起七八道细长橙金光束，最高到胸口，夹几颗金色星点——治疗命中时「光从脚下往上冒」的样子（lesserheal_base），落在施法者自己身上。 |
| `wowhead_81524.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/81524.jpg（Wowhead Classic 法术 2053 页的玩家截图，2008-05-14 上传，333×435） | f2538fca7225 | 与 81522 同一场景的后一帧：巨魔女双手仍举过肩、两掌橙金光晕，脚下竖起的橙金细光束更高，已越过腰到胸口以上，光束半透明、上端渐隐。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 1.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 1.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastholymagiclow.ogg` | https://wago.tools/api/casc/568915?download（客户端音效 `sound/spells/precastholymagiclow.ogg`，文件 ID 568915；2026-10-19 下载） | 9e8b758a4fd7 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_heal_low_base.ogg` | https://wago.tools/api/casc/569570?download（客户端音效 `sound/spells/heal_low_base.ogg`，文件 ID 569570；2026-10-19 下载） | 996125bd05c3 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
| `wowhead_81523.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/81523.jpg（Wowhead Classic 法术 2052 页的玩家截图，2008-05-14 上传，362×459） | 5759fcc408e6 | 与 81522 / 81524 同一场景的中间一帧：巨魔女（蓝皮红发）双手张开举过肩、两掌各一团橙金光晕，脚下竖起六七道细长橙金光束、已到胸口以上，夹几颗金色星点——lesserheal_base @脚下的命中光；原版老模型，橙红地面看不出地图 |
