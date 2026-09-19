# Moorfields木偶戏棚 · Seedance 主体

> **本卡由 `tools/gen_sk3_assets.py` 生成——改卡＝改生成器重跑**（rule 4i ①）。手改会在下次 `--check` 时被发现。

**Place × State**：`城墙外北侧的 Moorfields 空地` × `1666-09-01 下午 · 白天 · Polichinelly 演出中`

**图集落点**：本目录。每张图导入后按其路由键落在 `bg8_Moorfields木偶戏棚/bg8-N.png`——同目录多图互不覆盖，重导只覆盖同名那一张。历史参考图在 `ref/`，索引 `refs.md`。

---

## 这个主体是干什么的

娱乐段，也是皮普斯线的可视化落点：他带着妻子与 Mercer 来看戏，**撞见 Young Killigrew 一伙、吓得躲起来**（`timeline.*` T0）。Polichinelly 就是潘趣的前身，这是英格兰最早的潘趣演出记录之一。

---

## 锁定描述符（跨镜 byte-identical，自然色名无 hex）

| # | 字段 | 值 |
|---|---|---|
| 1 | 类型 / 时代 / 室内外 | 1666 年伦敦城外空地上的临时木偶戏棚，室外 |
| 2 | 空间结构 + 方位 | 开阔草地上支起一座布幔木偶棚，观众三面围站；机位在观众后侧朝棚看 |
| 3 | 主要建筑或自然元素 | 木架布幔戏棚、远处的城墙与塔林轮廓、空地上的树 |
| 4 | 标志道具或装饰 | 木偶棚的小台口、围观人群、卖吃食的挑担 |
| 5 | 默认光源 / 时辰 | 下午：开阔地，光平均、没有窄巷的压迫感 |
| 6 | 配色（自然色名） | 主：草绿、风化木褐、布幔的褪色条纹；辅：sadd colours 的人群衣着；点缀：远处塔林的灰 |
| 7 | 氛围关键词 | 开阔、松、笑声、跟城里两种空气 |
| 8 | 一句话锁定 | 城外草地上一座布幔木偶棚，三面围站的人在笑 |

**锁定串必带「不是 X」**：**不是**室内剧场；**不是**维多利亚式的潘趣与朱迪摊（形制要早得多）；棚上**不出现文字招牌**

---

## img2img 工艺（D7 / dossier §15b）

**两步走**；底本弱，主要靠文字 + `bg0` 基调继承。

## 参考图依据

| ref_id | 用的局部 | 证明的 fact_id | 进 `参考:` 槽 |
|---|---|---|---|
| `bg3_pudding_lane_street.ref03` | Laroon《Cryes》1687：街头表演与围观人群的形态 | `custom.*` | ⚠️ 晚 21 年，只看姿态与棚的做法 |

## 形制词对账（每个可截图指认的形制 → fact_id）

> fact_id 不进 prompt 块，全部在本表对账。

| prompt 里的形制词 | fact_id | tag |
|---|---|---|
| Polichinelly 木偶戏（潘趣前身） | `london1666.timeline.*` | ✅ T0 皮普斯 9/1 逐字 |
| 皮普斯在此躲 Young Killigrew 一伙 | `london1666.timeline.*` | ✅ T0 |

## 已知空白（不编，显式留着）

⚠️ 1666 年木偶戏棚的确切形制无直接图像（Laroon 晚 21 年）——按 ⚠️ 推测处理，片中不做形制断言。

---

## 锚点图 prompt

> 首行是路由键（rule 4b-A）——出图工具按 prompt 前几个字命名下载，键不在首位，图就落不回本目录。

```text
bg8-1_Moorfields木偶戏棚锚点

场景: 城墙外一片开阔草地上支着一座临时的木偶戏棚：木架子上蒙着褪色条纹布幔，上方开一个小小的台口，木偶在台口上方活动；三面围站着看戏的人，穿赤褐、枯叶褐、茶褐这类暗沉的日常色，有人在笑；边上有挑担卖吃食的；远处是城墙与城里密集的塔林轮廓，罩在褐灰的霾里

光线: 下午开阔地的平均光，云影缓慢移过草地
反向声明: 画面里没有任何火、没有任何暖色人造光源、天没有暗下来；空气里没有烟、没有落灰

摄影: 35mm 球面镜头，中等光圈，自然景深，手持
做旧: 木头有干裂与手泽，砖有烟熏与雨痕，布有洗旧与磨边，瓦有苔与缺角；所有痕迹都是**早已结束的冷状态**，不冒烟、不发光、不发烫

渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9

负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

**参考上传**（裸 `=>@` 占位，**绝不代填槽位号**）：

- （本主体无上传项：见上「img2img 工艺」——纯文字自由生成）

**参考用法**：历史原图只用于**保留原构图的 img2img**，不是风格参考（rule 18.1b）；**人物与面孔一律不进上传槽**——版画线条会刻进脸。
