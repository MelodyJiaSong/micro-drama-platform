# 对抗熵增 · Ferrari F80 品牌广告片

**105 秒 / 2.35:1 / 3840×2160 / 25fps / 61 镜 / 无对白**

- **task_name**：`duikang_shangzeng`（pinyin；中文名《对抗熵增》）
- **task_type**：`ai_video` ／ **sub_type**：`short`（单片广告）
- **主体**：Ferrari F80（2026 旗舰 hypercar，1200 马力）
- **当前阶段**：阶段 1–3 已完成；阶段 5–6 已出 3 个样板镜（14 / 20 / 60），其余 58 镜待产

---

## 一句话

在一座正在滑向热寂的城市里，唯一还在加速的东西，让世界重新开始动。
而观众跟了 105 秒的那匹马，**一直是车标**。

---

## 目录导航

| 路径 | 内容 |
|---|---|
| `0_参考资料/` | 原始素材：拍摄通告 PDF、分镜 PDF、竞品成片 `0710_v1.m4v` |
| `1_立项/concept.md` | **立项策划单 + 全片策略**（先读这个） |
| `1_立项/benchmark_teardown.md` | **竞品实测拆解**——8 条可测量缺陷与对应硬指标 |
| `2_世界观人设/world.md` | 熵增法则视觉规则书（什么瓦解、怎么瓦解、怎么复原） |
| `2_世界观人设/style_guide.md` | 双色系统、五幕调色表、节奏与声音规格、标准负面词串 |
| `2_世界观人设/props/f80_ferrari/` | **车型锁定描述符 + Seedream 参考图 prompt + Blender 白模规格** |
| `2_世界观人设/props/cavallino_horse/` | 那匹马（全片唯一暗线） |
| `2_世界观人设/characters/driver/` | 驾驶者（只给手 / 眼 / 侧脸 / 背影） |
| `2_世界观人设/scenes/` | 熵增都市 / 中世纪石板路 / 冰原冻湖 |
| `3_大纲/arc_outline.md` | **故事大纲 + 61 镜分镜总表**（含每镜时长、焦段、运镜） |
| `5_6_分镜与prompt/previz_plan.md` | **Blender previz 方案**（18 个镜头需要，含 TOML 示例与接线待办） |
| `5_6_分镜与prompt/shots/shotNN/` | 逐镜自包含文件（Shot context + 可直接复制的 prompt） |

---

## 使用说明（怎么把这些文件变成片子）

### 第一步 · 出参考图（Seedream）
1. 打开 `2_世界观人设/props/f80_ferrari/f80_ferrari.md` §3，
   逐条生成 6 张车型参考图（`3q_front` / `side` / `rear` / `front` / `badge` / `cockpit`）。
2. 同法生成 `cavallino_horse`（真马 + 青铜像 2 张）与 `driver`（眼 / 手 / 侧脸 3 张）。
3. 场景板按 `scenes/*.md` 的锁定描述符各出 1 张。
> **这一步是全片一致性的地基，务必先做完再动视频。**

### 第二步 · 出 previz（Blender，**61 镜全做**）
四步工序：**写 TOML → 出 .blend → 渲 MP4 → 上传当 reference_video**。
previz 管主干动作与人物物品位置，Seedance 管全部细节渲染与特效。
61 份 `previz_config.toml` 骨架已生成（`tools/gen_previz_scaffolds.py`），逐镜手调 TODO 后：
```bash
blender -b --factory-startup --python tools/previz/build_previz.py -- <shot>/previz_config.toml
python tools/whitemodel_to_mp4.py <shot> --fps 25 --project duikang_shangzeng
```

### 第三步 · 出片（Seedance 2.0）
打开 `shots/shotNN/shotNN.md`：
- **正向**：复制 `## 视频 prompt` 里的 ```text 代码块，整块粘进 prompt 框。
- **反向**：复制「反向提示词」代码块，粘进 **negative prompt 框**（不要并进正向）。
- **参考位**：按该镜「Reference uploads」表上传（图片 1–4 + 视频 1）。
- 比例选 **21:9**，时长按 `时长:` 字段。

### 第四步 · 剪辑
每镜按「剪辑说明」里的**成片用段**取片。总表见 `3_大纲/arc_outline.md`。
成片 pad 到 3840×2160（上下各 264px 黑边）。

### 第五步 · 混音
目标 **-14 LUFS / LRA ≥ 12**；第 43 镜处必须有 **≥1.0s 近静默**，第 44 镜是全片最大声。

---

## 角色 / 资产清单

| 资产 | 说明 | 出场 |
|---|---|---|
| `f80_ferrari` | Ferrari F80，Rosso Supercar 红。**全片唯一饱和主体** | 全片 |
| `cavallino_horse` | 一匹纯黑骏马。铜像 → 活马 → 并驾 → 粒子 → **车标** | 全片暗线 |
| `driver` | 驾驶者「她」。只给手 / 眼 / 侧脸 / 背影 | 4 次 |
| `entropy_city` | 熵增都市（广场 / 主街 / 高架 / 隧道） | Ⅰ Ⅱ Ⅳ Ⅴ |
| `medieval_road` | 中世纪石板路 | Ⅲa（11.5s） |
| `ice_plain` | 冰原冻湖。**封面首选场景** | Ⅲb（14.5s） |

---

## 风格关键词

灰烬色世界 · Rosso Supercar 红 · 唯一饱和主体 · 失色失序失速 ·
无方向光 · 逆光金尘 · 镜面冰原 · 电影级汽车广告实拍 · 35mm 胶片颗粒 ·
2.35:1 横向构图 · 零字幕 · 无对白

---

## 待用户裁定

1. **Tagline 四选一** —— 见 `1_立项/concept.md` §六（推荐 A：**熵，只输给速度。**）
2. **第Ⅳ幕是否加 1 句 OS** —— 见 `characters/driver/driver.md` §五（默认不加）
3. **F80 三维模型取得方式** —— 见 `previz_plan.md` §三（推荐方案 A：购买现成高模）
