# c1 树精卫士 · 原版模型参考（WC3 暗夜精灵建筑「远古守护者」`buildings\nightelf\AncientProtector`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1`＝视频约 25% 处），没下视频。
> **游戏里的红色 / 青色是队伍色**：前臂上那几道红（PlayDotA，红方）或青绿（Wowpedia 动图）色带随玩家变，不是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero99_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/99/character.gif（PlayDotA 树精卫士页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/treant-protector） | 01aa3bf06303 | **DotA 1 里的树精卫士本体**（120 px，51 帧）：佝偻前弓，**整个躯干、肩背和大腿被一大蓬鲜绿的叶子盖住**，叶丛里露出浅褐树皮的脸和两点黄光眼；头顶几根短枝杈像鹿角一样翘起；两条浅褐树皮长臂垂到膝下，末端三四根又长又尖的木爪；小腿是褐色根桩，脚边一圈叶子；前臂红色带是队伍色 |
| playdota_hero99_icon.gif | 同上 `/hero/99/icon.gif` | f6744b25cbfe | DotA 1 头像：侧脸，树皮质长鼻 / 眉骨，**一只发黄光的圆眼**，脸下半部被鲜绿叶丛（像胡子）盖住 |
| wowpedia_BTNTreant.png | https://static.wikia.nocookie.net/wowpedia/images/b/bd/BTNTreant.png（页面 https://wowpedia.fandom.com/wiki/Ancient_Protector_(Warcraft_III)，远古守护者的按钮图标就是这张） | 9d089c7ca130 | 经典图标，同 DotA 头像 |
| wowpedia_BTNTreant-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/d/df/BTNTreant-Reforged.png | 6a78880eb6b6 | 重制版图标（看细节）：浅褐纵纹树皮脸、深眼窝里**两只发黄光的眼**、长树皮鼻，脸下半与两颊全被一丛丛绿叶包着 |
| wowpedia_Ancientprotector.gif | https://static.wikia.nocookie.net/wowpedia/images/2/22/Ancientprotector.gif | 47941ec1073b | 经典模型静帧（最清楚）：**绿叶占全身面积一大半**，从头顶一直披到大腿；树皮脸在胸口高度，一只黄光眼；头顶短枝杈；两条树皮臂很长、垂到膝下，爪是三根尖长木指；腿短粗、被叶子盖着，只露根桩脚；臂上青色带＝队伍色 |
| yt_1dTbGv6GGWg_hq1.jpg | https://i.ytimg.com/vi/1dTbGv6GGWg/hq1.jpg（「DOTA 1 Rooftrellen Treant Protector SUPER HARD GAME」https://www.youtube.com/watch?v=1dTbGv6GGWg） | 7ab380aafe3d | DotA 1 游戏界面：选中 Rooftrellen，下方头像即上面的树皮脸；俯视距离下读得出的是一团绿 |
| yt_4zzmuwxAzPQ_maxresdefault.jpg | https://i.ytimg.com/vi/4zzmuwxAzPQ/maxresdefault.jpg（「Rooftrellen (Treant Protector) Item Build」https://www.youtube.com/watch?v=4zzmuwxAzPQ） | ae06a9084c99 | DotA 1 时期载入图式的插画（对照）：同样是满身绿叶的树精，树皮脸 |

## 结论（据图）

1. **主色是鲜绿**：全身大半被一层浓密的绿叶（偏黄绿、鲜活，不是暗绿）盖住——头顶、肩背、胸腹、大腿都是叶子；树皮只露在脸、两条长臂和脚。旧卡「深褐灰老树皮为主、头顶一蓬暗绿带紫的树冠」与原版相反。
2. **脸**：浅褐、纵纹的树皮脸，长在胸口高度（没有脖子，头和躯干一体），粗眉骨、长树皮鼻；**一对黄色发光的眼**（图标与模型都亮黄），这是第一识别点。旧卡「眼窝不发光」错。
3. **头顶**：几根短而粗的枝杈从叶丛里翘出，像一对小鹿角。
4. **臂**：两条浅褐树皮长臂，粗而长，垂到膝下；手是三四根又长又尖、略弯的木爪。
5. **腿**：短粗，大半被叶子盖住，露出褐色根桩脚。
6. **体态**：重心低、驼背前弓，像一座会走的绿色灌木堆；比例宽而矮。
7. 臂上的红 / 青色带是队伍色，照 m4 先例不进画面，改成树皮本色。

