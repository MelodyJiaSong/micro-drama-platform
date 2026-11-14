# c20 地精撕裂者 · 原版模型参考（WC3 中立「地精伐木机」，地图路径 `units\creeps\IronGolem`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面，没下视频。
> **队伍色提醒**：PlayDotA 动图与 Wowpedia 动图（红方）里肩头圆罩、膝盖、座位的大块红色随玩家颜色变，不是角色本色。`wowpedia_Goblin_Shredder.jpg` 是《魔兽世界》里的后期造型（紫铜色、橙红灯眼），只作对照，不照搬。
> 截图证实 d02 §20 的判断：地图路径名虽叫 IronGolem，模型就是 WC3 地精伐木机（与 Wowpedia 伐木机动图同一造型）。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero136_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/136/character.gif（PlayDotA 地精撕裂者页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/goblin-shredder） | d2b72617ccbb | **DotA 1 里的地精撕裂者本体**（120 px，10 帧）：一台矮壮宽厚的步行伐木机，**土黄 / 黄铜色的铆钉钢板**；顶上坐着绿皮地精；肩头圆罩带绿色灯；背后排气管冒灰烟；一侧手臂末端一面大圆锯片，另一侧是带刺的圆筒；短粗腿；红色块为队伍色 |
| playdota_hero136_character_frame.png | 本地：上图抽帧放大 | eebff09036d3 | 同上拼条 |
| playdota_hero136_icon.jpg | 同上 `/hero/136/icon.jpg` | 334e9aafc700 | DotA 1 头像（同 WC3 伐木机图标）：机甲正面「脸」——两只圆灯眼、獠牙状尖刺，顶上小地精 |
| wowpedia_BTNGoblinShredder.png | https://static.wikia.nocookie.net/wowpedia/images/2/2d/BTNGoblinShredder.png（页面 https://wowpedia.fandom.com/wiki/Goblin_Shredder_(Warcraft_III)） | cc0777b9ff9f | 经典图标，同上 |
| wowpedia_BTNGoblinShredder-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/2/26/BTNGoblinShredder-Reforged.png | 47acab1cd127 | 重制版图标（对照细节） |
| wowpedia_WC3shredder.gif | https://static.wikia.nocookie.net/wowpedia/images/4/4f/WC3shredder.gif | 11564daceea4 | **经典模型正面动图**（23 帧）：宽厚的躯干正面是一张「机械怪脸」——绿色圆灯眼、一排锯齿状的格栅大嘴；两肩圆罩上各一只绿灯、竖着尖刺；顶上地精驾驶座；两根排气管冒黑烟；右臂（画面左）大圆锯、左臂（画面右）带刺滚筒；短粗腿、大平脚 |
| wowpedia_WC3shredder_frame.png | 本地抽帧 | 1beaa20f534d | 同上拼条 |
| wowpedia_Goblin_Shredder.jpg | https://static.wikia.nocookie.net/wowpedia/images/d/d2/Goblin_Shredder.jpg（页面 https://wowpedia.fandom.com/wiki/Goblin_Shredder） | 556abe81a071 | 《魔兽世界》后期伐木机（对照，不照搬）：同样的「机械怪脸」（灯眼、獠牙格栅嘴、尖鼻）、顶上露出绿皮地精、两臂钩爪、短粗腿 |
| yt_px2uD-Vs30w_maxresdefault.jpg | https://i.ytimg.com/vi/px2uD-Vs30w/maxresdefault.jpg（「DotA v6.83c - Rizzrak Gameplay #28」https://www.youtube.com/watch?v=px2uD-Vs30w） | 0e5bc03454e4 | **DotA 1 模型大图（最清楚）**：土黄 / 黄铜色铆钉钢甲；正面怪脸：两只**绿色发光圆眼**、獠牙状弯刺、**锯齿格栅大嘴里透出橙色炉火**；两肩圆罩各一只绿灯、竖着弯角状尖刺；顶上红色座位里坐着绿皮小地精；顶后排气管喷火冒烟；**右臂一面大圆锯片**（白亮锯齿），**左臂一个箍满尖刺的圆滚筒**；粗短的腿 |
| yt_4aXFXhJ-gnM_maxresdefault.jpg | https://i.ytimg.com/vi/4aXFXhJ-gnM/maxresdefault.jpg（「Rizzrak (Goblin Shredder) Item Build」https://www.youtube.com/watch?v=4aXFXhJ-gnM） | f6ddf8a70fdb | 同一模型侧前方：矮壮宽厚轮廓、肩上尖刺、顶上地精、排气烟、锯片与尖刺滚筒 |

## 结论（据图）

1. **轮廓**：**矮壮宽厚**的两足伐木机——宽大的躯干、粗短的腿和大平脚，肩比身子还宽；不是瘦高的反关节长腿步行机。
2. **主色**：**土黄 / 黄铜色**的铆钉钢板（旧黄铜、做旧的卡其铁色），不是铁锈红（红色是队伍色）。
3. **正面怪脸（第一识别点）**：躯干正面像一张机械怪兽的脸——两只绿色发光圆灯眼、两侧獠牙状弯刺、一排锯齿状格栅大嘴，嘴里透出橙色炉火。
4. **驾驶者**：绿皮小地精**坐在机甲顶上**的座位里，不是坐在胸前驾驶座。
5. **两臂**：右臂一面大圆锯片；**左臂一个箍满尖刺的圆滚筒**（不是夹钳）。
6. **附加物**：两肩圆罩各一只绿灯、上面竖着弯角状尖刺；顶后排气管冒烟、喷火。

## 与当前立绘对比（2026-10-21）

当前立绘：`c20_Goblin_Shredder.png`（sha `62ee4f1c1968`，2026-10-18）。

- ❌ **轮廓**：瘦高锅炉 + 两条细长机械腿；原版是矮壮宽厚、短粗腿。
- ❌ **主色**：铁锈红；原版是土黄 / 黄铜色。
- ❌ **正面怪脸**：没有；原版躯干正面是绿灯眼、獠牙、锯齿格栅嘴。
- ❌ **驾驶位**：地精坐在胸前舱口里；原版坐在机甲顶上。
- ❌ **左臂**：夹钳；原版是尖刺滚筒。
- ✅ 右臂大圆锯片、绿皮地精驾驶、烟囱冒烟。

**差异等级：大**（轮廓、主色、正面怪脸三项识别层错）→ 改卡重出。
