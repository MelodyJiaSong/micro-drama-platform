---
worker_id: researcher-w6-refs
stage: 0
role: researcher
angle: reference-image-library
status: complete
blockers: []
confidence: high
---

# W6 · 参考图库（sk3 伦敦 · 1666-09-01 · 大火前一夜）

> 本文件是 `sk3/0_research/dossier.md` **第 15 节（参考来源 / 参考图库）** 的底稿，由 parent 合并。
> 末尾另有 **§15b image-to-image 可用性评估**——逐资产回答「这组图能不能直接当 img2img 输入」，是阶段 2 建卡的直接依据。
>
> **本站图库的地位与别站不同。** 用户 2026-09-18 定调：对标 Chloe VS History，**把公版历史图 image-to-image 转成照片级画面、保持原图完整性**，
> 而不是纯文字凭空生成（「信任来自史料」）。所以下面这 130 张**不是辅助材料，是画面的原始素材**。
> 这条与仓库现行 `ai_video.md` rule 18.1 直接冲突，见 §4——**需要一条明确的 divergence note，不能默默跑**。

---

## 0. 结论速览

- **实际下载 130 张，9 个资产全部达标（≥8），共 268 MB**，落盘在 `ai_videos/shikong_lvxing/sk3/0_research/refs/{asset_key}/ref/`，
  每个资产同目录一份 `refs.md`（`ref_fetch.py` 生成，字段合 rule 17.4：`ref_id / file / source_url / collection / accession / date / license / evidences / use`）。
- **另存一份原始底片**：`0_research/masters/hollar_1647_longview_master_28661x5560.jpg`（76.4 MB，28661×5560，未经任何缩放与补边）——见 §5 ②。
- **许可**：CC0 42 · Public domain 81 · CC BY 4.0 2 · CC BY-SA 4.0 2 · CC BY-SA 3.0 1 · CC BY 2.0 1 · No restrictions 1（已标⛔）。
  **127/130 可直接入画**；3 张 CC BY-SA 现代照片建议只进 prompt（§3 ②）。
- **`evidences:` 全部指向 sk1..w5 已注册的真实 `fact_id`**（`london1666.*`，共引用 37 个），`tools/facts_registry.py` 口径下零悬空引用。
- **机检**：130 条 `refs.md` 条目与盘上文件一一对应，无重号、无孤儿、无幽灵条目。
- **发现两个工具问题**（一个是 `ref_fetch.py` 的真 bug），见 §5。

### 一手底本（T0，本站画面的真正来源）

| 底本 | 年代 | 用于 |
|---|---|---|
| **Wenceslaus Hollar,《Long View of London from Bankside》** | 1647 | 片头航拍长镜 + 全城白模的双重依据（**最高优先**） |
| **Hollar,《A True and Exact Prospect of the Famous Citty of London》(火前/火后双联)** | 1666 | 火前天际线 + 片尾火后对照 |
| **Hollar 为 Dugdale《The History of St Pauls Cathedral》所作铜版组图** | 1658 | 旧圣保罗 1666 年状态（无尖顶 + Inigo Jones 门廊）逐立面 |
| **Hollar,《Byrsa Londinensis vulgo the Royal Exchange》** | c.1647 | 皇家交易所火前唯一一手内院图 |
| **Claes Van Visscher,《London panorama》** | 1616 | 旧伦敦桥满载房屋形态的最清晰一手 |
| **Claude de Jongh,《View of London Bridge》** | 1632 / 1630 | 旧伦敦桥油画（有明暗层次，img2img 首选） |
| **Hollar,《Ornatus Muliebris Anglicanus》/《Theatrum Mulierum》** | 1638–44 | 英国女装分阶层图录（Rijksmuseum CC0） |
| **Marcellus Laroon,《The Cryes of the City of London》** | 1687–88 | 街头行当 + 平民衣着（火后 20 年，`london1666.work.030` 已注册） |
| **Abraham Hondius,《The Frozen Thames, looking eastwards towards Old London Bridge》** | 1677 | 河面人群 + 桥体，油画质感 |
| **Faithorne & Newcourt 伦敦实测地图** | 1658 | 火前街道骨架 |

### 收藏机构分布

University of Toronto Wenceslaus Hollar Digital Collection 21 · Yale Center for British Art 6（CC0）·
Rijksmuseum（经 Commons）约 40（CC0）· The Met Open Access 若干（CC0）· Wellcome Collection 2（CC BY 4.0）·
British Library Mechanical Curator 3 · Google Art Project 3 · 其余为 Commons 个人上传 / 扫描件。

---

## 1. 达标总表

| asset_key | 资产 | 张数 | 其中 CC0/PD | 达标（≥8） |
|---|---|---|---|---|
| `bg0_london_panorama` | 整城全景（最高优先） | **12** | 11 | ✅ 达标 |
| `bg1_london_bridge` | 旧伦敦桥 | **11** | 11 | ✅ 达标 |
| `bg2_old_st_pauls` | 旧圣保罗大教堂（1666 年状态） | **15** | 15 | ✅ 达标 |
| `bg4_royal_exchange` | 皇家交易所（火前） | **10** | 8 | ✅ 达标 |
| `bg3_pudding_lane_street` | 街景与民居 | **22** | 18 | ✅ 达标 |
| `bg5_great_fire` | 大火本身的同时代图像 | **14** | 14 | ✅ 达标 |
| `dress_restoration_1660s` | 人物服饰（复辟时期各阶层） | **26** | 26 | ✅ 达标 |
| `thames_watermen` | 泰晤士河与船夫 / 河上交通 | **8** | 8 | ✅ 达标 |
| `map_london_1658` | 1666 年前后的伦敦地图 | **12** | 12 | ✅ 达标 |

**合计 130 张**，覆盖 9 个资产。


---

## 2. 逐资产总账

> 每张一行：`ref_id | file | date | license | 原图尺寸 / 盘上尺寸`，下挂 title / url / collection。
> **盘上尺寸 ≠ 原图尺寸**时说明被 `ref_aspect` 补边或折叠过（rule 17.7），标 ⚠️；做 img2img 要回 `source_url` 重取原图。
> 完整字段（含 `evidences` / `use`）见各资产目录下的 `refs.md`。

### 1 · 整城全景（最高优先） — `bg0_london_panorama`（12 张）

```text
ref01 | ref/ref01_1647_Long_view_of_London_commons.jpg | 1647 | Public domain | 原图28661x5560 盘上3840x1280 ⚠️已折叠/补边(原比例5.2:1)
     title: 1647 Long view of London From Bankside - Wenceslaus Hollar.jpg
     url:   https://commons.wikimedia.org/wiki/File:1647_Long_view_of_London_From_Bankside_-_Wenceslaus_Hollar.jpg
     coll:  Wikimedia Commons · Scanned from a facsimile
ref02 | ref/ref02_1647_Long_view_of_London_commons.jpg | 1647 | Public domain | 原图4777x3282 盘上3840x2638
     title: 1647 Long view of London From Bankside - Wenceslaus Hollar (cropped).jpg
     url:   https://commons.wikimedia.org/wiki/File:1647_Long_view_of_London_From_Bankside_-_Wenceslaus_Hollar_(cropped).jpg
     coll:  Wikimedia Commons · Scanned from a facsimile
ref03 | ref/ref03_1647_Long_view_of_London_commons.jpg | 1647 | Public domain | 原图2508x849 盘上2508x849
     title: 1647 Long view of London From Bankside - Wenceslaus Hollar (cropp1.jpg
     url:   https://commons.wikimedia.org/wiki/File:1647_Long_view_of_London_From_Bankside_-_Wenceslaus_Hollar_(cropp1.jpg
     coll:  Wikimedia Commons · Scanned from a facsimile
ref04 | ref/ref04_1647_Long_view_of_London_commons.jpg | 1647 | Public domain | 原图2180x1305 盘上2180x1305
     title: 1647 Long view of London From Bankside - Wenceslaus Hollar (cropped) (cropped).jpg
     url:   https://commons.wikimedia.org/wiki/File:1647_Long_view_of_London_From_Bankside_-_Wenceslaus_Hollar_(cropped)_(cropped).jpg
     coll:  Wikimedia Commons · Scanned from a facsimile
ref05 | ref/ref05_Wenceslaus_Hollar_i_A_Tr_commons.jpg | 1666 | CC0 | 原图1920x650 盘上1920x650
     title: Wenceslaus Hollar - (i) A True and Exact Prospect of the Famous Citty of London, (ii) Another Prospect of the Sayd - B1977.14.17815 - Yale Center for British Art.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar_-_(i)_A_True_and_Exact_Prospect_of_the_Famous_Citty_of_London,_(ii)_Another_Prospect_of_the_Sayd_-_B1977.14.17815_-_Yale_Center_for_British_Art.jpg
     coll:  Wikimedia Commons · Yale Center for British Art
ref06 | ref/ref06_Wenceslaus_Hollar_i_A_Tr_commons.jpg | 1666 | CC0 | 原图1920x618 盘上1920x640 ⚠️已折叠/补边(原比例3.1:1)
     title: Wenceslaus Hollar - (i) A True and Exact Prospect of the Famous Citty of London (ii) Another Prospect of the Sayd - B1977.14.17814 - Yale Center for British Art.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar_-_(i)_A_True_and_Exact_Prospect_of_the_Famous_Citty_of_London_(ii)_Another_Prospect_of_the_Sayd_-_B1977.14.17814_-_Yale_Center_for_British_Art.jpg
     coll:  Wikimedia Commons · Yale Center for British Art
ref07 | ref/ref07_Wenceslas_Hollar_London__commons.jpg | Unknown date (author lived 1 | Public domain | 原图2906x1904 盘上2906x1904
     title: Wenceslas Hollar - London before the fire (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London_before_the_fire_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref08 | ref/ref08_Panorama_of_London_by_Cl_commons.jpg | — | Public domain | 原图? 盘上2563x855
     title: Panorama of London by Claes Van Visscher, 1616.jpg
     url:   https://commons.wikimedia.org/wiki/File:Panorama_of_London_by_Claes_Van_Visscher,_1616.jpg
     coll:  Wikimedia Commons ·
ref09 | ref/ref09_Panorama_of_London_by_Cl_commons.jpg | 1616 | Public domain | 原图? 盘上1278x589
     title: Panorama of London by Claes Van Visscher, 1616 no angels.jpg
     url:   https://commons.wikimedia.org/wiki/File:Panorama_of_London_by_Claes_Van_Visscher,_1616_no_angels.jpg
     coll:  Wikimedia Commons · panorama of London by Claes Van Visscher, 1616
ref10 | ref/ref10_London_panorama_1616_jpg_commons.jpg | 1616 | Public domain | 原图? 盘上3840x1280
     title: London panorama, 1616.jpg
     url:   https://commons.wikimedia.org/wiki/File:London_panorama,_1616.jpg
     coll:  Wikimedia Commons · Library of Congress[1]
ref11 | ref/ref11_City_of_London_from_Sout_commons.jpg | circa 1630 | Public domain | 原图600x400 盘上600x400
     title: City of London from Southwark, c1630.jpg
     url:   https://commons.wikimedia.org/wiki/File:City_of_London_from_Southwark,_c1630.jpg
     coll:  Wikimedia Commons · From the collection of the Museum of London, which does not state the name of th
ref12 | ref/ref12_A_panorama_of_London_loo_commons.jpg | — | CC BY 4.0 | 原图4396x1612 盘上3840x1408
     title: A panorama of London, looking north from Lambeth. Wood engra Wellcome V0018424.jpg
     url:   https://commons.wikimedia.org/wiki/File:A_panorama_of_London,_looking_north_from_Lambeth._Wood_engra_Wellcome_V0018424.jpg
     coll:  Wikimedia Commons · https://wellcomeimages.org/indexplus/obf_images/83/45/49fb54a4a6cda0d34149ca71ce
```

