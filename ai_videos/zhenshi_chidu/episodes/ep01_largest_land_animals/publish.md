# publish draft · ep01_largest_land_animals（真实尺度 · True Scale）

> 代理起草（2026-11-07，2026-11-08 按第 3 版更新，加中文版、各平台文案与封面）。
> 第 3 版：AI 写实图抠像 + 精细草原场景。中英两版画面、时长、配乐完全相同，只差叠加文字（片中无旁白）。
> 归属：排行榜频道的子系列（播放列表「True Scale」区分，README 已定 #5）。
> 发布方式：
> - 英文版发 YouTube 与 TikTok。YouTube 已于 2026-11-08 经 API 传成**私享**：<https://youtu.be/gXIryNL5fp4>，Studio <https://studio.youtube.com/video/gXIryNL5fp4/edit>，记录在 `uploads.json`。公开由用户在 Studio 亲手点。
> - 中文版发国内平台（抖音、快手、B站、视频号、小红书），由用户手动上传。
> - 与排行榜频道一致。

## 文件

| | 英文版 | 中文版 |
|---|---|---|
| 成片（4:08，1920×1080 30fps，−14.1 LUFS） | `render/ep_master.mp4` | `render/ep_master_zh.mp4` |
| 置顶评论（出处） | `_build/pinned_comment.txt`（含链接） | `_build/pinned_comment_zh.txt`（无外链） |
| 封面 | `render/covers/en/` | `render/covers/zh/` |

## 封面对照

每种语言两种构图：
- **A**：冠军长颈鹿 + 1.75 m 人，推荐。
- **B**：30 只全体合影 + 人。

由 `_tools/thumbnail.py` 从 Blender 高清静帧合成，都标 AI IMAGE / AI 生成图：横版在右上，竖版在安全区右下。竖版 3:4 的文字都在居中 1:1 / 9:16 裁切的安全区内。

| 平台 | 用哪张（横版 A 换成 B 即另一构图；竖版只有 A） | 尺寸 |
|---|---|---|
| YouTube | `covers/en/A_yt.jpg`（= `render/thumb_A.jpg`，已设到上传的视频上） | 1280×720 |
| TikTok | `covers/en/A_3x4.jpg` | 1080×1440 |
| B站 | `covers/zh/A_16x9.jpg`；要求 4:3 时用 `A_4x3.jpg` | 1920×1080 / 1440×1080 |
| 抖音 | 竖封面 `covers/zh/A_3x4.jpg`，横封面 `covers/zh/A_4x3.jpg` | 1080×1440 / 1440×1080 |
| 快手 | `covers/zh/A_3x4.jpg`；横版位用 `A_16x9.jpg` | 1080×1440 |
| 视频号 | 竖封面 `covers/zh/A_3x4.jpg`，横封面 `covers/zh/A_16x9.jpg` | 1080×1440 / 1920×1080 |
| 小红书 | `covers/zh/A_3x4.jpg` | 1080×1440 |

---

# 英文版（English）

## Title

The 30 Largest Land Animals Ranked by Height | True Scale Size Comparison
（73 字符）

备选：How Tall Are the World's Largest Land Animals? True Scale Size Comparison

## Description

