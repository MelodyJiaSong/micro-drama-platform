# k651 地狱火 · 原生资料

> 暴雪娱乐版权素材，只给人看、写 prompt 用，不上传生成服务、不进成片。

| 文件 | 来源 URL / 时间点 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| `wowhead_4415.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/4415.jpg（Wowhead Classic 法术 1122 页的玩家截图，2006-12-09 上传，320×291） | 8d0f5b5aff6e | 地狱火全身：几块分离的灰绿岩石拼成的人形巨人（头、躯干、肩、拳、腿都是独立石块，岩缝橙黄熔岩纹），关节缝隙冒黄绿邪能火，胸前交叉缠两道紫色锁链，头顶一撮黑紫毛。雪地，2006 上传，老模型。 |
| `wowhead_75373.jpg` | https://wow.zamimg.com/uploads/screenshots/normal/75373.jpg（Wowhead Classic 法术 1122 页的玩家截图，2008-03-14 上传，634×467） | 1e3a383dc336 | 与 k638_征服恶魔 页 `wowhead_75371.jpg` 同一张图（sha 相同）：有特效。一只地狱火（几块分离的灰绿岩石拼成的巨人，岩面橙黄熔岩纹，关节处冒黄绿邪能火）胸前交叉缠两道紫色锁链（被奴役的标记），旁边站着亡灵女术士。部落木栅栏营地，2008 上传，老模型。地狱火模型参考（带锁链）。 |
| `0_research/refs/职业技能/动作/ReadySpellOmni_whcHM_0.mp4` | 动作库（[README](0_research/refs/职业技能/动作/README.md)「`ReadySpellOmni`」行；wowhead Classic 模型查看器逐帧渲染，人类男 Classic Era SD 老模型；同目录另有人类女 `_whcHF_0.mp4`、矮人男 `_whcDM_0.mp4`） | 75293f387de3 | **动作·读条（施法者） = ReadySpellOmni**：左臂屈肘把手立在脸前，在下巴到鼻尖之间上下起伏约一掌高、手指微收微张，右手垂胯侧，0.667 s 一个来回。 |
| `0_research/refs/职业技能/动作/SpellCastOmni_whcHM_0.mp4` | 动作库（[README](0_research/refs/职业技能/动作/README.md)「`SpellCastOmni`」行；wowhead Classic 模型查看器逐帧渲染，人类男 Classic Era SD 老模型；同目录另有人类女 `_whcHF_0.mp4`、矮人男 `_whcDM_0.mp4`） | cda78117050d | **动作·释放（施法者） = SpellCastOmni**：1.0 s：侧身弓步，左臂几乎伸直举过头、掌心朝天五指张开（0.1–0.85 s 定住），右手垂胯侧，随后放下。 |
| `0_research/refs/职业技能/动作/Stun_whcHM_0.mp4` | 动作库（[README](0_research/refs/职业技能/动作/README.md)「`Stun`」行；wowhead Classic 模型查看器逐帧渲染，人类男 Classic Era SD 老模型） | c1d2e93fce8c | **动作·持续（施法者）、持续（目标） = Stun**：屈膝弓背、双臂松垂、低头，2.0 s 一周期缓慢摇晃，没有出手动作。地狱火落地时范围内目标被击晕；数据同时标在施法者与目标。 |
| — | 客户端视觉链（命中→落点） | — | **Stand**：是召唤出的地狱火模型自己的站立动画，不是施法者动作；动作库未做（见动作库 README「没做」）。 |
| `sound_precastshadowmagiclow.ogg` | https://wago.tools/api/casc/569424?download（客户端音效 `sound/spells/precastshadowmagiclow.ogg`，文件 ID 569424；2026-10-19 下载） | b057d7f0fc70 | 原版音效：读条时在施法者身上播放（客户端视觉链） |
| `sound_shadowcast.ogg` | https://wago.tools/api/casc/569766?download（客户端音效 `sound/spells/cast/shadowcast.ogg`，文件 ID 569766；2026-10-19 下载） | 4bf9fb41c789 | 原版音效：释放时在施法者身上播放（客户端视觉链） |
| `sound_deathcoiltarget.ogg` | https://wago.tools/api/casc/568670?download（客户端音效 `sound/spells/deathcoiltarget.ogg`，文件 ID 568670；2026-10-19 下载） | 932dd2c2d2d3 | 原版音效：命中时在施法者身上播放（客户端视觉链） |
| `sound_infernalimpactbase.ogg` | https://wago.tools/api/casc/569601?download（客户端音效 `sound/spells/infernalimpactbase.ogg`，文件 ID 569601；2026-10-19 下载） | dd079aefe66b | 原版音效：命中时在落点身上播放（客户端视觉链） |
