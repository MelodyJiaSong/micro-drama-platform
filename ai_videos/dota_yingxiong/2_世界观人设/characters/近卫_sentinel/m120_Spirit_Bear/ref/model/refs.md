# m120 熊灵 · 原版模型参考（WC3 中立野怪「灰熊」`units\creeps\GrizzlyBear`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式（页面本身被 Cloudflare 拦，用 Wowpedia API 查到图片地址）。YouTube 只取封面与自动截帧（`hq1/hq2/hq3`），没下视频。
> **游戏里的红 / 蓝等纯色块常是队伍色**（随玩家变）：熊头顶那撮红毛、身上的蓝色斑块都是队伍色，不是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero67_skill-0.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/67/skill-0.gif（PlayDotA 德鲁伊页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/lone-druid） | da244456a1bb | DotA 1 技能图标「Summon Spirit Bear」＝WC3 灰熊图标：褐色熊头张嘴咆哮，**下颌一根白色长獠牙向上翘** |
| wowpedia_BTNGrizzlyBear.png | https://static.wikia.nocookie.net/wowpedia/images/9/98/BTNGrizzlyBear.png（页面 Bear (Warcraft III)） | 77b4064e7dd7 | WC3 经典图标，同上 |
| wowpedia_BTNGrizzlyBear-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/0/06/BTNGrizzlyBear-Reforged.png | 9aca90c51d49 | 重制版图标（看细节，不照搬）：土褐粗毛，**下颌一对向上的獠牙**，头顶一撮红毛（队伍色） |
| wowpedia_Bear.gif | https://static.wikia.nocookie.net/wowpedia/images/4/46/Bear.gif | 20ce2473589f | WC3 经典灰熊模型动图（17 帧）：土褐色，四足时肩背高耸、头低，人立拍击；爪长而发白 |
| wowpedia_Bear_frame.png | 由上一个 GIF 第 1 帧放大 3 倍转成 PNG（本地） | 66c73eaca91d | 同上，便于看图 |
| yt_It0GXYXIwTw_sddefault.jpg | https://i.ytimg.com/vi/It0GXYXIwTw/sddefault.jpg（「DotA Syllabear Beyond GODLIKE! Cuppycake (Titan Of Philippines)」https://www.youtube.com/watch?v=It0GXYXIwTw） | b3363f6a4015 | **DotA 1 熊灵最清楚的一张**（封面放大的模型）：德鲁伊身旁的熊灵，**通身灰紫 / 暗紫色毛**，背脊一道蓬乱尖毛，爪长而发白，佝偻巨大 |
| yt_It0GXYXIwTw_hq2.jpg | https://i.ytimg.com/vi/It0GXYXIwTw/hq2.jpg（同上） | d12e569be0d8 | 游戏界面选中「Spirit Bear」：头像是**紫色**的熊头，下颌獠牙 |
| yt_D5-oj-dFX2k_hq3.jpg | https://i.ytimg.com/vi/D5-oj-dFX2k/hq3.jpg（「DotA 6.81d - Lone Druid, Syllabear Beyond GODLIKE !」https://www.youtube.com/watch?v=D5-oj-dFX2k） | 40f00b0c0370 | 6.81d 界面选中「Spirit Bear」：头像是**淡紫蓝灰**色的熊，下颌獠牙 |
| yt_0SppJBz_xSw_maxresdefault.jpg | https://i.ytimg.com/vi/0SppJBz_xSw/maxresdefault.jpg（「Lone Druid beyond GODLIKE ! - Dota 1 Syllabear」https://www.youtube.com/watch?v=0SppJBz_xSw） | e66d14e39f5d | **v6.85k**（右上角版本号，比 6.83d 晚）：场上一头土褐色的熊、带蓝色队伍色斑块、头顶红毛，像未染色的 WC3 灰熊——和上面的紫色不同，可能是版本差异，也可能拍到的是德鲁伊的熊形态（对照，不作依据） |
| yt_frSI-opSK_0_maxresdefault.jpg | https://i.ytimg.com/vi/frSI-opSK_0/maxresdefault.jpg（「DOTA 1 Syllabear Lone Druid Beyond GODLIKE #19」https://www.youtube.com/watch?v=frSI-opSK_0） | a1509c67b760 | 版本不明（界面右上只显示 FPS）：选中单位头像是一头**白色**带獠牙的熊，血量 3500（对照，不作 6.83d 依据） |

## 结论（据图）

1. **体型**：粗壮佝偻的巨熊——肩背高耸、头低前压，背脊一道蓬乱尖毛；约为小兵的 2 倍。
2. **头**：宽头，**下颌一对短獠牙向上翘出嘴外**（WC3 灰熊图标、DotA 头像都有，第一识别点之一）。
3. **爪**：长而弯，偏白。
4. **毛色**：WC3 原模型是土褐色；**DotA 1 6.81d 的熊灵头像是淡紫蓝灰，另一局封面模型是灰紫**。6.85k 一局场上是土褐、另一局（版本不明）头像是白，版本之间有变化；6.83d 本身没截到，取最接近的 6.81d 灰紫，翻译成可信的暗灰紫毛色（world_rules §1.4）⚠️。
5. 头顶红毛、身上蓝斑是队伍色，不画。
6. 不半透明、不发光；身上没有鞍具饰物。

## 与当前立绘对比（2026-10-21）

旧图 `m120_Spirit_Bear_v1.png`（sha `34743b336e5a`，2026-10-18）：

- 真实质感巨熊、肩峰、无饰物、不发光：一致。
- **毛色：不一致**——旧图深灰褐、毛尖银灰（普通灰熊）；DotA 1 熊灵是灰紫。
- **獠牙：缺**——旧图嘴闭、没有下颌獠牙。
- 背脊尖毛、佝偻前压的姿态：偏弱（旧图是端正站立的普通灰熊）。

**差异等级：大**（主色错、獠牙缺，老玩家会认成普通熊，也分不清熊灵和熊形态）→ 改卡，新立绘待出（出图服务额度不足）。