## 与当前立绘对比（2026-10-21）

- 种族 / 体型：一致（会走的古树、佝偻、粗臂、根腿）。
- **主色：不一致**——旧图通体深褐灰老树皮，只在头肩有一蓬近乎黑的暗叶；原版是鲜绿叶子盖满全身、树皮只露脸臂脚。
- **眼：不一致**——旧图深眼窝不发光（旧卡负向里还写了「眼睛发光」）；原版一对黄光眼。
- 头顶：旧图是一大团树冠，原版是叶丛里翘出几根短枝杈。
- 手：旧图五六根枝指，原版三四根长尖木爪（小）。
- 腿：旧图是两截光秃的老树干，原版被叶子盖住只露根桩（中）。
- **差异等级：大**（主色与发光黄眼两项识别层错，老玩家看旧图会认成《指环王》的树人而不是 DotA 大树）→ 改卡重出。


## 2026-10-25 复核纠偏（follow-up 197）

用户否定的是 follow-up 066 当前图，不是仅 v1。重新逐帧看 PlayDotA 原版动图（0／12／25／38帧）、经典模型静图与头像；新增暴雪官方原文件 `blizzard_ancientprotector.gif`，SHA256 `47941ec1073b00383e0f8dca3963b681e26de2863a43a801ab54caba596ce1b9`，与已有 Wowpedia 镜像逐字节相同，**不是第二份独立模型证据**。

