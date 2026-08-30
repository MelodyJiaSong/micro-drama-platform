# F80 白模怎么用 —— 三个用途 · 具体流程

> ⚠ **2026-08-29 修订：用途① 已废止。** 新顺序是「图先行」——基准图由纯文字生成、
> 六张派生图挂基准图，白模反过来由这些图 image-to-3D 生成（见 `object_build_flow.md`）。
> 本文档的**用途③（逐镜 previz 的 reference_video）仍然有效，且已成为白模的唯一职责**；
> 用途① 的「白模图当 Seedream 结构参考位」不再执行，用途② 的转盘仍用于建立对象。


## 零、先厘清一件事：白模本体就是 Blender 文件

```
f80_ferrari.blend          ← 【白模本体】唯一真相。可编辑、可替换、可版本管理
       │
       │  渲染（Blender 干的活）
       ▼
   PNG / MP4               ← 【产物】给 Seedance 吃的东西
```

**Seedance 读不了 `.blend`，只吃图片和视频。** 所以：

- `.blend` = **母版**，留在仓库里，改它就等于改全片的车。
- `.png` / `.mp4` = **交付格式**，从母版渲出来，上传给 Seedance。

> **换车（升级白模）只需要一步**：把真 F80 高模存成 `f80_ferrari.blend` 覆盖掉，
> 然后重跑下面的命令——7 张定角图、10s 转盘、61 份 previz 配置**全部自动跟着换**。
> 你不需要改任何一个 prompt。

当前 `f80_ferrari.blend` 是脚本 blockout（`tools/build_duikang_assets.py` 生成）：
比例 / 姿态 / 离地 / 轴距 / 尾翼 / 扩散器都对，够当结构锁，但不是真 F80 的曲面。

---

## 白模的三个用途（互不相同，别混）

| 用途 | 产物 | 喂给 Seedance 的哪个位 | 锁住什么 |
|---|---|---|---|
| **① 结构参考图** | `whitemodel/angles/*.png` ×7 | Seedream 的**结构参考位** | 出写实图时的比例与姿态 |
| **② 建立对象** | `whitemodel/f80_ferrari_turntable.mp4` | Seedance 的**对象/参考位** | 这台车整体长什么样 |
| **③ 逐镜运镜与走位** | `shots/shotNN/shotNN_previz.mp4` | Seedance 的 **reference_video 位** | 本镜机位、轨迹、谁在哪 |

---

## 用途① · 出结构参考图（已完成，7 张在盘上）

**做什么**：白模从 7 个固定角度各渲一张，当 Seedream 出写实图时的「骨架」。

```bash
blender -b --factory-startup --python tools/render_object_turntable.py -- \
    --blend ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/f80_ferrari.blend \
    --out   ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/whitemodel \
    --name  f80_ferrari
```

产出 `whitemodel/angles/`：
`f80_ferrari_front.png` / `front3q.png` / `side.png` / `rear3q.png` / `rear.png` / `top.png` / `low3q.png`

**怎么用**：在 Seedream 里，对每个角度跑一次——
- 正向 prompt = `f80_ferrari.md` §3.2 的**基底 prompt**，把【角度子句】换成该角度那一句（§3.2 表）
- **结构参考图位** = 上传对应的 `whitemodel/angles/f80_ferrari_{tag}.png`
- 产物存 `ref_images/f80_ferrari_{tag}.png`

> **为什么要挂白模当结构参考**：没有它，7 张图会是 7 台比例不同的车
> （车轮位置、离地高度、轴距各画各的）。挂上它，7 张图的骨架是同一个源。

---

## 用途② · 建立对象（转盘已渲好，10.000s）

**做什么**：把整套身份包一次性喂给 Seedance，让它建立「f80_ferrari」这个对象。

上传内容 = **用途① 出的 7 张写实图** ＋ **`whitemodel/f80_ferrari_turntable.mp4`**

转盘的 5 个静止落点（可按时间戳抽帧核对）：

| t | 方位角 | 视角 |
|---|---|---|
| 0.75s | 0° | 正面 |
| **2.85s** | **45°** | **前四分之三 ← 主参考** |
| 4.85s | 90° | 正侧 |
| 6.85s | 135° | 后四分之三 |
| 9.10s | 180° | 正后 |

> 转盘是**灰模**，故意难看。它的任务是告诉模型「这台车的形体是这样的」，
> 不是告诉它「画面应该长这样」。外观由用途① 的写实图承担。

---

## 用途③ · 逐镜运镜与走位（每一镜都要，共 61 镜）

