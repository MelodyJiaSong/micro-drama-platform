# bianjing · Blender 建城指令（给 Claude 的任务书）

> **这份文件即指令**：新会话读它 + `city_plan.md` 就能开工，不必回看对话。
> 规范来源：`.claude/agent_refs/project/ai_video.md` rule 4d（白模闸门）+ 4g（环境几何）+ 4h（3D 工程契约）+ 4i（一致性纪律）；本系列偏离登记在 `specs/ai_video/sk1/divergence.md` #9 / #10。
> **本层只出 `.blend` + 校验 PNG，绝不渲 mp4**（rule 4g §J）。出 mp4 的只有 shot previz。
> **`.blend` 与任何灰模渲图绝不进出图 prompt 的参考位**（rule 4d ①）；一镜到底的 previz mp4 上传给 Seedance 作**运动 / 几何**参考是 divergence #10，长相仍来自锚点图。
> 只写指令与验收，不写代码——代码是 `tools/build_bianjing.py`，由本文件 §7 的接口约束。

---

## 1. 自查对账（开工第一件事，不许跳过；rule 4i §③）

```bash
# 几何现状：物件数 / collection / 包围盒 / 三块 Place 范围，一条命令全出（builder 落地后可用）
blender -b --factory-startup --python tools/build_bianjing.py -- --qc-only \
    "ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender/bianjing.blend"
```

**2026-09-14 基线**：什么都还没有——`bianjing.blend` 不存在、builder 不存在、三个白模不存在、`city_plan.png` 不存在。**动手前先量一遍盘上真实状态**，`city_plan.md` §0 与本节对不上的先改文档再开工。builder 第一次落地后把实测的 collection / 物件数 / 包围盒填进下表，此后每次重跑逐行复现：

| 项 | 值（2026-09-14 B_city phase 2a 实测：全城层 G ＋ 三块 Place 挪到 W11 真实锚点；三个白模全缺席 ＝ 全替身） |
|---|---|
| **phase 2b 重建**（D/E/F/H/I/J 六块新 Place、护龙河与御街宽改取 W11、正店门首） | A 与 phase 2a 同；B：`B_GATES` 13 · `B_HOUSES_PROXY` 2 · `B_MOAT` 6 · `B_RIVER` 2 · `B_STREET` 4 · `B_TREES` 1 · `B_WALL` 4（x −50…120）／ C：`C_CHAZI` 4 · `C_DITCH` 4 · `C_GALLERY` 2 · `C_HOUSES_PROXY` 5 · `C_MISC` 4 · `C_RIVER` 2 · `C_STREET` 5 · `C_ZHENGDIAN` 2 · `C_ZHOUQIAO` 7 ／ D：`D_CHAZI` 1 · `D_COURT` 3 · `D_DUN` 3 · `D_GROUND` 2 · `D_HALL` 1 · `D_MENLOU` 3 · `D_QUE` 2 · `D_RIVER` 2 · `D_STREET` 1 · `D_WALL` 1 ／ E：`E_DOCK` 1 · `E_GRANARY` 4 · `E_GROUND` 5 · `E_HOUSES_PROXY` 2 · `E_RIVER` 2 · `E_STREET` 1 · `E_TREES` 1 ／ F：`F_COURT` 6 · `F_GATE` 2 · `F_GROUND` 1 · `F_HOUSES_PROXY` 6 · `F_STREET` 1 · `F_WALL` 1 ／ H：`H_GATE` 2 · `H_GROUND` 1 · `H_HALL` 3 · `H_HOUSES_PROXY` 8 · `H_STREET` 1 · `H_WALL` 1 ／ I：`I_FENCE` 3 · `I_GROUND` 2 · `I_HOUSES_PROXY` 6 · `I_RIVER` 2 · `I_SHED` 6 · `I_STREET` 2 ／ J：`J_FIELDS` 2 · `J_GROUND` 1 · `J_ROAD` 3 · `J_TREES` 2 ／ G：`G_BLOCKS` 6427 · `G_GATES` 35 · `G_GROUND` 1 · `G_LANDMARKS` 19 · `G_STREETS` 17 · `G_SUBURBS` 21 · `G_WALL` 4 · `G_WATER` 1 ／ **合计 6717 物件、1 003 404 面**；包围盒不变；几何摘要 sha256 `38a7ffc32e218f711089234f6a97a0bf14846e57e1add519d7b882e656f19891`；QC 零失败（门洞 / 门口通透 5 项新检查全过） |
| collection / 物件 | A：`A_BRIDGE_PROXY` 1 · `A_DOCK` 3 · `A_HOUSES_PROXY` 10 · `A_POLES` 4 · `A_RIVER` 2 · `A_STREET` 6 · `A_TREES` 2 ／ B：`B_GATES` 13 · `B_HOUSES_PROXY` 2 · `B_MOAT` 6 · `B_RIVER` 2 · `B_STREET` 4 · `B_TREES` 1 · `B_WALL` 4 ／ C：`C_CHAZI` 4 · `C_DITCH` 4 · `C_GALLERY` 4 · `C_HOUSES_PROXY` 5 · `C_MISC` 5 · `C_RIVER` 2 · `C_STREET` 5 · `C_ZHOUQIAO` 7 ／ G：`G_BLOCKS` 6437 · `G_GATES` 36 · `G_GROUND` 1 · `G_LANDMARKS` 23 · `G_STREETS` 17 · `G_SUBURBS` 21 · `G_WALL` 4 · `G_WATER` 1 ／ **合计 6636 物件、972 992 面**；原型集合 `PROTO_p8/p9/p10/p10a_PROXY`（不挂场景树，被实例引用） |
| 包围盒（世界） | x −9000…10000，y −9000…9000（全城地面 19 × 18 km，判断：WP3 高空全景不露地面边），z −2.00…78.00（z 顶 ＝ 繁塔 76 m）；几何摘要 sha256 `9d40ed37b97c41ef5e38d971f3ddcd86e4852900f9f0ffce8e5c032e8ddedc6f`（`--qc-only` 复现；全城地面顶面布尔前切 41 × 41 网格——整片顶面若只剩几个带洞巨型 n-gon，显示三角化翻面、航拍里拉出放射状暗纹） |
| Place A 校验 | 锚点换成 W11 后全部换回 Place 局部坐标查：拱顶 z=5.600；坡道脚 y=±18.00、z=2.001；脚店 A 门脸中点 (−11.00, 18.25) → 坡道脚边 (−3.90, 18.00) 净距 7.10 m、桥尾视线通；一镜到底走廊 152 采样点零侵入；后墙线偏差 北 0.32 / 南 0.27 m |
| Place B 校验 | 入城镜走廊 (30,18)→(28,16)→(0,16)→(−15,18)、r 2.0 零侵入；两座旱门门洞通透；局部范围 x −50…50、y −45…45 |
| Place C 校验 | 局部 x −46…49（望火楼表行自身越出 1.0 m，WARN）、y −80…120；D 级无非表行几何 |
| 全城层 G 校验 | W11 §2.8：城墙 3（外 34.2/4/8.7、里 16/4⚠️/8.7、宫 12/3⚠️/8.7，⚠️＝顶宽 C 类推）＋马面；城门 36 / 37（东水门归 Place B）；河道 5（汴河在三块 Place 足迹内改走 Place 河轴）；街道 15 ＋ 御街设施延伸 2；地标 28（跳过 4、殿院 7、瓦子 3、坛 3、塔 2、池 2、殿基 / 桥 / 楼群 / 客店带 / 工地 / 苑 / 冈 各 1）＋宫内殿宇 11；街区 6437 块 / 143 843 个单元盒（C 级，御街两侧 250 m 与 Place B 周围 400 m 升 B 级）；郊外 20 段 / 879 盒 / 421 柳（B 级）；**Place 足迹内零侵入** |

