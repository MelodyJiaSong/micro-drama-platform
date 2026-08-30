# 《对抗熵增》制作流程 — Step 1 → Step 16

> 从当前状态走到 105 秒成片的**完整线性步骤**。
> 每步标了「谁做」和「现在到哪了」。**上一步没完成，不要开始下一步**（标了 ⚠ 的依赖尤其硬）。

---

## 阶段 A · 资产就位（一次性，全片只做一遍）

### Step 1 · Prompt 1 — F80 全景图 ｜ 你 ｜ ⬜ 未做

**纯文字，不挂任何 reference。** 前方偏右 45° 四分之三前侧、棚拍完整车身。

- prompt 全文 + 8 条验收清单：`props/object_build_flow.md` Prompt 1
- 产物存 `props/f80_ferrari/ref_images/f80_ferrari_全景.png`

> **反复重跑到过完 8 条验收为止。** Step 2 的三张、Step 3 的白模全部从它派生——
> 它错一点，后面四个全错。

---

### Step 2 · Prompt 2/3/4 — 正面 / 侧面 / 背面 ｜ 你 ｜ ⬜ 未做 ｜ ⚠ 依赖 Step 1

**三张都挂图1 当 reference**（星形，不是链式：图3 不参考图2）。

- 三条完整 prompt + 共用负面词：`props/object_build_flow.md` Prompt 2 / 3 / 4
- 产物存 `ref_images/f80_ferrari_{正面,侧面,背面}.png`

> 相机距离恒定 → 正面看起来比正侧小，**这是对的**，别为了填满画面拉近。
> 四张并排验轴距/离地/车高/漆色/轮毂；单张不一致只重跑那一张。

---

### Step 3 · Prompt 5 — 由图生白模 ｜ 我 ｜ 🔄 **闸门已建，等 mesh 来源** ｜ ⚠ 依赖 Step 1

**Prompt 5 是给 Claude 的，不是给出片模型的。** 整段贴给我即可，正文见
`props/object_build_flow.md` Prompt 5。

主参考 = 图1；图2/3/4 若已出好一并传入作补充视角。
→ `mcp__blender__generate_hyper3d_model_via_images` → 轮询 → 导入
→ 四步归一化（车头 +Y ／ 2.06×4.84×1.14 m ／ 原点落底面中心 ／ 清材质留灰模）
→ 覆盖 `props/f80_ferrari/f80_ferrari.blend` → 重跑下游两条命令：

```bash
blender -b --factory-startup --python tools/render_object_turntable.py --     --blend ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/f80_ferrari.blend     --out   ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/whitemodel     --name  f80_ferrari
# 61 份 previz 配置全部指向这个 .blend，一个配置一个 prompt 都不用改
blender -b --factory-startup --python tools/previz/build_previz.py -- .../shotNN/previz_config.toml
```

> **白模的职责变了**：不再是出图前的结构参考（图已先出好），
> 只做**出片前的运镜/走位工具**——逐镜 previz 的 `reference_video`。

---

### Step 3b · object 二 · 车的内饰 ｜ 你 + 我 ｜ ⬜ 未做 ｜ ⚠ 等 Step 1–3 全部完成再开

**流程与 object 一 完全一样，同样 5 个 prompt**：
prompt 1 无 reference 出内饰全景 → prompt 2/3/4 挂图1 出三角度 → prompt 5 给 Claude 生白模。
届时按同一结构落 `props/{内饰对象名}/`。

服务镜头：11（起动旋钮）· 12（仪表亮起）· 43（手悬拨片）· 44（扣下拨片）· 45（指针砸红区）。

---

### Step 4 · Seedream 出其余参考图 ｜ 你 ｜ ⬜ 未做

| 资产 | 张数 | prompt 出处 |
|---|---|---|
| 马（真马 + 青铜像） | 2 | `props/cavallino_horse/cavallino_horse.md` §4 |
| 驾驶者（眼 / 手 / 侧脸） | 3 | `characters/driver/driver.md` §6 |
| 场景板（熵增都市 4 板 / 中世纪 / 冰原） | 6 | `scenes/*.md` 锁定描述符 |
| 车徽微距 `badge`（落版 shot60） | 1 | `props/f80_ferrari/f80_ferrari.md` §3.4 |

> 与 Step 1–3 互不阻塞，可以并行做。

---

### Step 5 · 上传 Seedance，建立对象 ｜ 你 ｜ ⬜ 未做 ｜ ⚠ 依赖 Step 2+3+3b+4

把**身份包**整包上传，建立三个对象：

- **f80_ferrari** = 图1 全景 + 图2/3/4 正侧背（共 4 张）＋ Step 3 产出的转盘 MP4
- **内饰对象** = Step 3b 的 4 张
- **cavallino_horse** = Step 4 的 2 张
- **driver** = Step 4 的 3 张

> ⚠ **这一步没做完，绝对不要开始 Step 10 出片** —— 对象没建立，每镜的车都是不同的车。
> 这正是竞品车型漂移的原因。

---

## 阶段 B · 分镜就位（逐镜 61 次）

### Step 6 · 写完 61 个 shot prompt ｜ 我 ｜ 🔄 **21 / 61**

已出：**第Ⅰ幕全 9 镜 + 第Ⅱ幕全 11 镜**（shot01–20，2026-08-30 补齐 02–13 / 15–19）
＋ `shot60`（车徽揭示）
待出：其余 40 个（第Ⅲ幕 21–41、第Ⅳ幕 42–52、第Ⅴ幕 53–59+61）

每个 `shotNN.md` 含：画面速写 / Shot context / 视频 prompt（≤2000 字）/ 反向提示词 / 剪辑说明 / previz 指向

---

