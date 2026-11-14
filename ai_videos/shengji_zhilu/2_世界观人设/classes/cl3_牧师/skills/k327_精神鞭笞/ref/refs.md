# k327 精神鞭笞 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_3577.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/3577.jpg（Wowhead Classic 法术 18807 页的玩家截图，2006-12-08 上传，514×208） | 332030938066 | 旧版模型。白胡子矮人牧师在雪地里一手向前平伸推掌（ChannelCastDirected 姿势），掌前一团青白强光，一道细长青蓝光束从掌心向画面右侧直射出去。光是青蓝色而不是紫黑色；目标不在画面里。 |
| 动作参考 `ChannelCastDirected`（视觉链·出手＋引导，施法 引导 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ChannelCastDirected_whcHM_0.mp4`（人类男）；另有 `ChannelCastDirected_whcHF_0.mp4`（人类女）、`ChannelCastDirected_whcDM_0.mp4`（矮人男）；不复制文件 | 23c74af7faf2（HF 11af2be2d0ea，DM d9eb59569a5d） | 数据里「释放」与「引导（目标）」两个事件挂的是同一个动画（原数据如此），引导期间保持这个姿势。指向引导，0.5 s 一循环但逐帧看不出位移：身体侧转，左臂平伸指向目标（肩高、掌心朝前、手指朝上），右臂垂体侧，引导多久保持多久。 |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_naturemissileloop.ogg` | https://wago.tools/api/casc/569780?download（客户端音效 `sound/spells/missile/naturemissileloop.ogg`，文件 ID 569780；2026-10-19 下载） | d83b44d4618d | 原版音效：持续时在施法者身上播放（客户端视觉链） |
| `sound_holymissileloop.ogg` | https://wago.tools/api/casc/569779?download（客户端音效 `sound/spells/missile/holymissileloop.ogg`，文件 ID 569779；2026-10-19 下载） | cad54d860a36 | 原版音效：引导时在目标身上播放（客户端视觉链） |
| `wowhead_41803.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/41803.jpg（Wowhead Classic 法术 17311 页的玩家截图，2007-08-30 上传，721×426） | 5cd5ac9824ef | 绿色洞穴（带刺藤蔓），紫黑长袍、背负红色长剑的施法者侧身向左伸手推掌（ChannelCastDirected），一道明亮的青蓝波浪光束从掌心射向左侧的藤蔓状怪物，掌前和目标端各一团青白强光——精神鞭笞引导；光是青蓝色而不是紫黑色，与 3577 一致（manafunnel_impact_chest）；原版老模型 |