---

## 2. 输入（缺一不开工）

| 输入 | 路径 | 状态检查 |
|---|---|---|
| 摆放依据 | `scenes/bianjing/_blender/city_plan.md` §1 §2（**唯一**） | 表里每行有方块号、Place、局部中心、朝向 |
| 白模 | `props/p8_虹桥单体/whitemodel/p8_虹桥单体.blend`、`props/p9_桥尾脚店单元/whitemodel/p9_桥尾脚店单元.blend`、`props/p10_沿河民居单元/whitemodel/p10_沿河民居单元.blend`（+ `p10a/b/c.blend`） | 各自过了 `whitemodel_normalize.py` 闸门（退出码 0）、`whitemodel/angles/` 渲图人眼看过 |
| 锚点图（只给人眼对照） | `props/p8…/p8-1.png`、`p9…/p9-1.png`、`p10…/p10-1.png`、`scenes/bianjing/bg1_虹桥/bg1-1.png` | 各卡验收清单过完 |
| 俯视底图（可选） | `_blender/city_plan.png`（人工标号版） | 与 `city_plan.md` §2 表一致；**冲突以表为准** |

**白模缺席时的替身**：builder 必须能在白模缺席时用同尺寸盒子（`p8` ＝ 拱形板带、`p9` ＝ 8 × 7.5 × 7.5 盒、`p10` ＝ 12 × 6.5 × 6.6 盒）占位并在 collection 名上加 `_PROXY` 后缀——这样 previz 与走廊校验不必等白模；白模到位后重跑即替换。**替身绝不渲进任何 prompt 参考位。**

---

## 3. 坐标契约（与 `city_plan.md` §1 逐值一致；两边任何一个动了，另一个必须跟着动）

| 常量 | 值 | 含义 |
|---|---|---|
| 轴向 | `+X` 东（汴河下游）· `+Y` 北 · `+Z` 上 | 全 Place 一致 |
| `Z_WATER` / `Z_STREET` | `0.0` / `2.0` | 水面 / 两岸街面 |
| `Z_DECK_CROWN` | `5.6` | 虹桥拱顶桥面（拱顶净空 5.0 + 板厚 0.6） |
| `FRAMES`（W11 `[[place_anchor]]`） | A (6280, -4769) 转 -30° · B (2776, -2746) 转 -9.7° · C (0, 0) 转 -5.5° | 世界 ＝ 锚点 ＋ Rz(转角)·局部；Place 内一律用局部坐标。旧的 `A (0,0) · B (−400,0) · C (−900,0)` 是压缩占位偏移，2026-09-14 phase 2a 作废 |
| `BAY` | `4.0` | 面阔模数（p9 / p10 / 御廊 / 仓 全按它） |
| `RIVER_W` | `20.0` | 汴河宽（⚠️ 由桥长 21 推算） |
| 朝向约定 | 白模「前」＝ 门脸 ＝ 局部 −Y；摆放 `朝向` 字段 0 ＝ 门朝南、180 ＝ 门朝北、90 ＝ 门朝东、−90 ＝ 门朝西 | 与 `whitemodel_normalize.py` 目标朝向（前 +Y）**相差 180°**——builder 摆放时统一补这 180°，不改白模 |

