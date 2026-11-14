# 调研 · 第一期 3D 模型来源（世界最大陆地动物 Top 30 + 人体参照）

> 2026-11-06 代理调研。物种清单以 `ai_videos/paihangbang/episodes/ep04_largest_land_animals/data.json` 为准（30 条，第 15 名并列两种，所以没有第 16 名）。
> 规则依据：`bible.md` §0（用户定：全流程可商用）。许可**只采信 API / 页面上实际读到的字段**，读不到的写「未核实」。本次只做网页和公开 API 查询，没有下载任何模型文件；看过的缩略图都在会话临时目录里，不进仓库。
> 「合格候选」= 许可在白名单内（CC0 / CC BY 4.0 / 允许商用和修改的自定义许可）**并且**来源没有危险信号。只有许可字段合格、但来源存疑的，一律不算合格。

## 1. 结论摘要

**总体：30 种里 16 种有本物种的可用候选（其中 5 种质量或来源偏弱），14 种是缺口**，缺口要用近缘模型（`PROXY MODEL`）或简化剪影兜底。人体参照用 MPFB（自带素材 CC0，已读到许可原文），确定可用。

| # | 物种 | 状态 | 首选候选（详见 §3） |
|---|---|---|---|
| 1 | 非洲草原象 African Bush Elephant | ✅ 合格 | animalanimator「African Elephant Bull」CC BY |
| 2 | 亚洲象 Asian Elephant | ⚠ 弱 | sdpm「Elephant」（简介写的是印度象）CC BY，来源可信度中等 |
| 3 | 白犀 White Rhinoceros | ✅ 合格 | absol_cg / iznvm / MUVHN（科研复原雕塑扫描）CC BY |
| 4 | 印度犀 Indian Rhinoceros | ⚠ 弱 | 奥赛博物馆前的 Jacquemart 犀牛铜像扫描（edemaistre）CC BY，造型偏雕塑化 |
| 5 | 非洲森林象 African Forest Elephant | ❌ 缺口 | 用 #1 当近缘模型 |
| 6 | 河马 Hippopotamus | ✅ 合格 | andrey.「Hippo (downloadable, revised)」CC BY |
| 7 | 爪哇犀 Javan Rhinoceros | ❌ 缺口 | 用 #4 当近缘模型（同属） |
| 8 | 长颈鹿 Giraffe | ✅ 合格 | animalanimator「Reticulated Giraffe」CC BY |
| 9 | 黑犀 Black Rhinoceros | ❌ 缺口 | 没找到有物种辨识度的模型；用 #3 当近缘模型 |
| 10 | 印度野牛 Gaur | ❌ 缺口 | 用 Micket「Auroch」CC0（同为野生牛属）当近缘模型 |
| 11 | 野牦牛 Wild Yak | ⚠ 弱 | iedalton「Cart pulled by a Yak」CC BY（要去掉车）；另一个候选来源未核实 |
| 12 | 野水牛 Wild Water Buffalo | ⚠ 弱 | Gotta_go_evil_Fast「Jafarabadi Buffalo」CC BY（家养品种，来源未核实）；kenchoo 版本有归属争议 |
| 13 | 美洲野牛 American Bison | ✅ 合格 | sciamop「American Bison」CC BY（素模雕刻，585k 面，要减面）、Zafflex 低模 |
| 14 | 苏门答腊犀 Sumatran Rhinoceros | ❌ 缺口 | 用 #3 或 #4 当近缘模型，并标 `PROXY MODEL` |
| 15 | 非洲水牛 African Buffalo | ✅ 合格 | kenchoo「African Buffalo」CC BY（改自 Stephengury，CC BY，署名链完整） |
| 15 | 爪哇野牛 Banteng | ❌ 缺口 | 用 Micket「Auroch」CC0 当近缘模型 |
| 17 | 大羚羊 Giant Eland | ❌ 缺口 | 没有可用模型；先用剪影，或用牛科近缘模型并标注 |
| 18 | 欧洲野牛 European Bison | ❌ 缺口 | 用 #13 当近缘模型（同属） |
| 19 | 普通大羚羊 Common Eland | ❌ 缺口 | 同 #17 |
| 20 | 驼鹿 Moose | ✅ 合格 | cosmical「Hirvi (Alces alces)」CC BY（标本扫描，450k 面，要减面）、kingmoon3D、WildMesh_3D 卡通渲染版 |
| 21 | 北极熊 Polar Bear | ✅ 合格（偏卡通） | Sengchor「Polar Bear」CC BY；OGA STKRudy85 低模 CC0 |
| 22 | 细纹斑马 Grévy's Zebra | ❌ 缺口（同属） | 没有细纹斑马模型；用通用斑马模型当近缘模型 |
| 23 | 藏野驴 Kiang | ❌ 缺口 | 用 Quaternius Donkey（CC0 / QAL）当近缘模型（同属） |
| 24 | 棕熊 Brown Bear | ✅ 合格 | andrey.「Brown Bear (animated)」、criticaldamage9211「Grizzly Bear」CC BY |
| 25 | 马鹿 Elk (Wapiti) | ✅ 合格 | WildMesh_3D「Realistic Animated Elk」CC BY（简介明说可商用）；asik「Elk」素模 |
| 26 | 羚牛 Takin | ❌ 缺口 | 没有可用模型；用剪影 |
| 27 | 麝牛 Muskox | ✅ 合格（低模） | bojan6「Muskox_ Loop (3)」CC BY |
| 28 | 紫羚羊 Bongo | ❌ 缺口 | 唯一的候选（yoshi2024-2025）来源存疑，不收；用剪影或近缘模型 |
| 29 | 山斑马 Mountain Zebra | ❌ 缺口（同属） | 用通用斑马模型当近缘模型 |
| 30 | 平原斑马 Plains Zebra | ⚠ 弱 | micsir「Zebra」、dirdim「Zebra」（是幼驹）CC BY；都要人工复核 |
| — | 人体参照 1.75 m | ✅ 合格 | MPFB 自带素材 CC0（LICENSE.ASSETS.md 原文） |

