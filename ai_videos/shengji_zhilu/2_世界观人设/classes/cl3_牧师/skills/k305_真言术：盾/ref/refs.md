# k305 真言术：盾 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_3823.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3823.jpg（Wowhead Classic 法术 17 页的玩家截图，2006-12-09 上传，639×900） | 8d89b3a7526e | 旧版模型。暗夜精灵男牧师（蓝发、黑蓝长袍）一只手高举一根金色法杖，全身被一个暖金色竖椭圆光圈包住（光集中在环边，比人略高），胸前一团绿色星点（别的效果），四周金色星屑；室内石墙（铁炉堡风格）。与 3832 几乎同一帧。 |
| `wowhead_3832.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3832.jpg（Wowhead Classic 法术 10901 页的玩家截图，2006-12-09 上传，639×868） | de4441780c4c | 与 3823 几乎相同的一帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身，环边最亮，胸前绿色星点、四周金星屑。 |
| `wowhead_7226.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/7226.jpg（Wowhead Classic 法术 17 页的玩家截图，2006-12-13 上传，241×408） | c04a331cacb9 | 旧版模型。紫发白皮的施法者（白黑长袍）一只手握拳举过肩，头上一团青绿光（别的效果）；身体外隐约一个暗褐色竖椭圆环，在暗背景里几乎看不出——盾成形后常亮段的样子，很淡。 |
| `wowhead_44133.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/44133.jpg（Wowhead Classic 法术 17 页的玩家截图，2007-08-31 上传，297×418） | d15c460c77d2 | 旧版模型。暗夜精灵女牧师（紫袍）在红土地上侧身，一只手高举、掌心一点暖金光；全身外一个淡淡的暗金竖椭圆环，环边微亮，身体腰侧一点紫白光。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 本技能瞬发、没有读条时间，这段读条动作实际一般不出现，只播出手。全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastholymagiclow.ogg` | https://wago.tools/api/casc/568915?download（客户端音效 `sound/spells/precastholymagiclow.ogg`，文件 ID 568915；2026-10-19 下载） | 9e8b758a4fd7 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_divineshield.ogg` | https://wago.tools/api/casc/569738?download（客户端音效 `sound/spells/divineshield.ogg`，文件 ID 569738；2026-10-19 下载） | d254d55c36cd | 原版音效：持续时在施法者身上播放（客户端视觉链） |
| `wowhead_3824.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3824.jpg（Wowhead Classic 法术 592 页的玩家截图，2006-12-09 上传，639×887） | 79942fbc4dc6 | 铁炉堡石厅，暗夜精灵男牧师（蓝发、蓝黑金长袍）右手高举金色法杖，全身被一个暖金色竖椭圆光圈包住（环边最亮、比人略高），胸前一团绿色星点（别的效果），四周金色星屑——真言术：盾持续态（holydivineshield_state_base），给自己上盾；与 3823 / 3832 同一组；原版老模型 |
| `wowhead_3825.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3825.jpg（Wowhead Classic 法术 600 页的玩家截图，2006-12-09 上传，639×868） | 5d12d69ff854 | 与 3824 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
| `wowhead_3826.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3826.jpg（Wowhead Classic 法术 3747 页的玩家截图，2006-12-09 上传，639×862） | 41cf543e88e6 | 与 3825 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
| `wowhead_3827.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3827.jpg（Wowhead Classic 法术 6065 页的玩家截图，2006-12-09 上传，639×868） | 166e3f0eaebb | 与 3826 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
| `wowhead_3829.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3829.jpg（Wowhead Classic 法术 10898 页的玩家截图，2006-12-09 上传，639×871） | 058ed315e498 | 与 3827 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
| `wowhead_3830.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3830.jpg（Wowhead Classic 法术 10899 页的玩家截图，2006-12-09 上传，639×865） | 2a6bb1f67b32 | 与 3829 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
| `wowhead_3831.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3831.jpg（Wowhead Classic 法术 10900 页的玩家截图，2006-12-09 上传，639×862） | 1a74fc6bcae5 | 与 3830 同一场景的相邻帧：暗夜精灵男高举金杖，暖金竖椭圆光圈罩住全身、环边最亮，胸前绿色星点、四周金星屑，几乎无变化；原版老模型（铁炉堡） |