---

## 4. 建城步骤（确定性、可重跑；改几何 ＝ 改脚本重跑，**不手改 blend**，rule 4h §D）

1. **读表**：解析 `city_plan.md` §2 的三张表（列定义见 §7），得到 `(方块, 要素, 主体/建法, Place, 局部中心, 朝向, 尺寸, 级)` 记录；`主体/建法` 含「shot 层道具」的行**跳过**（它们属 previz TOML）；含「留位」的行放一个 `_PLACEHOLDER` 盒子。
2. **建骨架（脚本类，先于白模）**：
   - Place A：河道水面平面 + 河床（y −10…10）、两岸土坡（|y| 10…13，z 0→2 斜面）、沿河街（|y| 13…19，z=2）、码头平台、仓体块、表木（圆柱 + 横木 + 小块）、柳树 proxy（柱 + 冠球，桥头 ±8 m 内不放）。
   - Place B：城墙梯形截面沿 y 挤出（底 34 / 顶 4 / 高 8.7），每百步（≈ 150 m，本站范围内落 0–1 个）马面；水门缺口（y −11…11）+ 闸门薄板吊起态（z 6…8）+ 水门楼体块；两岸旱门台 + 门洞 + 单层歇山楼体块 + 马道斜坡；拐子城夹岸墙；护龙河水面（与汴河交汇处直接合并水面，⚠️）；过壕木桥板；牙道榆柳 proxy。
   - Place C：州桥桥面板（z=2.6）+ 桥下密排石柱（2 m 间距）+ 两侧石栏；四段石壁；御街街面；朱 / 黑杈子阵列（每 2 m 一根短柱）；两道御沟槽 + 岸树 proxy；两侧御廊柱廊（`BAY` 模数，柱 + 檐板）；阙楼体块；望火楼砖台 + 木亭；方井。
3. **摆白模**：按表 link 三个白模的 collection 实例（**不 append 网格副本**，一份几何多处实例，rule 4g §D）：方块 1 → `p8`；2 / 3 → `p9`（3 转 180°）；4–11、26、41 → `p10` 母网格，**逐实例**镜像（x 轴）/ 绕 Z ±2° / 等比 ±3% 微抖（种子固定 ＝ 方块号，重跑得同一座城）；38 → `p10a`。每个实例原点落 `Z_STREET`。
4. **精度分级**（rule 4g §E；表中「级」列）：A 级实例保留白模全部型面；B 级允许 decimate 到 ≤ 5k 面；C 级只放盒 / 柱 / 球；**D（镜头看不到）不建**——尤其 Place C 御街两侧 ±46 m 以外、Place A 房后 |y| > 30 的区域什么都不放。
5. **走廊 keep-out**（rule 4h §E）：一镜到底路径（`city_plan.md` §4 TOML 各关键帧位置）两侧各 2.5 m、机高 ±2 m 的管状走廊内**不得有任何几何**（桥面板与街面除外）；入城镜走廊（B：(30,18)→(−15,18)）同样处理。**小体量塞得进走廊之间，大体量只会被整块剔掉**——仓、正店留位这些大块离走廊 ≥ 10 m。
6. **ID 色约定**：本 blend 的**布局层**对象纯灰模、零材质、零灯光（rule 4g §G：建筑形状必须由 previz 传递，不上色）；长相只由步 8 的 look pass 加（divergence #19），previz mp4 用 workbench `color_type=OBJECT` 渲，不吃这些材质。ID 色只在 shot previz 的人物 proxy 上出现，且 prompt 里必须**正反向成对声明**——正向：「`角色索引: previz 视频中的纯色人形为身份标记，非服装、非灯光。绿色标记 = @林问，蓝色标记 = @李十六 …。最终画面中不得出现这些标记色`」；反向追加：「`绿色衣服、蓝色衣服、纯色人形、色块人物、荧光色服装、参考视频的标记色出现在画面中、发光的人`」。本 blend 不写这两句，写在每镜 prompt 里；这里只约定**建筑永远不上色**。
7. **写盘**：`_blender/bianjing.blend`（gitignore、走 R2）。**previz 脚本绝不写回这份文件**——每镜先 copy 到 `shots/shotNN/previz/shotNN_previz.blend` 再动（rule 4h §A）。
8. **写实化（look pass，divergence #19，2026-09-15 follow-up 005）**：builder 跑完 QC 后默认调 `tools/look_bianjing.py` 的 `dress()` 再存一次（`--no-look` 只出灰模；也可单独对现有 blend 跑 `blender -b bianjing.blend --python tools/look_bianjing.py -- --save`）。它只加长相、不动布局：材质颜色从 `bg*-1.png` 锚点图采样、纹理细节来自 `_blender/textures/polyhaven/`（`python tools/polyhaven_fetch.py` 拉取，全部 pack 进 blend，拷到 shot 目录不丢图）；`G_BLOCKS` / 郊外单元盒 → 宋式民居 GN 实例（`LOOK_houses`）、柳树球 → 垂柳实例（`LOOK_trees`）、p8 / p9 / p10 替身集合里加细模、歇山体块 → 曲面屋顶 + 斗拱（`LOOK_up_*`）、城楼盒 → 木构城楼。被替换的布局网格 hide_render 保留，QC 与 previz 探针照旧只看布局。校验图：`--stills all` 出 `_blender/look_*.png`（机位表在脚本 `VIEWS`）。