### 2 · 旧伦敦桥 — `bg1_london_bridge`（11 张）

```text
ref01 | ref/ref01_London_Bridge_1616_by_Cl_commons.jpg | 1616 | Public domain | 原图1850x1210 盘上1850x1210
     title: London Bridge (1616) by Claes Van Visscher.jpg
     url:   https://commons.wikimedia.org/wiki/File:London_Bridge_(1616)_by_Claes_Van_Visscher.jpg
     coll:  Wikimedia Commons · This image has been extracted from another file
ref02 | ref/ref02_Claude_de_Jongh_View_of__commons.jpg | circa 1632 | Public domain | 原图7193x3177 盘上3840x1696
     title: Claude de Jongh - View of London Bridge - Google Art Project.jpg
     url:   https://commons.wikimedia.org/wiki/File:Claude_de_Jongh_-_View_of_London_Bridge_-_Google_Art_Project.jpg
     coll:  Wikimedia Commons · vQGnI8LCW9UfSw at Google Cultural Institute maximum zoom level
ref03 | ref/ref03_Claude_de_Jongh_c_1600_1_commons.jpg | 1630 | Public domain | 原图944x289 盘上944x315 ⚠️已折叠/补边(原比例3.3:1)
     title: Claude de Jongh (c.1600-1663) - Old London Bridge - 88028831 - Kenwood House.jpg
     url:   https://commons.wikimedia.org/wiki/File:Claude_de_Jongh_(c.1600-1663)_-_Old_London_Bridge_-_88028831_-_Kenwood_House.jpg
     coll:  Wikimedia Commons · Art UK
ref04 | ref/ref04_London_bridge_1682_jpg_commons.jpg | 1682 | Public domain | 原图2298x658 盘上2298x766 ⚠️已折叠/补边(原比例3.5:1)
     title: London-bridge-1682.jpg
     url:   https://commons.wikimedia.org/wiki/File:London-bridge-1682.jpg
     coll:  Wikimedia Commons · Surveyed by: Morgan, William, d. 1690. Published: London, London Topographical S
ref05 | ref/ref05_West_side_of_London_Brid_commons.jpg | 1724 | Public domain | 原图2032x356 盘上2032x678 ⚠️已折叠/补边(原比例5.7:1)
     title: West side of London Bridg.jpg
     url:   https://commons.wikimedia.org/wiki/File:West_side_of_London_Bridg.jpg
     coll:  Wikimedia Commons · Bibliothèque nationale de France
ref06 | ref/ref06_A_View_of_London_Bridge__commons.jpg | circa 1830 | Public domain | 原图2500x1584 盘上2500x1584
     title: A View of London Bridge in the Year 1616, from an Engraving by John Vischer (BM 1880,1113.1529).jpg
     url:   https://commons.wikimedia.org/wiki/File:A_View_of_London_Bridge_in_the_Year_1616,_from_an_Engraving_by_John_Vischer_(BM_1880,1113.1529).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1880-1113-1529
ref07 | ref/ref07_A_View_of_London_Bridge__commons.jpg | circa 1830 | Public domain | 原图2500x1596 盘上2500x1596
     title: A View of London Bridge in the Year 1616, from an Engraving by John Vischer (BM Heal,Topography.85.c).jpg
     url:   https://commons.wikimedia.org/wiki/File:A_View_of_London_Bridge_in_the_Year_1616,_from_an_Engraving_by_John_Vischer_(BM_Heal,Topography.85.c).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_Heal-Topography-85-c
ref08 | ref/ref08_Ancient_Houses_at_the_Fo_commons.jpg | 1829 | Public domain | 原图2304x1839 盘上2304x1839
     title: Ancient Houses at the Foot of Old London Bridge, taken down Feby 1829 Shewing a Gothic Entrance (BM 1880,1113.5242).jpg
     url:   https://commons.wikimedia.org/wiki/File:Ancient_Houses_at_the_Foot_of_Old_London_Bridge,_taken_down_Feby_1829_Shewing_a_Gothic_Entrance_(BM_1880,1113.5242).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1880-1113-5242
ref09 | ref/ref09_Nonsuch_House_jpg_commons.jpg | 1873 | Public domain | 原图1398x1059 盘上1398x1059
     title: Nonsuch House.jpg
     url:   https://commons.wikimedia.org/wiki/File:Nonsuch_House.jpg
     coll:  Wikimedia Commons · https://archive.org/details/oldnewlondonanar02thor/page/18
ref10 | ref/ref10_P282_Palace_of_Nonsuch_o_commons.jpg | 1865 | Public domain | 原图1238x984 盘上1238x984
     title: P282 Palace of Nonsuch, on London Bridge.jpg
     url:   https://commons.wikimedia.org/wiki/File:P282_Palace_of_Nonsuch,_on_London_Bridge.jpg
     coll:  Wikimedia Commons · Internet Archive
ref11 | ref/ref11_Samuel_Scott_c_1702_1772_commons.jpg | 1753 | Public domain | 原图1200x661 盘上1200x661
     title: Samuel Scott (c.1702-1772) - Old London Bridge - 1401186 - National Trust.jpg
     url:   https://commons.wikimedia.org/wiki/File:Samuel_Scott_(c.1702-1772)_-_Old_London_Bridge_-_1401186_-_National_Trust.jpg
     coll:  Wikimedia Commons · Art UK
```

### 3 · 旧圣保罗大教堂（1666 年状态） — `bg2_old_st_pauls`（15 张）

```text
ref01 | ref/ref01_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图4332x3291 盘上3840x2917
     title: Wenceslas Hollar - St. Paul's. West front (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St._Paul%27s._West_front_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref02 | ref/ref02_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3856x2107 盘上3840x2098
     title: Wenceslas Hollar - St Paul's. North side (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._North_side_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref03 | ref/ref03_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3860x2153 盘上3840x2142
     title: Wenceslas Hollar - St Paul's. South side (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._South_side_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref04 | ref/ref04_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3215x2593 盘上3215x2593
     title: Wenceslas Hollar - St Paul's. East end (State 2) 2.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._East_end_(State_2)_2.jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref05 | ref/ref05_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图2218x3103 盘上2218x3103
     title: Wenceslas Hollar - St Paul's. East end (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._East_end_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref06 | ref/ref06_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图2614x3519 盘上2614x3519
     title: Wenceslas Hollar - St Paul's. The nave (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._The_nave_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref07 | ref/ref07_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图2692x3730 盘上2692x3730
     title: Wenceslas Hollar - St Paul's. The choir (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._The_choir_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref08 | ref/ref08_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3809x2797 盘上3809x2797
     title: Wenceslas Hollar - St Paul's Choir screen (State 3).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s_Choir_screen_(State_3).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref09 | ref/ref09_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3707x2561 盘上3707x2561
     title: Wenceslas Hollar - St Paul's. Chapter House (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St_Paul%27s._Chapter_House_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref10 | ref/ref10_Wenceslas_Hollar_St_Paul_commons.jpg | Unknown date (author lived 1 | Public domain | 原图5972x4330 盘上3840x2784
     title: Wenceslas Hollar - St. Paul's. Ground plan (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_St._Paul%27s._Ground_plan_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref11 | ref/ref11_Wenceslas_Hollar_Interio_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3844x2278 盘上3840x2276
     title: Wenceslas Hollar - Interior of the crypt of St Paul's (St. Faith) (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Interior_of_the_crypt_of_St_Paul%27s_(St._Faith)_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref12 | ref/ref12_Old_St_Paul_s_Cathedral__commons.jpg | 17th century | CC0 | 原图3602x2799 盘上3602x2799
     title: Old St. Paul's Cathedral, London, seen from the East MET DP814891.jpg
     url:   https://commons.wikimedia.org/wiki/File:Old_St._Paul%27s_Cathedral,_London,_seen_from_the_East_MET_DP814891.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref13 | ref/ref13_Wenceslaus_Hollar_East_e_commons.jpg | circa 1656 | Public domain | 原图806x640 盘上806x640
     title: Wenceslaus Hollar, East end of London’s Old St. Paul’s Cathedral, c. 1656.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar,_East_end_of_London%E2%80%99s_Old_St._Paul%E2%80%99s_Cathedral,_c._1656.jpg
     coll:  Wikimedia Commons · Artdaily.org
ref14 | ref/ref14_Old_St_Paul_s_Cathedral__commons.jpg | — | Public domain | 原图600x950 盘上600x950
     title: Old St Paul's Cathedral from Three Cranes Wharf.jpg
     url:   https://commons.wikimedia.org/wiki/File:Old_St_Paul%27s_Cathedral_from_Three_Cranes_Wharf.jpg
     coll:  Wikimedia Commons · Benham, William. Old St. Paul's Cathedral. London: Seeley and Co; New York: Macm
ref15 | ref/ref15_Inneres_von_St_Paul_Cath_commons.jpg | 1656 | Public domain | 原图2280x1610 盘上2280x1610
     title: Inneres von St. Paul Cathedral Wenzel Hollar.jpg
     url:   https://commons.wikimedia.org/wiki/File:Inneres_von_St._Paul_Cathedral_Wenzel_Hollar.jpg
     coll:  Wikimedia Commons · http://www.zeno.org/Kunstwerke/B/Hollar,+Wenzel%3A+London,+Inneres+von+St.+Paul+
```