```text
The 30 largest land animals on Earth, lined up from smallest to tallest at their true size, each one next to a 1.75 m (5 ft 9 in) man.
Ranked by typical shoulder height (adult males where data allow). Every number on screen has a source (full list with links in the pinned comment).

Chapters:
0:00 Intro: #30 Takin – #21 Grévy's Zebra
1:19 =19 Elk – #11 American Bison
2:29 Top 10
3:01 Top 5 and the tallest
3:43 All 30 together & sources

How we built it:
- Each animal is scaled by script so its shoulder (the yellow line) matches the number on the card; a script checks every one to within 2%.
- The 1.75 m man stands at the same distance from the camera as each animal, so perspective does not change their relative size.
- All 30 animals and the man are AI-generated images made for this video (marked "AI IMAGE"): a typical adult of each species, side view. Coat details are illustrative; the sizes are not.
- Landscape: the distant savanna backdrop and the acacias are AI-generated images; the 3D grass, rocks and lighting are from Poly Haven (CC0).

Notes on the data:
- Same 30 species as our weight ranking (heaviest wild land animals, typical adult male). Re-ranked here by shoulder height, so the order changes a lot: the hippo is 6th by weight but 18th by height; the giraffe is 8th by weight but 1st by height.
- Where sources give a range, we use its midpoint. Where only mixed-sex measurements exist, the card says "adults, both sexes" (11 species). Ties share a rank.
- Estimates (≈): muskox (sources disagree), brown bear (scaled from measured Kamchatka males).
- Polar bear (1.45 m, both sexes) and muskox (≈1.45 m) sit at the low end of published figures for big males (about 1.5–1.6 m). The gaur figure (1.88 m) is Nowak 1999 as quoted by Wikipedia; the Asian Wild Cattle Specialist Group gives 1.5–2.2 m.
- Height to the top of the head depends on how the head is held: the Handbook of the Mammals of the World gives 4.5–6.0 m for giraffes (both sexes); our giraffe image reaches about 4.6 m.

Main shoulder-height sources (every animal's source and link is in the pinned comment):
Larramendi 2016 (Acta Palaeontologica Polonica) · Handbook of the Mammals of the World (Lynx, 2009/2011) · San Diego Zoo Wildlife Alliance Library · Animal Diversity Web · Mammalian Species (ASM) accounts · Krasińska & Krasiński 2002 · Seryodkin et al. 2016 · IUCN SSC Asian Wild Cattle Specialist Group · Nowak 1999

Music: original instrumental generated for this channel with Suno (job b60957b7, clips 09516232 + 813a380a).
Animals and the 1.75 m man: AI-generated images made for this video. Sky and landscape: Poly Haven HDRIs "Mpumalanga Veld" (Greg Zaal) and "Plains Sunset" (Dimitrios Savva, Jarod Guest); ground texture "Grass Ground" (Charlotte Baglioni); 3D grass and rocks "Grass Medium 01/02", "Grass Bermuda 01", "Moon Rock 02" (Rico Cilliers, Rob Tuytel, Greg Zaal, Jenelle van Heerden); all CC0. Savanna backdrop and acacias: AI-generated for this video. Font: Inter (SIL OFL 1.1).

#TrueScale #SizeComparison #LargestAnimals #Animals
```

## Tags

largest land animals, animal size comparison, true scale, shoulder height, tallest animals, giraffe, elephant, animals ranked by size

## Comment 1（置顶）（2837 字符）

由 `_tools/make_ep01_meta.py` 生成（`_build/pinned_comment.txt`），出处与卡上简称逐条对应。