---

## 5. 校验产物（按需重出，不入 git、不进参考位；平面图与灰模透视各抓各的，rule 4h §E）

```bash
S="ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/_blender"
# 相机坐标 ＝ W11 [[place_anchor]] 锚点 ＋ Rz(转角)·Place 局部坐标（下列数值由该公式算出；锚点改了就重算）

# 5.1 全城平面图 —— 查三圈城墙、Place 位置、Place 互不重叠（2026-09-14 起工具已自带远裁剪修正）
blender -b --factory-startup --python tools/render_scene_plan.py -- "$S/bianjing.blend" "$S/plan.png" 2048

# 5.2 Place A / B / C 平面图（框世界包围盒；Place 本身是斜的）
blender -b --factory-startup --python tools/render_scene_plan.py -- "$S/bianjing.blend" "$S/plan_A.png" 2048 "6198,6362,-4837,-4701"
blender -b --factory-startup --python tools/render_scene_plan.py -- "$S/bianjing.blend" "$S/plan_B.png" 2048 "2719,2833,-2799,-2693"
blender -b --factory-startup --python tools/render_scene_plan.py -- "$S/bianjing.blend" "$S/plan_C.png" 2048 "-55,59,-84,124"

# 5.3 一镜到底起幅（局部 (3,−17,2.4) → (0.5,−8,4.6)）
blender -b --factory-startup --python tools/render_scene_view.py -- "$S/bianjing.blend" "$S/check_A_t00_桥头.png" "6274.10,-4785.22,2.4" "6276.43,-4776.18,4.6" 24 1600

# 5.4 拱顶东望（局部 (2.4,0,6.8) → (25,2,3)）
blender -b --factory-startup --python tools/render_scene_view.py -- "$S/bianjing.blend" "$S/check_A_t15_拱顶东望.png" "6282.08,-4770.20,6.8" "6302.65,-4779.77,3" 24 1600

# 5.5 脚店门口（局部 (−7,15.5,2.9) → (−11,19.5,3.2)）
blender -b --factory-startup --python tools/render_scene_view.py -- "$S/bianjing.blend" "$S/check_A_t26_脚店门口.png" "6281.69,-4752.08,2.9" "6280.22,-4746.61,3.2" 24 1600

# 5.6 Place B 入城起幅（局部 (30,18,3.2) → (0,16,4)）
blender -b --factory-startup --python tools/render_scene_view.py -- "$S/bianjing.blend" "$S/check_B_入城.png" "2808.60,-2733.31,3.2" "2778.70,-2730.23,4" 24 1600

# 5.7 Place C 州桥北望（局部 (0,−6,4.5) → (0,60,3)）
blender -b --factory-startup --python tools/render_scene_view.py -- "$S/bianjing.blend" "$S/check_C_州桥北望.png" "-0.58,-5.97,4.5" "5.75,59.72,3" 35 1600

# 5.8 全城层斜俯（WP3 三圈城墙 / WP2 东水门接缝）—— ⚠️ render_scene_view.py 仍用相机默认远裁剪 1000 m，
#     几公里外的机位要先抬 clip_end（本次用 render_init 处理器包一层跑，工具本身待修）
#     check_G_WP3_三城全景.png："4800,-6500,3802" → "-100,600,2" 24 mm；check_G_WP2_东水门接缝.png："5200,-4300,152" → "2776,-2746,10" 24 mm
```

---

## 6. 验收清单（builder 每次落地都过一遍；不过的先改脚本）