**缺口清单（14 个）：** 非洲森林象、爪哇犀、黑犀、印度野牛、苏门答腊犀、爪哇野牛、大羚羊、欧洲野牛、普通大羚羊、细纹斑马、藏野驴、羚牛、紫羚羊、山斑马；另有两种可以靠近缘模型补，但要先过数据组的意见：野牦牛、野水牛（候选偏弱）。

**建议风格路线：(b) 统一中性材质**，加两个小例外（详见 §5）：
- 所有模型去掉原贴图，统一用同一种黏土 / 哑光材质，再按物种上主色；
- 只有斑马和长颈鹿的花纹是认物种的关键，用我们自己写的程序化纹理补上（产出归我们所有，不涉及第三方贴图）。

理由：这样能把 30 个来源、不同精度的模型统一成一种画风；素模扫描、近缘模型和低模也能放在同一画面里，不显得突兀；贴图许可的风险也一并消掉。

**需要用户拍板的事：**
1. 缺口太多（14 种），是否接受大量 `PROXY MODEL`（近缘模型），还是换题、把条目缩到「有合格模型的种」？
2. `bible.md` §4.1 写了「TripoSR 图生 3D 兜底」，但本次任务说明「不用任何 AI 生成 3D」。这两条有冲突，本文件按「不用」处理，没有把 TripoSR 列入兜底方案。

## 2. 来源与许可规则

| 来源 | 许可（实际读到的字段 / 原文） | 商用结论 | 署名要求 | 出处 URL |
|---|---|---|---|---|
| Sketchfab | 逐模型。API `license.slug`：`by` 对应 `http://creativecommons.org/licenses/by/4.0/`，要求「Author must be credited. Commercial use is allowed.」；`cc0` 对应 CC0 1.0。`by-sa` / `by-nd` / `by-nc*` / `st` / `free-st` / `ed` 都在白名单外 | 只收 `by`、`cc0` | `by`：标题、作者、链接、CC BY 4.0，并注明「已修改」（缩放、换材质、摆姿势） | <https://api.sketchfab.com/v3/licenses> |
| Sketchfab 二次创作链 | 例如 kenchoo「Rebuilt」系列：简介写明原作及其 CC BY 4.0 | 原作也是 `by` 才能用；原作账号已注销、读不到许可的，算「未核实」 | 原作和改作都要署名 | 各模型页 |
| Poly Pizza | 网页和 API 都没取到：API 回 `401 "You need an API key"`；网页被 Cloudflare 人机验证拦住（没有绕过） | **未核实** | — | <https://api.poly.pizza/v1.1/search/elephant>、<https://poly.pizza/search/elephant> |
| Quaternius 官网 | 动物包页面写「License CC0」；站点许可页现为 Quaternius Asset License (QAL) v1.0（2026-08-28）：允许个人、教育、商业用途，允许「Use, copy, and modify」，产品（含 film、video、render）无需署名；禁止把素材本身单独转售或再分发。§7：按取得时的版本执行 | ✅（CC0 或 QAL 都在白名单内） | 不要求（QAL「No attribution is required」） | <https://quaternius.com/packs/ultimateanimatedanimals.html>、<https://quaternius.com/license.html> |
| OpenGameArt | 逐条 License(s) 字段 | 只收 CC0、CC-BY 3.0/4.0；CC-BY-SA 一律不收 | CC-BY 要署名 | 各条目页 |
| OGA · Micket（0 A.D. 作者） | 模型 CC0；但页面写明「Texture exists for the game 0AD」，贴图不在 CC0 包里（0 A.D. 美术素材的许可未核实，不用） | ✅ 只用网格 | 不要求 | <https://opengameart.org/content/white-rhinoceros> 等 |
| Poly Haven | 模型全站 CC0；API 列出的 521 个模型里，和动物相关的只有摆件、动物头和老鼠 | ✅，但没有可用的大型动物 | 不要求 | <https://api.polyhaven.com/assets?t=models> |
| Smithsonian 3D | 3D API 按物种搜：大象、野牛、熊、水牛只返回骨骼和文物，长颈鹿、犀牛、河马、斑马、驼鹿是 0 条 | 没有可用的完整躯体 | — | <https://3d-api.si.edu/api/v1.0/content/file/search?q=elephant&rows=50> |
| NIH 3D | 搜索页返回 404，没查到 | **未核实**（以生物医学模型为主） | — | <https://3d.nih.gov/search?q=elephant> |
| MorphoSource | Anubis 防护拒绝访问 | **未核实**（以 CT 骨骼为主，许可多为 NC，要逐条看） | — | <https://www.morphosource.org/catalog/media?q=elephant> |
| MPFB（人体） | `LICENSE.ASSETS.md` 标题为「Creative Commons CC0 1.0 Universal」；代码许可是 GPLv3（`LICENSE.CODE.md`），只约束插件本身 | ✅ 只用自带素材 | 不要求 | <https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.ASSETS.md> |

