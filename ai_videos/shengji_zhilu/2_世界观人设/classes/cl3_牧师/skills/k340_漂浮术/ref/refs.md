# k340 漂浮术 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_13856.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/13856.jpg（Wowhead Classic 法术 1706 页的玩家截图，2007-01-15 上传，449×645） | 64a93a38e364 | 旧版模型。红紫长袍施法者在暗夜精灵木屋前，整个人罩着一层淡紫蓝半透明光晕，脚底一小团青绿淡光、脚略离地；头上方一个暗紫物件加绿光（头饰或别的效果）。 |
| `wowhead_22138.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/22138.jpg（Wowhead Classic 法术 1706 页的玩家截图，2007-04-19 上传，363×556） | 713dc547d433 | 旧版模型。绿发暗夜精灵女（金紫长袍）站在城市银行前的台阶上，看不到任何特效，也看不出是否离地——只是人物站姿。 |
| `wowhead_25184.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/25184.jpg（Wowhead Classic 法术 1706 页的玩家截图，2007-06-01 上传，460×497） | 6cd80c97e2bd | 旧版模型。黄袍施法者在紫色地面、机械路牌旁身体前倾，两手各一团紫光；看不出漂浮术的特效。 |
| `wowhead_64167.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/64167.jpg（Wowhead Classic 法术 1706 页的玩家截图，2007-11-24 上传，302×624） | e8a78c7e97e6 | 旧版模型。戴兜帽的绿黑长袍施法者站在绿色洞穴里，头顶一圈白色小光点，身后一根橙红竖光柱带红色圆点（别的东西）；看不出漂浮术的特效。 |
| `wowhead_66151.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/66151.jpg（Wowhead Classic 法术 1706 页的玩家截图，2007-12-15 上传，649×806） | 1d8f2fd5f683 | 旧版模型。暗夜精灵女牧师（绿黑长袍）在树冠上方的空中一手高举、手边一圈淡青圆形符文环，脚下一团白亮星芒光爆，身后拖着一条很长的淡紫色云雾螺旋一直通到天上，周围青白星点。紫色拖尾是不是漂浮术本身看不出来（可能是别的效果）。 |
| `wowhead_77809.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/77809.jpg（Wowhead Classic 法术 1706 页的玩家截图，2008-04-01 上传，544×421） | 5e76b722fe1f | 旧版模型。蓝皮巨魔男（蓝黑金长袍）悬停在青绿色水面上方约半个身高，身上没有明显光效——漂浮术的效果就是人离地 / 离水悬着。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 本技能瞬发、没有读条时间，这段读条动作实际一般不出现，只播出手。全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `SpellCastOmni`（视觉链·出手，施法 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4`（人类男）；另有 `SpellCastOmni_whcHF_0.mp4`（人类女）、`SpellCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | cda78117050d（HF 370a8cc52410，DM 203abb65aed8） | 全向出手，1.0 s 单次：身体侧转、左肩朝前屈膝，左手猛甩举过头顶、掌心朝天五指张开，右手垂胯侧，举手静止约 0.75 s 后放下。 |
| `sound_precastmagelow.ogg` | https://wago.tools/api/casc/568938?download（客户端音效 `sound/spells/precastmagelow.ogg`，文件 ID 568938；2026-10-19 下载） | 00dd8da88cc3 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_levitateimpact.ogg` | https://wago.tools/api/casc/569172?download（客户端音效 `sound/spells/levitateimpact.ogg`，文件 ID 569172；2026-10-19 下载） | 2245a6d0b23d | 原版音效：命中时在施法者身上播放（客户端视觉链） |