### 4 · 皇家交易所（火前） — `bg4_royal_exchange`（10 张）

```text
ref01 | ref/ref01_Royal_Exchange_MET_DP823_commons.jpg | 1647 | CC0 | 原图3580x2116 盘上3580x2116
     title: Royal Exchange MET DP823176.jpg
     url:   https://commons.wikimedia.org/wiki/File:Royal_Exchange_MET_DP823176.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref02 | ref/ref02_Wenceslas_Hollar_Royal_E_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3638x2137 盘上3638x2137
     title: Wenceslas Hollar - Royal Exchange (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Royal_Exchange_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref03 | ref/ref03_FirstRoyalExchange_jpg_commons.jpg | — | Public domain | 原图400x309 盘上400x309
     title: FirstRoyalExchange.jpg
     url:   https://commons.wikimedia.org/wiki/File:FirstRoyalExchange.jpg
     coll:  Wikimedia Commons ·
ref04 | ref/ref04_N_N_1668_The_Roxall_Exch_commons.jpg | 1668 | Public domain | 原图980x616 盘上980x616
     title: N.N.(1668) The Roxall Exchange.jpg
     url:   https://commons.wikimedia.org/wiki/File:N.N.(1668)_The_Roxall_Exchange.jpg
     coll:  Wikimedia Commons · This file is from the Mechanical Curator collection, a set of over 1 million ima
ref05 | ref/ref05_ONL_1887_1_498_The_first_commons.jpg | 1873 (1887 copy) | Public domain | 原图1924x1336 盘上1924x1336
     title: ONL (1887) 1.498 - The first Royal Exchange.jpg
     url:   https://commons.wikimedia.org/wiki/File:ONL_(1887)_1.498_-_The_first_Royal_Exchange.jpg
     coll:  Wikimedia Commons · This file is from the Mechanical Curator collection, a set of over 1 million ima
ref06 | ref/ref06_The_Royal_Exchange_Londo_commons.jpg | — | CC BY 4.0 | 原图2454x3564 盘上2454x3564
     title: The Royal Exchange, London; elevation of the entrance facade Wellcome V0013153.jpg
     url:   https://commons.wikimedia.org/wiki/File:The_Royal_Exchange,_London;_elevation_of_the_entrance_facade_Wellcome_V0013153.jpg
     coll:  Wikimedia Commons · https://wellcomeimages.org/indexplus/obf_images/4a/f0/e4b4cfe2e915042028656e3803
ref07 | ref/ref07_Pictorial_Handbook_of_Lo_commons.jpg | 1854 | No restrictions ⛔只进prompt | 原图1766x1086 盘上1766x1086
     title: Pictorial Handbook of London (1854), p. 382 – Plan of first floor of Royal Exchange.jpg
     url:   https://commons.wikimedia.org/wiki/File:Pictorial_Handbook_of_London_(1854),_p._382_%E2%80%93_Plan_of_first_floor_of_Royal_Exchange.jpg
     coll:  Wikimedia Commons · https://www.flickr.com/photos/internetarchivebookimages/14779968001/
ref08 | ref/ref08_Wenceslaus_Hollar_Byrsa__commons.jpg | — | CC0 | 原图? 盘上1920x1185
     title: Wenceslaus Hollar - Byrsa Londienensis vulgo - the Royal Exchange - B1977.14.17833 - Yale Center for British Art.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar_-_Byrsa_Londienensis_vulgo_-_the_Royal_Exchange_-_B1977.14.17833_-_Yale_Center_for_British_Art.jpg
     coll:  Wikimedia Commons · Yale Center for British Art
ref09 | ref/ref09_Byrsa_Londinensis_vulgo__commons.jpg | circa 1647 | CC0 | 原图? 盘上3541x2084
     title: Byrsa Londinensis vulgo the Royal Exchange (Royal Exchange, London) MET DP823174.jpg
     url:   https://commons.wikimedia.org/wiki/File:Byrsa_Londinensis_vulgo_the_Royal_Exchange_(Royal_Exchange,_London)_MET_DP823174.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref10 | ref/ref10_Image_taken_from_page_77_commons.jpg | 1873 (1887 copy) | Public domain | 原图2657x1809 盘上2657x1809
     title: Image taken from page 775 of 'Old and New London, etc' (11190307493).jpg
     url:   https://commons.wikimedia.org/wiki/File:Image_taken_from_page_775_of_%27Old_and_New_London,_etc%27_(11190307493).jpg
     coll:  Wikimedia Commons · This file is from the Mechanical Curator collection, a set of over 1 million ima
```

### 5 · 街景与民居 — `bg3_pudding_lane_street`（22 张）

```text
ref01 | ref/ref01_View_of_Coldharbour_firs_commons.png | 2012-03-14 | Public domain | 原图780x1500 盘上780x1500
     title: View of Coldharbour first and after the Great Fire of 1666.PNG
     url:   https://commons.wikimedia.org/wiki/File:View_of_Coldharbour_first_and_after_the_Great_Fire_of_1666.PNG
     coll:  Wikimedia Commons · Cutout from http://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London_bef
ref02 | ref/ref02_Wenceslas_Hollar_London__commons.jpg | Unknown date (author lived 1 | Public domain | 原图3295x2322 盘上3295x2322
     title: Wenceslas Hollar - London.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London.jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref03 | ref/ref03_Wenceslas_Hollar_London__commons.jpg | Unknown date (author lived 1 | Public domain | 原图3471x2290 盘上3471x2290
     title: Wenceslas Hollar - London. St Catherine's church.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London._St_Catherine%27s_church.jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref04 | ref/ref04_Wenceslas_Hollar_Arundel_commons.jpg | Unknown date (author lived 1 | Public domain | 原图6464x2815 盘上3840x1672
     title: Wenceslas Hollar - Arundel House, from the N..jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Arundel_House,_from_the_N..jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref05 | ref/ref05_Wenceslas_Hollar_Arundel_commons.jpg | Unknown date (author lived 1 | Public domain | 原图6375x2773 盘上3840x1670
     title: Wenceslas Hollar - Arundel House, from the S..jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Arundel_House,_from_the_S..jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref06 | ref/ref06_Titelprent_van_Marcellus_commons.jpg | between 1688 and 1724 | CC0 | 原图3818x5652 盘上3818x5652
     title: Titelprent van Marcellus Laroon, The Cryes of the City of London Straatventers in Londen (serietitel) Het Geroep in de Stadt van Londen (serietitel op object) The Cryes of the city of London (serietitel op object), RP-P-1957-677.jpg
     url:   https://commons.wikimedia.org/wiki/File:Titelprent_van_Marcellus_Laroon,_The_Cryes_of_the_City_of_London_Straatventers_in_Londen_(serietitel)_Het_Geroep_in_de_Stadt_van_Londen_(serietitel_op_object)_The_Cryes_of_the_city_of_London_(serietitel_op_object),_RP-P-1957-677.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117620
ref07 | ref/ref07_Melkmeid_Straatventers_i_commons.jpg | between 1688 and 1724 | CC0 | 原图4100x6294 盘上3840x5895
     title: Melkmeid Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-686.jpg
     url:   https://commons.wikimedia.org/wiki/File:Melkmeid_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-686.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117629
ref08 | ref/ref08_Oesterverkoper_Straatven_commons.jpg | between 1688 and 1724 | CC0 | 原图4154x6102 盘上3840x5641
     title: Oesterverkoper Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-680.jpg
     url:   https://commons.wikimedia.org/wiki/File:Oesterverkoper_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-680.jpg
     coll:  Wikimedia Commons · https://hdl.handle.net/10934/RM0001.COLLECT.117628
ref09 | ref/ref09_Makreelverkoopster_Straa_commons.jpg | between 1688 and 1724 | CC0 | 原图4150x6170 盘上3840x5709
     title: Makreelverkoopster Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-684.jpg
     url:   https://commons.wikimedia.org/wiki/File:Makreelverkoopster_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-684.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117630
ref10 | ref/ref10_Aspergeverkoopster_Straa_commons.jpg | between 1688 and 1724 | CC0 | 原图4200x6306 盘上3840x5765
     title: Aspergeverkoopster Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-683.jpg
     url:   https://commons.wikimedia.org/wiki/File:Aspergeverkoopster_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-683.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117624
ref11 | ref/ref11_Inkoopster_van_tweedehan_commons.jpg | between 1688 and 1724 | CC0 | 原图3656x5624 盘上3656x5624
     title: Inkoopster van tweedehandskleding Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-679.jpg
     url:   https://commons.wikimedia.org/wiki/File:Inkoopster_van_tweedehandskleding_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-679.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.410625
ref12 | ref/ref12_Verkoper_van_tweedehands_commons.jpg | between 1688 and 1724 | CC0 | 原图4222x6270 盘上3840x5703
     title: Verkoper van tweedehandskleding Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-678.jpg
     url:   https://commons.wikimedia.org/wiki/File:Verkoper_van_tweedehandskleding_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-678.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117625
ref13 | ref/ref13_Verkoopster_van_de_Londo_commons.jpg | 1688 | CC0 | 原图3140x4700 盘上3140x4700
     title: Verkoopster van de London Gazette Londons Gazette here Nouvelle gazette Chi compra gli'anisi di Londra (titel op object) Straatverkopers in Londen (serietitel) The Cryes of the City of London Drawne after the Life (se, RP-P-2015-26-1421.jpg
     url:   https://commons.wikimedia.org/wiki/File:Verkoopster_van_de_London_Gazette_Londons_Gazette_here_Nouvelle_gazette_Chi_compra_gli%27anisi_di_Londra_(titel_op_object)_Straatverkopers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_Drawne_after_the_Life_(se,_RP-P-2015-26-1421.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.619964
ref14 | ref/ref14_Verkoopster_van_almanakk_commons.jpg | 1688 | CC0 | 原图3054x4754 盘上3054x4754
     title: Verkoopster van almanakken Buy a new almanack Almanachs nouveaux Lunarij dell anno nuovo (titel op object) Straatverkopers in Londen The Cryes of the City of London Drawne after the Life, RP-P-2015-26-942.jpg
     url:   https://commons.wikimedia.org/wiki/File:Verkoopster_van_almanakken_Buy_a_new_almanack_Almanachs_nouveaux_Lunarij_dell_anno_nuovo_(titel_op_object)_Straatverkopers_in_Londen_The_Cryes_of_the_City_of_London_Drawne_after_the_Life,_RP-P-2015-26-942.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.611049
ref15 | ref/ref15_Scharensliep_Straatvente_commons.jpg | between 1688 and 1724 | CC0 | 原图3638x5604 盘上3638x5604
     title: Scharensliep Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-686X.jpg
     url:   https://commons.wikimedia.org/wiki/File:Scharensliep_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-686X.jpg
     coll:  Wikimedia Commons · https://hdl.handle.net/10934/RM0001.COLLECT.495253
ref16 | ref/ref16_Mattenvlechter_Straatven_commons.jpg | ca. 1688 - ca. 1724 | CC0 | 原图3788x5726 盘上3788x5726
     title: Mattenvlechter Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-685.jpg
     url:   https://commons.wikimedia.org/wiki/File:Mattenvlechter_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-685.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.117622
ref17 | ref/ref17_Speldenverkoper_Straatve_commons.jpg | between 1688 and 1724 | CC0 | 原图4128x6276 盘上3840x5838
     title: Speldenverkoper Straatventers in Londen (serietitel) The Cryes of the City of London (serietitel), RP-P-1957-682.jpg
     url:   https://commons.wikimedia.org/wiki/File:Speldenverkoper_Straatventers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_(serietitel),_RP-P-1957-682.jpg
     coll:  Wikimedia Commons · https://hdl.handle.net/10934/RM0001.COLLECT.117627
ref18 | ref/ref18_Man_met_een_kijkkast_op__commons.jpg | 1688 | CC0 | 原图3058x4662 盘上3058x4662
     title: Man met een kijkkast op zijn rug Oh Rare Shoe Rare chose a voir Chi vuol veder meraviglie (titel op object) Straatverkopers in Londen (serietitel) The Cryes of the City of London Drawne after the Life (serietitel), RP-P-2015-26-626.jpg
     url:   https://commons.wikimedia.org/wiki/File:Man_met_een_kijkkast_op_zijn_rug_Oh_Rare_Shoe_Rare_chose_a_voir_Chi_vuol_veder_meraviglie_(titel_op_object)_Straatverkopers_in_Londen_(serietitel)_The_Cryes_of_the_City_of_London_Drawne_after_the_Life_(serietitel),_RP-P-2015-26-626.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.603601
ref19 | ref/ref19_337_338_High_Holborn_Sta_commons.jpg | 2014-05-31 16:15:57 | CC BY-SA 4.0 | 原图4608x3456 盘上3840x2880
     title: 337-338 High Holborn, Staple Inn 01.jpg
     url:   https://commons.wikimedia.org/wiki/File:337-338_High_Holborn,_Staple_Inn_01.jpg
     coll:  Wikimedia Commons · Own work
ref20 | ref/ref20_337_338_High_Holborn_Sta_commons.jpg | 2014-05-31 16:17:06 | CC BY-SA 4.0 | 原图4608x3456 盘上3840x2880
     title: 337-338 High Holborn, Staple Inn 04.jpg
     url:   https://commons.wikimedia.org/wiki/File:337-338_High_Holborn,_Staple_Inn_04.jpg
     coll:  Wikimedia Commons · Own work
ref21 | ref/ref21_Half_timbered_tudor_buil_commons.jpg | 2007-05-12 | CC BY-SA 3.0 | 原图3040x2288 盘上3040x2288
     title: Half-timbered tudor buildings, High Holborn.JPG
     url:   https://commons.wikimedia.org/wiki/File:Half-timbered_tudor_buildings,_High_Holborn.JPG
     coll:  Wikimedia Commons · Own work
ref22 | ref/ref22_Staple_Inn_High_Holborn__commons.jpg | 2009-10-17 10:56 | CC BY 2.0 | 原图2736x3648 盘上2736x3648
     title: Staple Inn, High Holborn, City of London (4053331805).jpg
     url:   https://commons.wikimedia.org/wiki/File:Staple_Inn,_High_Holborn,_City_of_London_(4053331805).jpg
     coll:  Wikimedia Commons · Staple Inn, High Holborn, City of London
```