```text
Shoulder-height sources (typical adults; males where data allow). Rank · animal · value: source — link (1/2)
#1 Giraffe 3.31 m: San Diego Zoo Wildlife Alliance Library, giraffe fact sheet (Ciofolo & Le Pendu 2013, Mammals of Africa; n=15-18) — https://ielc.libguides.com/sdzg/factsheets/giraffes/characteristics
#2 African Bush Elephant 3.20 m: Larramendi 2016, Acta Palaeontologica Polonica 61(3):537-574 — https://www.app.pan.pl/archive/published/app61/app001362014.pdf
#3 Asian Elephant 2.75 m: Larramendi 2016, Acta Palaeontologica Polonica 61(3):537-574 — https://www.app.pan.pl/archive/published/app61/app001362014.pdf
#4 African Forest Elephant 2.20 m: Larramendi 2016, Acta Palaeontologica Polonica 61(3):537-574 — https://www.app.pan.pl/archive/published/app61/app001362014.pdf
#5 Moose 2.00 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Alces alces (Cervidae) — https://tb.plazi.org/GgServer/xhtml/03A087C4FFDDFFDCFFB4FE48EE7DF8A4
#6 Wild Yak 1.89 m: Leslie & Schaller 2009, Mammalian Species 836 (citing Schaller 1998) — https://www.mammalogy.org/uploads/Leslie%20and%20Schaller%202009.pdf
#7 Gaur 1.88 m: Nowak 1999, Walker's Mammals of the World (via Wikipedia 'Gaur') — https://en.wikipedia.org/wiki/Gaur
#8 White Rhinoceros 1.78 m: Handbook of the Mammals of the World vol. 2 (2011), Rhinocerotidae, C. simum treatment via Plazi — https://tb.plazi.org/GgServer/xhtml/5E3FD96DFFEC721A4C39FE6BF7E1742B
=9 Indian Rhinoceros 1.75 m: Laurie, Lang & Groves 1983, Mammalian Species 211 (Rhinoceros unicornis) — http://web.archive.org/web/2016id_/http://www.science.smith.edu/msi/pdf/i0076-3519-211-01-0001.pdf
=9 Wild Water Buffalo 1.75 m: IUCN SSC Asian Wild Cattle Specialist Group – Wild water buffalo — https://www.asianwildcattle.org/wild-water-buffalo.html
#11 American Bison 1.74 m: Krasińska & Krasiński 2002, Acta Theriologica 47:85–106, Table 8 (American bison data from Halloran 1960, Wichita Mountains) — https://ibs.bialowieza.pl/g2/pdf/1357.pdf
#12 European Bison 1.72 m: Krasińska & Krasiński 2002, Acta Theriologica 47:85–106, Table 3 — https://ibs.bialowieza.pl/g2/pdf/1357.pdf
#13 Giant Eland 1.63 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Taurotragus derbianus — https://tb.plazi.org/GgServer/xhtml/03F507139965FFDF064CF444F8BAF825
#14 African Buffalo 1.62 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Syncerus caffer — https://tb.plazi.org/GgServer/xhtml/03F507139945FFFF0375F62EF68AF855
=15 Javan Rhinoceros 1.60 m: Handbook of the Mammals of the World vol. 2 (2011), Rhinocerotidae, R. sondaicus treatment via Plazi — https://tb.plazi.org/GgServer/xhtml/5E3FD96DFFEA721D493EF4A8FE6070D9
```

## Comment 1 的回复（2681 字符）

```text
(2/2)
=15 Banteng 1.60 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Bos javanicus — https://tb.plazi.org/GgServer/xhtml/03F507139948FFF303ABFE8AF6C9FA2B
#17 Common Eland 1.59 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Taurotragus oryx — https://tb.plazi.org/GgServer/xhtml/03F507139965FFDE0375FE20F5EBF4FF
#18 Hippopotamus 1.58 m: San Diego Zoo Wildlife Alliance Library, hippopotamus fact sheet (Kingdon 1979) — https://ielc.libguides.com/sdzg/factsheets/hippopotamus/characteristics
=19 Black Rhinoceros 1.55 m: Hillman-Smith & Groves 1994, Mammalian Species 455 (Diceros bicornis) — http://web.archive.org/web/2016id_/http://www.science.smith.edu/msi/pdf/i0076-3519-455-01-0001.pdf
=19 Elk (Wapiti) 1.55 m: Handbook of the Mammals of the World vol.2 (2011) Cervidae via Plazi — https://tb.plazi.org/GgServer/xhtml/03A087C4FFD5FFD4FF60FA22EFD5F46A
#21 Grévy's Zebra 1.50 m: Handbook of the Mammals of the World vol.2 (2011) Equidae via Plazi — https://tb.plazi.org/GgServer/xhtml/03B0E520E8155860FF1AAC47ECEDF4E7
=22 Polar Bear 1.45 m: DeMaster & Stirling 1981, Mammalian Species 145 (ASM), PDF hosted by NOAA SWFSC — https://swfsc-publications.fisheries.noaa.gov/publications/CR/1981/8111.PDF
=22 Muskox ≈1.45 m: ADW - Ovibos moschatus — https://animaldiversity.org/accounts/Ovibos_moschatus/ ; Alaska Dept. of Fish & Game - Muskox species profile — https://www.adfg.alaska.gov/index.cfm?adfg=muskox.printerfriendly
#24 Mountain Zebra 1.44 m: ADW - Equus zebra (references Penzhorn 1988) — https://animaldiversity.org/accounts/Equus_zebra/
#25 Kiang 1.40 m: ADW - Equus kiang — https://animaldiversity.org/accounts/Equus_kiang/
#26 Brown Bear ≈1.35 m: Seryodkin, Zhakov & Paczkowski 2016, Morphometric parameters of brown bears captured for research in Kamchatka (Far Eastern Agrarian Herald 3(39)) — https://vestnik.dalgau.ru/upload/iblock/1fa/Seryodkin.pdf
#27 Plains Zebra 1.30 m: SDZWA Library plains zebra fact sheet — https://ielc.libguides.com/sdzg/factsheets/plains_zebra/characteristics
=28 Sumatran Rhinoceros 1.25 m: Wilson & Mittermeier (eds) 2011, Handbook of the Mammals of the World Vol. 2 Hoofed Mammals, via Plazi treatment – Dicerorhinus sumatrensis — https://tb.plazi.org/GgServer/xhtml/5E3FD96DFFEB721E49E6FE2BF88F79D6
=28 Bongo 1.25 m: Handbook of the Mammals of the World vol.2 (2011) Bovidae via Plazi — https://tb.plazi.org/GgServer/xhtml/03F50713996EFFD606D4FE81FB19F2FD
#30 Takin 1.20 m: ADW - Budorcas taxicolor (citing Parker 1989; Nowak 1999) — https://animaldiversity.org/accounts/Budorcas_taxicolor/
```

