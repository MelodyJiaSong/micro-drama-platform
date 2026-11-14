# c52 地精修补匠 · 原版模型参考（WC3 中立英雄「地精修补匠」`Units\Creeps\HeroTinker`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式。GIF 已转成同名 `*_frame.png`。
> **队伍色提醒**：地精的**软帽、靴子**是队伍色——PlayDotA 动图与头像（红方）里是红，Wowpedia 游戏截图（蓝方）里帽子是蓝。黄铜机械架、钢胸甲、绿皮不随队伍变。
> WC3 原版修补匠的大招「工程升级 → 机器地精」会变成履带坦克形态（`GoblinTinker03.jpg`），**DotA 1 里没有这个形态**，只作对照。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero102_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/102/character.gif（PlayDotA 修补匠页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/tinker） | 011362f49bfe | **DotA 1 里的修补匠本体**（120 px，16 帧，红方）：小个绿皮地精**用自己的两条腿站着**；背上一副**黄铜色机械架**，两条多节机械臂从背后**拱过头顶**、末端是夹钳；放激光时一条臂前端变成炮口、喷出青白光，另一条臂上一排红点（火箭管）；背后冒灰烟；红帽红靴（队伍色） |
| playdota_hero102_character_frame.png | 上图 6 帧放大拼条（本地转换） | c1506efe9b95 | 同上 |
| playdota_hero102_icon.jpg | 同上 `/hero/102/icon.jpg` | a4689ea69e13 | DotA 1 头像：绿脸、**又长又尖的大鼻子**（像鸟喙）、小黄眼、尖耳；头戴软布帽（红＝队伍色）；**胸前一块带铆钉的银灰钢甲** |
| wowpedia_BTNHeroTinker.png | https://static.wikia.nocookie.net/wowpedia/images/e/e9/BTNHeroTinker.png（页面 https://wowpedia.fandom.com/wiki/Tinker_(Warcraft_III)） | 89535523dd92 | 经典图标，同 DotA 头像 |
| wowpedia_GoblinTinkerPortrait.JPG | https://static.wikia.nocookie.net/wowpedia/images/5/5b/GoblinTinkerPortrait.JPG | e2dc83ba3023 | 经典肖像：长鼻、软帽（红）、钢胸甲；肩后露出黄铜机械架 |
| wowpedia_TinkerOfficial.gif | https://static.wikia.nocookie.net/wowpedia/images/8/8a/TinkerOfficial.gif（转成 `wowpedia_TinkerOfficial_frame.png` 7a7ea9e38558） | 413c41491e25 | 官方肖像：同上，肩后黄铜机械臂根部 |
| wowpedia_Tinker.gif | https://static.wikia.nocookie.net/wowpedia/images/9/9e/Tinker.gif（转成 `wowpedia_Tinker_frame.png` 8dec24bacfd1） | ea98609d3fec | 经典模型旧版动图：**地精步行**，背上黄铜架子伸出两条长机械臂、在头顶上方张开夹钳；冒烟 |
| wowpedia_GoblinTinker02.jpg | https://static.wikia.nocookie.net/wowpedia/images/8/89/GoblinTinker02.jpg | 753c667b33c4 | WC3 游戏截图（蓝方）：俯视下是一个小地精背着一个圆筒形机身，两条黄铜机械臂高举过头，一条末端发青光 |
| wowpedia_GoblinTinker03.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/6f/GoblinTinker03.jpg | d4ffa4beafce | WC3 大招「机器地精」履带坦克形态（对照，**DotA 1 没有**） |
| wowpedia_Goblin_Tinker_Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/7/7d/Goblin_Tinker_Reforged.png | 2c6dad30d966 | 重制版（对照，不照搬）：同一结构更清楚——地精站在地上，背上背着机械架，两条巨大的多节机械臂从背后向两侧上方张开、末端是大夹钳 |
| wowpedia_BTNHeroTinker-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/5/56/BTNHeroTinker-Reforged.png | 4ae45b80ac62 | 重制版图标（对照）：长鼻、护目镜、烟斗 |

## 结论（据图）

1. **结构（第一识别点）**：不是坐在驾驶舱里的双腿机甲，而是**地精自己站着，背上背一副黄铜机械架**；架子上伸出**两条多节机械臂，从背后拱过头顶**，末端是夹钳。整体轮廓是「小地精 + 头顶上方两条大机械臂」。
2. **机械主色**：**黄铜 / 金黄色**，擦得发亮、带铆钉与关节；不是锈铁黑。
3. **武器**：一条机械臂前端可变成炮口，放出青白色激光；另一条臂上有一排短火箭管。背后冒灰烟。
4. **地精**：绿皮、**又长又尖的大鼻子**、小黄眼、尖耳；头戴软布帽（队伍色）；**胸前一块带铆钉的银灰钢胸甲**；脚穿靴（队伍色）。
5. 体量：地精本身矮小，机械臂举起后整体接近成年人高。

## 与当前立绘对比（2026-10-21）

- 绿皮地精、尖耳、机械臂、夹钳、冒烟：一致。
- **结构：不一致**——旧图是地精坐进一台双腿机甲的驾驶舱、腿是机械反关节腿；原版是地精自己两条腿站着、背着机械架。
- **机械臂位置：不一致**——旧图两臂在机身两侧下垂，原版从背后拱过头顶。
- **机械主色：不一致**——旧图锈黑铸铁，原版亮黄铜。
- 地精：旧图护目镜、皮围裙；原版软帽、钢胸甲、超长尖鼻（中）。
- **差异等级：大**（整体轮廓与机械主色都不对，老玩家第一眼认不出）→ 改卡，待出图。