### 6 · 大火本身的同时代图像 — `bg5_great_fire`（14 张）

```text
ref01 | ref/ref01_Anonymous_General_View_o_commons.jpg | — | CC0 | 原图1920x1137 盘上1920x1137
     title: Anonymous - General View of London during the Great Fire of 1666 - B1977.14.17854 - Yale Center for British Art.jpg
     url:   https://commons.wikimedia.org/wiki/File:Anonymous_-_General_View_of_London_during_the_Great_Fire_of_1666_-_B1977.14.17854_-_Yale_Center_for_British_Art.jpg
     coll:  Wikimedia Commons · Yale Center for British Art
ref02 | ref/ref02_London_Before_and_After__commons.jpg | 1666 | CC0 | 原图3918x735 盘上3840x1280 ⚠️已折叠/补边(原比例5.3:1)
     title: London Before and After the Fire MET DP827163.jpg
     url:   https://commons.wikimedia.org/wiki/File:London_Before_and_After_the_Fire_MET_DP827163.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref03 | ref/ref03_London_Before_and_After__commons.jpg | 1666 | CC0 | 原图3943x739 盘上3840x1280 ⚠️已折叠/补边(原比例5.3:1)
     title: London Before and After the Fire MET DP827201.jpg
     url:   https://commons.wikimedia.org/wiki/File:London_Before_and_After_the_Fire_MET_DP827201.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref04 | ref/ref04_Wenceslaus_Hollar_Burnin_commons.jpg | 1666 | CC0 | 原图1920x1190 盘上1920x1190
     title: Wenceslaus Hollar - Burning of old St Paul's Cathedral in the Fire of London - B1977.14.17818 - Yale Center for British Art.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar_-_Burning_of_old_St_Paul%27s_Cathedral_in_the_Fire_of_London_-_B1977.14.17818_-_Yale_Center_for_British_Art.jpg
     coll:  Wikimedia Commons · Yale Center for British Art
ref05 | ref/ref05_Verschuier_fire_jpg_commons.jpg | 1666 | Public domain | 原图5870x3573 盘上3840x2337
     title: Verschuier-fire.jpg
     url:   https://commons.wikimedia.org/wiki/File:Verschuier-fire.jpg
     coll:  Wikimedia Commons · http://www.kunst-fuer-alle.de/deutsch/kunst/kuenstler/kunstdruck/lieve-verschuie
ref06 | ref/ref06_The_Great_Fire_of_London_commons.jpg | circa 1670 | Public domain | 原图5138x6224 盘上3840x4652
     title: The Great Fire of London, with Ludgate and Old St. Paul's - Google Art Project.jpg
     url:   https://commons.wikimedia.org/wiki/File:The_Great_Fire_of_London,_with_Ludgate_and_Old_St._Paul%27s_-_Google_Art_Project.jpg
     coll:  Wikimedia Commons · 5QFYrsXh6Llrpg at Google Cultural Institute maximum zoom level
ref07 | ref/ref07_The_Great_Fire_of_London_commons.jpg | circa 1670 | Public domain | 原图2464x3000 盘上2464x3000
     title: The Great Fire of London, with Ludgate and Old St. Paul's.JPG
     url:   https://commons.wikimedia.org/wiki/File:The_Great_Fire_of_London,_with_Ludgate_and_Old_St._Paul%27s.JPG
     coll:  Wikimedia Commons · The painting was photographed in the Yale Center for British Art
ref08 | ref/ref08_Great_Fire_London_jpg_commons.jpg | 1675 | Public domain | 原图5477x3189 盘上3840x2236
     title: Great Fire London.jpg
     url:   https://commons.wikimedia.org/wiki/File:Great_Fire_London.jpg
     coll:  Wikimedia Commons · museumoflondonprints.com
ref09 | ref/ref09_The_Great_Fire_of_London_commons.png | c,1666 | Public domain | 原图1744x1365 盘上1744x1365
     title: The Great Fire of London.png
     url:   https://commons.wikimedia.org/wiki/File:The_Great_Fire_of_London.png
     coll:  Wikimedia Commons · https://artuk.org/discover/artworks/the-great-fire-of-london-50725/view_as/grid/
ref10 | ref/ref10_Great_Fire_1666_cropped__commons.jpg | 1666 | Public domain | 原图200x200 盘上200x200
     title: Great Fire 1666 cropped.jpg
     url:   https://commons.wikimedia.org/wiki/File:Great_Fire_1666_cropped.jpg
     coll:  Wikimedia Commons · Unknown sourceUnknown source
ref11 | ref/ref11_Old_St_Pauls_Ruins_1666__commons.png | circa 1673 | Public domain | 原图3188x2236 盘上3188x2236
     title: Old.St.Pauls.Ruins.1666.png
     url:   https://commons.wikimedia.org/wiki/File:Old.St.Pauls.Ruins.1666.png
     coll:  Wikimedia Commons · Scanned from Adrian Tinniswood, By Permission of Heaven: The Story of the Great
ref12 | ref/ref12_17th_century_fire_engine_commons.jpg | 17th century | Public domain | 原图300x187 盘上300x187
     title: 17th.century.fire.engine.jpg
     url:   https://commons.wikimedia.org/wiki/File:17th.century.fire.engine.jpg
     coll:  Wikimedia Commons · As described above
ref13 | ref/ref13_Print_satirical_print_fr_commons.jpg | 1667 | Public domain | 原图1342x1600 盘上1342x1600
     title: Print, satirical print, frontispiece (BM 1868,0808.13197).jpg
     url:   https://commons.wikimedia.org/wiki/File:Print,_satirical_print,_frontispiece_(BM_1868,0808.13197).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1868-0808-13197
ref14 | ref/ref14_GreatFireOfLondon1666_Vi_commons.jpg | — | Public domain | 原图1560x873 盘上1560x873
     title: GreatFireOfLondon1666 VictorianEngravingAfterVisscher300dpi.jpg
     url:   https://commons.wikimedia.org/wiki/File:GreatFireOfLondon1666_VictorianEngravingAfterVisscher300dpi.jpg
     coll:  Wikimedia Commons ·
```

### 7 · 人物服饰（复辟时期各阶层） — `dress_restoration_1660s`（26 张）

