# c28 巨魔战将 · 原版模型参考（WC3 中立野怪「森林巨魔猎手」`units\creeps\ForestTrollTrapper`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。`*_frame.png` 是本地从 GIF 抽帧放大的拼图，`compare_classic_crops.png` 是本地放大裁切拼图。
> **头上的红鬃不是队伍色**：Wowpedia 经典图标、经典动图、重制版图标都是红 / 橙红，DotA 头像是橙红。腕上、膝上的小块红色可能是队伍色。搜到的 `mvzKotFosqM` 封面是 Dota 2 原画，只收了它的游戏截帧。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero24_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/24/character.gif（PlayDotA 巨魔战将页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/troll-warlord） | f674656e7df1 | **DotA 1 里的本体**（120 px，14 帧，扔斧动作）：**鲜黄绿色皮肤**、深绿横纹的四肢细长，弓腰屈膝；**一大蓬红色乱鬃从头顶披到后背**；褐色皮甲背心与短皮裙；肩、前臂黑色带尖刺的护甲；两手各一把短柄手斧；大脚 |
| playdota_hero24_icon.gif | 同上 `/hero/24/icon.gif` | 54aac9a5789f | DotA 1 头像：黄绿色巨魔脸、长尖耳斜伸、黄眼、**橙红鬃发**；半边脸被深灰色的尖棱轮廓挡着（像铁面甲或阴影，分辨率不够确认） |
| wowpedia_BTNForestTrollTrapper.png | https://static.wikia.nocookie.net/wowpedia/images/8/88/BTNForestTrollTrapper.png（页面 https://wowpedia.fandom.com/wiki/Troll_Trapper） | 608a5208bec1 | 经典图标：绿脸、长尖耳、**大蓬红鬃**、长鼻 |
| wowpedia_BTNForestTrollTrapper-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/6/61/BTNForestTrollTrapper-Reforged.png | 6963a2261cde | 重制版图标（看细节）：绿皮带深色纹，长鼻、红眼、上弯骨色长獠牙、红紫鬃发 |
| wowpedia_Wc3r_forest_troll_trapper_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/7/78/Wc3r_forest_troll_trapper_portrait.png | 871db0ed0e99 | 重制版肖像：鲜绿皮、上弯长獠牙、长尖耳 |
| wowpedia_Foresttrolltrapper.gif | https://static.wikia.nocookie.net/wowpedia/images/c/c1/Foresttrolltrapper.gif | 3741772f46a1 | 经典模型动图（15 帧）：红鬃、黄绿皮、深色兽皮与甲 |
| wowpedia_Warcraft_III_creep_Forest_Troll_Trapper.jpg | https://static.wikia.nocookie.net/wowpedia/images/4/48/Warcraft_III_creep_Forest_Troll_Trapper.jpg | 52424d451dcd | 经典游戏截图：森林巨魔营地（远景） |
| wowpedia_Warcraft_III_creep_Forest_Troll.jpg | https://static.wikia.nocookie.net/wowpedia/images/a/a0/Warcraft_III_creep_Forest_Troll.jpg（页面 https://wowpedia.fandom.com/wiki/Troll_(Warcraft_III)） | 1f8f09c42d35 | 经典游戏截图：森林巨魔（同族），看肤色与体型 |
| yt_TUyOfMQ_U5o_hq2.jpg | https://i.ytimg.com/vi/TUyOfMQ_U5o/hq2.jpg（「DOTA 1 Troll Warlord Jah'rakal Beyond GODLIKE #11」https://www.youtube.com/watch?v=TUyOfMQ_U5o） | 5698cf780e77 | DotA 1 界面：名字 Jah'rakal，俯视远景 |
| yt_TUyOfMQ_U5o_maxresdefault.jpg | 同上 `maxresdefault.jpg` | efaedb54bdf6 | DotA 1 界面，同上 |
| yt_mvzKotFosqM_hq2.jpg | https://i.ytimg.com/vi/mvzKotFosqM/hq2.jpg（「Dota 1 Troll Warlord (Jah'rakal)! 1 vs 5 AI」https://www.youtube.com/watch?v=mvzKotFosqM） | 1db2db1c65f5 | DotA 1 6.74 界面，远景 |
| compare_classic_crops.png | 本地拼图 | 18e646d03f7e | 出图验收对照用 |

## 结论（据图）

1. **皮肤主色**：**鲜亮的黄绿色**，四肢上有深绿色横纹。不是灰绿 / 橄榄灰。
2. **头部**：**一大蓬红色（偏橙红）的乱鬃**从头顶一直披到后背，是远看最显眼的一块颜色；长尖耳向两侧斜伸；长鼻；一对上弯的骨色长獠牙。旧卡「剃光头只留一道细鬃」太少。
3. **体型**：弓腰屈膝、四肢细长、手大脚大，比小兵高一截（缩放 1.25）。
4. **衣甲**：褐色皮甲背心 / 兽皮、短皮裙；**肩头与前臂有黑色带尖刺的护甲**。
5. **武器**：双手各一把短柄手斧（远程时扔出）。
6. DotA 头像半边脸有深灰尖棱轮廓，可能是面甲也可能是阴影；模型动图里看不到面甲，不采用。

## 与当前立绘对比（2026-10-21）

- 一致：巨魔、长尖耳、上弯獠牙、高瘦驼背、短柄斧、兽皮裙、赤足。
- 不一致：① 皮肤灰橄榄色，原版鲜黄绿带深绿纹；② 头顶只有一道细窄的暗红鬃，原版一大蓬红鬃披到背；③ 没有黑色尖刺肩甲护臂；④ 躯干瘦到皮包骨，原版细长但有精干的肌肉。
- **差异等级：大**（皮肤主色、头部最显眼的红鬃两项不对，改卡重出）。