**这次发现、所有来源通用的排除规则：**
- **游戏提取**：例如 planeta-elefante（标题直接写着 Zoo Tycoon 2、Postal 2、The Lion King）、jimmyho905（Planet Zoo）、toro_ardido_modelos_3d（简介写明「from far cry 4」）。这些模型的 CC BY 标签无效，整批排除。和它们**面数完全一样**的别人上传的版本（GremorySaiyan、freddy1231、Otherspectre、oscar05.emiliano 等）也一并排除。
- **许可洗白**：voltairevillela「African Buffalo」（16238 面）和 WildMesh_3D 的「BUFFALO – DEMO FREE」（**CC BY-NC**，16238 面）网格相同。hendrikReyneke / NoaSeller / moizmuhammad373 的斑马（12306 面）和 kenchoo 的 **CC BY-NC-ND** 斑马网格相同。以上都排除。
- **AI 生成**（任务要求不用）：标签或简介写了 Meshy、`createdwithai`、AI 的一律排除，例如 sudiptamahato2007、pltcerdos、santanudas200120、noguyin、raven-woods、rt699448（标签含 `AI`）、EthanfromEngland「[MESHY 6]」。没有声明、但同一账号 2026 年批量上传、30 万面左右、没有简介的（rushilshar081108），算「疑似」，不收。
- **第三方 IP / 雕塑**：Stephengury 的「Zebra」其实是《马达加斯加》里的 Marty；Marvel 的犀牛人；noe-3d.at 的 CC0 动物（Liegender Bison、Eisbär、Wasserbüffel und Knabe）都是 20 世纪 60 年代作者的公共雕塑，雕塑家的著作权另算，`toolchain_licenses.md` 已规定第一季不做。以上排除。例外：奥赛博物馆的犀牛铜像，作者 Alfred Jacquemart 1896 年去世，铜像本身已进入公有领域，可以按 CC BY 的扫描件用。
- **来源存疑**：yoshi2024-2025（「Animalia - Kiang」等成批上传，没有简介；同一账号另有一件 `Free Standard`）；Dhruvin743（简介说是「从网上免费下载的模型」）。不收。

## 3. 候选表（30 种 + 人体）

图例：✅ 推荐｜🟡 能用但有保留｜⛔ 已排除（留作复核证据）。面数取 API 的 `faceCount`，许可取 API 的 `license.label`（`CC Attribution` = CC BY 4.0）。以下所有 Sketchfab 条目的 `isAgeRestricted` 都是 `false`，`isDownloadable` 都是 `true`。
模型页 URL 规则：`https://sketchfab.com/3d-models/<uid>`；详情 API：`https://api.sketchfab.com/v3/models/<uid>`。

