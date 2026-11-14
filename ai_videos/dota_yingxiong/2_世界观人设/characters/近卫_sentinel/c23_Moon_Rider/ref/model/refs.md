# c23 月之骑士 · 原版模型参考（WC3 暗夜精灵「女猎手」`units\nightelf\Huntress`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面，没下视频。`*_frame.png` 是本地从 GIF 抽帧放大的拼图，`compare_classic_crops.png` 是本地放大裁切拼图。
> **游戏里的红色 / 青色是队伍色**：那对很大的尖角肩甲、腰侧的圆片在 PlayDotA 动图里是红色、在 Wowpedia 动图里是青色，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero16_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/16/character.gif（PlayDotA 月之骑士页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/moon-rider） | 8025d1bef060 | **DotA 1 里的本体**（120 px，5 帧，红方）：黑豹前扑，嘴角两颗白长獠牙；骑手身后一缕**深绿长发**向后飘；一对很大的尖角肩甲向上翘（红色队伍色）；身体左侧竖挂一个**圆形月刃**（金边圆盘 + 外伸的弯刃） |
| playdota_hero16_icon.gif | 同上 `/hero/16/icon.gif` | fb7fecfb0a27 | DotA 1 头像：**紫银全包头盔**（盖住头顶、额头与两颊，盔面银色卷纹），长尖耳从盔侧穿出，紫皮，**深绿嘴唇**，盔后深绿长发 |
| wowpedia_BTNHuntress.png | https://static.wikia.nocookie.net/wowpedia/images/2/24/BTNHuntress.png（页面 https://wowpedia.fandom.com/wiki/Huntress_(Warcraft_III)） | fab1503b43d2 | 经典图标，与 DotA 头像相同 |
| wowpedia_BTNHuntress-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/e/e0/BTNHuntress-Reforged.png | 03578870337a | 重制版图标（看细节）：紫银头盔压到眉、护住两颊，绿色眉发，脸露出 |
| wowpedia_Wc3r_huntress_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/b/ba/Wc3r_huntress_portrait.png | a667d8fd4e96 | 重制版肖像：紫银盔、长尖耳、绿发 |
| wowpedia_Huntress_WC3.gif | https://static.wikia.nocookie.net/wowpedia/images/5/52/Huntress_%28WC3%29.gif | d8fbceca6533 | 经典模型动图（10 帧，青方）：黑豹、骑手绿发后飘、青色尖角大肩甲、左侧竖挂圆形月刃 |
| wowpedia_BTNUpgradeMoonGlaive.png | https://static.wikia.nocookie.net/wowpedia/images/e/e5/BTNUpgradeMoonGlaive.png（同页「月刃」升级图标） | c93b6e39020e | **月刃形制**：正中一个金边圆盘，周围三片向同一方向弯出的银白弯刃，像一个三刃飞轮 |
| wowpedia_BTNUpgradeMoonGlaive-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/2/2c/BTNUpgradeMoonGlaive-Reforged.png | 51729e4d68f0 | 同上的重制版：金边圆盘中间一个爪印，三片银白弯刃、刃根包金 |
| yt_hsxFSAzRo_8_maxresdefault.jpg | https://i.ytimg.com/vi/hsxFSAzRo_8/maxresdefault.jpg（「DOTA 1 Moon Rider Luna Moonfang Beyond GODLIKE #16」https://www.youtube.com/watch?v=hsxFSAzRo_8） | fa8415ec88bf | DotA 1 界面：名字 Luna Moonfang / Moon Rider，头像是紫银全包盔、尖耳、绿唇（与 BTN 同） |
| yt_mkpMrDR8bBM_maxresdefault.jpg | https://i.ytimg.com/vi/mkpMrDR8bBM/maxresdefault.jpg（「DOTA 1 Luna Moonfang Moon Rider Beyond GODLIKE #17」） | 0f2faed0c52e | DotA 1 界面，头像同上（另一侧角度） |
| compare_classic_crops.png | 本地拼图（动图放大裁切 + 头像 + 月刃图标） | 2c7f1e7964f5 | 出图验收对照用 |

同一频道 #18（`GbhhD4FvT0I`，标题注明 NEW SKINS）用的是换皮模型，没收。

## 结论（据图）

1. **坐骑**：黑色夜刃豹（黑豹），无斑点，**嘴角两颗白色长獠牙**露在外面。
2. **头盔**：紫银色**全包头盔**，盖住头顶、额头和两颊，盔面有银色卷纹，盔沿压到眉下；眼、鼻、嘴露在外面；长尖耳从盔侧穿出。旧卡「护颊盔 + 盔顶弯冠」接近，但当前立绘画成了只遮额头的冠饰。
3. **头发**：**深绿色**长发从盔后垂下、向后飘。旧卡「深靛蓝」错。
4. **皮肤 / 唇**：紫皮；嘴唇深绿（头像）。
5. **肩甲**：一对很大的尖角肩甲向上翘（游戏里是队伍色），是远看最显眼的轮廓之一。
6. **武器（用户最在意的那类）**：**圆形月刃**——正中一个金边圆盘，周围三片向同一方向弯出的银白弯刃，像三刃飞轮；游戏里竖挂在身体左侧。旧卡写的「三刃围成一圈」方向对，但当前立绘画成了**长柄双月牙斧**，形制错。

## 与当前立绘对比（2026-10-21）

- 一致：紫皮尖耳女战士、骑黑豹、画幅 16:9。
- 不一致：① 武器画成长柄上的两片月牙（像斧 / 长戟），原版是正中圆盘 + 三片弯刃的圆形飞轮月刃；② 头盔只是额前一道尖冠、头顶和两颊露着，原版是包住头顶与两颊的全盔；③ 头发黑紫，原版深绿；④ 黑豹没有露獠牙；⑤ 肩甲小，原版一对大尖角肩甲。
- **差异等级：大**（武器形制错、头发主色错，改卡重出）。

## 2026-10-26 参考分级（follow-up 274，qc_review ref_image.version）
- 移到 `_non_anchor/`（不作硬参考）：`compare_classic_crops.png`（拼图里混有 Reforged 裁切）、`wowpedia_BTNHuntress-Reforged.png`、`wowpedia_BTNUpgradeMoonGlaive-Reforged.png`（Reforged 月刃只有两片刃，与经典三刃冲突）、`wowpedia_Wc3r_huntress_portrait.png`。
- 硬参考保留经典低模：`playdota_hero16_character*`、`playdota_hero16_icon*`、`wowpedia_BTNHuntress.png`、`wowpedia_BTNUpgradeMoonGlaive.png`。
