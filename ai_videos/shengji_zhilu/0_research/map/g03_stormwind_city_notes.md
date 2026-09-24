# G03 · 暴风城 —— 测绘备注（非树数据）

> 树数据在 `g03_stormwind_city.yaml`，**这里一个节点字段都不重复**（仓库规则「一份东西只有一个出处，副本必漂」）。
> 版本锚点：经典旧世 Vanilla / Classic Era（1.12）。

---

## ① 自查对账

### 开工前读的 sk2 既有成果（本片区的主底稿）

| 文件 | 用到了什么 |
|---|---|
| `ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`（1432 行，全文读完） | 八区关系、GM 世界坐标 14 锚点、10 条相邻关系的双向对账、版本错置清单 14 条、未查 8 条 |
| `.../parts/w2_architecture.md`（landmark.001–036 段） | 全部 `look_zh` 的画面素材（雕像尺度、藤蔓塔、钴蓝内厅、蓝灰石板屋顶、月亮井形制、水中石堡形制） |
| `.../parts/w7_deeprun_tram.md`（claim 清单全读） | 矿道地铁的形制、时刻、两端站、地下湖、Vanilla/非 Vanilla 分界 |
| `.../dossier.md`、`.../look_from_images.md`、`.../parts/w6_daily_blacklist.md`（grep 核对） | 「全城唯一旅店」的反证、阿隆索斯·法奥裁定、店名作为子区域名的清单 |

sk2 的 GM 坐标表是 T3（玩家整理的传送坐标），但与 T1 wiki 的方位文字 10/10 吻合，所以本树的方位陈述直接沿用；
**节点的 `coords` 字段一律填的是 wiki 的地图百分比坐标（0–100），不是 GM 世界坐标**——世界坐标只在 `note_zh` 里带括号出现，供建模用。

### 本次实际抓取并读到正文的页面（warcraft.wiki.gg，`action=raw` / `api.php`，共 62 个）

- **区级 9 个**：Stormwind City、Trade District、Old Town、Mage Quarter、Cathedral Square、Dwarven District、Park、Stormwind Keep、Valley of Heroes
- **运河与水中建筑 5 个**：Canals (Stormwind City)、Stormwind Stockade (Classic)、Stormwind Stockade、Vault (Stormwind City)、Cut-Throat Alley
- **导航与索引 3 个**：Template:Stormwind City（**「暴风城子区域」官方导航框，本次完整性的主依据**）、Stormwind City points of interest、Category:Stormwind City shops（分类成员 37 条）
- **商店 37 个**：用 `generator=categorymembers&prop=revisions` 一次取回全文，逐页读 patch 段判定版本
- **其余 24 个**：Cathedral of Light、Wizard's Sanctum、Deeprun Tram、Stormwind City Cemetery、Stormwind Lake、Stormwind Gate、Northern Elwynn Mountains、Old Barracks、Champions' Hall、Command Center、Training Hall、SI:7 (Stormwind City)、Pig and Whistle Tavern、Gilded Rose、Blue Recluse、Slaughtered Lamb、City Hall、Orphanage、The Argent Dawn (Stormwind)、Stormwind Counting House、Trader's Hall、Gryphon Roost、Petitioner's Chamber、Royal Library、Royal Gallery、Throne room、Garden (Stormwind Keep)、Trading Post、Head of Onyxia、Rallying Cry of the Dragonslayer

### 中文译名来源

- **灰机 wiki（`warcraft.huijiwiki.com`）本次可访问**（`200`）——**这推翻了 sk2 记录的「全站 403」**（sk2 未查第 4 条可部分结案）。
  取到 `模板:暴风城`（中文导航框，与英文导航框逐条对应）与 `分类:暴风城商店`（33 条中文店名）。
  注意 `wow.huijiwiki.com` 仍是 302 跳转，正确域名是 `warcraft.huijiwiki.com`。
- **`classic.wowhead.com` / `www.wowhead.com` 全线 403**（CloudFront `Request blocked`），curl 与 WebFetch 都不行，
  任务书建议的 `&xml` 绕法本次**无效**。所以等级/坐标没能从 wowhead 二次核，wiki 页面里带 `{{coords}}` 的才填了 `coords`。
- **`worldofwarcraft.blizzard.com` 未再尝试**，城门弩炮那条沿用 sk2 经 WebFetch 提取的正文（sk2 已标「未能二次逐字复核」）。