| # | 物种 | 来源 | 模型名 | uid / URL | 许可 | 作者 | 面数 | 适合度备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | 非洲草原象 | Sketchfab | African Elephant Bull - Rigged & Animated | 436483857ce84c77bd0f6c76fb3d4d2d | CC BY | animalanimator | 85,704 | ✅ 写实、带绑定，2026-10 上传。简介另外要求署名时链接 animalanimator.com 的对应页面 |
| 1 | 非洲草原象 | Sketchfab | Elephant | 4ae161372d6a4219a87340339d1ffe03 | CC BY | rukh3d | 1,958 | ✅ 低模写实，适合路线 (b) |
| 1 | 非洲草原象 | Sketchfab | African Elephant | facb060916534e7eae8e6a5a8056185f | CC BY | Joseph.AD | 3,080 | 🟡 低模 |
| 1 | 非洲草原象 | Sketchfab | Elephant | f57057ad0c2044ec88c9ba5ab5c18a41 | CC BY | Stephengury | 3,524 | 🟡 这位上传者也上传过 IP 角色（Marty），原创性要复核 |
| 1 | 非洲草原象 | Sketchfab | African Elephant Textured | 49ad44f03f374433ac3a4f3143d7980c | CC BY | JohnMesplay | 53,341 | ⛔ 缩略图是机械象（概念设计 Robert Chew） |
| 2 | 亚洲象 | Sketchfab | Elephant | e0755e38063b4de0b152be78c6da99b5 | CC BY | sdpm | 39,394 | 🟡 简介写「3D Highpoly Indian Elephant created by SDPM」；剪影是亚洲象；有人重传了这位作者的河马（psk98077），说明作者自己应是原作者，但仍是中等可信 |
| 2 | 亚洲象 | Sketchfab | Asian Elephant #2 | e636b346fa7647b69f0a709af1f01d0d | CC BY | Avijoy.L | 28,994 | 🟡 Vectary 做的低精度原创，造型偏玩具 |
| 2 | 亚洲象 | OGA | low poly elephant model | <https://opengameart.org/content/low-poly-elephant-model> | CC0 | syncopika | 未核实（.blend 1.8 MB） | 🟡 通用灰色低模，没写是哪种象 |
| 2 | 亚洲象 | Sketchfab | elephant | ede84e2c3ae849348f1048cc18d91409 | CC BY | toro_ardido_modelos_3d | 15,820 | ⛔ 简介写明「from "farcry4"」 |
| 2 | 亚洲象 | Sketchfab | Asian Elephant | 005e3725b8d9484e94a71aeb9495aea6 | CC BY | Dhruvin743 | 5,223 | ⛔ 简介说是从网上下载的模型，只重画了贴图 |
| 3 | 白犀 | Sketchfab | White rhinoceros | 939baeb6d62a4824b8edb3c7f7ef54c7 | CC BY | absol_cg | 9,310 | ✅ 写实，Blender + Substance 制作 |
| 3 | 白犀 | Sketchfab | White Rhino | 8ae1030c47ed4d3c9acc8f1360aa73de | CC BY | iznvm | 70,486 | ✅ 素模，很适合路线 (b) |
| 3 | 白犀 | Sketchfab | White rhino (Ceratotherium simum) | 5cac7c73708b4f1bb247a73fed22b47d | CC BY | MUVHN（瓦伦西亚大学自然史博物馆） | 2,691,880 | 🟡 Pitarch 博士 1:15 科研复原黏土雕塑的扫描，形态最准；面数超标，要减面；署名时带上博物馆 |
| 3 | 白犀 | Sketchfab | White Rhinoceros | 65e9105d24314887bf8dafb06d3401d0 | CC BY | sdpm | 20,316 | 🟡 同 sdpm 的可信度说明 |
| 3 | 白犀 | OGA | White Rhinoceros | <https://opengameart.org/content/white-rhinoceros> | CC0 | Micket | 未核实（zip 78 KB） | 🟡 极低模，只用网格 |
| 4 | 印度犀 | Sketchfab | Day 191: A rhinoceros in Paris - 1scanaday | 337e1aba96b245448e3ba95a5fdde348 | CC BY | edemaistre | 64,177 | 🟡 奥赛博物馆前 Jacquemart 的犀牛铜像（铜像已进入公有领域）；要切掉底座；皮褶是雕塑化的 |
| 4 | 印度犀 | Sketchfab | Rhinocéros in Orsay museum, Paris | b824332212fc48e2adfff4eab46d9485 | CC BY | HoangHiepVu | 351,224 | 🟡 同一座铜像，精度更高，面数超标 |
| 4 | 印度犀 | Sketchfab | Rhino from Versailles (taxidermy) | c91d6ac0cf6f4a608b78ecb98052d841 | CC BY | marcusjt | 90,175 | 🟡 真实标本扫描，但缩略图显示扫描不完整 |
| 4 | 印度犀 | Sketchfab | Indian Rhino (Smoothie 3D) | 7e9695868ed64f419e09efdfe3120cb4 | CC BY | nebulousflynn | 20,548 | ⛔ 用一张维基共享资源照片生成；那张照片的许可未核实，若是 CC BY-SA 就会传染 |
| 5 | 非洲森林象 | — | （没找到合格模型） | — | — | — | — | ❌ 只找到 planeta-elefante 的「Forest elephant」（游戏提取，已排除）和 SpaceMonkeyBoi 的 348 面方块模型。用 #1 当近缘模型 |
| 6 | 河马 | Sketchfab | Hippo (downloadable, revised) | f3b84051e0824892ad5d551aa7040cdb | CC BY | andrey. | 82,804 | ✅ 写实；作者说明「all textures and model are created by hand」（原话出自同作者的熊模型页） |
| 6 | 河马 | Sketchfab | Hippopotamus | e3244268216244808d2603d23ef37310 | CC BY | Mehrus | 10,608 | ✅ 自雕自绘，标签 `noai` |
| 6 | 河马 | Sketchfab | Hippos | c0e0422d554a437083a306654977d1a6 | CC BY | thunders14 | 78,336 | 🟡 2016 年原作（kenchoo「Hippo」重建版的原作） |
| 6 | 河马 | Sketchfab | Hippopotamus amphibius | 0977b07597ea46f4a2f6a7cfacac523a | CC BY | Stephengury | 35,816 | 🟡 造型偏可爱；上传者可信度见 #1 |
| 7 | 爪哇犀 | — | （没找到） | — | — | — | — | ❌ `javan rhino`、`rhinoceros sondaicus` 都是 0 条；用 #4 当近缘模型（同属，体型更小） |
| 8 | 长颈鹿 | Sketchfab | Reticulated Giraffe - Rigged & Animated | b8a7cf34d2614b8c93e76d5300f9aaaa | CC BY | animalanimator | 58,915 | ✅ 网纹长颈鹿，写实；署名要求同 #1 |
| 8 | 长颈鹿 | Sketchfab | Giraffe | 522c042aad9f4348a74c2985ec3f99f9 | CC BY | BlueMesh | 3,932 | ✅ 低模写实，带绑定 |
| 8 | 长颈鹿 | Sketchfab | Giraffe | 98ecdd62c76d47dea44683b3f8b37bf6 | CC BY | Amx360 | 17,026 | ✅ |
| 8 | 长颈鹿 | Sketchfab | Giraffe camelopardalis | 4b78a5ed77b84305a588194e1f6e2ef5 | CC BY | Stephengury | 130,274 | 🟡 上传者可信度见 #1 |
| 9 | 黑犀 | Sketchfab | Rhino | 297542be5630405ebda68b8bbb3d5205 | CC BY | Stephengury | 50,000 | 🟡 没写是哪种犀牛，从缩略图分不出黑犀还是白犀 |
| 9 | 黑犀 | — | （没有物种专属的合格模型） | — | — | — | — | ❌ 写明「Black Rhinoceros」的只有 planeta-elefante（游戏提取）和 WaxFreeOintment 的体素模型；用 #3 当近缘模型 |
| 10 | 印度野牛 | OGA | Auroch (Male and female) | <https://opengameart.org/content/auroch-male-and-female> | CC0 | Micket | 未核实（zip 232 KB） | 🟡 近缘模型：原牛，和印度野牛同为牛属 |
| 10 | 印度野牛 | Sketchfab | Indian Gaur | 640e13903fff49bda7f3d178c8212c68 | CC BY | yoshi2024-2025 | 19,978 | ⛔ 来源存疑（见 §2） |
| 10 | 印度野牛 | Sketchfab | Indian Gaur model | 7d412c60aece4ec2acb57e07d8592d83 | CC BY | santanudas200120 | 741,878 | ⛔ Meshy AI 生成 |
| 11 | 野牦牛 | Sketchfab | Cart pulled by a Yak | 79effd5542c3427ba8b1d81b460338c4 | CC BY | iedalton | 3,788 | 🟡 低模，牦牛和车连在一起，要拆开；是家牦牛造型 |
| 11 | 野牦牛 | Sketchfab | Wild Yak | ebb7f00f6416454fbaf4ffa5f7037439 | CC BY | Gotta_go_evil_Fast | 4,342 | 🟡 没有简介，原创性未核实 |
| 11 | 野牦牛 | Sketchfab | yak | f04e827e94d048d2a72116faf0f67988 | CC BY | toro_ardido_modelos_3d | 5,938 | ⛔ 简介写明「from "far cry 4"」 |
| 12 | 野水牛 | Sketchfab | Jafarabadi Buffalo | cb15c03755394a71b57e6230daea574e | CC BY | Gotta_go_evil_Fast | 32,416 | 🟡 家养水牛品种，没有简介 |
| 12 | 野水牛 | Sketchfab | Water Buffalo | 124c4dec50a144489158eda878017f8c | CC BY | kenchoo | 30,200 | 🟡 同一网格的另一版简介写着「Nyilonelycompany claim was his model」，归属有争议 |
| 12 | 野水牛 | Sketchfab | water buffalo | 5a4c3796ea7e46ed8df88c60bddde1db | CC BY | noguyin | 19,659 | ⛔ Meshy AI 生成 |
| 13 | 美洲野牛 | Sketchfab | American Bison | d9e2d7f3ed0e4f9e98e154d0f05cfd9d | CC BY | sciamop | 584,896 | ✅ 素模雕刻（「Inspired by recent trip to Yellowstone」），很适合路线 (b)；要减面 |
| 13 | 美洲野牛 | Sketchfab | Low-poly Bison | 1e884702f6cb4bfe8dc90ecdf0a491a5 | CC BY | Zafflex | 2,138 | ✅ 低模 |
| 13 | 美洲野牛 | Sketchfab | Bison - animal | 4b8f112fffb84ce19dac2578b39e03b1 | CC BY | CMBC | 375,654 | 🟡 写实带贴图，原创性未核实，面数超标 |
| 13 | 美洲野牛 | Sketchfab | Animated Free Bison | be2dcd97db1c4b9c91a7728d9bc89925 | CC BY | AneesAnimates | 61,087 | 🟡 简介是营销文案，是否 AI 生成未核实 |
| 14 | 苏门答腊犀 | Sketchfab | Sumatran Rhino / (asiatic two-horned rhino) | 4cad8eca4b3549f786c864481575fc04 / 221961a1c293402a8adf81f3a14ef117 | CC BY | yoshi2024-2025 | 16,027 / 22,088 | ⛔ 来源存疑。缺口：用 #3 或 #4 当近缘模型 |
| 15 | 非洲水牛 | Sketchfab | African Buffalo | 10430df80e6446f2a77cb0ba93ed5cd1 | CC BY | kenchoo（改自 Stephengury） | 51,792 | ✅ 简介写明改自 Stephengury 的 CC BY 4.0 原作，两人都要署名 |
| 15 | 非洲水牛 | Sketchfab | African Buffalo | 0a3069416678435e967735e05c71c3b1 | CC BY | Stephengury | 8,312 | 🟡 原作；上传者可信度见 #1 |
| 15 | 非洲水牛 | Sketchfab | Cape Buffalo | 1f09d3c7729245ebb324ef878b8ca419 | CC BY | cmp_innovation_studio（卡内基自然史博物馆） | 49,562 | ⛔ 只有头部标本，没有躯体 |
| 15 | 非洲水牛 | Sketchfab | African Buffalo | c4d6b985fdc840aea430b6f540b6dff2 | CC BY | voltairevillela | 16,238 | ⛔ 许可洗白（原作是 WildMesh_3D 的 NC 模型） |
| 15 | 爪哇野牛 | — | （没找到） | — | — | — | — | ❌ `banteng`、`banteng cattle`、`bos javanicus` 都没有动物结果；用 #10 的 Auroch 当近缘模型 |
| 17 | 大羚羊 | — | （没找到） | — | — | — | — | ❌ `eland`、`giant eland` 都没有完整动物；`tragelaphus` 只搜到 rt699448 的 AI 模型。兜底见 §4 |
| 18 | 欧洲野牛 | — | （没找到） | — | — | — | — | ❌ MammalResearchInstitutePAS 的「Bison bonasus」**都是头骨**；raven-woods 的「European Wisent」是 Meshy 生成。用 #13 当近缘模型 |
| 19 | 普通大羚羊 | — | （没找到） | — | — | — | — | ❌ 同 #17 |
| 20 | 驼鹿 | Sketchfab | Hirvi (Alces alces) | 5a6866b2912348dabcb634acf5c93221 | CC BY | cosmical | 449,999 | ✅ 标本扫描，写实，带木底座要切掉；面数超标，要减面 |
| 20 | 驼鹿 | Sketchfab | Moose | 6ecd5623acfd4a57b2b5b472f601ef76 | CC BY | kingmoon3D | 12,509 | ✅ 写实低模 |
| 20 | 驼鹿 | Sketchfab | Moose Animated Cel Shading 3D Model | 33ce37106a24493ba4a6a6e2a9433bb6 | CC BY | WildMesh_3D | 6,394 | 🟡 卡通渲染风；简介明说可用于商业项目 |
| 20 | 驼鹿 | Sketchfab | Alces alces (Moose) | 77d17280c48742a9925c8789b603a531 等 | CC BY | MammalResearchInstitutePAS | 2.4M+ | ⛔ 是头骨 |
| 21 | 北极熊 | Sketchfab | Polar Bear | e4785419f10045e8805c3cecae763048 | CC BY | Sengchor | 179,192 | 🟡 偏卡通（标签 `noai`）；走路线 (b) 时可接受 |
| 21 | 北极熊 | OGA | White Bear (Low poly) | <https://opengameart.org/content/white-bear-low-poly> | CC0 | STKRudy85 | 未核实（7z 632 KB） | 🟡 低模，包里附 License.txt |
| 21 | 北极熊 | Sketchfab | Polar Bear | deeb7f4add9f4c36abaacdb73ce3e553 / 04dbccf27a694c8a82e5330f3056022f | CC BY | kenchoo / stokhuis | 18,438 / 21,100 | ⛔ 原作账号（AIUM2、nash808）已无法查询，原作许可**未核实** |
| 22 | 细纹斑马 | — | （没有物种专属模型） | — | — | — | — | ❌ 只找到头骨（laboratorinatura）；用 #30 的通用斑马当近缘模型，耳朵和花纹要另做 |
| 23 | 藏野驴 | Quaternius | Ultimate Animated Animal Pack（含 Donkey） | <https://quaternius.com/packs/ultimateanimatedanimals.html> | CC0（页面）/ QAL | Quaternius | 未核实 | 🟡 近缘模型（同属）；低多边形风格。包内 12 种动物，看预览图是：鹿 ×2、羊驼、狐狸、牛、公牛、哈士奇、驴、马、狼、柴犬 |
| 23 | 藏野驴 | Sketchfab | Animalia - Kiang (Male) | 0e61de3768b44b9eab5e985a702d2897 | CC BY | yoshi2024-2025 | 28,832 | ⛔ 来源存疑 |
| 23 | 藏野驴 | Sketchfab | Wild- Ass | 54b3933b79a84b608c6e498c072061a9 | CC BY | hendrikReyneke | 25,320 | ⛔ 同一天成批上传、没有简介，同批的斑马网格和 kenchoo 的 NC-ND 模型相同 |
| 24 | 棕熊 | Sketchfab | Brown Bear (animated) | 2f59c850fa4e46c08c3c72dd99a63c4b | CC BY | andrey. | 147,637 | ✅ 写实，手工制作 |
| 24 | 棕熊 | Sketchfab | Grizzly Bear Realistic Bear 3D Model | df9d941ee11a419db3a007775bdae832 | CC BY | criticaldamage9211 | 6,642 | ✅ 写实低模，标签 `noai` |
| 24 | 棕熊 | Sketchfab | Realistic Grizzly Bear - Game Ready Asset | 4657008bf6004ede9ff8e1f66e0df91f | CC BY | Hdjusj | 11,704 | 🟡 2026 年上传，是否 AI 生成未核实 |
| 24 | 棕熊 | Sketchfab | Grizzly Bear | 95baabcbc8634f6dace4376767a6024e | CC BY | freddy1231 | 34,060 | ⛔ 和 toro_ardido（游戏提取账号）的网格面数相同 |
| 25 | 马鹿 | Sketchfab | Realistic Animated Elk 3D Model | 787834f9caa2474d9f1814b807c072d7 | CC BY | WildMesh_3D | 7,886 | ✅ 简介写「use it in personal or commercial projects」；注意同一作者的「DEMO FREE」系列是 **NC**，不能用 |
| 25 | 马鹿 | Sketchfab | Elk | 9fdefa464e9044dca5fb5ce5d2aad4dd | CC BY | asik | 63,556 | ✅ 素模 |
| 25 | 马鹿 | Sketchfab | Red Elk | b5320822d040413c9ad6eab637e9dde0 | CC BY | rmark | 172,567 | ⛔ 是德州岩画扫描，不是动物 |
| 26 | 羚牛 | — | （没找到） | — | — | — | — | ❌ `takin`、`takin animal`、`budorcas` 都没有动物结果 |
| 27 | 麝牛 | Sketchfab | Muskox_ Loop (3) | de9e92409d0c482fbfd7e33160bf25c9 | CC BY | bojan6 | 5,460 | 🟡 低模，没有简介；同作者还有「Muskox_Loop (4)」e4408d48a3c24bbc86a2067e8d29cbdf（4,964 面） |
| 28 | 紫羚羊 | Sketchfab | African Bongo / Javan Bongo | c42a6b25b4254589b007c5bc0d0978ee / 06be47c75ff740b1a812f5138c79268f | CC BY | yoshi2024-2025 | 13,964 / 20,948 | ⛔ 来源存疑。缺口 |
| 29 | 山斑马 | — | （没有物种专属模型） | — | — | — | — | ❌ 用 #30 当近缘模型 |
| 30 | 平原斑马 | Sketchfab | Zebra | 3d6e29c0abc34c1d8e29c7939ee10238 | CC BY | micsir | 167,270 | 🟡 写实，没有简介，原创性未核实 |
| 30 | 平原斑马 | Sketchfab | Zebra | bd7258ee007b4e0fb521abb74bfa99d0 | CC BY | dirdim（Direct Dimensions） | 15,200 | 🟡 摄影测量，但**是幼驹**，比例不对；缩略图带公司水印 |
| 30 | 平原斑马 | Sketchfab | Plain Zebra | ff2875fb1a5b4771805a5fd35c8fe7bb | CC BY | gentryhsEAST | 16,212 | 🟡 学生作品（Digital Nature Museum），没有贴图，偏卡通 |
| 30 | 平原斑马 | Sketchfab | Zebra | 2306328d44b942efb16516cd6083e245 | CC BY | victorberdugo1 | 8,741 | ⛔ 这位上传者的「Elephant」和 onderonvermez 2016 年的模型网格相同，有转传前科 |
| 30 | 平原斑马 | Sketchfab | Zebra | bfd30bbd45894e7593da72a38df1066d | CC BY | Stephengury | 4,478 | ⛔ 是《马达加斯加》的 Marty |
| — | 人体参照 | MPFB 2 | 自带基础网格（按 1.75 m 生成） | <https://github.com/makehumancommunity/mpfb2> | CC0（素材） | MakeHuman Community | 可调 | ✅ 首选；只用自带素材，另下载的素材包要逐个核 |
| — | 人体参照（备选） | Quaternius | Universal Base Characters | <https://quaternius.com/packs/universalbasecharacters.html> | CC0（页面）/ QAL | Quaternius | 未核实 | 🟡 有 Regular 比例的男女体型，偏风格化 |
| — | 人体参照（备选） | Sketchfab | Human Base Mesh - Male | f952c9629058485e964636536c8c91a9 | CC BY | Ryan.Carvalho | 7,910 | 🟡 素模，A-pose，要摆成站姿 |
| — | 人体参照（备选） | Sketchfab | Male Lowpoly Base Mesh | 44d9a06186fa4068a50ab421bfcc38b2 | CC BY | Ryan.Carvalho | 1,480 | 🟡 低模剪影 |

