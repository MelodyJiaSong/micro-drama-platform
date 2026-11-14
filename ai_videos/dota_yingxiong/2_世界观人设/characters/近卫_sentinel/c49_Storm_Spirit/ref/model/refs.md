# c49 风暴之灵 · 原版模型参考（WC3 熊猫酒仙「元素分离」召出的「风暴」熊猫 `Units\Creeps\StormPandarenBrewmaster`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。GIF 已转成同名 `*_frame.png`。
> **游戏里的红色细边是队伍色**（PlayDotA 动图是红方）：领口、前襟边缘的红线随玩家变，不是角色本色；袍子本身的蓝色在红方动图里也是蓝，是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero53_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/53/character.gif（PlayDotA 风暴之灵页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/storm-spirit） | df1291126f6f | **DotA 1 里的风暴之灵本体**（120 px，6 帧）：**不透明的熊猫人**——灰白毛脸、绿眼；头戴**宽檐尖顶斗笠**（深褐草编，顶尖一块蓝）；**深蓝色长袍**，前襟一排盘扣，袖口与下摆浅蓝宽边，领口一道红线（队伍色）；矮胖圆滚；手里拎着一个小物件 |
| playdota_hero53_character_frame.png | 上图 6 帧放大拼条（本地转换） | ee15a7903eea | 同上，看出拳动作与袍摆 |
| playdota_hero53_icon.jpg | 同上 `/hero/53/icon.jpg` | 074292ef6abc | DotA 1 头像：熊猫圆脸，灰白毛、黑鼻头、黑眼圈、绿眼；头上斗笠帽檐、蓝色帽顶；蓝袍领口 |
| wowpedia_BTNStormBrewMaster.png | https://static.wikia.nocookie.net/wowpedia/images/2/2c/BTNStormBrewMaster.png（页面 https://wowpedia.fandom.com/wiki/Storm_(Warcraft_III)） | f8fb435f2d75 | 经典图标：同上，灰白熊猫脸、绿眼、斗笠、蓝袍 |
| wowpedia_Stormpanda.gif | https://static.wikia.nocookie.net/wowpedia/images/3/39/Stormpanda.gif | 3b6b964f9eb4 | 经典模型旧版动图（19 帧，转成 `wowpedia_Stormpanda_frame.png` 4929a84cfd8a）：斗笠、深蓝长袍浅蓝镶边、盘扣，袍摆宽大 |
| wowpedia_BTNStormBrewMaster-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/6/69/BTNStormBrewMaster-Reforged.png | a65d9a072600 | 重制版图标（对照，不照搬）：真实感熊猫人脸，白 / 棕毛，蓝眼 |
| yt_wDgrwu7BiQE_maxresdefault.jpg | https://i.ytimg.com/vi/wDgrwu7BiQE/maxresdefault.jpg（「DotA Ultimate Storm Spirit Raijin EXTREME FULL VERSION」https://www.youtube.com/watch?v=wDgrwu7BiQE） | 9f50c732c001 | **模型近景，最清楚的一张**（右边那只是风暴，左边黑袍的是另一只元素熊猫）：宽檐斗笠深褐草编、帽顶一块蓝、檐边一圈浅色；**宝蓝色宽袖长袍**，袖口与下摆浅蓝宽边，袍摆下露出灰色裤脚；两只白毛拳头；身体完全不透明 |
| yt_1266a6QlBbE_hq2.jpg | https://i.ytimg.com/vi/1266a6QlBbE/hq2.jpg（「DOTA 1 - Storm Spirit RAMPAGE!!! \| Beyond GODLIKE GAMEPLAY 2018」） | ade9f7875b26 | DotA 6.83 界面「Raijin Thunderkeg」，游戏内俯视：蓝袍斗笠的小个子在团战里 |

## 结论（据图）

1. **不是元素体**：DotA 1 的风暴之灵是一只**普通不透明的熊猫人**，毛皮灰白、黑眼圈黑鼻头、绿眼；没有半透明、没有体内电弧。电只出现在技能里。
2. **斗笠（第一识别点）**：一顶**宽檐尖顶的草编斗笠**，深褐色，檐边一圈浅色草茎，顶尖一块蓝色。
3. **长袍（主色）**：**宝蓝 / 深蓝色宽袖长袍**，前襟一排盘扣，袖口与下摆是浅蓝宽边；腰间深色带子；袍下灰色裤脚。领口红线是队伍色，不用。
4. **体型**：矮胖圆滚、圆脸，熊猫人比例。
5. **手**：白毛拳头，出拳攻击；手里有时拎一个小物件，看不清（不作识别层）。

## 与当前立绘对比（2026-10-21）

- 熊形、圆胖、圆耳：一致。
- **身体材质：不一致**——旧图是半透明蓝色风暴云体加电弧，原版是不透明的灰白熊猫毛皮。
- **斗笠：缺**——旧图负向里还专门排除了「草帽」，原版斗笠正是第一识别点。
- **长袍：缺**——旧图只有一条腰带，原版是宝蓝色宽袖长袍（负向里排除了「长袍」）。
- 主色：旧图通体发光蓝，原版是灰白毛 + 宝蓝袍 + 深褐斗笠。
- **差异等级：大**（材质、斗笠、长袍三项识别层都错，老玩家认不出）→ 改卡，待出图。