## TikTok

Cover: `covers/en/A_3x4.jpg`. Turn on the "AI-generated content" label.

```text
The 30 largest land animals, lined up at their true size next to a 1.75 m man. Ranked by shoulder height.
Every number on screen is sourced; full sources are in the YouTube description.
The animals and the man are AI-generated images, scaled by script to real measurements.

Which one surprised you? Tell us in the comments!

#truescale #sizecomparison #animals #giraffe #elephant #learnontiktok
```

---

# 中文版（国内平台）

各平台都不放外链。AI 生成内容标识：**本片含 AI 生成内容**（动物与参照人都是 AI 生成的图像），每个平台上传页都要勾选。

## 抖音 / 快手

标题（17 字，抖音 ≤30）：

```text
30种陆地巨兽按肩高排名｜真实比例
```

作品描述（153 字）：

```text
30种最大的陆地动物，按真实比例从矮到高排成一列，每一只旁边都站着一个1.75 m的人。
按典型肩高排名，画面上每个数字都有出处，见置顶评论。
动物和人都是AI生成的图像，尺寸按资料逐只缩放。
第1名你猜对了吗？哪一只最出乎你意料？评论区聊聊。

#真实尺度 #大小对比 #动物 #涨知识 #科普 #长颈鹿
```

封面：竖 `covers/zh/A_3x4.jpg`，横 `covers/zh/A_4x3.jpg`。

## B站

标题（26 字，≤80）：

```text
最大的 30 种陆地动物按肩高排名｜真实比例大小对比
```

- **分区**：知识 → 科学科普。
- **类型**：自制。
- **标签**（10 个，≤10）：陆地动物, 动物大小对比, 真实比例, 肩高, 最高的动物, 长颈鹿, 大象, 动物排行, 科普, 涨知识。

简介（1512 字，≤2000）：

