# c11 炼金术士 · 原版模型参考（WC3 中立英雄「地精炼金术士」`Units\Creeps\HeroGoblinAlchemist`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。
> **游戏里的红色是队伍色**：食人魔肩头的红甲片、地精胸前的红 V 形布随玩家变；脚下红光是光环特效。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero48_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/48/character.gif（PlayDotA 炼金术士页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/alchemist） | 7810426760b3 | **DotA 1 里的炼金术士本体**（120 px，18 帧）：**淡蓝色皮肤的食人魔**，头戴铜色头盔；**两只手各握一把直的宽刃短刀，刀尖朝下**；背上一座高高的木架，绿皮地精坐在木架上 |
| playdota_hero48_icon.jpg | 同上 `/hero/48/icon.jpg` | 2b99a1f8b0bc | DotA 1 头像：下方是食人魔——**铜色圆头盔、一道金框横缝护目**、下面露出淡蓝色的下半张脸；右上方是地精——绿皮、长尖鼻、**戴一副圆镜片护目镜** |
| wowpedia_BTNHeroAlchemist.png | https://static.wikia.nocookie.net/wowpedia/images/9/91/BTNHeroAlchemist.png（页面 https://wowpedia.fandom.com/wiki/Goblin_alchemist） | c0a8f5c228a5 | 经典图标，同 DotA 头像 |
| wowpedia_BTNHeroAlchemist-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/f/ff/BTNHeroAlchemist-Reforged.png | b0f8401d8513 | 重制版图标（看细节）：**蓝皮食人魔戴钢盔，金边 V 形护面，盔顶一根尖刺**，露出黄眼；后方地精黄绿皮、长尖鼻、尖耳、满口尖牙 |
| wowpedia_Alchemist.gif | https://static.wikia.nocookie.net/wowpedia/images/5/52/Alchemist.gif | 495ef7770ebb | 经典模型动图（15 帧）：同 PlayDotA——蓝皮食人魔、铜盔、双手两把宽刃短刀；背上木架高过头顶，木架里有一个浅色布包 / 罐子与几根木杆，地精坐在架顶 |
| wowpedia_Alchemist_official.gif | https://static.wikia.nocookie.net/wowpedia/images/2/2e/Alchemist_official.gif | b536019a7e83 | 魔兽 3 经典肖像（最清楚）：下方蓝皮食人魔、铜盔金框横缝护目、大下巴；上方绿皮地精坐在一座木板钉的架子上，**戴圆框眼镜**、长尖鼻、精瘦绿臂 |
| wowpedia_Goblinalch.JPG | https://static.wikia.nocookie.net/wowpedia/images/9/92/Goblinalch.JPG | 4f96bbe6c85a | 官方黑白原画（对照）：戴护目镜的地精伏案画图，背后是驮他的大块头 |
| yt_VvQl7AEBHK4_maxresdefault.jpg | https://i.ytimg.com/vi/VvQl7AEBHK4/maxresdefault.jpg（「Warcraft 3 Alchemist Quotes」https://www.youtube.com/watch?v=VvQl7AEBHK4） | 2aa900171da5 | 经典模型渲染：蓝皮食人魔弓步，两把短刀，背上木架与地精 |
| yt_PsK7NkERFHU_hq1.jpg | https://i.ytimg.com/vi/PsK7NkERFHU/hq1.jpg（「Razzil Darkbrew (Alchemist) + Fast Farm+Skill」） | c014488d5e3c | DotA 1 游戏界面：选中 Razzil Darkbrew，头像同上 |

## 结论（据图）

1. **食人魔是淡蓝色皮肤**（天蓝偏灰），不是灰褐。这是这对组合的主色。
2. **食人魔戴头盔**：一顶铜色（经典）/ 钢色（重制）圆头盔，正面一道金框横缝护目，盖住眼睛以上；只露出下半张脸和大下巴。重制版盔顶一根尖刺。旧卡「光头」错。
3. **食人魔拿刀**：两只手各握一把直的宽刃短刀（像大号切肉刀 / 拳刃），刀尖朝下。旧卡「两手空着」错。
4. **背架**：食人魔背上一座高高的木架（木板、木杆钉成，有布包与罐子），架顶高过食人魔的头，地精坐在架顶。
5. **地精**：绿皮、长尖鼻、尖耳、尖牙，**戴一副圆镜片护目镜 / 圆框眼镜在眼睛上**。旧卡的「额头推着黄铜护目镜」接近，改成戴在眼上的圆镜片。
6. 肩头红甲片、地精胸前红 V 是队伍色，照 m4 先例不进彩色，改成皮革本色。

## 与当前立绘对比（2026-10-21）

- 构成（地精骑在单头食人魔背上的木架里）、地精绿皮尖耳长鼻、满身药瓶：一致。
- **食人魔皮肤主色：不一致**——旧图灰褐，原版淡蓝。
- **食人魔头盔：缺**——旧图光头，原版铜盔金框横缝护目。
- **食人魔武器：缺**——旧图两手空着，原版双手各一把宽刃短刀。
- 背架：旧图是鞍座式矮木框，原版是高过头顶的木架（中）。
- **差异等级：大**（主色、头盔、武器三项识别层错）→ 改卡重出。