来源：[暴雪官方建筑页](https://classic.battle.net/war3/nightelf/buildings/ancientprotector.shtml)／[原图](https://classic.battle.net/war3/images/nightelf/buildings/ancientprotector.gif)，2026-10-25 免费下载。官方页证实建筑拔根后近战；英雄沿用该模型的证据仍是既有6.83d研究及PlayDotA原版动图，不从WC3建筑攻击方式推导英雄技能。

| 识别项 | 本次据图复核 | 当前图偏差／纠正 |
|---|---|---|
| 大体块 | 肩背前弓，脸与肩根一体，躯干紧凑，粗根腿；动画姿态影响比例 | 当前人形腰线、长大腿明显；改宽厚前弓树体与短粗根墩 |
| 面部 | 头像是侧向凸出的木鼻、圆黄眼与厚木眉；模型正面脸宽、嵌在叶冠下方 | 当前小人脸与细长下垂人鼻；改宽扁根瘤面甲和楔形木鼻 |
| 叶簇 | 密实绿叶呈簇、叶尖向外生长，覆盖肩背与下躯干 | 当前连续垂藤像雨衣；改独立硬挺枝叶簇，露出木质主结构 |
| 臂与掌 | 前臂是清楚的长木块大面，掌部有尖木根指 | 当前密集细根编织、镰刀指过大；改厚木板状前臂与简洁根掌 |
| 根足／枝杈 | 粗根墩、可见宽木脚；头顶粗短分叉枝 | 维持抓地体量，避免细长鹿角 |

前文「像灌木堆」「叶子一直披到大腿」「鹿角」「长鼻」过度抽象，不能单独作造型验收标准；鲜绿占比和黄眼正确不等于原型结构正确。此次先查整体比例及轮廓，再查面甲／木臂／根足，最后查叶色和材质。旧图检查只覆盖颜色、漏掉形体，是本次返工原因。

电影化选择：约4米高、肩宽约2.8米、叶片实体化及木纹细节均为本剧设计，非游戏精确测量；移除红／青队伍色延续既有约定。低清动图不能证明每根木指、叶种和背面结构，故不标成原典精确事实。Reforged／Dota 2 不作本轮经典造型依据。原版资料继续只供人眼研究，不上传生成服务。

### 本轮结果
三张候选均逐张看图。v3仍偏人形且覆绿不足；v4过度宽矮；v5修比例后作为当前候选，SHA `bd3f76599db96262aa66c2a88444c6f778765eef6ae213a16ea55b8d5620752c`，待用户审阅。三轮请求先记日志，只有本剧自制图上传为后续参考，原版图未上传。原版同机位精确几何匹配未验证。4张旧技能图已标待更新；无本剧分集目录，shot_pack 无适用集／镜头目标，未以全仓sync影响其他会话。


## 197版被用户否定（follow-up 207）
前一节的宽扁面甲、短粗楔鼻、肩宽及根腿比例属于代理对低清图的设计推导，不是原型事实；用户明确认为新图更偏，v3／v4／v5全部撤销候选选用状态。当前恢复066图仅作占位。重新取证优先原版轮廓及脸部木结构，禁止以旧生成图反推原版。直接上传原版参考仍待用户明确许可。


## 2026-10-25 重研：原版概念图（follow-up 211）

新取证（免费公开页面，wowpedia MediaWiki API 查到文件地址后从 static.wikia 取原格式；warcraft.wiki.gg 对脚本访问返回 Blocked，未用）：

| 文件 | 来源 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_WC3_concept_art_Ancient_protector_2000.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/64/Warcraft_3_concept_art_Ancient_protector.jpg（页面 Ancient protector，图上署「© 2000 Blizzard Entertainment」） | fbacdd63c824 | **WC3 原版设计稿，模型的设计源头，目前最清楚的形体证据**（侧前方，旁边矮人作比例）：见下 |
| wowpedia_Reforged_Ancient_protector_concept.jpg | https://static.wikia.nocookie.net/wowpedia/images/a/a6/Reforged_-_Ancient_protector_concept.jpg | 66ec086f1591 | Reforged 重绘草图（对照，非经典依据）：同一结构——长尖木鼻、苔须、断枝、队伍色带 |

据 2000 年概念图（与经典模型静帧、头像互证）：
1. **头不是人头**：肩前一团向前探出的苔丛隆包，脸在肩线高度、侧面看是**一截像断枝的长尖木鼻向前凸出**，一只圆形黄光眼嵌在厚木眉骨下，下巴垂下一大片苔蕨像长须。正面模型里这张脸嵌在胸口、叶冠下方（与图标一致）。
2. **体型高大、肩背隆起前耸，腿并不短**：露出的躯干和大腿是暖褐色深竖纹老树干；197 版「宽矮」「人形木脸」都偏离。
3. **苔蕨分块长**：头肩、胯部、前臂一团团；**膝下像苔藓绑腿一直包到脚背**（模型里是腿上的草叶裙）。
4. **背上和头顶许多断枝**，部分是锯平的年轮截面；树干上有粉白色木耳状菌；脚边草里开白色小花（模型的肩头、脚边也有白花）。
5. 臂：长粗木臂，模型前臂是宽扁木板、向腕部变宽，三根长尖木爪；巨大盘根脚。
6. 配色：饱满草绿 / 翠绿苔蕨 + 暖褐树干 + 黄光眼。

**上传许可**：用户 2026-10-25 在 follow-up 211 明确允许本次出图把原版概念图、模型静帧与两张头像上传给 Codex 作形体参考（上传用副本在 `upload/`，模型静帧与头像为 LANCZOS 放大；`ref1` 7e5d50d92b9a、`ref2` 9e5a2866f273、`ref3` 2c0903bdd82a、`ref4` 66db9ce43326）。许可只覆盖本角色这一轮立绘，不推广到其他角色或视频。