Sketchfab 上没有找到 CC0 的人体基础网格（`human base mesh`、`human scale reference`、`makehuman` 的 CC0 搜索都是 0 条或只有文物）。

## 4. 缺口兜底方案

按优先级排：

1. **近缘模型缩放（`PROXY MODEL`）**：用同属或同科模型，按数据表的肩高和体长**分轴缩放**，不能等比缩放，否则体型会失真。卡上标黄色 `PROXY MODEL`，描述框写「body shape based on <近缘种> model」。建议的对应关系：

   | 缺口 | 近缘模型 | 差异提示（建模时补，或接受） |
   |---|---|---|
   | 非洲森林象 | #1 非洲草原象 | 耳朵更圆、象牙更直并朝下；体型小一圈 |
   | 爪哇犀 | #4 印度犀 | 同属；体型小、皮褶相似 |
   | 苏门答腊犀 | #3 白犀或 #4 | 双角、有体毛、最小的犀牛；差异最大，可以考虑剪影 |
   | 黑犀 | #3 白犀 | 钩状上唇、头抬得较高；角的比例要改 |
   | 印度野牛、爪哇野牛 | OGA Micket「Auroch」（CC0） | 印度野牛背脊隆起高；爪哇野牛体型更瘦 |
   | 欧洲野牛 | #13 美洲野牛 | 腿更长、前躯毛更少 |
   | 细纹斑马、山斑马 | #30 平原斑马 | 细纹斑马耳朵大而圆；路线 (b) 下花纹用程序化纹理区分 |
   | 藏野驴 | Quaternius Donkey | 同属；按肩高缩放 |
   | 野牦牛、野水牛（候选偏弱时） | 牛类 / Auroch | 野牦牛的长毛裙边要靠造型补 |