```text
地球上最大的 30 种陆地动物，从矮到高按真实比例排成一列，每一只旁边都站着一个 1.75 m 的人。
按典型肩高排名（有数据时取成年雄性）。画面上每个数字都有出处，逐只出处见置顶评论。

章节：
0:00 开场：#30 扭角羚 – #21 细纹斑马
1:19 =19 北美马鹿 – #11 美洲野牛
2:29 前十
3:01 前五与冠军
3:43 30 种全体合影与资料来源

怎么做的：
- 每只动物都由脚本缩放，让肩部（黄线）正好等于卡上的数值；每一只都经脚本核对，误差在 2% 以内。
- 1.75 m 的人和每只动物离镜头一样远，透视不会改变两者的相对大小。
- 30 只动物和参照人都是为本片 AI 生成的图像（片中标「AI 生成图」），每种取典型成年个体的侧面。毛色细节只作示意，尺寸是真实的。
- 场景：远处的草原背景和金合欢是 AI 生成的图像；3D 草、石块和光照来自 Poly Haven（CC0）。

关于数据：
- 和我们的体重排行是同一份 30 种名单（最重的野生陆地动物，典型成年雄性），这里改按肩高重新排名，名次变化很大：河马按体重第 6，按肩高只排第 18；长颈鹿按体重第 8，按肩高第 1。
- 资料给出范围时取中值。只有雌雄合计数据的，卡上写「成年个体（雌雄合计）」（共 11 种）。并列的共享同一名次。
- 估计值（≈）：麝牛（资料有分歧）、棕熊（按堪察加实测雄性换算）。
- 北极熊（1.45 m，雌雄合计）和麝牛（≈1.45 m）处在已发表数据的低端，大型雄性约 1.5–1.6 m。印度野牛 1.88 m 出自 Nowak 1999（经维基百科转引）；IUCN 亚洲野牛专家组给出 1.5–2.2 m。
- 头顶高度取决于头怎么抬：《世界哺乳动物手册》给出长颈鹿高 4.5–6.0 m（雌雄合计），片中长颈鹿头顶约 4.6 m。
- 卡上「人高的 N 倍」= 肩高 ÷ 1.75 m。

主要肩高资料（每只动物的出处见置顶评论）：
Larramendi 2016（Acta Palaeontologica Polonica）· Handbook of the Mammals of the World（Lynx，2009/2011）· 圣地亚哥动物园野生动物联盟资料库 · Animal Diversity Web · Mammalian Species（美国哺乳动物学会）· Krasińska & Krasiński 2002 · Seryodkin et al. 2016 · IUCN SSC 亚洲野牛专家组 · Nowak 1999

配乐：本频道用 Suno 生成的原创纯音乐（job b60957b7，clips 09516232 + 813a380a）。
动物与 1.75 m 的人：为本片 AI 生成的图像。天空与场景：Poly Haven HDRI「Mpumalanga Veld」（Greg Zaal）、「Plains Sunset」（Dimitrios Savva、Jarod Guest）；地面贴图「Grass Ground」（Charlotte Baglioni）；3D 草与石块「Grass Medium 01/02」「Grass Bermuda 01」「Moon Rock 02」（Rico Cilliers、Rob Tuytel、Greg Zaal、Jenelle van Heerden）；均为 CC0。草原远景与金合欢：为本片 AI 生成。字体：Noto Sans SC（SIL OFL 1.1）。

#真实尺度 #大小对比 #动物 #科普
```

封面：`covers/zh/A_16x9.jpg`（要求 4:3 时用 `A_4x3.jpg`）。

置顶评论（946 字，B站单条 ≤1000），发布后发在评论区并置顶：

```text
肩高出处（典型成年个体，有数据时取雄性；资料给出范围时取中值）。名次 · 动物 · 肩高：出处
#1 长颈鹿 3.31 m：Ciofolo & Le Pendu 2013 (via SDZWA)
#2 非洲草原象 3.20 m：Larramendi 2016
#3 亚洲象 2.75 m：Larramendi 2016
#4 非洲森林象 2.20 m：Larramendi 2016
#5 驼鹿 2.00 m：Handbook of the Mammals of the World
#6 野牦牛 1.89 m：Leslie & Schaller 2009
#7 印度野牛 1.88 m：Nowak 1999
#8 白犀 1.78 m：Handbook of the Mammals of the World
=9 印度犀 1.75 m：Laurie, Lang & Groves 1983
=9 野水牛 1.75 m：IUCN SSC Asian Wild Cattle SG
#11 美洲野牛 1.74 m：Halloran 1960 (via Krasińska 2002)
#12 欧洲野牛 1.72 m：Krasińska & Krasiński 2002
#13 德氏大羚羊 1.63 m：Handbook of the Mammals of the World
#14 非洲水牛 1.62 m：Handbook of the Mammals of the World
=15 爪哇犀 1.60 m：Handbook of the Mammals of the World
=15 爪哇野牛 1.60 m：Handbook of the Mammals of the World
#17 普通大羚羊 1.59 m：Handbook of the Mammals of the World
#18 河马 1.58 m：San Diego Zoo Wildlife Alliance
=19 黑犀 1.55 m：Hillman-Smith & Groves 1994
=19 北美马鹿 1.55 m：Handbook of the Mammals of the World
（1/2）
```

