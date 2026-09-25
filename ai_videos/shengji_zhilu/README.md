# 《圣光刚好够用》 · shengji_zhilu

> *Just Enough Light* —— 一个刚到北郡修道院的圣骑士新兵，在这个世界里一步步长成能替别人撑住的人。
> **2026-09-24 剧集化转向**（concept G 组）：片中不出现游戏与玩家概念 · 面向英语观众（英文台词）· 16:9 · 单集约 10 分钟 · Seedance 出片
> 版本锚点：**经典旧世 Vanilla / Classic Era（1.12 口径）· 黑暗之门后第 25 年**

---

## 一句话

**练级不是为了变强到碾压谁，是为了在别人需要的时候还站得住。**

他打怪慢得要命、被队伍当 buff 机器使唤、**但死不了**——
这不是设定，是经典旧世圣骑士的真实数据。全剧的主题就长在这条数据上：
**他的高光永远是救人，不是杀敌。**

第一季的终点不是一件装备，是**五个人终于愿意再一起上线一次**。

---

## 目录导航

| 阶段 | 落点 | 状态 |
|---|---|---|
| **0 设定考据** | `0_research/` | ✅ **1857 条事实**（`ai_read` 1744）· 20 路调研 + 13 路地理测绘 |
| **1 立项** | `1_立项/concept.md` | ✅ 70 条创作裁定 + **G 组（G1–G9，剧集化转向，优先于其余条目）**；旧 20 集骨架暂停 |
| **2 世界观人设** | `2_世界观人设/` | ✅ **24 张卡** + casting + 人物网 |
| **2a 全图场景** | `2_世界观人设/scenes/{大陆}/{区}/bg{N}_*/` | 🔸 **两片大陆 49 区 · 804 个 bg**（编号唯一出处 `scenes/registry.toml`，总表 `scenes/scenes_index.md`）；每个 bg 一张锚点级主体卡 + 原版区图 ref + 场地平面图（rule 4k），bg1–3 / 17–22 是 v3 五 plate 档；写卡工作流进行中 |
| **2b 场景图 + 3D 层** | 场景图 `bg*/{目录}.png` + plate 图；`bg*/_blender/{bg}.blend`；物件 `2_世界观人设/props/p{N}_{名}/`（编号 `props/registry.toml`） | 🔸 **ep01 的 9 个场景齐了**：41 张场景图（9 锚点 + 32 plate，全 16:9，挂场景主要物件的 prop 正面图作参考）、9 份 blend（场景图挂同名机位相机背景 + prompt 文本块 + 单物体 GLB，占位 0）；**GLB 只装单个物体**；各区资产库已并进 props（462 → 449 件，p15–p463），场景只引用；其余 795 个 bg 还没出图 |
| **3 分集大纲** | `3_大纲/arc_outline.md` | ⏸ v3 暂停使用：旧 ep01–03 已并入新 ep01，ep02+ 按第一集反馈重排 |
| **4 文学剧本** | `4_剧本/episodes/epNN/` | 🔸 **ep01 *Buy Me Three*（撑三下）**：27 镜 / 652s，英文台词 + 中文意思，逐窗念白闸门与「新地方先给景」闸门全过；两轮审查已落地 blocker / major |
| **5/6 分镜与 prompt** | `5_6_分镜与prompt/episodes/epNN/` | 🔸 **ep01 已出**：27 个 `shotNN.md`（Seedance 五层 prompt + 英文配音块）+ `shotlist.md`（含切口审计）+ `all_shot_prompts.md`；生成器 `tools/gen_shots_szzl_ep01.py`（引擎 `tools/szzl_shot_engine.py`）。**previz 未做**（等北郡 blend 定稿）；阶段 5 五道审查未跑 |

### 几何与台词的两道生成时闸门（**不合格就生成不出产物**）

| 跑什么 | 管什么 |
|---|---|
| `blender -b --factory-startup --python tools/build_scene.py -- --all "<scenes 目录>"` | 场景几何：未登记的 `kind` / 块扎进山脊 / 块压块 / 块坐在河道上 / 机位埋在体块内部 |
| `python tools/script_tools.py check 4_剧本` | 台词：中文 ≤5 字/秒、英文 ≤3 词/秒，**逐时间窗核**（行尾【a–bs】）· 每镜 3–30s 且避开 4–6s 碎镜 · 单集区间读 `4_剧本/script.toml`（本剧 540–660s）· 新地方第一次出现须有 `场景展示`（新区 ≥12s / 新地点 ≥6s）· 禁古语与伪古英语 |
| `python tools/gen_shots_szzl_ep01.py` | 分镜与 prompt：切口比值（K31）· 共用串不点名光源（K32）· 镜内自洽（K33）· 版本红线 · 5000 字 · 零 hex · 裸 `=>@` · IP 红 / 黄级专名 · 台词与锁定串从源头读 · 写盘后回读 |
| `python tools/check_stage2.py ai_videos/shengji_zhilu` | 人设契约：零 hex · 锁定串 ≤30 · 人物灵魂 12 维 · voice_id ↔ casting（须 `en-`）· **零玩家概念（G1）** · **自负向** |
| `python tools/check_world_scenes_szzl.py [区目录或 bg 目录]` | 全图场景：登记簿落点 · 占位填完 · 锚点 prompt 1500–2000 字 · 版本红线 · **正文与一句话锁定零黄级专名（C3）** · 平面图最新 · 原版区图 ref（W1–W10） |

