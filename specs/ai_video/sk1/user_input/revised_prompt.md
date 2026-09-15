# sk1 · 合并后的完整意图（raw_prompt + 全部 follow-ups）

> 派生文件，由 `raw_prompt.md` + `follow_ups/*.md` 按时序拼成。改动请改源文件后重生成。

# sk1 · 《时空旅行》第 1 站 · 汴京 · 1120 · 清明日 — 原始请求

> **task_type**：`ai_video` · **sub_type**：`short`（单站独立成片，系列嵌套于 `ai_videos/shikong_lvxing/`）
> 系列级意图在 `specs/ai_video/shikong_lvxing/`；本目录只装 sk1 单站的。

## 用户意图（2026-09-13）

按系列提案 `ai_videos/shikong_lvxing/proposal.md` C §sk1 概念卡开工第一站：**北宋汴京 · 宣和二年（1120）· 清明日**。
先跑「阶段 0 史料调研 → 出 prompt」小闭环，看效果再选下一站。

阶段 0 参数（用户确认，2026-09-13）：严格度＝科普向娱乐（画面可截图指认的东西只允许 ✅ / ⚠️，❌ 只进纠错单元）；系列公共库本站新建；每个资产 ≥ 8 张历史参考图。

---

# sk1 · 后续指令日志 · 2026-09

> 单站意图的落点；系列级意图见 `specs/ai_video/shikong_lvxing/`。

---

## 001 — 2026-09-14 08:26:14 — sk1 另起片名：系列名不作单片标题

> target_stage: 1
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/README.md
>   - ai_videos/shikong_lvxing/sk1/1_立项/concept.md
> severity: low

### 指令

sk1 在剧目管理界面上显示的标题不能是《时空旅行》——那是系列名。为本站另起一个片名，README 首行等处统一。

### 一行摘要

片名由 Claude 自定并记判断；系列名只作前缀，与《荒野生活 · 深雪第一夜》同构。

---

## 002 — 2026-09-14 22:09:42 — 参考图宽高比进 Seedance 上传窗口

> target_stage: 2
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/**/ref/
> severity: low

### 指令

Seedance 上传图片的宽高比必须在 1:3 与 3:1 之间；把不满足要求的参考图改成满足要求的样子。

### 一行摘要

37 张 `ref/` 长卷图原地补边或折行拼版进窗口；入库工具自动处理，全局规则见 `ai_video.md` 17.7。

---

## 003 — 2026-09-14 22:09:42 — 世界锚点改为 bg0-1 全景

> target_stage: 2
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg0_汴京全城/bg0_汴京全城.md
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg1_虹桥/bg1_虹桥.md
> severity: medium

### 指令

用户问世界锚点为什么是 bg1-1 而不是 bg0-1 全景图；解释原因（rule 4e 命名 `bg1_` ＝世界锚点、首轮建库先定虹桥、bg0 是 W11 后补）后，用户选择改为 bg0-1。

### 一行摘要

`bg0-1` 只挂历史参考图、成为全片唯一世界锚点；`bg1-1` 降为虹桥地点锚点并改挂 `bg0-1`；其余主体的世界锚点句柄全部换成 `bg0-1`，只取基调、不取高空视角。

---

## 004 — 2026-09-14 22:09:42 — 天要蓝、水要绿

> target_stage: 6
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/style_guide.md
>   - tools/gen_shots_sk1.py
> severity: medium

### 指令

每个图片天空要蓝、水要绿，打个比方就像天气好的时候无人机航拍出来的效果。

### 一行摘要

所有场景卡与 36 镜：白天晴天通透蓝天、所有水面碧绿、去掉遮远景的薄雾，夜空深蓝；生成器按时段条件化追加天与水分句与负向（不进共用串）；p8–p10 image-to-3D 三视图保留阴天、只改水色。

---

## 005 — 2026-09-15 13:23:35 — 场景 blend 写实化 + shot01/02 blend

> target_stage: 6
> target_artifacts:
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend
>   - ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot01/
>   - ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot02/
> severity: high

### 指令

所有场景图已生成并下载。重建场景 blender 文件：不要只是方块，要利用这些场景图，把 3D 城市做得越接近真实越好；做好后截几张图给用户。然后把 shot01、shot02 的 blender 文件做好——shot 的 blend 就是拷贝场景 blend 再加上人物与动作，场景 blend 是基础。

### 一行摘要

场景 blend 从灰模升级为可渲染的写实城市（材质取色自锚点图 + CC0 PBR、程序化宋式民居 / 虹桥 / 柳树 / 曲面屋顶、晴天低日光），布局仍由 builder 唯一决定；shot01 / shot02 从新场景拷贝重建。

---

## 006 — 2026-09-15 13:34:10 — 建城参考下载图 + 场景 prompt

> target_stage: 6
> target_artifacts:
>   - tools/look_bianjing.py
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend
> severity: medium

### 指令

构建 3D 城市时，同时参考用户下载的场景图片**和**各场景卡里的 prompt（形制、材质、色名、禁用项），不只取图片颜色。

### 一行摘要

look pass 的建筑形制 / 材质 / 禁用项以 `bg*.md` prompt 为准、以 `bg*-1.png` 核对；与 prompt 冲突的现有细模逐项改。

---

## 007 — 2026-09-15 18:15:38 — 全城均匀铺满房子、建筑与人

> target_stage: 6
> target_artifacts:
>   - tools/build_bianjing.py
>   - tools/look_bianjing.py
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/city_plan.md
> severity: high

### 指令

不应只有河道两岸有房子：城内城外都要遍布房子、建筑和人。仔细参考 `bg0-1`，让整座城市与城外的建筑布局更均匀、合乎情理。

### 一行摘要

布局层补密：城内街区贴街贴河贴墙填满、地标院落不留大空地；城外每座城门外都有关厢、沿出城道路成街、田野里散布村落与树；look 层加全城静态行人。

---

## 008 — 2026-09-15 19:54:56 — 城内降密、去整齐、房子大小高低有别

> target_stage: 6
> target_artifacts:
>   - tools/build_bianjing.py
>   - tools/look_bianjing.py
>   - ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/city_plan.md
> severity: high

### 指令

俯视看城市太密太整齐：古代做不到那么多人口和那么规整的规划。城内降低密度；房子不能都一样，要有高有低、有大有小。先做 research，改得更贴近历史现实。

### 一行摘要

以史料（户口、宅院规模、坊巷肌理、城内空地）为据重排街区：不规则地块、按区位变化的密度、院落大小与层数分级、菜园池塘空地。