2. **自己建简化模型**：大羚羊、普通大羚羊、羚牛、紫羚羊这 4 种在开放库里完全没有。可以在 Blender 里用 Auroch 或牛的网格改角，或用基础几何体搭出剪影级模型。这是我们自己的作品，许可没有问题，但要花人工；卡上同样标 `PROXY MODEL`，或另标 `SIMPLIFIED`。
3. **简化剪影**：数据卡照常显示，但 3D 场景里用中性材质的平面或挤出剪影代替模型。兼容 `bible.md` 的比例机检（包围盒按数据设定）。
4. **不收这一条**（`bible.md` §0.3）：在 `topic.md` 记录，并重排名次。

本文件**不建议**用任何 AI 图生 3D 来兜底（见 §1 待拍板第 2 条）。

## 5. 风格路线评估：(a) 写实贴图混用 vs (b) 统一中性材质

| 维度 | (a) 写实贴图混用 | (b) 统一中性材质 + 物种主色 |
|---|---|---|
| 画风一致 | 差：同一画面里会同时出现 1,958 面的低模、270 万面的扫描、卡通渲染风、手绘贴图 | 好：统一的材质和光照把精度差异压平 |
| 能用的候选 | 只能用带好贴图的模型；素模（sciamop 美洲野牛、iznvm 白犀、asik 马鹿、MUVHN 雕塑）用不上 | 素模、扫描、低模、近缘模型都能用，候选池明显更大 |
| 近缘模型是否显眼 | 很显眼：用驴的贴图冒充藏野驴会误导观众 | 不显眼：体型差异由缩放体现，配合 `PROXY MODEL` 标即可 |
| 物种辨识 | 好（斑马、长颈鹿的花纹天然可见） | 斑马和长颈鹿会掉辨识度，要用程序化纹理补；其余物种靠剪影加主色就够 |
| 许可风险 | 贴图可能来自来源不明的照片（如 Smoothie 3D 用维基照片生成），要逐张核 | 原贴图全部弃用；网格仍按 CC BY 署名，注明「modified」 |
| 和 Vision 的关系 | 观感更「野生纪录片」 | 更贴合「一眼看出谁比谁大多少」：观众注意力在体型和比例上；同类尺度对比频道也多用简洁统一的渲染（MetaBallStudios 的具体材质做法本次没有逐期核实） |
| 制作量 | 每个模型要单独调 PBR、修贴图接缝 | 一套材质模板加 30 个主色值；脚本化程度高，渲染更快 |
| 许可前提 | ND 本就不收 | 要改材质，所以必须排除 ND（白名单已排除） |

