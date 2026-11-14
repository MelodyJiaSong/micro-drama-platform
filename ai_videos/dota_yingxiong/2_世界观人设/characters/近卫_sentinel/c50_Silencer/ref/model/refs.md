# c50 沉默术士 · 原版模型参考（WC3 血精灵单位「破法者」`units\human\BloodElfSpellThief`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面，没下视频。GIF 已转成同名 `*_frame.png`。
> **队伍色提醒**：破法者的**盔顶翎羽、大盾盾面、长袍前片**是队伍色——PlayDotA 动图（红方）里是红，重制版宣传图与 YouTube 蓝方截图里是蓝。不随队伍变的是**金色铠甲、深红长袍底色、深灰横纹下摆**。本卡把队伍色部位翻译成深红（血精灵的红金本色，也和底色统一）。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero96_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/96/character.gif（PlayDotA 沉默术士页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/silencer） | 1288fdd982d5 | **DotA 1 里的沉默术士本体**（120 px，14 帧，红方）：侧身站立；头顶几片高高竖起的红色翎羽冠；**金色翼形肩甲**；红金长袍及地，下摆深灰横纹；**身侧竖着一面和他差不多高的长盾**（盾面红、金边） |
| playdota_hero96_character_frame.png | 上图 6 帧放大拼条（本地转换） | 283ef660edcf | 同上 |
| playdota_hero96_icon.jpg | 同上 `/hero/96/icon.jpg` | 61cd44a77a12 | DotA 1 头像：**红色全盔**，额前一道金色眉饰，脸从盔的竖缝里露出来（眼、鼻、嘴）；白色眼睛；脸型瘦长 |
| wowpedia_BTNSpellBreaker.png | https://static.wikia.nocookie.net/wowpedia/images/d/dc/BTNSpellBreaker.png（页面 https://wowpedia.fandom.com/wiki/Spell_Breaker_(Warcraft_III)） | 2b3b39d1c2a2 | 经典图标，同 DotA 头像 |
| wowpedia_SpellbreakerWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/2/26/SpellbreakerWC3.gif | ba2d4ab19e6e | 经典模型动图（38 帧，转成 `wowpedia_SpellbreakerWC3_frame.png` 2c071092efca）：左臂一面**长盾**、盾顶边缘带金色尖饰；右手挥一柄**长柄宽刃**（刃比前臂长）；施法时举起武器、顶端发红光；长袍下摆深灰横纹 |
| wowpedia_Spell_breaker_w3.jpg | https://static.wikia.nocookie.net/wowpedia/images/9/94/Spell_breaker_w3.jpg | 36bc2504c65c | **经典模型渲染**（蓝底）：浅金色短发向后翘、红色盔帽；金色铠甲配绿色宝石点缀；**红色及地长袍**，金边、黑色涡纹；左臂**一面从肩到膝的长盾**（红面、金边、绿宝石）；右手平举**长柄武器**，前端一簇多片银色弯刃 |
| wowpedia_Spellbreaker.jpg | https://static.wikia.nocookie.net/wowpedia/images/e/e6/Spellbreaker.jpg | 38ec39be1e75 | 官方原画（Samwise 2002）：**盔顶两片高耸的红色翎羽**；金色翼形肩甲；红色长盾高过肩、盾顶边缘一排尖齿；**一柄很长的弯刃长刀，刃长超过他半个身高**；长袍下摆深灰横纹 |
| wowpedia_Spell_Breaker_reforged.png | https://static.wikia.nocookie.net/wowpedia/images/7/70/Spell_Breaker_reforged.png | 10ffeae7c2be | 重制版（对照）：同一设计，队伍色部位变蓝（翎羽、盾面、袍前片）；金翼肩甲、长盾、长弯刃；长袍底色深红、下摆黑金横纹 |
| wowpedia_BTNSpellBreaker-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/7/71/BTNSpellBreaker-Reforged.png | f250593528d2 | 重制版图标：金盔、红色翼形颊饰、绿眼、白皙瘦脸 |
| yt_6opHmTkbic0_maxresdefault.jpg | https://i.ytimg.com/vi/6opHmTkbic0/maxresdefault.jpg（「DOTA SILENCER KILLING EVERYONE!!! (+50 INT)」https://www.youtube.com/watch?v=6opHmTkbic0） | 3a048eae3356 | DotA 1 游戏内（蓝方）：金色肩甲与盔、蓝色是队伍色；身后一道掷出的长弯刃红光轨迹 |
| yt_tBb0-_hGjEs_maxresdefault.jpg | https://i.ytimg.com/vi/tBb0-_hGjEs/maxresdefault.jpg（「DotA 6.83d - Silencer, Nortrom Beyond GODLIKE ! #2 (RAMPAGE)」） | a448c252195a | DotA 6.83d 界面大头像：红盔竖缝露脸、金眉饰，名字 Nortrom |

## 结论（据图）

1. **种族**：白皙瘦长脸的精灵男性，浅金头发；尖长耳。
2. **头盔（第一识别点）**：一顶**全包头盔**，盔面正中一道竖缝露出眼、鼻、嘴，额前一道金色眉饰；**盔顶两片高高竖起的翎羽 / 鳍冠**（队伍色部位，本卡取深红）。不是普通开面盔。
3. **铠甲**：**金色**为主的华丽铠甲，**金色翼形肩甲**（羽翼状叠片）；**深红及地长袍**配金边，前片是队伍色；下摆深灰横纹（像层叠的甲裙）。
4. **盾**：左臂一面**长盾**，从肩到膝、几乎一人高，盾面深红、金边、盾顶一排尖饰。不是小圆盾。
5. **武器**：右手一柄**长柄宽弯刃**（刃比前臂长，整把接近他身高），掷出后旋转飞回。不是巴掌大的月牙飞刃。
6. 主色：金 + 深红 + 深灰。

## 与当前立绘对比（2026-10-21）

- 精灵、白皙、浅金发、红金配色：一致。
- **盾：不一致**——旧图一面小圆盾，原版一人高的长盾（侧面轮廓最显眼的部分）。
- **武器：不一致**——旧图手里一枚小月牙飞刃，原版是长柄宽弯刃。
- **头盔：不一致**——旧图是没有冠饰的红色开面盔，原版是金眉饰、竖缝露脸、顶上两片高翎羽的全盔。
- 铠甲主色：旧图暗红为主，原版金色铠甲为主、深红长袍为辅（中）；金色翼形肩甲缺。
- **差异等级：大**（盾、武器、头盔三项识别层都不对）→ 改卡，待出图。
