# c46 圣骑士 · 原版模型参考（WC3 兽人英雄「先知」`units\orc\HeroFarSeer`，缩放 1）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面，没下视频。
> **游戏里的红 / 蓝纯色块常是队伍色**（随玩家变）：狼背上的大块红布（PlayDotA 与 Wowpedia 动图都是红方录制）是队伍色，杖头的红光可能也随队伍色变；兜帽边缘的紫 / 青带在头像里随玩家变。白狼、褐色兜帽斗篷、绿皮是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero108_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/108/character.gif（PlayDotA 圣骑士页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/holy-knight） | e59a02f6037c | **DotA 1 里的陈本体**（120 px 动图）：绿皮兽人戴**褐色尖兜帽**、披褐色斗篷；肩上铁灰圆护肩；**骑一头白色巨狼**（背与腿带浅灰）；狼背红布（队伍色）上有圆形徽记，前缘两根向前弯翘的白色兽角；木框鞍；手举木法杖，杖头发红光 |
| playdota_hero108_icon.jpg | 同上 `/hero/108/icon.JPG` | 46eec72a46c8 | DotA 1 头像：绿皮兽人、**兜帽压到眉上**、黄眼、下巴前突；兜帽边缘彩色滚边（队伍色） |
| wowpedia_BTNHeroFarseer.png | https://static.wikia.nocookie.net/wowpedia/images/6/63/BTNHeroFarseer.png?format=original（页面 https://wowpedia.fandom.com/wiki/Far_Seer_(Warcraft_III)） | cd168e4e8c0f | WC3 先知图标，与 DotA 头像同一张 |
| wowpedia_BTNHeroFarseer-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/b/b5/BTNHeroFarseer-Reforged.png?format=original | b46151583c4c | 重制版图标：绿皮老兽人、紫色兜帽、**灰白浓眉**、下獠牙、鼻环（重制版重画，只看年龄与眉须） |
| wowpedia_Farseer2.gif | https://static.wikia.nocookie.net/wowpedia/images/4/4e/Farseer2.gif?format=original | 45ce56cda8ce | 经典版模型动图（较大）：**白色巨狼**、狼背红布（队伍色）与两根白兽角、木框鞍；骑者褐色兜帽斗篷、铁灰护肩；举杖施法 |
| yt_LZOhu9bCh_Q_maxresdefault.jpg | https://i.ytimg.com/vi/LZOhu9bCh_Q/maxresdefault.jpg（「DotA Gameplay Chen, Holy Knight」https://www.youtube.com/watch?v=LZOhu9bCh_Q） | 32c0b87a306e | 封面：DotA 1 头像 + 模型渲染（白狼、红马衣、绿皮骑者举杖） |
| yt_LL7RGR5illg_maxresdefault.jpg | https://i.ytimg.com/vi/LL7RGR5illg/maxresdefault.jpg（「DOTA 1 Chen Holy Knight Beyond GODLIKE」） | ea8e879c6ce0 | DotA 1 界面 3D 头像：绿皮兽人戴兜帽、下方白色（胡须 / 毛领），名字 Chen |
| compare_dota1_crops.png | 本地拼图（两份动图放大、封面裁切） | c920039cfdf1 | 出图验收对照用 |

## 结论（据图）

1. **骑者**：绿皮兽人（偏老，重制版灰白浓眉），**褐色尖兜帽戴在头上、压到眉上**，褐色斗篷披过肩背；肩上铁灰圆护肩。不是露头编辫。
2. **坐骑（识别层）**：**白色巨狼**，背与腿带浅灰。**不是灰狼**。
3. **狼具**：狼背一块大布（游戏里是队伍色，常见红）带圆形徽记，前缘两根向前弯翘的白色兽角；木框鞍。
4. **法杖**：木法杖，杖头发红光（可能随队伍色）。

## 与当前立绘对比（2026-10-21）

旧图 `c46_Holy_Knight_v1.png`（sha `a59d1a5be751`）：

- 绿皮獠牙兽人、骑巨狼、木法杖、皮革装：一致。
- 坐骑毛色：深灰巨狼 —— **不一致**（原版白狼）。
- 头部：露头、灰白长发编辫、额绳 —— **不一致**（原版褐色尖兜帽戴在头上）。
- 狼具：只有皮鞍 —— 不一致（原版红布马衣、两根白兽角）。
- 旧卡负向写了「白色狼」，正好挡掉原版坐骑颜色。

**差异等级：大**（坐骑毛色与头部最显眼的兜帽都错）→ 改卡并重出。