**建议：(b)，即中性黏土 / 哑光材质 + 物种主色。** 例外是斑马（黑白条纹）和长颈鹿（网纹），用我们自己写的 Blender 程序化纹理表现；产出归我们所有，不涉及第三方贴图。犀牛、象、河马用灰色系的不同明度区分。
**落地前**：按 `bible.md` §3 的要求，取同一组 5 种（象、白犀、长颈鹿、斑马、棕熊）各渲一版 (a) 和 (b)，交给用户看图拍板。

**署名格式（CC BY 4.0 §3(a)）**：`"<Title>" by <Author> (<Sketchfab URL>), CC BY 4.0, modified (rescaled, retextured, reposed)`。二次创作链（例如 kenchoo ← Stephengury）两人都要列。animalanimator 还要求附 animalanimator.com 的对应页面链接。

## 6. 下一步（留给模型下载步骤）

1. 用户先拍板 §1 的两个待定项和 §5 的风格路线。
2. 对 🟡 条目下载前人工看一遍模型页（线框、贴图、评论区有没有人指出是盗用），结论写回本表。
3. 下载后在 `episodes/<期>/licenses.csv` 逐条登记；下载时再读一次 API 的许可字段（许可以下载当时为准）。
4. Poly Pizza 要么申请 API key（免费 key 是否附带条款未核实），要么由用户在浏览器里人工搜索，补查 Quaternius 等 CC0 动物包。

## 7. 实际查询过的 URL（2026-11-06）

**Sketchfab 公开搜索 API（共 190 条：第一轮 49 个检索词、第二轮 46 个检索词，都是 `type=models&downloadable=true&count=24`，`license` 分别为 `cc0` 和 `by`）**：完整列表见下方附录。

**Sketchfab 其他接口：**
- 许可定义：<https://api.sketchfab.com/v3/licenses>
- 模型详情：`https://api.sketchfab.com/v3/models/<uid>`。§3 表中列出的每个 Sketchfab uid 都查过；另外查过 33ce37106a24493ba4a6a6e2a9433bb6、c0e0422d554a437083a306654977d1a6、4b78a5ed77b84305a588194e1f6e2ef5、cb15c03755394a71b57e6230daea574e、f57057ad0c2044ec88c9ba5ab5c18a41，以及 104bced5a4af49e091f63136a39ff2fe（rt699448，标签含 AI）。
- 按上传者列模型：`https://api.sketchfab.com/v3/search?type=models&user=<username>&count=24`。查过的上传者：animalanimator、WildMesh_3D、Sengchor、andrey.、cmp_innovation_studio、Stephengury、kenchoo、sdpm、AIUM2（0 条，账号不可查）、thunders14、nash808（0 条）、marcusjt、MUVHN、cosmical、gentryhsEAST、Mehrus、absol_cg、BlueMesh、yoshi2024-2025、planeta-elefante、Gotta_go_evil_Fast、asik、bojan6、iznvm、larycim、sciamop、onderonvermez、psk98077、Joseph.AD。