| # | 检查项（可证伪） | 不过的样子 |
|---|---|---|
| 1 ✅ | `bianjing.blend` 由 `build_bianjing.py` 一条命令从零生成，删掉重跑逐值复现 §1 基线 | 手改过的 blend、补丁脚本、重跑结果漂 |
| 2 ✅ | 三块 Place 世界偏移正确、互不重叠 | Place 之间几何搭在一起 |
| 3 ✅替身 | 方块 1 白模拱顶桥面 z=5.6 ± 0.1，坡道脚落在 y=±18、z=2 | 桥悬空 / 埋进街面 / 桥两端与街错层 |
| 4 ✅替身 | 方块 2 与坡道脚净距 ≥ 6 m，门口 (−11, 19) 可从桥尾一眼看到 | 脚店挡住坡道、或远到看不见欢门 |
| 5 ✅ | 沿河民居实例逐个微抖（镜像 / ±2° / ±3%），种子固定 | 八栋一模一样、或每次重跑排布变了 |
| 6 ✅ | 一镜到底走廊内零几何（桥面 / 街面除外） | 柳树 / 表木 / 席棚体块伸进走廊 |
| 7 ✅ | 全部对象零材质、零灯光、灰模 | 白模自带贴图残留、有色块 |
| 8 ✅ | `shot 层道具` 行没有被建进 blend | 船、席棚摊、太平车出现在场景层 |
| 9 ✅ | D 级区域为空（御街 ±46 m 外、房后 \|y\| > 30） | 为「好看」多建了远景 |
| 10 ◐ | 5.3–5.7 五张灰模透视里，锚点图能对上的体量（桥低而长、欢门高过屋脊、三栋低高低）都对上 | 比例与锚点图不符——先改脚本 / 白模，不改锚点图 |
| 11 ✅替身 | `plan_A.png` 上房子的进深线与街边平行、后墙成直线 | 房子歪斜、前后错位 |
| 12 ✅ | 表中每个 ⚠️ 数值在脚本里有注释指回 fact_id | 数值来源不可追 |

> **2026-09-14 B_city 验收记录**：1–9、11、12 过（3 / 4 / 11 是在替身上过的，白模到位后重跑复核）。10 只对上了卡片形体规格（`check_A_桥侧立面.png`：桥低而长、拱下通透、欢门骨架高过邻屋屋脊；`check_A_t26`：三栋低高低 + 披檐），锚点图 `bg1-1` / `p8-1` / `p9-1` / `p10-1` 未出，出图后再对照。5.1 原命令出**纯白图**：`render_scene_plan.py` 把正交相机放在 包围盒顶 + 跨度 ≈ 1143 m，超过新建相机默认远裁剪 1000 m（世界跨 1072 m）——本次用不改工具的包装脚本在 render_init 时抬高 clip_end 出图；工具本身待修（非本目录）。另出补充校验图 `plan_B.png` / `plan_C.png` / `check_A_桥侧立面.png` / `check_B_鸟瞰.png` / `check_C_鸟瞰.png`（顶视平面图里平顶体块与地面同灰，看不出 B / C 的判断建法）。三张一镜到底透视暴露的是**机位草案**问题、不是几何问题，见 §9 新增待办。

> **2026-09-14 B_city phase 2a 复验（W11 真实锚点）**：三块 Place 按 W11 `[[place_anchor]]` 落位后，1–9、11、12 在 Place 局部坐标里逐项重跑全过（数值与 phase 1 一致，§1 表）；新增「全城层在 Place 足迹内零侵入」一项亦过；10 仍只对上卡片形体规格。5.1–5.7 按 §5 新坐标重渲并逐张看过。全城层斜俯与 S 档航拍静帧另见 `shots/shot01|shot02|shot35/frames_check/`。

---

## 7. `tools/build_bianjing.py` 待建接口（只定契约，不写实现）

- **调用**：`blender -b --factory-startup --python tools/build_bianjing.py -- [<out.blend>] [--qc-only] [--place A|B|C]`；不传 `out` 用默认路径；`--qc-only` 只读现有 blend 出 §1 表；`--place` 只重建一块（其余从表读但不生成，便于快速迭代）。
- **唯一输入**：`scenes/bianjing/_blender/city_plan.md`。解析规则：
  1. 只读 `## 2. 要素表` 下以 `### Place X` 开头的三段，每段一张 markdown 表；表头固定八列 `方块 | 要素 | 主体 / 建法 | 局部中心 · 朝向 | 尺寸 | 级 | 依据 | ⚠️`。
  2. `方块` 列：去掉加粗符号，允许「4 5 6」多号一行 → 展开成多条记录，与「局部中心」列里以 `/` 分隔的多个坐标一一对应。
  3. `主体 / 建法` 列：以反引号包住的 `p8` / `p9` / `p10` / `p10a` 表示白模实例（含「绕 Z 转 180°」时朝向 +180）；含「脚本」走脚本生成器（按「要素」名分派：河道 / 土坡 / 街 / 城墙 / 旱门 / 拐子城 / 护龙河 / 木桥 / 杈子 / 御沟 / 御廊 / 阙楼 / 望火楼 / 井 / 表木 / 柳 / 仓 / 码头 / 州桥 / 石壁 各一个函数）；含「shot 层道具」**跳过**；含「留位」放 `_PLACEHOLDER` 盒。
  4. `局部中心 · 朝向` 列：`(x, y)` 取局部坐标；「门朝南 / 北 / 东 / 西」映射 0 / 180 / 90 / −90；「轴 N–S」「墙线 N–S」等给线状要素方向。
  5. `尺寸` 列：只解析 `a × b` / `a × b × c` 与 `z=…`；其余当注释。
  6. `级` 列：A / B / C / `—`；决定 decimate 与替身策略（§4 步 4）。
  7. 解析失败**直接 raise**、不猜（同 previz `SCHEMA` 的纪律）——表是契约，不是提示。