```text
ref01 | ref/ref01_Titelprent_voor_de_prent_commons.jpg | between 1665 and 1672 | CC0 | 原图1052x1782 盘上1052x1782
     title: Titelprent voor de prentserie 'Vrouwen gekleed volgens de Engelse mode, ca. 1640' Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel) Ornatus Muliebris Anglicanus The Severall Habits of E, RP-P-OB-116.244.jpg
     url:   https://commons.wikimedia.org/wiki/File:Titelprent_voor_de_prentserie_%27Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640%27_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel)_Ornatus_Muliebris_Anglicanus_The_Severall_Habits_of_E,_RP-P-OB-116.244.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.699554
ref02 | ref/ref02_Ciuis_Londinensis_Filia__commons.jpg | 1643 | CC0 | 原图3792x5742 盘上3792x5742
     title: Ciuis Londinensis Filia Cittiznes daugter (titel op object) Theatrum Mulierum (serietitel) Europese vrouwen in klederdracht (serietitel), RP-P-OB-11.532.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ciuis_Londinensis_Filia_Cittiznes_daugter_(titel_op_object)_Theatrum_Mulierum_(serietitel)_Europese_vrouwen_in_klederdracht_(serietitel),_RP-P-OB-11.532.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32729
ref03 | ref/ref03_Mercatoris_Londinensis_F_commons.jpg | 1643 | CC0 | 原图4004x5860 盘上3840x5620
     title: Mercatoris Londinensis Filia (titel op object) Theatrum Mulierum (serietitel) Europese vrouwen in klederdracht (serietitel), RP-P-OB-11.533.jpg
     url:   https://commons.wikimedia.org/wiki/File:Mercatoris_Londinensis_Filia_(titel_op_object)_Theatrum_Mulierum_(serietitel)_Europese_vrouwen_in_klederdracht_(serietitel),_RP-P-OB-11.533.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32730
ref04 | ref/ref04_Mulier_Generosa_Anglica__commons.jpg | 1643 | CC0 | 原图3990x5924 盘上3840x5701
     title: Mulier Generosa Anglica English gentle woman (titel op object) Theatrum Mulierum (serietitel) Europese vrouwen in klederdracht (serietitel), RP-P-OB-11.525.jpg
     url:   https://commons.wikimedia.org/wiki/File:Mulier_Generosa_Anglica_English_gentle_woman_(titel_op_object)_Theatrum_Mulierum_(serietitel)_Europese_vrouwen_in_klederdracht_(serietitel),_RP-P-OB-11.525.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32722
ref05 | ref/ref05_Mulier_Generosa_Anglica__commons.jpg | 1644 | CC0 | 原图3828x5872 盘上3828x5872
     title: Mulier Generosa Anglica (titel op object) Theatrum Mulierum (serietitel) Europese vrouwen in klederdracht (serietitel), RP-P-OB-11.527.jpg
     url:   https://commons.wikimedia.org/wiki/File:Mulier_Generosa_Anglica_(titel_op_object)_Theatrum_Mulierum_(serietitel)_Europese_vrouwen_in_klederdracht_(serietitel),_RP-P-OB-11.527.jpg
     coll:  Wikimedia Commons · https://hdl.handle.net/10934/RM0001.COLLECT.32724
ref06 | ref/ref06_Titelprent_voor_Ornatus__commons.jpg | 1640 | CC0 | 原图3780x5834 盘上3780x5834
     title: Titelprent voor Ornatus Muliebris Anglicanus Ornatus Muliebris Anglicanus (serietitel op object) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2679.jpg
     url:   https://commons.wikimedia.org/wiki/File:Titelprent_voor_Ornatus_Muliebris_Anglicanus_Ornatus_Muliebris_Anglicanus_(serietitel_op_object)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2679.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32636
ref07 | ref/ref07_Engelse_vrouw_met_breedg_commons.jpg | 1640 | CC0 | 原图3752x5900 盘上3752x5900
     title: Engelse vrouw met breedgerande hoed Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2698.jpg
     url:   https://commons.wikimedia.org/wiki/File:Engelse_vrouw_met_breedgerande_hoed_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2698.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32655
ref08 | ref/ref08_Engelse_vrouw_met_donker_commons.jpg | 1640 | CC0 | 原图3688x5828 盘上3688x5828
     title: Engelse vrouw met donkere hoed Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2696.jpg
     url:   https://commons.wikimedia.org/wiki/File:Engelse_vrouw_met_donkere_hoed_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2696.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32653
ref09 | ref/ref09_Engelse_vrouw_met_zakdoe_commons.jpg | 1638 | CC0 | 原图3798x5994 盘上3798x5994
     title: Engelse vrouw met zakdoek in de hand Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2702.jpg
     url:   https://commons.wikimedia.org/wiki/File:Engelse_vrouw_met_zakdoek_in_de_hand_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2702.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32659
ref10 | ref/ref10_Engelse_vrouw_van_stand__commons.jpg | 1639 | CC0 | 原图3728x5994 盘上3728x5994
     title: Engelse vrouw van stand, met vouwwaaier Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode ca. 1640 (serietitel), RP-P-1920-2683.jpg
     url:   https://commons.wikimedia.org/wiki/File:Engelse_vrouw_van_stand,_met_vouwwaaier_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode_ca._1640_(serietitel),_RP-P-1920-2683.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32640
ref11 | ref/ref11_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3906x5990 盘上3840x5889
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse keukenmeid met mand aan de arm Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2705.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_keukenmeid_met_mand_aan_de_arm_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2705.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32662
ref12 | ref/ref12_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3696x5996 盘上3696x5996
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met gedeeltelijk loshangend haar, op de rug gezien Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 164, RP-P-1920-2695.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_gedeeltelijk_loshangend_haar,_op_de_rug_gezien_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._164,_RP-P-1920-2695.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32652
ref13 | ref/ref13_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3734x5988 盘上3734x5988
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met handschoenen in de hand Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2704.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_handschoenen_in_de_hand_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2704.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32661
ref14 | ref/ref14_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3676x5940 盘上3676x5940
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met hoed en brede plooikraag Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2699.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_hoed_en_brede_plooikraag_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2699.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32656
ref15 | ref/ref15_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3784x5894 盘上3784x5894
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met hoed en mof Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2700.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_hoed_en_mof_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2700.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32657
ref16 | ref/ref16_Ornatus_Muliebris_Anglic_commons.jpg | 1640 | CC0 | 原图3754x5910 盘上3754x5910
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met hoog gesloten omslagdoek Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2703.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_hoog_gesloten_omslagdoek_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2703.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32660
ref17 | ref/ref17_Ornatus_Muliebris_Anglic_commons.jpg | 1638 | CC0 | 原图3742x5876 盘上3742x5876
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met kapje en mof Ornatus Muliebris Anglicanus (serietitel) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2693.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_kapje_en_mof_Ornatus_Muliebris_Anglicanus_(serietitel)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2693.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32650
ref18 | ref/ref18_Ornatus_Muliebris_Anglic_commons.jpg | 1639 | CC0 | 原图3774x5838 盘上3774x5838
     title: Ornatus Muliebris Anglicanus (De kleding van Engelse vrouwen) Engelse vrouw met masker, kap en mof Ornatus Muliebris Anglicanus (serietitel op object) Vrouwen gekleed volgens de Engelse mode, ca. 1640 (serietitel), RP-P-1920-2691.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ornatus_Muliebris_Anglicanus_(De_kleding_van_Engelse_vrouwen)_Engelse_vrouw_met_masker,_kap_en_mof_Ornatus_Muliebris_Anglicanus_(serietitel_op_object)_Vrouwen_gekleed_volgens_de_Engelse_mode,_ca._1640_(serietitel),_RP-P-1920-2691.jpg
     coll:  Wikimedia Commons · http://hdl.handle.net/10934/RM0001.COLLECT.32648
ref19 | ref/ref19_Any_Bakeing_Peares_jpg_commons.jpg | 1687 | Public domain | 原图600x921 盘上600x921
     title: Any Bakeing Peares.jpg
     url:   https://commons.wikimedia.org/wiki/File:Any_Bakeing_Peares.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref20 | ref/ref20_Buy_my_fat_Chickens_jpg_commons.jpg | 1687 | Public domain | 原图600x922 盘上600x922
     title: Buy my fat Chickens.jpg
     url:   https://commons.wikimedia.org/wiki/File:Buy_my_fat_Chickens.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref21 | ref/ref21_Four_for_Six_pence_Mackr_commons.jpg | 1687 | Public domain | 原图600x924 盘上600x924
     title: Four for Six pence Mackrell.jpg
     url:   https://commons.wikimedia.org/wiki/File:Four_for_Six_pence_Mackrell.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref22 | ref/ref22_Old_Cloaks_Suits_or_Coat_commons.jpg | 1687 | Public domain | 原图600x921 盘上600x921
     title: Old Cloaks Suits or Coats.jpg
     url:   https://commons.wikimedia.org/wiki/File:Old_Cloaks_Suits_or_Coats.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref23 | ref/ref23_The_London_Begger_jpg_commons.jpg | 1687 | Public domain | 原图600x950 盘上600x950
     title: The London Begger.jpg
     url:   https://commons.wikimedia.org/wiki/File:The_London_Begger.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref24 | ref/ref24_New_River_Water_jpg_commons.jpg | 1687 | Public domain | 原图600x901 盘上600x901
     title: New River Water.jpg
     url:   https://commons.wikimedia.org/wiki/File:New_River_Water.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref25 | ref/ref25_Ripe_Speragas_jpg_commons.jpg | 1687 | Public domain | 原图600x945 盘上600x945
     title: Ripe Speragas.jpg
     url:   https://commons.wikimedia.org/wiki/File:Ripe_Speragas.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
ref26 | ref/ref26_Buy_my_4_Ropes_of_Hard_O_commons.jpg | 1687 | Public domain | 原图600x926 盘上600x926
     title: Buy my 4 Ropes of Hard Onyons.jpg
     url:   https://commons.wikimedia.org/wiki/File:Buy_my_4_Ropes_of_Hard_Onyons.jpg
     coll:  Wikimedia Commons · Cryes of the City of London Drawne after the Life
```

### 8 · 泰晤士河与船夫 / 河上交通 — `thames_watermen`（8 张）

