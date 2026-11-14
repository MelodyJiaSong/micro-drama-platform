# 物品参考图（follow-up 310 建，follow-up 316 改为严格 DotA 1）

6.83d 全部 131 件物品 + 通用合成卷轴，每件一个目录 `{序号}_{英文名}/`（序号与 `2_世界观人设/props/shop_items.json` 的物品顺序一致，按 d08 §2 商店小节排列）。

| 文件 | 来源 | 覆盖 |
|---|---|---|
| `dota1_playdota_icon.jpg` | PlayDotA 物品库存档 `web.archive.org/web/2014im_/http://media.playdota.com/items/{id}/icon.jpg`（6.81 时代，DotA 1 物品栏图标，约 64 px） | 128 / 132 |
| `dota1_icon.*` | 上面缺的 4 件（暗影护符、赤红甲、奶酪、合成卷轴）另找的 DotA 1 地图 / 魔兽 3 原版图标，来源写在各自 `refs.md` | 见各目录 |
| `refs.md` | 每件：来源、sha、看到了什么、真人化取了什么 | 132 / 132 |
| `_dota1_icon_paths.json` | 从 6.83d 英文地图文件（archive.org 2015 存档，sha 见文件内）解析的「物品 → 物品栏图标 / 商店格子图标路径 / 是否地图自制」全表，132 行 | 132 / 132 |
| `_fetch_results.json` | 下载记录（URL、字节、sha256） | — |

规则（用户定，2026-11-01，follow-up 316；`world_rules.md` §1 第 6 条，剧级检查 `ref_image.dota1_only`）：**只依据 DotA 1 / 魔兽 3 原版图标**。Dota 2 图标已全部删除（原 132 张 `dota2_icon.png`），不再下载、不再参考；卡里借过 Dota 2 的造型已改回 DotA 1 原样并重出。DotA 1 图标看不清或缺图的部分，按 d08 原文或明说「创作 ⚠️」补，不拿 Dota 2 补。暴雪素材只作人眼参考，不进成片、不上传生成服务；锚点图全部零参考文生图。

物品在哪家商店 / 哪个 NPC 卖：`../../2_世界观人设/props/shop_items.md`。