- **常量**：§3 全部常量在脚本顶部集中声明，每个带注释指回 `city_plan.md` 与 fact_id。
- **输出**：`bianjing.blend` + stdout 的 §1 表（collection / 物件数 / 包围盒 / 走廊检查结果）；`--qc-only` 时退出码 ＝ 走廊检查是否通过。
- **禁止**：读 `city_plan.png`（图只给人看）；在布局代码里给对象上材质（长相只由 §4 步 8 的 look pass 加，带 `look` 标记）；写回 `props/*/whitemodel/*.blend`；生成 mp4。

---

## 8. 下游

| 谁 | 怎么用 |
|---|---|
| `shots/shotNN/previz/`（一镜到底） | `SCENE_MASTER` 指向本 blend；先 copy 再跑 `shotNN_previz.py`（S 档，读 `previz_config.toml` 的 `[[机位路径]]`，草案见 `city_plan.md` §4） |
| 其余全部镜次 | 同一份 blend，各自 previz 从它渲——**一致性来自「只有一份几何」**（rule 4g §D） |
| Seedance 一镜到底 | previz mp4 上传作运动 / 几何参考（divergence #10）；`参考:` 行写 `` `本镜运动参考(previz视频)=>@` ``、`` `bg0_汴京全城/bg0-1.png(世界锚点·世界基调)=>@` ``、`` `林问=>@` `` |

## 9. 待办

- [ ] 三个白模落地（各卡 Prompt 5）→ 本文件 §2 打勾
- [x] `tools/build_bianjing.py` 按 §7 落地 → 第一次跑完把实测值填进 §1 表（2026-09-14 B_city：全替身版；两层架构——全城体块层 `G` 为 stub，等 `0_research/parts/w11_city_layout.md` 的米制坐标表）
- [x] 5.1–5.7 七张校验图人眼过一遍 → §6 逐条打勾 → 更新 `city_plan.md` §0（2026-09-14：§6 除 #10 外全过；5.1 原命令出白图，见 §6 注）
- [ ] 阶段 5 落镜号前修 `city_plan.md` §4 一镜到底机位草案：t=0 起幅在桥面上，看不到拱、南侧表木在机后、北侧表木被拱顶挡住；t=15 机位 z 6.8 只比栏杆顶高 0.1 m、离东栏 1.4 m，栏杆糊满画面（rule 4h §E 同款坑）——机位移向桥轴或抬到栏杆顶 +0.5 m 以上；t=26 焦距 24 mm 距门口 5.7 m，欢门顶与屋脊出画
- [x] 全城层 G 按 `0_research/parts/w11_city_layout.md` §2.8 落地；三块 Place 挪到 W11 真实锚点（2026-09-14 phase 2a，§1 表）
- [x] S 档航拍 previz：`shots/shot01|shot02|shot35/`（`shotNN_previz.py` + `previz_config.toml` + `.blend` + `.mp4`；机位取相机审查 R3-01 / R3-02，shot35 起点 Place B 客店、终点 W11 WP3）
- [ ] W11 §2.8 同步 R3 修正：WP2 → [5760, −4470, 150]；删 WP4；WP5 → [30, 400, 50] / look [103, 1140, 25]；WP6 → xy [90, 1000]（研究件不在本工作者边界内，修正值暂只写在 shot TOML）
- [x] `tools/render_scene_view.py` 裁剪面随场景尺度走（2026-09-14 phase 2b：远裁剪取相机到场景包围盒最远角，近裁剪按离看点距离 / 离地高度放大，贴地近景仍 0.1 m）
- [x] phase 2b 细节 Place D 宣德楼内外 / E 汴河码头 / F 开封府 / H 相国寺 / I 桑家瓦子 / J 南薰门外踏青路落地（`city_plan.md` §2 新表；锚点只从 W11 条目推出，见 `DERIVED_ANCHORS`）；护龙河与御街宽改取 W11（判断见 `city_plan.md` §0）
- [x] 套景 `tools/build_sk1_sets.py` → `_blender/sets/{名}.blend`：客店房间 / 粥饭摊 / 饮子摊 / 夜市食摊（含包子摊、羊白肠摊变体）/ 坊巷街口 / 赵太丞家 / 园林 / 正店阁子 / 遗址坑
- [ ] shot01 / shot02 / shot35 的 `.blend` 与 `.mp4` 早于 phase 2b 的 Place B 护龙河外移与 Place D（协调者指示不重渲；shot02 末段看得见宣德楼、shot35 起点在 Place B）
- [ ] `bg1-1` 锚点图出图后，用 5.4 与之对照：体量对不上**改脚本**，不改锚点图
- [ ] 阶段 5 分配镜号后把 `shotNN` 落实、TOML `t` 与 `动作:` 对齐

### 9.1 phase 2b 白模动画进度（每渲完一镜追加一行；重启时从最后一行往下接）

档：A ＝ 通用引擎 `tools/previz/build_previz.py` + `previz_config.toml`；S ＝ `shotNN_previz.py` → `tools/previz_sk1.py` + `previz_config.toml`（镜内切镜 / 变焦 / 跟拍 / 城景套景混切的 A 档镜升 S，判断见 `city_plan.md` §10）。时长一律 ffprobe 实测；checked ＝ `frames_check/` 静帧与拼图人眼看过。