```text
ref01 | ref/ref01_A_view_of_Lambeth_Palace_commons.jpg | 1625–77 | CC0 | 原图3886x2160 盘上3840x2134
     title: A view of Lambeth Palace from the river at Whitehall Stairs MET DP823187.jpg
     url:   https://commons.wikimedia.org/wiki/File:A_view_of_Lambeth_Palace_from_the_river_at_Whitehall_Stairs_MET_DP823187.jpg
     coll:  Wikimedia Commons · This file was donated to Wikimedia Commons as part of a project by the Metropoli
ref02 | ref/ref02_Wenceslaus_Hollar_Palati_commons.jpg | circa 1647 | Public domain | 原图6715x3019 盘上3840x1726
     title: Wenceslaus Hollar - Palatium Regis Prope Londinum, Vulgo Whitehall - Google Art Project.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslaus_Hollar_-_Palatium_Regis_Prope_Londinum,_Vulgo_Whitehall_-_Google_Art_Project.jpg
     coll:  Wikimedia Commons · xgGfXJczVmmasg at Google Cultural Institute maximum zoom level
ref03 | ref/ref03_Wenceslas_Hollar_Tower_o_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3667x2127 盘上3667x2127
     title: Wenceslas Hollar - Tower of London (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Tower_of_London_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref04 | ref/ref04_Abraham_Hondius_c_1625_1_commons.jpg | 1677 | Public domain | 原图800x494 盘上800x494
     title: Abraham Hondius (c.1625-1691) - The Frozen Thames, Looking Eastwards towards Old London Bridge, London - 35.190 - London Museum.jpg
     url:   https://commons.wikimedia.org/wiki/File:Abraham_Hondius_(c.1625-1691)_-_The_Frozen_Thames,_Looking_Eastwards_towards_Old_London_Bridge,_London_-_35.190_-_London_Museum.jpg
     coll:  Wikimedia Commons · Art UK
ref05 | ref/ref05_The_Frozen_Thames_1677_j_commons.jpg | 1677 | Public domain | 原图600x371 盘上600x371
     title: The Frozen Thames 1677.jpg
     url:   https://commons.wikimedia.org/wiki/File:The_Frozen_Thames_1677.jpg
     coll:  Wikimedia Commons · Original painting in the collection of the Museum of London
ref06 | ref/ref06_The_Frozen_Thames_1677_b_commons.jpg | 1677 | Public domain | 原图1920x1187 盘上1920x1187
     title: The Frozen Thames 1677 by Abraham Hondius.jpg
     url:   https://commons.wikimedia.org/wiki/File:The_Frozen_Thames_1677_by_Abraham_Hondius.jpg
     coll:  Wikimedia Commons · Historic Mysteries, the original painting is in the collection of the Museum of
ref07 | ref/ref07_Wenceslas_Hollar_Richmon_commons.jpg | Unknown date (author lived 1 | Public domain | 原图3596x1277 盘上3596x1277
     title: Wenceslas Hollar - Richmond.jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_Richmond.jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref08 | ref/ref08_These_copies_are_from_po_commons.jpg | 1809 | Public domain | 原图6852x8364 盘上3840x4687
     title: These copies are from portions of an extremely rare print by Visscher, the apparent circumstances of which evince it to have been taken early in the reign of King James 1st many years prior LCCN2017650793.jpg
     url:   https://commons.wikimedia.org/wiki/File:These_copies_are_from_portions_of_an_extremely_rare_print_by_Visscher,_the_apparent_circumstances_of_which_evince_it_to_have_been_taken_early_in_the_reign_of_King_James_1st_many_years_prior_LCCN2017650793.jpg
     coll:  Wikimedia Commons · Library of Congress
```

### 9 · 1666 年前后的伦敦地图 — `map_london_1658`（12 张）

```text
ref01 | ref/ref01_Maps_Of_Old_London_Faith_commons.jpg | 1658 | Public domain | 原图2641x2182 盘上2641x2182
     title: Maps Of Old London Faithorne.jpg
     url:   https://commons.wikimedia.org/wiki/File:Maps_Of_Old_London_Faithorne.jpg
     coll:  Wikimedia Commons · Maps of Old London, ed. G. E. (Geraldine Edith) Mitton (1908)
ref02 | ref/ref02_A_Map_or_Ground_Plot_of__commons.jpg | 1666 | Public domain | 原图1620x2500 盘上1620x2500
     title: A Map or Ground Plot of the Citty of London... (BM 1856,0607.6).jpg
     url:   https://commons.wikimedia.org/wiki/File:A_Map_or_Ground_Plot_of_the_Citty_of_London..._(BM_1856,0607.6).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1856-0607-6
ref03 | ref/ref03_Map_London_gutted_1666_j_commons.jpg | — | Public domain | 原图2369x1879 盘上2369x1879
     title: Map.London.gutted.1666.jpg
     url:   https://commons.wikimedia.org/wiki/File:Map.London.gutted.1666.jpg
     coll:  Wikimedia Commons ·
ref04 | ref/ref04_Wenceslas_Hollar_London__commons.jpg | Unknown date (author lived 1 | Public domain | 原图6940x2275 盘上3840x1280 ⚠️已折叠/补边(原比例3.1:1)
     title: Wenceslas Hollar - London before and after the fire (State 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London_before_and_after_the_fire_(State_1).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref05 | ref/ref05_Wenceslas_Hollar_London__commons.jpg | Unknown date (author lived 1 | Public domain | 原图3539x2367 盘上3539x2367
     title: Wenceslas Hollar - London before and after the fire (State 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Wenceslas_Hollar_-_London_before_and_after_the_fire_(State_2).jpg
     coll:  Wikimedia Commons · Artwork from University of Toronto Wenceslaus Hollar Digital Collection
ref06 | ref/ref06_Platte_Grondt_der_Verbra_commons.jpg | 1666 | Public domain | 原图2500x2000 盘上2500x2000
     title: Platte Grondt der Verbrande Stadt London (BM 1880,1113.1172).jpg
     url:   https://commons.wikimedia.org/wiki/File:Platte_Grondt_der_Verbrande_Stadt_London_(BM_1880,1113.1172).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1880-1113-1172
ref07 | ref/ref07_Platte_Grondt_der_Verbra_commons.jpg | 1666 | Public domain | 原图2500x2155 盘上2500x2155
     title: Platte Grondt der Verbrande Stadt London (BM 1885,1114.151).jpg
     url:   https://commons.wikimedia.org/wiki/File:Platte_Grondt_der_Verbrande_Stadt_London_(BM_1885,1114.151).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_1885-1114-151
ref08 | ref/ref08_Bodleian_Libraries_Propo_commons.jpg | 1666 | Public domain | 原图1000x739 盘上1000x739
     title: Bodleian Libraries, Proposal to rebuild the city of London after the Great Fire of 1666, by Val Knight.jpg
     url:   https://commons.wikimedia.org/wiki/File:Bodleian_Libraries,_Proposal_to_rebuild_the_city_of_London_after_the_Great_Fire_of_1666,_by_Val_Knight.jpg
     coll:  Wikimedia Commons · Digital Bodleian
ref09 | ref/ref09_Bodleian_Libraries_Sir_J_commons.jpg | 1666 | Public domain | 原图976x549 盘上976x549
     title: Bodleian Libraries, Sir John Evelyn's plan for rebuilding the city of London, after the Great Fire in the year 1666.jpg
     url:   https://commons.wikimedia.org/wiki/File:Bodleian_Libraries,_Sir_John_Evelyn%27s_plan_for_rebuilding_the_city_of_London,_after_the_Great_Fire_in_the_year_1666.jpg
     coll:  Wikimedia Commons · Digital Bodleian
ref10 | ref/ref10_John_Evelyn_s_plan_rebui_commons.png | — | Public domain | 原图873x521 盘上873x521
     title: John Evelyn's plan rebuilding London Great Fire 1666.png
     url:   https://commons.wikimedia.org/wiki/File:John_Evelyn%27s_plan_rebuilding_London_Great_Fire_1666.png
     coll:  Wikimedia Commons ·
ref11 | ref/ref11_Print_map_BM_Q_6_136_1_j_commons.jpg | between 1660 and 1666 | Public domain | 原图2500x1938 盘上2500x1938
     title: Print, map (BM Q,6.136 1).jpg
     url:   https://commons.wikimedia.org/wiki/File:Print,_map_(BM_Q,6.136_1).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_Q-6-136
ref12 | ref/ref12_Print_map_BM_Q_6_136_2_j_commons.jpg | between 1660 and 1666 | Public domain | 原图1825x2500 盘上1825x2500
     title: Print, map (BM Q,6.136 2).jpg
     url:   https://commons.wikimedia.org/wiki/File:Print,_map_(BM_Q,6.136_2).jpg
     coll:  Wikimedia Commons · https://www.britishmuseum.org/collection/object/P_Q-6-136
```

---

## 3. 许可纪律（逐图记录，不一律标 CC0）

### ① 本库的许可分布

| 许可 | 张数 | 能否入画 | 说明 |
|---|---|---|---|
| **CC0** | 42 | ✅ 可 | Rijksmuseum / Met Open Access / Yale Center for British Art。放弃一切权利，无署名义务 |
| **Public domain** | 81 | ✅ 可 | 17 世纪原作早已过版权期；Commons 的 PD 标记多为 `PD-old-100` / `PD-art` |
| **CC BY 4.0** | 2 | ✅ 可，**须署名** | Wellcome Collection 两张（`bg4.ref06` 交易所立面、`bg0.ref12` 兰贝斯全景） |
| **CC BY 2.0** | 1 | ✅ 可，**须署名** | `bg3.ref22` Staple Inn 现状照 |
| **CC BY-SA 4.0 / 3.0** | 3 | 🟡 **建议不入画** | 见 ② |
| **No restrictions** | 1 | ⛔ 已标「只进 prompt 不入画」 | `bg4.ref07`（Flickr Commons 口径，`ref_fetch` 保守判为非开放，保留该保守判定） |

### ② ShareAlike 会传染到成片——3 张 CC BY-SA 现代照片单列

`bg3_pudding_lane_street` 的 `ref19 / ref20`（CC BY-SA 4.0）与 `ref21`（CC BY-SA 3.0）是 **Staple Inn（1585 年建、躲过 1666 大火的伦敦木构架实物）现状照**。
它们在本库里质量最高——**已经是照片**，直接给 img2img 当木构架/悬挑楼层质感底子最省事。
但 **ShareAlike 的传染性对成片是实打实的法律风险**：拿 CC BY-SA 图做 img2img 生成的画面属于演绎作品，理论上整条片子要以同样许可释出。
**处置：标为「只进 prompt 不入画」**，即只用作作者读图写文字描述的依据，不进 Seedance 上传槽。
`ref22`（CC BY 2.0，同一处建筑）没有 SA 条款，**可以入画，署名即可**——需要照片级木构架底子时优先用它。