**这是白模在本片最主要的用途**，也是 follow-up 001 要求的「每镜都有 blender 文件」。

### 流程（四步）

```
① previz_config.toml        你/我写：机位、焦距、轨迹、谁在哪、什么时候动
        │  blender -b --python tools/previz/build_previz.py -- <config>
        ▼
② shotNN_previz.blend       白模 + 场景主档自动组装成的本镜 3D 场
        │  同一条命令直接续渲
        ▼
③ shotNN_previz.mp4         灰模动态视频
        │  上传
        ▼
④ Seedance reference_video  锁住主干动作 + 人物物品位置 + 机位
```

### 实际命令（以 shot25「中世纪车马并驾」为例，已实测跑通）

```bash
blender -b --factory-startup --python tools/previz/build_previz.py -- \
    ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot25/previz_config.toml
```

产出（同目录）：
- `shot25_previz.blend` —— 组装好的 3D 场（可在 Blender 里打开手调）
- `shot25_previz.mp4` —— **2560×1090 / 25fps / 8.04s**，这就是要上传的文件

> 若你的 Blender 构建没编进 FFMPEG，脚本会退回渲 PNG 序列，用这条收尾：
> `python tools/whitemodel_to_mp4.py shot25 --fps 25 --project duikang_shangzeng`

### 白模在 previz 里是怎么进去的

`previz_config.toml` 里这一段就是挂白模：

```toml
[["道具"]]
"名" = "f80"
"形" = "模型"
"档" = "ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/f80_ferrari.blend"
"尺寸" = [2.06, 4.84, 1.14]   # 宽×长×高，车头朝 +Y
```

引擎会自动：从这个 `.blend` 追加网格 → 合并 → 归一化到 `尺寸` 的包围盒 → 原点落底面中心。
所以**换白模不用改配置**，`档` 指向同一个路径即可。

### 关键约束：关键帧的 `t` ＝ prompt 里 `动作:` 的时间轴

```toml
  [["道具"."关键帧"]]
  t = 0.0
  "位置" = [0.0, 0.0, 0.0]
  [["道具"."关键帧"]]
  t = 8.0
  "位置" = [0.0, 0.0, 0.0]
```

这些 `t` 必须和 `shot25.md` 里 `动作:` 字段的 `0-2s` / `2-4s` 分拍**逐拍对齐**。
previz 是动作时刻表的唯一真相，prompt 抄它。两处不一致 = blocker。

---

## 每个 shot 最终上传给 Seedance 的东西（固定五位）

| 位 | 文件 | 来自 |
|---|---|---|
| **视频1** | `shots/shotNN/shotNN_previz.mp4` | **用途③** |
| 图片1 | `ref_images/f80_ferrari_{本镜视角}.png` | **用途①** 出的写实图 |
| 图片2 | `whitemodel/angles/f80_ferrari_{本镜视角}.png` | **用途①** 的白模渲染（结构再锁一道） |
| 图片3 | 场景板（entropy_city / medieval_road / ice_plain） | Seedream |
| 图片4 | 本镜的马 / 驾驶者 / 车徽参考图 | Seedream |

外加 `shotNN.md` 里的正向 prompt 与反向提示词。

---

## 三个用途的先后顺序

```
1. 先跑用途①②（一次性，全片只做一遍）
      白模 → 7 张定角图 → Seedream 出 7 张写实图 → 加转盘 → 建立对象
2. 再跑用途③（逐镜，61 次）
      每镜写/调 previz_config.toml → 渲 MP4
3. 最后出片
      每镜：prompt + 五个参考位 → Seedance
```

**用途①② 没做完就别开始用途③ 的出片**——对象没建立，每镜的车都会是不同的车。

---

## 当前状态（2026-08-29）

| 项 | 状态 |
|---|---|
| `f80_ferrari.blend` 白模本体 | ✅ 脚本 blockout（待换真高模） |
| 用途① 7 张定角白模渲染 | ✅ 已在 `whitemodel/angles/` |
| 用途① 7 张 **Seedream 写实图** | ❌ **未做——需你在 Seedream 侧跑** |
| 用途② 转盘 MP4 | ✅ 10.000s / 250 帧 |
| 用途② **建立对象** | ❌ **未做——需 ① 完成后上传** |
| 用途③ 61 份 previz 配置 | ✅ 全部通过 Blender 自检 |
| 用途③ **61 个 previz MP4** | 🔄 已渲 shot25 一个，其余 60 待渲 |
