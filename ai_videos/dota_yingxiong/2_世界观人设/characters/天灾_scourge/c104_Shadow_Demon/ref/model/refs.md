# c104 暗影恶魔 · 原版模型参考（WC3 恶魔族「艾瑞达术士」`units\demon\Warlock\Warlock`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> **队伍色提醒**：金色大肩甲上的嵌板颜色随玩家变（PlayDotA 图里红、YouTube 图里蓝），不是角色本色；腰下的品红布条与身后披风在红、蓝两方都是品红，是本色。

| 文件 | 来源 URL（含所在页面）| sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero132_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/132/character.gif（PlayDotA 英雄页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/shadow-demon） | 8117072ca327 | **DotA 1 本体动图**：**青灰绿（蓝绿）皮肤**、肌肉壮实的恶魔；全身**金色铠甲**——巨大的翼状金肩甲（嵌板红＝队伍色）、金臂甲、金护胫；头顶一排向上的鳍状尖冠；腰下品红破布条，身后一片品红破披风；没有长袍 |
| playdota_hero132_character_frame.png | 上图第 0 帧与中间帧放大 3 倍（本地） | ffeffca6d5e6 | 看图用 |
| playdota_hero132_icon.gif | 同上 `/hero/132/icon.gif` | 9d82a75ff329 | DotA 1 头像：紫色兜帽下一张暗脸、黄绿眼、红口（地图头像，与模型不是同一造型） |
| wowpedia_BTNArchimonde-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/d/d5/BTNArchimonde-Reforged.png（页面 https://wowpedia.fandom.com/wiki/Archimonde） | e6171d72469d | 阿克蒙德重制版图标（对照）：淡紫皮、绿眼、额上骨棱、尖耳——艾瑞达脸型参考，**不照搬肤色** |
| wowpedia_Eredar_Animated_Gif_W3.gif | https://static.wikia.nocookie.net/wowpedia/images/0/0e/Eredar_Animated_Gif_W3.gif（页面 https://wowpedia.fandom.com/wiki/Eredar_warlock） | f37543ec495f | WC3 艾瑞达动图（对照）：同样的金色翼状肩甲与金甲轮廓，但皮是红色、周身绿色邪火——可能是另一张贴图 / 另一兵种，**DotA 1 画面是青灰绿皮** |
| yt_jHtT1HQgi8w_maxresdefault.jpg | https://i.ytimg.com/vi/jHtT1HQgi8w/maxresdefault.jpg（「Dota 1 Shadow Demon Support Gameplay」https://www.youtube.com/watch?v=jHtT1HQgi8w） | 2463a103931b | **DotA 1 模型全身正面（最重要）**：青灰绿皮、宽肩厚胸、腹肌分明，胸前斜挂一条金链；头顶一排**向上张开的鳍状尖冠**，长尖耳向后上扬，下巴垂两根细长肉须，龇牙；**巨大的金色翼状肩甲**向两侧上方展开（嵌板蓝＝队伍色），背后还竖起一片金甲；金臂甲刻涡纹；金腰带垂下一块长金护裆板；下面是**品红破布条**；身后一片暗品红披风；**金护胫**包到脚背；没有角、没有长袍 |
| yt_7K2p2EikkzQ_maxresdefault.jpg | https://i.ytimg.com/vi/7K2p2EikkzQ/maxresdefault.jpg（「DOTA 1 Shadow Demon Eredar Beyond GODLIKE #5」） | 56903d9dfb0d | DotA 6.8x 界面头像（6.83 时代）：**青灰色**的脸，头顶鳍状尖冠、长尖耳、金耳环、下巴肉须 |
| yt_GILdHizmKUk_maxresdefault.jpg | https://i.ytimg.com/vi/GILdHizmKUk/maxresdefault.jpg（「Let's play DOTA Match: Eredar, Shadow Demon Gameplay part 1/3 v6.72f」） | 0f48c0cf24ad | **v6.72f 旧版**界面头像是品红紫皮、黄眼的艾瑞达脸——旧版本造型与 6.83 不同，**不作本卡依据**，只记差异 |
| compare_classic_crops.png | 本地拼图（DotA 1 模型全身 + 6.8x 界面肖像的放大裁切） | a3ae32c4d790 | 出图验收对照用 |

## 结论（据图）

1. **皮肤（主色）**：**青灰绿 / 蓝绿色**皮肤（6.83 时代）。旧卡「紫红皮」对应的是 v6.72f 的旧头像，不是 6.83 模型。
2. **头**：**没有角**。头顶是一排向上张开的鳍状尖冠（像一把骨质扇鳍），长尖耳向后上扬，金耳环，下巴垂两根细长肉须，龇牙。
3. **体型**：肌肉壮实的战士体型——宽肩、厚胸、腹肌分明，不是瘦高法师。
4. **服装（识别点）**：**不穿长袍**。上身赤裸、斜挂金链；全身**金色铠甲**——巨大的翼状金肩甲向两侧上方展开、背后一片竖起的金背甲、刻涡纹的金臂甲、金腰带与垂下的长金护裆板、金护胫。
5. **布**：腰下一圈**品红破布条**，身后一片暗品红破披风（本色）。
6. **脚**：金护胫包到脚背，游戏图里看不清是不是蹄 ⚠️。
7. 掌心常驻绿光：游戏模型里看不到（技能特效另算）。

## 与当前立绘对比（2026-10-21）

- 一致：恶魔、长尖耳、肉须、恶魔术士的阴冷气质。
- 不一致：① 皮肤**紫红**，原版**青灰绿**（主色错）；② 头上一对**大黑弯角**，原版**没有角**，是鳍状尖冠（头部最显眼特征错）；③ 穿**酒红长袍**，原版**赤裸上身 + 全身金甲 + 巨大翼状金肩甲**（服装轮廓与主色全错）；④ 体型瘦高，原版壮实；⑤ 品红破布条与披风缺失。
- **差异等级：大**（老玩家第一眼认不出是 DotA 1 的暗影恶魔）。
