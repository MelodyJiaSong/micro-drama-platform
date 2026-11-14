# k334 精神控制 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_44122.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/44122.jpg（Wowhead Classic 法术 605 页的玩家截图，2007-08-31 上传，339×498） | fdc8240e06e9 | 目标身上的效果：红皮獠牙兽人类 NPC（手拿镐，地狱火半岛，TBC 地图），头顶一团品红紫火苗，头后一道淡紫弧形光环——被精神控制的目标头部紫光。与 44124 同一张图。 |
| `wowhead_74123.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/74123.jpg（Wowhead Classic 法术 10912 页的玩家截图，2008-03-06 上传，1189×614） | 497325fb1261 | 旧版模型。沙地上一个红发人类女（皮甲、手持单手剑）头顶浮着一个紫色螺旋——两三道黑紫弧线绕着一团品红紫光球，里面几个白点；右边两个红鬃巨魔挥刀对着她；左上远处一个施法者头顶也挂着同样的紫色螺旋。印证施法者与被控者头顶都挂紫色螺旋。 |
| 动作参考 `ReadySpellOmni`（视觉链·读条，施法 引导 3 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4`（人类男）；另有 `ReadySpellOmni_whcHF_0.mp4`（人类女）、`ReadySpellOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 75293f387de3（HF 08d0dbe60116，DM 46d9f6ec0f75） | 全向读条，0.667 s 一循环：身体侧转，左手立在脸前、在下巴到鼻尖之间上下起伏约一掌高，手指微收微张、头轻点，右手垂在胯侧；读条多长就循环多少遍（人类女是左臂向侧下方伸出、掌心朝上缓缓起伏）。 |
| 动作参考 `ChannelCastDirected`（视觉链·出手＋引导，施法 引导 3 秒） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ChannelCastDirected_whcHM_0.mp4`（人类男）；另有 `ChannelCastDirected_whcHF_0.mp4`（人类女）、`ChannelCastDirected_whcDM_0.mp4`（矮人男）；不复制文件 | 23c74af7faf2（HF 11af2be2d0ea，DM d9eb59569a5d） | 数据里「释放」与「引导（目标）」两个事件挂的是同一个动画（原数据如此），引导期间保持这个姿势。指向引导，0.5 s 一循环但逐帧看不出位移：身体侧转，左臂平伸指向目标（肩高、掌心朝前、手指朝上），右臂垂体侧，引导多久保持多久。 |
| `sound_precastshadowmagiclow.ogg` | https://wago.tools/api/casc/569424?download（客户端音效 `sound/spells/precastshadowmagiclow.ogg`，文件 ID 569424；2026-10-19 下载） | b057d7f0fc70 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_curse.ogg` | https://wago.tools/api/casc/569079?download（客户端音效 `sound/spells/curse.ogg`，文件 ID 569079；2026-10-19 下载） | 16ea132c7fbb | 原版音效：持续时在施法者身上播放（客户端视觉链） |