**其他来源：**
- Poly Pizza：<https://poly.pizza/search/elephant>（curl 和浏览器都停在 Cloudflare 人机验证页）、<https://api.poly.pizza/v1.1/search/elephant>（401）
- Quaternius：<https://quaternius.com/packs/ultimateanimatedanimals.html>、<https://quaternius.com/assets/images/fullres/ultimateanimatedanimal.jpg>（预览图，用来认物种）、<https://quaternius.com/license.html>、<https://quaternius.com/packs/universalbasecharacters.html>
- Poly Haven：<https://api.polyhaven.com/assets?t=models>
- Smithsonian：<https://api.si.edu/openaccess/api/v1.0/search?q=elephant%20AND%20online_media_type:%223D%20Images%22&rows=20&api_key=DEMO_KEY>（0 条）；3D API `https://3d-api.si.edu/api/v1.0/content/file/search?q=<词>&rows=50`，词为 elephant、rhinoceros、hippopotamus、giraffe、bison、bear、zebra、moose、buffalo、human
- NIH 3D：<https://3d.nih.gov/search?q=elephant>（404）
- MorphoSource：<https://www.morphosource.org/catalog/media?q=elephant>（拒绝访问）
- MPFB：<https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.ASSETS.md>、<https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.CODE.md>
- OpenGameArt 高级搜索：`https://opengameart.org/art-search-advanced?keys=<词>&field_art_type_tid[]=10&sort_by=count&sort_order=DESC&items_per_page=48`，词为 elephant、rhino、rhinoceros、hippo、giraffe、bison、buffalo、yak、zebra、moose、polar bear、bear、elk、deer、antelope、eland、musk ox、donkey、cow、bull；作者检索 `keys=Micket`；条目页见 §3 表

### 附录：Sketchfab 搜索 URL 全表

```text
https://api.sketchfab.com/v3/search?type=models&q=african+elephant&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=african+elephant&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=elephant&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=elephant&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=asian+elephant&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=asian+elephant&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=forest+elephant&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=forest+elephant&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=white+rhino&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=white+rhino&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhino&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhino&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=indian+rhinoceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=indian+rhinoceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=javan+rhino&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=javan+rhino&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=black+rhino&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=black+rhino&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=sumatran+rhino&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=sumatran+rhino&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippopotamus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippopotamus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=giraffe&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=giraffe&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=gaur&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=gaur&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=yak&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=yak&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=water+buffalo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=water+buffalo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=buffalo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=buffalo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=american+bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=american+bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=european+bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=european+bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=wisent&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=wisent&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=cape+buffalo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=cape+buffalo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=african+buffalo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=african+buffalo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=banteng&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=banteng&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=eland&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=eland&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=moose&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=moose&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=polar+bear&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=polar+bear&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=zebra&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=zebra&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=grevy+zebra&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=grevy+zebra&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=kiang&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=kiang&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=wild+ass&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=wild+ass&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=onager&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=onager&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=donkey&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=donkey&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=brown+bear&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=brown+bear&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=grizzly+bear&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=grizzly+bear&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=elk&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=elk&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=wapiti&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=wapiti&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=red+deer&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=red+deer&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=takin&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=takin&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=muskox&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=muskox&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=musk+ox&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=musk+ox&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bongo&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bongo&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=antelope&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=antelope&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=cow&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=cow&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bull&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bull&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+base+mesh&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+base+mesh&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+scale+reference&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+scale+reference&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=man+realistic&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=man+realistic&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bongo+antelope&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bongo+antelope&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=giant+eland&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=giant+eland&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=common+eland&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=common+eland&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=takin+animal&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=takin+animal&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=budorcas&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=budorcas&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=kiang&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=kiang&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=tibetan+wild+ass&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=tibetan+wild+ass&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=yak+animal&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=yak+animal&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=wild+yak&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=wild+yak&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=javan+rhinoceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=javan+rhinoceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros+sondaicus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros+sondaicus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=sumatran+rhinoceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=sumatran+rhinoceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=banteng+cattle&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=banteng+cattle&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bos+javanicus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bos+javanicus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=gaur+bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=gaur+bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=indian+bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=indian+bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=seladang&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=seladang&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bubalus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bubalus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=arni&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=arni&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=musk+ox+animal&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=musk+ox+animal&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=ovibos&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=ovibos&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=wapiti&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=wapiti&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=cervus+canadensis&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=cervus+canadensis&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=mountain+zebra&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=mountain+zebra&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=plains+zebra&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=plains+zebra&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=grevy&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=grevy&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=giraffa&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=giraffa&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=loxodonta&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=loxodonta&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=elephas+maximus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=elephas+maximus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=diceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=diceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=ceratotherium&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=ceratotherium&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros+unicornis&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=rhinoceros+unicornis&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=greater+one-horned+rhinoceros&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=greater+one-horned+rhinoceros&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippopotamus+amphibius&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=hippopotamus+amphibius&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=bison+bison&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=bison+bison&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=syncerus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=syncerus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=tragelaphus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=tragelaphus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=alces&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=alces&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=ursus+maritimus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=ursus+maritimus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=ursus+arctos&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=ursus+arctos&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=equus&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=equus&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=taxidermy&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=taxidermy&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=stuffed+animal+museum&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=stuffed+animal+museum&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=makehuman&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=makehuman&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+body+scan&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=human+body+scan&downloadable=true&license=by&count=24
https://api.sketchfab.com/v3/search?type=models&q=person+3d+scan&downloadable=true&license=cc0&count=24
https://api.sketchfab.com/v3/search?type=models&q=person+3d+scan&downloadable=true&license=by&count=24
```