置顶评论的回复（448 字）：

```text
#21 细纹斑马 1.50 m：Handbook of the Mammals of the World
=22 北极熊 1.45 m：DeMaster & Stirling 1981
=22 麝牛 ≈1.45 m：ADW / Alaska Dept. of Fish & Game
#24 山斑马 1.44 m：Penzhorn 1988 (via ADW)
#25 藏野驴 1.40 m：Animal Diversity Web
#26 棕熊 ≈1.35 m：Seryodkin et al. 2016
#27 平原斑马 1.30 m：San Diego Zoo Wildlife Alliance
=28 苏门答腊犀 1.25 m：Handbook of the Mammals of the World
=28 紫羚 1.25 m：Handbook of the Mammals of the World
#30 扭角羚 1.20 m：Animal Diversity Web
（2/2）
```

## 视频号

```text
30种最大的陆地动物，按真实比例从矮到高排成一列，每一只旁边都站着一个1.75 m的人。按典型肩高排名，每个数字都有出处。
动物和人都是AI生成的图像，尺寸按资料逐只缩放。

#真实尺度 #大小对比 #动物 #涨知识
```

封面：竖 `covers/zh/A_3x4.jpg`，横 `covers/zh/A_16x9.jpg`。

## 小红书

标题（10 字，≤20）：30种巨兽和人比身高

```text
30种最大的陆地动物，按真实比例站成一排，每只旁边都有一个1.75 m的人 🦒

· 按典型肩高排名（有数据时取成年雄性），每个数字都有出处
· 长颈鹿肩高3.31 m，第1；河马按体重排第6，按肩高只排第18
· 动物和人都是AI生成的图像，尺寸按资料逐只缩放

你觉得哪一只最出乎意料？

#真实尺度 #动物 #涨知识 #科普 #大小对比 #长颈鹿
```

封面：`covers/zh/A_3x4.jpg`。

---

## Upload checklist（两版都适用）

- [ ] 用户看完成片并认可（审核项见 `review_for_user.md`；中文版另看一遍卡片文字）
- [ ] 中文版发国内平台（上面各节）；中文字烧在画面里，不能当英文视频的字幕或音轨
- [ ] 国内平台：简介、评论都不放外链
- [ ] 播放列表：True Scale（中文版用对应的中文播放列表）
- [ ] YouTube「Altered or synthetic content」：**勾选**。动物与参照人都是 AI 生成的写实图像，片中有标注，描述已写明。在其他平台也按该平台的 AI 内容声明勾选
- [ ] 配乐不登记 Content ID；被误认领时用 `ai_videos/zhenshi_chidu/request_log.md` 的 Suno 记录申诉
- [x] YouTube 已传私享，标题、描述、标签、AI 合成内容声明、封面 A 都已设好
- [ ] 你在 Studio 检查后亲手公开；公开后跑 `python ai_videos/zhenshi_chidu/_tools/upload.py comments ai_videos/zhenshi_chidu/episodes/ep01_largest_land_animals` 发出处评论，再在 Studio 把 Comment 1 置顶
- [ ] 封面：默认 A（冠军 + 人）；换 B 在 Studio 里传 `covers/en/B_yt.jpg`。各平台见「封面对照」
- [ ] 片尾推荐位（End screen）：放在最后 15 s 的来源卡上（3:53–4:08），不遮来源文字的右下角
