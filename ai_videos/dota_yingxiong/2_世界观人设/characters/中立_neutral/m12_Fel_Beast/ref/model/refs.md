# m12 魔能野兽 · 原版模型参考（WC3 中立野怪 Fel Beast，模型 `units\creeps\FelstalkerPurple`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。
> DotA 1 的魔能野兽直接用 WC3 野怪模型 `FelstalkerPurple`（缩放 0.8，d01 §5.2），WC3 里同名野怪 Fel Beast 就是这个紫色地狱犬；橙红色的 Fel Stalker 是同骨架另一个染色版，只作对照。DotA 1 游戏内能看清它的近景截图没找到。
> **游戏里的红 / 蓝等纯色块常是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Feldemon.gif | https://static.wikia.nocookie.net/wowpedia/images/0/0e/Feldemon.gif（页面 https://wowpedia.fandom.com/wiki/Fel_Beast_(Warcraft_III)） | 581e02f73f58 | **经典模型动图（Fel Beast 本体）**：紫色、低伏的四足兽；**脸是一块骨白色的兽颅骨甲**，下巴一丛灰白长须；**头顶向后伸出两根很长的淡褐骨色弯须**，像两根向后弯的长角；背脊一大丛**黑色尖刺**；全身是蓬乱的紫色粗毛 / 碎皮 |
| wowpedia_Warcraft_III_creep_Fel_Beast.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/11/Warcraft_III_creep_Fel_Beast.jpg（同页） | b61b3aa64b4d | **经典版游戏内截图（四只紫色 + 两只橙红）**：鲜紫色身体、前高后低、短粗腿与骨白爪；骨白颅面、颈下灰白须；两根长弯须从头顶甩到背后，比身体还长；背上黑刺 |
| wowpedia_Wc3r_fel_beast_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/c/c4/Wc3r_fel_beast_portrait.png（同页） | ba71f1954c89 | 经典画面头像：骨白色的颅骨面，大嘴一排尖牙，下面灰白毛，头顶后方深色刺 |
| wowpedia_BTNPurpleFelhound.png | https://static.wikia.nocookie.net/wowpedia/images/3/3e/BTNPurpleFelhound.png（同页） | 07ab85a11dd1 | 经典图标：骨白颅面 + 紫色身体 |
| wowpedia_BTNPurpleFelhound-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/a/ab/BTNPurpleFelhound-Reforged.png（同页） | 0f6aec397749 | 重制版图标（对照）：骨白头骨一样的脸壳，参差獠牙，下面褐色长毛 |
| wowpedia_FelStalkerWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/3/3a/FelStalkerWC3.gif（页面 https://wowpedia.fandom.com/wiki/Fel_Stalker_(Warcraft_III)） | db4bfe4e5804 | 同骨架的橙红版（Fel Stalker）动图（对照）：同样的骨白颅面、两根长弯须、背上黑刺 |
| wowpedia_Warcraft_III_creep_Fel_Stalker.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/61/Warcraft_III_creep_Fel_Stalker.jpg（同页） | fac0daf6c30d | 橙红版游戏内截图（对照） |
| compare_classic_crops.png | 本地拼图（游戏内截图放大 + 动图逐帧放大） | f021ebb4e47a | 出图验收对照用 |

## 结论（据图）

1. **种族 / 体型**：低伏、前高后低的四足恶魔兽，头低、短粗腿，体型像大型犬到小熊之间。
2. **主色**：紫色（模型本色，DotA 未另染）。全身是蓬乱的粗毛 / 碎皮，不是光皮。
3. **头 / 脸（第一识别点）**：脸和吻部是一块**骨白色的兽颅状骨甲**，大嘴一排尖牙；下巴与颈下垂一丛灰白长须。
4. **头顶附加物（第二识别点）**：**两根**很长的淡褐骨色弯须 / 角从头顶向后上方甩出，长过身体。
5. **背**：背脊一大丛**黑色尖刺**，不是肉触须。
6. **爪**：骨白色粗爪。

## 与当前立绘对比（2026-10-21）

当前立绘 `m12_Fel_Beast.png`（sha `ace4548f3df4`，2026-10-18 出，改名留档为 `m12_Fel_Beast_v1.png`）：

- ✅ 紫黑色四足恶魔犬，低头前倾，獠牙外露。
- ❌ 脸：紫色肉脸；原版是骨白色兽颅骨甲 + 灰白须——头部第一识别点缺失。
- ❌ 头顶：没有两根向后甩的长弯须。
- ❌ 背：一排七根紫色肉触须；原版是黑色尖刺丛 + 两根头须。旧卡「背脊 6–8 根肉触须」错。
- ❌ 质感：无毛光皮；原版是蓬乱粗毛 / 碎皮。旧卡负向「有毛的狗」把它排除了。

**差异等级：大**（头部骨甲、两根长须、背刺三项识别层都不对）→ 改卡，待出图（出图服务额度不足）。
