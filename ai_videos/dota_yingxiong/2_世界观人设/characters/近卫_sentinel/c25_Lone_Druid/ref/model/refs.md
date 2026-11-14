# c25 德鲁伊 · 原版模型参考（WC3 暗夜精灵「利爪德鲁伊」`units\nightelf\DruidoftheClaw`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1/2`），没下视频。`*_frame.png` 是本地从 GIF 抽帧放大的拼图，`compare_classic_crops.png` 是本地放大裁切拼图。
> **游戏里的红色 / 青色是队伍色**：双肩的大块垫肩、腰前一排圆珠在 PlayDotA 动图里是红色、在 Wowpedia 动图和 YouTube 截帧里是青色，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero67_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/67/character.gif（PlayDotA 德鲁伊页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/lone-druid） | 5e06477441d5 | **DotA 1 里的本体**（120 px，10 帧，红方）：极魁梧、肩背厚；头顶罩一张**褐色熊头**（能看到上颌一排牙）；两根细长的暗紫色角从头两侧斜伸；一大把**灰黑带白纹的长须 / 长发垂过胸口到腹部**；前臂与膝下是淡紫灰色护甲；腰下褐色兽皮；红色队伍色垫肩与腰前圆珠 |
| playdota_hero67_icon.gif | 同上 `/hero/67/icon.gif` | f995a0eace00 | DotA 1 头像：紫脸、浓眉、黄眼；**灰褐长发与长须**占满画面；头两侧露出两个白色角尖 |
| wowpedia_BTNDruidOfTheClaw.png | https://static.wikia.nocookie.net/wowpedia/images/9/91/BTNDruidOfTheClaw.png（页面 https://wowpedia.fandom.com/wiki/Druid_of_the_Claw_(Warcraft_III)） | 23c4afef246c | 经典图标，与 DotA 头像相同 |
| wowpedia_BTNDruidOfTheClaw-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/6/63/BTNDruidOfTheClaw-Reforged.png | 4e1bd0827905 | 重制版图标（看细节）：紫脸、青色脸纹、灰褐长须长发，额上长出深色兽角 |
| wowpedia_Wc3r_druid_of_the_claw_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/4/48/Wc3r_druid_of_the_claw_portrait.png | 8f78ee4750c1 | 重制版肖像：长尖耳、长须、头上细长兽角 |
| wowpedia_DCWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/e/e3/DCWC3.gif | 542d5bbe157f | 经典模型动图（28 帧，青方）：人形 → 变熊；人形的熊头兜帽、两根紫角、长须同上；熊形是**褐色巨熊**，背上仍有青色队伍色甲片 |
| wowpedia_BTNBearForm.png | https://static.wikia.nocookie.net/wowpedia/images/3/35/BTNBearForm.png | 5839b912c7dd | 熊形态技能图标（熊掌），只作对照 |
| yt_cTDom8aV56o_maxresdefault.jpg | https://i.ytimg.com/vi/cTDom8aV56o/maxresdefault.jpg（「Warcraft 3 Druid of the Claw Quotes」https://www.youtube.com/watch?v=cTDom8aV56o） | 80a7e03a6657 | **经典模型近景（最清楚的一张）**：正面魁梧，熊头兜帽，长须呈黑白条纹一直垂到腰；淡紫灰护臂护膝；褐色兽皮下摆；青色队伍色垫肩与腰珠；右下角是经典头像 |
| yt_cTDom8aV56o_hq1.jpg | 同上 `hq1.jpg` | 896ef2366fb1 | 同一模型另一帧，施法姿态 |
| yt_cTDom8aV56o_hq2.jpg | 同上 `hq2.jpg` | abcd932f8b35 | 正在变熊的一帧：熊头张口、褐毛 |
| yt_kw3jkBe_L2U_hq1.jpg | https://i.ytimg.com/vi/kw3jkBe_L2U/hq1.jpg（「DOTA 1 Syllabear Lone Druid Beyond GODLIKE #18」https://www.youtube.com/watch?v=kw3jkBe_L2U） | 6e5407cb608a | DotA 1 界面：名字 Syllabear，头像是同一张紫脸长须 |
| compare_classic_crops.png | 本地拼图 | 3a81cc5ea5fa | 出图验收对照用 |

## 结论（据图）

1. **体型**：极魁梧——肩背厚、胸宽、胳膊粗，站姿微微前压，比小兵高一截。旧卡「高大结实」不够，当前立绘偏瘦长。
2. **头部**：头顶罩一张**带毛的褐色熊头**当兜帽（熊的上颌和一排牙压在额顶），**不是**漂白的熊头骨；两根**细长、微弯的暗色兽角**从头两侧向后上方斜伸（不分叉，不是鹿角）。
3. **须发**：**灰褐长发与一大把灰黑长须**，长须一直垂过胸口到腹部（远看是胸前一道黑白条纹）。旧卡「短须、墨绿长发」错。
4. **皮肤 / 耳**：紫色皮肤、长尖耳，黄眼。
5. **衣甲**：双肩厚垫肩（游戏里是队伍色）；前臂与膝下是**淡紫灰色的硬护甲**；腰下褐色兽皮下摆；腰前一排圆珠（队伍色）。没有兵器，攻击靠投射物。
6. **熊形态**：同一个模型变成的**褐色巨熊**。

## 与当前立绘对比（2026-10-21）

- 一致：紫皮尖耳暗夜精灵男、熊主题装束、兽皮、赤足、无法杖。
- 不一致：① 头上是白色熊头骨，原版是带毛的褐色熊头兜帽；② 没有那两根细长兽角；③ 短须，原版是垂到腹部的长须（头像里最显眼的特征）；④ 墨绿头发，原版灰褐；⑤ 体型偏瘦长，原版极魁梧；⑥ 没有淡紫灰护臂护膝。
- **差异等级：大**（头部最显眼的长须、角与熊头形制都不对，改卡重出）。