**第一季的 3D 范围**（2026-09-21 用户定调）：只建**北郡山谷**与**闪金镇**；
暴风城复用 `shikong_lvxing/sk2` 的整城 blend；哨兵岭 / 西部荒野第一季不建。

### 先读哪几份

1. **`1_立项/concept.md`** —— **70 条创作裁定是下游所有阶段的宪法**，与它冲突的产物以它为准。
2. **`0_research/dossier.md`** —— 15 节设定考据的总纲（按游戏原典做了等价映射）。
3. **`0_research/map/world_overview.md`** —— 一页看全艾泽拉斯；细节进 `world_tree.md`（1908 节点，简中名以 Classic Era 客户端 AreaTable 为准）与 `zones/*.md`（50 份单区页）。
4. **`2_世界观人设/{world.md, style_guide.md}`** —— 双层规则与全片渲染/负向契约。
5. **`2_世界观人设/relationships.md`** —— **人物网**。rule 12.11-C：写改任何剧情之前必读。

---

## 这部剧的四条特殊规则

### 1. 主角知道自己在玩游戏，但镜头永远不离开艾泽拉斯

**自知玩家 · 现实零画面**（concept B1）。他有现代人的语感、会吐槽机制，
但**没有攻略、没有前世记忆、没有金手指**。观众需要的知识由队友「知无不言」说出来——
**而且他会说错**，这是本剧的剧情发动机。

现实世界全剧**最多出现 1–2 次**，且只给一只手 / 一块屏幕的反光 / 一段环境声（concept B7）。

### 2. 玩家与 NPC 长得一模一样，靠三件事区分

**玩家三件套**（concept B4）：① 无理由连跳 ② 绕圈跑 ③ 突然完全静止（挂机）
（+ 可选第四件：战斗一结束立刻蹲下翻尸体）。再叠一件公会战袍区分散人与有组织的。

**不用头顶名牌**——那要求生成模型在人物头顶稳定渲染一行汉字，是已知的高失败率需求；
而三件套零文字、零 UI、零额外资产，且老玩家的识别度比名牌更高——**那是他们自己做过的事**。

### 3. 游戏 UI 一个像素都不进生成块

**三层归属制**（concept B3）：
- **L1 入世层**＝画面本身（灵魂形态 / 墓地天使 / 狮鹫 / 品质辉光）→ 进 prompt；
- **L2 后期叠层**＝主角的视野（升级 / 接任务 / 掉落三时刻，单次 ≤1.5s，**只在 `视点: 主角` 的镜**）→ 后期贴；
- **L3 声音层**＝主角的耳朵（密语贴耳 / 公会低语场 / 世界频道嗡嗡底噪）。

### 4. 地是真的，人是编的

地图 / 怪 / 等级 / 任务 / 技能与获得等级 / 已知 NPC 的结局——**一个字都不动**。
主角与队友的性格来历关系、路上遇到的无名 NPC、任务之间的日常——**随便编**。

理由：魔兽的地图与怪是观众的**验证锚点**。看到霍格就知道这剧是懂的，
看到一个编出来的「西部荒野第二个村子」就立刻出戏。**而人是自由的**——玩家角色本来就不在原典里。

---

## 机检闸门（改完产物记得跑）

```bash
python tools/facts_registry.py   ai_videos/shengji_zhilu   # 事实注册表：枚举、quote、重复 id
python tools/build_world_tree.py --src ai_videos/shengji_zhilu/0_research/map   # 地理树：id 重复/孤儿/成环
python tools/build_blacklist.py  ai_videos/shengji_zhilu   # 误传黑名单 → 负向词库
python tools/check_stage2.py     ai_videos/shengji_zhilu   # 人物卡/场景档契约
python tools/wow_version_gate.py ai_videos/shengji_zhilu   # 经典旧世版本红线
```

**全部是闸门，不是报告**——不合格直接非零退出。
`world_tree.md` / `world_overview.md` / `zones/*.md` / `blacklist.md` / `negatives.txt` **都是生成物，手改无效**。

---

## 无人值守期间的判断

本项目的阶段 0–3 在 **AUTONOMOUS 模式**下完成（用户 2026-09-19 授权）。
**全部创作选择以 `*(judgment call — …)*` 内联记在产物里**，每一条都可被推翻。

**最值得优先复核的六条**见 `specs/ai_video/shengji_zhilu/pending_user.md`，
其中三条是**商业与形式决策，Claude 不该替你定**：IP 路线（片内用原名 / 片外品牌位不用）、
变现时点（前 10–20 集非商业）、剧名。

**需要人在电脑前做的七件事**（截 Classic 客户端图、导出色板 CSV、IP 专名实测…）同在那份清单里，
标 🔴 的会在出图前变成 blocker。
