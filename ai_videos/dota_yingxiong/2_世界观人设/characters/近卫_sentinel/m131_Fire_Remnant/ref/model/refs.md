# m131 火之余烬（火焰残影）· 原版模型参考（灰烬之灵本体模型 WC3 火焰熊猫 `Units\Creeps\FirePandarenBrewmaster` + 地图火焰特效）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧（`hq1/hq2/hq3`），没下视频。
> **游戏里的红 / 蓝等纯色块常是队伍色**（随玩家变）。残影本体没有单独的 WC3 模型，以 DotA 1 游戏内画面为主；本体外观另见 `c39_Ember_Spirit/ref/model/refs.md`。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| yt_oAbRiGyX63k_hq1.jpg | https://i.ytimg.com/vi/oAbRiGyX63k/hq1.jpg（「Xin ( Ember Spirit ) \| WTF Mode \| DOTA 1\| Atinad \| Rgc \| Iccup \| Wodota」https://www.youtube.com/watch?v=oAbRiGyX63k） | 0365b00020ee | **残影最清楚的一张**（DotA 1 地图 v7.00e6，左下角版本号）：两个一模一样的灰烬之灵——白灰熊猫、暗红长袍、手持刀——**各自站在地上一大圈橙黄色的火环里**，全身被火光照亮，**实体、不透明**；右边第三个是正沿着火线冲过来的本体 |
| yt_oAbRiGyX63k_hq2.jpg | https://i.ytimg.com/vi/oAbRiGyX63k/hq2.jpg（同上） | 4798603fe27c | 同一局：本体连续冲向残影引爆，一路金黄火线和一排红橙爆点 |
| yt_lemTD7NxOEc_maxresdefault.jpg | https://i.ytimg.com/vi/lemTD7NxOEc/maxresdefault.jpg（「Dota 6.73 Xin Fire Remnants」https://www.youtube.com/watch?v=lemTD7NxOEc） | ef6703cb5937 | 6.73（灰烬之灵刚加入）：放残影前选目标，本体白熊猫、暗红袍（对照本体外观） |
| yt_lemTD7NxOEc_hq3.jpg | https://i.ytimg.com/vi/lemTD7NxOEc/hq3.jpg（同上） | 963aa3c56ea4 | 同一视频：冲到残影处的瞬间，一团金黄火光炸开、身后拖金黄火线；残影本体看不清 |
| yt_yWEHLgm--rs_maxresdefault.jpg | https://i.ytimg.com/vi/yWEHLgm--rs/maxresdefault.jpg（「DOTA 1 \| Ember Spirit - Xin BEYOND GODLIKE \| Gameplay」https://www.youtube.com/watch?v=yWEHLgm--rs） | 48be0cfab6cf | v6.83s 界面：放大头像（白脸熊猫、绿眼、草编斗笠、暗红袍）；场上金黄火线连到目标 |
| playdota_hero137_skill-3.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/137/skill-3.jpg（PlayDotA 灰烬之灵页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/ember-spirit） | 85f4c423f1be | DotA 1 技能图标「Fire Remnant」：一张被火烧成橙红的熊猫脸、眼睛发亮（图标风格） |
| playdota_hero137_character.gif | 同上 `/hero/137/character.gif` | 150dac83de6b | DotA 1 灰烬之灵本体动图：白底炭灰熊猫、暗红长袍、金橙火焰形袍摆、双手宽刃直刀（残影就是这个模样） |
| playdota_hero137_character_frame.png | 由上一个 GIF 第 1 帧放大 3 倍转成 PNG（本地） | a7119ac9f0ae | 同上，便于看图 |
| wowpedia_Firepanda.gif | https://static.wikia.nocookie.net/wowpedia/images/9/99/Firepanda.gif?format=original（页面 Fire (Warcraft III)） | fb1ecf408a7a | WC3 火焰熊猫模型动图（本体对照，同 c39 refs） |

## 结论（据图）

1. **残影是本体的完整模样**：和灰烬之灵一模一样——白底炭灰熊猫、斗笠、暗红金扣长袍、火焰形袍摆、双刀；**实体、不透明**。不是只有火焰勾出轮廓的半透明火人。
2. **火**：每个残影脚下一大圈**橙黄火环**熊熊燃烧，火光把它从下往上照亮。
3. 引爆：本体沿一道金黄火线冲到残影处，炸出一团金黄 / 红橙火光。
4. 版本：最清楚的一张是 v7.00e6；6.73 与 6.83s 的画面里残影本体看不清，但没有看到「纯火焰人形」的画面 ⚠️。

## 与当前立绘对比（2026-10-21）

旧图 `m131_Fire_Remnant_v1.png`（sha `a2582a7dd8cb`，2026-10-18）：

- 熊猫形敦实轮廓、橙黄火、脚下焦痕：一致。
- **身体：不一致**——旧图是半透明的纯火焰熊身，没有毛色、衣服、斗笠、双刀；原版残影就是本体模样（实体），站在火环里。
- 旧卡负向把「实体毛发、衣物、五官清晰」都挡掉了，正好挡掉了原版的识别层。
- 旧图赤身无装备，老玩家认不出是火猫的残影（像一头火熊）。

**差异等级：大**（形态与服装武器全缺）→ 改卡（外观对齐已改过的 `c39` 卡），新立绘待出（出图服务额度不足）；出图时最好以 `c39` 新立绘为参考。
