# k311 复活术 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_2416.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/2416.jpg（Wowhead Classic 法术 2006 页的玩家截图，2006-12-07 上传，700×525） | e547583a5966 | 很早期的摆拍截图（2006 年 12 月上传，几人站成一圈）。竞技场式土台上一个白袍人类女躺在地上，从天到地贯穿整个画面的十几道金白竖光柱，地面一片金黄强光向四周放射——复活术生效时落在死者身上的通天光柱。施法者分不清是哪一个。 |
| `wowhead_8659.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/8659.jpg（Wowhead Classic 法术 2006 页的玩家截图，2006-12-15 上传，1149×748） | ad483987ce9c | 旧版模型。亡灵牧师（蓝色宽檐帽、黑白长袍）在沙地上半跪俯身，双手向前伸出、掌间一团暖金白光向外放射星芒，脚下地面一圈金白光芒四射；右边地上躺着一具紫衣尸体（被复活者）。这是 10 秒读条中：脚下光环＋双手高档光。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 10 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 10 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastholymagichigh.ogg` | https://wago.tools/api/casc/568440?download（客户端音效 `sound/spells/precastholymagichigh.ogg`，文件 ID 568440；2026-10-19 下载） | 7c5fc000c59a | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_holycast.ogg` | https://wago.tools/api/casc/569763?download（客户端音效 `sound/spells/cast/holycast.ogg`，文件 ID 569763；2026-10-19 下载） | af97f2196a88 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_resurrection.ogg` | https://wago.tools/api/casc/568667?download（客户端音效 `sound/spells/resurrection.ogg`，文件 ID 568667；2026-10-19 下载） | f78ecf1fb7d3 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