### ③ 「现代摄影 / 扫描件另有主张」这一条的实际落点

任务书提醒 17 世纪原作过期 ≠ 扫描件公版。本库实测：

- **Met / Rijksmuseum / Yale Center for British Art** 明确以 **CC0** 释出扫描件（它们主动放弃了对扫描件的任何主张），**可以放心**。
- **Wellcome Collection** 以 **CC BY 4.0** 释出——它**确实对扫描件主张了权利**，只是给了宽松许可。**必须署名**，不能当 PD 用。
- **本库未取 Royal Collection Trust 与大英博物馆的图**。两家的网站条款都不是无条件公版（BM 对图像另有非商业条款、RCT 更严），
  **按任务书要求没有默认公版、直接跳过**；Commons 上少数标注来源为 BM 的 `Mechanical Curator` 图（3 张）走的是 British Library 的 PD 释出，与 BM 馆藏条款不是一回事，已按 Commons 标注如实记录。
- **Commons 逐图确认已做**：许可字段直接取自各图 `extmetadata.LicenseShortName`，不是我推断的。

---

## 4. ⚠️ 与仓库现行规则的冲突（需要 parent 裁决 + divergence note）

**`ai_video.md` rule 18.1（2026-09-16，sk1 follow-up 014）明文规定：**

> 「画类参考图会把画风带进画面，文字否定挡不住……**修法**：画类史料降级为**作者对账**（`ref/` 照存、`refs.md` 照索引、形制词对账表照引用），**不进上传窗口**；上传位只给世界锚点、地点锚点与**照片类参考**。」

**本站的工艺决定（用户 2026-09-18）与之相反**：把公版历史图**直接**做 img2img、保原图完整性。

**这两条并不是简单的新旧覆盖，而是两种不同用法，值得写清楚再决定：**

| | rule 18.1 禁止的 | sk3 要做的 |
|---|---|---|
| 图的角色 | **形制参考**——配一段文字 prompt 去生成一个**新构图** | **构图本身**——把这张画「翻译」成照片 |
| 风格吸收 | 是 bug：不想要版画/绢本的笔触混进写实画面 | 是**前提**：本来就要保留这张图的构图、透视、建筑排布 |
| 失败模式 | 出来「像画的亲戚」 | 出来「不像原图」 |

**结论建议**：rule 18.1 的判断在它的语境里是对的，**不应因 sk3 而修改全仓规则**；
应按 CLAUDE.md「项目 spec 可覆盖 project-scoped ref，附 divergence note」的口子，在 `specs/ai_video/sk3/` 写一条 divergence：
**sk3 的场景/建筑/全景类 shot 走「历史图 img2img」，rule 18.1 的「画类不进上传窗口」在本站不适用；但 rule 18.1 仍适用于本站的人物锚点**——
人物走 Hollar/Laroon 版画 img2img 会把版画线条带进脸，那正是 18.1 说的坑（详见 §15b 第 7 项）。
**即：本站按「地点/建筑 = img2img，人物 = 文字 + 照片类参考」分流，而不是全站一刀切。** 这一条请 parent 在 dossier §15 里明确。

---

## 5. 工具问题（两个，其一是真 bug）

### ① 🔴 `tools/ref_fetch.py pull` 不是并发安全的——同一 `asset_dir` 并行跑会互相覆盖

**复现**：对同一个 `asset_dir` 同时起两个 `pull` 进程（我为了省时间这么做了），结果：

- `bg3_pudding_lane_street`：22 个文件，`refs.md` 只有 21 条，其中 `ref06/10/11/12` **四个编号各被两个文件共用**，1 个文件完全没进索引；
- `dress_restoration_1660s`：26 个文件里 `ref10/11/12/13/15/16` **六个编号重复**。

**根因**（`ref_fetch.py`）：

- `_next_index()` 扫目录取 `max+1`，是 **read-then-write**，两个进程会读到同一个 max；
- `append_ref()` 是对 `refs.md` 的 **read-modify-write**（`text[:text.rindex("```")] + entry`），后写的进程会把先写的那条**整条吃掉**。

**本次处置**：两个资产**整目录删掉重下**，改为**串行**跑（同一 `asset_dir` 内的多组 `use` 依次执行），复检 130 条全部一一对应、零重号。
**给后续 worker 的硬规则：不同 `asset_dir` 可以并行，同一个 `asset_dir` 必须串行。**
若要根治，建议给 `pull` 加一个 `asset_dir/.lock` 文件锁——但这是改公共工具，**没有动，留给 parent 决定**。

### ② 🟡 `pull` 下的是 MediaWiki 缩略图，不是原始底片（上限 3840px）

`_commons_pages()` 固定传 `iiurlwidth=2000`，`pull` 取 `thumburl`。对小于该尺寸的文件会回落到原图，所以 **125 张里 109 张拿到的就是原尺寸**；
但**16 张被截到 3840px**，其中一张是本站最要紧的图：

| 条目 | 原图 | 盘上 | 损失 |
|---|---|---|---|
| **`bg0_london_panorama.ref01` Hollar 1647 长卷** | **28661×5560** | 3840×1280 | **7.5×**，摊在九英尺长卷上等于每栋房子只剩几像素 |
| `bg1_london_bridge.ref02` de Jongh 油画 | 7193×3177 | 3840×1696 | 1.9× |
| `thames_watermen.ref08` Visscher 摹本 | 6852×8364 | 3840×4687 | 1.8× |
| 其余 13 张 | 4300–6900px | 3840px | ≤1.8×，**对 img2img 够用**（多数模型输入 ≤2048） |

**本次处置**：只对 1 号图补救——直接从 `upload.wikimedia.org` 抓了**未经任何处理的原始底片**存为
`0_research/masters/hollar_1647_longview_master_28661x5560.jpg`（76.4 MB，已校验 28661×5560），并在该资产 `refs.md` 顶部写明。
**它刻意放在 `refs/` 树之外**：5.15:1 超出 rule 17.7 的 1:3–3:1 窗口，留在 `ref/` 里会被 `ref_aspect fix` 补边成 28661×9554（2.74 亿像素）而毁掉。
现 `python tools/ref_aspect.py check refs/` 为 **0 outside**。
其余 15 张判断为够用，没有重抓。

### ③ 网络不稳（不是 bug，但会咬人）

整个任务里 Commons/Met 的 TLS 握手超时约 10 次（`_ssl.c:989: The handshake operation timed out`）。
`ref_fetch.py` 的 `search` 在多 query 模式下**一个 query 抛异常会带走整个进程**（后面的 query 全不跑，且已取到的结果不落盘）。
我在外面套了一层重试驱动才跑完。**后续 worker 建议一次只跑一个 query，或自带重试。**

---

## §15b · image-to-image 可用性评估（阶段 2 建卡的直接依据）

**判读口径**（四问，逐资产回答）：
① **分辨率够不够**——img2img 的有效输入普遍 ≤2048px 长边，故**长边 ≥1500px 即够用**，≥3000px 有余量可局部放大重绘。
② **是版画线条还是有明暗层次**——这是本站最吃重的一问。**蚀刻/铜版（line etching）只有黑白线条、没有连续调**，
img2img 会把线条当成纹理，出来是「线描感的照片」；**油画/水彩有连续明暗**，img2img 转照片级几乎是顺水推舟。
③ **视角能不能用**——是不是本站镜头要的机位（航拍 / 平视 / 内景）。
④ **要不要先拼接或切片**。

**全局结论：本库 130 张里，104 张长边 ≥1500px；但媒介上 100 张左右是铜版蚀刻线条、只有约 12 张是油画/水彩。
这意味着「img2img 保原图完整性」这条路在本站要分两种打法——见下面每个资产的「打法」一行。**

> **通用打法 A（线条版画）**：版画不能一步到照片。走**两步**——先 img2img **低 denoise（0.25–0.4）+「转为写实照片」**把线条压成灰阶体块，
> 再以第一步的产出为输入做第二步、提高 denoise 补材质与光。单步高 denoise 会丢掉建筑排布（等于白喂），单步低 denoise 会留一脸线。
> **通用打法 B（油画/水彩）**：一步 img2img，denoise 0.35–0.5，直接出照片级。

---

### 1 · `bg0_london_panorama` 整城全景 — **✅ 可用，且是本站最强的一张牌**

- **分辨率**：`../masters/hollar_1647_longview_master_28661x5560.jpg`（**28661×5560，未经处理**）。这是全库分辨率天花板。
  `ref/` 里的 `ref01` 是 3840px 补边副本，**img2img 不要用它，用 master**。
- **媒介**：**铜版蚀刻线条**（走打法 A）。1666 双联 `ref05/ref06`（Yale，CC0）同。Visscher 1616（`ref08/ref10`）亦为版画。
- **视角**：从 Southwark St Saviour 塔上南岸平视北望——**正是片头航拍长镜的落幅机位**，不需要换视角。
- **要不要切片**：**必须切**。28661px 长卷不能整张喂，按原六块版的分块**切成 6–8 段各约 3600–4800px 宽**分别 img2img，
  再在出片端横向拼回；接缝落在原版的分块线上最省事。**这也正好对应片头长镜的分镜**。
- **额外价值**：`ref05/ref06` 是 Hollar 1666 的**火前/火后同框双联**，片尾对照镜可以直接用同一张图的上下两半，构图天然对齐。
- ⚠️ `ref11`（600×400）、`ref09`（1278×589）偏小，只作对账。

### 2 · `bg1_london_bridge` 旧伦敦桥 — **✅ 可用，是全库里 img2img 最省事的一组**

- **媒介**：**这一组有油画**——`ref02` **Claude de Jongh《View of London Bridge》1632（7193×3177）** 是本库最理想的 img2img 输入：
  有完整明暗层次、有大气透视、有水面反光，**走打法 B 一步到位**。`ref03` 是同画家 1630 年版但只有 944×315，只作对账。
- 线条组：`ref01` Visscher 1616（桥上房屋最清晰）、`ref04` 1682、`ref05` 1724 西立面——走打法 A，用于**核对房屋数量与开间节奏**。
- **视角**：de Jongh 是**河面平视、桥身横贯画面**，适合本站的河上镜与桥全景镜；`ref05`（1724 西侧立面）是**正投影式立面**，
  **不适合 img2img，但是白模建桥的最佳图纸**。