运行库修正（`tools/previz_sk1.py`，2026-09-14 渲染途中发现，此前渲过的 S 档镜一律重渲，§9.1 旧行以新行为准）：
① 地面探针起点不低于本系街面（从跳板掉到水面后再也爬不回街面，人一路埋在地里走）；
② 显隐关键帧在切换前一帧补旧状态键（布尔通道也按贝塞尔插值，隐藏会提前好几秒）；
③ 关节人头上加鼻锥（头是光球，转脸看镜头与后脑对镜头渲出来一样，走位表「看谁」读不出）；
④ 建场日志逐段逐人打印 `CAMFIG`（离地高 / 占画高 / 是否在画内 / 是否显示），出片前先机检；
⑤ 探针打到水面 / 河床时从街面 +4 m 再打一次、只认朝上的面（虹桥拱顶桥面比街面高 2.7 m，从街面 +1.6 m 往下打会穿过桥面，
   站在桥上的人被放到桥下水面上——shot04 / shot26 的桥上行人、shot27 的桥上剪影）。

shot md 复核：配置按 mtime 1789363838 那版写（`动作:` + 「林问开口与视线时间表」）；渲染途中 33 份 md 又被重建一次（mtime 1789395057），逐字段比对 `duration / 镜头 / 分镜 / 时长 / 景别档 / 动作 / 视线表`，只有 shot26 浪头「浑黄 → 泛白」、shot34 天光「灰白 → 清冷蓝色」两处措辞，不涉及时刻、走位与机位，配置不改。

| shot | 档 | 场景来源 | 文件 | 时长 | checked |
|---|---|---|---|---|---|
| shot03 | A | bianjing.blend · Place A 南桥头 | `previz_config.toml` → `shot03_previz.mp4` 1280×720 | 700 帧 / 28.000 s | ✓ 2026-09-14（近景胸口以上、21–28 s 后拉；背后桥坡人流） |
| shot04 | S | bianjing.blend · Place A 虹桥桥面一镜到底 → 十千脚店门口 | `shot04_previz.py` + `previz_config.toml` → `shot04_previz.mp4` 1920×1080 | 700 帧 / 28.000 s | ✓ 2026-09-14（第二版：低角度侧跟全身上坡；12–16 挑担与伞从镜头前极近处掠过、低头钻过；16–20 机位抢到西栏内侧她正前方，扶栏、抬眼看北桥头木杆；20–26 回到左侧跟到桥尾；26–28 仰摇到三层欢门、她在画面下缘。第一版机位 16 s 穿过人体，已改） |
| shot04 | S | bianjing.blend · Place A 虹桥桥面一镜到底 → 十千脚店门口 | `shot04_previz.py` + `previz_config.toml` → `shot04_previz.mp4` 1920×1080 | 700 帧 / 28.000 s | ✓ 2026-09-14 第三版（运行库修正后重渲：桥上行人贴桥面 z 4.7–5.6、鼻锥读得出视线；走位与第二版一致） |
| shot06 | S | bianjing.blend · Place B 城外南岸高处 → 北旱门门洞 | `shot06_previz.py` + `previz_config.toml` → `shot06_previz.mp4` 1920×1080 | 650 帧 / 26.000 s | ✓ 2026-09-14（0–8 水门与两岸旱门远眺、城台剪影；8–26 门洞纵深：骡驴 / 太平车擦身、捂耳、骆驼穿门；20 s 一名路人从近镜左侧掠过，可接受） |
| shot18 | S | bianjing.blend · Place D 宣德门门扇 → 楼前广场 140 m → 她身后低位 | `shot18_previz.py` + `previz_config.toml` → `shot18_previz.mp4` 1920×1080 | 650 帧 / 26.000 s | ✓ 2026-09-14（门扇门钉特写；大远景五门洞墩台 + 门楼 + 朵楼 + 阙亭全入画、她自画右下走入；过肩仰拍 17–26 s 上摇到正脊，她侧过半张脸） |
| shot26 | S | bianjing.blend · Place A 南岸水边 → 纲船船头 | `shot26_previz.py` + `previz_config.toml` → `shot26_previz.mp4` 1920×1080 | 650 帧 / 26.000 s | ✓ 2026-09-14（第二版：机位移出柳树行；桅杆转轴抬到船篷顶，放倒后落在船篷上；20–26 s 拱底扫过画面上方） |
| shot01 / shot02 | S | bianjing.blend（写实化后，follow-up 005–006）重新拷贝 | `shotNN_previz.py` + `previz_config.toml`（新增水手 / 人群）→ `shotNN_previz.blend`；Cycles 校验帧 `shotNN/look/` | 750 帧 / 30.000 s（mp4 未重渲） | 待看 2026-09-15 15:05:39 |

### 9.2 取景对账：`景别档` ↔ 白模实际取景（2026-09-15 第一次逐镜对账）

**为什么要对**：`景别档: {起幅景别}{人占画高} → {落幅景别}{人占画高}` 是排镜阶段的第一约束（切口判定 M3 / 机检 K31 都拿它当输入），
而 S 档机位是逐镜手写坐标——两边此前从未对过账。白模是喂给 Seedance 的构图与运动参考，取景错了等于没给参考。

