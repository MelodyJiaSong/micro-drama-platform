# 时空旅行 · 暴风城的一天（sk2）

- 系列：《时空旅行》`ai_videos/shikong_lvxing/`（`series.json`；系列提案 `../proposal.md`）。本片片名「暴风城的一天」，系列名只作前缀。
- 本站：**魔兽世界 · 暴风城（Stormwind）· 经典旧世（Vanilla，大灾变之前）**，世界时间约 ADP 25 年。旅行者 **c4 艾拉 / Ella Hart**（28 岁，美国波特兰人，片中说**美式口音英语**）。
- **这是系列的第一个「虚拟城」**（第一站是北宋汴京，真实历史城）。方法论差别见 `../proposal.md § H 虚拟城支线`：史料换成**作品设定**，三档事实标签里的 ❌ 多了一个来源——**版本错置**（把大灾变之后的设定安到经典旧世头上）。
- 形态：**旅游 + 解说 + 偶尔与 NPC 互动**。刻意**没有重大事件**——卖点正是「在什么都没发生的一天里，这座城长什么样」。一枚金币、一天、八个城区、三顿饭、一晚。16:9，**14.7 分钟（882 s）**，**44 镜**，单镜 15–30 s。
- **当地人可以开口，但只说作品内逐字原文**，一个字不得自编（系列 follow-up 014 / `divergence #113`）。四位开口 NPC：卫兵、旅店老板奥里森、面包小贩、酒馆老板。知识一律由艾拉讲，NPC 不是解说员。

## 阶段进度（2026-09-20）

| 阶段 | 状态 | 产物 |
|---|---|---|
| 0 设定考据 | ✅ | `0_research/`（10 路 643+ 条事实、18 条跨路裁决） |
| 1 立项 | ✅ | `1_立项/concept.md` |
| 2 世界观人设 | ✅ | 13 个场景 / **27 张场景图**、17 张人物卡 / **17 张立绘**、22 个物件 / **66 张图 + 22 个白模** |
| 3 大纲 | ✅ | `3_大纲/outline.md`（44 镜分配表） |
| 4 剧本 | ✅ | `4_剧本/{script,dialogue}.md` |
| 5/6 分镜与 prompt | ✅ | 44 镜 + **44 条 previz（1280×720）** |
| 发布页 | ✅ | `5_6_分镜与prompt/publish.md`（四站） |
| **出片** | ⛔ | **被 `divergence #110` IP 定性挡着** |

**未完成**：17 个人物的 4 秒 turntable 视频（出片中）· BGM 12 段（`tools/stableaudio_gen.py` 需要 torch 与 HuggingFace gated 权重，**待本人接受许可**）· IP 定性 #110。

## 入口

- 镜表与切口审计：`5_6_分镜与prompt/shotlist.md`
- 全部 prompt：`5_6_分镜与prompt/all_shot_prompts.md`
- 四站发布页：`5_6_分镜与prompt/publish.md`
- **改镜头内容 ＝ 改 `tools/gen_shots_sk2.py` 重跑**，不要手改 `shotNN.md`（rule 4i ①）。
  同理：场景 look 层改 `tools/gen_scene_prompts_sk2.py`、turntable 章节改 `tools/gen_turntables_sk2.py`、
  城模型改 `tools/build_stormwind.py`、previz 机位改 `tools/previz_sk2.py`。

## 影像口径（2026-09-19 定）

**实拍电影，不是渲染图。** 形制/比例/配色按暴风城设定（蓝顶白石），**影像真实度拉满**——
这两个轴互相独立，「半写实」形容的是世界的设计、不是画面的渲染。
口径承自 `ai_video.md` §18（sk1「太像动画，全部重来」的产物），细则见 §25。
出图走 `gpt-image-2`（实测优于 gemini-3-pro-image 与 Seedream 5.0）。

## 单站意图与变更

`specs/ai_video/sk2/`（`changelog.md` 是这部片改过什么的唯一账本）；系列级意图：`specs/ai_video/shikong_lvxing/`。