### 抓取过程中的技术坑（给后面的片区）

1. `warcraft.wiki.gg` 的 `action=raw` **没有自定义 User-Agent 会很快被限流**，返回
   `{"error":{"code":"ratelimited",...}}` 而不是 HTTP 错误码——**它会被 curl 当成 200 写进文件**，不检查内容就会静默拿到空数据。
   加 UA 后恢复正常；批量取页请用 `api.php` 的 `generator=categorymembers&prop=revisions&rvslots=main` 一次拿完，别逐页 curl。
2. Windows 的 Python 默认 `cp1252` stdout，打印中文会 `UnicodeEncodeError`，前面要加 `PYTHONIOENCODING=utf-8`。

---

## ② 版本差异（4.0.3a 及其他补丁改了什么 —— 逐条）

本节全部是「**现行版本有 / 旧世没有**」或反之，凡是 ❌ 的都不得进树、也不得入画。

### A. 整块区域级

| # | 项 | 引入/改动补丁 | 判定 | 证据 |
|---|---|---|---|---|
| 1 | **暴风城港口** Stormwind Harbor | 3.0.2 | ❌ | `Patch 3.0.2: Added.`（sk2 已裁定） |
| 2 | **暴风城郊外** Stormwind City Outskirts（大使馆 / 熔炉 / 奥莉维亚的水池 / 沃勒顿农场 / 东部大地神殿） | 4.0.3a 起 | ❌ | 原文即写「built as a replacement for the Stormwind Park, swallowed by Deathwing's assault」 |
| 3 | **雄狮之眠** Lion's Rest（瓦里安之墓 + 阵亡者纪念墙） | 7.0.3 | ❌ | Park 页 `Patch 7.0.3: Lion's Rest has been built on the site of the former Park.` |
| 4 | **旧兵营** The Old Barracks | 4.0.3a | ❌ | Old Barracks 页 `Patch 4.0.3a: Added.`——它是**花园区废墟**时期才显示的子区域名，旧世没有 |
| 5 | **艾尔文北部山脉** Northern Elwynn Mountains | 5.0.4 | ❌ | `Patch 5.0.4: Added.`；位置在港口以北 |
| 6 | **法师区上方的肯瑞托营地** The Overlook | 6.0.2 | ❌ | 通往「生态圆顶」的后方基地 |
| 7 | **花园区被毁 / 焦土 / 巨龙爪痕** | 4.0.3a | ❌ | Park 页 `Patch 4.0.3a: Destroyed.`；**旧世的花园区是完好的绿地** |
| 8 | **半淤浅的运河**（淤泥 / 芦苇 / 露出水面的杂物 / 能趟过去） | 4.0.3a | ❌ | `Canals now halfway filled in with mud/silt, along with occasional reeds and lost debris.` |

### B. 【本次新发现 —— sk2 w1 需要更正的两条】

| # | 项 | 引入补丁 | 说明 |
|---|---|---|---|
| **9** | **暴风城公墓** Stormwind City Cemetery | **4.0.3a Added** | sk2 `stormwind.district.043` 把「大片的暴风城公墓在教堂广场以北」写成了旧世事实——那句话取自 Cathedral Square 页的**现行版本**描述。公墓页自己写 `Patch 4.0.3a: Added.`，**旧世教堂广场后面没有公墓**。已从树中剔除。 |
| **10** | **暴风湖** Stormwind Lake | **4.0.3a Added** | 同上，sk2 `stormwind.district.044`。原文：「the most prominent feature of a **new** park-like district ... opened in the northeastern part of the city, behind the Cathedral of Light」。旧世教堂广场北侧是城墙，不是湖。已剔除。 |

> 这两条是本片区最值得记的收获：**区级页面的「Points of interest」小节写的是当前版本，逐个点进去看 patch 段才是判定依据。**

### C. 建筑 / 店铺级

| # | 项 | 补丁 | 判定 | 旧世对应物 |
|---|---|---|---|---|
| 11 | 矮人区旅店 **黄金酒桶** The Golden Keg | 4.0.3a Added | ❌ | 旧世矮人区没有旅店；顺带——它的萨满训练师更晚（联盟 2.0.1 才有萨满） |
| 12 | 矮人区 **拍卖行** + **暴风城皇家银行** | 4.0.3a | ❌ | 旧世全城只有贸易区一个银行、一个拍卖行 |
| 13 | **珀斯板甲** Potts' Plates（矮人区） | 4.1.0 Added | ❌ | — |
| 14 | **林荫女士** The Shady Lady（矮人区黑市） | 4.2.0 Added | ❌ | 那栋楼旧世就在（割喉小巷唯一入口就穿过它），但**没有招牌名** |
| 15 | **登曼家族珠宝** Denman Family Jewelers | 4.0.3a Added | ❌ | 珠宝加工是 2.0.1 才有的专业 |
| 16 | **三缕风** The Three Winds | 4.3.0 Added | ❌ | 旧世同一位置是 **The Finest Thread**（裁缝材料铺） |
| 17 | **暴风城铭文设计店** The Scribe of Stormwind | 3.0.2 有 NPC / 4.0.3a 挂招牌 | ❌ | 旧世那栋楼空着；铭文专业本身是 3.0.2 才有的 |
| 18 | **考迪尔的附魔店** Cordell's Enchanting | 4.0.3a「Building given its name」 | ⚠️ 半 | **建筑与附魔师旧世就在**（卫兵指路原话：去监狱路上、法师区外侧的运河边有间附魔铺），只是没名字。树里以 `canals_enchanting_shop`「运河边的附魔师铺子」收录，**不套用后期店名** |
| 19 | **北剪理发** Northshear Abbey（理发店） | 3.0.2 Added（9.0.2 改名） | ❌ | 旧世没有理发店 |
| 20 | **交易者大厅** Trader's Hall | 建筑 1.9.0 有 / **名字 4.0.3a 才有** | ⚠️ 半 | 旧世贸易区中央确有拍卖行（1.9.0 起），但**不叫这个名字**；树里记作「贸易区拍卖行」 |
| 21 | **狮鹫栖木** Gryphon Roost | 「Subzone added to an existing area」4.0.3a | ⚠️ 半 | 地点与飞行管理员杜加尔·朗德瑞克旧世就在；只是旧世走上坡道时小地图不会跳出这个名字 |
| 22 | **猪和哨声** 作为子区域名 | 7.1.5 | ⚠️ 半 | 酒馆旧世就在；**但旧世它没有旅店老板**（玛根·蒂尔曼 4.0.1 才加，官方原文称此举让它成为暴风城的「第二家」旅店——反过来把此前的旅店数量钉死成 1） |
| 23 | **训练大厅** Training Hall | 9.0.1 | ❌ | 旧世是 **指挥中心 Command Center**（只有战士与猎人训练师）；职业训练师**分散在各区**，不集中 |
| 24 | **巫师圣殿的传送门大厅** Stormwind Portal Room | 8.1.5 | ❌ | 旧世塔内是法师训练塔（要爬外盘石阶上塔顶再过一个传送门去找训练师）；**成排的各主城/外域/德拉诺传送门一律不得入画**。sk2 `stormwind.district.032` 的措辞（「也是通往联盟各主城的传送门房间」）按此更正 |
| 25 | **暴风要塞内外全面重制** | 4.0.3a | ❌ | 露天步道通往王座厅、王座厅前的大喷泉、俯瞰暴风湖的花园平台——一个都不能出现 |
| 26 | **皇家画廊被移除** | 4.0.3a | ✅ 反向 | 旧世**有**，正片可以拍 |
| 27 | **旧城区↔贸易区的铁闸门被移除** | 大灾变 | ✅ 反向 | 旧世**有**，而且它是「这城有一块谁也进不去的地方」的天然钩子 |
| 28 | **教堂广场的乌瑟尔雕像** | 4.0.3a | ❌ | 旧世是**阿隆索斯·法奥纪念碑**。sk2 裁定，本树照办。「Uther the Lightbringer / A righteous Paladin」铭牌一入画就是穿帮 |
| 29 | **城门上的巨龙头颅 + 全城 buff** | 1.3.0 起、3.2.2 停 | ✅ 反向 | **旧世有、现行没有**。`Rallying Cry of the Dragonslayer` 页配图说明即「Nefarian's Head hanging from the gates of Stormwind」；1.7.0 还修过它的触发 bug |
| 30 | **宝库顶的钟停在 8:15** | 大灾变之后 | ❌ | 那是「死亡之翼袭城的时刻」的设定（致敬广岛）；旧世钟面不该停 |
| 31 | **比兹莫的搏击俱乐部**（矿道地铁暴风城站下方） | 5.1/5.3 | ❌ | — |
| 32 | **矿道地铁暴风城站口的坡道** | 4.0.3a | ❌ | 旧世站口形制与之不同（sk2 w7 已裁定） |
| 33 | **英雄谷的哈蒙德·克雷将军** | 《巫妖王之怒》后（前任马库斯·乔纳森在塞拉摩阵亡） | ❌ | 旧世骑马巡视谷地的是**马库斯·乔纳森** |
| 34 | **达纳斯雕像倒塌 / 谷地双塔的焦黑爪痕** | 4.0.3a | ❌ | 旧世五尊像与两塔都完好 |
| 35 | **勇士大厅的形态** | 1.4.0 加入 → 2.0.1 取消荣誉门槛 → 3.0.2 不再是独立实例 | ⚠️ | 旧世它**有荣誉门槛、是独立实例、有自己的载入画面、门可以关上**——这三点现在全没了 |

---

## ③ 存疑与未查

1. **祈愿室 Petitioner's Chamber（暴风要塞）—— 未进树。** 中英文导航框都把它列为要塞的当前子区域，
   但页面无 patch 段、且正文描述的是「沿坡道进要塞后右手第一间」——**那条坡道本身是 4.0.3a 才有的**。
   旧世要塞入口形制不同，无法确证这间房当年存在。**宁可漏一个真的，不编一个假的**，故留在此处。
   要补的话须从 1.12 客户端的 AreaTable / 旧世截图核。
2. **运河上到底有几座桥。** 只能确证三座：英雄谷石桥（车行宽桥）、教堂广场↔矮人区人行桥、要塞吊桥。
   其余桥的数量与形制**没有任何文字来源**（sk2 也没找到）。建模时桥数属自行设定，**口播不要报数字**。
3. **运河有没有水闸。** 遍查无记载，倾向「设定没写、且大概率没有」。
4. **阿隆索斯·法奥纪念碑长什么样。** 只知道旧世那儿是 monument 而非 statue，碑体形状/高度/有无人像浮雕全未知。
   **这是必经之地的构图中心，值得优先补图。**
5. **贸易区喷泉的形制**（几级水池、有无雕像、水柱高度）、**英雄谷石桥的尺寸**（桥长桥宽、雕像与桥的比例）——均无来源。
6. **矿道地铁水下段是不是玻璃穹顶** —— 文字来源只说「水下段其实是一个地下湖」，隧道断面与照明方式没写，须人眼核图。
7. **大教堂内部的「宏大议事厅」Grand Chamber** —— 出处是 RPG 设定书《Alliance Player's Guide》（非正史），未进树。
8. **冰锥甜筒 Cone of Cold（法师区儿童周冰淇淋摊）** —— 无 patch 记录，无法判断儿童周哪个补丁把它加进暴风城，未进树。
9. **译名分歧三处**（灰机 wiki vs sk2，均未能从 zhCN 客户端一手复核）：

   | 英文 | 灰机 wiki | sk2 用法 | 本树采用 |
   |---|---|---|---|
   | The Gilded Rose | **镶金玫瑰** | 镀金玫瑰 | 镶金玫瑰（灰机为条目正名；sk2 自己标了「译名待核」） |
   | Stormwind Counting House | **暴风城会计室** | 暴风城金库 / 暴风城银号 | 暴风城会计室 |
   | The Park | **花园** | 花园区 | 花园区（灰机正名「花园」，中文 GM 坐标表也写「花园」，加「区」字更像区名） |

   **Deeprun Tram = 矿道地铁** 两边一致，sk2 未查第 4 条的这一半可以结案（「地下城铁」不是官方译名）。
10. **The Finest Thread 的官方中文译名未查到**（灰机无此条目），树里保留英文原名并在 `note_zh` 里写明。
11. **wowhead 全线 403**，所以本树的 `coords` 只覆盖 25/101 个节点（都来自 wiki 页自带的 `{{coords}}`）。
    等级只有暴风城监狱有（22–30，7.3.5 前）。
12. **花园区只挂到 4 个节点**——这不是没查全，而是旧世的花园区**本来就没有更多命名地点**：
    它是一整片绿地，除月亮井与园区广场外没有任何有名字的店铺或建筑（全城 37 家商店里一家都不在花园区）。

---

## ④ 本片区的地图与图片链接清单

> **只记 URL 与版权状态，未下载、未保存任何字节。**
> 仓库既有裁定：**暴雪美术资产只进人眼、不入画、不上传给生成模型**——下面所有条目一律按此处理，
> 它们的用途是**人眼核形制**（补 §3 那几个「文字查不到长什么样」的空档），不是喂给出图模型的参考图。
> 版权状态一栏全部是「Blizzard Entertainment 版权，wiki 上以合理使用展示」。

### ✅ 可用于核 Vanilla 形制（页面自身标注了是旧世 / 旧世独有内容）

| 用途 | File 页 URL |
|---|---|
| **城门（大灾变之前）** | https://warcraft.wiki.gg/wiki/File:Gates.jpg |
| **完好的花园区** | https://warcraft.wiki.gg/wiki/File:The_Park.jpg |
| **花园区入口旗幡** | https://warcraft.wiki.gg/wiki/File:The_Park_banner.jpg |
| **奥妮克希亚头颅挂在城门上** | https://warcraft.wiki.gg/wiki/File:Onyxia%27s_head_in_Stormwind.jpg |
| **暴风城监狱 · 大灾变前的 boss 群像** | https://warcraft.wiki.gg/wiki/File:Stockbosses.jpg |
| 监狱载入画面 | https://warcraft.wiki.gg/wiki/File:Stormwind_Stockade_loading_screen.jpg |
| 矿道地铁载入画面 | https://warcraft.wiki.gg/wiki/File:Deeprun_Tram_loading_screen.jpg |
| 矿道地铁暴风城站 | https://warcraft.wiki.gg/wiki/File:VZ-Deeprun_Tram.jpg |
| 宝库（白天 / 夜间自运河看） | https://warcraft.wiki.gg/wiki/File:Stormwind_Vault.jpg ／ https://warcraft.wiki.gg/wiki/File:StormwindVaultAtNight.jpg |
| 割喉小巷 | https://warcraft.wiki.gg/wiki/File:Cut-Throat_Alley.jpg |

### ⚠️ 未标版本，须先核再用（4.0.3a 对这几块的改动程度不一）

| 用途 | File 页 URL |
|---|---|
| **暴风城全城地图（导航框用图）** | https://warcraft.wiki.gg/wiki/File:VZ-Stormwind_City.jpg |
| 贸易区 | https://warcraft.wiki.gg/wiki/File:The_Trade_District.jpg |
| 旧城区 | https://warcraft.wiki.gg/wiki/File:Old_Town.jpg |
| 法师区 | https://warcraft.wiki.gg/wiki/File:The_Mage_Quarter.jpg |
| 教堂广场 | https://warcraft.wiki.gg/wiki/File:Cathedral_Square.jpg |
| 教堂广场入口旗幡 | https://warcraft.wiki.gg/wiki/File:Cathedral_Square_banner.jpg |
| 矮人区 | https://warcraft.wiki.gg/wiki/File:The_Dwarven_District.jpg |
| 运河 | https://warcraft.wiki.gg/wiki/File:The_Canals_of_Stormwind_City.jpg |
| 英雄谷 | https://warcraft.wiki.gg/wiki/File:The_Valley_of_Heroes.jpg |
| 英雄谷（集换式卡牌画，非游戏截图） | https://warcraft.wiki.gg/wiki/File:Stormwind_City_TCG.jpg |
| 旧城区（《死亡骑士》漫画分格） | https://warcraft.wiki.gg/wiki/File:Old_Town_-_Death_Knight_manga.png |
| 矿道地铁路线图（**玩家自制、非官方**） | https://warcraft.wiki.gg/wiki/File:Deeprun_Tram_Map.jpg |

### ❌ 明确是大灾变及之后，仅作反面对照、**不得入画**

`File:Park_Destroyed.jpg` · `File:Stormwind_Guard_crying_over_Park.jpg` · `File:Lion%27s_Rest.jpg` ·
`File:Stormwind_Gate_Cataclysm.jpg` · `File:Stormwind_Keep_Post_Cata.jpg` · `File:Stormwind_Keep_Cataclysm.jpg` ·
`File:Cathedral_of_Light_Cataclysm.jpg` · `File:Cathedral_of_Light_inside_Cataclysm.jpg` ·
`File:The_Wizard%27s_Sanctum_Cata.jpg` · `File:Stormwind%27s_new_Portal_Room.jpg` ·
`File:Sharbour.jpg`（港口）· `File:Stormwind_Embassy.jpg` · `File:WorldMap-TheStockade.jpg`（4.0.3a 才加的副本地图，且监狱已被重制）·
`File:Stormwind_City_after_the_Cataclysm.jpg` · `File:View_of_clock_set_at_8-15_(and_3-45).jpg`（停摆的宝库钟面）

> **空档提示**：wiki 上**没有**标注为 Vanilla 的「王座厅内景」「镀金/镶金玫瑰内景」「阿隆索斯·法奥纪念碑」
> 「暴风城卫兵战袍正面」这四样图。sk2 已向用户提请**在 Classic Era 客户端里截图**，本片区确认这四项仍是空档。

---

## ⑤ 给下游的提醒

1. **合龙时的唯一外部依赖是 `kingdom_of_stormwind`。** 本片区所有 101 个节点的 parent 链最终收在
   `stormwind_city → kingdom_of_stormwind`。谁负责艾尔文森林/暴风王国那一片，请确保这个 id 存在且拼法一致。
2. **`adjacent` 只在 `stormwind_city` 一个节点上填了值（`[elwynn_forest]`），这是一处有意为之的偏离。**
   字段规则写的是「只有 zone / continent 填」，但暴风城在世界地图上**本身就是一个 zone**（AreaTable 1519），
   而「暴风城↔艾尔文森林」是全城唯一的陆路连接、下游必须知道。其余 100 个节点的 `adjacent` 一律是空列表。
   若生成器严格按 type 校验 adjacent，请把 `city` 也放进白名单，或由合龙方把这条边移到自己那侧。
3. **暴风城只有两个入口。** 陆路正门（艾尔文森林 → 暴风城大门 → 英雄谷石桥 → 贸易区南入口）
   与地下（矮人区东侧齿轮隧道 → 矿道地铁 → 铁炉堡）。**没有海港、城墙上没有第二道门**。
   去赤脊山 / 西部荒野 / 暮色森林都必须先出正门回艾尔文森林再分路。
4. **矿道地铁是跨片区节点。** 本树把它挂在 `dwarven_district` 下，只收了暴风城这一端的站与地下湖段。
   **铁炉堡那一端（机械侏儒区的车站）归铁炉堡片区**，请那边挂一个对应节点并在 `note_zh` 里互指，不要重复收录整条线。
5. **本树是纯 Vanilla 的，所以它比任何网上的暴风城地图都「少东西」。** 下游选景时看到某个地方树里没有，
   第一反应应该是查 §2 表里有没有它，而不是以为漏了。特别容易误入的六个：
   **港口 / 公墓 / 暴风湖 / 雄狮之眠 / 郊外农舍 / 巫师圣殿的传送门大厅**。
6. **选景强度排序（sk2 玩家记忆强度「强」与本树节点的对应）：**
   炉石绑在镶金玫瑰（全城唯一旅店）· 矿道地铁去铁炉堡 · 英雄谷五尊雕像 · 城门上的巨龙头颅 ·
   贸易区银行/拍卖行/邮箱三件套 · 运河里的两座水中石堡 · 监狱门口的集合石 · 花园区月亮井 ·
   已宰的羔羊地窖的召唤法阵 · 王座厅上坐着的那个孩子。这十个是排镜时优先保的。
7. **建模坐标基准沿用 sk2**：原点取城门（GM 世界坐标 `-9040.90, 451.38, 93.06`），
   `east = -(y-451.377)×0.9144`、`north = (x+9040.899)×0.9144`、`up = (z-93.056)×0.9144`（米）。
   全城包围盒约 **640 × 600 × 37 m**，要塞最高（+26.7 m）、花园区最低（−3.0 m）——
   **花园区往教堂广场是上坡、法师区往贸易区是下坡 22 m**，previz 不能按平地排。
8. **矮人区的识别特征是尺度不是材质**：层高压到 2.8 m、门洞 2.0 m（人类区是 3.5 m / 2.4 m）。
   这比任何贴图变化都管用（sk2 建模建议）。
9. **运河必须是深水**：堤顶到水面要有明显落差、能看见水下暗色石砌河床。做成能趟过去的浅水就等于把版本穿帮写进了几何。
