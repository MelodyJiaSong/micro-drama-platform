# k312 星辰碎片 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_70342.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/70342.jpg（Wowhead Classic 法术 10797 页的玩家截图，2008-01-29 上传，249×300） | d8a6c2e80469 | 目标身上的效果：青蓝皮独角食人魔，身体侧后方罩着一大片深蓝 / 蓝紫色半透明光幕，右上方一串青白小光点从天空往下落到它身上——星辰碎片引导中的星光坠落。施法者不在画面里。与 70348 同一张图。 |
| 动作参考 `ChannelCastOmni`（视觉链·出手＋引导，施法 引导 瞬发） | wowhead Classic 模型查看器逐帧渲染（Classic Era SD 老模型，纯色背景、无特效），动作分拍见 `0_research/refs/职业技能/动作/README.md`；引用 `0_research/refs/职业技能/动作/ChannelCastOmni_whcHM_0.mp4`（人类男）；另有 `ChannelCastOmni_whcHF_0.mp4`（人类女）、`ChannelCastOmni_whcDM_0.mp4`（矮人男）；不复制文件 | 58e62fd65f3d（HF d9f648e97ef2，DM 4716a9570ef7） | 数据里「释放」与「引导（目标）」两个事件挂的是同一个动画（原数据如此），引导期间保持这个姿势。全向引导，1.0 s 一循环但基本静止：身体侧转，左臂高举过头、肘微屈、掌心朝上 / 朝前，右手垂胯侧，引导多久举多久。 |
| `sound_starfireimpact.ogg` | https://wago.tools/api/casc/568008?download（客户端音效 `sound/spells/starfireimpact.ogg`，文件 ID 568008；2026-10-19 下载） | fdf140a302df | 原版音效：持续时在施法者身上播放（客户端视觉链） |
| `sound_precastmagelow.ogg` | https://wago.tools/api/casc/568938?download（客户端音效 `sound/spells/precastmagelow.ogg`，文件 ID 568938；2026-10-19 下载） | 00dd8da88cc3 | 原版音效：引导时在目标身上播放（客户端视觉链） |
