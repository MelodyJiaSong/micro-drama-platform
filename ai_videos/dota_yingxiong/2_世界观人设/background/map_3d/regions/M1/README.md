# M1 近卫中路一塔 · 区域精修（follow-up 298，Claude 接手）

**标准 A（用户 2026-10-31 定）**：3D 地图作 AI 出片的场景参考（开场图／峰值图底图、机位与空间关系），模型做到形体、颜色分区、比例、位置正确即可；真实感由出片模型补。不按“实拍级精模”审。

## 当前工作版本

`../../assembly_working_v022_lod_v004_m1_v005.blend`（源：Codex 2026-10-31 上午保存的 `assembly_working_v022_lod_v004.blend`，未改动）

| 版本 | 改动 | 脚本 |
|---|---|---|
| m1_v001 | 兵道 Paving 层：白砂岩石块 → 夯土（近卫土黄／天灾黑褐，按 Blight 混）＋踩痕噪声 | `0_research/map_regions/blender/patch_lane_surface.py` |
| m1_v002 | bg16 近卫塔改指 `lod_libraries/m1_recolor_v001/bg16/`：叶→橄榄绿、木→灰褐、有机物金属度 0 | `recolor_asset_library.py`、`remap_asset_libraries.py` |
| m1_v003 | m2 改指 `m1_recolor_v001/m2/`（侧背褪色米白→深棕羽毛，正面原色不动）；m3 改指 `m1_recolor_v002/m3/`（按明度分位数分区：亮部鎏金金属、暗部深棕木） | 同上 |
| m1_v004 | demo 编成首版：英雄在塔旁被塔挡住，弃用 | `stage_demo_wave.py` |
| m1_v005 | demo 编成（集合 `DEMO_M1`）：灰色英雄占位（1.8 m，面朝东北，路上 t=16）＋天灾常规波 4 食尸鬼（t=27–30）＋2 亡灵法师（t=34），面朝西南；近卫友军沿用原塔前兵线。站位见 `*_m1_v005_demo_stage.json` | `stage_demo_wave.py` |

**轻量查看版**（follow-up 299）：`../../assembly_working_v022_lod_v004_m1_v005_light.blend`，只在界面里看布局用（后台打开 52 s → 16 s；7200 万面 → 675 万面；贴图上限 1024）。库在 `lod_libraries/light_v001/`，脚本 `make_light_map.py`。近景树叶略稀、偏暗；出检查图和精修仍用上面的完整版。

检查图：`regions/M1/*_M1_{demo_side,side_SE,low_SE,wide_SE,lane_SW}.png`，`render_region_eye.py` 只读出图；太阳方向按机位临时设定（侧拍顺光、顺路机位右后方光、demo 侧拍东偏南，见 bg4 卡与 battlefield §4.2），不写回地图。

**demo 出片参考首选**：`assembly_working_v022_lod_v004_m1_v005_M1_demo_side.png`（bg4-2 侧拍轴：英雄画左、天灾从画右来）。

## M1 涉及资产（总装实际摆放）

bg16 近卫塔；兵线 m1 树人 ×3、m2 利爪德鲁伊、m3 投刃车；demo 对面天灾兵线 m4 食尸鬼、m5 死灵法师、m6 绞肉车（M1 当前未摆，按 battlefield §4.2 demo 编成另摆）。

## 已查明

- 树人“黑柱”不是模型坏：贴图齐、高 1.92 m（设定 1.9 m）；深色树皮＋暗紫叶是设计，原场景太阳在西北，东南侧拍全逆光。
- 7 个模型实测高度均与 `scale_table.md` 一致。
- bg16 库内网格记 1 m、实际渲染约 9 m；检查取景须用求值网格，不能用 bound_box。

## 待做

1. bg16 树冠顶 3–4 片悬空碎叶；强光下木头偏亮。
2. m2 皮肤仍偏白（设定淡紫）、背发未恢复绿色；m6 车尾复制车头、横骨悬空（demo 常规波不带绞肉车，暂缓）。m4、m5 按标准 A 判可用。
3. demo 正面（bg4-1）与反打（bg4-3）机位；英雄占位替换为具体英雄时按 `scale_table.md` 改高度。
4. 塔前友军树人目前在英雄身后约 15 m，需要时可前移入画。
