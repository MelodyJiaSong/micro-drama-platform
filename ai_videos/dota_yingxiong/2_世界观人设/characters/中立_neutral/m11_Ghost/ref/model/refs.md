# m11 鬼魂 · 原版模型参考（WC3 中立野怪 Ghost，模型 `units\creeps\BansheeGhost`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。
> DotA 1 的鬼魂直接用 WC3 野怪模型 `BansheeGhost`（缩放 1.05、染蓝，d01 §5.2），所以 WC3 经典版就是本卡标准；重制版（Reforged）只作对照，**不照它的造型**。DotA 1 游戏内能看清鬼魂的近景截图没找到（对战视频封面里野怪只有几个像素）。
> **游戏里的红 / 蓝等纯色块常是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Bansheeghost.gif | https://static.wikia.nocookie.net/wowpedia/images/6/63/Bansheeghost.gif（页面 https://wowpedia.fandom.com/wiki/Ghost_(Warcraft_III)） | 1ccee31cd3d5 | **经典模型动图（120 px，20 帧）**：灰白偏青的半透明女鬼，一头乱发全部向上竖起飘散；没有腿，下身拖成几条向后飘的破布尾；身后一团紫色的光雾 |
| wowpedia_Warcraft_III_creep_Ghost.jpg | https://static.wikia.nocookie.net/wowpedia/images/3/34/Warcraft_III_creep_Ghost.jpg（同页） | 3dabbe44288f | **经典版游戏内截图（雪地，两只 Ghost Level 3）**：整体是冷蓝色半透明人形，长发向上飘，破碎长袍下摆拖地成雾尾，背后泛一点紫光；左下头像是蓝白脸 |
| wowpedia_Wc3r_ghost_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/f/f7/Wc3r_ghost_portrait.png（同页） | be874fb0b336 | 经典画面头像：灰蓝的女性脸，**眼睛是两点发白的光**，五官完整（不是骷髅），白发向上蓬起成一圈 |
| wowpedia_BTNGhost.png | https://static.wikia.nocookie.net/wowpedia/images/d/d5/BTNGhost.png（同页） | fb18e96e32ef | 经典图标：几乎全白的女鬼脸，发丝是蓝色线条，下缘一点品红 |
| wowpedia_BTNGhost-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/7/7d/BTNGhost-Reforged.png（同页） | 9fa4240d9cb4 | 重制版图标（对照）：苍白女性脸、白瞳无瞳孔、冰蓝长发向上飘 |
| wowpedia_Ghost_Reforged.jpg | https://static.wikia.nocookie.net/wowpedia/images/7/75/Ghost_Reforged.jpg（同页） | 524fe7a839df | 重制版模型正背面（对照，不照搬）：冰蓝皮肤的女鬼，头发向上后方飘起，破碎长裙拖成尾，长指尖爪 |
| wowpedia_BansheeWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/a/ae/BansheeWC3.gif（页面 https://wowpedia.fandom.com/wiki/Banshee_(Warcraft_III)） | 16fd8aa4f565 | 同骨架的亡灵女妖（Banshee）经典动图：深色长袍、紫雾、头发上竖——同一套「女鬼」造型 |
| wowpedia_BTNBanshee.png | https://static.wikia.nocookie.net/wowpedia/images/6/65/BTNBanshee.png（同页） | 81d336474d9b | Banshee 经典图标（对照）：灰青脸、张大嘴尖叫、发丝向后飘 |
| compare_classic_crops.png | 本地拼图（游戏内截图放大 + 动图逐帧放大） | 3fa51a0a2ce7 | 出图验收对照用 |

## 结论（据图）

1. **种族 / 体型**：半透明的女性亡魂，人形、瘦长，悬空飘浮，**没有脚**，下身是破碎长袍拖成的雾尾。
2. **主色**：冷蓝 / 灰青白（DotA 再染蓝），半透明；背后常带一团淡紫色光雾。
3. **头部**：一头长发全部向上竖起、飘散（第一识别点）；脸是完整的女性脸，眼睛是两点发白的光，不是骷髅、不是空洞眼窝。
4. **附加物**：无武器、无饰物。

## 与当前立绘对比（2026-10-21）

当前立绘 `m11_Ghost.png`（sha `112480ce33a9`，2026-10-18 出）：

- ✅ 冷蓝色半透明女性亡魂，悬空无脚，破碎长袍下摆成雾尾——种族、主色、轮廓对。
- ✅ 长发向上飘散。
- ⚠️ 脸：当前是凹陷眼窝、张嘴尖叫，偏骷髅感；原版是完整女性脸、白光眼（小细节，远看读不出）。
- ⚠️ 原版背后的淡紫光雾没有（小细节）。

**差异等级：小**（识别层种族、主色、轮廓、上飘长发都对；只有脸部细节与紫雾不同）→ 不重出，只在此记录。以后若重出，可在 prompt 里补「完整的女性脸、两点发白的眼光」「背后一团淡紫色的薄雾」。