### Step 7 · 逐镜手调 previz 配置 ｜ 你＋我 ｜ 🔄 **1 / 61**

61 份 `previz_config.toml` 已生成且**全部通过 Blender 自检**，但它们是**能跑的骨架，不是能用的成品**。
每镜要手调三类值（配置里标了 `TODO`）：

1. **`方位角`** —— 决定谁在画左谁在画右（马必须恒在画左）
2. **`占画高` / `横向偏移`** —— 决定构图，多主体同框时尤其要调
3. **`[[道具."关键帧"]]` 的 `t` 与 `位置`** —— 决定动作时刻表

> 已调好的范例：`shots/shot25/previz_config.toml`（占画高 0.35→0.24、横向偏移 0→0.20、方位角 25→40）
> **这一步无法自动化。** 骨架保证合法与参数自洽，构图判断只能人做。

---

### Step 8 · 逐镜渲 previz MP4 ｜ 命令 ｜ 🔄 **1 / 61**

```bash
blender -b --factory-startup --python tools/previz/build_previz.py -- \
    ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shotNN/previz_config.toml
```

产出：`shotNN_previz.blend`（可打开手改）＋ `shotNN_previz.mp4`（2560×1090 / 25fps）

> Blender 无 FFMPEG 时退回 PNG 序列，用这条收尾：
> `python tools/whitemodel_to_mp4.py shotNN --fps 25 --project duikang_shangzeng`

---

### Step 9 · 对齐时刻表 ｜ 我 ｜ ⬜ 未做 ｜ ⚠ 依赖 Step 6+7

`previz_config.toml` 里关键帧的 `t` **必须**与 `shotNN.md` 里 `动作:` 字段的 `0-2s` / `2-4s` 分拍逐拍一致。
previz 是动作时刻表的唯一真相，prompt 抄它。**两处不一致 = blocker。**

---

## 阶段 C · 出片（逐镜 61 次）

### Step 10 · Seedance 生成 ｜ 你 ｜ ⬜ 未做 ｜ ⚠ 依赖 Step 5+6+8

每镜打开 `shotNN.md`，按「Reference uploads」表填五个位：

| 位 | 内容 |
|---|---|
| **视频1** | `shotNN_previz.mp4`（Step 8） |
| 图片1 | 本镜视角的**写实车图**（Step 3） |
| 图片2 | 本镜视角的**白模渲染**（Step 2，结构再锁一道） |
| 图片3 | 场景板（Step 4） |
| 图片4 | 本镜的马 / 驾驶者 / 车徽（Step 4） |

- **正向** = `## 视频 prompt` 的 ```text 整块
- **反向** = 「反向提示词」整块，粘进 negative prompt 框（**不要并进正向**）
- **比例** 21:9，**时长**按 `时长:` 字段（5–12s，**不是成片时长**）

---

### Step 11 · 逐镜剪出成片段 ｜ 你 ｜ ⬜ 未做

每镜按 `shotNN.md` 的「剪辑说明」取段——**生成 5–12s，成片只用 0.4–4.5s**。
生成侧有约 3.7 倍冗余，就是为了让你在剪辑台上有得选。

---

## 阶段 D · 成片

### Step 12 · 拼接 105 秒 ｜ 你 ｜ ⬜ 未做

按 `3_大纲/arc_outline.md` 的分镜总表顺序与入点拼。
五幕：16.0 + 18.0 + 32.5 + 20.0 + 18.5 = **105.0s**

### Step 13 · 调色 ｜ 你 ｜ ⬜ 未做

按 `2_世界观人设/style_guide.md` §二 五幕调色表。
铁律：**熵增段除车漆与尾灯外，画面不得出现任何饱和的红。**

### Step 14 · 混音 ｜ 你 ｜ ⬜ 未做

目标 **-14 LUFS / LRA ≥ 12**（竞品是 -12.1 / 6.5，一堵压平的墙）。
**第 43 镜必须有 ≥1.0s 近静默**（≤-45 dBFS），第 44 镜降档是全片最大声。

### Step 15 · 落版图形层 ｜ 你 ｜ ⬜ 未做

shot61（2.9s）：徽标水珠滑落 → 黑场 → `FERRARI F80` → 盾徽 → **tagline** → 黑场
> tagline 四选一待定，见 `1_立项/concept.md` §六（推荐 A：**熵，只输给速度。**）

### Step 16 · 交付 ｜ 你 ｜ ⬜ 未做

Pad 到 **3840×2160**（2.35:1 画面 + 上下各 264px 黑边）、**25fps**、H.264。
与竞品 `0710_v1.m4v` 同规格。

---

## 关键路径

```
Step 1 ─┬→ 2 ─┐
        └→ 3 ─┼→ 3b ─┐
   Step 4 ────┴───────┴→ 5 ──┐
                             ├→ 10 → 11 → 12 → 13 → 14 → 15 → 16
Step 6 ─┬→ 9 ────────────────┤
Step 7 ─┴→ 8 ────────────────┘
```

**Step 1（图1 全景）是全片唯一的单点瓶颈** —— Step 2 的三张、Step 3 的白模都从它派生，
它没定稿，后面全是白做。

**两条并行线**：资产线（1→5，你做）与分镜线（6→9，我做 + 你调）。
两条都到位才能开 Step 10。

---

## 现在该做什么

| 你 | 我 |
|---|---|
| **Step 1** 跑 Prompt 1 出图1（反复重跑到过 8 条验收） | **Step 6** 补完 57 个 shot prompt |
| **Step 2** 图1 过了再跑 Prompt 2/3/4 | **Step 7** 逐幕调 previz 配置（需你看构图） |
| 开着 Blender + addon，把 **Prompt 5** 贴给我 | — |

这两条**互不阻塞，可以同时开工**。
