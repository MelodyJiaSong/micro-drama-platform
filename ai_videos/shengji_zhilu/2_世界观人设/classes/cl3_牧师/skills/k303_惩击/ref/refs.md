# k303 惩击 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_22035.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/22035.jpg（Wowhead Classic 法术 585 页的玩家截图，2007-04-17 上传，859×733） | 6f4cd7f3da08 | 旧版模型。前景是一只蓝身、橙红鳍刺的生物（大半个画面），一道粗大的金黄光痕从画面左上方斜劈下来打在它身上，光痕沿途散着金色十字星点；远处一个牧师双手亮暖金手光。印证「没有飞行物，金光从上方斜劈进目标」。 |
| `wowhead_44310.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/44310.jpg（Wowhead Classic 法术 585 页的玩家截图，2007-08-31 上传，280×230） | 67986794b131 | 旧版模型。暗夜精灵女牧师（紫袍）在红土荒地，持光的手伸向一只背长橙色骨刺的灰紫四足兽，兽背上方炸开一团黄白星芒爆光、四射细金线——惩击命中瞬间（holysmite_low_chest）。 |
| `wowhead_82774.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/82774.jpg（Wowhead Classic 法术 585 页的玩家截图，2008-05-28 上传，420×297） | 41c1edb203c5 | 旧版模型。暗夜精灵女（紫发）近景，一只手朝前伸出、掌心对镜头，掌前一团白里透粉金的圆形光晕，像持光手前送（SpellCastDirected）；看不到目标和命中光。 |
| 动作参考 `ReadySpellDirected`（视觉链·读条，施法 1.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellDirected_whcHM_0.mp4`（人类男）；另有 `ReadySpellDirected_whcHF_0.mp4`（人类女）、`ReadySpellDirected_whcDM_0.mp4`（矮人男）；不复制文件 | 4e411cb1586a（HF 049e3c628a61，DM 511cd62312d4） | 指向读条，0.533 s 一循环（最快的读条手抖）：双手收在肚脐到下胸前相对「捧球」，一起上下起伏 5–8 cm 并略往前送，手指一张一合。 |
| 动作参考 `SpellCastDirected`（视觉链·出手，施法 1.5 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastDirected_whcHM_0.mp4`（人类男）；另有 `SpellCastDirected_whcHF_0.mp4`（人类女）、`SpellCastDirected_whcDM_0.mp4`（矮人男）；不复制文件 | 4d3b5e4b7862（HF 3cfe21ed7f1e，DM d18eb33b2e97） | 指向出手，1.0 s 单次：左肩对准目标屈膝下沉，左臂向目标平直推掌（肩高、掌心朝前、手指朝上），右臂向后下方张开平衡，推出后保持再收回。 |
| `sound_precastholymagiclow.ogg` | https://wago.tools/api/casc/568915?download（客户端音效 `sound/spells/precastholymagiclow.ogg`，文件 ID 568915；2026-10-19 下载） | 9e8b758a4fd7 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_holycast.ogg` | https://wago.tools/api/casc/569763?download（客户端音效 `sound/spells/cast/holycast.ogg`，文件 ID 569763；2026-10-19 下载） | af97f2196a88 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_holybolt.ogg` | https://wago.tools/api/casc/569402?download（客户端音效 `sound/spells/holybolt.ogg`，文件 ID 569402；2026-10-19 下载） | a42ec72ac4b3 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