- **年代校正（重要）**：`london1666.city.008` 记 1633 年火烧掉桥**北端**房屋、**到 1666 年仍未重建**。
  **Visscher 1616 与 de Jongh 1632 都画在那场火之前，桥北段是满的**——img2img 出来会是「北段有房」的错误状态。
  **建卡时必须在 prompt 里写死「桥北端自 St Magnus 起一段为空缺、只钉木板」，或在切片时避开北段**。这是本资产最大的坑。

### 3 · `bg2_old_st_pauls` 旧圣保罗 — **✅ 分辨率与覆盖最好，但全是线条**

- **分辨率**：15 张里 12 张 ≥3000px，`ref10` 平面图 5972×4330。**够用有余**。
- **媒介**：**全部是 Hollar 1658 铜版蚀刻**（Dugdale 那套），一张油画都没有——**必须走打法 A 两步**。
- **视角覆盖是全库最完整的**：西立面 `ref01`（**带 Inigo Jones 科林斯门廊**，`london1666.city.019`）、北立面 `ref02`、南立面 `ref03`、
  东端 `ref04/ref05`、中殿 `ref06`、唱诗席 `ref07`、唱诗屏 `ref08`、议事堂 `ref09`、地窖 `ref11`、**平面图 `ref10`**。
  **内景与外景都有，这在本库里是独一份**——「Paul's walk」市井内景镜（`london1666.city.022`）有直接依据。
- **1666 年状态已对上**：无尖顶（1561 年雷击后未重建，`london1666.city.018`）+ 有门廊，Dugdale 1658 正是这个状态。
- **切片**：立面图整张可直接喂；`ref10` 平面图**不是 img2img 素材，是白模图纸**。
- ⚠️ `ref13`(806×640)、`ref14`(600×950) 偏小，只作对账。

### 4 · `bg4_royal_exchange` 皇家交易所 — **🟡 可用但偏薄，内院只有一张一手**

- **分辨率**：`ref09`（Met，3541×2084）与 `ref01`（3580×2116）够用；`ref03`(400×309)、`ref04`(980×616) 偏小。
- **媒介**：Hollar 铜版（打法 A）。`ref06`（Wellcome，CC BY 4.0，2454×3564）是**立面测绘图**，做白模用，不做 img2img。
- **要害**：**火前内院（商人聚集的拱廊中庭）实质上只靠 `ref09`/`ref08`《Byrsa Londinensis》这一个母本**，
  其余多是同一母本的后世翻刻（`ref05` 1887、`ref10` 1887）。**独立一手视角只有 1–2 个**，
  想要别的机位只能靠白模补，**不能指望 img2img 变出新角度**。
- `ref07` 是 1854 年平面图且许可为 `No restrictions`（已标⛔），**只作平面对账**。

### 5 · `bg3_pudding_lane_street` 街景与民居 — **✅ 张数最多，但要分三堆用，别混**

这个资产里其实装了三种完全不同的东西，**阶段 2 建卡时应当拆成三张卡**：

- **(a) Hollar 伦敦宅邸/街景铜版**（`ref02–ref05`，其中 Arundel House 南北两张各 6400×2800）——
  **这是唯一的「火前伦敦真实街面」一手**，但画的是河畔贵族宅邸，**不是布丁巷那种窄巷民居**。打法 A。
- **(b) Laroon《Cryes of the City of London》1687–88**（`ref06–ref18`，Rijksmuseum CC0，多数 ≥3000px）——
  **单人立像、背景极简**。这类图 **img2img 出整条街是不可能的**，它的正确用法是
  **抠出人物姿态/担子/货品/衣着，作为群众层的贴片或文字描述依据**（`london1666.work.028/029/030`）。
- **(c) Staple Inn 现状照**（`ref19–ref22`）——**全库仅有的照片类参考**，木构架/悬挑楼层质感直给。
  但 `ref19/20/21` 是 **CC BY-SA，建议只进 prompt 不入画**（§3 ②）；**`ref22` 是 CC BY 2.0，可入画、署名即可——要照片底子就用它**。
- **缺口（诚实说明）**：**没有任何一张「1666 年布丁巷式窄巷民居街景」的同时代图像存世**——
  火烧掉了实物，火前也没人画过平民窄巷。这不是我没找到，是史料本身的空白。
  **街景只能靠 (a) 定形制 + (c) 定质感 + 白模定街宽（`london1666.housing.007` 禁 jetty 法条反推火前形态）三者合成**，
  **不存在可以直接 img2img 的布丁巷原图**。这一条请务必写进 dossier，避免阶段 2 反复找。

### 6 · `bg5_great_fire` 大火图像 — **✅ 可用，而且这一组油画最多**

- **媒介优势**：`ref05` Verschuier《火》(5870×3573)、`ref06/ref07`《The Great Fire with Ludgate and Old St Paul's》(5138×6224)、
  `ref08` 1675(5477×3189) 都是**油画**——**火光、烟、水面反射的明暗层次齐全，走打法 B 一步出照片级**，是全库 img2img 最容易出彩的一组。
- `ref02/ref03`（Met CC0）是 **Hollar 火前/火后同框双联**（3918×735，已补边到 3:1），**片尾对照镜直接可用**，但需按上下两半切开。
- `ref04` Hollar《圣保罗焚毁》、`ref11`《火后废墟》(3188×2236) 给火后镜。
- ⚠️ `ref10`(200×200)、`ref12`(300×187 火灾水龙) **太小，只能作对账**，不要喂 img2img。
- **注意**：这一组的用途是**片尾与火后复盘**。本站主线是**大火前一夜**，画面里**不应出现火**——
  与 `ai_video.md` 16.9「痕迹 vs 正在发生」同理，这批图误进阶段 2 的场景卡会把火烧进火前镜。**建卡时须隔离到单独的「片尾」卡**。

### 7 · `dress_restoration_1660s` 服饰 — **🔴 按 rule 18.1 办：不做 img2img，只作文字依据**

- **分辨率与覆盖极好**：26 张，17 张 ≥3000px，Rijksmuseum CC0 为主。
  Hollar《Ornatus Muliebris Anglicanus》1638–40 英国女装 + 《Theatrum Mulierum》1643–44 的
  **伦敦市民之女 / 伦敦商人之女 / 英国贵妇**三档分层（`ref02–ref05`）+ 1665 英国时装系列扉页（`ref01`）+ Laroon 平民档（`ref19–ref26`）。
- **但这一组是全库里最不该做 img2img 的**：**人物锚点走版画 img2img，会把铜版线条直接刻进脸**——
  这正是 `ai_video.md` rule 18.1 说的坑，且人脸对线条污染的容忍度远低于建筑。
- **正确用法**：作者读图 → 写成**锁定描述符文字**（按 rule 17.6「锁定串必带『不是 X』」模板）→ 文字进 prompt，**图不进上传槽**。
- **年代缺口须标注**：主力图录是 **1638–44**，比 1666 早 **22–28 年**。
  男装的 petticoat breeches 是 **1660 年复辟才随查理二世从法国带回来的**（`london1666.dress.004`），
  **Hollar 1640 年代的图里不可能有**；`ref01` 的 1665 系列与 Laroon 1688 才贴 1660 年代。
  **男装在本库里实质缺一手同时代图像**——建议阶段 2 补 Lely / John Michael Wright 的 1660 年代肖像（另找，本次未取）。
  这是本资产唯一的实质缺口。

### 8 · `thames_watermen` 泰晤士河 — **🟡 勉强达标（8 张），是全库最薄的一环**

- **能用的只有 3–4 张**：`ref02` Hollar 白厅河景(6715×3019)、`ref01` 兰贝斯宫河景(Met CC0,3886×2160)、`ref03` 伦敦塔(3667×2127)、
  `ref08` Visscher 摹本(6852×8364)。`ref04`(800×494)、`ref05`(600×371) 太小；`ref06` Hondius《冰冻泰晤士河》1920×1187 **是油画、可用打法 B**，但只此一张。
- **要害缺口**：**没有一张「泰晤士河客运摆渡 wherry 近景」的一手图像**。
  已注册的事实很扎实（`london1666.transport.006` 河为主干道、`.008` 冲桥危险、`.011` 约 2000 条 wherry、`work.017` 船夫行会两年学徒），
  **但都是文字，没有对应的画面**。船夫近景镜**只能靠全景图前景里的小船放大 + 白模补**。
- **已排除一个陷阱**：Commons 搜 "wherry" 会大量返回 **Norfolk wherry（诺福克运货帆驳）**，
  与泰晤士河**客运摆渡 wherry 是完全不同的船**，已全部剔除、未入库。后续 worker 请勿再踩。
- **建议**：若阶段 2 要做船夫镜，优先从 `bg0` 的 **28661px master 前景**切出河面船只局部——那是分辨率足够、且年代与视角都对的唯一来源。

### 9 · `map_london_1658` 地图 — **✅ 达标，但地图本来就不做 img2img**

- `ref01` Faithorne & Newcourt 1658（2641×2182）是**火前街道骨架**的一手；
  `ref04/ref05` Hollar 火前/火后对照平面（6940×2275）**同时给出火毁范围**；`ref06/ref07` 荷兰刻本《被焚伦敦平面图》1666。
- **用途不是 img2img，是白模与走位的底图**：整城白模的街道网、布丁巷位置（`london1666.city.011`）、
  泰晤士街走向（`.014`）、老天鹅码头在桥上游（`.015`）都从这里量。
- `ref08–ref10` 是**火后重建方案**（Evelyn / Wren），**与 1666-09-01 无关，只作片尾「后来怎么了」的资料**，不要混进火前场景。

---

### §15b 汇总：三条给阶段 2 的硬结论

1. **能一步 img2img 出照片级的只有约 12 张油画**（de Jongh 桥、Verschuier 与 Ludgate 两张火、Hondius 冰河等）。
   **其余约 100 张是铜版线条，必须两步走（打法 A）**，请把这一步写进阶段 2 的出图 SOP，否则第一批图会全是「线描感照片」。
2. **人物不走 img2img**（§15b 第 7 项）。**地点/建筑走 img2img，人物走文字锁定串 + 照片类参考**——
   这条分流就是 §4 那个规则冲突的落地答案。
3. **两个史料空白必须提前认下来，别让阶段 2 反复找**：
   **(a) 布丁巷式窄巷民居没有同时代图像**（§15b 第 5 项）；**(b) 泰晤士河客运 wherry 没有近景一手**（§15b 第 8 项）。
   两者都只能靠「全景图切局部 + 白模 + 文字」合成。