**怎么对**：`tools/previz_sk1.py` 渲完把每个机位关键帧的「人占画高 / 在不在画内」写进同目录
`shotNN_previz_report.txt`（与产物同寿，不放会被清掉的构建日志）；`tools/previz_frame_fix.py` 读它与 shot md 比对，
按 `人占画高 ∝ 焦距 / 距离` 反解（室内退距 ≤1.8 倍、室外 ≤2.5 倍，焦距夹 20–120 mm）。

**第一次结果（29 个 S 档镜）**：只有 3 个镜两端都落在 spec 的 ±40% 内。典型偏差——

| shot | spec 起→落 | 实测 起→落 | 性质 |
|---|---|---|---|
| shot21 | 0.20→0.15 | 3.65→0.19 | 起幅她几乎贴在镜头上（18 倍） |
| shot30 | 0.35→2.00 | 0.38→15.21 | 落幅是包子微距，人不是主体（物件特写档） |
| shot34 | 0.90→0.75 | 2.82→2.37 | 两端都只剩脸，人被裁出画 |
| shot08 | 0.35→0.75 | 0.82→2.60 | 落幅只剩脸 |
| shot04 | 0.20→0.30 | 0.85→0.56 | 起幅该是远景，实测近景 |
| shot06 | 0.10→0.50 | 0.02→0.69 | 起幅她太小（人在画里，未裁） |

**处置（2026-09-15）**：只修「人被裁出画」的 6 镜——shot07 / 08 / 28 / 29 / 31 / 34（改 `焦距` + `位置`，改的是 TOML，rule 4h ②）。
其余偏紧偏松但人还在画里的、以及物件特写档的，**只报不改**：那是 spec 与机位设计谁对的判断题，交用户定。
典型是客店房间——4.2 m 的屋子装不下「50 mm ＋ 近景 0.80」（需要 5.4 m 机距），要么改 `景别档`（连带重算切口比值），
要么改走位让她离镜头更近，要么认下更广的镜头。复核命令：

```
python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1            # 只报告
python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1 --apply    # 修「被裁出画」的
```

**事故与处置（同日）**：批渲进行中给运行库加落盘报告，字符串换行没转义 → 之后 **17 镜全部 3 秒内 SyntaxError 失败**
（队列不会停，一路把剩下的镜刷成 FAIL）。运行库已修、`py_compile` 过；失败镜与改过配置的镜按
`scratchpad/stale_previz.py`（mp4 vs config vs 运行库行为截止点）算出的陈旧表重渲。教训进 `ai_video.md` 4h §J / §K。

**收尾（2026-09-16 01:00–03:00，四轮渲染后）**：

| 指标 | 对账前 | 现在 |
|---|---|---|
| 两端都落在 spec ±40% 内的镜 | 3 / 29 | 6 / 24（有量测报告的） |
| 单端合格 | — | 29 / 48 |
| 按白模实际取景仍成立的硬切对 | 13 / 22 | 11 / 19（按 spec 全部 19 对成立） |

修成了的：shot07 落 1.52→0.79（spec 0.80）· shot08 落 2.60→0.78（0.75）· shot13 落 1.44→0.55（0.55）·
shot15 起 1.49→0.22（0.20）· shot16 落 1.82→0.77（0.75）· shot22 落 1.97→0.86（0.80）· shot28 落 1.28→0.49（0.50）·
shot29 起 4.44→1.23（1.20）· shot31 落 2.12→0.93（0.75）· shot34 2.82/2.37→0.87/0.78（0.90/0.75）· shot17 起 1.31→0.40（0.30）。

**两个实测坑（都栽过）**：
① **室内往后退会退到墙外**——shot31 落幅按 1.8 倍退距后，后半段整屏灰（相机在阁子墙外看墙背面）。
   室内只许改焦距：shot31 最终 50 mm → 22 mm、机位不动，人占画高 0.93、画面正常。
② **人离「看向点」很远的镜，沿视线缩放机位会把 frac 放大或缩小到失控**——shot18 落幅一轮 2.93 → 0.01 → 9.98
   来回震荡（工具假设人就在看向点上，这类镜不成立）。已加阻尼（一次只走 70%），但 shot18 / shot21 / shot27 三镜
   最终**回滚到作者原值**、标为「人工定框」：机器改不动的，不如留着原样让人看图定。

**留给用户的判断题**（`python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1` 随时可复现）：
- 一端偏离但人仍在画里的 14 镜（远景她太小或近景她太紧）：shot04 / 06 / 07 / 08 / 10 / 14 / 16 / 20 / 22 / 24 / 25 / 31 / 33 / 36 的某一端；
- 物件特写档（人不是主体，`景别档` 的数不适用）：shot18 起、shot23 起、shot30 落；
- 人工定框三镜：shot18 落、shot21 起、shot27 起；
- 按量测仍不合格的 8 对切口：shot07→08、12→13、16→17、19→20、21→22、24→25、27→28、33→34——
  要么把机位改到 spec（室内可能做不到），要么改 `景别档` 并重算这几对的切口比值。

